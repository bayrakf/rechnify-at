#!/usr/bin/env python3
"""Fill remaining gaps from Bestandsanalyse. Idempotent-ish. Run: python3 scripts/ship_gaps.py"""
from __future__ import annotations

import re
import shutil
from datetime import date
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
TODAY = date.today().isoformat()
AMOUNTS = list(range(1500, 5010, 10)) + list(range(5200, 6100, 100)) + [6500, 7000, 8000, 9000, 10000]

CITIES = [
    # slug, name, country at|de, note (no invented tax rates)
    ("wien", "Wien", "at"),
    ("graz", "Graz", "at"),
    ("linz", "Linz", "at"),
    ("salzburg", "Salzburg", "at"),
    ("innsbruck", "Innsbruck", "at"),
    ("berlin", "Berlin", "de"),
    ("muenchen", "München", "de"),
    ("hamburg", "Hamburg", "de"),
    ("koeln", "Köln", "de"),
    ("frankfurt", "Frankfurt", "de"),
    ("stuttgart", "Stuttgart", "de"),
    ("duesseldorf", "Düsseldorf", "de"),
]


def unique_amount_content(amount: int, formatted: str, country_name: str, code: str) -> str:
    median = "3.650 € (AT-Median Vollzeit)" if code == "at" else "ca. 3.500 € (DE-Median Vollzeit, Richtwert)"
    if amount < 2000:
        category, comparison = "Einstiegsgehalt", f"unter dem typischen Median ({median})"
    elif amount < 3000:
        category, comparison = "unteres Mittelfeld", f"nahe dem Median ({median})"
    elif amount < 4000:
        category, comparison = "mittleres Einkommen", f"um den Median ({median})"
    elif amount < 5000:
        category, comparison = "gehobenes Mittelfeld", f"über dem Median ({median})"
    elif amount < 6000:
        category, comparison = "hohes Einkommen", f"deutlich über dem Median ({median})"
    else:
        category, comparison = "Spitzenverdiener", f"weit über dem Median ({median})"

    prefix = "" if code == "at" else "/de"
    sv = (
        f"<li><strong>Sozialversicherung:</strong> ca. {amount * 0.1807:.0f} € (18,07 %, bis Höchstbeitragsgrundlage)</li>"
        if code == "at"
        else "<li><strong>Sozialversicherung:</strong> Arbeitnehmeranteil typisch knapp über 20 % (KV/RV/AV/PV, Näherung)</li>"
    )
    special = (
        f"Jahressechstel ca. {amount * 12 / 6:.0f} € — 13./14. Gehalt bis dahin begünstigt besteuert (AT)."
        if code == "at"
        else "DE: progressiver ESt-Tarif; Kirchensteuer/Soli je nach Fall möglich."
    )
    return f"""
      <section class="content-section" style="margin-top:32px;">
        <h2>Was bedeutet {formatted} € Brutto in {country_name}?</h2>
        <p>Ein Bruttogehalt von {formatted} €/Monat fällt in {country_name} in die Kategorie <strong>{category}</strong> — {comparison}.</p>
        <h3>Abzüge (Orientierung)</h3>
        <ul>
          {sv}
          <li><strong>Lohnsteuer:</strong> progressiv nach Tarif — genaue Summe im Rechner oben</li>
        </ul>
        <p>{special}</p>
        <h3>Vergleich</h3>
        <ul>
          <li><a href="{prefix}/finanzen/brutto-netto/{max(1500, amount - 100)}-brutto-in-netto.html">{max(1500, amount - 100)} € Brutto → Netto</a></li>
          <li><a href="{prefix}/finanzen/brutto-netto/{min(10000, amount + 100)}-brutto-in-netto.html">{min(10000, amount + 100)} € Brutto → Netto</a></li>
          <li><a href="{prefix}/finanzen/gehaltsrechner.html">Zum vollen Gehaltsrechner</a></li>
        </ul>
        <p class="help">Stand {TODAY}. Orientierungswerte, keine Steuerberatung.</p>
      </section>
"""


