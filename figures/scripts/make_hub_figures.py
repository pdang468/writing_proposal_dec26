"""Chapter 3 figures, drawn from the result files of the research repo.

    python figures/scripts/make_hub_figures.py /path/to/representation_alignment

Writes figures/ch3/{hub_architecture,direction_recovery,hub_gates}.{pdf,png}.
Sources: results/v6_3/hpc-final/inversion.json, results/legal128w/v6_3/inversion.json (5,000 validation
prompts each); both oct_w5c-noise.json zero-noise rows (G2, 500 development prompts);
results/legal256w/v7_2/main/v8_6-readiness.json; results/legal10s/v7_2/main/oct_w5b-summary.json (G2) and
oct_w5b-report.md (G1 0.9705, shuffled 0.044; no result file in the local mirror, typed below).
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


def gates():
    a, l128 = load("results/v6_3/hpc-final/inversion.json"), load("results/legal128w/v6_3/inversion.json")
    l256 = load("results/legal256w/v7_2/main/v8_6-readiness.json")
    l10_g2 = load("results/legal10s/v7_2/main/oct_w5b-summary.json")["decisions"]["Q1"]["g2"]
    g2 = lambda rel: load(rel)["sets"]["iso-r0"]["macro_word_f1"]
    shuffled = lambda d: d["cross_mean"]["shuffled"]["word_f1"]
    rows = [  # corpus, G1 cross mean, G2, shuffled floor (cross mean; legal256w: largest cross direction)
        ("Corpus A", a["cross_mean"]["hub"]["word_f1"], g2("results/v7_2/main/oct_w5c-noise.json"), shuffled(a)),
        ("legal128w", l128["cross_mean"]["hub"]["word_f1"], g2("results/legal128w/v7_2/main/oct_w5c-noise.json"),
         shuffled(l128)),
        ("legal256w", l256["g1"]["cross_mean"], l256["g2"]["macro_f1"], l256["g1"]["shuffled_max"]),
        ("legal10s", 0.9705, l10_g2, 0.044),  # G1 and shuffled: oct_w5b-report.md
    ]
    for r in rows:
        print(r[0], [round(v, 4) for v in r[1:]])
    GRAY = "#9a9994"
    fig, ax = plt.subplots(figsize=(5.8, 3.0))
    width = 0.28
    series = [("G1: mean of six cross directions, validation", BLUE), ("G2: true hub output, development", ORANGE),
              ("shuffled memory (control)", GRAY)]
    for i, row in enumerate(rows):
        for k, (value, (_, color)) in enumerate(zip(row[1:], series)):
            x = i + (k - 1) * (width + 0.035)
            ax.bar(x, value, width, color=color, zorder=2)
            ax.text(x, value + 0.012, f"{value:.3f}", ha="center", va="bottom", fontsize=6.3, color=INK)
    for y, text in ((0.90, "G1 threshold\n0.90"), (0.20, "shuffled limit\n0.20")):
        ax.axhline(y, color=INK2, lw=0.7, ls=(0, (4, 3)), zorder=1)
        ax.text(len(rows) - 0.42, y, text, fontsize=7.5, color=INK2, ha="left", va="center",
                bbox=dict(fc=SURFACE, ec="none", pad=1.5), zorder=4)
    ax.set_xticks(range(len(rows)), [r[0] for r in rows])
    ax.set_xlim(-0.5, len(rows) + 0.25)
    ax.set_ylim(0, 1.08)
    ax.set_yticks([0, 0.2, 0.4, 0.6, 0.8, 1.0])
    ax.set_ylabel("free-run word-F1")
    ax.tick_params(axis="x", length=0)
    ax.grid(axis="y", zorder=0)
    handles = [plt.Rectangle((0, 0), 1, 1, color=c) for _, c in series]
    fig.legend(handles, [n for n, _ in series], loc="upper center", ncol=1, fontsize=7.5,
               bbox_to_anchor=(0.5, 1.0), handlelength=1.4)
    fig.tight_layout(rect=(0, 0, 1, 0.84))
    save(fig, "hub_gates")


architecture()
directions()
gates()
