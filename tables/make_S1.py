#!/usr/bin/env python3
"""Build tables/S1_coverage_thresholds.csv: k-hat* for learning-threshold (L_T) factors 0.5-0.9.

Source: results/{cicids2017,cse2018}/v3_2/expA_runs.csv (EXP-A, v3.2 baseline notebooks).

  0.5 and 0.8  -> stored by the notebook (columns kstar_05 / kstar of expA_kstar_<target>.csv).
                  This script re-derives them from expA_runs.csv and ABORTS unless all 160 rows match
                  the stored values exactly.
  0.6, 0.7, 0.9 -> derived post hoc from expA_runs.csv with the same function and the same rule.

The function `estimate_kstar` below is copied verbatim from the v3.2 notebooks
(notebooks/*/01_v3_2_baseline_*.ipynb; exported in scripts/*/01_v3_2_baseline_*.py).
verify_verbatim() checks that text against the exported scripts at run time.

The per-cell rule is the one in the notebooks' report_A(): mean target recall over ALL seeds present
for each k, at fixed (target, aggregator, f); the learnable line is factor x reference, where
reference = mean FedAvg recall at f = 0 and k = max k. Only non-private (eps = inf), multiclass
(binary = False), rmult = 1 rows are used. No new decision rule is introduced here.

NOT built here: a column for an "all-five-seeds rule". No such rule is defined in the notebooks or in any
CLAIMS_SUMMARY file, so it is not computed.

Usage:  python tables/make_S1.py --selftest   # synthetic checks only
        python tables/make_S1.py              # selftest, reproduce, derive, write
"""
import os, re, sys, inspect
import numpy as np
import pandas as pd

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
LEARNABLE_FRAC = 0.8                       # notebook constant (same value in both v3.2 notebooks)
STORED_FACTORS = {0.8: "kstar", 0.5: "kstar_05"}
DERIVED_FACTORS = [0.6, 0.7, 0.9]
EXPECTED_SEEDS = 5
DATASETS = {"CICIDS2017": "cicids2017", "CSE-CIC-IDS2018": "cse2018"}
VERBATIM_SRC = {"cicids2017": "scripts/cicids2017/01_v3_2_baseline_resume.py",
                "cse2018": "scripts/cse2018/01_v3_2_baseline_continue_full2.py"}


# ---- verbatim copy from the v3.2 notebooks (do not edit) -------------------------------------
def estimate_kstar(k_values, recalls, ref, frac=LEARNABLE_FRAC):
    ks = np.asarray(k_values); r = np.asarray(recalls, float)
    o = np.argsort(ks); ks, r = ks[o], r[o]
    ok = np.where(np.isnan(r), False, r >= frac * ref)
    if not len(ok) or not ok[-1]: return "never"
    j = len(ok) - 1
    while j - 1 >= 0 and ok[j - 1]: j -= 1
    return int(ks[j])
# ---- end verbatim ------------------------------------------------------------------------------


def verify_verbatim():
    mine = inspect.getsource(estimate_kstar).rstrip()
    for tag, rel in VERBATIM_SRC.items():
        t = open(os.path.join(ROOT, rel)).read()
        m = re.search(r"^def estimate_kstar\(.*?(?=^\S)", t, re.S | re.M)
        assert m and m.group(0).rstrip() == mine, f"estimate_kstar differs from {rel}"
        c = re.search(r"^LEARNABLE_FRAC\s*=\s*([0-9.]+)", t, re.M)
        assert c and float(c.group(1)) == LEARNABLE_FRAC, f"LEARNABLE_FRAC differs in {rel}"
    print("verify_verbatim: estimate_kstar and LEARNABLE_FRAC identical to both v3.2 notebooks")


