"""Search eligible document text; a mention is not a privacy-policy verdict."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
from collections import defaultdict
from pathlib import Path

from evidence_inspector import parse_time
from system_activity_mapper import canonical, identifiers_in

RESOURCE_RE = re.compile(r'\b(?:account|analytics|search|support|export|data_flow|backup|audit_record|tombstone|legal_hold|object|marketing|cache|email_delivery)_\d+\b')
TIMESTAMP_RE = re.compile(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2})')


class UnstructuredInspector:
    SUPPORTED = {'.pdf','.png','.jpg','.jpeg','.txt','.log','.csv'}

    def __init__(self,dataset_dir=None,*,image_notes_path=None,image_text_extractor=None):
        self.dataset_dir = Path(dataset_dir or Path(__file__).resolve().parents[1]/'dataset').resolve()
        with (self.dataset_dir/'evidence_files.csv').open(encoding='utf-8-sig',newline='') as stream:
            self.manifest = list(csv.DictReader(stream))
        self.image_notes_path = Path(image_notes_path or Path(__file__).with_name('image_observations.md'))
        self.image_text_extractor = image_text_extractor
        self._notes = None
        self._cache = {}
        self._pdf_cache = {}
        self._pdf_versions = {}

    def extract_text_from_pdf(self,pdf_path):
        """Use the actual PDF text layer; compressed bytes are not readable text."""
        path = Path(pdf_path).resolve()
        signature = (path.stat().st_mtime_ns,path.stat().st_size)
        if path not in self._pdf_cache or self._pdf_versions[path]!=signature:
            import fitz
            with fitz.open(path) as document:
                pages = [page.get_text() for page in document]
            if not any(page.strip() for page in pages):
                raise ValueError(f'PDF has no text layer; OCR is required: {path.name}')
            self._pdf_cache[path] = pages
            self._pdf_versions[path] = signature
        return '\n'.join(self._pdf_cache[path])

    def reviewed_image_records(self,metadata,path):
        """Reuse literal reviewed fields only when the exact source hash matches."""
        if self._notes is None:
            if not self.image_notes_path.exists():
                self._notes = {}
            else:
                block = re.search(r'```json\s*(.*?)\s*```',self.image_notes_path.read_text(encoding='utf-8'),re.S)
                if not block:
                    raise ValueError('Image review cache has no JSON block')
                self._notes = {r['file_path']:r for r in json.loads(block[1])}
        entry = self._notes.get(metadata['file_path'])
        if entry is None:
            raise ValueError(f'Image requires OCR or a reviewed extraction: {Path(path).name}')
        if hashlib.sha256(Path(path).read_bytes()).hexdigest()!=entry['sha256']:
            raise ValueError(f'Image changed; review required: {Path(path).name}')
        return entry['records']

    def _extract(self,metadata,path):
        key = (metadata['file_id'],str(path),path.stat().st_mtime_ns,path.stat().st_size)
        if key in self._cache:
            return self._cache[key]
        suffix=path.suffix.casefold();units=[]
        def add(text,location,method,observed=None):
            if not text.strip():return
            tokens=identifiers_in(text)|{canonical(r) for r in RESOURCE_RE.findall(text)}
            units.append({'text':text,'location':location,'method':method,
                          'observed':parse_time(observed or metadata['captured_at']),'tokens':tokens})
        if suffix=='.pdf':
            self.extract_text_from_pdf(path)
            for page,text in enumerate(self._pdf_cache[path],1):add(text,f'page:{page}','pdf_text_layer')
        elif suffix in {'.png','.jpg','.jpeg'}:
            if self.image_text_extractor is not None:
                text=self.image_text_extractor(path)
                if not isinstance(text,str) or not text.strip():
                    raise ValueError(f'OCR returned no usable text: {path.name}')
                add(text,'image','ocr_callback')
            else:
                for number,record in enumerate(self.reviewed_image_records(metadata,path),1):
                    add(json.dumps(record,ensure_ascii=False),f'reviewed_record:{number}','reviewed_image_fields')
        elif suffix=='.csv':
            with path.open(encoding='utf-8-sig',newline='') as stream:
                for number,row in enumerate(csv.DictReader(stream),2):
                    times=[parse_time(row[k]) for k in ('observed_at','event_time','captured_at','recorded_at') if row.get(k)]
                    add(json.dumps(row,ensure_ascii=False),f'row:{number}','csv_text',max(times) if times else None)
        else:
            for number,line in enumerate(path.read_text(encoding='utf-8-sig').splitlines(),1):
                # Leading event timestamps describe an observation. Dates merely
                # mentioned later in prose are not treated as observation times.
                timestamp=TIMESTAMP_RE.match(line.lstrip('- '))
                add(line,f'line:{number}','plain_text',timestamp[0] if timestamp else None)
        index=defaultdict(set)
        for number,unit in enumerate(units):
            for token in unit['tokens']:index[token].add(number)
        self._cache[key]=(units,index)
        return units,index

    def scan_unstructured_evidence(self,identifier,audit_at,*,identifiers=()):
        cutoff=parse_time(audit_at)
        terms={canonical(term) for term in (identifier,*identifiers) if term is not None and str(term).strip()}
        if not terms:raise ValueError('At least one non-empty identifier is required')
        matches=[]
        for metadata in sorted(self.manifest,key=lambda m:(parse_time(m['captured_at']),m['file_id'])):
            if parse_time(metadata['captured_at'])>cutoff:continue
            path=(self.dataset_dir/metadata['file_path']).resolve()
            if not path.is_relative_to(self.dataset_dir):raise ValueError('Evidence path escapes dataset')
            if path.suffix.casefold() not in self.SUPPORTED:continue
            units,index=self._extract(metadata,path)
            selected=set().union(*(index.get(term,set()) for term in terms))
            for number in sorted(selected):
                unit=units[number]
                if unit['observed']>cutoff:continue
                matches.append({'file_id':metadata['file_id'],'file_name':path.name,
                    'file_type':path.suffix[1:].casefold(),'path':str(path),
                    'captured_at':metadata['captured_at'],'observed_at':unit['observed'].isoformat(),
                    'location':unit['location'],'extraction_method':unit['method'],
                    'matched_identifiers':sorted(terms&unit['tokens']),
                    'resource_mentions':sorted(set(RESOURCE_RE.findall(unit['text']))),
                    'snippet':unit['text'][:500],'policy_verdict':None})
        return matches


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--dataset',type=Path)
    parser.add_argument('--identifier',action='append',required=True)
    parser.add_argument('--audit-at',required=True)
    args=parser.parse_args()
    rows=UnstructuredInspector(args.dataset).scan_unstructured_evidence(
        args.identifier[0],args.audit_at,identifiers=args.identifier[1:])
    print(json.dumps(rows,ensure_ascii=False,indent=2))
