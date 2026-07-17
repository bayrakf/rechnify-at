#!/usr/bin/env python3
"""Generate sitemap.xml and inject consistent SEO meta tags across all HTML pages."""

from __future__ import annotations

import re
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = "https://rechnify.at"
TODAY = date.today().isoformat()

# AT path -> DE path (canonical pairs for hreflang)
HREFLANG_PAIRS: dict[str, str] = {
    "arbeitszeit/kommen-gehen-rechner.html": "de/arbeitszeit/kommen-gehen-rechner.html",
    "arbeitszeit/urlaubstage-rechner.html": "de/arbeitszeit/urlaubstage-rechner.html",
    "arbeitszeit/ueberstundenrechner.html": "de/arbeitszeit/ueberstundenrechner.html",
    "arbeitszeit/stundenlohn-rechner.html": "de/arbeitszeit/stundenlohn-rechner.html",
    "arbeitszeit/teilzeitrechner.html": "de/arbeitszeit/teilzeitrechner.html",
    "arbeitszeit/arbeitstage-rechner.html": "de/arbeitszeit/arbeitstage-rechner.html",
    "arbeitszeit/brueckentage-planer.html": "de/arbeitszeit/brueckentage-planer.html",
    "finanzen/gehaltsrechner.html": "de/finanzen/gehaltsrechner.html",
    "finanzen/gehaltserhoehung-rechner.html": "de/finanzen/gehaltserhoehung-rechner.html",
    "finanzen/kryptosteuerrechner.html": "de/finanzen/kryptosteuerrechner.html",
    "finanzen/mwst-rechner.html": "de/finanzen/mwst-rechner.html",
    "finanzen/sachbezugsrechner.html": "de/finanzen/sachbezugsrechner.html",
    "finanzen/pendlerrechner.html": "de/finanzen/pendlerrechner.html",
    "finanzen/etf-sparplan-rechner.html": "de/finanzen/etf-sparplan-rechner.html",
    "finanzen/leasingrechner.html": "de/finanzen/leasingrechner.html",
    "finanzen/kreditrechner.html": "de/finanzen/kreditrechner.html",
    "familie/kinderbetreuungsgeld.html": "de/familie/elterngeld.html",
}

DE_TO_AT = {de: at for at, de in HREFLANG_PAIRS.items()}

HIGH_PRIORITY = {
    "index.html",
    "arbeitszeit/kommen-gehen-rechner.html",
    "de/arbeitszeit/kommen-gehen-rechner.html",
    "arbeitszeit/stundenlohn-rechner.html",
    "de/arbeitszeit/stundenlohn-rechner.html",
    "finanzen/gehaltsrechner.html",
    "de/finanzen/gehaltsrechner.html",
}

LOW_PRIORITY = {
    "impressum.html",
    "datenschutz.html",
}

ROBOTS_META = (
    '<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1" />'
)
ADSENSE_SCRIPT = (
    '<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-5052220565736445" '
    'crossorigin="anonymous"></script>'
)
OG_TWITTER = """\
<meta property="og:image" content="https://rechnify.at/assets/images/favicon-512x512.png" />
  <meta property="og:image:alt" content="rechnify.at Logo" />
  <meta name="twitter:card" content="summary" />
  <meta name="twitter:image" content="https://rechnify.at/assets/images/favicon-512x512.png" />"""


def page_loc(rel: str) -> str:
    if rel == "index.html":
        return f"{BASE}/"
    return f"{BASE}/{rel}"


def page_priority(rel: str) -> str:
    if rel == "index.html":
        return "1.0"
    if rel in HIGH_PRIORITY:
        return "0.9"
    if rel in LOW_PRIORITY:
        return "0.3"
    if rel.startswith("de/"):
        return "0.8"
    if rel.startswith(("ueber-uns", "kontakt")):
        return "0.4"
    return "0.8"


