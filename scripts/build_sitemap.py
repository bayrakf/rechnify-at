#!/usr/bin/env python3
"""Baut sitemap.xml aus der Index-Policy.

Nutzt dieselbe Entscheidung wie `fix_noindex.py` (siehe seo_policy.py),
damit Sitemap und robots-Meta nicht auseinanderlaufen koennen.

Aufruf:  python3 scripts/build_sitemap.py
"""
from __future__ import annotations

import datetime
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from seo_policy import ROOT, all_pages, should_index, twin_of, url_for

TODAY = datetime.date.today().isoformat()
RE_ALT = re.compile(r'<link rel="alternate" hreflang="([^"]+)" href="([^"]+)"')


def lastmod(rel: str) -> str:
    """Datum des letzten Commits der Datei. Massen-Bumps auf 'heute' entwerten lastmod bei Google."""
    out = subprocess.run(
        # Boilerplate-Commits (Fonts, Nav, Footer, Styles) aendern keinen Inhalt.
        ["git", "log", "-1", "--format=%cs", "-E", "--invert-grep",
         r"--grep=^(style|perf|chore)|^fix\((ux|legal)\)", "--", rel],
        cwd=ROOT, capture_output=True, text=True,
    ).stdout.strip()
    return out or TODAY  # neue, noch nicht committete Seite


def alternates(rel: str) -> str:
    """hreflang der Seite selbst hat Vorrang, damit Sitemap und Seite nicht widersprechen."""
    with open(os.path.join(ROOT, rel), encoding="utf-8") as fh:
        own = RE_ALT.findall(fh.read(20000))
    if own:
        return "\n".join(f'    <xhtml:link rel="alternate" hreflang="{l}" href="{h}"/>' for l, h in own)
    twin = twin_of(rel)
    if twin and should_index(twin):
        at, de = (twin, rel) if rel.startswith("de/") else (rel, twin)
        at_url, de_url = url_for(at), url_for(de)
        return (
            f'    <xhtml:link rel="alternate" hreflang="de-AT" href="{at_url}"/>\n'
            f'    <xhtml:link rel="alternate" hreflang="de-DE" href="{de_url}"/>\n'
            f'    <xhtml:link rel="alternate" hreflang="x-default" href="{at_url}"/>'
        )
    url = url_for(rel)
    lang = "de-DE" if rel.startswith("de/") else "de-AT"
    return (
        f'    <xhtml:link rel="alternate" hreflang="{lang}" href="{url}"/>\n'
        f'    <xhtml:link rel="alternate" hreflang="x-default" href="{url}"/>'
    )


def main() -> int:
    pages = [p for p in all_pages() if should_index(p)]
    entries = []
    for rel in pages:
        entries.append(
            "  <url>\n"
            f"    <loc>{url_for(rel)}</loc>\n"
            f"{alternates(rel)}\n"
            f"    <lastmod>{lastmod(rel)}</lastmod>\n"
            "  </url>"
        )

    xml = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"\n'
        '        xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
        + "\n".join(entries)
        + "\n</urlset>\n"
    )
    with open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8") as fh:
        fh.write(xml)
    print(f"sitemap.xml geschrieben: {len(pages)} URLs")
    return 0


if __name__ == "__main__":
    sys.exit(main())
