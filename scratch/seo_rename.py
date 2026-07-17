import os
import re

replacements = {
    "gehaltsrechner.html": {
        "title": "Brutto Netto Rechner",
        "h1": "Brutto Netto Rechner"
    },
    "sachbezugsrechner.html": {
        "title": "Firmenwagenrechner & Sachbezug",
        "h1": "Firmenwagenrechner & Sachbezug"
    },
    "pendlerrechner.html": {
        "title": "Pendlerpauschale Rechner",
        "h1": "Pendlerpauschale Rechner"
    },
    "mwst-rechner.html": {
        "title": "Mehrwertsteuer-Rechner",
        "h1": "Mehrwertsteuer-Rechner"
    },
    "kommen-gehen-rechner.html": {
        "title": "Arbeitszeitrechner",
        "h1": "Arbeitszeitrechner"
    }
}

base_dir = "/Users/bayrakf/Applications (Parallels)/rechnify.at"
directories_to_scan = [
    os.path.join(base_dir, "finanzen"),
    os.path.join(base_dir, "arbeitszeit"),
    os.path.join(base_dir, "de", "finanzen"),
    os.path.join(base_dir, "de", "arbeitszeit")
]

for directory in directories_to_scan:
    if not os.path.exists(directory):
        continue
    for filename in os.listdir(directory):
        if filename in replacements:
            filepath = os.path.join(directory, filename)
            with open(filepath, 'r') as f:
                content = f.read()

            new_title = replacements[filename]["title"]
            new_h1 = replacements[filename]["h1"]
            
            is_de = "/de/" in filepath
            country_suffix = " Deutschland" if is_de else " Österreich"
            
            # Find and replace title
            content = re.sub(r'<title>.*?</title>', f'<title>{new_title}{country_suffix} | rechnify.at</title>', content)
            # Find and replace H1
            content = re.sub(r'<h1.*?>.*?</h1>', f'<h1 style="margin-bottom:8px;">{new_h1}{country_suffix}</h1>', content)

            with open(filepath, 'w') as f:
                f.write(content)
            print(f"Updated {filepath}")