def hreflang_block(rel: str) -> str:
    if rel == "index.html":
        loc = page_loc(rel)
        return (
            f'  <link rel="alternate" hreflang="de-AT" href="{loc}" />\n'
            f'  <link rel="alternate" hreflang="de-DE" href="{loc}" />\n'
            f'  <link rel="alternate" hreflang="x-default" href="{loc}" />'
        )
    if rel in HREFLANG_PAIRS:
        at, de = rel, HREFLANG_PAIRS[rel]
        return (
            f'  <link rel="alternate" hreflang="de-AT" href="{page_loc(at)}" />\n'
            f'  <link rel="alternate" hreflang="de-DE" href="{page_loc(de)}" />\n'
            f'  <link rel="alternate" hreflang="x-default" href="{page_loc(at)}" />'
        )
    if rel in DE_TO_AT:
        at, de = DE_TO_AT[rel], rel
        return (
            f'  <link rel="alternate" hreflang="de-AT" href="{page_loc(at)}" />\n'
            f'  <link rel="alternate" hreflang="de-DE" href="{page_loc(de)}" />\n'
            f'  <link rel="alternate" hreflang="x-default" href="{page_loc(at)}" />'
        )
    loc = page_loc(rel)
    return (
        f'  <link rel="alternate" hreflang="de-AT" href="{loc}" />\n'
        f'  <link rel="alternate" hreflang="x-default" href="{loc}" />'
    )


def sitemap_hreflang_links(rel: str) -> str:
    lines: list[str] = []
    if rel == "index.html":
        loc = page_loc(rel)
        for lang in ("de-AT", "de-DE", "x-default"):
            lines.append(
                f'    <xhtml:link rel="alternate" hreflang="{lang}" href="{loc}"/>'
            )
        return "\n".join(lines)
    if rel in HREFLANG_PAIRS:
        at, de = rel, HREFLANG_PAIRS[rel]
        lines.append(f'    <xhtml:link rel="alternate" hreflang="de-AT" href="{page_loc(at)}"/>')
        lines.append(f'    <xhtml:link rel="alternate" hreflang="de-DE" href="{page_loc(de)}"/>')
        lines.append(f'    <xhtml:link rel="alternate" hreflang="x-default" href="{page_loc(at)}"/>')
        return "\n".join(lines)
    if rel in DE_TO_AT:
        at, de = DE_TO_AT[rel], rel
        lines.append(f'    <xhtml:link rel="alternate" hreflang="de-AT" href="{page_loc(at)}"/>')
        lines.append(f'    <xhtml:link rel="alternate" hreflang="de-DE" href="{page_loc(de)}"/>')
        lines.append(f'    <xhtml:link rel="alternate" hreflang="x-default" href="{page_loc(at)}"/>')
        return "\n".join(lines)
    loc = page_loc(rel)
    lines.append(f'    <xhtml:link rel="alternate" hreflang="de-AT" href="{loc}"/>')
    lines.append(f'    <xhtml:link rel="alternate" hreflang="x-default" href="{loc}"/>')
    return "\n".join(lines)


