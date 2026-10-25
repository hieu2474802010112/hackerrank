# Evaluation Report: Ghost Data Still Exists

## Scope and safeguards

Predictions are computed from participant-facing identity, history, activity, rules and evidence files. The solver never reads public expected outputs; only this evaluator reads them after prediction. No organizer files, case-family labels, hash guesses, fabricated resource IDs or sample-answer lookups are used. All 94 manifest files are opened. SQL, supported JSON/log schemas, verified image transcriptions and resource-bearing PDF text produce observations. Business PDFs without directly mapped resource IDs are retained for review but are not converted into invented resource IDs.

These public samples have been used for debugging, so this is a development-set evaluation, not an independent holdout estimate. Full-dataset accuracy is unknown.

## Measured public-sample metrics

| Metric | Result | Definition |
| --- | --- | --- |
| Status accuracy | 23/32 (71.88%) | Exact deletion_status |
| Exact row accuracy | 9/32 (28.12%) | Status and entire ordered step array |
| Step accuracy | 114/196 (58.16%) | Exact step at the same array position; denominator sums max(predicted, expected) lengths per case |
| Field accuracy | 941/1372 (68.59%) | Seven fields per aligned step; missing/extra positions have seven errors |
| Structural sequence accuracy | 32/32 (100.00%) | Required phase/operation/system/resource order and consecutive step numbers; does not measure semantic completeness |
| Coverage warnings | 23/32 | Missing linked primary state or unreadable required state |

Evaluation runtime: 1.50 seconds.

## Failures found and improvements

- Replaced random hash classification and invented evidence/resource identifiers with evidence-derived resource observations and policy actions.
- Added current and historical exact identity matching, trace-ID joins, nested JSON bundles, service readbacks, multiple log encodings, and SQLite primary/replica inspection.
- Added UTC-aware cutoff checks for both file availability and observation time. Later files cannot establish either state or ownership for an earlier audit.
- Added compact UTF-8 serialization, stable sorting, consecutive numbering, and atomic output writes.
- Missing evidence is not treated as proof of absence. Conservative INCOMPLETE results with coverage warnings are used where no linked primary state is available. These warnings are limitations, not evidence-backed findings.
- Some anonymized/absent resources have no explicit identity-bearing link in eligible evidence. The solver does not guess ownership from numeric IDs or nearby timestamps. This causes sample misses that remain unresolved.
- Old observations and ambiguous catalog links may require richer collection-scope handling; records absent from a partial capture must not be assumed deleted.
- Reviewed image observations are tied to SHA-256 digests. They contain literal source fields, not expected case labels. A changed image requires review rather than silently reusing stale observations.

## Mismatch details

| Case | Predicted | Expected | Predicted steps | Expected steps |
| --- | --- | --- | --- | --- |
| case_01 | INCOMPLETE | COMPLETE | 0 | 1 |
| case_02 | INCOMPLETE | COMPLETE | 0 | 1 |
| case_03 | COMPLETE | COMPLETE | 2 | 3 |
| case_04 | INCOMPLETE | COMPLETE | 0 | 2 |
| case_07 | INCOMPLETE | INCOMPLETE | 6 | 4 |
| case_08 | INCOMPLETE | INCOMPLETE | 3 | 4 |
| case_09 | INCOMPLETE | INCOMPLETE | 3 | 5 |
| case_10 | INCOMPLETE | INCOMPLETE | 3 | 4 |
| case_17 | INCOMPLETE | INCOMPLETE | 6 | 5 |
| case_18 | INCOMPLETE | INCOMPLETE | 12 | 14 |
| case_20 | INCOMPLETE | INCOMPLETE | 6 | 8 |
| case_21 | INCOMPLETE | COMPLETE | 1 | 3 |
| case_22 | INCOMPLETE | INCOMPLETE | 7 | 8 |
| case_23 | INCOMPLETE | INCOMPLETE | 6 | 8 |
| case_24 | INCOMPLETE | INCOMPLETE | 6 | 7 |
| case_25 | INCOMPLETE | COMPLETE | 1 | 3 |
| case_26 | INCOMPLETE | COMPLETE | 4 | 6 |
| case_27 | INCOMPLETE | COMPLETE | 4 | 6 |
| case_28 | INCOMPLETE | COMPLETE | 4 | 6 |
| case_29 | INCOMPLETE | INCOMPLETE | 12 | 14 |
| case_30 | INCOMPLETE | INCOMPLETE | 12 | 14 |
| case_31 | INCOMPLETE | COMPLETE | 2 | 3 |
| case_32 | INCOMPLETE | INCOMPLETE | 4 | 5 |