def generate_at_amounts() -> int:
    src = (BASE / "finanzen/gehaltsrechner.html").read_text(encoding="utf-8")
    out_dir = BASE / "finanzen/brutto-netto"
    out_dir.mkdir(parents=True, exist_ok=True)
    n = 0
    for amount in AMOUNTS:
        path = out_dir / f"{amount}-brutto-in-netto.html"
        if path.exists() and amount % 100 != 0:
            # still regenerate 10er for consistency
            pass
        formatted = f"{amount:,}".replace(",", ".")
        html = src
        html = re.sub(r"<title>.*?</title>", f"<title>{formatted} € Brutto in Netto Österreich | rechnify.at</title>", html, count=1)
        desc = f"Wie viel Netto bleibt von {formatted} € Brutto in Österreich? Steuern, SV und Abzüge für 2026 berechnen."
        html = re.sub(r'<meta name="description" content="[^"]*" />', f'<meta name="description" content="{desc}" />', html, count=1)
        html = re.sub(r'<meta property="og:title" content="[^"]*" />', f'<meta property="og:title" content="{formatted} € Brutto in Netto Österreich" />', html, count=1)
        html = re.sub(r'<meta property="og:description" content="[^"]*" />', f'<meta property="og:description" content="{desc}" />', html, count=1)
        canon = f"https://rechnify.at/finanzen/brutto-netto/{amount}-brutto-in-netto.html"
        html = re.sub(r'<link rel="canonical" href="[^"]*" />', f'<link rel="canonical" href="{canon}" />', html, count=1)
        html = re.sub(r'<meta property="og:url" content="[^"]*" />', f'<meta property="og:url" content="{canon}" />', html, count=1)
        html = re.sub(r'<link rel="alternate" hreflang="[^"]+" href="[^"]+" />\n?', "", html)
        hreflang = (
            f'  <link rel="alternate" hreflang="de-AT" href="{canon}" />\n'
            f'  <link rel="alternate" hreflang="de-DE" href="https://rechnify.at/de/finanzen/brutto-netto/{amount}-brutto-in-netto.html" />\n'
            f'  <link rel="alternate" hreflang="x-default" href="{canon}" />\n'
        )
        html = html.replace(f'<link rel="canonical" href="{canon}" />', f'<link rel="canonical" href="{canon}" />\n{hreflang}', 1)
        html = re.sub(r"<h1[^>]*>.*?</h1>", f"<h1>{formatted} € Brutto in Netto Österreich</h1>", html, count=1, flags=re.S)
        html = re.sub(
            r'<input type="number" id="grossMonthly"[^>]*>',
            f'<input type="number" id="grossMonthly" value="{amount}" min="0" step="100">',
            html,
            count=1,
        )
        block = unique_amount_content(amount, formatted, "Österreich", "at")
        if "<!-- FAQ Section -->" in html:
            html = html.replace("<!-- FAQ Section -->", block + "\n      <!-- FAQ Section -->", 1)
        elif "</main>" in html:
            html = html.replace("</main>", block + "\n</main>", 1)
        if "btn.click()" not in html:
            html = html.replace(
                "</body>",
                "<script>document.addEventListener('DOMContentLoaded',()=>{setTimeout(()=>{const b=document.getElementById('calculate');if(b)b.click();},100);});</script>\n</body>",
                1,
            )
        path.write_text(html, encoding="utf-8")
        n += 1
    print(f"AT amounts: {n}")
    return n


