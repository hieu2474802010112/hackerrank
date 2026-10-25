# Public-reference resource provenance investigation

References are diagnostic targets only. Scanning excludes sample_output.csv, sample request/output templates and organizer data; textual occurrence is not ownership proof. Existing engine observations are checked separately for cutoff and identity ownership. No solver labels are patched.

Identity files have no account_id/resource_id columns: identities contain user_id/name/email/phone/email_hash/updated_at and history contains audit_id/user_id/event_time/field_name/old_value/new_value. Thus an account ID cannot be read from a nonexistent identity column.

## Nine status mismatches

| Case | Expected account | Reference evidence | Explicit owner-linked eligible observation | Eligible text sources containing ID | Later text sources |
| --- | --- | --- | --- | --- | --- |
| case_01 | account_001 | evidence_54 | False | none | none |
| case_02 | account_002 | evidence_54 | False | none | none |
| case_04 | account_004 | evidence_54 | False | none | none |
| case_21 | account_6440 | evidence_92 | False | evidence_92 | none |
| case_25 | account_3136 | evidence_92 | False | evidence_92 | none |
| case_26 | account_5684 | evidence_92 | False | evidence_92 | evidence_02 |
| case_27 | account_3866 | evidence_92 | False | evidence_92 | evidence_02 |
| case_28 | account_5482 | evidence_92 | False | evidence_92 | none |
| case_31 | account_4857 | evidence_51 | False | none | none |

## case_21 tombstone

The public reference for case_21 contains only account_6440 VERIFY_RECORD_ABSENT, audit_record_3737 VERIFY_RECORD_PRESENT and analytics_5335 VERIFY_RECORD_ANONYMIZED, all citing evidence_92. It does not contain a tombstone step. Treating the ambiguous tombstone_17 as a permitted retained record would not by itself fix the missing account mapping. Its ownership must be independently established or rejected.

## Interpretation

The existing engine already handles scoped-snapshot absence and explicit 404/null readbacks, but does not use unowned readbacks to infer a person. Evidence_92 contains explicit resource-ID profile lookup 404s; those prove the named resource absent, not which user owned it. Evidence_54 is a primary/failover table snapshot, where an absent resource cannot be mapped to a user by numeric suffix. Future identity-bearing events are excluded. The matching failure is therefore not sufficient evidence that absence parsing itself is missing or that all 343 warnings share a single proven cause.

## All missing expected-step source occurrences

### case_01 / account_001 / VERIFY_RECORD_ABSENT

Reference citation: evidence_54; eligible engine owner link: False.

- No exact ID occurrence in supported text sources. Images/PDFs require their actual extraction; this text scan is not proof of absence.

### case_02 / account_002 / VERIFY_RECORD_ABSENT

Reference citation: evidence_54; eligible engine owner link: False.

- No exact ID occurrence in supported text sources. Images/PDFs require their actual extraction; this text scan is not proof of absence.

### case_03 / analytics_9406 / VERIFY_RECORD_ANONYMIZED

Reference citation: evidence_94; eligible engine owner link: False.

- evidence_94: evidence/logs/resource_lookup_trace_20260926_103856.log — captured 2026-09-26T10:38:56Z; file eligible: True

### case_04 / account_004 / VERIFY_RECORD_ABSENT

Reference citation: evidence_54; eligible engine owner link: False.

- No exact ID occurrence in supported text sources. Images/PDFs require their actual extraction; this text scan is not proof of absence.

### case_04 / analytics_901 / VERIFY_RECORD_ANONYMIZED

Reference citation: evidence_56; eligible engine owner link: False.

- evidence_56: evidence/records/customer_analytics_report_20260907.json — captured 2026-09-07T09:45:00Z; file eligible: True

### case_07 / support_001 / REPORT_REMAINING_RECORD

Reference citation: evidence_58; eligible engine owner link: True.

- No exact ID occurrence in supported text sources. Images/PDFs require their actual extraction; this text scan is not proof of absence.

### case_07 / support_001 / DELETE_RECORD

Reference citation: ; eligible engine owner link: True.

- No exact ID occurrence in supported text sources. Images/PDFs require their actual extraction; this text scan is not proof of absence.

### case_07 / account_007 / VERIFY_RECORD_ABSENT

