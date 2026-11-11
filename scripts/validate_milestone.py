"""Validate Milestone 0 structure; does not validate facts or market demand."""
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BLUEPRINT = ROOT / 'books/book-001/blueprint'


def rows(path):
    with path.open(newline='', encoding='utf-8') as stream:
        reader = csv.DictReader(stream)
        data = list(reader)
        if any(None in row or None in row.values() for row in data):
            raise ValueError(f'Malformed CSV: {path}')
        return data


def validate():
    pages = rows(BLUEPRINT / 'PAGE_PLAN.csv')
    species = rows(BLUEPRINT / 'SPECIES_LIST.csv')
    facts = rows(BLUEPRINT / 'FACT_CHECK_LOG.csv')
    assert [int(row['page']) for row in pages] == list(range(1, 65))
    ids = {row['species_id'] for row in species}
    assert len(species) == len(ids) == 30
    assert len({row['common_name_candidate'] for row in species}) == 30
    assert len({row['illustration_concept'] for row in species}) == 30
    assert len({row['activity_concept'] for row in species}) == 30
    for kind in ('colouring', 'activity'):
        selected = [row for row in pages if row['page_type'] == kind]
        assert len(selected) == 30
        assert {row['species_id'] for row in selected} == ids
    for index, bird in enumerate(species, 1):
        art, activity = pages[2 * index:2 * index + 2]
        assert art['species_id'] == activity['species_id'] == bird['species_id']
        assert int(activity['page']) == int(art['page']) + 1
    assert len(facts) == 150 and len({r['check_id'] for r in facts}) == 150
    assert all(r['status'] == 'pending' and not r['retrieved_at_utc'] for r in facts)
    assert {r['species_id'] for r in facts} == ids
    scores = rows(ROOT / 'research/niche_scorecard.csv')
    assert [r['reported_score_out_of_100'] for r in scores] == ['73.2', '63.3', '59.5']
    assert rows(ROOT / 'research/competitors.csv') == []
    slots = rows(ROOT / 'research/manual_collection.csv')
    assert len(slots) == 15 and all(not r['asin'] for r in slots)
    for path in ROOT.rglob('*.csv'):
        rows(path)
    print('PASS: 64 pages, 30 art/activity pairs, 150 pending checks, CSV structure.')
    print('NOT VALIDATED: missing workbook/Markdown, scores, marketplace facts, bird facts, KDP rules.')


if __name__ == '__main__':
    validate()
