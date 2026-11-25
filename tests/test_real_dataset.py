"""Tests d'intégration sur les quatre exports réels inclus dans le dépôt."""
import csv
import json
import unittest
from collections import Counter
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

class TestCorpusReel(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with (ROOT/'data/merged/raw_bibliographic_dataset.csv').open(encoding='utf-8-sig',newline='') as f:
            cls.rows=list(csv.DictReader(f))

    def test_nombre_et_provenance(self):
        self.assertEqual(len(self.rows),14311)
        self.assertEqual(dict(Counter(r['source'] for r in self.rows)),{
            'Scopus':3751,'WoS':2416,'IEEE':3574,'OpenAlex':4570,
        })

    def test_colonnes_et_donnees_observees(self):
        self.assertEqual(list(self.rows[0]),['id','title','authors','year','source','doi'])
        self.assertEqual(sum(not r['title'].strip() for r in self.rows),0)
        self.assertEqual(sum(not r['year'].strip() for r in self.rows),3)
        self.assertEqual(sum(not r['source'].strip() for r in self.rows),0)

    def test_defis_documentes(self):
        with (ROOT/'results/quality/lab4_defi1_trois_references.csv').open(encoding='utf-8-sig',newline='') as f:
            entries=list(csv.DictReader(f))
        self.assertEqual(len(entries),3)
        self.assertTrue(all(int(row['number_of_sources'])>=3 for row in entries))
        with (ROOT/'results/quality/lab4_defi2_openalex_exclusif.csv').open(encoding='utf-8-sig',newline='') as f:
            challenge=list(csv.DictReader(f))
        self.assertEqual(len(challenge),1)
        self.assertEqual(challenge[0]['source'],'OpenAlex')

if __name__=='__main__':unittest.main()
