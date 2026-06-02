"""Post-process .ind to fix miscategorized subitems from makeindex sorting glitches.

Currently handles: U(A,epsilon) subitems → Uncountability; Uniform limit thm → Uniform metric
"""
import os
import re

bs = chr(92)
ind_path = os.path.join(os.path.dirname(__file__), "..", "Topology_by_Munkres.ind")

with open(ind_path, "r", encoding="utf-8") as f:
    lines = f.readlines()

# Hard-merge duplicate L1s: move subitems from wrong to target L1
L1_MERGES = []

# Fix "L1: YYY" entries -> split into L1 "L1:" with L2 "YYY"
L1_SPLITS = [
    ("Uncountability: of " + bs + "(\\mathcal{P}({\\mathbb{Z}}_{ + })" + bs + ")", "Uncountability:"),
]

# Fix \left/\right duplicate L1 entries
# Rule: find \left entry that follows its non-\left counterpart, merge them
i = 0
left_fixed = 0
while i < len(lines):
    s = lines[i].strip()
    if s.startswith(bs + "item ") and bs + "left" in s:
        # Get the core text (strip \item, \left, \right, \(, \), and \hyperpage)
        name = s[len(bs + "item "):]
        hp = name.find(bs + "hyperpage");
        if hp >= 0: name = name[:hp]
        core = name.strip().rstrip(",")
        core = core.replace(bs + "left", "").replace(bs + "right", " ")
        core = core.replace(bs + "(", "").replace(bs + ")", "")
        core = re.sub(r'\s+', ' ', core).strip()
        # Check the preceding L1 entry — if it has the same core text (after similar stripping), merge
        prev_l1 = i - 1
        while prev_l1 >= 0:
            ps = lines[prev_l1].strip()
            if ps.startswith(bs + "item ") and not ps.startswith(bs + "subitem "):
                pname = ps[len(bs + "item "):]
                hp2 = pname.find(bs + "hyperpage")
                if hp2 >= 0: pname = pname[:hp2]
                pcore = pname.strip().rstrip(",")
                pcore = pcore.replace(bs + "(", "").replace(bs + ")", "")
                pcore = re.sub(r'\s+', ' ', pcore).strip()
                # Simple heuristic: if core starts with pcore, they're related
                if core.startswith(pcore) and len(pcore) >= 4:
                    # Merge: move subitems from i to prev_l1
                    subs = []
                    k = i + 1
                    while k < len(lines):
                        sk = lines[k].strip()
                        if sk.startswith(bs + "item ") or sk.startswith(bs + "lettergroup{"):
                            break
                        if sk.startswith(bs + "subitem "):
                            subs.append(lines.pop(k))
                            continue
                        k += 1
                    lines.pop(i)
                    insert_at = prev_l1 + 1
                    while insert_at < len(lines) and lines[insert_at].strip().startswith(bs + "subitem "):
                        insert_at += 1
                    for sl in reversed(subs):
                        lines.insert(insert_at, sl)
                    left_fixed += 1
                    i -= 1  # re-check this index
                break
            prev_l1 -= 1
    i += 1

if left_fixed:
    print(f"Fixed \\left/\\right duplicates: {left_fixed} entries")

# Process L1 splits: rename "XXX: YYY" -> "XXX" (L2 already present)
for full_frag, base_name in L1_SPLITS:
    for i, line in enumerate(lines):
        s = line.strip()
        if s.startswith(bs + "item ") and full_frag in s:
            old_text = s[len(bs + "item "):]
            hp = old_text.find(bs + "hyperpage")
            pages = old_text[hp:] if hp >= 0 else ""
            lines[i] = bs + "item " + base_name + (" " + pages if pages else "") + "\n"
            break

l1_merged = 0
for wrong_frag, target_frag in L1_MERGES:
    wrong_idx = target_idx = None
    for i, line in enumerate(lines):
        s = line.strip()
        if s.startswith(bs + "item ") and target_frag in s:
            target_idx = i
        if s.startswith(bs + "item ") and wrong_frag in s:
            wrong_idx = i
    if wrong_idx is not None and target_idx is not None and wrong_idx != target_idx:
        # Move subitems from wrong to target (bottom-up pop preserves indices above)
        sub_lines = []
        j = wrong_idx + 1
        while j < len(lines):
            sj = lines[j].strip()
            if sj.startswith(bs + "item ") or sj.startswith(bs + "lettergroup{"):
                break
            if sj.startswith(bs + "subitem "):
                sub_lines.append(lines.pop(j))
                continue
            j += 1
        # Remove the wrong L1 itself
        lines.pop(wrong_idx)
        # Insert subitems after target's last subitem
        if sub_lines:
            insert_at = target_idx + 1
            if target_idx > wrong_idx:
                insert_at -= 1  # adjust for removed wrong L1
            while insert_at < len(lines) and lines[insert_at].strip().startswith(bs + "subitem "):
                insert_at += 1
            for sl in reversed(sub_lines):
                lines.insert(insert_at, sl)
        l1_merged += 1

