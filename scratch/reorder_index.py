import re

filepath = "/Users/bayrakf/Applications (Parallels)/rechnify.at/index.html"
with open(filepath, "r") as f:
    content = f.read()

# Find the arbeitszeit section
match_arb = re.search(r'(<section class="category-section" id="arbeitszeit">.*?</section>)', content, flags=re.DOTALL)
arb_text = match_arb.group(1)

# Find the finanzen section
match_fin = re.search(r'(<section class="category-section" id="finanzen">.*?</section>)', content, flags=re.DOTALL)
fin_text = match_fin.group(1)

if arb_text and fin_text and content.find(arb_text) < content.find(fin_text):
    # Swap them
    new_content = content.replace(arb_text, "%%ARB_PLACEHOLDER%%")
    new_content = new_content.replace(fin_text, arb_text)
    new_content = new_content.replace("%%ARB_PLACEHOLDER%%", fin_text)
    
    with open(filepath, "w") as f:
        f.write(new_content)
    print("Swapped sections successfully.")
else:
    print("Already swapped or not found.")
