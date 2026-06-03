"""Deduplicate adjacent identical \index{...} commands in tex source files.

\index{foo}\index{foo}\index{foo} -> \index{foo}
Uses string parsing (no regex) to avoid Python 3.14 bad escape issues.
"""

import os
import sys


def dedup_line(line):
    """Replace adjacent identical \\index{...} with a single copy."""
    result = []
    i = 0
    last_token = None

    while i < len(line):
        if line[i:i+7] == '\\index{':
            depth = 1
            j = i + 7
            while j < len(line) and depth > 0:
                if line[j] == '{':
                    depth += 1
                elif line[j] == '}':
                    depth -= 1
                j += 1
            token = line[i:j]
            if token != last_token:
                result.append(token)
                last_token = token
            i = j
        else:
            result.append(line[i])
            last_token = None
            i += 1

    return ''.join(result)


def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    lines = content.split('\n')
    changed_lines = 0

    for i, line in enumerate(lines):
        new_line = dedup_line(line)
        if new_line != line:
            lines[i] = new_line
            changed_lines += 1

    if changed_lines:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))
        print(f'{os.path.basename(filepath)}: {changed_lines} lines deduplicated')
    else:
        print(f'{os.path.basename(filepath)}: no duplicates found')


if __name__ == '__main__':
    chapters_dir = sys.argv[1] if len(sys.argv) > 1 else 'chapters'
    if not os.path.isdir(chapters_dir):
        chapters_dir = os.path.join(os.path.dirname(__file__), '..', 'chapters')

    for f in sorted(os.listdir(chapters_dir)):
        if f.endswith('.tex'):
            process_file(os.path.join(chapters_dir, f))
