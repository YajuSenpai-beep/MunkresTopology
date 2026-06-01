# 索引精修笔记

基于 2026-06-02 对编译版索引的逐条修复经验。

## 一、修复流程（4 步）

```bash
# 1. 编译生成 idx
xelatex -interaction=nonstopmode Topology_by_Munkres.tex

# 2. makeindex（必须带 -s 指定样式文件）
makeindex -s Topology_by_Munkres.ist Topology_by_Munkres.idx

# 3. 后处理 .ind（合并重复 + 重分配符号 + 首字母大写）
python latex-index-tool/_fix_ind.py

# 4. 最终编译
xelatex -interaction=nonstopmode Topology_by_Munkres.tex
xelatex -interaction=nonstopmode Topology_by_Munkres.tex
```

## 二、关键工具

### `_fix_ind.py`
位置：`latex-index-tool/_fix_ind.py`
功能三合一：
1. 合并大小写重复条目（合并页码）
2. 重分配 Symbol 分组条目到对应字母分组
3. 首字母大写（跳过数学符号）

### `_postfix.py`
位置：`latex-index-tool/_postfix.py`  
功能：`\idx`/`\idxmath`/`\idxsub` → `\index` 转换 + 双参数修复

## 三、常见问题类型与修复方法

### 3.1 大小写重复（如 Antipode 出现 3 次）

**原因**：预存条目使用 `\idx{Antipode}`，引擎新增条目使用 `\index{antipode@Antipode}`。排序键不同导致 makeindex 输出两条。

**修复**：`_fix_ind.py` 自动合并。关键行：
```python
clean = clean.strip().rstrip(", ").lower()  # 注意：rstrip(", ") 不是 rstrip(",")
```
**教训**：`rstrip(",")` 不能去除逗号后的空格，必须用 `rstrip(", ")`。

### 3.2 数学符号在 Symbol 分组（如 \(\mathbb{R}\)）

**原因**：makeindex 将非字母开头的条目放入 Symbols 组。即使排序键是 "R"，`.ist` 中的 `symhead_positive` 仍生效。

**修复**：
1. `.ist` 中设置 `symhead_positive ""` 和 `symhead_negative ""`
2. `_fix_ind.py` 中通过 `letter_map` 将符号条目重分配到对应字母分组

```python
letter_map = {
    "mathbb{R}": "R", "{B}^{n}": "B", "{S}^{1}": "S",
    "2-cell": "T", "2-manifold": "T",
}
```

### 3.3 缺少子条目（L2 缺失）

**根因分类**：

| 类型 | 示例 | 原因 |
|------|------|------|
| 措辞不同 | 数据 "accumulation point of **a** net" vs tex "of **the** net" | 一词之差，精确匹配失败 |
| 词性不同 | 数据 "independence of path" vs tex "independent of path" | 名词 vs 形容词 |
| 多了冠词 | 数据 "is isomorphism" vs tex "is **an** isomorphism" | 引擎找不到精确短语 |
| 处在数学禁区 | tex 中文字在 `\(...\)` 附近，`find_math_ranges` 误覆盖 | 引擎的 `_is_forbidden` 返回 True |

**修复**：手动在 tex 中找到对应文字，插入 `\index{}` 命令。

**示例 1**：accumulation point of a net
```latex
% 原 tex：we say that x is an accumulation point of the net
% 修复后：
we say that \(x\) is an \index{Accumulation point of a net}accumulation point of the net
```

**示例 2**：Axiom of choice 子条目
```latex
% vs. well-ordering theorem
One such is the well-ordering theorem\index{Axiom of choice!vs. well-ordering theorem}

% vs. nonemptiness of product  
... is not empty\index{Axiom of choice!vs. nonemptiness of product}.
```

**示例 3**：alpha_hat 子条目
```latex
% independent of path
\index{alpha@\widehat{\alpha}!independent of path}is independent of path

% is an isomorphism
\index{alpha@\widehat{\alpha}!is an isomorphism}is an isomorphism
```

### 3.4 .ist 文件注意事项

```
headings_flag 1                    # 必须，开启字母分组
heading_prefix "  \\lettergroup{"  # 分组标题前缀
heading_suffix "}\n"              # 分组标题后缀
symhead_positive ""               # 空字符串，取消 Symbols 组
symhead_negative ""               # 空字符串，取消 numbers 组
```

**关键**：makeindex 必须用 `-s` 参数指定 .ist 文件。

## 四、已手动修复条目清单

| 条目 | 位置 | 修复方式 |
|------|------|---------|
| Accumulation point of a net | Ch3 L1539 | 手动加 `\index{}` |
| Absolute retract!vs. universal extension property | Ch4 | 改 L1→L2，加 vs. 前缀 |
| Adjoining a 2-cell!effect on fundamental group | Ch11 | 手动加 `\index{}` |
| \(\widehat{\alpha}\)!independent of path | Ch9 | 手动加 `\index{}`（含 sort key） |
| \(\widehat{\alpha}\)!is an isomorphism | Ch9 | 手动加 `\index{}` |
| Axiom of choice!vs. nonemptiness of product | Ch2 L1694 | 手动加 `\index{}` |
| Axiom of choice!vs. well-ordering theorem | Ch1 L2047 | 改 `\index{well-ordering}` 为子条目 |
| h_*!dependence on base point | Ch9 | 手动加 `\index{}` |

## 五、引擎已知局限

1. **精确子串匹配 vs 模糊匹配**：引擎先精确匹配，失败后模糊匹配（单词窗口法）。但模糊匹配只对 L1 生效，L2 仍用精确+无数学禁区回退。
2. **`\(...\)` 数学禁区**：`find_math_ranges` 可能误将非数学区域标记为禁区。
3. **数据措辞差异**：数据条目中的 "a" vs "the"、"independence" vs "independent" 等细微差异导致匹配失败。
4. **`\textsl{...}` 等格式化命令**：引擎将其参数区域视为命令参数而跳过，但用户可能希望索引其中的文字。已通过 `is_inside_command_arg` 的格式化命令例外处理。

## 六、最终状态

| 指标 | 值 |
|------|:---:|
| 索引条目 | 619（合并后） |
| 大小写重复 | 0 |
| 字母分组 | 25/26 (A-Z, 缺Y) |
| Symbol 分组 | 已移除 |
| makeindex 拒绝 | 0 |
| LaTeX 错误 | 8（非致命） |
| PDF 页数 | 607 |
