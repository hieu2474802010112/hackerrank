# Case 55 and environment recheck

Created an isolated .venv in the repository and installed the pinned PyMuPDF==1.28.0 requirement. Ran all 39 tests successfully. Full run to tmp/reverified_output.csv took 6.03 seconds, passed structural validation (518 cases, 2,688 steps), and was byte-identical to the existing output.csv (SHA-256 fa637194c35dacdc9a6134c664a1b1a97320a01aa24dc5ada795cab5bc2ac2eb). Predictions and 343 coverage warnings are unchanged.

Inspected original evidence_32 visually again. It shows backup_9287 for the subject email, its archive path, creation time, AES-256 encryption, checksum, last drill and retention end. It does not expose a restore permission or restore-blocked field. Other archives' restore activity is not state proof for backup_9287. Rule_14 requires RETAIN for BACKUP_ARCHIVE under condition "Restore access can be blocked". Archive presence alone is therefore not a deletion violation or proof of active restore access. No fabricated restore-risk or deletion steps were added.

case_55 remains unresolved, not proven compliant. Its primary account link is available only after the audit cutoff, and its eligible backup restore state remains UNKNOWN. No sample labels or output rows were manually changed.

To repeat the checks without relying on system PATH:

    .\.venv\Scripts\python.exe -X utf8 -m unittest discover -s code/evaluation -p test_*.py
    .\.venv\Scripts\python.exe -X utf8 code/main.py --output tmp/reverified_output.csv
    .\.venv\Scripts\python.exe -X utf8 code/evaluation/validate_output.py --output tmp/reverified_output.csv

The virtual environment must remain excluded from submission archives. Trace files are still active-session snapshots, not post-exit exports.
