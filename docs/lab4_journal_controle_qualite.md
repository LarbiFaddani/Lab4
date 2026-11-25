# LAB 4 — Contrôle de qualité du dataset et défis pratiques

**Date de contrôle :** 25 novembre 2026  
**Périmètre :** `raw_bibliographic_dataset.csv`, 14 311 notices brutes, sans suppression de doublons.  
**Sujet :** Blockchain-Enabled Trustworthy Federated Learning for Secure and Privacy-Preserving Collaborative AI.

## 1. Audit des métadonnées

| Source | Notices | Titres absents | Années absentes | Auteurs absents | DOI absents | Notices datées 2027 |
|---|---:|---:|---:|---:|---:|---:|
| Scopus | 3 751 | 0 | 0 | 1 | 37 | 39 |
| Web of Science | 2 416 | 0 | 0 | 0 | 30 | 16 |
| IEEE Xplore | 3 574 | 0 | 3 | 2 | 31 | 0 |
| OpenAlex | 4 570 | 0 | 0 | 23 | 121 | 1 |
| **Total** | **14 311** | **0** | **3** | **26** | **219** | **56** |

La colonne `source` est renseignée dans chacune des **14 311 notices**. Trois notices IEEE ont une année vide : la condition « chaque titre et année renseignés » est donc **partiellement satisfaite**. Les années 2027 sont hors de la fenêtre 2020–2026 envisagée et doivent être contrôlées (éventuelle publication anticipée, métadonnée erronée ou filtre mal appliqué). Ne pas les supprimer automatiquement.

La détection des doublons a été exécutée en Python (3 681 groupes DOI répétés, 3 722 groupes de titres normalisés répétés, 52 paires floues selon le script testé) et dans Rayyan (11 039 notices potentielles signalées). La **résolution et la suppression définitives relèvent du LAB 5**. Les nombres des différentes méthodes ne s'additionnent pas et ne mesurent pas la même unité statistique.

## 2. Questions de vérification

**Q1 — Comparaison Scopus / Web of Science.** Scopus a retourné **3 751** références contre **2 416** pour Web of Science, soit **1 335 références supplémentaires** pour Scopus. Cela ne prouve pas qu'une base est « meilleure » : leurs collections de revues, actes de conférences et documents indexés diffèrent. Par ailleurs, les filtres observés ne sont pas complètement harmonisés (Scopus incluait 2020–2027 dans une capture ; WoS 2021–2027), ce qui interdit une comparaison strictement contrôlée.

**Q2 — Raisons des écarts malgré des requêtes similaires.** `TITLE-ABS-KEY` (Scopus) et `TS` (Web of Science) n'interrogent pas exactement les mêmes champs. Les moteurs diffèrent dans le traitement des variantes lexicales, des termes composés, de la ponctuation et des métadonnées. La fréquence de mise à jour, la couverture documentaire, la langue, les types de documents retenus et la disponibilité des résumés influencent également les résultats. Pour une comparaison rigoureuse, il faudrait aligner les dates, les années, la langue et les catégories documentaires, et conserver chaque version de requête.

**Q3 — Métadonnées incomplètes.** Oui : **3 années absentes**, **26 listes d'auteurs absentes**, **219 DOI absents**, ainsi que **56 enregistrements datés de 2027** à vérifier. Les titres et les sources sont complets. La correction doit s'effectuer par vérification des notices d'origine et, au besoin, de la page de l'éditeur / DOI, avec conservation de la donnée brute et journal de corrections. Un DOI manquant n'est pas un motif d'exclusion automatique : utiliser le titre normalisé, l'année et les auteurs pour le rapprochement.

## 3. Défi pratique 1 — Trois références indexées dans au moins trois bases

Les trois exemples suivants figurent dans **les quatre exports** (Scopus, Web of Science, IEEE Xplore, OpenAlex), DOI identique et titre cohérent :

| Titre | DOI | Bases constatées |
|---|---|---|
| Block Hunter: Federated Learning for Cyber Threat Hunting in Blockchain-Based IIoT Networks | `10.1109/tii.2022.3168011` | Scopus ; WoS ; IEEE ; OpenAlex |
| Blockchain-Enabled Secure and Trusted Federated Data Sharing in IIoT | `10.1109/tii.2022.3215192` | Scopus ; WoS ; IEEE ; OpenAlex |
| ChainFL: A Simulation Platform for Joint Federated Learning and Blockchain in Edge/Cloud Computing Environments | `10.1109/tii.2021.3117481` | Scopus ; WoS ; IEEE ; OpenAlex |

Note de qualité : pour les deux derniers articles, OpenAlex affiche respectivement **2022 au lieu de 2023** et **2021 au lieu de 2022** dans les autres sources. Cela illustre pourquoi les années doivent être harmonisées à partir de la publication de référence ; ne pas écraser la donnée d'origine.

## 4. Défi pratique 2 — Présent dans OpenAlex, absent des exports Scopus et WoS

- **Titre :** Blockchain-Based Privacy-Enhancing Federated Learning in Smart Healthcare: A Survey
- **Année OpenAlex :** 2025
- **DOI :** `10.3390/blockchains3010001`
- **Constat :** 1 notice dans OpenAlex et **aucune correspondance par DOI ou titre normalisé** dans les fichiers Scopus et Web of Science fournis. Cet article est donc absent **du corpus extrait**, sans prétendre qu'il est absolument absent des catalogues vivants de ces plateformes.
- **Explication plausible, non vérifiée pour cette revue précise :** couverture distincte des revues, délais d'indexation, différences de champs interrogés ou de filtres, ou métadonnées incompletes.

L'examen automatisé a retrouvé **1 340 notices OpenAlex** sans DOI ni titre normalisé correspondant dans les exports Scopus ou Web of Science. Ce chiffre mesure une absence **dans ces exports** et non une absence totale d'indexation ; il ne représente pas nécessairement 1 340 publications uniques.

## 5. Actions avant LAB 5

1. Vérifier les 3 notices sans année et les 56 notices datées 2027 ; garder une trace des corrections.
2. Conserver les quatre exports originaux, le dataset fusionné, le script et ses résultats.
3. Utiliser les listes de doublons potentiels déjà produites pour préparer LAB 5. Ne pas soustraire les 11 039 résultats Rayyan des 14 311 : ils désignent des *candidats*, pas des exclusions définitives.
4. Ne commencer le screening des titres et résumés (LAB 6) qu'après la déduplication (LAB 5), selon la séquence annoncée.

## 6. Reproductibilité

Depuis le dossier contenant `raw_bibliographic_dataset.csv` :

```bash
python lab4_controle_qualite.py
```

Le script exploite uniquement la bibliothèque standard Python, conserve le fichier brut, génère le contrôle par source, les anomalies, les exemples des deux défis et un rapport JSON. Les résultats sont déterminés par les quatre exports chargés le 24 novembre 2026.
