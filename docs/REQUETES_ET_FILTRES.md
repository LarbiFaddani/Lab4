# Journal des requêtes, filtres et limites de reproductibilité

**Sujet** : Blockchain-Enabled Trustworthy Federated Learning for Secure and Privacy-Preserving Collaborative AI.  
**Période des collectes observées** : 22–24 novembre 2026.  
Les chaînes ci-dessous sont des **formulations de travail reconstruites** d'après la stratégie utilisée, **pas des copier-coller certifiés de chaque session**. Les traces des interfaces et le journal `Lab4_journal_recherche_5_bases.csv` prévalent pour les filtres réellement observés. Ne pas présenter ces requêtes comme identiques aux recherches exécutées sans vérifier les historiques de recherche.

## Stratégie commune

```text
("blockchain" OR "distributed ledger")
AND ("federated learning" OR "federated machine learning")
AND ("security" OR "privacy" OR "trust" OR "data integrity" OR "poisoning attack")
```

| Base | Syntaxe candidate | Filtres observés | Résultats | Export |
|---|---|---|---:|---|
| Scopus | `TITLE-ABS-KEY(("blockchain" OR "distributed ledger") AND ("federated learning" OR "federated machine learning") AND ("security" OR "privacy" OR "trust" OR "data integrity" OR "poisoning attack"))` | Années 2020–2027 visibles dans capture ; types et langue à revérifier | 3 751 | CSV Zotero sauvegardé |
| Web of Science | `TS=(("blockchain" OR "distributed ledger") AND ("federated learning" OR "federated machine learning") AND ("security" OR "privacy" OR "trust" OR "data integrity" OR "poisoning attack"))` | Années 2021–2027 et anglais observés | 2 416 | RIS d'origine par lots, puis CSV Zotero |
| IEEE Xplore | Requête booléenne à trois blocs | 2020–2026 ; revues et conférences | 3 574 | 6 CSV sources, BibTeX converti, puis CSV Zotero |
| ACM DL | Recherche avancée à trois blocs | Jan. 2020–nov. 2026, ACM Full-Text Collection | 1 559 | Impossible : Premium requis |
| OpenAlex | `("blockchain" OR "distributed ledger") AND "federated learning" AND ("security" OR "privacy" OR "trust")` | Depuis 2020 ; types article/review/conference paper ; limite 5 opérateurs booléens | 4 570 | CSV source, BibTeX converti, puis CSV Zotero |

**Important** : les années affichées et opérateurs ne sont pas strictement identiques entre les bases. Les volumes ne constituent pas une comparaison expérimentale à filtres harmonisés. Pour répliquer strictement le protocole 2020–2026, il faudra lancer de nouvelles recherches, en les consignant dans **de nouvelles lignes** du journal sans écraser l'historique.

Le fichier `data/raw_zotero/` contient les *exports CSV depuis Zotero*, et non nécessairement les exports natifs de chaque base. La normalisation a été exécutée sur ces quatre fichiers.
