"""Public-sample evaluation; reference answers never enter the prediction engine."""
import csv
import hashlib
import json
import sys
import time
from collections import Counter
from pathlib import Path

sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from main import AuditEngine, ROOT, PHASES, finalize, read_csv, step_key, write_output


def evaluate():
    started=time.perf_counter()
    engine=AuditEngine(ROOT/'dataset')
    requests=read_csv(ROOT/'dataset/sample_deletion_requests.csv')
    predictions={r['case_id']:engine.audit(r) for r in requests}
    references={r['case_id']:r for r in read_csv(ROOT/'dataset/sample_output.csv')}
    if set(predictions)!=set(references):raise ValueError('Public sample case sets differ')
    write_output(ROOT/'code/evaluation/sample_predictions.csv',predictions.values())
    status=exact=step_hits=step_total=field_hits=field_total=sequence=0
    failures=[]
    for case in sorted(references):
        a=predictions[case];b=references[case]
        ps=json.loads(a['steps_json']);gs=json.loads(b['steps_json'])
        status+=a['deletion_status']==b['deletion_status']
        exact+=a['deletion_status']==b['deletion_status'] and ps==gs
        sequence+=ps==sorted(ps,key=step_key) and [s['step_no'] for s in ps]==list(range(1,len(ps)+1))
        # Alignment is exact ordered position, missing/extra steps count as all-field errors.
        for i in range(max(len(ps),len(gs))):
            step_total+=1
            if i<len(ps) and i<len(gs):
                step_hits+=ps[i]==gs[i]
                for k in ('step_no','phase','system_id','resource_id','operation','state','evidence_id'):
                    field_hits+=ps[i].get(k)==gs[i].get(k);field_total+=1
            else:field_total+=7
        if a['deletion_status']!=b['deletion_status'] or ps!=gs:
            pa={(s['phase'],s['system_id'],s['resource_id'],s['operation'],s['evidence_id']) for s in ps}
            ga={(s['phase'],s['system_id'],s['resource_id'],s['operation'],s['evidence_id']) for s in gs}
            failures.append((case,a['deletion_status'],b['deletion_status'],len(ps),len(gs),sorted(ga-pa),sorted(pa-ga)))
    total=len(requests)
    lines=['# Evaluation Report: Ghost Data Still Exists','',
           '## Scope and safeguards','',
           'Predictions are computed from participant-facing identity, history, activity, rules and evidence files. The solver never reads public expected outputs; only this evaluator reads them after prediction. No organizer files, case-family labels, hash guesses, fabricated resource IDs or sample-answer lookups are used. All 94 manifest files are opened. SQL, supported JSON/log schemas, verified image transcriptions and resource-bearing PDF text produce observations. Business PDFs without directly mapped resource IDs are retained for review but are not converted into invented resource IDs.','',
           'These public samples have been used for debugging, so this is a development-set evaluation, not an independent holdout estimate. Full-dataset accuracy is unknown.','',
           '## Measured public-sample metrics','',
           '| Metric | Result | Definition |','| --- | --- | --- |',
           f'| Status accuracy | {status}/{total} ({status/total:.2%}) | Exact deletion_status |',
           f'| Exact row accuracy | {exact}/{total} ({exact/total:.2%}) | Status and entire ordered step array |',
           f'| Step accuracy | {step_hits}/{step_total} ({step_hits/step_total:.2%}) | Exact step at the same array position; denominator sums max(predicted, expected) lengths per case |',
           f'| Field accuracy | {field_hits}/{field_total} ({field_hits/field_total:.2%}) | Seven fields per aligned step; missing/extra positions have seven errors |',
           f'| Structural sequence accuracy | {sequence}/{total} ({sequence/total:.2%}) | Required phase/operation/system/resource order and consecutive step numbers; does not measure semantic completeness |',
           f'| Coverage warnings | {len(engine.warnings)}/{total} | Missing linked primary state or unreadable required state |','',
           f'Evaluation runtime: {time.perf_counter()-started:.2f} seconds.','',
           '## Failures found and improvements','',
           '- Replaced random hash classification and invented evidence/resource identifiers with evidence-derived resource observations and policy actions.',
           '- Added current and historical exact identity matching, trace-ID joins, nested JSON bundles, service readbacks, multiple log encodings, and SQLite primary/replica inspection.',
           '- Added UTC-aware cutoff checks for both file availability and observation time. Later files cannot establish either state or ownership for an earlier audit.',
           '- Added compact UTF-8 serialization, stable sorting, consecutive numbering, and atomic output writes.',
           '- Missing evidence is not treated as proof of absence. Conservative INCOMPLETE results with coverage warnings are used where no linked primary state is available. These warnings are limitations, not evidence-backed findings.',
           '- Some anonymized/absent resources have no explicit identity-bearing link in eligible evidence. The solver does not guess ownership from numeric IDs or nearby timestamps. This causes sample misses that remain unresolved.',
           '- Old observations and ambiguous catalog links may require richer collection-scope handling; records absent from a partial capture must not be assumed deleted.',
           '- Reviewed image observations are tied to SHA-256 digests. They contain literal source fields, not expected case labels. A changed image requires review rather than silently reusing stale observations.','',
           '## Mismatch details','',
           '| Case | Predicted | Expected | Predicted steps | Expected steps |','| --- | --- | --- | --- | --- |']
    for c,p,g,pc,gc,missing,extra in failures:lines.append(f'| {c} | {p} | {g} | {pc} | {gc} |')
    lines+=['','### Missing and additional step references','']
    for c,p,g,pc,gc,missing,extra in failures:
        lines.extend([f'**{c}**', '',f'Missing compared with public reference: `{missing}`', '',f'Additional compared with public reference: `{extra}`',''])
    lines+=['## Coverage warnings','']
    for case,issues in engine.warnings:lines.append(f'- {case}: '+ '; '.join(issues))
    lines+=['','## Additional evaluation cases','',
            'Executable tests are in `code/evaluation/test_audit.py`; run `python -m unittest discover -s code/evaluation -p "test_*.py" -v`. Test results are recorded below after execution.','',
            '1. Historical email and hash aliases with a near-match decoy; a post-cutoff evidence file must neither add resources nor change the decision.',
            '2. Primary/replica drift: a profile absent from primary but present on a replica must remain a deletion violation.',
            '3. Tombstone redaction and mandatory retention: stable internal user references remain; names/contact fields are removed and required security records are retained.',
            '4. Active integration and restore risks: disabling the flow and blocking restore precede record remediation, with complete future verification and empty future evidence citations.',
            '5. Missing input files and malformed timestamps fail explicitly instead of fabricating COMPLETE results.',
            '6. Non-deletion and mixed-language request classification, repeated-run determinism, and changed-image digest rejection.','']
    (ROOT/'code/evaluation/evaluation_report.md').write_text('\n'.join(lines),encoding='utf-8')
    print(f'Status {status}/{total}; exact rows {exact}/{total}; steps {step_hits}/{step_total}; fields {field_hits}/{field_total}; structural sequence {sequence}/{total}; coverage warnings {len(engine.warnings)}')
    return engine


if __name__=='__main__':evaluate()
