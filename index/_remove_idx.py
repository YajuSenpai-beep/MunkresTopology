"""Remove all \idx{}, \idxmath{}, \idxsub{}, \index{} commands from chapters."""
import glob, re

def brace_match(text, start):
    """Find matching } for { at position start-1."""
    depth = 0
    for i in range(start, len(text)):
        if text[i] == "{":
            depth += 1
        elif text[i] == "}":
            if depth == 0:
                return i
            depth -= 1
    return -1

def remove_idx_commands(text):
    # Process commands from longest to shortest to avoid partial matches
    result = []
    i = 0
    while i < len(text):
        # Check for \idxmath{
        if text[i:].startswith("\\idxmath{"):
            b1 = i + 8  # position of first {
            e1 = brace_match(text, b1 + 1)
            if e1 >= 0 and e1 + 1 < len(text) and text[e1 + 1] == "{":
                b2 = e1 + 1
                e2 = brace_match(text, b2 + 1)
                if e2 >= 0:
                    # Keep only the display part (second arg)
                    result.append(text[b2 + 1:e2])
                    i = e2 + 1
                    continue
        # Check for \idx{
        elif text[i:].startswith("\\idx{"):
            b1 = i + 4
            e1 = brace_match(text, b1 + 1)
            if e1 >= 0:
                # Keep the term text
                result.append(text[b1 + 1:e1])
                i = e1 + 1
                continue
        # Check for \idxsub{...}{...}
        elif text[i:].startswith("\\idxsub{"):
            b1 = i + 7
            e1 = brace_match(text, b1 + 1)
            if e1 >= 0 and e1 + 1 < len(text) and text[e1 + 1] == "{":
                b2 = e1 + 1
                e2 = brace_match(text, b2 + 1)
                if e2 >= 0:
                    # Remove entirely (no visible text)
                    i = e2 + 1
                    continue
        # Check for \index{
        elif text[i:].startswith("\\index{"):
            b1 = i + 6
            e1 = brace_match(text, b1 + 1)
            if e1 >= 0:
                # Remove entirely
                i = e1 + 1
                continue
        # Not an idx command
        result.append(text[i])
        i += 1

    return "".join(result)

for fp in sorted(glob.glob("chapters/Chapter_*.tex")):
    if "backup" in fp or "test" in fp:
        continue
    with open(fp, "r", encoding="utf-8") as f:
        c = f.read()

    before = c.count("\\idx{") + c.count("\\idxmath{") + c.count("\\idxsub{") + c.count("\\index{")
    if before == 0:
        continue

    new_c = remove_idx_commands(c)
    after = new_c.count("\\idx{") + new_c.count("\\idxmath{") + new_c.count("\\idxsub{")

    with open(fp, "w", encoding="utf-8") as f:
        f.write(new_c)
    name = fp.replace("chapters/Chapter_", "").replace(".tex", "").replace("_", " ")
    print("{}: {} -> {} idx removed".format(name, before, after))

print("Done.")