Reference citation: ; eligible engine owner link: False.

- No exact ID occurrence in supported text sources. Images/PDFs require their actual extraction; this text scan is not proof of absence.

### case_07 / support_001 / VERIFY_RECORD_ABSENT

Reference citation: ; eligible engine owner link: True.

- No exact ID occurrence in supported text sources. Images/PDFs require their actual extraction; this text scan is not proof of absence.

### case_08 / account_008 / VERIFY_RECORD_ABSENT

Reference citation: ; eligible engine owner link: False.

- No exact ID occurrence in supported text sources. Images/PDFs require their actual extraction; this text scan is not proof of absence.

### case_08 / export_001 / VERIFY_RECORD_ABSENT

Reference citation: ; eligible engine owner link: True.

- evidence_59: evidence/records/customer_export_jobs_20260914.json — captured 2026-09-14T15:40:00Z; file eligible: True

### case_09 / account_3960 / VERIFY_RECORD_ABSENT

Reference citation: ; eligible engine owner link: False.

- evidence_06: evidence/logs/structured_service_events_eu_west_20260918.log — captured 2026-09-18T11:55:24Z; file eligible: False

### case_09 / audit_record_4902 / VERIFY_RECORD_PRESENT

Reference citation: ; eligible engine owner link: False.

- evidence_06: evidence/logs/structured_service_events_eu_west_20260918.log — captured 2026-09-18T11:55:24Z; file eligible: False

### case_09 / backup_4978 / VERIFY_RESTORE_BLOCKED

Reference citation: ; eligible engine owner link: True.

- evidence_06: evidence/logs/structured_service_events_eu_west_20260918.log — captured 2026-09-18T11:55:24Z; file eligible: False
- evidence_93: evidence/databases/customer_data_inventory_20260916.sql — captured 2026-09-16T08:37:39Z; file eligible: True

### case_10 / account_010 / VERIFY_RECORD_ABSENT

Reference citation: ; eligible engine owner link: False.

- No exact ID occurrence in supported text sources. Images/PDFs require their actual extraction; this text scan is not proof of absence.

### case_10 / support_002 / VERIFY_RECORD_ABSENT

Reference citation: ; eligible engine owner link: True.

- evidence_61: evidence/logs/support_replica.log — captured 2026-09-17T22:00:19Z; file eligible: True

### case_17 / audit_record_1797 / VERIFY_RECORD_PRESENT

Reference citation: ; eligible engine owner link: True.

- evidence_01: evidence/logs/service_events_ap_south_20260915.log — captured 2026-09-15T11:59:39Z; file eligible: True

### case_17 / backup_3245 / VERIFY_RESTORE_BLOCKED

Reference citation: ; eligible engine owner link: True.

- evidence_01: evidence/logs/service_events_ap_south_20260915.log — captured 2026-09-15T11:59:39Z; file eligible: True

### case_18 / account_5521 / VERIFY_RECORD_ABSENT

Reference citation: ; eligible engine owner link: False.

- No exact ID occurrence in supported text sources. Images/PDFs require their actual extraction; this text scan is not proof of absence.

### case_18 / search_4013 / VERIFY_RECORD_ABSENT

Reference citation: ; eligible engine owner link: True.

- evidence_94: evidence/logs/resource_lookup_trace_20260926_103856.log — captured 2026-09-26T10:38:56Z; file eligible: True

### case_18 / audit_record_6645 / VERIFY_RECORD_PRESENT

Reference citation: ; eligible engine owner link: False.

- No exact ID occurrence in supported text sources. Images/PDFs require their actual extraction; this text scan is not proof of absence.

### case_18 / support_5569 / VERIFY_RECORD_REDACTED

Reference citation: ; eligible engine owner link: True.

- evidence_94: evidence/logs/resource_lookup_trace_20260926_103856.log — captured 2026-09-26T10:38:56Z; file eligible: True

### case_18 / analytics_037 / VERIFY_RECORD_ANONYMIZED

Reference citation: ; eligible engine owner link: True.

- evidence_94: evidence/logs/resource_lookup_trace_20260926_103856.log — captured 2026-09-26T10:38:56Z; file eligible: True

### case_18 / data_flow_4890 / VERIFY_DATA_FLOW_DISABLED

Reference citation: ; eligible engine owner link: True.

