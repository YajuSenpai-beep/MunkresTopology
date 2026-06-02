"""Compare C section of OCR vs .ind — thorough entry-by-entry comparison."""
import re
from pathlib import Path

ROOT = Path(__file__).parent.parent.parent
bs = chr(92)

ind = (ROOT / 'Topology_by_Munkres.ind').read_text(encoding='utf-8')
ocr_text = (ROOT / 'original' / 'temp' / 'index.tex').read_text(encoding='utf-8')

# Extract C section from .ind
c_start = ind.find(bs + 'lettergroup{C}')
d_start = ind.find(bs + 'lettergroup{D}')
ind_c = ind[c_start:d_start] if d_start > c_start else ind[c_start:]

# Extract C section from OCR
c_start_ocr = ocr_text.find('\nC\n')
d_start_ocr = ocr_text.find('\nD\n', c_start_ocr + 1)
ocr_c = ocr_text[c_start_ocr:d_start_ocr] if d_start_ocr > c_start_ocr else ocr_text[c_start_ocr:]

# Parse OCR C entries: L1 flush-left, L2 indented
ocr_lines = ocr_c.splitlines()
ocr_entries = []  # [(l1, [l2s])]
current_l1 = None
current_subs = []

for line in ocr_lines:
    stripped = line.strip()
    if not stripped or re.match(r'^[A-Z]$', stripped):
        if current_l1 is not None:
            ocr_entries.append((current_l1, current_subs))
        if re.match(r'^[A-Z]$', stripped) and stripped != 'C':
            break
        current_l1 = None
        current_subs = []
        continue

    if line.startswith(' ') or line.startswith('\t'):
        if current_l1 is not None:
            current_subs.append(stripped)
    else:
        if current_l1 is not None:
            ocr_entries.append((current_l1, current_subs))
        current_l1 = stripped
        current_subs = []

if current_l1 is not None:
    ocr_entries.append((current_l1, current_subs))

# Parse .ind C entries
ind_lines = ind_c.splitlines()
ind_entries = []
current_l1 = None
current_subs = []

for line in ind_lines:
    stripped = line.strip()
    if not stripped:
        continue
    if bs + 'item ' in stripped[:10]:
        if current_l1 is not None:
            ind_entries.append((current_l1, current_subs))
        current_l1 = stripped[stripped.find(bs+'item ')+len(bs+'item '):].strip()
        # Strip hyperpage
        idx_hp = current_l1.find(bs + 'hyperpage')
        if idx_hp >= 0:
            current_l1 = current_l1[:idx_hp].strip().rstrip(',')
        current_subs = []
    elif bs + 'subitem ' in stripped[:15]:
        sub = stripped[stripped.find(bs+'subitem ')+len(bs+'subitem '):].strip()
        idx_hp = sub.find(bs + 'hyperpage')
        if idx_hp >= 0:
            sub = sub[:idx_hp].strip().rstrip(',')
        current_subs.append(sub)

if current_l1 is not None:
    ind_entries.append((current_l1, current_subs))

def norm(s):
    s = s.lower()
    s = re.sub(r'[{}$^_\\]', '', s)
    s = re.sub(r'[{}]', '', s)
    s = re.sub(r'\s+', ' ', s).strip().rstrip(',.')
    return s

# Build OCR normalized map
ocr_map = {}
for l1, subs in ocr_entries:
    k = norm(l1)
    if len(k) >= 2:
        ocr_map[k] = (l1, [norm(s) for s in subs])

# Build .ind normalized map
ind_map = {}
for l1, subs in ind_entries:
    k = norm(l1)
    if len(k) >= 2:
        ind_map[k] = (l1, [norm(s) for s in subs])

# Compare
ocr_keys = set(ocr_map.keys())
ind_keys = set(ind_map.keys())

missing_l1 = ocr_keys - ind_keys
extra_l1 = ind_keys - ocr_keys
common = ocr_keys & ind_keys

print(f'OCR C entries: {len(ocr_entries)} L1')
print(f'.ind C entries: {len(ind_entries)} L1')
print(f'Missing L1: {len(missing_l1)}')
print(f'Extra L1: {len(extra_l1)}')

# Report missing L1
if missing_l1:
    print(f'\n=== MISSING L1 ({len(missing_l1)}) ===')
    for k in sorted(missing_l1):
        l1, subs = ocr_map[k]
        print(f'  - {l1[:100]}')
        for s in subs[:3]:
            print(f'      L2: {s[:100]}')
        if len(subs) > 3:
            print(f'      ... +{len(subs)-3} more L2')

# Report extra L1
if extra_l1:
    print(f'\n=== EXTRA L1 ({len(extra_l1)}) ===')
    for k in sorted(extra_l1):
        l1, subs = ind_map[k]
        print(f'  + {l1[:100]}')

# Compare L2 for common entries
missing_l2_count = 0
print(f'\n=== MISSING L2 (from common L1s) ===')
for k in sorted(common):
    ocr_l1, ocr_subs = ocr_map[k]
    ind_l1, ind_subs = ind_map[k]
    ocr_sub_set = set(ocr_subs)
    ind_sub_set = set(ind_subs)
    missing = ocr_sub_set - ind_sub_set
    if missing:
        missing_l2_count += len(missing)
        print(f'  [{ocr_l1[:60]}]')
        for s in sorted(missing)[:5]:
            print(f'    MISS: {s[:100]}')
        if len(missing) > 5:
            print(f'    ... +{len(missing)-5} more')

print(f'\nTotal missing L2: {missing_l2_count}')

# Check for duplicates
ind_l1_norm = [norm(l1) for l1, _ in ind_entries]
from collections import Counter
dupes = {k: v for k, v in Counter(ind_l1_norm).items() if v > 1}
if dupes:
    print(f'\n=== DUPLICATES ===')
    for k, v in dupes.items():
        print(f'  {k[:80]}: {v} times')
