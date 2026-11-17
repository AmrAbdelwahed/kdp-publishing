"""Regression checks for the two source-preserving review replacements."""
import csv
import hashlib
import json
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path
import fitz

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'books/book-001/woodpecker-revisions'
OLD = ROOT / 'books/book-001/preflight-9'


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


class WoodpeckerRevisionTest(unittest.TestCase):
    def test_sources_and_true_vectors(self):
        records = json.loads((OUT / 'ARTWORK_REVISIONS.json').read_text())
        self.assertEqual([(r['species_id'], r['page']) for r in records], [('B09', 18), ('B10', 20)])
        names = ['Downy Woodpecker on Tree Trunk.png', 'Unfilled Wing Hairy Woodpecker.png']
        for r, name in zip(records, names):
            self.assertEqual(digest(ROOT / name), r['source_sha256'])
            self.assertEqual(digest(ROOT / r['source']), r['source_sha256'])
            self.assertEqual(digest(ROOT / r['svg']), r['svg_sha256'])
            self.assertTrue(r['user_visual_candidate_approval'])
            self.assertFalse(r['scientific_approval'])
            self.assertFalse(r['physical_print_approval'])
            tags = [e.tag.rsplit('}', 1)[-1] for e in ET.parse(ROOT / r['svg']).getroot().iter()]
            self.assertIn('path', tags)
            self.assertNotIn('image', tags)
            quality = json.loads((ROOT / r['svg']).with_name('quality.json').read_text())
            self.assertGreater(quality['threshold_mask_iou'], .89)
            self.assertEqual(quality['source_enclosed_white_regions_25px'], quality['vector_enclosed_white_regions_25px'])
            with fitz.open(ROOT / r['vector_pdf']) as art:
                self.assertEqual(art[0].get_images(), [])

    def test_only_two_art_regions_change(self):
        with fitz.open(OLD / 'interior-candidate-REVIEW.pdf') as old, fitz.open(OUT / '64-page-interior-woodpecker-REVIEW.pdf') as new:
            self.assertEqual(len(new), 64)
            for i in range(64):
                a, b = old[i], new[i]
                self.assertEqual(tuple(a.rect), tuple(b.rect))
                self.assertEqual(a.get_text(), b.get_text())
                self.assertEqual(b.get_images(), [])
                if i not in (17, 19):
                    self.assertEqual(a.get_pixmap(alpha=False).samples, b.get_pixmap(alpha=False).samples, i + 1)
                else:
                    rect = fitz.Rect(121, 149, 491, 601)
                    for clip in [fitz.Rect(0, 0, 612, rect.y0), fitz.Rect(0, rect.y1, 612, 792), fitz.Rect(0, rect.y0, rect.x0, rect.y1), fitz.Rect(rect.x1, rect.y0, 612, rect.y1)]:
                        self.assertEqual(a.get_pixmap(clip=clip, alpha=False).samples, b.get_pixmap(clip=clip, alpha=False).samples, i + 1)
                    self.assertNotEqual(a.get_pixmap(clip=rect).samples, b.get_pixmap(clip=rect).samples)
                    self.assertTrue(any(x[1].startswith('fzFrm') for x in b.get_xobjects()))
            self.assertIn('checked wings', new[18].get_text())
            self.assertIn('bill hidden', new[20].get_text())
            self.assertIn('Not enough clues', new[20].get_text())
            for page in new:
                for font in page.get_fonts(full=True):
                    self.assertTrue(new.extract_font(font[0])[3])
        with fitz.open(OUT / 'woodpeckers-side-by-side-ACTUAL-SIZE.pdf') as doc:
            self.assertEqual(len(doc), 1)
            self.assertEqual(tuple(doc[0].rect), (0, 0, 1224, 792))
            self.assertIn('Downy Woodpecker', doc[0].get_text())
            self.assertIn('Hairy Woodpecker', doc[0].get_text())
        with fitz.open(OUT / 'woodpeckers-source-vs-vector-ACTUAL-SIZE.pdf') as doc:
            self.assertEqual(len(doc), 4)
            self.assertTrue(all(tuple(p.rect) == (0, 0, 612, 792) for p in doc))

    def test_issue_register_retains_other_findings(self):
        def rows(path):
            with path.open(newline='') as f:
                return {r['species_id']: r for r in csv.DictReader(f)}
        old = rows(OLD / 'ARTWORK_ISSUE_REGISTER.csv')
        new = rows(OUT / 'ARTWORK_ISSUE_REGISTER.csv')
        self.assertEqual(old.keys(), new.keys())
        for key in old:
            if key not in ('B09', 'B10'):
                self.assertEqual(old[key], new[key])
            else:
                self.assertEqual(new[key]['classification'], 'NEEDS HUMAN OR PRINT REVIEW')
                self.assertEqual(new[key]['expert_approval'], 'PENDING')
                self.assertEqual(new[key]['physical_print_approval'], 'PENDING')


if __name__ == '__main__':
    unittest.main()
