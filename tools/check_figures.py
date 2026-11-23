# -*- coding: utf-8 -*-
"""检查 LaTeX 里的图片引用是否都有对应 PDF。

规则：
- `\\munkresfig{name}` 和 `\\includegraphics{images/name}` 都算引用；
- 每个引用必须有 `images/name.pdf`；
- 可选 `--require-no-png`：要求 images/ 下不再有 PNG（PNG→PDF 收尾后启用）。
"""
import argparse
import glob
import os
import re
import sys

MREF = re.compile(r'\\munkresfig(?:\[[^\]]*\])?\{([^}]+)\}')
IREF = re.compile(r'\\includegraphics(?:\[[^\]]*\])?\{([^}]+)\}')

def refs_from_tex(root):
    refs = set()
    for f in glob.glob(os.path.join(root, "**", "*.tex"), recursive=True):
        if os.sep + ".git" + os.sep in f:
            continue
        with open(f, encoding="utf-8", errors="ignore") as fh:
            s = fh.read()
        refs.update(MREF.findall(s))
        for p in IREF.findall(s):
            if not p.startswith("images/"):
                continue
            n = p[len("images/"):]
            for ext in (".pdf", ".png", ".jpg", ".jpeg"):
                if n.lower().endswith(ext):
                    n = n[:-len(ext)]
                    break
            refs.add(n)
    return refs

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".")
    ap.add_argument("--require-no-png", action="store_true")
    args = ap.parse_args()
    root = os.path.abspath(args.root)
    refs = refs_from_tex(root)
    images = os.path.join(root, "images")
    pdfs = {os.path.basename(p)[:-4] for p in glob.glob(os.path.join(images, "*.pdf"))}
    missing = sorted(refs - pdfs)
    print("figure refs: %d, pdf: %d, missing: %d" % (len(refs), len(pdfs), len(missing)))
    for n in missing:
        print("MISSING PDF: images/%s.pdf" % n)
    if args.require_no_png:
        pngs = sorted(os.path.basename(p) for p in glob.glob(os.path.join(images, "*.png")))
        if pngs:
            print("PNG REMAINS: %d (first: %s)" % (len(pngs), ", ".join(pngs[:5])))
    if missing or (args.require_no_png and glob.glob(os.path.join(images, "*.png"))):
        return 1
    return 0

if __name__ == "__main__":
    sys.exit(main())
