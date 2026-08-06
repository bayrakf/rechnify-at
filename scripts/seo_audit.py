#!/usr/bin/env python3
"""SEO-Audit fuer rechnify.at.

Prueft die statische Site auf die Fehlerklassen, die Google als
Qualitaetsprobleme wertet. Laeuft ohne Netzwerk gegen die lokalen Dateien.

Aufruf:  python3 scripts/seo_audit.py
Exit 1, wenn eine Pruefung fehlschlaegt.
"""
from __future__ import annotations

import collections
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://rechnify.at/"

# Seiten, die bewusst keine SEO-Regeln erfuellen muessen.
EXEMPT = {"404.html", "graphify-out/graph.html", "embed.html"}

RE_TITLE = re.compile(r"<title>(.*?)</title>", re.S)
RE_DESC = re.compile(r'name="description"\s+content="(.*?)"', re.S)
RE_CANON = re.compile(r'rel="canonical"\s+href="([^"]+)"')
RE_H1 = re.compile(r"<h1[\s>]")
RE_ROBOTS = re.compile(r'name="robots"\s+content="([^"]*)"')
RE_HREFLANG = re.compile(r'hreflang="([^"]+)"\s+href="([^"]+)"')
RE_HREF = re.compile(r'href="([^"#?]+)"')


def html_files() -> list[str]:
    out = []
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if not d.startswith(".") and d != "node_modules"]
        for name in filenames:
            if name.endswith(".html"):
                out.append(os.path.relpath(os.path.join(dirpath, name), ROOT))
    return sorted(out)


def url_to_path(url: str) -> str:
    """Wandelt eine Site-URL in den erwarteten Dateipfad um."""
    path = url.replace(SITE, "").split("#")[0].split("?")[0]
    if path == "" or path.endswith("/"):
        path += "index.html"
    return path


def audit() -> int:
    files = html_files()
    existing = set(files)
    pages = {}
    for rel in files:
        with open(os.path.join(ROOT, rel), encoding="utf-8", errors="ignore") as fh:
            pages[rel] = fh.read()

    checked = [f for f in files if f not in EXEMPT]

    def indexable(rel: str) -> bool:
        m = RE_ROBOTS.search(pages[rel])
        return not (m and "noindex" in m.group(1))

    indexed = [f for f in checked if indexable(f)]

    problems: dict[str, list[str]] = collections.OrderedDict()

    def record(name: str, items: list[str]) -> None:
        problems[name] = items

    # --- Meta-Basics, nur fuer indexierbare Seiten relevant ---
    record("ohne canonical", [f for f in checked if not RE_CANON.search(pages[f])])

    canon_wrong = []
    for f in checked:
        m = RE_CANON.search(pages[f])
        if not m:
            continue
        expected = SITE + f.replace("index.html", "")
        if m.group(1).rstrip("/") != expected.rstrip("/"):
            canon_wrong.append(f"{f} -> {m.group(1)}")
    record("canonical zeigt woanders hin", canon_wrong)

    def visible_html(rel: str) -> str:
        """HTML ohne script/style, damit z. B. PDF-Templates nicht mitzaehlen."""
        return re.sub(r"(?s)<(script|style)\b.*?</\1>", "", pages[rel])

    record("ohne h1", [f for f in checked if not RE_H1.search(visible_html(f))])
    record("mehr als ein h1", [f for f in checked if len(RE_H1.findall(visible_html(f))) > 1])
    record("ohne description", [f for f in checked if not RE_DESC.search(pages[f])])

    titles = collections.defaultdict(list)
    descs = collections.defaultdict(list)
    for f in indexed:
        t = RE_TITLE.search(pages[f])
        if t:
            titles[t.group(1).strip()].append(f)
        d = RE_DESC.search(pages[f])
        if d:
            descs[d.group(1).strip()].append(f)
    record(
        "doppelte titles (indexierbar)",
        [f"{len(v)}x {k[:60]}" for k, v in titles.items() if len(v) > 1],
    )
    record(
        "doppelte descriptions (indexierbar)",
        [f"{len(v)}x {k[:60]}" for k, v in descs.items() if len(v) > 1],
    )

    # --- hreflang muss auf existierende Dateien zeigen ---
    hreflang_dead = []
    for f in checked:
        for lang, url in RE_HREFLANG.findall(pages[f]):
            if url_to_path(url) not in existing:
                hreflang_dead.append(f"{f} [{lang}] -> {url}")
    record("hreflang zeigt ins Leere", hreflang_dead)

    # --- interne Links duerfen nicht ins Leere zeigen ---
    inbound = collections.Counter()
    dead_links = []
    for f in files:
        base = os.path.dirname(f)
        for href in RE_HREF.findall(pages[f]):
            if href.startswith(("http", "mailto", "tel", "//", "data:")):
                continue
            target = href.lstrip("/") if href.startswith("/") else os.path.normpath(os.path.join(base, href))
            if target == "" or target.endswith("/"):
                target += "index.html"
            if target in existing:
                inbound[target] += 1
            elif target.endswith(".html"):
                dead_links.append(f"{f} -> {href}")
    record("interne Links ins Leere", sorted(set(dead_links)))

    # --- Orphans: indexierbare Seiten ohne internen Eingangslink ---
    record("orphans (indexierbar, 0 interne Links)", [f for f in indexed if inbound[f] == 0])

    # --- Sitemap-Konsistenz ---
    sitemap_path = os.path.join(ROOT, "sitemap.xml")
    if os.path.exists(sitemap_path):
        with open(sitemap_path, encoding="utf-8") as fh:
            sitemap = fh.read()
        locs = re.findall(r"<loc>([^<]+)</loc>", sitemap)
        record("sitemap: Datei fehlt", [u for u in locs if url_to_path(u) not in existing])
        record(
            "sitemap: Seite ist noindex",
            [u for u in locs if url_to_path(u) in existing and not indexable(url_to_path(u))],
        )
        in_sitemap = {url_to_path(u) for u in locs}
        record("indexierbar aber nicht in sitemap", [f for f in indexed if f not in in_sitemap])

    # --- Report ---
    print(f"Dateien gesamt: {len(files)}   geprueft: {len(checked)}   indexierbar: {len(indexed)}")
    print()
    failed = 0
    for name, items in problems.items():
        mark = "OK  " if not items else "FAIL"
        if items:
            failed += 1
        print(f"[{mark}] {name}: {len(items)}")
        for item in items[:8]:
            print(f"         {item}")
        if len(items) > 8:
            print(f"         ... und {len(items) - 8} weitere")
    print()
    print("Ergebnis:", "alles sauber" if not failed else f"{failed} Pruefung(en) fehlgeschlagen")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(audit())
