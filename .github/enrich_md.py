#!/usr/bin/env python3
"""
V2: Aggressive enrichment - extracts substantial content from TXT transcripts.
Outputs richer, more readable sections appended to MD notes.
"""

import os, re, sys

def extract_model_answer(lines):
    """Extract the teacher's model answer - use broader heuristics."""
    start_markers = [
        '各位考官', '考生开始答题', '考生思考完毕', '下面考生',
        '我来答', '给大家答', '示范一下', '演示一下',
        '下面我来', '下面我给', '我来给大家答', '试着答',
        '我答一遍', '我们来答', '开始答题', '先来答题',
        '回答一下', '答一下这道',
    ]
    end_markers = [
        '答题完毕', '回答完毕', '考生回答完毕',
        '以上就是', '这道题就这样', '这道题就答',
        '好，这道题', 'OK这道', '这就是这道题',
        '这是我的看法', '以上就是我的', '这道题答',
    ]

    candidates = []
    for i, line in enumerate(lines):
        stripped = line.strip()
        if len(stripped) < 5: continue
        for m in start_markers:
            if m in stripped:
                end_i = min(i + 80, len(lines))
                for j in range(i+1, end_i):
                    for em in end_markers:
                        if em in lines[j].strip():
                            end_i = j + 1
                            break
                    else:
                        continue
                    break
                chunk = '\n'.join(lines[i:end_i])
                if len(chunk) > 150:
                    candidates.append(chunk)
                break

    # Fallback: for practice questions, the latter half is usually the answer
    if not candidates and len(lines) > 100:
        mid = len(lines) * 3 // 5  # Start from 60% mark
        end = len(lines) - 3
        chunk = '\n'.join(lines[mid:end])
        if len(chunk) > 500:
            candidates.append(chunk)

    # Also try: capture from "这道题" to the end of substantive content
    if not candidates and len(lines) > 50:
        for i, line in enumerate(lines):
            if re.search(r'(?:这道题|这个题目|我们来看)', line) and i > len(lines) * 0.3:
                chunk = '\n'.join(lines[i:len(lines)-3])
                if len(chunk) > 400:
                    candidates.append(chunk)
                break

    if candidates:
        candidates.sort(key=len, reverse=True)
        result = candidates[0]
        # Keep more content (up to 6000 chars)
        if len(result) > 6000:
            result = result[:6000] + "\n\n...(完整答题请参考TXT原文)"
        return result
    return ""


def extract_key_expressions(lines):
    """Extract reusable expressions with surrounding context."""
    expressions = []

    for i, line in enumerate(lines):
        stripped = line.strip()
        if len(stripped) < 15 or len(stripped) > 200:
            continue

        # Lines that look like teaching/advice
        score = 0
        if re.search(r'(?:要|不要|必须|注意|关键|核心|重点|记住)', stripped): score += 1
        if re.search(r'(?:目的|手段|矛盾|结果|分析|思考|答题)', stripped): score += 1
        if re.search(r'(?:不是.{3,30}而是|与其.{3,20}不如|宁可.{3,20}也不)', stripped): score += 2
        if re.search(r'(?:你可以|建议大家|各位|考官|亮点|加分|高分|低分)', stripped): score += 1

        if score >= 2:
            expressions.append(stripped)

    # Deduplicate by similarity
    seen = set()
    unique = []
    for e in expressions:
        key = e[:40]
        if key not in seen:
            seen.add(key)
            unique.append(e)

    return unique[:20]


def extract_examples(lines):
    """Extract examples and stories with full context."""
    examples = []
    buffer = []
    in_example = False

    example_triggers = ['比如', '例如', '举个例子', '好比', '就像', '假设', '想象一下',
        '真题', '这道真题', '有一道题', '之前有一道']

    for line in lines:
        stripped = line.strip()

        if any(t in stripped for t in example_triggers) and len(stripped) > 15:
            if buffer:
                examples.append('\n'.join(buffer))
            buffer = [stripped]
            in_example = True
        elif in_example:
            if len(stripped) > 10:
                buffer.append(stripped)
                if len(buffer) > 12:  # Max 12 lines per example
                    examples.append('\n'.join(buffer))
                    buffer = []
                    in_example = False
            else:
                if buffer:
                    examples.append('\n'.join(buffer))
                buffer = []
                in_example = False

    if buffer:
        examples.append('\n'.join(buffer))

    # Filter: keep substantial ones only
    good = [e for e in examples if len(e) > 50]

    # Deduplicate and limit
    seen = set()
    unique = []
    for e in good:
        key = e[:60]
        if key not in seen:
            seen.add(key)
            unique.append(e)

    return unique[:15]