def generate_cities() -> int:
    n = 0
    for slug, name, code in CITIES:
        prefix = "" if code == "at" else "/de"
        country = "Österreich" if code == "at" else "Deutschland"
        lang = "de-AT" if code == "at" else "de-DE"
        locale = "de_AT" if code == "at" else "de_DE"
        calc = f"{prefix}/finanzen/gehaltsrechner.html"
        twin_slug = None
        # optional twin cities not paired 1:1 — skip hreflang pairs
        og = f"https://rechnify.at/assets/images/og/gehalt-{slug}.png"
        out = BASE / (f"finanzen/gehalt/gehalt-{slug}.html" if code == "at" else f"de/finanzen/gehalt/gehalt-{slug}.html")
        out.parent.mkdir(parents=True, exist_ok=True)
        canon = f"https://rechnify.at{prefix}/finanzen/gehalt/gehalt-{slug}.html"
        html = f"""<!DOCTYPE html>
<html lang="{lang}">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Gehalt {name} – Brutto Netto Rechner | rechnify.at</title>
  <meta name="description" content="Gehalt in {name} ({country}) berechnen: Brutto zu Netto mit lokalem Rechner. Orientierung 2026 — keine erfundenen Stadt-Steuersätze." />
  <link rel="canonical" href="{canon}" />
  <meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1" />
  <link rel="alternate" hreflang="{lang}" href="{canon}" />
  <link rel="alternate" hreflang="x-default" href="{canon}" />
  <meta property="og:type" content="website" />
  <meta property="og:title" content="Gehalt {name} – Brutto Netto" />
  <meta property="og:description" content="Nettogehalt für {name} mit dem {country}-Rechner berechnen." />
  <meta property="og:url" content="{canon}" />
  <meta property="og:image" content="{og}" />
  <meta property="og:image:alt" content="Gehalt {name} – rechnify.at" />
  <meta property="og:locale" content="{locale}" />
  <meta property="og:site_name" content="rechnify.at" />
  <meta name="twitter:card" content="summary_large_image" />
  <link rel="icon" href="/assets/images/favicon.ico" sizes="48x48" />
  <link rel="manifest" href="/site.webmanifest" />
  <meta name="theme-color" content="#1858C7" />
  <link rel="stylesheet" href="/tokens.css?v=1.2" />
  <link rel="stylesheet" href="/assets/css/global.css?v=3.1" />
</head>
<body>
  <header class="site-header"><div class="header-inner">
    <a href="{ '/' if code == 'at' else '/de/' }" class="site-logo"><span class="site-logo-text">rechnify<span>.at</span></span></a>
  </div></header>
  <nav class="breadcrumb" aria-label="Brotkrumen">
    <a href="/">Start</a><span class="breadcrumb-sep">/</span>
    <a href="{prefix}/finanzen/">Finanzen</a><span class="breadcrumb-sep">/</span>
    <span class="breadcrumb-current">Gehalt {name}</span>
  </nav>
  <main class="site-main">
    <article class="content-section">
      <h1>Gehalt {name} – Brutto in Netto</h1>
      <p>Du suchst das typische oder dein persönliches Gehalt in <strong>{name}</strong> ({country})? Steuern und Sozialabgaben richten sich nach dem nationalen Recht von {country} — nicht nach einem eigenen „Städtetarif“. Nutze den Rechner für die exakte Netto-Schätzung.</p>
      <p><a class="btn" href="{calc}">Zum Gehaltsrechner {country} ➔</a></p>
      <h2>Was beeinflusst Gehälter in {name}?</h2>
      <ul>
        <li>Branche und Beruf (siehe auch unsere <a href="{prefix}/finanzen/gehalt/">Berufsseiten</a>)</li>
        <li>Berufserfahrung und Qualifikation</li>
        <li>Vollzeit vs. Teilzeit</li>
        <li>{'Pendlerpauschale / Pendlereuro (AT)' if code == 'at' else 'Entfernungspauschale (DE)'} bei längerem Arbeitsweg</li>
      </ul>
      <p class="help">Kein erfundener Stadt-Durchschnitt. Stand {TODAY}. Keine Steuerberatung.</p>
      <p class="updated" data-updated="{TODAY}">Zuletzt aktualisiert: {TODAY}</p>
    </article>
  </main>
  <script src="/assets/js/global.js?v=3.1"></script>
</body>
</html>
"""
        out.write_text(html, encoding="utf-8")
        n += 1
    print(f"City pages: {n}")
    return n


