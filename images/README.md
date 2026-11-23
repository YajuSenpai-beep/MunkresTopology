# images/

本目录同时存放**编译用 PDF** 和**历史测量用 PNG**，两者用途不同。

| 文件 | 用途 |
|---|---|
| `*.pdf` | 编译资产。`\munkresfig` / `\includegraphics` 使用不带扩展名的 `images/<图号>`，XeLaTeX 优先取 PDF。 |
| `*.png` | 历史测量与溯源资产。多张 `figures_src/fig_*.tex` 的注释写“几何实测自 `images/<图号>.png`”，坐标直接按这些 PNG 量出。 |
| `isbn_barcode.svg` | 条码源文件；PDF 已生成。 |

## 不要直接删 PNG

- 193 张 PNG 与 `论文素材/03_插图管线/images_processed/` 中的同名文件逐字节相同；
- 600dpi 真值在仓库外的 `figpipe/src_hi/`；
- 但历史 `.tex` 注释引用的是**本目录**的路径，直接删除会让溯源路径断掉。

已冻结一份快照（2026-11-24）：

```
论文素材/03_插图管线/images_repo_snapshot_20261124/
```

如确实要转为 PDF-only 仓库，先确认快照完整、再把历史注释的溯源路径写清楚，最后才 `git rm images/*.png`。

## 检查

```bash
python tools/check_figures.py
```

确认每个图片引用都有对应 PDF；PNG→PDF 收尾后可加 `--require-no-png`。
