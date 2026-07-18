#!/usr/bin/env python3
"""Fix all 8 SEO issues across rechnify.at (AT + DE pages).

Issues fixed:
  1. Unique content paragraph per brutto-netto page (thin content fix)
  2. og:url wrong on all 43 gehalt pages
  3. h1 generic on all 43 gehalt pages
  4. Breadcrumb text "Gehaltsrechner" instead of job name
  5. BreadcrumbList JSON-LD missing on brutto-netto + gehalt pages
  6. hreflang de-DE missing on AT brutto-netto + gehalt pages
  7. hreflang de-AT + x-default missing on AT gehalt pages
  8. Font loading blocking on AT brutto-netto pages
  9. Affiliate href="#" dead link on brutto-netto pages

Safe to re-run (idempotent checks on every mutation).
"""
import re
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent


def calc_netto_at(gross: float) -> tuple:
    sv = min(gross, 6930) * 0.1807
    base_y = (gross - sv) * 12
    if base_y > 104859:
        t = ((base_y - 104859) * 0.50 + (104859 - 70365) * 0.48
             + (70365 - 36458) * 0.40 + (36458 - 21992) * 0.30
             + (21992 - 13539) * 0.20)
    elif base_y > 70365:
        t = ((base_y - 70365) * 0.48 + (70365 - 36458) * 0.40
             + (36458 - 21992) * 0.30 + (21992 - 13539) * 0.20)
    elif base_y > 36458:
        t = ((base_y - 36458) * 0.40 + (36458 - 21992) * 0.30
             + (21992 - 13539) * 0.20)
    elif base_y > 21992:
        t = (base_y - 21992) * 0.30 + (21992 - 13539) * 0.20
    elif base_y > 13539:
        t = (base_y - 13539) * 0.20
    else:
        t = 0.0
    tax = max(0.0, t / 12 - 496 / 12)
    return round(gross - sv - tax), round(sv), round(tax)


def fmt(n: int) -> str:
    return f"{n:,}".replace(",", ".")


JOB_NAMES = {
    "abteilungsleiter":   "Abteilungsleiter",
    "anwalt":             "Rechtsanwalt",
    "apotheker":          "Apotheker",
    "architekt":          "Architekt",
    "arzt":               "Arzt/Ärztin",
    "bauingenieur":       "Bauingenieur",
    "buchhalter":         "Buchhalter",
    "controller":         "Controller",
    "data-scientist":     "Data Scientist",
    "devops":             "DevOps Engineer",
    "elektriker":         "Elektriker",
    "fahrer":             "Fahrer",
    "filialleiter":       "Filialleiter",
    "friseur":            "Friseur/Friseurin",
    "geschaeftsfuehrer":  "Geschäftsführer",
    "handwerker":         "Handwerker",
    "hr-manager":         "HR Manager",
    "ingenieur":          "Ingenieur",
    "it-admin":           "IT-Administrator",
    "kellner":            "Kellner/Kellnerin",
    "koch":               "Koch/Köchin",
    "krankenschwester":   "Krankenschwester",
    "lehrer":             "Lehrer/Lehrerin",
    "lkw-fahrer":         "LKW-Fahrer",
    "marketing-manager":  "Marketing Manager",
    "maschinenbau":       "Maschinenbauingenieur",
    "pfleger":            "Pfleger/Pflegerin",
    "physiotherapeut":    "Physiotherapeut",
    "pilot":              "Pilot/Pilotin",
    "polizist":           "Polizist/Polizistin",
    "product-manager":    "Product Manager",
    "professor":          "Professor/Professorin",
    "psychologe":         "Psychologe/Psychologin",
    "sales":              "Sales Manager",
    "sekretaerin":        "Sekretärin",
    "softwareentwickler": "Softwareentwickler",
    "sozialarbeiter":     "Sozialarbeiter/in",
    "steuerberater":      "Steuerberater/in",
    "tierarzt":           "Tierarzt/Tierärztin",
    "tischler":           "Tischler/Tischlerin",
    "ux-designer":        "UX Designer",
    "verkaeufer":         "Verkäufer/in",
    "zahnarzt":           "Zahnarzt/Zahnärztin",
}

FONT_BLOCK = ('href="https://fonts.googleapis.com/css2?family='
              'Space+Grotesk:wght@600;700&display=swap" rel="stylesheet" />')
FONT_ASYNC = ('href="https://fonts.googleapis.com/css2?family='
              'Space+Grotesk:wght@600;700&display=swap" rel="stylesheet" '
              'media="print" onload="this.media=\'all\'" />\n  '
              '<noscript><link href="https://fonts.googleapis.com/css2?family='
              'Space+Grotesk:wght@600;700&display=swap" rel="stylesheet" /></noscript>')


