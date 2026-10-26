# =============================================================================
#  WITNESS-COUNT STUDY -- final analysis + publication figures (no GPU, no training)
# =============================================================================
#  Inputs : mit2_runs_2017.csv, mit2_runs_2018.csv  (raw rows from witness_mit2_*.py)
#           + the v3.2 and mit-1.0 results below, transcribed from their run logs
#             (cicids_2017_full_output, CICIDS_2018_full_output, cicids_17/18_mitigation_output).
#  Outputs: figures/*.pdf + *.png (300 dpi), tables/*.csv + tables/*.md
#  Usage  : python witness_analysis.py --csv17 mit2_runs_2017.csv --csv18 mit2_runs_2018.csv --out results
#  Corrections applied here (disclosed, not hidden):
#    (1) grid-censored floor check: with grid {1,2,3,4,6,8}, k* = 6 means the true k* is 5 or 6, so it is
#        CONSISTENT with the floor f+1 = 5.  The pre-registered rule (k* <= f+1) ignored this.
#    (2) robustness is reported split by f <= F_HAT (inside the base rule's own tolerance) vs f > F_HAT.
#    Pre-registered verdicts are reported alongside, unchanged.
# =============================================================================
import argparse, os, math, json
import numpy as np, pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle

GRID = [1, 2, 3, 4, 6, 8]; KMAX = 8; NEVER = 9.3
N, F_HAT, LEARN = 20, 2, 0.8
TARGETS = [("2017", "Botnet"), ("2017", "Portscan"), ("2018", "Brute Force"), ("2018", "Botnet")]
TL = lambda ds, t: f"CICIDS{ds} {t}" if ds == "2017" else f"CSE-CIC-IDS2018 {t}"
TS = lambda ds, t: f"{t} ('{ds[2:]})"

# Okabe-Ito colour-blind-safe palette
C = {"fedavg": "#000000", "cwmed": "#D55E00", "trmean": "#E69F00", "mkrum": "#CC79A7", "geomed": "#56B4E9",
     "bucket_cwmed": "#009E73", "cclip": "#0072B2", "nnm_cwmed": "#999933",
     "base": "#D55E00", "orcinf": "#56B4E9", "elect": "#E69F00", "sra": "#009E73", "sra_l10": "#0072B2",
     "sra_rr3": "#CC79A7", "sra_rr1": "#999999", "sra_rand": "#7F7F7F"}
LAB = {"fedavg": "FedAvg", "cwmed": "Coord. median", "trmean": "Trimmed mean", "mkrum": "Multi-Krum",
       "geomed": "Geo. median", "bucket_cwmed": "Bucketing+CM", "cclip": "Centered clip", "nnm_cwmed": "NNM+CM",
       "base": "Robust rule (base)", "orcinf": "Witness boost (oracle, unclipped)", "elect": "Electorate restriction",
       "sra": r"SRA ($\lambda_W$=3, pre-reg.)", "sra_l10": r"SRA ($\lambda_W$=10, post-hoc)",
       "sra_rr3": r"SRA, RR bit $\varepsilon_w$=3", "sra_rr1": r"SRA, RR bit $\varepsilon_w$=1", "sra_rand": "SRA, random W"}

plt.rcParams.update({"font.family": "serif", "font.serif": ["DejaVu Serif", "Times New Roman", "Times"],
                     "mathtext.fontset": "dejavuserif", "font.size": 8, "axes.titlesize": 8.5, "axes.labelsize": 8,
                     "legend.fontsize": 6.8, "xtick.labelsize": 7, "ytick.labelsize": 7, "axes.linewidth": 0.6,
                     "lines.linewidth": 1.2, "lines.markersize": 3.8, "axes.spines.top": False,
                     "axes.spines.right": False, "legend.frameon": False, "savefig.bbox": "tight",
                     "savefig.pad_inches": 0.02, "pdf.fonttype": 42, "ps.fonttype": 42})
W1, W2 = 3.5, 7.16   # IEEE single / double column (inches)

# ---------------- transcribed from the v3.2 run logs ----------------
AGG8 = ["fedavg", "cwmed", "trmean", "mkrum", "geomed", "bucket_cwmed", "cclip", "nnm_cwmed"]
V3_TARGETS = ["Botnet ('17)", "Portscan ('17)", "Brute Force ('17)", "Brute Force ('18)", "Botnet ('18)"]
V3_KSTAR = {  # C1b: k* at f = 0 (non-private), tax = k* - k*(FedAvg)
    "Botnet ('17)":      [2, 7, 3, 4, 5, 5, 4, 4],
    "Portscan ('17)":    [1, 7, 4, 4, 5, 5, 4, 4],
    "Brute Force ('17)": [1, 9, 3, 4, 4, 5, 4, 4],
    "Brute Force ('18)": [1, 10, 3, 4, 5, 5, 4, 4],
    "Botnet ('18)":      [1, 9, 4, 4, 6, 5, 5, 4]}
