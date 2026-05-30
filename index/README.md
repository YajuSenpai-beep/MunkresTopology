# Index System

Munkres Topology 索引系统。所有与索引相关的脚本、数据、校验、生成、文档集中管理于此。

## 目录结构

```
index/
  utils.js                     # 共享工具（JSON 读取、括号匹配、命令提取、格式化）
  check-all.js                 # 总控：一键运行全部检查

  assign-chapters.js           # 生成：按页数范围分配 1418 条条目到 14 章
  insert-commands.js           # 生成：将分章条目自动插入 .tex 源文件
  verify-assignments.js        # 校验：检查分章条目是否匹配对应章节内容
  audit-skipped.js             # 校验：审计被跳过的条目是否可找到

  TROUBLESHOOTING.md           # 故障排除与经验记录

  data/                        # 索引条目数据（JSON）
    ch01_entries.json          #   Chapter  1 分章条目（自动生成）
    ch02_entries.json          #   Chapter  2 分章条目（自动生成）
    ch03_entries.json          #   Chapter  3 分章条目（自动生成）
    ch04_entries.json          #   Chapter  4 分章条目（自动生成）
    ch05_entries.json          #   Chapter  5 分章条目（自动生成）
    ch06_entries.json          #   Chapter  6 分章条目（自动生成）
    ch07_entries.json          #   Chapter  7 分章条目（自动生成）
    ch08_entries.json          #   Chapter  8 分章条目（自动生成）
    ch09_entries.json          #   Chapter  9 分章条目（自动生成）
    ch10_entries.json          #   Chapter 10 分章条目（自动生成）
    ch11_entries.json          #   Chapter 11 分章条目（自动生成）
    ch12_entries.json          #   Chapter 12 分章条目（自动生成）
    ch13_entries.json          #   Chapter 13 分章条目（自动生成）
    ch14_entries.json          #   Chapter 14 分章条目（自动生成）

  validate/                    # 数据校验
    master-json.js             #   校验 original/index_entries.json 结构完整性
    chapter-jsons.js           #   校验 data/ch*_entries.json 结构完整性
    crossref.js                #   交叉比对章节 JSON ↔ master JSON
    pdf-compare.js             #   原始书 index.pdf ↔ index_entries.json 覆盖对比

  scan/                        # 源码分析
    commands.js                #   扫描 .tex 文件中的 \idx/\idxsub/\idxmath 命令
    coverage.js                #   对比源码命令 vs master JSON，计算覆盖率

  check/                       # 系统检查
    config.js                  #   校验 .sty / .ist / Makefile 索引配置
    build.js                   #   校验 .idx / .ind / .log 构建产物
```

## 数据流

```
  original/index_entries.json
         │
         ├──→ assign-chapters.js ──→ data/ch*_entries.json
         │         │
         │         └──→ insert-commands.js ──→ chapters/*.tex
         │
         ├──→ validate/master-json.js
         ├──→ validate/crossref.js ←── data/ch*_entries.json
         ├──→ scan/coverage.js ←── scan/commands.js ←── chapters/*.tex
         └──→ validate/pdf-compare.js ←── original/pdf/index.pdf

  TopologyBook.sty ──→ check/config.js
  Makefile          ──→ check/config.js
  *.ist             ──→ check/config.js
  *.idx/*.ind/*.log ──→ check/build.js
```

## 使用方式

```bash
# 生成分章 JSON（从 original/index_entries.json 按页数分配）
node index/assign-chapters.js

# 插入 L1 索引命令到 chapters/（正文章节）
node index/insert-commands.js 5 --l1-only --chapters

# 插入到全部 14 章
for ch in $(seq 1 14); do node index/insert-commands.js $ch --l1-only --chapters; done

# 运行全部检查
node index/check-all.js

# 单独运行某个脚本
node index/validate/master-json.js
node index/scan/commands.js
```

## 脚本职责速查

| 脚本 | 类型 | 输入 | 输出 |
|------|------|------|------|
| `assign-chapters.js` | 生成 | `original/index_entries.json` | `data/ch*_entries.json` |
| `insert-commands.js` | 生成 | `data/ch*_entries.json` + `.tex` | 插入了 `\idx` / `\idxmath` 的 `.tex` |
| `verify-assignments.js` | 校验 | `data/` + `chapters_backup/*.tex` | 逐章术语匹配报告 |
| `audit-skipped.js` | 审计 | `chapters/*.tex` | 被跳过的 L1 条目可查性 |
| `validate/master-json.js` | 校验 | `original/index_entries.json` | 结构完整性 |
| `validate/chapter-jsons.js` | 校验 | `data/ch*_entries.json` | 逐章结构完整性 |
| `validate/crossref.js` | 校验 | data JSON + master JSON | 交叉比对 |
| `validate/pdf-compare.js` | 校验 | `original/pdf/index.pdf` + master | L1/L2 覆盖 |
| `scan/commands.js` | 扫描 | `chapters/*.tex` | 逐章 `\idx` 统计 |
| `scan/coverage.js` | 扫描 | .tex + master | 覆盖率 + 缺失清单 |
| `check/config.js` | 系统 | `.sty` `.ist` `Makefile` | 配置完整性 |
| `check/build.js` | 系统 | `.idx` `.ind` `.log` | 构建产物状态 |

## 当前状态

- **Master JSON**: 1418 条目（685 L1 + 733 L2），与原始书 index.pdf 完整覆盖
- **分章 JSON**: 14 章全部生成（`data/ch01_entries.json` ~ `ch14_entries.json`），基于页数范围自动分配
- **L1 插入**: 14 章 `.tex` 已插入 549 条 L1 索引命令（`\idx{}` + `\idxmath{}`）
- **编译**: 0 错误，0 拒绝，549 accepted by makeindex
- **配置**: 完备（16/16 通过）
- **L2 插入**: 尚未开始

## 索引命令格式

| 命令 | 用途 | 示例 |
|------|------|------|
| `\idx{term}` | L1 索引条目，正文渲染为粗斜体 | `\idx{Compactness}` |
| `\idxmath{sort}{display}` | L1 数学符号条目 | `\idxmath{A}{\(\bar{A}\) (closure)}` |
| `\idxsub{parent}{child}` | L2 子条目，仅写入 .idx | `\idxsub{Compactness}{of product space}` |

## 故障排除

见 [TROUBLESHOOTING.md](TROUBLESHOOTING.md)，记录了：

- **XeLaTeX + makeindex: `\idxmath` 中鲁棒命令展开问题** — `\widetilde{d}` 导致 1 rejected 的定位与修复
- **102→0 错误的完整修复历程** — 5 类问题的原因和解决方案
- **`\idxmath` 使用预防指南** — 哪些数学命令需要 `\protect`
