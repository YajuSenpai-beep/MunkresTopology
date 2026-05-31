"""Compare chapter idx displays with original PDF text."""
import glob, os, re, sys

ch = sys.argv[1] if len(sys.argv) > 1 else "2"
chap_file = f"chapters/Chapter_{ch}_*.tex"
files = sorted(glob.glob(chap_file))
if not files:
    # Try matching by number
    pattern = f"chapters/Chapter_{ch}_*"
    files = sorted(glob.glob(pattern))
if not files:
    # Try with leading zeros or other patterns
    files = sorted(glob.glob(f"chapters/Chapter_*{ch}*"))
if not files:
    print(f"Chapter {ch} not found")
    exit(1)

fp = files[0]
name = fp.replace("chapters/Chapter_", "").replace(".tex", "").replace("_", " ")
print(f"Processing: {name}")

with open(fp, "r", encoding="utf-8") as f:
    c = f.read()

# Extract idx displays
displays = {}
i = 0
while i < len(c):
    if c[i:i+5] == "\\idx{":
        j = i + 5; depth = 1
        while j < len(c) and depth > 0:
            if c[j] == "{": depth += 1
            elif c[j] == "}": depth -= 1
            j += 1
        key = c[i+5:j-1]
        displays[key] = displays.get(key, 0) + 1
        i = j
    elif c[i:i+6] == "\\idx[":
        k = c.index("]", i + 6)
        display = c[i+6:k]
        displays[display] = displays.get(display, 0) + 1
        i = k + 1
    else:
        i += 1

print("{} unique idx displays".format(len(displays)))

# Read parsed original PDF
base = "C:/Users/didhf/mineru-downloads"
orig = ""
prefix = f"chap{ch}_"
for fn in os.listdir(base):
    if fn.startswith(prefix) and fn.endswith(".md"):
        with open(os.path.join(base, fn), "r", encoding="utf-8") as f:
            orig += f.read()

print("Original text: {} chars".format(len(orig)))

# Compare
missing = []
for d in sorted(displays.keys()):
    if len(d) < 3:
        continue
    # Clean for comparison
    clean = d.replace("{", "").replace("}", "")
    clean = re.sub(r"\\(mathbb|mathbf|mathcal|mathscr|mathfrak)\{([^}]*)\}", r"\2", clean)
    clean = re.sub(r"\\[a-zA-Z]+\{([^}]*)\}", r"\1", clean)
    clean = re.sub(r"\\[a-zA-Z]+", "", clean)
    clean = clean.replace("\\left", "").replace("\\right", "")
    clean = clean.replace("\\lbrack", "[").replace("\\rbrack", "]")
    clean = clean.strip()
    if len(clean) > 2 and clean.lower() not in orig.lower():
        missing.append((d, clean))

print("\nNOT in original: {}/{}".format(len(missing), len(displays)))
for d, clean in missing[:20]:
    print("  display: [{}]".format(d))
