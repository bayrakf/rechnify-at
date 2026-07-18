import os
import re
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent

# Step 1: Amounts for DE
DE_SOURCE = BASE_DIR / 'de' / 'finanzen' / 'gehaltsrechner.html'
DE_TARGET_DIR = BASE_DIR / 'de' / 'finanzen' / 'brutto-netto'
DE_TARGET_DIR.mkdir(parents=True, exist_ok=True)

AMOUNTS = list(range(1500, 5010, 10)) + list(range(5200, 6100, 100)) + [6500, 7000, 8000, 9000, 10000]

def generate_unique_content(amount, formatted_amount, country_name, country_code):
    """Generate unique SEO content for each pSEO page."""
    # Categorize amount
    if amount < 2000:
        category = "Einstiegsgehalt"
        context = "im unteren Einkommensbereich"
        comparison = "unter dem österreichischen Median"
    elif amount < 3000:
        category = "unteres Mittelfeld"
        context = "im unteren bis mittleren Einkommensbereich"
        comparison = "nahe dem österreichischen Median"
    elif amount < 4000:
        category = "mittleres Einkommen"
        context = "im mittleren Einkommensbereich"
        comparison = "um den österreichischen Median"
    elif amount < 5000:
        category = "gehobenes Mittelfeld"
        context = "im gehobenen mittleren Einkommensbereich"
        comparison = "über dem österreichischen Median"
    elif amount < 6000:
        category = "hohes Einkommen"
        context = "im oberen Einkommensbereich"
        comparison = "deutlich über dem österreichischen Median"
    else:
        category = "Spitzenverdiener"
        context = "im obersten Einkommensbereich"
        comparison = "weit über dem österreichischen Median"

    sv_rate = 18.07 if country_code == "at" else 0
    sv_amount = amount * 0.1807 if country_code == "at" else 0

    content = f'''
      <!-- Unique SEO Content -->
      <section class="content-section" style="margin-top: 32px;">
        <h2>Was bedeutet {formatted_amount} € Brutto in {country_name}?</h2>
        <p>Ein Bruttogehalt von {formatted_amount} € pro Monat fällt in {country_name} in die Kategorie <strong>{category}</strong>. Das bedeutet: Du liegst {comparison} von ca. 3.650 € (Median Vollzeit, Stand 2024/2025).{' Bei diesem Einkommen ist die Steuerprogression bereits spürbar.' if amount > 3000 else ' Bei diesem Einkommen ist die Steuerbelastung noch moderat.'}</p>
        
        <h3>So setzt sich dein Netto zusammen</h3>
        <p>Von deinen {formatted_amount} € Brutto werden folgende Abzüge berechnet:</p>
        <ul>
          <li><strong>Sozialversicherung (SV):</strong> ca. {sv_amount:.0f} € ({sv_rate:.2f}% des Bruttos){' – gedeckelt bis zur Höchstbeitragsgrundlage von 6.930 €' if country_code == 'at' else ''}</li>
          <li><strong>Lohnsteuer:</strong> Progressiver Steuertarif, abhängig von der Steuerstufe</li>
          <li><strong>Verkehrsabsetzbetrag:</strong> Wird steuermindernd berücksichtigt (nur AT)</li>
        </ul>
        <p>Das <strong>Netto-Gehalt</strong> ist der Betrag, der tatsächlich auf dein Konto überwiesen wird. Verwende den Rechner oben, um die exakte Summe zu sehen.</p>
        
        <h3>{formatted_amount} € Brutto – Jahresübersicht</h3>
        <p>Bei {formatted_amount} € monatlichem Brutto ergeben sich folgende Jahreswerte:</p>
        <ul>
          <li><strong>Brutto pro Jahr (14 Gehälter):</strong> ca. {(amount * 14):,} € (inkl. 13./14. Gehalt)</li>
          <li><strong>Brutto pro Jahr (12 Gehälter):</strong> ca. {(amount * 12):,} € (ohne Sonderzahlungen)</li>
          <li><strong>Netto pro Jahr:</strong> Siehe Rechner-Ergebnis oben</li>
        </ul>
        
        <h3>Steuerliche Besonderheiten bei {formatted_amount} €</h3>
        <p>{'Bei diesem Einkommen liegt dein Jahressechstel bei ca. ' + f'{amount * 12 / 6:.0f} €' + '. Das bedeutet: Deine 13. und 14. Gehaltszahlungen werden bis zu dieser Grenze mit nur 6% besteuert – ein erheblicher Steuervorteil gegenüber dem laufenden Gehalt.' if country_code == 'at' else 'In Deutschland greift der progressive Einkommensteuertarif. Bei diesem Einkommen befindest du dich in einer mittleren Steuerstufe. Kirchensteuer und Solidaritätszuschlag können zusätzlich anfallen.'}</p>
        
        <h3>Vergleich mit anderen Gehältern</h3>
        <p>Wie schneidet {formatted_amount} € im Vergleich ab? Hier eine Übersicht:</p>
        <ul>
          <li><a href="/{'de/' if country_code == 'de' else ''}finanzen/brutto-netto/{max(1500, amount - 100)}-brutto-in-netto.html">{max(1500, amount - 100)} € Brutto → Netto</a></li>
          <li><a href="/{'de/' if country_code == 'de' else ''}finanzen/brutto-netto/{min(10000, amount + 100)}-brutto-in-netto.html">{min(10000, amount + 100)} € Brutto → Netto</a></li>
          <li><a href="/{'de/' if country_code == 'de' else ''}finanzen/brutto-netto/3000-brutto-in-netto.html">3.000 € Brutto → Netto (Median-Nähe)</a></li>
          <li><a href="/{'de/' if country_code == 'de' else ''}finanzen/brutto-netto/5000-brutto-in-netto.html">5.000 € Brutto → Netto (gehobenes Einkommen)</a></li>
        </ul>
        
        <h3>Tipps für {formatted_amount} € Brutto</h3>
        <p>Bei einem Bruttogehalt von {formatted_amount} € solltest du folgende Aspekte beachten:</p>
        <ul>
          <li><strong>Gehaltsverhandlung:</strong>{' Prüfe, ob du Pendlerpauschale oder Familienbonus Plus geltend machen kannst.' if country_code == 'at' else ' Prüfe, ob du Werbungskosten oder Sonderausgaben geltend machen kannst.'}</li>
          <li><strong>Lohnnebenkosten:</strong> Dein Arbeitgeber zahlt zusätzlich ca. {(amount * 0.30):.0f} € an Lohnnebenkosten (SV-Dienstgeberanteil, Kommunalsteuer etc.)</li>
          <li><strong>Kaufkraft:</strong> Bei 2,5% Inflation pro Jahr verliert dein Netto in 5 Jahren ca. {(amount * 0.12):.0f} € an Kaufkraft</li>
          <li><strong>Altersvorsorge:</strong>{' Bei diesem Einkommen lohnt sich die freiwillige Höherversicherung oder ein privater Pensionsfonds.' if amount > 3000 else ' Prüfe die staatliche Pensionskasse und überlege eine freiwillige Zusatzversicherung.'}</li>
        </ul>
      </section>
'''
    return content

