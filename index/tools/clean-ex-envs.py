"""Remove all theorem/proof/lemma environments from exercise blocks.
Convert to \\textsl{Thm.} / \\textsl{Proof.} / \\textsl{Lemma.}"""
import glob, re

TAGS = {
    "theorem": "Theorem.",
    "proof": "Proof.",
    "lemma": "Lemma",
}

for fp in sorted(glob.glob("chapters/Chapter_*.tex")):
    if "backup" in fp:
        continue
    with open(fp, "r", encoding="utf-8") as f:
        c = f.read()

    lines = c.split("\n")

    # Find all exercise block ranges
    ex_ranges = []
    in_ex = False
    ex_start = 0
    for i, line in enumerate(lines):
        if "\\section*{Exercises}" in line:
            if in_ex:
                ex_ranges.append((ex_start, i - 1))
            in_ex = True
            ex_start = i
        elif "\\section*{" in line and "Exercises" not in line and in_ex:
            ex_ranges.append((ex_start, i - 1))
            in_ex = False
    if in_ex:
        ex_ranges.append((ex_start, len(lines) - 1))

    fixes = 0
    for start, end in ex_ranges:
        # Build the block content
        block = "\n".join(lines[start:end + 1])

        # Replace each env type
        for env_name, display in TAGS.items():
            begin_tag = "\\begin{" + env_name + "}"
            end_tag = "\\end{" + env_name + "}"

            # Pattern: \begin{env}[opt] ... \end{env}
            # Replace \begin{env}[Name] with \textsl{display (Name)}
            def repl_begin(m):
                opt = m.group(1) if m.group(1) else ""
                if opt:
                    return r"\textsl{" + display + " (" + opt.strip("[]") + ").}"
                else:
                    return r"\textsl{" + display + "}"

            # \begin{env}[opt]
            block = re.sub(
                re.escape(begin_tag) + r"(\[.*?\])?",
                repl_begin,
                block,
            )

            # \end{env} -> remove
            block = re.sub(re.escape(end_tag), "", block)

        # Replace the block in lines
        new_block_lines = block.split("\n")
        lines[start:end + 1] = new_block_lines
        fixes += 1

    if fixes > 0:
        with open(fp, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
        print(f"{fp.replace('chapters/', '')}: {fixes} blocks cleaned")

print("\nDone.")