### Missing and additional step references

**case_01**

Missing compared with public reference: `[('VERIFICATION', 'account_service', 'account_001', 'VERIFY_RECORD_ABSENT', 'evidence_54')]`

Additional compared with public reference: `[]`

**case_02**

Missing compared with public reference: `[('VERIFICATION', 'account_service', 'account_002', 'VERIFY_RECORD_ABSENT', 'evidence_54')]`

Additional compared with public reference: `[]`

**case_03**

Missing compared with public reference: `[('VERIFICATION', 'analytics_platform', 'analytics_9406', 'VERIFY_RECORD_ANONYMIZED', 'evidence_94')]`

Additional compared with public reference: `[]`

**case_04**

Missing compared with public reference: `[('VERIFICATION', 'account_service', 'account_004', 'VERIFY_RECORD_ABSENT', 'evidence_54'), ('VERIFICATION', 'analytics_platform', 'analytics_901', 'VERIFY_RECORD_ANONYMIZED', 'evidence_56')]`

Additional compared with public reference: `[]`

**case_07**

Missing compared with public reference: `[('VERIFICATION', 'account_service', 'account_007', 'VERIFY_RECORD_ABSENT', '')]`

Additional compared with public reference: `[('FINDING', 'object_storage', 'object_19', 'REPORT_REMAINING_RECORD', 'evidence_46'), ('REMEDIATION', 'object_storage', 'object_19', 'DELETE_RECORD', ''), ('VERIFICATION', 'object_storage', 'object_19', 'VERIFY_RECORD_ABSENT', '')]`

**case_08**

Missing compared with public reference: `[('VERIFICATION', 'account_service', 'account_008', 'VERIFY_RECORD_ABSENT', '')]`

Additional compared with public reference: `[]`

**case_09**

Missing compared with public reference: `[('VERIFICATION', 'account_service', 'account_3960', 'VERIFY_RECORD_ABSENT', ''), ('VERIFICATION', 'security_service', 'audit_record_4902', 'VERIFY_RECORD_PRESENT', '')]`

Additional compared with public reference: `[]`

**case_10**

Missing compared with public reference: `[('VERIFICATION', 'account_service', 'account_010', 'VERIFY_RECORD_ABSENT', '')]`

Additional compared with public reference: `[]`

**case_17**

Missing compared with public reference: `[]`

Additional compared with public reference: `[('VERIFICATION', 'account_service', 'account_6523', 'VERIFY_RECORD_ABSENT', '')]`

**case_18**

Missing compared with public reference: `[('VERIFICATION', 'account_service', 'account_5521', 'VERIFY_RECORD_ABSENT', ''), ('VERIFICATION', 'security_service', 'audit_record_6645', 'VERIFY_RECORD_PRESENT', '')]`

Additional compared with public reference: `[]`

**case_20**

Missing compared with public reference: `[('VERIFICATION', 'account_service', 'account_5037', 'VERIFY_RECORD_ABSENT', ''), ('VERIFICATION', 'security_service', 'audit_record_5569', 'VERIFY_RECORD_PRESENT', '')]`

Additional compared with public reference: `[]`

**case_21**

Missing compared with public reference: `[('VERIFICATION', 'account_service', 'account_6440', 'VERIFY_RECORD_ABSENT', 'evidence_92'), ('VERIFICATION', 'analytics_platform', 'analytics_5335', 'VERIFY_RECORD_ANONYMIZED', 'evidence_92'), ('VERIFICATION', 'security_service', 'audit_record_3737', 'VERIFY_RECORD_PRESENT', 'evidence_92')]`

Additional compared with public reference: `[('VERIFICATION', 'security_service', 'audit_record_3737', 'VERIFY_RECORD_PRESENT', '')]`

**case_22**

Missing compared with public reference: `[('VERIFICATION', 'account_service', 'account_4990', 'VERIFY_RECORD_ABSENT', '')]`

Additional compared with public reference: `[]`

**case_23**

Missing compared with public reference: `[('VERIFICATION', 'account_service', 'account_410', 'VERIFY_RECORD_ABSENT', ''), ('VERIFICATION', 'security_service', 'audit_record_4128', 'VERIFY_RECORD_PRESENT', '')]`

Additional compared with public reference: `[]`

**case_24**

