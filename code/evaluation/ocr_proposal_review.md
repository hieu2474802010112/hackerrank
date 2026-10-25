# Review of the supplied all-in-one OCR replacement

The attachment was extracted unchanged to tmp/ocr_proposal/main.py and executed in an isolated output directory on the 32 public requests. The production main.py and root output.csv were not replaced; the output SHA-256 was checked before and after.

| Metric | Supplied replacement | Retained solver |
| --- | --- | --- |
| Status accuracy | 22/32 (68.75%) | 23/32 (71.875%) |
| Exact rows (status and parsed ordered steps) | 0/32 | 9/32 |

Replacement runtime: 22.47 seconds. It reported 14 requests with some textual/SQL/image match; these are not verified ownership or policy determinations. Tesseract is unavailable on this machine, and its OCR wrapper silently catches that failure. It does not use the working local Windows OCR bridge already integrated into the retained solver.

Material issues:

- All evidence and identity history are searched without the audit cutoff; parse_iso_time is never used.
- Any occurrence is treated as a leak; deletion_rules.csv, retention, anonymization, redaction, tombstones and process/restore risks are not evaluated.
- No match becomes COMPLETE without evidence of absence. OCR/parser failures are swallowed and can therefore falsely support COMPLETE.
- account_/search_ resource IDs are synthesized from case_id. Findings and COMPLETE verification cite fixed evidence_54/evidence_92 regardless of source contents.
- Historical emails are collected but not actually passed into the search calls. Phone and historical hash coverage is lost.
- Substring/filename matching permits misleading matches, and SQL/whole-image co-occurrence is not an ownership relationship.
- Numeric case sorting differs from the required lexicographic case_id ordering used by the retained solver.

Decision: retain the existing evidence-grounded implementation and its OCRInspector. No replacement behavior in this attachment establishes a safe improvement. Current validation: 39/39 unit tests; full output has 518 cases, 2,688 valid ordered steps and eligible citations. Coverage remains unresolved for 343 requests. Neither these tests nor schema validity establishes full-dataset correctness.