def fix_brutto_netto_at(path: Path) -> None:
    m = re.match(r"^(\d+)-brutto-in-netto$", path.stem)
    if not m:
        return
    amount = int(m.group(1))
    net, sv, tax = calc_netto_at(amount)
    html = path.read_text(encoding="utf-8")
    url = f"https://rechnify.at/finanzen/brutto-netto/{path.name}"
    de_url = f"https://rechnify.at/de/finanzen/brutto-netto/{path.name}"
    af = fmt(amount); nf = fmt(net); sf = fmt(sv); tf = fmt(tax)

    # 1. Fix blocking font -> async
    if FONT_BLOCK in html:
        html = html.replace('<link ' + FONT_BLOCK, '<link ' + FONT_ASYNC)

    # 2. Add hreflang de-DE
    if 'hreflang="de-DE"' not in html:
        html = html.replace(
            '  <link rel="alternate" hreflang="x-default"',
            f'  <link rel="alternate" hreflang="de-DE" href="{de_url}" />\n'
            '  <link rel="alternate" hreflang="x-default"',
        )

    # 3. BreadcrumbList JSON-LD
    if "BreadcrumbList" not in html:
        bc = (
            '  <script type="application/ld+json">\n'
            '  {"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":['
            '{"@type":"ListItem","position":1,"name":"Start","item":"https://rechnify.at/"},'
            '{"@type":"ListItem","position":2,"name":"Finanzen","item":"https://rechnify.at/finanzen/"},'
            '{"@type":"ListItem","position":3,"name":"Brutto-Netto Tabelle","item":"https://rechnify.at/finanzen/brutto-netto/"},'
            f'{{"@type":"ListItem","position":4,"name":"{af} EUR Brutto in Netto","item":"{url}"}}'
            ']}\n'
            '  </script>\n'
        )
        html = html.replace("</head>", bc + "</head>")

    # 4. Unique content section before FAQ
    if "Unique SEO Content" not in html:
        section = (
            '      <!-- Unique SEO Content -->\n'
            '      <section class="content-section" style="margin-top:32px;padding:24px;'
            'background:var(--soft);border-radius:12px;border:1px solid var(--border);">\n'
            f'        <h2>{af} \u20ac Brutto in Netto \u2013 \u00d6sterreich 2026</h2>\n'
            f'        <p>Von <strong>{af}\u00a0\u20ac Brutto</strong> bleiben in \u00d6sterreich '
            f'(Stand 2026) monatlich ca.\u00a0<strong>{nf}\u00a0\u20ac</strong> Netto \u00fcbrig. '
            f'Davon entfallen <strong>{sf}\u00a0\u20ac</strong> auf die Sozialversicherung (18,07\u00a0%) '
            f'und <strong>{tf}\u00a0\u20ac</strong> auf die Lohnsteuer \u2013 berechnet nach dem '
            'offiziellen Tarif 2026 inkl. Verkehrsabsetzbetrag.</p>\n'
            '        <p>Beim 13. und 14. Gehalt (Urlaubs-/Weihnachtsgeld) greift das Jahressechstel: '
            'Sonderzahlungen werden mit nur ca.\u00a06\u00a0% besteuert, was die j\u00e4hrliche '
            'Nettoauszahlung sp\u00fcrbar erh\u00f6ht.</p>\n'
            '        <ul>\n'
            f'          <li><strong>Monatliches Netto (12x):</strong> ca.\u00a0{nf}\u00a0\u20ac</li>\n'
            f'          <li><strong>Sozialversicherung (18,07\u00a0%):</strong> {sf}\u00a0\u20ac/Monat</li>\n'
            f'          <li><strong>Lohnsteuer:</strong> {tf}\u00a0\u20ac/Monat</li>\n'
            '          <li><strong>13./14. Gehalt:</strong> steuerlich beg\u00fcnstigt (Jahressechstel)</li>\n'
            '        </ul>\n'
            '      </section>\n\n'
        )
        html = html.replace("      <!-- FAQ Section -->", section + "      <!-- FAQ Section -->")

    # 5. Fix dead affiliate link
    html = html.replace(
        '<a href="#" target="_blank" rel="noopener" class="btn-aff">',
        '<a href="https://www.durchblicker.at/konto" target="_blank" rel="noopener sponsored" class="btn-aff">',
    )

    path.write_text(html, encoding="utf-8")


