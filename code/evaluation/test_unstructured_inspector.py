"""Unstructured retrieval keeps text mentions separate from policy findings."""
import csv
import hashlib
import json
import sys
import tempfile
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from unstructured_inspector import UnstructuredInspector

T='2026-09-15T12:00:00Z'


class UnstructuredInspectorTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.root=Path(self.temp.name);self.rows=[]

    def tearDown(self):self.temp.cleanup()

    def file(self,name,text,captured=T):
        path=self.root/name;path.write_text(text,encoding='utf-8')
        self.rows.append([name,name,'fixture',captured]);return path

    def inspector(self,**kwargs):
        with (self.root/'evidence_files.csv').open('w',encoding='utf-8',newline='') as f:
            w=csv.writer(f);w.writerow(['file_id','file_path','origin','captured_at']);w.writerows(self.rows)
        return UnstructuredInspector(self.root,**kwargs)

    def test_exact_aliases_phone_and_future_records(self):
        self.file('events.log',T+' owner user_05 old@example.test +1 (234) 567-8901 resource account_1\n'
                  +T+' owner user_050 old.jr@example.test resource account_2\n'
                  +'2026-09-16T00:00:00Z owner user_05 resource account_3\n')
        self.file('future.txt','user_05 account_4','2026-09-16T00:00:00Z')
        matches=self.inspector().scan_unstructured_evidence('user_05',T,
            identifiers=['old@example.test','+12345678901'])
        self.assertEqual(len(matches),1)
        self.assertEqual(matches[0]['resource_mentions'],['account_1'])
        self.assertEqual(matches[0]['location'],'line:1')
        self.assertIsNone(matches[0]['policy_verdict'])

    def test_compressed_pdf_text_layer_and_page_provenance(self):
        import fitz
        path=self.root/'report.pdf'
        document=fitz.open();page=document.new_page();page.insert_text((50,50),'person@example.test account_1')
        page=document.new_page();page.insert_text((50,50),'other@example.test account_2')
        document.save(path,deflate=True);document.close()
        self.rows.append(['pdf','report.pdf','fixture',T])
        matches=self.inspector().scan_unstructured_evidence('person@example.test',T)
        self.assertEqual(len(matches),1)
        self.assertEqual(matches[0]['location'],'page:1')
        self.assertEqual(matches[0]['extraction_method'],'pdf_text_layer')

    def test_image_review_digest_and_record_boundaries(self):
        image=self.root/'console.png';image.write_bytes(b'fixture image bytes')
        self.rows.append(['image','console.png','fixture',T])
        notes=self.root/'notes.md'
        notes.write_text('```json\n'+json.dumps([{'file_path':'console.png',
            'sha256':hashlib.sha256(image.read_bytes()).hexdigest(),'records':[
                {'resource_id':'account_1','email':'person@example.test'},
                {'resource_id':'account_2','email':'person.jr@example.test'}]}])+'\n```',encoding='utf-8')
        inspector=self.inspector(image_notes_path=notes)
        matches=inspector.scan_unstructured_evidence('person@example.test',T)
        self.assertEqual(len(matches),1)
        self.assertEqual(matches[0]['resource_mentions'],['account_1'])
        image.write_bytes(b'changed source')
        with self.assertRaisesRegex(ValueError,'Image changed'):
            inspector.scan_unstructured_evidence('person@example.test',T)

    def test_unknown_image_requires_ocr_and_callback_is_explicit(self):
        self.file('unknown.jpg','fixture image bytes')
        with self.assertRaisesRegex(ValueError,'requires OCR'):
            self.inspector(image_notes_path=self.root/'absent.md').scan_unstructured_evidence('person@example.test',T)
        matches=self.inspector(image_text_extractor=lambda path:'person@example.test account_1').scan_unstructured_evidence('person@example.test',T)
        self.assertEqual(matches[0]['extraction_method'],'ocr_callback')

    def test_unlisted_file_and_future_csv_row_are_excluded(self):
        self.file('rows.csv','email,observed_at\nperson@example.test,2026-09-16T00:00:00Z\n')
        (self.root/'unlisted.txt').write_text('person@example.test',encoding='utf-8')
        self.assertEqual(self.inspector().scan_unstructured_evidence('person@example.test',T),[])

    def test_image_only_pdf_and_empty_queries_fail_explicitly(self):
        import fitz
        path=self.root/'scanned.pdf';document=fitz.open();document.new_page();document.save(path);document.close()
        self.rows.append(['pdf','scanned.pdf','fixture',T])
        inspector=self.inspector()
        with self.assertRaisesRegex(ValueError,'OCR is required'):
            inspector.scan_unstructured_evidence('person@example.test',T)
        with self.assertRaisesRegex(ValueError,'non-empty'):
            inspector.scan_unstructured_evidence('',T)


if __name__=='__main__':unittest.main()
