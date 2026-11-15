"""Build 8B with the existing renderer and derive its answer/copy records from one source."""
from pathlib import Path
import csv
import json
from build_interior_8a import build

OUT=Path(__file__).resolve().parents[1]/'books/book-001/interior-8b'


def build_review():
    activities=json.loads((OUT/'ACTIVITIES.json').read_text(encoding='utf8'))
    fields=['species_id','species','page','format','title','fact','instruction','options','answer','observation',
            'intended_sex_plumage','sources','fact_status','illustration_status','case_note']
    with (OUT/'FINAL_PROPOSED_COPY.csv').open('w',newline='',encoding='utf8') as f:
        w=csv.DictWriter(f,fieldnames=fields,lineterminator='\n');w.writeheader()
        for a in activities:
            row={k:a.get(k,'') for k in fields};row['options']=' | '.join(a['options'])
            row['sources']=' | '.join(s['url']+' ('+s['retrieved_at_utc']+', '+s['section']+')' for s in a['sources'])
            w.writerow(row)
    fields=['species_id','activity_page','format','instruction','answer_on_page_63','coverage_status']
    with (OUT/'ANSWER_KEY_COVERAGE.csv').open('w',newline='',encoding='utf8') as f:
        w=csv.DictWriter(f,fieldnames=fields,lineterminator='\n');w.writeheader()
        for a in activities:
            w.writerow(dict(species_id=a['species_id'],activity_page=a['page'],format=a['format'],
                            instruction=a['instruction'],answer_on_page_63=a['answer'],
                            coverage_status='Option and key checked programmatically; human age and science review pending'))
    report=('# Answer-key coverage\n\nEach activity has a page-63 entry. Choices were reordered without changing '
            'source facts; comparison diagrams move with the corresponding option. Colour and drawing entries are '
            'pattern guidance, not the only acceptable artistic interpretation. Human review remains pending.\n\n'
            '| Page | Format | Key |\n|---:|---|---|\n')
    for a in activities:report+=f"| {a['page']} | {a['format']} | {a['answer']} |\n"
    (OUT/'ANSWER_KEY_COVERAGE.md').write_text(report,encoding='utf8')
    build(OUT,'64-page-interior-8b-REVIEW.pdf',include_glossary=True)


if __name__=='__main__':build_review()
