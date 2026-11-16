"""Prepare human-review candidates from the selected cover and audited 8B interior."""
from pathlib import Path
import hashlib
import json
import shutil
import tempfile
import fitz
from reportlab.lib.colors import black
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from build_interior_review import FONT, BOLD

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'books/book-001/preflight-9'
PREV=ROOT/'books/book-001/interior-8b'
COVER=ROOT/'books/book-001/cover-8h'
ART=(4,6,18,20,26,30,44,54,58,60)
pdfmetrics.registerFont(TTFont('P9',FONT));pdfmetrics.registerFont(TTFont('P9Bold',BOLD))


def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()


def text(c,s,x,y,size=11,bold=False):
    c.setFont('P9Bold' if bold else 'P9',size);c.drawString(x,y,s)


def build():
    OUT.mkdir(parents=True,exist_ok=True)
    # Preserve the review interior; remove internal draft labels from a separate candidate.
    with fitz.open(PREV/'64-page-interior-8b-REVIEW.pdf') as doc:
        if len(doc)!=64:raise ValueError('Expected 64 review pages')
        for i,page in enumerate(doc):
            all_spans=[s for b in page.get_text('dict')['blocks'] for l in b.get('lines',[]) for s in l['spans']]
            spans=[s for s in all_spans if 'REVIEW DRAFT' in s['text']]
            if len(spans)!=(2 if i==63 else 1):raise ValueError(f'Unexpected review labels on page {i+1}')
            foot=[s for s in spans if s['text']==f'REVIEW DRAFT • {i+1}']
            if len(foot)!=1:raise ValueError(f'Unexpected footer on page {i+1}')
            source_lines=[]
            if i==63:
                original=['Bird clues: Cornell Lab of Ornithology, All About Birds. The digital species names link to the',
                          'guides. Check local guides for region and season.']
                source_lines=[next(s for s in all_spans if s['text']==value) for value in original]
                links=page.get_links()
                if len(links)!=30:raise ValueError('Expected 30 source links in the review draft')
                for link in links:page.delete_link(link)
            for s in spans+source_lines:page.add_redact_annot(fitz.Rect(s['bbox']),fill=False,cross_out=False)
            page.apply_redactions(images=0,graphics=0,text=0)
            page.insert_font(fontname='P9Sans',fontfile=FONT)
            page.insert_text(foot[0]['origin'],str(i+1),fontsize=9,fontname='P9Sans')
            if source_lines:
                replacement=['Bird clues: Cornell Lab of Ornithology, All About Birds.',
                             'Find each bird by name; check local guides for region and season.']
                for old,new in zip(source_lines,replacement):
                    page.insert_text(old['origin'],new,fontsize=10.5,fontname='P9Sans')
        doc.subset_fonts();doc.set_metadata({'title':'Backyard Bird Detectives — interior candidate, human review pending'})
        doc.save(OUT/'interior-candidate-REVIEW.pdf',garbage=4,deflate=True)
    # This is byte-for-byte the user's visually selected A review wrap, not a fresh render.
    wrap=COVER/'A-full-wrap-REVIEW.pdf';shutil.copyfile(wrap,OUT/'selected-cover-full-wrap-CANDIDATE.pdf')
    with fitz.open(COVER/'A-front-back-actual-size-REVIEW.pdf') as src,fitz.open() as front:
        front.insert_pdf(src,from_page=0,to_page=0);front.set_metadata({'title':'Selected A cover front — actual-size review'})
        front.save(OUT/'selected-cover-front-actual-size.pdf',garbage=4,deflate=True)
    source_scene=ROOT/'books/book-001/cover-8f/B1-scene-native-crop.png'
    model_scene=COVER/'assets/B1-original-realesrgan-x4.png'
    template=ROOT/'books/book-001/cover-8e/source/KDP-template-original.pdf'
    manifest={'selected':'A — original B1 scene reconstructed with Real-ESRGAN x4plus',
        'user_decision':'Visual direction approved; no scientific, print, rights, upload or publication approval.',
        'source_scene':str(source_scene.relative_to(ROOT)),'source_scene_sha256':sha(source_scene),
        'selected_scene':str(model_scene.relative_to(ROOT)),'selected_scene_sha256':sha(model_scene),
        'source_wrap':str(wrap.relative_to(ROOT)),'source_wrap_sha256':sha(wrap),
        'candidate_wrap':'selected-cover-full-wrap-CANDIDATE.pdf','candidate_wrap_sha256':sha(OUT/'selected-cover-full-wrap-CANDIDATE.pdf'),
        'template':str(template.relative_to(ROOT)),'template_sha256':sha(template),
        'scene_native_pixels':[1102,903],'model_output_pixels':[4408,3612],
        'effective_output_ppi':[518.59,518.91],'native_detail_ppi':[129.65,129.73],
        'human_scientific_approval':False,'human_print_approval':False,'publication_approval':False,
        'open_gates':['AI reconstruction detail','scientific anatomy','artwork and font rights','color handling','template MediaBox mismatch','physical print and KDP Previewer']}
    (OUT/'COVER_SELECTION.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf8')
    with tempfile.TemporaryDirectory(prefix='bird-m9-') as tmp:
        path=Path(tmp)/'cover.pdf';c=canvas.Canvas(str(path),pagesize=(612,792),pageCompression=1,initialFontName='P9')
        text(c,'LOCAL PRINT REVIEW — MILESTONE 9',48,740,18,True)
        text(c,'LETTER • 100% / Actual Size • no Fit or Shrink',48,712,11,True)
        text(c,'Print duplex, long-edge binding; keep this cover as the first right-hand page.',48,687,11)
        text(c,'Each illustration then sits on the left, with its activity on the right.',48,666,11)
        text(c,'This packet is for review; no expert, physical or KDP approval is assumed.',48,645,10)
        text(c,'FLAGGED PAIRS AND SUPPORTING PAGES',48,598,12,True)
        labels=['4–5 Blue Jay','6–7 American Robin','18–19 Downy Woodpecker','20–21 Hairy Woodpecker',
                '26–27 Mourning Dove / thin-line screen','30–31 American Goldfinch','44–45 Dark-eyed Junco','54–55 Common Grackle',
                '58–59 Northern Mockingbird','60–61 Eastern Bluebird','62–64 Log, answer key and source notes']
        for i,label in enumerate(labels):text(c,label,65,570-i*28,11)
        text(c,'Print the selected A cover front separately at 100%.',48,235,11,True)
        text(c,'Record real observations on the review sheet; do not infer KDP approval.',48,210,10)
        c.showPage();c.save()
        with fitz.open(path) as cover,fitz.open(OUT/'interior-candidate-REVIEW.pdf') as interior,fitz.open() as packet:
            packet.insert_pdf(cover)
            for n in ART:packet.insert_pdf(interior,from_page=n-1,to_page=n)
            packet.insert_pdf(interior,from_page=61,to_page=63)
            packet.xref_set_key(packet.pdf_catalog(),'PageLayout','/TwoPageRight')
            packet.set_metadata({'title':'24-page interior local print packet — review only'})
            packet.save(OUT/'interior-print-packet-100-percent.pdf',garbage=4,deflate=True)
    c=canvas.Canvas(str(OUT/'physical-review-checklist.pdf'),pagesize=(612,792),pageCompression=1,initialFontName='P9')
    text(c,'PHYSICAL REVIEW — NO APPROVAL ASSUMED',48,742,17,True)
    text(c,'Use the separate cover and 24-page interior packet at 100% / Actual Size.',48,715,10)
    checks=['Measure 8.5 × 11 in; note printer clipping and print settings.',
        'Cover: type readable; color, reconstructed detail and edge cropping acceptable.',
        'Cover: inspect cardinal crest, bill, mask, feet, feather artifacts and seams.',
        'Text and source notes legible; inner and outer margins have clearance.',
        'Fine lines survive, especially the dove; mark gaps and fused borders.',
        'Downy and Hairy: review mismatch between wing pattern and activity clues.',
        'Jay, Robin, Goldfinch, Junco, Mockingbird and Bluebird: inspect flagged clues.',
        'Grackle eye: is the light iris ring visible and colorable at printed size?',
        'Complete activities with a child/caregiver; note unclear instructions and spaces.',
        'Review colors, trim, barcode placement and binding on a later KDP proof.']
    for i,line in enumerate(checks):
        y=680-i*37;c.rect(48,y-2,10,10,fill=0,stroke=1);text(c,line,66,y,9.5)
    text(c,'Page / observation / decision:',48,286,11,True)
    for y in (255,225,195,165,135):c.line(48,y,564,y)
    text(c,'Reviewer and date (optional): ______________________________________',48,96,10)
    text(c,'This sheet records real feedback, not automatic KDP or scientific approval.',48,68,9)
    c.setFillColor(black);c.showPage();c.save()
    print('Built 64-page interior candidate, selected cover and 24-page review packet.')

if __name__=='__main__':build()
