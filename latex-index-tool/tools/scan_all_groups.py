"""Comprehensive OCR vs .ind comparison for all letter groups."""
from pathlib import Path
import re
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

ROOT = Path(__file__).parent.parent.parent
bs = chr(92)

ind = (ROOT / 'Topology_by_Munkres.ind').read_text(encoding='utf-8')
ocr_text = (ROOT / 'original' / 'temp' / 'index.tex').read_text(encoding='utf-8')

# ── Parse OCR into {letter: [(l1, [l2s])]} ──
# OCR: entries are flush-left. L2s follow their L1, separated by blank lines
# L1 entries typically have page numbers, L2s are continuations
ocr_groups = {}
current_letter = None
current_l1 = None
current_subs = []

lines = ocr_text.splitlines()
i = 0
while i < len(lines):
    line = lines[i]
    stripped = line.strip()

    # Letter heading
    if re.match(r'^[A-Z]$', stripped):
        if current_l1 is not None and current_letter is not None:
            ocr_groups.setdefault(current_letter, []).append((current_l1, current_subs))
        current_letter = stripped
        current_l1 = None
        current_subs = []
        i += 1
        continue

    # Symbol heading
    if re.match(r'^\\mathbb\{R\}$', stripped):
        if current_l1 is not None and current_letter is not None:
            ocr_groups.setdefault(current_letter, []).append((current_l1, current_subs))
        current_letter = 'R'
        current_l1 = None
        current_subs = []
        i += 1
        continue

    if not stripped:
        i += 1
        continue

    # Heuristic: entries with page numbers are L1, entries without are L2
    has_pages = bool(re.search(r',?\s*\d{1,4}(?:\s*,\s*\d{1,4})*$', stripped))
    has_see = '(see' in stripped or '(cont.)' in stripped

    if line[0] in (' ', '\t'):
        # Indented = L2
        if current_l1 is not None:
            current_subs.append(stripped)
    elif has_pages or has_see or stripped.endswith(':'):
        # L1 (has page numbers, cross-ref, or colon)
        if current_l1 is not None and current_letter is not None:
            ocr_groups.setdefault(current_letter, []).append((current_l1, current_subs))
        current_l1 = stripped
        current_subs = []
    else:
        # No page numbers, probably L2
        if current_l1 is not None:
            current_subs.append(stripped)

    i += 1

if current_l1 is not None and current_letter is not None:
    ocr_groups.setdefault(current_letter, []).append((current_l1, current_subs))

# ── Parse .ind into {letter: [(l1, [l2s])]} ──
ind_groups = {}
current_letter = None
current_l1 = None
current_subs = []

ind_lines = ind.splitlines()
for line in ind_lines:
    stripped = line.strip()
    if not stripped:
        continue

    m = re.search(re.escape(bs + 'lettergroup') + r'\{(\w+)\}', stripped)
    if m:
        if current_l1 is not None and current_letter is not None:
            ind_groups.setdefault(current_letter, []).append((current_l1, current_subs))
        current_letter = m.group(1)
        current_l1 = None
        current_subs = []
        continue

    if stripped.startswith(bs + 'item ') and not stripped.startswith(bs + 'subitem '):
        if current_l1 is not None and current_letter is not None:
            ind_groups.setdefault(current_letter, []).append((current_l1, current_subs))
        l1 = stripped[len(bs + 'item '):]
        hp = l1.find(bs + 'hyperpage')
        if hp >= 0: l1 = l1[:hp].strip().rstrip(',')
        current_l1 = l1
        current_subs = []
        continue

    if stripped.startswith(bs + 'subitem '):
        sub = stripped[len(bs + 'subitem '):]
        hp = sub.find(bs + 'hyperpage')
        if hp >= 0: sub = sub[:hp].strip().rstrip(',')
        current_subs.append(sub)

if current_l1 is not None and current_letter is not None:
    ind_groups.setdefault(current_letter, []).append((current_l1, current_subs))

# ── Normalize ──
def norm(s):
    s = s.lower()
    s = re.sub(r'[{}$^_\\]', '', s)
    s = re.sub(r'\s+', ' ', s).strip().rstrip(',.')
    return s

# ── Compare each letter ──
DONE = set('ABJKUVWXZ')  # Already verified letter groups

for letter in sorted(set(list(ocr_groups.keys()) + list(ind_groups.keys())) - DONE):
    ocr_entries = ocr_groups.get(letter, [])
    ind_entries = ind_groups.get(letter, [])

    if not ocr_entries:
        continue

    ocr_map = {}
    for l1, subs in ocr_entries:
        k = norm(l1)
        if k and len(k) >= 2:
            ocr_map[k] = (l1, [norm(s) for s in subs])

    ind_map = {}
    for l1, subs in ind_entries:
        k = norm(l1)
        if k and len(k) >= 2:
            ind_map[k] = (l1, [norm(s) for s in subs])

    ocr_keys = set(ocr_map.keys())
    ind_keys = set(ind_map.keys())

    missing_l1 = ocr_keys - ind_keys
    extra_l1 = ind_keys - ocr_keys

    # Skip cross-refs
    def is_crossref(name):
        return '(see' in name.lower() or name.strip().endswith(':') and not any(
            c.isalpha() for c in name.split(':')[1].strip() if c != ' '
        )

    real_missing = [k for k in missing_l1 if not is_crossref(ocr_map[k][0])]

    if real_missing or extra_l1:
        print(f'\n{"="*60}')
        print(f'  {letter}: OCR={len(ocr_entries)} L1, IND={len(ind_entries)} L1')
        print(f'  Missing L1: {len(real_missing)}, Extra L1: {len(extra_l1)}')
        print(f'{"="*60}')

        if real_missing:
            print(f'  --- MISSING L1 ---')
            for k in sorted(real_missing)[:15]:
                l1, subs = ocr_map[k]
                print(f'  - {l1[:100]}')
                for s in subs[:3]:
                    print(f'      L2: {s[:100]}')
                if len(subs) > 3:
                    print(f'      ... +{len(subs)-3} more')
            if len(real_missing) > 15:
                print(f'  ... and {len(real_missing)-15} more')

        if extra_l1:
            print(f'  --- EXTRA L1 ---')
            for k in sorted(extra_l1)[:10]:
                l1, _ = ind_map[k]
                print(f'  + {l1[:100]}')

    # L2 comparison for common L1s
    common = ocr_keys & ind_keys
    l2_issues = []
    for k in common:
        ocr_l1, ocr_subs = ocr_map[k]
        ind_l1, ind_subs = ind_map[k]
        ocr_set = set(ocr_subs)
        ind_set = set(ind_subs)
        m = ocr_set - ind_set
        if m:
            l2_issues.append((ocr_l1, sorted(m), 'missing'))

    if l2_issues:
        total_missing = sum(len(m) for _, m, _ in l2_issues)
        if total_missing > 3 or letter in 'DEFGHI':
            print(f'  --- MISSING L2 ({total_missing} total) ---')
            for l1_name, subs, _ in l2_issues[:10]:
                print(f'  [{l1_name[:60]}]')
                for s in subs[:5]:
                    print(f'    - {s[:100]}')
            if len(l2_issues) > 10:
                print(f'  ... and {len(l2_issues)-10} more entries with missing L2s')

print(f'\n{"="*60}')
print('Scan complete.')
