"""Print a reference-driven prompt for one SPECIES_LIST.csv entry; no images generated."""
import argparse
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REFERENCE = 'books/book-001/artwork/candidates/cardinal-revised-review/source.png'


def prompt(species_id):
    with (ROOT / 'books/book-001/blueprint/SPECIES_LIST.csv').open(newline='', encoding='utf-8') as stream:
        row = next((r for r in csv.DictReader(stream) if r['species_id'] == species_id), None)
    if row is None:
        raise ValueError(f'Unknown species ID: {species_id}')
    return (f"Attach {REFERENCE} as a visual STYLE reference. Create one NEW original "
            f"black-outline colouring illustration of {row['common_name_candidate']} for ages 6–9. "
            f"Use its own species-specific silhouette and anatomy, not the cardinal's pose or shape. "
            f"Composition concept: {row['illustration_concept']}. "
            "Match the reference's smooth moderately bold line weight, generous colouring spaces, "
            "simple naturalistic style and sparse background. Full subject within margins; white "
            "background; no text, shading, grey or copied photographs. Vary pose and environment "
            "from prior birds. Check identifying features, plumage and anatomy in a reliable field "
            f"guide before approval; unverified source locator: {row['candidate_reference_url']}. "
            "Human review must confirm line thickness, scientific accuracy and print placement.")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('species_id', nargs='+', help='one or more IDs, e.g. B05 B06')
    parser.add_argument('--json', action='store_true', help='produce a generation-prompts.json list')
    args = parser.parse_args()
    if args.json:
        with (ROOT / 'books/book-001/blueprint/SPECIES_LIST.csv').open(newline='', encoding='utf-8') as stream:
            names = {r['species_id']: r['common_name_candidate'] for r in csv.DictReader(stream)}
        entries = [{'species_id': sid, 'species': names[sid], 'prompt': prompt(sid),
                    'visual_reference': REFERENCE, 'scientific_status': 'pending human reference review'}
                   for sid in args.species_id]
        print(json.dumps(entries, indent=2, ensure_ascii=False))
    else:
        for sid in args.species_id:
            print(prompt(sid))
