"""Activity ownership and workflow-claim safety regressions."""
import sys
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from system_activity_mapper import SystemActivityMapper


def event(number,when,resource,kind,details,result='SUCCESS'):
    return {'activity_id':f'activity_{number}','event_time':when,'event_type':kind,
            'source_system':'worker','target_system':'account_service',
            'resource_id':resource,'reported_result':result,'details':details}


T='2026-09-15T12:00:00Z'


class SystemActivityMapperTests(unittest.TestCase):
    def test_exact_tokens_and_timezone_cutoff(self):
        mapper=SystemActivityMapper(activities=[
            event(1,T,'account_1','LINK_RESOURCE_IDENTITY','Linked to OLD@example.test and user_05.'),
            event(2,T,'account_2','LINK_RESOURCE_IDENTITY','Linked to old.jr@example.test and user_050.'),
            event(3,'2026-09-15T12:00:01Z','account_3','LINK_RESOURCE_IDENTITY','Linked to old@example.test and user_05.')])
        rows=mapper.find_resources_for_identifiers(['old@example.test','user_05'],'2026-09-15T19:00:00+07:00')
        self.assertEqual([r['activity_id'] for r in rows],['activity_1'])
        self.assertEqual(rows[0]['matched_identifiers'],['old@example.test','user_05'])

    def test_anonymous_history_follows_only_explicitly_linked_resource(self):
        mapper=SystemActivityMapper(activities=[
            event(1,'2026-09-14T12:00:00Z','account_1','LINK_RESOURCE_IDENTITY','Owner previous@example.test.'),
            event(2,T,'account_1','DELETE_RECORD','Requested operation completed.'),
            event(3,T,'account_2','DELETE_RECORD','Requested operation completed.'),
            event(4,'2026-09-16T00:00:00Z','account_1','SYNC_RECORD','Replication completed.')])
        rows=mapper.find_resources_for_emails(['previous@example.test'],T)
        self.assertEqual([r['activity_id'] for r in rows],['activity_1','activity_2'])
        self.assertEqual([r['match_kind'] for r in rows],['IDENTITY_MATCH','RESOURCE_HISTORY'])
        self.assertEqual(rows[1]['matched_identifiers'],[])

    def test_success_is_claim_not_verified_absence_or_anonymization(self):
        activities=[event(1,T,'analytics_1','ANONYMIZE_RECORD','Reported anonymization.'),
                    event(2,T,'account_1','DELETE_RECORD','Reported deletion.'),
                    event(3,T,'account_2','DELETE_RECORD','Failed deletion.','FAILED'),
                    event(4,'2026-09-16T00:00:00Z','account_1','SYNC_RECORD','Later sync.')]
        states=SystemActivityMapper(activities=activities).deduce_resource_state(activities,T)
        self.assertEqual(states['analytics_1']['claimed_state'],'ANONYMIZED')
        self.assertEqual(states['account_1']['claimed_state'],'ABSENT')
        self.assertIsNone(states['account_2']['claimed_state'])
        for state in states.values():
            self.assertEqual(state['status'],'UNKNOWN')
            self.assertFalse(state['verified'])
            self.assertEqual(state['evidence_id'],'')
        self.assertEqual(states['account_1']['activity_ids'],['activity_2'])

    def test_conflicting_ownership_retains_provenance_and_phone_normalization(self):
        mapper=SystemActivityMapper(activities=[
            event(1,T,'account_1','LINK_RESOURCE_IDENTITY','Owner +1 (234) 567-8901 and user_one.'),
            event(2,T,'account_1','LINK_RESOURCE_IDENTITY','Owner user_two.')])
        owners,provenance=mapper.ownership_links({'tel:+12345678901':{'user_one'},'user_one':{'user_one'},'user_two':{'user_two'}},T)
        self.assertEqual(owners['account_1'],{'user_one','user_two'})
        self.assertEqual(provenance['account_1'],{'activity_1','activity_2'})

    def test_invalid_times_duplicates_and_empty_query_fail_explicitly(self):
        with self.assertRaisesRegex(ValueError,'Invalid event_time'):
            SystemActivityMapper(activities=[event(1,'invalid','account_1','DELETE_RECORD','Claim.')])
        row=event(1,T,'account_1','DELETE_RECORD','Claim.')
        with self.assertRaisesRegex(ValueError,'unique'):
            SystemActivityMapper(activities=[row,row])
        with self.assertRaisesRegex(ValueError,'non-empty'):
            SystemActivityMapper(activities=[]).find_resources_for_emails([''],T)


if __name__=='__main__':unittest.main()
