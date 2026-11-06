"""Chapter 3 figures, drawn from the result files of the research repo.

    python figures/scripts/make_hub_figures.py /path/to/representation_alignment

Writes figures/ch3/{hub_architecture,direction_recovery,hub_translation,hub_ceiling}.{pdf,png}.
Sources: results/v6_3/hpc-final/inversion.json, results/legal128w/v6_3/inversion.json (5,000 validation
prompts each); both oct_w5c-noise.json zero-noise rows (G2, 500 development prompts);
results/legal256w/v7_2/main/v8_6-readiness.json;
mixed-oct_w5b-L.json and mixed-v8_6-s1.json (per-decoder G2). legal10s is left out of both bar figures.
"""
import json
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.patches import FancyBboxPatch

ROOT = Path(sys.argv[1])
OUT = Path(__file__).resolve().parents[1]
INK, INK2, GRID, SURFACE = "#0b0b0b", "#52514e", "#e6e5e1", "#ffffff"
BLUE, ORANGE = "#2a78d6", "#eb6834"
RAMP = ["#cde2fb", "#9ec5f4", "#6da7ec", "#3987e5", "#256abf", "#184f95", "#0d366b"]
plt.rcParams.update({
    "font.family": "serif", "font.size": 9, "axes.edgecolor": INK2, "axes.linewidth": 0.6,
    "axes.spines.top": False, "axes.spines.right": False, "xtick.color": INK2, "ytick.color": INK2,
    "axes.labelcolor": INK, "grid.color": GRID, "grid.linewidth": 0.6, "legend.frameon": False,
    "pdf.fonttype": 42,
})
MODELS = [("qwen", "Qwen"), ("olmo", "OLMo"), ("smollm", "SmolLM")]


def load(rel):
    return json.loads((ROOT / rel).read_text())


def save(fig, name):
    path = OUT / "ch3" / name
    fig.savefig(path.with_suffix(".pdf"))
    fig.savefig(path.with_suffix(".png"), dpi=200)
    plt.close(fig)
    print(path.with_suffix(".pdf"))


def architecture():
    fig, ax = plt.subplots(figsize=(6.4, 2.5))
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 40)
    ax.axis("off")
    rows = [31, 19, 7]
    h = 8.5

    def box(x, y, w, text, fill, dashed=False, height=h):
        ax.add_patch(FancyBboxPatch((x, y - height / 2), w, height, boxstyle="round,pad=0,rounding_size=1",
                                    fc=fill, ec=INK2, lw=0.8, ls=(0, (3, 2)) if dashed else "-"))
        ax.text(x + w / 2, y, text, ha="center", va="center", fontsize=7.5, color=INK, linespacing=1.25)

    def arrow(x0, y0, x1, y1):
        ax.annotate("", (x1, y1), (x0, y0), arrowprops=dict(arrowstyle="-|>", color=INK2, lw=0.8,
                                                            shrinkA=0, shrinkB=0, mutation_scale=7))

    sources = [("Qwen3.5-0.8B\nblock 18, 1024", "$\\to$ 1024"), ("OLMo-2-1B\nblock 12, 2048", "$\\to$ 2048"),
               ("SmolLM2-1.7B\nblock 18, 2048", "$\\to$ 2048")]
    decoders = ["Qwen\ndecoder", "OLMo\ndecoder", "SmolLM\ndecoder"]
    light, dark = "#eeeeec", "#cfcfcb"
    for y, (src, _) in zip(rows, sources):
        box(0, y, 17, src, SURFACE, dashed=True)
        box(21, y, 13, "adapter\n$\\to$ 1024", light)
        arrow(17, y, 21, y)
        arrow(34, y, 38, y)
    box(38, 19, 13, "shared\ntrunk\n1024 $\\to$ 512", dark, height=32.5)
    box(55, 19, 9, "hub\noutput\n$m_t$, 512", SURFACE, height=14)
    arrow(51, 19, 55, 19)
    for y, (_, width), dec in zip(rows, sources, decoders):
        box(69, y, 13, f"projector\n{width}", light)
        box(86, y, 14, dec, SURFACE, dashed=True)
        arrow(64, 19, 69, y)
        arrow(82, y, 86, y)
    ax.text(8.5, 38, "hidden state $s_t$", ha="center", fontsize=7.5, color=INK2)
    ax.text(93, 38, "memory rows", ha="center", fontsize=7.5, color=INK2)
    fig.subplots_adjust(0.01, 0.02, 0.99, 0.98)
    save(fig, "hub_architecture")


