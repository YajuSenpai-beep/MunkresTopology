"""Fix environment formatting: \begin{env}text -> \begin{env}\n\ttext"""
import glob, re

envs = ["proof", "theorem", "lemma", "corollary", "definition", "example", "proposition", "addendum", "property"]

files = sorted(glob.glob("chapters/Chapter_*[2-9]*.tex")) + \
        sorted(glob.glob("chapters/Chapter_1[0-4]*.tex"))

total = 0

for fp in files:
    name = fp.replace("chapters/Chapter_", "").replace(".tex", "").replace("_", " ")
    with open(fp, "r", encoding="utf-8") as f:
        lines = f.readlines()

    fixes = 0
    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()
        if stripped.startswith("%") or not stripped:
            i += 1
            continue

        indent = line[:len(line) - len(line.lstrip())]

        for env in envs:
            begin_tag = "\\begin{" + env + "}"
            end_tag = "\\end{" + env + "}"

            if begin_tag not in stripped:
                continue

            # Get text after \begin{env} (skip optional [arg])
            idx = stripped.index(begin_tag) + len(begin_tag)
            rest = stripped[idx:].strip()

            # Skip optional argument [name]
            if rest.startswith("["):
                bracket_depth = 0
                opt_end = -1
                for j, ch in enumerate(rest):
                    if ch == "[":
                        bracket_depth += 1
                    elif ch == "]":
                        bracket_depth -= 1
                        if bracket_depth == 0:
                            opt_end = j
                            break
                if opt_end >= 0:
                    rest = rest[opt_end + 1:].strip()

            if not rest:
                i += 1
                continue  # already clean

            # Found \begin{env} with text after it
            body_indent = indent + "\t"

            # Case 1: The \end{env} is also on this line (1-line environment)
            if end_tag in stripped:
                # Extract content between begin and end
                content_start = stripped.index(begin_tag) + len(begin_tag)
                # Skip optional arg again for content extraction
                tmp = stripped[content_start:].strip()
                if tmp.startswith("["):
                    bd = 0
                    oe = -1
                    for j, ch in enumerate(tmp):
                        if ch == "[":
                            bd += 1
                        elif ch == "]":
                            bd -= 1
                            if bd == 0:
                                oe = j
                                break
                    if oe >= 0:
                        tmp = tmp[oe + 1:].strip()
                content_end = tmp.index(end_tag)
                content = tmp[:content_end].strip()

                # Keep optional argument if present
                opt_arg = ""
                after_begin = stripped[stripped.index(begin_tag) + len(begin_tag):].strip()
                if after_begin.startswith("["):
                    bd = 0
                    oe = -1
                    for j, ch in enumerate(after_begin):
                        if ch == "[":
                            bd += 1
                        elif ch == "]":
                            bd -= 1
                            if bd == 0:
                                oe = j
                                break
                    if oe >= 0:
                        opt_arg = after_begin[:oe + 1]

                if opt_arg:
                    lines[i] = indent + begin_tag + opt_arg + "\n"
                else:
                    lines[i] = indent + begin_tag + "\n"
                lines.insert(i + 1, body_indent + content + "\n")
                lines.insert(i + 2, indent + end_tag + "\n")
                fixes += 1
                break

            # Case 2: Text after \begin{env}, \end{env} is on a later line
            else:
                # Keep optional argument
                opt_arg = ""
                after_begin = stripped[stripped.index(begin_tag) + len(begin_tag):].strip()
                if after_begin.startswith("["):
                    bd = 0
                    oe = -1
                    for j, ch in enumerate(after_begin):
                        if ch == "[":
                            bd += 1
                        elif ch == "]":
                            bd -= 1
                            if bd == 0:
                                oe = j
                                break
                    if oe >= 0:
                        opt_arg = after_begin[:oe + 1]
                        rest = after_begin[oe + 1:].strip()
                    else:
                        rest = after_begin
                else:
                    rest = after_begin

                if opt_arg:
                    lines[i] = indent + begin_tag + opt_arg + "\n"
                else:
                    lines[i] = indent + begin_tag + "\n"
                lines.insert(i + 1, body_indent + rest + "\n")
                fixes += 1
                break

        i += 1

    if fixes > 0:
        with open(fp, "w", encoding="utf-8") as f:
            f.writelines(lines)
        print(f"{name}: {fixes} fixes")
        total += fixes
    else:
        print(f"{name}: clean")

# Also fix Ch1 for any remaining issues
fp1 = "chapters/Chapter_1_Set_Theory_and_Logic.tex"
# (Ch1 is already confirmed clean, skip)

print(f"\nTotal: {total} fixes")
