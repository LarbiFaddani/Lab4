#!/usr/bin/env python3
"""LAB 4 — Détection reproductible des doublons potentiels (sans suppression).
Usage: python lab4_analyser_doublons.py raw_bibliographic_dataset.csv
Dépendances: bibliothèque standard. rapidfuzz facultatif pour candidats flous.
"""
from __future__ import annotations
import csv, hashlib, json, re, sys, unicodedata
from collections import defaultdict, Counter
from pathlib import Path
from difflib import SequenceMatcher

INPUT = Path(sys.argv[1]) if len(sys.argv)>1 else Path('data/merged/raw_bibliographic_dataset.csv')
OUT = Path(sys.argv[2]) if len(sys.argv)>2 else Path('results/duplicates')
OUT.mkdir(parents=True, exist_ok=True)
STOP = {'the','and','for','with','from','using','based','towards','toward','into','over','under','via','its','their','this','that','of','on','in','to','a','an','by','at','or','de','des','du','la','le','les','et','pour','en','une','un'}

def tidy(s): return ' '.join((s or '').split())
def clean_doi(s):
    s=tidy(s).lower().strip().strip('.,;')
    s=re.sub(r'^https?://(?:dx\.)?doi\.org/', '', s)
    s=re.sub(r'^(?:doi\s*:\s*)+', '', s)
    return s if re.match(r'^10\.\d{4,9}/\S+$',s) else ''
def clean_title(s):
    s=unicodedata.normalize('NFKD',tidy(s).lower())
    s=''.join(c for c in s if not unicodedata.combining(c))
    s=re.sub(r'\\(?:textbackslash|textbf|emph|textit)\b\s*', ' ',s)
    s=re.sub(r'[^\w\s]+',' ',s,flags=re.UNICODE)
    return ' '.join(s.split())
def first_author(s):
    return clean_title(re.split(r';|\|',s or '')[0])
def yearint(s):
    m=re.search(r'\b(?:19|20)\d{2}\b',s or '')
    return int(m.group()) if m else None

def write_csv(name,headers,lines):
    p=OUT/name
    with p.open('w',newline='',encoding='utf-8-sig') as f:
        w=csv.writer(f);w.writerow(headers);w.writerows(lines)
    return str(p)

with INPUT.open(encoding='utf-8-sig',newline='') as f:
    records=list(csv.DictReader(f))
req={'id','title','authors','year','source','doi'}
if not records or not req.issubset(records[0]):
    raise SystemExit(f'Colonnes requises absentes : {sorted(req-set(records[0] if records else []))}')
for i,r in enumerate(records,1):
    r['_line']=i;r['_doi']=clean_doi(r['doi']);r['_title']=clean_title(r['title']);r['_year']=yearint(r['year']);r['_author']=first_author(r['authors'])

by_doi=defaultdict(list);by_title=defaultdict(list)
for i,r in enumerate(records):
    if r['_doi']: by_doi[r['_doi']].append(i)
    if r['_title']: by_title[r['_title']].append(i)

doi_groups={k:v for k,v in by_doi.items() if len(v)>1}
title_groups={k:v for k,v in by_title.items() if len(v)>1}

def render_group(groups,kind):
    for key,idxs in sorted(groups.items(),key=lambda kv:(-len(kv[1]),kv[0])):
        for i in idxs:
            r=records[i]
            yield [kind,key,len(idxs),r['_line'],r['source'],r['year'],r['doi'],r['title'],r['authors']]

write_csv('doublons_doi_exact.csv',['type','cle_normalisee','taille_groupe','ligne_dataset','source','year','doi','title','authors'],render_group(doi_groups,'doi'))
write_csv('doublons_titre_exact.csv',['type','cle_normalisee','taille_groupe','ligne_dataset','source','year','doi','title','authors'],render_group(title_groups,'titre'))

# Regroupement conservateur : DOI commun -> même cluster; titre égal ET années compatibles ET DOI non contradictoires -> même cluster.
parent=list(range(len(records)))
def root(a):
    while parent[a]!=a:
        parent[a]=parent[parent[a]];a=parent[a]
    return a
def union(a,b): parent[root(b)]=root(a)
review=[]
for k,idxs in doi_groups.items():
    for j in idxs[1:]: union(idxs[0],j)
    norm_titles={records[i]['_title'] for i in idxs if records[i]['_title']}
    if len(norm_titles)>1:
        review.append(['meme_doi_titres_differents',idxs[0]+1,idxs[-1]+1,records[idxs[0]]['source'],records[idxs[-1]]['source'],records[idxs[0]]['title'],records[idxs[-1]]['title'],k])
