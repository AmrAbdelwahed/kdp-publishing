"""Overlay six activity designs on the preserved 64-page review; no artwork is changed."""
from pathlib import Path
import html
import json
import tempfile

import fitz
from PIL import Image, ImageDraw, ImageFont
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph

from build_interior_review import FONT, BOLD

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'books/book-001/interior-8a'
BASE = ROOT / 'books/book-001/interior-review/64-page-interior-REVIEW.pdf'
pdfmetrics.registerFont(TTFont('Detective', FONT))
pdfmetrics.registerFont(TTFont('DetectiveBold', BOLD))


def build():
    activities = json.loads((OUT / 'ACTIVITIES.json').read_text(encoding='utf8'))
    assert len(activities) == 30
    with tempfile.TemporaryDirectory(prefix='bird-8a-') as tmp:
        tmp = Path(tmp)
        c = canvas.Canvas(str(tmp / 'replacement-pages.pdf'), pagesize=(612, 792), pageCompression=1,
                          initialFontName='Detective')

        def para(value, x, top, width, size=12.5, bold=False, height=60):
            style = ParagraphStyle('p', fontName='DetectiveBold' if bold else 'Detective',
                                   fontSize=size, leading=size * 1.32)
            p = Paragraph(html.escape(value), style)
            _, used = p.wrap(width, height)
            if used > height or x < 36 or x + width > 576 or top - used < 36 or top > 756:
                raise ValueError(f'Text outside its reserved area: {value!r}')
            p.drawOn(c, x, top - used)
            return used

        def rounded(x, y, width, height, radius=8):
            if x < 36 or x + width > 576 or y < 36 or y + height > 756:
                raise ValueError('Shape outside safe margins')
            c.setLineWidth(.85)
            c.roundRect(x, y, width, height, radius, fill=0, stroke=1)

        def frame(page, section):
            x = 54 if page % 2 else 45
            c.setLineWidth(.8)
            c.line(x, 752, 612 - (45 if page % 2 else 54), 752)
            para('BIRD DETECTIVES  /  ' + section, x, 747, 445, 9, height=15)
            c.circle(x + 478, 738, 5, stroke=1, fill=0)
            c.line(x + 482, 734, x + 487, 729)
            c.line(x, 58, 612 - (45 if page % 2 else 54), 58)
            para('REVIEW DRAFT  •  ' + str(page), x, 54, 450, 9, height=15)
            return x

        def section_caption(value, x, y):
            c.setLineWidth(1.3)
            c.line(x, y-5, x+21, y-5)
            para(value, x+30, y+2, 400, 10, True, height=15)

        def activity_header(a):
            x = frame(a['page'], 'IDENTIFY  /  OBSERVE')
            para(a['species'], x, 719, 385, 20, True, 55)
            para('CASE '+a['species_id'][1:], x+410, 715, 80, 10, True, 18)
            para(a['title'], x, 678, 420, 12.5, True, 25)
            # Six small original line symbols distinguish the page formats.
            ix, iy = x+458, 670
            c.setLineWidth(1.1)
            if a['format']=='challenge':
                c.circle(ix+8,iy,7,stroke=1,fill=0);c.line(ix+13,iy-5,ix+19,iy-11)
            elif a['format']=='compare':
                c.roundRect(ix,iy-7,10,16,2,stroke=1,fill=0);c.roundRect(ix+14,iy-7,10,16,2,stroke=1,fill=0)
            elif a['format']=='colour':
                c.circle(ix+8,iy,7,stroke=1,fill=0);c.circle(ix+21,iy,7,stroke=1,fill=0)
            elif a['format']=='journal':
                c.roundRect(ix,iy-10,21,22,3,stroke=1,fill=0);c.line(ix+5,iy+4,ix+16,iy+4);c.line(ix+5,iy-1,ix+16,iy-1)
            elif a['format']=='draw':
                c.line(ix+3,iy-8,ix+20,iy+9);c.line(ix+6,iy-10,ix+23,iy+7);c.line(ix+3,iy-8,ix+6,iy-10)
            else:
                c.circle(ix+4,iy,3,stroke=1,fill=0);c.circle(ix+21,iy,3,stroke=1,fill=0);c.line(ix+7,iy,ix+18,iy)
            # A slim ruled clue is common branding; the activity region differs by format.
            c.setLineWidth(2.1);c.line(x, 633, x, 573)
            para('CLUE', x+13, 651, 460, 10, True, 18)
            para(a['fact'], x+13, 631, 465, 12.5, height=63)
            para(a['instruction'], x, 552, 493, 12.5, height=78)
            return x

        def observation(a, x):
            c.setDash(2, 3); c.line(x, 223, x+495, 223);c.setDash()
            para('OPTIONAL  /  LOOK OUT', x, 211, 490, 10, True, height=15)
            para(a['observation'], x, 191, 490, 11.5, height=50)
            c.line(x, 126, x+495, 126)
            para('A note or sketch:', x, 117, 485, 10, height=15)

        def circle_choice(x, y, text, letter, width=460):
            rounded(x, y, width, 48, 8)
            c.setLineWidth(1.1);c.circle(x+23, y+24, 12, stroke=1, fill=0)
            para(letter, x+19, y+30, 20, 9, True, 15)
            para(text, x+45, y+32, width-55, 12, height=36)

        def challenge(a, x):
            section_caption('CIRCLE ONE CLUE', x, 484)
            for i, opt in enumerate(a['options']):
                circle_choice(x, 412-i*62, opt, chr(65+i), 300)
            rounded(x+315, 314, 170, 159, 8)
            para('YOUR BIRD PAGE', x+326, 460, 145, 9.5, True, 16)
            para('Check page 63 after you choose.', x, 239, 480, 10, height=15)

        def pair_cards(a, x):
            # These are labeled conceptual pattern diagrams, not anatomical drawings.
            sid = a['species_id']
            left = x+3; right = x+252
            for pos, option in ((left,a['options'][0]), (right,a['options'][1])):
                rounded(pos, 310, 237, 174, 10)
                para(option, pos+10, 471, 217, 12, True, 38)
            if sid == 'B02':
                for pos, text in ((left,'blue / black / white'), (right,'white / light gray')):
                    for j in range(3):rounded(pos+20+j*62, 358, 52, 44, 3)
                    para(text, pos+16, 345, 205, 10, height=30)
            elif sid == 'B08':
                for idx,pos in enumerate((left,right)):
                    c.circle(pos+94, 392, 13, stroke=1, fill=0)
                    c.circle(pos+94, 392, 3, stroke=1, fill=1)
                    if idx == 0:c.line(pos+55, 419, pos+133, 419)
                    else:c.line(pos+55, 392, pos+81, 392);c.line(pos+107, 392, pos+133, 392)
                    para('above' if idx==0 else 'through',pos+55,365,140,10,height=16)
            elif sid == 'B14':
                for idx,pos in enumerate((left,right)):
                    c.ellipse(pos+52, 358, pos+180, 429, stroke=1, fill=0)
                    if idx == 0:
                        c.line(pos+86, 366, pos+86, 420); c.line(pos+141, 366, pos+141, 420)
                    else:
                        for dx,dy in ((91,381),(121,402),(142,381),(88,405)):c.circle(pos+dx,dy,4,stroke=1,fill=0)
            elif sid == 'B20':
                for idx,pos in enumerate((left,right)):
                    c.arc(pos+53,362,pos+180,425,0,180)
                    c.line(pos+68,388,pos+160,388); c.line(pos+68,398,pos+160,398)
                    para('white stripes' if idx==0 else 'tan stripes',pos+45,370,170,10,height=16)
            elif sid == 'B26':
                for idx,pos in enumerate((left,right)):
                    c.ellipse(pos+55,360,pos+180,427,stroke=1,fill=0)
                    if idx==0:
                        for dx,dy in ((82,386),(109,405),(142,381),(151,406),(107,372)):c.circle(pos+dx,dy,4,stroke=1,fill=0)
                    else:
                        c.line(pos+85,378,pos+151,411);c.line(pos+85,390,pos+135,415)
            para('POSITION KEYS / line colour is not plumage' if sid=='B08' else 'PATTERN KEYS / not bird portraits',x,290,485,9.5,height=15)
            para('Circle A or B. Check page 63.',x,269,485,10,height=15)

        def colour(a, x):
            section_caption('COLOUR THE KEY', x, 483)
            sid=a['species_id']
            if sid=='B09':
                for row in range(2):
                    for col in range(2):
                        xx=x+85+col*110; yy=300+(1-row)*72
                        rounded(xx,yy,100,64,3)
                        colour_name='BLACK' if (row+col)%2==0 else 'WHITE'
                        para(colour_name,xx+10,yy+38,85,11,True,17)
                para('Make a simple pattern key.',x+320,383,160,11,height=50)
            elif sid=='B21':
                para('ADULT',x+10,451,150,11,True,18)
                for j,name in enumerate(('BLACK','WHITE','BLACK','WHITE')):
                    xx=x+10+j*64;rounded(xx,355,58,79,3);para(name,xx+3,400,53,11,True,17)
                rounded(x+307,355,160,79,6);para('YOUNG',x+322,416,130,11,True,18);para('BROWN marks',x+322,388,130,10,height=20)
            else:
                for idx,opt in enumerate(a['options']):
                    xx=x+10+idx*245;rounded(xx,317,230,140,9)
                    if sid=='B27':c.circle(xx+115, 385, 37, stroke=1, fill=0)
                    else:c.circle(xx+115, 387, 32, stroke=1, fill=0)
                    para(opt,xx+10,340,210,11,True,20)
            para('These are colour keys, not bird portraits.',x,271,485,10,height=15)

        def journal(a, x):
            # A clipboard note separates an imaginary case from optional observations.
            rounded(x+16, 289, 463, 194, 7)
            c.line(x+45,449,x+450,449);c.line(x+45,409,x+450,409)
            para('IMAGINARY FIELD NOTE',x+31,470,420,11,True,18)
            para(a['case_note'],x+31,436,410,11.5,height=30)
            para('What can this detective record?',x+31,394,410,11,True,22)
            for i,opt in enumerate(a['options']):
                yy=366-i*24;c.rect(x+34,yy-8,11,11,stroke=1,fill=0)
                para(f'{chr(65+i)}  {opt}',x+53,yy+4,390,12,height=19)
            para('Choose one. Check page 63.',x+20,271,470,10,height=15)

        def draw_key(a, x):
            sid=a['species_id'];rounded(x+3,292,487,190,9)
            para('MAKE YOUR PATTERN KEY',x+18,469,450,10,True,18)
            if sid in ('B05','B11'):
                opts=a['options'];count=len(opts);width=425/count
                for i,opt in enumerate(opts):
                    xx=x+25+i*width;rounded(xx,325,width-8,95,3);para(opt,xx+4,378,width-16,11,True,18)
            elif sid=='B17':
                for i,opt in enumerate(('HEAD','BREAST','TAIL')):
                    xx=x+30+i*145;rounded(xx,335,130,72,6);para(opt,xx+12,379,105,11,True,18)
            elif sid=='B23':
                c.arc(x+145,335,x+345,437,0,180);rounded(x+185,408,120,21,3)
                c.circle(x+245,371,5,stroke=1,fill=1)
                para('crown band',x+25,403,125,10,height=15);para('eye dot',x+25,373,125,10,height=15)
            elif sid=='B29':
                path=c.beginPath();path.moveTo(x+105,342);path.curveTo(x+155,435,x+330,435,x+390,345);path.curveTo(x+300,322,x+190,319,x+105,342);path.close();c.drawPath(path,stroke=1,fill=0)
            para('A pattern key is a clue, not a bird portrait.',x+12,270,470,10,height=16)

        def lab(a, x):
            pairs=[p.split('=',1) for p in a['options']]
            right=[pairs[-1][1]]+[p[1] for p in pairs[:-1]]
            section_caption('DRAW LINES TO MATCH',x,484)
            for i,pair in enumerate(pairs):
                yy=423-i*51;rounded(x+6,yy,177,39,7);rounded(x+310,yy,177,39,7)
                para(f'{i+1}  {pair[0]}',x+17,yy+28,155,12,True,19)
                para(f'{chr(65+i)}  {right[i]}',x+320,yy+28,155,12,True,19)
                c.circle(x+189,yy+19,2,stroke=1,fill=0);c.circle(x+303,yy+19,2,stroke=1,fill=0)
            para('Check your links on page 63.',x,271,485,10,height=15)

        # Page 1: a compact mission map, with observation kept explicitly optional.
        x=frame(1,'START HERE')
        para('Backyard Bird Detectives',x,716,495,24,True,60)
        para('A colour • identify • observe adventure',x,671,490,13,True,30)
        para('Welcome, detective! Each bird has a picture on the left and a clue mission on the right.',x,632,490,13,height=70)
        for i,(number,title,desc) in enumerate((('1','COLOUR','Use any colours, or follow a clue key.'),('2','IDENTIFY','Read the clue and solve a small mission.'),('3','OBSERVE','Look quietly if you wish; NOT SEEN and UNSURE are useful notes.'))):
            yy=480-i*103;rounded(x,yy,495,85,10);c.circle(x+35,yy+43,18,stroke=1,fill=0);para(number,x+30,yy+51,20,13,True,20);para(title,x+68,yy+67,395,12,True,20);para(desc,x+68,yy+44,405,11.5,height=40)
        para('Birds differ by place, season and age. Never disturb a bird or nest; ask an adult before exploring.',x,153,490,11.5,height=60)
        c.showPage()

        renderers={'challenge':challenge,'compare':pair_cards,'colour':colour,'journal':journal,'draw':draw_key,'lab':lab}
        for a in activities:
            x=activity_header(a);renderers[a['format']](a,x);observation(a,x);c.showPage()

        # Page 62: a real or picture observation log, so a child can complete it indoors.
        x=frame(62,'DETECTIVE LOG');para('My observation log',x,718,490,22,True,55)
        para('Look quietly with an adult or study a picture. Mark what you really saw; write UNSURE for hidden clues.',x,674,490,12.5,height=68)
        for i in range(4):
            y=514-i*104;rounded(x,y,495,90,8);para(f'RECORD {i+1}    Real bird  [ ]     Picture  [ ]',x+13,y+73,465,10.5,True,20)
            para('Date / place: _____________________    NOT SEEN  [ ]',x+13,y+50,465,10.5,height=20)
            para('One clue or sketch: __________________________________',x+13,y+27,465,10.5,height=20)
        c.showPage()

        # Page 63: an explicit answer entry for every activity page.
        x=frame(63,'CASE SOLUTIONS');para('Detective answer key',x,718,490,21,True,55)
        para('Check your choice or pattern. For notes and drawings, a careful observation may have more than one good answer.',x,676,490,11.5,height=55)
        for i,a in enumerate(activities):
            col=i//15;row=i%15;xx=x+col*251;top=620-row*30
            para(f"{a['page']}. {a['answer']}",xx,top,238,11.5,height=28)
        para('A hidden clue is not proof. UNSURE is a real detective answer.',x,150,490,10.5,True,30)
        c.showPage()

        # Page 64: digitally clickable species source index plus accessible printed site name.
        x=frame(64,'SOURCES & CREDITS');para('Sources and credits',x,718,490,21,True,55)
        para('Bird clues: Cornell Lab of Ornithology, All About Birds. The digital species names link to the guides. Check local guides for region and season.',x,676,490,10.5,height=58)
        para('allaboutbirds.org/guide/',x,610,490,10,True,18)
        for i,a in enumerate(activities):
            col=i//15;row=i%15;xx=x+col*251;top=590-row*25
            para(f"{a['species_id']}  {a['species']}",xx,top,238,9.5,height=22)
            c.linkURL(a['sources'][0]['url'],(xx,top-13,xx+238,top),relative=0)
        para('Original AI-generated illustrations. DejaVu Sans fonts: Bitstream Vera license; see accompanying font notices.',x,179,490,9.5,height=40)
        para('REVIEW DRAFT — scientific, print and publication approval pending.',x,115,490,9.5,True,25)
        c.showPage();c.save()

        # Reuse previous 64-page PDF as the canonical source for 30 original vector-art pages.
        new_path=tmp/'replacement-pages.pdf'
        with fitz.open(BASE) as base, fitz.open(new_path) as replacement, fitz.open() as doc:
            if len(base)!=64 or len(replacement)!=34:raise ValueError('Unexpected input page count')
            for page in range(1,65):
                if page==1: source,idx=replacement,0
                elif page in (62,63,64):source,idx=replacement,30+page-61
                elif page%2==0:source,idx=base,page-1
                else:source,idx=replacement,1+(page-3)//2
                doc.insert_pdf(source,from_page=idx,to_page=idx)
            # Add small, unchanged vector portraits to the challenge format only.
            manifest=json.loads((ROOT/'books/book-001/interior-review/WORKING_ARTWORK_MANIFEST.json').read_text())['entries']
            by_id={entry['species_id']:entry for entry in manifest}
            for a in activities:
                if a['format'] != 'challenge':continue
                page=doc[a['page']-1]; x=54
                with fitz.open(ROOT/by_id[a['species_id']]['vector_art_pdf']) as art:
                    page.show_pdf_page(fitz.Rect(x+325, 792-444, x+475, 792-326),art,0,keep_proportion=True)
            doc.xref_set_key(doc.pdf_catalog(),'PageLayout','/TwoPageRight')
            doc.save(OUT/'64-page-interior-8a-REVIEW.pdf',deflate=True,garbage=4)
            for name,indices,cols in [('all-pages-contact.png',range(64),8),('activity-pages-contact.png',range(2,62,2),6)]:
                rows=(len(indices)+cols-1)//cols;sheet=Image.new('RGB',(cols*220,rows*298),'white')
                for slot,index in enumerate(indices):
                    pix=doc[index].get_pixmap(matrix=fitz.Matrix(.32,.32),alpha=False)
                    im=Image.frombytes('RGB',(pix.width,pix.height),pix.samples)
                    sheet.paste(im,((slot%cols)*220+12,(slot//cols)*298+12))
                sheet.save(OUT/name)
            # Show six genuinely different activity formats at identical scale.
            sheet=Image.new('RGB',(2*380,6*510),'white');draw=ImageDraw.Draw(sheet)
            f=ImageFont.truetype(FONT,14)
            for i in range(6):
                index=2+2*i
                for col,source in enumerate((base,doc)):
                    pix=source[index].get_pixmap(matrix=fitz.Matrix(.55,.55),alpha=False)
                    im=Image.frombytes('RGB',(pix.width,pix.height),pix.samples)
                    sheet.paste(im,(col*380+20,i*510+35))
                    draw.text((col*380+20,i*510+10),'PREVIOUS' if col==0 else 'REVISED',font=f,fill='black')
            sheet.save(OUT/'previous-versus-revised.png')
    print('Built 64-page review from original art pages and 34 revised pages.')

if __name__ == '__main__':
    build()