def directions():
    files = {"Corpus A": "results/v6_3/hpc-final/inversion.json", "legal128w": "results/legal128w/v6_3/inversion.json"}
    cmap = LinearSegmentedColormap.from_list("blue", RAMP)
    fig, axes = plt.subplots(1, 2, figsize=(6.4, 2.75))
    for ax, (name, rel) in zip(axes, files.items()):
        d = load(rel)
        grid = [[d["directions"][f"{s}->{t}"]["hub"] for t, _ in MODELS] for s, _ in MODELS]
        assert all(c["prompt_count"] == 5000 for row in grid for c in row)
        image = ax.imshow([[c["word_f1"] for c in row] for row in grid], cmap=cmap, vmin=0.80, vmax=1.0)
        for i, row in enumerate(grid):
            for j, c in enumerate(row):
                color = "white" if c["word_f1"] > 0.93 else INK
                ax.text(j, i - 0.1, f"{c['word_f1']:.3f}", ha="center", va="center", color=color, fontsize=9.5)
                ax.text(j, i + 0.26, f"exact {c['exact_match']:.2f}", ha="center", va="center", color=color, fontsize=7)
        for k in (0.5, 1.5):
            ax.axhline(k, color=SURFACE, lw=2)
            ax.axvline(k, color=SURFACE, lw=2)
        ax.set_xticks(range(3), [m for _, m in MODELS])
        ax.set_yticks(range(3), [m for _, m in MODELS])
        ax.xaxis.tick_top()
        ax.xaxis.set_label_position("top")
        ax.set_xlabel("decoder")
        ax.tick_params(length=0)
        for s in ax.spines.values():
            s.set_visible(False)
        shuffled = d["cross_mean"]["shuffled"]["word_f1"]
        ax.set_title(f"{name}: cross mean {d['cross_mean']['hub']['word_f1']:.3f}, shuffled {shuffled:.3f}",
                     fontsize=8.5, color=INK, y=-0.14)
    axes[0].set_ylabel("source model")
    fig.tight_layout(rect=(0, 0, 0.93, 1))
    bar = fig.colorbar(image, cax=fig.add_axes([0.94, 0.2, 0.012, 0.55]))
    bar.set_label("free-run word-F1", fontsize=8)
    bar.outline.set_visible(False)
    bar.ax.tick_params(length=0, labelsize=7.5)
    save(fig, "direction_recovery")


def bar_axes(figsize):
    fig, ax = plt.subplots(figsize=figsize)
    ax.set_ylim(0, 1.08)
    ax.set_yticks([0, 0.2, 0.4, 0.6, 0.8, 1.0])
    ax.set_ylabel("free-run word-F1")
    ax.tick_params(axis="x", length=0)
    ax.grid(axis="y", zorder=0)
    return fig, ax


def translation():
    """G1: a prompt enters through one model and is decoded by another; mean of the six cross directions."""
    a, l128 = load("results/v6_3/hpc-final/inversion.json"), load("results/legal128w/v6_3/inversion.json")
    l256 = load("results/legal256w/v7_2/main/v8_6-readiness.json")["g1"]
    rows = [  # corpus, cross mean, shuffled control (cross mean; legal256w: largest cross direction)
        ("Corpus A", a["cross_mean"]["hub"]["word_f1"], a["cross_mean"]["shuffled"]["word_f1"]),
        ("legal128w", l128["cross_mean"]["hub"]["word_f1"], l128["cross_mean"]["shuffled"]["word_f1"]),
        ("legal256w", l256["cross_mean"], l256["shuffled_max"]),
    ]
    series = [("hub output", BLUE), ("shuffled control", "#9a9994")]
    fig, ax = bar_axes((3.8, 2.9))
    width = 0.36
    for i, row in enumerate(rows):
        print("G1", row[0], [round(v, 4) for v in row[1:]])
        for k, (value, (_, color)) in enumerate(zip(row[1:], series)):
            x = i + (k - 0.5) * (width + 0.04)
            ax.bar(x, value, width, color=color, zorder=2)
            ax.text(x, value + 0.012, f"{value:.3f}", ha="center", va="bottom", fontsize=7.5, color=INK)
    ax.set_xticks(range(len(rows)), [r[0] for r in rows])
    fig.legend([plt.Rectangle((0, 0), 1, 1, color=c) for _, c in series], [n for n, _ in series],
               loc="upper center", ncol=2, fontsize=8, bbox_to_anchor=(0.55, 1.0), handlelength=1.2, columnspacing=2.0)
    fig.tight_layout(rect=(0, 0, 1, 0.92))
    save(fig, "hub_translation")


def ceiling():
    """G2: the true hub output of OLMo decoded by each frozen decoder, 500 development prompts."""
    def from_noise(rel):
        return {k: v["word_f1"] for k, v in load(rel)["sets"]["iso-r0"]["per_decoder"].items()}

    def from_setting(rel):
        g2 = load(rel)["setting"]["corpus"]["g2"]
        assert g2["prompts"] == 500
        return g2["per_decoder"]

    rows = [
        ("Corpus A", from_noise("results/v7_2/main/oct_w5c-noise.json")),
        ("legal128w", from_setting("results/legal128w/v7_2/main/mixed-oct_w5b-L.json")),
        ("legal256w", from_setting("results/legal256w/v7_2/main/mixed-v8_6-s1.json")),
    ]
    fig, ax = bar_axes((5.0, 3.0))
    width = 0.26
    ticks, labels = [], []
    for i, (name, per) in enumerate(rows):
        values = [per[m] for m, _ in MODELS]
        print("G2", name, [round(v, 4) for v in values], "mean", round(sum(values) / 3, 4))
        for k, ((_, label), value) in enumerate(zip(MODELS, values)):
            x = i + (k - 1) * (width + 0.03)
            ax.bar(x, value, width, color=ORANGE, zorder=2)
            ax.text(x, value + 0.012, f"{value:.3f}", ha="center", va="bottom", fontsize=6.3, color=INK)
            ticks.append(x)
            labels.append(label)
        ax.text(i, -0.11, name, ha="center", va="top", fontsize=9, color=INK, transform=ax.get_xaxis_transform())
    ax.set_xticks(ticks, labels, fontsize=6.3)
    fig.subplots_adjust(left=0.115, right=0.99, top=0.97, bottom=0.2)
    save(fig, "hub_ceiling")


architecture()
directions()
translation()
ceiling()
