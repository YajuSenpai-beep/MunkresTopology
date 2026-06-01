r"""Post-process tex files after engine insertion: idx→index, capitalize, sort keys.

Run AFTER `latex-index insert` to normalize all index entries in tex source.
This eliminates the need for _fix_ind.py post-processing of .ind files.
"""
import glob

bs = chr(92)

for fn in sorted(glob.glob("../chapters/Chapter_*.tex")):
    with open(fn, encoding="utf-8") as f:
        c = f.read()

    # ── 1. Convert \idx commands to \index ──
    # \idx[display]{key} → \index{key}
    while True:
        i = c.find(bs + "idx[")
        if i < 0:
            break
        bd = c.find("]", i + 4)
        b2 = c.find("{", bd + 1)
        b3 = c.find("}", b2 + 1)
        if bd > 0 and b3 > 0:
            c = c[:i] + bs + "index{" + c[b2 + 1 : b3] + "}" + c[b3 + 1 :]
    c = c.replace(bs + "idx{", bs + "index{")
    c = c.replace(bs + "idxmath{", bs + "index{")
    c = c.replace(bs + "idxsub{", bs + "index{")

    # ── 2. Fix two-argument \index{sort}{display} → \index{sort@display} ──
    i = 0
    while True:
        i = c.find(bs + "index{", i)
        if i < 0:
            break
        b1 = c.find("}", i + 7)
        if b1 < 0:
            break
        if b1 + 1 < len(c) and c[b1 + 1] == "{":
            b2 = c.find("}", b1 + 2)
            if b2 > 0:
                c = (
                    c[:i]
                    + bs
                    + "index{"
                    + c[i + 7 : b1]
                    + "@"
                    + c[b1 + 2 : b2]
                    + "}"
                    + c[b2 + 1 :]
                )
                i += 1
        i += 1

    # ── 3. Capitalize + add lowercase sort keys to simple text entries ──
    i = 0
    while True:
        i = c.find(bs + "index{", i)
        if i < 0:
            break
        b1 = c.find("}", i + 7)
        if b1 < 0 or b1 - i > 200:
            i += 1
            continue
        key = c[i + 7 : b1]
        # Skip entries with @ ! \ $ (already have sort key, sub-entry, or math)
        if "@" in key or "!" in key or bs in key or "$" in key:
            i = b1 + 1
            continue
        # Capitalize first letter
        cap = (
            key[0].upper() + key[1:]
            if key and key[0].isalpha() and key[0].islower()
            else key
        )
        lk = key.lower()
        if cap != key and lk != key:
            c = c[: i + 7] + lk + "@" + cap + c[b1:]
        elif cap != key:
            c = c[: i + 7] + cap + c[b1:]
        elif lk != key:
            c = c[: i + 7] + lk + "@" + key + c[b1:]
        i = c.find("}", i + 7) + 1

    # ── 4. Add letter sort keys to symbol entries ──
    symbol_fixes = {
        "2-cell": "T",
        "2-manifold": "T",
    }
    for term, letter in symbol_fixes.items():
        old = bs + "index{" + term
        if old in c:
            c = c.replace(old, bs + "index{" + letter + "@" + term)

    with open(fn, "w", encoding="utf-8") as f:
        f.write(c)

print("Post-fix complete: idx→index, two-arg, capitalize, sort keys.")
