"""Integrate original and reconstructed B1 scene into the frozen 8E layout for review."""
from pathlib import Path
import struct
import tempfile
import fitz
from PIL import Image,ImageDraw,ImageFont
import build_cover_8e as original_builder

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'books/book-001/cover-8g'
FONT=Path('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf')
SOURCE=OUT/'assets/source-original.png'
MODEL=OUT/'assets/realesrgan-x4plus-candidate.png'
DETAILS=[
 ('Crest, mask and bill',(520,65,805,380)),
 ('Wing and feather structure',(320,275,730,565)),
 ('Tail, legs and feet',(195,455,790,830)),
 ('Magnifier rim and notebook',(25,0,1120,505)),
 ('Binoculars and background',(630,565,1386,1135)),
 ('Model tile junction near wing / branch',(650,460,850,660)),
]


def png_stream(path):
    """Reuse an opaque, non-interlaced RGB PNG's lossless filtered IDAT in a PDF."""
    with open(path,'rb') as f:
        if f.read(8)!=b'\x89PNG\r\n\x1a\n':raise ValueError(f'Not PNG: {path}')
        parts=[];header=None
        while True:
            size=struct.unpack('>I',f.read(4))[0];kind=f.read(4);data=f.read(size);f.read(4)
            if kind==b'IHDR':header=struct.unpack('>IIBBBBB',data)
            elif kind==b'IDAT':parts.append(data)
            elif kind==b'IEND':break
    width,height,bits,color,compression,filter_method,interlace=header
    if (bits,color,compression,filter_method,interlace)!=(8,2,0,0,0):
        raise ValueError(f'Expected non-interlaced RGB8 PNG: {path}')
    return width,height,b''.join(parts)


def set_png_stream(doc,xref,path):
    width,height,data=png_stream(path)
    doc.update_stream(xref,data,compress=0)
    doc.xref_set_key(xref,'Filter','/FlateDecode')
    doc.xref_set_key(xref,'DecodeParms',f'<</Predictor 15 /Colors 3 /BitsPerComponent 8 /Columns {width}>>')
    return width,height


def compact_integrated(pdf_path,png_path):
    """Remove ASCII85 overhead while preserving every PNG source pixel."""
    doc=fitz.open(pdf_path);xrefs={im['xref'] for p in doc for im in p.get_image_info(xrefs=True)}
    if len(xrefs)!=1:raise ValueError(f'Expected exactly one scene raster in {pdf_path}')
    set_png_stream(doc,xrefs.pop(),png_path)
    tmp=pdf_path.with_name(pdf_path.stem+'-tmp.pdf')
    doc.save(tmp,garbage=4,deflate=True);doc.close();tmp.replace(pdf_path)


def build():
    with Image.open(SOURCE) as src,Image.open(MODEL) as rec:
        if src.size!=(1386,1135) or rec.size!=(5544,4540):raise ValueError('Unexpected source or 4x model dimensions')
    original_builder.OUT=OUT
    for label,path in [('source',SOURCE),('reconstructed',MODEL)]:
        original_builder.build(scene_path=path)
        for name in ('B1-full-wrap-REVIEW.pdf','front-back-actual-size-REVIEW.pdf'):
            compact_integrated(OUT/name,path)
        for name,renamed in [('B1-full-wrap-REVIEW.pdf',f'{label}-integrated-REVIEW.pdf'),
            ('front-back-actual-size-REVIEW.pdf',f'{label}-front-back-actual-size-REVIEW.pdf'),
            ('B1-front-screen-preview.png',f'{label}-front-screen.png'),
            ('B1-back-screen-preview.png',f'{label}-back-screen.png'),
            ('B1-wrap-screen-preview.png',f'{label}-wrap-screen.png')]:
            (OUT/name).replace(OUT/renamed)
    # Two letter-size pages place the entire scene at its exact final dimensions.
    # The separately generated front/back PDFs show the two integrated versions.
    compare=fitz.open()
    for label,path in [('USER ORIGINAL — 163 PPI',SOURCE),('REAL-ESRGAN x4 — OUTPUT SAMPLING ~652 PPI',MODEL)]:
        page=compare.new_page(width=612,height=792);page.insert_font(fontname='dejavu',fontfile=str(FONT))
        page.insert_text((24,45),label,fontsize=12,fontname='dejavu')
        page.insert_text((24,64),'Review only • image placed 8.5 × 6.9608 in • print Actual Size',fontsize=9,fontname='dejavu')
        xref=page.insert_image(fitz.Rect(0,140,612,641.1745),filename=str(path),keep_proportion=False)
        set_png_stream(compare,xref,path)
    compare.set_metadata({'title':'Original and reconstructed B1 artwork — actual-size comparison, review only'})
    compare.save(OUT/'actual-size-comparison-REVIEW.pdf',garbage=4,deflate=True);compare.close()
    detail=fitz.open()
    with Image.open(SOURCE) as src,Image.open(MODEL) as rec,tempfile.TemporaryDirectory(prefix='cover-8g-details-') as tmp:
        for i,(label,box) in enumerate(DETAILS):
            page=detail.new_page(width=612,height=792);page.insert_font(fontname='dejavu',fontfile=str(FONT))
            page.insert_text((25,35),label,fontsize=16,fontname='dejavu')
            page.insert_text((25,60),'Original source',fontsize=11,fontname='dejavu');page.insert_text((319,60),'Real-ESRGAN ×4',fontsize=11,fontname='dejavu')
            page.insert_text((25,757),'Same image region and displayed size. Reconstruction may invent details.',fontsize=9,fontname='dejavu')
            a=Path(tmp)/f'{i}-a.png';b=Path(tmp)/f'{i}-b.png';src.crop(box).save(a)
            rec.crop(tuple(x*4 for x in box)).save(b)
            for path,rect in [(a,fitz.Rect(20,75,293,722)),(b,fitz.Rect(319,75,592,722))]:
                xref=page.insert_image(rect,filename=str(path),keep_proportion=True)
                set_png_stream(detail,xref,path)
    detail.set_metadata({'title':'B1 source versus AI reconstruction — enlarged details, review only'})
    detail.save(OUT/'enlarged-detail-comparison-REVIEW.pdf',garbage=4,deflate=True);detail.close()
    # Display-scaled previews are for screen comparison only.
    paths=[ROOT/'books/book-001/cover-8f/B1-front-screen-preview.png',OUT/'source-front-screen.png',OUT/'reconstructed-front-screen.png']
    sheet=Image.new('RGB',(1080,550),'#f3f2ec');draw=ImageDraw.Draw(sheet);f=ImageFont.truetype(str(FONT),16)
    for i,(label,path) in enumerate(zip(['8F baseline','New source','AI reconstruction'],paths)):
        with Image.open(path) as p:
            img=p.convert('RGB');img.thumbnail((330,475),Image.Resampling.LANCZOS)
        x=20+360*i;draw.text((x,8),label,font=f,fill='black');sheet.paste(img,(x,38))
    draw.text((20,522),'Screen preview — layout unchanged; scene, edges and print quality require human review.',font=f,fill='black')
    sheet.save(OUT/'composition-comparison.png')
    print('Built both review wraps, actual-size comparison and six paired detail pages.')

if __name__=='__main__':build()
