# LaTeX Index Tool — 通用 LaTeX 索引自动插入工具

配置驱动、项目无关的生产级工具，用于在 LaTeX 源文件中自动插入 `\index{}` 命令。

```
index/
├── latex_index/        # Python 核心包（16 模块）
├── core/               # Node.js 引擎（保留兼容）
├── config/             # YAML 配置文件
├── tools/              # 独立批处理脚本
├── tests/              # pytest 测试套件（409 项，89% 覆盖）
├── data/               # 索引条目 JSON 数据
└── test/               # 测试用 .tex 样本
```

---

## 快速开始 | Quick Start

### 安装 | Installation

```bash
# pip 安装（推荐）
pip install latex-index-tool

# 可选组件
pip install latex-index-tool[tui]             # Rich TUI 界面
pip install latex-index-tool[progress]        # 进度条
pip install latex-index-tool[xindy]           # 中文拼音排序
pip install latex-index-tool[all]             # 全部

# 一键安装脚本
curl -sSL https://.../install.sh | bash       # Linux / macOS
iwr https://.../install.ps1 | powershell      # Windows

# 包管理器
brew install latex-index-tool                 # macOS (Homebrew)
scoop install latex-index-tool                # Windows (Scoop)

# 源码安装（开发模式）
cd index && pip install -e ".[dev]"
```

### 基本使用

```bash
# 预览
latex-index insert --chapter 1 --dry-run

# 正式插入 + 进度条
latex-index insert --chapter 1 --progress

# Rich TUI 交互界面
latex-index insert --chapter 1 --interactive --tui

# 多文件项目模式
latex-index insert --main main.tex --entries data/entries.json

# 解析 OCR 索引文本
latex-index parse index.txt -o entries.json

# 扫描已有索引
latex-index scan chapter.tex -o report.txt

# 生成索引分析报告
latex-index report chapter.tex --entries data/entries.json

# 生成 xindy 排序规则
latex-index xindy --languages english chinese-pinyin -o index_style.xdy

# latexmk 编译集成
latex-index setup --project-dir .          # 生成 .latexmkrc
latex-index rollback chapter.tex           # 恢复备份
latex-index rollback --list chapter.tex    # 列出备份
latex-index rollback --clean 5 chapter.tex # 清理旧备份

# 批处理工具
latex-index tools format-env --chapter 2
latex-index tools convert-exercises --chapter 3
latex-index tools ocr-fix --chapter 1
latex-index tools scan-issues
```

### Python API

```python
from latex_index.engine import IndexEngine
from latex_index.config import load_config

config = load_config("config/default.yaml")
engine = IndexEngine(config)

with open("chapter.tex") as f:
    content = f.read()

entries = [
    {"term": "compact space", "level": 1},
    {"term": "open cover", "level": 2, "parent": "compact space"},
]

# 标准搜索
ops = engine.find_insertions(content, entries)

# 快速搜索（Aho-Corasick，适合大规模词条）
ops = engine.find_insertions_fast(content, entries, progress=True)

# 应用修改
result = engine.apply(content, ops)
```

---

## CLI 完整参考

### `latex-index insert` — 索引插入

| 参数 | 说明 |
|------|------|
| `--config PATH` | 配置文件路径（YAML/JSON），默认使用内置配置 |
| `--chapter N` | 章节编号（单文件模式） |
| `--entries PATH` | 条目 JSON 文件，默认 `data/ch0N_entries.json` |
| `--main PATH` | 多文件项目主文件，自动解析 `\input`/`\include` |
| `--dry-run` | 预览模式，仅显示将要插入的条目和位置 |
| `--l1-only` | 仅处理 L1 条目 |
| `--fast` | 强制使用 Aho-Corasick 自动机 |
| `--interactive`, `-i` | 交互模式（自动检测 Rich，回退到命令行） |
| `--tui` | 强制使用 Rich TUI（支持 all/range/select/search） |
| `--progress` | 显示进度条（需安装 tqdm） |

### `latex-index parse` — 索引文本解析

```bash
latex-index parse index.txt --format indented -o entries.json
latex-index parse index.txt --format run-in -o entries.json
```

| 参数 | 说明 |
|------|------|
| `input` | 索引文本文件路径 |
| `--format` | 格式：`indented`（默认）或 `run-in` |
| `--output`, `-o` | 输出 JSON 文件路径 |

