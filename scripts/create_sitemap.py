#!/usr/bin/env python3
"""Sitemap = filesystem scan. Delegates to ship_gaps.write_sitemap."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from ship_gaps import write_sitemap

if __name__ == "__main__":
    write_sitemap()
