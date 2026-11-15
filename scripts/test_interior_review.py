"""Structural checks for the 64-page review interior; not a print certification."""
import csv,json,re,unittest
from pathlib import Path
import fitz
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'books/book-001/interior-review'

class InteriorReviewTest(unittest.TestCase):
 def test_review_invariants(self):
  entries=json.loads((OUT/'WORKING_ARTWORK_MANIFEST.json').read_text())['entries']
  with (OUT/'REVISED_ACTIVITY_COPY.csv').open(newline='') as f: rows=list(csv.DictReader(f))
  with (OUT/'SCIENTIFIC_VERIFICATION.csv').open(newline='') as f: facts=list(csv.DictReader(f))
  self.assertEqual((len(entries),len(rows),len(facts)),(30,30,150))
  for e in entries:
   self.assertFalse(e['human_approval']);self.assertFalse(e['print_approval'])
   self.assertTrue((ROOT/e['vector_art_pdf']).is_file())
   svg=(ROOT/e['svg_path']).read_text();self.assertIn('<path',svg);self.assertIsNone(re.search(r'<(?:\w+:)?image\b',svg))
  with fitz.open(OUT/'64-page-interior-REVIEW.pdf') as doc:
   self.assertEqual(len(doc),64);self.assertEqual(doc.xref_get_key(doc.pdf_catalog(),'PageLayout')[1],'/TwoPageRight')
   for i,page in enumerate(doc):
    self.assertEqual((page.rect.width,page.rect.height),(612,792));self.assertFalse(page.get_images())
    self.assertIn(f'REVIEW DRAFT • {i+1}',page.get_text())
    blocks=page.get_text('blocks')
    for j,block in enumerate(blocks):
     self.assertGreaterEqual(block[0],35);self.assertGreaterEqual(block[1],35);self.assertLessEqual(block[2],577);self.assertLessEqual(block[3],757)
     for other in blocks[j+1:]:
      overlap=fitz.Rect(block[:4]) & fitz.Rect(other[:4]); self.assertTrue(overlap.is_empty or overlap.get_area()<2, f'Overlapping text on page {i+1}')
   for i,row in enumerate(rows):
    self.assertIn(row['species'],doc[1+2*i].get_text());self.assertIn(row['species'],doc[2+2*i].get_text())
    self.assertIn(row['reference_fact'],doc[2+2*i].get_text().replace('\n',' '))

if __name__=='__main__':unittest.main()