Missing compared with public reference: `[('VERIFICATION', 'security_service', 'audit_record_7095', 'VERIFY_RECORD_PRESENT', '')]`

Additional compared with public reference: `[]`

**case_25**

Missing compared with public reference: `[('VERIFICATION', 'account_service', 'account_3136', 'VERIFY_RECORD_ABSENT', 'evidence_92'), ('VERIFICATION', 'analytics_platform', 'analytics_1895', 'VERIFY_RECORD_ANONYMIZED', 'evidence_92'), ('VERIFICATION', 'security_service', 'audit_record_451', 'VERIFY_RECORD_PRESENT', 'evidence_92')]`

Additional compared with public reference: `[('VERIFICATION', 'security_service', 'audit_record_451', 'VERIFY_RECORD_PRESENT', '')]`

**case_26**

Missing compared with public reference: `[('VERIFICATION', 'account_service', 'account_5684', 'VERIFY_RECORD_ABSENT', 'evidence_92'), ('VERIFICATION', 'analytics_platform', 'analytics_4566', 'VERIFY_RECORD_ANONYMIZED', 'evidence_92'), ('VERIFICATION', 'backup_service', 'backup_3120', 'VERIFY_RESTORE_BLOCKED', 'evidence_92'), ('VERIFICATION', 'integration_service', 'data_flow_6244', 'VERIFY_DATA_FLOW_DISABLED', 'evidence_92'), ('VERIFICATION', 'security_service', 'audit_record_5416', 'VERIFY_RECORD_PRESENT', 'evidence_92'), ('VERIFICATION', 'support_platform', 'support_4715', 'VERIFY_RECORD_REDACTED', 'evidence_92')]`

Additional compared with public reference: `[('VERIFICATION', 'backup_service', 'backup_3120', 'VERIFY_RESTORE_BLOCKED', ''), ('VERIFICATION', 'integration_service', 'data_flow_6244', 'VERIFY_DATA_FLOW_DISABLED', ''), ('VERIFICATION', 'security_service', 'audit_record_5416', 'VERIFY_RECORD_PRESENT', ''), ('VERIFICATION', 'support_platform', 'support_4715', 'VERIFY_RECORD_REDACTED', '')]`

**case_27**

Missing compared with public reference: `[('VERIFICATION', 'account_service', 'account_3866', 'VERIFY_RECORD_ABSENT', 'evidence_92'), ('VERIFICATION', 'analytics_platform', 'analytics_4574', 'VERIFY_RECORD_ANONYMIZED', 'evidence_92'), ('VERIFICATION', 'backup_service', 'backup_5970', 'VERIFY_RESTORE_BLOCKED', 'evidence_92'), ('VERIFICATION', 'integration_service', 'data_flow_2295', 'VERIFY_DATA_FLOW_DISABLED', 'evidence_92'), ('VERIFICATION', 'security_service', 'audit_record_3830', 'VERIFY_RECORD_PRESENT', 'evidence_92'), ('VERIFICATION', 'support_platform', 'support_4707', 'VERIFY_RECORD_REDACTED', 'evidence_92')]`

Additional compared with public reference: `[('VERIFICATION', 'backup_service', 'backup_5970', 'VERIFY_RESTORE_BLOCKED', ''), ('VERIFICATION', 'integration_service', 'data_flow_2295', 'VERIFY_DATA_FLOW_DISABLED', ''), ('VERIFICATION', 'security_service', 'audit_record_3830', 'VERIFY_RECORD_PRESENT', ''), ('VERIFICATION', 'support_platform', 'support_4707', 'VERIFY_RECORD_REDACTED', '')]`

**case_28**

Missing compared with public reference: `[('VERIFICATION', 'account_service', 'account_5482', 'VERIFY_RECORD_ABSENT', 'evidence_92'), ('VERIFICATION', 'analytics_platform', 'analytics_6077', 'VERIFY_RECORD_ANONYMIZED', 'evidence_92'), ('VERIFICATION', 'backup_service', 'backup_838', 'VERIFY_RESTORE_BLOCKED', 'evidence_92'), ('VERIFICATION', 'integration_service', 'data_flow_2337', 'VERIFY_DATA_FLOW_DISABLED', 'evidence_92'), ('VERIFICATION', 'security_service', 'audit_record_9265', 'VERIFY_RECORD_PRESENT', 'evidence_92'), ('VERIFICATION', 'support_platform', 'support_2351', 'VERIFY_RECORD_REDACTED', 'evidence_92')]`