def generate_de_amounts():
    with open(DE_SOURCE, 'r', encoding='utf-8') as f:
        template = f.read()

    for amount in AMOUNTS:
        formatted_amount = f"{amount:,}".replace(',', '.')
        
        # Replace Title
        html = re.sub(r'<title>.*?</title>', f'<title>{formatted_amount} € Brutto in Netto Deutschland | rechnify.at</title>', template)
        
        # Replace Description
        desc = f'Wie viel Netto bleibt von {formatted_amount} € Brutto in Deutschland? Berechne sofort Steuern, SV und dein Gehalt für 2026.'
        html = re.sub(r'<meta name="description" content=".*?" />', f'<meta name="description" content="{desc}" />', html)
        html = re.sub(r'<meta property="og:title" content=".*?" />', f'<meta property="og:title" content="{formatted_amount} € Brutto in Netto Deutschland" />', html)
        html = re.sub(r'<meta property="og:description" content=".*?" />', f'<meta property="og:description" content="{desc}" />', html)
        
        # Canonical tag
        new_canonical = f'https://rechnify.at/de/finanzen/brutto-netto/{amount}-brutto-in-netto.html'
        html = re.sub(r'<link rel="canonical" href=".*?" />', f'<link rel="canonical" href="{new_canonical}" />', html)
        
        # Remove hreflang links
        html = re.sub(r'<link rel="alternate" hreflang="de-AT".*?/>\n?', '', html)
        html = re.sub(r'<link rel="alternate" hreflang="de-DE".*?/>\n?', '', html)
        html = re.sub(r'<link rel="alternate" hreflang="x-default".*?/>\n?', '', html)
        
        # Replace H1
        html = re.sub(r'<h1>.*?</h1>', f'<h1>{formatted_amount} € Brutto in Netto</h1>', html)
        
        # Replace the sub-paragraph
        html = re.sub(r'<p>Berechne dein exaktes Netto-Gehalt.*?für Deutschland.</p>', f'<p>Wie viel Netto bleibt von {formatted_amount} € Brutto in Deutschland?</p>', html)
        
        # Inject the value into the input field
        html = html.replace('<input type="number" id="grossMonthly" placeholder="z.B. 3500" min="0" step="100">', f'<input type="number" id="grossMonthly" value="{amount}" min="0" step="100">')
        
        # Add unique content before FAQ section
        unique_content = generate_unique_content(amount, formatted_amount, "Deutschland", "de")
        html = html.replace('<!-- FAQ Section -->', unique_content + '\n      <!-- FAQ Section -->')
        
        # Add auto-click script
        html = html.replace('</body>', "<script>document.addEventListener('DOMContentLoaded', () => { setTimeout(() => { const btn = document.getElementById('calculate'); if(btn) btn.click(); }, 100); });</script></body>")
        
        filepath = DE_TARGET_DIR / f"{amount}-brutto-in-netto.html"
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html)
            
    print(f"Generated {len(AMOUNTS)} pSEO pages for Germany amounts.")

