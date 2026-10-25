# HackerRank Orchestrate - October 2026

## Ghost Data Still Exists

Build an AI agent that audits whether a user's personal data was actually deleted.

A deletion workflow may report **Complete** while data still exists in databases, logs, support attachments, exports, search indexes, archives, or backups. Sync and restore processes may also bring deleted data back.

For each request, the agent must first determine whether deletion was actually requested. It then returns `COMPLETE`, `INCOMPLETE`, or `NOT_APPLICABLE`, reports any remaining data or recreation risk, and produces the ordered remediation and verification steps required to finish an authorized deletion safely.

Read [`problem_statement.md`](./problem_statement.md) for the complete challenge contract.

---

## Quick Start

Clone the repository and move into the project directory:

```bash
git clone https://github.com/interviewstreet/hackerrank-orchestrate-october26.git
cd hackerrank-orchestrate-october26
```

Start your AI coding tool from the **repository root** so it automatically reads [`AGENTS.md`](./AGENTS.md) and logs your session turns to `log.txt` in the root directory.

Build your solution in `code/main.py`, or use another language and document its setup and run command clearly in your README.

Your solution must:

- Read the input files from `dataset/`
- Generate one prediction row for every request in `dataset/deletion_requests.csv`
- Write the final predictions to `output.csv` in the repository root

Run the starter Python entry point with:

```bash
python3 code/main.py
```

The blank template at `dataset/output.csv` is provided as a reference. Your final generated file for submission must be the root-level `output.csv`.


## Dataset

All participant-facing files are in `dataset/`:

| File | Contents |
| --- | --- |
| `deletion_requests.csv` | 518 requests |
| `sample_deletion_requests.csv` | 32 sample requests |
| `sample_output.csv` | Correct sample answers |
| `user_identities.csv` | Current user identities |
| `user_audit_log.csv` | Historical identity changes |
| `system_activity.csv` | Activity across services and data processes |
| `deletion_rules.csv` | Required treatment for each data category |
| `evidence_files.csv` | Manifest of supplied evidence files |
| `output.csv` | Blank output template |

Evidence is stored under `dataset/evidence/` and may include PDFs, images, logs, JSON, plain text, or SQL snapshot exports. SQL captures may contain a primary database, regional replicas, a reporting replica, or a failover replica so replication drift can be investigated directly. The `.sql` files are readable as text and executable with SQLite.

Only `deletion_requests.csv` requires answers. The other files provide evidence and context.

---

## Output

Create `output.csv` with these columns in this exact order:

```text
case_id,deletion_status,steps_json
```

Produce exactly one row per request. `deletion_status` is `COMPLETE`, `INCOMPLETE`, or `NOT_APPLICABLE`. `steps_json` is an ordered JSON array containing findings, remediation actions, and verification checks. Use an empty array (`[]`) for `NOT_APPLICABLE`. Evidence references may be a `file_id`, `activity_id`, or `audit_id`. Determine the resource state at `audit_at` from the available evidence; reported workflow statuses and operation results are claims. Use `dataset/sample_output.csv` as the format reference.

The final file must contain 518 data rows sorted by `case_id` (plus the header row). The grader parses `steps_json` as JSON, so object-key order and whitespace do not matter; array order does. Order findings, remediation, and verification in that phase order. Within a phase, follow the operation order in the problem statement, then sort by `system_id` and `resource_id`.

---

## Evaluation

`output.csv` will be compared with hidden canonical answers. Scoring considers:

- deletion assessment accuracy;
- current and historical identity resolution;
- discovery of remaining data and recreation risks;
- correct policy application and evidence references; and
- completeness and ordering of remediation and verification steps.

Your `code.zip` must include:

```text
code/evaluation/evaluation_report.md
code/evaluation/usage_report.md
```