- evidence_94: evidence/logs/resource_lookup_trace_20260926_103856.log — captured 2026-09-26T10:38:56Z; file eligible: True

### case_20 / account_5037 / VERIFY_RECORD_ABSENT

Reference citation: ; eligible engine owner link: False.

- No exact ID occurrence in supported text sources. Images/PDFs require their actual extraction; this text scan is not proof of absence.

### case_20 / search_4262 / VERIFY_RECORD_ABSENT

Reference citation: ; eligible engine owner link: True.

- evidence_94: evidence/logs/resource_lookup_trace_20260926_103856.log — captured 2026-09-26T10:38:56Z; file eligible: True

### case_20 / audit_record_5569 / VERIFY_RECORD_PRESENT

Reference citation: ; eligible engine owner link: False.

- No exact ID occurrence in supported text sources. Images/PDFs require their actual extraction; this text scan is not proof of absence.

### case_20 / data_flow_1770 / VERIFY_DATA_FLOW_DISABLED

Reference citation: ; eligible engine owner link: True.

- evidence_94: evidence/logs/resource_lookup_trace_20260926_103856.log — captured 2026-09-26T10:38:56Z; file eligible: True

### case_21 / account_6440 / VERIFY_RECORD_ABSENT

Reference citation: evidence_92; eligible engine owner link: False.

- evidence_92: evidence/records/service_resource_export_20260915_114455.json — captured 2026-09-15T11:44:55Z; file eligible: True

### case_21 / audit_record_3737 / VERIFY_RECORD_PRESENT

Reference citation: evidence_92; eligible engine owner link: True.

- evidence_02: evidence/records/customer_data_snapshot_bundle_20260917.json — captured 2026-09-17T12:00:00Z; file eligible: False
- evidence_92: evidence/records/service_resource_export_20260915_114455.json — captured 2026-09-15T11:44:55Z; file eligible: True

### case_21 / analytics_5335 / VERIFY_RECORD_ANONYMIZED

Reference citation: evidence_92; eligible engine owner link: False.

- evidence_02: evidence/records/customer_data_snapshot_bundle_20260917.json — captured 2026-09-17T12:00:00Z; file eligible: False
- evidence_92: evidence/records/service_resource_export_20260915_114455.json — captured 2026-09-15T11:44:55Z; file eligible: True

### case_22 / account_4990 / VERIFY_RECORD_ABSENT

Reference citation: ; eligible engine owner link: False.

- No exact ID occurrence in supported text sources. Images/PDFs require their actual extraction; this text scan is not proof of absence.

### case_22 / search_8911 / VERIFY_RECORD_ABSENT

Reference citation: ; eligible engine owner link: True.

- evidence_05: evidence/databases/customer_data_read_replica_20260921.sql — captured 2026-09-21T10:00:00Z; file eligible: True

### case_22 / audit_record_3482 / VERIFY_RECORD_PRESENT

Reference citation: ; eligible engine owner link: True.

- evidence_05: evidence/databases/customer_data_read_replica_20260921.sql — captured 2026-09-21T10:00:00Z; file eligible: True

### case_22 / analytics_4440 / VERIFY_RECORD_ANONYMIZED

Reference citation: ; eligible engine owner link: True.

- evidence_05: evidence/databases/customer_data_read_replica_20260921.sql — captured 2026-09-21T10:00:00Z; file eligible: True

### case_23 / account_410 / VERIFY_RECORD_ABSENT

Reference citation: ; eligible engine owner link: False.

- No exact ID occurrence in supported text sources. Images/PDFs require their actual extraction; this text scan is not proof of absence.

### case_23 / export_7364 / VERIFY_RECORD_ABSENT

Reference citation: ; eligible engine owner link: True.

- evidence_02: evidence/records/customer_data_snapshot_bundle_20260917.json — captured 2026-09-17T12:00:00Z; file eligible: False
- evidence_92: evidence/records/service_resource_export_20260915_114455.json — captured 2026-09-15T11:44:55Z; file eligible: True

### case_23 / search_898 / VERIFY_RECORD_ABSENT

Reference citation: ; eligible engine owner link: True.

