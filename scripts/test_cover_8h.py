"""Ensure two comparison candidates preserve approved cover layout and raster placement."""
from pathlib import Path
import hashlib
import unittest
import fitz
from PIL import Image

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'books/book-001/cover-8h'
B=ROOT/'books/book-001/cover-8g'
SRC=ROOT/'books/book-001/cover-8f/B1-scene-native-crop.png'

class CoverComparisonTest(unittest.TestCase):
    def test_native_source_and_frozen_cover(self):
        self.assertEqual(hashlib.sha256(SRC.read_bytes()).hexdigest(),'3627d8fa6d1f0be90968f56368222db4635ce4e2e16096d8c1686b40e54ff365')
        a=OUT/'assets/B1-original-realesrgan-x4.png';b=B/'assets/realesrgan-x4plus-candidate.png'
        self.assertEqual(hashlib.sha256(b.read_bytes()).hexdigest(),'834567be0f1311c371b59cdbaf621ae3f0810beef480b7eb4c9b96833121f0a3')
        for p,size in [(SRC,(1102,903)),(a,(4408,3612)),(b,(5544,4540))]:
            with Image.open(p) as im:self.assertEqual(im.size,size)
        with fitz.open(OUT/'A-full-wrap-REVIEW.pdf') as d,fitz.open(B/'reconstructed-integrated-REVIEW.pdf') as e:
            self.assertEqual(d[0].rect,e[0].rect);self.assertEqual(d[0].get_text(),e[0].get_text())
            def spans(page):return [(s['text'],s['font'],s['size'],s['bbox']) for x in page.get_text('dict')['blocks'] for y in x.get('lines',[]) for s in y['spans']]
            self.assertEqual(spans(d[0]),spans(e[0]))
            clip=fitz.Rect(0,0,631,810)
            self.assertEqual(d[0].get_pixmap(clip=clip).samples,e[0].get_pixmap(clip=clip).samples)
            for doc,path in [(d,a),(e,b)]:
                imgs=doc[0].get_image_info(xrefs=True);self.assertEqual(len(imgs),1);image=imgs[0]
                self.assertAlmostEqual(image['bbox'][2]-image['bbox'][0],612,places=2)
                self.assertAlmostEqual(image['bbox'][3]-image['bbox'][1],501.1745,places=2)
                with Image.open(path) as im:self.assertEqual(fitz.Pixmap(doc,image['xref']).samples,im.convert('RGB').tobytes())
                for f in doc[0].get_fonts(full=True):self.assertNotIn('Helvetica',f[3]);self.assertTrue(doc.extract_font(f[0])[3])

    def test_review_outputs(self):
        with fitz.open(OUT/'A-front-back-actual-size-REVIEW.pdf') as doc:
            self.assertEqual(len(doc),2)
            for p in doc:self.assertEqual((p.rect.width,p.rect.height),(612,792))
        with fitz.open(OUT/'full-size-front-comparison-REVIEW.pdf') as doc:
            self.assertEqual(len(doc),1);self.assertEqual((doc[0].rect.width,doc[0].rect.height),(1240,840))
        for path in ('A-source-vs-reconstruction-details.pdf','A-vs-B-actual-size-details.pdf'):
            with fitz.open(OUT/path) as doc:
                self.assertEqual(len(doc),5)
                for p in doc:self.assertEqual((p.rect.width,p.rect.height),(612,792))
        with Image.open(OUT/'thumbnail-comparison.png') as im:self.assertEqual(im.size,(540,340))

if __name__=='__main__':unittest.main()
