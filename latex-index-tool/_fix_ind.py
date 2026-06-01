r"""Post-process .ind: merge duplicates, redistribute symbols, capitalize.

Usage: python _fix_ind.py
Input/Output: ../Topology_by_Munkres.ind
"""
import sys
from collections import defaultdict

bs = chr(92)
import os
ind_path = os.path.join(os.path.dirname(__file__), "..", "Topology_by_Munkres.ind")

# === Load ===
with open(ind_path, "r", encoding="utf-8") as f:
    lines = f.readlines()

# === Merge case-duplicate entries ===
# Group main entries by lowercase text
entries_by_lower = defaultdict(list)
i = 0
while i < len(lines):
    s = lines[i].strip()
    if s.startswith(bs + "item ") and not s.startswith(bs + "subitem "):
        text = s[6:]
        pages = []
        clean = text
        while bs + "hyperpage{" in clean:
            hp = clean.find(bs + "hyperpage{")
            he = clean.find("}", hp)
            if he > hp:
                pages.append(clean[hp + 11 : he])
                clean = clean[:hp] + clean[he + 1 :]
        clean = clean.strip().rstrip(", ").lower()
        entries_by_lower[clean].append((i, text.strip(), pages))
    i += 1

to_remove = set()
for lower, group in entries_by_lower.items():
    if len(group) > 1:
        all_pages = []
        for (_, _, pages) in group:
            all_pages.extend(pages)
        unique_pages = sorted(set(all_pages), key=lambda x: int(x) if x.isdigit() else 0)
        first_idx, first_text, _ = group[0]
        # Rebuild merged line
        new_entry = first_text
        while bs + "hyperpage{" in new_entry:
            hp = new_entry.find(bs + "hyperpage{")
            he = new_entry.find("}", hp)
            if he > hp:
                new_entry = new_entry[:hp] + new_entry[he + 1 :]
        new_entry = new_entry.rstrip(", ")
        if unique_pages:
            new_entry += ", " + ", ".join(
                bs + "hyperpage{" + p + "}" for p in unique_pages
            )
        lines[first_idx] = bs + "item " + new_entry + "\n"
        for (idx, _, _) in group[1:]:
            to_remove.add(idx)

lines = [l for i, l in enumerate(lines) if i not in to_remove]
print(f"Merged: {len(to_remove)} duplicate lines")

# === Redistribute empty group entries ===
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

letter_map = {
    "mathbb{R}": "R", "{B}^{n}": "B", "{S}^{1}": "S", "{S}^{n}": "S",
    "{h}_{ * }": "H", "2-cell": "T", "2-manifold": "T", "{P}^{2}": "P",
    "bar{A}": "A", "mathbb  {R}": "R", "mathbb{R}}^{J}": "R",
    "mathbb{R}}_{K}": "R", "mathbb{R}}_{\\ell": "R",
}

letter_positions = {}
for i, line in enumerate(new_lines):
    if line.strip().startswith(bs + "lettergroup{"):
        letter = line.strip()[len(bs + "lettergroup{") : -1]
        letter_positions[letter] = i

insertions = defaultdict(list)
for line in empty_entries:
    s = line.strip()
    entry = s[6:]
    letter = None
    for pattern, l in letter_map.items():
        if pattern in entry:
            letter = l; break
    if not letter and entry.startswith("2-"):
        letter = "T"
    if not letter:
        for ml in [("mathbb{R}", "R"), ("mathbb{N}", "N"), ("mathbb{Z}", "Z")]:
            if ml[0] in entry:
                letter = ml[1]; break
    if letter and letter in letter_positions:
        insertions[letter].append(line)

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

print(f"Redistributed: {len(empty_entries)} symbol entries")

# === Capitalize first letter (skip math symbols) ===
for idx, line in enumerate(final):
    s = line.strip()
    if s.startswith(bs + "item ") and not s.startswith(bs + "subitem "):
        rest = s[6:]
        first_alpha = -1
        i = 0
        while i < len(rest):
            ch = rest[i]
            if ch == bs:
                j = i + 1
                while j < len(rest) and rest[j].isalpha():
                    j += 1
                i = j; continue
            elif ch in "{$":
                depth = 1 if ch == "{" else 0
                i += 1
                while i < len(rest) and depth > 0:
                    if rest[i] == "{": depth += 1
                    elif rest[i] == "}": depth -= 1
                    i += 1
                continue
            elif ch.isalpha():
                first_alpha = i; break
            else: i += 1
        if first_alpha >= 0 and rest[first_alpha].islower():
            rest = rest[:first_alpha] + rest[first_alpha].upper() + rest[first_alpha + 1 :]
        final[idx] = bs + "item " + rest + "\n"

# === Write ===
with open(ind_path, "w", encoding="utf-8") as f:
    f.writelines(final)

# === Report ===
with open(ind_path, "r", encoding="utf-8") as f:
    result = f.read()
has_empty = bs + "lettergroup{}" in result

# Count duplicates
from collections import Counter
count_entries = []
for line in final:
    s = line.strip()
    if s.startswith(bs + "item ") and not s.startswith(bs + "subitem "):
        text = s[6:]
        while bs + "hyperpage{" in text:
            hp = text.find(bs + "hyperpage{"); he = text.find("}", hp)
            if he > hp: text = text[:hp] + text[he + 1 :]
        count_entries.append(text.strip().rstrip(",").lower())

dupes = {k: v for k, v in Counter(count_entries).items() if v > 1}

print(f"Empty group: {has_empty}")
print(f"Main entries: {len(count_entries)}")
print(f"Duplicates: {len(dupes)}")
print(f"Lines: {len(lines)} -> {len(final)}")
