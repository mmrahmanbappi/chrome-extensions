#!/usr/bin/env python3
"""Makes web images and 1200x630 social images from each tool's promo picture.

Run from the repository root:  python3 tools/make_images.py   (needs Pillow)
"""
import glob
import os

from PIL import Image, ImageDraw, ImageFont

os.makedirs("images/og", exist_ok=True)
os.makedirs("images/icons", exist_ok=True)
slugs = sorted(p.split("/")[1] for p in glob.glob("technical-seo/*/promo/linkedin-post.png"))
for s in slugs:
    src = Image.open(f"technical-seo/{s}/promo/linkedin-post.png").convert("RGB")
    w, h = src.size
    for width in (1200, 800):
        src.resize((width, int(h * width / w)), Image.LANCZOS).save(f"images/{s}-{width}.webp", "WEBP", quality=82, method=6)
    src.resize((1200, int(h * 1200 / w)), Image.LANCZOS).save(f"images/{s}-1200.jpg", "JPEG", quality=82, optimize=True, progressive=True)
    src.crop((0, 0, w, int(w / 1.905))).resize((1200, 630), Image.LANCZOS).save(f"images/og/{s}.jpg", "JPEG", quality=85, optimize=True)
    Image.open(f"technical-seo/{s}/icons/icon128.png").save(f"images/icons/{s}.png")

# Social image for the home page
bold = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
regular = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
og = Image.new("RGB", (1200, 630), (246, 245, 241))
d = ImageDraw.Draw(og)
d.text((80, 90), "Seven free SEO", font=ImageFont.truetype(bold, 76), fill=(20, 35, 28))
d.text((80, 180), "Chrome extensions", font=ImageFont.truetype(bold, 76), fill=(20, 35, 28))
d.text((84, 300), "Orphan pages, click depth, canonical chains, crawl budget,", font=ImageFont.truetype(regular, 30), fill=(90, 100, 95))
d.text((84, 342), "the 2MB limit, cache and security audits.", font=ImageFont.truetype(regular, 30), fill=(90, 100, 95))
x = 84
for s in slugs:
    icon = Image.open(f"technical-seo/{s}/icons/icon128.png").convert("RGBA").resize((96, 96), Image.LANCZOS)
    og.paste(icon, (x, 440), icon)
    x += 140
d.text((84, 575), "mmseo.app", font=ImageFont.truetype(regular, 26), fill=(26, 140, 96))
og.save("images/og/home.jpg", "JPEG", quality=88, optimize=True)
print("images done")
