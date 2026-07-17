import os
from datetime import datetime

base_url = "https://rechnify.at"

html_files = []
for root, _, files in os.walk("."):
    if "node_modules" in root or ".git" in root or "scratch" in root:
        continue
    for file in files:
        if file.endswith(".html"):
            path = os.path.join(root, file)
            html_files.append(path)

sitemap_urls = []
for path in html_files:
    # clean path
    cleaned = path.replace("./", "/").replace("\\", "/")
    if cleaned == "/index.html":
        loc = base_url + "/"
    else:
        loc = base_url + cleaned
        
    sitemap_urls.append(f"""  <url>
    <loc>{loc}</loc>
    <lastmod>{datetime.now().strftime('%Y-%m-%d')}</lastmod>
    <changefreq>weekly</changefreq>
  </url>""")

sitemap = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{chr(10).join(sitemap_urls)}
</urlset>"""

with open("sitemap.xml", "w") as f:
    f.write(sitemap)
    
print("Updated sitemap.xml")
