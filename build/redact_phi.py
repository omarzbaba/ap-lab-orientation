#!/usr/bin/env python3
"""Redact patient identifiers from Dr. Favaza's lab photos so they can be reused.

Reads the UNTOUCHED originals in assets/originals/, draws OPAQUE boxes (not blur —
blur can stay legible) over the label regions an automated pathologist review flagged
as containing readable name / MRN / DOB, and writes the redacted web copy to
assets/img/. Reproducible and idempotent. Originals are never modified (they still
contain PHI — do not distribute assets/originals/ or source/).

Boxes are fractional (x0,y0,x1,y1) of each image's width/height.
"""
import os
from PIL import Image, ImageDraw

HERE = os.path.dirname(__file__)
ORIG = os.path.join(HERE, "..", "assets", "originals")
IMG = os.path.join(HERE, "..", "assets", "img")
NAVY = (13, 27, 42)        # #0d1b2a
BORDER = (0, 119, 182)     # #0077b6
MAXDIM = 2200              # match the web-image pipeline downscale

# web_name -> (original_name, [fractional boxes])
JOBS = {
    "image5.jpg":   ("image5.png",   [(0.42, 0.52, 0.76, 0.84),   # jar label: name/MRN/DOB + handwriting
                                       (0.76, 0.58, 1.00, 0.81)]), # cassette label
    "image32.jpeg": ("image32.jpeg", [(0.00, 0.00, 1.00, 0.33),   # top slide-label row + notes above
                                       (0.00, 0.46, 0.99, 0.66)]), # bottom slide-label row
    "image33.jpeg": ("image33.jpeg", [(0.02, 0.09, 0.83, 0.30)]), # slide labels
}
DELETE = ["image4.jpg", "image25.jpeg"]   # unused, PHI-heavy — remove from deployed set

def process(web_name, orig_name, boxes):
    src = os.path.join(ORIG, orig_name)
    if not os.path.exists(src):
        print(f"  [skip] original {orig_name} not found"); return
    im = Image.open(src).convert("RGB")
    if max(im.size) > MAXDIM:
        s = MAXDIM / max(im.size)
        im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    w, h = im.size
    d = ImageDraw.Draw(im)
    for (x0, y0, x1, y1) in boxes:
        px = (int(x0 * w), int(y0 * h), int(x1 * w), int(y1 * h))
        d.rectangle(px, fill=NAVY)
        d.rectangle(px, outline=BORDER, width=max(2, w // 600))
    out = os.path.join(IMG, web_name)
    im.save(out, quality=88)
    print(f"  {web_name}  <- {orig_name}  ({len(boxes)} box(es)) [{w}x{h}]")

print("Redacting (from originals):")
for web, (orig, boxes) in JOBS.items():
    process(web, orig, boxes)

print("Removing unused PHI-heavy files from assets/img/:")
for fn in DELETE:
    p = os.path.join(IMG, fn)
    if os.path.exists(p):
        os.remove(p); print(f"  removed {fn}")
    else:
        print(f"  [skip] {fn} already gone")
print("Done. (assets/originals/ unchanged and still contains PHI.)")
