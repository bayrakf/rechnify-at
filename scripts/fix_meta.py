#!/usr/bin/env python3
"""Macht Meta-Descriptions und Titles eindeutig.

Generierte Seiten haben die Beschreibung ihrer Vorlage geerbt. Google
wertet das als Duplicate-Signal. Dieses Skript leitet aus dem tatsaechlichen
Seiteninhalt (Betrag, Beruf, Durchschnittsgehalt, Land) eine eigene
Beschreibung ab und haengt bei AT/DE-Zwillingen das Land an den Titel.

Aufruf:  python3 scripts/fix_meta.py [--dry-run]
"""
from __future__ import annotations

import collections
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

RE_DESC = re.compile(r'(<meta name="description"\s+content=")(.*?)(")', re.S)
RE_OG_DESC = re.compile(r'(<meta property="og:description"\s+content=")(.*?)(")', re.S)
RE_TITLE = re.compile(r"(<title>)(.*?)(</title>)", re.S)
RE_OG_TITLE = re.compile(r'(<meta property="og:title"\s+content=")(.*?)(")', re.S)
RE_H1 = re.compile(r"<h1[^>]*>(.*?)</h1>", re.S)
RE_ROBOTS = re.compile(r'name="robots"\s+content="([^"]*)"')
RE_TAGS = re.compile(r"<[^>]+>")
RE_AVG = re.compile(r"Durchschnittliches Gehalt:\s*([\d.,]+)\s*€")
RE_AMOUNT_FILE = re.compile(r"(\d+)-brutto-in-netto\.html$")


def all_html() -> list[str]:
    out = []
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if not d.startswith(".") and d != "node_modules"]
        for name in filenames:
            if name.endswith(".html"):
                out.append(os.path.relpath(os.path.join(dirpath, name), ROOT))
    return sorted(out)


def is_indexable(html: str) -> bool:
    m = RE_ROBOTS.search(html)
    return not (m and "noindex" in m.group(1))


def clean(text: str) -> str:
    return RE_TAGS.sub("", text).replace("&amp;", "&").strip()


def euro(value: int) -> str:
    return f"{value:,}".replace(",", ".")


def describe(rel: str, html: str) -> str | None:
    """Baut eine seitenspezifische Beschreibung, sonst None."""
    country = "Deutschland" if rel.startswith("de/") else "Österreich"
    h1 = RE_H1.search(html)
    heading = clean(h1.group(1)) if h1 else ""

    amount = RE_AMOUNT_FILE.search(rel)
    if amount:
        value = int(amount.group(1))
        extra = (
            "inklusive 13. und 14. Gehalt"
            if country == "Österreich"
            else "nach Steuerklasse und Sozialabgaben"
        )
        return (
            f"{euro(value)} € brutto in netto für {country} 2026: So viel bleibt monatlich "
            f"übrig, {extra}. Mit Aufschlüsselung von Sozialversicherung und Lohnsteuer."
        )

    if "/gehalt/" in rel:
        avg = RE_AVG.search(html)
        job = heading.split("Gehalt", 1)[-1].split("–")[0].strip() or heading
        job = job.replace(country, "").strip(" –-")
        if rel.rsplit("/", 1)[-1].startswith("gehalt-"):
            city = job or rel.rsplit("/", 1)[-1][7:-5].capitalize()
            return (
                f"Gehälter in {city} 2026: Was verdient man dort brutto und wie viel bleibt "
                f"netto übrig? Mit Brutto-Netto-Rechner für {country}."
            )
        if avg:
            closing = (
                "Berechne direkt das Netto inklusive 13. und 14. Gehalt."
                if country == "Österreich"
                else "Berechne direkt das Netto nach Steuerklasse und Sozialabgaben."
            )
            return (
                f"Was verdient ein {job} in {country}? Durchschnittlich {avg.group(1)} € brutto "
                f"im Monat 2026. {closing}"
            )
        return (
            f"Was verdient ein {job} in {country} 2026? Durchschnittsgehalt brutto und netto "
            f"mit direkter Berechnung."
        )

    return None


def main() -> int:
    dry = "--dry-run" in sys.argv
    files = all_html()

    # Zuerst Descriptions individualisieren.
    desc_changed = 0
    for rel in files:
        path = os.path.join(ROOT, rel)
        with open(path, encoding="utf-8") as fh:
            html = fh.read()
        if not is_indexable(html):
            continue
        new_desc = describe(rel, html)
        if not new_desc:
            continue
        updated = RE_DESC.sub(lambda m: m.group(1) + new_desc + m.group(3), html, count=1)
        updated = RE_OG_DESC.sub(lambda m: m.group(1) + new_desc + m.group(3), updated, count=1)
        if updated != html:
            desc_changed += 1
            if not dry:
                with open(path, "w", encoding="utf-8") as fh:
                    fh.write(updated)

    # Danach doppelte Titles auflösen: AT/DE-Zwillinge bekommen das Land.
    titles = collections.defaultdict(list)
    for rel in files:
        with open(os.path.join(ROOT, rel), encoding="utf-8") as fh:
            html = fh.read()
        if not is_indexable(html):
            continue
        t = RE_TITLE.search(html)
        if t:
            titles[t.group(2).strip()].append(rel)

    title_changed = 0
    for title, rels in titles.items():
        if len(rels) < 2:
            continue
        for rel in rels:
            country = "Deutschland" if rel.startswith("de/") else "Österreich"
            if country.lower() in title.lower():
                continue
            head, sep, brand = title.partition(" | ")
            new_title = f"{head} {country}{sep}{brand}" if sep else f"{title} {country}"
            path = os.path.join(ROOT, rel)
            with open(path, encoding="utf-8") as fh:
                html = fh.read()
            updated = RE_TITLE.sub(lambda m: m.group(1) + new_title + m.group(3), html, count=1)
            updated = RE_OG_TITLE.sub(
                lambda m: m.group(1) + new_title + m.group(3), updated, count=1
            )
            if updated != html:
                title_changed += 1
                if not dry:
                    with open(path, "w", encoding="utf-8") as fh:
                        fh.write(updated)

    print(f"Descriptions individualisiert: {desc_changed}")
    print(f"Titles entdoppelt:             {title_changed}")
    if dry:
        print("(dry-run, nichts geschrieben)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
