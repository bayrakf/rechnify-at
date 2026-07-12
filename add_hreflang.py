import os

tools = [
    ('arbeitszeit/urlaubstage-rechner.html', 'de/arbeitszeit/urlaubstage-rechner.html'),
    ('arbeitszeit/ueberstundenrechner.html', 'de/arbeitszeit/ueberstundenrechner.html'),
    ('finanzen/mwst-rechner.html', 'de/finanzen/mwst-rechner.html')
]

for at_file, de_file in tools:
    at_path = f"/{at_file}"
    de_path = f"/{de_file}"
    
    # AT FILE
    with open(at_file, 'r') as f:
        content = f.read()
    hreflangs = f"""<link rel="alternate" hreflang="de-AT" href="https://rechnify.at{at_path}" />
  <link rel="alternate" hreflang="de-DE" href="https://rechnify.at{de_path}" />"""
    
    if 'hreflang="de-AT"' not in content:
        content = content.replace(f'<link rel="canonical" href="https://rechnify.at{at_path}" />', 
                                  f'<link rel="canonical" href="https://rechnify.at{at_path}" />\n  {hreflangs}')
        with open(at_file, 'w') as f:
            f.write(content)
            
    # DE FILE
    with open(de_file, 'r') as f:
        content = f.read()
    if 'hreflang="de-AT"' not in content:
        content = content.replace(f'<link rel="canonical" href="https://rechnify.at{de_path}" />', 
                                  f'<link rel="canonical" href="https://rechnify.at{de_path}" />\n  {hreflangs}')
        with open(de_file, 'w') as f:
            f.write(content)

print("Hreflangs added")
