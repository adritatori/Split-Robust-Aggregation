# =============================================================================
#  WITNESS-COUNT STUDY -- mit-3 analysis (final run): figures 11-15, tables T6-T9, updated story arc
#  Usage: python witness_analysis_mit3.py --m2_17 mit2_runs_2017.csv --m2_18 mit2_runs_2018.csv \
#                                         --m3_17 mit3_runs_2017.csv --m3_18 mit3_runs_2018.csv --out results
#  Needs witness_analysis.py (same folder) for shared style and helpers.
# =============================================================================
import argparse, os
import numpy as np, pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
from witness_analysis import (C, LAB, W1, W2, GRID, KMAX, NEVER, LEARN, TARGETS, TS, kstar, kn, save, paired)

ATT = ["fang_w", "minmax_w", "alie_w", "minmax_h", "fang_h", "split"]
ATT_LAB = {"fang_w": "Fang\n(in W)", "minmax_w": "min-max\n(in W)", "alie_w": "ALIE\n(in W)",
           "minmax_h": "min-max\n(in H)", "fang_h": "Fang\n(in H)", "split": "split\n(W + H)"}
BASE_OF = {"fang_h": "fang_w"}

def load3(a17, a18):
    x = pd.read_csv(a17); x["ds"] = "2017"; y = pd.read_csv(a18); y["ds"] = "2018"
    d = pd.concat([x, y], ignore_index=True)
    ref = d[d.exp == "REF"].groupby(["ds", "target"]).target_recall.mean().to_dict()
    return d, ref

def st(g):
    return (float(g.benign_fpr.mean()), float(g.other_attack_recall_mean.mean()), float(g.target_recall.mean()))

def m6_table(d, ref):
    rows = []
    m6 = d[d.exp == "M6"]
    for ds, t in TARGETS:
        x = m6[(m6.ds == ds) & (m6.target == t)]; line = LEARN * ref[(ds, t)]
        for k, f in [(3, 2), (6, 2), (6, 4), (2, 4)]:
            c = x[(x.k == k) & (x.f == f)]
            for a in ATT:
                fed = st(c[(c["agg"] == "fedavg") & (c.attack == BASE_OF.get(a, a))])
                for g in ["cwmed", "trmean", "mkrum"]:
                    b = st(c[(c["agg"] == g) & (c.arm == "base") & (c.attack == BASE_OF.get(a, a))])
                    for arm in ["sra", "sra_l10", "sra_cap"]:
                        s = st(c[(c["agg"] == g) & (c.arm == arm) & (c.attack == a)])
                        rows.append(dict(ds=ds, target=t, k=k, f=f, attack=a, agg=g, arm=arm,
                                         zone="k<=f" if k <= f else ("f<=F_HAT" if f <= 2 else "f>F_HAT"),
                                         holds=paired(b[0], b[1], s[0], s[1]), covered=s[2] >= line,
                                         recall=s[2], base_recall=b[2], fedavg_recall=fed[2], fpr=s[0], other=s[1],
                                         base_fpr=b[0], base_other=b[1], line=line))
    return pd.DataFrame(rows)

def fig_adaptive(R, out):
    fig, axs = plt.subplots(1, 2, figsize=(W2, 2.6), gridspec_kw={"width_ratios": [1.7, 1], "wspace": 0.3})
    ax = axs[0]; s = R[(R.zone == "f<=F_HAT") & (R.arm == "sra")]; x = np.arange(len(ATT)); w = 0.26
    for i, (col, key, lab) in enumerate([("fedavg_recall", "fedavg", "FedAvg"), ("base_recall", "base", "Robust rule (base)"),
                                         ("recall", "sra", "SRA")]):
        m = s.groupby("attack")[col].mean().reindex(ATT); lo = s.groupby("attack")[col].min().reindex(ATT)
        ax.bar(x + (i - 1) * w, m.values, w, color=C[key], label=lab, alpha=0.9)
        ax.errorbar(x + (i - 1) * w, m.values, yerr=[m.values - lo.values, np.zeros(len(x))], fmt="none", ecolor="k", lw=0.6, capsize=1.5)
    ax.axhline(s.line.mean(), color="#777777", ls=":", lw=0.8); ax.text(5.45, s.line.mean() + 0.02, "learnable", fontsize=5.8, ha="right")
    ax.set_xticks(x); ax.set_xticklabels([ATT_LAB[a] for a in ATT], fontsize=6.3); ax.set_ylim(0, 1.08)
    ax.set_ylabel("rare-attack recall under attack"); ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.28), ncol=3, fontsize=6)
    ax.set_title("(a) Rare-attack recall, $f=2\\leq\\hat F$ (whisker = worst cell)", loc="left")
    ax = axs[1]; zones = ["f<=F_HAT", "f>F_HAT", "k<=f"]; zl = ["$f\\leq\\hat F$", "$f>\\hat F$", "$k\\leq f$\n(liars majority)"]
    for i, arm in enumerate(["sra", "sra_l10", "sra_cap"]):
        v = [R[(R.arm == arm) & (R.zone == z)].holds.mean() for z in zones]
        ax.bar(np.arange(3) + (i - 1) * 0.26, v, 0.26, color=C.get(arm, "#CC79A7") if arm != "sra_cap" else "#CC79A7", label=LAB.get(arm, "SRA, capped W weight (post-hoc)"))
        for j, z in enumerate(zones):
            n = int(R[(R.arm == arm) & (R.zone == z)].holds.sum()); tot = len(R[(R.arm == arm) & (R.zone == z)])
            ax.text(j + (i - 1) * 0.26, 0.04, f"{n}/{tot}", ha="center", fontsize=4.6, rotation=90, va="bottom", color="w")
    ax.set_xticks(range(3)); ax.set_xticklabels(zl, fontsize=6.3); ax.set_ylim(0, 1.05)
    ax.set_ylabel("share HOLDS (paired vs base)"); ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.28), fontsize=5.3)
    ax.set_title("(b) Robustness by zone", loc="left")
    save(fig, out, "fig11_adaptive_attacks")

