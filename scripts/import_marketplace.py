"""Validate manual Amazon CSV captures and append immutable, content-addressed batches.
No network or third-party packages. See research/marketplace/CAPTURE_GUIDE.md.
"""
import argparse
import csv
import hashlib
import io
import json
import re
import tempfile
from datetime import datetime, timezone, date
from decimal import Decimal, InvalidOperation
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
FIELDS = '''capture_id marketplace product_title asin product_url classification classification_reason age_range format page_count price currency price_context bsr bsr_category star_rating rating_count publication_date publisher educational_features key_differentiation customer_feedback feedback_url feedback_date observed_weaknesses discovery search_query discovery_url source_url collected_at evidence_refs confidence missing_values notes'''.split()
REQUIRED = 'capture_id marketplace product_title asin product_url classification classification_reason format source_url collected_at evidence_refs confidence missing_values'.split()
DYNAMIC = {'price', 'price_context', 'bsr', 'bsr_category', 'star_rating', 'rating_count'}


def product_url(value, host, asin):
    u = urlsplit(value)
    if u.scheme != 'https' or u.hostname not in (host, 'www.' + host) or u.username or u.password or u.port:
        raise ValueError('Product URL must use HTTPS and the exact marketplace host')
    match = re.search(r'/(?:dp|gp/product)/([A-Z0-9]{10})(?:/|$)', u.path)
    if not match or match[1] != asin:
        raise ValueError('Product URL ASIN mismatch')


def parse_csv(data, root):
    reader = csv.DictReader(io.StringIO(data.decode('utf-8-sig'), newline=''))
    if reader.fieldnames != FIELDS:
        raise ValueError('Headers must match capture_template.csv exactly, including order')
    records = []
    ids = set()
    evidence = {}
    for line, raw in enumerate(reader, 2):
        if None in raw or None in raw.values():
            raise ValueError(f'Row {line}: malformed CSV')
        r = {k: v.strip() for k, v in raw.items()}
        # Unfilled template slots are not observations.
        if not any(v for k, v in r.items() if k not in ('capture_id', 'marketplace')):
            continue
        try:
            if any(not r[k] for k in REQUIRED):
                raise ValueError('Missing required identity, provenance or missing-values explanation')
            if r['capture_id'] in ids:
                raise ValueError('Duplicate capture_id in input')
            ids.add(r['capture_id'])
            if r['marketplace'] not in ('Amazon.com', 'Amazon.ca'):
                raise ValueError('marketplace must be Amazon.com or Amazon.ca')
            if not re.fullmatch('[A-Z0-9]{10}', r['asin']):
                raise ValueError('ASIN must be 10 uppercase letters/digits; preserve leading zeros')
            host = r['marketplace'].lower()
            product_url(r['product_url'], host, r['asin'])
            product_url(r['source_url'], host, r['asin'])
            if r['format'] != 'paperback':
                raise ValueError('Select and verify paperback; other formats do not qualify')
            if r['classification'] not in ('direct', 'adjacent', 'uncertain'):
                raise ValueError('Invalid classification')
            if r['confidence'] not in ('low', 'medium', 'high'):
                raise ValueError('Invalid confidence')
            if r['discovery'] not in ('', 'sponsored', 'organic', 'unknown', 'direct_link'):
                raise ValueError('Invalid discovery')
            observed = datetime.fromisoformat(r['collected_at'].replace('Z', '+00:00'))
            if observed.tzinfo is None or observed > datetime.now(timezone.utc):
                raise ValueError('collected_at needs a timezone and cannot be in the future')
            r['collected_at'] = observed.astimezone(timezone.utc).isoformat()
            for field, minimum in [('page_count', 1), ('bsr', 1), ('rating_count', 0)]:
                if r[field] and (not re.fullmatch(r'\d+', r[field]) or int(r[field]) < minimum):
                    raise ValueError(f'Invalid {field}; use unformatted integer or blank')
            for field in ('price', 'star_rating'):
                if r[field]:
                    n = Decimal(r[field])
                    if not n.is_finite() or n <= 0 or (field == 'star_rating' and not 1 <= n <= 5):
                        raise ValueError(f'Invalid {field}')
            if r['currency'] and r['currency'] != ('USD' if host == 'amazon.com' else 'CAD'):
                raise ValueError('Currency does not match marketplace')
            if r['price'] and (not r['currency'] or not r['price_context']):
                raise ValueError('Price needs currency and offer/condition context')
            if r['bsr'] and not r['bsr_category']:
                raise ValueError('BSR needs its category')
            for field in ('publication_date', 'feedback_date'):
                if r[field]:
                    date.fromisoformat(r[field])
            if r['customer_feedback'] and not (r['feedback_url'] and r['feedback_date']):
                raise ValueError('Feedback requires exact source URL and review date')
            for ref in r['evidence_refs'].split(';'):
                path = Path(ref)
                if path.is_absolute() or '..' in path.parts:
                    raise ValueError('Evidence paths must be relative inside the repository')
                path = (root / path).resolve()
                if not path.is_relative_to(root.resolve()) or not path.is_file():
                    raise ValueError(f'Evidence file missing or outside repository: {ref}')
                evidence[ref] = path.read_bytes()
            r['verification_status'] = 'pending_human_evidence_review'
            records.append(r)
        except (ValueError, InvalidOperation) as error:
            raise ValueError(f'Row {line}: {error}') from error
    if not records:
        raise ValueError('No completed observations; blank template is not evidence')
    return records, evidence


