> Historical diagnostic snapshot: the later unstructured investigation repaired evidence_48 parsing, reducing current full-run warnings to 343. See unstructured_report.md and coverage_report.md for the current output; older counts/digests below describe the earlier run.

# Review of supplied replacement main.py

The attachment was extracted without changing its Python code and saved at `tmp/candidate_review/main.py`. Its AuditEngine was instantiated against the supplied dataset; only its request DataFrame was replaced by the 32 public sample requests. It ran in a temporary working directory so it could not overwrite the current submission output. Public answers were read only after predictions.

| Metric | Supplied replacement | Current solver baseline |
| --- | --- | --- |
| Correct sample statuses | 15/32 (46.88%) | 23/32 (71.88%) |
| Exact sample rows | 0/32 (0.00%) | 9/32 (28.12%) |

False COMPLETE compared with the public reference: `['case_05', 'case_06', 'case_07', 'case_08', 'case_09', 'case_10', 'case_11', 'case_12', 'case_13', 'case_14', 'case_15', 'case_16', 'case_17', 'case_18', 'case_19', 'case_20', 'case_22']`.
Findings whose cited text file does not contain their purported resource ID: 5. This is a literal-resource diagnostic, not complete semantic validation.

## Material regressions

- SQLite is imported but no SQL snapshot is loaded or queried.
- The deletion policy file is never read. All detected matches become search-record deletions regardless of category or retention requirements.
- Resources are constructed from the case suffix instead of taken from evidence.
- Finding citations use the globally latest eligible file, even if a different file contained the matched email.
- A plain substring match anywhere in any eligible JSON file is called a leak; no latest resource state is reconstructed.
- No email match produces COMPLETE, although missing evidence does not prove absence.
- A historical request email cannot resolve user_id unless it also matches the current identity snapshot. Phones and hashes are omitted, and history timestamps are not filtered.
- Final case ordering is numeric rather than the required string ordering; invalid times silently become naive datetime.min.
- Logs, PDF and image observations are omitted, as are safe handling and tests for unresolved evidence coverage.

The candidate has not replaced code/main.py or the root output.csv. Its source is retained outside the code package for review. The current solver still has 353 unresolved coverage cases; preserving it does not establish submission readiness.