V3_TAX = {  # C1b tax column as logged
    "Botnet ('17)": [1, 6, 2, 3, 4, 4, 3, 3], "Portscan ('17)": [0, 6, 3, 3, 4, 4, 3, 3],
    "Brute Force ('17)": [0, 8, 2, 3, 3, 4, 3, 3], "Brute Force ('18)": [0, 9, 2, 3, 4, 4, 3, 3],
    "Botnet ('18)": [0, 8, 3, 3, 5, 4, 4, 3]}
V3_FLOOR_MAXREC = {  # C1a: max target recall at k <= f (floor held on 40/40)
    "Botnet ('17)": [0.090, 0, 0.001, 0, 0, 0, 0, 0], "Portscan ('17)": [0.187, 0, 0.030, 0, 0, 0, 0, 0],
    "Brute Force ('17)": [0.288, 0, 0.094, 0.001, 0, 0, 0, 0.002],
    "Brute Force ('18)": [0.217, 0, 0.096, 0, 0, 0, 0, 0], "Botnet ('18)": [0.020, 0, 0, 0, 0, 0, 0, 0]}
V3_ROUNDS = {  # C2: k*(R), k*(2R), k*(3R) per robust aggregator
    "Botnet ('17)": {"cwmed": [7, 7, 5], "trmean": [3, 3, 3], "mkrum": [4, 4, 3], "geomed": [5, 5, 3],
                     "bucket_cwmed": [5, 5, 3], "cclip": [4, 3, 3], "nnm_cwmed": [4, 3, 3]},
    "Portscan ('17)": {"cwmed": [7, 6, 5], "trmean": [4, 3, 3], "mkrum": [4, 3, 3], "geomed": [5, 4, 3],
                       "bucket_cwmed": [5, 4, 4], "cclip": [4, 3, 3], "nnm_cwmed": [4, 3, 3]},
    "Brute Force ('17)": {"cwmed": [9, 6, 5], "trmean": [3, 3, 3], "mkrum": [4, 3, 3], "geomed": [4, 3, 3],
                          "bucket_cwmed": [5, 4, 4], "cclip": [4, 3, 2], "nnm_cwmed": [4, 3, 3]},
    "Brute Force ('18)": {"cwmed": [10, 9, 9], "trmean": [3, 3, 3], "mkrum": [4, 4, 3], "geomed": [5, 4, 3],
                          "bucket_cwmed": [5, 5, 5], "cclip": [4, 3, 3], "nnm_cwmed": [4, 3, 3]},
    "Botnet ('18)": {"cwmed": [9, 8, 7], "trmean": [4, 3, 3], "mkrum": [4, 3, 3], "geomed": [6, 5, 4],
                     "bucket_cwmed": [5, 5, 4], "cclip": [5, 4, 3], "nnm_cwmed": [4, 3, 3]}}
V3_DP = {  # C3: k* at f=0 for [non-private, clip-only, eps=10, eps=3, eps=1]
    "Botnet ('17)": {"fedavg": [1, 2, 3, 4, 6], "cwmed": [8, 8, 3, 3, 16], "trmean": [3, 3, 3, 3, 6], "mkrum": [4, 4, 2, 3, 12]},
    "Brute Force ('18)": {"fedavg": [1, 2, 2, 2, 4], "cwmed": [12, 12, 2, 2, 4], "trmean": [3, 4, 2, 2, 4], "mkrum": [4, 4, 2, 2, 4]},
    "Botnet ('18)": {"fedavg": [2, 2, 2, 3, 4], "cwmed": [12, 12, 2, 3, 6], "trmean": [4, 4, 2, 2, 4], "mkrum": [4, 4, 2, 2, 4]}}
# mit-1.0 M0: wall edge (largest k that still fails at 3R) vs the aggregator's tolerance F_HAT
M0 = {"Botnet ('17)": {"trmean": [1, 2, 2, 3], "mkrum": [1, 2, 3, 4], "nnm_cwmed": [1, 2, 3, 4]},
      "Portscan ('17)": {"trmean": [1, 2, 3, 4], "mkrum": [1, 2, 3, 4], "nnm_cwmed": [1, 2, 3, 4]},
      "Brute Force ('18)": {"trmean": [1, 2, 3, 4], "mkrum": [1, 2, 3, 4], "nnm_cwmed": [1, 2, 3, 4]},
      "Botnet ('18)": {"trmean": [1, 2, 3, 4], "mkrum": [1, 2, 3, 4], "nnm_cwmed": [1, 2, 3, 4]}}

# ---------------- helpers ----------------
def kstar(ks, rec, ref):
    ks = np.asarray(ks); r = np.asarray(rec, float); o = np.argsort(ks); ks, r = ks[o], r[o]
    ok = np.where(np.isnan(r), False, r >= LEARN * ref)
    if not len(ok) or not ok[-1]: return None      # never within the grid
    j = len(ok) - 1
    while j - 1 >= 0 and ok[j - 1]: j -= 1
    return int(ks[j])

def kn(k): return NEVER if k is None else k
def kstr(k): return "never" if k is None else str(k)
def prev_grid(k): return max([g for g in GRID if g < k], default=0)
def floor_reached(k, f, censored=True):
    if k is None: return False
    return k <= f + 1 or (censored and prev_grid(k) < f + 1 <= k)

