"""Full C section comparison: OCR vs .ind, L1 and L2."""
from pathlib import Path
import re
from collections import defaultdict

ROOT = Path(__file__).parent.parent.parent
bs = chr(92)

ind = (ROOT / 'Topology_by_Munkres.ind').read_text(encoding='utf-8')
ocr_text = (ROOT / 'original' / 'temp' / 'index.tex').read_text(encoding='utf-8')

# ── Parse OCR C section ──
# Extract from "\nC\n" to "\nD\n"
c_start = ocr_text.find('\nC\n')
d_start = ocr_text.find('\nD\n', c_start + 2)
ocr_c = ocr_text[c_start:d_start]

# Parse: flush-left = L1, indented = L2
ocr_lines = ocr_c.splitlines()
ocr_entries = []  # [(l1_raw, [l2_raw...])]
current_l1 = None
current_subs = []

for line in ocr_lines:
    stripped = line.strip()
    if not stripped:
        # Blank line = separator between entries
        continue
    if re.match(r'^[A-Z]$', stripped):
        continue  # skip the C header

    if line[0] in (' ', '\t'):
        # Indented = L2
        if current_l1 is not None:
            current_subs.append(stripped)
    else:
        # Flush left = new L1
        if current_l1 is not None:
            ocr_entries.append((current_l1, current_subs))
        current_l1 = stripped
        current_subs = []

if current_l1 is not None:
    ocr_entries.append((current_l1, current_subs))

# ── Parse .ind C section ──
c_start_ind = ind.find(bs + 'lettergroup{C}')
d_start_ind = ind.find(bs + 'lettergroup{D}')
ind_c = ind[c_start_ind:d_start_ind] if d_start_ind > c_start_ind else ind[c_start_ind:]

ind_lines = ind_c.splitlines()
ind_entries = []
current_l1 = None
current_subs = []

for line in ind_lines:
    stripped = line.strip()
    if not stripped:
        continue
    if stripped.startswith(bs + 'item ') and not stripped.startswith(bs + 'subitem '):
        if current_l1 is not None:
            ind_entries.append((current_l1, current_subs))
        current_l1 = stripped[len(bs + 'item '):]
        # Strip hyperpage
        hp = current_l1.find(bs + 'hyperpage')
        if hp >= 0:
            current_l1 = current_l1[:hp].strip().rstrip(',')
        current_subs = []
    elif stripped.startswith(bs + 'subitem '):
        sub = stripped[len(bs + 'subitem '):]
        hp = sub.find(bs + 'hyperpage')
        if hp >= 0:
            sub = sub[:hp].strip().rstrip(',')
        current_subs.append(sub)
if current_l1 is not None:
    ind_entries.append((current_l1, current_subs))

# ── Normalize ──
def norm(s):
    s = s.lower().strip()
    s = re.sub(r'[{}$^_\\]', '', s)
    s = re.sub(r'\s+', ' ', s).strip().rstrip(',.')
    return s

# ── Compare L1 ──
ocr_l1_map = {}
for l1, subs in ocr_entries:
    key = norm(l1)
    if len(key) >= 2:
        ocr_l1_map[key] = (l1, [norm(s) for s in subs])

ind_l1_map = {}
for l1, subs in ind_entries:
    key = norm(l1)
    if len(key) >= 2:
        ind_l1_map[key] = (l1, [norm(s) for s in subs])

# Cross-references to ignore
crossrefs = {'choice axiom (see axiom of choice)', 'circle, unit (see s1)',
             'compact, 164 (see also compact hausdorff space, compactness)',
             'connected space, 148 (see also connectedness)',
             'complete metric space, 264 (see also completeness)',
             'completely regular space, 211 (see also complete regularity)'}

ocr_keys = set(ocr_l1_map.keys())
ind_keys = set(ind_l1_map.keys())

missing_l1 = [k for k in sorted(ocr_keys - ind_keys) if norm(ocr_l1_map[k][0]) not in crossrefs]
extra_l1 = sorted(ind_keys - ocr_keys)

print(f'OCR C L1: {len(ocr_l1_map)}, .ind C L1: {len(ind_l1_map)}')
print(f'Missing L1: {len(missing_l1)}, Extra L1: {len(extra_l1)}')

if missing_l1:
    print('\n=== MISSING L1 (OCR has, .ind lacks) ===')
    for k in missing_l1[:30]:
        l1, subs = ocr_l1_map[k]
        display = l1[:100]
        print(f'  - {display}')
        for s in subs[:3]:
            print(f'      L2: {s[:100]}')
        if len(subs) > 3:
            print(f'      ... +{len(subs)-3} more L2')

if extra_l1:
    print(f'\n=== EXTRA L1 (.ind has, OCR lacks) ===')
    for k in extra_l1[:15]:
        l1, subs = ind_l1_map[k]
        print(f'  + {l1[:100]}')

# ── Compare L2 for common L1s ──
common = ocr_keys & ind_keys
missing_l2_count = 0
extra_l2_count = 0
l2_report = []

for k in sorted(common):
    ocr_l1, ocr_subs = ocr_l1_map[k]
    ind_l1, ind_subs = ind_l1_map[k]
    ocr_set = set(ocr_subs)
    ind_set = set(ind_subs)
    m = ocr_set - ind_set
    e = ind_set - ocr_set
    if m or e:
        if m:
            missing_l2_count += len(m)
        if e:
            extra_l2_count += len(e)
        l2_report.append((ocr_l1, sorted(m), sorted(e)))

print(f'\n=== L2 DIFFERENCES ({len(l2_report)} L1s affected) ===')
print(f'Missing L2: {missing_l2_count}, Extra L2: {extra_l2_count}')
for l1, m, e in l2_report[:40]:
    print(f'\n  [{l1[:60]}]')
    for s in m[:8]:
        print(f'    OCR has, .ind MISS: {s[:100]}')
    if len(m) > 8:
        print(f'    ... +{len(m)-8} more missing')
    for s in e[:5]:
        print(f'    .ind has, OCR MISS: {s[:100]}')
    if len(e) > 5:
        print(f'    ... +{len(e)-5} more extra')

print(f'\nTotal: {len(missing_l1)} missing L1, {missing_l2_count} missing L2, {extra_l2_count} extra L2')
