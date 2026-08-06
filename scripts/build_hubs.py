#!/usr/bin/env python3
"""Generiert die Hub-/Kategorieseiten von rechnify.at.

Hubs sind der Klebstoff der Seitenstruktur: sie geben jeder Unterseite
einen internen Eingangslink, machen Verzeichnis-URLs abrufbar statt 404
und buendeln Themen fuer Suchmaschinen.

Die Rechner-Listen werden aus den vorhandenen Dateien gelesen (Titel +
h1), damit Hub und Bestand nicht auseinanderlaufen.

Aufruf:  python3 scripts/build_hubs.py
"""
from __future__ import annotations

import html
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://rechnify.at"

RE_H1 = re.compile(r"<h1[^>]*>(.*?)</h1>", re.S)
RE_TITLE = re.compile(r"<title>(.*?)</title>", re.S)
RE_DESC = re.compile(r'name="description"\s+content="(.*?)"', re.S)
RE_TAGS = re.compile(r"<[^>]+>")


def page_meta(rel: str) -> dict[str, str]:
    """Liest Ueberschrift und Beschreibung einer bestehenden Seite."""
    with open(os.path.join(ROOT, rel), encoding="utf-8", errors="ignore") as fh:
        raw = fh.read()
    h1 = RE_H1.search(raw)
    title = RE_TITLE.search(raw)
    desc = RE_DESC.search(raw)
    label = RE_TAGS.sub("", h1.group(1)).strip() if h1 else ""
    if not label and title:
        label = title.group(1).split("|")[0].strip()
    return {
        "label": html.unescape(label),
        "desc": html.unescape(desc.group(1).strip()) if desc else "",
    }


def list_pages(directory: str, exclude: tuple[str, ...] = ()) -> list[str]:
    full = os.path.join(ROOT, directory)
    if not os.path.isdir(full):
        return []
    out = []
    for name in sorted(os.listdir(full)):
        if not name.endswith(".html") or name == "index.html" or name in exclude:
            continue
        out.append(f"{directory}/{name}")
    return out


def first_sentence(text: str, limit: int = 120) -> str:
    """Kuerzt auf den ersten Satz, sonst auf die letzte ganze Wortgrenze."""
    text = text.strip()
    cut = text.find(". ")
    if 0 < cut <= limit:
        return text[: cut + 1]
    if len(text) <= limit:
        return text
    return text[:limit].rsplit(" ", 1)[0].rstrip(",;:") + " …"


def link_list(rels: list[str], with_desc: bool = True) -> str:
    items = []
    for rel in rels:
        meta = page_meta(rel)
        desc = ""
        if with_desc and meta["desc"]:
            desc = f' <span class="hub-list-desc">{html.escape(first_sentence(meta["desc"]))}</span>'
        items.append(f'        <li><a href="/{rel}">{html.escape(meta["label"])}</a>{desc}</li>')
    return "\n".join(items)


HEADER_NAV = """      <nav class="site-nav" id="siteNav">
        <a href="/">🏠 Start</a>
        <a href="/#finanzen">💶 Finanzen</a>
        <a href="/#arbeitszeit">⏰ Arbeitszeit</a>
        <a href="/#familie">👶 Familie</a>
        <a href="/#mathematik">📐 Mathematik</a>
        <a href="/#alltag">⚖️ Alltag</a>
      </nav>"""