def fig_dp_alie(d, out):
    m7 = d[(d.exp == "M7") & (d["agg"] != "fedavg")].copy(); m7["dp"] = np.isfinite(m7.eps)
    fig, axs = plt.subplots(1, 2, figsize=(W2, 2.4), sharey=False, gridspec_kw={"wspace": 0.25})
    labs = [TS(ds, t) for ds, t in TARGETS]; x = np.arange(len(TARGETS)); w = 0.2
    for ax, (att, ttl) in zip(axs, [("alie", "(a) ALIE"), ("fang_w", "(b) Fang inside W")]):
        for i, (arm, dp, col, hatch, lab) in enumerate([("base", False, C["base"], "", "base, non-private"),
                                                         ("base", True, C["base"], "///", "base, DP $\\varepsilon$=3"),
                                                         ("sra", False, C["sra"], "", "SRA, non-private"),
                                                         ("sra", True, C["sra"], "///", "SRA, DP $\\varepsilon$=3")]):
            v = [m7[(m7.ds == ds) & (m7.target == t) & (m7.arm == arm) & (m7.dp == dp) & (m7.attack == att)].target_recall.mean() for ds, t in TARGETS]
            ax.bar(x + (i - 1.5) * w, v, w, color=col, alpha=0.9 if not dp else 0.45, hatch=hatch, edgecolor="k", lw=0.3, label=lab)
        ax.set_xticks(x); ax.set_xticklabels(labs, fontsize=6.2, rotation=20, ha="right"); ax.set_ylim(0, 1.08); ax.set_title(ttl, loc="left")
    axs[0].set_ylabel("rare-attack recall ($k$=6, $f$=2)"); axs[1].legend(loc="upper left", bbox_to_anchor=(1.0, 1.0), fontsize=6)
    save(fig, out, "fig12_dp_arms_the_attacker")

def fig_floor_k5(d, ref, out):
    m8 = d[d.exp == "M8"]
    fig, ax = plt.subplots(figsize=(W1 + 0.6, 2.1)); x = np.arange(len(TARGETS)); w = 0.2
    for i, (agg, arm, key, lab) in enumerate([("fedavg", "base", "fedavg", "FedAvg"), (None, "base", "base", "Robust rule (base, mean of 3)"),
                                              (None, "sra", "sra", "SRA"), (None, "sra_cap", "sra_l10", "SRA capped (post-hoc)")]):
        v = []
        for ds, t in TARGETS:
            s = m8[(m8.ds == ds) & (m8.target == t) & (m8.arm == arm)]
            s = s[s["agg"] == "fedavg"] if agg == "fedavg" else s[s["agg"] != "fedavg"]
            v.append(s.target_recall.mean())
        ax.bar(x + (i - 1.5) * w, v, w, color=C[key], label=lab, alpha=0.9 if key != "sra_l10" else 0.5)
    for j, (ds, t) in enumerate(TARGETS):
        ax.hlines(LEARN * ref[(ds, t)], j - 0.45, j + 0.45, color="#555555", ls=":", lw=0.8)
    ax.set_xticks(x); ax.set_xticklabels([TS(ds, t) for ds, t in TARGETS], fontsize=6.5); ax.set_ylim(0, 1.08)
    ax.set_ylabel("rare-attack recall"); ax.legend(loc="upper left", bbox_to_anchor=(1.0, 1.0), fontsize=6)
    ax.set_title("Exactly at the floor: $k=f+1=5$ witnesses vs $f=4$ attackers", loc="left")
    save(fig, out, "fig13_floor_measured_k5")