def kstar_table(d, target, fracs):
    """Same selection and grouping as report_A() in the notebooks. Returns (ref, rows)."""
    d = d.copy()
    d["binary"] = d["binary"].astype(str).str.lower().isin(["true", "1"])
    d = d[(d.target == target) & (d.eps.astype(float) == float("inf")) & (~d.binary) & (d.rmult == 1)]
    ref = d[(d["agg"] == "fedavg") & (d.f == 0) & (d.k == d.k.max())].target_recall.mean()
    rows = []
    for agg in sorted(d["agg"].unique(), key=lambda a: list(d["agg"].unique()).index(a)):
        for f in sorted(d.f.unique()):
            sel = d[(d["agg"] == agg) & (d.f == f)]
            g = sel.groupby("k").target_recall.mean()
            seeds = sel.groupby("k").seed.nunique()
            row = {"target": target, "agg": agg, "f": int(f), "n_seeds_min": int(seeds.min()),
                   "n_seeds_max": int(seeds.max()), "n_k": int(len(g))}
            for fr in fracs:
                row[fr] = estimate_kstar(g.index.values, g.values, ref, fr)
            rows.append(row)
    return float(ref), rows


# ---- synthetic, messy checks (run before touching the real file) -----------------------------
def selftest():
    print("SYNTHETIC SELF-TEST of estimate_kstar (ref = 1.0, frac = 0.8 unless stated)")
    K = [1, 2, 3, 4, 6, 8]
    cases = [
        ("clean monotone", K, [0, 0, .5, .85, .9, .95], 1.0, .8, 4),
        ("non-monotone: dip in the middle, recovers", K, [.9, 0, .85, 0, .9, .95], 1.0, .8, 6),
        ("non-monotone: learned early, lost at the largest k", K, [.9, .9, .9, .9, .9, .5], 1.0, .8, "never"),
        ("blip above the line, then below, then fine", K, [0, .9, 0, 0, .85, .9], 1.0, .8, 6),
        ("tie exactly at L_T (0.8 >= 0.8*1.0)", K, [0, 0, .8, .8, .8, .8], 1.0, .8, 3),
        ("just below L_T", K, [0, 0, .7999, .8, .8, .8], 1.0, .8, 4),
        ("missing k (k=3 not tested)", [1, 2, 4, 8], [0, .85, .9, .95], 1.0, .8, 2),
        ("unsorted k, same as sorted", [8, 1, 4, 2, 6, 3], [.95, 0, .85, 0, .9, .5], 1.0, .8, 4),
        ("NaN recall at a middle k counts as not learned", K, [0, 0, .9, np.nan, .9, .9], 1.0, .8, 6),
        ("NaN at the largest k -> never", K, [0, 0, .9, .9, .9, np.nan], 1.0, .8, "never"),
        ("all NaN -> never", K, [np.nan] * 6, 1.0, .8, "never"),
        ("empty input -> never", [], [], 1.0, .8, "never"),
        ("single k above line", [8], [.9], 1.0, .8, 8),
        ("single k below line", [8], [.7], 1.0, .8, "never"),
        ("lower factor admits earlier k", K, [0, .55, .6, .85, .9, .95], 1.0, .5, 2),
        ("same curve, factor 0.9", K, [0, .55, .6, .85, .9, .95], 1.0, .9, 6),
    ]
    bad = 0
    for name, ks, rs, ref, fr, want in cases:
        got = estimate_kstar(ks, rs, ref, fr)
        ok = got == want; bad += not ok
        print(f"  [{'PASS' if ok else 'FAIL'}] {name:55s} -> {got!s:6s} (expected {want})")
    # float ties: the literal line 0.752 vs 0.8 * 0.94
    ref = 0.94
    line = 0.8 * ref
    got = estimate_kstar([1, 2], [0.0, 0.752], ref, 0.8)
    print(f"  [INFO] 0.8*0.94 = {line!r}; recall 0.752 at the line -> {got}  (ties are decided by float rounding)")
    # missing seed through the table builder: 5 seeds everywhere except one dropped row
    rng = np.random.default_rng(0)
    rows = []
    for s in range(5):
        for k in K:
            for agg in ("fedavg", "cwmed"):
                base = 0.0 if (agg == "cwmed" and k < 4) else 0.9
                rows.append(dict(target="T", k=k, f=0, agg=agg, eps=float("inf"), seed=s, binary=False, rmult=1,
                                 target_recall=base + rng.normal(0, .01)))
    d = pd.DataFrame(rows)
    d = d[~((d["agg"] == "cwmed") & (d.k == 3) & (d.seed == 4))]            # one missing seed in one cell
    ref, out = kstar_table(d, "T", [0.5, 0.8, 0.9])
    cw = [r for r in out if r["agg"] == "cwmed"][0]
    ok = cw["n_seeds_min"] == 4 and cw["n_seeds_max"] == 5 and cw[0.8] == 4
    bad += not ok
    print(f"  [{'PASS' if ok else 'FAIL'}] missing seed is visible (n_seeds_min={cw['n_seeds_min']}, max={cw['n_seeds_max']}), "
          f"cwmed k*(0.8)={cw[0.8]}")
    print(f"SELF-TEST: {'ALL PASSED' if not bad else str(bad) + ' FAILED'}")
    return bad == 0


