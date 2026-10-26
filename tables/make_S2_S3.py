#!/usr/bin/env python3
"""Extract tables S2 and S3 from files already in the repo (S1 is built by make_S1.py).

Nothing is recomputed except plain means of stored per-run recalls (S2), used to cross-check the printed
summary. k-hat* values and the learning threshold are copied from the notebook's own printed output.

  S2_portscan_dp_eps3.csv  <- results/cicids2017/mit2/mit2_runs.csv (exp M5, Portscan, f = 0, eps = 3, seeds 0-2)
                              + results/cicids2017/mit2/CLAIMS_SUMMARY_MIT2_cicids2017.md (stored k-hat*, threshold)
  S3_class_counts.csv      <- saved stdout of notebooks/*/01_v3_2_baseline_*.ipynb ("Final class counts (train / test)")
"""
import glob, json, os, re, sys
import numpy as np
import pandas as pd

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
OUT = os.path.join(ROOT, "tables")
DATASETS = {"CICIDS2017": "cicids2017", "CSE-CIC-IDS2018": "cse2018"}


def md_block(text, head_prefix):
    for b in re.split(r"\n(?=## )", text):
        if b.startswith(head_prefix):
            return b
    raise KeyError(head_prefix)


def s2():
    base = os.path.join(ROOT, "results", "cicids2017", "mit2")
    d = pd.read_csv(os.path.join(base, "mit2_runs.csv"))
    m = d[(d.exp == "M5") & (d.target == "Portscan") & (d.f == 0) & (d.eps == 3.0)]
    ref = m[(m["agg"] == "fedavg") & (m.k == 16)].target_recall
    md = open(os.path.join(base, "CLAIMS_SUMMARY_MIT2_cicids2017.md")).read()
    ref_txt = float(re.search(r"DP reference FedAvg k=16: ([0-9.]+)", md_block(md, "## Portscan | M5 mean target recall under DP")).group(1))
    line_txt = float(re.search(r"learnable line 0\.8x DP reference = ([0-9.]+)", md_block(md, "## Portscan | M5 k* under DP")).group(1))
    print(f"S2: DP reference from runs file = {ref.mean():.4f} ({len(ref)} seeds); printed in summary = {ref_txt}")
    if round(ref.mean(), 3) != ref_txt:
        sys.exit("STOP: DP reference recall in the runs file does not match the printed summary")
    # stored k-hat* rows: " 0 trmean   4 (tax 0) 3 (tax 0)"; fedavg has only the base column
    kblock = md_block(md, "## Portscan | M5 k* under DP")
    ks = {}
    for ln in kblock.splitlines():
        mm = re.match(r"\s*0\s+(\w+)\s+(.*)$", ln)
        if not mm: continue
        agg, rest = mm.group(1), mm.group(2)
        cells = re.findall(r"(\d+|never)\s*\((?:tax (-?\d+)|floor (\d+))\)", rest)
        arms = ["base"] if agg == "fedavg" else ["base", "sra"]
        for arm, (k, tax, floor) in zip(arms, cells):
            ks[(agg, arm)] = (k, tax if tax != "" else "", f"floor {floor}" if floor else "")
    rows = []
    for (agg, arm), g in m.groupby(["agg", "arm"]):
        for k, gg in g.groupby("k"):
            kstar, tax, note = ks.get((agg, arm), ("", "", ""))
            rows.append({"dataset": "CICIDS2017", "target": "Portscan", "eps": 3.0, "f": 0, "agg": agg, "arm": arm,
                         "k": int(k), "n_seeds": int(gg.seed.nunique()), "mean_target_recall": round(gg.target_recall.mean(), 4),
                         **{f"recall_seed{int(sd)}": round(float(v), 4) for sd, v in gg.groupby("seed").target_recall.mean().items()},
                         "kstar_stored": kstar, "tax_vs_fedavg_dp_stored": tax, "kstar_note": note,
                         "dp_reference_recall": round(ref.mean(), 4), "learnable_line_stored": line_txt,
                         "source_runs": "results/cicids2017/mit2/mit2_runs.csv",
                         "source_summary": "results/cicids2017/mit2/CLAIMS_SUMMARY_MIT2_cicids2017.md"})
    df = pd.DataFrame(rows).sort_values(["agg", "arm", "k"]).reset_index(drop=True)
    # cross-check against the printed 2-decimal table
    tbl = md_block(md, "## Portscan | M5 mean target recall under DP")
    bad = 0
    cur = None
    for ln in tbl.splitlines():
        mm = re.match(r"(\w+)\s+(base|sra)\s+([0-9. ]+)$", ln.strip()) or re.match(r"(base|sra)\s+([0-9. ]+)$", ln.strip())
        if not mm: continue
        if mm.lastindex == 3: cur, arm, vals = mm.group(1), mm.group(2), mm.group(3)
        else: arm, vals = mm.group(1), mm.group(2)
        for k, v in zip([1, 2, 3, 4, 6, 8], vals.split()):
            got = df[(df["agg"] == cur) & (df.arm == arm) & (df.k == k)].mean_target_recall
            if len(got) != 1 or abs(round(got.iloc[0], 2) - float(v)) > 1e-9: bad += 1
    print(f"S2: {len(df)} rows; mismatches vs printed table: {bad}")
    if bad: sys.exit("STOP: recomputed means differ from the printed M5 table")
    df.to_csv(os.path.join(OUT, "S2_portscan_dp_eps3.csv"), index=False)
    return len(df)


def last_block(text, title, nxt_blank=True):
    i = text.rfind(title)
    if i < 0: return None
    lines = text[i:].splitlines()[2:]
    out = []
    for ln in lines:
        if not ln.strip(): break
        out.append(ln)
    return out


def s3():
    rows = []
    for ds, tag in DATASETS.items():
        nb = glob.glob(os.path.join(ROOT, "notebooks", tag, "01_v3_2_baseline_*.ipynb"))[0]
        j = json.load(open(nb))
        txt = "".join(j["cells"][0]["outputs"][0]["text"])
        fin = last_block(txt, "Final class counts (train / test)")
        clean = last_block(txt, "Clean counts (Normal = sampled clean / rate -> estimated full)")
        cc = {}
        for ln in clean or []:
            m = re.match(r"\s+(.+?)\s+clean\s+([\d,]+)\s+full-data estimate\s+([\d,]+)", ln)
            if m: cc[m.group(1).strip()] = (int(m.group(2).replace(",", "")), int(m.group(3).replace(",", "")))
        for ln in fin:
            m = re.match(r"\s+(.+?)\s+([\d,]+)\s*/\s*([\d,]+)\s*$", ln)
            c, tr, te = m.group(1).strip(), int(m.group(2).replace(",", "")), int(m.group(3).replace(",", ""))
            rows.append({"dataset": ds, "class": c, "final_train": tr, "final_test": te,
                         "source_file": os.path.relpath(nb, ROOT)})
    df = pd.DataFrame(rows)
    print(f"S3: {len(df)} rows")
    df.to_csv(os.path.join(OUT, "S3_class_counts.csv"), index=False)
    return len(df)


if __name__ == "__main__":
    s2(); s3()
