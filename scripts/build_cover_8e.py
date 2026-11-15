"""Build a KDP-template-aligned REVIEW wrap; low-resolution artwork is not print-ready."""
from pathlib import Path
import json
import fitz
from PIL import Image
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'books/book-001/cover-8e'
TEMPLATE=OUT/'source/KDP-template-original.pdf'
FONT=Path('/usr/share/fonts/truetype/dejavu')
for name,file in [('BirdSans','DejaVuSans.ttf'),('BirdBold','DejaVuSans-Bold.ttf'),('BirdSerif','DejaVuSerif-Bold.ttf')]:
    pdfmetrics.registerFont(TTFont(name,str(FONT/file)))


def template_geometry():
    with fitz.open(TEMPLATE) as d:
        page=d[0];draw=page.get_drawings();rects=[x for x in draw if x['type']=='f']
        bg=rects[0]['rect']; trim=[x['rect'] for x in draw if x['type']=='s' and x['color']==(0.,0.,0.)][0]
        folds=sorted(x['rect'].x0 for x in draw if x['type']=='s' and x['color']==(0.,0.,1.))
        barcode=[x['rect'] for x in rects if x['fill']==(1.,1.,0.)][0]
        assert len(folds)==2 and abs(bg.height-810)<.01 and abs(trim.x0-9)<.01
        return dict(media_width=page.rect.width,width=bg.width,height=bg.height,trim=list(trim),folds=folds,barcode_top_origin=list(barcode))


def centered(c,text,y,font,size,x):
    while pdfmetrics.stringWidth(text,font,size)>546:size-=.25
    c.setFont(font,size);c.drawCentredString(x,y,text)


def build():
    OUT.mkdir(parents=True,exist_ok=True);g=template_geometry()
    (OUT/'TEMPLATE_GEOMETRY.json').write_text(json.dumps(g,indent=2)+'\n')
    # Crop original 8D pixels, without enlargement. The crop still includes detailed
    # notebook, magnifier and binoculars as well as some textured green background.
    with Image.open(ROOT/'books/book-001/cover-8d/B1-background.png') as src:
        src.crop((0,430,1102,1333)).save(OUT/'B1-scene-native-crop.png')
    w,h=g['width'],g['height'];left,right=g['folds']; bx=9;by=9;fx=right
    green=HexColor('#173c2b');cream=HexColor('#fff9e8');gold=HexColor('#e2c473')
    temp=OUT/'wrap-before-inset.pdf'
    c=canvas.Canvas(str(temp),pagesize=(w,h),pageCompression=1,initialFontName='BirdSans')
    c.setTitle('B1 KDP-template-aligned cover — REVIEW ONLY, NOT PRINT READY')
    # Vector foundation continues through bleed and across blank spine.
    c.setFillColor(green);c.rect(0,0,w,h,fill=1,stroke=0)
    # Back: same copy and field-guide panel as 8D. Barcode zone receives background only.
    c.setFillColor(cream);c.roundRect(bx+35,by+35,542,722,18,fill=1,stroke=0)
    c.setFillColor(HexColor('#a64332'));c.setFont('BirdSerif',29)
    c.drawString(bx+65,by+697,'A backyard adventure');c.drawString(bx+65,by+661,'for curious bird detectives')
    c.setFillColor(green);c.setFont('BirdSans',16)
    for i,line in enumerate(['Meet 30 North American birds through coloring','pages and playful identification activities.',
                             'Look for field marks, try an observation challenge,','and discover that birds vary by place and season.']):
        c.drawString(bx+65,by+610-i*25,line)
    c.setFillColor(gold);c.roundRect(bx+65,by+428,482,54,10,fill=1,stroke=0)
    c.setFillColor(green);c.setFont('BirdBold',18);c.drawCentredString(bx+306,by+445,'COLOR  •  IDENTIFY  •  OBSERVE')
    c.setFont('BirdBold',15);c.drawString(bx+65,by+384,'Inside: original black-and-white line art')
    c.setFont('BirdSans',14);c.drawString(bx+65,by+360,'For kids ages 6–9')
    # Front vector background fills the outer bleed; scene remains the low-PPI native crop.
    c.setFillColor(HexColor('#fdf3e0'));c.rect(fx,by+535,w-fx,810-(by+535),fill=1,stroke=0)
    scene_y=by+(1427-1333)*792/1427;scene_h=903*792/1427
    c.drawImage(str(OUT/'B1-scene-native-crop.png'),fx,scene_y,width=612,height=scene_h,mask='auto')
    c.setFillColor(cream);c.roundRect(fx+28,by+535,556,233,14,fill=1,stroke=0)
    c.setFillColor(green);mid=fx+306
    centered(c,'Backyard',by+715,'BirdBold',49,mid);centered(c,'Bird Detectives',by+662,'BirdBold',49,mid)
    centered(c,'Color, Spot & Explore',by+625,'BirdSans',22,mid)
    c.setFillColor(green);c.roundRect(fx+66,by+548,480,62,10,fill=1,stroke=0)
    c.setFillColor(cream);centered(c,'A Coloring & Activity Book',by+582,'BirdBold',21,mid)
    centered(c,'for Kids Ages 6–9',by+557,'BirdBold',20,mid)
    c.setFillColor(cream);c.rect(fx,0,w-fx,by+53,fill=1,stroke=0)
    c.setFillColor(green);centered(c,'30 Birds to Color, Identify & Discover',by+24,'BirdBold',16,mid)
    c.save()
    # Existing B01 source stays vector. Its science and print checks remain pending.
    doc=fitz.open(temp)
    with fitz.open(ROOT/'books/book-001/artwork/candidates/cardinal-revised-review/cardinal-vector-art.pdf') as art:
        doc[0].show_pdf_page(fitz.Rect(bx+65,h-(by+330),bx+225,h-(by+95)),art,0,keep_proportion=True,overlay=True)
    doc.save(OUT/'B1-full-wrap-REVIEW.pdf',garbage=4,deflate=True);doc.close();temp.unlink()
    with fitz.open(OUT/'B1-full-wrap-REVIEW.pdf') as wrap:
        # Trimmed 8.5 x 11-in pages intended for local 100% / Actual Size review.
        proof=fitz.open()
        for x in (right,9):
            p=proof.new_page(width=612,height=792)
            p.show_pdf_page(p.rect,wrap,0,clip=fitz.Rect(x,9,x+612,801),keep_proportion=False)
        proof.set_metadata({'title':'B1 front and back trim previews — REVIEW ONLY'});proof.save(OUT/'front-back-actual-size-REVIEW.pdf',garbage=4,deflate=True);proof.close()
        wrap[0].get_pixmap(matrix=fitz.Matrix(1,1),alpha=False).save(OUT/'B1-wrap-screen-preview.png')
    with fitz.open(OUT/'front-back-actual-size-REVIEW.pdf') as p:
        for i,side in enumerate(('front','back')):
            p[i].get_pixmap(matrix=fitz.Matrix(1.5,1.5),alpha=False).save(OUT/f'B1-{side}-screen-preview.png')
    print('Built template-aligned review wrap and 100%-size previews; raster resolution gate remains open.')

if __name__=='__main__':build()
