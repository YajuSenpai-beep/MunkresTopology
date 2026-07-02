#!/usr/bin/env python3
"""
Conservative Chinese speech manuscript filler removal.
Target: 3-5% character reduction. Keep ALL ## sections.
"""

import re
import sys
import os

INPUT = r"E:\BaiduNetdiskDownload\老梅面试\讲话稿成品\完整稿\10_典题精讲_模拟类.md"
OUTPUT = r"E:\BaiduNetdiskDownload\老梅面试\讲话稿成品\精炼稿\10_典题精讲_模拟类.md"

with open(INPUT, 'r', encoding='utf-8') as f:
    text = f.read()

total_before = len(text)
sections_before = len(re.findall(r'^## ', text, re.MULTILINE))
separators_before = len(re.findall(r'^---', text, re.MULTILINE))

print(f"BEFORE: {total_before} chars, {sections_before} sections, {separators_before} separators")

removal_stats = {}

def record(category, removed_chars):
    removal_stats[category] = removal_stats.get(category, 0) + removed_chars

# ============================================================
# RULE 1: Stuttering — 3+ identical Chinese chars in a row → 1
# ============================================================
def rule1_stuttering(t):
    count = 0
    removed = 0
    def repl(m):
        nonlocal count, removed
        count += 1
        r = len(m.group(0)) - 1
        removed += r
        return m.group(1)
    t = re.sub(r'([一-鿿])\1{2,}', repl, t)
    record('stutter', removed)
    print(f"  R1 Stuttering (3+ same char): {count} fixes, {removed} chars removed")
    return t

# ============================================================
# RULE 2: Exact consecutive phrase repeats (2-10 char phrase)
# ============================================================
def rule2_phrase_repeats(t):
    count = 0
    removed = 0
    def repl(m):
        nonlocal count, removed
        phrase = m.group(1)
        # Skip single-function chars
        if phrase in ('的', '了', '着', '过', '得'):
            return m.group(0)
        count += 1
        r = len(m.group(0)) - len(phrase)
        removed += r
        return phrase
    t = re.sub(r'([一-鿿]{3,10})(?:[，,、]?\s*)\1', repl, t)
    record('phrase_repeat', removed)
    print(f"  R2 Phrase repeats: {count} fixes, {removed} chars removed")
    return t

# ============================================================
# RULE 3: "就是，就是" → "就是，" double-word stuttering
# ============================================================
def rule3_double_stutter(t):
    count = 0
    removed = 0
    def repl(m):
        nonlocal count, removed
        r = len(m.group(0)) - len(m.group(1))
        removed += r
        count += 1
        return m.group(1)
    t = re.sub(r'([一-鿿]{2})(?:[，,、]\s*)\1(?:[，,、]\s*)', repl, t)
    record('double_stutter', removed)
    print(f"  R3 Double-word stuttering: {count} fixes, {removed} chars removed")
    return t

# ============================================================
# RULE 4: Pure interjections — 啧, 嘶
# ============================================================
def rule4_interjections(t):
    count = 0
    removed = 0
    for pattern in [r'啧[，,、]?\s*', r'嘶[，,、]?\s*']:
        for m in re.findall(pattern, t):
            removed += len(m.strip())
            count += 1
        t = re.sub(pattern, '', t)
    record('interjections', removed)
    print(f"  R4 Interjections (啧/嘶): {count} fixes, {removed} chars removed")
    return t

# ============================================================
# RULE 5: "所以说" at sentence/paragraph start (pure transitional filler)
# ============================================================
def rule5_suoyishuo(t):
    count = 0
    removed = 0
    def repl(m):
        nonlocal count, removed
        r = len(m.group(0))
        removed += r
        count += 1
        return ''
    t = re.sub(r'(?:^|(?<=[。！？]))\s*所以说[，,、]?\s*', repl, t, flags=re.MULTILINE)
    record('suoyishuo', removed)
    print(f"  R5 所以说 (sentence start): {count} fixes, {removed} chars removed")
    return t

# ============================================================
# RULE 6: "那个什么" / "那个啥" filler phrases
# ============================================================
def rule6_filler_phrases(t):
    count = 0
    removed = 0
    for pattern in [r'那个什么[的之]?[，,、]?\s*', r'那个啥[的之]?[，,、]?\s*']:
        for m in re.findall(pattern, t):
            removed += len(m)
            count += 1
        t = re.sub(pattern, '', t)
    record('filler_phrase', removed)
    print(f"  R6 Filler phrases (那个什么/那个啥): {count} fixes, {removed} chars removed")
    return t

# ============================================================
# RULE 7: "就是，" at clause start repeated → single
# ============================================================
def rule7_jiushi_repeat(t):
    count = 0
    removed = 0
    def repl(m):
        nonlocal count, removed
        r = len(m.group(0)) - len('就是，')
        removed += r
        count += 1
        return '就是，'
    t = re.sub(r'就是[，,、]\s*就是[，,、]?\s*', repl, t)
    record('jiushi_repeat', removed)
    print(f"  R7 就是 repeat: {count} fixes, {removed} chars removed")
    return t

