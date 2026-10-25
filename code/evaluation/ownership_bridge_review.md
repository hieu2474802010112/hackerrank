# Ownership bridges and step mismatch classification

This is a public-sample diagnostic only; expected answers never enter predictions. Comparison keys ignore step_no and evidence_id to distinguish missing/extra semantic steps from citation or numbering differences. No main solver or output.csv edits were made.

## Nine missing-account attribution checks

| Case | Account | Eligible activity | Identity/correlation fields in that activity |
| --- | --- | --- | --- |
| case_01 | account_001 | activity_3342 | No user/email/session/request/ticket key in matched activity rows |
| case_02 | account_002 | activity_3376 | No user/email/session/request/ticket key in matched activity rows |
| case_04 | account_004 | none | No user/email/session/request/ticket key in matched activity rows |
| case_21 | account_6440 | activity_3661 | No user/email/session/request/ticket key in matched activity rows |
| case_25 | account_3136 | activity_3597 | No user/email/session/request/ticket key in matched activity rows |
| case_26 | account_5684 | activity_3600 | No user/email/session/request/ticket key in matched activity rows |
| case_27 | account_3866 | activity_3530 | No user/email/session/request/ticket key in matched activity rows |
| case_28 | account_5482 | activity_3529 | No user/email/session/request/ticket key in matched activity rows |
| case_31 | account_4857 | activity_3682 | No user/email/session/request/ticket key in matched activity rows |

The matching activity rows describe the target resource and a claimed deletion result. They supply neither an identity nor a session/request/ticket correlation key. Text-source scans in sample_resource_provenance.md found no additional eligible identity-bearing resource occurrence for these accounts. Eligible API 404 rows in evidence_92 carry resource_id/observed_at/status_code/profile=null without an owner. No new grounded bridge was established by these checks. This is a limitation of the implemented inspection, not proof that every possible bridge is absent.

## Fourteen step-only mismatches

| Case | Missing semantic steps | Extra semantic steps | Different citations on shared steps | Missing resources | Extra resources |
| --- | --- | --- | --- | --- | --- |
| case_03 | 1 | 0 | 0 | analytics_9406 | none |
| case_07 | 1 | 3 | 0 | account_007 | object_19 |
| case_08 | 1 | 0 | 0 | account_008 | none |
| case_09 | 2 | 0 | 0 | account_3960, audit_record_4902 | none |
| case_10 | 1 | 0 | 0 | account_010 | none |
| case_17 | 0 | 1 | 0 | none | account_6523 |
| case_18 | 2 | 0 | 0 | account_5521, audit_record_6645 | none |
| case_20 | 2 | 0 | 0 | account_5037, audit_record_5569 | none |
| case_22 | 1 | 0 | 0 | account_4990 | none |
| case_23 | 2 | 0 | 0 | account_410, audit_record_4128 | none |
| case_24 | 1 | 0 | 0 | audit_record_7095 | none |
| case_29 | 2 | 0 | 0 | account_7012, audit_record_3954 | none |
| case_30 | 2 | 0 | 0 | account_4163, audit_record_1707 | none |
| case_32 | 1 | 0 | 0 | account_8858 | none |

All 14 cases have a substantive missing or extra step. None has a different evidence_id on a shared semantic step, so these are not citation-only errors or only positional numbering errors. case_07 has an additional three-step object_19 plan; case_17 has one additional account_6523 step. Whether extra steps are source-attribution, time-selection or policy errors requires inspecting the corresponding evidence; the public reference alone does not justify deleting them.

case_21 reference has no tombstone step. Ambiguous ownership cannot be silently converted to a valid retained record or dropped solely to match a reference.
