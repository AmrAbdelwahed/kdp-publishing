"""Import immutable Week 1 evidence. Requires openpyxl (already installed here).
Run from any directory: python scripts/import_week1.py. No network requests.
"""
import csv
import hashlib
import json
from datetime import datetime, timezone
from decimal import Decimal, ROUND_CEILING, ROUND_HALF_UP
from pathlib import Path

import openpyxl

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / 'research/raw'
D = lambda value: Decimal(str(value))


def save_csv(name, records, fields):
    with (ROOT / 'research' / name).open('w', newline='', encoding='utf-8') as stream:
        writer = csv.DictWriter(stream, fieldnames=fields, lineterminator='\n')
        writer.writeheader()
        writer.writerows(records)


def import_sources():
    book = RAW / 'week1_scorecard.xlsx'
    report = ROOT / 'research/import_manifest.json'
    hashes = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in
              (book, RAW / 'week1_niche_validation.md')}
    if report.exists():
        manifest = json.loads(report.read_text())
        if manifest['sha256'] != hashes:
            raise ValueError('Raw evidence changed; investigate before replacing the manifest')
    else:
        manifest = {'imported_at_utc': datetime.now(timezone.utc).isoformat(),
                    'research_date_reported': '2026-11-10', 'sha256': hashes,
                    'uploaded_workbook_name': 'week1_scorecard_1_.xlsx',
                    'stored_workbook_name': book.name,
                    'retrieval_timestamp_note': 'Source research date only; individual web retrieval times absent'}
        report.write_text(json.dumps(manifest, indent=2) + '\n')
    wb = openpyxl.load_workbook(book, data_only=False)
    cached = openpyxl.load_workbook(book, data_only=True)
    assert wb.sheetnames == ['Niche Scorecard', '18 Competitors', 'Royalty Scenarios']
    snapshot = {s.title: {c.coordinate: {'raw': c.value, 'cached': cached[s.title][c.coordinate].value}
                        for row in s for c in row if c.value is not None} for s in wb}
    (ROOT / 'research/workbook_cells.json').write_text(json.dumps(snapshot, indent=2, ensure_ascii=False) + '\n')
    score = wb['Niche Scorecard']
    weights = [D(score.cell(6, col).value) for col in range(2, 7)]
    assert sum(weights) == 1
    scores = []
    criteria = ['demand', 'differentiation', 'competition_ease', 'economics', 'kdp_fit']
    for row in range(2, 5):
        values = [D(score.cell(row, col).value) for col in range(2, 7)]
        assert all(1 <= v <= 5 for v in values)
        weighted = sum(v * w for v, w in zip(values, weights))
        total = weighted / 5 * 100
        assert abs(D(cached[score.title][f'G{row}'].value) - weighted) < D('0.000000001')
        assert abs(D(cached[score.title][f'H{row}'].value) - total) < D('0.000000001')
        assert score[f'G{row}'].value == '=' + '+'.join(f'{c}{row}*{c}$6' for c in 'BCDEF')
        assert score[f'H{row}'].value == f'=G{row}/5*100'
        record = {'niche': score.cell(row, 1).value, 'reported_score_out_of_100': str(total.normalize()),
                  'recomputed_score_out_of_100': str(total.normalize()), 'weighted_out_of_5': str(weighted),
                  'evidence_class': 'analyst_judgment', 'source_artifact': 'research/raw/week1_scorecard.xlsx',
                  'source_location': f"Niche Scorecard!A{row}:H{row}; weights B6:F6",
                  'calculation_status': 'matches_source_inputs_and_cache',
                  'limitations': 'Arithmetic verified; qualitative judgments are not validated sales probabilities'}
        record.update({f'{k}_rating': str(v) for k, v in zip(criteria, values)})
        record.update({f'{k}_weight': str(w) for k, w in zip(criteria, weights)})
        scores.append(record)
    save_csv('niche_scorecard.csv', scores, list(scores[0]))
    competitors = []
    for row in range(2, 20):
        cells = [wb['18 Competitors'].cell(row, col).value for col in range(1, 19)]
        niche,title,relevance,market,identifier,us,ca,provenance,pages,published,stars,count,bsr,url,source,secondary,position,limitations = cells
        markets = [('US', us), ('CA', ca)] if us is not None and ca is not None else [('CA', ca)] if ca is not None else [('US', us)]
        evidence = 'third_party_snapshot' if 'aggregator' in market else 'publisher_or_retailer'
        for region, price in markets:
            # ISBN10 is retained as such, not silently asserted to be a confirmed ASIN.
            known = identifier if identifier != 'Unverified' else ''
            note = 'Source research imported; not independently retrieved. Web retrieval time absent. '
            if row == 17:
                note += 'Ratings attributed to aggregator but exact rating URL not identified; do not attribute to publisher. '
            record = dict(record_id=f'W1-{row:02}-{region}',work_id=f'W1-{row:02}',niche=niche,
                          marketplace='Amazon.ca' if region == 'CA' and 'aggregator' in market else 'Amazon.com' if 'aggregator' in market else '',
                          source_market=market,observation_region=region,title=title,
                          asin=known if known.startswith('B0') else '',isbn10=known if known and not known.startswith('B0') else '',
                          identifier_as_reported=identifier,format='',language='',page_count=pages,price=price,
                          currency='CAD' if region == 'CA' else 'USD',price_provenance=provenance,
                          publication_as_reported=published,review_count='',rating_count=count,star_rating=stars,bsr='',bsr_category='',
                          bsr_as_reported=bsr,relevance=relevance,age_range='',positioning=position,
                          educational_features='',source_url=source,secondary_source_url=secondary,product_url=url,
                          source_type=evidence,research_date_reported='2026-11-10',retrieved_at_utc='',
                          imported_at_utc=manifest['imported_at_utc'],source_artifact='research/raw/week1_scorecard.xlsx',
                          source_location=f"18 Competitors!A{row}:R{row}",verification_status='imported_not_live_verified',
                          limitations=note + limitations)
            competitors.append(record)
    assert len(competitors) == 20 and len({r['work_id'] for r in competitors}) == 18
    save_csv('competitors.csv', competitors, list(competitors[0]))
    royalties=[]
    s=wb['Royalty Scenarios']
    for row in range(2, 8):
        market,price,rate,cost=[s.cell(row,col).value for col in range(1,5)]
        royalty=D(price)*D(rate)-D(cost)
        assert royalty > 0
        assert abs(D(cached[s.title][f'E{row}'].value)-royalty) < D('0.000000001')
        assert s[f'E{row}'].value == f'=B{row}*C{row}-D{row}'
        breaks={str(spend): int((D(spend)/royalty).to_integral_value(rounding=ROUND_CEILING)) for spend in (20,50)}
        for col,spend in [('F',20),('G',50)]:
            assert s[f'{col}{row}'].value == f'=ROUNDUP({spend}/E{row},0)'
            assert cached[s.title][f'{col}{row}'].value == breaks[str(spend)]
        royalties.append(dict(market=market,currency='USD' if market=='US' else 'CAD',list_price=price,
                              royalty_rate=rate,print_cost=cost,recomputed_royalty=str(royalty),
                              displayed_royalty=str(royalty.quantize(D('0.01'), rounding=ROUND_HALF_UP)),break_even_20=breaks['20'],break_even_50=breaks['50'],
                              source_url=s[f'H{row}'].value,source_artifact='research/raw/week1_scorecard.xlsx',
                              source_location=f'Royalty Scenarios!A{row}:H{row}',calculation_status='matches_formula_and_cache',
                              current_policy_status='not_independently_verified',retrieved_at_utc='',
                              limitations='Same-currency spend coverage only; excludes other costs; not profit or sales forecast'))
    save_csv('royalty_scenarios.csv', royalties, list(royalties[0]))
    print('PASS: immutable source hashes; 3 scores; 18 works / 20 market observations; 6 royalty scenarios.')


if __name__ == '__main__':
    import_sources()
