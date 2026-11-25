# LAB 4 — Collecte systématique des références bibliographiques

**Sujet doctoral :** *Blockchain-Enabled Trustworthy Federated Learning for Secure and Privacy-Preserving Collaborative AI*  
**Auteur :** FADDANI Larbi — Doctorant, ENSA El Jadida (Université Chouaïb Doukkali)  
**Période :** novembre 2026  
**Statut :** collecte et audit LAB 4 réalisés ; déduplication finale reportée au LAB 5.  
**Méthode :** collecte interbases, journal de recherche, export, Zotero, Python, Rayyan, contrôles de qualité, documentation PRISMA 2020.

## 1. Objectif

Constituer et documenter un corpus traçable de références bibliographiques sur Blockchain et Federated Learning pour l'intelligence artificielle collaborative sécurisée. Cinq bases ont été interrogées ; quatre ont fourni des exports bibliographiques. Le dépôt contient les **vrais exports CSV Zotero**, le corpus normalisé, les scripts Python, les tests, les résultats, les défis pratiques et des captures d'écran.

## 2. Résultats réels

| Source | Références présentes dans le corpus | Statut |
|---|---:|---|
| Scopus | 3 751 | Import Zotero et CSV disponibles |
| Web of Science | 2 416 | Import Zotero et CSV disponibles |
| IEEE Xplore | 3 574 | Import Zotero et CSV disponibles |
| OpenAlex | 4 570 | Import Zotero et CSV disponibles |
| ACM Digital Library | 1 559 *résultats affichés* | Export bloqué (Premium requis), **0 référence ajoutée** |
| **Total brut fusionné** | **14 311** | **Aucune déduplication définitive** |

**Attention :** le résultat « 11 039 doublons potentiels Rayyan » n'est pas le nombre de suppressions ni le nombre d'articles uniques. Il appartient au **LAB 5** de valider les rapprochements et de dédupliquer.

### Qualité des données

| Contrôle | Nombre de notices concernées |
|---|---:|
| Titre absent | 0 |
| Année absente | 3 |
| Source absente | 0 |
| Auteur absent | 26 |
| DOI absent ou invalide | 219 |
| Année égale à 2027 | 56 |

La présence de documents datés de 2027 et la non-uniformité des filtres (Scopus 2020–2027, WoS 2021–2027 sur captures) sont des **limites explicites** ; aucune correction silencieuse n'a été apportée aux fichiers originaux.

## 3. Plan du dépôt

```text
LAB4_Blockchain_FL_GitHub_FINAL/
├── README.md
├── requirements.txt
├── data/
│   ├── raw_zotero/                  # 4 CSV d'origine exportés depuis Zotero
│   │   ├── scopus.csv
│   │   ├── wos.csv
│   │   ├── IEEE.csv
│   │   └── openAlex.csv
│   └── merged/
│       └── raw_bibliographic_dataset.csv
├── scripts/
│   ├── fusion_zotero_lab4.py       # Fusion + normalisation, aucune suppression
│   ├── analyser_doublons.py        # DOI, titre, similarité, conflits
│   └── controle_qualite.py         # Complétude, défis 1 et 2
├── tests/
│   └── test_pipeline.py            # Tests unitaires sur cas synthétiques
├── results/
│   ├── rapport_normalisation.json
│   ├── duplicates/                 # Rapports et groupes candidats
│   └── quality/                    # Audit et défis pratiques
├── docs/
│   ├── REQUETES_ET_FILTRES.md
│   ├── METHODOLOGIE.md
│   ├── PREUVES.md
│   ├── RECOMMANDATIONS_LAB5.md
│   ├── Lab4_journal_recherche_5_bases.csv
│   └── lab4_journal_controle_qualite.md
└── evidence/screenshots/           # Captures d'exécution et d'interfaces
```

## 4. Prérequis et exécution (Windows / VS Code)

Python **3.10+** ; les scripts fonctionnent avec la **bibliothèque standard** (pas de `pip install` obligatoire). `rapidfuzz` est optionnel pour accélérer le calcul flou.

```powershell
# Depuis la racine du repository
python -m unittest discover -s tests -v

# 1) Regénérer le dataset de 14 311 références
python scripts/fusion_zotero_lab4.py --dir data/raw_zotero --out data/merged/raw_bibliographic_dataset.csv --report results/rapport_normalisation.json

# 2) Identifier les doublons potentiels SANS les supprimer
python scripts/analyser_doublons.py data/merged/raw_bibliographic_dataset.csv results/duplicates

# 3) Contrôler la qualité et les deux défis
python scripts/controle_qualite.py data/merged/raw_bibliographic_dataset.csv results/quality
```

**Résultats attendus :** les scripts doivent conserver **14 311 lignes**, produire les quatre répartitions par source, identifier les regroupements exacts et les candidats flous et sauvegarder les rapports dans `results/`. Le script de qualité doit produire `lab4_controle_par_base.csv`, `lab4_anomalies_metadonnees.csv`, `lab4_defi1_trois_references.csv`, `lab4_defi2_openalex_exclusif.csv` et `lab4_rapport_controle_qualite.json`.

**Note importante** : les deux scripts de diagnostic ne doivent **pas** produire un dataset dédupliqué ni supprimer de ligne ; le traitement final sera documenté séparément dans le LAB 5.

## 5. Contrôle méthodologique — requêtes et filtres

