# Méthodologie — LAB 4

## Définition du corpus
Collecte de documents sur l'intersection Blockchain, Federated Learning, sécurité, confidentialité et confiance. Recherches dans Scopus, Web of Science, IEEE Xplore, ACM DL et OpenAlex. Quatre bases ont permis un export ; ACM a été consultée mais son export était bloqué par l'accès Premium.

## Pipeline reproductible
1. Rechercher et noter équation, date, filtres, effectif affiché et limites.
2. Exporter et sauvegarder sans modifier les originaux.
3. Importer via RIS/BibTeX dans Zotero ; contrôler le nombre de références.
4. Exporter les quatre collections Zotero en CSV (`data/raw_zotero/`).
5. Fusionner et normaliser : `scripts/fusion_zotero_lab4.py` produit six colonnes obligatoires dans `raw_bibliographic_dataset.csv`. `id` est une clé de rapprochement, **pas une clé unique par ligne**.
6. Détecter les groupes de DOI et titres répétés et les candidats flous (script `analyser_doublons.py`), **sans suppression**.
7. Contrôler la complétude et exécuter les deux défis pratiques (`controle_qualite.py`).
8. Importer les fichiers RIS dans Rayyan et comparer les correspondances proposées ; la résolution systématique automatique exige Premium et n'a pas été achevée.

## Contrôles et anomalies
- 14 311 notices : Scopus 3 751, WoS 2 416, IEEE 3 574, OpenAlex 4 570.
- 0 titres manquants ; 3 années manquantes ; 26 auteurs manquants ; 219 DOI absents/non valides ; 0 source vide ; 56 notices datées de 2027.
- Groupes DOI répétés : 3 681 ; groupes de titres répétés : 3 722. La métrique de candidats flous dépend du blocage et du moteur de comparaison ; ne pas assimiler ces métriques au nombre de références à supprimer.
- Rayyan a signalé 11 039 **notices/cas à résoudre** dans ses critères propres. Le processus de résolution n'est pas finalisé.
- Aucun fichier ne prouve l'élimination effective de tous les doublons ni le nombre final d'articles uniques.

## Pourquoi les résultats Scopus et WoS diffèrent ?
Scopus : 3 751 ; WoS : 2 416 ; écart de 1 335. Les bases n'ont pas la même couverture de revues et conférences, la même indexation ni les mêmes politiques d'actualisation. Les requêtes `TITLE-ABS-KEY` et `TS` n'interrogent pas toujours des champs équivalents ; en outre les filtres observés diffèrent. Cet écart n'est donc pas interprétable comme performance d'une base.

## Métadonnées incomplètes
Les trois années IEEE vides et les DOI manquants sont signalés dans le CSV d'anomalies. Les notices doivent être contrôlées avec les fiches éditeurs, DOI et moteurs de bases, en journalisant les corrections. Les notices datées de 2027 doivent être revérifiées avant le screening. L'absence de DOI n'est pas un motif d'exclusion automatique.

## Défis
- **Défi 1** : 3 DOI attestés dans quatre exports (voir `results/quality/lab4_defi1_trois_references.csv` et le détail des groupes).
- **Défi 2** : DOI `10.3390/blockchains3010001` dans OpenAlex mais absent des exports fournis Scopus et WoS **selon DOI et titre normalisé**. Ceci ne signifie pas qu'il est absent de l'intégralité des index Scopus/WoS.

## Limites
- Requêtes d'interface exactes non certifiées par historique sauvegardé ; le journal note la syntaxe candidate et les filtres observés.
- Les sources CSV de ce dépôt sont des exports Zotero, dont certains champs peuvent différer de l'export natif.
- Absence d'export ACM Premium : aucun enregistrement ACM n'a été inventé.
- L'identification des doublons est préparatoire ; la déduplication définitive appartient au LAB 5 et le screening au LAB 6.
