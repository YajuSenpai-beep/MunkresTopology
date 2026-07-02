"""Quick stats for Chapter 2."""
import re

with open(r'chapters/Chapter_2_Topological_Spaces_and_Continuous_Functions.tex', 'r', encoding='utf-8') as f:
    c = f.read()

BS = chr(92)
BS2 = BS + BS

# Count remaining index entries using simple string count
idx_count = c.count(BS + 'index{')
print(f'Remaining \\index entries: {idx_count}')

# Environment balance
envs = ['centeredblock','centeredblock*','definition','theorem','lemma',
        'corollary','example','proof','enumerate','itemize','description','aligned']
for env in envs:
    b = c.count(BS + r'begin{' + env + '}')
    e = c.count(BS + r'end{' + env + '}')
    if b != e:
        print(f'  MISMATCH: {env}: {b} begin / {e} end')
    elif b > 0:
        print(f'  OK: {env}: {b}/{e}')

# Quote balance
open_q = c.count('``')
close_q = c.count("''")
print(f'\nQuotes: `` = {open_q} / \'\' = {close_q} (diff={open_q-close_q})')

# Line/word count
lines = len(c.split('\n'))
words = len(c.split())
print(f'Lines: {lines}')
print(f'Words (approx): {words}')