# ---- real data ---------------------------------------------------------------------------------
def load():
    runs, stored = {}, {}
    for ds, tag in DATASETS.items():
        base = os.path.join(ROOT, "results", tag, "v3_2")
        runs[ds] = pd.read_csv(os.path.join(base, "expA_runs.csv"))
        for t in runs[ds]["target"].unique():
            p = os.path.join(base, f"expA_kstar_{t.replace(' ', '_')}.csv")
            stored[(ds, t)] = pd.read_csv(p)
    return runs, stored


def norm(v):
    return v if isinstance(v, str) else int(v)


def main():
    verify_verbatim()
    if not selftest():
        sys.exit("self-test failed; nothing computed")
    if "--selftest" in sys.argv:
        return
    runs, stored = load()
    allf = sorted(list(STORED_FACTORS) + DERIVED_FACTORS)
    out, mism, n_rows = [], [], 0
    for ds, d in runs.items():
        for t in d["target"].unique():
            ref, rows = kstar_table(d, t, allf)
            st = stored[(ds, t)]
            for r in rows:
                s = st[(st["agg"] == r["agg"]) & (st.f == r["f"])]
                assert len(s) == 1, (ds, t, r["agg"], r["f"])
                for fr, col in STORED_FACTORS.items():
                    n_rows += 1 if fr == 0.8 else 0
                    if str(norm(s.iloc[0][col])) != str(r[fr]):
                        mism.append((ds, t, r["agg"], r["f"], fr, s.iloc[0][col], r[fr]))
                out.append({"dataset": ds, "target": r["target"], "rule": r["agg"], "f": r["f"],
                            "n_seeds_min": r["n_seeds_min"], "n_seeds_max": r["n_seeds_max"],
                            **{f"kstar_{fr:.1f}": r[fr] for fr in allf}})
    print(f"reproduction of stored k-hat*: {n_rows} (dataset, target, rule, f) rows x 2 factors; mismatches: {len(mism)}")
    if mism:
        for m in mism: print("  MISMATCH", m)
        sys.exit("STOP: stored values not reproduced exactly; derived factors NOT computed")
    df = pd.DataFrame(out)
    seeds_ok = bool(((df.n_seeds_min == EXPECTED_SEEDS) & (df.n_seeds_max == EXPECTED_SEEDS)).all())
    print(f"rows: {len(df)}; seeds per (rule, f, k) cell: min {df.n_seeds_min.min()}, max {df.n_seeds_max.max()}")
    if not seeds_ok:
        sys.exit(f"STOP: not every cell has {EXPECTED_SEEDS} seeds; derived factors NOT written")
    dst = os.path.join(ROOT, "tables", "S1_coverage_thresholds.csv")
    df.drop(columns=["n_seeds_min", "n_seeds_max"]).to_csv(dst, index=False)
    print("wrote", os.path.relpath(dst, ROOT))


if __name__ == "__main__":
    main()
