"""Check which l1-manual-review entries are still missing from .ind."""
import re
from pathlib import Path

ROOT = Path(__file__).parent.parent.parent
bs = chr(92)

ind_text = (ROOT / 'Topology_by_Munkres.ind').read_text(encoding='utf-8')

# Extract all \item and \subitem entries
items = re.findall(re.escape(chr(92) + 'item') + r'\s+(.+)', ind_text)
subitems = re.findall(re.escape(chr(92) + 'subitem') + r'\s+(.+)', ind_text)

l1_terms = [
    'Counterimage', 'Inf A', 'Infimum', 'm-tuple', 'omega-tuple',
    'Ball, unit', 'Bd A', 'epsilon-ball', 'First-countability',
    'Hilbert cube', 'Int A', 'ell-2 topology', 'T1 axiom', 'Tower',
    'Bicompactness', 'Coset', 'epsilon-neighborhood of a set',
    'Left coset', 'Perfect map', 'R^n - 0', 'S^n (unit sphere)',
    'Cofinal', 'Curve', 'Directed set', 'G_delta set',
    'Line with two origins', 'Net', 'Second-countability', 'Subnet',
    'T_i axioms', '2-manifold', 'F_sigma set', 'Functor',
    'sigma-locally discrete', 'sigma-locally finite',
    'Stone-Cech compactification', 'sigma-compact',
    'Cube in R^n', 'k-plane', 'widehat alpha', '[f]',
    'k-fold covering', 'Star-convex set', 'Clockwise loop',
    '2-cell', 'CW complex', 'm-fold projective plane',
    'n-fold torus', 'Normalizer', '2-manifold with boundary', 'Cone',
    'Zermelo', 'Sup A', 'Supremum', 'R^n', 'S_bar_Omega',
]

def norm(s: str) -> str:
    s = s.lower()
    s = re.sub(bs + r'[a-zA-Z]+', '', s)
    s = re.sub(r'[{}$^_]', '', s)
    s = re.sub(r'\s+', ' ', s).strip()
    return s

ind_items_norm = [norm(i) for i in items]
ind_subs_norm = [norm(i) for i in subitems]

print('=== L1 entries status ===')
missing_terms = []
found_terms = []
for term in l1_terms:
    n = norm(term)
    found_l1 = any(n in i for i in ind_items_norm)
    found_l2 = any(n in i for i in ind_subs_norm)
    if found_l1:
        status = 'L1 OK'
        found_terms.append(term)
    elif found_l2:
        status = 'L2 OK'
        found_terms.append(term)
    else:
        status = 'MISSING'
        missing_terms.append(term)
    print(f'  [{status}] {term[:60]}')

print(f'\nTotal: {len(l1_terms)}, Found: {len(found_terms)}, Missing: {len(missing_terms)}')
if missing_terms:
    print('\n== MISSING ENTRIES ==')
    for t in missing_terms:
        print(f'  - {t}')
