"""Inspect participant SQL snapshots. A match is presence, not a policy verdict."""
from __future__ import annotations

import argparse
import csv
import json
import re
import sqlite3
from contextlib import closing
from datetime import datetime, timezone
from pathlib import Path


def parse_time(value):
    timestamp = datetime.fromisoformat(str(value).replace('Z', '+00:00'))
    if timestamp.tzinfo is None:
        timestamp = timestamp.replace(tzinfo=timezone.utc)
    return timestamp.astimezone(timezone.utc)


def quote_identifier(name):
    return '"' + name.replace('"', '""') + '"'


def load_sql_snapshot(sql_filepath):
    """Return an isolated, read-only-after-loading connection; caller closes it.

    Invalid UTF-8 and SQL errors propagate with file context. They must never
    become an empty result that could be mistaken for successful deletion.
    """
    path = Path(sql_filepath)
    script = path.read_text(encoding='utf-8-sig')
    connection = sqlite3.connect(':memory:')
    connection.row_factory = sqlite3.Row
    try:
        connection.executescript(script)
        connection.execute('PRAGMA query_only = ON')
    except sqlite3.Error as exc:
        connection.close()
        raise ValueError(f'Cannot load SQL snapshot {path.name}: {exc}') from exc
    return connection


def table_names(connection):
    return [row[0] for row in connection.execute(
        "SELECT name FROM sqlite_master WHERE type = 'table' ORDER BY name"
    ) if not row[0].startswith('sqlite_')]


def text_matches(value, identifier):
    """Case-insensitive complete scalar or delimited token, never LIKE wildcards."""
    if not isinstance(value, str):
        return False
    text, target = value.strip().casefold(), identifier.strip().casefold()
    if re.fullmatch(r'\+[\d\s().-]+', target) and re.fullmatch(r'\+[\d\s().-]+', text):
        actual_digits = ''.join(c for c in text if c.isdigit())
        target_digits = ''.join(c for c in target if c.isdigit())
        if 7 <= len(target_digits) <= 15:
            return actual_digits == target_digits
    if text == target:
        return True
    # Email, hash and ID punctuation belong to the token. This excludes suffix
    # decoys and treats SQL wildcard characters in the search term literally.
    boundary = r'\w@.+%\-'
    return re.search(r'(?<![' + boundary + '])' + re.escape(target)
                     + r'(?![' + boundary + '])', text) is not None


def matching_identifiers(value, identifiers):
    if isinstance(value, dict):
        return set().union(*(matching_identifiers(v, identifiers)
                             for v in value.values()))
    if isinstance(value, list):
        return set().union(*(matching_identifiers(v, identifiers) for v in value))
    return {identifier for identifier in identifiers if text_matches(value, identifier)}


class EvidenceInspector:
    def __init__(self, dataset_dir=None):
        self.dataset_dir = Path(dataset_dir or Path(__file__).resolve().parents[1] / 'dataset').resolve()

    load_sql_snapshot = staticmethod(load_sql_snapshot)

    def search_user_in_snapshot(self, connection, identifier, *, additional_identifiers=(), audit_at=None):
        """Inspect flat fields and nested record_json, preserving table provenance.

        Optional cutoff checks reject explicit future scope/row timestamps. The
        collection scope time takes precedence over a last-write timestamp.
        An identifier that matches several fields still yields one row.
        """
        identifiers = {v.strip() for v in (identifier, *additional_identifiers)
                       if isinstance(v, str) and v.strip()}
        if not identifiers:
            raise ValueError('At least one non-empty identifier is required')
        if connection is None:
            raise ValueError('A successfully loaded snapshot connection is required')
        cutoff = parse_time(audit_at) if audit_at is not None else None
        tables = table_names(connection)
        scopes = {}
        if 'snapshot_scope' in tables:
            scopes = {r['origin_system']: parse_time(r['captured_at'])
                      for r in connection.execute('SELECT * FROM snapshot_scope')}
        systems = {
            'customer_profiles': 'account_service',
            'customer_search_documents': 'search_service',
            'customer_analytics_profiles': 'analytics_platform',
            'support_records': 'support_platform',
            'customer_exports': 'export_service',
            'connector_subscriptions': 'integration_service',
            'backup_restore_entries': 'backup_service',
            'security_audit_records': 'security_service',
        }
        matches = []
        for table in tables:
            if table == 'snapshot_scope':
                continue
            for row in connection.execute('SELECT * FROM ' + quote_identifier(table)):
                record = dict(row)
                parsed = None
                values = record
                if 'record_json' in record:
                    try:
                        parsed = json.loads(record['record_json'])
                    except (TypeError, json.JSONDecodeError) as exc:
                        raise ValueError(f'Invalid record_json in table {table}') from exc
                    values = {k: v for k, v in record.items() if k != 'record_json'}
                    values['parsed_json'] = parsed
                system = record.get('origin_system', systems.get(table))
                if cutoff is not None:
                    observed = scopes.get(system)
                    if observed is not None and observed > cutoff:
                        continue
                    for timestamp_key in ('observed_at', 'captured_at', 'updated_at'):
                        timestamp_value = record.get(timestamp_key)
                        if timestamp_value and parse_time(timestamp_value) > cutoff:
                            break
                    else:
                        timestamp_value = None
                    if timestamp_value:
                        continue
                found = matching_identifiers(values, identifiers)
                if found:
                    if parsed is not None:
                        record['parsed_json'] = parsed
                    matches.append({'table': table, 'data': record,
                                    'matched_identifiers': sorted(found)})
        return matches

    def audit_user_across_all_snapshots(self, user_id, email, audit_at_str, *, identifiers=()):
        """Return matching rows from manifest-listed SQL files available by cutoff.

        Empty results mean no matching SQL rows were found, not proof of absence.
        Historical identifiers may be supplied through identifiers. Final policy
        treatment and cross-format state reconstruction remain in AuditEngine.
        """
        cutoff = parse_time(audit_at_str)
        with (self.dataset_dir / 'evidence_files.csv').open(encoding='utf-8-sig', newline='') as stream:
            manifest = list(csv.DictReader(stream))
        terms = [v for v in (user_id, email, *identifiers) if isinstance(v, str) and v.strip()]
        if not terms:
            raise ValueError('At least one non-empty identifier is required')
        result = []
        for evidence in sorted(manifest, key=lambda item: (parse_time(item['captured_at']), item['file_id'])):
            if parse_time(evidence['captured_at']) > cutoff:
                continue
            path = (self.dataset_dir / evidence['file_path']).resolve()
            if not path.is_relative_to(self.dataset_dir):
                raise ValueError('Evidence path escapes dataset')
            if path.suffix.casefold() != '.sql':
                continue
            with closing(load_sql_snapshot(path)) as connection:
                matches = self.search_user_in_snapshot(connection, terms[0],
                    additional_identifiers=terms[1:], audit_at=audit_at_str)
            if matches:
                result.append({'file_id': evidence['file_id'], 'file': evidence['file_path'],
                               'origin': evidence['origin'], 'captured_at': evidence['captured_at'],
                               'matches': matches})
        return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--dataset', type=Path)
    parser.add_argument('--user-id', default='')
    parser.add_argument('--email', default='')
    parser.add_argument('--identifier', action='append', default=[])
    parser.add_argument('--audit-at', required=True)
    args = parser.parse_args()
    result = EvidenceInspector(args.dataset).audit_user_across_all_snapshots(
        args.user_id, args.email, args.audit_at, identifiers=args.identifier)
    print(json.dumps(result, ensure_ascii=False, indent=2))
