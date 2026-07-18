#!/usr/bin/env python3
"""Generate sitemap.xml for rechnify.at — no changefreq/priority, correct hreflang."""

import os
from pathlib import Path
from datetime import date

BASE_DIR = Path(__file__).resolve().parent.parent
TODAY = date.today().isoformat()

# URL pairs: (at_path, de_path or None)
# If de_path is None, only AT/x-default
PAIRED_URLS = [
    ('/arbeitszeit/arbeitstage-rechner.html', '/de/arbeitszeit/arbeitstage-rechner.html'),
    ('/arbeitszeit/brueckentage-planer.html', '/de/arbeitszeit/brueckentage-planer.html'),
    ('/arbeitszeit/kommen-gehen-rechner.html', '/de/arbeitszeit/kommen-gehen-rechner.html'),
    ('/arbeitszeit/stundenlohn-rechner.html', '/de/arbeitszeit/stundenlohn-rechner.html'),
    ('/arbeitszeit/teilzeitrechner.html', '/de/arbeitszeit/teilzeitrechner.html'),
    ('/arbeitszeit/ueberstundenrechner.html', '/de/arbeitszeit/ueberstundenrechner.html'),
    ('/arbeitszeit/urlaubstage-rechner.html', '/de/arbeitszeit/urlaubstage-rechner.html'),
    ('/finanzen/etf-sparplan-rechner.html', '/de/finanzen/etf-sparplan-rechner.html'),
    ('/finanzen/gehaltserhoehung-rechner.html', '/de/finanzen/gehaltserhoehung-rechner.html'),
    ('/finanzen/gehaltsrechner.html', '/de/finanzen/gehaltsrechner.html'),
    ('/finanzen/kreditrechner.html', '/de/finanzen/kreditrechner.html'),
    ('/finanzen/kryptosteuerrechner.html', '/de/finanzen/kryptosteuerrechner.html'),
    ('/finanzen/leasingrechner.html', '/de/finanzen/leasingrechner.html'),
    ('/finanzen/mwst-rechner.html', '/de/finanzen/mwst-rechner.html'),
    ('/finanzen/pendlerrechner.html', '/de/finanzen/pendlerrechner.html'),
    ('/finanzen/sachbezugsrechner.html', '/de/finanzen/sachbezugsrechner.html'),
    ('/familie/kinderbetreuungsgeld.html', '/de/familie/elterngeld.html'),
]

AT_ONLY_URLS = [
    '/',
    '/alltag/altersrechner.html',
    '/alltag/bmi-rechner.html',
    '/alltag/einheitenrechner.html',
    '/alltag/kaufkraftrechner.html',
    '/arbeitszeit/schichtplan-rechner.html',
    '/arbeitszeit/ueberstunden-auszahlen-oesterreich.html',
    '/familie/schwangerschaftsrechner.html',
    '/finanzen/13-14-gehalt-oesterreich.html',
    '/finanzen/brutto-netto-oesterreich-vs-deutschland.html',
    '/finanzen/brutto-netto/',
    '/finanzen/familienbonus-rechner.html',
    '/finanzen/netto-rechner-oesterreich-2026.html',
    '/finanzen/mwst-oesterreich-vs-deutschland.html',
    '/finanzen/rabattrechner.html',
    '/finanzen/zinsrechner.html',
    '/mathematik/dreisatzrechner.html',
    '/mathematik/prozentrechner.html',
    '/mathematik/taschenrechner.html',
    '/ueber-uns.html',
    '/kontakt.html',
    '/impressum.html',
    '/datenschutz.html',
]

DE_ONLY_URLS = [
    '/de/finanzen/kirchensteuer-erklaert.html',
    '/de/finanzen/kirchensteuer-rechner.html',
    '/de/finanzen/netto-rechner-deutschland-2026.html',
]

# pSEO amount pages
AMOUNTS = list(range(1500, 6100, 100)) + [6500, 7000, 8000, 9000, 10000]

# pSEO profession pages
PROFESSIONS = [
    "architekt", "arzt", "buchhalter", "elektriker", "friseur",
    "ingenieur", "kellner", "krankenschwester", "lehrer", "lkw-fahrer",
    "marketing-manager", "polizist", "softwareentwickler", "tischler", "verkaeufer"
]

