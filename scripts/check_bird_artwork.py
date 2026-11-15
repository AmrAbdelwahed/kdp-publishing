"""Check candidate image geometry and provenance; never approve anatomy automatically."""
import hashlib
import json
from pathlib import Path
from PIL import Image, ImageChops, ImageOps

ROOT = Path(__file__).resolve().parents[1]
ART = ROOT / 'books/book-001/artwork'
# Actual image fit box in the prototype (points); aspect-ratio-preserving.
BOX_W, BOX_H = 507, 435


def analyze(entry):
    path = (ROOT / entry['path']).resolve()
    if not path.is_relative_to(ART.resolve()) or not path.is_file():
        raise ValueError('Artwork path must be an existing file within artwork/')
    content = path.read_bytes()
    digest = hashlib.sha256(content).hexdigest()
    if digest != entry['sha256'] or not entry.get('provenance'):
        raise ValueError(f'Artwork identity/provenance mismatch: {path.name}')
    with Image.open(path) as image:
        image.load()
        width, height = image.size
        scale = min(BOX_W / width, BOX_H / height)
        placed_w, placed_h = width * scale, height * scale
        ppi_x, ppi_y = width / (placed_w / 72), height / (placed_h / 72)
        gray = ImageOps.grayscale(image)
        ink = gray.point(lambda x: 255 if x < 200 else 0)
        bounds = ink.getbbox()
        small = ImageOps.grayscale(image).resize((9, 8))
        dhash = sum((small.getpixel((x, y)) > small.getpixel((x+1, y))) << (y*8+x)
                    for y in range(8) for x in range(8))
        edges = bool(bounds and min(bounds[0], bounds[1], width-bounds[2], height-bounds[3]) < min(width,height)*0.01)
        return {'species':entry['species'], 'path':entry['path'], 'sha256':digest,
                'provenance':entry['provenance'], 'format':image.format, 'pixels':[width,height],
                'placed_inches':[round(placed_w/72,3), round(placed_h/72,3)],
                'effective_ppi':[round(ppi_x,1), round(ppi_y,1)], 'resolution_pass':min(ppi_x,ppi_y)>=300,
                'ink_bbox_pixels':bounds, 'edge_ink_warning':edges,
                'blank_warning':bounds is None or sum(ink.histogram()[1:]) < width*height*0.001,
                'human_approved':entry.get('human_approved') is True,
                'approval_record_complete':bool(entry.get('reviewer') and entry.get('reviewed_at') and entry.get('approval_scope')),
                'approved_directory':path.is_relative_to((ART/'approved').resolve()),
                'line_and_placement_reviewed':entry.get('line_and_placement_reviewed') is True,
                'line_thickness':'not automatically verified; inspect at final scale',
                'anatomy_and_field_marks':'human review required', '_dhash':dhash}


def report(entries):
    result=[analyze(x) for x in entries]
    for i,a in enumerate(result):
        a['possible_duplicates']=[b['species'] for j,b in enumerate(result) if j!=i and
                                  (a['sha256']==b['sha256'] or (a['_dhash']^b['_dhash']).bit_count()<=6)]
        a['ready_for_placement'] = all([a['resolution_pass'], not a['blank_warning'], not a['edge_ink_warning'],
                                        a['human_approved'], a['approval_record_complete'], a['approved_directory'], a['line_and_placement_reviewed'],
                                        not a['possible_duplicates']])
    for a in result: del a['_dhash']
    return result


if __name__ == '__main__':
    entries=json.loads((ART/'manifest.json').read_text())
    data=report(entries)
    (ART/'image-quality-report.json').write_text(json.dumps(data,indent=2)+'\n')
    for r in data:
        print(r['species'],r['pixels'],r['effective_ppi'],'ready:',r['ready_for_placement'])
