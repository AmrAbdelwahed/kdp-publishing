"""Check selected cover, clean review candidate, evidence registers and local print packet."""
import csv
import hashlib
import json
import unittest
from pathlib import Path
import fitz
from build_preflight_9 import ART

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'books/book-001/preflight-9'
OLD=ROOT/'books/book-001/interior-8b'
COVER=ROOT/'books/book-001/cover-8h'


def csv_rows(p):
    with p.open(newline='',encoding='utf8') as f:return list(csv.DictReader(f))


def norm(text):return ' '.join(text.split())


class MilestoneNineTest(unittest.TestCase):
    def test_selected_cover_geometry_and_fonts(self):
        manifest=json.loads((OUT/'COVER_SELECTION.json').read_text())
        p=OUT/manifest['candidate_wrap'];source=COVER/'A-full-wrap-REVIEW.pdf'
        self.assertEqual(hashlib.sha256(p.read_bytes()).hexdigest(),hashlib.sha256(source.read_bytes()).hexdigest())
        self.assertEqual(manifest['candidate_wrap_sha256'],manifest['source_wrap_sha256'])
        self.assertFalse(manifest['human_scientific_approval']);self.assertFalse(manifest['human_print_approval'])
        self.assertFalse(manifest['publication_approval'])
        for key in ('source_scene','selected_scene','template'):
            self.assertEqual(hashlib.sha256((ROOT/manifest[key]).read_bytes()).hexdigest(),manifest[key+'_sha256'])
        with fitz.open(p) as doc:
            page=doc[0];self.assertEqual(len(doc),1);self.assertAlmostEqual(page.rect.width,(.125+8.5+64*.002252+8.5+.125)*72,places=2)
            self.assertEqual(page.rect.height,810);im=page.get_image_info(xrefs=True)
            self.assertEqual(len(im),1);self.assertEqual((im[0]['width'],im[0]['height']),(4408,3612))
            self.assertAlmostEqual(im[0]['bbox'][2]-im[0]['bbox'][0],612,places=2)
            self.assertAlmostEqual(im[0]['bbox'][3]-im[0]['bbox'][1],501.1745,places=2)
            bar=fitz.Rect(459,696.6,603,783);back=fitz.Rect(18,18,612,792);front=fitz.Rect(640.3772,18,1234.3772,792)
            self.assertFalse(bar.intersects(fitz.Rect(im[0]['bbox'])))
            for form in page.get_xobjects():
                if form[2]==0:
                    r=fitz.Rect(form[3]);self.assertFalse(bar.intersects(fitz.Rect(r.x0,810-r.y1,r.x1,810-r.y0)))
            text=norm(page.get_text())
            for phrase in ('Backyard Bird Detectives','Color, Spot & Explore','A Coloring & Activity Book for Kids Ages 6–9'):
                self.assertIn(phrase,text)
            for phrase in ('Black Solid Line','Blue Dashed Line','REMOVE THIS TEMPLATE','Barcode Location & Size'):
                self.assertNotIn(phrase,text)
            for block in page.get_text('dict')['blocks']:
                for line in block.get('lines',[]):
                    for s in line['spans']:
                        if s['text'].strip():
                            rect=fitz.Rect(s['bbox']);self.assertTrue(back.contains(rect) or front.contains(rect),s['text']);self.assertFalse(bar.intersects(rect))
            for f in page.get_fonts(full=True):self.assertNotIn('Helvetica',f[3]);self.assertTrue(doc.extract_font(f[0])[3])
        with fitz.open(OUT/'selected-cover-front-actual-size.pdf') as new,fitz.open(COVER/'A-front-back-actual-size-REVIEW.pdf') as old:
            self.assertEqual(tuple(new[0].rect),(0,0,612,792));self.assertEqual(new[0].get_pixmap(matrix=fitz.Matrix(.5,.5)).samples,old[0].get_pixmap(matrix=fitz.Matrix(.5,.5)).samples)

    def test_clean_interior_and_registers(self):
        activities=json.loads((OLD/'ACTIVITIES.json').read_text());claims=csv_rows(OUT/'FACT_AND_ANSWER_AUDIT.csv');issues=csv_rows(OUT/'ARTWORK_ISSUE_REGISTER.csv')
        self.assertEqual((len(activities),len(claims),len(issues)),(30,30,9))
        self.assertEqual(sum(x['classification']=='CONFIRMED MATERIAL DEFECT' for x in issues),2)
        self.assertEqual({x['species_id'] for x in issues},{'B02','B03','B09','B10','B15','B22','B27','B29','B30'})
        self.assertEqual({x['species_id'] for x in issues if x['classification']=='CONFIRMED MATERIAL DEFECT'},{'B09','B10'})
        self.assertIn('light ring',next(x['current_evidence_and_limits'] for x in issues if x['species_id']=='B27'))
        self.assertTrue(all(x['expert_approval']=='PENDING' and x['physical_print_approval']=='PENDING' for x in issues))
        self.assertTrue(all(x['primary_excerpt_found']=='YES' and x['additional_excerpts_found']=='YES' and x['human_approval']=='PENDING' for x in claims))
        self.assertEqual(sum(int(x['additional_excerpt_count']) for x in claims),25)
        self.assertEqual(len(csv_rows(OLD/'SCIENTIFIC_VERIFICATION.csv')),150)
        with fitz.open(OLD/'64-page-interior-8b-REVIEW.pdf') as old,fitz.open(OUT/'interior-candidate-REVIEW.pdf') as new:
            self.assertEqual(len(new),64);self.assertEqual(new.xref_get_key(new.pdf_catalog(),'PageLayout')[1],'/TwoPageRight')
            self.assertEqual(len(new[63].get_links()),0);self.assertEqual(len(old[63].get_links()),30)
            self.assertEqual({x.get('uri','') for x in old[63].get_links()},{x['source_url'] for x in claims})
            self.assertIn('allaboutbirds.org/guide/',new[63].get_text())
            self.assertIn('Find each bird by name; check local guides for region and season.',new[63].get_text())
            self.assertNotIn('digital species names',new[63].get_text())
            for i,(a,b) in enumerate(zip(old,new)):
                self.assertEqual(tuple(b.rect),(0,0,612,792));self.assertNotIn('REVIEW DRAFT',b.get_text())
                self.assertEqual(b.get_links(),[]);self.assertEqual(list(b.annots() or []),[])
                self.assertEqual(b.get_images(),[])
                for block in b.get_text('dict')['blocks']:
                    for line in block.get('lines',[]):
                        for span in line['spans']:
                            if span['text'].strip():
                                x0,y0,x1,y1=span['bbox'];self.assertGreaterEqual(min(x0,y0,612-x1,792-y1),35)
                                self.assertGreaterEqual(span['size'],8.99)
                foot=[s['text'] for x in b.get_text('dict')['blocks'] for l in x.get('lines',[]) for s in l['spans'] if s['bbox'][1]>735 and s['text'].strip()]
                self.assertEqual(foot,[str(i+1)])
                # Only the footer and the documented source-page edits may differ from 8B.
                regions=[fitz.Rect(0,0,612,735)] if i!=63 else [fitz.Rect(0,0,612,115),fitz.Rect(0,148,612,675),fitz.Rect(0,692,612,735)]
                regions.append(fitz.Rect(0,755,612,792))
                for rect in regions:
                    self.assertEqual(a.get_pixmap(clip=rect,alpha=False).samples,b.get_pixmap(clip=rect,alpha=False).samples,f'unexpected visible change on page {i+1}')
                for f in b.get_fonts(full=True):self.assertTrue(new.extract_font(f[0])[3],f'font not embedded on page {i+1}')
            answers=norm(new[62].get_text())
            for a,claim in zip(activities,claims):
                pg=new[int(a['page'])-1];actual=norm(pg.get_text())
                self.assertEqual(a['species_id'],claim['species_id']);self.assertIn(norm(a['fact']),actual);self.assertIn(norm(a['instruction']),actual)
                self.assertIn(norm(f"{a['page']}. {a['answer']}"),answers)
        self.assertEqual(len(json.loads((OUT/'SOURCE_RECHECK.json').read_text())),36)

    def test_packet_spreads_are_actual_candidate_pages(self):
        with fitz.open(OUT/'interior-candidate-REVIEW.pdf') as candidate,fitz.open(OUT/'interior-print-packet-100-percent.pdf') as packet:
            self.assertEqual(len(packet),24);self.assertEqual(packet.xref_get_key(packet.pdf_catalog(),'PageLayout')[1],'/TwoPageRight')
            sequence=[n for art in ART for n in (art,art+1)]+[62,63,64];self.assertEqual(len(sequence),23)
            for i,n in enumerate(sequence,start=1):
                self.assertEqual(tuple(packet[i].rect),(0,0,612,792))
                self.assertEqual(packet[i].get_pixmap(matrix=fitz.Matrix(.3,.3),alpha=False).samples,candidate[n-1].get_pixmap(matrix=fitz.Matrix(.3,.3),alpha=False).samples)
            for i,art in enumerate(ART):self.assertEqual(art%2,0);self.assertEqual((i*2+2)%2,0)
        with fitz.open(OUT/'physical-review-checklist.pdf') as doc:self.assertEqual(len(doc),1)

if __name__=='__main__':unittest.main()
