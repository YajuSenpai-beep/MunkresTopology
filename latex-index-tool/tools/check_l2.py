"""Check which L2 entries from l2_missing_in_pdf.txt are still missing."""
import re
from pathlib import Path

ROOT = Path(__file__).parent.parent.parent
bs = chr(92)

ind = (ROOT / 'Topology_by_Munkres.ind').read_text(encoding='utf-8')

# Parse \item + \subitem structure using string methods (avoid regex issues)
lines = ind.splitlines()
l2_map = {}
current_parent = None
for line in lines:
    line = line.strip()
    if not line:
        continue
    item_prefix = bs + 'item '
    sub_prefix = bs + 'subitem '
    hp_pattern = bs + 'hyperpage'

    if line.startswith(item_prefix):
        current_parent = line[len(item_prefix):].strip()
        # Remove \hyperpage{...} using simple string ops
        idx = current_parent.find(hp_pattern)
        while idx >= 0:
            end = current_parent.find('}', idx)
            if end >= 0:
                current_parent = current_parent[:idx] + current_parent[end+1:]
            idx = current_parent.find(hp_pattern)
        current_parent = re.sub(r',?\s+', ' ', current_parent).strip().rstrip(',')
        l2_map[current_parent] = []
    elif line.startswith(sub_prefix):
        sub = line[len(sub_prefix):].strip()
        idx = sub.find(hp_pattern)
        while idx >= 0:
            end = sub.find('}', idx)
            if end >= 0:
                sub = sub[:idx] + sub[end+1:]
            idx = sub.find(hp_pattern)
        sub = re.sub(r',?\s+', ' ', sub).strip().rstrip(',')
        if current_parent:
            l2_map[current_parent].append(sub)

entries = [
    ('Compactness', 'in C(X, R^n)'),
    ('Connectedness', 'of R^omega'),
    ('Continuity: of algebraic operations in R', 'of min{f,g}'),
    ('Countable dense subset', 'in R^J'),
    ('Countable dense subset', 'in R_ell'),
    ('Countability', 'of Z'),
    ('Covering space', 'of R^2 - 0'),
    ('Covering space', 'of S^1'),
    ('Fixed point theorem: for B^n', 'for [0,1]'),
    ('Free abelian group', 'rank'),
    ('Fundamental group', 'of S^1'),
    ('Fundamental group', 'of S^n'),
    ('Metrizability: of compact Hausdorff space', 'of R^J'),
    ('Normality', 'of R_ell'),
    ('Normality', 'of R^J'),
    ('Paracompactness', 'of R^J'),
    ('Paracompactness', 'of R^omega'),
    ('Paracompactness', 'of S_Omega'),
    ('Path connectedness', 'of B^n'),
    ('Path connectedness', 'of S^n'),
    ('Second-countability', 'of C(I,R)'),
    ('Second-countability', 'of R_ell'),
    ('Simply connected', 'S^n'),
    ('Simply connected', 'tree'),
    ('Standard topology: on R', 'on R^2'),
    ('Stone-Cech compactification', 'of S_Omega'),
    ('Uncountability: of P(Z+)', 'of R'),
    ('Uncountability: of P(Z+)', 'of {0,1}^omega'),
    ('Well-ordered set', 'Z+'),
    ('Well-ordered set', 'Z+ x Z+'),
]

def norm(s):
    s = s.lower()
    s = re.sub(r'[{}$^_\\]', '', s)
    s = s.replace('{', '').replace('}', '')
    s = re.sub(r'\s+', ' ', s).strip()
    return s

print('=== L2 entries status ===')
missing = []
found = []
for parent, child in entries:
    n_parent = norm(parent)
    n_child = norm(child)
    ok = False
    for p, subs in l2_map.items():
        if n_parent in norm(p):
            for s in subs:
                if n_child in norm(s):
                    ok = True
                    break
            if ok:
                break
    if ok:
        found.append((parent, child))
        print(f'  OK: {parent} -> {child}')
    else:
        missing.append((parent, child))
        print(f'  MISS: {parent} -> {child}')

print(f'\nFound: {len(found)}, Missing: {len(missing)}')
if missing:
    print('\n== STILL MISSING ==')
    for p, c in missing:
        print(f'  {p} -> {c}')
