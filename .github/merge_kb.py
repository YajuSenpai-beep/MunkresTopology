#!/usr/bin/env python3
"""
Merge all 200 enriched MD notes into a consolidated knowledge base.
Output: 10 well-organized MD files.
"""

import os, re, sys

BASE = r"E:\BaiduNetdiskDownload\老梅面试"
OUT = r"E:\BaiduNetdiskDownload\老梅面试\面试知识库"

# Category definitions
CATEGORIES = {
    "00_梅矛盾体系总纲": {
        "desc": "核心理论框架：梅矛盾体系、挖矿论、四要素分析、备考策略",
        "files": [],
    },
    "01_社会现象类": {
        "desc": "社会现象类题目的理论、分析方法、答题框架与完整示范",
        "files": [],
    },
    "02_态度观点类": {
        "desc": "态度观点类题目的理论、分析方法、答题框架与完整示范",
        "files": [],
    },
    "03_组织管理类": {
        "desc": "组织管理/组织流程类题目的理论、分析方法、答题框架与完整示范",
        "files": [],
    },
    "04_矛盾类": {
        "desc": "矛盾类题目的理论、分析方法、答题框架与完整示范",
        "files": [],
    },
    "05_情景模拟类": {
        "desc": "情景模拟/人际关系类题目的理论、分析方法、答题框架与完整示范",
        "files": [],
    },
    "06_答题工具箱": {
        "desc": "所有课程中提取的行动工具箱、操作步骤、自查清单",
        "files": [],
    },
    "07_关键话术速查": {
        "desc": "所有课程中提取的可直接套用的表述模板和金句",
        "files": [],
    },
    "08_案例素材库": {
        "desc": "所有课程中引用的真题、新闻、故事等素材",
        "files": [],
    },
    "09_面试热点与文章": {
        "desc": "热点解读、经典文章分析、时政素材",
        "files": [],
    },
}

# === FILE CATEGORIZATION RULES ===

def categorize(md_path):
    """Determine which category a file belongs to."""
    path = md_path.lower()
    fname = os.path.basename(md_path)
    parent = os.path.basename(os.path.dirname(os.path.dirname(md_path)))

    # 【06】面试红宝石 - all basic theory -> 00
    if '【06】' in path or '面试红宝石' in path:
        return "00_梅矛盾体系总纲"

    # 【07】梅矛盾2.5 - distributed by topic
    if '【07】' in path or '梅矛盾2.5' in path:
        if '社会现象' in fname or '社会现象' in path:
            return "01_社会现象类"
        if '态度观点' in fname or '态度观点' in path:
            return "02_态度观点类"
        if '组织' in fname or '组织' in path:
            return "03_组织管理类"
        if '矛盾' in fname and '社会现象' not in fname:
            return "04_矛盾类"
        if '模拟' in fname or '模拟' in path:
            return "05_情景模拟类"
        return "00_梅矛盾体系总纲"  # default for 07

    # 【19】梅矛盾1.0 - distributed by title
    if '【19】' in path or '梅矛盾1.0' in path:
        if '社会现象' in fname:
            return "01_社会现象类"
        if '态度观点' in fname:
            return "02_态度观点类"
        if '组织' in fname and '情景' not in fname:
            return "03_组织管理类"
        if '矛盾类' in fname or ('矛盾' in fname and '四要素' not in fname and '总纲' not in fname):
            return "04_矛盾类"
        if '情景模拟' in fname or '模拟' in fname:
            return "05_情景模拟类"
        return "00_梅矛盾体系总纲"

    # 【10】面试小礼包 - by subdirectory
    if '【10】' in path:
        if '社会现象' in path:
            return "01_社会现象类"
        if '态度观点' in path:
            return "02_态度观点类"
        if '组织管理' in path or '组织类' in path:
            return "03_组织管理类"
        if '矛盾类' in path:
            return "04_矛盾类"
        if '模拟类' in path:
            return "05_情景模拟类"
        if '梅矛盾发展理论' in path:
            return "00_梅矛盾体系总纲"
        if '热点解读' in path:
            return "09_面试热点与文章"
        if '经典文章' in path:
            return "09_面试热点与文章"
        return "09_面试热点与文章"

    # 【35】面试刷题 - distributed by title keywords
    if '【35】' in path or '刷题' in path:
        # Parse title for topic
        if any(kw in fname for kw in ['社会现象', '社会现实']):
            return "01_社会现象类"
        if any(kw in fname for kw in ['态度观点', '寓言', '观点']):
            return "02_态度观点类"
        if any(kw in fname for kw in ['组织流程', '组织类', '目的导向', '读题', '明确目的', '明确身份', '读潜台词', '抬杠找亮点', '调研']):
            return "03_组织管理类"
        if any(kw in fname for kw in ['矛盾分析', '矛盾类', '虚假矛盾', '矛盾化解', '整体性思维', '三种矛盾', '锚定重点', '桥分析']):
            return "04_矛盾类"
        if any(kw in fname for kw in ['情景模拟', '模拟类', '价值排序', '融合答题', '直接否定', '劝谁', '倾向性', '沟通', '醉翁之意']):
            return "05_情景模拟类"
        if any(kw in fname for kw in ['信息定位', '分析方法', '并列分析', '细节把握', '专项答疑', '好差评']):
            return "00_梅矛盾体系总纲"
        return "00_梅矛盾体系总纲"

    return "00_梅矛盾体系总纲"


