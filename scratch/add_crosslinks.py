import os
import re

def add_crosslink(filepath, link_html, after_text):
    if not os.path.exists(filepath):
        print(f"File {filepath} not found.")
        return
    with open(filepath, 'r') as f:
        content = f.read()
    
    if "seo-crosslink" in content:
        print(f"Crosslink already in {filepath}")
        return

    # Insert right before the last closing div of the card
    match = re.search(r'(</div>\s*</div>\s*<!-- END CALCULATOR -->)', content)
    if match:
        new_content = content.replace(match.group(1), f'\n{link_html}\n{match.group(1)}')
        with open(filepath, 'w') as f:
            f.write(new_content)
        print(f"Updated {filepath}")
    else:
        print(f"Could not find anchor in {filepath}")

# 1. Gehaltsrechner -> Teilzeitrechner
link_gehalt_at = '''
        <div class="seo-crosslink" style="margin-top: 20px; padding: 15px; background: var(--color-paper-2); border-radius: 10px; border: 1px dashed var(--color-primary); text-align: center;">
            <p style="margin: 0;">💡 <strong>Tipp:</strong> Überlegst du deine Stunden zu reduzieren? <a href="/arbeitszeit/teilzeitrechner.html" style="font-weight: bold; color: var(--color-primary);">Nutze unseren Teilzeitrechner ➔</a></p>
        </div>
'''
link_gehalt_de = '''
        <div class="seo-crosslink" style="margin-top: 20px; padding: 15px; background: var(--color-paper-2); border-radius: 10px; border: 1px dashed var(--color-primary); text-align: center;">
            <p style="margin: 0;">💡 <strong>Tipp:</strong> Überlegst du deine Stunden zu reduzieren? <a href="/de/arbeitszeit/teilzeitrechner.html" style="font-weight: bold; color: var(--color-primary);">Nutze unseren Teilzeitrechner ➔</a></p>
        </div>
'''
add_crosslink('finanzen/gehaltsrechner.html', link_gehalt_at, "")
add_crosslink('de/finanzen/gehaltsrechner.html', link_gehalt_de, "")

# 2. Teilzeitrechner -> Stundenlohnrechner
link_teilzeit_at = '''
        <div class="seo-crosslink" style="margin-top: 20px; padding: 15px; background: var(--color-paper-2); border-radius: 10px; border: 1px dashed var(--color-primary); text-align: center;">
            <p style="margin: 0;">💡 <strong>Tipp:</strong> Berechne deinen exakten Stundenlohn. <a href="/arbeitszeit/stundenlohn-rechner.html" style="font-weight: bold; color: var(--color-primary);">Zum Stundenlohnrechner ➔</a></p>
        </div>
'''
link_teilzeit_de = '''
        <div class="seo-crosslink" style="margin-top: 20px; padding: 15px; background: var(--color-paper-2); border-radius: 10px; border: 1px dashed var(--color-primary); text-align: center;">
            <p style="margin: 0;">💡 <strong>Tipp:</strong> Berechne deinen exakten Stundenlohn. <a href="/de/arbeitszeit/stundenlohn-rechner.html" style="font-weight: bold; color: var(--color-primary);">Zum Stundenlohnrechner ➔</a></p>
        </div>
'''
add_crosslink('arbeitszeit/teilzeitrechner.html', link_teilzeit_at, "")
add_crosslink('de/arbeitszeit/teilzeitrechner.html', link_teilzeit_de, "")

# 3. Leasingrechner -> Kreditrechner (we will build Kreditrechner next, link will be valid)
link_leasing_at = '''
        <div class="seo-crosslink" style="margin-top: 20px; padding: 15px; background: var(--color-paper-2); border-radius: 10px; border: 1px dashed var(--color-primary); text-align: center;">
            <p style="margin: 0;">💡 <strong>Tipp:</strong> Leasing oder Barkauf mit Autokredit? <a href="/finanzen/kreditrechner.html" style="font-weight: bold; color: var(--color-primary);">Berechne die Kreditrate ➔</a></p>
        </div>
'''
link_leasing_de = '''
        <div class="seo-crosslink" style="margin-top: 20px; padding: 15px; background: var(--color-paper-2); border-radius: 10px; border: 1px dashed var(--color-primary); text-align: center;">
            <p style="margin: 0;">💡 <strong>Tipp:</strong> Leasing oder Barkauf mit Autokredit? <a href="/de/finanzen/kreditrechner.html" style="font-weight: bold; color: var(--color-primary);">Berechne die Kreditrate ➔</a></p>
        </div>
'''
add_crosslink('finanzen/leasingrechner.html', link_leasing_at, "")
add_crosslink('de/finanzen/leasingrechner.html', link_leasing_de, "")
