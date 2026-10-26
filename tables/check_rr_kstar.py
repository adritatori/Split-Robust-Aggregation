#!/usr/bin/env python3
"""Recompute the randomized-flag check (paper Fig. 11b) from mit2_runs.csv.

Reads   results/{cicids2017,cse2018}/mit2/mit2_runs.csv   (exp M3, arms sra_rr1 and sra_rr3, seeds 0-2)
Writes  tables/rr_kstar_check.csv                         (one row per configuration, 72 rows)

The functions below are NOT reimplemented: they are executed verbatim from the exported notebook code
scripts/cicids2017/04_mit3_defense_aware.py (identical in the CSE-CIC-IDS2018 export):
estimate_kstar, ks_from, k_num, rr_predicted_kstar, rr_prob_kstar (with the one-line fix
cy[min(x - f - 1, len(cy) - 1)]), rr_match. This script only selects rows and counts.

Reading of the numbers
  * measured k-hat* = m on the grid {1,2,3,4,6,8} means the true value lies in the interval
    (previous grid point, m]; 'never' means above 8 (same reading as rr_match in the notebook).
  * a predicted k of 9 or more is beyond the grid maximum of 8 and counts as 'never'
    (for example the binomial prediction 11 at eps_w = 1, f = 4).
  * "between the two predictions": the measured interval overlaps [min, max] of the expected-count
    prediction (rr_predicted_kstar) and the binomial prediction (rr_prob_kstar).

Provenance: these numbers are recomputed here. They are not part of the saved run logs or the
CLAIMS_SUMMARY files, whose re-analysis step failed before the fix.
"""
import ast, math, os, sys
import numpy as np
import pandas as pd

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SRC = os.path.join(ROOT, "scripts", "cicids2017", "04_mit3_defense_aware.py")
NEEDED = ["LEARNABLE_FRAC", "N_CLIENTS", "estimate_kstar", "ks_from", "k_num",
          "rr_predicted_kstar", "rr_prob_kstar", "rr_match"]
K_GRID = [1, 2, 3, 4, 6, 8]
RULES = ["cwmed", "trmean", "mkrum"]
ARMS = {"sra_rr1": 1.0, "sra_rr3": 3.0}


def load_notebook_functions():
    text = open(SRC, encoding="utf-8").read()
    lines = text.splitlines()
    ns = {"np": np, "pd": pd, "math": math}
    for node in ast.parse(text).body:
        name = getattr(node, "name", None)
        if name is None and isinstance(node, ast.Assign) and isinstance(node.targets[0], ast.Name):
            name = node.targets[0].id
        if name in NEEDED:
            exec("\n".join(lines[node.lineno - 1:node.end_lineno]), ns)
    missing = [n for n in NEEDED if n not in ns]
    assert not missing, missing
    assert "len(cy) - 1" in text, "rr_prob_kstar does not carry the fix"
    return ns


def interval(m, grid=K_GRID):
    """Grid-censored reading of a measured k-hat*."""
    if m == "never":
        return max(grid) + 1, float("inf")
    m = int(m)
    return max([g for g in grid if g < m], default=0) + 1, m


def main():
    ns = load_notebook_functions()
    kmax = max(K_GRID)
    rows = []
    for ds, tag in (("CICIDS2017", "cicids2017"), ("CSE-CIC-IDS2018", "cse2018")):
        d = pd.read_csv(os.path.join(ROOT, "results", tag, "mit2", "mit2_runs.csv"))
        for target in sorted(d[d.exp == "M3"].target.unique()):
            ref = float(d[(d.exp == "REF") & (d.target == target)].target_recall.mean())
            for arm, eps in ARMS.items():
                for f in (0, 2, 4):
                    for rule in RULES:
                        sel = d[(d.exp == "M3") & (d.target == target) & (d["agg"] == rule) & (d.arm == arm) & (d.f == f)]
                        meas = ns["ks_from"](sel, "target_recall", ref, kmax)
                        pe, pp = ns["rr_predicted_kstar"](eps, f), ns["rr_prob_kstar"](eps, f)
                        lo, hi = interval(meas)
                        pe_n = 99 if pe is None else int(pe)
                        pp_n = 99 if pp is None else int(pp)
                        rows.append({
                            "dataset": ds, "target": target, "eps_w": eps, "f": f, "rule": rule,
                            "n_seeds": int(sel.seed.nunique()), "reference_recall": round(ref, 4),
                            "measured_kstar": meas, "interval_low": lo, "interval_high": hi,
                            "pred_expected": pe, "pred_binomial": pp,
                            "expected_within1": ns["rr_match"](meas, pe, K_GRID, 1),
                            "expected_within2": ns["rr_match"](meas, pe, K_GRID, 2),
                            "expected_below_interval": pe_n < lo, "expected_above_interval": pe_n > hi,
                            "binomial_within1": ns["rr_match"](meas, pp, K_GRID, 1),
                            "binomial_below_interval": pp_n < lo, "binomial_above_interval": pp_n > hi,
                            "measured_between_predictions": bool(hi >= min(pe_n, pp_n) and lo <= max(pe_n, pp_n)),
                        })
    df = pd.DataFrame(rows)
    out = os.path.join(ROOT, "tables", "rr_kstar_check.csv")
    df.to_csv(out, index=False)
    e1, e3 = df[df.eps_w == 1.0], df[df.eps_w == 3.0]
    print(f"configurations: {len(df)} (expected 72); seeds per configuration: {sorted(df.n_seeds.unique())}")
    print(f"expected-count prediction within 1 client: {int(df.expected_within1.sum())}/72; within 2: {int(df.expected_within2.sum())}/72")
    print(f"  eps_w=1 within 1: {int(e1.expected_within1.sum())}/36;  eps_w=3 prediction below the measured interval: {int(e3.expected_below_interval.sum())}/36")
    print(f"binomial prediction above the measured interval at eps_w=1: {int(e1.binomial_above_interval.sum())}/36")
    print(f"measured between the two predictions: {int(df.measured_between_predictions.sum())}/72")
    print("predicted k by (eps_w, f):", {(e, f): (g.pred_expected.iloc[0], g.pred_binomial.iloc[0]) for (e, f), g in df.groupby(["eps_w", "f"])})
    print("wrote", os.path.relpath(out, ROOT))


if __name__ == "__main__":
    sys.exit(main())
