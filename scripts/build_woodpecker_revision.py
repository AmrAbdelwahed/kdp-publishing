"""Build the two-bird review interior and comparisons from preserved sources.

Run after tracing B09-v2 and B10-v2 with process_bird_batch.py.
"""
import csv, json, hashlib, io
from pathlib import Path
import fitz
from PIL import Image,ImageOps,ImageDraw,ImageFont
R=Path(__file__).resolve().parents[1]; out=R/'books/book-001/woodpecker-revisions'; batch=R/'books/book-001/artwork/batch-02'; old=R/'books/book-001/preflight-9/interior-candidate-REVIEW.pdf'; out.mkdir(exist_ok=True)
specs=[('B09','Downy Woodpecker',18),('B10','Hairy Woodpecker',20)]
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
manifest=[]
with fitz.open(old) as doc:
 for sid,name,num in specs:
  page=doc[num-1]; forms=[x for x in page.get_xobjects() if x[2]==0]; assert len(forms)==1 and forms[0][1]=='Fm1'
  box=fitz.Rect(forms[0][3]); rect=fitz.Rect(box.x0,page.rect.height-box.y1,box.x1,page.rect.height-box.y0)
  matches=[]
  for x in page.get_contents():
   s=doc.xref_stream(x)
   if b'/Fm1 Do' in s: matches.append((x,s))
  assert len(matches)==1 and matches[0][1].count(b'/Fm1 Do')==1
  doc.update_stream(matches[0][0],matches[0][1].replace(b'/Fm1 Do',b''))
  art=batch/'processed'/f'{sid}-v2'/f'{sid}-vector-art.pdf'
  with fitz.open(art) as vect: page.show_pdf_page(rect,vect,0,keep_proportion=True)
  source=batch/'originals'/f'{sid}-v2.png'; qpath=art.parent/'quality.json'; quality=json.loads(qpath.read_text()); quality.pop('reference_path',None);quality.pop('reference_sha256',None); quality['visual_candidate_approval']='USER_ACCEPTED';quality['note']='Pipeline default reference fields removed: reference use in creating supplied artwork was not provided.';qpath.write_text(json.dumps(quality,indent=2)+'\n')
  manifest.append({'species_id':sid,'species':name,'revision':'v2','page':num,'source':str(source.relative_to(R)),'source_sha256':sha(source),'svg':str((art.parent/f'{sid}-provisional.svg').relative_to(R)),'svg_sha256':sha(art.parent/f'{sid}-provisional.svg'),'vector_pdf':str(art.relative_to(R)),'vector_pdf_sha256':sha(art),'user_visual_candidate_approval':True,'scientific_approval':False,'physical_print_approval':False,'artwork_box_pt':list(rect),'source_commit':'18e73368d2a2c6a5eb3004f76c3788b0c6962317'})
 doc.save(out/'64-page-interior-woodpecker-REVIEW.pdf',garbage=4,deflate=True)
(out/'ARTWORK_REVISIONS.json').write_text(json.dumps(manifest,indent=2)+'\n')
# Exact same box and scale as revised interior; source is padded without resizing before placement.
comp=fitz.open(); font='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
for m in manifest:
 sid=m['species_id'];rect=fitz.Rect(m['artwork_box_pt']); src=R/m['source']; art=R/m['vector_pdf']
 for mode in ('SOURCE PNG','TRACED VECTOR'):
  page=comp.new_page(width=612,height=792);page.insert_font(fontname='DV',fontfile=font)
  page.insert_text((45,62),f'{m["species"]} / {mode} / ACTUAL SIZE',fontsize=12,fontname='DV')
  page.insert_text((45,85),'Same placement as interior; scientific and physical review pending.',fontsize=9,fontname='DV')
  if mode=='SOURCE PNG':
   with Image.open(src) as im:
    padded=ImageOps.expand(im.convert('RGB'),border=80,fill='white');buf=io.BytesIO();padded.save(buf,format='PNG')
   page.insert_image(rect,stream=buf.getvalue(),keep_proportion=True)
  else:
   with fitz.open(art) as v:page.show_pdf_page(rect,v,0,keep_proportion=True)
  page.insert_text((45,660),'Print at 100% / actual size. Do not fit to page.',fontsize=10,fontname='DV')
comp.save(out/'woodpeckers-source-vs-vector-ACTUAL-SIZE.pdf',garbage=4,deflate=True)
comp.close()
# Both actual interior pages adjacent, without scaling, on a 17 x 11 inch sheet.
with fitz.open(out/'64-page-interior-woodpecker-REVIEW.pdf') as interior:
 spread=fitz.open(); page=spread.new_page(width=1224,height=792)
 page.show_pdf_page(fitz.Rect(0,0,612,792),interior,17)
 page.show_pdf_page(fitz.Rect(612,0,1224,792),interior,19)
 spread.save(out/'woodpeckers-side-by-side-ACTUAL-SIZE.pdf',garbage=4,deflate=True)
 spread.close()
# enlarged source/vector corresponding wing crops for manual inspection
sheet=Image.new('RGB',(1600,1600),'white'); draw=ImageDraw.Draw(sheet); font=ImageFont.truetype(font,26)
for row,m in enumerate(manifest):
 with Image.open(R/m['source']) as im: orig=ImageOps.expand(im.convert('RGB'),border=80,fill='white')
 with fitz.open(R/m['vector_pdf']) as doc:
  pix=doc[0].get_pixmap(alpha=False); vector=Image.frombytes('RGB',(pix.width,pix.height),pix.samples)
 for col,(im,label) in enumerate([(orig,'SOURCE'),(vector,'VECTOR')]):
  crop=im.crop((280,640,650,1360));crop.thumbnail((740,720));x=col*800+(800-crop.width)//2;y=row*800+65;sheet.paste(crop,(x,y));draw.text((col*800+20,row*800+15),m['species']+' '+label+' — enlarged wing',font=font,fill='black')
sheet.save(out/'wing-detail-source-vs-vector.png')
with (R/'books/book-001/preflight-9/ARTWORK_ISSUE_REGISTER.csv').open(newline='') as f:
 reader=csv.DictReader(f);fields=reader.fieldnames; rows=list(reader)
for row in rows:
 if row['species_id'] in ('B09','B10'):
  row['classification']='NEEDS HUMAN OR PRINT REVIEW'
  row['current_evidence_and_limits']='User-supplied v2 replaces v1 broad dark bands with outlined wing markings; source and vector inspection and equal enclosed-region counts support trace fidelity. Identification and correct coloring of checked wings require knowledgeable human review.'
  row['action']='Compare v2 and printed actual-size trace with Cornell; review checked wing coloring, head stripes, bill proportions, feet and tail. Scientific and physical approval remain pending.'
with (out/'ARTWORK_ISSUE_REGISTER.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=fields,lineterminator='\n');w.writeheader();w.writerows(rows)
