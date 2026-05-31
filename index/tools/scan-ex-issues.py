"""Scan Ch2-14 for exercise conversion issues."""
import glob, re

for fp in sorted(glob.glob("chapters/Chapter_[2-9]_*.tex")) + sorted(glob.glob("chapters/Chapter_1[0-4]_*.tex")):
    name = fp.replace("chapters/Chapter_", "").replace(".tex", "").replace("_", " ")
    with open(fp, "r", encoding="utf-8") as f:
        c = f.read()

    issues = []
    lines = c.split("\n")

    for i, line in enumerate(lines):
        s = line.strip()

        # (a) in parent text (pattern: \item (a) text text)
        if s.startswith("\\item (a) "):
            issues.append(f"L{i+1}: (a) in parent: {s[:80]}")

        # Merged exercise numbers on same line
        if re.search(r"[a-z]\)\s*\.\s*\d+\.", s):
            issues.append(f"L{i+1}: possible merged ex: {s[:80]}")

    if issues:
        print(f"\n{name}:")
        for iss in issues:
            print(f"  {iss}")
    else:
        print(f"{name}: clean")
