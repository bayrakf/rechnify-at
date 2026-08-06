#!/usr/bin/env python3
"""Eine Stelle, die entscheidet, welche Seite in den Google-Index soll.

Vorher gab es zwei Wahrheiten: das robots-Meta in der Datei und die
Sitemap. Sie sind auseinandergelaufen (392 DE-Seiten auf noindex, die 367
AT-Zwillinge nicht). Diese Datei ist die einzige Quelle; `fix_noindex.py`
schreibt sie in die Dateien, `build_sitemap.py` in die sitemap.xml.

Leitgedanke: Eine Seite gehoert nur dann in den Index, wenn sie eigenen
Wert hat. Generierte Betragsseiten in 10-Euro-Schritten haben den nicht,
runde Betraege und Berufsseiten schon.
"""
from __future__ import annotations

import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://rechnify.at"

# Rechtliches und Technisches gehoert nicht in die Suche.
# changelog.html bleibt drin: Tarif-Updates sind ein Aktualitaetssignal.
EXCLUDED_FILES = {
    "impressum.html",
    "datenschutz.html",
    "404.html",
    "embed.html",
}

EXCLUDED_DIRS = ("graphify-out/", "scripts/", "node_modules/", "scratch/")

RE_AMOUNT = re.compile(r"(\d+)-brutto-in-netto\.html$")

# Betragsseiten: nur runde 500er-Schritte sind eigenstaendig genug.
AMOUNT_STEP = 500


def all_pages() -> list[str]:
    """Alle HTML-Seiten des Projekts, relativ zum Repo-Root."""
    out = []
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if not d.startswith(".") and d != "node_modules"]
        for name in filenames:
            if name.endswith(".html"):
                out.append(os.path.relpath(os.path.join(dirpath, name), ROOT))
    return sorted(out)


def should_index(rel: str) -> bool:
    """Entscheidet, ob eine Seite indexiert werden soll."""
    rel = rel.replace(os.sep, "/")
    if rel in EXCLUDED_FILES or os.path.basename(rel) in EXCLUDED_FILES:
        return False
    if any(rel.startswith(d) for d in EXCLUDED_DIRS):
        return False

    amount = RE_AMOUNT.search(rel)
    if amount:
        return int(amount.group(1)) % AMOUNT_STEP == 0

    return True


def url_for(rel: str) -> str:
    """Kanonische URL einer Seite (Verzeichnis-URLs ohne index.html)."""
    rel = rel.replace(os.sep, "/")
    if rel == "index.html":
        return f"{SITE}/"
    if rel.endswith("/index.html"):
        return f"{SITE}/{rel[:-10]}"
    return f"{SITE}/{rel}"


def twin_of(rel: str) -> str | None:
    """Das Sprach-Gegenstueck einer Seite, falls es existiert."""
    rel = rel.replace(os.sep, "/")
    other = rel[3:] if rel.startswith("de/") else f"de/{rel}"
    return other if os.path.exists(os.path.join(ROOT, other)) else None


if __name__ == "__main__":
    pages = all_pages()
    indexed = [p for p in pages if should_index(p)]
    print(f"Seiten gesamt: {len(pages)}")
    print(f"davon indexiert: {len(indexed)}")
    print(f"davon noindex:   {len(pages) - len(indexed)}")
