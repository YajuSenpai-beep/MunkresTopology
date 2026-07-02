#!/usr/bin/env python3
"""
Process raw ASR transcripts into structured speech manuscripts (讲话稿).

Core algorithm:
1. Join fragmented ASR lines into flowing paragraphs
2. Add Chinese punctuation at semantic boundaries
3. Remove pure filler words while preserving ALL content
4. Segment at major topic transitions (transition words, questions, etc.)
5. Target ~1.1:1 density (remove ~9% filler, add punctuation)

Key distinction from previous attempts:
- NOT condensing/summarizing — preserving full spoken content
- Adding structure: paragraphs, punctuation, logical breaks
- Each TXT → one complete lecture in the output
"""

import re
import os
import sys

# ─── Filler words to remove ───────────────────────────────────────────
PURE_FILLERS = {
    '啊', '嗯', '呃', '呵', '哦', '哈', '哈哈', '哈哈哈', '嘿嘿',
    '好吧啊', '好啊', '嗯啊', '呃啊', '啊嗯',
}

# Standalone affirmations that don't carry content when alone
STANDALONE_FILLERS = {
    '对', '是', '对呀', '是啊', '对对对', '是是是', '好', '行',
    '对吧', '对的对的', '是的', '没错', '嗯嗯', '嗯嗯嗯',
}

# Laughter and interjections to strip from within sentences
# These are pure vocal sounds that don't belong in a written manuscript
LAUGHTER_PATTERNS = [
    '哈哈哈哈哈哈',
    '哈哈哈哈',
    '哈哈哈',
    '哈哈',
    '呵呵呵呵',
    '呵呵呵',
    '呵呵',
    '嘿嘿嘿',
    '嘿嘿',
    '嘻嘻嘻',
    '嘻嘻',
    '吼吼吼',
    '吼吼',
    '呵',   # single-char light laugh (only when standalone, not part of words)
]

# ─── Sentence/paragraph boundary markers ──────────────────────────────
# Words that, when appearing at the START of a line, indicate a new
# thought/sentence is beginning (not just mid-sentence continuation)

# Strong paragraph breaks — start a NEW PARAGRAPH
PARAGRAPH_STARTERS = [
    '所以', '但是', '而且', '不过', '然而', '因此', '于是',
    '首先', '其次', '最后', '另外', '此外', '当然', '其实', '总之',
    '那', '那么', '所以呢', '但是呢',
    '好', '来', '下面', '接下来', '好了', '行吧', '好吧',
    '第一', '第二', '第三', '第四', '第五',
    '换而言之', '换言之', '具体来说', '比如说', '举个例子', '比方说',
    '也就是说', '就是说', '换句话说',
    '还有一个', '还有呢', '还有一点',
    '再一个', '再就是', '再者', '再者说',
    '最后呢', '总的来说', '总结一下', '概括来说',
    '回到', '回过头来', '反过来说', '反过来讲',
]

# Sentence breaks — new sentence but same paragraph
SENTENCE_STARTERS = [
    '所以', '但是', '而且', '不过', '然而', '因此', '于是', '然后',
    '当然', '其实', '毕竟', '反正',
    '那', '这', '那么', '然后呢',
    '为什么', '什么', '怎么', '怎么样', '怎么办',
    '我', '你', '他', '她', '大家', '各位', '我们', '他们', '你们',
    '请问', '记得', '注意', '关键是', '重点是',
    '对吧', '对不对', '明白吗', '懂吗', '知道吗',
    '另外呢', '还有', '同时', '同样',
    '如果', '假如', '比如说', '比方讲',
    '因为', '所以呢', '但是呢',
    '你看', '你想', '大家想', '大家看',
    '接下来呢', '然后接下来',
    '这个', '那个',
    '其实呢', '事实上', '实际上',
    '可以说', '应该说',
    '我觉得', '我认为', '我的看法是',
    '坦白说', '说实话', '老实说', '说实在的',
    '当然啦', '自然',
    '另外呢', '再者说了',
]


def is_paragraph_start(line: str) -> bool:
    """Check if line starts a new paragraph (major topic shift)."""
    for starter in sorted(PARAGRAPH_STARTERS, key=len, reverse=True):
        if line.startswith(starter) and len(line) > len(starter) + 1:
            return True
    return False


def is_sentence_start(line: str) -> bool:
    """Check if line starts a new sentence (minor break)."""
    for starter in sorted(SENTENCE_STARTERS, key=len, reverse=True):
        if line.startswith(starter) and len(line) > len(starter) + 1:
            return True
    return False


