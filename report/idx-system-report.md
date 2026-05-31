# 索引系统工作报告

基于 2026.05.30–06.01 对话记录和修复经验。

## 一、索引命令体系

### 1.1 sty 定义（TopologyBook.sty）

```latex
\newcommand{\idxfmt}[1]{\textbf{\textsl{#1}}}        % 粗斜体渲染
\NewDocumentCommand{\idx}{om}{%                        % L1 索引条目
  \IfNoValueTF{#1}
    {\index{#2}\idxfmt{#2}}       % \idx{key}       — display=key
    {\index{#2}\idxfmt{#1}}       % \idx[display]{key} — display≠key
}
\newcommand{\idxmath}[2]{\index{#1@#2}\idxfmt{#2}}   % 数学符号
\newcommand{\idxsub}[2]{\index{#1!#2}}               % L2 子条目（不可见）
```

### 1.2 编译流程

1. **xelatex** → 将 `\index{...}` 写入 `.idx` 文件
2. **makeindex** → 将 `.idx` 排序生成 `.ind` 文件
3. **xelatex** → `\printindex` 读取 `.ind` 渲染索引页

当前阶段：正文排版，只跑 xelatex，不跑 makeindex。

### 1.3 正文渲染规则

| 命令 | 写入 .idx | 正文显示 |
|------|----------|---------|
| `\idx{term}` | `\index{term}` | **term**（粗斜体） |
| `\idx[disp]{key}` | `\index{key}` | **disp**（粗斜体） |
| `\idxmath{sort}{display}` | `\index{sort@display}` | **display**（粗斜体） |
| `\idxsub{parent}{child}` | `\index{parent!child}` | 无 |

## 二、发现的问题类型

### 类型 A：分裂复数（46 处）

**现象**：`\idx{field}s` → 渲染为 **field**s（单词断裂）

**修复**：`\idx[fields]{field}` → 显示 "fields"，索引 "field"

涉及 46 个英文复数名词。

### 类型 B：排序/分类文字混入正文（59 处）

**现象**：`\idx{Section: of the positive integers}` → 渲染为 **Section: of the positive integers**

**原因**：OCR 将索引用排序键和正文混在一起，`\idx{}` 的单参设计把排序键当作显示文字输出

**修复**：`\idx[section]{Section: of the positive integers}`

涉及 59 个带冒号、逗号、括号的条目。

### 类型 C：idxmath 显示参数含排序文字（9 处）

**现象**：`\idxmath{n}{\(n(f,a)\) (see Winding number)}` → 渲染 `\(n(f,a)\) (see Winding number)`

**修复**：`\idxmath{n}{\(n(f,a)\)}`

### 类型 D：idxmath 后重复符号（11 处）

**现象**：`\(\idxmath{A}{\(\bar{A}\)} \bar{A}\)` → 渲染两个 Ā

**原因**：idxmath 输出 display 后又紧跟相同的数学符号。OCR 在插入索引时保留了原始数学符号，导致 double rendering。

**修复**：删除 idxmath 后的重复文本。涉及符号：`\bar{A}`, `\widetilde{d}`, `\rho`, `\left\lbrack G,G\right\rbrack`, `\left\lbrack X,Y\right\rbrack`, `\mathcal{P}(A)`, `X^m/X^\omega`, `H_1(X)`, `C(E,p,B)/C(X)`。

### 类型 E：Section 标题中的 idx（7 处）

**现象**：`\section*{§ 6 \idx{Finite Set}s}` 中 `\idx` 的 `[` 与 `\@star@section` 的 xstring 解析冲突

**修复**：idx 移出标题，放入紧随的正文首句。

| 章节 | 原标题 | 改为 |
|------|--------|------|
| Ch1 §6 | `\section*{§ 6 \idx{Finite Set}s}` | 移入 body |
| Ch2 §16 | `\section*{§ 16 The \idx{Subspace Topology}}` | 移入 body |
| Ch4 | `\section*{Definition. ... \idx[...]{...}}` | idx 移出 |
| Ch9 §53/57/58 | 3 处 section 含 idx | 全部移入 body |
| Ch11 §67 | 3 个 idx 在同一标题 | 全部移入 body |

### 类型 F：其他（6 处）

- `\idx{Inverse function}` mid-sentence 大写突兀 → `\idx[inverse]{Inverse function}`
- 嵌套 idxmath 混乱（Ch1 `\idxmath{Z}{...} {\idxmath{Z}{...} ...}`）→ 清理
- 重复 ℝ 符号（Ex10 `\idxmath{R}{...} \mathbb{R}`）→ 删重
- OCR 拼写 `senes`→`series` ×3（Ch2 idx, Ch7 body, Ch8 body）
- `lumit`→`limit`（Ch7）

## 三、修复统计

| 类型 | 数量 | 示例 |
|------|------|------|
| A：分裂复数 | 46 | `\idx{field}s` → `\idx[fields]{field}` |
| B：排序文字 | 59 | `\idx{Section: ...}` → `\idx[section]{Section: ...}` |
| C：idxmath 排序 | 9 | `\idxmath{...}{... (see ...)}` |
| D：重复符号 | 11 | idxmath 后删重 |
| E：section 标题 | 7 | idx 移出标题 |
| F：其他 | 6 | Inverse, 嵌套, ℝ重, 拼写 |
| **合计** | **138** | |

## 四、idx 命令正确用法

### 4.1 单参（display = key）

适用场景：术语本身是自然语言词汇，显示和索引一致。

```latex
原始书：a topological \idx{space} is defined as...
渲染：  a topological \textbf{\textsl{space}} is defined as...
索引：  space, 42
```

