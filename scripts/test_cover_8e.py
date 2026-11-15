"""Verify supplied template geometry, native scene crop and review-wrap invariants."""
import hashlib
import json
import unittest
from pathlib import Path
import fitz
from PIL import Image, ImageChops

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'books/book-001/cover-8e'

class TemplateWrapTest(unittest.TestCase):
    def test_template_and_original_crop(self):
        template=OUT/'source/KDP-template-original.pdf'
        self.assertEqual(hashlib.sha256(template.read_bytes()).hexdigest(),'15c08c0ad55b241d6dc11c097f1fc6b35467aa6ff6bd6b302f7191c6eb06b9fa')
        g=json.loads((OUT/'TEMPLATE_GEOMETRY.json').read_text())
        self.assertEqual(g['media_width'],1252.0)
        self.assertAlmostEqual(g['width'],1252.3772,places=3)
        self.assertEqual(g['height'],810.0)
        self.assertAlmostEqual(g['folds'][0],621,places=3)
        self.assertAlmostEqual(g['folds'][1],631.3772,places=3)
        self.assertAlmostEqual(g['barcode_top_origin'][0],459,places=2)
        self.assertAlmostEqual(g['barcode_top_origin'][1],696.6,places=2)
        self.assertAlmostEqual(g['barcode_top_origin'][2],603,places=2)
        self.assertAlmostEqual(g['barcode_top_origin'][3],783,places=2)
        with Image.open(ROOT/'books/book-001/cover-8d/B1-background.png') as source,Image.open(OUT/'B1-scene-native-crop.png') as actual:
            expected=source.crop((0,430,1102,1333));self.assertEqual(actual.size,(1102,903))
            self.assertIsNone(ImageChops.difference(expected,actual).getbbox())

    def test_wrap_copy_fonts_and_spacing(self):
        g=json.loads((OUT/'TEMPLATE_GEOMETRY.json').read_text())
        bar=fitz.Rect(g['barcode_top_origin']);back=fitz.Rect(18,18,612,792);front=fitz.Rect(g['folds'][1]+9,18,g['width']-18,792)
        with fitz.open(OUT/'B1-full-wrap-REVIEW.pdf') as doc:
            page=doc[0];self.assertAlmostEqual(page.rect.width,g['width'],places=2);self.assertEqual(page.rect.height,810)
            text=' '.join(page.get_text().split())
            for content in ['Backyard Bird Detectives','Color, Spot & Explore','A Coloring & Activity Book for Kids Ages 6–9','30 North American birds']:
                self.assertIn(content,text)
            for guide in ['Barcode Location & Size','Black Solid Line','Blue Dashed Line','REMOVE THIS TEMPLATE']:
                self.assertNotIn(guide,text)
            for block in page.get_text('dict')['blocks']:
                for line in block.get('lines',[]):
                    for span in line['spans']:
                        if not span['text'].strip():continue
                        box=fitz.Rect(span['bbox']);self.assertTrue(back.contains(box) or front.contains(box),span['text'])
                        self.assertFalse(box.intersects(bar),span['text'])
            for font in page.get_fonts(full=True):
                self.assertNotIn('Helvetica',font[3]);self.assertTrue(doc.extract_font(font[0])[3],font[3])
            images=page.get_image_info(xrefs=True);self.assertEqual(len(images),1);im=images[0]
            self.assertEqual((im['width'],im['height']),(1102,903))
            self.assertAlmostEqual(im['bbox'][2]-im['bbox'][0],612,places=2)
            self.assertLess(im['width']/((im['bbox'][2]-im['bbox'][0])/72),130)
            for xo in page.get_xobjects():
                if xo[2]==0:
                    r=fitz.Rect(xo[3]);top=fitz.Rect(r.x0,810-r.y1,r.x1,810-r.y0)
                    self.assertTrue(back.contains(top));self.assertFalse(bar.intersects(top))

    def test_actual_size_trim_pages(self):
        with fitz.open(OUT/'front-back-actual-size-REVIEW.pdf') as proof:
            self.assertEqual(len(proof),2)
            for page in proof:self.assertEqual(tuple(page.rect),(0,0,612,792))
            self.assertIn('Bird Detectives',proof[0].get_text());self.assertIn('bird detectives',proof[1].get_text())

if __name__=='__main__':unittest.main()
