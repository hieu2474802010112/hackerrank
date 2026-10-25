import csv
from pathlib import Path
import sys
import tempfile
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from ocr_inspector import OCRInspector, OCRExtractionError

T='2026-09-15T12:00:00Z'

class OCRTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.root=Path(self.temp.name)
        self.path=self.root/'person@example.test.png';self.path.write_bytes(b'image')
        with (self.root/'evidence_files.csv').open('w',newline='') as f:
            w=csv.writer(f);w.writerow(['file_id','file_path','captured_at'])
            w.writerow(['image',self.path.name,T])

    def tearDown(self):self.temp.cleanup()

    def test_exact_match_cutoff_and_filename_is_not_evidence(self):
        inspector=OCRInspector(self.root,backend=lambda p:{'text':'person.jr@example.test user_050','backend':'fixture'})
        self.assertEqual(inspector.scan_image_evidence('person@example.test',T),[])
        self.assertEqual(inspector.scan_image_evidence('user_05',T),[])
        self.assertEqual(inspector.scan_image_evidence('person.jr@example.test','2026-09-14T12:00:00Z'),[])
        hit=inspector.scan_image_evidence('person.jr@example.test',T)[0]
        self.assertIsNone(hit['policy_verdict']);self.assertTrue(hit['requires_review'])
        self.assertEqual(hit['file_id'],'image')

    def test_cache_invalidates_when_source_changes(self):
        calls=[]
        def backend(p):calls.append(p);return {'text':'user_05','backend':'fixture'}
        inspector=OCRInspector(self.root,backend=backend)
        before=inspector.extract(self.path);inspector.extract(self.path)
        self.assertEqual(len(calls),1)
        self.path.write_bytes(b'changed image')
        after=inspector.extract(self.path)
        self.assertEqual(len(calls),2);self.assertNotEqual(before['sha256'],after['sha256'])

    def test_failure_and_empty_text_are_explicit(self):
        with self.assertRaises(OCRExtractionError):
            OCRInspector(self.root,backend=lambda p:{'text':''}).extract(self.path)
        def broken(p):raise RuntimeError('engine unavailable')
        with self.assertRaisesRegex(OCRExtractionError,'engine unavailable'):
            OCRInspector(self.root,backend=broken).extract(self.path)
        with self.assertRaises(ValueError):
            OCRInspector(self.root).scan_image_evidence('',T)

if __name__=='__main__':unittest.main()
