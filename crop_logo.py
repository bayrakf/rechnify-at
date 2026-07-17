from PIL import Image, ImageChops
import os

img_path = "/Users/bayrakf/.gemini/antigravity/brain/35ab1ad0-9ade-44ce-9d49-059ba19b927c/rechnify_logo_new_1784034210472.jpg"
img = Image.open(img_path).convert("RGB")
w, h = img.size

# We want to crop the top square part, ignoring the text at the bottom.
box = (200, 100, 800, 700)
cropped = img.crop(box)

# Now find the actual bounding box of non-white pixels
bg = Image.new(cropped.mode, cropped.size, (255, 255, 255))
diff = ImageChops.difference(cropped, bg)
bbox = diff.getbbox()

if bbox:
    # pad the bbox
    pad = 40
    new_box = (
        max(0, bbox[0] - pad),
        max(0, bbox[1] - pad),
        min(cropped.width, bbox[2] + pad),
        min(cropped.height, bbox[3] + pad)
    )
    cropped = cropped.crop(new_box)

# Make it a perfect square
cw, ch = cropped.size
size = max(cw, ch)
square = Image.new('RGB', (size, size), (255, 255, 255))
offset = ((size - cw) // 2, (size - ch) // 2)
square.paste(cropped, offset)

out_dir = "/Users/bayrakf/Applications (Parallels)/rechnify.at/assets/images"
os.makedirs(out_dir, exist_ok=True)

# Save logo.jpg
square.resize((512, 512), Image.Resampling.LANCZOS).save(f"{out_dir}/logo.jpg")

# Save favicons
square.resize((180, 180), Image.Resampling.LANCZOS).save(f"{out_dir}/apple-touch-icon.png")
square.resize((32, 32), Image.Resampling.LANCZOS).save(f"{out_dir}/favicon-32x32.png")
square.resize((16, 16), Image.Resampling.LANCZOS).save(f"{out_dir}/favicon-16x16.png")

# Save favicon.ico
square.resize((64, 64), Image.Resampling.LANCZOS).save(f"{out_dir}/favicon.ico", format="ICO")

print("Logo processed and saved!")