def boot(df, ref, B=500, seed=0):
    piv = df.pivot_table(index="seed", columns="k", values="target_recall", aggfunc="mean")
    if not len(piv): return None, None, None
    pt = kn(kstar(piv.columns.values, piv.mean(0).values, ref)); rng = np.random.default_rng(seed); bs = []
    for _ in range(B):
        s = rng.choice(len(piv), len(piv), replace=True); bs.append(kn(kstar(piv.columns.values, piv.iloc[s].mean(0).values, ref)))
    return pt, float(np.percentile(bs, 5)), float(np.percentile(bs, 95))

def kstar5(m2, d3, ref):
    rows = []
    for ds, t in TARGETS:
        a = m2[(m2.ds == ds) & (m2.target == t) & (m2.exp == "M3") & (m2.arm.isin(["base", "sra", "sra_l10"]))]
        b = d3[(d3.ds == ds) & (d3.target == t) & (d3.exp == "M9")]
        x = pd.concat([a, b], ignore_index=True); r = ref[(ds, t)]
        for f in [0, 2, 4]:
            for agg, arm in [("fedavg", "base"), ("cwmed", "base"), ("trmean", "base"), ("mkrum", "base"),
                             ("cwmed", "sra"), ("trmean", "sra"), ("mkrum", "sra"), ("cwmed", "sra_l10"), ("trmean", "sra_l10"), ("mkrum", "sra_l10")]:
                s = x[(x["agg"] == agg) & (x.arm == arm) & (x.f == f)]
                p, lo, hi = boot(s, r)
                rows.append(dict(ds=ds, target=t, f=f, agg=agg, arm=arm, seeds=s.seed.nunique(), kstar=p, lo=lo, hi=hi))
    return pd.DataFrame(rows)

def fig_kstar5(K, out):
    fig, axs = plt.subplots(1, 4, figsize=(W2, 2.0), sharey=True)
    for ax, (ds, t) in zip(axs, TARGETS):
        ax.fill_between([-0.4, 4.4], [-0.4, 4.4], 0, color="#EEEEEE", zorder=0); ax.plot([-0.4, 4.4], [0.6, 5.4], "k:", lw=0.8)
        for o, (agg, arm, key, lab) in zip([-0.15, -0.05, 0.05, 0.15], [("fedavg", "base", "fedavg", "FedAvg"), ("cwmed", "base", "cwmed", "Coord. median"),
                                                                    ("mkrum", "base", "mkrum", "Multi-Krum"), ("cwmed", "sra", "sra", "SRA (on coord. median)")]):
            s = K[(K.ds == ds) & (K.target == t) & (K["agg"] == agg) & (K.arm == arm)].sort_values("f")
            ax.errorbar(s.f + o, s.kstar, yerr=[s.kstar - s.lo, s.hi - s.kstar], fmt="o-", color=C[key], label=lab, capsize=1.5, lw=1.1 if arm != "sra" else 1.6)
        ax.set_title(TS(ds, t)); ax.set_xticks([0, 2, 4]); ax.set_xlabel("Byzantine members $f$"); ax.set_ylim(0, 9.8)
        ax.set_yticks([1, 2, 3, 4, 5, 6, 7, 8, NEVER]); ax.set_yticklabels(["1", "2", "3", "4", "5", "6", "7", "8", ">8"])
    axs[0].set_ylabel("$k^*$ (5 seeds, 90% bootstrap)"); axs[-1].legend(loc="upper left", bbox_to_anchor=(1.0, 1.0), fontsize=6)
    save(fig, out, "fig14_kstar_5_seeds")

def fig_story7(out):
    fig, ax = plt.subplots(figsize=(W2, 1.35)); ax.axis("off"); ax.set_xlim(0, 14); ax.set_ylim(0, 1.2)
    steps = [("1 Floor", "$k\\leq f$: nothing\ncan learn it", "#BBBBBB"),
             ("2 Witness tax", "robust rules need\n2-9 extra witnesses", "#D55E00"),
             ("3 Wall at $\\hat F$", "not a delay;\nedge $=\\hat F$ (46/48)", "#E69F00"),
             ("4 Identity", "removes the tax;\nclaims gameable", "#56B4E9"),
             ("5 SRA", "one bit + strata:\nfloor, 48/48 robust", "#009E73"),
             ("6 Adaptive", "6 SRA-aware attacks:\n144/144 robust", "#0072B2"),
             ("7 Trilemma", "DP noise dissolves\nwall AND arms ALIE", "#CC79A7")]
    for i, (h, b, c) in enumerate(steps):
        x = 0.05 + i * 2.0
        ax.add_patch(FancyBboxPatch((x, 0.1), 1.8, 1.0, boxstyle="round,pad=0.03", fc=c, alpha=0.25, ec=c, lw=1))
        ax.text(x + 0.9, 0.87, h, ha="center", fontsize=6.6, weight="bold"); ax.text(x + 0.9, 0.42, b, ha="center", va="center", fontsize=4.9)
        if i < 6: ax.annotate("", xy=(x + 2.0, 0.6), xytext=(x + 1.85, 0.6), arrowprops=dict(arrowstyle="->", lw=0.8))
    save(fig, out, "fig00_story_arc")

