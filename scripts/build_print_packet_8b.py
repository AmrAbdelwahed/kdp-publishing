"""Assemble an actual-size local-print packet from the approved review PDF."""
from pathlib import Path
import tempfile
import fitz
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from build_interior_review import FONT, BOLD

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'books/book-001/interior-8b'
INTERIOR=OUT/'64-page-interior-8b-REVIEW.pdf'
# A cover, then complete even/odd pairs, then the original pages 62–64.
SPREADS=[(2,3),(4,5),(8,9),(18,19),(20,21),(30,31),(44,45),(58,59)]
pdfmetrics.registerFont(TTFont('Packet',FONT))
pdfmetrics.registerFont(TTFont('PacketBold',BOLD))


def line(c,text,x,y,size=11,bold=False):
    c.setFont('PacketBold' if bold else 'Packet',size);c.drawString(x,y,text)


def checkbox(c,text,x,y):
    c.rect(x,y-2,10,10,fill=0,stroke=1);line(c,text,x+18,y,11)


def build():
    with tempfile.TemporaryDirectory(prefix='bird-print-') as tmp:
        cover=Path(tmp)/'cover.pdf';c=canvas.Canvas(str(cover),pagesize=(612,792),pageCompression=1,initialFontName='Packet')
        line(c,'LOCAL PRINT REVIEW',48,735,20,True)
        line(c,'Backyard Bird Detectives / Milestone 8B',48,710,12,True)
        lines=['Print LETTER size at 100% / Actual Size. Turn off Fit or Shrink.',
               'For facing pages: long-edge duplex; this cover is the first right-hand side.',
               'The next pages are complete illustration/activity pairs, in master order.',
               'Keep this cover: it ensures each illustration prints on a left-hand page.',
               'No physical printing, scientific review or KDP approval is assumed.']
        for i,t in enumerate(lines):line(c,t,48,671-i*25,11)
        line(c,'SELECTED BOOK PAGES',48,512,13,True)
        labels=['2–3  Cardinal / clean reference','4–5  Blue Jay / flagged wing','8–9  Chickadee / lookalikes',
                '18–19  Downy / complex wing','20–21  Hairy / comparison note','30–31  Goldfinch / small detail',
                '44–45  Junco / uncertain boundary','58–59  Mockingbird / wingbars',
                '62–64  Observation log, answers, smallest source labels']
        for i,t in enumerate(labels):line(c,t,60,483-i*25,11)
        line(c,'Review-only packet; use the separate review and feedback sheets.',48,190,10)
        c.showPage();c.save()
        with fitz.open(cover) as first,fitz.open(INTERIOR) as original,fitz.open() as packet:
            packet.insert_pdf(first)
            for left,right in SPREADS:packet.insert_pdf(original,from_page=left-1,to_page=right-1)
            packet.insert_pdf(original,from_page=61,to_page=63)
            packet.xref_set_key(packet.pdf_catalog(),'PageLayout','/TwoPageRight')
            packet.save(OUT/'actual-size-print-packet.pdf',deflate=True,garbage=4)

    c=canvas.Canvas(str(OUT/'PRINT_REVIEW_SHEET.pdf'),pagesize=(612,792),pageCompression=1,initialFontName='Packet')
    line(c,'ACTUAL-SIZE PRINT REVIEW',48,741,19,True)
    line(c,'Print at 100%; inspect the packet before making a decision.',48,713,11)
    labels=['Text and small source labels are readable.','Fine lines reproduce cleanly without disappearing.',
            'Colouring spaces are inviting and usable.','Important boundaries are neither broken nor fused.',
            'Inner and outer margins have safe clearance.','Writing and drawing areas are large enough.',
            'Activities and answer choices are clear.','Bird anatomy and identification clues match a checked source.',
            'Overall page quality is appropriate for a child’s book.']
    for i,t in enumerate(labels):checkbox(c,t,50,674-i*38)
    line(c,'Page / issue / suggestion:',48,312,11,True)
    for y in [280,250,220,190,160]:c.line(48,y,564,y)
    line(c,'Reviewer / date (optional): ______________________________',48,105,10)
    line(c,'This is local feedback, not KDP or scientific approval.',48,75,10)
    c.showPage();c.save()

    c=canvas.Canvas(str(OUT/'CHILD_CAREGIVER_FEEDBACK.pdf'),pagesize=(612,792),pageCompression=1,initialFontName='Packet')
    line(c,'BIRD DETECTIVE / TRY-IT SHEET',48,741,18,True)
    line(c,'For a child and caregiver: try a few pages together.',48,714,11)
    line(c,'Age band (optional):   6–7  [ ]     8–9  [ ]     Other  [ ]',48,685,11)
    questions=['Which activity did you like? What made it fun?',
               'Was any word, clue or direction confusing?',
               'Could you find an answer without another website or book?',
               'Was there enough room to colour, draw or write?',
               'Did any bird or marking look unclear? Which page?',
               'What would make the book more fun or easier to use?']
    for i,t in enumerate(questions):
        y=647-i*82;line(c,t,48,y,11,True);c.line(48,y-27,564,y-27);c.line(48,y-49,564,y-49)
    line(c,'Please do not include a child’s name. Feedback has not yet been collected.',48,116,10)
    c.showPage();c.save()
    print('Built a 20-page duplex packet and two one-page feedback sheets.')

if __name__=='__main__':build()
