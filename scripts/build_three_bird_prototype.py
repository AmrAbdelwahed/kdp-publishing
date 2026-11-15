"""Build a six-page facing-spread proof; not a KDP-ready interior."""
from pathlib import Path
import fitz
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'books/book-001/prototype'
pdfmetrics.registerFont(TTFont('DejaVu', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'))
pdfmetrics.registerFont(TTFont('DejaVuBold', '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'))
BODY = ParagraphStyle('body', fontName='DejaVu', fontSize=12, leading=17)
SMALL = ParagraphStyle('small', fontName='DejaVu', fontSize=9, leading=12)
TITLE = ParagraphStyle('title', fontName='DejaVuBold', fontSize=22, leading=28)
HEADING = ParagraphStyle('heading', fontName='DejaVuBold', fontSize=14, leading=19)
BIRDS = [
 {'name':'Northern Cardinal', 'page':2, 'cue':'Look for a crest, a thick bill and a long tail.', 'kind':'cardinal', 'task':'Circle the THREE clue cards that describe the bird on the left.', 'clues':['Crest','Thick bill','Long tail','Webbed feet'], 'observe':'With an adult, look quietly at a bird or a guide. Sketch its head. Is the bill thick or thin?', 'note':'Range varies. Check a local bird guide.', 'skill':'Compare shapes'},
 {'name':'Black-capped Chickadee', 'page':8, 'cue':'Look for a dark cap, pale cheek and dark bib.', 'kind':'chickadee', 'task':'Use the clue cards to label your sketch below.', 'clues':['Cap','Cheek','Bib'], 'observe':'Look at a bird or a guide with an adult. Check what you can see:  cap  /  cheek  /  bib.', 'note':'Similar chickadees can look alike. Check a local guide.', 'skill':'Combine clues'},
 {'name':'American Robin', 'page':6, 'cue':'Look for long legs, a slim bill and a rounded belly.', 'kind':'robin', 'task':'Build a field note: add the missing words from the clue cards.', 'clues':['breast','bill','legs'], 'observe':'Look at a bird or a guide with an adult. Sketch the outline. Mark any hidden parts with a question mark.', 'note':'When and where robins appear varies. Check a local guide.', 'skill':'Record before guessing'}]


def build():
 OUT.mkdir(parents=True, exist_ok=True)
 pdf=OUT/'three-bird-prototype.pdf'
 c=canvas.Canvas(str(pdf), pagesize=letter, pageCompression=1)
 W,H=letter
 def draw_page(bird, activity):
  number=bird['page']+int(activity)
  left,right=(45,36) if number%2 else (36,45)
  width=W-left-right
  def check(x,y,w,h):
   if min(w,h)<0 or x<left or y<36 or x+w>W-right or y+h>H-36:
    raise ValueError(f'Page {number}: object outside safe box: {(x,y,w,h)}')
  def rect(x,y,w,h,radius=0):
   check(x,y,w,h); c.roundRect(x,y,w,h,radius,stroke=1,fill=0)
  def text(value,x,top,w,style=BODY):
   p=Paragraph(value,style); _,h=p.wrap(w, H); check(x,top-h,w,h); p.drawOn(c,x,top-h); return top-h
  text('BIRD DETECTIVES  /  DRAFT - FACTS AND ART AWAIT REVIEW',left,755,width,SMALL)
  text(bird['name'],left,730,width,TITLE)
  text('02  IDENTIFY  +  03  OBSERVE' if activity else '01  COLOUR  +  02  IDENTIFY',left,695,width,HEADING)
  if not activity:
   text(bird['cue'],left,661,width)
   x=left+12; bottom=190; w=width-24; h=435; check(x,bottom,w,h)
   if bird['kind']=='cardinal':
    img=ROOT/'books/book-001/assets/test-illustration/northern-cardinal-style-test-2026-11-15.png'
    c.drawImage(ImageReader(str(img)),x,bottom,width=w,height=h,preserveAspectRatio=True,anchor='c')
    text('STYLE SAMPLE ONLY: anatomy and resolution not approved.',left,168,width,SMALL)
   else:
    rect(x,bottom,w,h,8);text('BIRD ART PLACEHOLDER',x+22,bottom+h/2+15,w-44,HEADING)
    text('Artwork and identification marks await review.',x+22,bottom+h/2-12,w-44,SMALL)
   text('Use a checked reference for colours. It is okay to be unsure.',left,135,width,SMALL)
  else:
   rect(left,535,width,132,9)
   text('CLUE LAB',left+14,652,width-28,HEADING)
   text(bird['task'],left+14,627,width-28)
   if bird['kind']=='cardinal':
    for i,label in enumerate(bird['clues']):
     x=left+14+i*122;rect(x,550,112,35,7);text(label,x+27,574,80,SMALL)
     check(x+6,558,15,16)
     if i==0:
      path=c.beginPath();path.moveTo(x+7,559);path.lineTo(x+12,572);path.lineTo(x+17,559);c.drawPath(path)
     elif i==1:
      path=c.beginPath();path.moveTo(x+7,559);path.lineTo(x+19,566);path.lineTo(x+7,573);path.close();c.drawPath(path)
     elif i==2: c.line(x+7,560,x+19,570);c.line(x+7,564,x+19,574)
     else: text('?',x+8,572,12,SMALL)
   elif bird['kind']=='chickadee':
    # Conceptual cap / cheek / bib shapes, not a species drawing.
    for i,label in enumerate(bird['clues']):
     x=left+14+i*155;rect(x,550,145,35,7);text(label,x+32,574,108,SMALL)
     check(x+7,558,18,18);c.circle(x+16,567,8)
     if i==0: c.line(x+10,572,x+22,572)
     elif i==1: c.circle(x+18,567,3)
     else: c.line(x+12,562,x+20,562)
   else:
    for i,label in enumerate(bird['clues']):
     x=left+14+i*155;rect(x,550,145,35,7);text(label,x+32,574,108,SMALL)
     check(x+7,558,18,18);c.circle(x+16,567,8)
     if i==0: c.arc(x+11,561,x+21,570,180,180)
     elif i==1: c.line(x+19,568,x+25,566)
     else: c.line(x+13,562,x+13,558);c.line(x+19,562,x+19,558)
   rect(left,308,width,207,9)
   text('DETECTIVE MISSION',left+14,500,width-28,HEADING)
   if bird['kind']=='cardinal':
    text('Not every card fits. Draw a line to the part you noticed.',left+14,472,width-28)
    text('My best clue: __________________________________',left+14,425,width-28)
   elif bird['kind']=='chickadee':
    text('Draw a bird head. Add arrows for your three clues.',left+14,472,width-28)
    rect(left+14,329,width-28,110,5)
   else:
    text('I see a rounded __________, a slim __________,',left+14,472,width-28)
    text('and long __________. If hidden, write NOT SURE.',left+14,435,width-28)
    text('Use the clue cards above; then check the bird on the left.',left+14,388,width-28)
   rect(left,115,width,175,9)
   text('OBSERVE OR USE A GUIDE',left+14,276,width-28,HEADING)
   text(bird['observe'],left+14,250,width-28)
   text('NOT SURE  [ ]     NOT SEEN  [ ]',left+14,185,width-28,SMALL)
   text(bird['note'],left+14,158,width-28,SMALL)
  text('DRAFT  /  '+bird['skill']+'  /  intended page '+str(number),left,52,width,SMALL)
  c.showPage()
 for bird in BIRDS:
  draw_page(bird,False);draw_page(bird,True)
 c.save()
 with fitz.open(pdf) as doc:
  if len(doc)!=6: raise ValueError('Expected six pages')
  sheet=Image.new('RGB',(2*326,3*416),'white')
  for i,page in enumerate(doc):
   if abs(page.rect.width-612)>.01 or abs(page.rect.height-792)>.01: raise ValueError('Incorrect trim')
   pix=page.get_pixmap(matrix=fitz.Matrix(1,1),alpha=False)
   img=Image.frombytes('RGB',(pix.width,pix.height),pix.samples);img.thumbnail((306,396))
   sheet.paste(img,((i%2)*326+10,(i//2)*416+10))
  sheet.save(OUT/'contact-sheet.png')
 print('PASS: six 612 × 792 pt pages, mirrored design safe boxes, three facing spreads.')


if __name__=='__main__': build()