# ============================================================
# RULE 8: "呃，" removal as interjection
#   "呃，" or "呃" at start of clause after punctuation
# ============================================================
def rule8_e_interjection(t):
    count = 0
    removed = 0
    for m in re.finditer(r'([。，,、\s])呃[，,、]?\s*', t):
        removed += len(m.group(0)) - len(m.group(1))
        count += 1
    t = re.sub(r'([。，,、\s])呃[，,、]?\s*', r'\1', t)
    record('e_interjection', removed)
    print(f"  R8 呃 interjection: {count} fixes, {removed} chars removed")
    return t

# ============================================================
# RULE 9: Conservative "啊" removal at clause end
#   Only when 啊 is clearly filler (not question, not fixed expression)
#   Pattern: statement-word + 啊 + [，。]
#   KEEP: 好啊, 对啊, 行啊, 是啊, 该啊, 看啊, 听啊
#   KEEP: after question words 什么啊, 怎么啊, 谁啊, 哪啊
# ============================================================
def rule9_a_filler(t):
    count = 0
    removed = 0
    # Remove "啊" when preceded by a non-question, non-fixed-expression word
    # and followed by ， or 。
    # KEEP patterns: words ending with 好对行是该要看听
    # KEEP: question words 什么, 怎么, 谁, 哪, 几, 吗
    # We match: [preceding char that's NOT one of the safe chars] 啊 [，。]
    # Actually safer: remove 啊 only when preceded by multi-char phrases
    # that don't end with safe chars

    def repl(m):
        nonlocal count, removed
        word_before = m.group(1)  # the word(s) before 啊
        punct = m.group(2)        # the punctuation after 啊
        # KEEP: if the word is a single char that's common in fixed expressions
        safe_single = '好对行是该要看听来去走说有能做给让叫请'
        if len(word_before) == 1 and word_before in safe_single:
            return m.group(0)
        # KEEP: if the word ends with a question indicator
        if word_before.endswith(('什么', '怎么', '为什', '干什')):
            return m.group(0)
        # KEEP: 啊 preceded by 吗, 吧, 呢 (double particles)
        # OK to remove: standalone 啊 after complete statement
        count += 1
        removed += 1  # remove just the 啊
        return word_before + punct

    t = re.sub(r'([一-鿿]{1,6})啊([，。])', repl, t)
    record('a_filler', removed)
    print(f"  R9 啊 filler (clause end): {count} fixes, {removed} chars removed")
    return t

# ============================================================
# RULE 10: "嘛" at clause end removal
#   KEEP: 干嘛, 什么嘛 (question-like)
# ============================================================
def rule10_ma_filler(t):
    count = 0
    removed = 0
    def repl(m):
        nonlocal count, removed
        word_before = m.group(1)
        punct = m.group(2)
        # KEEP in question expressions
        if word_before in ('干', '什') or word_before.endswith(('什么', '干什')):
            return m.group(0)
        count += 1
        removed += 1
        return word_before + punct
    t = re.sub(r'([一-鿿]{1,6})嘛([，。])', repl, t)
    record('ma_filler', removed)
    print(f"  R10 嘛 filler (clause end): {count} fixes, {removed} chars removed")
    return t

# ============================================================
# RULE 11: "呢" at end of non-question clauses
#   Very conservative — only when clearly filler in statement
# ============================================================
def rule11_ne_filler(t):
    count = 0
    removed = 0
    def repl(m):
        nonlocal count, removed
        word_before = m.group(1)
        punct = m.group(2)
        # KEEP: question words
        if word_before in ('什么', '怎么', '谁', '哪', '为什', '干什'):
            return m.group(0)
        # KEEP: 呢 preceded by 的 (nominalization marker)
        if word_before.endswith('的'):
            return m.group(0)
        # OK to remove
        count += 1
        removed += 1
        return word_before + punct
    t = re.sub(r'([一-鿿]{1,6})呢([，。])', repl, t)
    record('ne_filler', removed)
    print(f"  R11 呢 filler (clause end): {count} fixes, {removed} chars removed")
    return t

