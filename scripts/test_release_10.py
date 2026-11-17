"""Check release exports against frozen candidates; no print approval implied."""
import hashlib
import io
import json
import re
import unittest
from pathlib import Path

import fitz
import numpy as np
from PIL import Image, ImageCms

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'books/book-001/release-10'
OLD_INTERIOR = ROOT / 'books/book-001/woodpecker-revisions/64-page-interior-woodpecker-REVIEW.pdf'
OLD_COVER = ROOT / 'books/book-001/preflight-9/selected-cover-full-wrap-CANDIDATE.pdf'


class ReleaseCandidateTests(unittest.TestCase):
    def assert_clean(self, doc):
        self.assertEqual(doc.xref_get_key(-1, 'Info')[0], 'null')
        self.assertEqual(doc.xref_xml_metadata(), 0)
        self.assertFalse(doc.is_encrypted)
        for page in doc:
            self.assertEqual(page.get_links(), [])
            self.assertEqual(list(page.annots() or []), [])
            for f in page.get_fonts(full=True):
                self.assertTrue(doc.extract_font(f[0])[3], f[3])
                kind, val = doc.xref_get_key(f[0], 'ToUnicode')
                if kind == 'xref':
                    stream = doc.xref_stream(int(val.split()[0]))
                    self.assertTrue(all(int(n) <= 100 for n in re.findall(rb'(\d+) beginbfchar', stream)))

    def test_interior_only_credits_change(self):
        with fitz.open(OLD_INTERIOR) as old, fitz.open(OUT / 'interior-release-candidate.pdf') as new:
            self.assertEqual(len(new), 64)
            self.assertEqual(new.xref_get_key(new.pdf_catalog(), 'PageLayout')[1], '/TwoPageRight')
            self.assert_clean(new)
            for i in range(64):
                a, b = old[i], new[i]
                self.assertEqual(tuple(b.rect), (0, 0, 612, 792))
                self.assertEqual(b.get_images(), [])
                if i < 63:
                    self.assertEqual(a.get_text(), b.get_text())
                    self.assertEqual(a.get_pixmap(alpha=False).samples, b.get_pixmap(alpha=False).samples, i + 1)
                else:
                    before, after = a.get_text(), b.get_text()
                    self.assertIn('see accompanying font', before)
                    self.assertNotIn('accompanying font', after)
                    self.assertIn('AI-generated illustrations. Fonts: DejaVu Sans; Bitstream Vera license.', after)
                    for rect in (fitz.Rect(0, 0, 612, 612), fitz.Rect(0, 640, 612, 792)):
                        self.assertEqual(a.get_pixmap(clip=rect, alpha=False).samples, b.get_pixmap(clip=rect, alpha=False).samples)
                for block in b.get_text('dict')['blocks']:
                    for line in block.get('lines', []):
                        for span in line['spans']:
                            if span['text'].strip():
                                x0, y0, x1, y1 = span['bbox']
                                self.assertGreaterEqual(min(x0, y0, 612-x1, 792-y1), 27)
                for shape in b.get_drawings():
                    rect = shape['rect']
                    self.assertGreaterEqual(min(rect.x0, rect.y0, 612-rect.x1, 792-rect.y1), 27)
                self.assertNotIn('REVIEW DRAFT', b.get_text())
            for n in (18, 20):
                self.assertNotIn('Fm1', [x[1] for x in new[n-1].get_xobjects() if x[2] == 0])
                self.assertIn('fzFrm0', [x[1] for x in new[n-1].get_xobjects() if x[2] == 0])
            # Ensure the old nested artwork streams are not retained anywhere.
            old_streams = set()
            for n in (18, 20):
                for x in old[n-1].get_xobjects():
                    if x[1] == 'Fm1' and x[2] != 0:
                        old_streams.add(hashlib.sha256(old.xref_stream(x[0])).digest())
            self.assertEqual(len(old_streams), 2)
            new_streams = {hashlib.sha256(new.xref_stream(x)).digest() for x in range(1, new.xref_length()) if new.xref_is_stream(x)}
            self.assertTrue(old_streams.isdisjoint(new_streams))

    def test_cover_geometry_text_and_color(self):
        with fitz.open(OLD_COVER) as old, fitz.open(OUT / 'cover-b1-a-cmyk-release-candidate.pdf') as new:
            self.assert_clean(new)
            a, b = old[0], new[0]
            self.assertEqual(len(new), 1)
            self.assertEqual(tuple(a.rect), tuple(b.rect))
            self.assertAlmostEqual(b.rect.width, 17.394128 * 72, places=2)
            self.assertEqual(b.rect.height, 810)
            self.assertEqual(a.get_text(), b.get_text())
            wa, wb = a.get_text('words'), b.get_text('words')
            self.assertEqual(wa, wb)
            images = b.get_image_info(xrefs=True)
            self.assertEqual(len(images), 1)
            self.assertEqual((images[0]['width'], images[0]['height'], images[0]['cs-name']), (4408, 3612, 'DeviceCMYK'))
            self.assertFalse(images[0]['has-mask'])
            # Compare source and stored converted pixels on a spatial grid.
            source_image = Image.open(io.BytesIO(old.extract_image(a.get_image_info(xrefs=True)[0]['xref'])['image'])).convert('RGB')
            samples = np.asarray(source_image)[::173, ::173].copy()
            transform = ImageCms.buildTransformFromOpenProfiles(
                ImageCms.getOpenProfile('/usr/share/color/icc/ghostscript/default_rgb.icc'),
                ImageCms.getOpenProfile('/usr/share/color/icc/ghostscript/default_cmyk.icc'),
                'RGB', 'CMYK', renderingIntent=1)
            expected = np.asarray(ImageCms.applyTransform(Image.fromarray(samples, 'RGB'), transform))
            pix = fitz.Pixmap(new, images[0]['xref'])
            actual = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width, 4)[::173, ::173]
            self.assertTrue(np.array_equal(expected, actual))
            self.assertEqual(tuple(images[0]['bbox']), tuple(a.get_image_info(xrefs=True)[0]['bbox']))
            streams = set(b.get_contents()) | {x[0] for x in b.get_xobjects()}
            for x in streams:
                data = new.xref_stream(x)
                self.assertNotRegex(data, rb'(?<![\w.])(?:[+-]?(?:\d+\.?\d*|\.\d+)\s+){3}(?:rg|RG)\b')
            self.assertNotIn('ICCBased', new.xref_object(images[0]['xref']))
            barcode = fitz.Rect(459, 696.6, 603, 783)
            for block in b.get_text('dict')['blocks']:
                for line in block.get('lines', []):
                    for span in line['spans']:
                        if span['text'].strip():
                            rect = fitz.Rect(span['bbox'])
                            self.assertFalse(barcode.intersects(rect))
                            self.assertFalse(rect.intersects(fitz.Rect(621, 0, 631.3772, 810)))
            for phrase in ('Black Solid Line', 'Blue Dashed Line', 'REMOVE THIS TEMPLATE', 'Barcode Location & Size'):
                self.assertNotIn(phrase, b.get_text())

    def test_packet_uses_current_interior(self):
        sequence = [n for art in [4, 6, 18, 20, 26, 30, 44, 54, 58, 60] for n in (art, art+1)] + [63, 64]
        with fitz.open(OUT / 'interior-release-candidate.pdf') as interior, fitz.open(OUT / 'physical-review-packet.pdf') as packet:
            self.assertEqual(len(packet), 25)
            for i, n in enumerate(sequence, start=1):
                self.assertEqual(interior[n-1].get_pixmap(alpha=False).samples, packet[i].get_pixmap(alpha=False).samples)
            self.assertEqual(tuple(packet[-1].rect), (0, 0, 612, 792))

    def test_color_metrics_and_source_hash(self):
        info = json.loads((OUT / 'color-measurements.json').read_text())
        self.assertEqual(info['scene_pixels'], [4408, 3612])
        self.assertEqual(info['vector_rgb8_to_cmyk8']['(0, 0, 0)'], [0, 0, 0, 255])
        self.assertGreater(info['mean_absolute_rgb_channel_change'], 0)
        selection = json.loads((ROOT / 'books/book-001/preflight-9/COVER_SELECTION.json').read_text())
        for key in ('source_scene', 'selected_scene', 'source_wrap'):
            self.assertEqual(hashlib.sha256((ROOT / selection[key]).read_bytes()).hexdigest(), selection[key + '_sha256'])


if __name__ == '__main__':
    unittest.main()
