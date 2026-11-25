#!/usr/bin/env python3
"""LAB4: audit reproducible du dataset brut. Ne supprime aucune référence."""
import csv, re, unicodedata, collections, pathlib, json, sys
IN = pathlib.Path(sys.argv[1]) if len(sys.argv)>1 else pathlib.Path('data/merged/raw_bibliographic_dataset.csv')
DIR = pathlib.Path(sys.argv[2]) if len(sys.argv)>2 else pathlib.Path('results/quality')
DIR.mkdir(parents=True, exist_ok=True)
def tidy(x): return re.sub(r'\s+',' ',str(x or '')).strip()
def norm_title(s):
    s=unicodedata.normalize('NFKD',tidy(s).lower())
    s=''.join(c for c in s if not unicodedata.combining(c))
    return tidy(re.sub(r'[^a-z0-9]+',' ',s))
def norm_doi(s):
    s=tidy(s).lower()
    return re.sub(r'^doi:\s*|^https?://(?:dx\.)?doi\.org/','',s).rstrip(' .')
def write(name, cols, rows):
    with (DIR/name).open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=cols); w.writeheader();w.writerows(rows)
with IN.open(encoding='utf-8-sig',newline='') as f: ds=list(csv.DictReader(f))
required=['id','title','authors','year','source','doi']
assert all(c in ds[0] for c in required), 'Champs obligatoires absents'
for i,r in enumerate(ds,2):
    r['_line']=i
    r['_doi']=norm_doi(r['doi'])
    r['_title']=norm_title(r['title'])
by_source=collections.defaultdict(list)
for r in ds: by_source[r['source']].append(r)
qc=[]
for source,items in sorted(by_source.items()):
    qc.append(dict(source=source, count=len(items), missing_id=sum(not tidy(r['id']) for r in items),missing_title=sum(not tidy(r['title']) for r in items),missing_authors=sum(not tidy(r['authors']) for r in items),missing_year=sum(not tidy(r['year']) for r in items), missing_source=sum(not tidy(r['source']) for r in items),missing_doi=sum(not r['_doi'] for r in items), year_2027=sum(tidy(r['year'])=='2027' for r in items),year_outside_2020_2026=sum(not re.fullmatch(r'202[0-6]',tidy(r['year'])) for r in items)))
qcols=['source','count','missing_id','missing_title','missing_authors','missing_year','missing_source','missing_doi','year_2027','year_outside_2020_2026'];write('lab4_controle_par_base.csv',qcols,qc)
anomalies=[]
for r in ds:
    issues=[]
    for k in required:
        if not tidy(r[k]): issues.append('missing_'+k)
    if not re.fullmatch(r'202[0-6]',tidy(r['year'])): issues.append('year_outside_2020_2026_or_missing')
    if issues:
        anomalies.append(dict(csv_line=r['_line'],source=r['source'],title=r['title'],year=r['year'],doi=r['doi'],anomalies='; '.join(issues)))
write('lab4_anomalies_metadonnees.csv',['csv_line','source','title','year','doi','anomalies'],anomalies)
# Un même DOI dans >= 3 bases (preuve forte et reproductible)
groups=collections.defaultdict(list)
for r in ds:
    if r['_doi']: groups[r['_doi']].append(r)
repeated=[]
for doi,rows in groups.items():
    sources=sorted(set(r['source'] for r in rows))
    if len(sources)>=3:
        title=collections.Counter(r['title'] for r in rows).most_common(1)[0][0]
        repeated.append(dict(doi=doi,title=title,sources='; '.join(sources),number_of_sources=len(sources),records=len(rows),years='; '.join(sorted(set(r['year'] for r in rows)))))
repeated.sort(key=lambda r:(-r['number_of_sources'],r['doi']))
write('lab4_references_3_bases_ou_plus.csv',['doi','title','sources','number_of_sources','records','years'],repeated)
# Priorité aux 3 articles pertinents et effectivement présents dans 4 bases.
chosen=['10.1109/tii.2022.3168011','10.1109/tii.2022.3215192','10.1109/tii.2021.3117481']
examples=[r for doi in chosen for r in repeated if r['doi']==doi]
write('lab4_defi1_trois_references.csv',list(examples[0]),examples) if examples else None
# Présence/absence dans les seuls exports, par DOI OU titre normalisé
scopus_wos=[r for r in ds if r['source'] in ('Scopus','WoS')]
other_dois=set(r['_doi'] for r in scopus_wos if r['_doi'])
other_titles=set(r['_title'] for r in scopus_wos if r['_title'])
oa_only=[]
for r in ds:
    if r['source']!='OpenAlex':continue
    if r['_doi'] and r['_doi'] in other_dois:continue
    if r['_title'] and r['_title'] in other_titles:continue
    oa_only.append(dict(title=r['title'],year=r['year'],doi=r['doi'],source=r['source'],id=r['id']))
write('lab4_openalex_absents_scopus_wos.csv',['title','year','doi','source','id'],oa_only)
selected_doi='10.3390/blockchains3010001'
challenge2=next((r for r in oa_only if norm_doi(r['doi'])==selected_doi),None)
if challenge2:
    write('lab4_defi2_openalex_exclusif.csv',list(challenge2),[challenge2])
report={'input_file':IN.name,'total':len(ds),'by_source':qc,'missing_title':sum(not r['title'].strip() for r in ds),'missing_year':sum(not r['year'].strip() for r in ds),'missing_authors':sum(not r['authors'].strip() for r in ds),'missing_doi':sum(not r['_doi'] for r in ds),'missing_source':sum(not r['source'].strip() for r in ds),'year_2027':sum(r['year'].strip()=='2027' for r in ds),'at_least_3_sources_groups_by_doi':len(repeated),'openalex_absent_scopus_wos_by_doi_and_title':len(oa_only),'challenge1':examples,'challenge2':challenge2,'deduplication':'Identification only; no records removed','scope_limitation':'Absence means absent from the provided exported datasets, not necessarily from entire bibliographic databases.'}
(DIR/'lab4_rapport_controle_qualite.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print('TOTAL',len(ds));print('QUALITE',qc);print('>=3 SOURCES DOI',len(repeated));print('OA seulement vs Scopus/WoS',len(oa_only));print('DEFI2',challenge2)
