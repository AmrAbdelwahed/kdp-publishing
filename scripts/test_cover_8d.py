"""Check review copy, image placement, font use and conceptual wrap labeling."""
import hashlib
import json
import unittest
from pathlib import Path
import fitz
from PIL import Image

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'books/book-001/cover-8d'

class CoverReviewTest(unittest.TestCase):
    def test_front_copy_and_native_resolution(self):
        provenance=json.loads((OUT/'ARTWORK_PROVENANCE.json').read_text())
        self.assertEqual([x['version'] for x in provenance],['B1','B2'])
        for row in provenance:
            v=row['version']; p=OUT/row['asset']
            self.assertEqual(hashlib.sha256(p.read_bytes()).hexdigest(),row['sha256'])
            with Image.open(p) as source:
                self.assertEqual(source.size,tuple(row['native_pixels']))
            with fitz.open(OUT/f'{v}-front-review.pdf') as d:
                page=d[0];self.assertEqual(tuple(page.rect),(0,0,612,792))
                text=' '.join(page.get_text().split())
                for wanted in ('Backyard Bird Detectives','Color, Spot & Explore',
                    'A Coloring & Activity Book for Kids Ages 6–9','30 Birds to Color, Identify & Discover'):
                    self.assertIn(wanted,text)
                images=page.get_image_info(xrefs=True);self.assertEqual(len(images),1)
                im=images[0]; self.assertEqual((im['width'],im['height']),(1102,1427))
                self.assertEqual(tuple(im['bbox']),(0,0,612,792))
                self.assertLess(im['width']/8.5,300)
                fonts={x[3]:x[0] for x in page.get_fonts(full=True)}
                for block in page.get_text('dict')['blocks']:
                    for line in block.get('lines',[]):
                        for span in line['spans']:
                            if not span['text'].strip():continue
                            bbox=span['bbox'];self.assertGreaterEqual(min(bbox[0],bbox[1],612-bbox[2],792-bbox[3]),18)
                            name=span['font'];matches=[xref for font,xref in fonts.items() if name in font]
                            self.assertTrue(matches,f'font not found: {name}')
                            self.assertTrue(any(d.extract_font(x)[3] for x in matches),f'visible font not embedded: {name}')

    def test_back_and_wrap_are_review_only(self):
        with fitz.open(OUT/'back-cover-review.pdf') as d:
            text=' '.join(d[0].get_text().split())
            for word in ('30 North American birds','black-and-white line art','BARCODE AREA — PLACEHOLDER','REVIEW DRAFT'):
                self.assertIn(word,text)
            self.assertFalse(d[0].get_images(),'Back inset should remain vector')
        with fitz.open(OUT/'provisional-wrap-NOT-TO-SCALE.pdf') as d:
            text=d[0].get_text();self.assertIn('NOT TO SCALE',text);self.assertIn('OFFICIAL KDP TEMPLATE REQUIRED',text)
            for word in d[0].get_text('words'):
                # At and below the two panels, nothing should be typeset on the arbitrary spine band.
                if word[1]>=55:self.assertFalse(word[0]<662 and word[2]>652)

if __name__=='__main__':unittest.main()
