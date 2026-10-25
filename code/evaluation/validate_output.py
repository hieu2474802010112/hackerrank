"""Validate submission structure, request coverage and citation cutoffs."""
import argparse
import json
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from main import ROOT, PHASES, instant, read_csv, step_key

OP_STATES={
    'REPORT_REMAINING_RECORD':'PRESENT','REPORT_EXPOSED_PII':'PRESENT',
    'REPORT_ACTIVE_DATA_FLOW':'ACTIVE','REPORT_RESTORE_RISK':'ACTIVE',
    'DISABLE_DATA_FLOW':'DISABLED','BLOCK_RESTORE':'BLOCKED','DELETE_RECORD':'ABSENT',
    'REDACT_RECORD':'REDACTED','ANONYMIZE_RECORD':'ANONYMIZED',
    'VERIFY_RECORD_ABSENT':'ABSENT','VERIFY_RECORD_PRESENT':'PRESENT',
    'VERIFY_RECORD_REDACTED':'REDACTED','VERIFY_RECORD_ANONYMIZED':'ANONYMIZED',
    'VERIFY_DATA_FLOW_DISABLED':'DISABLED','VERIFY_RESTORE_BLOCKED':'BLOCKED',
}
FIELDS={'step_no','phase','system_id','resource_id','operation','state','evidence_id'}


def validate(output=ROOT/'output.csv',requests=ROOT/'dataset/deletion_requests.csv',dataset=ROOT/'dataset'):
    output=Path(output);requests=Path(requests);dataset=Path(dataset)
    rows=read_csv(output);reqs={r['case_id']:r for r in read_csv(requests)}
    if not rows or list(rows[0])!=['case_id','deletion_status','steps_json']:raise ValueError('Invalid output columns')
    ids=[r['case_id'] for r in rows]
    if len(ids)!=len(set(ids)) or set(ids)!=set(reqs) or ids!=sorted(ids):raise ValueError('Case coverage/uniqueness/order mismatch')
    evidence={m['file_id']:instant(m['captured_at']) for m in read_csv(dataset/'evidence_files.csv')}
    evidence.update({a['activity_id']:instant(a['event_time']) for a in read_csv(dataset/'system_activity.csv')})
    evidence.update({a['audit_id']:instant(a['event_time']) for a in read_csv(dataset/'user_audit_log.csv')})
    nsteps=0
    for r in rows:
        status=r['deletion_status'];steps=json.loads(r['steps_json']);case=r['case_id'];cutoff=instant(reqs[case]['audit_at'])
        if status not in {'COMPLETE','INCOMPLETE','NOT_APPLICABLE'}:raise ValueError(f'{case}: invalid status')
        if not isinstance(steps,list):raise ValueError(f'{case}: expected array')
        if status=='NOT_APPLICABLE' and steps:raise ValueError(f'{case}: unauthorized steps')
        for i,s in enumerate(steps,1):
            if set(s)!=FIELDS or type(s['step_no']) is not int or s['step_no']!=i:raise ValueError(f'{case}: invalid step fields/number')
            if s['phase'] not in PHASES or s['operation'] not in PHASES[s['phase']]:raise ValueError(f'{case}: invalid phase/operation')
            if s['state']!=OP_STATES[s['operation']]:raise ValueError(f'{case}: invalid state')
            if not all(isinstance(s[k],str) for k in FIELDS-{'step_no'}):raise ValueError(f'{case}: non-string fields')
            if not s['system_id'] or not s['resource_id']:raise ValueError(f'{case}: missing resource/system')
            if status=='COMPLETE' and s['phase']!='VERIFICATION':raise ValueError(f'{case}: non-verification COMPLETE step')
            future=status=='INCOMPLETE' and s['phase']!='FINDING'
            if future and s['evidence_id']:raise ValueError(f'{case}: future evidence citation')
            if not future and (s['evidence_id'] not in evidence or evidence[s['evidence_id']]>cutoff):raise ValueError(f'{case}: missing/late evidence')
        if steps!=sorted(steps,key=step_key):raise ValueError(f'{case}: step order mismatch')
        nsteps+=len(steps)
    print(f'PASS: {len(rows)} cases, exact columns, unique sorted IDs, {nsteps} valid ordered steps, eligible citations.')
    return len(rows),nsteps


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--output',type=Path,default=ROOT/'output.csv')
    args=parser.parse_args();validate(args.output)