### `latex-index scan` — 索引扫描

```bash
latex-index scan chapter.tex -o report.txt
```

扫描文件中已有的 `\index{}`、`\idx{}`、`\idxmath{}`、`\idxsub{}` 命令。

### `latex-index report` — 索引分析报告

```bash
# 完整报告（覆盖率 + 重复 + 配对）
latex-index report chapter.tex --entries data/entries.json --candidates words.txt

# 基础报告（仅统计）
latex-index report chapter.tex
```

| 参数 | 说明 |
|------|------|
| `input` | .tex 文件路径 |
| `--entries` | 条目 JSON，用于覆盖率分析 |
| `--candidates` | 候选词条文件（每行一个），用于缺失检测 |
| `--output`, `-o` | 输出报告文件路径 |

### `latex-index setup` — 编译集成

```bash
latex-index setup                    # 生成 .latexmkrc（含自动备份）
latex-index setup --no-backup        # 不含备份
```

自动生成的 `.latexmkrc` 在编译前自动插入索引、编译后重新生成索引。

### `latex-index rollback` — 备份回滚

```bash
latex-index rollback chapter.tex           # 恢复到最近备份
latex-index rollback --list chapter.tex    # 列出所有备份
latex-index rollback --clean 5 chapter.tex # 清理旧备份，保留 5 个
```

### `latex-index xindy` — 排序规则生成

```bash
# 生成英文索引样式
latex-index xindy -o index_style.xdy

# 中英混合索引
latex-index xindy --languages english chinese-pinyin -o index_style.xdy

# 列出支持的语言
latex-index xindy --list-langs
```

支持的语言：`english`、`chinese-pinyin`、`chinese-stroke`、`greek`、`math-symbols`。

### `latex-index tools` — 批处理工具集

| 子命令 | 功能 |
|--------|------|
| `format-env` | 修复环境格式 `\begin{env}text` → 三行拆分 |
| `convert-exercises` | 转换习题为 `enumerate` 格式（含子题） |
| `clean-ex-envs` | 清理习题内 theorem/proof/lemma → `\textsl{}` |
| `fix-subitems` | 修复 `\item (a)` 父级条目 |
| `wrap-examples` | 用 `centeredblock` 包裹 `example` 环境 |
| `ocr-fix` | OCR 拼写修复（含词边界保护） |
| `scan-issues` | 扫描已知问题（拼写、引号、格式） |

所有子命令支持 `--chapter N`、`--files a.tex b.tex`、`--continue-on-error`。

---

## 配置手册

### 完整配置 | Full Configuration

```yaml
# ── 版本（工具兼容性校验） ──
version: 1                                      # int, 必需

# ── 索引处理器 ──
index_processor: "makeindex"                    # str, 默认 "makeindex", 可选 "xindy"

# ── 模板 ──
templates:                                      # dict, 必需
  l1: "\\index{${key}}"                         # str — 普通 L1 条目
  l1Math: "\\index{${sort}@${display}}"          # str — 数学符号
  l2: "\\index{${parent}!${child}}"              # str — L2 子条目

# ── 文件匹配 ──
file_pattern: "Chapter_${num}_*.tex"            # str, ${num} → 章节编号
chapter_source_dir: "chapters"                  # str, 章节 .tex 文件目录

# ── 别名：正文变体 → 索引键 ──
aliases:                                        # dict[str, list[str]], 默认 {}
  "inverse image": ["preimage"]
  "compactness": ["compact"]

# ── 数学快捷方式 ──
math_shortcuts:                                 # dict[str, list[str]], 默认 {}
  "\\mathbb{R}": ["\\R"]
  "\\mathbb{Z}": ["\\Z"]

# ── 跳过模式（正则） ──
skip_patterns: []                               # list[str], 默认 []

# ── 日志 ──
log_level: "INFO"                               # str, 默认 "INFO", 可选 DEBUG/INFO/WARNING/ERROR
log_file: "index_tool.log"                      # str, 日志轮转 5×10MB
```

### 配置项速查 | Config Reference

