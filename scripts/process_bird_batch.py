"""Trace one unapproved original into a new revision; never overwrite prior assets.

Example: PYTHONPATH=/tmp/kdp-vector-tools python scripts/process_bird_batch.py
    --id B02 --source books/book-001/artwork/batch-01/originals/B02.png --revision v1
Requires the dependencies of vector_recovery.py, including vtracer.
"""
import argparse
import hashlib
import json
import shutil
import tempfile
from datetime import datetime, timezone
from pathlib import Path
import fitz
import numpy as np
from PIL import Image, ImageOps
from scipy import ndimage
import vector_recovery as pipeline

ROOT = Path(__file__).resolve().parents[1]
BATCH = ROOT / 'books/book-001/artwork/batch-01'
REFERENCE = ROOT / 'books/book-001/artwork/candidates/cardinal-revised-review/source.png'


def process(species_id, source, revision, batch=BATCH):
    batch = batch.resolve()
    art_root = (ROOT / 'books/book-001/artwork').resolve()
    if not batch.is_relative_to(art_root) or not batch.name.startswith('batch-'):
        raise ValueError('Batch must be a batch-* directory inside the artwork directory')
    prompts = json.loads((batch / 'generation-prompts.json').read_text())
    spec = next((x for x in prompts if x['species_id'] == species_id), None)
    if not spec:
        raise ValueError(f'{species_id} has no recorded prompt in {batch}')
    if not spec.get('generation_provenance') or not spec.get('reference_use'):
        raise ValueError('Record actual generation provenance and reference use before processing')
    if not revision or not revision.isalnum():
        raise ValueError('Revision must contain only letters and digits')
    source = source.resolve()
    if not source.is_relative_to((batch / 'originals').resolve()) or not source.is_file():
        raise ValueError('Source must be a preserved original PNG in the selected batch originals directory')
    target = batch / 'processed' / f'{species_id}-{revision}'
    if target.exists():
        raise FileExistsError(f'{target} already exists; use a new revision; previous assets are never overwritten')
    target.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(dir=target.parent, prefix='.staging-') as temporary:
        stage = Path(temporary)
        (stage / 'input/candidates').mkdir(parents=True)
        (stage / 'output').mkdir()
        shutil.copyfile(source, stage / 'input/candidates' / f'{species_id}.png')
        pipeline.ART, pipeline.OUT = stage / 'input', stage / 'output'
        info, padded, vector = pipeline.trace(species_id, stage)
        with fitz.open(stream=vector, filetype='pdf') as doc:
            pix = doc[0].get_pixmap(matrix=fitz.Matrix(1, 1), alpha=False)
            rendered = Image.frombytes('RGB', (pix.width, pix.height), pix.samples).convert('L')
        ink = np.asarray(rendered) < 128
        distance = ndimage.distance_transform_edt(ink)
        peaks = (distance == ndimage.maximum_filter(distance, size=3)) & ink
        # Trace's M1E metric was hardcoded for 1472 px; use this canvas's true fit.
        scale = min(507 / padded.width, 435 / padded.height)
        widths_pt = (2 * distance[peaks] - 1) * scale
        info['thin_local_maxima_below_075pt_pct'] = round(100 * float(np.mean(widths_pt < .75)), 2) if widths_pt.size else None
        info['width_screen_canvas_height'] = padded.height
        info['raw_effective_ppi_at_padded_placement'] = round(72 / scale, 1)
        info['placed_art_inches'] = [round(padded.width * scale / 72, 3), round(padded.height * scale / 72, 3)]
        im = Image.open(source).convert('L')
        source_ink = ImageOps.grayscale(im).point(lambda value: 255 if value < 200 else 0).getbbox()
        info['original_ink_bbox'] = source_ink
        info['original_edge_warning'] = bool(source_ink and min(source_ink[0], source_ink[1], im.width - source_ink[2], im.height - source_ink[3]) < min(im.size) * .01)
        info.update(species=spec['species'], species_id=species_id, revision=revision,
                    source_path=str(source.relative_to(ROOT)),
                    source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
                    reference_path=str(REFERENCE.relative_to(ROOT)),
                    reference_sha256=hashlib.sha256(REFERENCE.read_bytes()).hexdigest(),
                    provenance=spec['generation_provenance'], reference_use=spec['reference_use'],
                    processed_at_utc=datetime.now(timezone.utc).isoformat(),
                    human_approved=False, scientific_review='pending', print_review='pending',
                    warning='Heuristics do not prove closed regions or minimum stroke width; inspect at actual size')
        (stage / 'output' / 'quality.json').write_text(json.dumps(info, indent=2, ensure_ascii=False) + '\n')
        # Renaming a directory into a new target keeps previously completed revisions intact.
        (stage / 'output').rename(target)
    return info


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--id', required=True, dest='species_id')
    parser.add_argument('--source', required=True, type=Path)
    parser.add_argument('--revision', required=True)
    parser.add_argument('--batch', type=Path, default=BATCH, help='batch-* directory under books/book-001/artwork')
    args = parser.parse_args()
    print(json.dumps(process(args.species_id, args.source, args.revision, args.batch), indent=2, ensure_ascii=False))
