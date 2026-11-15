"""Build the provisional 64-page interior using the existing PDF/vector tools."""
from pathlib import Path
import csv, json, tempfile, html
import fitz
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT/'books/book-001/interior-review'
FONT='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
BOLD='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
pdfmetrics.registerFont(TTFont('ReviewSans',FONT)); pdfmetrics.registerFont(TTFont('ReviewBold',BOLD))

def build():
    acts=list(csv.DictReader((OUT/'REVISED_ACTIVITY_COPY.csv').open(newline='',encoding='utf-8')))
    entries=json.loads((OUT/'WORKING_ARTWORK_MANIFEST.json').read_text())['entries']
    assert len(acts)==len(entries)==30
    with tempfile.TemporaryDirectory(prefix='interior-review-') as tmp:
        tmp=Path(tmp); c=canvas.Canvas(str(tmp/'layout.pdf'),pagesize=(612,792),pageCompression=1,initialFontName='ReviewSans')
        def paragraph(value,x,top,width,size=12,bold=False,max_height=90):
            style=ParagraphStyle('text',fontName='ReviewBold' if bold else 'ReviewSans',fontSize=size,leading=size*1.38)
            p=Paragraph(html.escape(value),style);_,height=p.wrap(width,max_height)
            if height>max_height: raise ValueError(f'Text overflow: {value}')
            if x<36 or x+width>576 or top-height<36 or top>756: raise ValueError('Text outside safe bounds')
            p.drawOn(c,x,top-height)
        def frame(num,tag):
            x=54 if num%2 else 45
            c.setLineWidth(.8);c.line(x,752,612-(45 if num%2 else 54),752)
            paragraph('BIRD DETECTIVES  /  '+tag,x,747,450,9,max_height=16)
            c.circle(x+478,738,5,stroke=1,fill=0);c.line(x+482,734,x+487,729)
            c.line(x,58,612-(45 if num%2 else 54),58)
            paragraph('REVIEW DRAFT  •  '+str(num),x,54,450,9,max_height=15)
            return x
        def box(x,y,w,h):
            if x<36 or x+w>576 or y<36 or y+h>750:raise ValueError('box outside safe bounds')
            c.setLineWidth(1);c.roundRect(x,y,w,h,9,stroke=1,fill=0)
        x=frame(1,'WELCOME')
        paragraph('Backyard Bird Detectives',x,716,495,25,True,60)
        paragraph('COLOUR  •  IDENTIFY  •  OBSERVE',x,668,490,14,True)
        paragraph('Welcome, detective! Each bird has a picture on the left and a mission on the right. Colour at your own pace, use the clue card, and try the activity.',x,625,490,14,max_height=115)
        paragraph('Birds vary by place, season and age. It is always okay to say NOT SURE. Never disturb a bird or its nest. Ask an adult before exploring outdoors.',x,480,490,13,max_height=110)
        paragraph('What will you notice first?',x,330,490,18,True);box(x,145,490,145)
        c.showPage()
        for i,(a,e) in enumerate(zip(acts,entries)):
            assert a['species_id']==e['species_id']
            n=2+i*2; x=frame(n,'01 COLOUR')
            paragraph(a['species'],x,718,490,21,True,50)
            paragraph('Colour the bird. Look closely at its shape.',x,681,490,12,max_height=30)
            # Artwork is inserted as vector after layout, in this reserved safe region.
            paragraph('Look for the clue on the next page.',x,137,490,10,max_height=20)
            c.showPage(); n+=1;x=frame(n,'02 IDENTIFY  /  03 OBSERVE')
            paragraph(a['species']+'  •  Detective mission',x,718,495,18,True,55)
            box(x,550,495,107);paragraph('CLUE CARD',x+14,640,460,12,True,25)
            paragraph(a['reference_fact'],x+14,613,465,12,max_height=58)
            box(x,270,495,260);paragraph('YOUR MISSION',x+14,512,460,13,True,22)
            paragraph(a['revised_activity_copy'],x+14,486,465,12,max_height=100)
            if i%3==0:
                box(x+15,296,215,95);box(x+260,296,215,95)
            elif i%3==1:
                box(x+15,296,465,95)
            else:
                for y in (375,345,315):c.line(x+18,y,x+477,y)
            box(x,91,495,158);paragraph('OPTIONAL  /  OBSERVE',x+14,232,460,12,True,25)
            paragraph(a['observe_extension'],x+14,207,460,11,max_height=60)
            paragraph('My clue: __________________________________',x+14,140,460,11,max_height=30)
            c.showPage()
        x=frame(62,'FIELD NOTES');paragraph('My observation log',x,718,490,22,True)
        paragraph('With an adult, observe quietly. Use a question mark when you are unsure. You can also record a picture you studied.',x,674,490,12,max_height=80)
        for i in range(5):
            y=530-i*90;box(x,y,495,78);paragraph('Date or place: __________________    Seen / Picture / Unsure',x+12,y+61,470,10,max_height=20);paragraph('Clue or sketch: _________________________________________',x+12,y+35,470,10,max_height=20)
        c.showPage();x=frame(63,'ANSWERS AND NOTES');paragraph('Detective answers',x,718,490,22,True)
        for i,line in enumerate(['Page 43: No. Young White-crowned Sparrows can have different head markings.','Page 49: The Carolina Wren in this picture faces right.','Page 53: The spotted starling represents fresh winter plumage.','Pages 9 and 11: Similar chickadees can need more clues. UNSURE is a useful answer.','Many drawings and observations have more than one good answer. Record what you can see.']):paragraph(line,x,662-i*88,490,12,max_height=65)
        c.showPage();x=frame(64,'SOURCES AND CREDITS');paragraph('Sources and credits',x,718,490,21,True)
        paragraph('Bird identification references: Cornell Lab of Ornithology, All About Birds. Open a listed guide online for regional and seasonal details.',x,678,495,10,max_height=55)
        paragraph('allaboutbirds.org/guide/',x,623,495,10,True,max_height=20)
        for i,(a,e) in enumerate(zip(acts,entries)):
            col=i//15;row=i%15; xx=x+col*250;yy=601-row*29
            label=f"{a['species_id']}  {a['species']}";paragraph(label,xx,yy,235,8.5,max_height=20)
            c.linkURL(a['source_url'],(xx,yy-13,xx+235,yy),relative=0)
        paragraph('Illustrations: original AI-generated artwork; human editorial and scientific review pending.',x,146,495,9,max_height=35)
        paragraph('This interior is a review draft and is not approved for publication.',x,100,495,9,max_height=30)
        c.showPage();c.save()
        with fitz.open(tmp/'layout.pdf') as doc:
            for i,e in enumerate(entries):
                p=doc[1+2*i];path=ROOT/e['vector_art_pdf']
                if not path.is_file():raise FileNotFoundError(path)
                with fitz.open(path) as art:p.show_pdf_page(fitz.Rect(60,150,552,600),art,0,keep_proportion=True)
            doc.xref_set_key(doc.pdf_catalog(),'PageLayout','/TwoPageRight')
            target=OUT/'64-page-interior-REVIEW.pdf';doc.save(target,deflate=True,garbage=4)
            for name,indices,cols in [('all-pages-contact.png',range(64),8),('activity-pages-contact.png',range(2,62,2),6)]:
                rows=(len(indices)+cols-1)//cols;sheet=Image.new('RGB',(cols*204,rows*276),'white')
                for slot,index in enumerate(indices):
                    pix=doc[index].get_pixmap(matrix=fitz.Matrix(.3,.3),alpha=False);im=Image.frombytes('RGB',(pix.width,pix.height),pix.samples);sheet.paste(im,((slot%cols)*204+10,(slot//cols)*276+10))
                sheet.save(OUT/name)
    print('Built provisional 64-page interior and contact sheets.')

if __name__=='__main__':build()
