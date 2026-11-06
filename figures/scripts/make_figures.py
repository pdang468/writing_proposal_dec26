"""Figures for chapters 3 and 4, drawn from the result files of the research repo.

    python figures/scripts/make_figures.py /path/to/representation_alignment

Writes figures/ch3/noise_tolerance.{pdf,png} and figures/ch4/budget_curve.{pdf,png}.
Sources: results/v7_2/main/oct_w5c-noise.json, results/legal128w/v7_2/main/oct_w5c-noise.json,
results/v7_2/main/mixed-v7_9-s5.json. Seeds, prompt counts and cell names are read from those files.
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


def noise():
    files = {"legal128w": ROOT / "results/legal128w/v7_2/main/oct_w5c-noise.json",
             "Corpus A": ROOT / "results/v7_2/main/oct_w5c-noise.json"}
    style = {"legal128w": (BLUE, "o", "-"), "Corpus A": (ORANGE, "s", (0, (5, 2)))}
    data = {name: json.loads(path.read_text()) for name, path in files.items()}
    fig, axes = plt.subplots(1, 2, figsize=(6.3, 2.9), sharey=True)
    for ax, (family, title) in zip(axes, [("iso", "Isotropic noise"), ("cov", "Covariance-shaped noise")]):
        for name, d in data.items():
            assert d["prompts"] == 500
            levels = d["levels"]
            ys = [d["sets"]["iso-r0" if r == 0 else f"{family}-r{r:g}"]["macro_word_f1"] for r in levels]
            color, marker, ls = style[name]
            ax.plot(levels, ys, color=color, marker=marker, ls=ls, lw=1.6, ms=4.5,
                    markeredgecolor="white", markeredgewidth=0.6, label=name, clip_on=False)
        ax.axvline(0.4, color=INK2, lw=0.6, ls=":")
        ax.set_title(title, fontsize=9, color=INK, loc="left")
        ax.set_xlabel(r"relative error $r$ (units of $\rho_H$)")
        ax.set_xticks([0, 0.2, 0.4, 0.6, 0.8, 1.0])
        ax.set_ylim(0, 1.02)
        ax.grid(axis="y")
    axes[0].set_ylabel("macro word-F1")
    axes[1].annotate("$r = 0.4$", (0.4, 0.06), xytext=(4, 0), textcoords="offset points", color=INK2, fontsize=8)
    axes[0].legend(loc="lower left", fontsize=8, handlelength=2.6)
    fig.tight_layout()
    save(fig, "ch3/noise_tolerance")


def budget():
    d = json.loads((ROOT / "results/v7_2/main/mixed-v7_9-s5.json").read_text())
    noise_a = json.loads((ROOT / "results/v7_2/main/oct_w5c-noise.json").read_text())
    g2 = noise_a["sets"]["iso-r0"]["macro_word_f1"]
    budgets = [10, 30, 100, 300, 1000]
    series = {
        "supervised (residual + ridge)": (lambda b: f"b{b}/a1/r1", VIOLET, "o", (0, (5, 2))),
        "hybrid": (lambda b: f"b{b}/a0.95/sq/m0/t0.1152/r1/B2048", GREEN, "s", "-"),
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
    ax.annotate(f"hub ceiling G2 {g2:.3f}", (10, g2), xytext=(0, 3), textcoords="offset points", fontsize=8, color=INK2)
    ax.axhspan(min(wrong), max(wrong), color=INK2, alpha=0.15, lw=0)
    ax.annotate(f"wrong memory {min(wrong):.2f} to {max(wrong):.2f}", (10, max(wrong)), xytext=(0, 3),
                textcoords="offset points", fontsize=8, color=INK2)
    print("wrong memory range", min(wrong), max(wrong))
    ax.set_xscale("log")
    ax.set_xticks(budgets)
    ax.set_xticklabels([str(b) for b in budgets])
    ax.minorticks_off()
    ax.set_ylim(0, 1.02)
    ax.set_xlabel("budget (paired prompts)")
    ax.set_ylabel("macro word-F1")
    ax.grid(axis="y")
    ax.legend(loc="center right", fontsize=8, handlelength=2.6)
    fig.tight_layout()
    save(fig, "ch4/budget_curve")


noise()
budget()
