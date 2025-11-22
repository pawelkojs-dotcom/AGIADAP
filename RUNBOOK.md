
# RUNBOOK — Repro + Unified Figures (fig1–fig4)

This runbook explains how to **reproduce** the core experiments and how to **consolidate**
all plots into a single, publication‑ready style (`fig1.png`–`fig4.png`).

> **Outputs (after `make figures`):**
>
> - [fig1.png](sandbox:/mnt/data/fig1.png) — Multi‑Layer Intentional Agent: overview  
> - [fig2.png](sandbox:/mnt/data/fig2.png) — Scaling study  
> - [fig3.png](sandbox:/mnt/data/fig3.png) — Consolidation (real multi‑layer)  
> - [fig4.png](sandbox:/mnt/data/fig4.png) — Consolidation (single‑layer baseline)

---

## 1) Requirements

- Python 3.9+ with NumPy and Matplotlib (already available in this environment)
- Source scripts present in `/mnt/data`:
  - `consolidation_study.py`
  - `consolidation_single_layer.py`
  - `scaling_study (2).py`
- Existing raw PNGs (if you don’t want to re‑run experiments):
  - `multi_layer_intentionality (1).png`
  - `scaling_study (1).png`
  - `consolidation_real_model.png`
  - `consolidation_single_layer.png`

The pipeline is aligned with the **AGI Adaptonics** starter kit and its operational workflow (Two‑line law; σ–Θ–γ; falsifiability gates). See the project **ROADMAP**, **Startup Kit**, and **Kernel** for canonical definitions and milestones.  

---

## 2) Quick Start (most users)

```bash
# Build all consolidated figures (uses existing PNGs if present)
make figures

# Build a single figure
make fig3

# Bundle into ./artifacts/
make dist
```

The figure style is defined in `figures/paper_style.py` and applied by `figures/build_figures.py`.
All titles, margins, fonts, grids, and color cycles are unified, color‑blind‑safe, and publication‑ready.

---

## 3) Full Reproduction (optional)

If you want to regenerate the raw plots from scratch:

```bash
# Re-run experiments and regenerate the raw source PNGs
make repro

# Then rebuild the unified figures
make figures
```

Notes:
- `repro` calls:
  - `python consolidation_study.py` → `consolidation_real_model.png`
  - `python consolidation_single_layer.py` → `consolidation_single_layer.png`
  - `python 'scaling_study (2).py'` → `scaling_study.png` (or `scaling_study (1).png`)
- After these complete, `make figures` wraps each PNG into a **consistent frame** with a common title, caption, and margins.

---

## 4) Figure Map (what each file shows)

- **fig1** — *Multi‑Layer Intentional Agent: Complete Analysis.*  
  Six panels: coherence σ, intentionality α, effective layers n_eff, indirect information ratio, semantic dimension d_sem, and task success.

- **fig2** — *Scaling Study.*  
  System‑size scaling (N=5→100) for intentionality metrics, performance, and compute time.

- **fig3** — *Consolidation (Real Multi‑Layer).*  
  Probability of reaching R4, transition time, and time spent in R4.

- **fig4** — *Consolidation (Single‑Layer Baseline).*  
  Four experiments (A–D): scaling in N, scaling in d, long runs, and ablations.

---

## 5) Style Guide (in code)

The style is defined once in `figures/paper_style.py`:
- Colorblind‑safe palette
- DejaVu Sans typography
- Thin spines, outward ticks
- Grid on y only
- 300 dpi export with tight bounding box

You can tweak the palette or font sizes there; all figures will update on the next build.

---

## 6) Troubleshooting

- **Make can’t find Python:** set `PYTHON=/path/to/python` (e.g., `make PYTHON=python3 figures`).
- **Spaces in filenames:** the Makefile quotes paths that contain spaces (e.g., `scaling_study (2).py`).
- **No raw PNGs present:** run `make repro` or place PNGs in `/mnt/data` under the expected names.
- **Different file names:** edit `DEFAULT_SOURCES` in `figures/build_figures.py` to point to your PNGs.

---

## 7) Provenance & Canon

- Workflow and milestones follow the **ROADMAP** and **Starter Kit** for the AGI Adaptonics thread.  
- Figures correspond to the **σ–Θ–γ** formalism and the two‑line law (Kernel) used system‑wide.

Happy reproducing!
