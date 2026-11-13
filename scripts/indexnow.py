#!/usr/bin/env python3
"""Ping IndexNow (Bing/Yandex/etc.) after deploy.

Aufruf:  python3 scripts/indexnow.py [--since <git-sha>]
Mit --since nur die seitdem geaenderten, indexierbaren Seiten melden.
Bing empfiehlt, nur geaenderte URLs zu senden; staendig alle zu pingen
kann die Beachtung der Pings senken. Ohne/ungueltiges --since: alle.
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HOST = "rechnify.at"
KEY = "48203d7933394ec8a062b7e4943c572b"
KEY_LOCATION = f"https://{HOST}/{KEY}.txt"
ENDPOINTS = [
    "https://api.indexnow.org/indexnow",
    "https://yandex.com/indexnow",
]
SITEMAP = ROOT / "sitemap.xml"


def urls_from_sitemap() -> list[str]:
    text = SITEMAP.read_text(encoding="utf-8")
    return re.findall(r"<loc>(https://rechnify\.at[^<]+)</loc>", text)


def changed_urls(since: str, known: list[str]) -> list[str] | None:
    """Geaenderte Seiten seit `since` als URLs, None wenn der Commit unbekannt ist."""
    res = subprocess.run(
        ["git", "diff", "--name-only", since, "HEAD", "--", "*.html"],
        cwd=ROOT, capture_output=True, text=True,
    )
    if res.returncode != 0:
        return None
    sys.path.insert(0, str(ROOT / "scripts"))
    from seo_policy import url_for

    wanted = {url_for(rel) for rel in res.stdout.splitlines()}
    return [u for u in known if u in wanted]  # nur indexierbare (= in Sitemap)


def submit(urls: list[str]) -> int:
    # IndexNow soft-caps ~10k; we have <200
    payload = {
        "host": HOST,
        "key": KEY,
        "keyLocation": KEY_LOCATION,
        "urlList": urls,
    }
    data = json.dumps(payload).encode("utf-8")
    success = False
    for ep in ENDPOINTS:
        req = urllib.request.Request(
            ep,
            data=data,
            headers={"Content-Type": "application/json; charset=utf-8"},
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=30) as res:
                code = res.getcode()
                body = res.read().decode("utf-8", errors="replace")
                print(f"IndexNow ({ep}) {code}: {len(urls)} URLs")
                if body:
                    print(body[:300])
                if code in (200, 202):
                    success = True
                    break
        except urllib.error.HTTPError as e:
            print(f"IndexNow ({ep}) HTTP {e.code}: {e.read().decode('utf-8', errors='replace')[:200]}", file=sys.stderr)
        except urllib.error.URLError as e:
            print(f"IndexNow ({ep}) error: {e}", file=sys.stderr)
    return 0 if success else 1


def main() -> int:
    urls = urls_from_sitemap()
    if not urls:
        print("No URLs in sitemap.xml", file=sys.stderr)
        return 1
    if len(sys.argv) == 3 and sys.argv[1] == "--since" and sys.argv[2].strip("0"):
        changed = changed_urls(sys.argv[2], urls)
        if changed is None:
            print(f"Commit {sys.argv[2]} unbekannt, sende alle URLs")
        elif not changed:
            print("Keine indexierbare Seite geaendert, kein Ping")
            return 0
        else:
            urls = changed
    # Always include homepage + key location host check path
    if f"https://{HOST}/" not in urls:
        urls.insert(0, f"https://{HOST}/")
    return submit(urls)


if __name__ == "__main__":
    raise SystemExit(main())
