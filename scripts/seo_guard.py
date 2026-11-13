#!/usr/bin/env python3
"""SEO-Guard: blockt ungewollte SEO-Aenderungen an bestehenden Seiten.

Vergleicht jede geaenderte .html gegen einen Git-Stand (Default HEAD):
title, description, canonical, robots, hreflang, H1-H3, Anzahl JSON-LD,
entfernte interne Links, Wortzahl (Toleranz 10 %). Reines CSS/Markup-Redesign
muss gruen bleiben.

Aufruf:  python3 scripts/seo_guard.py [--base REF] [--allow title,desc,ld]
Felder fuer --allow: title desc canon robots hreflang h ld links words
Exit 1 bei nicht erlaubter Abweichung oder geloeschter Seite.
"""
from __future__ import annotations

import argparse
import html
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from seo_audit import EXEMPT, RE_CANON, RE_DESC, RE_HREFLANG, RE_ROBOTS, RE_TITLE, ROOT

RE_HEAD = re.compile(r"<h([1-3])\b[^>]*>(.*?)</h\1>", re.S | re.I)
RE_LD = re.compile(r"application/ld\+json")
RE_LINK = re.compile(r'href="(/[^"#?]*)"')
RE_NOTEXT = re.compile(r"<(script|style)\b.*?</\1>", re.S | re.I)
RE_TAG = re.compile(r"<[^>]+>")


def fields(s: str) -> dict:
    text = html.unescape(RE_TAG.sub(" ", RE_NOTEXT.sub("", s)))
    return {
        "title": RE_TITLE.findall(s),
        "desc": RE_DESC.findall(s),
        "canon": RE_CANON.findall(s),
        "robots": RE_ROBOTS.findall(s),
        "hreflang": sorted(RE_HREFLANG.findall(s)),
        "h": [" ".join(RE_TAG.sub("", t).split()) for _, t in RE_HEAD.findall(s)],
        "ld": len(RE_LD.findall(s)),
        "links": set(RE_LINK.findall(s)),
        "words": len(text.split()),
    }


def diff(old: str, new: str, allow: set[str] = frozenset()) -> list[str]:
    a, b = fields(old), fields(new)
    out = []
    for k in a:
        if k in allow:
            continue
        if k == "links":
            gone = sorted(a[k] - b[k])  # neue Links sind ok, entfernte nicht
            if gone:
                out.append(f"links entfernt: {gone}")
        elif k == "words":
            if abs(b[k] - a[k]) > max(10, a[k] * 0.1):
                out.append(f"words: {a[k]} -> {b[k]}")
        elif a[k] != b[k]:
            out.append(f"{k}: {a[k]} -> {b[k]}")
    return out


def _selftest() -> None:
    a = '<title>Alt</title><h1>X</h1><a href="/a.html">a</a><p>eins zwei drei</p>'
    assert diff(a, a.replace("<h1>", '<h1 class="big">')) == []
    assert diff(a, a.replace("/a.html", "/b.html")) == ["links entfernt: ['/a.html']"]
    assert diff(a, a.replace("Alt", "Neu")) and not diff(a, a.replace("Alt", "Neu"), {"title"})


def git(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True)


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--base", default="HEAD")
    p.add_argument("--allow", default="", help="Komma-Liste erlaubter Felder")
    args = p.parse_args()
    allow = {x.strip() for x in args.allow.split(",") if x.strip()}
    _selftest()

    files = git("diff", "--name-only", args.base, "--", "*.html").stdout.splitlines()
    bad = 0
    for rel in files:
        if rel in EXEMPT or rel.startswith(("graft/", "graphify-out/")):
            continue
        old = git("show", f"{args.base}:{rel}")
        if old.returncode != 0:
            continue  # neue Seite, kein Risiko fuer bestehendes Ranking
        path = os.path.join(ROOT, rel)
        if not os.path.exists(path):
            print(f"✗ {rel}: Seite geloescht")
            bad += 1
            continue
        with open(path, encoding="utf-8") as fh:
            problems = diff(old.stdout, fh.read(), allow)
        if problems:
            bad += 1
            print(f"✗ {rel}")
            for line in problems:
                print(f"    {line}")
    print(f"seo_guard: {len(files)} geaenderte Seiten, {bad} mit SEO-Abweichung")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