def render(
    *,
    path: str,
    lang: str,
    title: str,
    description: str,
    h1: str,
    intro: str,
    sections: list[tuple[str, str, str]],
    breadcrumb: list[tuple[str, str]],
    hreflang: dict[str, str] | None = None,
) -> str:
    """Baut eine Hub-Seite. `sections` = (Ueberschrift, Text, Listen-HTML)."""
    url = f"{SITE}/{path.replace('index.html', '')}"
    alt = ""
    if hreflang:
        alt = "\n".join(
            f'  <link rel="alternate" hreflang="{k}" href="{v}" />' for k, v in hreflang.items()
        )
        alt += "\n"

    crumbs = ""
    for label, href in breadcrumb:
        crumbs += f'    <a href="{href}">{label}</a><span class="breadcrumb-sep">/</span>\n'

    body_sections = ""
    for heading, text, links in sections:
        body_sections += f"      <h2>{heading}</h2>\n"
        if text:
            body_sections += f"      <p>{text}</p>\n"
        body_sections += f'      <ul class="hub-list">\n{links}\n      </ul>\n'

    breadcrumb_items = []
    for i, (label, href) in enumerate(breadcrumb, start=1):
        target = SITE + "/" if href == "/" else SITE + href
        breadcrumb_items.append(
            f'{{"@type":"ListItem","position":{i},"name":"{label}","item":"{target}"}}'
        )
    breadcrumb_items.append(
        f'{{"@type":"ListItem","position":{len(breadcrumb) + 1},"name":"{h1}","item":"{url}"}}'
    )

    return f"""<!DOCTYPE html>
<html lang="{lang}">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{title}</title>
  <meta name="description" content="{description}" />
  <link rel="canonical" href="{url}" />
  <meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1" />
{alt}  <meta property="og:type" content="website" />
  <meta property="og:title" content="{title}" />
  <meta property="og:description" content="{description}" />
  <meta property="og:url" content="{url}" />
  <meta property="og:image" content="{SITE}/assets/images/og-share.png" />
  <meta name="twitter:card" content="summary_large_image" />
  <meta property="og:locale" content="{'de_AT' if lang == 'de-AT' else 'de_DE'}" />
  <meta property="og:site_name" content="rechnify.at" />
  <link rel="icon" href="/assets/images/favicon.ico" sizes="48x48" />
  <link rel="apple-touch-icon" sizes="180x180" href="/assets/images/apple-touch-icon.png" />
  <link rel="manifest" href="/site.webmanifest" />
  <meta name="theme-color" content="#1858C7" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@600;700&display=swap" rel="stylesheet" media="print" onload="this.media='all'" />
  <noscript><link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@600;700&display=swap" rel="stylesheet" /></noscript>
  <link rel="stylesheet" href="/tokens.css?v=1.2" />
  <link rel="stylesheet" href="/assets/css/global.css?v=3.1" media="print" onload="this.media='all'" />
  <noscript><link rel="stylesheet" href="/assets/css/global.css?v=3.1" /></noscript>
  <script type="application/ld+json">
  {{"@context":"https://schema.org","@type":"CollectionPage","name":"{h1}","url":"{url}","description":"{description}","isPartOf":{{"@type":"WebSite","name":"rechnify.at","url":"{SITE}/"}}}}
  </script>
  <script type="application/ld+json">
  {{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{','.join(breadcrumb_items)}]}}
  </script>
</head>
<body>
  <header class="site-header">
    <div class="header-inner">
      <a href="/" class="site-logo" aria-label="rechnify.at – Startseite">
        <picture><source srcset="/assets/images/logo-72.webp" type="image/webp" /><img src="/assets/images/logo-72.jpg" alt="rechnify Logo" width="36" height="36" decoding="async" /></picture>
        <span class="site-logo-text">rechnify<span>.at</span></span>
      </a>
{HEADER_NAV}
      <div class="header-actions">
        <button class="btn-icon" id="darkModeToggle" aria-label="Dunkelmodus aktivieren" type="button">🌙</button>
      </div>
    </div>
  </header>
  <nav class="breadcrumb" aria-label="Brotkrumen">
{crumbs}    <span class="breadcrumb-current">{h1}</span>
  </nav>
  <main class="site-main">
    <article class="content-section">
      <h1>{h1}</h1>
      <p class="subtitle">{intro}</p>
{body_sections}      <p class="help" style="margin-top:24px;">Alle Berechnungen sind Orientierungswerte und ersetzen keine Beratung. Stand: 2026.</p>
    </article>
  </main>
  <footer class="site-footer">
    <div class="footer-inner">
      <div class="footer-grid">
        <div class="footer-brand">
          <span class="site-logo-text">rechnify<span>.at</span></span>
          <p>Kostenlose Online-Rechner für Österreich &amp; Deutschland.</p>
        </div>
        <div class="footer-col">
          <h3>Beliebt</h3>
          <ul>
            <li><a href="/finanzen/gehaltsrechner.html">Gehaltsrechner AT</a></li>
            <li><a href="/de/finanzen/gehaltsrechner.html">Gehaltsrechner DE</a></li>
            <li><a href="/arbeitszeit/ueberstundenrechner.html">Überstundenrechner</a></li>
          </ul>
        </div>
        <div class="footer-col">
          <h3>Info</h3>
          <ul>
            <li><a href="/ueber-uns.html">Über uns</a></li>
            <li><a href="/kontakt.html">Kontakt</a></li>
            <li><a href="/impressum.html">Impressum</a></li>
            <li><a href="/datenschutz.html">Datenschutz</a></li>
          </ul>
        </div>
      </div>
    </div>
  </footer>
  <script src="/assets/js/analytics.js?v=3.1"></script>
  <script src="/assets/js/ui.js?v=3.1"></script>
  <script src="/assets/js/core.js?v=3.1"></script>
</body>
</html>
"""


