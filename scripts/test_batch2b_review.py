"""Check Milestone 2B reference identity, visual decisions and review proof."""
import hashlib
import json
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path
import fitz

ROOT=Path(__file__).resolve().parents[1]
BATCH=ROOT/'books/book-001/artwork/batch-01'
EXPECTED={'B04':'ab346d674dd7926b4a91b0a054c3d2f5755d264d624cf0159bd125fefd1c8d8c',
          'B13':'ecf1898278e702aa56943655c2e55891b4491e31a3697867647ee81b3196224d'}


class BatchTwoBTests(unittest.TestCase):
    def test_preserved_accepted_designs_and_revision_sources(self):
        data=json.loads((BATCH/'manifest.json').read_text())
        entries={e['species_id']:e for e in data['entries']}
        prompts={e['species_id']:e for e in json.loads((BATCH/'revision-prompts-v2.json').read_text())}
        self.assertEqual(set(entries),{'B02','B03','B04','B07','B13'})
        self.assertEqual(set(prompts),{'B02','B03','B07'})
        for sid,digest in EXPECTED.items():
            e=entries[sid]
            self.assertEqual(e['original_sha256'],digest)
            self.assertEqual(hashlib.sha256((ROOT/e['original_path']).read_bytes()).hexdigest(),digest)
            self.assertEqual(e['visual_decision'],'PROVISIONALLY_ACCEPTED_BY_USER')
            self.assertFalse(e['human_approval'])
            self.assertFalse(e['print_approval'])
        for sid in prompts:
            e=entries[sid];q=json.loads((ROOT/e['quality_path']).read_text())
            self.assertEqual(q['revision'],'v2')
            self.assertEqual(q['source_sha256'],hashlib.sha256((ROOT/e['original_path']).read_bytes()).hexdigest())
            self.assertEqual(len(e['prior_revisions']),1)
            old=e['prior_revisions'][0]
            self.assertEqual(hashlib.sha256((ROOT/old['original_path']).read_bytes()).hexdigest(),old['original_sha256'])
            self.assertFalse(e['human_approval']);self.assertFalse(e['print_approval'])
            self.assertEqual(q['input_reference_hashes'],prompts[sid]['reference_sha256'])
            for path,digest in q['input_reference_hashes'].items():
                self.assertEqual(hashlib.sha256((ROOT/path).read_bytes()).hexdigest(),digest)
            svg=ROOT/e['svg_path'];self.assertEqual(hashlib.sha256(svg.read_bytes()).hexdigest(),e['svg_sha256'])
            tags=[el.tag.rsplit('}',1)[-1] for el in ET.parse(svg).getroot().iter()]
            self.assertIn('path',tags);self.assertNotIn('image',tags)
            with fitz.open(ROOT/e['vector_art_pdf']) as d:self.assertFalse(d[0].get_images())

    def test_proof_facing_pairs_and_labels(self):
        path=BATCH/'review-2b/six-bird-provisional-proof.pdf'
        expected=[2,3,4,5,6,7,8,9,14,15,26,27]
        with fitz.open(path) as d:
            self.assertEqual(len(d),12)
            self.assertEqual(d.xref_get_key(d.pdf_catalog(),'PageLayout')[1],'/TwoPageLeft')
            for i,(page,num) in enumerate(zip(d,expected)):
                self.assertEqual((page.rect.width,page.rect.height),(612,792))
                text=page.get_text();self.assertIn(f'intended page {num}',text)
                self.assertIn('FACTS AND ART AWAIT REVIEW',text)
                if i%2==0:
                    self.assertFalse(page.get_images())
                    self.assertTrue('UNAPPROVED' in text or 'PRINT / FACT CHECK PENDING' in text)
                left,right=(45,36) if num%2 else (36,45)
                for block in page.get_text('blocks'):
                    x0,y0,x1,y1=block[:4]
                    self.assertGreaterEqual(x0,left-1);self.assertLessEqual(x1,612-right+1)
                    self.assertGreaterEqual(y0,35);self.assertLessEqual(y1,757)
            self.assertIn('VISUALLY ACCEPTED',d[6].get_text())
            self.assertIn('VISUALLY ACCEPTED',d[10].get_text())

    def test_revisions_do_not_overwrite(self):
        from process_bird_batch import process
        for sid in ('B02','B03','B07'):
            source=BATCH/'originals'/f'{sid}-v2.png'
            before=hashlib.sha256(source.read_bytes()).hexdigest()
            with self.assertRaises(FileExistsError):process(sid,source,'v2')
            self.assertEqual(hashlib.sha256(source.read_bytes()).hexdigest(),before)


if __name__=='__main__':unittest.main()
