import os, re, shutil

BASE = r"E:\BaiduNetdiskDownload\老梅面试\【10】老梅的面试小礼包"
OUT = r"E:\BaiduNetdiskDownload\老梅面试\面试知识库\10_面试小礼包"

section_types = ['核心主题','关键概念','核心观点','核心原理','常见误区','关联知识','行动工具箱','课后练习','答题示范']
remove_sections = ['操作实录','关键话术','案例素材']
os.makedirs(OUT, exist_ok=True)

stats = {'cleaned': 0, 'copied_docs': 0}

for root, dirs, files in os.walk(BASE):
    # Skip existing md笔记/笔记 dirs for file collection, handle them separately
    if 'md笔记' in root or '笔记' in root:
        continue

    rel = os.path.relpath(root, BASE)
    out_dir = os.path.join(OUT, rel) if rel != '.' else OUT

    for f in files:
        fpath = os.path.join(root, f)

        # Copy docx/pdf files
        if f.endswith(('.docx', '.pdf')):
            os.makedirs(out_dir, exist_ok=True)
            shutil.copy2(fpath, os.path.join(out_dir, f))
            stats['copied_docs'] += 1
            continue

        # Find matching MD
        if f.endswith('.txt'):
            md_name = f.replace('.txt', '.md')
            md_candidates = [
                os.path.join(root, 'md笔记', md_name),
                os.path.join(root, '笔记', md_name),
            ]
            md_path = None
            for c in md_candidates:
                if os.path.exists(c):
                    md_path = c
                    break

            if not md_path:
                continue

            # Process MD
            content = open(md_path, encoding='utf-8').read()

            # Split into sections
            raw_sections = []
            cur_title = ''
            cur_body = []
            for line in content.split('\n'):
                if re.match(r'^##\s+', line):
                    if cur_body:
                        raw_sections.append((cur_title.strip(), '\n'.join(cur_body).strip()))
                    cur_title = line.strip()
                    cur_body = []
                else:
                    cur_body.append(line)
            if cur_body:
                raw_sections.append((cur_title.strip(), '\n'.join(cur_body).strip()))

            # Keep last of each type, filter unwanted
            kept = {}
            for title, body in raw_sections:
                if any(s in title for s in remove_sections):
                    continue
                matched = None
                for t in section_types:
                    if t in title:
                        matched = t
                        break
                if matched:
                    kept[matched] = (title, body)
                elif title:
                    kept[title] = (title, body)

            # Build output
            fname = f.replace('.txt', '').strip()
            out_lines = [f"# {fname}\n", f"> 来源：【10】老梅的面试小礼包 / {rel}\n"]

            for stype in section_types:
                if stype in kept:
                    title, body = kept[stype]
                    new_title = '### ' + title.replace('## ', '')
                    out_lines.append(f"\n{new_title}\n")
                    body = re.sub(r'^#### ', '##### ', body, flags=re.MULTILINE)
                    body = re.sub(r'^### ', '#### ', body, flags=re.MULTILINE)
                    body = re.sub(r'^## ', '### ', body, flags=re.MULTILINE)
                    out_lines.append(body)

            for stype, (title, body) in kept.items():
                if stype not in section_types:
                    new_title = '### ' + title.replace('## ', '')
                    out_lines.append(f"\n{new_title}\n")
                    out_lines.append(body)

            os.makedirs(out_dir, exist_ok=True)
            out_path = os.path.join(out_dir, md_name)
            with open(out_path, 'w', encoding='utf-8') as fout:
                fout.write('\n'.join(out_lines))

            stats['cleaned'] += 1

print(f"Cleaned {stats['cleaned']} MD files")
print(f"Copied {stats['copied_docs']} docx/pdf files")

# Print summary by directory
print("\nOutput structure:")
for root, dirs, files in os.walk(OUT):
    md_count = sum(1 for f in files if f.endswith('.md'))
    other = [f for f in files if not f.endswith('.md')]
    if md_count > 0 or other:
        rel = os.path.relpath(root, OUT)
        info = f"  {rel}: {md_count} MDs"
        if other:
            info += f", {len(other)} docs"
        print(info)
