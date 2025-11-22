
# Makefile — Repro + unified figures (fig1–fig4)
# Usage:
#   make figures       # build fig1..fig4 with a unified style
#   make fig1          # build a single figure
#   make repro         # (optional) rerun experiments to regenerate raw PNGs
#   make clean         # remove generated fig*.png
#   make dist          # create ./artifacts/ with figures

PYTHON ?= python3
FIGDIR := figures

# --- Default target
.PHONY: all
all: figures

# --- Style + wrappers
.PHONY: figures fig1 fig2 fig3 fig4
figures: fig1 fig2 fig3 fig4

fig1:
	$(PYTHON) -m figures.build_figures --fig fig1 --outdir /mnt/data

fig2:
	$(PYTHON) -m figures.build_figures --fig fig2 --outdir /mnt/data

fig3:
	$(PYTHON) -m figures.build_figures --fig fig3 --outdir /mnt/data

fig4:
	$(PYTHON) -m figures.build_figures --fig fig4 --outdir /mnt/data

# --- Optional: rerun underlying experiments to refresh the source PNGs
.PHONY: repro repro-consolidation repro-scaling
repro: repro-consolidation repro-scaling

repro-consolidation:
	# Real multi-layer consolidation
	$(PYTHON) '/mnt/data/consolidation_study.py'
	# Single-layer baseline consolidation
	$(PYTHON) '/mnt/data/consolidation_single_layer.py'

repro-scaling:
	# Scaling study (file name contains a space on this system)
	$(PYTHON) '/mnt/data/scaling_study (2).py'

# --- Hygiene
.PHONY: clean dist
clean:
	rm -f /mnt/data/fig1.png /mnt/data/fig2.png /mnt/data/fig3.png /mnt/data/fig4.png

dist: figures
	mkdir -p artifacts
	cp -f /mnt/data/fig1.png artifacts/
	cp -f /mnt/data/fig2.png artifacts/
	cp -f /mnt/data/fig3.png artifacts/
	cp -f /mnt/data/fig4.png artifacts/
	@echo "Artifacts ready in ./artifacts"

