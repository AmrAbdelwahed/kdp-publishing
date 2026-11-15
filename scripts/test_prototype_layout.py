"""Integration checks for facing-spread proof. Run after building it."""
import csv
import unittest
from pathlib import Path
import fitz

ROOT = Path(__file__).resolve().parents[1]


class PrototypeLayoutTests(unittest.TestCase):
    def test_pdf_spreads_and_text_bounds(self):
        path = ROOT / 'books/book-001/prototype/three-bird-prototype.pdf'
        expected = [(2, 'Northern Cardinal'), (3, 'Northern Cardinal'),
                    (8, 'Black-capped Chickadee'), (9, 'Black-capped Chickadee'),
                    (6, 'American Robin'), (7, 'American Robin')]
        with fitz.open(path) as doc:
            self.assertEqual(len(doc), len(expected))
            for page, (book_page, title) in zip(doc, expected):
                self.assertAlmostEqual(page.rect.width, 612)
                self.assertAlmostEqual(page.rect.height, 792)
                text = page.get_text()
                self.assertIn(title, text)
                self.assertIn(f'intended page {book_page}', text)
                self.assertIn('FACTS AND ART AWAIT REVIEW', text)
                left, right = (45, 36) if book_page % 2 else (36, 45)
                for block in page.get_text('blocks'):
                    x0, y0, x1, y1 = block[:4]
                    self.assertGreaterEqual(x0, left - 1)
                    self.assertLessEqual(x1, 612 - right + 1)
                    self.assertGreaterEqual(y0, 35)
                    self.assertLessEqual(y1, 792 - 35)
            for i in (0, 2, 4):
                self.assertIn('COLOUR', doc[i].get_text())
                self.assertIn('OBSERVE', doc[i + 1].get_text())

    def test_complete_facing_page_plan(self):
        with (ROOT / 'books/book-001/blueprint/PAGE_PLAN.csv').open(newline='') as f:
            rows = list(csv.DictReader(f))
        self.assertEqual([int(r['page']) for r in rows], list(range(1, 65)))
        self.assertEqual(rows[0]['page_type'], 'front_matter')
        self.assertEqual([r['page_type'] for r in rows[61:]], ['back_matter'] * 3)
        ids = set()
        for i in range(1, 61, 2):
            left, right = rows[i:i+2]
            self.assertEqual((left['page_type'], right['page_type']), ('colouring', 'activity'))
            self.assertEqual(left['species_id'], right['species_id'])
            self.assertEqual(int(left['page']) % 2, 0)
            self.assertEqual(int(right['page']), int(left['page']) + 1)
            ids.add(left['species_id'])
        self.assertEqual(len(ids), 30)


if __name__ == '__main__': unittest.main()