BASE = 'https://rechnify.at'

def hreflang_block(at_path, de_path):
    """Generate xhtml:link alternates for a URL entry."""
    lines = []
    lines.append(f'    <xhtml:link rel="alternate" hreflang="de-AT" href="{BASE}{at_path}"/>')
    if de_path:
        lines.append(f'    <xhtml:link rel="alternate" hreflang="de-DE" href="{BASE}{de_path}"/>')
    lines.append(f'    <xhtml:link rel="alternate" hreflang="x-default" href="{BASE}{at_path}"/>')
    return '\n'.join(lines)

def url_entry(loc, at_path, de_path=None, lastmod=TODAY):
    """Generate a single <url> entry."""
    if de_path:
        block = hreflang_block(at_path, de_path)
    else:
        block = f'    <xhtml:link rel="alternate" hreflang="de-AT" href="{loc}"/>\n    <xhtml:link rel="alternate" hreflang="x-default" href="{loc}"/>'
    return f"""  <url>
    <loc>{loc}</loc>
{block}
    <lastmod>{lastmod}</lastmod>
  </url>"""

def generate_sitemap():
    entries = []
    
    # Homepage
    entries.append(url_entry(f'{BASE}/', '/', '/de/', TODAY))
    
    # Paired URLs (AT + DE versions)
    for at_path, de_path in PAIRED_URLS:
        entries.append(url_entry(f'{BASE}{at_path}', at_path, de_path, TODAY))
    
    # AT-only URLs
    for path in AT_ONLY_URLS:
        if path == '/':
            continue  # already added
        entries.append(url_entry(f'{BASE}{path}', path, None, TODAY))
    
    # DE-only URLs
    for path in DE_ONLY_URLS:
        entries.append(url_entry(f'{BASE}{path}', path, None, TODAY))
    
    # pSEO amount pages AT
    for amount in AMOUNTS:
        at_path = f'/finanzen/brutto-netto/{amount}-brutto-in-netto.html'
        de_path = f'/de/finanzen/brutto-netto/{amount}-brutto-in-netto.html'
        entries.append(url_entry(f'{BASE}{at_path}', at_path, de_path, TODAY))
    
    # pSEO amount pages DE (separate entries for DE versions)
    for amount in AMOUNTS:
        de_path = f'/de/finanzen/brutto-netto/{amount}-brutto-in-netto.html'
        at_path = f'/finanzen/brutto-netto/{amount}-brutto-in-netto.html'
        entries.append(url_entry(f'{BASE}{de_path}', at_path, de_path, TODAY))
    
    # pSEO profession pages AT
    for prof in PROFESSIONS:
        at_path = f'/finanzen/gehalt/{prof}-gehalt-netto.html'
        de_path = f'/de/finanzen/gehalt/{prof}-gehalt-netto.html'
        entries.append(url_entry(f'{BASE}{at_path}', at_path, de_path, TODAY))
    
    # pSEO profession pages DE
    for prof in PROFESSIONS:
        at_path = f'/finanzen/gehalt/{prof}-gehalt-netto.html'
        de_path = f'/de/finanzen/gehalt/{prof}-gehalt-netto.html'
        entries.append(url_entry(f'{BASE}{de_path}', at_path, de_path, TODAY))
    
    # Brutto-netto index pages
    entries.append(url_entry(f'{BASE}/finanzen/brutto-netto/', '/finanzen/brutto-netto/', None, TODAY))
    entries.append(url_entry(f'{BASE}/de/finanzen/brutto-netto/', '/de/finanzen/brutto-netto/', None, TODAY))
    
    xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
        xmlns:xhtml="http://www.w3.org/1999/xhtml">
{chr(10).join(entries)}
</urlset>"""
    
    sitemap_path = BASE_DIR / 'sitemap.xml'
    with open(sitemap_path, 'w', encoding='utf-8') as f:
        f.write(xml)
    
    print(f"Generated sitemap.xml with {len(entries)} URLs (no changefreq/priority, correct hreflang)")

if __name__ == '__main__':
    generate_sitemap()