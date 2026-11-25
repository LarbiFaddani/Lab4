"""Tests unitaires du pipeline LAB4 avec données synthétiques."""
import csv, json, subprocess, sys, tempfile, unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from fusion_zotero_lab4 import canonical_doi, title_key, parse_year, bibliographic_id, build_dataset, INPUTS

class TestNormalisation(unittest.TestCase):
    def test_doi_url(self):
        self.assertEqual(canonical_doi('https://doi.org/10.1109/ABC.2024.123'), '10.1109/abc.2024.123')
    def test_doi_invalide(self):
        self.assertEqual(canonical_doi('inconnu'), '')
    def test_titre_unicode(self):
        self.assertEqual(title_key('  Sécurité : Fédérée! '), 'securite federee')
    def test_year_date(self):
        self.assertEqual(parse_year('', '2023-10-12'), '2023')
    def test_id_partage_doi(self):
        self.assertEqual(bibliographic_id('10.1234/xyz','Un titre','2025','Scopus','1'),bibliographic_id('10.1234/xyz','Autre','2026','WoS','2'))
    def test_id_hash_same_title_year(self):
        self.assertEqual(bibliographic_id('','Titre unique','2024','Scopus','1'),bibliographic_id('','TITRE UNIQUE','2024','WoS','2'))

class TestPipeline(unittest.TestCase):
    def test_fusion_complete_sans_suppression(self):
        with tempfile.TemporaryDirectory() as t:
            t=Path(t)
            for src, name in INPUTS.items():
                with (t/name).open('w',encoding='utf-8',newline='') as f:
                    writer=csv.DictWriter(f,fieldnames=['Title','Author','Publication Year','Date','DOI','Key']);writer.writeheader()
                    writer.writerow({'Title':'Test Federated Learning','Author':'A. Example','Publication Year':'2024','DOI':'10.1234/example','Key':src})
            build_dataset(t,t/'dataset.csv',t/'report.json')
            with (t/'dataset.csv').open(encoding='utf-8-sig',newline='') as f:rows=list(csv.DictReader(f))
            self.assertEqual(len(rows),4)
            self.assertEqual(set(r['source'] for r in rows),set(INPUTS))
            self.assertEqual(len(set(r['id'] for r in rows)),1)
            report=json.loads((t/'report.json').read_text())
            self.assertEqual(report['total_lignes_brutes'],4)
            self.assertEqual(report['groupes_id_repetes'],1)
    def test_detection_sur_fixture(self):
        with tempfile.TemporaryDirectory() as t:
            t=Path(t); raw=t/'dataset.csv';out=t/'output'
            with raw.open('w',encoding='utf-8',newline='') as f:
                w=csv.DictWriter(f,fieldnames=['id','title','authors','year','source','doi']);w.writeheader()
                w.writerows([
                {'id':'1','title':'Sample Article','authors':'X','year':'2024','source':'Scopus','doi':'10.1234/abc'},
                {'id':'2','title':'Sample Article','authors':'X','year':'2024','source':'WoS','doi':'https://doi.org/10.1234/abc'},
                {'id':'3','title':'Distinct Study','authors':'Y','year':'2023','source':'IEEE','doi':''}])
            subprocess.run([sys.executable,str(ROOT/'scripts/analyser_doublons.py'),str(raw),str(out)],check=True,capture_output=True,text=True)
            result=json.loads((out/'rapport_doublons.json').read_text())
            self.assertEqual(result['groupes_doi_repetes'],1)
            self.assertEqual(result['lignes_entree'],3)
            self.assertTrue((out/'doublons_doi_exact.csv').exists())

if __name__=='__main__': unittest.main()
