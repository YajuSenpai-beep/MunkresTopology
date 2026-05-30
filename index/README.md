# Index Checking System

Munkres Topology 索引检查系统。所有与索引相关的脚本、数据、校验逻辑集中管理于此。

## 目录结构

```
index/
  utils.js                     # 共享工具（JSON 读取、括号匹配、命令提取、格式化）
  check-all.js                 # 总控：一键运行全部 7 项检查

  data/                        # 索引条目数据（JSON）
    ch10_entries.json          #   Chapter 10 分章条目
    ch11_entries.json          #   Chapter 11 分章条目
    ch12_entries.json          #   Chapter 12 分章条目
    ch13_entries.json          #   Chapter 13 分章条目
    ch14_entries.json          #   Chapter 14 分章条目

  validate/                    # 数据校验
    master-json.js             #   校验 original/index_entries.json 结构完整性
    chapter-jsons.js           #   校验 data/ch*_entries.json 结构完整性
    crossref.js                #   交叉比对章节 JSON ↔ master JSON
    pdf-compare.js             #   原始书 index.pdf ↔ index_entries.json 覆盖对比

  scan/                        # 源码分析
    commands.js                #   扫描 14 章 .tex 文件中的 \idx/\idxsub/\idxmath 命令
    coverage.js                #   对比源码命令 vs master JSON，计算覆盖率

  check/                        # 系统检查
    config.js                  #   校验 .sty / .ist / Makefile 索引配置
    build.js                   #   校验 .idx / .ind / .log 构建产物
```

## 数据流

```
  original/index_entries.json ──→ validate/master-json.js
         │                              │
         ├──────────────→ validate/crossref.js ←── data/ch*_entries.json
         │                              │              │
         ├──────────────→ scan/coverage.js            │
         │                      │                     │
         │              scan/commands.js ←── chapters/*.tex
         │
         └──────────────→ validate/pdf-compare.js ←── original/pdf/index.pdf

  TopologyBook.sty ──→ check/config.js
  Makefile          ──→ check/config.js
  *.ist             ──→ check/config.js

  *.idx / *.ind / *.log ──→ check/build.js
```

## 使用方式

```bash
# 运行全部检查
node index/check-all.js

# 跳过 .tex 扫描（快速模式）
node index/check-all.js --quick

# 单独运行某个脚本
node index/validate/master-json.js
node index/scan/commands.js

# JSON 输出（程序化消费）
node index/check-all.js --json
```

## 脚本职责速查

| 脚本 | 输入 | 输出 | 退出码 |
|------|------|------|--------|
| `validate/master-json.js` | `original/index_entries.json` | 结构校验报告 | 0=通过, 1=数据损坏 |
| `validate/chapter-jsons.js` | `data/ch*_entries.json` | 逐章校验报告 | 0=通过, 1=数据损坏 |
| `validate/crossref.js` | 章节 JSON + master JSON | 交叉比对报告 | 0=通过, 1=存在不匹配 |
| `validate/pdf-compare.js` | `original/pdf/index.pdf` + master JSON | L1/L2 覆盖报告 | 0=通过, 1=存在缺失 |
| `scan/commands.js` | `chapters/*.tex` | 逐章 \idx 命令统计 | 始终 0 |
| `scan/coverage.js` | .tex 源码 + master JSON | 覆盖率 + 缺失清单 | 1=源码有异常条目 |
| `check/config.js` | `.sty` `.ist` `Makefile` `.tex` | 配置完整性 | 0=完整, 1=缺配置 |
| `check/build.js` | `.idx` `.ind` `.log` | 构建产物状态 | 0=无 LaTeX 错误 |

## 当前状态

- **Master JSON**: 1418 条目（685 L1 + 733 L2），结构无损坏，与原始书 index.pdf 完整覆盖
- **章节 JSON**: 仅 ch10–14 已提取（252 条），ch1–9 待提取（1166 条）
- **索引命令**: 所有 14 章 .tex 文件中尚未插入任何 `\idx{}` 命令
- **覆盖率**: 0%（索引尚未实施）
- **配置**: 完备（16/16 通过）

## 索引命令格式

| 命令 | 用途 | 示例 |
|------|------|------|
| `\idx{term}` | L1 索引条目，正文渲染为粗斜体 | `\idx{Compactness}` |
| `\idxmath{sort}{display}` | L1 数学符号条目，sort 为排序键 | `\idxmath{A}{\(\bar{A}\) (closure)}` |
| `\idxsub{parent}{child}` | L2 子条目，仅写入 .idx 不渲染 | `\idxsub{Compactness}{of product space}` |
