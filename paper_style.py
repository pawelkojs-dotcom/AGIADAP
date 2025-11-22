
"""
figures/paper_style.py — unified, publication‑ready Matplotlib style for Adaptonics (fig1–fig4)
- Colorblind‑safe palette
- Consistent typography
- Clean axes with thin spines and outward ticks
- Grid for y only
"""
from matplotlib import rcParams

PALETTE = [
    "#1b9e77",  # teal
    "#d95f02",  # orange
    "#7570b3",  # indigo
    "#e7298a",  # magenta
    "#66a61e",  # green
    "#e6ab02",  # gold
    "#a6761d",  # brown
    "#1f78b4",  # blue
]

def apply():
    # Typography
    rcParams["font.family"] = "DejaVu Sans"
    rcParams["font.size"] = 10
    rcParams["axes.titlesize"] = 12
    rcParams["axes.labelsize"] = 11
    rcParams["figure.titlesize"] = 14
    rcParams["legend.fontsize"] = 9
    rcParams["xtick.labelsize"] = 9
    rcParams["ytick.labelsize"] = 9
    # Layout
    rcParams["figure.dpi"] = 120
    rcParams["savefig.dpi"] = 300
    rcParams["savefig.bbox"] = "tight"
    rcParams["savefig.pad_inches"] = 0.05
    rcParams["axes.linewidth"] = 0.8
    rcParams["xtick.direction"] = "out"
    rcParams["ytick.direction"] = "out"
    rcParams["axes.spines.right"] = False
    rcParams["axes.spines.top"] = False
    rcParams["axes.grid"] = True
    rcParams["grid.linestyle"] = ":"
    rcParams["grid.color"] = "#cccccc"
    rcParams["grid.alpha"] = 0.7
    rcParams["axes.prop_cycle"] = __import__("matplotlib").cycler(color=PALETTE)
    # Figure defaults
    rcParams["figure.facecolor"] = "white"
    rcParams["axes.facecolor"] = "white"
    rcParams["legend.frameon"] = False
    rcParams["errorbar.capsize"] = 3
    # Tight layout slightly looser for composite images
    rcParams["figure.autolayout"] = False