def tables(R, d, ref, K, out):
    os.makedirs(os.path.join(out, "tables"), exist_ok=True)
    T6 = R.groupby(["arm", "zone"]).agg(paired_holds=("holds", "sum"), covered=("covered", "sum"), cells=("holds", "size")).reset_index()
    T6b = R[(R.zone == "f<=F_HAT") & (R.arm == "sra")].groupby("attack").agg(
        sra_mean=("recall", "mean"), sra_worst=("recall", "min"), base_mean=("base_recall", "mean"),
        fedavg_mean=("fedavg_recall", "mean")).reindex(ATT).round(3).reset_index()
    T6c = R[(R.arm == "sra") & (~R.holds)][["ds", "target", "k", "f", "attack", "agg", "fpr", "other", "base_fpr", "base_other", "recall"]].round(3)
    m7 = d[(d.exp == "M7") & (d["agg"] != "fedavg")].copy(); m7["dp"] = np.isfinite(m7.eps); rows = []
    for ds, t in TARGETS:
        for arm in ["base", "sra"]:
            for dp in [False, True]:
                c = m7[(m7.ds == ds) & (m7.target == t) & (m7.arm == arm) & (m7.dp == dp)]
                cl = c[c.attack == "mimic"]
                for a in ["signflip", "alie", "fang_w", "minmax_h"]:
                    at = c[c.attack == a]
                    rows.append(dict(target=TS(ds, t), arm=arm, dp="eps=3" if dp else "none", attack=a,
                                     target_recall=round(at.target_recall.mean(), 3),
                                     fpr_rise=round(at.benign_fpr.mean() - cl.benign_fpr.mean(), 3),
                                     other_drop=round(cl.other_attack_recall_mean.mean() - at.other_attack_recall_mean.mean(), 3)))
    T7 = pd.DataFrame(rows)
    m8 = d[d.exp == "M8"]
    T8 = m8.assign(agg2=np.where(m8["agg"] == "fedavg", "fedavg", "robust")).groupby(["ds", "target", "arm", "agg2"]).target_recall.mean().round(3).unstack(["arm", "agg2"])
    T8.columns = [f"{a}|{b}" for a, b in T8.columns]; T8 = T8.reset_index()
    T8["learnable_line"] = [round(LEARN * ref[(ds, t)], 3) for ds, t in zip(T8.ds, T8.target)]
    K2 = K.assign(ci=[f"{p:.0f} [{l:.0f},{h:.0f}]" if p is not None else "-" for p, l, h in zip(K.kstar, K.lo, K.hi)])
    T9 = K2.pivot_table(index=["ds", "target", "f"], columns=["arm", "agg"], values="ci", aggfunc="first").reset_index()
    T9.columns = ["|".join([c for c in col if c]) if isinstance(col, tuple) else col for col in T9.columns]
    for name, T in [("T6_adaptive_by_zone", T6), ("T6b_adaptive_target_recall", T6b), ("T6c_sra_adaptive_breaks", T6c),
                    ("T7_dp_x_attacks", T7), ("T8_floor_k5_f4", T8), ("T9_kstar_5seeds_ci", T9)]:
        T.to_csv(os.path.join(out, "tables", f"{name}.csv"), index=False)
        open(os.path.join(out, "tables", f"{name}.md"), "w").write(T.to_markdown(index=False))
        print(f"\n== {name}\n{T.to_string(index=False)}")

def main():
    ap = argparse.ArgumentParser()
    for k, v in [("m2_17", "mit2_runs_2017.csv"), ("m2_18", "mit2_runs_2018.csv"), ("m3_17", "mit3_runs_2017.csv"), ("m3_18", "mit3_runs_2018.csv"), ("out", "results")]:
        ap.add_argument(f"--{k}", default=v)
    a = ap.parse_args(); os.makedirs(os.path.join(a.out, "figures"), exist_ok=True)
    d3, ref = load3(a.m3_17, a.m3_18); m2, _ = load3(a.m2_17, a.m2_18)
    R = m6_table(d3, ref); K = kstar5(m2, d3, ref)
    fig_story7(a.out); fig_adaptive(R, a.out); fig_dp_alie(d3, a.out); fig_floor_k5(d3, ref, a.out); fig_kstar5(K, a.out)
    tables(R, d3, ref, K, a.out)

if __name__ == "__main__":
    main()