- `evaluation_report.md` must cover case, row, field, and sequence accuracy, at least three additional evaluation cases created by you, failures found, and improvements made.
- `usage_report.md` must cover the final full-dataset run, including model providers and names, model calls, input and output tokens, total and average tokens per request, and estimated total and per-request cost. Include per-model and overall totals when using multiple models.

**Important:** Place `evaluation_report.md` and `usage_report.md` inside `code/evaluation/` (matching `code/evaluation/main.py` in this starter layout), write your complete evaluation metrics, custom evaluation test cases, and token/cost breakdowns directly inside those Markdown files, and keep prompts in source code or Markdown files. Automated code evaluation ignores raw data files (`.csv`, `.tsv`, `.json`, `.jsonl`, `.sql`, `.log`), so content stored only in those formats will not be visible to the code judge or AI interviewer.

---

## Chat Transcript

This repository includes [`AGENTS.md`](./AGENTS.md), which instructs compatible AI coding tools to append conversation summaries to `log.txt` in the repository root:

| Platform | Path |
| --- | --- |
| macOS / Linux | `<repo root>/log.txt` |
| Windows | `<repo root>\log.txt` |

- Always launch your AI coding agent from the repository root (or explicitly ask it to read `./AGENTS.md` first) so every turn is logged to `log.txt` with the required `User Prompt`, `Agent Response Summary`, `Actions`, and `Context` sections.
- Upload `log.txt` directly as your `chat_transcript` submission on HackerRank.
- Do not include API keys, tokens, credentials, or secrets in prompts, code, configuration, or `log.txt`.

---

## Packaging `code.zip` and Submission

| Item | Description |
| --- | --- |
| `code.zip` | Runnable solution, prompts, configuration, `README.md`, and `evaluation/` reports |
| `output.csv` | One answer row for each of the 518 requests in `dataset/deletion_requests.csv` |
| `chat_transcript` | The root `log.txt` file generated by your coding agent |
| AI interview | Live explanation of your architecture, approach, and evaluation |

You may use any programming language, model, framework, or retrieval approach. Include clear setup and execution instructions in `README.md` inside `code.zip`.

To package `code.zip` from the repository root without bundling the dataset:

**macOS / Linux:**

```bash
zip -r code.zip README.md code -x "*/__pycache__/*" "*/.venv/*" "*/venv/*" "*/node_modules/*" "*/.git/*" "*/.DS_Store"
```

**Windows (PowerShell):**

```powershell
Compress-Archive -Path README.md, code -DestinationPath code.zip -Force
```

When packaging `code.zip`:

- Keep your evaluation reports in `code/evaluation/` so they are bundled automatically with `code` (or add `evaluation` to the archive command above if you placed them in a top-level `evaluation/` directory).
- Do **not** include `dataset/`, virtual environments (`.venv`, `venv`, `node_modules`), or build caches (`__pycache__`). On Windows, keep `.venv` at the repository root (outside `code/`) and remove any `code/__pycache__` folders before running `Compress-Archive`.
- Do **not** include nested archives (`.zip`, `.tar`, `.gz`, `.tgz`, `.7z`, `.rar`) inside `code.zip` — submissions containing nested archive files will be rejected.

Before submitting, confirm that:

- `output.csv` has the exact header `case_id,deletion_status,steps_json` and contains all 518 data rows sorted by `case_id`;
- every `steps_json` value is a valid JSON array with consecutive step numbers starting at `1`;
- findings cite valid evidence IDs, and `COMPLETE` verification steps cite evidence proving the current state;
- proposed remediation and future verification steps use an empty `evidence_id` (`""`);
- `code.zip` includes your runnable code, `README.md`, `code/evaluation/evaluation_report.md`, and `code/evaluation/usage_report.md`;
- `log.txt` follows the `AGENTS.md` turn format and is uploaded to the `chat_transcript` slot; and
- no API keys, credentials, real personal data, or sensitive configuration values are included.


## Evidence-grounded Python implementation

Install Python 3.10+ and the PDF reader, then run from the repository root:

