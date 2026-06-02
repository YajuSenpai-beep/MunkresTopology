"""Post-process .ind to fix B^n subitems misattached to B^2 by makeindex.

makeindex mis-sorts entries with ^ in the sort key, placing B^n L2 subitems
under B^2 instead of B^n. This script moves them to the correct parent.

Run AFTER _fix_ind.py.
"""
import os

bs = chr(92)
ind_path = os.path.join(os.path.dirname(__file__), "..", "Topology_by_Munkres.ind")

with open(ind_path, "r", encoding="utf-8") as f:
    lines = f.readlines()

# Find B^n L1 entry and B^2 L1 entry in the B section
bn_idx = None
b2_idx = None
in_b_section = False

for i, line in enumerate(lines):
    s = line.strip()
    if bs + "lettergroup{B}" in s:
        in_b_section = True
        continue
    if in_b_section and s.startswith(bs + "lettergroup{"):
        in_b_section = False
        continue
    if not in_b_section:
        continue
    if s.startswith(bs + "item "):
        if "{B}^{n}" in s:
            bn_idx = i
        elif "{B}^{2}" in s:
            b2_idx = i

if bn_idx is None or b2_idx is None:
    # No fix needed
    print(f"B^n: {bn_idx}, B^2: {b2_idx} — no B^n fix needed")
    exit(0)

# Collect subitems under B^2
b2_subs = []
j = b2_idx + 1
while j < len(lines):
    sj = lines[j].strip()
    if sj.startswith(bs + "item ") or sj.startswith(bs + "lettergroup{"):
        break
    if sj.startswith(bs + "subitem "):
        sub_text = sj[len(bs + "subitem "):].lower()
        if "compactness" in sub_text or "fundamental group" in sub_text or "path connectedness" in sub_text:
            b2_subs.append((j, lines[j]))
    j += 1

if not b2_subs:
    print("No B^n subitems found under B^2")
    exit(0)

# Remove from B^2 (bottom-up to preserve indices)
for j, _ in reversed(b2_subs):
    del lines[j]

# Insert after B^n (after any existing subitems)
insert_at = bn_idx + 1
while insert_at < len(lines):
    sj = lines[insert_at].strip()
    if sj.startswith(bs + "subitem "):
        insert_at += 1
    else:
        break

for _, sub_line in reversed(b2_subs):
    lines.insert(insert_at, sub_line)

with open(ind_path, "w", encoding="utf-8") as f:
    f.writelines(lines)

print(f"Moved {len(b2_subs)} B^n subitems from B^2 to B^n")
