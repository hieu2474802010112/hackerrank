"""Deep-lookup tests use independent synthetic snapshots, never expected cases."""
import csv
import hashlib
import sys
import tempfile
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from sqlite_deep_query import SQLiteDeepInspector

T='2026-09-15T12:00:00Z'


class SQLiteDeepQueryTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.root=Path(self.temp.name)
        self.inspector=SQLiteDeepInspector(self.root)

    def tearDown(self):self.temp.cleanup()

    def fixture(self,script,captured=T):
        path=self.root/'snapshot.sql';path.write_text(script,encoding='utf-8')
        with (self.root/'evidence_files.csv').open('w',encoding='utf-8',newline='') as f:
            writer=csv.writer(f);writer.writerow(['file_id','file_path','origin','captured_at'])
            writer.writerow(['test_snapshot','snapshot.sql','test',captured])
        return path

    def test_nested_hash_is_retrieved_without_classifying_retained_record(self):
        digest=hashlib.sha256(b'person@example.test').hexdigest()
        path=self.fixture('CREATE TABLE records (resource_id TEXT,record_json TEXT);'
            +f'''INSERT INTO records VALUES ('audit_record_1','{{"identity":{{"email_hash":"{digest}"}}}}');''')
        rows=self.inspector.deep_query_snapshot(path,'','person@example.test',T)
        self.assertEqual(len(rows),1)
        self.assertEqual(rows[0]['file_id'],'test_snapshot')
        self.assertEqual(rows[0]['data']['parsed_json']['identity']['email_hash'],digest)
        self.assertIsNone(rows[0]['policy_verdict'])

    def test_declared_composite_join_uses_all_columns(self):
        path=self.fixture('''
CREATE TABLE identities (tenant TEXT,subject_key INTEGER,email TEXT,PRIMARY KEY(tenant,subject_key));
CREATE TABLE customer_profiles (resource_id TEXT,tenant TEXT,identity_key INTEGER,
FOREIGN KEY(tenant,identity_key) REFERENCES identities(tenant,subject_key));
INSERT INTO identities VALUES ('a',1,'person@example.test'),('b',1,'other@example.test');
INSERT INTO customer_profiles VALUES ('account_1','a',1),('account_2','b',1);
''')
        rows=self.inspector.deep_query_snapshot(path,'','person@example.test',T)
        children=[r for r in rows if r['table']=='customer_profiles']
        self.assertEqual([r['data']['resource_id'] for r in children],['account_1'])
        self.assertEqual(children[0]['match_kind'],'DECLARED_FOREIGN_KEY')
        self.assertEqual(len(children[0]['join_path'][0]['join_columns']),2)

    def test_matching_column_names_alone_do_not_create_join(self):
        path=self.fixture('''
CREATE TABLE identities (identity_id INTEGER,email TEXT);
CREATE TABLE customer_profiles (resource_id TEXT,identity_id INTEGER);
INSERT INTO identities VALUES (1,'person@example.test');
INSERT INTO customer_profiles VALUES ('account_1',1);
''')
        rows=self.inspector.deep_query_snapshot(path,'','person@example.test',T)
        self.assertEqual([r['table'] for r in rows],['identities'])

    def test_future_file_and_future_join_scope_are_excluded(self):
        path=self.fixture('not SQL','2026-09-16T00:00:00Z')
        self.assertEqual(self.inspector.deep_query_snapshot(path,'','person@example.test',T),[])
        path=self.fixture('''
CREATE TABLE snapshot_scope (origin_system TEXT,captured_at TEXT);
INSERT INTO snapshot_scope VALUES ('account_service','2026-09-16T00:00:00Z');
CREATE TABLE identities (id INTEGER PRIMARY KEY,email TEXT);
CREATE TABLE customer_profiles (resource_id TEXT,identity_id INTEGER REFERENCES identities(id));
INSERT INTO identities VALUES (1,'person@example.test');
INSERT INTO customer_profiles VALUES ('account_1',1);
''')
        rows=self.inspector.deep_query_snapshot(path,'','person@example.test',T)
        self.assertFalse(any(r['table']=='customer_profiles' for r in rows))

    def test_md5_requires_explicit_diagnostic_opt_in(self):
        digest=hashlib.md5(b'person@example.test').hexdigest()
        path=self.fixture(f"CREATE TABLE records (email_hash TEXT); INSERT INTO records VALUES ('{digest}');")
        self.assertEqual(self.inspector.deep_query_snapshot(path,'','person@example.test',T),[])
        rows=self.inspector.deep_query_snapshot(path,'','person@example.test',T,include_md5=True)
        self.assertTrue(rows[0]['unverified_md5_candidate'])
        self.assertIsNone(rows[0]['policy_verdict'])

    def test_international_phone_formatting_does_not_match_a_near_number(self):
        path=self.fixture('''CREATE TABLE support_records (resource_id TEXT,requester_phone TEXT);
INSERT INTO support_records VALUES ('support_1','+1 (234) 567-8901'),('support_2','+1 (234) 567-8902');''')
        rows=self.inspector.deep_query_snapshot(path,'','',T,identifiers=['+12345678901'])
        self.assertEqual([r['data']['resource_id'] for r in rows],['support_1'])


if __name__=='__main__':unittest.main()
