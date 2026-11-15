"""Check batch-01 provenance, vector integrity, facing pairs and review gates."""
import csv
import hashlib
import json
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path
import fitz

ROOT=Path(__file__).resolve().parents[1]
BATCH=ROOT/'books/book-001/artwork/batch-01'


class BatchOneTests(unittest.TestCase):
    def test_artwork_provenance_and_unapproved_state(self):
        manifest=json.loads((BATCH/'manifest.json').read_text())
        rows=manifest['entries']
        self.assertEqual({r['species_id'] for r in rows},{'B02','B03','B04','B07','B13'})
        self.assertEqual(len({r['original_sha256'] for r in rows}),5)
        reference=ROOT/'books/book-001/artwork/candidates/cardinal-revised-review/source.png'
        ref_hash=hashlib.sha256(reference.read_bytes()).hexdigest()
        for r in rows:
            self.assertEqual(hashlib.sha256((ROOT/r['original_path']).read_bytes()).hexdigest(),r['original_sha256'])
            self.assertEqual(hashlib.sha256((ROOT/r['svg_path']).read_bytes()).hexdigest(),r['svg_sha256'])
            self.assertEqual(r['visual_reference_sha256'],ref_hash)
            self.assertEqual(hashlib.sha256((ROOT/r['vector_art_pdf']).read_bytes()).hexdigest(),r['vector_pdf_sha256'])
            self.assertFalse(r['human_approval'])
            self.assertFalse(r['print_approval'])
            self.assertIn(r['review_classification'],('READY_FOR_HUMAN_REVIEW','NEEDS_TARGETED_CORRECTION','REGENERATE_REQUIRED'))
            tags=[e.tag.rsplit('}',1)[-1] for e in ET.parse(ROOT/r['svg_path']).getroot().iter()]
            self.assertIn('path',tags)
            self.assertNotIn('image',tags)
            with fitz.open(ROOT/r['vector_art_pdf']) as doc:
                self.assertEqual(len(doc[0].get_images()),0)
                self.assertGreater(len(doc[0].get_drawings()),0)

    def test_facing_proof_and_layout(self):
        expected=[2,3,4,5,6,7,8,9,14,15,26,27]
        with fitz.open(BATCH/'six-bird-provisional-proof.pdf') as doc:
            self.assertEqual(len(doc),12)
            self.assertEqual(doc.xref_get_key(doc.pdf_catalog(),'PageLayout')[1],'/TwoPageLeft')
            for index,(page,number) in enumerate(zip(doc,expected)):
                self.assertEqual((page.rect.width,page.rect.height),(612,792))
                self.assertIn(f'intended page {number}',page.get_text())
                self.assertIn('FACTS AND ART AWAIT REVIEW',page.get_text())
                if index%2==0:
                    self.assertEqual(len(page.get_images()),0)
                    self.assertTrue('UNAPPROVED' in page.get_text() or 'PRINT / FACT CHECK PENDING' in page.get_text())
                left,right=(45,36) if number%2 else (36,45)
                for block in page.get_text('blocks'):
                    x0,y0,x1,y1=block[:4]
                    self.assertGreaterEqual(x0,left-1)
                    self.assertLessEqual(x1,612-right+1)
                    self.assertGreaterEqual(y0,35)
                    self.assertLessEqual(y1,757)

    def test_existing_revision_cannot_be_overwritten(self):
        from process_bird_batch import process
        source=ROOT/'books/book-001/artwork/batch-01/originals/B02.png'
        before=hashlib.sha256(source.read_bytes()).hexdigest()
        with self.assertRaises(FileExistsError):
            process('B02',source,'v1')
        self.assertEqual(hashlib.sha256(source.read_bytes()).hexdigest(),before)

    def test_remaining_schedule_has_exact_24_species(self):
        with (ROOT/'books/book-001/blueprint/SPECIES_LIST.csv').open(newline='') as stream:
            ids={row['species_id'] for row in csv.DictReader(stream)}
        selected={'B01','B02','B03','B04','B07','B13'}
        schedule=(BATCH/'REMAINING_BATCHES.md').read_text().split('## Future batch 2',1)[1]
        for sid in ids-selected:
            self.assertEqual(schedule.count(sid+' '),1,sid)
        self.assertEqual(len(ids-selected),24)
        for sid in selected:self.assertNotIn(sid+' ',schedule)


if __name__=='__main__':unittest.main()