def write_de_hubs() -> None:
    fin_at = (BASE / "finanzen/index.html").read_text(encoding="utf-8")
    az_at = (BASE / "arbeitszeit/index.html").read_text(encoding="utf-8")

    def to_de(html: str, section: str) -> str:
        html = html.replace('lang="de-AT"', 'lang="de-DE"')
        html = html.replace("Österreich 2026", "Deutschland 2026")
        html = html.replace("de_AT", "de_DE")
        html = html.replace(f"https://rechnify.at/{section}/", f"https://rechnify.at/de/{section}/")
        html = html.replace(f'href="/{section}/"', f'href="/de/{section}/"')
        html = html.replace(f"/{section}/", f"/de/{section}/")  # careful — may double
        # undo double
        html = html.replace("/de/de/", "/de/")
        # fix tool links already under /de/
        html = re.sub(r'href="/de/(arbeitszeit|finanzen)/de/', r'href="/de/\1/', html)
        # AT-only tools: point to DE twins where they exist
        swaps = {
            "/de/finanzen/gehaltsrechner.html": "/de/finanzen/gehaltsrechner.html",
            "/finanzen/gehaltsrechner.html": "/de/finanzen/gehaltsrechner.html",
        }
        # rebuild from AT hub more carefully
        return html

    # Simpler: write lean DE hubs from scratch
    for section, title, links in [
        (
            "finanzen",
            "Finanzen & Steuern Rechner Deutschland 2026",
            [
                ("/de/finanzen/gehaltsrechner.html", "Brutto-Netto Gehaltsrechner DE"),
                ("/de/finanzen/brutto-netto/", "Brutto-Netto Betragsübersicht"),
                ("/de/finanzen/mwst-rechner.html", "MwSt-Rechner DE"),
                ("/de/finanzen/pendlerrechner.html", "Pendlerrechner DE"),
                ("/de/finanzen/kirchensteuer-rechner.html", "Kirchensteuer-Rechner"),
                ("/de/finanzen/kreditrechner.html", "Kreditrechner"),
                ("/de/finanzen/leasingrechner.html", "Leasingrechner"),
                ("/de/finanzen/etf-sparplan-rechner.html", "ETF-Sparplan"),
                ("/de/finanzen/kryptosteuerrechner.html", "Krypto-Steuer"),
                ("/finanzen/brutto-netto-oesterreich-vs-deutschland.html", "AT vs DE Vergleich"),
            ],
        ),
        (
            "arbeitszeit",
            "Arbeitszeit & Personal Rechner Deutschland 2026",
            [
                ("/de/arbeitszeit/kommen-gehen-rechner.html", "Kommen-Gehen Rechner"),
                ("/de/arbeitszeit/ueberstundenrechner.html", "Überstundenrechner"),
                ("/de/arbeitszeit/stundenlohn-rechner.html", "Stundenlohnrechner"),
                ("/de/arbeitszeit/teilzeitrechner.html", "Teilzeitrechner"),
                ("/de/arbeitszeit/urlaubstage-rechner.html", "Urlaubstage"),
                ("/de/arbeitszeit/brueckentage-planer.html", "Brückentage-Planer"),
                ("/de/arbeitszeit/arbeitstage-rechner.html", "Arbeitstage-Rechner"),
            ],
        ),
    ]:
        lis = "\n".join(f'        <li><a href="{h}">{t}</a></li>' for h, t in links)
        html = f"""<!DOCTYPE html>
<html lang="de-DE">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{title} | rechnify.at</title>
  <meta name="description" content="{title}. Kostenlose Rechner, lokal im Browser." />
  <link rel="canonical" href="https://rechnify.at/de/{section}/" />
  <meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1" />
  <link rel="alternate" hreflang="de-DE" href="https://rechnify.at/de/{section}/" />
  <link rel="alternate" hreflang="de-AT" href="https://rechnify.at/{section}/" />
  <link rel="alternate" hreflang="x-default" href="https://rechnify.at/{section}/" />
  <meta property="og:type" content="website" />
  <meta property="og:title" content="{title}" />
  <meta property="og:url" content="https://rechnify.at/de/{section}/" />
  <meta property="og:image" content="https://rechnify.at/assets/images/og/hub-{section}-de.png" />
  <meta property="og:locale" content="de_DE" />
  <meta property="og:site_name" content="rechnify.at" />
  <link rel="manifest" href="/site.webmanifest" />
  <meta name="theme-color" content="#1858C7" />
  <link rel="stylesheet" href="/tokens.css?v=1.2" />
  <link rel="stylesheet" href="/assets/css/global.css?v=3.1" />
</head>
<body>
  <header class="site-header"><div class="header-inner">
    <a href="/de/" class="site-logo"><span class="site-logo-text">rechnify<span>.at</span></span></a>
  </div></header>
  <nav class="breadcrumb" aria-label="Brotkrumen">
    <a href="/">Start</a><span class="breadcrumb-sep">/</span>
    <a href="/de/">DE</a><span class="breadcrumb-sep">/</span>
    <span class="breadcrumb-current">{section.title()}</span>
  </nav>
  <main class="site-main">
    <article class="content-section">
      <h1>{title}</h1>
      <p>Kostenlose Rechner für Deutschland. Berechnungen lokal im Browser.</p>
      <ul class="hub-list">
{lis}
      </ul>
      <p><a href="/{section}/">Zur Österreich-Übersicht ➔</a></p>
      <p class="updated" data-updated="{TODAY}">Zuletzt aktualisiert: {TODAY}</p>
    </article>
  </main>
  <script src="/assets/js/global.js?v=3.1"></script>
</body>
</html>
"""
        dest = BASE / f"de/{section}/index.html"
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(html, encoding="utf-8")
        print("hub", dest.relative_to(BASE))


