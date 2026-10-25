"""Evidence-grounded deletion audit. Prediction never reads sample_output.csv."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import time
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from evidence_inspector import load_sql_snapshot, table_names
from system_activity_mapper import SystemActivityMapper
from unstructured_inspector import UnstructuredInspector
from ocr_inspector import OCRInspector

ROOT = Path(__file__).resolve().parents[1]
PHASES = {
    'FINDING': ['REPORT_REMAINING_RECORD', 'REPORT_EXPOSED_PII', 'REPORT_ACTIVE_DATA_FLOW', 'REPORT_RESTORE_RISK'],
    'REMEDIATION': ['DISABLE_DATA_FLOW', 'BLOCK_RESTORE', 'DELETE_RECORD', 'REDACT_RECORD', 'ANONYMIZE_RECORD'],
    'VERIFICATION': ['VERIFY_RECORD_ABSENT', 'VERIFY_RECORD_PRESENT', 'VERIFY_RECORD_REDACTED', 'VERIFY_RECORD_ANONYMIZED', 'VERIFY_DATA_FLOW_DISABLED', 'VERIFY_RESTORE_BLOCKED'],
}
STATES = {'DELETE':'ABSENT', 'REDACT':'REDACTED', 'ANONYMIZE':'ANONYMIZED', 'RETAIN':'PRESENT', 'DISABLE':'DISABLED', 'BLOCK':'BLOCKED'}
VERIFY = {'DELETE':'VERIFY_RECORD_ABSENT', 'REDACT':'VERIFY_RECORD_REDACTED', 'ANONYMIZE':'VERIFY_RECORD_ANONYMIZED', 'RETAIN':'VERIFY_RECORD_PRESENT', 'DISABLE':'VERIFY_DATA_FLOW_DISABLED', 'BLOCK':'VERIFY_RESTORE_BLOCKED'}
COLLECTIONS = {
    'customer_profiles':'USER_PROFILE', 'customer_search_documents':'SEARCH_INDEX_ENTRY',
    'customer_analytics_reports':'ANALYTICS_PROFILE', 'backup_catalog':'BACKUP_ARCHIVE',
    'customer_export_jobs':'USER_EXPORT', 'connector_configurations':'DATA_FLOW',
    'security_audit_events':'SECURITY_AUDIT_LOG', 'support_conversations':'SUPPORT_MESSAGE',
    'ticket_attachments':'SUPPORT_ATTACHMENT', 'retained_order_records':'LEGAL_HOLD_RECORD',
    'deleted_customer_references':'ACCOUNT_TOMBSTONE',
}
RESOURCE_RE = re.compile(r'\b(?:account|analytics|search|support|export|data_flow|backup|audit_record|tombstone|legal_hold|object|marketing|cache|email_delivery)_\d+\b')
IDENT_RE = re.compile(r'[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}|\buser_\d+\b|\b[a-fA-F0-9]{64}\b')
EMPTY = {'', 'null', 'none', '[redacted]', 'redacted', 'no direct identifier', '-'}


def instant(value):
    if isinstance(value, datetime): return value
    dt = datetime.fromisoformat(str(value).replace('Z', '+00:00'))
    if dt.tzinfo is None: dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


def read_csv(path):
    with Path(path).open(encoding='utf-8-sig', newline='') as f:
        return list(csv.DictReader(f))


def normalize(value):
    return str(value).strip().casefold()


def canonical_identifier(value):
    """Normalize formatting without guessing a country code or fuzzy identity."""
    text = normalize(value)
    if re.fullmatch(r'\+[\d\s().-]+', text):
        digits = ''.join(c for c in text if c.isdigit())
        if 7 <= len(digits) <= 15:
            return 'tel:+' + digits
    return text


def resource_references(value):
    """Follow explicit foreign keys, not arbitrary IDs mentioned in prose."""
    if isinstance(value, dict):
        for key, item in value.items():
            if key in {'source_resource_id', 'source_resource_ids', 'parent_resource_id', 'parent_resource_ids'}:
                for candidate in leaves(item):
                    if RESOURCE_RE.fullmatch(candidate):
                        yield candidate
            elif isinstance(item, (dict, list)):
                yield from resource_references(item)
    elif isinstance(value, list):
        for item in value:
            yield from resource_references(item)


def leaves(value):
    if isinstance(value, dict):
        for v in value.values(): yield from leaves(v)
    elif isinstance(value, list):
        for v in value: yield from leaves(v)
    elif value is not None: yield str(value)


def truth(value):
    if isinstance(value, bool): return value
    if normalize(value) in {'true', '1', 'yes', 'allow', 'allowed', 'active', 'enabled'}: return True
    if normalize(value) in {'false', '0', 'no', 'deny', 'denied', 'blocked', 'disabled'}: return False
    return None


def step_key(s):
    phase = s['phase']
    return list(PHASES).index(phase), PHASES[phase].index(s['operation']), s['system_id'], s['resource_id']


def finalize(steps):
    unique = {(s['phase'], s['operation'], s['system_id'], s['resource_id']): s for s in steps}
    result = sorted(unique.values(), key=step_key)
    for i, s in enumerate(result, 1): s['step_no'] = i
    return result


def authorizes_deletion(text):
    text = normalize(text).replace('’', "'")
    # Explicit preservation/negation takes precedence over a quoted deletion term.
    if re.search(r"(?:do not|don't|not asking (?:you )?to|not requesting)\s+(?:delete|remove|erase|close|deletion)", text): return False
    if re.search(r'(?:keep|leave) (?:my |the )?(?:account|profile|purchase history).{0,25}(?:active|as it is|in place|open)', text): return False
    if 'continue using the service' in text: return False
    if re.search(r'not asking for deletion|not a request to (?:erase|delete|remove)|without remov(?:ing|al)',text):return False
    if re.search(r'(?:marketing lists only|opt[ -]?out of marketing|stop (?:the )?promotional emails)',text) and not re.search(r'(?:delete|erase|close) (?:my |the |this )?account',text):return False
    if re.search(r'delet|remov|eras|clos(?:e|ed|ure|ing)|elimin|supprim|suppression|exclus|삭제|削除|löschen|löschung|borrar', text): return True
    return bool(re.search(r'profile is gone|cannot identify me|fully removed', text))


@dataclass
class Observation:
    system: str
    resource: str
    category: str
    record: dict
    observed: datetime
    available: datetime
    evidence: str
    state: str | None = None
    links: set[str] = field(default_factory=set)
    authority: int = 1
    scope: str = ''


@dataclass
class Coverage:
    system: str
    category: str
    resources: set[str]
    observed: datetime
    available: datetime
    evidence: str
    scope: str
    global_profiles: bool = False


class AuditEngine:
    def __init__(self, dataset):
        self.dataset = Path(dataset).resolve()
        self.identities = read_csv(self.dataset/'user_identities.csv')
        self.derive_email_hashes = bool(self.identities) and all(
            hashlib.sha256(normalize(r['email']).encode('utf-8')).hexdigest() == r['email_hash']
            for r in self.identities)
        self.history = read_csv(self.dataset/'user_audit_log.csv')
        self.activities = read_csv(self.dataset/'system_activity.csv')
        self.activity_mapper = SystemActivityMapper(activities=self.activities)
        self.manifest = read_csv(self.dataset/'evidence_files.csv')
        self.unstructured_inspector = UnstructuredInspector(self.dataset)
        self.ocr_inspector = OCRInspector(self.dataset)
        self.rules = {r['data_category']: r['required_action'] for r in read_csv(self.dataset/'deletion_rules.csv')}
        self.observations = []
        self.coverage = []
        self.warnings = []
        self.by_resource = defaultdict(list)
        self.cutoff_cache = {}
        self.file_subjects = defaultdict(set)
        for m in self.manifest:
            p = (self.dataset/m['file_path']).resolve()
            if not p.is_relative_to(self.dataset): raise ValueError('Evidence path escapes dataset')
            if not p.is_file(): raise FileNotFoundError(p)
            suffix=p.suffix.lower()
            if suffix=='.json': self.load_json(m, p)
            elif suffix=='.sql': self.load_sql(m, p)
            elif suffix=='.log': self.load_log(m, p)
            elif suffix=='.txt': self.load_text(m, p.read_text(encoding='utf-8'))
            elif suffix=='.pdf': self.load_pdf(m,p)
            elif suffix!='.png': raise ValueError(f'Unsupported evidence: {p}')
        self.load_images()
        for obs in self.observations:
            self.by_resource[obs.resource].append(obs)
        self.activity_by_resource = defaultdict(list)
        for a in self.activities: self.activity_by_resource[a['resource_id']].append(a)

    def add(self, m, system, resource, category, record, observed=None, state=None, links=(), authority=1, scope=''):
        if not resource or not category: return
        obs=Observation(system, resource, category, record, instant(observed or m['captured_at']), instant(m['captured_at']), m['file_id'], state, set(str(v) for v in links if v is not None), authority, scope)
        self.observations.append(obs)
        return obs

    def load_json(self,m,p):
        d=json.loads(p.read_text(encoding='utf-8'))
        if 'service_exports' in d:
            for system, collections in d['service_exports'].items():
                for collection, rows in collections.items():
                    for r in rows:
                        rid=r['resource_id']; category=self.default_category(system,rid)
                        state=None;record=r
                        if collection=='profile_lookups':
                            state='ABSENT' if r.get('profile') is None and r.get('status_code')==404 else 'PRESENT'
                            record=r.get('profile') or {}
                        elif collection=='index_queries':
                            state='PRESENT' if r['hits']['total'] else 'ABSENT'
                            record={'documents':r['hits'].get('documents',[])}
                        self.add(m,system,rid,category,record,r.get('observed_at'),state,links=[r.get('query','')],authority=3)
        snapshots = list(d.get('snapshots', []))
        if 'collection' in d and 'records' in d:
            collection=d['collection']
            system={'customer_analytics_reports':'analytics_platform','customer_export_jobs':'export_service'}.get(collection)
            if not system: raise ValueError(f'Unknown top-level collection {collection}')
            snapshots.append(dict(d, data_store=system))
        if 'records' in d and 'collection' not in d:
            for r in d['records']:
                self.add(m,r['system'],r['resource_id'],r['record_type'],r,r.get('recorded_at'),self.result_state(r['result']))
        elif not snapshots and 'service_exports' not in d: raise ValueError(f'Unrecognized JSON evidence {p.name}')
        for snapshot in snapshots:
            system=snapshot['data_store']; collection=snapshot['collection']; observed=snapshot['captured_at']
            category=COLLECTIONS.get(collection)
            if collection=='operational_record_history':
                for r in snapshot['records']:
                    self.add(m,r['system'],r['resource_id'],r['record_type'],r,r.get('recorded_at',observed),self.result_state(r['result']),links=[r.get('lookup_value','')])
                continue
            if not category: raise ValueError(f'Unknown collection {collection}')
            records=snapshot['records']
            self.coverage.append(Coverage(system,category,{r['resource_id'] for r in records},instant(observed),instant(m['captured_at']),m['file_id'],collection))
            for r in records: self.add(m,system,r['resource_id'],category,r,observed,scope=collection)

    def load_sql(self,m,p):
        # Execute supplied SQLite captures only in a private memory database.
        conn=load_sql_snapshot(p)
        try:
            tables=table_names(conn)
            scope_times = {r['origin_system']: r['captured_at'] for r in conn.execute('select * from snapshot_scope')} if 'snapshot_scope' in tables else {}
            sql_categories = {
                'customer_profiles': ('account_service','USER_PROFILE'),
                'customer_search_documents': ('search_service','SEARCH_INDEX_ENTRY'),
                'customer_analytics_profiles': ('analytics_platform','ANALYTICS_PROFILE'),
                'support_records': ('support_platform','SUPPORT_MESSAGE'),
                'customer_exports': ('export_service','USER_EXPORT'),
                'connector_subscriptions': ('integration_service','DATA_FLOW'),
                'backup_restore_entries': ('backup_service','BACKUP_ARCHIVE'),
                'security_audit_records': ('security_service','SECURITY_AUDIT_LOG'),
            }
            for table in tables:
                if table == 'snapshot_scope': continue
                quoted='"'+table.replace('"','""')+'"'
                rows=[dict(r) for r in conn.execute('select * from '+quoted)]
                groups=defaultdict(list)
                if not rows and table in sql_categories:
                    system,category=sql_categories[table]
                    if system in scope_times:
                        self.coverage.append(Coverage(system,category,set(),instant(scope_times[system]),instant(m['captured_at']),m['file_id'],table))
                elif not rows and table.startswith('customer_profiles_'):
                    self.coverage.append(Coverage('account_service','USER_PROFILE',set(),instant(m['captured_at']),instant(m['captured_at']),m['file_id'],'customer_profiles',True))
                for r in rows:
                    if 'record_json' in r:
                        record=json.loads(r['record_json']);system=r['origin_system'];category=COLLECTIONS[r['collection_name']]
                        scope=r['collection_name']
                    elif table in sql_categories:
                        record=r;system,category=sql_categories[table];scope=table
                    elif table.startswith('customer_profiles'):
                        record=r;system='account_service';category='USER_PROFILE';scope='customer_profiles'
                    elif table.startswith('search_documents'):
                        record=r;system='search_service';category='SEARCH_INDEX_ENTRY';scope='customer_search_documents'
                    else: raise ValueError(f'Unknown SQL table {table}')
                    # Snapshot capture establishes presence even if the last write predates it.
                    self.add(m,system,r['resource_id'],category,record,scope_times.get(system),scope=scope,authority=2)
                    groups[(system,category,scope)].append(r['resource_id'])
                for (system,category,scope), resources in groups.items():
                    self.coverage.append(Coverage(system,category,set(resources),instant(m['captured_at']),instant(m['captured_at']),m['file_id'],scope,table.startswith('customer_profiles_') and 'snapshot_scope' not in tables))
        finally: conn.close()

    @staticmethod
    def result_state(result):
        return {'FOUND':'PRESENT','NOT_FOUND':'ABSENT','IDENTIFIABLE':'PRESENT','ANONYMIZED':'ANONYMIZED','REDACTED':'REDACTED','ACTIVE':'ACTIVE','BLOCKED':'BLOCKED','DISABLED':'DISABLED'}.get(result)

    @staticmethod
    def default_category(system,rid):
        return {'account_service':'USER_PROFILE','search_service':'SEARCH_INDEX_ENTRY','analytics_platform':'ANALYTICS_PROFILE','support_platform':'SUPPORT_MESSAGE','integration_service':'DATA_FLOW','backup_service':'BACKUP_ARCHIVE','export_service':'USER_EXPORT','security_service':'SECURITY_AUDIT_LOG','identity_service':'ACCOUNT_TOMBSTONE','marketing_platform':'MARKETING_PROFILE'}.get(system)

    @staticmethod
    def parse_log_line(line):
        when=line.split(' ',1)[0]
        if '{' in line:
            try: return when,json.loads(line[line.index('{'):])
            except json.JSONDecodeError: pass
        # Lambda envelopes escape the inner logfmt; unwrap without evaluating code.
        line=line.replace('\\"','"')
        data={k:(a if a else b) for k,a,b in re.findall(r'(\w+)=(?:"([^"]*)"|([^\s"]+))',line)}
        bracket=re.search(r'\[\w+\]\s+\[([^]]+)\]\s+\[([^]]+)\]\s+(\w+):',line)
        if bracket:
            data.setdefault('service',bracket[1]);data.setdefault('trace_id',bracket[2]);data.setdefault('event',bracket[3])
        pipe=re.match(r'^\S+\s*\|\s*\w+\s*\|\s*([^|]+)\|\s*([^|]+)\|\s*([^|]+)\|',line)
        if pipe:
            data.setdefault('service',pipe[1].strip())
            data.setdefault('trace_id',pipe[2].strip())
            data.setdefault('event',pipe[3].strip())
        syslog=re.search(r'<\d+>1\s+\S+\s+(\S+)\s+(\S+)\s+-\s+-',line)
        if syslog:
            data.setdefault('service',syslog[1]);data.setdefault('trace_id',syslog[2])
        data.setdefault('service',data.get('function',''))
        data.setdefault('trace_id',data.get('requestId',''))
        return when,data

    def load_log(self,m,p):
        traces=defaultdict(list)
        for line in p.read_text(encoding='utf-8').splitlines():
            if not line.strip(): continue
            when,d=self.parse_log_line(line)
            event=d.get('event','');rid=d.get('resource_id');system=d.get('system',d.get('service',''))
            trace=d.get('trace_id')
            if trace:
                for k in ('lookup_key','match_key','subject_key','scan_key','owner_key','subject_ref','correlation_key'):
                    if k in d: traces[trace].append(d[k])
            if not rid: continue
            category=self.default_category(system,rid);state=None;record=dict(d)
            if event=='record_lookup': category=d['record_type'];state=self.result_state(d['result'])
            elif event=='profile_lookup_completed': category='USER_PROFILE';state='ABSENT' if str(d.get('rows'))=='0' else 'PRESENT'
            elif event=='index_query_completed': category='SEARCH_INDEX_ENTRY';state='PRESENT' if d.get('result')=='hit' else 'ABSENT'
            elif event in ('analytics_identity_scan','analytics_profile_read','analytics_profile_read_completed'):
                category='ANALYTICS_PROFILE'
                if d.get('direct_identifiers')=='0':state='ANONYMIZED'
                elif event=='analytics_identity_scan':state='PRESENT'
            elif event=='contact_lookup_completed' and system=='analytics_platform': category='SECONDARY_IDENTIFIER';state='PRESENT'
            elif event in ('attachment_pii_scan',): category='SUPPORT_ATTACHMENT';state='PRESENT'
            elif event in ('message_pii_scan','support_ticket_read_completed'): category='SUPPORT_MESSAGE'
            elif event=='message_read':category='SUPPORT_MESSAGE';state='REDACTED' if d.get('message_text')=='[REDACTED]' else 'PRESENT'
            elif event in ('connector_heartbeat','connector_config_loaded','connector_config_read_completed'):
                category='DATA_FLOW';state='DISABLED' if truth(d.get('enabled')) is False else 'ACTIVE'
            elif event in ('restore_candidate_evaluated','restore_authorization_completed','restore_policy_read_completed'):
                category='BACKUP_ARCHIVE'
                allowed=truth(d.get('restore_allowed',d.get('eligible',d.get('decision'))))
                state='BLOCKED' if allowed is False else 'ACTIVE' if allowed is True else None
            elif event in ('export_download_check_completed','export_metadata_read_completed'): category='USER_EXPORT';state='PRESENT' if truth(d.get('available')) else 'ABSENT'
            elif event=='audit_record_read_completed':category='SECURITY_AUDIT_LOG';state='PRESENT' if str(d.get('rows'))=='1' else 'ABSENT'
            elif event=='contact_query_completed':category='SUPPORT_ATTACHMENT';state='PRESENT' if str(d.get('rows'))=='1' else 'ABSENT';system='support_platform'
            else: continue
            if category:
                self.add(m,system,rid,category,record,when,state,traces.get(trace,[]),authority=3 if 'read_completed' in event else 2)

    def load_text(self,m,text):
        for line in text.splitlines():
            if not line.startswith('- '):continue
            parts=[x.strip() for x in line[2:].split('|')]
            if len(parts)==6:
                when,system,rid,category,result,lookup=parts
                self.add(m,system,rid,category,{'lookup_value':lookup},when,self.result_state(result),links=[lookup])

    def load_pdf(self,m,p):
        text=self.unstructured_inspector.extract_text_from_pdf(p)
        resources=set(RESOURCE_RE.findall(text))
        if 'Support reference' in text:
            for rid in resources:
                self.add(m,'support_platform',rid,'SUPPORT_ATTACHMENT',{'document_text':text},state='PRESENT')
        elif 'Event reference' in text:
            for rid in resources:
                self.add(m,'security_service',rid,'SECURITY_AUDIT_LOG',{'document_text':text},state='PRESENT')
        else:
            matched=False
            for a in self.activities:
                if a['event_type']!='LINK_RESOURCE_IDENTITY':continue
                labels=re.findall(r'\(([^)]+)\)',a['details'])
                if not any(label in text for label in labels):continue
                category=self.default_category(a['target_system'],a['resource_id'])
                if not category:continue
                # The catalog establishes the business document's resource ID, not its deletion state.
                obs=self.add(m,a['target_system'],a['resource_id'],category,{'document_text':text},state='PRESENT')
                obs.available=max(obs.available,instant(a['event_time']))
                matched=True
            if not matched:
                self.document_texts=getattr(self,'document_texts',[])+[(m,text)]

    def load_images(self):
        notes=Path(__file__).with_name('image_observations.md')
        if not notes.exists():raise FileNotFoundError('Reviewed image observations are required')
        entries=json.loads(re.search(r'```json\s*(.*?)\s*```',notes.read_text(encoding='utf-8'),re.S)[1])
        manifest={m['file_path']:m for m in self.manifest}
        for e in entries:
            if e['file_path'] not in manifest:continue
            m=manifest[e['file_path']];p=self.dataset/m['file_path']
            if hashlib.sha256(p.read_bytes()).hexdigest()!=e['sha256']:raise ValueError(f'Image changed; review required: {p.name}')
            for r in e['records']:
                self.add(m,r['system'],r['resource_id'],r['category'],r['record'])

    def aliases_at(self,cutoff):
        values=defaultdict(set)
        # Reverse later identity updates before adding only historical values known by the cutoff.
        for r in self.identities:
            user=r['user_id']; current=dict(r)
            for a in sorted((a for a in self.history if a['user_id']==user),key=lambda a:a['event_time'],reverse=True):
                if instant(a['event_time'])>cutoff:current[a['field_name']]=a['old_value']
            for k in ('user_id','name','email','phone','email_hash'):
                if current.get(k): values[canonical_identifier(current[k])].add(user)
        for a in self.history:
            if instant(a['event_time'])<=cutoff:
                for k in ('old_value','new_value'):
                    if a[k]:values[canonical_identifier(a[k])].add(a['user_id'])
        # Derive only a hash algorithm verified against every supplied current
        # identity. Eligible historical email aliases are hashed, never future ones.
        if self.derive_email_hashes:
            for alias, users in list(values.items()):
                if re.fullmatch(r'[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}', alias):
                    values[hashlib.sha256(alias.encode('utf-8')).hexdigest()].update(users)
        return values

    @staticmethod
    def owners(value,aliases):
        found=set()
        for v in leaves(value):
            found.update(aliases.get(canonical_identifier(v),()))
            for token in IDENT_RE.findall(v): found.update(aliases.get(normalize(token),()))
            # Normalize only the same international phone digits; near-number decoys stay distinct.
            for phone in re.findall(r'\+\d[\d ().-]{7,}\d',v): found.update(aliases.get(canonical_identifier(phone),()))
        return found

    def resource_owners(self,cutoff,aliases):
        mapping=defaultdict(set);file_users=defaultdict(set)
        eligible=[o for o in self.observations if o.available<=cutoff and o.observed<=cutoff]
        for o in eligible:
            users=self.owners([o.record,list(o.links)],aliases)
            mapping[o.resource].update(users);file_users[o.evidence].update(users)
        activity_owners,activity_provenance=self.activity_mapper.ownership_links(aliases,cutoff)
        for resource,users in activity_owners.items():mapping[resource].update(users)
        self.activity_link_provenance=getattr(self,'activity_link_provenance',{})
        self.activity_link_provenance[cutoff]=activity_provenance
        # A search document can establish its source profile's owner even when
        # that profile has already disappeared. Resolve full connected components
        # rather than propagating in one direction for only three iterations.
        adjacency=defaultdict(set)
        for o in eligible:
            for rid in set(resource_references(o.record))-{o.resource}:
                adjacency[o.resource].add(rid);adjacency[rid].add(o.resource)
        visited=set()
        for root in sorted(adjacency):
            if root in visited:continue
            component=set();pending=[root]
            while pending:
                rid=pending.pop()
                if rid in component:continue
                component.add(rid);pending.extend(adjacency[rid]-component)
            users=set().union(*(mapping[rid] for rid in component))
            for rid in component:mapping[rid].update(users)
            visited.update(component)
        for o in eligible:file_users[o.evidence].update(mapping[o.resource])
        return mapping,file_users,eligible

    @staticmethod
    def pii_present(record,include_reference=False):
        keys={'name','full_name','display_name','email','phone','email_hash','requester_name','requester_email','requester_phone','owner_email','owner_phone','customer_email','uploaded_by','matched_value'}
        if include_reference:keys|={'user_id','customer_reference','subject_reference','subject_ref'}
        found=False
        def walk(v):
            nonlocal found
            if isinstance(v,dict):
                for k,val in v.items():
                    if k in keys and val is not None and normalize(val) not in EMPTY:found=True
                    if k in {'message_text','message_excerpt','document_text'} and val and (IDENT_RE.search(str(val)) or re.search(r'\+\d[\d ()-]{7,}',str(val))):found=True
                    if isinstance(val,(dict,list)):walk(val)
            elif isinstance(v,list):
                for x in v:walk(x)
        walk(record)
        return found

    def treatment(self,o):
        if o.category=='DATA_FLOW':return 'DISABLE'
        if o.category=='BACKUP_ARCHIVE':return 'BLOCK'
        if o.category not in self.rules:raise ValueError(f'No policy for {o.category}')
        return self.rules[o.category]

    def observed_state(self,o):
        if o.state:return o.state
        if o.category=='DATA_FLOW':
            enabled=truth(o.record.get('enabled'))
            return 'ACTIVE' if enabled is True else 'DISABLED' if enabled is False else 'UNKNOWN'
        if o.category=='BACKUP_ARCHIVE':
            allowed=truth(o.record.get('restore_allowed'))
            return 'ACTIVE' if allowed is True else 'BLOCKED' if allowed is False else 'UNKNOWN'
        action=self.treatment(o)
        if action=='ANONYMIZE':return 'PRESENT' if self.pii_present(o.record,True) else 'ANONYMIZED'
        if action=='REDACT':
            if o.category=='ACCOUNT_TOMBSTONE' and not any(k in o.record for k in ('name','full_name','email','phone','email_hash')):return 'UNKNOWN'
            return 'PRESENT' if self.pii_present(o.record) else 'REDACTED'
        return 'PRESENT'

    def audit(self,request):
        if not authorizes_deletion(request['request_text']):return {'case_id':request['case_id'],'deletion_status':'NOT_APPLICABLE','steps_json':'[]'}
        cutoff=instant(request['audit_at'])
        if cutoff not in self.cutoff_cache:
            aliases=self.aliases_at(cutoff)
            self.cutoff_cache[cutoff]=(aliases,*self.resource_owners(cutoff,aliases))
        aliases,mapping,file_users,eligible=self.cutoff_cache[cutoff]
        subjects=aliases.get(normalize(request['email']),set())
        if len(subjects)!=1:raise ValueError(f"Unresolved/ambiguous identity for {request['case_id']}")
        user=next(iter(subjects))
        resources={rid for rid,users in mapping.items() if users=={user}}
        uncertain=[f'{rid}: ambiguous resource ownership' for rid,users in mapping.items() if user in users and len(users)>1];observed=[]
        for rid in sorted(resources):
            candidates=[o for o in self.by_resource.get(rid,[]) if o.available<=cutoff and o.observed<=cutoff]
            # Only a whole-collection snapshot with subject context can prove an absent record.
            if candidates:
                known=candidates[0]
            else:
                specs={(a['target_system'],self.default_category(a['target_system'],rid))
                       for a in self.activity_by_resource.get(rid,[])
                       if instant(a['event_time'])<=cutoff and self.default_category(a['target_system'],rid)}
                if len(specs)!=1:
                    uncertain.append(f'{rid}: explicit ownership link but no eligible state or unambiguous system')
                    continue
                system,category=next(iter(specs))
                # A routing record identifies the system; it never proves a
                # deletion result. Only a scoped snapshot below can prove absence.
                known=Observation(system,rid,category,{},cutoff,cutoff,'','UNKNOWN')
            if self.treatment(known)=='DELETE':
                for c in self.coverage:
                    if c.available>cutoff or c.observed>cutoff or c.system!=known.system or c.category!=known.category:continue
                    if rid in c.resources:continue
                    if not (user in file_users[c.evidence] or c.global_profiles):continue
                    candidates.append(Observation(c.system,rid,c.category,{},c.observed,c.available,c.evidence,'ABSENT',authority=2))
            if not candidates:
                uncertain.append(f'{rid}: explicit ownership link but no eligible state')
                continue
            # Newer readbacks supersede older records; at equal capture, retain any replica violation.
            latest=max(o.observed for o in candidates)
            same=[o for o in candidates if o.observed==latest]
            def priority(o):
                state=self.observed_state(o); action=self.treatment(o)
                return state!=STATES[action],o.authority,o.available,o.evidence
            chosen=max(same,key=priority)
            if self.observed_state(chosen)=='UNKNOWN':uncertain.append(f'{rid}: missing state fields')
            else:observed.append(chosen)
        if not any(o.category=='USER_PROFILE' for o in observed):uncertain.append('No identity-linked primary account state')
        findings=[];remediations=[];verifications=[]
        for o in observed:
            action=self.treatment(o);state=self.observed_state(o);desired=STATES[action]
            if state!=desired:
                if action=='RETAIN':uncertain.append(f'{o.resource}: required retained record missing');continue
                finding={'DELETE':'REPORT_REMAINING_RECORD','REDACT':'REPORT_EXPOSED_PII','ANONYMIZE':'REPORT_EXPOSED_PII','DISABLE':'REPORT_ACTIVE_DATA_FLOW','BLOCK':'REPORT_RESTORE_RISK'}[action]
                report_state='ACTIVE' if action in {'DISABLE','BLOCK'} else 'PRESENT'
                findings.append(self.step(o,'FINDING',finding,report_state,o.evidence))
                operation={'DELETE':'DELETE_RECORD','REDACT':'REDACT_RECORD','ANONYMIZE':'ANONYMIZE_RECORD','DISABLE':'DISABLE_DATA_FLOW','BLOCK':'BLOCK_RESTORE'}[action]
                remediations.append(self.step(o,'REMEDIATION',operation,desired,''))
            verifications.append(self.step(o,'VERIFICATION',VERIFY[action],desired,o.evidence))
        incomplete=bool(findings or uncertain)
        if incomplete:
            for s in verifications:s['evidence_id']=''
        if uncertain:self.warnings.append((request['case_id'],uncertain))
        steps=finalize(findings+remediations+verifications)
        return {'case_id':request['case_id'],'deletion_status':'INCOMPLETE' if incomplete else 'COMPLETE','steps_json':json.dumps(steps,ensure_ascii=False,separators=(',',':'))}

    @staticmethod
    def step(o,phase,operation,state,evidence):
        return {'step_no':0,'phase':phase,'system_id':o.system,'resource_id':o.resource,'operation':operation,'state':state,'evidence_id':evidence}


def write_output(path,results):
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    temporary=path.with_suffix(path.suffix+'.tmp')
    with temporary.open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=['case_id','deletion_status','steps_json']);w.writeheader();w.writerows(sorted(results,key=lambda r:r['case_id']))
    temporary.replace(path)


def run_audit(dataset=None,requests=None,output=None,strict=False):
    engine=AuditEngine(dataset or ROOT/'dataset')
    rows=read_csv(requests or engine.dataset/'deletion_requests.csv')
    results=[engine.audit(r) for r in rows]
    if strict and engine.warnings:
        raise ValueError(f'{len(engine.warnings)} cases have unresolved evidence coverage; refusing to write output in strict mode')
    write_output(output or ROOT/'output.csv',results)
    return engine,results


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--dataset',type=Path,default=ROOT/'dataset')
    parser.add_argument('--requests',type=Path)
    parser.add_argument('--output',type=Path,default=ROOT/'output.csv')
    parser.add_argument('--strict',action='store_true',help='Refuse to write predictions if required evidence coverage is unresolved')
    parser.add_argument('--ocr-report',type=Path,help='Write diagnostic image-text matches; OCR does not establish ownership or state')
    args=parser.parse_args();started=time.perf_counter()
    engine,results=run_audit(args.dataset,args.requests,args.output,args.strict)
    if args.ocr_report:
        diagnostics=[]
        for request in read_csv(args.requests or args.dataset/'deletion_requests.csv'):
            aliases=engine.aliases_at(instant(request['audit_at']))
            subjects=aliases.get(normalize(request['email']),set())
            identifiers=[value for value,owners in aliases.items() if len(subjects)==1 and owners==subjects]
            hits=engine.ocr_inspector.scan_image_evidence(request['email'],request['audit_at'],identifiers=identifiers)
            if hits:diagnostics.append({'case_id':request['case_id'],'hits':hits})
        args.ocr_report.parent.mkdir(parents=True,exist_ok=True)
        args.ocr_report.write_text(json.dumps(diagnostics,ensure_ascii=False,indent=2),encoding='utf-8')
        print(f'OCR text matches in {len(diagnostics)} cases; these require review and do not change predictions.')
    print(f'Wrote {len(results)} cases to {args.output} in {time.perf_counter()-started:.2f}s; {len(engine.warnings)} cases have evidence coverage warnings.')
    for case,issues in engine.warnings[:10]:print(case,':','; '.join(issues))