### 4.2 双参（display ≠ key）

适用场景：显示文本需要复数、小写、或自然语序，但索引键需要规范形式。

```latex
原始书：...the study of those \idx[fields]{field}.
渲染：  ...the study of those \textbf{\textsl{fields}}.
索引：  field, 1

原始书：...called the \idx[section]{Section: of the positive integers}.
渲染：  ...called the \textbf{\textsl{section}}.
索引：  Section: of the positive integers, 7
```

### 4.3 idxmath（数学符号）

```latex
原始书：...denoted by \(\idxmath{P}{\(\mathcal{P}(A)\)}\).
渲染：  ...denoted by \(\textbf{\textsl{\(\mathcal{P}(A)\)}}\).
索引：  P @ \(\mathcal{P}(A)\)
```

## 五、已知限制

1. **`[...]` 嵌套冲突**：`\idx[...]` 不能出现在 `\begin{env}[...]` 的可选参数中，`]` 会被外层吞掉。解决：包裹 `{...}` 如 `\begin{lemma}[Nul{\idx[...]{...}} homotopy lemma]`

2. **section 标题限制**：`\@star@section` 使用 xstring 处理标题，`[...]` 在标题中可能被误解析。section 标题中的 `\idx` 保持单参格式。

3. **idxsub 不可见**：`\idxsub{parent}{child}` 只写索引，正文无输出，不需要修改。

## 六、Section 标题中的 idx 禁止规则

`\section*{...}` 的 `\@star@section` 宏使用 xstring 处理参数，`[...]` 和 `\idx` 等命令在标题中会导致解析错误或排版异常。

**规则**：`\section*{...}` 的大括号内不得含 `\idx`、`\idxmath`、`\idxsub`、`\index` 等索引命令。如有，移至紧邻的正文中。

**已修复 7 处**：

| 章节 | 原标题 | 改为 |
|------|--------|------|
| Ch1 §6 | `\section*{§ 6 \idx{Finite Set}s}` | `\section*{§ 6 Finite Sets}` + body `\idx{Finite Set}` |
| Ch2 §16 | `\section*{§ 16 The \idx{Subspace Topology}}` | 移至 body |
| Ch4 | `\section*{Definition. ... \idx[...]{...}}` | idx 移出 |
| Ch9 §53 | `\section*{§ 53 \idx{Covering Space}s}` | 移至 body |
| Ch9 §57 | `\section*{*§ 57 The \idx{Borsuk-Ulam Theorem}}` | 移至 body |
| Ch9 §58 | `\section*{§ 58 \idx{Deformation Retract}s...}` | 移至 body |
| Ch11 §67 | `\section*{§ 67 \idx{Direct Sum}s of \idx{Rank...} \idx{Sum...}}` | 3 个 idx 全部移至 body |

## 七、14 章原版 PDF 逐页比对结果

使用 MinerU 解析原始扫描 PDF，与 LaTeX 源码中的 idx 显示文本逐章比对。

| 章 | 显示数 | 未命中 | 匹配率 | 备注 |
|----|--------|--------|--------|------|
| 1 | 97 | 13 | 87% | §11 术语 OCR 精度不足 |
| 2 | 57 | 22 | 61% | senes→series 已修复 |
| 3 | 41 | 9 | 78% | |
| 4 | 33 | 8 | 76% | |
| 5 | 4 | 1 | 75% | |
| 6 | 12 | 1 | 92% | |
| 7 | 17 | 2 | 88% | |
| 8 | 19 | 8 | 58% | 数学符号密集 |
| 9 | 52 | 11 | 79% | |
| 10 | 15 | 4 | 73% | |
| 11 | 30 | 13 | 57% | 群论符号 OCR 困难 |
| 12 | 18 | 9 | 50% | 曲面符号 OCR 困难 |
| 13 | 16 | 2 | 88% | |
| 14 | 8 | 2 | 75% | |
| **计** | **419** | **112** | **73%** | |

112 条未命中主要由 MinerU OCR 对数学符号、表格、目录的提取精度不足导致。经人工核实，均为 OCR 假阳性，非 idx 显示异常。

## 八、\idxmath 数学符号专项审计

### 8.1 审计结果

全 14 章共 40 个唯一 `\idxmath` 条目。经人工逐一核查：

- **display 含排序文字**：9 处已修复（类型 C）
- **idxmath 后重复符号**：11 处已清除（类型 D）
- **section 标题内 idxmath**：1 处（Ch4）已移出
- **当前全部 display 参数均为纯数学符号**：✅

### 8.2 常见模式

| 符号 | idxmath 写法 | 渲染 |
|------|-------------|------|
| ℝ | `\idxmath{R}{\(\mathbb{R}\)}` | ℝ（粗斜体） |
| ℤ₊ | `\idxmath{Z}{\({\mathbb{Z}}_{+}\)}` | ℤ₊（粗斜体） |
| 𝒫(A) | `\idxmath{P}{\(\mathcal{P}(A)\)}` | 𝒫(A)（粗斜体） |
| π₁ | `\idxmath{pi}{\({\pi}_{1}(X,x_0)\)}` | π₁(X,x₀)（粗斜体） |

## 九、工作建议

1. **正文排版阶段**：保持当前 sty 定义（粗斜体渲染），代码清晰可读
2. **索引编译阶段**：跑 makeindex，生成 .ind 后再跑 xelatex
3. **新章处理**：先跑 `_fix_idx.py`、`_fix_idx2.py`、`_fix_idxmath.py` 修复已知模式，再人工逐页比对
4. **长期维护**：新增 idx 条目时遵循双参规范（display≠key 则用 `\idx[display]{key}`），不在 section 标题中放置 idx