# === MERGE LOGIC ===

def merge_category(cat_name, cat_info, all_files):
    """Merge all files in a category into one MD."""
    if not all_files:
        return None

    out_path = os.path.join(OUT, f"{cat_name}.md")

    # Sort: theory first, then practice
    theory_files = [f for f in all_files if '【06】' in f or '【07】' in f or '【19】' in f]
    practice_files = [f for f in all_files if f not in theory_files]

    all_sorted = theory_files + practice_files

    sections = []
    sections.append(f"# {cat_name.replace('00_','').replace('01_','').replace('02_','').replace('03_','').replace('04_','').replace('05_','').replace('06_','').replace('07_','').replace('08_','').replace('09_','')}\n")
    sections.append(f"> {cat_info['desc']}\n")
    sections.append(f"> 共 {len(all_sorted)} 篇笔记合并\n")
    sections.append("\n---\n")

    # Table of contents (plain text, no broken links)
    sections.append("\n## 目录\n")
    for i, f in enumerate(all_sorted):
        fname = os.path.basename(f).replace('.md', '')
        content = open(f, encoding='utf-8').read()
        theme_match = re.search(r'##\s*.*?核心主题\s*\n+(.+)', content)
        theme = theme_match.group(1).strip()[:80] if theme_match else fname[:60]
        sections.append(f"{i+1}. **{fname}** — {theme}")
    sections.append("\n---\n")

    # Content
    for i, f in enumerate(all_sorted):
        content = open(f, encoding='utf-8').read()

        # Clean up: remove the original H1 if exists
        content = re.sub(r'^# .+\n', '', content)

        # Demote all headings by one level so Outline shows proper hierarchy:
        #   H1 = document title
        #   H2 = section titles (each note)
        #   H3 = sub-sections (核心主题, 关键概念, 答题示范...)
        #   H4 = deeper sections (公式与定理, 推导过程...)
        content = re.sub(r'^#### ', '##### ', content, flags=re.MULTILINE)
        content = re.sub(r'^### ', '#### ', content, flags=re.MULTILINE)
        content = re.sub(r'^## ', '### ', content, flags=re.MULTILINE)

        rel_path = f.replace(BASE, '').replace('\\', '/')
        dir_name = rel_path.split('/')[1] if len(rel_path.split('/')) > 1 else ''
        fname = os.path.basename(f).replace('.md', '')

        # Section title as H2 (shows as top-level in Outline)
        sections.append(f'\n## {fname}\n')
        sections.append(f"> 来源: {dir_name}\n")
        sections.append(content)
        sections.append("\n---\n")

    merged = '\n'.join(sections)

    os.makedirs(OUT, exist_ok=True)
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(merged)

    return out_path


def build_toolkit_section():
    """Extract all '行动工具箱' sections from all MDs."""
    toolkits = []
    for root, dirs, files in os.walk(BASE):
        if OUT in root: continue
        for f in files:
            if not f.endswith('.md'): continue
            md_path = os.path.join(root, f)
            content = open(md_path, encoding='utf-8').read()

            # Extract 行动工具箱 section
            toolkit_match = re.search(r'##\s*🛠️\s*行动工具箱\s*\n(.*?)(?=##\s|\Z)', content, re.DOTALL)
            if toolkit_match:
                toolkit_text = toolkit_match.group(1).strip()
                if len(toolkit_text) > 50:
                    # Get source name
                    fname = f.replace('.md', '')
                    dir_name = os.path.basename(os.path.dirname(os.path.dirname(md_path)))
                    toolkits.append((fname, dir_name, toolkit_text))

    return toolkits


def build_expression_collection():
    """Extract all '关键话术' sections from all MDs."""
    expressions = []
    for root, dirs, files in os.walk(BASE):
        if OUT in root: continue
        for f in files:
            if not f.endswith('.md'): continue
            md_path = os.path.join(root, f)
            content = open(md_path, encoding='utf-8').read()

            expr_match = re.search(r'##\s*💬\s*关键话术\s*\n(.*?)(?=##\s|\Z)', content, re.DOTALL)
            if expr_match:
                expr_text = expr_match.group(1).strip()
                if len(expr_text) > 30:
                    fname = f.replace('.md', '')
                    dir_name = os.path.basename(os.path.dirname(os.path.dirname(md_path)))
                    expressions.append((fname, dir_name, expr_text))

    return expressions