def history(base):
    return [row for path in sorted(base.glob('*/observations.json')) for row in json.loads(path.read_text())]


def flag_changes(old, new):
    flags = []
    for r in new:
        for previous in old:
            if r['marketplace'] == previous['marketplace'] and r['asin'] == previous['asin']:
                different = [k for k in FIELDS if r[k] and previous[k] and r[k] != previous[k]
                             and k not in ('capture_id', 'collected_at', 'evidence_refs', 'notes')]
                same_time = r['collected_at'] == previous['collected_at']
                flags.append({'capture_id': r['capture_id'], 'previous_capture_id': previous['capture_id'],
                              'type': 'same_time_conflict' if same_time and different else 'repeat_product',
                              'differing_fields': different,
                              'potential_metadata_conflicts': [k for k in different if k not in DYNAMIC]})
            elif r['product_title'].casefold() == previous['product_title'].casefold():
                flags.append({'capture_id': r['capture_id'], 'previous_capture_id': previous['capture_id'],
                              'type': 'possible_same_work_other_asin_or_market'})
    return flags


def ingest(source, root=ROOT, dry_run=False):
    data = source.read_bytes()
    records, evidence = parse_csv(data, root)
    batch_id = hashlib.sha256(data).hexdigest()
    base = root / 'research/marketplace/batches'
    target = base / batch_id
    if target.exists():
        return {'status': 'already_imported', 'batch_id': batch_id}
    old = history(base)
    old_ids = {r['capture_id'] for r in old}
    if old_ids.intersection(r['capture_id'] for r in records):
        raise ValueError('capture_id already exists; use a new ID for corrections/reobservations')
    flags = flag_changes(old, records)
    for i, r in enumerate(records):
        flags.extend(flag_changes(records[:i], [r]))
    report = {'status': 'dry_run' if dry_run else 'imported', 'batch_id': batch_id,
              'imported_at_utc': datetime.now(timezone.utc).isoformat(), 'observations': len(records),
              'flags': flags, 'evidence_sha256': {k: hashlib.sha256(v).hexdigest() for k, v in evidence.items()},
              'verification': 'Import validates structure only; all evidence still needs human review'}
    if not dry_run:
        base.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(dir=base, prefix='.pending-') as temporary:
            staging = Path(temporary) / 'batch'
            staging.mkdir()
            (staging / 'input.csv').write_bytes(data)
            (staging / 'observations.json').write_text(json.dumps(records, indent=2, ensure_ascii=False) + '\n')
            (staging / 'report.json').write_text(json.dumps(report, indent=2) + '\n')
            assets = staging / 'evidence'
            assets.mkdir()
            for content in evidence.values():
                (assets / hashlib.sha256(content).hexdigest()).write_bytes(content)
            staging.rename(target)
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('csv_file', type=Path, nargs='?')
    parser.add_argument('--history', action='store_true', help='Print combined historical observations as JSON')
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()
    try:
        if args.history:
            print(json.dumps(history(ROOT / 'research/marketplace/batches'), indent=2))
        elif args.csv_file:
            print(json.dumps(ingest(args.csv_file, dry_run=args.dry_run), indent=2))
        else:
            parser.error('Supply a CSV file or --history')
    except (ValueError, OSError) as error:
        parser.exit(1, f'Import rejected: {error}\n')


if __name__ == '__main__':
    main()
