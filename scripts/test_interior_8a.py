"""Meaningful checks for the redesigned review; visual and expert approval remain separate."""
from pathlib import Path
import csv
import hashlib
import json
import re
import unittest

import fitz

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'books/book-001/interior-8a'
BASE=ROOT/'books/book-001/interior-review/64-page-interior-REVIEW.pdf'


def normal(text):
    return ' '.join(text.split())


class Interior8ATest(unittest.TestCase):
    def test_review_invariants(self):
        activities=json.loads((OUT/'ACTIVITIES.json').read_text(encoding='utf8'))
        entries=json.loads((OUT/'WORKING_ARTWORK_MANIFEST.json').read_text(encoding='utf8'))['entries']
        with (OUT/'SCIENTIFIC_VERIFICATION.csv').open(newline='',encoding='utf8') as f: log=list(csv.DictReader(f))
        with (OUT/'CLAIM_AUDIT.csv').open(newline='',encoding='utf8') as f: audit=list(csv.DictReader(f))
        with (OUT/'ANSWER_KEY_COVERAGE.csv').open(newline='',encoding='utf8') as f: keys=list(csv.DictReader(f))
        self.assertEqual((len(activities),len(entries),len(log),len(audit),len(keys)),(30,30,150,30,30))
        expected_ids=[f'B{i:02d}' for i in range(1,31)]
        self.assertEqual([a['species_id'] for a in activities],expected_ids)
        self.assertEqual([x['species_id'] for x in entries],expected_ids)
        self.assertEqual([x['species_id'] for x in audit],expected_ids)
        self.assertEqual(len({a['instruction'] for a in activities}),30)
        self.assertEqual(len({a['observation'] for a in activities}),30)
        formats={'challenge','compare','colour','journal','draw','lab'}
        self.assertEqual({a['format'] for a in activities},formats)
        self.assertTrue(all(sum(a['format']==fmt for a in activities)==5 for fmt in formats))
        self.assertEqual(len({row['check_id'] for row in log}),150)
        self.assertTrue(any('PENDING' in row['status'] for row in log))
        hashes=[]
        for a,e,claim,key in zip(activities,entries,audit,keys):
            self.assertEqual(claim['exact_customer_facing_claim'],a['fact'])
            self.assertEqual(key['answer_on_page_63'],a['answer'])
            self.assertTrue(a['sources'] and all(s['url'] and s['retrieved_at_utc'] for s in a['sources']))
            self.assertEqual(e['human_approval'],False);self.assertEqual(e['print_approval'],False)
            svg=(ROOT/e['svg_path']).read_text(encoding='utf8')
            self.assertIn('<path',svg);self.assertIsNone(re.search(r'<(?:\w+:)?image\b',svg))
            path=ROOT/e['vector_art_pdf'];digest=hashlib.sha256(path.read_bytes()).hexdigest()
            self.assertEqual(digest,e['selected_vector_sha256']);hashes.append(digest)
            if a['format'] in {'challenge','journal'}:
                self.assertIn(a['answer'],[chr(65+i) for i in range(len(a['options']))])
            elif a['format']=='compare':self.assertIn(a['answer'],('A','B'))
            elif a['format']=='lab':
                pairs=[p.split('=',1) for p in a['options']]
                expected=', '.join(f'{i+1}–{chr(65+(i+1)%len(pairs))}' for i in range(len(pairs)))
                self.assertEqual(a['answer'],expected)
        self.assertEqual(len(set(hashes)),30,'Duplicated selected vector artwork')
        with fitz.open(BASE) as old,fitz.open(OUT/'64-page-interior-8a-REVIEW.pdf') as doc:
            self.assertEqual(len(doc),64)
            self.assertEqual(doc.xref_get_key(doc.pdf_catalog(),'PageLayout')[1],'/TwoPageRight')
            answer_text=normal(doc[62].get_text())
            font_refs=set()
            for i,page in enumerate(doc):
                font_refs.update(f[0] for f in page.get_fonts(full=True))
                self.assertEqual((page.rect.width,page.rect.height),(612,792))
                self.assertFalse(page.get_images())
                self.assertIn(f'REVIEW DRAFT • {i+1}',normal(page.get_text()))
                blocks=page.get_text('blocks')
                for j,block in enumerate(blocks):
                    self.assertGreaterEqual(block[0],35);self.assertGreaterEqual(block[1],35)
                    self.assertLessEqual(block[2],577);self.assertLessEqual(block[3],757)
                    for other in blocks[j+1:]:
                        intersection=fitz.Rect(block[:4]) & fitz.Rect(other[:4])
                        self.assertTrue(intersection.is_empty or intersection.get_area()<2,f'Text collision on page {i+1}')
                spans=[span for block in page.get_text('dict')['blocks']
                       for line in block.get('lines',[]) for span in line['spans'] if span['text'].strip()]
                for j,span in enumerate(spans):
                    self.assertGreaterEqual(span['size'],8.99)
                    for other in spans[j+1:]:
                        overlap=fitz.Rect(span['bbox']) & fitz.Rect(other['bbox'])
                        self.assertTrue(overlap.is_empty or overlap.get_area()<2,f'Text span collision on page {i+1}')
            self.assertEqual(len(doc[63].get_links()),30)
            self.assertTrue(font_refs)
            for ref in font_refs:self.assertGreater(len(doc.extract_font(ref)[3]),0, f'Font {ref} is not embedded')
            for i,a in enumerate(activities):
                art_page=doc[1+2*i];activity_page=doc[2+2*i]
                self.assertIn(a['species'],art_page.get_text());self.assertIn(a['species'],activity_page.get_text())
                text=normal(activity_page.get_text())
                self.assertIn(normal(a['fact']),text);self.assertIn(normal(a['instruction']),text)
                if a.get('case_note'):self.assertIn(normal(a['case_note']),text)
                self.assertIn(normal(f"{a['page']}. {a['answer']}"),answer_text)
                # Verify retained art pages render identically to the preceding milestone.
                transform=fitz.Matrix(.3,.3)
                self.assertEqual(old[1+2*i].get_pixmap(matrix=transform,alpha=False).samples,
                                 art_page.get_pixmap(matrix=transform,alpha=False).samples)

if __name__=='__main__':unittest.main()
