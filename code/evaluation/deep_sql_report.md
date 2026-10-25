> Historical diagnostic snapshot: the later unstructured investigation repaired evidence_48 parsing, reducing current full-run warnings to 343. See unstructured_report.md and coverage_report.md for the current output; older counts/digests below describe the earlier run.

# Deep SQLite inspection and proposal comparison

## Snapshot schema audit

- All 24 manifest-listed SQL snapshots were executed in isolated in-memory SQLite databases.
- Declared foreign-key joined rows: 0. The schema audit found zero declared foreign-key relations.
- The only audit-named table is security_audit_records. It stores retained security events, not old/new identity changes. No user_audit_log table exists inside these snapshots; identity history remains in the supplied CSV.
- Existing customer_reference / subject_reference / user_id values are already checked against current and historical subject identifiers by the main solver.
- Non-empty hash fields in SQL rows: `{('email_hash', 64): 39}`. No 32-character MD5-valued hash fields were observed in this scan. This is a field-length observation, not a proof that no other encoding exists.

## Implemented diagnostic

- Added code/sqlite_deep_query.py using the existing exact-identity SQLite reader and mandatory manifest/file/row/scope cutoffs.
- It retrieves nested record_json hashes; supplied phone/historical identifiers can be passed with --identifier.
- Joins use PRAGMA-declared FK columns, including composite and implicit primary-key references, with explicit provenance. Matching column names alone do not create a relationship.
- SHA-256 email candidates are searched. MD5 is opt-in (--include-md5), marked unverified, and is not inserted into the main ownership index.
- Returned rows carry policy_verdict=null; retained security rows and compliant tombstones are not automatically classified as leaks.
- The module is an inspection tool; the validated main.py remains the prediction entry point. No automatic claim that deep_hits implies INCOMPLETE is added.

## Supplied replacement main.py

The attachment was saved unchanged to tmp/sqlite_deep_proposal/main.py and run against the 32 public requests in a temporary working directory. Only its request DataFrame was changed to the public requests. Existing source and output were preserved.

| Metric | Supplied replacement | Current solver |
| --- | --- | --- |
| Correct sample statuses | 13/32 | 23/32 |
| Exact sample rows | 0/32 | 9/32 |

The supplied replacement scans future snapshots, invents resource IDs and fixed evidence_54/evidence_92 citations, does not apply deletion_rules.csv, and labels any match as a leak. It cannot replace the current solver safely. It also does not actually execute JOINs; parsing record_json happens only after its initial filters, which can miss hash-only matches inside JSON.

## Validation and remaining limitations

- 29/29 synthetic tests passed, including six new tests for nested hash retrieval, declared composite joins, refusal to infer joins, future capture/scope exclusion, explicitly unverified MD5 candidates, and phone-format/near-number discrimination.
- Real lookup for user_05 returns account_005 in customer_profiles_failover_replica, citing evidence_54.
- No measured reduction of the 353 coverage-warning cases is claimed. Main sample accuracy remains 23/32 statuses and 9/32 exact rows; the earlier full output is unchanged.
