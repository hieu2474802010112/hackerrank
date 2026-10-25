"""Local OCR retrieval. Text matches are leads, never policy verdicts."""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess

from evidence_inspector import parse_time
from system_activity_mapper import canonical, identifiers_in


class OCRExtractionError(RuntimeError):
    pass


class OCRInspector:
    def __init__(self, dataset_dir='dataset', *, backend=None):
        self.dataset_dir = Path(dataset_dir).resolve()
        self.backend = backend
        self._cache = {}

    def extract(self, image_path):
        path = Path(image_path).resolve()
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        key = (str(path), digest)
        if key in self._cache:
            return dict(self._cache[key])
        try:
            if self.backend is not None:
                result = self.backend(path)
            elif shutil.which('tesseract'):
                import pytesseract
                from PIL import Image
                with Image.open(path) as image:
                    text = pytesseract.image_to_string(image, lang='eng')
                result = {'text': text, 'backend': 'tesseract', 'language': 'eng'}
            elif os.name == 'nt':
                powershell = Path(os.environ.get('SystemRoot', r'C:\Windows')) / 'System32/WindowsPowerShell/v1.0/powershell.exe'
                process = subprocess.run([str(powershell), '-NoProfile', '-NonInteractive',
                    '-File', str(Path(__file__).with_name('windows_ocr.ps1')),
                    '-ImagePath', str(path)], capture_output=True, encoding='utf-8',
                    errors='replace', timeout=60, check=True)
                result = json.loads(process.stdout.lstrip('\ufeff'))
            else:
                raise OCRExtractionError('No local OCR engine available; install Tesseract with English data')
            if not isinstance(result, dict) or not isinstance(result.get('text'), str) or not result['text'].strip():
                raise OCRExtractionError(f'OCR returned no usable text: {path.name}')
            result = {**result, 'path': str(path), 'sha256': digest,
                      'policy_verdict': None, 'requires_review': True}
        except OCRExtractionError:
            raise
        except Exception as error:
            raise OCRExtractionError(f'OCR failed for {path.name}: {error}') from error
        self._cache[key] = result
        return dict(result)

    def extract_text_from_image(self, image_path):
        return self.extract(image_path)['text']

    def scan_image_evidence(self, identifier, audit_at, *, identifiers=()):
        import csv
        terms = {canonical(value) for value in (identifier, *identifiers)
                 if value is not None and str(value).strip()}
        if not terms:
            raise ValueError('At least one non-empty identifier is required')
        cutoff = parse_time(audit_at)
        with (self.dataset_dir / 'evidence_files.csv').open(encoding='utf-8-sig', newline='') as stream:
            manifest = list(csv.DictReader(stream))
        matches = []
        for row in manifest:
            if parse_time(row['captured_at']) > cutoff:
                continue
            path = (self.dataset_dir / row['file_path']).resolve()
            if not path.is_relative_to(self.dataset_dir):
                raise ValueError('Evidence path escapes dataset')
            if path.suffix.casefold() not in {'.png', '.jpg', '.jpeg'}:
                continue
            result = self.extract(path)
            matched = terms & identifiers_in(result['text'])
            if matched:
                matches.append({**result, 'file_id': row['file_id'],
                    'captured_at': row['captured_at'], 'match_type': 'ocr_content',
                    'matched_identifiers': sorted(matched)})
        return matches
