"""Check all chapters for environment formatting: begin-content-end should be 3+ lines."""
import glob

envs = ["proof", "theorem", "lemma", "corollary", "definition", "example", "proposition"]

files = sorted(glob.glob("chapters/Chapter_*.tex"))

total_one_line = 0
total_begin_text = 0
total_text_end = 0

for fp in files:
    name = fp.replace("chapters/Chapter_", "").replace(".tex", "").replace("_", " ")
    with open(fp, "r", encoding="utf-8") as f:
        lines = f.readlines()

    issues = []

    for env in envs:
        begin_tag = "\\begin{" + env + "}"
        end_tag = "\\end{" + env + "}"

        for i, line in enumerate(lines, 1):
            stripped = line.strip()

            # Pattern 1: \begin{env}...content...\end{env} on ONE line
            if begin_tag in stripped and end_tag in stripped:
                issues.append(f"L{i}: {env} on ONE line: {stripped[:80]}")
                total_one_line += 1

            # Pattern 2: \begin{env} has text after it (no newline)
            if begin_tag in stripped:
                after_begin = stripped[stripped.index(begin_tag) + len(begin_tag):].strip()
                if after_begin and not after_begin.startswith("[") and not after_begin.startswith("%"):
                    issues.append(f"L{i}: {env} begin then text: {stripped[:80]}")
                    total_begin_text += 1

            # Pattern 3: text before \end{env} on same line (not just whitespace)
            if end_tag in stripped:
                before_end = stripped[:stripped.index(end_tag)].strip()
                # Skip if it's just "\item" or empty (begin and end on different lines)
                if before_end and begin_tag not in stripped:
                    # Check if it's just a period or short ending
                    if len(before_end) > 3 and not before_end.startswith("\\item"):
                        issues.append(f"L{i}: {env} text before end: {stripped[:80]}")
                        total_text_end += 1

    if issues:
        print(f"\n## {name} ({len(issues)} issues)")
        for iss in issues[:15]:
            print(f"  {iss}")
        if len(issues) > 15:
            print(f"  ... and {len(issues) - 15} more")

print(f"\n\nTotal: 1-line={total_one_line}, begin+text={total_begin_text}, text+end={total_text_end}")
