"""Cover integration: source integrity, raster placement and frozen vector layout."""
from pathlib import Path
import hashlib
import unittest
import fitz
from PIL import Image

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'books/book-001/cover-8g'
PREV=ROOT/'books/book-001/cover-8f'

class Cover8GTest(unittest.TestCase):
    def test_source_integrity_and_reconstruction_geometry(self):
        source=OUT/'assets/source-original.png';model=OUT/'assets/realesrgan-x4plus-candidate.png'
        self.assertEqual(hashlib.sha256(source.read_bytes()).hexdigest(),'592a55d6849e1bea6bc43d4b6c61d7b30122ffbad982c3afb4b3950c4923de79')
        with Image.open(source) as im:self.assertEqual(im.size,(1386,1135))
        with Image.open(model) as im:self.assertEqual(im.size,(5544,4540))
        for label,dimensions in [('source',(1386,1135)),('reconstructed',(5544,4540))]:
            with fitz.open(OUT/f'{label}-integrated-REVIEW.pdf') as doc:
                self.assertEqual(len(doc),1);page=doc[0]
                self.assertAlmostEqual(page.rect.width,1252.3772,places=2);self.assertEqual(page.rect.height,810)
                images=page.get_image_info(xrefs=True);self.assertEqual(len(images),1)
                im=images[0];self.assertEqual((im['width'],im['height']),dimensions)
                with Image.open(source if label=='source' else model) as original:
                    self.assertEqual(fitz.Pixmap(doc,im['xref']).samples,original.convert('RGB').tobytes())
                self.assertAlmostEqual(im['bbox'][2]-im['bbox'][0],612,places=3)
                self.assertAlmostEqual(im['bbox'][3]-im['bbox'][1],501.1745,places=2)
                for font in page.get_fonts(full=True):
                    self.assertNotIn('Helvetica',font[3]);self.assertTrue(doc.extract_font(font[0])[3])

    def test_frozen_layout_back_and_comparisons(self):
        with fitz.open(PREV/'B1-full-wrap-REVIEW.pdf') as baseline,fitz.open(OUT/'source-integrated-REVIEW.pdf') as source,fitz.open(OUT/'reconstructed-integrated-REVIEW.pdf') as candidate:
            self.assertEqual(baseline[0].get_text(),source[0].get_text());self.assertEqual(source[0].get_text(),candidate[0].get_text())
            # Back and spine must be exactly unchanged at review-render resolution.
            clip=fitz.Rect(0,0,631,810)
            samples=[doc[0].get_pixmap(matrix=fitz.Matrix(1,1),clip=clip,alpha=False).samples for doc in (baseline,source,candidate)]
            self.assertEqual(samples[0],samples[1]);self.assertEqual(samples[1],samples[2])
            # Text geometry, type and size are identical even though the scene changed.
            def spans(p):return [(s['text'],s['font'],s['size'],s['bbox']) for b in p.get_text('dict')['blocks'] for l in b.get('lines',[]) for s in l['spans']]
            self.assertEqual(spans(baseline[0]),spans(source[0]));self.assertEqual(spans(source[0]),spans(candidate[0]))
        for name,pages in [('actual-size-comparison-REVIEW.pdf',2),('enlarged-detail-comparison-REVIEW.pdf',6)]:
            with fitz.open(OUT/name) as doc:
                self.assertEqual(len(doc),pages)
                for page in doc:self.assertEqual((page.rect.width,page.rect.height),(612,792))
                if name.startswith('actual-size'):
                    for page,path in zip(doc,[OUT/'assets/source-original.png',OUT/'assets/realesrgan-x4plus-candidate.png']):
                        im=page.get_image_info(xrefs=True)[0];rect=fitz.Rect(im['bbox'])
                        self.assertAlmostEqual(rect.width,612,places=2)
                        self.assertAlmostEqual(rect.height,501.1745,places=2)
                        with Image.open(path) as original:
                            self.assertEqual(fitz.Pixmap(doc,im['xref']).samples,original.convert('RGB').tobytes())

if __name__=='__main__':unittest.main()
