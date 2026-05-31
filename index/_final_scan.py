"""Final punctuation/OCR scan for Ch2-14."""
import glob

for fp in sorted(glob.glob("chapters/Chapter_[2-9]_*.tex")) + sorted(glob.glob("chapters/Chapter_1[0-4]_*.tex")):
    name = fp.replace("chapters/Chapter_","").replace(".tex","").replace("_"," ")
    with open(fp, "r", encoding="utf-8") as f:
        c = f.read()
    lines = c.split("\n")
    issues = []

    for i, line in enumerate(lines, 1):
        s = line.strip()
        if not s or s.startswith("%"):
            continue

        # Spelling
        for w in ["ongin","posiave","Structly","ngorously","conduction",
                  "Schernatically","simplyby","Siliarly","to proved","Simularly"]:
            if w in s:
                issues.append("L{}: spelling '{}'".format(i, w))

        # mathbf Z or A
        if "\\mathbf{Z}" in s or "\\mathbf{A}" in s:
            issues.append("L{}: mathbf font".format(i))

        # Unicode smart quotes
        if "“" in s or "”" in s or "‘" in s or "’" in s:
            issues.append("L{}: Unicode smart quote".format(i))

        # Unbalanced LaTeX quotes (simple heuristic)
        oq = s.count("``")
        cq = s.count("''")
        if oq != cq and (oq > 0 or cq > 0):
            issues.append("L{}: unbalanced quotes ({}``/{})".format(i, oq, cq, ''))

        # Period-for-colon: f.A -> f : A
        if "f.\\mathbb" in s or "h.\\{" in s:
            issues.append("L{}: period-for-colon".format(i))

    if issues:
        print("\n{}: {} issues".format(name, len(issues)))
        for iss in issues[:8]:
            print("  " + iss)
        if len(issues) > 8:
            print("  ... +{}".format(len(issues)-8))
    else:
        print("{}: clean".format(name))

print("\nDone.")
