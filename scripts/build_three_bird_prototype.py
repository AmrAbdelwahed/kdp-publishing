"""Build the six-page editorial preview, not a KDP-ready interior."""
from pathlib import Path
import fitz
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.utils import ImageReader
from reportlab.lib.pagesizes import letter
from reportlab.lib.colors import black, Color
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
from PIL import Image, ImageOps, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'books/book-001/prototype'
FONT = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
BOLD = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
pdfmetrics.registerFont(TTFont('DejaVu', FONT))
pdfmetrics.registerFont(TTFont('DejaVuBold', BOLD))
STYLE = ParagraphStyle('body', fontName='DejaVu', fontSize=13, leading=19, textColor=black)
SMALL = ParagraphStyle('small', fontName='DejaVu', fontSize=9, leading=13, textColor=black)
BIRDS = [
 ('Northern Cardinal',3,'Find the tall crest, thick short bill and long tail. Circle the crest.', 'Cardinals have a pointed crest and a strong, cone-shaped bill.', 'Sketch a bird\'s head from a safe spot with an adult, or use a reference picture. Is the bill short or long? Circle one. Mark not sure if you cannot see it.', 'Cardinals live in some parts of North America. Check a local range map.', 'Use shape as one clue.'),
 ('Black-capped Chickadee',9,'Find a dark cap, light cheek and dark patch under the bill. Point to each.', 'Look for a dark cap and bib with light cheeks. Similar birds can share these clues.', 'Draw three boxes: cap, cheek, bib. Check each one you can see on a bird or reference picture. Mark not sure if the view is poor.', 'This chickadee occurs in some northern areas. Check a local range map.', 'Use a combination of clues.'),
 ('American Robin',7,'Find the long legs, straight slim bill and rounded belly. Point to the eye and tail.', 'A robin has a warm orange-red breast and a darker head and back. Light can change how colours look.', 'Draw the outline of a bird or a reference picture. Notice its head, breast and legs. Mark not sure when a part is hidden.', 'Where and when robins appear varies. Check a local seasonal map.', 'Record what you see before guessing.')]


def build():
 OUT.mkdir(parents=True, exist_ok=True)
 pdf=OUT/'three-bird-prototype.pdf'
 c=canvas.Canvas(str(pdf), pagesize=letter, pageCompression=1)
 W,H=letter
 def page(bird, number, is_art, cue, fact, activity, regional, outcome):
  left,right=(45,36) if number%2 else (36,45)
  width=W-left-right
  def box(x,y,w,h):
   assert x >= left and y >= 36 and x+w <= W-right and y+h <= H-36, (number,x,y,w,h)
  def text(txt,x,top,w,style=STYLE):
   p=Paragraph(txt,style); _,h=p.wrap(w, H); box(x,top-h,w,h); p.drawOn(c,x,top-h); return top-h
  text('DRAFT PROTOTYPE • FACTS AND ART AWAIT REVIEW',left,H-38,width,SMALL)
  y=text(bird,left,H-62,width,ParagraphStyle('title',parent=STYLE,fontName='DejaVuBold',fontSize=22,leading=28))
  y=text('COLOUR AND IDENTIFY' if is_art else 'EXPLORE AND OBSERVE',left,y-8,width,SMALL)
  if is_art:
   y=text(cue,left,y-16,width)
   x=left+20; bottom=185; w=width-40; h=y-bottom-18; box(x,bottom,w,h)
   if number==3:
    im=ROOT/'books/book-001/assets/test-illustration/northern-cardinal-style-test-2026-11-15.png'
    c.drawImage(ImageReader(str(im)),x,bottom,width=w,height=h,preserveAspectRatio=True,anchor='c',mask='auto')
    text('STYLE TEST ONLY • anatomy and print resolution unapproved',left,160,width,SMALL)
   else:
    c.setStrokeColor(black);c.rect(x,bottom,w,h);text('ILLUSTRATION PLACEHOLDER — no artwork generated',x+12,bottom+h/2,w-24,SMALL)
  else:
   y=text('<b>Notice:</b> '+fact,left,y-22,width)
   y=text('<b>Try it:</b> '+activity,left,y-22,width)
   y=text('<b>Where and when:</b> '+regional,left,y-22,width)
   y=text('<b>Detective skill:</b> '+outcome,left,y-22,width)
   y=text('Draw your observation here:',left,y-28,width)
   box(left,y-190,width,175);c.rect(left,y-190,width,175)
   text('No bird nearby? Use a reference picture. It is okay to be unsure.',left,y-205,width,SMALL)
  text(f'PROTOTYPE • intended book page {number}',left,50,width,SMALL)
  c.showPage()
 for bird,n,cue,fact,act,region,outcome in BIRDS:
  page(bird,n,True,cue,fact,act,region,outcome);page(bird,n+1,False,cue,fact,act,region,outcome)
 c.save()
 doc=fitz.open(pdf)
 assert len(doc)==6
 images=[]
 for page in doc:
  assert abs(page.rect.width-612)<.01 and abs(page.rect.height-792)<.01
  pix=page.get_pixmap(matrix=fitz.Matrix(1,1),alpha=False)
  img=Image.frombytes('RGB',(pix.width,pix.height),pix.samples)
  img.thumbnail((306,396)); images.append(img)
 sheet=Image.new('RGB',(3*326,2*416),'white')
 for i,img in enumerate(images): sheet.paste(img,((i%3)*326+10,(i//3)*416+10))
 sheet.save(OUT/'contact-sheet.png')
 print('Created',pdf,'and contact-sheet.png; six letter pages; content bounds checked.')


if __name__=='__main__': build()
