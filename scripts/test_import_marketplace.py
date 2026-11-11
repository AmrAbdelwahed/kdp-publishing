"""Run: python -m unittest discover -s scripts -p 'test_import_marketplace.py'."""
import csv
import json
import tempfile
import unittest
from pathlib import Path

from import_marketplace import FIELDS, ingest, history


class ImportTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        (self.root / 'capture.txt').write_text('Synthetic test evidence, not a real listing')
        self.row = dict.fromkeys(FIELDS, '')
        self.row.update(capture_id='test1', marketplace='Amazon.com', product_title='Synthetic fixture',
                        asin='0000000001', product_url='https://www.amazon.com/dp/0000000001',
                        classification='uncertain', classification_reason='Test only', format='paperback',
                        source_url='https://www.amazon.com/dp/0000000001', collected_at='2026-01-01T12:00:00Z',
                        evidence_refs='capture.txt', confidence='low', missing_values='All optional fields absent')

    def source(self, rows):
        p = self.root / 'input.csv'
        with p.open('w', newline='') as stream:
            writer = csv.DictWriter(stream, fieldnames=FIELDS)
            writer.writeheader()
            writer.writerows(rows)
        return p

    def test_append_repeat_and_conflict(self):
        p = self.source([self.row])
        first = ingest(p, self.root)
        base = self.root / 'research/marketplace/batches'
        saved = {str(p): p.read_bytes() for p in base.rglob('*') if p.is_file()}
        self.assertEqual(ingest(p, self.root)['status'], 'already_imported')
        corrected = dict(self.row, capture_id='test2', page_count='64')
        report = ingest(self.source([corrected]), self.root)
        self.assertEqual(len(history(base)), 2)
        self.assertEqual(report['flags'][0]['type'], 'repeat_product')
        changed = dict(corrected, capture_id='test3', page_count='80')
        report = ingest(self.source([changed]), self.root)
        self.assertTrue(any(f['type'] == 'same_time_conflict' for f in report['flags']))
        for name, content in saved.items():
            self.assertEqual(Path(name).read_bytes(), content)
        self.assertEqual(json.loads((base / first['batch_id'] / 'observations.json').read_text())[0]['price'], '')

    def test_reject_bad_inputs_without_writes(self):
        for changes in [dict(asin='bad'), dict(currency='CAD'), dict(price='NaN'),
                        dict(collected_at='2026-01-01'), dict(bsr='0'), dict(bsr='20'),
                        dict(star_rating='6'), dict(evidence_refs='../secret'),
                        dict(product_url='https://www.amazon.com.evil.test/dp/0000000001'),
                        dict(format='hardcover'), dict(source_url='https://www.amazon.ca/dp/0000000001')]:
            with self.subTest(changes=changes), self.assertRaises(ValueError):
                ingest(self.source([dict(self.row, **changes)]), self.root)
        self.assertFalse((self.root / 'research/marketplace/batches').exists())

    def test_dry_run_and_empty_template(self):
        self.assertEqual(ingest(self.source([self.row]), self.root, True)['status'], 'dry_run')
        self.assertFalse((self.root / 'research/marketplace/batches').exists())
        with self.assertRaisesRegex(ValueError, 'No completed observations'):
            ingest(self.source([dict.fromkeys(FIELDS, '')]), self.root)

    def test_duplicate_ids_are_rejected(self):
        with self.assertRaisesRegex(ValueError, 'Duplicate capture_id'):
            ingest(self.source([self.row, self.row]), self.root)
        ingest(self.source([self.row]), self.root)
        with self.assertRaisesRegex(ValueError, 'already exists'):
            ingest(self.source([dict(self.row, notes='changed')]), self.root)


if __name__ == '__main__':
    unittest.main()
