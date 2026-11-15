"""Check frozen B1 design, measured references and official formula."""
import hashlib
import json
import math
import unittest
from pathlib import Path
import fitz
from PIL import Image,ImageChops

ROOT=Path(__file__).resolve().parents[1]
PREV=ROOT/'books/book-001/cover-8e'
OUT=ROOT/'books/book-001/cover-8f'

class CoverPreflightTest(unittest.TestCase):
    def test_formula_and_frozen_design(self):
        spine=64*.002252; width=.125+8.5+spine+8.5+.125
        with fitz.open(PREV/'B1-full-wrap-REVIEW.pdf') as old,fitz.open(OUT/'B1-full-wrap-REVIEW.pdf') as new:
            self.assertAlmostEqual(new[0].rect.width,width*72,places=2)
            self.assertAlmostEqual(new[0].rect.height,11.25*72,places=2)
            self.assertEqual(old[0].get_pixmap().samples,new[0].get_pixmap().samples)
            for font in new[0].get_fonts(full=True):
                self.assertNotIn('Helvetica',font[3]);self.assertTrue(new.extract_font(font[0])[3])
            im=new[0].get_image_info(xrefs=True);self.assertEqual(len(im),1)
            self.assertEqual((im[0]['width'],im[0]['height']),(1102,903))
            self.assertLess(im[0]['width']/8.5,130)
        with fitz.open(OUT/'B1-vector-base-ARTWORK-MISSING.pdf') as base:
            self.assertEqual(base[0].get_image_info(),[])
            self.assertIn('Bird Detectives',base[0].get_text())
        with fitz.open(OUT/'front-back-actual-size-REVIEW.pdf') as proof:
            self.assertEqual(len(proof),2)
            for page in proof:self.assertEqual(tuple(page.rect),(0,0,612,792))

    def test_reference_windows_preserve_native_pixels_and_dimensions(self):
        rows=json.loads((OUT/'REFERENCE_SLOTS.json').read_text());self.assertEqual(len(rows),3)
        with Image.open(PREV/'B1-scene-native-crop.png') as source:
            for row in rows:
                path=OUT/row['file']; self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(),row['sha256'])
                x0,y0,x1,y1=row['source_rect_px'];w=(x1-x0)*8.5/1102;h=(y1-y0)*11/1427
                self.assertEqual(row['minimum_pixels_300ppi'],[math.ceil(w*300),math.ceil(h*300)])
                self.assertEqual(row['original_pixels'],[x1-x0,y1-y0]);self.assertIn('REFERENCE ONLY',row['status'])
                with Image.open(path) as crop:
                    self.assertIsNone(ImageChops.difference(source.crop((x0,y0,x1,y1)),crop).getbbox())

if __name__=='__main__':unittest.main()
