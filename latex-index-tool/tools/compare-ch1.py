"""Compare Ch1 idx displays with original PDF text."""
import glob, os

# Extract all idx displays from Ch1 LaTeX
with open("chapters/Chapter_1_Set_Theory_and_Logic.tex", "r", encoding="utf-8") as f:
    c = f.read()

displays = []
i = 0
while i < len(c):
    if c[i:i+5] == "\\idx{":
        j = i + 5; depth = 1
        while j < len(c) and depth > 0:
            if c[j] == "{": depth += 1
            elif c[j] == "}": depth -= 1
            j += 1
        displays.append(c[i+5:j-1])
        i = j
    elif c[i:i+6] == "\\idx[":
        k = c.index("]", i + 6)
        display = c[i+6:k]
        displays.append(display)
        i = k + 1
    else:
        i += 1

displays = sorted(set(d for d in displays if len(d) < 80))
print("Ch1: {} unique idx display texts".format(len(displays)))

# Read parsed original PDF text
base = "C:/Users/didhf/mineru-downloads"
orig = ""
for fn in os.listdir(base):
    if fn.startswith("chap1_") and fn.endswith(".md"):
        with open(os.path.join(base, fn), "r", encoding="utf-8") as f:
            orig += f.read()

print("Original text: {} chars".format(len(orig)))

# Check each display
missing = []
for d in displays:
    # Strip LaTeX formatting for comparison
    clean = d.replace("{", "").replace("}", "")
    clean = clean.replace("\\mathbb{Z}", "Z").replace("\\mathbb{R}", "R")
    clean = clean.replace("\\mathcal", "").replace("\\mathbf", "")
    clean = clean.replace("\\left", "").replace("\\right", "")
    clean = clean.replace("\\lbrack", "[").replace("\\rbrack", "]")
    # Remove any remaining LaTeX commands
    import re
    clean = re.sub(r"\\[a-zA-Z]+\{", "", clean)
    clean = clean.replace("}", "")

    if clean.lower() not in orig.lower() and len(clean) > 2:
        missing.append((d, clean))

print("\nDisplays NOT found in original: {}".format(len(missing)))
for d, clean in missing[:30]:
    print("  display: [{}]".format(d))
    print("    clean:  [{}]".format(clean))