for k,idxs in title_groups.items():
    for pos,a in enumerate(idxs):
        for b in idxs[pos+1:]:
            x,y=records[a],records[b]
            if x['_doi'] and y['_doi'] and x['_doi']!=y['_doi']:
                review.append(['meme_titre_doi_differents',a+1,b+1,x['source'],y['source'],x['title'],y['title'],f"{x['_doi']} | {y['_doi']}"])
            elif x['_year'] is not None and y['_year'] is not None and abs(x['_year']-y['_year'])>1:
                review.append(['meme_titre_annees_eloignees',a+1,b+1,x['source'],y['source'],x['title'],y['title'],f"{x['_year']} | {y['_year']}"])
            else: union(a,b)
clusters=defaultdict(list)
for i in range(len(records)): clusters[root(i)].append(i)
clusters={k:v for k,v in clusters.items() if len(v)>1}
cluster_rows=[]
for seq,idxs in enumerate(sorted(clusters.values(), key=lambda v:min(v)),1):
    for i in idxs:
        r=records[i]
        cluster_rows.append([f'EX{seq:05d}',len(idxs),r['_line'],r['source'],r['year'],r['doi'],r['title'],r['authors']])
write_csv('groupes_doublons_exacts.csv',['groupe','taille_groupe','ligne_dataset','source','year','doi','title','authors'],cluster_rows)

# Candidats flous = propositions A REVOIR, pas fusionnés.
# Blocking via (année, token rare) ; protège contre comparaison quadratique totale.
try:
    from rapidfuzz.fuzz import ratio as rapid_ratio
    def similarity(x,y): return rapid_ratio(x,y)
    matcher='rapidfuzz'
except ImportError:
    def similarity(x,y): return 100*SequenceMatcher(None,x,y).ratio()
    matcher='difflib'

# Exclure les clés exactes et les couples qui portent le même DOI.
by_year=defaultdict(list)
for i,r in enumerate(records):
    if r['_year'] and len(r['_title'])>=25: by_year[r['_year']].append(i)
# Token de 5+ lettres: sélectionner pour chaque document jusqu'à deux tokens parmi les moins fréquents de son année.
blocks=defaultdict(list)
for yr,idxs in by_year.items():
    freq=Counter(t for i in idxs for t in set(records[i]['_title'].split()) if len(t)>=5 and t not in STOP)
    for i in idxs:
        toks={t for t in records[i]['_title'].split() if len(t)>=5 and t not in STOP and freq[t]>=2 and freq[t]<=200}
        chosen=sorted(toks,key=lambda t:(freq[t],t))[:3]
        for t in chosen: blocks[(yr,t)].append(i)

candidates=set()
for ids in blocks.values():
    if len(ids)>200:continue
    for ia,a in enumerate(ids):
        for b in ids[ia+1:]:
            if a!=b:candidates.add((min(a,b),max(a,b)))

fuzzy=[]
for a,b in sorted(candidates):
    x,y=records[a],records[b]
    if x['_title']==y['_title']:continue
    if x['_doi'] and y['_doi'] and x['_doi']==y['_doi']:continue
    # Avoid duplicates due to cross-base DOI contradictions unless manually reviewed
    score=similarity(x['_title'],y['_title'])
    if score>=92:
        fuzzy.append([a+1,b+1,x['source'],y['source'],x['year'],y['year'],x['doi'],y['doi'],round(score,2),x['title'],y['title'],'A_VERIFIER'])
fuzzy.sort(key=lambda r:(-r[8],r[0],r[1]))
write_csv('doublons_flous_a_verifier.csv',['ligne_1','ligne_2','source_1','source_2','annee_1','annee_2','doi_1','doi_2','similarite_pct','titre_1','titre_2','decision'],fuzzy)
write_csv('conflits_a_verifier.csv',['type','ligne_1','ligne_2','source_1','source_2','titre_1','titre_2','details'],review)

report={
 'fichier_entree':INPUT.name,'lignes_entree':len(records),'repartition_sources':dict(Counter(r['source'] for r in records)),
 'doi_absents_ou_non_valides':sum(not r['_doi'] for r in records),
 'groupes_doi_repetes':len(doi_groups),'lignes_dans_groupes_doi':sum(map(len,doi_groups.values())),
 'groupes_titres_repetes':len(title_groups),'lignes_dans_groupes_titres':sum(map(len,title_groups.values())),
 'groupes_exacts_conservateurs':len(clusters),
 'lignes_dans_groupes_exacts':sum(map(len,clusters.values())),
 'excedent_de_lignes_dans_groupes_exacts':sum(len(v)-1 for v in clusters.values()),
 'candidats_flous_a_verifier':len(fuzzy),'conflits_a_verifier':len(review),
 'methode_fuzzy':matcher,'seuil_fuzzy_pct':92,
 'avertissement':'Aucune ligne supprimée. Les groupes exacts sont calculés par DOI ou par titre exact compatible. Les candidats flous et conflits doivent être vérifiés manuellement avant déduplication finale.',
 'fichiers_crees':['doublons_doi_exact.csv','doublons_titre_exact.csv','groupes_doublons_exacts.csv','doublons_flous_a_verifier.csv','conflits_a_verifier.csv']
}
(OUT/'rapport_doublons.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(report,ensure_ascii=False,indent=2))
