"""Build two screen-review cover directions; not a KDP cover generator."""
from pathlib import Path
import fitz
from PIL import Image, ImageDraw, ImageFont
from reportlab.lib.colors import HexColor, Color
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'books/book-001/cover-8d'
FONTS = Path('/usr/share/fonts/truetype/dejavu')
pdfmetrics.registerFont(TTFont('CoverSans', str(FONTS/'DejaVuSans.ttf')))
pdfmetrics.registerFont(TTFont('CoverBold', str(FONTS/'DejaVuSans-Bold.ttf')))
pdfmetrics.registerFont(TTFont('CoverSerif', str(FONTS/'DejaVuSerif-Bold.ttf')))
W, H = 612, 792
GREEN = HexColor('#173c2b')
GOLD = HexColor('#f3ca5d')
CREAM = HexColor('#fff9e8')


def center(c, text, y, font, size, color=GREEN):
    while pdfmetrics.stringWidth(text, font, size) > 546:
        size -= .25
    c.setFillColor(color); c.setFont(font, size); c.drawCentredString(W/2, y, text)


def front(which):
    c = canvas.Canvas(str(OUT/f'{which}-front-review.pdf'), pagesize=(W,H), pageCompression=1)
    c.setTitle(f'{which} front cover — REVIEW DRAFT, not print-ready')
    c.drawImage(str(OUT/f'{which}-background.png'), 0, 0, W, H)
    c.setFillColor(CREAM); c.roundRect(28, 535, W-56, 233, 14, fill=1, stroke=0)
    title_font = 'CoverBold' if which == 'B1' else 'CoverSerif'
    center(c, 'Backyard', 715, title_font, 49)
    center(c, 'Bird Detectives', 662, title_font, 49)
    center(c, 'Color, Spot & Explore', 625, 'CoverSans', 22)
    c.setFillColor(GREEN if which == 'B1' else HexColor('#d9b15f'))
    c.roundRect(66, 548, W-132, 62, 10, fill=1, stroke=0)
    color = CREAM if which == 'B1' else GREEN
    center(c, 'A Coloring & Activity Book', 582, 'CoverBold', 21, color)
    center(c, 'for Kids Ages 6–9', 557, 'CoverBold', 20, color)
    c.setFillColor(CREAM); c.rect(0, 0, W, 53, fill=1, stroke=0)
    center(c, '30 Birds to Color, Identify & Discover', 24, 'CoverBold', 16)
    c.save()


def back():
    c = canvas.Canvas(str(OUT/'back-cover-review.pdf'), pagesize=(W,H), pageCompression=1)
    c.setTitle('Back cover — REVIEW DRAFT, not print-ready')
    c.setFillColor(GREEN); c.rect(0,0,W,H,fill=1,stroke=0)
    c.setFillColor(CREAM); c.roundRect(35,35,542,722,18,fill=1,stroke=0)
    c.setFillColor(HexColor('#a64332'));c.setFont('CoverSerif',29)
    c.drawString(65,697,'A backyard adventure')
    c.drawString(65,661,'for curious bird detectives')
    c.setFillColor(GREEN);c.setFont('CoverSans',16)
    for i,line in enumerate(['Meet 30 North American birds through coloring', 'pages and playful identification activities.', 'Look for field marks, try an observation challenge,', 'and discover that birds vary by place and season.']):
        c.drawString(65,610-i*25,line)
    c.setFillColor(HexColor('#e2c473'));c.roundRect(65,428,482,54,10,fill=1,stroke=0)
    c.setFillColor(GREEN);c.setFont('CoverBold',18);c.drawCentredString(W/2,445,'COLOR  •  IDENTIFY  •  OBSERVE')
    c.setFont('CoverBold',15);c.drawString(65,384,'Inside: original black-and-white line art')
    c.setFont('CoverSans',14);c.drawString(65,360,'For kids ages 6–9')
    # Conceptual placeholder only; official template defines the final location and dimensions.
    c.setStrokeColor(HexColor('#9a9a9a'));c.setFillColor(HexColor('#ffffff'));c.rect(315,75,226,100,fill=1,stroke=1)
    c.setFillColor(HexColor('#777777'));c.setFont('CoverSans',11);c.drawCentredString(428,120,'BARCODE AREA — PLACEHOLDER')
    c.setFont('CoverSans',9);c.drawCentredString(W/2,50,'REVIEW DRAFT  •  Barcode placement and print layout not approved')
    c.save()
    # Insert the selected original vector art as a small, clearly identified interior preview.
    path=OUT/'back-cover-review.pdf'; doc=fitz.open(path)
    with fitz.open(ROOT/'books/book-001/artwork/candidates/cardinal-revised-review/cardinal-vector-art.pdf') as art:
        doc[0].show_pdf_page(fitz.Rect(65, H-330, 225, H-95),art,0,keep_proportion=True,overlay=True)
    doc.save(OUT/'back-cover-review-tmp.pdf',garbage=4,deflate=True);doc.close()
    (OUT/'back-cover-review-tmp.pdf').replace(path)


