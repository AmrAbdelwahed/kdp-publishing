"""Create review-only release candidates from the frozen PDFs; no source is overwritten.

Uses Pillow/LittleCMS with Ghostscript's local sRGB and SWOP CMYK profiles.
The chosen SWOP condition is provisional, not a claim about KDP's printer.
"""
import io
import json
import re
from pathlib import Path

import fitz
import numpy as np
from PIL import Image, ImageCms

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'books/book-001/release-10'
INTERIOR = ROOT / 'books/book-001/woodpecker-revisions/64-page-interior-woodpecker-REVIEW.pdf'
COVER = ROOT / 'books/book-001/preflight-9/selected-cover-full-wrap-CANDIDATE.pdf'
RGB_PROFILE = '/usr/share/color/icc/ghostscript/default_rgb.icc'
CMYK_PROFILE = '/usr/share/color/icc/ghostscript/default_cmyk.icc'
RGB_PATTERN = re.compile(rb'(?<![\w.])([+-]?(?:\d+\.?\d*|\.\d+))\s+([+-]?(?:\d+\.?\d*|\.\d+))\s+([+-]?(?:\d+\.?\d*|\.\d+))\s+(rg|RG)\b')


def split_font_maps(doc):
    """Split oversized bfchar blocks without changing any character mapping."""
    refs = set()
    for page in doc:
        for font in page.get_fonts(full=True):
            kind, value = doc.xref_get_key(font[0], 'ToUnicode')
            if kind == 'xref':
                refs.add(int(value.split()[0]))
    changed = 0
    for ref in refs:
        data = doc.xref_stream(ref)
        def fix(match):
            nonlocal changed
            lines = match.group(2).strip().splitlines()
            if len(lines) != int(match.group(1)):
                raise ValueError(f'Invalid font mapping count in xref {ref}')
            if len(lines) <= 100:
                return match.group(0)
            changed += 1
            chunks = [lines[i:i + 100] for i in range(0, len(lines), 100)]
            return b'\n'.join(str(len(c)).encode() + b' beginbfchar\n' + b'\n'.join(c) + b'\nendbfchar' for c in chunks)
        fixed = re.sub(rb'(\d+) beginbfchar\s*(.*?)\s*endbfchar', fix, data, flags=re.S)
        if fixed != data:
            doc.update_stream(ref, fixed)
    return changed


def clean_document(doc):
    doc.set_metadata({})
    doc.del_xml_metadata()


def build_interior():
    with fitz.open(INTERIOR) as doc:
        assert len(doc) == 64
        # Old vector artwork was deliberately removed from the drawing streams but
        # left in these two resources. Remove the now-unreferenced forms.
        for n in (18, 20):
            page = doc[n - 1]
            assert all(b'/Fm1 Do' not in doc.xref_stream(x) for x in page.get_contents())
            assert doc.xref_get_key(page.xref, 'Resources/XObject/Fm1')[0] == 'xref'
            doc.xref_set_key(page.xref, 'Resources/XObject/Fm1', 'null')
        page = doc[63]
        old = b'(Original AI-generated illustrations. DejaVu Sans fonts: Bitstream Vera license; see accompanying font)Tj T* (notices.)Tj T*'
        new = b'(AI-generated illustrations. Fonts: DejaVu Sans; Bitstream Vera license.)Tj T*'
        matches = [(xref, doc.xref_stream(xref)) for xref in page.get_contents() if old in doc.xref_stream(xref)]
        assert len(matches) == 1 and matches[0][1].count(old) == 1
        doc.update_stream(matches[0][0], matches[0][1].replace(old, new))
        cmaps = split_font_maps(doc)
        clean_document(doc)
        doc.save(OUT / 'interior-release-candidate.pdf', garbage=4, deflate=True)
    return cmaps


def rgb_to_cmyk(rgb, transform):
    # Preserve paper white and neutral black as pure process colors.
    if rgb == (0, 0, 0):
        return (0, 0, 0, 255)
    if rgb == (255, 255, 255):
        return (0, 0, 0, 0)
    return ImageCms.applyTransform(Image.new('RGB', (1, 1), rgb), transform).getpixel((0, 0))