def write_sitemap() -> int:
    BASE_URL = "https://rechnify.at"
    skip = {"scratch/", "node_modules/"}
    noindex_always = {"impressum.html", "datenschutz.html"}
    pages = []
    for p in sorted(BASE.rglob("*.html")):
        rel = p.relative_to(BASE).as_posix()
        if any(s in rel for s in skip):
            continue
        if rel in noindex_always:
            continue
        pages.append(rel)

    def loc(rel: str) -> str:
        if rel == "index.html":
            return f"{BASE_URL}/"
        if rel.endswith("/index.html"):
            return f"{BASE_URL}/{rel[:-10]}"
        return f"{BASE_URL}/{rel}"
    entries = []
    for rel in pages:
        url = loc(rel)
        # hreflang twin
        twin = None
        if rel.startswith("de/"):
            at = rel[3:]
            if (BASE / at).exists():
                twin = ("de-AT", loc(at), "de-DE", url)
        else:
            de = f"de/{rel}"
            if (BASE / de).exists():
                twin = ("de-AT", url, "de-DE", loc(de))

        if twin:
            a_lang, a_href, d_lang, d_href = twin
            xd = a_href
            block = (
                f'    <xhtml:link rel="alternate" hreflang="{a_lang}" href="{a_href}"/>\n'
                f'    <xhtml:link rel="alternate" hreflang="{d_lang}" href="{d_href}"/>\n'
                f'    <xhtml:link rel="alternate" hreflang="x-default" href="{xd}"/>'
            )
        else:
            block = (
                f'    <xhtml:link rel="alternate" hreflang="de-AT" href="{url}"/>\n'
                f'    <xhtml:link rel="alternate" hreflang="x-default" href="{url}"/>'
            )
        entries.append(
            f"""  <url>
    <loc>{url}</loc>
{block}
    <lastmod>{TODAY}</lastmod>
  </url>"""
        )

    xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
        xmlns:xhtml="http://www.w3.org/1999/xhtml">
{chr(10).join(entries)}
</urlset>
"""
    (BASE / "sitemap.xml").write_text(xml, encoding="utf-8")
    print(f"sitemap: {len(entries)} URLs")
    return len(entries)


def generate_ogs() -> int:
    from PIL import Image, ImageDraw, ImageFont

    out = BASE / "assets/images/og"
    out.mkdir(parents=True, exist_ok=True)
    n = 0

    def make(path: Path, title: str, sub: str) -> None:
        nonlocal n
        img = Image.new("RGB", (1200, 630), "#1858C7")
        d = ImageDraw.Draw(img)
        d.rectangle([0, 480, 1200, 630], fill="#0f3d8c")
        try:
            font_b = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 64)
            font_s = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 36)
        except OSError:
            font_b = ImageFont.load_default()
            font_s = font_b
        d.text((64, 180), title[:48], fill="white", font=font_b)
        d.text((64, 280), sub[:60], fill="#cfe0ff", font=font_s)
        d.text((64, 530), "rechnify.at", fill="white", font=font_s)
        img.save(path, "PNG", optimize=True)
        n += 1

    for slug, name, code in CITIES:
        make(out / f"gehalt-{slug}.png", f"Gehalt {name}", "Brutto → Netto Rechner")
    make(out / "hub-finanzen-de.png", "Finanzen DE", "Rechner-Übersicht")
    make(out / "hub-arbeitszeit-de.png", "Arbeitszeit DE", "Rechner-Übersicht")
    # also update AT hub og optional
    make(out / "hub-finanzen-at.png", "Finanzen AT", "Rechner-Übersicht")
    make(out / "hub-arbeitszeit-at.png", "Arbeitszeit AT", "Rechner-Übersicht")
    print(f"OG pngs: {n}")
    return n


def patch_misc() -> None:
    # redirects
    red = BASE / "_redirects"
    text = red.read_text(encoding="utf-8")
    extras = [
        "/finanzen /finanzen/ 301",
        "/arbeitszeit /arbeitszeit/ 301",
        "/blog /blog/ 301",
        "/de/finanzen /de/finanzen/ 301",
        "/de/arbeitszeit /de/arbeitszeit/ 301",
        "/de /de/ 301",
    ]
    for line in extras:
        if line.split()[0] not in text:
            text = text.rstrip() + "\n" + line + "\n"
    red.write_text(text, encoding="utf-8")

    # llms.txt
    (BASE / "llms.txt").write_text(
        f"""# rechnify.at