- evidence_02: evidence/records/customer_data_snapshot_bundle_20260917.json — captured 2026-09-17T12:00:00Z; file eligible: False
- evidence_92: evidence/records/service_resource_export_20260915_114455.json — captured 2026-09-15T11:44:55Z; file eligible: True

### case_23 / audit_record_4128 / VERIFY_RECORD_PRESENT

Reference citation: ; eligible engine owner link: False.

- evidence_02: evidence/records/customer_data_snapshot_bundle_20260917.json — captured 2026-09-17T12:00:00Z; file eligible: False

### case_24 / audit_record_7095 / VERIFY_RECORD_PRESENT

Reference citation: ; eligible engine owner link: False.

- evidence_02: evidence/records/customer_data_snapshot_bundle_20260917.json — captured 2026-09-17T12:00:00Z; file eligible: False

### case_25 / account_3136 / VERIFY_RECORD_ABSENT

Reference citation: evidence_92; eligible engine owner link: False.

- evidence_92: evidence/records/service_resource_export_20260915_114455.json — captured 2026-09-15T11:44:55Z; file eligible: True

### case_25 / audit_record_451 / VERIFY_RECORD_PRESENT

Reference citation: evidence_92; eligible engine owner link: True.

- evidence_02: evidence/records/customer_data_snapshot_bundle_20260917.json — captured 2026-09-17T12:00:00Z; file eligible: False
- evidence_92: evidence/records/service_resource_export_20260915_114455.json — captured 2026-09-15T11:44:55Z; file eligible: True

### case_25 / analytics_1895 / VERIFY_RECORD_ANONYMIZED

Reference citation: evidence_92; eligible engine owner link: False.

- evidence_02: evidence/records/customer_data_snapshot_bundle_20260917.json — captured 2026-09-17T12:00:00Z; file eligible: False
- evidence_92: evidence/records/service_resource_export_20260915_114455.json — captured 2026-09-15T11:44:55Z; file eligible: True

### case_26 / account_5684 / VERIFY_RECORD_ABSENT

Reference citation: evidence_92; eligible engine owner link: False.

- evidence_02: evidence/records/customer_data_snapshot_bundle_20260917.json — captured 2026-09-17T12:00:00Z; file eligible: False
- evidence_92: evidence/records/service_resource_export_20260915_114455.json — captured 2026-09-15T11:44:55Z; file eligible: True

### case_26 / audit_record_5416 / VERIFY_RECORD_PRESENT

Reference citation: evidence_92; eligible engine owner link: True.

- evidence_02: evidence/records/customer_data_snapshot_bundle_20260917.json — captured 2026-09-17T12:00:00Z; file eligible: False
- evidence_92: evidence/records/service_resource_export_20260915_114455.json — captured 2026-09-15T11:44:55Z; file eligible: True

### case_26 / support_4715 / VERIFY_RECORD_REDACTED

Reference citation: evidence_92; eligible engine owner link: True.

- evidence_02: evidence/records/customer_data_snapshot_bundle_20260917.json — captured 2026-09-17T12:00:00Z; file eligible: False
- evidence_92: evidence/records/service_resource_export_20260915_114455.json — captured 2026-09-15T11:44:55Z; file eligible: True

### case_26 / analytics_4566 / VERIFY_RECORD_ANONYMIZED

Reference citation: evidence_92; eligible engine owner link: False.

- evidence_02: evidence/records/customer_data_snapshot_bundle_20260917.json — captured 2026-09-17T12:00:00Z; file eligible: False
- evidence_92: evidence/records/service_resource_export_20260915_114455.json — captured 2026-09-15T11:44:55Z; file eligible: True

### case_26 / data_flow_6244 / VERIFY_DATA_FLOW_DISABLED

Reference citation: evidence_92; eligible engine owner link: True.

- evidence_02: evidence/records/customer_data_snapshot_bundle_20260917.json — captured 2026-09-17T12:00:00Z; file eligible: False
- evidence_92: evidence/records/service_resource_export_20260915_114455.json — captured 2026-09-15T11:44:55Z; file eligible: True

### case_26 / backup_3120 / VERIFY_RESTORE_BLOCKED

Reference citation: evidence_92; eligible engine owner link: True.

- evidence_02: evidence/records/customer_data_snapshot_bundle_20260917.json — captured 2026-09-17T12:00:00Z; file eligible: False
- evidence_92: evidence/records/service_resource_export_20260915_114455.json — captured 2026-09-15T11:44:55Z; file eligible: True

