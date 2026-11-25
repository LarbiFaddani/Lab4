#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""LAB 4 : fusion reproductible des exports CSV de Zotero, SANS déduplication.

Entrées par défaut : IEEE.csv, openAlex.csv, wos.csv, scopus.csv
Sorties : raw_bibliographic_dataset.csv et rapport_normalisation.json
Aucune bibliothèque externe n'est nécessaire (Python >= 3.9).
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import unicodedata
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

INPUTS = {
    "Scopus": "scopus.csv",
    "WoS": "wos.csv",
    "IEEE": "IEEE.csv",
    "OpenAlex": "openAlex.csv",
}
COLUMNS = ["id", "title", "authors", "year", "source", "doi"]


def compact(value: str | None) -> str:
    return re.sub(r"\s+", " ", unicodedata.normalize("NFKC", value or "")).strip()


def canonical_doi(value: str | None) -> str:
    doi = compact(value).lower()
    doi = re.sub(r"^(?:https?://(?:dx\.)?doi\.org/|doi\s*:\s*)", "", doi, flags=re.I)
    doi = doi.strip().strip("<>\u200b")
    # Ne pas considérer un DOI invalide comme une vraie clé de rapprochement.
    return doi if re.match(r"^10\.\d{4,9}/\S+$", doi) else ""


def title_key(value: str) -> str:
    # Normalisation réservée à la fabrication de l'empreinte : conserve title lisible.
    text = compact(value).casefold()
    text = unicodedata.normalize("NFKD", text)
    text = "".join(ch for ch in text if not unicodedata.combining(ch))
    return re.sub(r"[^a-z0-9]+", " ", text).strip()


def bibliographic_id(doi: str, title: str, year: str, source: str, key: str) -> str:
    if doi:
        return "doi:" + doi
    # Même titre+année sans DOI dans plusieurs bases -> même ID candidat.
    basis = (title_key(title) + "|" + year) if title else (source + "|" + key + "|" + year)
    return "titlehash:" + hashlib.sha256(basis.encode("utf-8")).hexdigest()[:24]


def parse_year(value: str | None, date: str | None) -> str:
    for candidate in (compact(value), compact(date)):
        match = re.search(r"\b(?:18|19|20|21)\d{2}\b", candidate)
        if match:
            return match.group(0)
    return ""


def build_dataset(directory: Path, output: Path, report_path: Path) -> None:
    all_rows = []
    source_reports = {}
    for source, filename in INPUTS.items():
        path = directory / filename
        if not path.is_file():
            raise FileNotFoundError(f"Fichier manquant pour {source}: {path}")
        count = Counter()
        with path.open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            expected = {"Title", "Author", "Publication Year", "DOI"}
            absent = expected - set(reader.fieldnames or [])
            if absent:
                raise ValueError(f"{filename}: colonnes Zotero manquantes: {sorted(absent)}")
            for original in reader:
                title = compact(original.get("Title"))
                authors = compact(original.get("Author"))
                year = parse_year(original.get("Publication Year"), original.get("Date"))
                doi = canonical_doi(original.get("DOI"))
                if not title: count["missing_title"] += 1
                if not authors: count["missing_authors"] += 1
                if not year: count["missing_year"] += 1
                if not doi: count["missing_doi"] += 1
                count["rows"] += 1
                all_rows.append({
                    "id": bibliographic_id(doi, title, year, source, original.get("Key", "")),
                    "title": title, "authors": authors, "year": year,
                    "source": source, "doi": doi,
                })
        source_reports[source] = {"fichier": filename, **dict(count)}
        print(f"{source:9s} : {count['rows']:5d} références")

    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=COLUMNS)
        writer.writeheader()
        writer.writerows(all_rows)

    occur = Counter(row["id"] for row in all_rows)
    duplicated_ids = {identifier: number for identifier, number in occur.items() if number > 1}
    report = {
        "generation_utc": datetime.now(timezone.utc).isoformat(),
        "inputs": source_reports,
        "total_lignes_brutes": len(all_rows),
        "colonnes": COLUMNS,
        "identifiants_distincts": len(occur),
        "groupes_id_repetes": len(duplicated_ids),
        "lignes_dans_groupes_id_repetes": sum(duplicated_ids.values()),
        "lignes_excedentaires_si_groupes_confirmes": sum(n - 1 for n in duplicated_ids.values()),
        "avertissement": (
            "Ces ID répétés sont des candidats à vérifier, pas des doublons validés. "
            "Aucune ligne n'a été supprimée. Les articles sans DOI sont rapprochés "
            "par titre normalisé + année. Un DOI absent/invalide n'est pas inventé."
        ),
        "exemples_identifiants_repetes": dict(list(duplicated_ids.items())[:15]),
    }
    with report_path.open("w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    print(f"\nTOTAL : {len(all_rows)} lignes (sans déduplication)")
    print(f"ID répétés (groupes candidats) : {len(duplicated_ids)}")
    print(f"CSV : {output}\nRapport : {report_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="LAB4 : normaliser et fusionner 4 CSV exportés de Zotero")
    parser.add_argument("--dir", type=Path, default=Path("."), help="Dossier des 4 CSV")
    parser.add_argument("--out", type=Path, default=Path("raw_bibliographic_dataset.csv"))
    parser.add_argument("--report", type=Path, default=Path("rapport_normalisation.json"))
    args = parser.parse_args()
    build_dataset(args.dir, args.out, args.report)
