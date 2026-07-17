import os
import re
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent

# Step 1: Amounts for DE
DE_SOURCE = BASE_DIR / 'de' / 'finanzen' / 'gehaltsrechner.html'
DE_TARGET_DIR = BASE_DIR / 'de' / 'finanzen' / 'brutto-netto'
DE_TARGET_DIR.mkdir(parents=True, exist_ok=True)

AMOUNTS = list(range(1500, 6100, 100)) + [6500, 7000, 8000, 9000, 10000]

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
    "friseur": {"name": "Friseur", "amount": 1800}
}

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
    
    print("All pSEO generations complete.")
