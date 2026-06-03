"""Compare original entries (JSON) vs. compiled .ind and output missing entries.

Usage: python _compare_index.py [--brief] > report/missing-entries.txt
"""

import json
import re
import os
import sys


def esc(cmd):
    return re.escape(cmd)


# --- Parse compiled .ind ---
def parse_ind(filepath):
    """Parse Topology_by_Munkres.ind -> {L1_text: [L2_texts]}"""
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    result = {}
    current_l1 = None

    for line in lines:
        s = line.strip()

        if re.match(esc(r'\lettergroup') + r'\{(\w+)\}', s):
            continue

        m = re.match(esc(r'\item') + r'\s+(.*?)(?:,\s*)?$', s)
        if m:
            current_l1 = clean_ind_text(m.group(1))
            if current_l1 and current_l1 not in result:
                result[current_l1] = []
            continue

        m = re.match(esc(r'\subitem') + r'\s+(.*?)(?:,\s*)?$', s)
        if m:
            text = clean_ind_text(m.group(1))
            if current_l1 and current_l1 in result:
                result[current_l1].append(text)
            continue

    return result


def clean_ind_text(text):
    text = text.strip()
    text = re.sub(r'\s*' + esc(r'\hyperpage') + r'\{[^}]*\}', '', text)
    text = text.rstrip(',').strip()
    text = ' '.join(text.split())
    return text


# --- Parse JSON entries ---
def parse_json_entries(filepath):
    """Parse original/index_entries.json -> [(L1, L2_or_None), ...].
    Handles (cont.) suffixes and compound parent names from OCR."""
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)

    entries = data['entries']
    result = []
    current_l1 = None

    for e in entries:
        term = clean_json_text(e['term'])
        if e['level'] == 1:
            # Strip (cont.) — continuation of previous L1
            clean = re.sub(r'\s*\(cont\.\)\s*', '', term).strip()
            # Handle compound: "Foo: bar" — real parent is "Foo"
            if ': ' in clean:
                parts = clean.split(': ', 1)
                if current_l1 and norm_key(current_l1).startswith(norm_key(parts[0])):
                    pass  # compound continuation, keep current_l1
                else:
                    current_l1 = clean
            else:
                current_l1 = clean
            result.append((current_l1, []))
        elif e['level'] == 2:
            if current_l1 is not None and result:
                result[-1][1].append(term)

    return result


def clean_json_text(text):
    text = text.strip()
    text = ' '.join(text.split())
    return text


# --- Normalize for comparison ---
def norm_key(text):
    """Create a normalized key for fuzzy matching."""
    t = text.lower()
    t = re.sub(r'\$[^$]+\$', '', t)
    t = re.sub(r'\\(?:\(|\)|\[|\])', '', t)  # remove \( \) \[ \]
    t = re.sub(r'\\(?:mathbf|mathbb|mathcal|mathrm|text|widehat|bar|tilde)\{([^}]*)\}', r'\1', t)
    t = re.sub(r'\\[a-zA-Z]+', '', t)
    t = re.sub(r'[^\w\s]', '', t)
    t = ' '.join(t.split())
    return t


def find_match(target, candidates):
    """Find best match for target in candidates dict {norm_key: original_key}."""
    nk = norm_key(target)
    if nk in candidates:
        return candidates[nk]

    # Fuzzy: substring match
    for ck, cv in candidates.items():
        if nk in ck or ck in nk:
            return cv

    # Try word-by-word overlap
    target_words = set(nk.split())
    for ck, cv in candidates.items():
        ck_words = set(ck.split())
        if target_words & ck_words and len(target_words & ck_words) >= min(len(target_words), len(ck_words)) * 0.7:
            return cv

    return None


# --- Main ---
def compare(base_dir):
    ind_file = os.path.join(base_dir, 'Topology_by_Munkres.ind')
    json_file = os.path.join(base_dir, 'original', 'index_entries.json')

    ind = parse_ind(ind_file)
    json_entries = parse_json_entries(json_file)

    # Build ind lookup
    ind_keys = {norm_key(k): k for k in ind}

    missing_l1 = []
    missing_l2 = []

    for l1_term, l2_terms in json_entries:
        matched_l1 = find_match(l1_term, ind_keys)

        if matched_l1 is None:
            missing_l1.append(l1_term)
            for l2 in l2_terms:
                missing_l2.append((l1_term, l2))
        else:
            ind_l2s = ind.get(matched_l1, [])
            ind_l2_keys = {norm_key(k): k for k in ind_l2s}

            for l2 in l2_terms:
                matched_l2 = find_match(l2, ind_l2_keys)
                if matched_l2 is None:
                    missing_l2.append((l1_term, l2))

    brief = '--brief' in sys.argv

    if not brief:
        print("MISSING L1 ENTRIES")
        print("=" * 60)
        for l1 in missing_l1:
            print(l1)

        print()
        print("MISSING L2 ENTRIES (parent!child)")
        print("=" * 60)
        for l1, l2 in missing_l2:
            print(f"{l1}!{l2}")

    print()
    print(f"Total L1 in JSON: {len(json_entries)}")
    print(f"Total L1 in .ind: {len(ind)}")
    print(f"Missing L1: {len(missing_l1)}")
    print(f"Missing L2: {len(missing_l2)}")


if __name__ == '__main__':
    base = sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith('--') else '.'
    compare(base)
