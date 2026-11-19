"""Figures for chapter 4, drawn from the result files of the research repo.

    python figures/scripts/make_figures.py /path/to/representation_alignment

Writes figures/ch4/{budget_curve,grid_search,standard_cell,rewriting,cross_entropy,leak_shape,grid_leak_size,budget_curve_legal}.{pdf,png}.
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
BLUE, ORANGE = "#2a78d6", "#eb6834"
HYBRID, SUPERVISED = "#4c72b0", "#dd8452"
plt.rcParams.update({
    "font.family": "serif", "font.size": 9, "axes.edgecolor": INK2, "axes.linewidth": 0.6,
    "axes.spines.top": False, "axes.spines.right": False, "xtick.color": INK2, "ytick.color": INK2,
    "axes.labelcolor": INK, "grid.color": GRID, "grid.linewidth": 0.6, "legend.frameon": False,
    "pdf.fonttype": 42,
})


def save(fig, rel):
    import matplotlib.text, matplotlib.ticker
    def shown(s):  # names as the dissertation prints them: legal128w in result files is legal100t in the text
        return s.replace("legal128w", "legal100t").replace(" (seed 1)", "").replace(" (three seeds)", "")
    renamed = False
    for ax in fig.axes:
        for axis in (ax.xaxis, ax.yaxis):
            fmt = axis.get_major_formatter()
            if isinstance(fmt, matplotlib.ticker.FixedFormatter):
                renamed |= any(shown(s) != s for s in fmt.seq)
                fmt.seq = [shown(s) for s in fmt.seq]
    for text in fig.findobj(matplotlib.text.Text):
        renamed |= shown(text.get_text()) != text.get_text()
        text.set_text(shown(text.get_text()))
    if renamed:
        print("RENAMED", rel)
    path = OUT / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path.with_suffix(".pdf"))
    fig.savefig(path.with_suffix(".png"), dpi=200)
    plt.close(fig)
    print(path.with_suffix(".pdf"))


def gap(ax, x, low, high):
    """The difference hybrid minus supervised, written beside a bracket at x."""
    ax.annotate("", (x, high), (x, low), arrowprops=dict(arrowstyle="<->", color=INK2, lw=0.8, shrinkA=0, shrinkB=0))
    ax.annotate(f"+{high - low:.2f}", (x, (low + high) / 2), xytext=(3, 0), textcoords="offset points",
                va="center", fontsize=8, color=INK2)


def budget():
    d = json.loads((ROOT / "results/v7_2/main/mixed-v7_9-s5.json").read_text())
    reference = json.loads((ROOT / "results/v7_2/main/factorial.json").read_text())
    g2 = reference["controls"]["true_olmo_code"]["macro_f1"]
    budgets = [10, 30, 100]  # leaks up to 1,500 rows (2026-11-16); 300 and 1,000 prompts hold 3,013 and 9,982 rows
    series = {
        "supervised fit": (lambda b: f"b{b}/a1/r1", SUPERVISED, "o", (0, (5, 2))),
        "hybrid fit": (lambda b: f"b{b}/a0.95/sq/m0/t0.1152/r1/B2048", HYBRID, "s", "-"),
    }
    seeds = sorted(d["seeds"])
    assert seeds == ["1", "2", "3"]
    # leak size in rows: the aligned pairs of each budget's whole prompts, mean over the three seeds
    rows = [round(sum(d["seeds"][s]["budgets"][str(b)]["anchor_counts"]["valid_aligned_pairs"] for s in seeds) / 3) for b in budgets]
    print("Corpus A rows per budget", dict(zip(budgets, rows)))
    fig, ax = plt.subplots(figsize=(4.6, 3.1))
    wrong = []
    for label, (cell, color, marker, ls) in series.items():
        per = [[d["seeds"][s]["cells"][cell(b)]["final"]["macro_f1"] for s in seeds] for b in budgets]
        wrong += [d["seeds"][s]["cells"][cell(b)]["wrong_memory"]["macro_f1"] for s in seeds for b in budgets]
        mean = [sum(p) / len(p) for p in per]
        ax.fill_between(rows, [min(p) for p in per], [max(p) for p in per], color=color, alpha=0.18, lw=0)
        ax.plot(rows, mean, color=color, marker=marker, ls=ls, lw=1.6, ms=4.5,
                markeredgecolor="white", markeredgewidth=0.6, label=label)
        print(label, [round(m, 3) for m in mean])
    ax.axhline(g2, color=INK2, lw=0.8, ls=":")
    ax.annotate(f"hub reference {g2:.3f}", (rows[0], g2), xytext=(0, 3), textcoords="offset points", fontsize=8, color=INK2)
    ax.axhspan(min(wrong), max(wrong), color=INK2, alpha=0.15, lw=0)
    ax.annotate(f"mismatched-prompt control {min(wrong):.2f} to {max(wrong):.2f}", (rows[0], max(wrong)), xytext=(0, 3),
                textcoords="offset points", fontsize=8, color=INK2)
    print("wrong memory range", min(wrong), max(wrong))
    ax.set_xscale("log")
    ax.set_xticks(rows)
    ax.set_xticklabels([f"{r:,}" for r in rows])
    ax.minorticks_off()
    ax.set_ylim(0, 1.02)
    ax.set_xlabel("leaked rows")
    ax.set_ylabel("word-F1 (mean of three decoders)")
    ax.grid(axis="y")
    ax.legend(loc="center right", fontsize=8, handlelength=2.6)
    fig.tight_layout()
    save(fig, "ch4/budget_curve")


budget()


CORPORA = [("NQ", "results/v7_2/main"), ("legal128w", "results/legal128w/v7_2/main")]
# the main comparison also runs on legal10w (w46b); the grid search of legal10w is drawn once its job has finished
MAIN = [CORPORA[0], ("legal10w", "results/legal10w/v7_2/main"), CORPORA[1]]  # panel order: NQ, legal10w, legal128w


def load(rel):
    return json.loads((ROOT / rel).read_text())


def grid(rows=90, out="ch4/grid_search"):
    """Hybrid word-F1 over supervision fraction and temperature, seed 1, 500 selection prompts.
    Solid outline: the setting of the main comparison. Dashed outline (grids other than 90 rows): the best cell when it differs."""
    alphas = [0.8, 0.9, 0.95, 0.99]
    mults = [0.25, 0.5, 1, 2, 4]
    fig, axes = plt.subplots(1, 3, figsize=(9.6, 2.7))
    for ax, (name, root) in zip(axes, MAIN):
        d = load(f"{root}/mixed-w46-grid{'' if rows == 90 else f'-L{rows}'}.json")
        cells = d["seeds"]["1"]["cells"]
        taus = d["setting"]["tau_grid"]
        assert len(taus) == len(mults)
        z = []
        for a in alphas:
            row = []
            for t in taus:
                keys = [k for k in cells if k.startswith(f"b{rows}/a{a:g}/sq/") and f"/t{t:g}/" in k]
                assert len(keys) == 1, (a, t, keys)
                row.append(cells[keys[0]]["final"]["macro_f1"])
            z.append(row)
        sup = cells[f"b{rows}/a1/r1/L{rows}-span9"]["final"]["macro_f1"]
        hi = max(max(r) for r in z)
        ax.imshow(z, cmap="Blues", vmin=0, vmax=hi, aspect="auto")
        for i, row in enumerate(z):
            for j, v in enumerate(row):
                ax.text(j, i, f"{v:.2f}", ha="center", va="center", fontsize=8,
                        color="white" if v > 0.6 * hi else INK)
        i, j = alphas.index(0.9), mults.index(2)
        ax.add_patch(plt.Rectangle((j - 0.5, i - 0.5), 1, 1, fill=False, edgecolor=ORANGE, lw=1.8))
        _, bi, bj = max((v, i_, j_) for i_, r in enumerate(z) for j_, v in enumerate(r))
        if rows != 90 and (bi, bj) != (i, j):
            ax.add_patch(plt.Rectangle((bj - 0.5, bi - 0.5), 1, 1, fill=False, edgecolor=ORANGE, lw=1.4, ls="--"))
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
    save(fig, out)


def standard():
    """Hybrid against supervised fit at the selected setting, 4,500 held-out prompts, three seeds."""
    fig, ax = plt.subplots(figsize=(5.6, 2.9))
    width = 0.34
    for i, (name, root) in enumerate(MAIN):
        per = {"supervised fit": [], "hybrid fit": []}
        for s in "123":
            d = load(f"{root}/w46-confirmation-s{s}.json")
            assert d["prompts"] == 4500 and d["population"] == "confirmation"
            for key, cell in d["cells"].items():
                per["supervised fit" if "/a1/" in key else "hybrid fit"].append(cell["macro_f1"])
        for k, (label, color) in enumerate((("supervised fit", SUPERVISED), ("hybrid fit", HYBRID))):
            vals = per[label]
            assert len(vals) == 3
            x = i + (k - 0.5) * width
            mean = sum(vals) / 3
            ax.bar(x, mean, width * 0.92, color=color, label=label if i == 0 else None)
            ax.scatter([x] * 3, vals, s=9, color=INK, zorder=3, linewidths=0)
            ax.annotate(f"{mean:.2f}", (x, max(vals)), xytext=(0, 5), textcoords="offset points",
                        ha="center", fontsize=8, color=INK)
            print(name, label, round(mean, 4), [round(v, 4) for v in vals])
        means = [sum(per[k]) / 3 for k in ("supervised fit", "hybrid fit")]
        gap(ax, i + width + 0.05, means[0], means[1])
    ax.set_xticks(range(len(MAIN)))
    ax.set_xticklabels([c[0] for c in MAIN])
    ax.set_xlim(-0.5, len(MAIN) - 0.25)
    ax.set_ylim(0, 1.0)
    ax.set_ylabel("word-F1 (mean of three decoders)")
    ax.grid(axis="y")
    ax.set_axisbelow(True)
    ax.legend(loc="upper right", fontsize=8)
    fig.tight_layout()
    save(fig, "ch4/standard_cell")


def rewriting():
    """Second-round rewriting against the best single decoder, 90-row leak, 450 selection prompts, three datasets."""
    panels = [("NQ", "results/v7_2/main"), ("legal10w", "results/legal10w/v7_2/main"), ("legal100t", "results/legal128w/v7_2/main")]
    series = [("SmolLM decoder alone (round 1)", "#b9b8b3", "smollm"), ("rewrite of the SmolLM reconstruction", BLUE, "rewrite of smollm"),
              ("rewrite of all three reconstructions", ORANGE, "rewrite of three")]
    fig, ax = plt.subplots(figsize=(6.0, 3.0))
    width = 0.26
    for i, (name, root) in enumerate(panels):
        d = load(f"{root}/framework/attacker/rewriting-best-decoder.json")
        assert d["prompts"] == 450 and d["metrics"]["folded"]["best_decoder"] == "smollm"
        m = d["metrics"]["folded"]
        for k, (label, color, key) in enumerate(series):
            x, v = i + (k - 1) * width, m["mean"][key]
            ax.bar(x, v, width * 0.92, color=color, label=label if i == 0 else None)
            ax.annotate(f"{v:.2f}", (x, v), xytext=(0, 2), textcoords="offset points", ha="center", fontsize=8, color=INK)
        g = m["gain_rewrite_of_three_over_best"]
        ax.text(i, m["mean"]["rewrite of three"] + 0.075, f"+{g[0]:.2f}", ha="center", fontsize=8.5, color=INK, fontweight="bold")
        c = m["mean"]["control rewrite of three"]
        ax.plot([i - 1.5 * width, i + 1.5 * width], [c, c], color=INK, lw=0.9, ls=":", zorder=5,
                label="mismatched-prompt control" if i == 0 else None)
        print(name, {k: round(v, 4) for k, v in m["mean"].items()}, [round(x, 4) for x in g])
    ax.set_xticks(range(len(panels)))
    ax.set_xticklabels([p_[0] for p_ in panels])
    ax.set_ylim(0, 1.3)
    ax.set_yticks([0, 0.2, 0.4, 0.6, 0.8, 1.0])
    ax.set_ylabel("word-F1")
    ax.grid(axis="y")
    ax.set_axisbelow(True)
    ax.legend(loc="upper right", fontsize=7.5)
    fig.tight_layout()
    save(fig, "ch4/rewriting")


def cross_entropy():
    """Excess cross-entropy per content word under teacher forcing at the 90-row leak, three datasets."""
    panels = [
        ("NQ", "results/v7_2/main/framework/teacher_forced-w46/summary.json", "t0.11522"),
        ("legal10w", "results/legal10w/v7_2/main/framework/teacher_forced-w46/summary.json", "t0.1476"),
        ("legal100t", "results/legal128w/v7_2/main/framework/teacher_forced-w46/summary.json", "t0.1297"),
    ]
    fig, ax = plt.subplots(figsize=(5.6, 2.9))
    width, step = 0.26, 1.0
    series = (("unconditional baseline", "#b9b8b3"), ("supervised fit", SUPERVISED), ("hybrid fit", HYBRID))
    for i, (name, rel, tau) in enumerate(panels):
        arms = load(rel)["arms"]
        get = lambda key: arms[key]["classes"]["content"]["excess_per_word"]
        values = (get("no_memory"), get("b90-a1-r1-L90-span9"), get(f"b90-a0.9-sq-m0-{tau}-r1-B8192-L90-span9"))
        for k, (v, (label, color)) in enumerate(zip(values, series)):
            x = i * step + (k - 1) * width
            ax.bar(x, v, width * 0.92, color=color, label=label if i == 0 else None)
            ax.annotate(f"{v:.2f}", (x, v), xytext=(0, 2), textcoords="offset points", ha="center", fontsize=8, color=INK)
        print(name, "none, supervised, hybrid", [round(v, 4) for v in values])
    ax.set_xticks([i * step for i in range(len(panels))])
    ax.set_xticklabels([p_[0] for p_ in panels])
    ax.set_ylabel("excess cross-entropy\n(nats per content word)")
    ax.set_ylim(0, 12.5)
    ax.grid(axis="y")
    ax.set_axisbelow(True)
    ax.legend(loc="upper right", fontsize=8)
    fig.tight_layout()
    save(fig, "ch4/cross_entropy")


grid()
standard()
rewriting()
cross_entropy()


def bars(ax, groups, width=0.36, step=1.0):
    """Paired bars, supervised then hybrid, with the value above each bar."""
    for i, (sup, hyb) in enumerate(groups):
        for k, (v, color, label) in enumerate(((sup, SUPERVISED, "supervised fit"), (hyb, HYBRID, "hybrid fit"))):
            x = i * step + (k - 0.5) * width
            ax.bar(x, v, width * 0.92, color=color, label=label if i == 0 else None)
            ax.annotate(f"{v:.2f}", (x, v), xytext=(0, 2), textcoords="offset points", ha="center", fontsize=8, color=INK)
        gap(ax, i * step + width + 0.05, sup, hyb)


def leak_shape():
    """90 leaked rows spread over more or fewer prompts at the setting of the main comparison, 500 selection prompts."""
    L = "results/legal128w/v7_2/main"
    H = "a0.9/sq/m0/t0.1297/r1/B8192"
    cell = lambda rel, key: load(rel)["seeds"]["1"]["cells"][key]
    f1 = lambda c: c["final"]["macro_f1"]
    comp = f"{L}/mixed-w46-std-L90-composition.json"
    specs = [
        ("2 prompts\n90 rows", comp, f"b90/{H}/L90-prefix", "b90/a1/r1/L90-prefix"),
        ("10 prompts\n9 rows each", f"{L}/mixed-w46-std.json", f"b90/{H}/L90-span9", "b90/a1/r1/L90-span9"),
        ("90 prompts\n1 row each", comp, f"b90/{H}/L90-random", "b90/a1/r1/L90-random"),
    ]
    groups = []
    for name, rel, hk, sk in specs:
        h, s_ = cell(rel, hk), cell(rel, sk)
        groups.append((f1(s_), f1(h)))
        print(name.replace("\n", " "), "supervised", round(f1(s_), 4), "hybrid", round(f1(h), 4), h.get("anchor_counts"))
    step = 1.4
    fig, ax = plt.subplots(figsize=(5.2, 2.9))
    bars(ax, groups, step=step)
    ax.set_xticks([i * step for i in range(len(specs))])
    ax.set_xticklabels([s_[0] for s_ in specs], fontsize=8)
    ax.set_xlim(-0.5, 2 * step + 0.95)
    ax.set_ylim(0, 0.5)
    ax.set_ylabel("word-F1 (mean of three decoders)")
    ax.grid(axis="y")
    ax.set_axisbelow(True)
    ax.legend(loc="upper left", fontsize=8)
    fig.tight_layout()
    save(fig, "ch4/leak_shape")


def grid_leak_size():
    """The grid of grid() at a leak of 900 rows (nine rows from each of 100 prompts), seed 1, 500 selection prompts."""
    grid(rows=900, out="ch4/grid_leak_size")


def budget_legal(corpus="legal128w", out="ch4/budget_curve_legal"):
    """legal128w: hybrid against supervised fit by budget of whole prompts, seed 1, 500 selection prompts."""
    rows = [r for r in load(f"results/{corpus}/v7_2/main/v8_6-summary.json")["rows"] if r["pairs"] <= 1500]  # leaks up to 1,500 rows
    budgets = [r["pairs"] for r in rows]  # leak size in rows (aligned pairs of the whole leaked prompts)
    sup = [r["supervised"] for r in rows]
    hyb = [r["hybrid_B8192"] for r in rows]
    wrong = [r["wrong_memory_large"] for r in rows]
    g2 = load(f"results/{corpus}/v7_2/main/mixed-v7_9-s0.json")["setting"]["corpus"]["g2"]["macro_f1"]
    fig, ax = plt.subplots(figsize=(4.6, 3.1))
    ax.plot(budgets, sup, color=SUPERVISED, marker="o", ls=(0, (5, 2)), lw=1.6, ms=4.5,
            markeredgecolor="white", markeredgewidth=0.6, label="supervised fit")
    ax.plot(budgets, hyb, color=HYBRID, marker="s", lw=1.6, ms=4.5,
            markeredgecolor="white", markeredgewidth=0.6, label="hybrid fit")
    ax.axhline(g2, color=INK2, lw=0.8, ls=":")
    ax.annotate(f"hub reference {g2:.3f}", (budgets[0], g2), xytext=(0, 3), textcoords="offset points", fontsize=8, color=INK2)
    ax.axhspan(min(wrong), max(wrong), color=INK2, alpha=0.15, lw=0)
    ax.annotate(f"mismatched-prompt control {min(wrong):.2f} to {max(wrong):.2f}", (budgets[1], max(wrong)), xytext=(0, 3),
                textcoords="offset points", fontsize=8, color=INK2)
    ax.set_xscale("log")
    ax.set_xticks(budgets)
    ax.set_xticklabels([f"{b:,}" for b in budgets], fontsize=7.5)
    ax.minorticks_off()
    ax.set_ylim(0, 1.05)
    ax.set_xlabel("leaked rows")
    ax.set_ylabel("word-F1 (mean of three decoders)")
    ax.grid(axis="y")
    ax.legend(loc="center right", fontsize=8, handlelength=2.6)
    fig.tight_layout()
    save(fig, out)
    print("legal budgets", budgets, "sup", [round(v, 4) for v in sup], "hyb", [round(v, 4) for v in hyb],
          "E", [(round(r["E"]["mean_diff"], 4), round(r["E"]["ci_low"], 4), round(r["E"]["ci_high"], 4)) for r in rows])


leak_shape()
grid_leak_size()
budget_legal()
budget_legal("legal10w", "ch4/budget_curve_legal10w")


def leak_size_three():
    """One design on three datasets: hybrid (alpha 0.95, tau 2d, B 8,192) against the supervised fit by leaked rows, seed 1,
    500 selection prompts, leaks of 1, 3, 5, 10, 30 and 100 whole prompts, shown up to 1,500 rows."""
    panels = []
    d = load("results/v7_2/main/mixed-v8_5-s1.json")["seeds"]["1"]
    xs, sup, hyb, wrong = [], [], [], []
    for b in (1, 3, 5, 10, 30, 100):
        h, s_ = d["cells"][f"b{b}/a0.95/sq/m0/t0.1152/r1/B8192"], d["cells"][f"b{b}/a1/r1"]
        xs.append(d["budgets"][str(b)]["anchor_counts"]["valid_aligned_pairs"])
        sup.append(s_["final"]["macro_f1"]); hyb.append(h["final"]["macro_f1"]); wrong.append(h["wrong_memory"]["macro_f1"])
    g2 = json.loads((ROOT / "results/v7_2/main/factorial.json").read_text())["controls"]["true_olmo_code"]["macro_f1"]
    panels.append(("NQ", xs, sup, hyb, wrong, g2))
    for corpus in ("legal128w", "legal10w"):
        rows = [r for r in load(f"results/{corpus}/v7_2/main/v8_6-summary.json")["rows"] if r["pairs"] <= 1500]
        g2 = load(f"results/{corpus}/v7_2/main/mixed-v7_9-s0.json")["setting"]["corpus"]["g2"]["macro_f1"]
        panels.append((corpus, [r["pairs"] for r in rows], [r["supervised"] for r in rows], [r["hybrid_B8192"] for r in rows],
                       [r["wrong_memory_large"] for r in rows], g2))
    fig, axes = plt.subplots(1, 3, figsize=(9.6, 3.0), sharey=True)
    for ax, (name, xs, sup, hyb, wrong, g2) in zip(axes, panels):
        ax.plot(xs, sup, color=SUPERVISED, marker="o", ls=(0, (5, 2)), lw=1.6, ms=4.5, markeredgecolor="white", markeredgewidth=0.6, label="supervised fit")
        ax.plot(xs, hyb, color=HYBRID, marker="s", lw=1.6, ms=4.5, markeredgecolor="white", markeredgewidth=0.6, label="hybrid fit")
        ax.axhline(g2, color=INK2, lw=0.8, ls=":")
        ax.annotate(f"hub reference {g2:.3f}", (xs[0], g2), xytext=(0, 3), textcoords="offset points", fontsize=7.5, color=INK2)
        ax.set_xscale("log"); ax.set_xticks(xs); ax.set_xticklabels([f"{x:,}" for x in xs], fontsize=7.5); ax.minorticks_off()
        ax.set_ylim(0, 1.05); ax.set_xlabel("leaked rows"); ax.set_title(name, fontsize=9); ax.grid(axis="y")
        print(name, xs, "sup", [round(v, 3) for v in sup], "hyb", [round(v, 3) for v in hyb], "gain", [round(h - s_, 3) for h, s_ in zip(hyb, sup)])
    axes[0].set_ylabel("word-F1 (mean of three decoders)")
    axes[0].legend(loc="center right", fontsize=8, handlelength=2.6)
    fig.tight_layout()
    save(fig, "ch4/leak_size_three")


def leak_size_span9():
    """The main comparison's leak at six sizes on three datasets: the first nine rows of 1, 3, 5, 10, 30 and 100 prompts
    (9 to 900 rows), hybrid (alpha 0.9, tau 2d, B 8,192) against the supervised fit, seed 1, 500 selection prompts.
    The 90-row point is seed 1 of mixed-w46-std. A size whose result file is missing is drawn as a hollow grey marker
    and the figure carries a placeholder mark until every size is present."""
    sizes = (9, 27, 45, 90, 270, 900)
    fig, axes = plt.subplots(1, 3, figsize=(9.6, 3.0), sharey=True)
    missing = 0
    for ax, (name, root) in zip(axes, MAIN):
        xs, sup, hyb = [], [], []
        for size in sizes:
            path = ROOT / root / ("mixed-w46-std.json" if size == 90 else f"mixed-w46-std-L{size}.json")
            if not path.is_file() or json.loads(path.read_text()).get("status") != "complete":
                missing += 1
                ax.plot([size], [0.03], marker="o", ms=5, mfc="none", mec=INK2, mew=0.8, ls="none")
                continue
            cells = json.loads(path.read_text())["seeds"]["1"]["cells"]
            pick = lambda a: next(c for k, c in cells.items() if k.startswith(f"b{size}/a{a}/") and k.endswith(f"L{size}-span9"))
            xs.append(size); sup.append(pick("1")["final"]["macro_f1"]); hyb.append(pick("0.9")["final"]["macro_f1"])
        ax.plot(xs, sup, color=SUPERVISED, marker="o", ls=(0, (5, 2)), lw=1.6, ms=4.5, markeredgecolor="white", markeredgewidth=0.6, label="supervised fit")
        ax.plot(xs, hyb, color=HYBRID, marker="s", lw=1.6, ms=4.5, markeredgecolor="white", markeredgewidth=0.6, label="hybrid fit")
        for x, s_, h in zip(xs, sup, hyb):
            ax.annotate(f"{h - s_:+.2f}", (x, max(h, s_)), xytext=(0, 5), textcoords="offset points", ha="center", fontsize=7.5, color=INK2)
        g2 = (json.loads((ROOT / "results/v7_2/main/hub-dev-eval-m32.json").read_text())["olmo_source_mean"]["hub"] if name == "NQ"  # cap rows+32, as the main comparison
              else load(f"{root}/mixed-v7_9-s0.json")["setting"]["corpus"]["g2"]["macro_f1"])
        ax.axhline(g2, color=INK2, lw=0.8, ls=":")
        ax.annotate(f"hub reference {g2:.3f}", (sizes[0], g2), xytext=(0, 3), textcoords="offset points", fontsize=7.5, color=INK2)
        ax.set_xscale("log"); ax.set_xticks(sizes); ax.set_xticklabels([str(s) for s in sizes], fontsize=7.5); ax.minorticks_off()
        ax.set_xlim(6.5, 1250); ax.set_ylim(0, 1.05); ax.set_xlabel("leaked rows"); ax.set_title(name, fontsize=9); ax.grid(axis="y")
        print(name, xs, "sup", [round(v, 3) for v in sup], "hyb", [round(v, 3) for v in hyb], "gain", [round(h - s_, 3) for h, s_ in zip(hyb, sup)])
    axes[0].set_ylabel("word-F1 (mean of three decoders)")
    axes[0].legend(loc="center left", fontsize=8, handlelength=2.6)
    if missing:
        fig.text(0.5, 0.5, f"PLACEHOLDER: {missing} of {3 * len(sizes)} points pending", ha="center", va="center", fontsize=18,
                 color="#c0392b", alpha=0.35, rotation=12)
    fig.tight_layout()
    save(fig, "ch4/leak_size_three")


leak_size_span9()
