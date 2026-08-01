#!/usr/bin/env python3
"""Ping IndexNow (Bing/Yandex/etc.) with sitemap URLs after deploy."""

from __future__ import annotations

import json
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HOST = "rechnify.at"
KEY = "48203d7933394ec8a062b7e4943c572b"
KEY_LOCATION = f"https://{HOST}/{KEY}.txt"
ENDPOINT = "https://api.indexnow.org/indexnow"
SITEMAP = ROOT / "sitemap.xml"


def urls_from_sitemap() -> list[str]:
    text = SITEMAP.read_text(encoding="utf-8")
    return re.findall(r"<loc>(https://rechnify\.at[^<]+)</loc>", text)


def submit(urls: list[str]) -> int:
    # IndexNow soft-caps ~10k; we have <200
    payload = {
        "host": HOST,
        "key": KEY,
        "keyLocation": KEY_LOCATION,
        "urlList": urls,
    }
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        ENDPOINT,
        data=data,
        headers={"Content-Type": "application/json; charset=utf-8"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as res:
            code = res.getcode()
            body = res.read().decode("utf-8", errors="replace")
            print(f"IndexNow {code}: {len(urls)} URLs")
            if body:
                print(body[:500])
            return 0 if code in (200, 202) else 1
    except urllib.error.HTTPError as e:
        print(f"IndexNow HTTP {e.code}: {e.read().decode('utf-8', errors='replace')[:500]}", file=sys.stderr)
        return 1
    except urllib.error.URLError as e:
        print(f"IndexNow error: {e}", file=sys.stderr)
        return 1


def main() -> int:
    urls = urls_from_sitemap()
    if not urls:
        print("No URLs in sitemap.xml", file=sys.stderr)
        return 1
    # Always include homepage + key location host check path
    if f"https://{HOST}/" not in urls:
        urls.insert(0, f"https://{HOST}/")
    return submit(urls)


if __name__ == "__main__":
    raise SystemExit(main())
