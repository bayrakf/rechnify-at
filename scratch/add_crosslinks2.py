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

    # Insert right before <!-- Premium Girokonto Affiliate Box -->
    match = re.search(r'(<!-- Premium Girokonto Affiliate Box -->)', content)
    if match:
        new_content = content.replace(match.group(1), f'{link_html}\n            {match.group(1)}')
        with open(filepath, 'w') as f:
            f.write(new_content)
        print(f"Updated {filepath}")
    else:
        print(f"Could not find anchor in {filepath}")

# 1. Gehaltsrechner -> Teilzeitrechner
link_gehalt_at = '''
            <div class="seo-crosslink" style="margin-top: 24px; padding: 15px; background: var(--color-paper-2); border-radius: 10px; border: 1px dashed var(--color-primary); text-align: center;">
                <p style="margin: 0; font-size: 0.95rem;">💡 <strong>Tipp:</strong> Überlegst du deine Stunden zu reduzieren? <br><a href="/arbeitszeit/teilzeitrechner.html" style="font-weight: bold; color: var(--color-primary); display: inline-block; margin-top: 5px;">Nutze unseren Teilzeitrechner ➔</a></p>
            </div>
'''
link_gehalt_de = '''
            <div class="seo-crosslink" style="margin-top: 24px; padding: 15px; background: var(--color-paper-2); border-radius: 10px; border: 1px dashed var(--color-primary); text-align: center;">
                <p style="margin: 0; font-size: 0.95rem;">💡 <strong>Tipp:</strong> Überlegst du deine Stunden zu reduzieren? <br><a href="/de/arbeitszeit/teilzeitrechner.html" style="font-weight: bold; color: var(--color-primary); display: inline-block; margin-top: 5px;">Nutze unseren Teilzeitrechner ➔</a></p>
            </div>
'''
add_crosslink('finanzen/gehaltsrechner.html', link_gehalt_at, "")
add_crosslink('de/finanzen/gehaltsrechner.html', link_gehalt_de, "")
