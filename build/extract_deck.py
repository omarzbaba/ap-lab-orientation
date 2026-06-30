#!/usr/bin/env python3
"""Extract ordered text + referenced media per slide from an unzipped PPTX."""
import os, re, sys, glob
import xml.etree.ElementTree as ET

base = sys.argv[1]
NS = {
    'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
    'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships',
}

def slide_num(path):
    m = re.search(r'slide(\d+)\.xml$', path)
    return int(m.group(1)) if m else 0

slides = sorted(glob.glob(os.path.join(base, 'ppt/slides/slide*.xml')), key=slide_num)

for sp in slides:
    n = slide_num(sp)
    tree = ET.parse(sp)
    root = tree.getroot()
    # Ordered text: walk paragraphs, join runs
    lines = []
    for p in root.iter('{http://schemas.openxmlformats.org/drawingml/2006/main}p'):
        runs = [t.text for t in p.iter('{http://schemas.openxmlformats.org/drawingml/2006/main}t') if t.text]
        txt = ''.join(runs).strip()
        if txt:
            lines.append(txt)
    # Media refs from the slide's rels
    rels_path = os.path.join(base, 'ppt/slides/_rels', f'slide{n}.xml.rels')
    media = []
    if os.path.exists(rels_path):
        rtree = ET.parse(rels_path)
        for rel in rtree.getroot():
            tgt = rel.get('Target', '')
            if 'media/' in tgt:
                media.append(os.path.basename(tgt))
    print(f"===== SLIDE {n} =====")
    if media:
        print(f"[images: {', '.join(sorted(set(media)))}]")
    for ln in lines:
        print(f"  • {ln}")
    if not lines:
        print("  (no text)")
    print()
