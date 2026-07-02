#!/usr/bin/env python3
"""
Batch convert all \includegraphics patterns in MunkresTopology chapter files
to use the unified \munkresfig command.

Patterns handled (in order):
  1. A1: center + includegraphics + hspace + blank + Figure X.Y → \munkresfig[W]{N.M}[Figure N.M]
  2. A2: center + includegraphics + hspace (no label)               → \munkresfig[W]{N.M}
  3. B:  inline \begin{center} \includegraphics... \end{center} \hspace*{3em} Figure X.Y
         inside \item (single-line)                                 → \munkresfig[W]{N.M}[Figure N.M]
  4. B-silent: inline without Figure label                          → \munkresfig[W]{N.M}
"""

import re
import os
import sys

CHAPTERS_DIR = os.path.join(os.path.dirname(__file__), '..', 'chapters')

# ── Pattern 1: labeled standalone (A1) ──────────────────────────────
# Matches: \begin{center}\n  \includegraphics[width=W\textwidth]{images/X.jpg}\n\end{center}\n\hspace*{3em} \n\nFigure Y.Z\n
# The Figure label text is captured verbatim as group 3
RE_A1 = re.compile(
    r'\\begin\{center\}\n'
    r'\s*\\includegraphics\[width=([\d.]+)\\textwidth\]\{images/([\d.]+)\.jpg\}\n'
    r'\s*\\end\{center\}\n'
    r'\s*\\hspace\*\{3em\}\s*\n'
    r'\s*\n'                          # blank line between hspace and Figure
    r'\s*(Figure\s+[\d.]+\S?)\s*\n',   # capture Figure label
    re.MULTILINE
)

# ── Pattern 2: unlabeled standalone (A2) ────────────────────────────
# Matches: \begin{center}\n  \includegraphics[width=W\textwidth]{images/X.jpg}\n\end{center}\n\hspace*{3em} \n
# Must NOT be followed by "Figure" on the next non-blank line
RE_A2 = re.compile(
    r'\\begin\{center\}\n'
    r'\s*\\includegraphics\[width=([\d.]+)\\textwidth\]\{images/([\d.]+)\.jpg\}\n'
    r'\s*\\end\{center\}\n'
    r'\s*\\hspace\*\{3em\}\s*\n'
    r'(?!\s*\n\s*Figure\s)',           # negative lookahead: NOT followed by Figure label
    re.MULTILINE
)

# ── Pattern 3: inline labeled (B) ───────────────────────────────────
# Matches: \begin{center} \includegraphics[width=W\textwidth]{images/X.jpg} \end{center} \hspace*{3em} Figure Y.Z
RE_B = re.compile(
    r'\\begin\{center\}\s+'
    r'\\includegraphics\[width=([\d.]+)\\textwidth\]\{images/([\d.]+)\.jpg\}\s+'
    r'\\end\{center\}\s+'
    r'\\hspace\*\{3em\}\s+'
    r'(Figure\s+[\d.]+\S?)',           # capture Figure label
    re.MULTILINE
)

# ── Pattern 4: inline unlabeled (B-silent) ──────────────────────────
# Matches: \begin{center} \includegraphics[width=W\textwidth]{images/X.jpg} \end{center} \hspace*{3em}
# (no Figure label following)
RE_B_SILENT = re.compile(
    r'\\begin\{center\}\s+'
    r'\\includegraphics\[width=([\d.]+)\\textwidth\]\{images/([\d.]+)\.jpg\}\s+'
    r'\\end\{center\}\s+'
    r'\\hspace\*\{3em\}(?!\s+Figure)',  # negative lookahead: NOT followed by Figure
    re.MULTILINE
)

# ── Pattern 5: Fix missing images/ prefix ───────────────────────────
# Matches \includegraphics[...]{N.M.jpg} where images/ prefix is missing
RE_MISSING_PREFIX = re.compile(
    r'\\includegraphics\[(width=[\d.]+\\textwidth)\]\{(?!images/)([\d.]+\.jpg)\}'
)


def convert_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content
    counts = {'A1': 0, 'A2': 0, 'B': 0, 'B_silent': 0, 'prefix_fix': 0}

    # Step 1: Pattern A1 (labeled standalone) — must be first
    def repl_a1(m):
        counts['A1'] += 1
        width = m.group(1)
        fname = m.group(2)
        label = m.group(3).strip()
        return f'\\munkresfig[{width}]{{{fname}}}[{label}]\n'

    content = RE_A1.sub(repl_a1, content)

    # Step 2: Pattern B (inline labeled) — before A2 since they share prefix
    def repl_b(m):
        counts['B'] += 1
        width = m.group(1)
        fname = m.group(2)
        label = m.group(3).strip()
        return f'\\munkresfig[{width}]{{{fname}}}[{label}]'

    content = RE_B.sub(repl_b, content)

    # Step 3: Pattern B-silent (inline unlabeled)
    def repl_b_silent(m):
        counts['B_silent'] += 1
        width = m.group(1)
        fname = m.group(2)
        return f'\\munkresfig[{width}]{{{fname}}}'

    content = RE_B_SILENT.sub(repl_b_silent, content)

    # Step 4: Pattern A2 (unlabeled standalone) — after A1
    def repl_a2(m):
        counts['A2'] += 1
        width = m.group(1)
        fname = m.group(2)
        return f'\\munkresfig[{width}]{{{fname}}}\n'

    content = RE_A2.sub(repl_a2, content)

    # Step 5: Fix missing images/ prefix
    def repl_prefix(m):
        counts['prefix_fix'] += 1
        width_spec = m.group(1)
        fname = m.group(2)
        return f'\\includegraphics[{width_spec}]{{images/{fname}}}'

    content = RE_MISSING_PREFIX.sub(repl_prefix, content)

    total = sum(counts.values())
    if total == 0:
        return None, counts

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    return total, counts


def main():
    chapter_files = sorted(
        f for f in os.listdir(CHAPTERS_DIR)
        if f.endswith('.tex')
    )

    total_images = 0
    grand_counts = {'A1': 0, 'A2': 0, 'B': 0, 'B_silent': 0, 'prefix_fix': 0}

    for fname in chapter_files:
        filepath = os.path.join(CHAPTERS_DIR, fname)
        n, counts = convert_file(filepath)
        if n is not None:
            print(f'  {fname}: {n} conversions')
            for k, v in counts.items():
                if v:
                    print(f'    {k}: {v}')
                    grand_counts[k] += v
            total_images += n

    print(f'\n═══ TOTAL: {total_images} conversions ═══')
    for k, v in grand_counts.items():
        if v:
            print(f'  {k}: {v}')


if __name__ == '__main__':
    main()
