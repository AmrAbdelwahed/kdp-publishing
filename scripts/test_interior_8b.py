"""Checks for semantic answer order, layout, preserved artwork and duplex print packet."""
import csv
import hashlib
import json
import shutil
import tempfile
import unittest
from collections import Counter
from pathlib import Path

import fitz
from build_interior_8a import build as build_8a
from build_print_packet_8b import SPREADS

ROOT=Path(__file__).resolve().parents[1]
PREV=ROOT/'books/book-001/interior-8a'
OUT=ROOT/'books/book-001/interior-8b'


def read_csv(path):
    with path.open(newline='',encoding='utf8') as f:return list(csv.DictReader(f))


def norm(text):return ' '.join(text.split())


class Interior8BTest(unittest.TestCase):
    def test_answer_meaning_science_and_layout(self):
        old=json.loads((PREV/'ACTIVITIES.json').read_text(encoding='utf8'))
        now=json.loads((OUT/'ACTIVITIES.json').read_text(encoding='utf8'))
        entries=json.loads((OUT/'WORKING_ARTWORK_MANIFEST.json').read_text(encoding='utf8'))['entries']
        claims=read_csv(OUT/'CLAIM_AUDIT.csv');keys=read_csv(OUT/'ANSWER_KEY_COVERAGE.csv')
        copy=read_csv(OUT/'FINAL_PROPOSED_COPY.csv')
        reviews=read_csv(OUT/'ACTIVITY_REVIEW.csv');log=read_csv(OUT/'SCIENTIFIC_VERIFICATION.csv')
        self.assertEqual(tuple(map(len,(old,now,entries,claims,keys,copy,reviews,log))),(30,30,30,30,30,30,30,150))
        self.assertEqual(len({x['check_id'] for x in log}),150)
        self.assertTrue(all(x['recheck_status'].startswith('PASS') for x in claims))
        self.assertTrue(all('PENDING' in x['human_testing_status'] for x in reviews))
        for fmt,counts in [('challenge',{'A':1,'B':2,'C':2}),('compare',{'A':2,'B':3}),('journal',{'A':1,'B':2,'C':2})]:
            self.assertEqual(Counter(x['answer'] for x in now if x['format']==fmt),counts)
        self.assertEqual({x['format'] for x in now},{'challenge','compare','colour','journal','draw','lab'})
        hashes=[]
        for previous,a,e,claim,key,record in zip(old,now,entries,claims,keys,copy):
            self.assertEqual(previous['species_id'],a['species_id']);self.assertEqual(a['species_id'],e['species_id'])
            self.assertEqual(a['fact'],claim['exact_customer_facing_claim']);self.assertEqual(a['answer'],key['answer_on_page_63'])
            self.assertEqual(a['species_id'],record['species_id'])
            for field in ('fact','instruction','answer'):
                self.assertEqual(a[field],record[field])
            self.assertEqual(' | '.join(a['options']),record['options'])
            self.assertEqual(a['instruction'],key['instruction'])
            displayed=a['answer']
            if a['format'] in ('challenge','journal'):
                displayed+=' / '+a['options'][ord(a['answer'])-65]
            elif a['format']=='compare':
                displayed+=' / '+a['options'][ord(a['answer'])-65][3:]
            self.assertEqual(displayed,claim['displayed_answer'])
            self.assertEqual(a['human_approval'] if 'human_approval' in a else False,False)
            self.assertFalse(e['human_approval']);self.assertFalse(e['print_approval'])
            if a['species_id']!='B26':self.assertEqual(previous['fact'],a['fact'])
            if a['species_id']!='B12':self.assertEqual(previous['instruction'],a['instruction'])
            if a['format'] in ('challenge','journal'):
                self.assertEqual(previous['options'][ord(previous['answer'])-65],a['options'][ord(a['answer'])-65])
            elif a['format']=='compare' and a['species_id']!='B14':
                self.assertEqual(previous['options'][ord(previous['answer'])-65][3:],a['options'][ord(a['answer'])-65][3:])
                self.assertEqual(sorted(a.get('compare_order',[0,1])),[0,1])
            elif a['format']=='lab':
                n=len(a['options']);expected=', '.join(f'{i+1}–{chr(65+(i+1)%n)}' for i in range(n))
                self.assertEqual(a['answer'],expected)
            path=ROOT/e['vector_art_pdf'];digest=hashlib.sha256(path.read_bytes()).hexdigest()
            self.assertEqual(digest,e['selected_vector_sha256']);hashes.append(digest)
        self.assertEqual(len(set(hashes)),30)
        with fitz.open(PREV/'64-page-interior-8a-REVIEW.pdf') as previous,fitz.open(OUT/'64-page-interior-8b-REVIEW.pdf') as doc:
            self.assertEqual(len(doc),64);self.assertEqual(doc.xref_get_key(doc.pdf_catalog(),'PageLayout')[1],'/TwoPageRight')
            self.assertIn('BIRD WORDS:',doc[0].get_text());self.assertEqual(len(doc[63].get_links()),30)
            answer_text=norm(doc[62].get_text());fonts=set()
            for i,page in enumerate(doc):
                fonts.update(v[0] for v in page.get_fonts(full=True))
                self.assertEqual((page.rect.width,page.rect.height),(612,792));self.assertFalse(page.get_images())
                self.assertIn(f'REVIEW DRAFT • {i+1}',norm(page.get_text()))
                spans=[s for b in page.get_text('dict')['blocks'] for l in b.get('lines',[]) for s in l['spans'] if s['text'].strip()]
                for j,span in enumerate(spans):
                    x0,y0,x1,y1=span['bbox'];self.assertGreaterEqual(x0,35);self.assertGreaterEqual(y0,35)
                    self.assertLessEqual(x1,577);self.assertLessEqual(y1,757);self.assertGreaterEqual(span['size'],8.99)
                    for other in spans[j+1:]:
                        overlap=fitz.Rect(span['bbox']) & fitz.Rect(other['bbox'])
                        self.assertTrue(overlap.is_empty or overlap.get_area()<2,f'Text overlap on page {i+1}')
            self.assertTrue(fonts)
            for ref in fonts:self.assertGreater(len(doc.extract_font(ref)[3]),0)
            for i,a in enumerate(now):
                art=doc[1+2*i];activity=doc[2+2*i];text=norm(activity.get_text())
                self.assertIn(a['species'],art.get_text());self.assertIn(a['species'],text)
                self.assertIn(norm(a['fact']),text);self.assertIn(norm(a['instruction']),text)
                self.assertIn(norm(f"{a['page']}. {a['answer']}"),answer_text)
                self.assertEqual(previous[1+2*i].get_pixmap(matrix=fitz.Matrix(.3,.3),alpha=False).samples,
                                 art.get_pixmap(matrix=fitz.Matrix(.3,.3),alpha=False).samples)
            # After reversing A/B cards, the diagram content must move with its label.
            blue=doc[4];self.assertGreater(blue.search_for('blue / black / white')[0].x0,306)
            self.assertLess(blue.search_for('white / light gray')[0].x0,306)
            nut=doc[16];above=[r for r in nut.search_for('above') if r.y0>400]
            through=[r for r in nut.search_for('through') if r.y0>400]
            self.assertEqual(len(above),1);self.assertGreater(above[0].x0,306)
            self.assertEqual(len(through),1);self.assertLess(through[0].x0,306)
            pigeon=norm(doc[28].get_text());self.assertIn('A SAMPLE A',pigeon);self.assertIn('B SAMPLE B',pigeon)

    def test_local_print_packet_and_actual_size_art(self):
        with fitz.open(OUT/'64-page-interior-8b-REVIEW.pdf') as source,fitz.open(OUT/'actual-size-print-packet.pdf') as packet:
            self.assertEqual(len(packet),20);self.assertEqual(packet.xref_get_key(packet.pdf_catalog(),'PageLayout')[1],'/TwoPageRight')
            self.assertIn('100%',packet[0].get_text())
            sequence=[p for pair in SPREADS for p in pair]+[62,63,64]
            self.assertEqual(len(sequence),19)
            for i,page_number in enumerate(sequence,start=1):
                self.assertEqual((packet[i].rect.width,packet[i].rect.height),(612,792))
                self.assertIn(f'REVIEW DRAFT • {page_number}',norm(packet[i].get_text()))
                self.assertEqual(packet[i].get_pixmap(matrix=fitz.Matrix(.25,.25),alpha=False).samples,
                                 source[page_number-1].get_pixmap(matrix=fitz.Matrix(.25,.25),alpha=False).samples)
            for i,(left,right) in enumerate(SPREADS):
                self.assertEqual(left%2,0);self.assertEqual(right,left+1)
                self.assertEqual((2+2*i)%2,0,'Art must fall on packet verso/left')
        with fitz.open(OUT/'eight-bird-actual-size-original-vs-vector.pdf') as proof,fitz.open(OUT/'64-page-interior-8b-REVIEW.pdf') as interior:
            self.assertEqual(len(proof),16)
            for i,page_number in enumerate([4,6,18,20,30,44,58,60]):
                original=proof[2*i];vector=proof[2*i+1]
                self.assertEqual((original.rect.width,original.rect.height),(612,792))
                images=original.get_images(full=True);self.assertEqual(len(images),1)
                image_rect=original.get_image_rects(images[0][0])[0]
                bounds=fitz.Rect(vector.get_xobjects()[0][3]);converted=fitz.Rect(bounds.x0,792-bounds.y1,bounds.x1,792-bounds.y0)
                for a,b in zip(image_rect,converted):self.assertAlmostEqual(a,b,delta=.02)
                self.assertEqual(vector.get_xobjects()[0][3],interior[page_number-1].get_xobjects()[0][3])
        for name in ['PRINT_REVIEW_SHEET.pdf','CHILD_CAREGIVER_FEEDBACK.pdf','eight-bird-artwork-review.pdf']:
            with fitz.open(OUT/name) as doc:
                for page in doc:self.assertEqual((page.rect.width,page.rect.height),(612,792))

    def test_prior_builder_defaults_remain_compatible(self):
        with tempfile.TemporaryDirectory(prefix='bird-8a-regression-') as tmp:
            out=Path(tmp);shutil.copyfile(PREV/'ACTIVITIES.json',out/'ACTIVITIES.json')
            build_8a(out,'rebuilt.pdf')
            with fitz.open(PREV/'64-page-interior-8a-REVIEW.pdf') as expected,fitz.open(out/'rebuilt.pdf') as rebuilt:
                self.assertEqual(len(expected),len(rebuilt))
                for i in range(64):
                    self.assertEqual(expected[i].get_pixmap(matrix=fitz.Matrix(.2,.2),alpha=False).samples,
                                     rebuilt[i].get_pixmap(matrix=fitz.Matrix(.2,.2),alpha=False).samples,f'Prior design changed on page {i+1}')

if __name__=='__main__':unittest.main()
