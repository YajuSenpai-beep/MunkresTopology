"""Compare L2 entries for R, S, T sections: OCR vs .ind."""
from pathlib import Path
import re, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

ROOT = Path(__file__).parent.parent.parent
bs = chr(92)
ind = (ROOT / 'Topology_by_Munkres.ind').read_text(encoding='utf-8')
ocr_text = (ROOT / 'original' / 'temp' / 'index.tex').read_text(encoding='utf-8')

def parse_ind_section(letter):
    start = ind.find(bs + 'lettergroup{' + letter + '}')
    if start < 0: return []
    end = len(ind)
    for nxt in ['S','T','U','V']:
        n = ind.find(bs + 'lettergroup{' + nxt + '}', start + 10)
        if n > start and n < end: end = n
    section = ind[start:end]
    entries = []
    current_l1 = None; current_subs = []
    for line in section.splitlines():
        s = line.strip()
        if not s: continue
        if s.startswith(bs + 'item ') and not s.startswith(bs + 'subitem '):
            if current_l1: entries.append((current_l1, current_subs))
            l1 = s[len(bs+'item '):]
            hp = l1.find(bs+'hyperpage')
            if hp >= 0: l1 = l1[:hp].strip().rstrip(',')
            current_l1 = l1; current_subs = []
        elif s.startswith(bs + 'subitem '):
            sub = s[len(bs+'subitem '):]
            hp = sub.find(bs+'hyperpage')
            if hp >= 0: sub = sub[:hp].strip().rstrip(',')
            current_subs.append(sub)
    if current_l1: entries.append((current_l1, current_subs))
    return entries

def parse_ocr_section(letter):
    c_start = ocr_text.find('\n' + letter + '\n')
    if c_start < 0: return []
    c_end = len(ocr_text)
    for nxt in 'RSTUVWXYZ':
        n = ocr_text.find('\n' + nxt + '\n', c_start + 2)
        if n > c_start and n < c_end: c_end = n
    section = ocr_text[c_start:c_end]
    lines = section.splitlines()
    entries = []
    current_l1 = None; current_subs = []
    for line in lines:
        s = line.strip()
        if not s or re.match(r'^[A-Z]$', s): continue
        has_pages = bool(re.search(r',?\s*\d{1,4}(?:\s*,\s*\d{1,4})*$', s))
        if line[0] not in (' ','\t') and (has_pages or s.rstrip().endswith(':') or '(cont.)' in s or '(see' in s):
            if current_l1 and current_letter:
                entries.append((current_l1, current_subs))
            current_l1 = s; current_subs = []
        else:
            if current_l1: current_subs.append(s)
    if current_l1: entries.append((current_l1, current_subs))
    return entries

def norm(s):
    s = s.lower()
    s = re.sub(bs+r'[a-zA-Z]+', '', s)
    s = re.sub(r'[{}$^_\\]', '', s)
    s = re.sub(r'\s+', ' ', s).strip().rstrip(',.')
    return s

for letter in 'RST':
    ind_entries = parse_ind_section(letter)
    # Build .ind map
    ind_map = {}
    for l1, subs in ind_entries:
        k = norm(l1)
        if k and len(k) >= 2:
            ind_map[k] = (l1, [norm(s) for s in subs])

    # Since OCR parsing is unreliable for L2, manually list known L2-heavy entries
    big_entries = {
        'R': ['Regularity', 'Restriction', 'mathbb{R}'],
        'S': ['Second-countability', 'Simply connected', 'Seifert-van Kampen', 'Stone-Čech', 'Separation'],
        'T': ['Topological dimension', 'Topological group', 'Topologist', 'Tychonoff', 'Tube lemma'],
    }

    print(f'\n=== {letter}: looking for big L2 entries ===')
    for entry_hint in big_entries.get(letter, []):
        for k, (l1, subs) in ind_map.items():
            if entry_hint.lower() in k:
                print(f'  {l1[:80]}: {len(subs)} L2s')
                for s in subs[:8]:
                    print(f'    - {s[:100]}')
                if len(subs) > 8:
                    print(f'    ... +{len(subs)-8} more')
                break

print('\nDone.')
