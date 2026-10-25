"""Deep SQL retrieval with explicit FK joins; matches are not deletion verdicts."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from collections import defaultdict
from contextlib import closing
from pathlib import Path

from evidence_inspector import (EvidenceInspector, load_sql_snapshot, parse_time,
                                quote_identifier, table_names)


class SQLiteDeepInspector(EvidenceInspector):
    @staticmethod
    def compute_email_hashes(email):
        """Candidate encodings for diagnosis, not assumed identity ground truth."""
        if not isinstance(email, str) or not email.strip():
            return []
        raw = email.strip().casefold().encode('utf-8')
        return [hashlib.sha256(raw).hexdigest(), hashlib.md5(raw).hexdigest()]

    @staticmethod
    def foreign_key_rows(connection):
        """Execute joins declared by PRAGMA, including composite foreign keys.

        Returned rows retain both sides and the actual join columns. No relation
        is inferred from similarly named columns or a shared numeric suffix.
        """
        tables = table_names(connection)
        results = []
        for child in tables:
            groups = defaultdict(list)
            for row in connection.execute('PRAGMA foreign_key_list(' + quote_identifier(child) + ')'):
                groups[row['id']].append(dict(row))
            for key, parts in groups.items():
                parts.sort(key=lambda p: p['seq'])
                parent = parts[0]['table']
                if parent not in tables:
                    raise ValueError(f'Missing FK parent table {parent}')
                primary = sorted((dict(col) for col in connection.execute(
                    'PRAGMA table_info(' + quote_identifier(parent) + ')') if col['pk']),
                    key=lambda col: col['pk'])
                pairs = []
                for part in parts:
                    target = part['to']
                    if not target:
                        if part['seq'] >= len(primary):
                            raise ValueError(f'Cannot resolve implicit FK for {child}')
                        target = primary[part['seq']]['name']
                    pairs.append((part['from'], target))
                child_columns = [col['name'] for col in connection.execute(
                    'PRAGMA table_info(' + quote_identifier(child) + ')')]
                parent_columns = [col['name'] for col in connection.execute(
                    'PRAGMA table_info(' + quote_identifier(parent) + ')')]
                fields = ['c.' + quote_identifier(col) for col in child_columns]
                fields += ['p.' + quote_identifier(col) for col in parent_columns]
                condition = ' AND '.join('c.' + quote_identifier(a) + '=p.' + quote_identifier(b)
                                         for a,b in pairs)
                query = ('SELECT ' + ','.join(fields) + ' FROM ' + quote_identifier(child)
                         + ' AS c JOIN ' + quote_identifier(parent) + ' AS p ON ' + condition)
                for row in connection.execute(query):
                    split = len(child_columns)
                    results.append({'child_table':child, 'parent_table':parent,
                                    'join_columns':pairs,
                                    'child':dict(zip(child_columns,tuple(row)[:split])),
                                    'parent':dict(zip(parent_columns,tuple(row)[split:]))})
        return results

    def deep_query_snapshot(self, sql_path, user_id, email, audit_at, *, identifiers=(),
                            include_md5=False):
        """Query one manifest-listed, eligible capture and its declared FK links."""
        path = Path(sql_path).resolve()
        with (self.dataset_dir/'evidence_files.csv').open(encoding='utf-8-sig',newline='') as stream:
            manifest = list(csv.DictReader(stream))
        matches = [m for m in manifest if (self.dataset_dir/m['file_path']).resolve()==path]
        if len(matches)!=1 or path.suffix.casefold()!='.sql' or not path.is_relative_to(self.dataset_dir):
            raise ValueError('Snapshot must have one SQL entry inside the dataset manifest')
        metadata = matches[0]
        cutoff = parse_time(audit_at)
        if parse_time(metadata['captured_at'])>cutoff:
            return []
        terms = {term.strip() for term in (user_id,email,*identifiers)
                 if isinstance(term,str) and term.strip()}
        if not terms:
            raise ValueError('At least one non-empty identifier is required')
        for address in list(terms):
            if '@' in address:
                hashes = self.compute_email_hashes(address)
                terms.update(hashes if include_md5 else hashes[:1])
        with closing(load_sql_snapshot(path)) as connection:
            direct = self.search_user_in_snapshot(connection,next(iter(terms)),
                additional_identifiers=sorted(terms),audit_at=audit_at)
            joins = self.foreign_key_rows(connection)
            scopes = {row['origin_system']:parse_time(row['captured_at']) for row in
                      connection.execute('SELECT * FROM snapshot_scope')} if 'snapshot_scope' in table_names(connection) else {}
        # Only traverse rows already admitted by the base time filter. Parent
        # identity rows can seed child rows without putting their PII into the
        # child's observed fields or interpreting a successful workflow as proof.
        def fingerprint(table, row):
            return table,json.dumps(row,sort_keys=True,ensure_ascii=False,default=str)
        matched = {}
        for hit in direct:
            record = {k:v for k,v in hit['data'].items() if k!='parsed_json'}
            matched[fingerprint(hit['table'],record)] = dict(hit, match_kind='DIRECT', join_path=[])
        def eligible_row(table,row):
            systems={'customer_profiles':'account_service','customer_search_documents':'search_service',
                     'customer_analytics_profiles':'analytics_platform','support_records':'support_platform',
                     'customer_exports':'export_service','connector_subscriptions':'integration_service',
                     'backup_restore_entries':'backup_service','security_audit_records':'security_service'}
            system=row.get('origin_system',systems.get(table))
            if system in scopes and scopes[system]>cutoff:
                return False
            return all(not row.get(k) or parse_time(row[k])<=cutoff
                       for k in ('updated_at','observed_at','captured_at'))
        changed = True
        while changed:
            changed = False
            for join in joins:
                if not eligible_row(join['child_table'],join['child']) or not eligible_row(join['parent_table'],join['parent']):
                    continue
                for source,target in (('parent','child'),('child','parent')):
                    source_key = fingerprint(join[source+'_table'],join[source])
                    target_key = fingerprint(join[target+'_table'],join[target])
                    if source_key not in matched or target_key in matched:
                        continue
                    anchor = matched[source_key]
                    edge = {k:join[k] for k in ('child_table','parent_table','join_columns')}
                    record = dict(join[target])
                    if 'record_json' in record:
                        record['parsed_json'] = json.loads(record['record_json'])
                    matched[target_key] = {'table':join[target+'_table'],'data':record,
                        'matched_identifiers':anchor['matched_identifiers'],
                        'match_kind':'DECLARED_FOREIGN_KEY', 'join_path':anchor['join_path']+[edge]}
                    changed = True
        result = []
        md5_candidates = {self.compute_email_hashes(a)[1] for a in (email,*identifiers)
                          if isinstance(a,str) and '@' in a}
        for key, hit in sorted(matched.items()):
            hit.update(file_id=metadata['file_id'],file=metadata['file_path'],
                       captured_at=metadata['captured_at'],policy_verdict=None)
            hit['unverified_md5_candidate'] = bool(set(hit['matched_identifiers']) & md5_candidates)
            result.append(hit)
        return result

    def search_all_databases(self, user_id, email, audit_at, *, identifiers=(),include_md5=False):
        with (self.dataset_dir/'evidence_files.csv').open(encoding='utf-8-sig',newline='') as stream:
            manifest = list(csv.DictReader(stream))
        results = {}
        for metadata in sorted(manifest,key=lambda m:(parse_time(m['captured_at']),m['file_id'])):
            if not metadata['file_path'].lower().endswith('.sql') or parse_time(metadata['captured_at'])>parse_time(audit_at):
                continue
            hits = self.deep_query_snapshot(self.dataset_dir/metadata['file_path'],user_id,email,
                audit_at,identifiers=identifiers,include_md5=include_md5)
            if hits:
                results[metadata['file_id']] = hits
        return results


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--dataset',type=Path)
    parser.add_argument('--user-id',default='')
    parser.add_argument('--email',default='')
    parser.add_argument('--identifier',action='append',default=[])
    parser.add_argument('--audit-at',required=True)
    parser.add_argument('--include-md5',action='store_true',help='Include explicitly unverified MD5 candidates for diagnosis')
    args=parser.parse_args()
    result=SQLiteDeepInspector(args.dataset).search_all_databases(args.user_id,args.email,
        args.audit_at,identifiers=args.identifier,include_md5=args.include_md5)
    print(json.dumps(result,ensure_ascii=False,indent=2))