def previews():
    for n in ('B1','B2'):
        with fitz.open(OUT/f'{n}-front-review.pdf') as doc:
            pix=doc[0].get_pixmap(matrix=fitz.Matrix(1.8,1.8),alpha=False)
            pix.save(OUT/f'{n}-front-preview.png')
    with fitz.open(OUT/'back-cover-review.pdf') as doc:
        doc[0].get_pixmap(matrix=fitz.Matrix(1.5,1.5),alpha=False).save(OUT/'back-cover-preview.png')
    sheet=Image.new('RGB',(540,340),'#f1f0e9');draw=ImageDraw.Draw(sheet)
    f=ImageFont.truetype(str(FONTS/'DejaVuSans-Bold.ttf'),20)
    s=ImageFont.truetype(str(FONTS/'DejaVuSans.ttf'),13)
    for i,n in enumerate(('B1','B2')):
        im=Image.open(OUT/f'{n}-front-preview.png').convert('RGB');im.thumbnail((185,240),Image.Resampling.LANCZOS)
        x=35+255*i;draw.text((x,10),n,font=f,fill='#173c2b');sheet.paste(im,(x,38));draw.text((x,287),'185 px wide',font=s,fill='#173c2b')
    draw.text((35,318),'Screen simulation • not an Amazon listing',font=s,fill='#173c2b')
    sheet.save(OUT/'thumbnail-comparison.png')
    # A conceptual arrangement, with arbitrary spine width and barcode placeholder.
    wrap=fitz.open(); page=wrap.new_page(width=1304,height=872)
    page.insert_text((40,34),'REVIEW ONLY — NOT TO SCALE — OFFICIAL KDP TEMPLATE REQUIRED',fontsize=18,color=(.55,.1,.1))
    with fitz.open(OUT/'back-cover-review.pdf') as doc: page.show_pdf_page(fitz.Rect(40,55,652,847),doc,0)
    page.draw_rect(fitz.Rect(652,55,662,847),color=(.10,.22,.16),fill=(.10,.22,.16))
    with fitz.open(OUT/'B1-front-review.pdf') as doc: page.show_pdf_page(fitz.Rect(662,55,1274,847),doc,0)
    wrap.set_metadata({'title':'Conceptual wrap preview — NOT TO SCALE — NO KDP TEMPLATE'});wrap.save(OUT/'provisional-wrap-NOT-TO-SCALE.pdf',deflate=True,garbage=4);wrap.close()
    with fitz.open(OUT/'provisional-wrap-NOT-TO-SCALE.pdf') as doc:doc[0].get_pixmap(matrix=fitz.Matrix(1,1),alpha=False).save(OUT/'provisional-wrap-preview.png')


if __name__ == '__main__':
    OUT.mkdir(parents=True,exist_ok=True)
    for version in ('B1','B2'):front(version)
    back();previews()