def fix_gehalt_at(path: Path) -> None:
    job_key = path.stem.replace("-gehalt-netto", "")
    job_name = JOB_NAMES.get(job_key, job_key.replace("-", " ").title())
    url = f"https://rechnify.at/finanzen/gehalt/{path.name}"
    de_url = f"https://rechnify.at/de/finanzen/gehalt/{path.name}"
    html = path.read_text(encoding="utf-8")

    # 1. Fix og:url
    html = re.sub(
        r'<meta property="og:url" content="https://rechnify\.at/finanzen/gehaltsrechner\.html" />',
        f'<meta property="og:url" content="{url}" />',
        html,
    )

    # 2. Fix h1
    html = re.sub(
        r'<h1 style="margin-bottom:8px;">Brutto Netto Rechner \u00d6sterreich</h1>',
        f'<h1 style="margin-bottom:8px;">Gehalt {job_name} \u00d6sterreich \u2013 Brutto Netto 2026</h1>',
        html,
    )

    # 3. Fix breadcrumb
    html = html.replace(
        '<span class="breadcrumb-current">Gehaltsrechner</span>',
        f'<span class="breadcrumb-current">Gehalt {job_name}</span>',
    )

    # 4. hreflang
    if 'hreflang="de-AT"' not in html:
        hreflang_block = (
            f'  <link rel="alternate" hreflang="de-AT" href="{url}" />\n'
            f'  <link rel="alternate" hreflang="de-DE" href="{de_url}" />\n'
            f'  <link rel="alternate" hreflang="x-default" href="{url}" />\n'
        )
        html = html.replace('  <meta name="robots"', hreflang_block + '  <meta name="robots"')
    elif 'hreflang="de-DE"' not in html:
        html = html.replace(
            '  <link rel="alternate" hreflang="x-default"',
            f'  <link rel="alternate" hreflang="de-DE" href="{de_url}" />\n'
            '  <link rel="alternate" hreflang="x-default"',
        )

    # 5. BreadcrumbList
    if "BreadcrumbList" not in html:
        bc = (
            '  <script type="application/ld+json">\n'
            '  {"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":['
            '{"@type":"ListItem","position":1,"name":"Start","item":"https://rechnify.at/"},'
            '{"@type":"ListItem","position":2,"name":"Finanzen","item":"https://rechnify.at/finanzen/"},'
            '{"@type":"ListItem","position":3,"name":"Gehalt","item":"https://rechnify.at/finanzen/gehalt/"},'
            f'{{"@type":"ListItem","position":4,"name":"Gehalt {job_name}","item":"{url}"}}'
            ']}\n'
            '  </script>\n'
        )
        html = html.replace("</head>", bc + "</head>")

    path.write_text(html, encoding="utf-8")


def fix_gehalt_de(path: Path) -> None:
    job_key = path.stem.replace("-gehalt-netto", "")
    job_name = JOB_NAMES.get(job_key, job_key.replace("-", " ").title())
    url = f"https://rechnify.at/de/finanzen/gehalt/{path.name}"
    html = path.read_text(encoding="utf-8")

    html = re.sub(
        r'<meta property="og:url" content="https://rechnify\.at/(?:de/)?finanzen/gehaltsrechner\.html" />',
        f'<meta property="og:url" content="{url}" />',
        html,
    )
    html = re.sub(
        r'<h1 style="margin-bottom:8px;">(?:Brutto Netto Rechner \u00d6sterreich|Brutto Netto Rechner Deutschland)</h1>',
        f'<h1 style="margin-bottom:8px;">Gehalt {job_name} Deutschland \u2013 Brutto Netto 2026</h1>',
        html,
    )
    html = html.replace(
        '<span class="breadcrumb-current">Gehaltsrechner</span>',
        f'<span class="breadcrumb-current">Gehalt {job_name}</span>',
    )

    if "BreadcrumbList" not in html:
        bc = (
            '  <script type="application/ld+json">\n'
            '  {"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":['
            '{"@type":"ListItem","position":1,"name":"Start","item":"https://rechnify.at/de/"},'
            '{"@type":"ListItem","position":2,"name":"Finanzen","item":"https://rechnify.at/de/finanzen/"},'
            '{"@type":"ListItem","position":3,"name":"Gehalt","item":"https://rechnify.at/de/finanzen/gehalt/"},'
            f'{{"@type":"ListItem","position":4,"name":"Gehalt {job_name}","item":"{url}"}}'
            ']}\n'
            '  </script>\n'
        )
        html = html.replace("</head>", bc + "</head>")

    path.write_text(html, encoding="utf-8")


def main() -> None:
    at_bn = BASE / "finanzen" / "brutto-netto"
    pages = sorted(p for p in at_bn.glob("*.html") if p.stem != "index")
    print(f"Fixing {len(pages)} AT brutto-netto pages...")
    for p in pages:
        fix_brutto_netto_at(p)

    at_g = BASE / "finanzen" / "gehalt"
    pages = sorted(at_g.glob("*.html"))
    print(f"Fixing {len(pages)} AT gehalt pages...")
    for p in pages:
        fix_gehalt_at(p)

    de_g = BASE / "de" / "finanzen" / "gehalt"
    if de_g.exists():
        pages = sorted(de_g.glob("*.html"))
        print(f"Fixing {len(pages)} DE gehalt pages...")
        for p in pages:
            fix_gehalt_de(p)

    print("Done.")


if __name__ == "__main__":
    main()
