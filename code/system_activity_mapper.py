"""Time-bounded activity ownership lookup; workflow results remain claims."""
from __future__ import annotations

import argparse
import csv
import json
import re
from collections import defaultdict
from pathlib import Path

from evidence_inspector import parse_time


def canonical(value):
    text = str(value).strip().casefold()
    if re.fullmatch(r'\+[\d\s().-]+', text):
        digits = ''.join(c for c in text if c.isdigit())
        if 7 <= len(digits) <= 15:
            return 'tel:+' + digits
    return text


def identifiers_in(value):
    text = str(value or '')
    result = {canonical(text)} if text.strip() else set()
    # Extract full tokens: user_05 never matches user_050; a final sentence
    # period is punctuation, while periods inside email addresses are preserved.
    for token in re.findall(r'[\w.+%-]+@[\w.-]+\.[A-Za-z]{2,}', text):
        result.add(canonical(token.rstrip('.')))
    result.update(canonical(token) for token in re.findall(r'\buser_[\w]+\b', text))
    result.update(token.casefold() for token in re.findall(r'\b[a-fA-F0-9]{64}\b', text))
    result.update(canonical(token) for token in re.findall(r'\+\d[\d ().-]{7,}\d', text))
    return result


class SystemActivityMapper:
    REQUIRED = {'activity_id','event_time','event_type','source_system','target_system',
                'resource_id','reported_result','details'}
    CLAIMS = {'DELETE_RECORD':'ABSENT','ANONYMIZE_RECORD':'ANONYMIZED',
              'REDACT_RECORD':'REDACTED','INDEX_RECORD':'PRESENT',
              'SYNC_RECORD':'PRESENT','UPDATE_RECORD':'PRESENT',
              'DISABLE_DATA_FLOW':'DISABLED','BLOCK_RESTORE':'BLOCKED'}

    def __init__(self, dataset_dir=None, *, activities=None):
        if activities is None:
            dataset = Path(dataset_dir or Path(__file__).resolve().parents[1]/'dataset')
            with (dataset/'system_activity.csv').open(encoding='utf-8-sig', newline='') as stream:
                reader = csv.DictReader(stream)
                if not self.REQUIRED <= set(reader.fieldnames or []):
                    raise ValueError('system_activity.csv is missing required columns')
                activities = list(reader)
        self.activities = [dict(row) for row in activities]
        self.times = []
        self.by_identifier = defaultdict(set)
        self.by_resource = defaultdict(set)
        self.identifiers = []
        seen = set()
        for index, row in enumerate(self.activities):
            if not self.REQUIRED <= set(row):
                raise ValueError('Activity is missing required columns')
            if not row['activity_id'] or row['activity_id'] in seen:
                raise ValueError('Activity IDs must be non-empty and unique')
            seen.add(row['activity_id'])
            try:
                self.times.append(parse_time(row['event_time']))
            except (TypeError, ValueError) as exc:
                raise ValueError(f"Invalid event_time for {row['activity_id']}") from exc
            tokens = identifiers_in(row['details']) | identifiers_in(row['resource_id'])
            for field in ('email','user_id','phone','email_hash','subject_reference','customer_reference'):
                if row.get(field):
                    tokens.update(identifiers_in(row[field]))
            self.identifiers.append(tokens)
            for token in tokens:
                self.by_identifier[token].add(index)
            self.by_resource[row['resource_id']].add(index)

    def find_resources_for_identifiers(self, identifiers, audit_at, *, include_resource_history=True):
        cutoff = parse_time(audit_at)
        terms = {canonical(term) for term in identifiers if term is not None and str(term).strip()}
        if not terms:
            raise ValueError('At least one non-empty identifier is required')
        seeds = set().union(*(self.by_identifier.get(term,set()) for term in terms))
        seeds = {index for index in seeds if self.times[index] <= cutoff}
        selected = set(seeds)
        if include_resource_history:
            for resource in {self.activities[i]['resource_id'] for i in seeds}:
                selected.update(i for i in self.by_resource[resource] if self.times[i] <= cutoff)
        result = []
        for index in sorted(selected, key=lambda i:(self.times[i],self.activities[i]['activity_id'])):
            row = dict(self.activities[index])
            row['matched_identifiers'] = sorted(terms & self.identifiers[index])
            row['match_kind'] = 'IDENTITY_MATCH' if index in seeds else 'RESOURCE_HISTORY'
            result.append(row)
        return result

    def find_resources_for_emails(self, emails, audit_at):
        return self.find_resources_for_identifiers(emails, audit_at)

    def ownership_links(self, aliases, audit_at):
        """Return owner sets and activity provenance without inferring state."""
        cutoff = parse_time(audit_at)
        owners = defaultdict(set)
        provenance = defaultdict(set)
        for index, row in enumerate(self.activities):
            if self.times[index] > cutoff:
                continue
            subjects = set().union(*(aliases.get(token,set()) for token in self.identifiers[index]))
            if subjects:
                owners[row['resource_id']].update(subjects)
                provenance[row['resource_id']].add(row['activity_id'])
        return owners, provenance

    def deduce_resource_state(self, activities, audit_at):
        """Summarize reported transitions, never elevate them to verified state.

        For compatibility with the proposed API, status is always UNKNOWN and
        evidence_id is empty. claimed_state/claimed_activity_id are diagnostic
        workflow assertions that must be checked against independent evidence.
        """
        cutoff = parse_time(audit_at)
        eligible = [row for row in activities if parse_time(row['event_time']) <= cutoff]
        result = {}
        for row in sorted(eligible,key=lambda r:(parse_time(r['event_time']),r['activity_id'])):
            resource = row['resource_id']
            state = result.setdefault(resource, {'system_id':row['target_system'] or row['source_system'],
                'status':'UNKNOWN','verified':False,'evidence_id':'',
                'claimed_state':None,'claimed_activity_id':'','activity_ids':[]})
            state['last_event'] = row['event_type']
            state['last_event_at'] = row['event_time']
            state['activity_ids'].append(row['activity_id'])
            if row['event_type']=='LINK_RESOURCE_IDENTITY':
                state['system_id'] = row['target_system'] or row['source_system']
            if row['reported_result']=='SUCCESS' and row['event_type'] in self.CLAIMS:
                state['claimed_state'] = self.CLAIMS[row['event_type']]
                state['claimed_activity_id'] = row['activity_id']
        return result


if __name__=='__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--dataset', type=Path)
    parser.add_argument('--email', action='append', default=[])
    parser.add_argument('--user-id', action='append', default=[])
    parser.add_argument('--identifier', action='append', default=[])
    parser.add_argument('--audit-at', required=True)
    args = parser.parse_args()
    mapper = SystemActivityMapper(args.dataset)
    rows = mapper.find_resources_for_identifiers(args.email+args.user_id+args.identifier,args.audit_at)
    print(json.dumps({'activities':rows,'reported_states':mapper.deduce_resource_state(rows,args.audit_at)},
                     ensure_ascii=False,indent=2))