Additional compared with public reference: `[('VERIFICATION', 'backup_service', 'backup_838', 'VERIFY_RESTORE_BLOCKED', ''), ('VERIFICATION', 'integration_service', 'data_flow_2337', 'VERIFY_DATA_FLOW_DISABLED', ''), ('VERIFICATION', 'security_service', 'audit_record_9265', 'VERIFY_RECORD_PRESENT', ''), ('VERIFICATION', 'support_platform', 'support_2351', 'VERIFY_RECORD_REDACTED', '')]`

**case_29**

Missing compared with public reference: `[('VERIFICATION', 'account_service', 'account_7012', 'VERIFY_RECORD_ABSENT', ''), ('VERIFICATION', 'security_service', 'audit_record_3954', 'VERIFY_RECORD_PRESENT', '')]`

Additional compared with public reference: `[]`

**case_30**

Missing compared with public reference: `[('VERIFICATION', 'account_service', 'account_4163', 'VERIFY_RECORD_ABSENT', ''), ('VERIFICATION', 'security_service', 'audit_record_1707', 'VERIFY_RECORD_PRESENT', '')]`

Additional compared with public reference: `[]`

**case_31**

Missing compared with public reference: `[('VERIFICATION', 'account_service', 'account_4857', 'VERIFY_RECORD_ABSENT', 'evidence_51'), ('VERIFICATION', 'identity_service', 'tombstone_440', 'VERIFY_RECORD_REDACTED', 'evidence_51'), ('VERIFICATION', 'security_service', 'audit_record_6909', 'VERIFY_RECORD_PRESENT', 'evidence_51')]`

Additional compared with public reference: `[('VERIFICATION', 'identity_service', 'tombstone_440', 'VERIFY_RECORD_REDACTED', ''), ('VERIFICATION', 'security_service', 'audit_record_6909', 'VERIFY_RECORD_PRESENT', '')]`

**case_32**

Missing compared with public reference: `[('VERIFICATION', 'account_service', 'account_8858', 'VERIFY_RECORD_ABSENT', '')]`

Additional compared with public reference: `[]`

## Coverage warnings

- case_01: No identity-linked primary account state
- case_02: No identity-linked primary account state
- case_04: No identity-linked primary account state
- case_07: No identity-linked primary account state
- case_08: tombstone_17: ambiguous resource ownership; No identity-linked primary account state
- case_09: No identity-linked primary account state
- case_10: No identity-linked primary account state
- case_12: tombstone_17: ambiguous resource ownership
- case_17: tombstone_17: ambiguous resource ownership
- case_18: No identity-linked primary account state
- case_20: No identity-linked primary account state
- case_21: tombstone_17: ambiguous resource ownership; No identity-linked primary account state
- case_22: No identity-linked primary account state
- case_23: No identity-linked primary account state
- case_24: tombstone_17: ambiguous resource ownership
- case_25: No identity-linked primary account state
- case_26: No identity-linked primary account state
- case_27: No identity-linked primary account state
- case_28: No identity-linked primary account state
- case_29: tombstone_17: ambiguous resource ownership; No identity-linked primary account state
- case_30: No identity-linked primary account state
- case_31: No identity-linked primary account state
- case_32: No identity-linked primary account state

## Additional evaluation cases

Executable tests are in `code/evaluation/test_audit.py`; run `python -m unittest discover -s code/evaluation -p "test_*.py" -v`. Test results are recorded below after execution.

1. Historical email and hash aliases with a near-match decoy; a post-cutoff evidence file must neither add resources nor change the decision.
2. Primary/replica drift: a profile absent from primary but present on a replica must remain a deletion violation.
3. Tombstone redaction and mandatory retention: stable internal user references remain; names/contact fields are removed and required security records are retained.
4. Active integration and restore risks: disabling the flow and blocking restore precede record remediation, with complete future verification and empty future evidence citations.
5. Missing input files and malformed timestamps fail explicitly instead of fabricating COMPLETE results.
6. Non-deletion and mixed-language request classification, repeated-run determinism, and changed-image digest rejection.

## Final readiness review

Rechecked 39/39 tests, sample metrics, 518-row/2,688-step validation and 343 coverage warnings. The packaged solver ran after extraction and reproduced output.csv byte for byte. case_55 has an empty INCOMPLETE plan, exposing unresolved evidence rather than a complete audit. See readiness_report.md; structural validity is not prediction correctness.
