import os
from pathlib import Path
import re

BASE_DIR = Path(__file__).resolve().parent.parent

# Define the standard "Passende Rechner" blocks per category
RELATED_BLOCKS = {
    "arbeitszeit": """
      <!-- Passende Rechner -->
      <div class="related-tools" style="margin-top: 32px; padding: 24px; background: white; border-radius: 12px; border: 1px solid var(--border);">
        <h3 style="margin-top: 0;">🔗 Passende Rechner</h3>
        <ul style="list-style: none; padding: 0; margin: 0; display: flex; flex-direction: column; gap: 8px;">
          <li><a href="{prefix}/finanzen/gehaltsrechner.html" style="text-decoration: none; color: var(--primary); font-weight: 500;">➔ Brutto-Netto Gehaltsrechner</a></li>
          <li><a href="{prefix}/arbeitszeit/stundenlohn-rechner.html" style="text-decoration: none; color: var(--primary); font-weight: 500;">➔ Stundenlohn-Rechner</a></li>
          <li><a href="{prefix}/arbeitszeit/urlaubstage-rechner.html" style="text-decoration: none; color: var(--primary); font-weight: 500;">➔ Urlaubstage-Rechner</a></li>
          <li><a href="{prefix}/arbeitszeit/kommen-gehen-rechner.html" style="text-decoration: none; color: var(--primary); font-weight: 500;">➔ Kommen-Gehen-Rechner</a></li>
        </ul>
      </div>
""",
    "finanzen": """
      <!-- Passende Rechner -->
      <div class="related-tools" style="margin-top: 32px; padding: 24px; background: white; border-radius: 12px; border: 1px solid var(--border);">
        <h3 style="margin-top: 0;">🔗 Passende Rechner</h3>
        <ul style="list-style: none; padding: 0; margin: 0; display: flex; flex-direction: column; gap: 8px;">
          <li><a href="{prefix}/finanzen/gehaltsrechner.html" style="text-decoration: none; color: var(--primary); font-weight: 500;">➔ Brutto-Netto Gehaltsrechner</a></li>
          <li><a href="{prefix}/arbeitszeit/ueberstundenrechner.html" style="text-decoration: none; color: var(--primary); font-weight: 500;">➔ Überstundenrechner (inkl. Steuerfreibetrag)</a></li>
          <li><a href="{prefix}/finanzen/pendlerrechner.html" style="text-decoration: none; color: var(--primary); font-weight: 500;">➔ Pendlerrechner (Österreich)</a></li>
          <li><a href="{prefix}/finanzen/familienbonus-rechner.html" style="text-decoration: none; color: var(--primary); font-weight: 500;">➔ Familienbonus Plus Rechner</a></li>
        </ul>
      </div>
""",
    "familie": """
      <!-- Passende Rechner -->
      <div class="related-tools" style="margin-top: 32px; padding: 24px; background: white; border-radius: 12px; border: 1px solid var(--border);">
        <h3 style="margin-top: 0;">🔗 Passende Rechner</h3>
        <ul style="list-style: none; padding: 0; margin: 0; display: flex; flex-direction: column; gap: 8px;">
          <li><a href="{prefix}/finanzen/familienbonus-rechner.html" style="text-decoration: none; color: var(--primary); font-weight: 500;">➔ Familienbonus Plus Rechner</a></li>
          <li><a href="{prefix}/familie/schwangerschaftsrechner.html" style="text-decoration: none; color: var(--primary); font-weight: 500;">➔ Schwangerschaftsrechner (SSW)</a></li>
          <li><a href="{prefix}/familie/elterngeld.html" style="text-decoration: none; color: var(--primary); font-weight: 500;">➔ Kinderbetreuungsgeld / Elterngeld</a></li>
          <li><a href="{prefix}/finanzen/gehaltsrechner.html" style="text-decoration: none; color: var(--primary); font-weight: 500;">➔ Brutto-Netto Gehaltsrechner</a></li>
        </ul>
      </div>
"""
}

def process_directory(base_path, folder_name, is_de):
    folder_path = base_path / folder_name
    if not folder_path.exists():
        return
    
    prefix = '/de' if is_de else ''
    block = RELATED_BLOCKS[folder_name].replace('{prefix}', prefix)
    # fix elterngeld vs kbg link manually
    if is_de and '/familie/elterngeld.html' in block:
        pass
    elif not is_de:
        block = block.replace('/familie/elterngeld.html', '/familie/kinderbetreuungsgeld.html')
    
    for html_file in folder_path.rglob("*.html"):
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()

        if '<!-- Passende Rechner -->' in content:
            new_content = re.sub(r'<!-- Passende Rechner -->.*?</div>\s*(?=</main>|</div>\s*</main>)', block, content, flags=re.DOTALL)
            content = new_content
        else:
            content = content.replace('</main>', block + '\n  </main>')

        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated: {html_file.relative_to(BASE_DIR)}")

# AT Folders
for folder in ['arbeitszeit', 'finanzen', 'familie']:
    process_directory(BASE_DIR, folder, False)

# DE Folders
for folder in ['arbeitszeit', 'finanzen', 'familie']:
    process_directory(BASE_DIR / 'de', folder, True)
