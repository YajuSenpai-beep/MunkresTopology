"""Find all duplicate entries in the compiled .ind file."""
from pathlib import Path
import re
from collections import defaultdict

ROOT = Path(__file__).parent.parent.parent
bs = chr(92)

ind = (ROOT / 'Topology_by_Munkres.ind').read_text(encoding='utf-8')

# Parse all \item entries (L1)
lines = ind.splitlines()
entries = []
current_l1 = None
current_subs = []

for line in lines:
    stripped = line.strip()
    if not stripped:
        continue

    item_prefix = bs + 'item '
    sub_prefix = bs + 'subitem '

    if stripped.startswith(item_prefix):
        if current_l1 is not None:
            entries.append((current_l1, current_subs))
        current_l1 = stripped[len(item_prefix):].strip()
        # Strip hyperpage
        hp = current_l1.find(bs + 'hyperpage')
        if hp >= 0:
            current_l1 = current_l1[:hp].strip().rstrip(',')
        current_subs = []
    elif stripped.startswith(sub_prefix):
        sub = stripped[len(sub_prefix):].strip()
        hp = sub.find(bs + 'hyperpage')
        if hp >= 0:
            sub = sub[:hp].strip().rstrip(',')
        current_subs.append(sub)

if current_l1 is not None:
    entries.append((current_l1, current_subs))

# Normalize entries for comparison
def clean(text):
    """Normalize LaTeX for comparison."""
    t = text.strip()
    # Remove math mode delimiters
    t = t.replace('$', '')
    # Normalize math delimiters \(...\) to same as $...$
    t = t.replace(chr(92) + '(', '').replace(chr(92) + ')', '')
    # Collapse whitespace
    t = re.sub(r'\s+', ' ', t).strip()
    return t.lower()

# Group by cleaned L1 text
groups = defaultdict(list)
for l1, subs in entries:
    key = clean(l1)
    groups[key].append((l1, subs))

print(f'Total L1 entries: {len(entries)}')
print(f'Unique normalized L1 keys: {len(groups)}')

# Find duplicates
dupes = {k: v for k, v in groups.items() if len(v) > 1}
print(f'Duplicate groups: {len(dupes)}')

for key, group in sorted(dupes.items()):
    print(f'\n--- {len(group)}x: "{group[0][0][:60]}" ---')
    for i, (l1, subs) in enumerate(group):
        print(f'  Copy {i+1}: "{l1[:80]}"')
        if subs:
            for s in subs[:3]:
                print(f'    L2: {s[:80]}')
            if len(subs) > 3:
                print(f'    ... +{len(subs)-3} more L2')
