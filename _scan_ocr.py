import os, re

PATTERNS = [
    # missing space before math inline
    (r'([a-z])\\\(', 'missing space before \\( '),
    # missing space after math inline
    (r'\\\)([a-zA-Z])', 'missing space after \\) '),
    # digit stuck to word: "to0", "is1"
    (r'\b([a-zA-Z]+)(\d+)\b', 'digit stuck to word'),
    # "off the" vs "of the"
    (r'\boff\s+the\b', '"off the" (should be "of the")'),
    # missing period after year
    (r'(\d{4})\s+([A-Z][a-z])', 'missing period after year'),
    # 3+ spaces
    (r' {3,}', '3+ spaces'),
    # typos
    (r'\bderving\b', '"derving" typo'),
    (r'\bto0\b', '"to0" should be "to 0"'),
    (r'\bthier\b', '"thier" typo'),
    (r'\bteh\b', '"teh" typo'),
    (r'\brecieve\b', '"recieve" typo'),
]

for fn in sorted(os.listdir('chapters')):
    if not fn.startswith('Chapter_1'):
        continue
    fp = os.path.join('chapters', fn)
    with open(fp, encoding='utf-8') as f:
        lines = f.readlines()

    issues = []
    for i, line in enumerate(lines, 1):
        for pattern, desc in PATTERNS:
            m = re.search(pattern, line)
            if m:
                # skip false positives inside \begin, \end, \cite, etc.
                if any(cmd in line for cmd in ['\\begin{', '\\end{', '\\cite{', '\\ref{']):
                    continue
                issues.append((i, desc, m.group(0), line.strip()[:120]))
                break

    short = fn.replace('Chapter_', 'Ch').replace('.tex', '')
    if issues:
        print(f'\n=== {short} ===')
        for lineno, desc, match, text in issues[:40]:
            print(f'  L{lineno} [{desc}] "{match}"')
            print(f'         {text}')
    else:
        print(f'{short}: no issues found')