def build_example_collection():
    """Extract all '案例素材' sections from all MDs."""
    examples = []
    for root, dirs, files in os.walk(BASE):
        if OUT in root: continue
        for f in files:
            if not f.endswith('.md'): continue
            md_path = os.path.join(root, f)
            content = open(md_path, encoding='utf-8').read()

            ex_match = re.search(r'##\s*📖\s*案例素材\s*\n(.*?)(?=##\s|\Z)', content, re.DOTALL)
            if ex_match:
                ex_text = ex_match.group(1).strip()
                if len(ex_text) > 30:
                    fname = f.replace('.md', '')
                    dir_name = os.path.basename(os.path.dirname(os.path.dirname(md_path)))
                    examples.append((fname, dir_name, ex_text))

    return examples


# === MAIN ===

if __name__ == '__main__':
    print("Categorizing 200 MD files...")

    # Step 1: Collect all MDs and categorize
    for root, dirs, files in os.walk(BASE):
        if OUT in root:
            continue
        for f in files:
            if not f.endswith('.md'):
                continue
            md_path = os.path.join(root, f)
            cat = categorize(md_path)
            CATEGORIES[cat]["files"].append(md_path)

    # Print categorization summary
    for cat_name in sorted(CATEGORIES.keys()):
        n = len(CATEGORIES[cat_name]["files"])
        print(f"  {cat_name}: {n} files")

    print(f"\nMerging into: {OUT}")

    # Step 2: Merge categories 00-05 (by type)
    for cat_name in sorted(CATEGORIES.keys()):
        if cat_name in ["06_答题工具箱", "07_关键话术速查", "08_案例素材库"]:
            continue  # handled separately
        files = CATEGORIES[cat_name]["files"]
        out_path = merge_category(cat_name, CATEGORIES[cat_name], files)
        if out_path:
            size_kb = os.path.getsize(out_path) / 1024
            print(f"  -> {cat_name}.md ({size_kb:.0f} KB, {len(files)} files)")

    # Step 3: Build toolkit, expressions, examples collections
    print("\nBuilding quick-reference collections...")

    # 06 - Action Toolkits
    toolkits = build_toolkit_section()
    if toolkits:
        out = os.path.join(OUT, "06_答题工具箱.md")
        content = []
        content.append("# 答题工具箱\n")
        content.append(f"> 从 {len(toolkits)} 篇笔记中提取的所有行动工具箱、操作步骤、自查清单\n")
        content.append("\n---\n")
        for fname, dir_name, text in toolkits:
            content.append(f"## {fname}\n")
            content.append(f"> 来源: {dir_name}\n\n")
            content.append(text)
            content.append("\n\n---\n")
        with open(out, 'w', encoding='utf-8') as f:
            f.write('\n'.join(content))
        print(f"  -> 06_答题工具箱.md ({os.path.getsize(out)/1024:.0f} KB, {len(toolkits)} entries)")

    # 07 - Key Expressions
    expressions = build_expression_collection()
    if expressions:
        out = os.path.join(OUT, "07_关键话术速查.md")
        content = []
        content.append("# 关键话术速查\n")
        content.append(f"> 从 {len(expressions)} 篇笔记中提取的可直接套用的表述模板和金句\n")
        content.append("\n---\n")
        for fname, dir_name, text in expressions:
            content.append(f"## {fname}\n")
            content.append(f"> 来源: {dir_name}\n\n")
            content.append(text)
            content.append("\n\n---\n")
        with open(out, 'w', encoding='utf-8') as f:
            f.write('\n'.join(content))
        print(f"  -> 07_关键话术速查.md ({os.path.getsize(out)/1024:.0f} KB, {len(expressions)} entries)")

    # 08 - Example Collection
    examples = build_example_collection()
    if examples:
        out = os.path.join(OUT, "08_案例素材库.md")
        content = []
        content.append("# 案例素材库\n")
        content.append(f"> 从 {len(examples)} 篇笔记中提取的真题、新闻、故事等素材\n")
        content.append("\n---\n")
        for fname, dir_name, text in examples:
            content.append(f"## {fname}\n")
            content.append(f"> 来源: {dir_name}\n\n")
            content.append(text)
            content.append("\n\n---\n")
        with open(out, 'w', encoding='utf-8') as f:
            f.write('\n'.join(content))
        print(f"  -> 08_案例素材库.md ({os.path.getsize(out)/1024:.0f} KB, {len(examples)} entries)")

    print("\nDone! Knowledge base created at:")
    print(f"  {OUT}")
    for f in sorted(os.listdir(OUT)):
        size = os.path.getsize(os.path.join(OUT, f)) / 1024
        print(f"    {f} ({size:.0f} KB)")