# ============================================================
# RULE 12: Additional interjections — 嗯, 额, 哈 as standalone fillers
# ============================================================
def rule12_more_interjections(t):
    count = 0
    removed = 0
    # "嗯，" / "嗯。" at start of clause (after punctuation)
    for m in re.finditer(r'([。，,、\s])嗯[，,、。]?\s*', t):
        removed += len(m.group(0)) - len(m.group(1))
        count += 1
    t = re.sub(r'([。，,、\s])嗯[，,、。]?\s*', r'\1', t)

    # "额，" / "额" at clause start
    for m in re.finditer(r'([。，,、\s])额[，,、]?\s*', t):
        removed += len(m.group(0)) - len(m.group(1))
        count += 1
    t = re.sub(r'([。，,、\s])额[，,、]?\s*', r'\1', t)

    # "哈，" / "哈" as interjection (NOT "哈哈")
    for m in re.finditer(r'(?<![哈一-鿿])哈[，,、]?\s*', t):
        # Skip if followed by another 哈 (would be 哈哈)
        if t[m.end():m.end()+1] != '哈':
            removed += len(m.group(0))
            count += 1
    t = re.sub(r'(?<![哈一-鿿])哈[，,、]?\s*(?!哈)', '', t)

    # "诶，" interjection
    for m in re.findall(r'诶[，,、]?\s*', t):
        removed += len(m)
        count += 1
    t = re.sub(r'诶[，,、]?\s*', '', t)

    record('more_interjections', removed)
    print(f"  R12 More interjections (嗯/额/哈/诶): {count} fixes, {removed} chars removed")
    return t

# ============================================================
# RULE 13: Clean up double punctuation
# ============================================================
def rule13_cleanup(t):
    count = 0
    removed = 0
    # Fix patterns like "，。" → "。" or "，，" → "，"
    for pattern, replacement in [
        (r'[，,]\s*[。]', '。'),   # "，。" → "。"
        (r'[，,]\s*[，,]', '，'),  # "，，" → "，"
        (r'[。]\s*[，,]', '。'),   # "。，" → "。"
        (r'[、]\s*[、]', '、'),    # "、、" → "、"
    ]:
        for m in re.finditer(pattern, t):
            r = len(m.group(0)) - len(replacement)
            if r > 0:
                removed += r
                count += 1
        t = re.sub(pattern, replacement, t)

    record('cleanup', removed)
    print(f"  R13 Double-punct cleanup: {count} fixes, {removed} chars removed")
    return t

# ============================================================
# RULE 14: 2-char stuttering like "这这", "去去", "等等等"
#   Reduce to single char when clearly stutter (not semantic repetition)
# ============================================================
def rule14_twochar_stutter(t):
    count = 0
    removed = 0
    # "这这" → "这", "去去" → "去" but only when followed by other chars
    # and not part of a meaningful word
    def repl(m):
        nonlocal count, removed
        count += 1
        removed += 1
        return m.group(1)
    # Only match 2 identical chars that are NOT part of a known double-char word
    # and are followed immediately by another Chinese character
    t = re.sub(r'(?<![一-鿿])([一-鿿])\1(?=[一-鿿])', repl, t)
    record('twochar_stutter', removed)
    print(f"  R14 2-char stuttering: {count} fixes, {removed} chars removed")
    return t

# ============================================================
# Apply all rules
# ============================================================
text = rule1_stuttering(text)
text = rule2_phrase_repeats(text)
text = rule3_double_stutter(text)
text = rule4_interjections(text)
text = rule8_e_interjection(text)
text = rule12_more_interjections(text)
text = rule5_suoyishuo(text)
text = rule6_filler_phrases(text)
text = rule7_jiushi_repeat(text)
text = rule9_a_filler(text)
text = rule10_ma_filler(text)
text = rule11_ne_filler(text)
text = rule13_cleanup(text)

# ============================================================
# Verify
# ============================================================
total_after = len(text)
sections_after = len(re.findall(r'^## ', text, re.MULTILINE))
separators_after = len(re.findall(r'^---', text, re.MULTILINE))
reduction = total_before - total_after
pct = (reduction / total_before) * 100

print(f"\n{'='*60}")
print(f"SUMMARY:")
print(f"  BEFORE: {total_before} chars")
print(f"  AFTER:  {total_after} chars")
print(f"  REMOVED: {reduction} chars ({pct:.1f}%)")
print(f"  Sections: {sections_before} → {sections_after}")
print(f"  Separators: {separators_before} → {separators_after}")
for cat, chars in sorted(removal_stats.items(), key=lambda x: -x[1]):
    print(f"    {cat}: {chars} chars")

if sections_after != sections_before:
    print(f"\nERROR: Section count changed! {sections_before} → {sections_after}")
    sys.exit(1)

if separators_after != separators_before:
    print(f"\nERROR: Separator count changed! {separators_before} → {separators_after}")
    sys.exit(1)

if pct < 3.0:
    print(f"\nWARNING: Reduction {pct:.1f}% is below 3% target")
elif pct > 5.5:
    print(f"\nWARNING: Reduction {pct:.1f}% is above 5% target")

# ============================================================
# Write output
# ============================================================
os.makedirs(os.path.dirname(OUTPUT), exist_ok=True)
with open(OUTPUT, 'w', encoding='utf-8') as f:
    f.write(text)

print(f"\nOutput written to: {OUTPUT}")
