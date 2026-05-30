with open("chapters/Chapter_1_Set_Theory_and_Logic.tex", "r", encoding="utf-8") as f:
    lines = f.readlines()

# Find lines with "\item (a) ..." that are immediately followed by a \begin{enumerate}
# These need the (a) content moved into the sub-enumerate
i = 0
fixes = 0
while i < len(lines):
    line = lines[i]
    # Check if this line starts with \item (a) (with optional whitespace indent)
    stripped = line.lstrip()
    if stripped.startswith("\\item (a) "):
        # Check if the next non-empty line starts a sub-enumerate
        j = i + 1
        while j < len(lines) and lines[j].strip() == "":
            j += 1
        if j < len(lines) and "\\begin{enumerate}" in lines[j]:
            # Extract the (a) content
            content = stripped[len("\\item (a) "):]

            # Replace this line with just \item (same indentation)
            indent = line[:len(line) - len(line.lstrip())]
            lines[i] = indent + "\\item\n"

            # Find the first \item in the sub-enumerate and insert the (a) content before it
            k = j + 1
            while k < len(lines):
                if "\\item" in lines[k]:
                    sub_indent = lines[k][:len(lines[k]) - len(lines[k].lstrip())]
                    lines.insert(k, sub_indent + "\\item " + content)
                    fixes += 1
                    break
                k += 1

    i += 1

with open("chapters/Chapter_1_Set_Theory_and_Logic.tex", "w", encoding="utf-8") as f:
    f.writelines(lines)

print(f"Fixed {fixes} exercises.")