def ends_with_punct(text: str) -> bool:
    """Check if text already ends with Chinese punctuation."""
    return bool(re.search(r'[。！？….」)】、，]', text[-1]))


def txt_to_speech(text: str) -> str:
    """
    Convert raw ASR transcript into structured speech manuscript.

    Returns markdown-formatted speech with:
    - Paragraphs separated by blank lines
    - Proper Chinese punctuation
    - All substantive content preserved
    """
    lines = [l.strip() for l in text.split('\n')]

    # ── Pass 1: Filter and join ─────────────────────────────────────
    clean_lines = []
    for s in lines:
        if not s:
            continue
        if s in PURE_FILLERS:
            continue
        if s in STANDALONE_FILLERS:
            continue
        # Remove lines that are just punctuation or single English chars
        if len(s) <= 1 and not re.search(r'[一-鿿]', s):
            continue
        clean_lines.append(s)

    if not clean_lines:
        return ''

    # ── Pass 2: Build paragraphs ────────────────────────────────────
    paragraphs = []  # list of list of sentences
    current_para = []  # current paragraph (list of sentences)
    current_sent = ''  # current sentence being built

    for line in clean_lines:
        # Check for paragraph break
        if current_sent and is_paragraph_start(line) and len(current_sent) > 15:
            # Close current sentence
            if not ends_with_punct(current_sent):
                current_sent += '。'
            current_para.append(current_sent)
            current_sent = line

            # Also close the paragraph if we have enough content
            para_text = ''.join(current_para)
            if len(para_text) > 150:
                paragraphs.append(current_para)
                current_para = []
            continue

        # Check for sentence break within paragraph
        if current_sent and is_sentence_start(line) and len(current_sent) > 12:
            # Close current sentence
            if not ends_with_punct(current_sent):
                current_sent += '。'
            current_para.append(current_sent)
            current_sent = line
            continue

        # Continuation — join with comma
        if current_sent:
            sep = '，' if not ends_with_punct(current_sent) else ''
            current_sent += sep + line
        else:
            current_sent = line

    # Drain remaining
    if current_sent:
        if not ends_with_punct(current_sent):
            current_sent += '。'
        current_para.append(current_sent)
    if current_para:
        paragraphs.append(current_para)

    # ── Pass 3: Join paragraphs and clean ───────────────────────────
    final_paragraphs = []
    for para_sentences in paragraphs:
        para_text = ''.join(para_sentences)
        para_text = para_text.strip()

        # Skip very short paragraphs
        if len(para_text) < 10:
            continue

        # Ensure paragraph ends with proper punctuation
        if not re.search(r'[。！？….」)】]', para_text[-1]):
            para_text += '。'

        # Clean up punctuation artifacts
        para_text = re.sub(r'，{2,}', '，', para_text)
        para_text = re.sub(r'。{2,}', '。', para_text)
        para_text = re.sub(r'、{2,}', '、', para_text)
        para_text = re.sub(r'，。', '。', para_text)
        para_text = re.sub(r'，，', '，', para_text)
        para_text = re.sub(r'。。', '。', para_text)
        # Remove comma immediately after period
        para_text = re.sub(r'。，', '。', para_text)

        # Strip laughter/interjections (pure vocal sounds, not content)
        for laugh in LAUGHTER_PATTERNS:
            para_text = para_text.replace(laugh, '')

        # Clean up any double punctuation left by laughter removal
        para_text = re.sub(r'，{2,}', '，', para_text)
        para_text = re.sub(r'。{2,}', '。', para_text)
        para_text = re.sub(r'，。', '。', para_text)
        para_text = re.sub(r'。，', '。', para_text)
        # Clean up leading/trailing/isolated punctuation
        para_text = para_text.strip('，。')
        para_text = re.sub(r'^[，。]', '', para_text)

        final_paragraphs.append(para_text)

    return '\n\n'.join(final_paragraphs)


# ─── Module configuration ──────────────────────────────────────────────
BASE = r'E:\BaiduNetdiskDownload\老梅面试'

MODULES = {
    '06': {
        'name': '面试红宝石',
        'txt_dir': os.path.join(BASE, '【06】老梅面试基础课【面试红宝石】', 'txt'),
        'output': '06-面试红宝石.md',
    },
    '07': {
        'name': '梅矛盾2.5',
        'txt_dir': os.path.join(BASE, '【07】老梅公考面试理论课【梅矛盾2.5版】', 'txt'),
        'output': '07-梅矛盾2.5.md',
    },
    '19': {
        'name': '梅矛盾1.0',
        'txt_dir': os.path.join(BASE, '【19】老梅梅矛盾面试理论1.0【完整版】', 'txt'),
        'output': '19-梅矛盾1.0.md',
    },
    '35': {
        'name': '面试刷题',
        'txt_dir': os.path.join(BASE, '【35】老梅面试刷题', 'txt'),
        'output': '35-面试刷题.md',
    },
}

