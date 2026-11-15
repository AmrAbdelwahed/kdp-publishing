"""Prepare an honest review proof from the original M1E paths; no anatomical edits."""
from pathlib import Path
import io
import xml.etree.ElementTree as ET
import fitz
from PIL import Image, ImageDraw, ImageFont

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'books/book-001/artwork/vector-recovery'
OUT=ROOT/'books/book-001/artwork/vector-review-1f'
FONT='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
NAMES=('cardinal','robin','chickadee')


def make():
 OUT.mkdir(parents=True,exist_ok=True)
 vectors={}
 for name in NAMES:
  source=BASE/f'{name}-provisional.svg'
  root=ET.parse(source).getroot()
  if name=='chickadee':
   # Crop only blank outer canvas; preserve unscaled paths and aspect-ratio fit.
   root.set('width','1299');root.set('height','1412');root.set('viewBox','30 30 1299 1412')
  target=OUT/f'{name}-review-required.svg'
  ET.register_namespace('', 'http://www.w3.org/2000/svg')
  ET.ElementTree(root).write(target,encoding='utf-8',xml_declaration=True)
  with fitz.open(str(target)) as doc: vectors[name]=doc.convert_to_pdf()
  with fitz.open(stream=vectors[name],filetype='pdf') as doc:
   if doc[0].get_images():raise ValueError('Raster embedded in vector art')
   doc.save(OUT/f'{name}-review-art.pdf',deflate=True)
  # Comparison: same page box and aspect fit, original M1E versus M1F canvas.
  with fitz.open() as comp:
   for label,data in [('M1E original vector',None),('M1F review version - NOT APPROVED',vectors[name])]:
    pg=comp.new_page(width=612,height=792);pg.insert_font(fontname='DV',fontfile=FONT)
    pg.insert_text((42,45),name.upper()+' / '+label,fontname='DV',fontsize=11)
    if data is None:
     with fitz.open(str(source)) as original: data=original.convert_to_pdf()
    with fitz.open(stream=data,filetype='pdf') as artwork:
     pg.show_pdf_page(fitz.Rect(48,167,555,602),artwork,0,keep_proportion=True)
    pg.insert_text((42,638),'REVIEW REQUIRED: no anatomical corrections certified.',fontname='DV',fontsize=10)
   comp.save(OUT/f'{name}-comparison.pdf',deflate=True)
 # Reuse existing six-page proof, leaving the original PDF unchanged.
 proof=BASE/'three-bird-provisional-vector-prototype.pdf'
 with fitz.open(proof) as doc:
  pg=doc[2];box=fitz.Rect(48,167,555,602)
  pg.add_redact_annot(box,fill=(1,1,1));pg.apply_redactions(images=2,graphics=1,text=0)
  with fitz.open(stream=vectors['chickadee'],filetype='pdf') as artwork:
   pg.show_pdf_page(box,artwork,0,keep_proportion=True)
  doc.save(OUT/'six-page-review-proof.pdf',deflate=True,garbage=4)
 # 2 columns, one spread per row.
 with fitz.open(OUT/'six-page-review-proof.pdf') as doc:
  sheet=Image.new('RGB',(652,1248),'white')
  for i,page in enumerate(doc):
   pix=page.get_pixmap(matrix=fitz.Matrix(0.5,0.5),alpha=False)
   im=Image.frombytes('RGB',(pix.width,pix.height),pix.samples);sheet.paste(im,((i%2)*326+10,(i//2)*416+10))
  sheet.save(OUT/'facing-spread-contact-sheet.png')
  for i,name in [(0,'cardinal'),(2,'chickadee'),(4,'robin')]:
   with fitz.open() as single:
    single.insert_pdf(doc,from_page=i,to_page=i);single.save(OUT/f'{name}-printable-review-page.pdf',deflate=True,garbage=4)
 # Original vs framing comparison thumbnails; diagnostic, not a quality approval.
 sheet=Image.new('RGB',(1280,2160),'white');draw=ImageDraw.Draw(sheet);font=ImageFont.truetype(FONT,22)
 for row,name in enumerate(NAMES):
  with fitz.open(OUT/f'{name}-comparison.pdf') as d:
   for col in range(2):
    pix=d[col].get_pixmap(matrix=fitz.Matrix(1,1),alpha=False);im=Image.frombytes('RGB',(pix.width,pix.height),pix.samples);im.thumbnail((600,660));sheet.paste(im,(col*640+20,row*720+40))
  draw.text((20,row*720+8),name.upper()+': M1E VECTOR / M1F REVIEW VERSION',font=font,fill='black')
 sheet.save(OUT/'original-versus-review-sheet.png')
 print('Created review artifacts. Only chickadee framing changed; anatomy remains unverified.')

if __name__=='__main__':make()