| 键 | 类型 | 默认值 | 说明 |
|----|------|--------|------|
| `version` | int | 1 | 配置格式版本，不匹配时警告 |
| `index_processor` | str | `"makeindex"` | 索引处理器：`makeindex` 或 `xindy` |
| `templates.l1` | str | `"\\index{${key}}"` | L1 条目模板 |
| `templates.l1Math` | str | `"\\index{${sort}@${display}}"` | 数学符号模板 |
| `templates.l2` | str | `"\\index{${parent}!${child}}"` | L2 子条目模板 |
| `file_pattern` | str | `"Chapter_${num}_*.tex"` | 章节文件名模式 |
| `chapter_source_dir` | str | `"chapters"` | 章节文件目录 |
| `aliases` | dict | `{}` | 正文变体 → 索引键映射 |
| `math_shortcuts` | dict | `{}` | LaTeX 命令 → 简写映射 |
| `skip_patterns` | list | `[]` | 跳过匹配的行（正则） |
| `log_level` | str | `"INFO"` | 日志级别 |
| `log_file` | str | `"index_tool.log"` | 日志文件路径 |

### 模板变量

| 变量 | 说明 | 示例 |
|------|------|------|
| `${key}` | 索引键（排序用） | `compact space` |
| `${display}` | 显示文本 | `\(\mathbb{R}\)` |
| `${sort}` | 数学符号排序键 | `R` |
| `${parent}` | 父条目名称 | `compact space` |
| `${child}` | 子条目名称 | `open cover` |

### 条目 JSON 格式

```json
{
  "entries": [
    {"term": "compact space", "level": 1},
    {"term": "open cover", "level": 2, "parent": "compact space"},
    {"term": "\\(\\mathbb{R}\\)", "level": 1, "sort_key": "R",
     "display": "\\(\\mathbb{R}\\)"}
  ]
}
```

### 中文索引

设置 `index_processor: "xindy"` 并配合排序规则：

```bash
# 生成中英混合 xindy 样式文件
latex-index xindy --languages english chinese-pinyin -o index_style.xdy

# 在配置中指定
# index_processor: "xindy"
```

```python
from latex_index.collation import sort_key_for

# 拼音排序
sorted(entries, key=lambda e: sort_key_for(e["term"], "pinyin"))

# 笔画排序
sorted(entries, key=lambda e: sort_key_for(e["term"], "stroke"))
```

---

## 安全特性

| 特性 | 实现 |
|------|------|
| **原子写入** | `tempfile.mkstemp()` + `os.replace()` |
| **文件锁** | 跨平台独占锁（`fcntl` / `msvcrt`），防并发损坏 |
| **dry-run** | `--dry-run` 仅打印，不修改文件 |
| **交互确认** | `--interactive` 支持 Rich TUI (all/range/select/search) + 命令行回车 |
| **批处理容错** | `--continue-on-error` 单文件失败后继续 |
| **备份回滚** | `latex-index rollback` 恢复任意历史备份 |
| **LaTeX 语义安全** | 跳过数学模式、注释、抄录环境、ExplSyntax、tikzpicture、tabular 等 |
| **编码检测** | UTF-8 → latin-1 → cp1252 自动回退 |
| **换行符保留** | 自动检测 `\r\n`/`\n`，保持原格式 |
| **日志轮转** | `RotatingFileHandler` 5×10MB，防磁盘写满 |
| **去重** | 长词优先，重叠位置自动跳过 |

### LaTeX 命令参数自动避开

引擎自动跳过 50+ 标准命令的参数区域：
`\section`, `\chapter`, `\label`, `\ref`, `\cite`, `\textcite`, `\parencite`, `\index`, `\textbf`, `\emph`, `\footnote`, `\includegraphics`, `\caption`, `\newcommand` 等。

### LaTeX 环境自动避开

`\ExplSyntaxOn/Off` · `verbatim` · `lstlisting` · `minted` · `tikzpicture` · `pgfplots` · `axis` · `tabular` · `tabularx` · `longtable` · `array`

### `\index` 高级格式

- `|see{other}` — 交叉引用
- `|seealso{other}` — 参见引用
- `|(` / `|)` — 范围索引（`report` 命令可检测未配对）

---

## 性能

