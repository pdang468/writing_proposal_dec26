"""Figure for chapter 4, drawn from the result files of the research repo.

    python figures/scripts/make_figures.py /path/to/representation_alignment

Writes figures/ch4/budget_curve.{pdf,png}.
Sources: results/v7_2/main/mixed-v7_9-s5.json and, for the hub reference, results/v7_2/main/factorial.json
(controls.true_olmo_code). Seeds, prompt counts and cell names are read from those files.
"""
import json
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(sys.argv[1])
OUT = Path(__file__).resolve().parents[1]
INK, INK2, GRID = "#0b0b0b", "#52514e", "#e6e5e1"
BLUE, ORANGE, VIOLET, GREEN = "#2a78d6", "#eb6834", "#6250d6", "#008300"
plt.rcParams.update({
    "font.family": "serif", "font.size": 9, "axes.edgecolor": INK2, "axes.linewidth": 0.6,
    "axes.spines.top": False, "axes.spines.right": False, "xtick.color": INK2, "ytick.color": INK2,
    "axes.labelcolor": INK, "grid.color": GRID, "grid.linewidth": 0.6, "legend.frameon": False,
    "pdf.fonttype": 42,
})


def save(fig, rel):
    path = OUT / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path.with_suffix(".pdf"))
    fig.savefig(path.with_suffix(".png"), dpi=200)
    plt.close(fig)
    print(path.with_suffix(".pdf"))


def budget():
    d = json.loads((ROOT / "results/v7_2/main/mixed-v7_9-s5.json").read_text())
    reference = json.loads((ROOT / "results/v7_2/main/factorial.json").read_text())
    g2 = reference["controls"]["true_olmo_code"]["macro_f1"]
    budgets = [10, 30, 100, 300, 1000]
    series = {
        "supervised fit": (lambda b: f"b{b}/a1/r1", VIOLET, "o", (0, (5, 2))),
        "hybrid fit": (lambda b: f"b{b}/a0.95/sq/m0/t0.1152/r1/B2048", GREEN, "s", "-"),
    }
    seeds = sorted(d["seeds"])
    assert seeds == ["1", "2", "3"]
    fig, ax = plt.subplots(figsize=(4.6, 3.1))
    wrong = []
    for label, (cell, color, marker, ls) in series.items():
        per = [[d["seeds"][s]["cells"][cell(b)]["final"]["macro_f1"] for s in seeds] for b in budgets]
        wrong += [d["seeds"][s]["cells"][cell(b)]["wrong_memory"]["macro_f1"] for s in seeds for b in budgets]
        mean = [sum(p) / len(p) for p in per]
        ax.fill_between(budgets, [min(p) for p in per], [max(p) for p in per], color=color, alpha=0.18, lw=0)
        ax.plot(budgets, mean, color=color, marker=marker, ls=ls, lw=1.6, ms=4.5,
                markeredgecolor="white", markeredgewidth=0.6, label=label)
        print(label, [round(m, 3) for m in mean])
    ax.axhline(g2, color=INK2, lw=0.8, ls=":")
    ax.annotate(f"hub reference {g2:.3f}", (10, g2), xytext=(0, 3), textcoords="offset points", fontsize=8, color=INK2)
    ax.axhspan(min(wrong), max(wrong), color=INK2, alpha=0.15, lw=0)
    ax.annotate(f"mismatched-prompt control {min(wrong):.2f} to {max(wrong):.2f}", (10, max(wrong)), xytext=(0, 3),
                textcoords="offset points", fontsize=8, color=INK2)
    print("wrong memory range", min(wrong), max(wrong))
    ax.set_xscale("log")
    ax.set_xticks(budgets)
    ax.set_xticklabels([str(b) for b in budgets])
    ax.minorticks_off()
    ax.set_ylim(0, 1.02)
    ax.set_xlabel("budget (paired sequences)")
    ax.set_ylabel("word-F1 (mean of three decoders)")
    ax.grid(axis="y")
    ax.legend(loc="center right", fontsize=8, handlelength=2.6)
    fig.tight_layout()
    save(fig, "ch4/budget_curve")


budget()