def rr_pred(eps, f, n=N):
    p = math.exp(eps) / (1 + math.exp(eps))
    for k in range(1, n - f + 1):
        if k * p > (n - k - f) * (1 - p) + f + 1e-12: return k
    return None

def rr_match(meas, pred, tol=1):
    if meas is None: return pred is None or pred + tol > KMAX
    if pred is None: return False
    return max(prev_grid(meas) + 1, pred - tol) <= min(meas, pred + tol)

def save(fig, out, name):
    for ext in ("pdf", "png"):
        fig.savefig(os.path.join(out, "figures", f"{name}.{ext}"), dpi=300)
    plt.close(fig); print(f"  figure: {name}")

def load(csv17, csv18):
    a = pd.read_csv(csv17); a["ds"] = "2017"
    b = pd.read_csv(csv18); b["ds"] = "2018"
    d = pd.concat([a, b], ignore_index=True)
    ref = d[d.exp == "REF"].groupby(["ds", "target"]).target_recall.mean().to_dict()
    return d, ref

def ks_of(d, ds, t, exp, agg, arm, f, ref, eps=None):
    s = d[(d.ds == ds) & (d.target == t) & (d.exp == exp) & (d["agg"] == agg) & (d.arm == arm) & (d.f == f)]
    if eps is not None: s = s[np.isclose(s.eps, eps)]
    m = s.groupby("k").target_recall.mean()
    return kstar(m.index.values, m.values, ref) if len(m) else None

