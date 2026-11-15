"""Build A/B B1 cover comparisons using the frozen 8E layout and 8G PDF helpers."""
from pathlib import Path
import fitz
from PIL import Image,ImageDraw,ImageFont
import build_cover_8e as layout
from build_cover_8g import compact_integrated

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'books/book-001/cover-8h'
A=OUT/'assets/B1-original-realesrgan-x4.png'
B=ROOT/'books/book-001/cover-8g/assets/realesrgan-x4plus-candidate.png'
B_PROOF=ROOT/'books/book-001/cover-8g/reconstructed-front-back-actual-size-REVIEW.pdf'
OLD_PROOF=ROOT/'books/book-001/cover-8f/front-back-actual-size-REVIEW.pdf'
FONT=Path('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf')
CLIPS=[
 ('Crest, face and bill',fitz.Rect(215,275,485,475)),
 ('Wing, tail, legs and feet',fitz.Rect(120,380,500,650)),
 ('Magnifier and notebook',fitz.Rect(90,270,520,520)),
 ('Binoculars and lower edge',fitz.Rect(295,500,590,705)),
 ('Original-scene tile junction',fitz.Rect(235,385,405,575)),
]


def details(first_path,second_path,first_label,second_label,destination):
    out=fitz.open()
    with fitz.open(first_path) as first,fitz.open(second_path) as second:
        for title,clip in CLIPS:
            page=out.new_page(width=612,height=792);page.insert_font(fontname='dejavu',fontfile=str(FONT))
            page.insert_text((28,28),title+' — trim-region comparison, 100% scale',fontname='dejavu',fontsize=12)
            for label,source,top in [(first_label,first,58),(second_label,second,420)]:
                page.insert_text((35,top-9),label,fontname='dejavu',fontsize=10)
                page.show_pdf_page(fitz.Rect(35,top,35+clip.width,top+clip.height),source,0,clip=clip,keep_proportion=False)
            page.insert_text((28,778),'Same physical page region; print Actual Size. Review only.',fontname='dejavu',fontsize=9)
    out.set_metadata({'title':'Actual-size B1 detail comparison — REVIEW ONLY'})
    out.save(destination,garbage=4,deflate=True);out.close()


def build():
    with Image.open(A) as im:
        if im.size!=(4408,3612):raise ValueError('Expected a 4× reconstruction of the 1102 × 903 source')
    with Image.open(B) as im:
        if im.size!=(5544,4540):raise ValueError('Unexpected 8G candidate dimensions')
    layout.OUT=OUT;layout.build(scene_path=A)
    for filename in ('B1-full-wrap-REVIEW.pdf','front-back-actual-size-REVIEW.pdf'):
        compact_integrated(OUT/filename,A)
    (OUT/'B1-full-wrap-REVIEW.pdf').replace(OUT/'A-full-wrap-REVIEW.pdf')
    (OUT/'front-back-actual-size-REVIEW.pdf').replace(OUT/'A-front-back-actual-size-REVIEW.pdf')
    # Side-by-side native-size fronts, with labels in a separate top strip.
    wide=fitz.open();page=wide.new_page(width=1240,height=840);page.insert_font(fontname='dejavu',fontfile=str(FONT))
    with fitz.open(OUT/'A-front-back-actual-size-REVIEW.pdf') as a,fitz.open(B_PROOF) as b:
        for label,src,x in [('A — original B1 reconstruction',a,4),('B — new-scene reconstruction',b,624)]:
            page.insert_text((x+8,24),label,fontname='dejavu',fontsize=12)
            page.show_pdf_page(fitz.Rect(x,38,x+612,830),src,0,keep_proportion=False)
    wide.set_metadata({'title':'B1 front covers A and B, actual trim size, review only'})
    wide.save(OUT/'full-size-front-comparison-REVIEW.pdf',garbage=4,deflate=True);wide.close()
    details(OLD_PROOF,OUT/'A-front-back-actual-size-REVIEW.pdf','A source at original sampling','A: Real-ESRGAN 4×',OUT/'A-source-vs-reconstruction-details.pdf')
    details(OUT/'A-front-back-actual-size-REVIEW.pdf',B_PROOF,'A: original B1 reconstruction','B: replacement-scene reconstruction',OUT/'A-vs-B-actual-size-details.pdf')
    # A and B previews both use the same 185-pixel thumbnail width.
    with fitz.open(B_PROOF) as b:
        pix=b[0].get_pixmap(matrix=fitz.Matrix(1.5,1.5),alpha=False)
        b_img=Image.frombytes('RGB',(pix.width,pix.height),pix.samples)
    with Image.open(OUT/'B1-front-screen-preview.png') as a_img:a_img=a_img.convert('RGB')
    out=Image.new('RGB',(540,340),'#f3f2ec');d=ImageDraw.Draw(out);font=ImageFont.truetype(str(FONT),17)
    for i,(name,im) in enumerate([('A: Original B1',a_img),('B: New scene',b_img)]):
        im.thumbnail((185,240),Image.Resampling.LANCZOS);x=35+i*255;d.text((x,8),name,font=font,fill='#173c2b');out.paste(im,(x,36))
    d.text((35,308),'185 px wide • review simulation',font=font,fill='#173c2b');out.save(OUT/'thumbnail-comparison.png')
    print('Built A cover, full-size A/B fronts, thumbnails and actual-size detail comparisons.')

if __name__=='__main__':build()