# Hardcoded fixes: (wrong_parent_text, sub_fragment, target_parent_text)
FIXES = [
    # U(A,epsilon) -> Uncountability
    ("U( {A,\\epsilon }", "0,1", "Uncountability"),
    ("U( {A,\\epsilon }", "mathbb", "Uncountability"),
    ("U( {A,\\epsilon }", "transcendental", "Uncountability"),
    # Uniform limit theorem completeness -> Uniform metric
    ("Uniform limit theorem", "completeness", "Uniform metric"),
    ("Uniform limit theorem", "vs. sup metric", "Uniform metric"),
]

total_fixed = 0

for wrong_parent_frag, sub_frag, target_frag in FIXES:
    # Find all matching instances
    wrong_parent_idx = None
    target_idx = None

    # Find wrong parent
    for i, line in enumerate(lines):
        s = line.strip()
        if s.startswith(bs + "item ") and wrong_parent_frag in s:
            wrong_parent_idx = i
            break

    # Find target parent
    for i, line in enumerate(lines):
        s = line.strip()
        if s.startswith(bs + "item ") and target_frag in s:
            target_idx = i
            break

    if wrong_parent_idx is None or target_idx is None:
        continue

    # Find matching subitem under wrong parent
    j = wrong_parent_idx + 1
    while j < len(lines):
        sj = lines[j].strip()
        if sj.startswith(bs + "item ") or sj.startswith(bs + "lettergroup{"):
            break
        if sj.startswith(bs + "subitem ") and sub_frag in sj:
            # Found! Move this subitem
            sub_line = lines.pop(j)
            # Adjust target_idx if we removed a line before it
            if j < target_idx:
                target_idx -= 1
            # Find insertion point: after all existing subitems of target
            insert_at = target_idx + 1
            while insert_at < len(lines) and lines[insert_at].strip().startswith(bs + "subitem "):
                insert_at += 1
            lines.insert(insert_at, sub_line)
            total_fixed += 1
            # Adjust wrong_parent_idx if we removed a line before it
            if j < wrong_parent_idx:
                wrong_parent_idx -= 1
            # Don't increment j since we popped a line
            continue
        j += 1

# Deduplicate L2 subitems under the same parent
sub_removed = 0
i = 0
while i < len(lines):
    s = lines[i].strip()
    if s.startswith(bs + "item ") and not s.startswith(bs + "subitem "):
        seen = {}
        j = i + 1
        while j < len(lines):
            sj = lines[j].strip()
            if sj.startswith(bs + "item ") or sj.startswith(bs + "lettergroup{"):
                break
            if sj.startswith(bs + "subitem "):
                sub_text = sj[len(bs + "subitem "):]
                sub_clean = sub_text.strip().lower()
                sub_clean = sub_clean.replace(bs + "(", "").replace(bs + ")", "").replace("$", "")
                sub_clean = sub_clean.replace(bs + "mathbb{r}", "r").replace(bs + "mathbb{R}", "r")
                while bs + "hyperpage{" in sub_clean:
                    hp = sub_clean.find(bs + "hyperpage{"); he = sub_clean.find("}", hp)
                    if he > hp: sub_clean = sub_clean[:hp] + sub_clean[he+1:]
                sub_clean = sub_clean.strip().rstrip(", ")
                if sub_clean in seen:
                    lines.pop(j)
                    sub_removed += 1
                    continue
                else:
                    seen[sub_clean] = True
            j += 1
        i = j
    else:
        i += 1

if total_fixed or sub_removed or l1_merged:
    with open(ind_path, "w", encoding="utf-8") as f:
        f.writelines(lines)
    msg = f"Fixed miscategorized: {total_fixed} subitems"
    if l1_merged:
        msg += f", merged {l1_merged} L1 duplicates"
    if sub_removed:
        msg += f", merged {sub_removed} L2 duplicates"
    print(msg)
else:
    print("No miscategorized subitems found")
