# latex-index-tool 端到端教学脚本

配合 [asciinema](https://asciinema.org) 录制使用。

---

## 场景：从 OCR 索引文本到最终 PDF 索引

### 准备工作

```bash
# 安装工具
pip install latex-index-tool[tui,progress]

# 项目结构
tree -L 2
# chapters/
#   Chapter_1_Introduction.tex
#   Chapter_2_Basics.tex
#   ...
# index/
#   data/           (索引条目 JSON)
#   config/         (配置文件)
```

### 第一步：扫描 OCR 索引文本

```bash
# 假设你有一个从 PDF OCR 提取的索引文本
cat raw_index.txt

# 运行解析器
latex-index parse raw_index.txt --format indented -o entries.json

# 查看结构化结果
head -30 entries.json
```

### 第二步：查看配置

```bash
# 查看模板配置
cat config/default.yaml

# 可选：自定义模板
# 编辑 config/default.yaml 修改 templates 部分
```

### 第三步：预览插入（Dry Run）

```bash
# 查看第 1 章将插入哪些索引
latex-index insert --chapter 1 --dry-run --progress

# 交互式预览（Rich TUI）
latex-index insert --chapter 1 --dry-run --interactive --tui
```

### 第四步：正式插入

```bash
# 备份原文件
latex-index rollback chapters/Chapter_1.tex --list

# 正式插入索引
latex-index insert --chapter 1 --progress
```

### 第五步：生成分析报告

```bash
# 检查覆盖率和重复
latex-index report chapters/Chapter_1.tex \
    --entries data/ch01_entries.json \
    -o report.txt

cat report.txt
```

### 第六步：生成 xindy 排序规则

```bash
# 为中文索引生成拼音排序
latex-index xindy \
    --languages english chinese-pinyin \
    -o index_style.xdy
```

### 第七步：编译验证

```bash
# 设置 latexmk 集成
latex-index setup

# 编译
xelatex main.tex
makeindex main.idx -s index_style.xdy
xelatex main.tex

# 查看 PDF 中的索引
```

### 第八步：批量处理所有章节

```bash
# 使用批处理工具
latex-index tools convert-exercises --chapter 2
latex-index tools clean-ex-envs
latex-index tools scan-issues --chapter 1

# 或使用循环
for ch in $(seq 1 14); do
    latex-index insert --chapter $ch
done
```

### 第九步：回滚（如果需要）

```bash
# 查看备份
latex-index rollback --list chapters/Chapter_1.tex

# 恢复
latex-index rollback chapters/Chapter_1.tex
```

---

## 录制命令

```bash
# 安装 asciinema
pip install asciinema

# 录制
asciinema rec latex-index-demo.cast \
    -c "bash docs/TUTORIAL.sh"

# 播放
asciinema play latex-index-demo.cast
```