### case_27 / account_3866 / VERIFY_RECORD_ABSENT

Reference citation: evidence_92; eligible engine owner link: False.

- evidence_02: evidence/records/customer_data_snapshot_bundle_20260917.json — captured 2026-09-17T12:00:00Z; file eligible: False
- evidence_92: evidence/records/service_resource_export_20260915_114455.json — captured 2026-09-15T11:44:55Z; file eligible: True

### case_27 / audit_record_3830 / VERIFY_RECORD_PRESENT

Reference citation: evidence_92; eligible engine owner link: True.

- evidence_02: evidence/records/customer_data_snapshot_bundle_20260917.json — captured 2026-09-17T12:00:00Z; file eligible: False
- evidence_92: evidence/records/service_resource_export_20260915_114455.json — captured 2026-09-15T11:44:55Z; file eligible: True

### case_27 / support_4707 / VERIFY_RECORD_REDACTED

Reference citation: evidence_92; eligible engine owner link: True.

- evidence_02: evidence/records/customer_data_snapshot_bundle_20260917.json — captured 2026-09-17T12:00:00Z; file eligible: False
- evidence_92: evidence/records/service_resource_export_20260915_114455.json — captured 2026-09-15T11:44:55Z; file eligible: True

### case_27 / analytics_4574 / VERIFY_RECORD_ANONYMIZED

Reference citation: evidence_92; eligible engine owner link: False.

- evidence_02: evidence/records/customer_data_snapshot_bundle_20260917.json — captured 2026-09-17T12:00:00Z; file eligible: False
- evidence_92: evidence/records/service_resource_export_20260915_114455.json — captured 2026-09-15T11:44:55Z; file eligible: True

### case_27 / data_flow_2295 / VERIFY_DATA_FLOW_DISABLED

Reference citation: evidence_92; eligible engine owner link: True.

- evidence_02: evidence/records/customer_data_snapshot_bundle_20260917.json — captured 2026-09-17T12:00:00Z; file eligible: False
- evidence_92: evidence/records/service_resource_export_20260915_114455.json — captured 2026-09-15T11:44:55Z; file eligible: True

### case_27 / backup_5970 / VERIFY_RESTORE_BLOCKED

Reference citation: evidence_92; eligible engine owner link: True.

- evidence_02: evidence/records/customer_data_snapshot_bundle_20260917.json — captured 2026-09-17T12:00:00Z; file eligible: False
- evidence_92: evidence/records/service_resource_export_20260915_114455.json — captured 2026-09-15T11:44:55Z; file eligible: True

### case_28 / account_5482 / VERIFY_RECORD_ABSENT

Reference citation: evidence_92; eligible engine owner link: False.

- evidence_92: evidence/records/service_resource_export_20260915_114455.json — captured 2026-09-15T11:44:55Z; file eligible: True

### case_28 / audit_record_9265 / VERIFY_RECORD_PRESENT

Reference citation: evidence_92; eligible engine owner link: True.

- evidence_02: evidence/records/customer_data_snapshot_bundle_20260917.json — captured 2026-09-17T12:00:00Z; file eligible: False
- evidence_92: evidence/records/service_resource_export_20260915_114455.json — captured 2026-09-15T11:44:55Z; file eligible: True

### case_28 / support_2351 / VERIFY_RECORD_REDACTED

Reference citation: evidence_92; eligible engine owner link: True.

- evidence_02: evidence/records/customer_data_snapshot_bundle_20260917.json — captured 2026-09-17T12:00:00Z; file eligible: False
- evidence_92: evidence/records/service_resource_export_20260915_114455.json — captured 2026-09-15T11:44:55Z; file eligible: True

### case_28 / analytics_6077 / VERIFY_RECORD_ANONYMIZED

Reference citation: evidence_92; eligible engine owner link: False.

- evidence_02: evidence/records/customer_data_snapshot_bundle_20260917.json — captured 2026-09-17T12:00:00Z; file eligible: False
- evidence_92: evidence/records/service_resource_export_20260915_114455.json — captured 2026-09-15T11:44:55Z; file eligible: True

### case_28 / data_flow_2337 / VERIFY_DATA_FLOW_DISABLED