def split_gehalt(directory: str) -> tuple[list[str], list[str]]:
    """Trennt Stadt- von Berufsseiten."""
    pages = list_pages(directory)
    cities = [p for p in pages if os.path.basename(p).startswith("gehalt-")]
    jobs = [p for p in pages if p not in cities]
    return cities, jobs


def build() -> int:
    written = []

    def write(path: str, content: str) -> None:
        full = os.path.join(ROOT, path)
        os.makedirs(os.path.dirname(full), exist_ok=True)
        with open(full, "w", encoding="utf-8") as fh:
            fh.write(content)
        written.append(path)

    home = ("Start", "/")

    # ---- alltag ----
    write(
        "alltag/index.html",
        render(
            path="alltag/index.html",
            lang="de-AT",
            title="Alltag & Gesundheit Rechner 2026 | rechnify.at",
            description="Kostenlose Rechner für den Alltag: BMI, Kalorienbedarf, Stromkosten, Währungen, Schulnoten, Einheiten und Alter. Lokal im Browser.",
            h1="Alltag & Gesundheit Rechner",
            intro="Rechner für den Alltag: Gesundheit, Energie, Geld und Schule. Alle Berechnungen laufen lokal in deinem Browser, ohne Datenweitergabe.",
            sections=[
                (
                    "Alle Alltagsrechner",
                    "Von Körperwerten über Haushaltskosten bis zu Umrechnungen – hier findest du die Rechner für alltägliche Fragen.",
                    link_list(list_pages("alltag")),
                ),
            ],
            breadcrumb=[home],
            hreflang={"de-AT": f"{SITE}/alltag/", "x-default": f"{SITE}/alltag/"},
        ),
    )

    # ---- familie ----
    write(
        "familie/index.html",
        render(
            path="familie/index.html",
            lang="de-AT",
            title="Familien-Rechner Österreich 2026 | rechnify.at",
            description="Rechner rund um Familie und Kinder in Österreich: Kinderbetreuungsgeld, Schwangerschaft, Studienbeitrag. Kostenlos und ohne Anmeldung.",
            h1="Familien-Rechner Österreich",
            intro="Rechner rund um Kinder, Geburt und Ausbildung in Österreich. Für Deutschland gibt es eigene Varianten.",
            sections=[
                (
                    "Familie & Kinder in Österreich",
                    "Berechne Geldleistungen und Termine rund um Familiengründung und Ausbildung.",
                    link_list(list_pages("familie")),
                ),
                (
                    "Für Deutschland",
                    "Die deutschen Entsprechungen mit den dort gültigen Regeln.",
                    '        <li><a href="/de/familie/">Familien-Rechner Deutschland</a></li>\n'
                    + link_list(list_pages("de/familie")),
                ),
                (
                    "AT und DE im Vergleich",
                    "Wo die beiden Systeme sich unterscheiden.",
                    '        <li><a href="/finanzen/kinderbetreuungsgeld-vs-elterngeld.html">'
                    "Kinderbetreuungsgeld (AT) vs Elterngeld (DE)</a></li>",
                ),
            ],
            breadcrumb=[home],
            hreflang={
                "de-AT": f"{SITE}/familie/",
                "de-DE": f"{SITE}/de/familie/",
                "x-default": f"{SITE}/familie/",
            },
        ),
    )

    # ---- de/familie ----
    write(
        "de/familie/index.html",
        render(
            path="de/familie/index.html",
            lang="de-DE",
            title="Familien-Rechner Deutschland 2026 | rechnify.at",
            description="Rechner rund um Familie und Kinder in Deutschland: Elterngeld und Basiselterngeld berechnen. Kostenlos, lokal im Browser.",
            h1="Familien-Rechner Deutschland",
            intro="Rechner rund um Kinder und Elternzeit nach deutschem Recht.",
            sections=[
                (
                    "Familie & Kinder in Deutschland",
                    "Berechne Elterngeld und plane die Elternzeit.",
                    link_list(list_pages("de/familie")),
                ),
                (
                    "Für Österreich",
                    "Die österreichischen Entsprechungen findest du hier.",
                    '        <li><a href="/familie/">Familien-Rechner Österreich</a></li>\n'
                    + link_list(list_pages("familie")),
                ),
                (
                    "DE und AT im Vergleich",
                    "Wo die beiden Systeme sich unterscheiden.",
                    '        <li><a href="/finanzen/kinderbetreuungsgeld-vs-elterngeld.html">'
                    "Kinderbetreuungsgeld (AT) vs Elterngeld (DE)</a></li>",
                ),
            ],
            breadcrumb=[home],
            hreflang={
                "de-AT": f"{SITE}/familie/",
                "de-DE": f"{SITE}/de/familie/",
                "x-default": f"{SITE}/familie/",
            },
        ),
    )

    # ---- mathematik ----
    write(
        "mathematik/index.html",
        render(
            path="mathematik/index.html",
            lang="de-AT",
            title="Mathematik-Rechner online 2026 | rechnify.at",
            description="Kostenlose Mathematik-Rechner: Prozentrechner, Dreisatz und Taschenrechner mit Verlauf. Direkt im Browser, ohne Installation.",
            h1="Mathematik-Rechner",
            intro="Die Klassiker für Schule, Studium und Beruf. Ohne Installation, direkt im Browser.",
            sections=[
                (
                    "Alle Mathematik-Rechner",
                    "Prozente, Verhältnisse und allgemeine Berechnungen.",
                    link_list(list_pages("mathematik")),
                ),
            ],
            breadcrumb=[home],
            hreflang={"de-AT": f"{SITE}/mathematik/", "x-default": f"{SITE}/mathematik/"},
        ),
    )

    # ---- de/ Landing ----
    write(
        "de/index.html",
        render(
            path="de/index.html",
            lang="de-DE",
            title="Rechner für Deutschland 2026 – Brutto Netto, Arbeitszeit | rechnify.at",
            description="Alle Rechner für Deutschland 2026: Brutto-Netto-Gehaltsrechner, Kirchensteuer, Pendlerpauschale, Arbeitszeit und Elterngeld. Kostenlos.",
            h1="Rechner für Deutschland",
            intro="Alle Rechner nach deutschem Steuer- und Arbeitsrecht, Stand 2026. Für Österreich gibt es eigene Varianten mit AT-Regeln.",
            sections=[
                (
                    "Bereiche im Überblick",
                    "Die deutschen Kategorien auf einen Blick.",
                    '        <li><a href="/de/finanzen/">Finanzen &amp; Steuern Deutschland</a></li>\n'
                    '        <li><a href="/de/arbeitszeit/">Arbeitszeit Deutschland</a></li>\n'
                    '        <li><a href="/de/familie/">Familie Deutschland</a></li>\n'
                    '        <li><a href="/de/finanzen/gehalt/">Gehalt nach Beruf &amp; Stadt</a></li>\n'
                    '        <li><a href="/de/finanzen/brutto-netto/">Brutto-Netto nach Betrag</a></li>',
                ),
                (
                    "Finanzen & Steuern",
                    "Brutto-Netto, Kirchensteuer, Pendlerpauschale und weitere Steuerthemen für Deutschland.",
                    link_list(list_pages("de/finanzen")),
                ),
                (
                    "Arbeitszeit",
                    "Arbeitszeit, Überstunden und Stundenlohn nach deutschem Arbeitsrecht.",
                    link_list(list_pages("de/arbeitszeit")),
                ),
                (
                    "Familie",
                    "Elterngeld und Familienleistungen in Deutschland.",
                    link_list(list_pages("de/familie")),
                ),
            ],
            breadcrumb=[home],
            hreflang={
                "de-DE": f"{SITE}/de/",
                "de-AT": f"{SITE}/",
                "x-default": f"{SITE}/",
            },
        ),
    )

    # ---- finanzen/gehalt (AT) ----
    cities_at, jobs_at = split_gehalt("finanzen/gehalt")
    write(
        "finanzen/gehalt/index.html",
        render(
            path="finanzen/gehalt/index.html",
            lang="de-AT",
            title="Gehalt nach Beruf & Stadt Österreich 2026 | rechnify.at",
            description="Was verdient man in Österreich? Durchschnittsgehälter nach Beruf und Stadt, jeweils mit Brutto-Netto-Berechnung für 2026.",
            h1="Gehalt nach Beruf & Stadt in Österreich",
            intro="Durchschnittsgehälter für Österreich, jeweils direkt mit Brutto-Netto-Berechnung inklusive 13. und 14. Gehalt.",
            sections=[
                (
                    "Gehalt nach Stadt",
                    "Regionale Gehaltsunterschiede in den größten Städten Österreichs.",
                    link_list(cities_at, with_desc=False),
                ),
                (
                    "Gehalt nach Beruf",
                    "Typische Bruttogehälter je Berufsbild und was davon netto übrig bleibt.",
                    link_list(jobs_at, with_desc=False),
                ),
                (
                    "Freie Berechnung",
                    "Dein Gehalt ist nicht dabei? Nutze den freien Rechner.",
                    '        <li><a href="/finanzen/gehaltsrechner.html">Brutto-Netto-Rechner Österreich</a></li>\n'
                    '        <li><a href="/finanzen/brutto-netto/">Brutto-Netto nach Betrag</a></li>',
                ),
            ],
            breadcrumb=[home, ("Finanzen", "/finanzen/")],
            hreflang={
                "de-AT": f"{SITE}/finanzen/gehalt/",
                "de-DE": f"{SITE}/de/finanzen/gehalt/",
                "x-default": f"{SITE}/finanzen/gehalt/",
            },
        ),
    )

    # ---- de/finanzen/gehalt ----
    cities_de, jobs_de = split_gehalt("de/finanzen/gehalt")
    write(
        "de/finanzen/gehalt/index.html",
        render(
            path="de/finanzen/gehalt/index.html",
            lang="de-DE",
            title="Gehalt nach Beruf & Stadt Deutschland 2026 | rechnify.at",
            description="Was verdient man in Deutschland? Durchschnittsgehälter nach Beruf und Stadt, jeweils mit Brutto-Netto-Berechnung für 2026.",
            h1="Gehalt nach Beruf & Stadt in Deutschland",
            intro="Durchschnittsgehälter für Deutschland, jeweils direkt mit Brutto-Netto-Berechnung nach deutschem Steuerrecht.",
            sections=[
                (
                    "Gehalt nach Stadt",
                    "Regionale Gehaltsunterschiede in den größten deutschen Städten.",
                    link_list(cities_de, with_desc=False),
                ),
                (
                    "Gehalt nach Beruf",
                    "Typische Bruttogehälter je Berufsbild und das resultierende Netto.",
                    link_list(jobs_de, with_desc=False),
                ),
                (
                    "Freie Berechnung",
                    "Dein Gehalt ist nicht dabei? Nutze den freien Rechner.",
                    '        <li><a href="/de/finanzen/gehaltsrechner.html">Brutto-Netto-Rechner Deutschland</a></li>\n'
                    '        <li><a href="/de/finanzen/brutto-netto/">Brutto-Netto nach Betrag</a></li>',
                ),
            ],
            breadcrumb=[home, ("Deutschland", "/de/"), ("Finanzen", "/de/finanzen/")],
            hreflang={
                "de-AT": f"{SITE}/finanzen/gehalt/",
                "de-DE": f"{SITE}/de/finanzen/gehalt/",
                "x-default": f"{SITE}/finanzen/gehalt/",
            },
        ),
    )

    for path in written:
        print("geschrieben:", path)
    print(f"\n{len(written)} Hub-Seiten erzeugt.")
    return 0


if __name__ == "__main__":
    sys.exit(build())
