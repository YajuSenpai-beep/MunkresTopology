"""Convert Ch2 exercise blocks to enumerate format."""
import re

fp = "chapters/Chapter_2_Topological_Spaces_and_Continuous_Functions.tex"
with open(fp, "r", encoding="utf-8") as f:
    c = f.read()

lines = c.split("\n")
blocks = []
in_block = False
block_start = 0

for i, line in enumerate(lines):
    is_ex = "\\section*{Exercises}" in line
    is_next_sec = "\\section*{" in line and not is_ex

    if is_ex:
        if in_block:
            blocks.append((block_start, i - 1))
        in_block = True
        block_start = i
    elif is_next_sec and in_block:
        blocks.append((block_start, i - 1))
        in_block = False

if in_block:
    blocks.append((block_start, len(lines) - 1))

print(f"Found {len(blocks)} exercise blocks in Ch2")

# Process each block
total_fixes = 0
for b_idx, (start, end) in enumerate(blocks):
    block_lines = lines[start + 1:end + 1]

    # Parse exercises: find numbered items and subparts
    items = []
    current = None

    for line in block_lines:
        s = line.strip()
        if not s:
            continue

        # Main exercise: number followed by period and space
        m = re.match(r"^(\d+)\.\s+(.*)", s)
        if m:
            if current:
                items.append(current)
            current = {"num": int(m.group(1)), "text": m.group(2), "subs": []}
            continue

        # Sub-part: (a), (b), etc.
        m = re.match(r"^\(([a-z])\)\s+(.*)", s)
        if m and current:
            current["subs"].append((m.group(1), m.group(2)))
            continue

        # Continuation text for current item
        if current:
            if current["subs"]:
                letter, text = current["subs"][-1]
                current["subs"][-1] = (letter, text + " " + s)
            else:
                current["text"] += " " + s

    if current:
        items.append(current)

    # Build new content
    new_lines = [lines[start]]  # \section*{Exercises}
    new_lines.append("\\begin{enumerate}[itemsep=0.4em, parsep=0pt, topsep=0pt, partopsep=0pt, leftmargin=*, label=\\arabic*., ref=\\arabic*]")

    for item in items:
        if item["subs"]:
            new_lines.append("\\item " + item["text"])
            new_lines.append("  \\begin{enumerate}[itemsep=0.2em, parsep=0pt, topsep=0pt, partopsep=0pt, leftmargin=*, label=(\\alph*), align=left]")
            for letter, text in item["subs"]:
                new_lines.append("  \\item " + text)
            new_lines.append("  \\end{enumerate}")
        else:
            new_lines.append("\\item " + item["text"])

    new_lines.append("\\end{enumerate}")

    # Replace
    old_len = end - start + 1
    lines[start:end + 1] = new_lines
    diff = len(new_lines) - old_len

    # Adjust subsequent block positions
    for j in range(b_idx + 1, len(blocks)):
        blocks[j] = (blocks[j][0] + diff, blocks[j][1] + diff)

    print(f"  Block #{b_idx + 1}: {len(items)} exercises, {sum(1 for it in items if it['subs'])} with subparts")

with open(fp, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

print("Done.")
