# latex-index-tool 生态集成设计文档

## 1. texdoc 集成

### 背景
texdoc 是 TeX Live 发行版的文档查找工具。latex-index-tool 可通过提供 texdoc 可识别的配置，让用户通过 `texdoc latex-index` 查看手册。

### 实施方案
1. 在 `$TEXMF/doc/latex/latex-index/` 下安装 `latex-index.pdf` 手册
2. 注册到 texdoc 数据库：
   ```
   # texdoc.cnf
   alias latex-index = latex_index_tool_manual
   ```
3. 随 PyPI 包发布预编译的 PDF 手册，由安装脚本放入 TEXMF 树

### 状态：设计阶段，等待手册编写

---

## 2. arXiv 提交流程集成

### 背景
arXiv 接受 LaTeX 源码提交。用户可在提交前通过 latex-index-tool 自动插入索引命令。

### 实施方案
1. **预提交脚本**：`arxiv-prepare.sh`
   ```bash
   # 在提交 arXiv 前运行
   latex-index insert --main main.tex --entries index_entries.json
   latex-index xindy --languages english -o index_style.xdy
   # 打包
   tar czf submit.tar.gz *.tex *.sty *.xdy *.bbl figures/
   ```
2. **注意事项**：
   - arXiv 使用 TeX Live 2016（较老），需确保兼容性
   - `\index` 命令是标准 LaTeX2e，无需额外包
   - xindy 样式文件需包含在提交包中

### 状态：脚本模板可用，需按项目定制

---

## 3. CI/CD 完整流水线

```
Git Push
  ├── GitHub Actions: test (3.10, 3.11, 3.12) + lint + mypy
  ├── GitHub Actions: benchmark (hard threshold 5s)
  └── On tag push:
        ├── Build Docker image → GitHub Container Registry
        ├── Build PyInstaller exe → Attach to release
        ├── Publish to PyPI
        └── Update brew formula (sha256)

Manual:
  - brew formula: submit PR to homebrew-core
  - scoop manifest: update version in bucket
```

## 4. 分发矩阵

| 平台 | 方式 | 状态 |
|------|------|:---:|
| Linux/macOS | `pip install` | ✅ |
| Linux/macOS | `brew install` | 🔧 模板就绪 |
| Windows | `pip install` | ✅ |
| Windows | `scoop install` | 🔧 模板就绪 |
| 任意 | Docker `ghcr.io/...` | ✅ |
| 任意 | PyInstaller `.exe` | ✅ |
| 任意 | `install.sh` / `install.ps1` | ✅ |
| Web | Overleaf wrapper | ✅ |
| Editor | VS Code tasks | ✅ |

## 5. 未来路线图

- [ ] 手册 PDF (texdoc 集成)
- [ ] brew formula 提交到 homebrew-core
- [ ] scoop manifest 提交到 main bucket
- [ ] arXiv 预提交自动化脚本
- [ ] Overleaf 官方集成 (提交到 Overleaf 模板库)
