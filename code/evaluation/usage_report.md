# Token Usage and Cost Analysis Report

## Latest full run

The current evidence-grounded solver processed **518 requests** in **4.68 seconds**, producing 2,688 steps after the evidence_48 pipe-log parser repair. Status distribution: `{'INCOMPLETE': 457, 'COMPLETE': 51, 'NOT_APPLICABLE': 10}`. Output SHA-256: `fa637194c35dacdc9a6134c664a1b1a97320a01aa24dc5ada795cab5bc2ac2eb`.

Prediction and document diagnostics use local Python, SQLite and PyMuPDF with reviewed SHA-256-verified source-image fields. The optional local Windows en-US OCR diagnostic was executed on the 11 supplied images; it made no remote API calls. Its 39.69-second full run found 8 requests with eligible identifier matches but did not change predictions. OCR text requires review before any ownership/state promotion; no OCR API billing applies.

| Component | Provider / model | Calls | Input tokens | Output tokens | Total tokens | Estimated API cost (USD) |
| --- | --- | --- | --- | --- | --- | --- |
| Full audit inference | No runtime model | 0 | 0 | 0 | 0 | 0.00 |
| Overall inference total | Local computation | 0 | 0 | 0 | 0 | 0.00 |

Average input/output/total tokens per request: **0 / 0 / 0**. Estimated inference model API cost per request: **USD 0.00**.

## Accounting limits

Development and visual review use Codex with OpenAI model `gpt-6.1-sol` verified in session metadata. Authoring conversation tokens, subscription charges and development costs are unavailable from the audit runtime and are not included in the zero inference figures. Local computing costs are not estimated. The earlier candidate scripts were evaluated locally and made no model API calls.

The full run still has **343 coverage-warning cases**. Public results remain 23/32 correct statuses and 9/32 exact rows; full-dataset correctness is unknown. The output is best effort and not a fully verified submission.
