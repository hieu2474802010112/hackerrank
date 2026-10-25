# Local OCR evaluation

Windows native en-US OCR was exercised through the included PowerShell bridge. Tesseract is not on PATH; no installation or remote OCR API was used. All 11 manifest-listed images were eligible for at least one request and processed successfully during the full diagnostic run.

## Results

- Full diagnostic run: 518 requests, 39.69 seconds including solver, local OCR and alias lookup.
- Exact eligible image-text matches: 8 requests across 7 distinct source images. These counts are retrieval results, not newly resolved requests.
- Matching uses current and cutoff-eligible historical email/user/phone/hash identifiers. File capture times must not exceed audit_at.
- Main predictions remain unchanged: 51 COMPLETE, 457 INCOMPLETE, 10 NOT_APPLICABLE; 343 coverage-warning cases. Output has 518 rows and 2,688 valid steps.
- Public sample: 23/32 correct statuses; 9/32 exact rows. 39/39 unit tests pass.

| Case | Sources | Matched identifiers |
| --- | --- | --- |
| case_33 | evidence_23 | ingrid.dahl@outlook.com |
| case_34 | evidence_04 | haruka.s1838@zoho.com, tel:+819076102507 |
| case_35 | evidence_09 | g.silva76@gmail.com, user_13 |
| case_39 | evidence_14 | jain.aditi@gmail.com |
| case_45 | evidence_37 | user_03 |
| case_50 | evidence_19 | darwish.omar@icloud.com, user_20 |
| case_52 | evidence_23 | ingrid.dahl@outlook.com |
| case_53 | evidence_28 | kagyeman8947@fastmail.com |

## Interpretation and limits

The first OCR result misread user_11 as user_ll and inserted whitespace in account_5762. No fuzzy ID correction is applied. All matched screenshots already have source-hash-verified reviewed fields used by the solver. No additional ownership edge or policy state has been established from the OCR text in this change. A page-wide match does not join all its resource IDs to that person, especially in search results with decoys.

OCR results include source SHA-256, backend/language, original text, requires_review=true and policy_verdict=null. Filenames never establish content. Empty extraction or missing engines raise explicit errors. Cached results invalidate when source bytes change. Regression tests cover exact matching versus near matches, future captures, filename-only matches, changed source hashes, empty queries and backend failures.

Normal predictions continue to use reviewed image records; --ocr-report is an explicit diagnostic. A future image requires review before extracted ownership or state enters predictions. Windows native OCR requires Windows PowerShell and the en-US language pack; optional Tesseract requires its executable plus Pillow/pytesseract. No extra Python package is required for the Windows backend.
