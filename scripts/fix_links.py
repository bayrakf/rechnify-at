#!/usr/bin/env python3
"""Repariert tote interne Links und hreflang-Verweise.

Zwei Fehlerklassen, die beim Generieren der pSEO-Seiten entstanden sind:

1. Nachbar-Links ("naechster Betrag") zeigen auf Betragsseiten, die es in
   dieser Sprachversion nie gab. Sie werden auf den naechstgelegenen
   vorhandenen Betrag umgebogen, sonst entfernt.
2. hreflang verweist auf ein Sprach-Gegenstueck, das nicht existiert.
   Solche Verweise werden entfernt; x-default faellt dann auf die Seite
   selbst zurueck.

Aufruf:  python3 scripts/fix_links.py [--dry-run]
"""
from __future__ import annotations

import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://rechnify.at/"

RE_HREFLANG_LINE = re.compile(
    r'[ \t]*<link rel="alternate" hreflang="([^"]+)" href="([^"]+)"\s*/?>\n?'
)
RE_LI_LINK = re.compile(r'[ \t]*<li><a href="(/[^"]+\.html)">[^<]*</a></li>\n?')
RE_AMOUNT = re.compile(r"/(\d+)-brutto-in-netto\.html$")


def all_html() -> list[str]:
    out = []
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if not d.startswith(".") and d != "node_modules"]
        for name in filenames:
            if name.endswith(".html"):
                out.append(os.path.relpath(os.path.join(dirpath, name), ROOT))
    return sorted(out)


def url_to_path(url: str) -> str:
    path = url.replace(SITE, "").split("#")[0].split("?")[0].lstrip("/")
    if path == "" or path.endswith("/"):
        path += "index.html"
    return path


def nearest_amount(target: str, existing: set[str]) -> str | None:
    """Sucht die naechstgelegene vorhandene Betragsseite im selben Ordner."""
    m = RE_AMOUNT.search(target)
    if not m:
        return None
    directory = os.path.dirname(target).lstrip("/")
    wanted = int(m.group(1))
    candidates = []
    for rel in existing:
        if os.path.dirname(rel) != directory:
            continue
        am = RE_AMOUNT.search("/" + rel)
        if am:
            candidates.append((abs(int(am.group(1)) - wanted), int(am.group(1)), rel))
    if not candidates:
        return None
    candidates.sort()
    if candidates[0][0] == 0:
        return None
    return "/" + candidates[0][2]


def main() -> int:
    dry = "--dry-run" in sys.argv
    files = all_html()
    existing = set(files)

    fixed_links = redirected = removed_links = removed_hreflang = 0
    touched: set[str] = set()

    for rel in files:
        path = os.path.join(ROOT, rel)
        with open(path, encoding="utf-8") as fh:
            html = fh.read()
        original = html

        # --- 1. tote Listen-Links ---
        def repair_li(match: re.Match[str]) -> str:
            nonlocal redirected, removed_links
            target = match.group(1).lstrip("/")
            if target in existing:
                return match.group(0)
            replacement = nearest_amount(match.group(1), existing)
            if replacement:
                redirected += 1
                amount = RE_AMOUNT.search(replacement).group(1)
                indent = match.group(0)[: len(match.group(0)) - len(match.group(0).lstrip())]
                return f'{indent}<li><a href="{replacement}">{amount} € Brutto → Netto</a></li>\n'
            removed_links += 1
            return ""

        html = RE_LI_LINK.sub(repair_li, html)

        # --- 2. hreflang ins Leere ---
        had_hreflang = 'hreflang="' in html

        def repair_hreflang(match: re.Match[str]) -> str:
            nonlocal removed_hreflang
            if url_to_path(match.group(2)) in existing:
                return match.group(0)
            removed_hreflang += 1
            return ""

        html = RE_HREFLANG_LINE.sub(repair_hreflang, html)

        # Hatte die Seite hreflang und ist x-default dabei weggefallen,
        # zeigt x-default nun auf die Seite selbst.
        if had_hreflang and 'hreflang="x-default"' not in html and 'rel="canonical"' in html:
            self_url = SITE + rel.replace("index.html", "")
            html = html.replace(
                '<link rel="canonical"',
                f'<link rel="alternate" hreflang="x-default" href="{self_url}" />\n  <link rel="canonical"',
                1,
            )

        if html != original:
            touched.add(rel)
            fixed_links += 1
            if not dry:
                with open(path, "w", encoding="utf-8") as fh:
                    fh.write(html)

    print(f"Dateien geaendert:        {len(touched)}")
    print(f"Links umgebogen:          {redirected}")
    print(f"Links entfernt:           {removed_links}")
    print(f"hreflang-Zeilen entfernt: {removed_hreflang}")
    if dry:
        print("(dry-run, nichts geschrieben)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
