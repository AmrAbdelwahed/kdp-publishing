"""Build a provisional batch proof using the existing page layout and traced artwork."""
from pathlib import Path
import json
import tempfile
import fitz
from PIL import Image, ImageOps, ImageDraw, ImageFont
import build_three_bird_prototype as layout

ROOT = Path(__file__).resolve().parents[1]
BATCH = ROOT / 'books/book-001/artwork/batch-01'
FONT = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'


def build(output_dir=BATCH):
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    manifest = json.loads((BATCH / 'manifest.json').read_text())
    entries = {r['species_id']: r for r in manifest['entries']}
    existing = {r['kind']: r for r in layout.BIRDS}
    jay = {'name':'Blue Jay','page':4,'kind':'bluejay','cue':'Look closely at the crest, bill and tail.',
           'task':'Compare this bird with a checked bird guide.', 'clues':['Crest','Collar','Tail'],
           'mission_lines':['Sketch this bird and one from a guide.', 'Circle a difference in head shape or tail.'], 'draw_boxes':True,
           'observe':'With an adult, look quietly at a bird or guide. Which shapes can you see?',
           'note':'Use a local guide; not all birds are found everywhere.', 'skill':'Compare shapes'}
    nuthatch = {'name':'White-breasted Nuthatch','page':14,'kind':'nuthatch',
                'cue':'Look at the head, bill and tail.', 'task':'Which way is the bird facing?', 'clues':['Head','Bill','Tail'],
                'mission_lines':['Draw an arrow from the body toward the head.', 'Compare it with a bird picture in a checked guide.'], 'draw_boxes':True,
                'observe':'With an adult, look quietly at a bird or guide. Sketch the direction it faces.',
                'note':'Check a local guide; not all birds are found everywhere.', 'skill':'Notice direction'}
    dove = {'name':'Mourning Dove','page':26,'kind':'dove','cue':'Point to the head and long tail.',
            'task':'Compare body and tail shapes with a checked guide.', 'clues':['Head','Body','Tail'],
            'mission_lines':['Sketch the bird on the left and one in a guide.', 'Circle a shape that looks different.'], 'draw_boxes':True,
            'observe':'With an adult, observe a bird or a guide. Is its tail short or long?',
            'note':'Use a local guide; birds vary by place and season.', 'skill':'Compare silhouettes'}
    layout.BIRDS = [existing['cardinal'], jay, existing['robin'], existing['chickadee'], nuthatch, dove]
    with tempfile.TemporaryDirectory(prefix='bird-batch-proof-') as tmp:
        layout.OUT = Path(tmp)
        layout.build()
        proof = output_dir / 'six-bird-provisional-proof.pdf'
        with fitz.open(Path(tmp) / 'three-bird-prototype.pdf') as doc:
            subjects = [('B01','cardinal'),('B02','Blue Jay'),('B03','American Robin'),
                        ('B04','Black-capped Chickadee'),('B07','White-breasted Nuthatch'),('B13','Mourning Dove')]
            for i,(sid,name) in enumerate(subjects):
                page = doc[2*i]
                area = fitz.Rect(48,167,555,602)
                page.add_redact_annot(area,fill=(1,1,1))
                if sid == 'B01':
                    page.add_redact_annot(fitz.Rect(36,621,345,643),fill=(1,1,1))
                    vector = ROOT/'books/book-001/artwork/candidates/cardinal-revised-review/cardinal-vector-art.pdf'
                    label = 'MASTER STYLE: VISUALLY ACCEPTED; PRINT / FACT CHECK PENDING'
                else:
                    vector = ROOT/entries[sid]['vector_art_pdf']
                    if entries[sid].get('visual_decision') == 'PROVISIONALLY_ACCEPTED_BY_USER':
                        label = 'VISUALLY ACCEPTED / PRINT / FACT CHECK PENDING'
                    else:
                        label = entries[sid]['review_classification'].replace('_',' ') + ' / UNAPPROVED'
                page.apply_redactions(images=2,graphics=1,text=0)
                with fitz.open(vector) as artwork:
                    page.show_pdf_page(area,artwork,0,keep_proportion=True)
                page.insert_font(fontname='DV',fontfile=FONT)
                page.insert_text((40,640),label,fontsize=9,fontname='DV')
            doc.xref_set_key(doc.pdf_catalog(),'PageLayout','/TwoPageLeft')
            doc.save(proof,deflate=True,garbage=4)
            if len(doc)!=12: raise ValueError('Expected six pairs')
            sheet=Image.new('RGB',(2*326,6*416),'white')
            for i,page in enumerate(doc):
                if (page.rect.width,page.rect.height)!=(612,792): raise ValueError('Unexpected page size')
                pix=page.get_pixmap(matrix=fitz.Matrix(.5,.5),alpha=False)
                im=Image.frombytes('RGB',(pix.width,pix.height),pix.samples)
                sheet.paste(im,((i%2)*326+10,(i//2)*416+10))
            sheet.save(output_dir/'facing-spreads-contact.png')
    # 5 pairs of original source and rendered vector. Both fit identical thumbnails.
    sheet=Image.new('RGB',(1200,5*700),'white')
    draw=ImageDraw.Draw(sheet); font=ImageFont.truetype(FONT,20)
    for row,sid in enumerate(['B02','B03','B04','B07','B13']):
        entry=entries[sid]
        original=ImageOps.expand(Image.open(ROOT/entry['original_path']).convert('RGB'),border=80,fill='white')
        with fitz.open(ROOT/entry['vector_art_pdf']) as pdf:
            pix=pdf[0].get_pixmap(matrix=fitz.Matrix(.5,.5),alpha=False)
            vector=Image.frombytes('RGB',(pix.width,pix.height),pix.samples)
        for col,im in enumerate((original,vector)):
            im.thumbnail((560,620));sheet.paste(im,(col*600+(600-im.width)//2,row*700+62))
            draw.text((col*600+12,row*700+10),f"{entry['species']} / {'ORIGINAL' if col==0 else 'VECTOR'}",font=font,fill='black')
            draw.text((col*600+12,row*700+36),entry['review_classification'].replace('_',' '),font=font,fill='black')
    sheet.save(output_dir/'original-versus-vector-contact.png')
    print('Created provisional 12-page proof and contact sheets; scientific and print review remain pending.')


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=BATCH)
    build(parser.parse_args().output)
