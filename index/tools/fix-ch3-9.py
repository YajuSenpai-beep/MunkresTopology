"""Batch fix OCR errors for Ch3-9, then convert exercises."""
import glob, re

files = sorted(glob.glob("chapters/Chapter_[3-9]_*.tex"))

print("=== PHASE 1: OCR text fixes ===\n")

for fp in files:
    name = fp.replace("chapters/Chapter_", "").replace(".tex", "").replace("_", " ")
    with open(fp, "r", encoding="utf-8") as f:
        c = f.read()

    fixes = 0

    # Use word-boundary regex for terms that could appear inside other words
    word_boundary_reps = [
        (r"\bongin\b", "origin"),  # \b prevents "belonging" -> "belorigin"
    ]
    for pat, repl in word_boundary_reps:
        new_c, n = re.subn(pat, repl, c)
        if n > 0:
            c = new_c
            fixes += n

    reps = [
        ("posiave", "positive"), ("Structly", "Strictly"),
        ("ngorously", "rigorously"), ("conduction", "condition"),
        ("Schernatically", "Schematically"), ("Siliarly", "Similarly"),
        ("to proved", "to prove"),
    ]
    for old, new in reps:
        if old in c:
            c = c.replace(old, new)
            fixes += 1

    if "{\\mathbf{Z}}_{ + }" in c:
        n = c.count("{\\mathbf{Z}}_{ + }")
        c = c.replace("{\\mathbf{Z}}_{ + }", "{\\mathbb{Z}}_{ + }")
        fixes += n

    period_fixes = [
        ("is empty On", "is empty. On"), ("is empty Not", "is empty. Not"),
        ("disjoint It", "disjoint. It"), ("surjective For", "surjective. For"),
        ("countable Since", "countable. Since"), ("countable Its", "countable. Its"),
        ("set Given", "set. Given"), ("uncountable Then", "uncountable. Then"),
        ("versions Formulated", "versions. Formulated"),
        ("however Specifically", "however. Specifically"),
    ]
    for old, new in period_fixes:
        if old in c:
            c = c.replace(old, new)
            fixes += 1

    if fixes > 0:
        with open(fp, "w", encoding="utf-8") as f:
            f.write(c)
        print(f"{name}: {fixes} OCR fixes")
    else:
        print(f"{name}: clean")

# Phase 2
print("\n=== PHASE 2: Exercise conversion ===\n")

for fp in files:
    name = fp.replace("chapters/Chapter_", "").replace(".tex", "").replace("_", " ")
    with open(fp, "r", encoding="utf-8") as f:
        c = f.read()

    if r"label=\arabic*" in c:
        print(f"{name}: already converted")
        continue

    lines = c.split("\n")
    blocks = []
    in_block = False
    block_start = 0

    for i, line in enumerate(lines):
        is_ex = "\\section*{Exercises}" in line
        is_next = "\\section*{" in line and not is_ex
        if is_ex:
            if in_block: blocks.append((block_start, i - 1))
            in_block = True; block_start = i
        elif is_next and in_block:
            blocks.append((block_start, i - 1))
            in_block = False
    if in_block: blocks.append((block_start, len(lines) - 1))

    if not blocks:
        print(f"{name}: no blocks")
        continue

    total_ex = 0
    for b_idx, (start, end) in enumerate(blocks):
        block_lines = lines[start + 1:end + 1]
        items = []
        current = None

        for line in block_lines:
            s = line.strip()
            if not s: continue
            m = re.match(r"^(\d+)\.\s+(.*)", s)
            if m:
                if current: items.append(current)
                current = {"num": int(m.group(1)), "text": m.group(2), "subs": []}
                continue
            m = re.match(r"^\(([a-z])\)\s+(.*)", s)
            if m and current:
                current["subs"].append((m.group(1), m.group(2)))
                continue
            if current:
                if current["subs"]:
                    letter, text = current["subs"][-1]
                    current["subs"][-1] = (letter, text + " " + s)
                else:
                    current["text"] += " " + s
        if current: items.append(current)

        new_lines = [lines[start]]
        new_lines.append(r"\begin{enumerate}[itemsep=0.4em, parsep=0pt, topsep=0pt, partopsep=0pt, leftmargin=*, label=\arabic*., ref=\arabic*]")
        for item in items:
            if item["subs"]:
                new_lines.append(r"\item " + item["text"])
                new_lines.append(r"  \begin{enumerate}[itemsep=0.2em, parsep=0pt, topsep=0pt, partopsep=0pt, leftmargin=*, label=(\alph*), align=left]")
                for letter, text in item["subs"]:
                    new_lines.append(r"  \item " + text)
                new_lines.append(r"  \end{enumerate}")
            else:
                new_lines.append(r"\item " + item["text"])
        new_lines.append(r"\end{enumerate}")

        old_len = end - start + 1
        lines[start:end + 1] = new_lines
        diff = len(new_lines) - old_len
        for j in range(b_idx + 1, len(blocks)):
            blocks[j] = (blocks[j][0] + diff, blocks[j][1] + diff)
        total_ex += len(items)

    with open(fp, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"{name}: {len(blocks)} blocks, {total_ex} exercises")

print("\nDone.")
