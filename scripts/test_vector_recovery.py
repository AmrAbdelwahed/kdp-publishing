"""Check vector experiment outputs and original evidence identity."""
import hashlib
import json
from pathlib import Path
import unittest
import xml.etree.ElementTree as ET
import fitz
from PIL import Image

ROOT=Path(__file__).resolve().parents[1]
ART=ROOT/'books/book-001/artwork'
OUT=ART/'vector-recovery'


class VectorRecoveryTests(unittest.TestCase):
    def test_sources_and_vectors(self):
        entries=json.loads((ART/'manifest.json').read_text())
        measured=json.loads((OUT/'measurements.json').read_text())
        self.assertEqual(len(measured),3)
        for m in measured:
            entry=next(x for x in entries if x['species']==m['species'])
            self.assertEqual(hashlib.sha256((ROOT/entry['path']).read_bytes()).hexdigest(),entry['sha256'])
            self.assertEqual(m['source_sha256'],entry['sha256'])
            self.assertEqual(m['added_padding_pixels'],80)
            svg=OUT/(m['species']+'-provisional.svg')
            tags=[x.tag.rsplit('}',1)[-1] for x in ET.parse(svg).getroot().iter()]
            self.assertIn('path',tags)
            self.assertNotIn('image',tags)
            with fitz.open(OUT/(m['species']+'-vector-art.pdf')) as pdf:
                self.assertEqual(len(pdf[0].get_images()),0)
                self.assertGreater(len(pdf[0].get_drawings()),0)
            with Image.open(OUT/(m['species']+'-vector-300dpi.png')) as im:
                self.assertEqual(im.size,(2550,3300))
            with fitz.open(OUT/(m['species']+'-comparison-print-size.pdf')) as pdf:
                self.assertEqual(len(pdf),2)
                self.assertEqual((pdf[0].rect.width,pdf[0].rect.height),(612,792))
                self.assertGreater(len(pdf[0].get_images()),0)
                self.assertEqual(len(pdf[1].get_images()),0)
                self.assertGreater(len(pdf[1].get_drawings()),0)

    def test_vector_proof_remains_unapproved(self):
        with fitz.open(OUT/'three-bird-provisional-vector-prototype.pdf') as pdf:
            self.assertEqual(len(pdf),6)
            for i in (0,2,4):
                self.assertIn('PROVISIONAL VECTOR - NOT APPROVED',pdf[i].get_text())
                self.assertEqual(len(pdf[i].get_images()),0)
                self.assertGreater(len(pdf[i].get_drawings()),0)


if __name__=='__main__':unittest.main()
