# ============================================================
#  Munkres Topology — Build System
#  Usage:
#    make        Build complete PDF via latexmk (auto-converge: xelatex+biber+makeindex)
#    make cover  Build cover-only PDF (Cover.tex → Cover.pdf)
#    make figures Rebuild hand-rebuilt illustration PDFs (figures_src/ → images/)
#    make index  Rebuild index only (xelatex + makeindex + xelatex×2)
#    make quick  Single xelatex pass (fast debug)
#    make bib    Rebuild bibliography only (xelatex + biber + xelatex)
#    make clean  Clean intermediate files (keep PDF + .ist)
#    make dist   Deep clean (keep only source)
# ------------------------------------------------------------
#  NOTE: `make` 用 latexmk 自动跑到收敛,以确保 hyperref /PageLabels 与书印页码一致
#        (未收敛时 /PageLabels 可能把正文起点记错,导致阅读器页码偏 ~3 页)。
#
#  NOTE: 封面(Cover.tex, 三栏跨页 45cm)与内文分开编译 —— 内文统一 21cm,
#        避免阅读器按最宽页缩放导致正文页显示偏左;印刷时封面本也单独出片。
# ============================================================

TARGET  = Topology_by_Munkres
COVER   = Cover
SRC_DIR = chapters
TEX_SRC = $(wildcard $(SRC_DIR)/*.tex)
FIG_SRC = figures_src
FIG_TEX = $(wildcard $(FIG_SRC)/fig_*.tex)
# figures_src/fig_2.2.tex → images/2.2.pdf（去掉 fig_ 前缀：书里引用的是图号）
FIG_PDF = $(patsubst $(FIG_SRC)/fig_%.tex,images/%.pdf,$(FIG_TEX))
# ⚠ 插图必须进依赖表：否则换了图 `make` 会说「无事可做」，出的还是旧 PDF。
IMAGES  = $(wildcard images/*.png) $(wildcard images/*.pdf) $(wildcard images/*.svg)
STY     = TopologyBook.sty
IST     = $(TARGET).ist
MAIN    = $(TARGET).tex
LATEXMK = latexmk -pdf -xelatex -interaction=nonstopmode
XELATEX = xelatex -interaction=nonstopmode
INDEXER = makeindex -s $(IST) $(TARGET).idx

.PHONY: all index quick bib clean dist temp cover figures

# ---- full build (first time / release) ----
all: $(TARGET).pdf $(COVER).pdf

# latexmk 自动重复编译至收敛,并自动调用 biber/makeindex
$(TARGET).pdf: $(MAIN) $(STY) $(IST) $(TEX_SRC) Bibliography.bib $(FIG_PDF) $(IMAGES)
	$(LATEXMK) --shell-escape $(MAIN)

# ---- cover only (跨页封面；TikZ overlay 需两趟定坐标) ----
$(COVER).pdf: $(COVER).tex $(SRC_DIR)/cover2.tex
	$(XELATEX) --shell-escape $(COVER).tex
	$(XELATEX) --shell-escape $(COVER).tex

cover: $(COVER).pdf

# ---- 手工重建插图的编译产物（figures_src/fig_N.M.tex → images/N.M.pdf）----
# 书里 \munkresfig 的 \includegraphics 不带扩展名，**优先 PDF**，
# 所以产物一进 images/ 就自动取代同名 PNG，章节 .tex 不用改。
# ⚠ 只在 figures_src/ 里编（standalone 文档，靠本目录外的文件会编不过）；
#   产物必须去掉 fig_ 前缀落到 images/ 下。
figures: $(FIG_PDF)

images/%.pdf: $(FIG_SRC)/fig_%.tex
	cd $(FIG_SRC) && $(XELATEX) fig_$*.tex
	mv $(FIG_SRC)/fig_$*.pdf $@
	rm -f $(FIG_SRC)/fig_$*.aux $(FIG_SRC)/fig_$*.log

# ---- index-only rebuild ----
index:
	$(XELATEX) $(MAIN)
	$(INDEXER)
	$(XELATEX) $(MAIN)
	$(XELATEX) $(MAIN)

# ---- bibliography-only rebuild ----
bib:
	$(XELATEX) $(MAIN)
	biber $(TARGET)
	$(XELATEX) $(MAIN)

# ---- single pass (syntax check) ----
quick:
	$(XELATEX) $(MAIN)

# ---- legacy alias ----
temp: quick

# ---- clean intermediate files (keep PDF + .ist) ----
clean:
	latexmk -c
	rm -f *.ilg

# ---- deep clean (keep only source) ----
dist:
	latexmk -C
	rm -f *.bbl *.gz *.ilg *.xdv