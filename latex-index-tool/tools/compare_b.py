"""Compare B section of OCR vs .ind"""
import re
from pathlib import Path

ROOT = Path(__file__).parent.parent.parent
bs = chr(92)

ind = (ROOT / 'Topology_by_Munkres.ind').read_text(encoding='utf-8')

# OCR B entries: L1 -> [L2s]
ocr_b = {
    'Baire category theorem': ['special case'],
    'Baire space': ['compact Hausdorff space', 'complete metric space',
                     'fine topology on C(X,Y)', 'locally compact Hausdorff space'],
    'Baire space (cont.)': ['open subspace of Baire space',
                             'R^J in box, product, uniform topologies'],
    'Ball, unit': [],
    'Barber of Seville paradox': [],
    'Base point': [],
    'Base point choice:': ['effect on h_*', 'effect on pi_1'],
    'Basis:': ['for a free abelian group', 'for a topology'],
    'Bd A': [],
    'beta(X)': [],
    'Betti number': [],
    'Bicompactness': [],
    'Bijective function': [],
    'Binary operation': [],
    'Bing metrization theorem': [],
    'Bisection theorem': [],
    'B^n': ['compactness', 'fundamental group', 'path connectedness'],
    'Borsuk lemma': [],
    'Borsuk-Ulam theorem': [],
    'Boundary:': ['of a set', 'of a surface with boundary'],
    'Bounded above': [],
    'Bounded below': [],
    'Bounded function': [],
    'Bounded metric': [],
    'Bounded set': [],
    'Box topology': ['basis for', 'Hausdorff condition', 'subspace',
                     'vs. fine topology', 'vs. product topology', 'vs. uniform topology'],
    'Brouwer fixed-point theorem': [],
    'B^2': [],
    'B(x,epsilon)': [],
}

print(f'OCR B section: {len(ocr_b)} L1, {sum(len(v) for v in ocr_b.values())} L2')
print()

# Extract B section from .ind
b_start = ind.find(bs + 'lettergroup{B}')
c_start = ind.find(bs + 'lettergroup{C}')
b_sec = ind[b_start:c_start] if c_start > b_start else ind[b_start:]

missing_l1 = []
missing_l2 = []

for l1, subs in ocr_b.items():
    # Check L1 in .ind
    l1_lower = l1.lower()
    # Simplify for matching
    l1_key = l1_lower.split(':')[0].split('(')[0].strip()
    l1_key2 = l1_key.replace('bare', 'baire').replace('beta(x)', 'beta')

    # Search b_sec for this L1
    ind_lower = b_sec.lower()
    found_l1 = False
    # Try a few key parts
    parts = l1_key.split()
    if len(parts) >= 2:
        found_l1 = parts[0].lower() in ind_lower and parts[-1].lower() in ind_lower
    if not found_l1:
        found_l1 = l1_key[:8].lower() in ind_lower

    if not found_l1:
        missing_l1.append(l1)
        for sub in subs:
            missing_l2.append((l1, sub))
    else:
        # Check L2s
        for sub in subs:
            # Normalize for comparison
            sub_check = sub.lower()
            sub_check = sub_check.replace('c(x,y)', 'c').replace('r^j', 'r')
            sub_check = sub_check.replace('h_*', 'h').replace('pi_1', 'pi')

            # Very simple: check if key words from sub appear in b_sec near the L1
            l1_pos = ind_lower.find(l1_key[:10])
            if l1_pos >= 0:
                nearby = b_sec.lower()[l1_pos:l1_pos+600]
            else:
                nearby = b_sec.lower()

            # Check sub keywords
            sub_words = [w for w in sub_check.split() if len(w) >= 3]
            if sub_words:
                sub_found = all(w in nearby for w in sub_words[:3])
            else:
                sub_found = sub_check[:5] in nearby

            if not sub_found:
                missing_l2.append((l1, sub))

print('=== MISSING L1 (OCR has, .ind lacks) ===')
for m in missing_l1:
    print(f'  - {m}')

print(f'\n=== MISSING L2 ({len(missing_l2)} entries) ===')
for parent, child in missing_l2:
    print(f'  - {parent}  ->  {child}')

# Check duplicates
bn_items = re.findall(r'\\item\s+.*B.*n.*,', b_sec)
bx_items = re.findall(r'\\item\s+.*B\s*\(.*x.*,', b_sec)
print(f'\n=== POTENTIAL DUPLICATES ===')
print(f'B^n variants: {len(bn_items)}')
for i in bn_items:
    print(f'  {i[:60]}')
print(f'B(x,e) variants: {len(bx_items)}')
for i in bx_items:
    print(f'  {i[:60]}')

# Also show what's in .ind B section (all L1 items)
print(f'\n=== .ind B section L1 items ===')
items = re.findall(r'\\item\s+(.+?)(?:,|\n)', b_sec)
for i, item in enumerate(items):
    # Clean up
    item = re.sub(r'\\hyperpage\{[^}]+\}', '', item)
    item = item.strip().rstrip(',')
    print(f'  {i+1}. {item[:80]}')
