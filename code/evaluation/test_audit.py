"""Synthetic safety regressions, independent of public/hidden expected answers."""
import csv
import json
import hashlib
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from main import AuditEngine, authorizes_deletion, instant, run_audit

T='2026-09-15T12:00:00Z'


class AuditSafetyTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.root=Path(self.temp.name)
        self.csv('user_identities.csv',['user_id','name','email','phone','email_hash','updated_at'],[
            ['user_alpha','Test Subject','current@example.test','+1 234 567 8901','ab'*32,'2026-01-01T00:00:00Z']])
        self.csv('user_audit_log.csv',['audit_id','user_id','event_time','field_name','old_value','new_value'],[
            ['audit_alias','user_alpha','2026-02-01T00:00:00Z','email','previous@example.test','current@example.test']])
        self.csv('system_activity.csv',['activity_id','event_time','event_type','source_system','target_system','resource_id','reported_result','details'],[])
        self.csv('deletion_rules.csv',['rule_id','data_category','condition','required_action'],[
            ['r1','USER_PROFILE','Always','DELETE'],['r2','SEARCH_INDEX_ENTRY','Always','DELETE'],
            ['r3','ACCOUNT_TOMBSTONE','Only stable reference is allowed','REDACT'],
            ['r4','ANALYTICS_PROFILE','Still attributable','ANONYMIZE'],
            ['r5','SECURITY_AUDIT_LOG','Within retention','RETAIN']])
        self.manifest=[]
        self.request={'case_id':'synthetic','email':'current@example.test','audit_at':T,'requested_at':'2026-09-01T00:00:00Z','reported_at':'2026-09-02T00:00:00Z','reported_status':'COMPLETE','request_text':'Please delete my account.'}

    def tearDown(self):self.temp.cleanup()

    def csv(self,name,fields,rows):
        with (self.root/name).open('w',encoding='utf-8',newline='') as f:
            w=csv.writer(f);w.writerow(fields);w.writerows(rows)

    def evidence(self,name,content,captured=T):
        p=self.root/name;p.write_text(content,encoding='utf-8')
        self.manifest.append([name,name,'synthetic_fixture',captured])

    def engine(self):
        self.csv('evidence_files.csv',['file_id','file_path','origin','captured_at'],self.manifest)
        return AuditEngine(self.root)

    def account_absent(self):
        self.evidence('account.json',json.dumps({'records':[{'recorded_at':T,'system':'account_service','resource_id':'account_900','record_type':'USER_PROFILE','result':'NOT_FOUND','subject_reference':'current@example.test'}]}))

    def snapshot(self,name,system,collection,records):
        self.evidence(name,json.dumps({'snapshots':[{'captured_at':T,'data_store':system,'collection':collection,'records':records}]}))

    def test_historical_alias_decoy_and_future_file(self):
        self.account_absent()
        self.snapshot('search.json','search_service','customer_search_documents',[
            {'resource_id':'search_900','email':'previous@example.test'},
            {'resource_id':'search_901','email':'previous.jr@example.test'}])
        self.evidence('future.json',json.dumps({'records':[{'recorded_at':T,'system':'search_service','resource_id':'search_902','record_type':'SEARCH_INDEX_ENTRY','result':'FOUND','subject_reference':'current@example.test'}]}),'2026-09-16T00:00:00Z')
        r=self.engine().audit(self.request);steps=json.loads(r['steps_json'])
        self.assertEqual(r['deletion_status'],'INCOMPLETE')
        self.assertEqual({s['resource_id'] for s in steps},{'account_900','search_900'})
        findings=[s for s in steps if s['phase']=='FINDING']
        self.assertEqual([(s['resource_id'],s['evidence_id']) for s in findings],[('search_900','search.json')])
        self.assertTrue(all(s['evidence_id']=='' for s in steps if s['phase']!='FINDING'))

    def test_replica_presence_overrides_primary_absence(self):
        self.account_absent()
        self.evidence('replica.sql', '''CREATE TABLE customer_profiles_primary (resource_id TEXT,user_id TEXT,email TEXT);
CREATE TABLE customer_profiles_failover_replica (resource_id TEXT,user_id TEXT,email TEXT);
INSERT INTO customer_profiles_failover_replica VALUES ('account_900','user_alpha','current@example.test');''')
        r=self.engine().audit(self.request);steps=json.loads(r['steps_json'])
        self.assertEqual(r['deletion_status'],'INCOMPLETE')
        self.assertEqual(steps[0]['operation'],'REPORT_REMAINING_RECORD')
        self.assertEqual(steps[0]['evidence_id'],'replica.sql')

    def test_tombstone_and_retention(self):
        self.account_absent()
        self.snapshot('tombstone.json','identity_service','deleted_customer_references',[
            {'resource_id':'tombstone_900','subject_reference':'user_alpha','name':None,'email':None,'phone':None,'email_hash':None}])
        self.snapshot('security.json','security_service','security_audit_events',[
            {'resource_id':'audit_record_900','subject_reference':'user_alpha','retention_until':'2030-01-01T00:00:00Z'}])
        engine=self.engine();r=engine.audit(self.request);steps=json.loads(r['steps_json'])
        self.assertEqual(r['deletion_status'],'COMPLETE')
        self.assertEqual({s['operation'] for s in steps},{'VERIFY_RECORD_ABSENT','VERIFY_RECORD_REDACTED','VERIFY_RECORD_PRESENT'})
        self.assertTrue(all(s['evidence_id'] for s in steps))
        for o in engine.observations:
            if o.resource=='tombstone_900':o.record['email']='previous@example.test'
        r=engine.audit(self.request);steps=json.loads(r['steps_json'])
        self.assertEqual(r['deletion_status'],'INCOMPLETE')
        self.assertTrue(any(s['operation']=='REDACT_RECORD' for s in steps))
        self.assertFalse(any(s['resource_id']=='audit_record_900' and s['operation']=='DELETE_RECORD' for s in steps))

    def test_flow_restore_and_dependency_order(self):
        self.snapshot('profile.json','account_service','customer_profiles',[{'resource_id':'account_900','email':'current@example.test'}])
        self.snapshot('connector.json','integration_service','connector_configurations',[{'resource_id':'data_flow_900','subject_selector':'current@example.test','enabled':True}])
        self.snapshot('backup.json','backup_service','backup_catalog',[{'resource_id':'backup_900','subject_reference':'user_alpha','restore_allowed':True}])
        r=self.engine().audit(self.request);steps=json.loads(r['steps_json'])
        self.assertEqual([s['operation'] for s in steps if s['phase']=='REMEDIATION'],['DISABLE_DATA_FLOW','BLOCK_RESTORE','DELETE_RECORD'])
        self.assertEqual([s['step_no'] for s in steps],list(range(1,len(steps)+1)))
        self.assertEqual({s['operation'] for s in steps if s['phase']=='VERIFICATION'},{'VERIFY_RECORD_ABSENT','VERIFY_DATA_FLOW_DISABLED','VERIFY_RESTORE_BLOCKED'})

    def test_missing_files_and_bad_time_fail(self):
        self.engine()
        (self.root/'user_identities.csv').unlink()
        with self.assertRaises(FileNotFoundError):AuditEngine(self.root)
        with self.assertRaises(ValueError):instant('not-a-timestamp')

    def test_request_intent_and_repeatability(self):
        for text in ['Please export my data and keep the account active.',"Do not delete my account; just stop marketing emails.",'Please change my email. I want to continue using the service.', 'Please remove me from marketing lists only.', 'I am not asking for deletion.', 'Please correct it without removing any records.', 'This is an information request, not a request to erase it.']:
            self.assertFalse(authorizes_deletion(text))
        for text in ['このアカウントを削除してください。','Solicito la eliminación de mi cuenta.','Please delete my account and its export.']:
            self.assertTrue(authorizes_deletion(text))
        self.account_absent();e=self.engine()
        self.assertEqual(e.audit(self.request),e.audit(self.request))

    def test_log_correlation_without_status_claims(self):
        self.account_absent()
        self.evidence('observed.log',T+' level=DEBUG service=search_service trace_id=lookup event=index_query_started match_key="previous@example.test"\n'+T+' level=INFO service=search_service trace_id=lookup resource_id=search_900 event=index_query_completed result=hit\n')
        self.csv('system_activity.csv',['activity_id','event_time','event_type','source_system','target_system','resource_id','reported_result','details'],[
            ['claim','2026-09-02T00:00:00Z','DELETE_RECORD','deletion_worker','search_service','search_900','SUCCESS','Claimed successful deletion.']])
        result=self.engine().audit(self.request)
        self.assertEqual(result['deletion_status'],'INCOMPLETE')
        self.assertEqual(json.loads(result['steps_json'])[0]['evidence_id'],'observed.log')

    def test_strict_mode_preserves_existing_output_on_coverage_failure(self):
        self.snapshot('search.json','search_service','customer_search_documents',[{'resource_id':'search_900','email':'current@example.test'}])
        self.engine()
        self.csv('requests.csv',list(self.request),[list(self.request.values())])
        output=self.root/'output.csv';output.write_text('existing output',encoding='utf-8')
        with self.assertRaisesRegex(ValueError,'refusing to write output'):
            run_audit(self.root,self.root/'requests.csv',output,strict=True)
        self.assertEqual(output.read_text(encoding='utf-8'),'existing output')
        self.assertEqual(instant('2026-09-15T19:00:00+07:00'),instant(T))

    def test_image_digest_rejects_changed_source(self):
        notes=Path(__file__).resolve().parents[1]/'image_observations.md'
        import re
        entry=json.loads(re.search(r'```json\s*(.*?)\s*```',notes.read_text(encoding='utf-8'),re.S)[1])[0]
        image=self.root/entry['file_path'];image.parent.mkdir(parents=True);image.write_bytes(b'changed image')
        self.manifest.append(['changed_image',entry['file_path'],'test',T])
        with self.assertRaisesRegex(ValueError,'Image changed'):self.engine()

    def test_search_foreign_key_links_absent_primary_without_trusting_delete_claim(self):
        self.snapshot('search.json','search_service','customer_search_documents',[
            {'resource_id':'search_900','email':'previous@example.test','source_resource_id':'account_900'}])
        self.evidence('profile.sql','CREATE TABLE customer_profiles_primary (resource_id TEXT,email TEXT);')
        self.csv('system_activity.csv',['activity_id','event_time','event_type','source_system','target_system','resource_id','reported_result','details'],[
            ['routing','2026-09-02T00:00:00Z','DELETE_RECORD','deletion_worker','account_service','account_900','FAILED','Submitted primary profile account_900 to account_service.']])
        result=self.engine().audit(self.request);steps=json.loads(result['steps_json'])
        primary=[s for s in steps if s['resource_id']=='account_900']
        self.assertEqual(len(primary),1)
        self.assertEqual(primary[0]['operation'],'VERIFY_RECORD_ABSENT')
        self.assertEqual(primary[0]['evidence_id'],'')
        self.assertFalse(any(s['resource_id']=='account_900' and s['phase']=='FINDING' for s in steps))

    def test_phone_format_and_derived_historical_email_hash(self):
        current_hash=hashlib.sha256(b'current@example.test').hexdigest()
        self.csv('user_identities.csv',['user_id','name','email','phone','email_hash','updated_at'],[
            ['user_alpha','Test Subject','current@example.test','+1 (234) 567-8901',current_hash,'2026-01-01T00:00:00Z']])
        self.account_absent()
        self.snapshot('phone.json','search_service','customer_search_documents',[
            {'resource_id':'search_900','phone':'+12345678901'}])
        self.snapshot('hash.json','analytics_platform','customer_analytics_reports',[
            {'resource_id':'analytics_900','email_hash':hashlib.sha256(b'previous@example.test').hexdigest()}])
        result=self.engine().audit(self.request)
        findings={s['resource_id'] for s in json.loads(result['steps_json']) if s['phase']=='FINDING'}
        self.assertEqual(findings,{'search_900','analytics_900'})

    def test_long_reference_chain_cycle_and_prose_do_not_create_identity_links(self):
        self.account_absent()
        records=[]
        for i in range(6):
            record={'resource_id':f'search_{910+i}','source_resource_id':f'search_{910+(i+1)%6}'}
            if i==5:
                record['email']='current@example.test'
                record['debug_note']='Search search_999 belongs to a different customer.'
            records.append(record)
        records.append({'resource_id':'search_999','email':'unrelated@example.test'})
        self.snapshot('chain.json','search_service','customer_search_documents',records)
        result=self.engine().audit(self.request)
        findings={s['resource_id'] for s in json.loads(result['steps_json']) if s['phase']=='FINDING'}
        self.assertEqual(findings,{f'search_{910+i}' for i in range(6)})

    def test_future_foreign_key_cannot_resolve_a_primary(self):
        self.snapshot('search.json','search_service','customer_search_documents',[
            {'resource_id':'search_900','email':'current@example.test'}])
        self.evidence('future.json',json.dumps({'snapshots':[{'captured_at':T,'data_store':'search_service','collection':'customer_search_documents','records':[
            {'resource_id':'search_900','email':'current@example.test','source_resource_id':'account_900'}]}]}),'2026-09-16T00:00:00Z')
        self.evidence('profile.sql','CREATE TABLE customer_profiles_primary (resource_id TEXT,email TEXT);')
        self.csv('system_activity.csv',['activity_id','event_time','event_type','source_system','target_system','resource_id','reported_result','details'],[
            ['routing','2026-09-02T00:00:00Z','DELETE_RECORD','deletion_worker','account_service','account_900','SUCCESS','Submitted account_900.']])
        engine=self.engine();result=engine.audit(self.request)
        self.assertNotIn('account_900',{s['resource_id'] for s in json.loads(result['steps_json'])})
        self.assertTrue(any('No identity-linked primary account state' in issues for _,issues in engine.warnings))

    def test_pipe_log_correlates_interleaved_traces_without_decoy_leakage(self):
        self.evidence('pipe.log',
            T+' | DEBUG | account_service | tr-owner | profile_lookup_started | lookup_key="previous@example.test"\n'
            +T+' | DEBUG | account_service | tr-decoy | profile_lookup_started | lookup_key="previous.jr@example.test"\n'
            +T+' | INFO | account_service | tr-decoy | profile_lookup_completed | resource_id="account_901" rows="1" http_status="200"\n'
            +T+' | INFO | account_service | tr-owner | profile_lookup_completed | resource_id="account_900" rows="0" http_status="404"\n'
            +T+' | INFO | search_service | tr-search | index_query_completed | resource_id="search_900" result="hit" correlation_key="previous@example.test"\n')
        engine=self.engine();result=engine.audit(self.request);steps=json.loads(result['steps_json'])
        self.assertEqual(result['deletion_status'],'INCOMPLETE')
        self.assertEqual({s['resource_id'] for s in steps},{'account_900','search_900'})
        self.assertEqual(steps[0]['resource_id'],'search_900')
        self.assertEqual(steps[0]['evidence_id'],'pipe.log')
        self.assertEqual(engine.warnings,[])


if __name__=='__main__':unittest.main()
