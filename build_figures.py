
"""
figures/build_figures.py — consolidate project plots into a unified paper style (fig1–fig4).
This script is robust: if raw scripts/JSON are not available, it will fall back to
wrapping the existing PNGs into consistently titled canvases.
"""
import os
import argparse
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from textwrap import fill

# Apply unified style
from .paper_style import apply as apply_style
apply_style()

# Known default sources from the current workspace
DEFAULT_SOURCES = {
    "fig1": {
        "title": "Figure 1 — Multi‑Layer Intentional Agent: Complete Analysis",
        "src_candidates": [
            "/mnt/data/multi_layer_intentionality (1).png",
            "/mnt/data/multi_layer_intentionality.png",
        ],
        "caption": "Six‑panel overview: coherence σ, intentionality α, effective layers n_eff, indirect information ratio, semantic dimension d_sem, and task success."
    },
    "fig2": {
        "title": "Figure 2 — Scaling Study: Multi‑Layer Intentional System",
        "src_candidates": [
            "/mnt/data/scaling_study (1).png",
            "/mnt/data/scaling_study.png",
        ],
        "caption": "N=5→100 scaling across intentionality metrics, performance, and computational cost."
    },
    "fig3": {
        "title": "Figure 3 — Consolidation (Real Multi‑Layer Model)",
        "src_candidates": [
            "/mnt/data/consolidation_real_model.png",
        ],
        "caption": "Probability of reaching R4, transition time, and time spent in R4 for the real multi‑layer model."
    },
    "fig4": {
        "title": "Figure 4 — Consolidation Baseline (Single‑Layer σ‑Θ‑γ)",
        "src_candidates": [
            "/mnt/data/consolidation_single_layer.png",
        ],
        "caption": "Baseline single‑layer consolidation: experiments A–D (scaling in N, scaling in d, long‑run stability, ablations)."
    },
}

def _pick_first_existing(paths):
    for p in paths:
        if os.path.exists(p):
            return p
    return None

def _compose_from_png(src_png, title, out_png, caption=None):
    img = mpimg.imread(src_png)
    # Create a canvas with unified margins
    fig = plt.figure(figsize=(13, 8))  # landscape A4-ish
    ax = fig.add_axes([0.03, 0.12, 0.94, 0.83])
    ax.imshow(img)
    ax.axis("off")
    # Title
    fig.suptitle(title, y=0.98, fontweight="bold")
    # Caption (wrapped)
    if caption:
        fig.text(0.03, 0.035, fill(caption, 140), ha="left", va="bottom", color="#444444")
    # Subtle border
    for spine in ["left", "right", "top", "bottom"]:
        ax.spines[spine].set_visible(False)
    # Save
    fig.savefig(out_png)
    plt.close(fig)

def build_one(fig_id, cfg, outdir):
    src = _pick_first_existing(cfg["src_candidates"])
    if not src:
        raise FileNotFoundError(f"No source image found for {fig_id}. Tried: {cfg['src_candidates']}")
    out = os.path.join(outdir, f"{fig_id}.png")
    _compose_from_png(src, cfg["title"], out, cfg.get("caption"))
    return out

def build_all(outdir):
    os.makedirs(outdir, exist_ok=True)
    outs = {}
    for fig_id, cfg in DEFAULT_SOURCES.items():
        outs[fig_id] = build_one(fig_id, cfg, outdir)
    return outs

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--fig", choices=list(DEFAULT_SOURCES.keys()), help="Build a single figure by id")
    parser.add_argument("--outdir", default="/mnt/data", help="Output directory")
    parser.add_argument("--all", action="store_true", help="Build all figures (fig1–fig4)")
    args = parser.parse_args()

    if args.fig:
        out = build_one(args.fig, DEFAULT_SOURCES[args.fig], args.outdir)
        print(out)
    else:
        # default: build all
        outs = build_all(args.outdir)
        for k, v in outs.items():
            print(f"{k}: {v}")

if __name__ == "__main__":
    main()