Reference citation: evidence_92; eligible engine owner link: True.

- evidence_02: evidence/records/customer_data_snapshot_bundle_20260917.json — captured 2026-09-17T12:00:00Z; file eligible: False
- evidence_92: evidence/records/service_resource_export_20260915_114455.json — captured 2026-09-15T11:44:55Z; file eligible: True

### case_28 / backup_838 / VERIFY_RESTORE_BLOCKED

Reference citation: evidence_92; eligible engine owner link: True.

- evidence_02: evidence/records/customer_data_snapshot_bundle_20260917.json — captured 2026-09-17T12:00:00Z; file eligible: False
- evidence_92: evidence/records/service_resource_export_20260915_114455.json — captured 2026-09-15T11:44:55Z; file eligible: True

### case_29 / account_7012 / VERIFY_RECORD_ABSENT

Reference citation: ; eligible engine owner link: False.

- No exact ID occurrence in supported text sources. Images/PDFs require their actual extraction; this text scan is not proof of absence.

### case_29 / search_1993 / VERIFY_RECORD_ABSENT

Reference citation: ; eligible engine owner link: True.

- evidence_02: evidence/records/customer_data_snapshot_bundle_20260917.json — captured 2026-09-17T12:00:00Z; file eligible: False
- evidence_92: evidence/records/service_resource_export_20260915_114455.json — captured 2026-09-15T11:44:55Z; file eligible: True

### case_29 / audit_record_3954 / VERIFY_RECORD_PRESENT

Reference citation: ; eligible engine owner link: False.

- evidence_02: evidence/records/customer_data_snapshot_bundle_20260917.json — captured 2026-09-17T12:00:00Z; file eligible: False

### case_29 / support_5281 / VERIFY_RECORD_REDACTED

Reference citation: ; eligible engine owner link: True.

- evidence_02: evidence/records/customer_data_snapshot_bundle_20260917.json — captured 2026-09-17T12:00:00Z; file eligible: False
- evidence_92: evidence/records/service_resource_export_20260915_114455.json — captured 2026-09-15T11:44:55Z; file eligible: True

### case_29 / analytics_5208 / VERIFY_RECORD_ANONYMIZED

Reference citation: ; eligible engine owner link: True.

- evidence_02: evidence/records/customer_data_snapshot_bundle_20260917.json — captured 2026-09-17T12:00:00Z; file eligible: False
- evidence_92: evidence/records/service_resource_export_20260915_114455.json — captured 2026-09-15T11:44:55Z; file eligible: True

### case_29 / data_flow_3827 / VERIFY_DATA_FLOW_DISABLED

Reference citation: ; eligible engine owner link: True.

- evidence_02: evidence/records/customer_data_snapshot_bundle_20260917.json — captured 2026-09-17T12:00:00Z; file eligible: False
- evidence_92: evidence/records/service_resource_export_20260915_114455.json — captured 2026-09-15T11:44:55Z; file eligible: True

### case_30 / account_4163 / VERIFY_RECORD_ABSENT

Reference citation: ; eligible engine owner link: False.

- No exact ID occurrence in supported text sources. Images/PDFs require their actual extraction; this text scan is not proof of absence.

### case_30 / search_9359 / VERIFY_RECORD_ABSENT

Reference citation: ; eligible engine owner link: True.

- evidence_02: evidence/records/customer_data_snapshot_bundle_20260917.json — captured 2026-09-17T12:00:00Z; file eligible: False
- evidence_92: evidence/records/service_resource_export_20260915_114455.json — captured 2026-09-15T11:44:55Z; file eligible: True

### case_30 / audit_record_1707 / VERIFY_RECORD_PRESENT

Reference citation: ; eligible engine owner link: False.

- evidence_02: evidence/records/customer_data_snapshot_bundle_20260917.json — captured 2026-09-17T12:00:00Z; file eligible: False

### case_30 / support_6477 / VERIFY_RECORD_REDACTED

Reference citation: ; eligible engine owner link: True.

- evidence_02: evidence/records/customer_data_snapshot_bundle_20260917.json — captured 2026-09-17T12:00:00Z; file eligible: False
- evidence_92: evidence/records/service_resource_export_20260915_114455.json — captured 2026-09-15T11:44:55Z; file eligible: True

