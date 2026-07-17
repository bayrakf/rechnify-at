import os
import re
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent
SOURCE_HTML = BASE_DIR / 'finanzen' / 'gehaltsrechner.html'
TARGET_DIR = BASE_DIR / 'finanzen' / 'brutto-netto'

# Ensure target directory exists
TARGET_DIR.mkdir(parents=True, exist_ok=True)

def generate_pseo_pages():
    with open(SOURCE_HTML, 'r', encoding='utf-8') as f:
        template = f.read()

    # Amounts to generate: 1500 to 6000 in steps of 100, plus some high ones
    amounts = list(range(1500, 6100, 100)) + [6500, 7000, 8000, 9000, 10000]

    for amount in amounts:
        amount_str = str(amount)
        formatted_amount = f"{amount:,}".replace(',', '.')
        
        # 1. Replace Title
        title_pattern = r'<title>.*?</title>'
        new_title = f'<title>{formatted_amount} € Brutto in Netto Österreich | rechnify.at</title>'
        html = re.sub(title_pattern, new_title, template)

        # 2. Replace Description
        desc_pattern = r'<meta name="description" content=".*?" />'
        new_desc = f'<meta name="description" content="Wie viel Netto bleibt von {formatted_amount} € Brutto in Österreich? Berechne sofort Steuern, SV und Abzüge für 2026." />'
        html = re.sub(desc_pattern, new_desc, html)

        # 3. Replace OG tags
        html = re.sub(r'<meta property="og:title" content=".*?" />', f'<meta property="og:title" content="{formatted_amount} € Brutto in Netto Österreich" />', html)
        html = re.sub(r'<meta property="og:description" content=".*?" />', f'<meta property="og:description" content="Wie viel Netto bleibt von {formatted_amount} € Brutto in Österreich? Berechne sofort Steuern, SV und Abzüge für 2026." />', html)

        # Canonical tag points to the pSEO page to avoid duplicate content penalties
        new_canonical = f'https://rechnify.at/finanzen/brutto-netto/{amount}-brutto-in-netto.html'
        html = re.sub(r'<link rel="canonical" href=".*?" />', f'<link rel="canonical" href="{new_canonical}" />', html)

        # Remove hreflang links (since pSEO pages are AT specific and don't have DE equivalents right now)
        html = re.sub(r'<link rel="alternate" hreflang="de-AT".*?/>\n?', '', html)
        html = re.sub(r'<link rel="alternate" hreflang="de-DE".*?/>\n?', '', html)
        html = re.sub(r'<link rel="alternate" hreflang="x-default".*?/>\n?', '', html)

        # 4. Replace H1
        h1_pattern = r'<h1>.*?</h1>'
        new_h1 = f'<h1>{formatted_amount} € Brutto in Netto</h1>'
        html = re.sub(h1_pattern, new_h1, html)
        
        # Replace the sub-paragraph
        p_pattern = r'<p>Berechne dein exaktes Netto-Gehalt.*?für Österreich.</p>'
        new_p = f'<p>Wie viel Netto bleibt von {formatted_amount} € Brutto in Österreich?</p>'
        html = re.sub(p_pattern, new_p, html)

        # 5. Inject the value into the input field
        input_pattern = r'<input type="number" id="grossMonthly" placeholder="z.B. 3500" min="0" step="100">'
        new_input = f'<input type="number" id="grossMonthly" value="{amount}" min="0" step="100">'
        html = html.replace(input_pattern, new_input)

        # 6. Add auto-click script
        auto_click_script = """
  <script>
    // pSEO Auto-Calculate
    document.addEventListener('DOMContentLoaded', () => {
      setTimeout(() => {
        const btn = document.getElementById('calculate');
        if(btn) btn.click();
      }, 100);
    });
  </script>
</body>
"""
        html = html.replace('</body>', auto_click_script)

        # Write the file
        filename = f"{amount}-brutto-in-netto.html"
        filepath = TARGET_DIR / filename
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html)
        
        print(f"Generated {filename}")

if __name__ == '__main__':
    print("Starting Programmatic SEO Generation...")
    generate_pseo_pages()
    print("Done!")