def generate_sitemap(pages: list[str]) -> str:
    entries: list[str] = []
    for rel in sorted(pages, key=lambda p: (p != "index.html", p)):
        loc = page_loc(rel)
        alt = sitemap_hreflang_links(rel)
        alt_block = f"\n{alt}" if alt else ""
        entries.append(
            f"""  <url>
    <loc>{loc}</loc>{alt_block}
    <lastmod>{TODAY}</lastmod>
    <changefreq>{"weekly" if rel == "index.html" else "monthly"}</changefreq>
    <priority>{page_priority(rel)}</priority>
  </url>"""
        )
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
        xmlns:xhtml="http://www.w3.org/1999/xhtml">
{chr(10).join(entries)}
</urlset>
"""


def patch_html(path: Path, rel: str) -> bool:
    text = path.read_text(encoding="utf-8")
    orig = text
    is_noindex = rel in ("impressum.html", "datenschutz.html")

    # Collapse blank-line spam left by prior SEO patches
    text = re.sub(r"\n{3,}", "\n\n", text)

    # Regional lang + OG locale on DE twins
    if rel.startswith("de/"):
        text = re.sub(r'<html\s+lang="de(?:-AT)?"', '<html lang="de-DE"', text, count=1)
        text = re.sub(
            r'<meta property="og:locale" content="de_AT" />',
            '<meta property="og:locale" content="de_DE" />\n  <meta property="og:locale:alternate" content="de_AT" />',
            text,
            count=1,
        )
    elif rel != "index.html" and not rel.startswith("de/"):
        text = re.sub(r'<html\s+lang="de(?:-DE)?"', '<html lang="de-AT"', text, count=1)
        if 'og:locale:alternate' not in text:
            text = re.sub(
                r'(<meta property="og:locale" content="de_AT" />)',
                r'\1\n  <meta property="og:locale:alternate" content="de_DE" />',
                text,
                count=1,
            )

    # Cache-bust shared CSS
    text = re.sub(
        r'/assets/css/global\.css(?:\?v=[^"\']+)?',
        "/assets/css/global.css?v=2.3",
        text,
    )
    text = re.sub(r"/tokens\.css(?:\?v=[^\"'\\s>]+)?", "/tokens.css?v=1.2", text)

    # Remove old hreflang variants (case inconsistent)
    text = re.sub(r'\s*<link rel="alternate" hreflang="[^"]+" href="[^"]+" />\n?', "\n", text)

    canon_match = re.search(r'<link rel="canonical" href="([^"]+)" />', text)
    if not canon_match:
        return False

    canonical_tag = canon_match.group(0)

    # Rebuild SEO block after canonical
    seo_lines = [canonical_tag]
    if not is_noindex:
        if ROBOTS_META not in text:
            seo_lines.append(f"  {ROBOTS_META}")
    seo_lines.append(hreflang_block(rel))
    if ADSENSE_SCRIPT not in text:
        seo_lines.append(f"  {ADSENSE_SCRIPT}")

    # Replace first canonical occurrence with full block
    text = text.replace(canonical_tag, "\n".join(seo_lines), 1)

    # Remove duplicate robots meta if any left
    if not is_noindex:
        count = text.count(ROBOTS_META)
        if count > 1:
            parts = text.split(ROBOTS_META)
            text = parts[0] + ROBOTS_META + ROBOTS_META.join(parts[1:]).replace(ROBOTS_META, "", count - 1)

    if "og:image" not in text and 'property="og:type"' not in text:
        # After og:url or og:description or meta description
        anchor = None
        for pattern in (
            r'<meta property="og:url" content="[^"]+" />',
            r'<meta property="og:description" content="[^"]+" />',
            r'<meta name="description" content="[^"]+" />',
        ):
            m = re.search(pattern, text)
            if m:
                anchor = m.group(0)
                break
        if anchor:
            text = text.replace(anchor, f"{anchor}\n  {OG_TWITTER}", 1)

    # Add og tags on pages missing Open Graph entirely
    if 'property="og:type"' not in text and rel != "index.html":
        title_m = re.search(r"<title>([^<]+)</title>", text)
        desc_m = re.search(r'<meta name="description" content="([^"]+)"', text)
        if title_m and desc_m and canon_match:
            og = f"""
  <!-- Open Graph -->
  <meta property="og:type" content="website" />
  <meta property="og:title" content="{title_m.group(1).replace('"', '&quot;')}" />
  <meta property="og:description" content="{desc_m.group(1)}" />
  <meta property="og:url" content="{canon_match.group(1)}" />
  <meta property="og:locale" content="de_AT" />
  <meta property="og:site_name" content="rechnify.at" />
  {OG_TWITTER}"""
            text = text.replace(
                f'  <meta name="description" content="{desc_m.group(1)}" />',
                f'  <meta name="description" content="{desc_m.group(1)}" />{og}',
                1,
            )

    if text != orig:
        text = re.sub(r"\n{3,}", "\n\n", text)
        path.write_text(text, encoding="utf-8")
        return True
    return False


def main() -> None:
    pages = sorted(p.relative_to(ROOT).as_posix() for p in ROOT.glob("**/*.html"))
    (ROOT / "sitemap.xml").write_text(generate_sitemap(pages) + "\n", encoding="utf-8")
    print(f"sitemap.xml — {len(pages)} URLs, lastmod {TODAY}")

    changed = 0
    for rel in pages:
        if patch_html(ROOT / rel, rel):
            changed += 1
    print(f"Patched SEO meta on {changed} HTML files")


if __name__ == "__main__":
    main()