> Kostenlose Präzisionsrechner für Österreich und Deutschland. Alle Berechnungen lokal im Browser.

Site: https://rechnify.at/
Locales: de-AT (root), de-DE (/de/)
Updated: {TODAY}

## Top tools

- [Brutto-Netto Österreich](https://rechnify.at/finanzen/gehaltsrechner.html)
- [Brutto-Netto Deutschland](https://rechnify.at/de/finanzen/gehaltsrechner.html)
- [AT vs DE Vergleich](https://rechnify.at/finanzen/brutto-netto-oesterreich-vs-deutschland.html)
- [Kalorienrechner / TDEE](https://rechnify.at/alltag/kalorienrechner.html)
- [Währungsumrechner](https://rechnify.at/alltag/waehrungsumrechner.html)
- [Schulnotenrechner](https://rechnify.at/alltag/schulnotenrechner.html)
- [MwSt AT](https://rechnify.at/finanzen/mwst-rechner.html) / [MwSt DE](https://rechnify.at/de/finanzen/mwst-rechner.html)
- [Überstunden](https://rechnify.at/arbeitszeit/ueberstundenrechner.html)
- [Kommen-Gehen](https://rechnify.at/arbeitszeit/kommen-gehen-rechner.html)
- [Leasing Barkauf/Kredit](https://rechnify.at/finanzen/leasingrechner.html)
- [Kredit Tilgungsplan](https://rechnify.at/finanzen/kreditrechner.html)
- [Pendler AT](https://rechnify.at/finanzen/pendlerrechner.html)

## Hubs

- Finanzen AT: https://rechnify.at/finanzen/
- Finanzen DE: https://rechnify.at/de/finanzen/
- Arbeitszeit AT: https://rechnify.at/arbeitszeit/
- Arbeitszeit DE: https://rechnify.at/de/arbeitszeit/
- Blog: https://rechnify.at/blog/
- Embed: https://rechnify.at/embed.html

## pSEO

- Brutto-Netto Beträge AT/DE: /finanzen/brutto-netto/ und /de/finanzen/brutto-netto/
- Berufe: /finanzen/gehalt/ und /de/finanzen/gehalt/
- Städte: z.B. /finanzen/gehalt/gehalt-wien.html, /de/finanzen/gehalt/gehalt-berlin.html

## Optional

- Sitemap: https://rechnify.at/sitemap.xml
- Privacy: https://rechnify.at/datenschutz.html
""",
        encoding="utf-8",
    )

    # manifest shortcuts
    (BASE / "site.webmanifest").write_text(
        """{
  "name": "rechnify.at – Online-Rechner",
  "short_name": "rechnify",
  "description": "Kostenlose Online-Rechner für Österreich und Deutschland.",
  "start_url": "/",
  "scope": "/",
  "display": "standalone",
  "background_color": "#f6f8fc",
  "theme_color": "#1858C7",
  "lang": "de-AT",
  "icons": [
    { "src": "/assets/images/favicon-192x192.png", "sizes": "192x192", "type": "image/png", "purpose": "any" },
    { "src": "/assets/images/favicon-512x512.png", "sizes": "512x512", "type": "image/png", "purpose": "any" },
    { "src": "/assets/images/apple-touch-icon.png", "sizes": "180x180", "type": "image/png", "purpose": "any" }
  ],
  "shortcuts": [
    { "name": "Gehaltsrechner AT", "url": "/finanzen/gehaltsrechner.html", "description": "Brutto-Netto Österreich" },
    { "name": "Gehaltsrechner DE", "url": "/de/finanzen/gehaltsrechner.html", "description": "Brutto-Netto Deutschland" },
    { "name": "Kalorienrechner", "url": "/alltag/kalorienrechner.html", "description": "TDEE berechnen" },
    { "name": "Blog", "url": "/blog/", "description": "Guides & Tipps" }
  ]
}
""",
        encoding="utf-8",
    )

    # ads.txt — already has publisher; ensure newline
    ads = (BASE / "ads.txt").read_text(encoding="utf-8").strip() + "\n"
    (BASE / "ads.txt").write_text(ads, encoding="utf-8")

    # AT hub og images if present in HTML
    for hub in ("finanzen/index.html", "arbeitszeit/index.html"):
        p = BASE / hub
        t = p.read_text(encoding="utf-8")
        key = "finanzen" if "finanzen" in hub else "arbeitszeit"
        t2 = t.replace(
            'content="https://rechnify.at/assets/images/og-share.png"',
            f'content="https://rechnify.at/assets/images/og/hub-{key}-at.png"',
            1,
        )
        if t2 != t:
            p.write_text(t2, encoding="utf-8")

    print("misc patched")


def patch_homepage_blog() -> None:
    p = BASE / "index.html"
    t = p.read_text(encoding="utf-8")
    if 'href="/blog/"' not in t:
        t = t.replace(
            '<li><a href="/datenschutz.html">Datenschutz</a></li>',
            '<li><a href="/blog/">Blog</a></li>\n            <li><a href="/datenschutz.html">Datenschutz</a></li>',
            1,
        )
        t = t.replace(
            '<li><a href="/finanzen/mwst-rechner.html">MwSt-Rechner</a></li>',
            '<li><a href="/finanzen/mwst-rechner.html">MwSt-Rechner</a></li>\n            <li><a href="/blog/">Blog &amp; Guides</a></li>',
            1,
        )
        # sidebar
        if 'href="/blog/"' not in t or t.count('href="/blog/"') < 2:
            t = t.replace(
                '<a href="#alltag"><span class="icon">⚖️</span> Alltag</a>',
                '<a href="#alltag"><span class="icon">⚖️</span> Alltag</a>\n      <a href="/blog/"><span class="icon">📰</span> Blog</a>',
                1,
            )
    p.write_text(t, encoding="utf-8")
    print("homepage blog link")


def inject_last_updated() -> None:
    """Add tiny stamp via global.js once."""
    js = BASE / "assets/js/global.js"
    t = js.read_text(encoding="utf-8")
    if "injectLastUpdated" in t:
        print("last-updated already")
        return
    snippet = """
  function injectLastUpdated() {
    if (document.querySelector('.updated,[data-updated]')) return;
    const main = document.querySelector('main.site-main, main');
    if (!main || !document.querySelector('.calc-body, #resultBox, #grossMonthly, .calculator')) return;
    const el = document.createElement('p');
    el.className = 'updated help';
    el.style.cssText = 'margin-top:24px;font-size:0.85rem;color:var(--color-ink-3)';
    el.textContent = 'Zuletzt aktualisiert: 2026-07-18';
    main.appendChild(el);
  }
"""
    # call on DOMContentLoaded — find existing listener start
    if "document.addEventListener('DOMContentLoaded'" in t:
        t = t.replace(
            "document.addEventListener('DOMContentLoaded', () => {",
            "document.addEventListener('DOMContentLoaded', () => {\n  injectLastUpdated();",
            1,
        )
        # insert function before first DOMContentLoaded
        idx = t.find("document.addEventListener('DOMContentLoaded'")
        t = t[:idx] + snippet + "\n" + t[idx:]
        js.write_text(t, encoding="utf-8")
        print("last-updated inject")
    else:
        print("no DOMContentLoaded — skip")


if __name__ == "__main__":
    generate_at_amounts()
    generate_cities()
    write_de_hubs()
    generate_ogs()
    patch_misc()
    patch_homepage_blog()
    inject_last_updated()
    write_sitemap()
    print("DONE")