# Module 10 sub-modules (from directory names)
MOD10_BASE = os.path.join(BASE, '【10】老梅的面试小礼包')
MOD10_SUB = {
    '典题精讲_态度观点': '10_典题精讲_态度观点.md',
    '典题精讲_模拟类': '10_典题精讲_模拟类.md',
    '典题精讲_矛盾类': '10_典题精讲_矛盾类.md',
    '典题精讲_社会现象': '10_典题精讲_社会现象.md',
    '典题精讲_组织管理': '10_典题精讲_组织管理.md',
    '梅矛盾发展理论': '10_梅矛盾发展理论.md',
    '热点解读': '10_热点解读.md',
    '经典文章解读': '10_经典文章解读.md',
}

OUTPUT_DIR = os.path.join(BASE, '讲话稿成品')


def process_module(name, txt_dir, output_file):
    """Process a single module: all TXTs → one MD with lecture sections."""
    if not os.path.isdir(txt_dir):
        print(f'  [SKIP] Directory not found: {txt_dir}')
        return None

    txt_files = sorted([
        f for f in os.listdir(txt_dir)
        if f.endswith('.txt') and not f.startswith('._')
    ])

    if not txt_files:
        print(f'  [SKIP] No TXT files in {txt_dir}')
        return None

    print(f'  Processing {len(txt_files)} TXT files...')

    sections = []
    for i, fname in enumerate(txt_files):
        fpath = os.path.join(txt_dir, fname)
        with open(fpath, 'r', encoding='utf-8', errors='replace') as f:
            raw = f.read()

        # Clean filename for section header
        clean_name = fname.replace('.txt', '').strip()
        # Remove leading numbers like "1.", "01.", "1、" etc
        clean_name = re.sub(r'^\d+[\.\、\s]+', '', clean_name)
        # Collapse whitespace
        clean_name = re.sub(r'\s+', '', clean_name)

        processed = txt_to_speech(raw)

        if processed:
            header = f'## {clean_name}\n\n'
            sections.append(header + processed)

        if (i + 1) % 10 == 0:
            print(f'    {i+1}/{len(txt_files)} done...')

    # Module header
    module_header = f'# {name}\n\n'
    full_text = module_header + '\n\n---\n\n'.join(sections)

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    out_path = os.path.join(OUTPUT_DIR, output_file)
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(full_text)

    size_kb = os.path.getsize(out_path) / 1024
    print(f'  → {output_file}: {len(sections)} lectures, {size_kb:.1f} KB')
    return len(sections)


def main():
    print('=' * 60)
    print('Processing 老梅面试 TXT → 讲话稿')
    print('=' * 60)

    total_lectures = 0

    # Process modules 06, 07, 19, 35
    for mod_id in ['06', '07', '19', '35']:
        mod = MODULES[mod_id]
        print(f'\n[{mod_id}] {mod["name"]}')
        count = process_module(mod['name'], mod['txt_dir'], mod['output'])
        if count:
            total_lectures += count

    # Process module 10 sub-modules — discover via os.walk()
    print(f'\n[10] 面试小礼包')
    mod10_count = 0

    # Discover all txt directories under MOD10_BASE
    mod10_txt_dirs = []
    for root, dirs, files in os.walk(MOD10_BASE):
        if os.path.basename(root) == 'txt':
            parent = os.path.dirname(root)  # dir containing txt/
            rel = os.path.relpath(parent, MOD10_BASE)  # e.g. '典题精讲\态度观点'
            mod10_txt_dirs.append((rel, root))

    # Sort for consistent output order
    mod10_txt_dirs.sort(key=lambda x: x[0])

    for rel, txt_dir in mod10_txt_dirs:
        # Build output filename: replace path separators with _
        safe_name = rel.replace('\\', '_').replace('/', '_')
        output_file = f'10_{safe_name}.md'

        print(f'  10/{rel}')
        count = process_module(safe_name.replace('_', '·'), txt_dir, output_file)
        if count:
            total_lectures += count
            mod10_count += count

    print(f'\n{"=" * 60}')
    print(f'TOTAL: {total_lectures} lectures processed')
    print(f'Output: {OUTPUT_DIR}')
    print(f'{"=" * 60}')


if __name__ == '__main__':
    main()
