# 索引系统经验总结

基于 2026-06-01 ~ 06-02 索引工具试错经验。

## 一、模板选择：\idx vs \index

| 命令 | 写入 .idx | 正文显示 | 适用场景 |
|------|----------|---------|---------|
| `\idx{key}` | `\index{key}` | **粗斜体 key** | 手动标注，需要正文高亮 |
| `\idx[disp]{key}` | `\index{key}` | **粗斜体 disp** | 复数/变形 |
| `\idxmath{sort}{display}` | `\index{sort@display}` | **粗斜体 display** | 数学符号 |
| `\idxsub{parent}{child}` | `\index{parent!child}` | 无 | L2 子条目 |
| `\index{key}` | `\index{key}` | **无** | 自动化插入 |

**关键结论**：自动化索引插入必须使用 `\index{}` 而非 `\idx{}`。`\idx` 会在正文渲染粗斜体文字，导致与原文重复显示。

## 二、排序键与大小写合并

### 问题
makeindex 对大小写敏感。"Field" 和 "field" 被当作两个不同条目。

### 解决
使用 `@` 语法分离排序键和显示文本：
```latex
\index{field@Field}       → 排序 "field"，显示 "Field"
\index{field@field}       → 排序 "field"，显示 "field"
```
两者在索引中合并为一条，排序键统一小写。

### 实现
```yaml
# config/default.yaml
templates:
  l1: "\\index{${key_lower}@${key}}"
```

```python
# engine.py — _build_cmd()
key_lower = key_sanitized.lower()
t.replace("${key_lower}", key_lower)
```

## 三、makeindex 样式文件 (.ist)

### 路径
编译时必须用 `-s` 指定：
```bash
makeindex -s Topology_by_Munkres.ist Topology_by_Munkres.idx
```

### 关键配置
```
headings_flag 1
heading_prefix "  \\lettergroup{"
heading_suffix "}\n"
symhead_positive ""        # 取消 Symbols 分组
symhead_negative ""        # 取消 numbers 分组
```

### 字母分组
`headings_flag 1` 自动创建 A-Z 字母标题。数学符号条目必须有字母排序键（如 `R@\(\mathbb{R}\)`），否则会落入空的符号分组。

## 四、索引条目生成中的陷阱

### 4.1 Python 转义问题
| 写法 | Python 解释 | 结果 |
|------|-----------|------|
| `"\\right"` | `\r` + `ight` = chr(13) + "ight" | 错误 |
| `r"\right"` | 字面量 `\right` | 正确 |
| `chr(92) + "right"` | 字面量 `\right` | 正确 |

**方案**：所有包含 LaTeX 反斜杠的字符串统一使用 `chr(92)`。

### 4.2 fragile 命令
`\left`、`\right`、`\(`、`\)` 在 `\index{}` 中会被 LaTeX 展开为底层原语（`\setbox`、`\mathaccent`），导致 makeindex 拒绝。

**方案**：引擎 `_sanitize_display()` 自动剥离 `\left`/`\right`/`\lbrack`/`\rbrack`，将 `\(`/`\)` 转换为 `$`。

### 4.3 安全移除规则
`\left`/`\right` 只删除紧跟**非字母字符**的（分隔符），保留 `\rightarrow`、`\leftarrow` 等完整命令。
```python
for prefix in ['left', 'right']:
    # 只在后面跟非字母字符时才移除
    if next_char_is_not_alpha:
        remove(prefix)
```

### 4.4 `\idxmath` 双参数转换
`\idxmath{sort}{display}` 两个参数，转 `\index` 时需合并为 `\index{sort@display}`：
```python
c.replace('\\idxmath{', '\\index{')
# 然后修复双参数：\index{sort}{display} → \index{sort@display}
```

### 4.5 `is_inside_index` 覆盖范围
原始函数仅检查 `\index{...}`，未覆盖 `\idx{}`、`\idx[display]{key}`、`\idxmath{}{}`、`\idxsub{}{}`。已重写为全面覆盖。

### 4.6 引擎搜索安全性
数学条目（带 `sort_key`）的搜索路径使用了 `content.find()` 直接查找，绕过了 `is_inside_command_arg` 和 `is_inside_index` 检查。已修复为使用 `_find_text()`。

## 五、已验证的完整工作流

```bash
# 1. 从干净源文件开始
git checkout <commit-hash> -- chapters/

# 2. 运行索引插入
cd latex-index-tool
python -m latex_index insert --config config/default.yaml --chapter 1 --entries data/ch01_entries.json

# 3. 后处理
#    - \idx/\idxmath/\idxsub → \index
#    - 双参数修复（\index{sort}{display} → \index{sort@display}）
#    - 安全移除 \left/\right（非字母后）
#    - 补充字母排序键

# 4. 编译
rm -f *.aux *.idx *.ilg *.ind *.toc
xelatex Topology_by_Munkres.tex
makeindex -s Topology_by_Munkres.ist Topology_by_Munkres.idx
xelatex Topology_by_Munkres.tex
xelatex Topology_by_Munkres.tex
```

## 六、最终状态

| 指标 | 值 |
|------|:---:|
| 索引条目 | 1448 |
| makeindex 拒绝 | 0 |
| 字母标题 | A-Z（25/26） |
| 大小写碰撞 | 0 |
| LaTeX 错误 | 2（非致命） |
| PDF 页数 | 611 |