# Step 2: Professions for AT and DE
PROFESSIONS = {
    "lehrer": {"name": "Lehrer", "amount": 3600},
    "softwareentwickler": {"name": "Softwareentwickler", "amount": 4200},
    "krankenschwester": {"name": "Krankenschwester", "amount": 3200},
    "polizist": {"name": "Polizist", "amount": 3100},
    "kellner": {"name": "Kellner", "amount": 1900},
    "arzt": {"name": "Arzt", "amount": 5800},
    "elektriker": {"name": "Elektriker", "amount": 2700},
    "tischler": {"name": "Tischler", "amount": 2500},
    "buchhalter": {"name": "Buchhalter", "amount": 3200},
    "verkaeufer": {"name": "Verkäufer", "amount": 2100},
    "marketing-manager": {"name": "Marketing Manager", "amount": 3800},
    "architekt": {"name": "Architekt", "amount": 4000},
    "ingenieur": {"name": "Ingenieur", "amount": 4500},
    "lkw-fahrer": {"name": "LKW-Fahrer", "amount": 2400},
    "friseur": {"name": "Friseur", "amount": 1800},
    "pfleger": {"name": "Pflegekraft", "amount": 2800},
    "koch": {"name": "Koch", "amount": 2400},
    "anwalt": {"name": "Anwalt", "amount": 5500},
    "steuerberater": {"name": "Steuerberater", "amount": 6000},
    "apotheker": {"name": "Apotheker", "amount": 5200},
    "psychologe": {"name": "Psychologe", "amount": 4500},
    "maschinenbau": {"name": "Maschinenbauer", "amount": 4300},
    "bauingenieur": {"name": "Bauingenieur", "amount": 4000},
    "pilot": {"name": "Pilot", "amount": 8500},
    "zahnarzt": {"name": "Zahnarzt", "amount": 7500},
    "tierarzt": {"name": "Tierarzt", "amount": 5000},
    "professor": {"name": "Professor", "amount": 6500},
    "data-scientist": {"name": "Data Scientist", "amount": 5000},
    "product-manager": {"name": "Product Manager", "amount": 5500},
    "controller": {"name": "Controller", "amount": 3800},
    "filialleiter": {"name": "Filialleiter", "amount": 3200},
    "abteilungsleiter": {"name": "Abteilungsleiter", "amount": 5000},
    "geschaeftsfuehrer": {"name": "Geschäftsführer", "amount": 8000},
    "it-admin": {"name": "IT-Administrator", "amount": 3900},
    "devops": {"name": "DevOps-Engineer", "amount": 4600},
    "ux-designer": {"name": "UX-Designer", "amount": 4200},
    "sales": {"name": "Vertriebsmitarbeiter", "amount": 3300},
    "hr-manager": {"name": "HR-Manager", "amount": 4000},
    "sekretaerin": {"name": "Sekretärin", "amount": 2200},
    "handwerker": {"name": "Handwerker", "amount": 2500},
    "fahrer": {"name": "Berufskraftfahrer", "amount": 2400},
    "sozialarbeiter": {"name": "Sozialarbeiter", "amount": 3000},
    "physiotherapeut": {"name": "Physiotherapeut", "amount": 2700}
}

