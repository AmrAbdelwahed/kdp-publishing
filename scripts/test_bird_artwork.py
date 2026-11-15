"""Tests for identity, resolution and human-approval gates."""
import hashlib
import json
import tempfile
import unittest
from pathlib import Path
from PIL import Image, ImageDraw
import check_bird_artwork as quality


class ArtworkChecks(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.old_root, self.old_art = quality.ROOT, quality.ART
        self.addCleanup(self.restore)
        quality.ROOT = Path(self.tmp.name)
        quality.ART = quality.ROOT / 'artwork'
        (quality.ART/'approved').mkdir(parents=True)
        img=Image.new('RGB',(1900,2000),'white')
        ImageDraw.Draw(img).rectangle((200,200,1700,1800),outline='black',width=8)
        self.file=quality.ART/'approved/bird.png'
        img.save(self.file)
        self.entry=dict(species='cardinal',path='artwork/approved/bird.png',sha256=hashlib.sha256(self.file.read_bytes()).hexdigest(),provenance='test fixture',human_approved=False,reviewer='',reviewed_at='',approval_scope='')

    def restore(self):
        quality.ROOT, quality.ART = self.old_root, self.old_art

    def test_human_and_line_review_are_required(self):
        result=quality.report([self.entry])[0]
        self.assertTrue(result['resolution_pass'])
        self.assertFalse(result['ready_for_placement'])
        self.entry.update(human_approved=True,reviewer='Reviewer',reviewed_at='2026-11-14',approval_scope='anatomy and field marks',line_and_placement_reviewed=True)
        self.assertTrue(quality.report([self.entry])[0]['ready_for_placement'])

    def test_hash_mismatch_rejected(self):
        self.entry['sha256']='bad'
        with self.assertRaisesRegex(ValueError,'identity/provenance'):
            quality.report([self.entry])

    def test_duplicates_flagged_and_fail(self):
        second=dict(self.entry,species='robin')
        results=quality.report([self.entry,second])
        self.assertEqual(results[0]['possible_duplicates'],['robin'])
        self.assertFalse(results[0]['ready_for_placement'])

    def test_current_candidate_resolution_fails(self):
        quality.ROOT, quality.ART = self.old_root, self.old_art
        entries=json.loads((quality.ART/'manifest.json').read_text())
        self.assertTrue(all(not a['resolution_pass'] for a in quality.report(entries)))


if __name__ == '__main__': unittest.main()
