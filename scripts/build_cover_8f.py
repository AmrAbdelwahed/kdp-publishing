"""Reuse the frozen 8E design and prepare native-pixel replacement references."""
from pathlib import Path
from math import ceil
import hashlib
import json
from PIL import Image
import build_cover_8e as prior

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'books/book-001/cover-8f'
# Reference areas intentionally overlap and include background; they are not isolated cutouts.
SLOTS={
    'cardinal-reference':(145,145,750,740),
    'magnifier-notebook-reference':(20,105,900,903),
    'binoculars-reference':(490,590,1102,903),
}


def build():
    OUT.mkdir(parents=True,exist_ok=True)
    prior.OUT=OUT
    prior.build(include_scene=False)
    (OUT/'B1-full-wrap-REVIEW.pdf').replace(OUT/'B1-vector-base-ARTWORK-MISSING.pdf')
    prior.build()
    scene=OUT/'B1-scene-native-crop.png'; records=[]
    with Image.open(scene) as im:
        for name,(x0,y0,x1,y1) in SLOTS.items():
            path=OUT/f'{name}.png';im.crop((x0,y0,x1,y1)).save(path)
            # Coordinates are on the frozen 8E 8.5 x 11-in trim, measured from top left.
            x=x0*8.5/1102;y=(430+y0)*11/1427
            w=(x1-x0)*8.5/1102;h=(y1-y0)*11/1427
            records.append(dict(name=name,file=path.name,source_rect_px=[x0,y0,x1,y1],
                original_pixels=[x1-x0,y1-y0],front_trim_top_left_inches=[x,y],
                placement_inches=[w,h],minimum_pixels_300ppi=[ceil(w*300),ceil(h*300)],
                sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
                status='REFERENCE ONLY: contains background and overlap; not an isolated or high-resolution asset'))
    (OUT/'REFERENCE_SLOTS.json').write_text(json.dumps(records,indent=2)+'\n')
    print('Built frozen review wrap, vector-only base and native-pixel reference slots.')

if __name__=='__main__':build()