def generate_profession_content(name, amount, country_name, country_code):
    """Generate unique content for profession pages."""
    formatted_amount = f"{amount:,}".replace(',', '.')
    
    content = f'''
      <!-- Unique SEO Content -->
      <section class="content-section" style="margin-top: 32px;">
        <h2>Wie viel verdient ein {name} in {country_name}?</h2>
        <p>Ein {name} in {country_name} verdient durchschnittlich ca. <strong>{formatted_amount} € Brutto pro Monat</strong>. Das entspricht einem Jahresbrutto von ca. {(amount * 14):,} € (inkl. 13./14. Gehalt) bzw. {(amount * 12):,} € (ohne Sonderzahlungen).{' Das liegt ' + ('über' if amount > 3650 else 'unter') + ' dem österreichischen Median von ca. 3.650 €.' if country_code == 'at' else ' Das liegt ' + ('über' if amount > 3500 else 'unter') + ' dem deutschen Median von ca. 3.500 €.'}</p>
        
        <h3>Gehaltsentwicklung als {name}</h3>
        <p>Das Gehalt als {name} hängt von mehreren Faktoren ab:</p>
        <ul>
          <li><strong>Berufserfahrung:</strong> Einsteiger verdienen ca. 20-30% weniger, erfahrene Fachkräfte 10-20% mehr</li>
          <li><strong>Region:</strong> In städtischen Gebieten wird tendenziell mehr gezahlt</li>
          <li><strong>Branche:</strong> Private Unternehmen zahlen oft mehr als öffentliche</li>
          <li><strong>Spezialisierung:</strong> Zusatzqualifikationen können das Gehalt steigern</li>
        </ul>
        
        <h3>Netto-Gehalt als {name}</h3>
        <p>Bei {formatted_amount} € Brutto bleiben nach Abzug von Sozialversicherung und Lohnsteuer{' ca. ' + f'{amount * 0.68:.0f} €' + ' Netto pro Monat übrig (Richtwert).' if country_code == 'at' else ' ca. ' + f'{amount * 0.65:.0f} €' + ' Netto pro Monat übrig (Richtwert).'}</p>
        
        <h3>Vergleich mit anderen Berufen</h3>
        <p>Wie schneidet ein {name} im Vergleich ab?</p>
        <ul>
          <li><a href="/{'de/' if country_code == 'de' else ''}finanzen/gehalt/arzt-gehalt-netto.html">Arzt Gehalt (Top-Verdiener)</a></li>
          <li><a href="/{'de/' if country_code == 'de' else ''}finanzen/gehalt/softwareentwickler-gehalt-netto.html">Softwareentwickler Gehalt</a></li>
          <li><a href="/{'de/' if country_code == 'de' else ''}finanzen/gehalt/lehrer-gehalt-netto.html">Lehrer Gehalt</a></li>
          <li><a href="/{'de/' if country_code == 'de' else ''}finanzen/gehalt/kellner-gehalt-netto.html">Kellner Gehalt (Einstiegsbereich)</a></li>
        </ul>
        
        <h3>Tipps für {name}</h3>
        <p>Als {name} solltest du folgende Möglichkeiten prüfen:</p>
        <ul>
          <li><strong>Gehaltsverhandlung:</strong> Recherchiere Branchen-Standards und bereite dich gut vor</li>
          <li><strong>Weiterbildung:</strong> Zertifikate und Spezialisierungen können das Gehalt steigern</li>
          <li><strong>{'Pendlerpauschale' if country_code == 'at' else 'Entfernungspauschale'}:</strong> Prüfe, ob du absetzen kannst</li>
          <li><strong>{'Familienbonus Plus' if country_code == 'at' else 'Kindergeld'}:</strong> Falls du Kinder hast</li>
        </ul>
      </section>
'''
    return content

