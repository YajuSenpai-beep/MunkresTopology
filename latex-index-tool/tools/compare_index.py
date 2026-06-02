"""Compare compiled .ind against OCR original index.tex."""
import re, sys
from pathlib import Path
from collections import defaultdict
import io

ROOT = Path(__file__).parent.parent.parent

def strip_tex_math(text: str) -> str:
    """Reduce LaTeX math to comparable form."""
    # Remove \hyperpage{...}
    text = re.sub(r'\\hyperpage\{[^}]+\}', '', text)
    # Remove \lettergroup{...}
    text = re.sub(r'\\lettergroup\{[^}]+\}', '', text)
    # Normalize $...$ and \(...\) both to empty (math is math)
    text = re.sub(r'\$[^$]+\$', 'MATH', text)
    text = re.sub(r'\\\([^)]+\\\)', 'MATH', text)
    # Collapse whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    text = text.rstrip(', ')
    return text

def normalize_for_compare(text: str) -> str:
    """Normalize for loose comparison."""
    t = text.lower()
    # Remove all page numbers
    t = re.sub(r',?\s*\\hyperpage\{[^}]+\}', '', t)
    t = re.sub(r',?\s*\d{1,4}(?:\s*,\s*\d{1,4})*', '', t)
    # Normalize braces/curly
    t = t.replace('{', '').replace('}', '')
    # Collapse whitespace
    t = re.sub(r'\s+', ' ', t).strip()
    t = t.rstrip(',. ')
    return t

def parse_ind(path: str) -> dict:
    """Parse compiled .ind -> {letter: [(l1_norm, [l2_norm...]), ...]}"""
    text = Path(path).read_text(encoding="utf-8")
    groups = {}
    current_letter = None
    current_l1 = None
    current_subs = []

    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        m = re.search(r'\\lettergroup\{(\w+)\}', line)
        if m:
            current_letter = m.group(1)
            groups[current_letter] = []
            current_l1 = None
            current_subs = []
            continue
        m = re.match(r'\\item\s+(.+)', line)
        if m:
            if current_l1 is not None and current_letter is not None:
                groups[current_letter].append((current_l1, current_subs))
            current_l1 = strip_tex_math(m.group(1)).strip()
            current_subs = []
            continue
        m = re.match(r'\\subitem\s+(.+)', line)
        if m:
            current_subs.append(strip_tex_math(m.group(1)).strip())
            continue

    if current_l1 is not None and current_letter is not None:
        groups[current_letter].append((current_l1, current_subs))

    return groups

def parse_ocr(path: str) -> dict:
    """Parse OCR original index -> {letter: [(l1, [l2...]), ...]}"""
    text = Path(path).read_text(encoding="utf-8")
    groups = {}
    current_letter = None
    current_l1 = None
    current_subs = []

    lines = text.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        if not stripped:
            i += 1
            continue

        # Letter heading (single uppercase letter, possibly with extra chars)
        if re.match(r'^[A-Z]$', stripped):
            if current_l1 is not None and current_letter is not None:
                groups[current_letter].append((current_l1, current_subs))
            current_letter = stripped
            if current_letter not in groups:
                groups[current_letter] = []
            current_l1 = None
            current_subs = []
            i += 1
            continue

        # Symbol heading like \mathbb{R}
        if re.match(r'^\\mathbb\{R\}$', stripped):
            if current_l1 is not None and current_letter is not None:
                groups[current_letter].append((current_l1, current_subs))
            current_letter = '\\mathbb{R}'
            groups[current_letter] = []
            current_l1 = None
            current_subs = []
            i += 1
            continue

        # Indented line = L2
        if line.startswith(' ') or line.startswith('\t'):
            if current_l1 is not None:
                current_subs.append(stripped)
        else:
            # Flush left = L1
            if current_l1 is not None and current_letter is not None:
                groups[current_letter].append((current_l1, current_subs))
            current_l1 = stripped
            current_subs = []

        i += 1

    if current_l1 is not None and current_letter is not None:
        groups[current_letter].append((current_l1, current_subs))

    # Merge \mathbb{R} into R group
    if '\\mathbb{R}' in groups:
        if 'R' not in groups:
            groups['R'] = []
        groups['R'].extend(groups['\\mathbb{R}'])
        del groups['\\mathbb{R}']

    return groups