| 场景 | 策略 | 复杂度 |
|------|------|--------|
| 常规 (< 1000 词条, < 500KB) | 逐条搜索 | O(n·k) |
| 大规模 (≥ 1000 词条) | Aho-Corasick 自动机 | O(n + m) |
| 超大文件 (> 50MB) | 自动限制词条数 | 防止 OOM |
| 超大文件 (> 10MB) | 缓冲写入 | 减少内存碎片 |

使用 `--progress` 可显示实时进度条（需安装 tqdm）。

---

## 测试

```bash
cd index
pip install -e ".[dev]"

# 全部测试（409 项，89% 覆盖）
make test

# 覆盖率报告
pytest tests/ --cov=latex_index --cov-report=term

# 分类运行
pytest tests/test_engine.py -v        # 引擎
pytest tests/test_tex_utils.py -v     # LaTeX 工具
pytest tests/test_matcher.py -v       # Aho-Corasick 自动机
pytest tests/test_parser.py -v        # 解析器
pytest tests/test_project.py -v       # 多文件项目
pytest tests/test_config.py -v        # 配置管理
pytest tests/test_scanner.py -v       # 索引扫描
pytest tests/test_cli.py -v           # CLI 命令
pytest tests/test_tools_cli.py -v     # 批处理工具
pytest tests/test_collation.py -v     # 排序规则
pytest tests/test_fuzz.py -v          # 模糊测试
pytest tests/test_reporter.py -v      # 报告生成
pytest tests/test_tui.py -v           # Rich TUI
pytest tests/test_latexmk.py -v       # 编译集成
pytest tests/test_xindy.py -v         # xindy 生成
pytest tests/test_integration.py -v   # 集成测试
pytest tests/test_regression.py -v    # 回归测试
pytest tests/test_exceptions.py -v    # 异常测试
pytest tests/test_performance.py -v   # 性能测试

# 类型检查 + 代码风格 + 测试
make all
```

---

## 开发

```bash
# 安装开发依赖
pip install -e ".[dev]"

# 代码检查
make lint          # ruff
make typecheck     # mypy --strict
make fmt           # ruff format

# 构建
make build         # python -m build

# Docker 构建
docker build -t latex-index-tool .
docker run -v $(pwd):/app latex-index-tool insert --chapter 1 --dry-run

# PyInstaller 打包
pyinstaller latex-index.spec
```

### 工具链

| 工具 | 用途 | 配置 |
|------|------|------|
| pytest | 测试 | `pyproject.toml` [tool.pytest] |
| ruff | Lint + 格式化 | `pyproject.toml` [tool.ruff] |
| mypy | 静态类型检查 | `pyproject.toml` [tool.mypy] (strict) |
| PyInstaller | 打包独立 exe | `latex-index.spec` |
| Rich | TUI 交互界面 | 可选依赖 |
| pypinyin | 中文拼音排序 | 可选依赖 |
| tqdm | 进度条 | 可选依赖 |

### CI/CD

| 事件 | 动作 |
|------|------|
| push / PR → main | 测试 (3.10/3.11/3.12) + lint + mypy |
| push / PR → main | 性能 benchmark |
| tag → main | Docker 镜像 → GitHub Container Registry |
| tag → main | 发布 PyPI |

### 发布流程

1. `make all` — 确保全部通过（409 测试 + mypy + ruff）
2. 更新 `pyproject.toml` 版本号
3. 更新 `CHANGELOG.md`
4. `git tag v1.0.0 && git push --tags`
5. CI 自动构建 Docker 镜像并发布到 PyPI

---

## 目录说明

| 路径 | 内容 |
|------|------|
| `latex_index/` | Python 包（engine, parser, tex_utils, matcher, config, project, scanner, cli, tools_cli, collation, reporter, tui, latexmk, xindy） |
| `core/` | Node.js 引擎（保留兼容） |
| `config/` | default.yaml |
| `tools/` | 独立批处理脚本（也可通过 `latex-index tools` 调用） |
| `tests/` | pytest 测试套件（409 项，89% 覆盖） |
| `data/` | 14 章索引条目 JSON |
| `test/` | 测试用 .tex 样本 |

---

## 贡献

欢迎提交 Issue 和 Pull Request。

```bash
# 贡献前请确保
make all        # 完整检查（tests + mypy + ruff）
pytest tests/   # 409 项测试全部通过
```

---

## 许可

MIT License