def build_cover():
    rgb = ImageCms.getOpenProfile(RGB_PROFILE)
    cmyk = ImageCms.getOpenProfile(CMYK_PROFILE)
    transform = ImageCms.buildTransformFromOpenProfiles(rgb, cmyk, 'RGB', 'CMYK', renderingIntent=1)
    with fitz.open(COVER) as doc:
        page = doc[0]
        infos = page.get_image_info(xrefs=True)
        assert len(infos) == 1 and (infos[0]['width'], infos[0]['height']) == (4408, 3612)
        ref = infos[0]['xref']
        source = Image.open(io.BytesIO(doc.extract_image(ref)['image'])).convert('RGB')
        assert source.size == (4408, 3612)
        converted = ImageCms.applyTransform(source, transform)
        # Lossless Flate stream, no resampling; ICC profile is used to convert,
        # but not embedded, consistent with KDP's recorded profile guidance.
        doc.update_stream(ref, converted.tobytes(), compress=1)
        doc.xref_set_key(ref, 'ColorSpace', '/DeviceCMYK')
        doc.xref_set_key(ref, 'DecodeParms', 'null')
        streams = set(page.get_contents()) | {x[0] for x in page.get_xobjects()}
        colors = {}
        for stream in streams:
            data = doc.xref_stream(stream)
            if re.search(rb'\b(?:cs|CS|sc|SC|scn|SCN)\b', data):
                raise ValueError(f'Unexpected explicit color-space operator in xref {stream}')
            def replace(match):
                values = tuple(round(float(v) * 255) for v in match.group(1, 2, 3))
                if any(v < 0 or v > 255 for v in values):
                    raise ValueError(f'Invalid RGB operand: {values}')
                result = rgb_to_cmyk(values, transform)
                colors[str(values)] = result
                op = b'k' if match.group(4) == b'rg' else b'K'
                return b' '.join(f'{v / 255:.6f}'.encode() for v in result) + b' ' + op
            changed = RGB_PATTERN.sub(replace, data)
            if changed != data:
                doc.update_stream(stream, changed)
        assert colors and len(colors) == 6, colors
        cmaps = split_font_maps(doc)
        clean_document(doc)
        doc.save(OUT / 'cover-b1-a-cmyk-release-candidate.pdf', garbage=4, deflate=True)
    # Sample the full scene uniformly; compare source RGB to a simulated roundtrip.
    sample = source.resize((551, 452), Image.Resampling.BOX)
    sample_cmyk = ImageCms.applyTransform(sample, transform)
    back_transform = ImageCms.buildTransformFromOpenProfiles(cmyk, rgb, 'CMYK', 'RGB', renderingIntent=1)
    simulated = ImageCms.applyTransform(sample_cmyk, back_transform)
    delta = np.abs(np.asarray(sample, dtype=np.int16) - np.asarray(simulated, dtype=np.int16))
    return dict(vector_rgb8_to_cmyk8=colors, scene_pixels=list(source.size), sampled_pixels=sample.width * sample.height,
                mean_absolute_rgb_channel_change=float(delta.mean()),
                p95_max_channel_change=float(np.percentile(delta.max(axis=2), 95)),
                max_channel_change=int(delta.max()), font_cmaps_split=cmaps)


def build_comparisons():
    result = fitz.open()
    page = result.new_page(width=1240, height=840)
    font = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
    page.insert_font(fontname='DV', fontfile=font)
    clip = fitz.Rect(631.3772, 9, 1243.3772, 801)
    for label, path, x in [('RGB SOURCE', COVER, 4), ('CMYK SWOP CANDIDATE', OUT / 'cover-b1-a-cmyk-release-candidate.pdf', 624)]:
        page.insert_text((x + 8, 24), label + ' — 100% scale', fontsize=11, fontname='DV')
        with fitz.open(path) as source:
            page.show_pdf_page(fitz.Rect(x, 38, x + 612, 830), source, 0, clip=clip, keep_proportion=False)
    result.save(OUT / 'rgb-vs-cmyk-front-comparison.pdf', garbage=4, deflate=True)
    result.close()
    with fitz.open(OUT / 'rgb-vs-cmyk-front-comparison.pdf') as doc:
        doc[0].get_pixmap(matrix=fitz.Matrix(1, 1), alpha=False).save(str(OUT / 'rgb-vs-cmyk-screen.png'))


def build_packet():
    out = fitz.open()
    page = out.new_page(width=612, height=792)
    font = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
    page.insert_font(fontname='DV', fontfile=font)
    text = ('PHYSICAL REVIEW PACKET — NO APPROVAL IMPLIED\n\n'
            'Print at Actual Size / 100% on letter paper.\n'
            'Includes the four priority birds, both woodpeckers, Goldfinch,\n'
            'Junco, Grackle, Mourning Dove, answers, sources and cover.\n'
            'Compare field marks and colouring spaces; inspect small text.\n'
            'Check the cover scene, reconstructed feathers and colour.\n'
            'A letter-size crop cannot test spine, trim or gutter tolerance;\n'
            'those require the KDP Previewer and a physical proof.\n'
            'See PHYSICAL_REVIEW.md for the complete checklist.')
    page.insert_textbox(fitz.Rect(45, 55, 567, 700), text, fontname='DV', fontsize=12, lineheight=1.5)
    sequence = [4, 6, 18, 20, 26, 30, 44, 54, 58, 60]
    with fitz.open(OUT / 'interior-release-candidate.pdf') as interior:
        for n in sequence:
            out.insert_pdf(interior, from_page=n - 1, to_page=n)
        out.insert_pdf(interior, from_page=62, to_page=63)
    # Actual trim-size crops, no automatic scaling. These are review pages,
    # not the single full-wrap cover for KDP.
    with fitz.open(OUT / 'cover-b1-a-cmyk-release-candidate.pdf') as cover:
        for clip in (fitz.Rect(631.3772, 9, 1243.3772, 801), fitz.Rect(9, 9, 621, 801)):
            p = out.new_page(width=612, height=792)
            p.show_pdf_page(p.rect, cover, 0, clip=clip, keep_proportion=False)
    out.xref_set_key(out.pdf_catalog(), 'PageLayout', '/TwoPageRight')
    out.set_metadata({'title': 'Physical review packet — approval pending'})
    out.save(OUT / 'physical-review-packet.pdf', garbage=4, deflate=True)
    out.close()


if __name__ == '__main__':
    OUT.mkdir(parents=True, exist_ok=True)
    interior_maps = build_interior()
    metrics = build_cover()
    build_comparisons()
    build_packet()
    metrics['interior_font_cmaps_split'] = interior_maps
    (OUT / 'color-measurements.json').write_text(json.dumps(metrics, indent=2) + '\n')
    print(json.dumps(metrics, indent=2))
