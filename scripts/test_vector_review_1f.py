"""Check review proof, canvas-only framing and unmodified original art."""
import hashlib
import json
from pathlib import Path
import unittest
import xml.etree.ElementTree as ET
import fitz

ROOT=Path(__file__).resolve().parents[1]
ART=ROOT/'books/book-001/artwork'
OLD=ART/'vector-recovery'
NEW=ART/'vector-review-1f'


class ReviewProofTests(unittest.TestCase):
    def test_canvas_change_never_changes_existing_paths(self):
        entries=json.loads((ART/'manifest.json').read_text())
        for name in ('cardinal','robin','chickadee'):
            old=ET.parse(OLD/f'{name}-provisional.svg').getroot()
            new=ET.parse(NEW/f'{name}-review-required.svg').getroot()
            paths=lambda root:[x.attrib for x in root.iter() if x.tag.endswith('path')]
            self.assertEqual(paths(old),paths(new))
            if name=='chickadee':
                self.assertEqual(new.get('viewBox'),'30 30 1299 1412')
            else:
                self.assertEqual(old.attrib,new.attrib)
            entry=next(x for x in entries if x['species']==name)
            self.assertEqual(hashlib.sha256((ROOT/entry['path']).read_bytes()).hexdigest(),entry['sha256'])
            self.assertFalse(entry['human_approved'])

    def test_proof_has_six_vector_pages_and_approval_labels(self):
        with fitz.open(NEW/'six-page-review-proof.pdf') as doc:
            self.assertEqual(len(doc),6)
            for i,page in enumerate(doc):
                self.assertEqual((page.rect.width,page.rect.height),(612,792))
                if i%2==0:
                    self.assertEqual(len(page.get_images()),0)
                    self.assertIn('PROVISIONAL VECTOR - NOT APPROVED',page.get_text())
                    self.assertGreater(len(page.get_drawings()),0)
            for index,num in enumerate((2,3,8,9,6,7)):
                self.assertIn(f'intended page {num}',doc[index].get_text())
        with fitz.open(str(NEW/'chickadee-review-required.svg')) as doc:
            artwork=doc[0]
            bbox=None
            for drawing in artwork.get_drawings():
                rect=fitz.Rect(drawing['rect'])
                bbox=rect if bbox is None else bbox.include_rect(rect)
            self.assertIsNotNone(bbox)
            self.assertGreater(bbox.x0,50)
            self.assertGreater(artwork.rect.width-bbox.x1,50)
            self.assertGreater(bbox.y0,50)
            self.assertGreater(artwork.rect.height-bbox.y1,50)


if __name__=='__main__':unittest.main()
