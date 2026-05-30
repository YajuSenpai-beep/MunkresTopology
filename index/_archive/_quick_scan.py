import re
with open("chapters/Chapter_1_Set_Theory_and_Logic.tex", "r", encoding="utf-8") as f:
    c = f.read()

blocks = list(re.finditer(r"\\section\*\{Exercises\}|\\section\*\{\\* Supplementary", c))
print(f"Exercise blocks: {len(blocks)}")

# Check for (a) in parent text: \item (a) ...content... \begin{enumerate}
# We look for lines where \item (a) appears before a sub-enumerate
pattern = r"\\item \(a\).*?\\begin\{enumerate\}"
matches = re.findall(pattern, c, re.DOTALL)
if matches:
    print(f"WARNING: {len(matches)} exercises still have (a) in parent:")
    for m in matches:
        print(f"  {m[:100]}...")
else:
    print("OK: No (a) in parent text")

# Check OCR artifacts
checks = [
    ("{A}_{t}", "{A}_{t} OCR artifact"),
    ("{B}_{t}", "{B}_{t} OCR artifact"),
    (r"f.\{ 1,\\ldots ,8\}", "f. colon error"),
    (r"h \\cdot  B", "h cdot colon error"),
    (r"k \\cdot  \{S\}", "k cdot colon error"),
    ("\\rbrack", "rbrack residual"),
]
for pattern, desc in checks:
    if pattern in c:
        print(f"WARNING: {desc}")
    else:
        print(f"OK: {desc} not found")

# Check exercises 3/4 merged
if ". 4. The \\idx{Fibonacci}" in c:
    print("WARNING: Ex3/4 still merged")
else:
    print("OK: Ex3/4 separated")

if ". *8. Show" in c:
    print("WARNING: Ex8 still merged")
else:
    print("OK: Ex8 separated")

print("\nDone.")