def get_letter(entry_text: str) -> str:
    """Get the first letter of entry (for OCR entries which have no letter grouping)."""
    t = entry_text.strip()
    if not t:
        return '?'
    if t.startswith('\\'):
        # Math symbol entry
        return 'SYM'
    c = t[0].upper()
    if c.isalpha():
        return c
    return 'SYM'

def main():
    ind_path = ROOT / 'Topology_by_Munkres.ind'
    ocr_path = ROOT / 'original' / 'temp' / 'index.tex'

    ind = parse_ind(str(ind_path))
    ocr = parse_ocr(str(ocr_path))

    # Map symbol groups
    symbol_map = {'\\mathbb{R}': 'R'}

    # Build flat sets for comparison per letter
    all_letters = sorted(set(list(ind.keys()) + list(ocr.keys())))

    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

    print("=== MISSING/EXTRA L1 ENTRIES BY LETTER ===")

    total_missing_l1 = 0
    total_extra_l1 = 0
    total_missing_l2 = 0

    for letter in all_letters:
        ocr_entries = ocr.get(letter, [])
        ind_entries = ind.get(letter, [])

        if not ocr_entries and not ind_entries:
            continue

        # Build normalized maps
        ocr_norm = {}
        for l1, subs in ocr_entries:
            k = normalize_for_compare(l1)
            if k:
                ocr_norm[k] = (l1, subs)

        ind_norm = {}
        for l1, subs in ind_entries:
            k = normalize_for_compare(l1)
            if k:
                ind_norm[k] = (l1, subs)

        ocr_keys = set(ocr_norm.keys())
        ind_keys = set(ind_norm.keys())

        missing_keys = ocr_keys - ind_keys
        extra_keys = ind_keys - ocr_keys
        common_keys = ocr_keys & ind_keys

        if missing_keys or extra_keys:
            print(f"\n[{letter}] OCR={len(ocr_entries)}, IND={len(ind_entries)}, missing={len(missing_keys)}, extra={len(extra_keys)}")

            if missing_keys:
                total_missing_l1 += len(missing_keys)
                print("  MISSING L1:")
                for k in sorted(missing_keys)[:20]:
                    l1, subs = ocr_norm[k]
                    s = l1[:100]
                    print(f"    - {s}")
                    for sub in subs[:3]:
                        print(f"        L2: {sub[:100]}")
                    if len(subs) > 3:
                        print(f"        ... +{len(subs)-3} more L2")
                if len(missing_keys) > 20:
                    print(f"    ... and {len(missing_keys)-20} more missing L1")

            if extra_keys:
                total_extra_l1 += len(extra_keys)
                print("  EXTRA L1:")
                for k in sorted(extra_keys)[:10]:
                    l1, subs = ind_norm[k]
                    print(f"    + {l1[:100]}")
                if len(extra_keys) > 10:
                    print(f"    ... and {len(extra_keys)-10} more extra L1")

        # L2 comparison for common L1s
        if common_keys:
            for k in sorted(common_keys):
                ocr_l1, ocr_subs = ocr_norm[k]
                ind_l1, ind_subs = ind_norm[k]
                ocr_sub_norm = {normalize_for_compare(s) for s in ocr_subs}
                ind_sub_norm = {normalize_for_compare(s) for s in ind_subs}
                missing_subs = ocr_sub_norm - ind_sub_norm
                if missing_subs:
                    total_missing_l2 += len(missing_subs)
                    # Only show if significant
                    if len(missing_subs) >= 3 or letter in 'ABC':
                        print(f"  [{letter}] L2 under '{ocr_l1[:50]}':")
                        for s in sorted(missing_subs)[:5]:
                            print(f"    MISS L2: {s[:100]}")
                        if len(missing_subs) > 5:
                            print(f"    ... +{len(missing_subs)-5} more")

    print(f"\n{'='*60}")
    print(f"TOTAL: Missing L1={total_missing_l1}, Extra L1={total_extra_l1}, Missing L2={total_missing_l2}")

if __name__ == '__main__':
    main()
