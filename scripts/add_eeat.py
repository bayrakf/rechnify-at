#!/usr/bin/env python3
"""Add E-E-A-T signals (author bio, sources, Person schema) to all blog articles."""

import os
import re
import glob

BLOG_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "blog")

# Author bio HTML template
AUTHOR_BIO = '''
      <!-- Author Bio -->
      <div
        style="margin-top:40px; padding:24px; background:var(--color-paper-2); border-radius:12px; display:flex; gap:16px; align-items:flex-start;">
        <div
          style="width:56px; height:56px; border-radius:50%; background:var(--color-accent); color:#fff; display:flex; align-items:center; justify-content:center; font-size:1.4rem; font-weight:700; flex-shrink:0;">
          F</div>
        <div>
          <h3 style="margin:0 0 4px; font-size:1.1rem;">Firat Bayrak</h3>
          <p style="margin:0; font-size:0.9rem; color:var(--color-ink-2); line-height:1.5;">Entwickler und Betreiber von
            rechnify.at. Erstellt kostenlose Online-Rechner für Österreich und Deutschland mit Fokus auf Transparenz und
            Datenschutz. Alle Berechnungen basieren auf amtlichen Quellen (BMF, WKO, Sozialversicherung).</p>
          <div style="margin-top:8px; display:flex; gap:12px; font-size:0.85rem;">
            <a href="/ueber-uns.html" style="color:var(--color-accent); font-weight:600;">Mehr über rechnify.at →</a>
          </div>
        </div>
      </div>

'''

# Sources per article (keyed by filename)
SOURCES = {
    "ueberstunden-oesterreich.html": "Arbeitszeitgesetz (AZG), WKO Kollektivverträge, Arbeiterkammer (AK). Stand: Juli 2026.",
    "brutto-netto-tabelle-oesterreich-2026.html": "BMF Österreich (Lohnsteuer), Sozialversicherung.gv.at (SV-Sätze), WKO (Sonderzahlungen). Stand: Juli 2026.",
    "13-14-gehalt-erklaert.html": "BMF Österreich (§67 EStG), WKO (Sonderzahlungen), Sozialversicherung.gv.at. Stand: Juli 2026.",
    "gehaltsverhandlung-tipps.html": "Arbeiterkammer (AK), WKO (Kollektivverträge), Statistik Austria (Gehaltsdaten). Stand: Juli 2026.",
    "pendlerpauschale-guide.html": "BMF Österreich (§16 EStG), WKO (Pendlerrechner), FinanzOnline. Stand: Juli 2026.",
    "pendlerpauschale-oesterreich-2026.html": "BMF Österreich (§16 EStG), WKO (Pendlerrechner), FinanzOnline. Stand: Juli 2026.",
}

DEFAULT_SOURCES = "BMF Österreich, WKO, Sozialversicherung.gv.at, Arbeiterkammer (AK). Stand: Juli 2026."


def get_sources_html(filename):
    """Generate the sources section HTML for a given filename."""
    source_text = SOURCES.get(filename, DEFAULT_SOURCES)
    return f'''
      <!-- Sources -->
      <div
        style="margin-top:24px; padding:16px 20px; background:var(--color-paper-2); border-radius:8px; font-size:0.85rem; color:var(--color-ink-3);">
        <strong>Quellen:</strong> {source_text}
      </div>

'''


def update_author_schema(content):
    """Replace Organization author with Person author in Article schema."""
    # Match both inline and multiline author patterns
    patterns = [
        # Inline: "author": { "@type": "Organization", "name": "rechnify.at" },
        r'"author":\s*\{\s*"@type":\s*"Organization",\s*"name":\s*"rechnify\.at"\s*\}',
        # Multiline:
        # "author": {
        #   "@type": "Organization",
        #   "name": "rechnify.at"
        # },
        r'"author":\s*\{\s*\n\s*"@type":\s*"Organization",\s*\n\s*"name":\s*"rechnify\.at"\s*\n\s*\}',
    ]

    replacement = '''"author": {
      "@type": "Person",
      "name": "Firat Bayrak",
      "url": "https://rechnify.at/ueber-uns.html"
    }'''

    for pattern in patterns:
        content = re.sub(pattern, replacement, content)

    return content


def add_author_bio_and_sources(content, filename):
    """Add author bio and sources section before the 'Letzte Aktualisierung' div or </article>."""

    # Check if author bio already exists
    if "Author Bio" in content:
        print(f"  → Already has author bio, skipping bio insertion")
        return content

    sources_html = get_sources_html(filename)
    insert_block = AUTHOR_BIO + sources_html

    # Pattern 1: Find the "Letzte Aktualisierung" div and insert before it
    pattern1 = r'(<div\s+style="margin-top:\d+px;\s*padding-top:\d+px;\s*border-top:1px solid var\(--color-rule\);\s*text-align:center;">\s*<p[^>]*>Letzte Aktualisierung[^<]*</p>\s*</div>)'

    def replace_fn1(match):
        return insert_block + match.group(1)

    new_content = re.sub(pattern1, replace_fn1, content)

    if new_content != content:
        return new_content

    # Pattern 2: Find </article> and insert before it (for articles without "Letzte Aktualisierung")
    pattern2 = r'(</article>)'
    def replace_fn2(match):
        return insert_block + match.group(1)

    new_content = re.sub(pattern2, replace_fn2, content, count=1)

    return new_content


def process_file(filepath):
    """Process a single blog article HTML file."""
    filename = os.path.basename(filepath)
    print(f"Processing: {filename}")

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content

    # 1. Update author schema
    content = update_author_schema(content)

    # 2. Add author bio and sources
    content = add_author_bio_and_sources(content, filename)

    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  → Updated ✓")
        return True
    else:
        print(f"  → No changes needed")
        return False


def main():
    print("=" * 60)
    print("Adding E-E-A-T signals to blog articles")
    print("=" * 60)

    # Find all HTML files in the blog directory
    blog_files = sorted(glob.glob(os.path.join(BLOG_DIR, "*.html")))

    # Skip index.html
    blog_files = [f for f in blog_files if os.path.basename(f) != "index.html"]

    print(f"\nFound {len(blog_files)} blog articles to process:\n")

    updated = 0
    for filepath in blog_files:
        if process_file(filepath):
            updated += 1

    print(f"\n{'=' * 60}")
    print(f"Done! Updated {updated}/{len(blog_files)} articles.")
    print("=" * 60)


if __name__ == "__main__":
    main()