```powershell
python -m pip install -r code/requirements.txt
python -X utf8 code/main.py
python -X utf8 code/evaluation/main.py
python -X utf8 -m unittest discover -s code/evaluation -p "test_*.py" -v
```

`code/main.py` resolves the dataset relative to its location and writes the root `output.csv`. Override paths using `--dataset`, `--requests`, and `--output`. Run `python -X utf8 code/main.py --strict` to refuse output when evidence coverage is unresolved; strict failure leaves any existing output unchanged.

The solver resolves exact current/historical identifiers, joins log lines by trace IDs, executes supplied SQL captures in isolated in-memory SQLite databases, compares replicas, reads JSON snapshots and service exports, and extracts PDF text. It checks both evidence availability and observation time against `audit_at`. Activity completion claims are not deletion proof. Policies determine delete/redact/anonymize/retain actions; flow and restore changes precede record remediation.

The eleven supplied PNGs were visually reviewed during development. Literal resource fields and source SHA-256 digests are recorded in `code/image_observations.md`. Predictions verify these digests before applying the observations. This is a reviewed extraction cache, not case-answer data; changed images require a new review. No model API is invoked by the final script.

The current implementation remains incomplete: some absent or anonymized resources have no identity-bearing link in the evidence handled by this resolver. Ambiguous/missing primary-account coverage produces a conservative `INCOMPLETE` result and a warning, not a fabricated finding or a claim of proven noncompliance. See the measured public-sample metrics and detailed mismatch list in `code/evaluation/evaluation_report.md` and full-run coverage warnings in `code/evaluation/coverage_report.md`. Public-sample accuracy does not establish accuracy on the 518 unseen cases. The default output is best effort; it is not a fully verified submission.

Public expected answers are read only by the evaluation script, after predictions have been computed. The prediction engine does not read `sample_output.csv` or organizer files, and does not infer resource IDs from case numbers.


### Inspect SQL evidence for one subject

The reusable `EvidenceInspector` in `code/evidence_inspector.py` provides `load_sql_snapshot`, `search_user_in_snapshot`, and `audit_user_across_all_snapshots`. The audit engine shares its SQL loader. For a diagnostic query:

```powershell
python -X utf8 code/evidence_inspector.py --user-id user_05 --email leila.haddad@yahoo.com --audit-at 2026-09-08T13:40:00Z
```

Add `--identifier` repeatedly for a historical email, phone or hash. Only manifest-listed SQL files captured at or before the cutoff are scanned. The helper returns file IDs, capture times, table names, matched identifiers and parsed nested JSON. Matching uses complete identifiers instead of SQL `LIKE` wildcards; rows matching both user ID and email are returned once. Malformed SQL/JSON raises an error rather than silently producing no matches. Caller-owned snapshot connections must be closed; the cross-snapshot method closes its own connections.

These are matching records, not automatically privacy violations: retained audit records and correctly redacted tombstones can legitimately remain. Conversely, zero SQL matches alone does not prove deletion across logs, JSON, support documents or other services. The main audit engine applies the policy and combines evidence formats.


### Analyze unresolved evidence coverage

```powershell
python -X utf8 code/evaluation/analyze_coverage.py
```

This writes `code/evaluation/coverage_report.md` with measured reason groups, eligible historical alias counts, linked source IDs, unattributed primary-readback counts and later identity links excluded from predictions. It reads no public expected answers. Later evidence is inspected only to explain why a link cannot establish an earlier audit; it is not sent to the prediction engine.

Current retrieval improvements resolve explicit source/parent foreign keys in both directions through complete connected components. They can link an absent profile back to a surviving search document without deriving resource IDs from user or case numbers. Phone punctuation is normalized without guessing country codes; historical-email SHA-256 hashes are derived only after validating that algorithm against every supplied current identity. Snapshot state remains separate from ownership/routing activity.


### Inspect identity-bearing system activity

