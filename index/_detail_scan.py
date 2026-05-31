"""Detailed per-chapter issue breakdown."""
import re, glob

files = sorted(glob.glob("chapters/Chapter_*[2-9]*.tex")) + \
        sorted(glob.glob("chapters/Chapter_1[0-4]*.tex"))

print("name|lines|spell|colon|bracket|quotes|font|period|star|cb_miss|ex_miss|long|total")

for fp in files:
    name = fp.replace("chapters/Chapter_", "").replace(".tex", "").replace("_", " ")
    with open(fp, "r", encoding="utf-8") as f:
        c = f.read()
    lines = c.split("\n")

    spell = sum(1 for l in lines if any(w in l for w in ["ongin", "posiave", "Structly",
        "ngorously", "conduction", "Schernatically", "simplyby", "Siliarly", "to proved"]))
    colon_p = sum(1 for l in lines if "f.\\mathbb" in l or "h.\\{" in l or "f.\\{" in l)
    bracket = sum(1 for l in lines if "\\rbrack" in l and "right\\rbrack" not in l)
    quotes = sum(1 for l in lines if l.count("``") != l.count("''") and (l.count("``") > 0 or l.count("''") > 0))
    font = sum(1 for l in lines if "\\mathbf{Z}" in l or "\\mathbf{A}" in l or "\\mathbf{C}" in l)
    period = sum(1 for l in lines if any(p in l for p in [
        "is empty On", "is empty Not", "disjoint It", "surjective For",
        "countable Since", "countable Its", "set Given", "uncountable Then",
        "versions Formulated", "however Specifically", "integers",
    ]))
    star = sum(1 for l in lines if "(*)" in l and "\\left(*" not in l and "\\(*" not in l)

    ex = c.count("\\begin{example}")
    cb = c.count("\\begin{centeredblock}")
    cb_miss = max(0, ex - cb)

    ex_sec = c.count("\\section*{Exercises}")
    en_fmt = len(re.findall(r"\\begin\{enumerate\}.*?label=\\arabic", c))
    ex_miss = max(0, ex_sec - en_fmt)

    long_lines = sum(1 for l in lines if len(l) > 250)

    tot = spell + colon_p + bracket + quotes + font + period + star + cb_miss + ex_miss + long_lines
    print(f"{name}|{len(lines)}|{spell}|{colon_p}|{bracket}|{quotes}|{font}|{period}|{star}|{cb_miss}|{ex_miss}|{long_lines}|{tot}")
