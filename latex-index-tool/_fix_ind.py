"""Post-process .ind: redistribute entries from empty group to letter groups.
Usage: python _fix_ind.py
Input: ../Topology_by_Munkres.ind (modified in place)
"""
import sys, os
from collections import defaultdict
bs = chr(92)

ind_path = "../Topology_by_Munkres.ind"
with open(ind_path, "r", encoding="utf-8") as f:
    lines = f.readlines()

# === Step 1: Remove empty lettergroup and collect its entries ===
new_lines = []
empty_entries = []
i = 0
while i < len(lines):
    s = lines[i].strip()
    if s == bs + "lettergroup{}":
        i += 1
        while i < len(lines) and not lines[i].strip().startswith(bs + "lettergroup{"):
            if lines[i].strip().startswith(bs + "item "):
                empty_entries.append(lines[i])
            i += 1
        continue
    new_lines.append(lines[i])
    i += 1

if empty_entries:
    print(f"Found {len(empty_entries)} entries in empty group.")
else:
    print("No empty group. Nothing to do.")
    sys.exit(0)

# === Step 2: Assign each entry to a letter group ===
letter_map = {
    # Symbol -> letter mapping
    "mathbb{R}": "R",
    "{B}^{n}": "B",
    "{S}^{1}": "S",
    "{S}^{n}": "S",
    "{h}_{ * }": "H",
    "2-cell": "T",
    "2-manifold": "T",
    "{P}^{2}": "P",
    "bar{A}": "A",
    "mathbb  {R}": "R",
    "mathbb{R}}^{J}": "R",
    "mathbb{R}}_{K}": "R",
    "mathbb{R}}_{\\ell": "R",
    "mathbb{R}}(\\ell": "R",
    "{\\mathbb  {R}}": "R",
    "{\\mathbb{R}}^{J}": "R",
    "{\\mathbb{R}}_{K}": "R",
    "{\\mathbb{R}}_{\\ell": "R",
}

letter_positions = {}
for i, line in enumerate(new_lines):
    if line.strip().startswith(bs + "lettergroup{"):
        letter = line.strip()[len(bs + "lettergroup{") : -1]
        letter_positions[letter] = i

insertions = defaultdict(list)
for line in empty_entries:
    s = line.strip()
    entry = s[6:]  # after \item
    letter = None

    # Try exact match first
    for pattern, l in letter_map.items():
        if pattern in entry:
            letter = l
            break

    # Try numeric -> word mapping
    if not letter:
        if entry.startswith("2-"):
            letter = "T"
    # Try mathbb{R} → R, mathbb{N} → N, etc
    if not letter:
        for math_letter in [("mathbb{R}", "R"), ("mathbb{N}", "N"), ("mathbb{Z}", "Z"),
                            ("mathbb{Q}", "Q"), ("mathbb{C}", "C")]:
            if math_letter[0] in entry:
                letter = math_letter[1]; break

    if letter and letter in letter_positions:
        insertions[letter].append(line)
    else:
        print(f"  WARNING: could not assign: {entry[:60]}")

# === Step 3: Rebuild with insertions ===
final = []
for i, line in enumerate(new_lines):
    final.append(line)
    s = line.strip()
    if s.startswith(bs + "lettergroup{"):
        letter = s[len(bs + "lettergroup{") : -1]
        if letter in insertions:
            for el in insertions[letter]:
                final.append(el)
            del insertions[letter]

with open(ind_path, "w", encoding="utf-8") as f:
    f.writelines(final)

# Verify
with open(ind_path, "r", encoding="utf-8") as f:
    result = f.read()
remains = "lettergroup{}" in result
print(f"Empty group remaining: {remains}")
print(f"Lines: {len(lines)} -> {len(final)}")
