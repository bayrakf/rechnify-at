import os
import glob

def insert_toggle(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    target_str = '<button class="btn-icon" id="darkModeToggle"'
    insert_str = '<button class="btn-icon country-switch" id="countryToggle" title="Land wechseln" type="button">🇦🇹 AT</button>\n        '

    if 'id="countryToggle"' not in content:
        content = content.replace(target_str, insert_str + target_str)
        with open(filepath, 'w') as f:
            f.write(content)
        print(f"Updated {filepath}")
    else:
        print(f"Skipped {filepath} (already has toggle)")

for root, dirs, files in os.walk('.'):
    for file in files:
        if file.endswith('.html'):
            insert_toggle(os.path.join(root, file))
