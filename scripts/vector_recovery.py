"""Reproduce the provisional vectorization experiment; requires VTracer 0.6.15.
Run: PYTHONPATH=/tmp/kdp-vector-tools python scripts/vector_recovery.py
Outputs are review artifacts, not approved production assets.
"""
from pathlib import Path
import hashlib, io, json, tempfile, xml.etree.ElementTree as ET
import fitz
import numpy as np
from PIL import Image, ImageOps, ImageDraw, ImageFont
from scipy import ndimage
import vtracer

ROOT=Path(__file__).resolve().parents[1]
ART=ROOT/'books/book-001/artwork'
OUT=ART/'vector-recovery'
NAMES=('cardinal','robin','chickadee')
PAD=80
FONT='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'

def png_from_fitz(pix):
 return Image.frombytes('RGB',(pix.width,pix.height),pix.samples)


def trace(name, temp):
 source=ART/'candidates'/f'{name}.png'
 image=Image.open(source).convert('L')
 ink=np.array(image)<160
 labels,count=ndimage.label(ink)
 sizes=np.bincount(labels.ravel()); tiny=sizes<4;tiny[0]=False
 clean=ink & ~tiny[labels]
 padded=ImageOps.expand(Image.fromarray(np.uint8(~clean)*255),border=PAD,fill=255)
 temp_png=temp/f'{name}.png';padded.save(temp_png)
 svg=OUT/f'{name}-provisional.svg'
 vtracer.convert_image_to_svg_py(str(temp_png),str(svg),colormode='binary',mode='spline',filter_speckle=4,corner_threshold=60,length_threshold=4.0,max_iterations=10,splice_threshold=45,path_precision=2)
 tree=ET.parse(svg); elems=list(tree.getroot().iter()); names=[e.tag.rsplit('}',1)[-1] for e in elems]
 if 'image' in names or 'path' not in names: raise ValueError('SVG must contain vector paths, no embedded image')
 doc=fitz.open(str(svg)); vector=doc.convert_to_pdf();doc.close()
 pdf=OUT/f'{name}-vector-art.pdf';pdf.write_bytes(vector)
 with fitz.open(stream=vector,filetype='pdf') as d:
  pix=d[0].get_pixmap(matrix=fitz.Matrix(1,1),alpha=False)
  rendered=png_from_fitz(pix).convert('L').resize(padded.size)
  assert not d[0].get_images(), 'Vector art PDF contains raster image'
 ref=np.array(padded)<128; result=np.array(rendered)<128
 union=np.count_nonzero(ref|result); iou=np.count_nonzero(ref&result)/union
 # Count enclosed white regions above 25 pixels; an approximate topology indicator only.
 def holes(mask):
  labels,n=ndimage.label(~mask); counts=np.bincount(labels.ravel()); edges=np.unique(np.r_[labels[0,:],labels[-1,:],labels[:,0],labels[:,-1]])
  return sum(1 for k in range(1,n+1) if k not in edges and counts[k]>=25)
 bbox=Image.fromarray(np.uint8(result)*255).getbbox()
 dist=ndimage.distance_transform_edt(result)
 peaks=(dist==ndimage.maximum_filter(dist,size=3)) & result
 widths=(2*dist[peaks]-1)*435/1472
 thin_pct=100*float(np.mean(widths<0.75)) if widths.size else None
 return dict(species=name,source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),svg_paths=names.count('path'),svg_has_image=False,svg_bytes=svg.stat().st_size,
             input_size=list(image.size),canvas_size=list(padded.size),added_padding_pixels=PAD,source_ink_pixels=int(ink.sum()),removed_speckle_pixels=int((ink & ~clean).sum()),
             threshold=160,threshold_mask_iou=round(float(iou),4),source_enclosed_white_regions_25px=holes(ref),vector_enclosed_white_regions_25px=holes(result),
             vector_ink_bbox=bbox,thin_local_maxima_below_075pt_pct=round(thin_pct,2) if thin_pct is not None else None,
             minimum_line_thickness_pt='not proven: filled paths and raster-based local-maxima heuristic; inspect manually',
             anatomical_approval='not reviewed',disposition='PROVISIONAL_REVIEW_REQUIRED'),padded,vector