Trois concepts ont été combinés avec `AND` (Blockchain, Federated Learning, sécurité/vie privée/confiance) et des synonymes avec `OR`. Les syntaxes `TITLE-ABS-KEY` (Scopus), `TS` (WoS), la recherche avancée IEEE/ACM et les filtres OpenAlex ont été étudiés. **Voir [`docs/REQUETES_ET_FILTRES.md`](docs/REQUETES_ET_FILTRES.md)** pour les formulations, dates, nombres, filtres observés et limites. La chaîne exacte exécutée sur chaque interface n'est pas intégralement récupérable depuis les captures actuelles : elle n'est pas présentée comme une preuve parfaite de reproductibilité.

## 6. Déduplication exploratoire

L'analyse Python examine les répétitions de DOI normalisés, les titres normalisés et les titres proches (similarité ; blocage heuristique pour réduire les comparaisons). Des groupes peuvent se chevaucher ; leurs volumes ne s'additionnent pas. Les conflits DOI/titre/année et les propositions floues requièrent une vérification humaine. **Aucun doublon n'a été supprimé dans le LAB 4.**

Zotero : quatre collections vérifiées par captures. Rayyan : import RIS des 14 311 notices, détection de 11 039 entrées signalées comme doublons potentiels, exemple de comparaison manuelle. La résolution automatique en masse est indisponible sans Premium ; la résolution finale aura lieu au LAB 5.

**Exécution vérifiée :** 11 tests automatiques réussis (8 tests unitaires synthétiques et 3 contrôles d’intégration sur les exports réels). Le calcul flou `analyser_doublons.py` produit **48 paires candidates** avec la méthode de blocage et la similarité `difflib` de cet environnement ; une exécution antérieure utilisant une méthode de présélection différente en avait signalé 52. Ces nombres ne sont pas interchangeables.

## 7. Défis pratiques

**Défi 1 — 3 publications dans au moins 3 bases :** les trois DOI ci-dessous sont présents dans **Scopus + WoS + IEEE + OpenAlex** dans le dataset fourni (voir `results/quality/lab4_defi1_trois_references.csv`).

| Publication | DOI | Sources |
|---|---|---|
| Block Hunter: Federated Learning for Cyber Threat Hunting in Blockchain-Based IIoT Networks | `10.1109/tii.2022.3168011` | IEEE, OpenAlex, Scopus, WoS |
| Blockchain-Enabled Secure and Trusted Federated Data Sharing in IIoT | `10.1109/tii.2022.3215192` | IEEE, OpenAlex, Scopus, WoS |
| ChainFL: A Simulation Platform for Joint Federated Learning and Blockchain in Edge/Cloud Computing Environments | `10.1109/tii.2021.3117481` | IEEE, OpenAlex, Scopus, WoS |

**Défi 2 — une référence OpenAlex absente des deux exports Scopus et WoS :**  
*Blockchain-Based Privacy-Enhancing Federated Learning in Smart Healthcare: A Survey* (2025), DOI `10.3390/blockchains3010001`. Absence vérifiée par **DOI et titre normalisé dans les fichiers collectés**, ce qui **ne prouve pas** l'absence générale de la notice dans Scopus/WoS.

## 8. Questions de vérification et résultats

**Q1. Pourquoi Scopus (3 751) ≠ WoS (2 416) ?** Différences de couverture de revues/conférences, délais d'indexation et filtres. Écart observé : **1 335**, mais les fenêtres chronologiques visibles diffèrent ; comparaison non strictement contrôlée.

**Q2. Pourquoi une recherche similaire varie-t-elle ?** Champs `TITLE-ABS-KEY` vs `TS`, moteurs de recherche, métadonnées, variantes lexicales, types de documents et mises à jour d'index.

**Q3. Métadonnées incomplètes ?** Oui : 3 années, 26 auteurs, 219 DOI manquants ; 56 années 2027 à vérifier. Ne pas inventer les valeurs ni exclure les références automatiquement. Tracer toute correction.

**PRISMA 2020 :** les chiffres de collecte bruts peuvent être conservés dans le registre d'identification, mais le nombre de références définitivement éliminées, puis sélectionnées, sera établi aux LAB 5–7. Le total 14 311 **n'est pas** le nombre d'études uniques.

## 9. Vérification / preuves

Exécuter les tests et conserver la sortie du terminal (`results/tests_unittest.txt`). Les captures existantes sont inventoriées dans [`docs/PREUVES.md`](docs/PREUVES.md). Les chiffres déclarés doivent pouvoir être retrouvés dans les fichiers CSV/JSON déposés et les scripts. Les fichiers de test ne sont que des **fixtures synthétiques**, jamais présentés comme résultats de recherche.

## 10. État des livrables / limites

**Terminé :** collecte des quatre bases accessibles, consultation ACM, journal, imports Zotero, fusion, normalisation, détection exploratoire, contrôle qualité, défis documentés, tests de code.  
**À poursuivre :** confirmer ou relancer les filtres harmonisés, retrouver les requêtes exactes de chaque session, compléter les 3 années absentes, vérifier les 56 années 2027, résoudre les conflits de métadonnées et les doublons (LAB 5), screening (LAB 6), PRISMA (LAB 7).

**Données :** consultez [`LICENSE_DATA.md`](LICENSE_DATA.md) avant de publier les exports issus de bases sous abonnement.
