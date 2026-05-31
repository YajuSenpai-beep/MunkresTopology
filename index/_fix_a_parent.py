"""Fix \item (a) TEXT -> \item + sub-enumerate with (a) as first item."""
import glob

for fp in sorted(glob.glob("chapters/Chapter_[2-9]_*.tex")) + sorted(glob.glob("chapters/Chapter_1[0-4]_*.tex")):
    with open(fp, "r", encoding="utf-8") as f:
        lines = f.readlines()

    fixes = 0
    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.lstrip()

        # Match: leading whitespace, \item (a) , then content
        if not stripped.startswith("\\item (a) "):
            i += 1
            continue

        # Check if \begin{enumerate} is on the same line (skip those)
        if "\\begin{enumerate}" in stripped:
            i += 1
            continue

        # Find the indent
        indent = line[:len(line) - len(line.lstrip())]
        # Extract the (a) content
        a_text = stripped[len("\\item (a) "):]

        # Find next non-empty line
        j = i + 1
        while j < len(lines) and not lines[j].strip():
            j += 1

        # Check if next line starts \begin{enumerate}
        if j >= len(lines):
            i += 1
            continue

        if not lines[j].lstrip().startswith("\\begin{enumerate}"):
            i += 1
            continue

        # Fix: change this line to just \item
        lines[i] = indent + "\\item\n"

        # Find first \item in the sub-enumerate, insert (a) before it
        k = j + 1
        while k < len(lines):
            if lines[k].lstrip().startswith("\\item"):
                sub_indent = lines[k][:len(lines[k]) - len(lines[k].lstrip())]
                lines.insert(k, sub_indent + "\\item " + a_text + "\n")
                fixes += 1
                break
            k += 1

        i += 1

    if fixes > 0:
        with open(fp, "w", encoding="utf-8") as f:
            f.writelines(lines)
        name = fp.replace("chapters/Chapter_", "").replace(".tex", "").replace("_", " ")
        print(f"{name}: {fixes} fixes")

print("Done.")
