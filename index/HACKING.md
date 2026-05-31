# HACKING — latex-index-tool 开发者手册

## 架构设计

```
latex_index/
├── engine.py          # 核心：索引插入引擎 (IndexEngine)
├── tex_utils.py       # LaTeX 语义：数学/注释/抄录检测，字符转义
├── matcher.py         # 性能：Aho-Corasick 多模式匹配自动机
├── parser.py          # 解析：OCR 索引文本 → JSON
├── config.py          # 配置：YAML/JSON 加载，深度合并
├── project.py         # 项目：多文件 \input/\include 解析
├── scanner.py         # 扫描：已有 \index/\idx 命令发现
├── reporter.py        # 报告：覆盖率/重复/缺失/配对分析
├── collation.py       # 排序：拼音/笔画/Unicode 排序键
├── latexmk.py         # 集成：latexmkrc 生成 + 备份回滚
├── xindy.py           # 排序：.xdy 规则文件生成
├── tui.py             # 交互：Rich TUI 索引选择界面
├── tools_cli.py       # 批处理：环境修复、习题转换、OCR 等
├── cli.py             # 入口：argparse CLI + 命令分发
└── __main__.py        # 入口：python -m latex_index
```

### 核心数据流

```
OCR 索引文本 (.txt)
    │
    ▼ parser.py
条目 JSON (entries.json) ──┬── config.yaml
                           │       │
                           ▼       ▼
    LaTeX 源文件 (.tex) → engine.py → 修改后的 .tex
                           │
                           ├── matcher.py (Aho-Corasick, >1000 词条)
                           ├── tex_utils.py (禁区检测)
                           └── project.py (\input/\include 解析)
```

## 模块职责

### engine.py
- `IndexEngine.find_insertions(content, entries)` — 主搜索
- `IndexEngine.find_insertions_fast(content, entries)` — Aho-Corasick 快速路径
- `IndexEngine.apply(content, operations)` — 应用插入
- `IndexEngine.process_large_file(path, entries, config)` — 超大文件流式处理
- `IndexEngine._build_cmd(entry)` — 模板 → 命令字符串

### tex_utils.py
- `find_math_ranges()` / `find_comment_ranges()` / `find_verbatim_ranges()` — 禁区检测
- `is_inside_command_arg()` — 50+ 标准命令参数避开
- `escape_index_term()` — makeindex/xindy 特殊字符转义
- `strip_latex()` — 去除数学模式标记

### matcher.py
- `PatternMatcher.add(pattern, key)` — 添加模式
- `PatternMatcher.finish()` — BFS 构建 fail 链接
- `PatternMatcher.search(text)` — 单次扫描 O(n+m)

## 如何添加新的 LaTeX 环境避让

1. 打开 `tex_utils.py`
2. 如果要跳过整个环境（如 `\begin{XXX}...\end{XXX}`），添加 `XXX` 到 `_VERBATIM_ENVS`（代码类）或 `_NO_INDEX_ENVS`（非索引区域）
3. 如果要跳过命令参数（如 `\cmd{arg}`），添加 `cmd` 到 `_STANDARD_COMMANDS` 正则
4. 在 `tests/test_tex_utils.py` 中添加对应的测试用例
5. 运行 `pytest tests/test_tex_utils.py -v` 确认

## 如何添加新的 CLI 命令

1. 在 `cli.py` 中添加 `cmd_xxx(args)` 函数
2. 在 `main()` 中通过 `sub.add_parser()` 注册子命令
3. 在 `tests/test_cli.py` 中添加 `TestCmdXxx` 测试类
4. 更新 `README.md` 的 CLI 参考表

## 测试指南

```bash
# 全部测试
make test

# 特定模块
pytest tests/test_engine.py -v

# 覆盖率
pytest tests/ --cov=latex_index --cov-report=term

# 单文件快速迭代
pytest tests/test_matcher.py -x --tb=short
```

### 测试文件对应关系

| 源文件 | 测试文件 |
|--------|---------|
| engine.py | test_engine.py |
| tex_utils.py | test_tex_utils.py |
| matcher.py | test_matcher.py |
| parser.py | test_parser.py |
| project.py | test_project.py |
| config.py | test_config.py |
| scanner.py | test_scanner.py |
| cli.py | test_cli.py |
| tools_cli.py | test_tools_cli.py |
| collation.py | test_collation.py |
| reporter.py | test_reporter.py |
| tui.py | test_tui.py |
| latexmk.py | test_latexmk.py |
| xindy.py | test_xindy.py |

## 代码风格

- Python 3.10+ with `from __future__ import annotations`
- mypy strict mode: `python -m mypy latex_index/ --strict`
- ruff lint: `ruff check latex_index/`
- ruff format: `ruff format latex_index/`
- 所有 LaTeX 命令字符串使用 raw strings: `r"\begin{env}"`

## 发布流程

1. `make all` — 确保 409 测试 + mypy + ruff 通过
2. 更新 `pyproject.toml` 版本号
3. 更新 `CHANGELOG.md`
4. 推送 tag: `git tag vX.Y.Z && git push --tags`
5. CI 自动构建 Docker 镜像 + 发布 PyPI

## 依赖关系

```
core (no deps): config.py, matcher.py, parser.py, scanner.py
   ↓
semantic: tex_utils.py (depends on: none)
   ↓
engine: engine.py (depends on: tex_utils, matcher, config)
   ↓
infra: project.py, reporter.py, collation.py, latexmk.py, xindy.py, tui.py
   ↓
cli: cli.py (depends on: all above)
   └── tools_cli.py
```

## 常见问题

**Q: 为什么覆盖率不到 95%?**
A: CLI 模块（cli.py, tools_cli.py）的部分路径依赖实际文件系统（如 chapters/ 目录），单元测试无法覆盖。如需提升，可添加端到端集成测试。

**Q: 如何处理超大项目?**
A: `engine.process_large_file()` 自动限制词条数。对 2000+ 页的项目，建议使用 `--fast` 标志强制 Aho-Corasick 模式。
