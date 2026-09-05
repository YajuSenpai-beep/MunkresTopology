# ============================================================
#  Munkres Topology — Build System
#  Usage:
#    make        Build complete PDF via latexmk (auto-converge: xelatex+biber+makeindex)
#    make index  Rebuild index only (xelatex + makeindex + xelatex×2)
#    make quick  Single xelatex pass (fast debug)
#    make bib    Rebuild bibliography only (xelatex + biber + xelatex)
#    make clean  Clean intermediate files (keep PDF + .ist)
#    make dist   Deep clean (keep only source)
# ------------------------------------------------------------
#  NOTE: `make` 用 latexmk 自动跑到收敛,以确保 hyperref /PageLabels 与书印页码一致
#        (未收敛时 /PageLabels 可能把正文起点记错,导致阅读器页码偏 ~3 页)。
# ============================================================

TARGET  = Topology_by_Munkres
SRC_DIR = chapters
TEX_SRC = $(wildcard $(SRC_DIR)/*.tex)
STY     = TopologyBook.sty
IST     = $(TARGET).ist
MAIN    = $(TARGET).tex
LATEXMK = latexmk -pdf -xelatex -interaction=nonstopmode
XELATEX = xelatex -interaction=nonstopmode
INDEXER = makeindex -s $(IST) $(TARGET).idx

.PHONY: all index quick bib clean dist temp

# ---- full build (first time / release) ----
all: $(TARGET).pdf

# latexmk 自动重复编译至收敛,并自动调用 biber/makeindex
$(TARGET).pdf: $(MAIN) $(STY) $(IST) $(TEX_SRC)
	$(LATEXMK) --shell-escape $(MAIN)

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