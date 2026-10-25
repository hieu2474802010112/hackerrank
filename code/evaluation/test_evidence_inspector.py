"""SQL retrieval regressions: cutoff, exact identity, replicas and load failures."""
import csv
import json
import sqlite3
import sys
import tempfile
import unittest
from contextlib import closing
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from evidence_inspector import EvidenceInspector, load_sql_snapshot


class EvidenceInspectorTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.inspector = EvidenceInspector(self.root)

    def tearDown(self):
        self.temp.cleanup()

    def snapshot(self, name, script):
        path = self.root / name
        path.write_text(script, encoding='utf-8')
        return path

    def test_exact_matches_nested_json_and_replica_provenance(self):
        path = self.snapshot('replicas.sql', '''
CREATE TABLE customer_data_primary (resource_id TEXT, record_json TEXT);
CREATE TABLE customer_data_replica (resource_id TEXT, record_json TEXT);
INSERT INTO customer_data_primary VALUES ('account_decoy','{"user_id":"user_050","email":"person05.jr@example.test"}');
INSERT INTO customer_data_replica VALUES ('account_real','{"identity":{"user_id":"user_05","email":"PERSON05@EXAMPLE.TEST"}}');
''')
        with closing(load_sql_snapshot(path)) as connection:
            rows = self.inspector.search_user_in_snapshot(connection, 'user_05',
                additional_identifiers=['person05@example.test'])
            self.assertEqual(len(rows), 1)
            self.assertEqual(rows[0]['table'], 'customer_data_replica')
            self.assertEqual(rows[0]['data']['parsed_json']['identity']['user_id'], 'user_05')
            self.assertEqual(rows[0]['matched_identifiers'], ['person05@example.test', 'user_05'])
            with self.assertRaises(sqlite3.OperationalError):
                connection.execute("DELETE FROM customer_data_replica")

    def test_manifest_cutoff_inclusive_and_unlisted_files_ignored(self):
        script = "CREATE TABLE profiles (email TEXT); INSERT INTO profiles VALUES ('subject@example.test');"
        self.snapshot('eligible.sql', script)
        self.snapshot('future.sql', 'invalid SQL that must not be opened')
        self.snapshot('unlisted.sql', script)
        with (self.root / 'evidence_files.csv').open('w', encoding='utf-8', newline='') as stream:
            writer = csv.writer(stream)
            writer.writerow(['file_id', 'file_path', 'origin', 'captured_at'])
            writer.writerow(['eligible', 'eligible.sql', 'test', '2026-09-15T12:00:00Z'])
            writer.writerow(['future', 'future.sql', 'test', '2026-09-16T00:00:00Z'])
        rows = self.inspector.audit_user_across_all_snapshots('', 'subject@example.test', '2026-09-15T19:00:00+07:00')
        self.assertEqual([r['file_id'] for r in rows], ['eligible'])
        self.assertEqual(rows[0]['captured_at'], '2026-09-15T12:00:00Z')

    def test_identifier_quoting_and_literal_wildcard(self):
        path = self.snapshot('quoted.sql', '''
CREATE TABLE "odd"" table" ("odd column" TEXT);
INSERT INTO "odd"" table" VALUES ('a%_@example.test'), ('alice@example.test');
''')
        with closing(load_sql_snapshot(path)) as connection:
            matches = self.inspector.search_user_in_snapshot(connection, 'a%_@example.test')
            self.assertEqual(len(matches), 1)
            self.assertEqual(matches[0]['table'], 'odd" table')

    def test_row_and_scope_future_timestamps_excluded(self):
        path = self.snapshot('scope.sql', '''
CREATE TABLE snapshot_scope (origin_system TEXT, captured_at TEXT);
INSERT INTO snapshot_scope VALUES ('account_service','2026-09-16T00:00:00Z');
CREATE TABLE customer_profiles (email TEXT, updated_at TEXT);
INSERT INTO customer_profiles VALUES ('subject@example.test','2026-09-01T00:00:00Z');
CREATE TABLE other_records (email TEXT, observed_at TEXT);
INSERT INTO other_records VALUES ('subject@example.test','2026-09-16T00:00:00Z');
''')
        with closing(load_sql_snapshot(path)) as connection:
            self.assertEqual(self.inspector.search_user_in_snapshot(connection,
                'subject@example.test', audit_at='2026-09-15T12:00:00Z'), [])

    def test_errors_are_not_silent_empty_results(self):
        with self.assertRaisesRegex(ValueError, 'Cannot load SQL snapshot'):
            load_sql_snapshot(self.snapshot('broken.sql', 'not valid SQL'))
        path = self.snapshot('broken_json.sql', "CREATE TABLE records (record_json TEXT); INSERT INTO records VALUES ('not JSON');")
        with closing(load_sql_snapshot(path)) as connection:
            with self.assertRaisesRegex(ValueError, 'Invalid record_json'):
                self.inspector.search_user_in_snapshot(connection, 'subject@example.test')
            with self.assertRaisesRegex(ValueError, 'non-empty identifier'):
                self.inspector.search_user_in_snapshot(connection, '')
        with self.assertRaisesRegex(ValueError, 'successfully loaded'):
            self.inspector.search_user_in_snapshot(None, 'subject@example.test')


if __name__ == '__main__':
    unittest.main()
