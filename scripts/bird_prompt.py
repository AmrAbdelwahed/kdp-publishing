"""Print a reference-driven prompt for one SPECIES_LIST.csv entry; no images generated."""
import argparse
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REFERENCE = 'books/book-001/artwork/candidates/cardinal-revised-review/source.png'


def prompt(species_id, species_reference=None):
    with (ROOT / 'books/book-001/blueprint/SPECIES_LIST.csv').open(newline='', encoding='utf-8') as stream:
        row = next((r for r in csv.DictReader(stream) if r['species_id'] == species_id), None)
    if row is None:
        raise ValueError(f'Unknown species ID: {species_id}')
    species_source = species_reference or row['candidate_reference_url']
    return (f"STYLE REFERENCE: attach {REFERENCE} as an image for line weight, simplicity and colouring-space style only. "
            f"SPECIES REFERENCE: {species_source}. Consult a separately verified, legally accessible reference "
            "for anatomy and markings; attach it separately when available. Compare closely related species before generation without inventing differences. A URL or description alone is not verified. "
            f"Create one NEW original black-outline colouring illustration of {row['common_name_candidate']} for ages 6–9. "
            f"Use its own species-specific silhouette and anatomy, not the cardinal's pose or shape. "
            f"Composition concept: {row['illustration_concept']}. "
            "Use the verified species-specific body shape and identification features; when verification is unavailable mark them pending. Match the reference's smooth moderately bold line weight, generous colouring spaces, "
            "simple naturalistic style and sparse background. Full subject within margins; white "
            "background; no text, shading, grey or copied photographs. Keep major dark plumage areas outlined and colourable, simplify fine details without erasing field marks, and preserve printable margins. Vary natural pose and environment "
            "from prior birds. Do not trace the species reference or copy its photo composition. "
            "Check identifying features, plumage and anatomy in a reliable field "
            f"guide before approval; unverified source locator: {row['candidate_reference_url']}. "
            "Human review must confirm line thickness, scientific accuracy and print placement.")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('species_id', nargs='+', help='one or more IDs, e.g. B05 B06')
    parser.add_argument('--species-reference', help='separately verified species reference path or URL (one species only)')
    parser.add_argument('--json', action='store_true', help='produce a generation-prompts.json list')
    args = parser.parse_args()
    if args.species_reference and len(args.species_id) != 1:
        parser.error('--species-reference applies to one species at a time')
    if args.json:
        with (ROOT / 'books/book-001/blueprint/SPECIES_LIST.csv').open(newline='', encoding='utf-8') as stream:
            names = {r['species_id']: r['common_name_candidate'] for r in csv.DictReader(stream)}
        entries = [{'species_id': sid, 'species': names[sid], 'prompt': prompt(sid, args.species_reference),
                    'visual_reference': REFERENCE, 'scientific_status': 'pending human reference review'}
                   for sid in args.species_id]
        print(json.dumps(entries, indent=2, ensure_ascii=False))
    else:
        for sid in args.species_id:
            print(prompt(sid, args.species_reference))
