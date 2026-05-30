# ============================================================
#  Munkres Topology — Build System
#  Usage:
#    make        Build complete PDF (xelatex×3 + biber + makeindex)
#    make index  Rebuild index only (xelatex + makeindex + xelatex×2)
#    make quick  Single xelatex pass (fast debug)
#    make bib    Rebuild bibliography only (xelatex + biber + xelatex)
#    make clean  Clean intermediate files (keep PDF + .ist)
#    make dist   Deep clean (keep only source)
# ============================================================

TARGET  = Topology_by_Munkres
SRC_DIR = chapters
TEX_SRC = $(wildcard $(SRC_DIR)/*.tex)
STY     = TopologyBook.sty
IST     = $(TARGET).ist
MAIN    = $(TARGET).tex
XELATEX = xelatex -interaction=nonstopmode
INDEXER = makeindex -s $(IST) $(TARGET).idx

.PHONY: all index quick bib clean dist temp

# ---- full build (first time / release) ----
all: $(TARGET).pdf

$(TARGET).pdf: $(MAIN) $(STY) $(IST) $(TEX_SRC)
	$(XELATEX) --shell-escape $(MAIN)
	biber $(TARGET)
	$(INDEXER)
	$(XELATEX) $(MAIN)
	$(XELATEX) $(MAIN)

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