# ---------------- figures ----------------
def fig_setup(out):
    fig, axs = plt.subplots(1, 2, figsize=(W2, 2.9))
    def member(ax, x, y, kind):
        col = {"W": "#009E73", "A": "#D55E00", "H": "#BBBBBB"}[kind]
        ax.add_patch(plt.Circle((x, y), 0.17, color=col, ec="k", lw=0.4, zorder=3))
    def box(ax, x, y, w, h, txt, fc="#F2F2F2", ec="k", fs=5.3):
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.05", fc=fc, ec=ec, lw=0.7))
        ax.text(x + w / 2, y + h / 2, txt, ha="center", va="center", fontsize=fs)
    arrow = lambda ax, x0, y0, x1, y1: ax.annotate("", xy=(x1, y1), xytext=(x0, y0), arrowprops=dict(arrowstyle="->", lw=0.8))
    for ax, title in zip(axs, ["(a) Standard robust aggregation", "(b) Split Robust Aggregation (SRA)"]):
        ax.set_xlim(0, 10); ax.set_ylim(0, 7.2); ax.set_aspect("equal"); ax.axis("off"); ax.set_title(title, loc="left")
    roles = ["W"] * 2 + ["A"] * 2 + ["H"] * 16
    ax = axs[0]
    for i, r in enumerate(roles):
        member(ax, 0.5 + (i % 10) * 0.42, 6.6 - (i // 10) * 0.45, r)
    ax.text(4.9, 6.75, "$k$ witnesses (hold the rare attack)", fontsize=5.8, color="#009E73", va="center")
    ax.text(4.9, 6.35, "$f$ Byzantine members", fontsize=5.8, color="#D55E00", va="center")
    ax.text(4.9, 5.95, "$N-k-f$ honest, no rare attack", fontsize=5.8, color="#555555", va="center")
    arrow(ax, 2.4, 5.8, 2.4, 4.65)
    box(ax, 0.2, 3.4, 4.4, 1.15, "one robust vote over all $N$\n(tolerates $\\hat F$ outliers)")
    arrow(ax, 2.4, 3.3, 2.4, 2.2)
    box(ax, 0.2, 0.9, 4.4, 1.2, "witnesses look like outliers:\nrare attack erased while $k\\leq\\hat F$",
        fc="#FBE9E1", ec="#D55E00")
    ax.text(5.1, 1.5, "wall at $k=\\hat F$;\nwitness tax = extra\nwitnesses needed\nabove the floor $f{+}1$",
            fontsize=5.3, va="center")
    ax = axs[1]
    for i in range(16):
        member(ax, 0.45 + (i % 8) * 0.42, 6.6 - (i // 8) * 0.45, "H")
    for i, r in enumerate(roles[:4]):
        member(ax, 6.2 + i * 0.42, 6.6, r)
    ax.text(1.9, 5.45, "H: bit 0", ha="center", fontsize=6.2)
    ax.text(6.85, 6.05, "W: bit 1 (claims evidence)", ha="center", fontsize=6.2)
    arrow(ax, 1.9, 5.25, 1.9, 4.65); arrow(ax, 6.85, 5.85, 6.85, 4.65)
    box(ax, 0.1, 3.4, 3.8, 1.15, "$a_H$: base robust rule\n(liars outside W face it)")
    box(ax, 4.9, 3.4, 3.9, 1.15, "$a_W$: coordinate median\n(liars must outnumber\nwitnesses inside W)")
    arrow(ax, 1.9, 3.3, 3.6, 2.2); arrow(ax, 6.85, 3.3, 5.6, 2.2)
    box(ax, 0.1, 0.7, 9.7, 1.45, "$a=a_H+\\frac{|W|}{N}\\,\\mathrm{clip}_{\\lambda_W\\tau}(a_W-a_H)$\n"
        "reaches the floor $k^*=f+1$;  damage $\\leq$ $\\frac{|W|}{N}\\lambda_W\\tau$",
        fc="#E6F4EE", ec="#009E73", fs=5.5)
    save(fig, out, "fig01_setup_and_sra")

def fig_floor_tax(d, ref, out):
    fig, axs = plt.subplots(1, 4, figsize=(W2, 1.95), sharey=True)
    for ax, (ds, t) in zip(axs, TARGETS):
        fs = [0, 2, 4]; r = ref[(ds, t)]
        ax.fill_between([-0.4, 4.4], [-0.4 + 0, 4.4], 0, color="#EEEEEE", zorder=0)
        ax.plot([-0.4, 4.4], [0.6, 5.4], color="k", ls=":", lw=0.8, zorder=1)
        for agg in ["fedavg", "cwmed", "trmean", "mkrum"]:
            ys = [kn(ks_of(d, ds, t, "M3", agg, "base", f, r)) for f in fs]
            ax.plot(fs, ys, "o-", color=C[agg], label=LAB[agg], zorder=3)
        ax.set_title(TS(ds, t)); ax.set_xticks(fs); ax.set_xlabel("Byzantine members $f$")
        ax.set_ylim(0, 9.8); ax.set_xlim(-0.4, 4.4); ax.set_yticks([1, 2, 3, 4, 5, 6, 7, 8, NEVER])
        ax.set_yticklabels(["1", "2", "3", "4", "5", "6", "7", "8", ">8"])
        ax.text(3.9, 1.0, "impossible\n($k\\leq f$)", ha="right", fontsize=5.8, color="#555555")
    axs[0].set_ylabel("witnesses needed $k^*$")
    axs[0].text(0.05, 1.55, "floor $f{+}1$", fontsize=5.8, rotation=36)
    axs[-1].legend(loc="upper left", bbox_to_anchor=(1.0, 1.0))
    save(fig, out, "fig02_floor_and_witness_tax")

def fig_tax_heatmap(out):
    M = np.array([V3_TAX[t] for t in V3_TARGETS]).T
    fig, ax = plt.subplots(figsize=(W1, 2.3))
    im = ax.imshow(M, cmap="Oranges", vmin=0, vmax=9, aspect="auto")
    for i in range(M.shape[0]):
        for j in range(M.shape[1]):
            ax.text(j, i, int(M[i, j]), ha="center", va="center", fontsize=7, color="w" if M[i, j] > 5 else "k")
    ax.set_xticks(range(len(V3_TARGETS))); ax.set_xticklabels(V3_TARGETS, rotation=25, ha="right")
    ax.set_yticks(range(len(AGG8))); ax.set_yticklabels([LAB[a] for a in AGG8])
    ax.spines[:].set_visible(False)
    cb = fig.colorbar(im, ax=ax, fraction=0.05, pad=0.02); cb.set_label("witness tax ($f=0$)")
    save(fig, out, "fig03_witness_tax_8_aggregators")

def fig_wall(out):
    fig, axs = plt.subplots(1, 2, figsize=(W2, 2.1), gridspec_kw={"width_ratios": [1.25, 1]})
    ax = axs[0]
    for agg in ["cwmed", "geomed", "bucket_cwmed", "mkrum", "cclip", "nnm_cwmed", "trmean"]:
        M = np.array([V3_ROUNDS[t][agg] for t in V3_TARGETS])
        ax.errorbar([1, 2, 3], M.mean(0), yerr=[M.mean(0) - M.min(0), M.max(0) - M.mean(0)], fmt="o-",
                    color=C[agg], label=LAB[agg], capsize=1.5, lw=1)
    ax.axhline(1, color="k", ls=":", lw=0.8); ax.text(1.0, 1.25, "FedAvg / floor ($k^*=1$)", fontsize=6)
    ax.set_xticks([1, 2, 3]); ax.set_xticklabels(["$R$", "$2R$", "$3R$"]); ax.set_xlabel("training rounds")
    ax.set_ylabel("witnesses needed $k^*$ ($f=0$)"); ax.set_ylim(0, 11)
    ax.set_title("(a) A wall, not a delay", loc="left")
    ax.legend(ncol=2, loc="upper right", fontsize=5.8)
    ax = axs[1]; rng = np.random.default_rng(0); mk = {"trmean": "s", "mkrum": "o", "nnm_cwmed": "^"}
    for t, dd in M0.items():
        for agg, v in dd.items():
            ax.scatter(np.array([1, 2, 3, 4]) + rng.uniform(-0.12, 0.12, 4), np.array(v) + rng.uniform(-0.08, 0.08, 4),
                       marker=mk[agg], color=C[agg], s=12, alpha=0.8, label=LAB[agg] if t == "Botnet ('17)" else None)
    ax.plot([0.5, 4.5], [0.5, 4.5], "k--", lw=0.8); ax.text(3.2, 4.3, "edge $=\\hat F$", fontsize=6.5)
    ax.set_xticks([1, 2, 3, 4]); ax.set_yticks([1, 2, 3, 4]); ax.set_xlabel("aggregator tolerance $\\hat F$")
    ax.set_ylabel("wall edge (largest $k$ filtered)")
    hit = sum(v[i] == i + 1 for dd in M0.values() for v in dd.values() for i in range(4))
    tot = sum(4 for dd in M0.values() for v in dd.values())
    ax.set_title(f"(b) Wall edge $=\\hat F$ in {hit}/{tot} cells", loc="left"); ax.legend(loc="lower right")
    save(fig, out, "fig04_wall_not_delay_and_fhat")

def fig_dp(out):
    fig, axs = plt.subplots(1, 3, figsize=(W2, 2.0), sharey=True)
    xl = ["non-\nprivate", "clip\nonly", "$\\varepsilon$=10", "$\\varepsilon$=3", "$\\varepsilon$=1"]
    for ax, t in zip(axs, V3_DP):
        for o, agg in zip([-0.09, -0.03, 0.03, 0.09], ["fedavg", "cwmed", "trmean", "mkrum"]):
            v = np.array(V3_DP[t][agg], float)
            ax.plot(np.arange(5) + o, v, "o-", color=C[agg], label=LAB[agg], ms=3.2)
        ax.set_yticks([1, 2, 4, 6, 8, 12, 16])
        ax.axvspan(1.6, 3.4, color="#E6F4EE", zorder=0)
        ax.set_xticks(range(5)); ax.set_xticklabels(xl); ax.set_title(t); ax.set_ylim(0, 17)
    axs[0].set_ylabel("witnesses needed $k^*$ ($f=0$)")
    axs[0].text(2.5, 15.6, "moderate noise\nshrinks the tax", ha="center", fontsize=5.8, color="#009E73")
    axs[-1].legend(loc="upper left", bbox_to_anchor=(1.0, 1.0))
    save(fig, out, "fig05_dp_u_shape")

def fig_sra_curves(d, ref, out):
    arms = [("fedavg", "base"), ("cwmed", "base"), ("cwmed", "orcinf"), ("cwmed", "elect"), ("cwmed", "sra")]
    fig, axs = plt.subplots(3, 4, figsize=(W2, 4.6), sharex=True, sharey=True)
    for j, (ds, t) in enumerate(TARGETS):
        r = ref[(ds, t)]
        for i, f in enumerate([0, 2, 4]):
            ax = axs[i][j]
            for agg, arm in arms:
                s = d[(d.ds == ds) & (d.target == t) & (d.exp == "M3") & (d["agg"] == agg) & (d.arm == arm) & (d.f == f)]
                m = s.groupby("k").target_recall.agg(["mean", "std"])
                key = "fedavg" if agg == "fedavg" else arm
                lab = "FedAvg" if agg == "fedavg" else ("Coord. median (base)" if arm == "base" else LAB[arm])
                ax.plot(m.index, m["mean"], marker="o", color=C[key], label=lab, lw=1.5 if arm == "sra" else 1,
                        ls="--" if agg == "fedavg" else "-", zorder=4 if arm == "sra" else 3)
                ax.fill_between(m.index, m["mean"] - m["std"], m["mean"] + m["std"], color=C[key], alpha=0.12, lw=0)
            ax.axhline(LEARN * r, color="#777777", lw=0.6, ls=":")
            ax.axvspan(0.5, f + 0.5, color="#EEEEEE", zorder=0) if f else None
            ax.axvline(f + 1, color="k", lw=0.6, ls="-.")
            ax.set_ylim(-0.03, 1.05); ax.set_xticks(GRID)
            if i == 0: ax.set_title(TS(ds, t))
            if j == 0: ax.set_ylabel(f"$f={f}$\ntarget recall")
            if i == 2: ax.set_xlabel("witnesses $k$")
    h, l = axs[0][0].get_legend_handles_labels()
    fig.legend(h, l, loc="upper center", ncol=5, bbox_to_anchor=(0.5, 1.035), fontsize=6.3)
    fig.text(0.5, -0.01, "grey band: $k\\leq f$ (impossible); dash-dot: floor $k=f+1$; dotted: learnable line "
             "(0.8$\\times$ reference); shading: $\\pm$1 s.d. over 3 seeds", ha="center", fontsize=6.3)
    save(fig, out, "fig06_sra_recovers_coverage")

def arm_tax_f0(d, ref, arm):
    v = []
    for ds, t in TARGETS:
        fa = ks_of(d, ds, t, "M3", "fedavg", "base", 0, ref[(ds, t)])
        for agg in ["cwmed", "trmean", "mkrum"]:
            k = ks_of(d, ds, t, "M3", "fedavg" if arm == "fedavg" else agg, "base" if arm == "fedavg" else arm, 0, ref[(ds, t)])
            v.append(max(0, kn(k) - kn(fa)))
    return np.array(v)

def m4_stat(d, ds, t, k, f, agg, arm, att):
    s = d[(d.ds == ds) & (d.target == t) & (d.exp == "M4") & (d.k == k) & (d.f == f) & (d["agg"] == agg) & (d.arm == arm) & (d.attack == att)]
    return float(s.benign_fpr.mean()), float(s.other_attack_recall_mean.mean())

def worst_other(d, arm, k, f):
    vals = []
    for ds, t in TARGETS:
        per = []
        for a in ["signflip", "alie"]:
            atts = [a] if arm in ("base", "fedavg") else [a, a + "_nc"]
            for att in atts:
                aggs = ["fedavg"] if arm == "fedavg" else ["cwmed", "trmean", "mkrum"]
                per.append(np.mean([m4_stat(d, ds, t, k, f, g, "base" if arm == "fedavg" else arm, att)[1] for g in aggs]))
        vals.append(min(per))
    return np.array(vals)

def fig_frontier(d, ref, out):
    arms = ["fedavg", "base", "orcinf", "elect", "sra", "sra_l10"]
    fig, axs = plt.subplots(1, 2, figsize=(W2, 2.35), sharey=True)
    for ax, (k, f, ttl) in zip(axs, [(6, 2, "(a) inside tolerance: $k=6$, $f=2\\leq\\hat F$"),
                                     (6, 4, "(b) beyond tolerance: $k=6$, $f=4>\\hat F$")]):
        for arm in arms:
            x = arm_tax_f0(d, ref, arm); y = worst_other(d, arm, k, f)
            key = arm
            ax.errorbar(x.mean(), y.mean(), xerr=[[x.mean() - x.min()], [x.max() - x.mean()]],
                        yerr=[[y.mean() - y.min()], [y.max() - y.mean()]], fmt="o", ms=6, color=C[key], capsize=2,
                        label=LAB[arm], zorder=4 if arm.startswith("sra") else 3)
        ax.set_xlabel("coverage cost: witness tax at $f=0$ (lower = better)")
        ax.set_title(ttl, loc="left"); ax.set_xlim(-0.5, 8.5); ax.set_ylim(-0.03, 1.05)
        ax.annotate("ideal corner", xy=(0.05, 1.0), xytext=(2.2, 0.72), fontsize=6.5, color="#555555",
                    arrowprops=dict(arrowstyle="->", lw=0.6, color="#555555"))
    axs[0].set_ylabel("robustness: worst-attack\nother-attack recall")
    axs[1].legend(loc="upper left", bbox_to_anchor=(1.0, 1.0))
    save(fig, out, "fig07_coverage_robustness_frontier")

def fig_rr(d, ref, out):
    fig, axs = plt.subplots(1, 2, figsize=(W2, 2.2), gridspec_kw={"width_ratios": [1.3, 1]})
    ax = axs[0]; e = np.linspace(0.3, 6, 200); rng = np.random.default_rng(1)
    for f, col in zip([0, 2, 4], ["#009E73", "#0072B2", "#D55E00"]):
        ax.plot(e, [kn(rr_pred(x, f)) if rr_pred(x, f) and rr_pred(x, f) <= KMAX else np.nan for x in e],
                color=col, label=f"prediction, $f={f}$")
        for eps, arm in [(1.0, "sra_rr1"), (3.0, "sra_rr3")]:
            ys = [kn(ks_of(d, ds, t, "M3", g, arm, f, ref[(ds, t)])) for ds, t in TARGETS for g in ["cwmed", "trmean", "mkrum"]]
            ax.scatter(eps + rng.uniform(-0.12, 0.12, len(ys)), np.array(ys) + rng.uniform(-0.1, 0.1, len(ys)),
                       color=col, s=8, alpha=0.6)
        ax.axhline(f + 1, color=col, lw=0.5, ls=":")
    ax.set_xlabel("local-DP budget of the witness bit $\\varepsilon_w$"); ax.set_ylabel("witnesses needed $k^*$")
    ax.set_yticks([1, 2, 3, 4, 5, 6, 7, 8, NEVER]); ax.set_yticklabels(["1", "2", "3", "4", "5", "6", "7", "8", ">8"])
    ax.set_title("(a) Predicted: $kp>(N-k-f)(1-p)+f$", loc="left"); ax.legend(loc="upper right")
    ax = axs[1]; ok1 = ok2 = n = 0; pts = []
    for ds, t in TARGETS:
        for f in [0, 2, 4]:
            for eps, arm in [(1.0, "sra_rr1"), (3.0, "sra_rr3")]:
                for g in ["cwmed", "trmean", "mkrum"]:
                    m = ks_of(d, ds, t, "M3", g, arm, f, ref[(ds, t)]); p = rr_pred(eps, f)
                    pts.append((kn(p) if p and p <= KMAX else NEVER, kn(m), f)); n += 1
                    ok1 += rr_match(m, p, 1); ok2 += rr_match(m, p, 2)
    P = np.array(pts)
    for f, col in zip([0, 2, 4], ["#009E73", "#0072B2", "#D55E00"]):
        q = P[P[:, 2] == f]
        ax.scatter(q[:, 0] + rng.uniform(-0.15, 0.15, len(q)), q[:, 1] + rng.uniform(-0.15, 0.15, len(q)),
                   color=col, s=9, alpha=0.7, label=f"$f={f}$")
    ax.plot([0.5, 9.5], [0.5, 9.5], "k--", lw=0.7)
    ax.set_xlabel("predicted $k^*$"); ax.set_ylabel("measured $k^*$ (grid)")
    ax.set_title(f"(b) $\\pm$1: {ok1}/{n};  $\\pm$2: {ok2}/{n}", loc="left"); ax.legend(loc="lower right")
    T = [1, 2, 3, 4, 5, 6, 7, 8, NEVER]; TLb = ["1", "2", "3", "4", "5", "6", "7", "8", ">8"]
    ax.set_xticks(T); ax.set_xticklabels(TLb); ax.set_yticks(T); ax.set_yticklabels(TLb)
    save(fig, out, "fig08_rr_privacy_price")
    return ok1, ok2, n

def paired(bf, bo, af, ao, tol=0.05, fmax=0.05):
    ok = af <= bf + tol + 1e-12 and ao >= bo - tol - 1e-12
    if bf <= fmax + 1e-12: ok = ok and af <= fmax + 1e-12
    return ok

def robustness_table(d):
    rows = []
    for ds, t in TARGETS:
        for (k, f) in [(6, 2), (6, 4), (2, 4)]:
            for a in ["signflip", "alie"]:
                for g in ["cwmed", "trmean", "mkrum"]:
                    bf, bo = m4_stat(d, ds, t, k, f, g, "base", a)
                    for arm in ["sra", "sra_l10", "orcinf", "elect"]:
                        for att in [a, a + "_nc"]:
                            af, ao = m4_stat(d, ds, t, k, f, g, arm, att)
                            rows.append(dict(ds=ds, target=t, k=k, f=f, attack=att, agg=g, arm=arm, base_fpr=bf,
                                             base_other=bo, arm_fpr=af, arm_other=ao, holds=paired(bf, bo, af, ao),
                                             base_broken=(bf > 0.05 or bo < 0.5)))
    return pd.DataFrame(rows)

def fig_robust_map(R, out):
    cols = [(k, f, a) for (k, f) in [(6, 2), (6, 4), (2, 4)] for a in ["signflip", "signflip_nc", "alie", "alie_nc"]]
    arms = ["sra", "sra_l10", "elect", "orcinf"]
    M = np.array([[R[(R.arm == arm) & (R.k == k) & (R.f == f) & (R.attack == a)].holds.mean() for (k, f, a) in cols] for arm in arms])
    fig, ax = plt.subplots(figsize=(W2, 1.65))
    im = ax.imshow(M, cmap="RdYlGn", vmin=0, vmax=1, aspect="auto")
    for i in range(M.shape[0]):
        for j in range(M.shape[1]):
            ax.text(j, i, f"{int(round(M[i, j] * 12))}/12", ha="center", va="center", fontsize=6.2)
    ax.set_yticks(range(len(arms))); ax.set_yticklabels([LAB[a] for a in arms])
    lab = {"signflip": "sign-flip", "signflip_nc": "sign-flip\n(no claim)", "alie": "ALIE", "alie_nc": "ALIE\n(no claim)"}
    ax.set_xticks(range(len(cols))); ax.set_xticklabels([lab[a] for _, _, a in cols], fontsize=5.8)
    for x in (3.5, 7.5): ax.axvline(x, color="k", lw=1)
    for x, s in [(1.5, "$k=6,\\ f=2\\leq\\hat F$ (must hold)"), (5.5, "$k=6,\\ f=4>\\hat F$ (base rule breaks)"),
                 (9.5, "$k=2,\\ f=4$ (liars outnumber witnesses)")]:
        ax.text(x, -0.9, s, ha="center", fontsize=6.5)
    ax.spines[:].set_visible(False)
    cb = fig.colorbar(im, ax=ax, fraction=0.025, pad=0.01); cb.set_label("share HOLDS (paired)", fontsize=6.5)
    save(fig, out, "fig09_robustness_map")

def fig_dp_sra(d, ref, out):
    fig, axs = plt.subplots(1, 4, figsize=(W2, 1.9), sharey=True)
    for ax, (ds, t) in zip(axs, TARGETS):
        s = d[(d.ds == ds) & (d.target == t) & (d.exp == "M5") & (d.k != 16)]
        for agg, arm, key, ls in [("fedavg", "base", "fedavg", "--"), ("cwmed", "base", "cwmed", "-"), ("cwmed", "sra", "sra", "-")]:
            m = s[(s["agg"] == agg) & (s.arm == arm)].groupby("k").target_recall.mean()
            ax.plot(m.index, m.values, "o", ls=ls, color=C[key], label={"fedavg": "FedAvg", "cwmed": "Coord. median (base)", "sra": "SRA"}[key])
        ax.set_title(TS(ds, t)); ax.set_xticks(GRID); ax.set_xlabel("witnesses $k$"); ax.set_ylim(-0.03, 1.05)
    axs[0].set_ylabel("target recall, DP $\\varepsilon=3$")
    axs[-1].legend(loc="upper left", bbox_to_anchor=(1.0, 1.0))
    save(fig, out, "fig10_dp_times_sra")

def fig_story(out):
    fig, ax = plt.subplots(figsize=(W2, 1.25)); ax.axis("off"); ax.set_xlim(0, 10); ax.set_ylim(0, 1.2)
    steps = [("1  Floor", "$k\\leq f$: nothing\ncan learn it", "#BBBBBB"),
             ("2  Witness tax", "robust rules need\n2-9 extra witnesses", "#D55E00"),
             ("3  Mechanism", "wall edge $=\\hat F$;\nDP noise reshapes it", "#E69F00"),
             ("4  Identity", "who the witnesses are\nremoves the tax", "#56B4E9"),
             ("5  SRA", "one bit + stratify:\nfloor, robustness kept", "#009E73")]
    for i, (h, b, c) in enumerate(steps):
        x = 0.1 + i * 2.0
        ax.add_patch(FancyBboxPatch((x, 0.1), 1.75, 1.0, boxstyle="round,pad=0.03", fc=c, alpha=0.25, ec=c, lw=1))
        ax.text(x + 0.875, 0.85, h, ha="center", fontsize=7.2, weight="bold")
        ax.text(x + 0.875, 0.4, b, ha="center", va="center", fontsize=6.2)
        if i < 4: ax.annotate("", xy=(x + 2.0, 0.6), xytext=(x + 1.8, 0.6), arrowprops=dict(arrowstyle="->", lw=0.9))
    save(fig, out, "fig00_story_arc")

# ---------------- tables ----------------
def tables(d, ref, R, out, rr):
    rows, fl = [], []
    for ds, t in TARGETS:
        r = ref[(ds, t)]
        for f in [0, 2, 4]:
            fa = ks_of(d, ds, t, "M3", "fedavg", "base", f, r)
            for g in ["cwmed", "trmean", "mkrum"]:
                row = {"dataset": ds, "target": t, "f": f, "agg": g, "FedAvg": kstr(fa)}
                for arm in ["base", "orcinf", "elect", "sra", "sra_l10", "sra_rr3", "sra_rr1", "sra_rand"]:
                    k = ks_of(d, ds, t, "M3", g, arm, f, r); row[arm] = kstr(k)
                    if arm in ("sra", "sra_l10"):
                        fl.append(dict(target=f"{t} ('{ds[2:]})", f=f, agg=g, arm=arm, kstar=kstr(k),
                                       prereg=floor_reached(k, f, False), censored=floor_reached(k, f, True)))
                rows.append(row)
    K = pd.DataFrame(rows); F = pd.DataFrame(fl)
    FS = F.groupby(["target", "arm"])[["prereg", "censored"]].mean().round(2).reset_index()
    RS = R.assign(zone=np.where(R.k <= R.f, "k<=f (bounded damage)", np.where(R.f <= F_HAT, "f<=F_HAT", "f>F_HAT"))) \
          .groupby(["arm", "zone"]).holds.agg(["sum", "count"]).reset_index()
    BRK = R[(R.arm == "sra") & (R.k > R.f) & (~R.holds)][["ds", "target", "k", "f", "attack", "agg", "base_fpr",
                                                           "base_other", "arm_fpr", "arm_other", "base_broken"]].round(3)
    M5 = []
    for ds, t in TARGETS:
        s = d[(d.ds == ds) & (d.target == t) & (d.exp == "M5")]
        rdp = s[(s["agg"] == "fedavg") & (s.k == 16)].target_recall.mean()
        for g in ["fedavg", "cwmed", "trmean", "mkrum"]:
            for arm in (["base"] if g == "fedavg" else ["base", "sra"]):
                m = s[(s["agg"] == g) & (s.arm == arm) & (s.k != 16)].groupby("k").target_recall.mean()
                M5.append(dict(target=f"{t} ('{ds[2:]})", agg=g, arm=arm, kstar_dp3=kstr(kstar(m.index, m.values, rdp))))
    M5 = pd.DataFrame(M5)
    os.makedirs(os.path.join(out, "tables"), exist_ok=True)
    for name, T in [("T1_kstar_all_arms", K), ("T2_floor_prereg_vs_censored", FS), ("T3_robustness_by_zone", RS),
                    ("T4_sra_breaks_k_gt_f", BRK), ("T5_dp_eps3_kstar", M5)]:
        T.to_csv(os.path.join(out, "tables", f"{name}.csv"), index=False)
        open(os.path.join(out, "tables", f"{name}.md"), "w").write(T.to_markdown(index=False))
        print(f"\n== {name}\n{T.to_string(index=False)}")
    print(f"\n== RR formula: within +-1 {rr[0]}/{rr[2]}, within +-2 {rr[1]}/{rr[2]}")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--csv17", default="mit2_runs_2017.csv"); ap.add_argument("--csv18", default="mit2_runs_2018.csv")
    ap.add_argument("--out", default="results"); a = ap.parse_args()
    os.makedirs(os.path.join(a.out, "figures"), exist_ok=True)
    d, ref = load(a.csv17, a.csv18)
    print("references:", {f"{k[1]} ('{k[0][2:]})": round(v, 3) for k, v in ref.items()})
    fig_story(a.out); fig_setup(a.out); fig_floor_tax(d, ref, a.out); fig_tax_heatmap(a.out); fig_wall(a.out)
    fig_dp(a.out); fig_sra_curves(d, ref, a.out); fig_frontier(d, ref, a.out)
    rr = fig_rr(d, ref, a.out); R = robustness_table(d); fig_robust_map(R, a.out); fig_dp_sra(d, ref, a.out)
    tables(d, ref, R, a.out, rr)

if __name__ == "__main__":
    main()
