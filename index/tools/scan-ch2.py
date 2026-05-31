"""Quick scan Ch2 for OCR error patterns known from Ch1."""
import re

fp = "chapters/Chapter_2_Topological_Spaces_and_Continuous_Functions.tex"
with open(fp, "r", encoding="utf-8") as f:
    c = f.read()

lines = c.split("\n")
print(f"Ch2: {len(lines)} lines\n")

issues = []

# 1. Straight double quotes
for i, line in enumerate(lines, 1):
    # Check for "text" pattern (straight quotes around words)
    m = re.findall(r'"([A-Za-z][^"]*[A-Za-z])"', line)
    if m:
        issues.append(f"L{i}: straight quotes: {m}")

# 2. Unbalanced LaTeX quotes (open ≠ close on same line, simplified)
for i, line in enumerate(lines, 1):
    open_q = line.count("``")
    close_q = line.count("''")
    if open_q != close_q and (open_q > 0 or close_q > 0):
        # Skip math superscript primes
        stripped = re.sub(r"\$.*?\$|\\\(.*?\\\)|\\\[.*?\\\]", "", line)
        o2 = stripped.count("``")
        c2 = stripped.count("''")
        if o2 != c2:
            issues.append(f"L{i}: unbalanced quotes ({open_q}`` vs {close_q}''): {line.strip()[:80]}")

# 3. Common OCR misspellings
spellings = [
    (r"\bongin\b", "origin"),
    (r"posiave", "positive"),
    (r"Structly", "Strictly"),
    (r"\bngorously\b", "rigorously"),
    (r"\bconduction\b", "condition"),
]
for pat, correct in spellings:
    for m in re.finditer(pat, c):
        line_num = c[:m.start()].count("\n") + 1
        issues.append(f"L{line_num}: spelling '{m.group()}' -> '{correct}'")

# 4. Period-for-colon in function definitions
for i, line in enumerate(lines, 1):
    m = re.findall(r"\\\([a-z]\.[A-Z]", line)
    if m:
        issues.append(f"L{i}: period-for-colon: {m}")

# 5. cdot-for-colon
for i, line in enumerate(lines, 1):
    if r"\cdot  {\" in line or r"\cdot  {" in line or r"\cdot  \math" in line:
        if "function" in line.lower() or "surjection" in line.lower() or "injection" in line.lower():
            issues.append(f"L{i}: possible cdot-for-colon: {line.strip()[:80]}")

# 6. Bracket mismatches
for i, line in enumerate(lines, 1):
    if r"\rbrack" in line and r"\left\lbrack" not in line and r"\right\rbrack" not in line:
        issues.append(f"L{i}: isolated \\rbrack: {line.strip()[:80]}")
    if line.strip().endswith("\\}") and "[Hint" in line:
        issues.append(f"L{i}: Hint ending with \\}: {line.strip()[:80]}")

# Report
if issues:
    print(f"Found {len(issues)} potential issues:\n")
    for iss in issues[:50]:
        print(f"  {iss}")
    if len(issues) > 50:
        print(f"\n  ... and {len(issues)-50} more")
else:
    print("No issues found!")