def extract_operation_walkthrough(lines):
    """Extract step-by-step analysis walkthrough."""
    walkthroughs = []

    # Find sections with sequential thinking
    for i, line in enumerate(lines):
        stripped = line.strip()
        if not stripped: continue

        # Detect procedural language
        is_procedure = False
        if re.search(r'(?:第一步|第二步|第三步|首先.*然后|先.*再.*最后)', stripped):
            is_procedure = True
        if re.search(r'(?:拿到题|看到题|审题|破题|读完题)', stripped) and len(stripped) > 20:
            is_procedure = True

        if is_procedure:
            end = min(i + 35, len(lines))
            chunk = '\n'.join(lines[i:end])
            step_count = len(re.findall(
                r'(?:第[一二三四五六七八九\d]+步|首先|然后|其次|接着|最后|再|之后|接下来|第一步)',
                chunk))
            if step_count >= 2 and len(chunk) > 200:
                walkthroughs.append(chunk)
                break  # Just take the first good one

    # Fallback: look for thinking-out-loud sections
    if not walkthroughs:
        for i, line in enumerate(lines):
            if re.search(r'(?:怎么分析|如何分析|怎么思考|我是怎么)', line):
                chunk = '\n'.join(lines[i:min(i+25, len(lines))])
                if len(chunk) > 150:
                    walkthroughs.append(chunk)
                    break

    return walkthroughs[:2]


def enrich_md(txt_path, md_path):
    """Main function: read TXT, extract content, append to MD."""
    with open(txt_path, encoding='utf-8') as f:
        txt = f.read()
    with open(md_path, encoding='utf-8') as f:
        md = f.read()

    if '答题示范' in md:
        # Check if already has substantial content
        parts = md.split('答题示范')
        if len(parts) > 1 and len(parts[1].strip()) > 200:
            return None, "already enriched"

    lines = txt.split('\n')

    model_answer = extract_model_answer(lines)
    key_exprs = extract_key_expressions(lines)
    examples = extract_examples(lines)
    walkthroughs = extract_operation_walkthrough(lines)

    new_sections = []

    if model_answer and len(model_answer) > 200:
        if len(model_answer) > 6000:
            model_answer = model_answer[:6000] + "\n\n---\n*(完整答题请参考TXT原文)*"
        new_sections.append(("🎙️ 答题示范", model_answer.strip()))

    if key_exprs:
        expr_lines = []
        for e in key_exprs:
            expr_lines.append(f"- {e}")
        new_sections.append(("💬 关键话术", '\n'.join(expr_lines)))

    if examples:
        ex_lines = []
        for e in examples:
            # Truncate very long examples
            text = e if len(e) < 500 else e[:500] + "..."
            ex_lines.append(f"- {text}")
        new_sections.append(("📖 案例素材", '\n'.join(ex_lines)))

    if walkthroughs:
        wt_content = '\n\n'.join(w[:2000] for w in walkthroughs)
        new_sections.append(("🔍 操作实录", wt_content))

    if not new_sections:
        return None, "nothing to extract"

    # Append to MD with proper formatting
    enriched = md.rstrip()
    for emoji_title, content in new_sections:
        enriched += f"\n\n## {emoji_title}\n\n{content}"
    enriched += '\n'

    with open(md_path, 'w', encoding='utf-8') as f:
        f.write(enriched)

    return [t for t, _ in new_sections], "ok"


if __name__ == '__main__':
    if len(sys.argv) == 3:
        txt_path, md_path = sys.argv[1], sys.argv[2]
        result, status = enrich_md(txt_path, md_path)
        print(f"Status: {status}")
        if result:
            print(f"Added: {result}")
    else:
        print("Usage: enrich_md.py <txt_path> <md_path>")