def generate_profession_pages(country_code, source_file, target_dir, country_name):
    target_dir.mkdir(parents=True, exist_ok=True)
    with open(source_file, 'r', encoding='utf-8') as f:
        template = f.read()

    for slug, data in PROFESSIONS.items():
        name = data["name"]
        amount = data["amount"]
        formatted_amount = f"{amount:,}".replace(',', '.')
        
        title = f"Gehalt {name} ({country_name}) - Brutto Netto Rechner"
        desc = f"Was verdient ein {name} in {country_name}? Durchschnittliches Gehalt: {formatted_amount} € Brutto. Berechne jetzt das Netto-Gehalt."
        
        html = re.sub(r'<title>.*?</title>', f'<title>{title} | rechnify.at</title>', template)
        html = re.sub(r'<meta name="description" content=".*?" />', f'<meta name="description" content="{desc}" />', html)
        html = re.sub(r'<meta property="og:title" content=".*?" />', f'<meta property="og:title" content="{title}" />', html)
        html = re.sub(r'<meta property="og:description" content=".*?" />', f'<meta property="og:description" content="{desc}" />', html)
        
        # Canonical
        prefix = "" if country_code == "at" else f"/{country_code}"
        new_canonical = f'https://rechnify.at{prefix}/finanzen/gehalt/{slug}-gehalt-netto.html'
        html = re.sub(r'<link rel="canonical" href=".*?" />', f'<link rel="canonical" href="{new_canonical}" />', html)
        
        # Remove hreflang links
        html = re.sub(r'<link rel="alternate" hreflang="de-AT".*?/>\n?', '', html)
        html = re.sub(r'<link rel="alternate" hreflang="de-DE".*?/>\n?', '', html)
        html = re.sub(r'<link rel="alternate" hreflang="x-default".*?/>\n?', '', html)
        
        html = re.sub(r'<h1>.*?</h1>', f'<h1>Gehalt {name} ({country_name})</h1>', html)
        
        if country_code == "at":
            html = re.sub(r'<p>Berechne dein exaktes Netto-Gehalt.*?für Österreich.</p>', f'<p>{desc}</p>', html)
        else:
            html = re.sub(r'<p>Berechne dein exaktes Netto-Gehalt.*?für Deutschland.</p>', f'<p>{desc}</p>', html)
            
        html = html.replace('<input type="number" id="grossMonthly" placeholder="z.B. 3500" min="0" step="100">', f'<input type="number" id="grossMonthly" value="{amount}" min="0" step="100">')
        
        # Add unique content before FAQ section
        unique_content = generate_profession_content(name, amount, country_name, country_code)
        html = html.replace('<!-- FAQ Section -->', unique_content + '\n      <!-- FAQ Section -->')
        
        html = html.replace('</body>', "<script>document.addEventListener('DOMContentLoaded', () => { setTimeout(() => { const btn = document.getElementById('calculate'); if(btn) btn.click(); }, 100); });</script></body>")
        
        filepath = target_dir / f"{slug}-gehalt-netto.html"
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html)
            
    print(f"Generated {len(PROFESSIONS)} profession pages for {country_name}.")

if __name__ == '__main__':
    print("Starting Step 1: DE Amount Pages...")
    generate_de_amounts()
    
    print("Starting Step 2: Profession Pages...")
    AT_SOURCE = BASE_DIR / 'finanzen' / 'gehaltsrechner.html'
    AT_TARGET_DIR = BASE_DIR / 'finanzen' / 'gehalt'
    generate_profession_pages('at', AT_SOURCE, AT_TARGET_DIR, "Österreich")
    
    DE_TARGET_DIR_PROFS = BASE_DIR / 'de' / 'finanzen' / 'gehalt'
    generate_profession_pages('de', DE_SOURCE, DE_TARGET_DIR_PROFS, "Deutschland")

    print("AT 10er-Schritte + cities + sitemap: python3 scripts/ship_gaps.py")
    print("All pSEO generations complete.")