### case_30 / analytics_3697 / VERIFY_RECORD_ANONYMIZED

Reference citation: ; eligible engine owner link: True.

- evidence_02: evidence/records/customer_data_snapshot_bundle_20260917.json — captured 2026-09-17T12:00:00Z; file eligible: False
- evidence_92: evidence/records/service_resource_export_20260915_114455.json — captured 2026-09-15T11:44:55Z; file eligible: True

### case_30 / data_flow_8524 / VERIFY_DATA_FLOW_DISABLED

Reference citation: ; eligible engine owner link: True.

- evidence_02: evidence/records/customer_data_snapshot_bundle_20260917.json — captured 2026-09-17T12:00:00Z; file eligible: False
- evidence_92: evidence/records/service_resource_export_20260915_114455.json — captured 2026-09-15T11:44:55Z; file eligible: True

### case_31 / account_4857 / VERIFY_RECORD_ABSENT

Reference citation: evidence_51; eligible engine owner link: False.

- No exact ID occurrence in supported text sources. Images/PDFs require their actual extraction; this text scan is not proof of absence.

### case_31 / audit_record_6909 / VERIFY_RECORD_PRESENT

Reference citation: evidence_51; eligible engine owner link: True.

- evidence_51: evidence/records/customer_data_snapshot_bundle_20260915.json — captured 2026-09-15T12:00:00Z; file eligible: True

### case_31 / tombstone_440 / VERIFY_RECORD_REDACTED

Reference citation: evidence_51; eligible engine owner link: True.

- evidence_51: evidence/records/customer_data_snapshot_bundle_20260915.json — captured 2026-09-15T12:00:00Z; file eligible: True

### case_32 / account_8858 / VERIFY_RECORD_ABSENT

Reference citation: ; eligible engine owner link: False.

- No exact ID occurrence in supported text sources. Images/PDFs require their actual extraction; this text scan is not proof of absence.

### case_32 / audit_record_7068 / VERIFY_RECORD_PRESENT

Reference citation: ; eligible engine owner link: True.

- evidence_51: evidence/records/customer_data_snapshot_bundle_20260915.json — captured 2026-09-15T12:00:00Z; file eligible: True

### case_32 / tombstone_9178 / VERIFY_RECORD_REDACTED

Reference citation: ; eligible engine owner link: True.

- evidence_51: evidence/records/customer_data_snapshot_bundle_20260915.json — captured 2026-09-15T12:00:00Z; file eligible: True

## Root participant CSV scan

- account_001: system_activity.csv / activity_3342 / 2026-08-20T16:41:43Z
- account_002: system_activity.csv / activity_3376 / 2026-08-22T07:30:03Z
- account_004: no exact token
- account_007: system_activity.csv / activity_3590 / 2026-09-01T19:28:39Z
- account_008: system_activity.csv / activity_3554 / 2026-08-31T13:48:58Z
- account_010: system_activity.csv / activity_3595 / 2026-09-02T10:08:37Z
- account_3136: system_activity.csv / activity_3597 / 2026-09-02T10:48:27Z
- account_3866: system_activity.csv / activity_3530 / 2026-08-30T10:57:28Z
- account_3960: system_activity.csv / activity_3703 / 2026-09-07T07:55:18Z
- account_410: system_activity.csv / activity_3662 / 2026-09-05T11:10:55Z
- account_4163: system_activity.csv / activity_3465 / 2026-08-27T10:55:42Z
- account_4857: system_activity.csv / activity_3682 / 2026-09-06T10:45:58Z
- account_4990: system_activity.csv / activity_3573 / 2026-09-01T09:12:11Z
- account_5037: system_activity.csv / activity_3734 / 2026-09-09T10:14:55Z
- account_5482: system_activity.csv / activity_3529 / 2026-08-30T10:46:13Z
- account_5521: system_activity.csv / activity_3732 / 2026-09-09T09:52:26Z
- account_5684: system_activity.csv / activity_3600 / 2026-09-02T11:08:43Z
- account_6440: system_activity.csv / activity_3661 / 2026-09-05T11:01:53Z
- account_7012: system_activity.csv / activity_3532 / 2026-08-30T11:06:57Z
- account_8858: system_activity.csv / activity_3685 / 2026-09-06T11:05:15Z