def main():
 OUT.mkdir(parents=True,exist_ok=True)
 font=ImageFont.truetype(FONT,23); small=ImageFont.truetype(FONT,18)
 review=Image.new('RGB',(3*640,760),'white'); rd=ImageDraw.Draw(review)
 compare=Image.new('RGB',(2*640,3*720),'white'); cd=ImageDraw.Draw(compare)
 details=Image.new('RGB',(4*500,3*540),'white'); dd=ImageDraw.Draw(details)
 vector_details=Image.new('RGB',(4*500,3*540),'white'); vd=ImageDraw.Draw(vector_details)
 cropboxes=[('HEAD / BILL',(580,0,1140,470)),('WING',(230,330,850,900)),('FEET',(420,770,1030,1150)),('TAIL / EDGE',(0,680,520,1312))]
 results=[];vectors={}
 with tempfile.TemporaryDirectory() as td:
  temp=Path(td)
  for i,name in enumerate(NAMES):
   info,padded,vector=trace(name,temp);results.append(info);vectors[name]=vector
   orig=Image.open(ART/'candidates'/f'{name}.png').convert('RGB')
   thumb=orig.copy();thumb.thumbnail((600,680));review.paste(thumb,(i*640+(640-thumb.width)//2,55));rd.text((i*640+20,12),name.upper()+' — ORIGINAL',font=font,fill='black')
   with fitz.open(stream=vector,filetype='pdf') as doc:
    vp=doc[0].get_pixmap(matrix=fitz.Matrix(1,1),alpha=False); vfull=png_from_fitz(vp); vimg=vfull.copy()
   for col,(im,label) in enumerate([(padded.convert('RGB'),'ORIGINAL + 80 PX PAD'),(vimg,'VECTOR RENDER')]):
    thumb=im.copy();thumb.thumbnail((600,660));compare.paste(thumb,(col*640+(640-thumb.width)//2,i*720+50));cd.text((col*640+18,i*720+12),name.upper()+' — '+label,font=font,fill='black')
   for j,(label,coords) in enumerate(cropboxes):
    crop=orig.crop(coords);crop.thumbnail((480,480));details.paste(crop,(j*500+(500-crop.width)//2,i*540+50));dd.text((j*500+10,i*540+10),f'{name.upper()} {label}',font=small,fill='black')
    shifted=tuple(v+PAD for v in coords); vcrop=vfull.crop(shifted);vcrop.thumbnail((480,480));vector_details.paste(vcrop,(j*500+(500-vcrop.width)//2,i*540+50));vd.text((j*500+10,i*540+10),f'{name.upper()} VECTOR {label}',font=small,fill='black')
   # Actual letter-size pages, identical placement box for original and vector.
   doc=fitz.open()
   for vector_mode in (False,True):
    page=doc.new_page(width=612,height=792);page.insert_font(fontname='DV',fontfile=FONT);page.insert_text((48,45),f'DRAFT {name.upper()} - '+('VECTOR' if vector_mode else 'ORIGINAL PNG'),fontsize=11,fontname='DV')
    rect=fitz.Rect(48,167,555,602)
    if vector_mode:
     with fitz.open(stream=vector,filetype='pdf') as src: page.show_pdf_page(rect,src,0,keep_proportion=True)
    else:
     buf=io.BytesIO();padded.save(buf,format='PNG');page.insert_image(rect,stream=buf.getvalue(),keep_proportion=True)
    page.insert_text((48,638),'Same placement box: 507 x 435 pt; 80 px source padding. Not approved.',fontsize=9,fontname='DV')
   doc.save(OUT/f'{name}-comparison-print-size.pdf',deflate=True)
   pix=doc[1].get_pixmap(matrix=fitz.Matrix(300/72,300/72),alpha=False)
   pix.save(str(OUT/f'{name}-vector-300dpi.png'))
   doc.close()
 review.save(OUT/'original-review-sheet.png');compare.save(OUT/'original-vs-vector-sheet.png');details.save(OUT/'original-detail-crops.png');vector_details.save(OUT/'vector-detail-crops.png')
 # Put provisional vector art into a separate proof; do not modify the approved-asset workflow.
 with fitz.open(ROOT/'books/book-001/prototype/three-bird-prototype.pdf') as doc:
  for i,name in [(0,'cardinal'),(2,'chickadee'),(4,'robin')]:
   page=doc[i];rect=fitz.Rect(48,167,555,602)
   page.add_redact_annot(rect,fill=(1,1,1))
   if i==0: page.add_redact_annot(fitz.Rect(36,621,345,643),fill=(1,1,1))
   page.apply_redactions(images=2,graphics=1,text=0)
   with fitz.open(stream=vectors[name],filetype='pdf') as src:page.show_pdf_page(rect,src,0,keep_proportion=True)
   page.insert_font(fontname='DV',fontfile=FONT);page.insert_text((48,640),'PROVISIONAL VECTOR - NOT APPROVED',fontsize=9,fontname='DV')
  doc.save(OUT/'three-bird-provisional-vector-prototype.pdf',deflate=True,garbage=4)
 (OUT/'measurements.json').write_text(json.dumps(results,indent=2)+'\n')
 print(json.dumps(results,indent=2))

if __name__=='__main__':main()
