"""Figures for chapter 4, drawn from the result files of the research repo.

    python figures/scripts/make_figures.py /path/to/representation_alignment

Writes figures/ch4/{budget_curve,grid_search,standard_cell,rewriting,cross_entropy}.{pdf,png}.
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


CORPORA = [("Corpus NQ", "results/v7_2/main"), ("legal128w", "results/legal128w/v7_2/main")]


def load(rel):
    return json.loads((ROOT / rel).read_text())


def grid():
    """Hybrid word-F1 over supervision fraction and temperature, seed 1, 500 selection prompts."""
    alphas = [0.8, 0.9, 0.95, 0.99]
    mults = [0.25, 0.5, 1, 2, 4]
    fig, axes = plt.subplots(1, 2, figsize=(6.6, 2.7))
    for ax, (name, root) in zip(axes, CORPORA):
        d = load(f"{root}/mixed-w46-grid.json")
        cells = d["seeds"]["1"]["cells"]
        taus = d["setting"]["tau_grid"]
        assert len(taus) == len(mults)
        z = []
        for a in alphas:
            row = []
            for t in taus:
                keys = [k for k in cells if k.startswith(f"b90/a{a:g}/sq/") and f"/t{t:g}/" in k]
                assert len(keys) == 1, (a, t, keys)
                row.append(cells[keys[0]]["final"]["macro_f1"])
            z.append(row)
        sup = cells["b90/a1/r1/L90-span9"]["final"]["macro_f1"]
        hi = max(max(r) for r in z)
        ax.imshow(z, cmap="Blues", vmin=0, vmax=hi, aspect="auto")
        for i, row in enumerate(z):
            for j, v in enumerate(row):
                ax.text(j, i, f"{v:.2f}", ha="center", va="center", fontsize=8,
                        color="white" if v > 0.6 * hi else INK)
        i, j = alphas.index(0.9), mults.index(2)
        ax.add_patch(plt.Rectangle((j - 0.5, i - 0.5), 1, 1, fill=False, edgecolor=ORANGE, lw=1.8))
        ax.set_xticks(range(len(mults)))
        ax.set_xticklabels([f"{m:g}d" for m in mults])
        ax.set_yticks(range(len(alphas)))
        ax.set_yticklabels([f"{a:g}" for a in alphas])
        ax.set_xlabel("temperature")
        ax.set_title(f"{name} (supervised fit {sup:.2f})", fontsize=9)
        for side in ("left", "bottom"):
            ax.spines[side].set_visible(False)
        ax.tick_params(length=0)
        print(name, "supervised", round(sup, 4), [[round(v, 4) for v in r] for r in z])
    axes[0].set_ylabel("supervision fraction")
    fig.tight_layout()
    save(fig, "ch4/grid_search")


def standard():
    """Hybrid against supervised fit at the selected setting, 4,500 held-out prompts, three seeds."""
    fig, ax = plt.subplots(figsize=(4.4, 2.9))
    width = 0.34
    for i, (name, root) in enumerate(CORPORA):
        per = {"supervised fit": [], "hybrid fit": []}
        for s in "123":
            d = load(f"{root}/w46-confirmation-s{s}.json")
            assert d["prompts"] == 4500 and d["population"] == "confirmation"
            for key, cell in d["cells"].items():
                per["supervised fit" if "/a1/" in key else "hybrid fit"].append(cell["macro_f1"])
        for k, (label, color) in enumerate((("supervised fit", VIOLET), ("hybrid fit", GREEN))):
            vals = per[label]
            assert len(vals) == 3
            x = i + (k - 0.5) * width
            mean = sum(vals) / 3
            ax.bar(x, mean, width * 0.92, color=color, alpha=0.85, label=label if i == 0 else None)
            ax.scatter([x] * 3, vals, s=9, color=INK, zorder=3, linewidths=0)
            ax.annotate(f"{mean:.2f}", (x, max(vals)), xytext=(0, 3), textcoords="offset points",
                        ha="center", fontsize=8, color=INK)
            print(name, label, round(mean, 4), [round(v, 4) for v in vals])
    ax.set_xticks(range(len(CORPORA)))
    ax.set_xticklabels([c[0] for c in CORPORA])
    ax.set_ylim(0, 1.0)
    ax.set_ylabel("word-F1 (mean of three decoders)")
    ax.grid(axis="y")
    ax.set_axisbelow(True)
    ax.legend(loc="upper right", fontsize=8)
    fig.tight_layout()
    save(fig, "ch4/standard_cell")


def rewriting():
    """Word-F1 before and after the second-round language model, 450 selection prompts, seed 1."""
    files = [
        ("Corpus NQ\nbudget 10", "results/v7_2/main/framework/attacker/attacker-b10-a0.95-sq-m0-t0.1152-r1-B8192-s1-haiku.json"),
        ("legal128w\nbudget 10", "results/legal128w/v7_2/main/framework/attacker/attacker-b10-a0.95-sq-m0-t0.1297-r1-B8192-s1-haiku.json"),
        ("legal128w\nbudget 100", "results/legal128w/v7_2/main/framework/attacker/attacker-b100-a0.95-sq-m0-t0.1297-r1-B8192-s1-haiku.json"),
    ]
    series = [("decoders, mean of three", INK2), ("rewrite of one reconstruction", BLUE), ("rewrite of three reconstructions", ORANGE)]
    fig, ax = plt.subplots(figsize=(5.2, 2.9))
    width = 0.26
    for i, (name, rel) in enumerate(files):
        d = load(rel)
        assert d["prompts_reported"] == 450 and d["model"].startswith("claude-haiku")
        a, b = d["table"]["hybrid rung A"]["word_f1"], d["table"]["hybrid rung B"]["word_f1"]
        vals = [b["before"], a["after"], b["after"]]
        for k, ((label, color), v) in enumerate(zip(series, vals)):
            x = i + (k - 1) * width
            ax.bar(x, v, width * 0.92, color=color, alpha=0.85, label=label if i == 0 else None)
            ax.annotate(f"{v:.2f}", (x, v), xytext=(0, 2), textcoords="offset points", ha="center", fontsize=8)
        print(name.replace("\n", " "), [round(v, 4) for v in vals])
    ax.set_xticks(range(len(files)))
    ax.set_xticklabels([f[0] for f in files])
    ax.set_ylim(0, 1.38)
    ax.set_yticks([0, 0.2, 0.4, 0.6, 0.8, 1.0])
    ax.set_ylabel("word-F1")
    ax.grid(axis="y")
    ax.set_axisbelow(True)
    ax.legend(loc="upper left", fontsize=7.5, ncol=1)
    fig.tight_layout()
    save(fig, "ch4/rewriting")


def cross_entropy():
    """Excess cross-entropy per content word under teacher forcing, against the budget."""
    panels = [
        ("Corpus NQ (three seeds)", "results/v7_2/main/framework/teacher_forced/summary.json", [10, 30, 100],
         "b{b}-a0.95-sq-m0-t0.1152-r1-B8192"),
        ("legal128w (seed 1)", "results/legal128w/v7_2/main/framework/teacher_forced/summary.json", [1, 10, 30, 100],
         "b{b}-a0.95-sq-m0-t0.1297-r1-B8192"),
    ]
    fig, axes = plt.subplots(1, 2, figsize=(6.6, 2.8), sharey=True)
    for ax, (name, rel, budgets, hybrid) in zip(axes, panels):
        arms = load(rel)["arms"]
        get = lambda key: arms[key]["classes"]["content"]["excess_per_word"]
        sup = [get(f"b{b}-a1-r1") for b in budgets]
        hyb = [get(hybrid.format(b=b)) for b in budgets]
        ax.plot(budgets, sup, color=VIOLET, marker="o", ls=(0, (5, 2)), lw=1.6, ms=4.5, label="supervised fit")
        ax.plot(budgets, hyb, color=GREEN, marker="s", lw=1.6, ms=4.5, label="hybrid fit")
        none = get("no_memory")
        ax.axhline(none, color=INK2, lw=0.8, ls=":")
        ax.annotate(f"no memory {none:.2f}", (budgets[0], none), xytext=(0, 3), textcoords="offset points",
                    fontsize=8, color=INK2)
        ax.set_xscale("log")
        ax.set_xticks(budgets)
        ax.set_xticklabels([str(b) for b in budgets])
        ax.minorticks_off()
        ax.set_xlabel("budget (paired sequences)")
        ax.set_title(name, fontsize=9)
        ax.grid(axis="y")
        print(name, "supervised", [round(v, 4) for v in sup], "hybrid", [round(v, 4) for v in hyb], "none", round(none, 4))
    axes[0].set_ylabel("excess cross-entropy\n(nats per content word)")
    axes[0].set_ylim(0, 8.5)
    axes[1].legend(loc="upper right", fontsize=8)
    fig.tight_layout()
    save(fig, "ch4/cross_entropy")


grid()
standard()
rewriting()
cross_entropy()