```powershell
python -X utf8 code/system_activity_mapper.py --email g.silva76@gmail.com --user-id user_13 --audit-at 2026-09-02T08:00:00Z
```

The dedicated `SystemActivityMapper` indexes complete identifiers, enforces the event cutoff, preserves matching activity IDs and follows anonymous history only for the same explicitly linked resource. `AuditEngine` uses this ownership index. `deduce_resource_state` returns workflow claims separately as `claimed_state`; `status` stays `UNKNOWN`, `verified` stays false and state `evidence_id` stays empty until independent evidence establishes state. A successful DELETE/SYNC/ANONYMIZE event is not a verification readback.

Measured activity counts and a per-case diagnosis are recorded in `code/evaluation/activity_mapping_report.md`. The supplied dataset has 4,011 activity rows but only 12 identity-bearing rows; these were already covered by the previous details scanner. The mapper improves inspection/provenance and regression coverage, but no accuracy or coverage gain was measured from this refactor.


### Deep SQL diagnostic with declared joins

```powershell
python -X utf8 code/sqlite_deep_query.py --user-id user_05 --email leila.haddad@yahoo.com --audit-at 2026-09-08T13:40:00Z
```

Add `--identifier` for each known historical email, phone or hash. The helper searches nested JSON, normalizes only the same international phone digits and executes only foreign-key joins declared by the database (including composite keys). Matching column names or nearby IDs are not enough to invent a join. File, row and collection-scope cutoffs remain mandatory.

`--include-md5` enables explicitly unverified MD5 diagnostic candidates; it does not add them to the main ownership index. Matches have `policy_verdict: null` because retained records may legitimately remain. The current prediction entry point continues to use the validated SHA-256/historical identity resolver and policy engine. See `code/evaluation/deep_sql_report.md` for measured schema findings and the comparison with the supplied replacement, which was not promoted.


### Search unstructured evidence with source locations

```powershell
python -X utf8 code/unstructured_inspector.py --identifier priya.raman@gmail.com --audit-at 2026-09-12T08:00:00Z
```

Repeat `--identifier` for historical emails, user IDs, phones or hashes. Searches inspect manifest-listed PDF, TXT, LOG, CSV and reviewed PNG/JPG fields within the cutoff. Results include page/line/row locations, matched identifiers and resource mentions; `policy_verdict` remains null. The main PDF reader uses this module. Text mentions are never promoted directly to a deletion finding.

PDF extraction uses PyMuPDF text layers, not raw binary strings. Predictions use the existing reviewed image extraction cache with source hashes. Scanned PDFs report that OCR is required.

### Local image OCR diagnostics

```powershell
python -X utf8 code/main.py --ocr-report tmp/ocr_matches.json
```

`OCRInspector` uses an available Tesseract executable with optional Pillow/pytesseract, or Windows native English OCR via the included `windows_ocr.ps1`. Windows OCR requires the installed en-US recognition language. No image is sent to a remote service. Other environments without an OCR engine fail explicitly when OCR is requested; normal predictions remain portable through reviewed image fields.

The diagnostic searches exact current/historical identifiers known by each audit cutoff, only in eligible manifest images. It caches text by source SHA-256, preserves backend/language and returns `requires_review: true`, `policy_verdict: null`. Filenames are not content evidence. OCR errors such as `user_11` becoming `user_ll` are not silently corrected, and identifiers or resources sharing a screenshot are not automatically joined. OCR reports do not alter predictions. See `code/evaluation/ocr_report.md` for measured results.

The search exposed the pipe-delimited log format in evidence_48; its service/event/trace columns are now parsed explicitly. Current full-run warnings fell from 353 to 343. See `code/evaluation/unstructured_report.md` for current retrieval counts, proposal comparison and limitations. Regenerate the full output with `python -X utf8 code/main.py` and inspect `code/evaluation/coverage_report.md` for unresolved cases.
