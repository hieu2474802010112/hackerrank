"""Triage coverage gaps without feeding later evidence into predictions."""
from collections import Counter, defaultdict
from pathlib import Path
import sys
import time
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from main import AuditEngine, ROOT, canonical_identifier, instant, read_csv


def analyze(dataset=ROOT/'dataset', report=ROOT/'code/evaluation/coverage_report.md'):
    engine=AuditEngine(dataset)
    requests=read_csv(Path(dataset)/'deletion_requests.csv')
    requests_by_case={r['case_id']:r for r in requests}
    started=time.perf_counter()
    results=[engine.audit(r) for r in requests]
    categories=Counter();rows=[];future_cache={}
    issue_counts=Counter(issue for _,issues in engine.warnings for issue in issues)
    for case,issues in engine.warnings:
        request=requests_by_case[case];cutoff=instant(request['audit_at'])
        aliases,mapping,file_users,eligible=engine.cutoff_cache[cutoff]
        subjects=aliases.get(canonical_identifier(request['email']),set())
        user=next(iter(subjects))
        if cutoff not in future_cache:
            by_owner=defaultdict(list)
            for observation in engine.observations:
                if observation.category!='USER_PROFILE':continue
                # Later evidence is read here solely to explain a gap. This map
                # is never sent to AuditEngine or used in submission predictions.
                if observation.available<=cutoff and observation.observed<=cutoff:continue
                owners=engine.owners([observation.record,list(observation.links)],aliases)
                if len(owners)==1:by_owner[next(iter(owners))].append(observation)
            future_cache[cutoff]=by_owner
        future=future_cache[cutoff].get(user,[])
        missing='No identity-linked primary account state' in issues
        reason='MISSING_VISIBLE_FIELDS'
        if missing:
            reason='PRIMARY_LINK_ONLY_AFTER_CUTOFF' if future else 'NO_PRIMARY_LINK_FOUND'
            categories[reason]+=1
        elif any('ambiguous' in issue for issue in issues):
            reason='AMBIGUOUS_LINK';categories[reason]+=1
        else:categories[reason]+=1
        future_sources=sorted({f'{o.resource} / {o.evidence} / available {o.available.isoformat()}' for o in future})
        history=[h for h in engine.history if h['user_id']==user and instant(h['event_time'])<=cutoff]
        history_values={canonical_identifier(h[k]) for h in history for k in ('old_value','new_value') if h[k]}
        unassigned={o.resource for o in eligible if o.category=='USER_PROFILE' and not mapping[o.resource]}
        sources=sorted({o.evidence for o in eligible if mapping[o.resource]=={user}})
        rows.append((case,user,reason,issues,len(history_values),len(unassigned),sources,future_sources))
    manifest_types=Counter(Path(m['file_path']).suffix for m in engine.manifest)
    lines=['# Full-run evidence coverage','',
           f'Processed {len(results)} requests. **{len(engine.warnings)} cases** have unresolved evidence coverage. These are best-effort predictions, not a complete evidence-backed submission.','',
           '## Measured root-cause groups','',
           '| Primary reason per affected case | Cases |','| --- | --- |']
    labels={
        'PRIMARY_LINK_ONLY_AFTER_CUTOFF':'Explicit primary identity link found only in later evidence; excluded from predictions',
        'NO_PRIMARY_LINK_FOUND':'No explicit primary ownership link found by implemented extractors',
        'MISSING_VISIBLE_FIELDS':'Required state field not visible in the supplied evidence',
        'AMBIGUOUS_LINK':'Conflicting or ambiguous resource ownership',
    }
    for reason,count in sorted(categories.items()):lines.append(f'| {labels[reason]} | {count} |')
    lines+=['','There may be several issues per case. The grouping above counts each affected case once. Detailed issue totals:','']
    for issue,count in sorted(issue_counts.items()):lines.append(f'- {count}: `{issue}`')
    lines+=['','## What was checked and changed','',
            f'- Identity history has {len(engine.history)} rows with fields `{dict(Counter(h["field_name"] for h in engine.history))}`. Both old and new values from eligible rows are indexed; the problem is not simply that old emails were skipped.',
            f'- Current-email SHA-256 derivation was checked against all {len(engine.identities)} supplied identities: {"verified" if engine.derive_email_hashes else "not consistently verified; derivation disabled"}. Only eligible email aliases are hashed.',
            '- Telephone aliases now use the same supplied international digits despite punctuation differences. No fuzzy name/phone matching or guessed country codes are used.',
            '- Explicit source/parent resource references are resolved in both directions through complete connected components, including chains longer than three links. IDs mentioned only in prose are not ownership edges.',
            '- A linked resource without a row can be checked against a declared collection snapshot, but a successful deletion activity is still not accepted as state proof. System routing and state evidence remain separate.',
            f'- All manifest source files were opened: `{dict(manifest_types)}`. PDF text and reviewed image fields participate in retrieval. The two image-state gaps remain unresolved because unseen fields cannot be inferred from a console title or health indicator.',
            '- File availability and internal observation/scope times are checked against the cutoff. The latest observation is chosen per linked resource; equal-time replica violations take precedence over an absent primary.',
            '- Reading a later capture for this diagnostic does not authorize using it to reconstruct an earlier audit. No later links in the table below are fed into the prediction engine.','',
            '## Per-case triage','',
            '| Case | Subject | Reason | Eligible historical values | Eligible unattributed primary resources | Sources linked to subject |','| --- | --- | --- | --- | --- | --- |']
    for case,user,reason,issues,old_count,unassigned,sources,future_sources in rows:
        lines.append(f'| {case} | {user} | {reason} | {old_count} | {unassigned} | {", ".join(sources) or "none"} |')
    lines+=['','The unattributed-primary count is shared evidence available at that cutoff, not a list of resources attributed to that person. It cannot be resolved by choosing a nearby event or a matching numeric suffix.','',
            '## Later links excluded from predictions','']
    for case,user,reason,issues,old_count,unassigned,sources,future_sources in rows:
        if future_sources:lines.append(f'- {case}: '+ '; '.join(future_sources))
    lines+=['','## Unresolved state details','']
    for case,user,reason,issues,old_count,unassigned,sources,future_sources in rows:
        if any('missing state fields' in issue for issue in issues):lines.append(f'- {case}: '+ '; '.join(issues))
    lines+=['','## Documents without a grounded resource mapping','']
    for manifest,text in getattr(engine,'document_texts',[]):
        lines.append(f"- {manifest['file_id']} (`{manifest['file_path']}`): text extracted, but no supplied resource-ID/catalog mapping was established. Do not fabricate a resource ID from an invoice/order number.")
    lines+=['','## Remaining work','',
            'Resolve unattributed readbacks through an explicit eligible identity/resource mapping if one can be extracted. Inspect any new source formats before declaring the gap irreducible. Keep strict mode enabled when evidence completeness is required; `--strict` refuses to write a result with unresolved coverage. Existing default labels for these cases are conservative fallbacks, not evidence-backed findings.','',
            f'Diagnostic runtime: {time.perf_counter()-started:.2f} seconds. Public sample answers are not read by this tool.','']
    Path(report).write_text('\n'.join(lines),encoding='utf-8')
    print(f'Coverage: {len(engine.warnings)}/{len(results)} cases; groups {dict(categories)}')
    return engine,results


if __name__=='__main__':analyze()
