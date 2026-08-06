#!/usr/bin/env python3
"""Schreibt die Index-Policy in die robots-Metatags der Seiten.

Quelle der Wahrheit ist `seo_policy.should_index`. Dasselbe Kriterium
bestimmt die Sitemap, damit beide nicht auseinanderlaufen koennen.

Aufruf:  python3 scripts/fix_noindex.py [--dry-run]
"""
from __future__ import annotations

import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from seo_policy import ROOT, all_pages, should_index

INDEX_ROBOTS = (
    '<meta name="robots" content="index, follow, max-image-preview:large, '
    'max-snippet:-1, max-video-preview:-1" />'
)
NOINDEX_ROBOTS = '<meta name="robots" content="noindex, nofollow" />'

RE_ROBOTS = re.compile(r'<meta name="robots" content="[^"]*"\s*/?>')

# Technische Seiten ohne robots-Steuerung: 404 und die Embed-Vorschau
# sollen weder in der Sitemap noch mit noindex angefasst werden.
KEEP_INDEXABLE = {"404.html", "embed.html"}


def main() -> int:
    dry = "--dry-run" in sys.argv
    to_noindex, to_index, missing = [], [], []

    for rel in all_pages():
        if rel in KEEP_INDEXABLE or os.path.basename(rel) in KEEP_INDEXABLE:
            continue
        path = os.path.join(ROOT, rel)
        with open(path, encoding="utf-8") as fh:
            html = fh.read()

        m = RE_ROBOTS.search(html)
        if not m:
            missing.append(rel)
            continue

        is_noindex = "noindex" in m.group(0)
        wants_index = should_index(rel)

        if wants_index and is_noindex:
            new = RE_ROBOTS.sub(INDEX_ROBOTS, html, count=1)
            to_index.append(rel)
        elif not wants_index and not is_noindex:
            new = RE_ROBOTS.sub(NOINDEX_ROBOTS, html, count=1)
            to_noindex.append(rel)
        else:
            continue

        if not dry:
            with open(path, "w", encoding="utf-8") as fh:
                fh.write(new)

    print(f"auf noindex gesetzt: {len(to_noindex)}")
    print(f"wieder indexierbar:  {len(to_index)}")
    if missing:
        print(f"ohne robots-Meta:    {len(missing)} -> {missing[:5]}")
    if dry:
        print("(dry-run, nichts geschrieben)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
