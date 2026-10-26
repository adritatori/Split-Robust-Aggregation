# Exported verbatim from notebooks/cse2018/03_mit2_sra.ipynb (single code cell). The notebook is the canonical source.
# =============================================================================
#  WITNESS-COUNT mit-2.0  SPLIT ROBUST AGGREGATION (SRA)  --  CSE-CIC-IDS2018  --  standalone, Kaggle-ready
# =============================================================================
#  Built on witness v3.2 + mit-1.0 (same loader, cleaning, partitions, model, trainer, calibration, and
#  every earlier Phase-0 self-test, which are rerun as a regression suite).  New in mit-2.0:
#
#  SRA: each member sends ONE bit "I have evidence of the target class" (optionally randomized response).
#       H = non-claimants -> base robust rule a_H.  W = claimants -> coordinate-wise median a_W.
#       a = a_H + (|W|/N) * clip_(lambda_W * tau)(a_W - a_H),  lambda_W = 3 (pre-registered), tau = honest radius.
#
#  M3  COVERAGE.  Problem: can the robust federation reach the P1 floor k* = f + 1?
#      Arms base | orcinf, elect (mit-1.0 anchors) | sra | sra_rr1 | sra_rr3 | sra_rand; f in (0, 2, 4).
#      + sra_l10 (POST-HOC diagnostic, lambda_W = 10): separates "SRA fails" from "lambda = 3 clips too hard"
#        (realistic synthetic data: stratum ratio 3.2-3.6, lambda = 3 clipped 84% of rounds).  Secondary headline only.
#      Negative result: sra does not remove the tax at f = 0 -> the representation wall is not a vote count
#      inside W (unlikely: orcinf removed it).
#  M4  ROBUSTNESS.  Sign-flip x10 and ALIE (z = 1), attackers claiming W and not claiming; (k, f) in
#      (6, 2), (6, 4) [k > f: must hold] and (2, 4) [liar-majority W: bounded damage].  PAIRED verdict vs the base
#      rule under the same attack.  Negative result: SRA breaks where base holds at k > f -> only VERIFIED
#      identity can do it; the paper ends on the frontier result.
#  M5  DP.  eps = 3, f = 0, base vs sra.
#  HEADLINE: TIGHT_FIX | PARTIAL | NO_SAFE_POINT_CONFIRMED.  Stop rule: last mitigation experiment -> write.
#
#  HOW TO RUN (Kaggle): Accelerator = GPU, Internet = ON (opacus for M5).
#    Inputs: the dataset (as in v3.2) + the v3.2 FULL output of THIS dataset (calibration and data_cache.npz; the mit-1.0 output also works for the cache).
#    Resumable: if the session stops, save the version, attach its output as an input, run again.
#    RUN_TARGETS = ["<one target>"] runs one target per session.
#    Last section of the log (+ CLAIMS_SUMMARY_MIT2_<tag>.md) = evidence table; raw rows in mit2_runs.csv.
#  Rough GPU cost: ~2-2.5 h for 2 targets (Brute Force, Botnet); R = 30-50 rounds.
# =============================================================================

import os, sys, glob, time, math, json, warnings, hashlib, subprocess, shutil, tempfile
import numpy as np
import pandas as pd
warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=FutureWarning)

# -----------------------------------------------------------------------------
# CONFIG
# -----------------------------------------------------------------------------
DATASET = "CSE-CIC-IDS2018"
VERSION = "mit2"              # resume key of THIS script
DATA_VERSION = "v3"           # v3.2 data cache / calibration are reused
SCRIPT_VERSION = "mit-2.0"    # display only
MODE = "FULL"                 # "QUICK" | "FULL"  (final v3.2 run = FULL)
RUN_TARGETS = None            # None = all eligible (up to N_TARGETS); or e.g. ["Botnet"]
RUN_EXP_A, RUN_EXP_QA, RUN_EXP_D, RUN_EXP_K0, RUN_EXP_B, RUN_EXP_C = False, False, False, False, False, False  # v3.2 grids not rerun
FORCE_PAST_PREFLIGHT = False  # True = run grids even if G1/G6 fail (NOT for paper numbers)
ONLY_SELF_TEST = False
DATA_PATH = None              # None -> auto-resolve under /kaggle/input
TIME_BUDGET_H = 11.0          # Kaggle sessions stop at 12 h; stop cleanly before that

ATTEMPTED_POLICY = "drop"     # "Attempted" flows (Engelen et al. 2021) are dropped
DROP_PORTS = True             # ports are a known shortcut (Arp et al., USENIX Sec 2022)
MAX_MISSING_FRAC = 0.5
NORMAL_SAMPLE_RATE = 0.035    # ~2.1M of 59.4M benign flows streamed in
TRAIN_CAP = {"Normal": 1_000_000, "_default": 300_000}
INTERNAL_PREFIX = "172.31."   # testbed's internal address space (AWS VPC)

N_CLIENTS = 20
F_HAT = 2
M_TARGET = 500                # TOTAL target training samples split over k witnesses
N_BG = 3000                   # background samples per client
BG_TEMPER = 0.5               # background class mix p ~ count^0.5  (state in paper)
RARE_SHARE = 0.01             # target must be < 1% of all (clean) flows
MIN_TEST = 100

LOCAL_STEPS = 10
BATCH = 128
SERVER_LR = 1.0
EVAL_EVERY = 5
LEARNABLE_FRAC = 0.8
DP_DELTA = 1e-5

# calibration + gates (pre-registered)
R_CAL_LIST = [150, 300]       # retry longer if a curve is not converged
PLATEAU_FRAC_MAX = 0.7        # plateau must be reached by 0.7 x R_CAL
RISE_TOL = 0.03               # last-20% mean minus previous-20% mean
LR_GRID = [0.05, 0.1, 0.3]
DP_LR_GRID = [0.05, 0.2, 0.5]
DP_CLIP_GRID = [0.1, 1.0, 5.0]
FPR_MAX = 0.05                # G6a
DEAD_RECALL = 0.05            # G6b
REF_MIN = 0.5                 # G6c
QA_MAJORITY = 0.75            # Q-A verdict: share of tax cells that must agree
LONG_MULT = 3                 # EXP-D: rounds multiplier
DELAY_GAIN = 0.2              # EXP-D: "PARTIAL" if recall gains >= this

if MODE == "QUICK":
    N_TARGETS = 1
    K_GRID = [1, 2, 3, 5, 8, 12, 16]
    F_GRID = [0, 1, 2, 4]
    SEEDS = [0, 1, 2]
    EPS_GRID = [1.0, 3.0, 10.0, float("inf"), -1.0]
    K_GRID_DP = [1, 3, 8, 16]
    AGGS_DP = ["fedavg", "cwmed", "trmean"]
    SEEDS_DP = [0, 1, 2]
    B_TARGETS = "all"
    K_GRID_QA = [1, 2, 3, 5, 8, 16]
    SEEDS_QA = [0, 1, 2]
    SEEDS_D = [0, 1, 2]
else:
    N_TARGETS = 3
    K_GRID = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 16]
    F_GRID = [0, 1, 2, 4]
    SEEDS = [0, 1, 2, 3, 4]
    EPS_GRID = [1.0, 3.0, 10.0, float("inf"), -1.0]
    K_GRID_DP = [1, 2, 3, 4, 6, 8, 12, 16]
    AGGS_DP = ["fedavg", "cwmed", "trmean", "mkrum"]
    SEEDS_DP = [0, 1, 2]
    B_TARGETS = "first"       # EXP-B (most expensive): "first" | "all" | list of class names
    B_TARGETS = ["Botnet", "Brute Force"]  # 2018: Botnet = comparable with 2017; BF completes its QUICK DP grid
    K_GRID_QA = [1, 2, 3, 4, 5, 6, 8, 12, 16]
    SEEDS_QA = [0, 1, 2]
    SEEDS_D = [0, 1, 2]

AGGS = ["fedavg", "cwmed", "trmean", "mkrum", "geomed", "bucket_cwmed", "cclip", "nnm_cwmed"]
# cclip     : centered clipping (Karimireddy, He, Jaggi, ICML 2021), centre = previous aggregate,
#             3 iterations, radius = median distance to the centre (scale-free).
# nnm_cwmed : nearest-neighbour mixing (Allouah et al., AISTATS 2023) -- each update replaced by the
#             mean of its N - F_HAT nearest neighbours -- then coordinate-wise median.  SOTA for
#             Byzantine robustness under heterogeneity, i.e. exactly the regime k lives in.
K0_AGGS = ["fedavg", "cwmed"]  # EXP-K0: zero-witness control (aggregator barely matters at k=0)

# developer smoke test (tiny grids on synthetic CSVs) -- never set on Kaggle
if os.environ.get("WITNESS_SMOKE"):
    DATA_PATH = os.environ.get("WITNESS_DATA"); MODE = "SMOKE"; N_TARGETS = 2
    K_GRID, F_GRID, SEEDS = [1, 3, 8], [0, 2], [0]
    K_GRID_DP, AGGS_DP, SEEDS_DP, EPS_GRID = [1], ["fedavg"], [0], [3.0, float("inf"), -1.0]
    K_GRID_QA, SEEDS_QA, SEEDS_D, B_TARGETS = [1, 3, 8], [0], [0], "first"
    R_CAL_LIST, LR_GRID, DP_LR_GRID, DP_CLIP_GRID = [30, 60], [0.3], [0.5], [5.0]
    N_BG, M_TARGET, MIN_TEST, AGGS = 150, 60, 10, ["fedavg", "cwmed", "trmean"]
    LONG_MULT, RARE_SHARE = 2, 0.2
    FORCE_PAST_PREFLIGHT = bool(os.environ.get("WITNESS_FORCE"))
    TIME_BUDGET_H = float(os.environ.get("WITNESS_BUDGET_H", TIME_BUDGET_H))
    NORMAL_SAMPLE_RATE = 0.5

CLASSES = []                  # set by the loader
T0 = time.time()
STOPPED = {"flag": False}

# -----------------------------------------------------------------------------
import torch

def ensure_opacus():
    try:
        import opacus  # noqa
        return True
    except ImportError:
        print("  opacus missing -> trying `pip install opacus` (needs Kaggle Internet ON)")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", "opacus"])
            import importlib; importlib.invalidate_caches()
            import opacus  # noqa
            print("  opacus installed OK"); return True
        except Exception as e:
            print(f"  [WARN] could not install opacus ({type(e).__name__}). DP experiments disabled.")
            return False

HAVE_OPACUS = ensure_opacus()
import torch.nn as nn
import torch.nn.functional as F
from torch.func import functional_call, vmap, grad
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

DEV = torch.device("cuda" if torch.cuda.is_available() else "cpu")
TAG = "cse2018"
OUT_BASENAME = f"witness_{VERSION}_{TAG}"
PREV_BASENAME = f"witness_{DATA_VERSION}_{TAG}"   # v3.2 output (calibration, data cache)
OUT_DIR = os.environ.get("WITNESS_OUT") or (f"/kaggle/working/{OUT_BASENAME}" if os.path.isdir("/kaggle/working")
                                            else os.path.abspath(f"./{OUT_BASENAME}"))
FIG_DIR = os.path.join(OUT_DIR, "figures")
os.makedirs(FIG_DIR, exist_ok=True)

def banner(t): print("\n" + "=" * 76 + f"\n  {t}\n" + "=" * 76, flush=True)
def sub(t): print("\n  " + "-" * 60 + f"\n  {t}\n  " + "-" * 60, flush=True)
def fname(s): return s.replace(" ", "_")
def eps_name(e): return "clip-only" if e < 0 else ("non-private" if not np.isfinite(e) else f"eps={e:g}")
def out_of_time(): return (time.time() - T0) > TIME_BUDGET_H * 3600

# =============================================================================
#  LABELS  (same macro mapping for CICIDS2017 and CSE-CIC-IDS2018)
# =============================================================================
CIC_CLASSES = ["Normal", "DoS", "DDoS", "Portscan", "Brute Force", "Botnet", "Web Attack"]

def cic_label(raw):
    s = str(raw).strip().lower()
    for ch in ["\u2013", "\u2014", "\ufffd", "\x96"]:
        s = s.replace(ch, "-")
    att = "attempted" in s
    if s in ("benign", "normal", ""): return "Normal", False
    if "heartbleed" in s: return "PROBE_Heartbleed", att
    if "infiltration" in s or "infilteration" in s: return "PROBE_Infiltration", att
    if "web attack" in s or "xss" in s or "sql" in s: return "Web Attack", att
    if "patator" in s or "brute" in s: return "Brute Force", att
    if "ddos" in s or "loit" in s: return "DDoS", att
    if s.startswith("dos") or any(w in s for w in ["hulk", "goldeneye", "slowloris", "slowhttp"]): return "DoS", att
    if "portscan" in s or "port scan" in s: return "Portscan", att
    if "bot" in s: return "Botnet", att
    return "UNKNOWN", att

def apply_attempted(macro, att, policy):
    if not att or macro.startswith("PROBE") or macro == "Normal": return macro
    return {"merge_parent": macro, "benign": "Normal"}.get(policy, "DROP")

def map_label(raw): return apply_attempted(*cic_label(raw), ATTEMPTED_POLICY)

# =============================================================================
#  CLEANING HELPERS (tested in Phase 0)
# =============================================================================
CIC_ID_COLS = {"flow id", "src ip", "dst ip", "timestamp", "src ip dec", "dst ip dec",
               "attempted category", "id", "_source_file", "label"}

def remove_conflicts_and_dups(F_df, labels):
    """Drop every row whose feature vector appears with >1 label, then exact duplicates."""
    h = pd.util.hash_pandas_object(F_df, index=False).values
    tmp = pd.DataFrame({"h": h, "y": labels})
    nlab = tmp.groupby("h")["y"].nunique()
    bad = nlab[nlab > 1].index
    conflict = tmp["h"].isin(bad).values
    dup = tmp.duplicated(subset=["h", "y"], keep="first").values
    keep = ~conflict & ~dup
    rep = {"conflicting_rows": int(conflict.sum()), "exact_duplicates": int((dup & ~conflict).sum()),
           "conflict_by_class": pd.Series(np.asarray(labels)[conflict]).value_counts().to_dict()}
    return keep, rep

def fit_transform_numeric(X_tr, X_te):
    X_tr = X_tr.astype(np.float64, copy=True); X_te = X_te.astype(np.float64, copy=True)
    X_tr[~np.isfinite(X_tr)] = np.nan; X_te[~np.isfinite(X_te)] = np.nan
    med = np.nanmedian(X_tr, 0); med[~np.isfinite(med)] = 0
    for X in (X_tr, X_te):
        r, c = np.where(np.isnan(X)); X[r, c] = med[c]
    X_tr = np.sign(X_tr) * np.log1p(np.abs(X_tr)); X_te = np.sign(X_te) * np.log1p(np.abs(X_te))
    mu, sd = X_tr.mean(0), X_tr.std(0) + 1e-6
    f = lambda X: np.clip((X - mu) / sd, -10, 10).astype(np.float32)
    return f(X_tr), f(X_te)

def select_targets(class_counts, y_tr, y_te, classes, m_target, min_test, rare_share):
    """class_counts: {class name: clean count in the FULL dataset (estimated if sampled)}."""
    tot = float(sum(class_counts.values())); rows = []
    for i, c in enumerate(classes):
        if c == "Normal": continue
        share = class_counts.get(c, 0) / tot if tot > 0 else 0.0
        ntr, nte = int(np.sum(y_tr == i)), int(np.sum(y_te == i))
        reasons = []
        if share >= rare_share: reasons.append(f"share {100*share:.2f}% >= {100*rare_share:.0f}%")
        if ntr < m_target: reasons.append(f"train {ntr} < M_TARGET {m_target}")
        if nte < min_test: reasons.append(f"test {nte} < {min_test}")
        rows.append({"class": c, "share_%": round(100 * share, 3), "train": ntr, "test": nte,
                     "eligible": not reasons, "why_not": "; ".join(reasons)})
    rep = pd.DataFrame(rows)
    elig = rep[rep.eligible].sort_values("share_%")["class"].tolist() if len(rep) else []
    return elig, rep

def stratified_split(y, classes, rng, test_frac=0.3, cap_normal=30000, cap_other=5000):
    tr, te = [], []
    for c in range(len(classes)):
        idx = rng.permutation(np.where(y == c)[0]); n_te = int(test_frac * len(idx))
        te.append(idx[:min(n_te, cap_normal if c == 0 else cap_other)]); tr.append(idx[n_te:])
    return np.concatenate(tr).astype(int), np.concatenate(te).astype(int)

def finish_split(F_tr, F_te, y_tr, y_te, feat_cols, extra_tr=None, extra_te=None):
    """Drop mostly-missing columns, remove test rows duplicating train, scale (train stats only)."""
    Xm = F_tr.to_numpy(np.float64, na_value=np.nan)
    frac_bad = np.mean(~np.isfinite(Xm), 0)
    keep_cols = [c for c, fb in zip(feat_cols, frac_bad) if fb <= MAX_MISSING_FRAC]
    dropped = [c for c in feat_cols if c not in keep_cols]
    print(f"  columns dropped (> {int(100*MAX_MISSING_FRAC)}% missing in train): {dropped if dropped else 'none'}")
    F_tr, F_te = F_tr[keep_cols], F_te[keep_cols]
    h_tr = set(pd.util.hash_pandas_object(F_tr, index=False).values)
    h_te = pd.util.hash_pandas_object(F_te, index=False).values
    leak = np.array([h in h_tr for h in h_te], dtype=bool)
    print(f"  test rows identical to a train row (removed, leakage): {int(leak.sum()):,}")
    F_te, y_te = F_te[~leak], y_te[~leak]
    if extra_te is not None: extra_te = extra_te[~leak]
    n_bad = int(np.sum(~np.isfinite(F_tr.to_numpy(np.float64, na_value=np.nan))))
    Xtr, Xte = fit_transform_numeric(F_tr.to_numpy(np.float64, na_value=np.nan),
                                     F_te.to_numpy(np.float64, na_value=np.nan))
    print(f"  non-finite train cells imputed with train medians: {n_bad:,}")
    print(f"  final features: {len(keep_cols)}")
    return Xtr, Xte, y_tr, y_te, keep_cols

def resolve_path(patterns):
    if DATA_PATH and os.path.isdir(DATA_PATH): return DATA_PATH
    for pat in patterns:
        hits = glob.glob(f"/kaggle/input/**/{pat}", recursive=True)
        if hits: return os.path.dirname(hits[0])
    raise FileNotFoundError("Set DATA_PATH to the dataset folder")

def read_csv_any(p, **kw):
    try: df = pd.read_csv(p, low_memory=False, **kw)
    except UnicodeDecodeError: df = pd.read_csv(p, low_memory=False, encoding="latin-1", **kw)
    df.columns = [str(c).strip() for c in df.columns]
    return df

# =============================================================================
#  DATA LOADER
# =============================================================================
def print_label_table(raw_counts):
    sub(f"Raw label -> macro (ATTEMPTED_POLICY='{ATTEMPTED_POLICY}')")
    for r, n in sorted(raw_counts.items(), key=lambda t: -t[1]):
        print(f"    {str(r)[:46]:46s} {n:>11,} -> {map_label(r)}")

def _find_cache():
    cands = [os.path.join(OUT_DIR, "data_cache.npz")]
    for base in (OUT_BASENAME, f"witness_mit1_{TAG}", PREV_BASENAME):
        cands += glob.glob(f"/kaggle/input/**/{base}/data_cache.npz", recursive=True)
    return [c for c in cands if os.path.exists(c)]

def _cache_meta():
    return {"version": VERSION, "rate": NORMAL_SAMPLE_RATE, "att": ATTEMPTED_POLICY, "ports": DROP_PORTS,
            "cap": TRAIN_CAP, "classes": CIC_CLASSES, "internal": INTERNAL_PREFIX}

def _subnets(src, dst):
    s = pd.Series(np.asarray(src, dtype=object)).astype(str)
    d = pd.Series(np.asarray(dst, dtype=object)).astype(str)
    ip = np.where(d.str.startswith(INTERNAL_PREFIX), d, np.where(s.str.startswith(INTERNAL_PREFIX), s, ""))
    sn = np.array(pd.Series(ip).str.rsplit(".", n=1).str[0].to_numpy(dtype=object), dtype=object, copy=True)
    sn[ip == ""] = "external"
    return sn

def _read_file(fp, cols, rate, file_seed):
    """Stream one CSV. Returns (X float32, macro, subnet, raw label counts, normal rows seen).
    Every row draws one uniform (same sequence for pyarrow and pandas paths), so the benign
    sample is identical whichever reader succeeds."""
    raw_feats, raw_lab, raw_src, raw_dst = cols
    def process(labels, getX, getS, getD, rng, acc):
        u, inv = np.unique(np.asarray(labels, dtype=str), return_inverse=True)
        for name, n in zip(u, np.bincount(inv, minlength=len(u))): acc["raw"][name] = acc["raw"].get(name, 0) + int(n)
        macro = np.array([map_label(x) for x in u], dtype=object)[inv]
        draw = rng.random(len(macro))
        keep = np.isin(macro, CLASSES)
        isn = macro == "Normal"
        acc["normal_seen"] += int(np.sum(keep & isn))
        keep &= (~isn) | (draw < rate)
        if keep.any():
            acc["X"].append(getX(keep)); acc["y"].append(macro[keep])
            acc["sn"].append(_subnets(getS(keep), getD(keep)) if raw_src and raw_dst
                             else np.full(int(keep.sum()), "external", dtype=object))
    def fresh(): return {"X": [], "y": [], "sn": [], "raw": {}, "normal_seen": 0}
    use = raw_feats + [raw_lab] + [c for c in (raw_src, raw_dst) if c]
    try:
        import pyarrow as pa, pyarrow.csv as pacsv
        types = {c: pa.float32() for c in raw_feats}; types.update({c: pa.string() for c in use if c not in raw_feats})
        reader = pacsv.open_csv(fp, read_options=pacsv.ReadOptions(block_size=64 << 20),
                                convert_options=pacsv.ConvertOptions(include_columns=use, column_types=types))
        rng, acc = np.random.default_rng(file_seed), fresh()
        for b in reader:
            lab = b.column(use.index(raw_lab)).to_numpy(zero_copy_only=False)
            def getX(m, b=b):
                fb = b.filter(pa.array(m))
                return np.column_stack([fb.column(i).to_numpy(zero_copy_only=False) for i in range(len(raw_feats))]).astype(np.float32)
            gs = (lambda m, b=b: b.column(use.index(raw_src)).to_numpy(zero_copy_only=False)[m]) if raw_src else None
            gd = (lambda m, b=b: b.column(use.index(raw_dst)).to_numpy(zero_copy_only=False)[m]) if raw_dst else None
            process(lab, getX, gs, gd, rng, acc)
        acc["reader"] = "pyarrow"
    except Exception as e:
        print(f"      [note] pyarrow reader failed ({type(e).__name__}: {str(e)[:80]}) -> pandas fallback")
        rng, acc = np.random.default_rng(file_seed), fresh()
        for ch in pd.read_csv(fp, usecols=use, chunksize=1_000_000, low_memory=False, dtype=str):
            lab = ch[raw_lab].astype(str).to_numpy()
            def getX(m, ch=ch):
                return ch.loc[m, raw_feats].apply(pd.to_numeric, errors="coerce").to_numpy(np.float32)
            gs = (lambda m, ch=ch: ch.loc[m, raw_src].to_numpy()) if raw_src else None
            gd = (lambda m, ch=ch: ch.loc[m, raw_dst].to_numpy()) if raw_dst else None
            process(lab, getX, gs, gd, rng, acc)
        acc["reader"] = "pandas"
    return acc

def load_data(path=None, rate=None, use_cache=True, write_cache=True):
    """CSE-CIC-IDS2018, corrected release (Liu et al., IEEE CNS 2022)."""
    global CLASSES
    CLASSES = CIC_CLASSES
    rate = NORMAL_SAMPLE_RATE if rate is None else rate
    banner("SECTION 1 -- LOAD + CLEAN CSE-CIC-IDS2018 (corrected release, streamed)")
    if use_cache:
        for cp in _find_cache():
            try:
                z = np.load(cp, allow_pickle=True); meta = json.loads(str(z["meta"]))
                if {k: v for k, v in meta.items() if k != "version"} == \
                   {k: v for k, v in json.loads(json.dumps(_cache_meta())).items() if k != "version"}:
                    print(f"  loaded cleaned data from cache: {cp}")
                    D = {k: z[k] for k in ["Xtr", "Xte", "ytr", "yte", "days_tr", "subnet_tr", "subnet_names"]}
                    D["class_counts"] = json.loads(str(z["class_counts"])); D["feats"] = list(z["feats"])
                    D["bg_counts"] = {CLASSES.index(c): v for c, v in D["class_counts"].items()}
                    print(f"  train {len(D['ytr']):,} | test {len(D['yte']):,} | features {D['Xtr'].shape[1]}")
                    return D
                print(f"  [note] cache {cp} built with different settings -> ignored")
            except Exception as e:
                print(f"  [note] cache {cp} unreadable ({type(e).__name__}) -> ignored")
    path = path or resolve_path(["Friday-02-03-2018.csv", "*02-03-2018*.csv"]); print(f"  DATA_PATH -> {path}")
    files = sorted(glob.glob(os.path.join(path, "*.csv")))
    if not files: raise FileNotFoundError(f"no CSV files in {path}")
    raw_hdr = list(pd.read_csv(files[0], nrows=0).columns)
    strip = {str(c).strip(): c for c in raw_hdr}
    head = read_csv_any(files[0], nrows=5000)
    lab = next((c for c in head.columns if c.lower() == "label"), None) or \
          next(c for c in head.columns if "label" in c.lower() and "attempt" not in c.lower())
    feats = [c for c in head.columns if c.lower() not in CIC_ID_COLS and c != lab
             and pd.api.types.is_numeric_dtype(head[c])]
    if DROP_PORTS: feats = [c for c in feats if "port" not in c.lower()]
    src = next((c for c in head.columns if c.lower() == "src ip"), None)
    dst = next((c for c in head.columns if c.lower() == "dst ip"), None)
    cols = ([strip[c] for c in feats], strip[lab], strip.get(src) if src else None, strip.get(dst) if dst else None)
    print(f"  {len(files)} files | features {len(feats)} | benign sample rate {rate} | IP columns: {bool(src and dst)}")
    Xs, ys, sns, days, raw, n_norm = [], [], [], [], {}, 0
    t0 = time.time()
    for fp in files:
        seed = int(hashlib.md5(os.path.basename(fp).encode()).hexdigest()[:8], 16)
        acc = _read_file(fp, cols, rate, seed)
        n = sum(len(v) for v in acc["y"]); tot = sum(acc["raw"].values())
        print(f"    {os.path.basename(fp):28s} rows={tot:>11,} kept={n:>9,} ({acc['reader']}, {time.time()-t0:.0f}s)", flush=True)
        for k_, v in acc["raw"].items(): raw[k_] = raw.get(k_, 0) + v
        n_norm += acc["normal_seen"]
        if n:
            Xs.append(np.concatenate(acc["X"])); ys.append(np.concatenate(acc["y"])); sns.append(np.concatenate(acc["sn"]))
            days.append(np.full(n, os.path.basename(fp).lower().replace(".csv", ""), dtype=object))
    print_label_table(raw)
    X = np.concatenate(Xs); macro = np.concatenate(ys); sn = np.concatenate(sns); day = np.concatenate(days)
    del Xs, ys, sns
    print(f"\n  benign flows seen {n_norm:,}, sampled {int(np.sum(macro=='Normal')):,}; attack flows kept {int(np.sum(macro!='Normal')):,}")
    Fdf = pd.DataFrame(X, columns=feats); del X
    keep, rep = remove_conflicts_and_dups(Fdf, macro)
    print(f"  conflicting-label rows removed: {rep['conflicting_rows']:,}  by class: {rep['conflict_by_class']}")
    print(f"  exact duplicates removed: {rep['exact_duplicates']:,}")
    Fdf = Fdf[keep].reset_index(drop=True); macro, sn, day = macro[keep], sn[keep], day[keep]
    y = pd.Series(macro).map({c: i for i, c in enumerate(CLASSES)}).to_numpy().astype(int)
    clean = {c: int(np.sum(y == i)) for i, c in enumerate(CLASSES)}
    class_counts = dict(clean); class_counts["Normal"] = int(round(clean["Normal"] / rate)) if rate > 0 else 0
    sub("Clean counts (Normal = sampled clean / rate -> estimated full)")
    for c in CLASSES: print(f"    {c:15s} clean {clean[c]:>10,}   full-data estimate {class_counts[c]:>12,}")
    tr, te = stratified_split(y, CLASSES, np.random.default_rng(0))
    capped = []
    for i, c in enumerate(CLASSES):
        idx = tr[y[tr] == i]; cap = TRAIN_CAP.get(c, TRAIN_CAP["_default"])
        capped.append(idx[:cap])
        if len(idx) > cap: print(f"    train pool {c} capped {len(idx):,} -> {cap:,} (background only)")
    tr = np.concatenate(capped)
    Xtr, Xte, ytr, yte, fk = finish_split(Fdf.loc[tr].reset_index(drop=True), Fdf.loc[te].reset_index(drop=True),
                                          y[tr], y[te], feats)
    cat = pd.Categorical(sn[tr])
    D = dict(Xtr=Xtr, Xte=Xte, ytr=ytr, yte=yte, days_tr=day[tr].astype(str), class_counts=class_counts,
             feats=fk, subnet_tr=cat.codes.astype(np.int32), subnet_names=np.array(cat.categories, dtype=str))
    D["bg_counts"] = {CLASSES.index(c): v for c, v in class_counts.items()}
    if write_cache:
      try:
        np.savez(os.path.join(OUT_DIR, "data_cache.npz"), Xtr=Xtr, Xte=Xte, ytr=ytr, yte=yte, days_tr=D["days_tr"],
                 subnet_tr=D["subnet_tr"], subnet_names=D["subnet_names"], feats=np.array(fk, dtype=str),
                 class_counts=json.dumps(class_counts), meta=json.dumps(_cache_meta()))
        print(f"  cache written: {os.path.join(OUT_DIR, 'data_cache.npz')}")
      except Exception as e:
        print(f"  [WARN] cache not written ({type(e).__name__})")
    return D

# =============================================================================
#  PARTITIONERS
# =============================================================================
def build_witness_partition(y_train, target_idx, k, f, n_clients, m_target, n_bg, bg_temper, rng, bg_counts=None):
    """Roles 'W' witness, 'H' honest non-witness, 'A' attacker.
    Exactly k honest clients hold target samples (total m_target, split evenly); each attacker
    holds ceil(m/k) target samples relabelled Normal (perfect mimicry); every client holds n_bg
    background samples.  bg_counts {class idx: count} sets the tempered mix (defaults to the
    pool sizes) -- used when pools are sub-sampled/capped so the mix still follows the data."""
    if k < 0: raise ValueError("k must be >= 0")
    if k == 0 and f > 0: raise ValueError("k = 0 control is defined for f = 0 only")
    if k + f > n_clients: raise ValueError(f"k + f = {k+f} exceeds n_clients = {n_clients}")
    tgt_pool = np.where(y_train == target_idx)[0]
    if len(tgt_pool) < k: raise ValueError(f"only {len(tgt_pool)} target samples for {k} witnesses")
    m_eff = min(m_target, len(tgt_pool)) if k > 0 else 0
    per_w = np.full(k, m_eff // k) if k > 0 else np.zeros(0, int)
    if k > 0: per_w[: m_eff % k] += 1
    tgt_perm = rng.permutation(tgt_pool)
    bg_classes = [c for c in np.unique(y_train) if c != target_idx]
    counts = np.array([float(bg_counts.get(int(c), np.sum(y_train == c))) if bg_counts else float(np.sum(y_train == c))
                       for c in bg_classes])
    p = counts ** bg_temper; p /= p.sum()
    pools = {c: np.where(y_train == c)[0] for c in bg_classes}
    roles = np.array(["H"] * n_clients, dtype=object)
    order = rng.permutation(n_clients); roles[order[:f]] = "A"; roles[order[f:f + k]] = "W"
    clients, cursor, w = [], 0, 0
    for i in range(n_clients):
        n_per = rng.multinomial(n_bg, p)
        bg = np.concatenate([rng.choice(pools[c], size=n, replace=len(pools[c]) < n)
                             for c, n in zip(bg_classes, n_per) if n > 0])
        idx, ov = bg, np.full(len(bg), -1)
        if roles[i] == "W":
            t = tgt_perm[cursor: cursor + per_w[w]]; cursor += per_w[w]; w += 1
            idx = np.concatenate([bg, t]); ov = np.concatenate([ov, np.full(len(t), -1)])
        elif roles[i] == "A":
            n_att = int(math.ceil(m_eff / k))
            t = rng.choice(tgt_pool, size=n_att, replace=n_att > len(tgt_pool))
            idx = np.concatenate([bg, t]); ov = np.concatenate([ov, np.zeros(len(t), int)])
        clients.append((idx.astype(int), ov))
    return clients, roles, m_eff

def build_daylock_clients(ytr, dtr, n_clients, n_classes, rng, per_class_cap=800, per_client=4000):
    """Natural structure: each capture day split into n_clients // n_days sub-clients.
    A class's witness count = number of sub-clients whose day contains it."""
    days = sorted(np.unique(dtr)); spd = max(1, n_clients // len(days))
    clients, wk, comp = [], {c: 0 for c in range(1, n_classes)}, []
    for dn in days:
        in_day = np.where(dtr == dn)[0]; splits = [[] for _ in range(spd)]
        for c in range(1, n_classes):
            pool = rng.permutation(in_day[ytr[in_day] == c])
            if len(pool) < spd: continue
            wk[c] += spd
            for s in range(spd): splits[s].append(pool[s::spd][:per_class_cap])
        norm = rng.permutation(in_day[ytr[in_day] == 0])
        for s in range(spd):
            have = sum(len(a) for a in splits[s]); splits[s].append(norm[s::spd][:max(0, per_client - have)])
            idx = np.concatenate(splits[s]).astype(int)
            if len(idx) == 0: continue
            clients.append((idx, np.full(len(idx), -1)))
            comp.append({"client": len(clients) - 1, "day": dn, **{c: int(np.sum(ytr[idx] == c)) for c in range(n_classes)}})
    return clients, wk, comp

# =============================================================================
#  AGGREGATORS  ([N, P] flattened deltas -> [P])
# =============================================================================
def agg_fedavg(U, **kw): return U.mean(0)
def agg_cwmed(U, **kw):
    S, _ = torch.sort(U, dim=0); n = U.shape[0]
    return S[n // 2] if n % 2 else 0.5 * (S[n // 2 - 1] + S[n // 2])
def agg_trmean(U, b=F_HAT, **kw):
    S, _ = torch.sort(U, dim=0); n = U.shape[0]; b = min(b, (n - 1) // 2)
    return S[b:n - b].mean(0)
def agg_mkrum(U, b=F_HAT, **kw):
    n = U.shape[0]; D = torch.cdist(U, U) ** 2; m = max(1, n - b - 2)
    scores = torch.sort(D, dim=1).values[:, 1:m + 1].sum(1)
    return U[torch.argsort(scores)[: max(1, n - b)]].mean(0)
def agg_geomed(U, iters=30, eps=1e-8, **kw):
    z = U.mean(0)
    for _ in range(iters):
        w = 1.0 / torch.clamp(torch.norm(U - z, dim=1), min=eps)
        z_new = (w[:, None] * U).sum(0) / w.sum()
        if torch.norm(z_new - z) < 1e-7: return z_new
        z = z_new
    return z
def agg_bucket_cwmed(U, s=2, gen=None, **kw):
    n = U.shape[0]; perm = torch.randperm(n, generator=gen).to(U.device)
    Up = U[perm]; nb = int(math.ceil(n / s))
    return agg_cwmed(torch.stack([Up[j * s: min((j + 1) * s, n)].mean(0) for j in range(nb)]))
def agg_cclip(U, prev=None, iters=3, **kw):
    """Centered clipping.  Centre = previous round's aggregate (zeros in round 1); radius = median
    distance of the updates to the current centre, recomputed each iteration."""
    v = torch.zeros(U.shape[1], device=U.device, dtype=U.dtype) if prev is None else prev.clone()
    for _ in range(iters):
        d = U - v; nr = torch.norm(d, dim=1)
        tau = torch.median(nr)
        scale = torch.clamp(tau / torch.clamp(nr, min=1e-12), max=1.0)
        v = v + (d * scale[:, None]).mean(0)
    return v
def agg_nnm_cwmed(U, b=F_HAT, **kw):
    """Nearest-neighbour mixing then coordinate-wise median."""
    n = U.shape[0]; m = max(1, n - b)
    idx = torch.topk(torch.cdist(U, U), m, dim=1, largest=False).indices   # includes self (distance 0)
    return agg_cwmed(U[idx].mean(1))
AGG_FN = {"fedavg": agg_fedavg, "cwmed": agg_cwmed, "trmean": agg_trmean,
          "mkrum": agg_mkrum, "geomed": agg_geomed, "bucket_cwmed": agg_bucket_cwmed,
          "cclip": agg_cclip, "nnm_cwmed": agg_nnm_cwmed}
ALL_AGGS = list(AGG_FN)

def predicted_kstar(agg, f, n=N_CLIENTS, b=F_HAT):
    if agg == "fedavg": return f + 1
    if agg in ("cwmed", "geomed"): return n // 2 + 1
    if agg == "trmean": return max(b, f) + 1
    return None

# =============================================================================
#  DECISION LOGIC (every rule here is tested on messy synthetic data in Phase 0)
# =============================================================================
def estimate_kstar(k_values, recalls, ref, frac=LEARNABLE_FRAC):
    ks = np.asarray(k_values); r = np.asarray(recalls, float)
    o = np.argsort(ks); ks, r = ks[o], r[o]
    ok = np.where(np.isnan(r), False, r >= frac * ref)
    if not len(ok) or not ok[-1]: return "never"
    j = len(ok) - 1
    while j - 1 >= 0 and ok[j - 1]: j -= 1
    return int(ks[j])

def smooth3(v):
    v = np.nan_to_num(np.asarray(v, float), nan=0.0)
    if len(v) < 3: return v
    p = np.r_[v[0], v, v[-1]]
    return (p[:-2] + p[1:-1] + p[2:]) / 3.0

def find_plateau(rounds, vals, frac=0.95, min_final=0.05):
    """First round after which the (3-pt smoothed) curve stays >= frac * final.
    final = mean of the last 3 smoothed points.  None if the curve never exceeds min_final."""
    v = smooth3(vals)
    if not len(v): return None
    final = float(np.mean(v[-3:]))
    if final < min_final: return None
    for i in range(len(v)):
        if np.min(v[i:]) >= frac * final: return int(rounds[i])
    return int(rounds[-1])

def curve_converged(rounds, vals, r_cal, frac_max=PLATEAU_FRAC_MAX, rise_tol=RISE_TOL):
    """G1 (v3).  ok = True/False, or None if the curve never learned (a finding, not a budget issue)."""
    R = np.asarray(rounds); v = smooth3(vals); p = find_plateau(R, vals)
    if p is None: return {"ok": None, "plateau": None, "rise": float("nan"), "why": "never rose above 0.05"}
    w = max(2, int(round(0.2 * len(v))))
    rise = float(np.mean(v[-w:]) - np.mean(v[-2 * w:-w])) if len(v) >= 2 * w else float("nan")
    late = p > frac_max * r_cal; rising = not (np.isfinite(rise) and rise <= rise_tol)
    why = "ok" if not (late or rising) else " & ".join(
        ([f"plateau {p} > {frac_max}x{r_cal}"] if late else []) + ([f"last-20% rise {rise:+.3f} > {rise_tol}"] if rising else []))
    return {"ok": not (late or rising), "plateau": int(p), "rise": rise, "why": why}

def g1_curve_ok(name, c):
    """A calibration curve passes G1 if converged.  The FedAvg k=1 curve may also pass if it never
    learned (a finding) or if it is still creeping but ALREADY above the learnable line -- more rounds
    cannot change that cell's verdict.  A k=1 curve creeping below the line fails."""
    if c["ok"] is True: return True
    return name.startswith("k=1") and (c["ok"] is None or bool(c.get("above_line", False)))

def preflight_gate(conv, ref_recall, target, classes):
    """G1 + G6, evaluated on calibration output BEFORE any grid.
    conv: {curve name: curve_converged dict}; the 'k=1 target' curve may be None (never learned).
    ref_recall: {class name: recall at the calibrated reference}; classes absent from test are skipped."""
    reasons, ok = [], True
    for nm, c in conv.items():
        if not g1_curve_ok(nm, c):
            ok = False; reasons.append(f"G1 FAIL: '{nm}' not converged ({c['why']})")
        elif c["ok"] is False:
            reasons.append(f"G1 NOTE: '{nm}' still creeping but already above the learnable line -> accepted")
    fpr = 1 - ref_recall.get("Normal", float("nan"))
    if not (np.isfinite(fpr) and fpr <= FPR_MAX + 1e-12):
        ok = False; reasons.append(f"G6a FAIL: benign FPR {fpr:.3f} > {FPR_MAX} at reference")
    dead = [c for c in classes if c not in ("Normal", target) and c in ref_recall
            and not (np.isfinite(ref_recall[c]) and ref_recall[c] >= DEAD_RECALL)]
    if dead:
        ok = False; reasons.append(f"G6b FAIL: dead non-target classes at reference {dead}")
    rt = ref_recall.get(target, float("nan"))
    if not (np.isfinite(rt) and rt >= REF_MIN):
        ok = False; reasons.append(f"G6c FAIL: target reference recall {rt:.3f} < {REF_MIN}")
    if ok: reasons.insert(0, "pre-flight passed (G1, G6)")
    return {"GO": ok, "reasons": reasons}

def gate_decision(d, kstars, ref):
    """Post-EXP-A gates G2-G5 (unchanged from v2; G1 moved to pre-flight)."""
    reasons, ok = [], True
    robust = [a for a in d["agg"].unique() if a != "fedavg"]
    r0 = [kstars.get((a, 0)) for a in robust]
    if not any((isinstance(v, (int, np.integer)) and v > 1) or v == "never" for v in r0):
        ok = False; reasons.append("G2 FAIL: every robust aggregator learns from k=1 -> witness story not supported")
    cells = [v for (a, f), v in kstars.items() if a != "fedavg"]
    if cells and np.mean([v == "never" for v in cells]) > 0.5:
        ok = False; reasons.append("G3 FAIL: boundary above largest k for most cells -> extend K_GRID")
    g = d.groupby(["agg", "f", "k"]).target_recall
    sds = g.std().fillna(0)
    if (sds > 0.25).mean() > 0.2:
        reasons.append(f"G4 FLAG: {100*(sds>0.25).mean():.0f}% of cells have seed sd>0.25 -> report per seed")
    means = g.mean().round(3); sd0 = sds < 0.005
    plateau_vals = means[sd0 & (means > 0.05) & (means < 0.95 * ref)].value_counts()
    if len(plateau_vals) and plateau_vals.iloc[0] >= 0.25 * len(means):
        ok = False
        reasons.append(f"G5 FAIL: {plateau_vals.iloc[0]} cells stuck at recall {plateau_vals.index[0]} with sd=0 "
                       "-> sub-population ceiling (label/data artefact), inspect target class")
    if ok and not reasons: reasons.append("all gates passed")
    return {"GO": ok, "reasons": reasons}

def tax_cells(kstar_f0, k_values):
    """Cells (agg, k) at f=0 where a robust aggregator fails but k >= 1: k < k*(agg), or all k if 'never'."""
    out = []
    for agg, ks in kstar_f0.items():
        if agg == "fedavg": continue
        for k in k_values:
            if ks == "never" or (isinstance(ks, (int, np.integer)) and k < ks): out.append((agg, k))
    return out

def qa_classify(values, ref, frac=LEARNABLE_FRAC, majority=QA_MAJORITY):
    """Q-A verdict over tax cells.  values = per-cell mean detection rate (any-attack or binary)."""
    v = np.asarray(values, float)
    if not np.isfinite(ref) or ref <= 0: return "UNDEFINED", float("nan")
    if len(v) == 0: return "NO_TAX_CELLS", float("nan")
    share = float(np.mean(np.where(np.isnan(v), False, v >= frac * ref)))
    if share >= majority: return "DETECTED", share
    if share <= 1 - majority: return "MISSED", share
    return "MIXED", share

def delay_verdict(base, long, ref, frac=LEARNABLE_FRAC, gain=DELAY_GAIN):
    """EXP-D: is the tax a wall (permanent) or a delay (slower learning)?"""
    if not (np.isfinite(base) and np.isfinite(long) and np.isfinite(ref)): return "NA"
    if base >= frac * ref: return "ALREADY_LEARNED"
    if long >= frac * ref: return "DELAY"
    if long - base >= gain: return "PARTIAL"
    return "WALL"

def kstar_long(tested_k, long_vals, kstar_R, ref, frac=LEARNABLE_FRAC):
    """k* after LONG_MULT x rounds.  Tested cells are k < k*(R); k*(R) itself (learned at R)
    is added as learned.  'never' stays open-ended if nothing above is learned."""
    ks = list(tested_k); vs = list(long_vals)
    if isinstance(kstar_R, (int, np.integer)) and kstar_R not in ks: ks.append(int(kstar_R)); vs.append(ref)
    if not ks: return kstar_R
    return estimate_kstar(ks, vs, ref, frac)

def append_row(csv, row):
    """Append one result row safely.  If the row has columns the file lacks (e.g. a new metric added in
    a later script version), the whole file is rewritten with the union of columns (old rows -> NaN);
    otherwise the row is written in the file's own column order.  Never misaligns columns."""
    new = pd.DataFrame([row])
    if not os.path.exists(csv):
        new.to_csv(csv, index=False); return
    cols = list(pd.read_csv(csv, nrows=0).columns)
    if set(new.columns) - set(cols):
        old = pd.read_csv(csv)
        pd.concat([old, new], ignore_index=True).to_csv(csv, index=False)
    else:
        new.reindex(columns=cols).to_csv(csv, mode="a", header=False, index=False)

def floor_held(cells, ref, frac=LEARNABLE_FRAC):
    """P1 check.  cells: list of mean recalls at k <= f.  Held if none reaches half the learnable line."""
    v = np.asarray(cells, float)
    if not len(v) or not np.isfinite(ref): return None, float("nan")
    m = float(np.nanmax(v)) if np.isfinite(v).any() else float("nan")
    return bool(np.all(np.where(np.isnan(v), 0, v) < 0.5 * frac * ref)), m

def p3_monotone(kstars_by_eps):
    """kstars_by_eps: list of k* ordered from weakest to strongest privacy (inf, 10, 3, 1).
    'never' = infinity.  Returns True if k* never decreases as privacy strengthens."""
    num = [float("inf") if k == "never" else float(k) for k in kstars_by_eps if k is not None]
    return all(b >= a for a, b in zip(num, num[1:]))

def k0_verdict(v, ref, frac=LEARNABLE_FRAC):
    """Zero-witness control: is the target detected with NO witnesses at all?"""
    if not (np.isfinite(v) and np.isfinite(ref) and ref > 0): return "UNDEFINED"
    return "DETECTABLE_WITHOUT_WITNESSES" if v >= frac * ref else "NEEDS_WITNESSES"

# =============================================================================
#  MODEL + FEDERATED TRAINER (vmap over clients, Poisson subsampling)
# =============================================================================
class MLP(nn.Module):
    def __init__(self, d, c):
        super().__init__()
        self.net = nn.Sequential(nn.Linear(d, 128), nn.ReLU(), nn.Linear(128, 64), nn.ReLU(), nn.Linear(64, c))
    def forward(self, x): return self.net(x)

def flat(P): return torch.cat([p.reshape(p.shape[0], -1) for p in P.values()], 1)
def unflat(vec, like):
    out, o = {}, 0
    for k, v in like.items(): n = v.numel(); out[k] = vec[o:o + n].view_as(v); o += n
    return out

def dp_sigmas(eps, client_sizes, steps, batch=BATCH):
    if not np.isfinite(eps) or eps < 0: return np.zeros(len(client_sizes))
    from opacus.accountants.utils import get_noise_multiplier
    cache, out = {}, []
    for n in client_sizes:
        q = min(1.0, batch / n); key = round(q, 6)
        if key not in cache:
            cache[key] = get_noise_multiplier(target_epsilon=eps, target_delta=DP_DELTA,
                                              sample_rate=q, steps=steps, accountant="rdp")
        out.append(cache[key])
    return np.array(out)

def poisson_batch(lens, L, batch, bmax, gen_dev):
    N = lens.shape[0]
    q = torch.clamp(batch / lens.float(), max=1.0)
    m = torch.binomial(lens.float(), q)
    trunc = int((m > bmax).sum()); m = torch.clamp(m, max=bmax)
    keys = torch.rand(N, L, device=lens.device)
    keys[torch.arange(L, device=lens.device)[None, :] >= lens[:, None]] = 2.0
    pos = torch.topk(-keys, bmax, dim=1).indices
    mask = (torch.arange(bmax, device=lens.device)[None, :] < m[:, None]).float()
    return pos, mask, trunc

@torch.no_grad()
def evaluate(model, params, X_te, y_te, n_classes, n_out):
    """Row-normalised confusion: M[true class, predicted output].  Absent class -> NaN row."""
    p = torch.cat([functional_call(model, params, (X_te[i:i + 65536],)).argmax(1) for i in range(0, len(X_te), 65536)])
    M = torch.zeros(n_classes, n_out, device=X_te.device)
    M.index_put_((y_te, p), torch.ones_like(p, dtype=torch.float), accumulate=True)
    tot = M.sum(1, keepdim=True)
    return torch.where(tot > 0, M / tot.clamp(min=1), torch.full_like(M, float("nan"))).cpu().numpy()

def run_federated(X_tr, y_tr, X_te, y_te, clients, roles, agg, n_classes, seed,
                  eps=float("inf"), rounds=40, lr=0.1, clip=1.0, batch=BATCH, binary=False,
                  fhat=F_HAT, report=None, attack="mimic", waa_lam=1.0, elect_cls=None, loud=None,
                  probe=None, probe_mode=None, sra_lam=None):
    """binary=True trains attack-vs-Normal (2 outputs) on the same data; mimic overrides stay Normal."""
    torch.manual_seed(seed); np.random.seed(seed)
    gen = torch.Generator().manual_seed(seed)
    d = X_tr.shape[1]; N = len(clients); n_out = 2 if binary else n_classes
    model = MLP(d, n_out).to(DEV)
    g_params = {k: v.detach().clone() for k, v in model.named_parameters()}
    lens = torch.tensor([len(c[0]) for c in clients], device=DEV); L = int(lens.max())
    bmax = min(L, int(batch + 6 * math.sqrt(batch)) + 1)
    IDX = torch.zeros(N, L, dtype=torch.long, device=DEV); LAB = torch.zeros(N, L, dtype=torch.long, device=DEV)
    for i, (idx, ov) in enumerate(clients):
        it = torch.as_tensor(idx, device=DEV); lab = y_tr[it].clone(); ovt = torch.as_tensor(ov, device=DEV)
        lab = torch.where(ovt >= 0, ovt, lab)
        if binary: lab = (lab > 0).long()
        IDX[i, :len(idx)] = it; LAB[i, :len(idx)] = lab

    def loss_b(p, x, y, m):
        ce = F.cross_entropy(functional_call(model, p, (x,)), y, reduction="none")
        return (ce * m).sum() / batch
    def loss_1(p, x, y):
        return F.cross_entropy(functional_call(model, p, (x.unsqueeze(0),)), y.unsqueeze(0))
    g_batch = vmap(grad(loss_b))
    g_ps = vmap(vmap(grad(loss_1), in_dims=(None, 0, 0)), in_dims=(0, 0, 0))
    use_clip = np.isfinite(eps)
    sig = torch.as_tensor(dp_sigmas(eps, lens.cpu().numpy(), rounds * LOCAL_STEPS, batch),
                          device=DEV, dtype=torch.float32)
    hist, trunc_total, prev_a = [], 0, None
    att_mask = np.asarray(roles) == "A"
    if attack not in ATTACKS: raise ValueError(f"unknown attack {attack}")
    elect_idx = head_row_index(g_params, elect_cls) if elect_cls is not None else None
    WT = torch.ones(N, L, device=DEV)
    if loud is not None:   # client-side amplification: witnesses up-weight their rare samples
        wm = torch.as_tensor(np.asarray(roles) == "W", device=DEV)
        WT = torch.where(wm[:, None] & (LAB == int(loud[0])), torch.full_like(WT, float(loud[1])), WT)
    for r in range(1, rounds + 1):
        P = {k: v.unsqueeze(0).repeat(N, *[1] * v.dim()).clone() for k, v in g_params.items()}
        for _ in range(LOCAL_STEPS):
            pos, mask, tr_ = poisson_batch(lens, L, batch, bmax, DEV); trunc_total += tr_
            if loud is not None: mask = mask * torch.gather(WT, 1, pos)
            bi = torch.gather(IDX, 1, pos); yb = torch.gather(LAB, 1, pos); xb = X_tr[bi]
            if not use_clip:
                G = g_batch(P, xb, yb, mask)
            else:
                Gs = g_ps(P, xb, yb)
                norms = torch.sqrt(sum((g.reshape(N, bmax, -1) ** 2).sum(-1) for g in Gs.values()))
                fac = torch.clamp(clip / (norms + 1e-12), max=1.0) * mask
                G = {}
                for k_, g in Gs.items():
                    gs = (g * fac.view(N, bmax, *[1] * (g.dim() - 2))).sum(1)
                    noise = torch.randn_like(gs) * (sig.view(N, *[1] * (gs.dim() - 1)) * clip)
                    G[k_] = (gs + noise) / batch
            P = {k_: P[k_] - lr * G[k_] for k_ in P}
        U = flat({k_: P[k_] - g_params[k_].unsqueeze(0) for k_ in P})
        if attack in ("signflip", "signflip_nc"): U = signflip(U, att_mask)
        elif attack in ("alie", "alie_nc"): U = alie(U, att_mask)
        vdir = sdel = None
        if probe_mode is not None: vdir, sdel = probe_signals(model, g_params, X_tr, y_tr, probe, lr)
        a = aggregate_round(U, agg, fhat, gen, prev_a, report, waa_lam, elect_idx, vdir, sdel, probe_mode, sra_lam=sra_lam)
        if not torch.isfinite(a).all(): a = torch.zeros_like(a)
        prev_a = a.detach()
        upd = unflat(SERVER_LR * a, g_params)
        g_params = {k_: g_params[k_] + upd[k_] for k_ in g_params}
        if r % EVAL_EVERY == 0 or r == rounds:
            hist.append({"round": r, "M": evaluate(model, g_params, X_te, y_te, n_classes, n_out)})
    if trunc_total: print(f"      [note] Poisson batch truncated {trunc_total} times (accounting deviation negligible)")
    return hist

def summarise_hist(hist, at_round=None):
    """Mean confusion over the last 2 evaluations (up to at_round).  Returns dict with
    rec_c (multiclass: predicted == c; binary: c>0 predicted attack, c=0 predicted Normal),
    any_c (share predicted as any attack) and M (confusion)."""
    h = [x for x in hist if at_round is None or x["round"] <= at_round]
    last = h[-2:] if len(h) >= 2 else h
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", category=RuntimeWarning)
        M = np.nanmean(np.stack([x["M"] for x in last]), 0)
    C, n_out = M.shape; out = {"M": M}
    for c in range(C):
        anyc = float(1 - M[c, 0]) if np.isfinite(M[c, 0]) else float("nan")
        out[f"any_{c}"] = anyc
        if n_out == 2: out[f"rec_{c}"] = float(M[c, 0]) if c == 0 else anyc
        else: out[f"rec_{c}"] = float(M[c, c])
    return out

def curve(hist, c, kind="rec"):
    return [summarise_hist([x])[f"{kind}_{c}"] for x in hist]

# =============================================================================
#  PHASE 0 -- SELF-TESTS ON MESSY SYNTHETIC DATA
# =============================================================================
def _synthetic_csvs(tmp, names, rows, with_ips, bad_value_file=None, seed=0):
    """Messy CICFlowMeter-like CSVs: attempted labels, probes, unicode dashes, inf strings,
    exact duplicates and planted label conflicts.  Returns planted-truth dict."""
    r = np.random.default_rng(seed)
    labs = ["BENIGN"] * 60 + ["DoS Hulk"] * 10 + ["DoS Hulk - Attempted"] * 3 + ["Botnet Ares"] * 8 + \
           ["Botnet Ares - Attempted"] * 2 + ["SSH-BruteForce"] * 6 + ["Infiltration - NMAP Portscan"] * 3 + \
           ["Web Attack \u2013 XSS"] * 2 + ["weird-label"] * 1
    cen = {"Normal": 0, "DoS": 4, "Botnet": -4, "Brute Force": 8, "Web Attack": -8}
    truth = {"conflicts": 0, "dups": 0, "per_class": {}}
    for fi, name in enumerate(names):
        lab = r.choice(labs, rows)
        mac = [map_label(x) for x in lab]
        mu = np.array([cen.get(m, 12) for m in mac], float)
        feats = {f"Feat {j}": np.round(mu + r.normal(0, 1, rows), 3) for j in range(6)}
        df = pd.DataFrame({"id": np.arange(rows), "Flow ID": "x", "Src Port": r.integers(1, 65000, rows),
                           "Dst Port": r.integers(1, 1000, rows), "Protocol": 6, "Timestamp": "2018-02-14 10:00:00",
                           **feats, "Flow Bytes/s": np.round(r.exponential(100, rows), 2),
                           "Label": lab, "Attempted Category": -1})
        if with_ips:
            df.insert(2, "Src IP", np.where(r.random(rows) < .5, "18.219.193.20", [f"172.31.{64+fi}.{i%200}" for i in range(rows)]))
            df.insert(4, "Dst IP", np.where(df["Src IP"].str.startswith("172.31."), "8.8.8.8", f"172.31.{65+fi}.5"))
        df["Flow Bytes/s"] = df["Flow Bytes/s"].astype(object); df.loc[:3, "Flow Bytes/s"] = "Infinity"
        dup = df[df.Label == "BENIGN"].iloc[:5].copy(); dup["id"] += 10 ** 6
        con = df[df.Label == "BENIGN"].iloc[5:7].copy(); con["Label"] = "DoS Hulk"; con["id"] += 2 * 10 ** 6
        df = pd.concat([df, dup, con], ignore_index=True)
        if bad_value_file is not None and fi == bad_value_file:
            df["Feat 0"] = df["Feat 0"].astype(object); df.loc[len(df) - 1, "Feat 0"] = "abc"
        truth["dups"] += 5; truth["conflicts"] += 4
        df.to_csv(os.path.join(tmp, name), index=False)
    return truth

def phase0_self_tests():
    global CLASSES
    banner("PHASE 0 -- SELF-TESTS ON MESSY SYNTHETIC DATA (must all pass)")
    fails = []
    def check(name, cond, detail=""):
        print(f"    [{'PASS' if cond else 'FAIL'}] {name} {detail}")
        if not cond: fails.append(name)
    CLASSES = CIC_CLASSES

    sub("T1 label mapping (CICIDS2017 + CSE-CIC-IDS2018 corrected releases)")
    cases = {"BENIGN": "Normal", " Web Attack \ufffd Brute Force": "Web Attack", "Web Attack – XSS": "Web Attack",
             "FTP-Patator - Attempted": "DROP", "DDoS": "DDoS", "DoS Hulk": "DoS", "PortScan": "Portscan",
             "Botnet": "Botnet", "Infiltration - Portscan": "PROBE_Infiltration", "Heartbleed": "PROBE_Heartbleed",
             "weird": "UNKNOWN", "DDoS-HOIC": "DDoS", "DDoS-LOIC-UDP - Attempted": "DROP", "DoS GoldenEye": "DoS",
             "FTP-BruteForce - Attempted": "DROP", "SSH-BruteForce": "Brute Force", "Botnet Ares": "Botnet",
             "Infiltration - NMAP Portscan": "PROBE_Infiltration", "Infilteration": "PROBE_Infiltration",
             "Infiltration - Dropbox Download - Attempted": "PROBE_Infiltration", "Web Attack - SQL": "Web Attack",
             "Web Attack - Brute Force - Attempted": "DROP", "DoS Slowloris": "DoS"}
    for raw, exp in cases.items():
        got = map_label(raw); check(f"'{raw}' -> {exp}", got == exp, f"(got {got})")

    sub("T2 witness partitioner (edge cases + tempered-mix override)")
    rng = np.random.default_rng(0)
    y = np.concatenate([np.zeros(5000), np.ones(400), np.full(37, 2), np.full(900, 3)]).astype(int); rng.shuffle(y)
    for k, f in [(1, 0), (3, 2), (7, 4), (16, 4), (1, 4)]:
        cl, roles, m = build_witness_partition(y, 2, k, f, 20, 1000, 300, 0.5, rng)
        hon_t = sum(np.sum((y[c[0]] == 2) & (c[1] < 0)) for c, r in zip(cl, roles) if r != "A")
        n_w = sum(1 for c, r in zip(cl, roles) if r != "A" and np.any(y[c[0]] == 2))
        att_ok = all(np.all(c[1][y[c[0]] == 2] == 0) for c, r in zip(cl, roles) if r == "A")
        check(f"k={k} f={f}", n_w == k and hon_t == m == 37 and att_ok and (roles == "A").sum() == f)
    for args, name in [((y, 2, 18, 4), "k+f>N raises"), ((np.r_[np.zeros(500), np.full(3, 2)].astype(int), 2, 5, 0), "too-few raises")]:
        try: build_witness_partition(*args, 20, 1000, 50, 0.5, rng); check(name, False)
        except ValueError: check(name, True)
    cl0, ro0, m0 = build_witness_partition(y, 2, 0, 0, 20, 1000, 300, 0.5, rng)
    check("k=0 f=0: no target rows anywhere, all honest, m_eff=0",
          m0 == 0 and all(np.sum(y[c[0]] == 2) == 0 for c in cl0) and set(ro0) == {"H"})
    for args, name in [((y, 2, 0, 2), "k=0 f>0 raises"), ((y, 2, -1, 0), "k<0 raises")]:
        try: build_witness_partition(*args, 20, 1000, 50, 0.5, rng); check(name, False)
        except ValueError: check(name, True)
    # capped pool (class 0 has 5000 rows) but true count 500,000 -> mix must follow the override
    cl, _, _ = build_witness_partition(y, 2, 1, 0, 20, 30, 4000, 0.5, np.random.default_rng(1),
                                       bg_counts={0: 500000, 1: 400, 3: 900})
    share0 = np.mean(np.concatenate([y[c[0]] for c in cl]) == 0)
    exp0 = 500000 ** .5 / (500000 ** .5 + 400 ** .5 + 900 ** .5)
    check("bg_counts override sets tempered mix", abs(share0 - exp0) < 0.02, f"({share0:.3f} vs {exp0:.3f})")

    sub("T3 aggregators")
    g = torch.Generator().manual_seed(0); base = torch.randn(20, 50, generator=g) * 0.1
    Ub = base.clone(); Ub[:2] = 1e3
    for name in ALL_AGGS:
        mx = float(AGG_FN[name](Ub, gen=torch.Generator().manual_seed(1)).abs().max())
        check(f"{name:13s} outlier behaviour", (mx < 1.0) if name != "fedavg" else (mx > 1.0), f"(max={mx:.2f})")
    for k in [3, 11]:
        Uw = base.clone(); Uw[:k, 0] += 5.0
        check(f"cwmed passes witness iff k>N/2 (k={k})", (float(agg_cwmed(Uw)[0]) > 1.0) == (k > 10))
        check(f"trmean(b=2) passes witness when k>b (k={k})", float(agg_trmean(Uw, b=2)[0]) > 0.3)
    Uw = base.clone(); Uw[:3, 0] += 5.0
    c_med = float(agg_cwmed(Uw)[0]); c_nnm = float(agg_nnm_cwmed(Uw)[0]); c_cc = float(agg_cclip(Uw)[0])
    check("nnm_cwmed passes more witness signal than cwmed (k=3)", c_nnm > c_med + 0.05, f"({c_nnm:.3f} vs {c_med:.3f})")
    check("cclip passes bounded witness signal (0.05 < x < fedavg)", 0.05 < c_cc < float(agg_fedavg(Uw)[0]), f"({c_cc:.3f})")
    Uo = base.clone(); Uo[:2] = 1e3
    prev = torch.full((50,), 0.5)
    check("cclip with non-zero centre ignores outliers", float((agg_cclip(Uo, prev=prev) - 0.5).abs().max()) < 1.0)
    Unan = base.clone(); Unan[0, 3] = float("nan")
    check("nnm_cwmed / cclip do not crash on a NaN row", agg_nnm_cwmed(Unan).shape == (50,) and agg_cclip(Unan).shape == (50,))

    sub("T4 boundary estimator")
    ks = [1, 2, 3, 5, 8, 12]
    check("clean step", estimate_kstar(ks, [0, 0, .1, .9, .9, .95], 1.0) == 5)
    check("blip ignored", estimate_kstar(ks, [0, .9, .1, .9, .9, .95], 1.0) == 5)
    check("NaN = fail", estimate_kstar(ks, [0, 0, .9, np.nan, .9, .9], 1.0) == 8)
    check("all fail -> never", estimate_kstar(ks, [0] * 6, 1.0) == "never")
    check("unsorted", estimate_kstar(ks[::-1], [.95, .9, .9, .1, 0, 0], 1.0) == 5)
    r2 = np.random.default_rng(3); hits = 0
    for _ in range(200):
        t = r2.choice(ks); hits += estimate_kstar(ks, np.where(np.array(ks) >= t, .95, .2) + r2.normal(0, .05, 6), 1.0) == t
    check("noisy recovery >= 0.9", hits / 200 >= 0.9, f"({hits}/200)")

    sub("T5 G1 convergence rule (v3) -- includes the real curve that fooled v2")
    R = np.arange(5, 151, 5)
    real_k1 = np.interp(R, np.arange(5, 150, 10), [0, 0, 0, 0, 0, 0, .14, .51, .72, .77, .74, .81, .80, .82, .83])
    c1 = curve_converged(R, real_k1, 150)
    check("pilot k=1 curve (still creeping) -> NOT converged", c1["ok"] is False, f"({c1['why']})")
    real_k16 = np.interp(R, np.arange(5, 150, 10), [0, 0, .85, .93, .95, .98, .98, .98, .98, .99, .98, .99, .99, 1, 1])
    c16 = curve_converged(R, real_k16, 150)
    check("pilot k=16 curve -> converged", c16["ok"] is True, f"({c16['why']})")
    check("late jump at 100 -> NOT converged", curve_converged(R, np.where(R < 100, 0.0, 0.9), 150)["ok"] is False)
    check("flat zero -> None (never learned)", curve_converged(R, np.zeros(len(R)), 150)["ok"] is None)
    rr = np.random.default_rng(5); n_ok = n_creep = 0
    for _ in range(200):
        n_ok += curve_converged(R, 0.9 * (1 - np.exp(-R / 15)) + rr.normal(0, .02, len(R)), 150)["ok"] is True
        n_creep += curve_converged(R, np.clip((R - 30) / 120, 0, 1) * 0.3 + 0.5 * (R >= 30) + rr.normal(0, .02, len(R)), 150)["ok"] is False
    check("noisy fast-saturating -> converged in >= 90%", n_ok >= 180, f"({n_ok}/200)")
    check("noisy linear creep -> NOT converged in >= 95%", n_creep >= 190, f"({n_creep}/200)")
    nanc = real_k16.copy(); nanc[[3, 10]] = np.nan
    check("NaN in curve -> no crash", curve_converged(R, nanc, 150)["ok"] in (True, False))
    check("too-short curve -> no crash", curve_converged(R[:3], [0.5, 0.6, 0.6], 150)["ok"] in (True, False, None))

    sub("T6 cleaning + target selection (share from full / estimated counts)")
    Fdf = pd.DataFrame({"a": [1, 1, 2, 2, 3, 3, 4], "b": [0, 0, 0, 0, 1, 1, 5]})
    lab = np.array(["x", "y", "x", "x", "z", "z", "x"])
    keep, rep = remove_conflicts_and_dups(Fdf, lab)
    check("conflict rows dropped (2), dup dropped (2), 3 kept", rep["conflicting_rows"] == 2 and
          rep["exact_duplicates"] == 2 and keep.sum() == 3, f"({rep})")
    cls = ["Normal", "A", "B", "C"]
    ytr_ = np.r_[np.zeros(100), np.ones(450), np.full(40, 2), np.full(700, 3)].astype(int)
    yte_ = np.r_[np.ones(120), np.full(10, 2), np.full(200, 3)].astype(int)
    el, rp = select_targets({"Normal": 9000, "A": 500, "B": 60, "C": 900}, ytr_, yte_, cls, 400, 100, 0.07)
    check("selector picks A (rarest eligible), rejects B (few), C (share)", el == ["A"], f"({el})")
    el2, _ = select_targets({"Normal": 90_000_000, "A": 500, "B": 60, "C": 900_000}, ytr_, yte_, cls, 400, 100, 0.07)
    check("huge estimated Normal makes C rare", el2 == ["A", "C"], f"({el2})")
    tr_, te_ = stratified_split(np.r_[np.zeros(100000), np.ones(50)].astype(int), ["Normal", "A"], np.random.default_rng(0))
    check("split: disjoint, caps, 30% test", len(set(tr_) & set(te_)) == 0 and np.sum(te_ < 100000) == 30000
          and np.sum(te_ >= 100000) == 15)

    sub("T7 Poisson subsampling")
    lens = torch.tensor([300, 3000, 5000], device=DEV); L = 5000
    tot, cnt = torch.zeros(3, device=DEV), 0
    for _ in range(300):
        pos, mask, _ = poisson_batch(lens, L, 128, 200, DEV)
        valid = (pos < lens[:, None]) | (mask == 0)
        cnt += int((~valid).sum()); tot += mask.sum(1)
    mb = (tot / 300).cpu().numpy()
    check("mean batch ~ 128 (within 5%)", np.all(np.abs(mb - 128) < 6.4), f"({np.round(mb,1)})")
    check("never samples padding", cnt == 0)

    sub("T8 DP calibration")
    if not HAVE_OPACUS:
        if RUN_EXP_B: check("opacus available -- Internet ON or RUN_EXP_B=False", False)
        else: print("    [SKIP] opacus missing, RUN_EXP_B=False")
    else:
        s = [dp_sigmas(e, [3000], 400)[0] for e in [1.0, 3.0, 10.0]]
        check("sigma decreasing in eps", s[0] > s[1] > s[2], f"({np.round(s,3)})")
        check("inf and clip-only -> sigma 0", dp_sigmas(float("inf"), [3000], 400)[0] == 0 and dp_sigmas(-1.0, [3000], 400)[0] == 0)
        from opacus.accountants import RDPAccountant
        acc = RDPAccountant()
        for _ in range(400): acc.step(noise_multiplier=s[0], sample_rate=BATCH / 3000)
        e = acc.get_epsilon(DP_DELTA); check("accountant round-trip eps~1", abs(e - 1) < 0.05, f"({e:.3f})")

    sub("T9 end-to-end on synthetic data (multiclass + binary)")
    r3 = np.random.default_rng(1); d, C = 12, 4; mus = r3.normal(0, 3, (C, d))
    ytr = r3.choice(C, 20000, p=[.6, .2, .15, .05]); Xtr = mus[ytr] + r3.normal(0, 1, (20000, d))
    yte = r3.choice(C, 4000, p=[.4, .2, .2, .2]); Xte = mus[yte] + r3.normal(0, 1, (4000, d))
    T = lambda a, dt=torch.float32: torch.tensor(a, dtype=dt, device=DEV)
    Xt, yt, Xe, ye = T(Xtr), T(ytr, torch.long), T(Xte), T(yte, torch.long)
    res = {}
    for agg, k, f, b in [("fedavg", 1, 0, False), ("cwmed", 1, 0, False), ("cwmed", 15, 0, False),
                         ("fedavg", 1, 3, False), ("fedavg", 15, 0, True), ("fedavg", 1, 3, True)]:
        cl, ro, _ = build_witness_partition(ytr, 3, k, f, 20, 400, 300, 0.5, np.random.default_rng(0))
        s = summarise_hist(run_federated(Xt, yt, Xe, ye, cl, ro, agg, C, 0, rounds=25, binary=b))
        res[(agg, k, f, b)] = s
        print(f"      {agg:7s} k={k:2d} f={f} {'binary' if b else 'multi '}: target recall = {s['rec_3']:.3f}  "
              f"any-attack = {s['any_3']:.3f}  FPR = {1-s['rec_0']:.3f}")
    for agg in ("cclip", "nnm_cwmed"):
        cl, ro, _ = build_witness_partition(ytr, 3, 15, 0, 20, 400, 300, 0.5, np.random.default_rng(0))
        s = summarise_hist(run_federated(Xt, yt, Xe, ye, cl, ro, agg, C, 0, rounds=25))
        check(f"{agg} k=15 learns (stateful path finite)", s["rec_3"] > 0.6, f"({s['rec_3']:.3f})")
    cl, ro, _ = build_witness_partition(ytr, 3, 0, 0, 20, 400, 300, 0.5, np.random.default_rng(0))
    s0 = summarise_hist(run_federated(Xt, yt, Xe, ye, cl, ro, "fedavg", C, 0, rounds=25))
    check("k=0 multiclass: target never predicted as itself", s0["rec_3"] < 0.05, f"({s0['rec_3']:.3f})")
    check("fedavg k=1 learns", res[("fedavg", 1, 0, False)]["rec_3"] > 0.6)
    check("cwmed k=1 suppresses", res[("cwmed", 1, 0, False)]["rec_3"] < 0.3)
    check("cwmed k=15 learns", res[("cwmed", 15, 0, False)]["rec_3"] > 0.6)
    check("fedavg k=1 f=3 mimic suppresses", res[("fedavg", 1, 3, False)]["rec_3"] < 0.3)
    check("binary k=15 detects, FPR < 0.1", res[("fedavg", 15, 0, True)]["rec_3"] > 0.6 and 1 - res[("fedavg", 15, 0, True)]["rec_0"] < 0.1)
    check("binary mimic k=1 f=3 suppresses", res[("fedavg", 1, 3, True)]["rec_3"] < 0.3)
    Mm = res[("fedavg", 1, 0, False)]["M"]
    check("confusion rows sum to 1", np.allclose(np.nansum(Mm, 1), 1, atol=1e-4))
    check("rec <= any-attack for attack classes", all(res[("fedavg", 1, 0, False)][f"rec_{c}"] <= res[("fedavg", 1, 0, False)][f"any_{c}"] + 1e-6 for c in range(1, C)))
    ye_missing = ye.clone(); ye_missing[ye_missing == 2] = 1
    Mx = evaluate(MLP(d, C).to(DEV), {k: v for k, v in MLP(d, C).to(DEV).named_parameters()}, Xe, ye_missing, C, C)
    check("absent test class -> NaN row, no crash", np.all(np.isnan(Mx[2])))
    h = run_federated(Xt, yt, Xe, ye, *build_witness_partition(ytr, 3, 15, 0, 20, 400, 300, 0.5, np.random.default_rng(0))[:2], "fedavg", C, 0, rounds=20)
    check("at_round summary uses only rounds <= at_round", summarise_hist(h, at_round=10)["M"].shape == (C, C)
          and np.allclose(summarise_hist(h, at_round=10)["M"], np.nanmean(np.stack([h[0]["M"], h[1]["M"]]), 0), equal_nan=True))
    if HAVE_OPACUS:
        cl, ro, _ = build_witness_partition(ytr, 3, 3, 0, 20, 400, 300, 0.5, np.random.default_rng(0))
        for e in (3.0, -1.0):
            hh = run_federated(Xt, yt, Xe, ye, cl, ro, "fedavg", C, 0, eps=e, rounds=10)
            check(f"DP path {eps_name(e)} finite", np.isfinite(summarise_hist(hh)["rec_3"]))

    sub("T10 gates: pre-flight (G1 + G6) and post-EXP-A (G2-G5)")
    good = {"k=max target": {"ok": True, "why": "ok"}, "macro": {"ok": True, "why": "ok"}, "k=1 target": {"ok": True, "why": "ok"}}
    refr = {"Normal": 0.99, "DoS": 0.9, "Botnet": 0.95, "Web Attack": 0.7}
    cl4 = ["Normal", "DoS", "Botnet", "Web Attack", "Portscan"]
    def pf(conv=good, rr=refr, tgt="Botnet"): return preflight_gate(conv, rr, tgt, cl4)["GO"]
    check("clean -> GO (absent class Portscan skipped)", pf())
    check("k=1 never learned -> still GO", pf({**good, "k=1 target": {"ok": None, "why": "never"}}))
    check("k=max not converged -> NO-GO", not pf({**good, "k=max target": {"ok": False, "why": "late"}}))
    check("k=1 creeping below line -> NO-GO", not pf({**good, "k=1 target": {"ok": False, "why": "rising", "above_line": False}}))
    check("k=1 creeping, above line -> GO", pf({**good, "k=1 target": {"ok": False, "why": "rising", "above_line": True}}))
    check("k=1 creeping, flag missing -> NO-GO", not pf({**good, "k=1 target": {"ok": False, "why": "rising"}}))
    check("above_line never rescues k=max", not pf({**good, "k=max target": {"ok": False, "why": "late", "above_line": True}}))
    check("macro never learned -> NO-GO", not pf({**good, "macro": {"ok": None, "why": "never"}}))
    check("FPR exactly 0.05 -> GO", pf(rr={**refr, "Normal": 0.95}))
    check("FPR 0.0501 -> NO-GO", not pf(rr={**refr, "Normal": 0.9499}))
    check("dead non-target class -> NO-GO", not pf(rr={**refr, "Web Attack": 0.0}))
    check("NaN recall on a present class -> NO-GO", not pf(rr={**refr, "DoS": float("nan")}))
    check("dead TARGET is G6c not G6b", not pf(rr={**refr, "Botnet": 0.3}))
    check("missing Normal key -> NO-GO", not pf(rr={k: v for k, v in refr.items() if k != "Normal"}))
    def fake(kst, sd, never, plateau=False):
        rows = []
        for a in ["fedavg", "cwmed"]:
            for f in [0, 2]:
                for k in [1, 3, 12]:
                    for s_, sg in enumerate([-1, 0, 1]):
                        r = (.9 if k >= (1 if a == "fedavg" else kst) else .05)
                        if plateau: r = .46
                        rows.append(dict(agg=a, f=f, k=k, seed=s_, target_recall=r + sg * (0 if plateau else sd)))
        ks_ = {(a, f): ("never" if (a == "cwmed" and never) else (1 if a == "fedavg" else kst)) for a in ["fedavg", "cwmed"] for f in [0, 2]}
        return pd.DataFrame(rows), ks_
    for (kst, sd, nev, pl), exp_go, name in [((12, .02, False, False), True, "clean -> GO"),
                                             ((1, .02, False, False), False, "no over-robustness -> NO-GO"),
                                             ((12, .02, True, False), False, "boundary outside grid -> NO-GO"),
                                             ((12, .02, False, True), False, "sd=0 plateau artefact -> NO-GO")]:
        dd, kk = fake(kst, sd, nev, pl); g_ = gate_decision(dd, kk, .9)
        check(name, g_["GO"] == exp_go, str(g_["reasons"]))
    dd, kk = fake(12, .3, False); g_ = gate_decision(dd, kk, .9)
    check("seed-unstable -> GO + flag", g_["GO"] and any("G4" in r for r in g_["reasons"]))

    sub("T11 Q-A verdict (missed vs detected-as-attack) over tax cells")
    kf0 = {"fedavg": 1, "cwmed": 8, "trmean": 3, "mkrum": "never"}
    tc = tax_cells(kf0, [1, 2, 3, 5, 8])
    check("tax cells: cwmed k<8, trmean k<3, mkrum all, no fedavg",
          set(tc) == {("cwmed", 1), ("cwmed", 2), ("cwmed", 3), ("cwmed", 5), ("trmean", 1), ("trmean", 2),
                      ("mkrum", 1), ("mkrum", 2), ("mkrum", 3), ("mkrum", 5), ("mkrum", 8)})
    check("no tax -> NO_TAX_CELLS", qa_classify([], 0.9)[0] == "NO_TAX_CELLS")
    check("all detected -> DETECTED", qa_classify([.9, .85, .95, .8], 0.95)[0] == "DETECTED")
    check("none detected -> MISSED", qa_classify([.0, .1, .02, np.nan], 0.95)[0] == "MISSED")
    check("half -> MIXED", qa_classify([.9, .9, .0, .0], 0.95)[0] == "MIXED")
    check("NaN counts as not detected", qa_classify([np.nan] * 4, 0.95)[0] == "MISSED")
    check("NaN / zero ref -> UNDEFINED", qa_classify([.9], np.nan)[0] == "UNDEFINED" and qa_classify([.9], 0.0)[0] == "UNDEFINED")
    check("boundary: exactly frac*ref counts as detected", qa_classify([0.8] * 4, 1.0)[0] == "DETECTED")

    sub("T12 EXP-D verdict (wall vs delay), k*(3R), zero-witness verdict")
    check("learns with more rounds -> DELAY", delay_verdict(0.0, 0.9, 1.0) == "DELAY")
    check("gains 0.3 but below line -> PARTIAL", delay_verdict(0.1, 0.4, 1.0) == "PARTIAL")
    check("stays at 0 -> WALL", delay_verdict(0.0, 0.05, 1.0) == "WALL")
    check("already learned at base -> ALREADY_LEARNED", delay_verdict(0.85, 0.9, 1.0) == "ALREADY_LEARNED")
    check("NaN -> NA", delay_verdict(np.nan, 0.9, 1.0) == "NA" and delay_verdict(0.1, np.nan, 1.0) == "NA")
    check("decline (forgetting) -> WALL", delay_verdict(0.5, 0.2, 1.0) == "WALL")
    check("k*(3R): cells 1-6 tested, learned from 4 -> 4", kstar_long([1, 2, 3, 4, 5, 6], [0, 0, .1, .9, .9, .9], 7, 1.0) == 4)
    check("k*(3R): nothing learned below -> k*(R)", kstar_long([1, 2], [0, .1], 3, 1.0) == 3)
    check("k*(3R): blip below a gap ignored", kstar_long([1, 2, 3], [.9, 0, .9], 4, 1.0) == 3)
    check("k*(3R): never stays never if long cells fail", kstar_long([1, 2], [0, 0], "never", 1.0) == "never")
    check("k*(3R): never becomes number if long cells learn", kstar_long([1, 2, 3], [0, .9, .9], "never", 1.0) == 2)
    check("k*(3R): NaN cell = not learned", kstar_long([1, 2, 3], [.9, np.nan, .9], 4, 1.0) == 3)
    check("k0 verdict: detected -> DETECTABLE_WITHOUT_WITNESSES", k0_verdict(0.95, 1.0) == "DETECTABLE_WITHOUT_WITNESSES")
    check("k0 verdict: 0 -> NEEDS_WITNESSES", k0_verdict(0.0, 1.0) == "NEEDS_WITNESSES")
    check("k0 verdict: NaN -> UNDEFINED", k0_verdict(np.nan, 1.0) == "UNDEFINED" and k0_verdict(.5, 0) == "UNDEFINED")

    sub("T15 safe CSV append (new columns in a later script version) + claim checks")
    tmpc = tempfile.mkdtemp(prefix="witness_t15_"); fcsv = os.path.join(tmpc, "r.csv")
    append_row(fcsv, {"a": 1, "b": 2}); append_row(fcsv, {"b": 3, "a": 4})
    r1 = pd.read_csv(fcsv)
    check("same columns, different order -> aligned", list(r1.a) == [1, 4] and list(r1.b) == [2, 3])
    append_row(fcsv, {"a": 5, "b": 6, "c": "x y"})
    r2 = pd.read_csv(fcsv)
    check("new column -> file rewritten, old rows NaN, no misalignment",
          list(r2.columns) == ["a", "b", "c"] and list(r2.a) == [1, 4, 5] and r2.c.isna().sum() == 2 and r2.c.iloc[2] == "x y")
    append_row(fcsv, {"a": 7, "b": 8})
    r3 = pd.read_csv(fcsv)
    check("row missing a column -> NaN there, others aligned", list(r3.a) == [1, 4, 5, 7] and pd.isna(r3.c.iloc[3]))
    shutil.rmtree(tmpc, ignore_errors=True)
    check("floor held: all cells ~0", floor_held([0.0, 0.02, 0.09], 0.94)[0] is True)
    check("floor broken: one cell at 0.5", floor_held([0.0, 0.5], 0.94)[0] is False)
    check("floor: NaN cell ignored, no crash", floor_held([np.nan, 0.01], 0.94)[0] is True)
    check("floor: no cells -> None", floor_held([], 0.94)[0] is None)
    check("P3 monotone: 1,3,8,never", p3_monotone([1, 3, 8, "never"]) is True)
    check("P3 violated: 16,3,3,8 (noise helps median)", p3_monotone([16, 3, 3, 8]) is False)
    check("P3: missing settings skipped", p3_monotone([3, 8]) is True)

    sub("T13 day-lock partition (natural witness structure)")
    yd = np.r_[np.zeros(3000), np.ones(400), np.full(3, 2), np.full(300, 3)].astype(int)
    dd_ = np.r_[np.repeat(["d1", "d2", "d3", "d4", "d5"], 600), np.repeat("d2", 400), np.repeat("d3", 3), np.repeat("d4", 300)]
    for nd, spd in [(5, 4)]:
        cl, wk, comp = build_daylock_clients(yd, dd_, 20, 4, np.random.default_rng(0))
        check("20 clients, 4 per day", len(cl) == 20)
        check("class 1 witnesses = 4 (one day)", wk[1] == 4, f"({wk})")
        check("class with 3 rows < 4 sub-clients -> 0 witnesses", wk[2] == 0)
        check("no index reused across clients", len(np.concatenate([c[0] for c in cl])) == len(np.unique(np.concatenate([c[0] for c in cl]))))
    cl10, wk10, _ = build_daylock_clients(yd, np.where(np.arange(len(yd)) % 2 == 0, dd_, np.char.add(dd_.astype(str), "b")), 20, 4, np.random.default_rng(0))
    check("10 days -> 2 sub-clients per day", len(cl10) == 20 and wk10[1] == 4, f"({wk10})")

    sub("T14 loader on messy synthetic CSVs (attempted, probes, inf strings, dups, conflicts)")
    tmp = tempfile.mkdtemp(prefix="witness_t14_")
    try:
        truth = _synthetic_csvs(tmp, ["Wednesday-14-02-2018.csv", "Thursday-15-02-2018.csv", "Friday-02-03-2018.csv"], 2000, with_ips=True, bad_value_file=1, seed=3)
        full = pd.concat([read_csv_any(f) for f in sorted(glob.glob(os.path.join(tmp, "*.csv")))])
        n_norm_true = int((full.Label == "BENIGN").sum())
        D = load_data(tmp, rate=0.5, use_cache=False, write_cache=False)
        check("classes restricted to macro set", set(np.unique(np.r_[D["ytr"], D["yte"]])) <= set(range(len(CIC_CLASSES))))
        check("no ID / port / Attempted-Category features", not any(("port" in f.lower()) or f.lower() in CIC_ID_COLS for f in D["feats"]), f"({D['feats']})")
        check("inf strings + bad value handled, features finite", np.isfinite(D["Xtr"]).all() and np.isfinite(D["Xte"]).all())
        n_att_valid = int(full.Label.map(map_label).isin(CIC_CLASSES[1:]).sum())
        n_att_kept = sum(v for c, v in D["class_counts"].items() if c != "Normal")
        check("all valid attack rows kept except planted conflicts/dups", n_att_valid - truth["conflicts"] <= n_att_kept <= n_att_valid,
              f"({n_att_kept} of {n_att_valid})")
        est = D["class_counts"]["Normal"]
        check("estimated full Normal within 10% of truth", abs(est - n_norm_true) / n_norm_true < 0.10, f"({est} vs {n_norm_true})")
        check("3 days in day labels", len(np.unique(D["days_tr"])) == 3)
        check("subnets extracted (internal /24s present)", any(str(s).startswith("172.31.") for s in D["subnet_names"]))
        cols = None
        head = read_csv_any(sorted(glob.glob(os.path.join(tmp, "*.csv")))[0], nrows=10)
        fc = [c for c in head.columns if c.lower() not in CIC_ID_COLS and pd.api.types.is_numeric_dtype(head[c]) and "port" not in c.lower()]
        cols = (fc, "Label", "Src IP", "Dst IP")
        fp0 = sorted(glob.glob(os.path.join(tmp, "*.csv")))[0]
        a1 = _read_file(fp0, cols, 0.5, 123)
        import builtins
        real_import = builtins.__import__
        def no_arrow(name, *a, **k):
            if name.startswith("pyarrow"): raise ImportError("forced")
            return real_import(name, *a, **k)
        builtins.__import__ = no_arrow
        try: a2 = _read_file(fp0, cols, 0.5, 123)
        finally: builtins.__import__ = real_import
        check("pyarrow and pandas readers keep the identical sample", a1["reader"] == "pyarrow" and a2["reader"] == "pandas"
              and np.array_equal(np.concatenate(a1["y"]), np.concatenate(a2["y"]))
              and np.allclose(np.concatenate(a1["X"]), np.concatenate(a2["X"]), equal_nan=True))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
        CLASSES = CIC_CLASSES

    print(f"\n  PHASE 0 RESULT: {'ALL PASSED' if not fails else f'{len(fails)} FAILED -> {fails}'}")
    return not fails

# =============================================================================
#  CALIBRATION  (+ pre-flight gate inputs)
# =============================================================================
def calibrate(Xt, yt, Xe, ye, D, target):
    path = os.path.join(OUT_DIR, f"calibration_{fname(target)}_M{M_TARGET}.json")
    if os.path.exists(path):
        cal = json.load(open(path)); print(f"  loaded existing calibration: {path}"); return cal
    banner(f"CALIBRATION -- target {target} (FedAvg, f=0, non-private reference)")
    ytr_np = D["ytr"]; ti = CLASSES.index(target); C = len(CLASSES); kmax = max(K_GRID)
    macro_of = lambda s: float(np.nanmean([s[f"rec_{c}"] for c in range(C)]))
    part = lambda k: build_witness_partition(ytr_np, ti, k, 0, N_CLIENTS, M_TARGET, N_BG, BG_TEMPER,
                                             np.random.default_rng(99), bg_counts=D["bg_counts"])[:2]
    cl, ro = part(kmax); cl1, ro1 = part(1)
    R0 = R_CAL_LIST[0]; curves = {}
    sub(f"CAL-1 learning rate (k={kmax}, {R0} rounds, selection metric = macro recall over ALL classes)")
    for lr in LR_GRID:
        h = run_federated(Xt, yt, Xe, ye, cl, ro, "fedavg", C, 99, rounds=R0, lr=lr)
        curves[lr] = h; s = summarise_hist(h)
        print(f"    lr={lr:<5} macro recall={macro_of(s):.3f}  target recall={s[f'rec_{ti}']:.3f}")
    lr_best = max(LR_GRID, key=lambda l: macro_of(summarise_hist(curves[l])))
    for R in R_CAL_LIST:
        h = curves[lr_best] if R == R0 else run_federated(Xt, yt, Xe, ye, cl, ro, "fedavg", C, 99, rounds=R, lr=lr_best)
        h1 = run_federated(Xt, yt, Xe, ye, cl1, ro1, "fedavg", C, 99, rounds=R, lr=lr_best)
        rr = [x["round"] for x in h]
        cv = {"k=max target": curve_converged(rr, curve(h, ti), R),
              "macro": curve_converged(rr, [np.nanmean([summarise_hist([x])[f"rec_{c}"] for c in range(C)]) for x in h], R),
              "k=1 target": curve_converged(rr, curve(h1, ti), R)}
        line = LEARNABLE_FRAC * summarise_hist(h)[f"rec_{ti}"]
        cv["k=1 target"]["above_line"] = bool(summarise_hist(h1)[f"rec_{ti}"] >= line)
        sub(f"CAL-2 rounds at R_CAL={R} (converged = plateau by {PLATEAU_FRAC_MAX}xR_CAL AND last-20% rise <= {RISE_TOL})")
        print(f"    k={kmax} target curve: " + " ".join(f"{v:.2f}" for v in curve(h, ti)[1::2]))
        print(f"    k=1  target curve : " + " ".join(f"{v:.2f}" for v in curve(h1, ti)[1::2]))
        for nm, c in cv.items():
            extra = f"  above learnable line: {c['above_line']}" if "above_line" in c else ""
            print(f"    {nm:13s} plateau={c['plateau']}  rise={c['rise']:+.3f}  -> {c['ok']} ({c['why']}){extra}")
        if all(g1_curve_ok(nm, c) for nm, c in cv.items()): break
        if R != R_CAL_LIST[-1]: print("    -> not converged, retrying with a longer calibration run")
    cands = [c["plateau"] for c in cv.values() if c["plateau"] is not None]
    rounds = int(min(R, max(20, int(math.ceil(max(cands) / EVAL_EVERY)) * EVAL_EVERY))) if cands else R
    if cv["k=1 target"]["ok"] is None:
        print("    k=1 never learned under FedAvg: recorded as a FINDING (dilution), not a budget issue.")
    s_ref = summarise_hist(h, at_round=rounds)
    ref_recall = {c: s_ref[f"rec_{i}"] for i, c in enumerate(CLASSES) if np.isfinite(s_ref[f"rec_{i}"])}
    cal = {"lr": lr_best, "rounds": rounds, "r_cal_used": R,
           "conv": {k: {kk: (None if (isinstance(vv, float) and not np.isfinite(vv)) else vv) for kk, vv in v.items()} for k, v in cv.items()},
           "fedavg_k1_learned": cv["k=1 target"]["ok"] is not None, "ref_recall": ref_recall}
    if RUN_EXP_B and HAVE_OPACUS:
        sub("CAL-3 DP-SGD lr x clip on clip-only runs (no noise), same reference")
        best = None
        for c_ in DP_CLIP_GRID:
            for lr in DP_LR_GRID:
                s = summarise_hist(run_federated(Xt, yt, Xe, ye, cl, ro, "fedavg", C, 99, eps=-1.0, rounds=rounds, lr=lr, clip=c_))
                print(f"    clip={c_:<4} lr={lr:<5} macro={macro_of(s):.3f} target={s[f'rec_{ti}']:.3f}")
                if best is None or macro_of(s) > best[0]: best = (macro_of(s), c_, lr)
        cal.update({"dp_clip": best[1], "dp_lr": best[2]})
        print("    NOTE: tuned on clip-only runs; tuning cost is not added to the privacy budget (state this in the paper).")
    json.dump(cal, open(path, "w"), indent=1, default=str)
    print(f"\n  CALIBRATION RESULT: lr={cal['lr']} rounds={cal['rounds']} (R_CAL used {R}) "
          f"dp_clip={cal.get('dp_clip')} dp_lr={cal.get('dp_lr')}")
    print("  reference per-class recall: " + ", ".join(f"{c}={v:.3f}" for c, v in ref_recall.items()))
    return cal

# =============================================================================
#  EXPERIMENT RUNNER (resumable, keyed by calibration + settings)
# =============================================================================
KEY_COLS = ["target", "k", "f", "agg", "eps", "seed", "binary", "rmult"]

def cfg_id(cal):
    s = json.dumps({"v": VERSION, "cal": {k: cal[k] for k in ("lr", "rounds") if k in cal},
                    "dp": [cal.get("dp_clip"), cal.get("dp_lr")], "M": M_TARGET, "NBG": N_BG, "N": N_CLIENTS,
                    "B": BATCH, "LS": LOCAL_STEPS, "att": ATTEMPTED_POLICY, "T": BG_TEMPER}, sort_keys=True)
    return hashlib.md5(s.encode()).hexdigest()[:8]

def run_one(c, Xt, yt, Xe, ye, D, cal):
    ti = CLASSES.index(c["target"]); C = len(CLASSES)
    rng = np.random.default_rng(1000 * c["seed"] + 17 * c["k"] + c["f"])
    cl, roles, m_eff = build_witness_partition(D["ytr"], ti, c["k"], c["f"], N_CLIENTS, M_TARGET, N_BG, BG_TEMPER,
                                               rng, bg_counts=D["bg_counts"])
    dp = np.isfinite(c["eps"]); rounds = int(cal["rounds"] * c["rmult"])
    h = run_federated(Xt, yt, Xe, ye, cl, roles, c["agg"], C, c["seed"], eps=c["eps"], rounds=rounds,
                      lr=cal["dp_lr"] if dp else cal["lr"], clip=cal.get("dp_clip", 1.0), binary=bool(c["binary"]))
    s = summarise_hist(h); sb = summarise_hist(h, at_round=cal["rounds"])
    extra = {}
    if c["rmult"] != 1:   # EXP-D: keep the whole target curve (round-budget figure) and the 2R point
        extra = {"target_recall_2R": summarise_hist(h, at_round=2 * cal["rounds"])[f"rec_{ti}"],
                 "target_curve": " ".join(f"{x['round']}:{summarise_hist([x])[f'rec_{ti}']:.3f}" for x in h)}
    other = [s[f"rec_{j}"] for j in range(1, C) if j != ti and np.isfinite(s[f"rec_{j}"])]
    M = s["M"]
    row = {**c, "m_eff": m_eff, "target_recall": s[f"rec_{ti}"], "target_recall_base": sb[f"rec_{ti}"],
           "target_any_attack": s[f"any_{ti}"], "target_to_normal": float(M[ti, 0]),
           "benign_fpr": 1 - s["rec_0"],
           "other_attack_recall_mean": float(np.mean(other)) if other else float("nan"),
           "other_attack_recall_min": float(np.min(other)) if other else float("nan"),
           **{f"recall_{CLASSES[j]}": s[f"rec_{j}"] for j in range(C)},
           **{f"tgt_to_{CLASSES[j]}": (float(M[ti, j]) if not c["binary"] else float("nan")) for j in range(C)},
           **extra}
    return row

def exp_grid(name, configs, csv, Xt, yt, Xe, ye, D, cal):
    """Returns (rows for this calibration, complete?).  Stops cleanly at TIME_BUDGET_H."""
    cid = cfg_id(cal)
    for c in configs: c.setdefault("binary", False); c.setdefault("rmult", 1)
    done = pd.read_csv(csv) if os.path.exists(csv) else pd.DataFrame()
    keys = set()
    if len(done) and "cfg_id" in done:
        dd = done[done.cfg_id.astype(str) == cid]
        keys = set(tuple(r) for r in dd[KEY_COLS].astype(str).values)
    norm = lambda c: tuple(str(c[k]) if k != "binary" else str(bool(c[k])) for k in KEY_COLS)
    todo = [c for c in configs if norm(c) not in keys]
    print(f"  {name}: {len(configs)} configs, {len(configs)-len(todo)} done (cfg {cid}), {len(todo)} to run")
    t0 = time.time()
    for i, c in enumerate(todo, 1):
        if out_of_time():
            STOPPED["flag"] = True
            print(f"  [TIME BUDGET] {TIME_BUDGET_H} h reached: {i-1}/{len(todo)} done. Save this version, attach its"
                  f" output as an input, re-run -> resumes here."); break
        row = {**run_one(c, Xt, yt, Xe, ye, D, cal), "cfg_id": cid}
        row["binary"] = bool(row["binary"])
        append_row(csv, row)
        if i in (1, 2) or i % 10 == 0 or i == len(todo):
            el = time.time() - t0
            print(f"    [{i}/{len(todo)}] {el/60:.1f} min, ETA {el/i*(len(todo)-i)/60:.1f} min | {c['agg']} k={c['k']} "
                  f"f={c['f']} {eps_name(c['eps'])}{' BIN' if c['binary'] else ''}{' x'+str(c['rmult']) if c['rmult']!=1 else ''}"
                  f" -> tgt {row['target_recall']:.3f}", flush=True)
    out = pd.read_csv(csv); out = out[out.cfg_id.astype(str) == cid].copy()
    out["binary"] = out["binary"].astype(str).str.lower().isin(["true", "1"])
    have = set(tuple(r) for r in out[KEY_COLS].astype(str).values)
    complete = all(norm(c) in have for c in configs)
    if not complete: print(f"  {name}: INCOMPLETE -> reports for this experiment skipped until resumed")
    return out, complete


# =============================================================================
#  MITIGATION + MECHANISM CHECK  (mit-1.0)  -- everything below is new
# =============================================================================
#  M0  mechanism check : does the wall move with F_HAT (the number of attackers the
#                        aggregator is configured to tolerate)?  f = 0, 3R rounds.
#  M1  mitigation      : witness-aware aggregation (WAA), pre-registered by PAPER_PLAN_v2 §3
#                        row 4 ("walls dominate").  Arms: base | oracle | rand | rr1 | rr3.
#  M2  robustness cost : does WAA give Byzantine members a way in?  Update-level sign-flip
#                        attackers who ALWAYS claim to be witnesses.
# =============================================================================
M_TARGETS_N = 2                      # first two eligible targets (rarest first); override with RUN_TARGETS
SEEDS_M = [0, 1, 2]
REF_K = 16                           # reference = FedAvg, f=0, k=16 (same definition as v3.2)
# M0
RUN_M0 = True
K_M0 = [1, 2, 3, 4, 5, 6, 8, 10]
FHAT_M0 = [1, 2, 3, 4]
AGGS_M0 = ["trmean", "mkrum", "nnm_cwmed"]   # the only aggregators whose rule uses F_HAT
M0_RMULT = 3                          # one 3R run gives recall at R, 2R and 3R (constant lr)
# M1
RUN_M1 = True
K_M1 = [1, 2, 3, 4, 6, 8]
F_M1 = [0, 2]
AGGS_M1 = ["cwmed", "trmean", "mkrum"]
RR_EPS = {"rr1": 1.0, "rr3": 3.0}     # local-DP budget of the ONE-SHOT witness bit (randomized response)
INF = float("inf")
# arm -> (who reports, influence multiplier lambda).  Claimed witnesses are clipped to lambda x the honest
# radius tau.  lambda = 1 : a claimant moves the model no more than an honest member does.
# lambda = inf : no clipping (the oracle's coverage upper bound -- and the most a liar can exploit).
# arm -> (who reports, lambda, mode).  mode: None | "waa" | "elect" | "loud"
#   waa   : claimed witnesses bypass the robust rule, clipped to lambda x honest radius
#   elect : ELECTORATE RESTRICTION -- the target class's own output-layer parameters (its logit row + bias)
#           are aggregated with the SAME robust rule, but only over members that claim to have seen the
#           class; every other parameter is aggregated as usual over everyone.  Non-witnesses have no
#           evidence about that class yet (softmax makes them push its logit DOWN -- FedRS, KDD 2021), so
#           they lose their vote there.  Liars must out-vote the true witnesses AMONG CLAIMANTS (k > f).
#   loud  : no server change -- witnesses up-weight their rare samples x LOUD_W in the local loss
#           (client-side amplification; predicted NOT to help: robust rules count votes, not volume)
ARMS = {"base": (None, None, None),
        "orc1": ("oracle", 1.0, "waa"), "orc10": ("oracle", 10.0, "waa"), "orcinf": ("oracle", INF, "waa"),
        "randinf": ("rand", INF, "waa"), "rr3inf": ("rr3", INF, "waa"),
        "elect": ("oracle", None, "elect"), "electrr1": ("rr1", None, "elect"), "electrr3": ("rr3", None, "elect"),
        "loud": (None, None, "loud"),
        "verify": (None, None, "verify"), "probeonly": (None, None, "server")}
#   verify    : VERIFIED electorate -- no self-report.  The server holds a small labelled probe set (N_PROBE_T
#               target flows + N_PROBE_B benign flows).  Each round, a member votes on the class's logit row only
#               if its update there points the same way as the server's probe direction (cosine > 0).
#               Uses side information, so it may legitimately beat the P1 floor.
#   probeonly : TRAP CONTROL -- no electorate; the server simply adds its own probe-trained update (weight 1/N).
#               If this alone works, verification adds nothing ("if you have samples, just train on them").
ARMS_M1 = list(ARMS)
CANDIDATE_ARMS = ["orc1", "orc10", "orcinf", "elect", "verify"]   # judged on coverage AND robustness
SIDE_INFO_ARMS = ["verify", "probeonly"]                           # exempt from the floor-violation flag
LOUD_W = 10.0
N_PROBE_T, N_PROBE_B = 20, 200
K0_ARMS = ["base", "probeonly", "verify"]                          # k = 0 control: can the probe alone detect?
# M2
RUN_M2 = True
K_M2 = 6
F_M2 = [2, 4]
AGGS_M2 = ["cwmed", "trmean", "mkrum"]
SIGNFLIP_SCALE = 10.0                 # attacker update = -10 x mean honest update (turns the FedAvg mean negative for f >= 2 of 20)
ARMS_M2 = ["base"] + CANDIDATE_ARMS
# pre-registered thresholds (see print_rules_m)
TAX_TOL = 1          # "removed" = tax <= 1 (FedAvg itself shows tax 0-1)
TAX_GAIN = 2         # "reduced" = tax falls by >= 2
CELL_MAJ = 2 / 3     # share of cells that must agree
RR_TOL = 1           # RR "cheap" = k*_RR <= k*_oracle + 1
COLLATERAL_TOL = 0.05
ATTACK_DROP = 0.2    # M2 attack counts as effective if FedAvg loses >= 0.2 other-attack recall (or FPR > FPR_MAX)

if os.environ.get("WITNESS_SMOKE"):
    M_TARGETS_N, SEEDS_M, REF_K = 1, [0], 8
    K_M0, FHAT_M0, AGGS_M0, M0_RMULT = [1, 3], [1, 3, 4], ["trmean"], 2
    K_M1, F_M1, AGGS_M1 = [1, 3, 8], [0, 2], ["cwmed", "trmean"]
    ARMS_M1 = ["base", "orc1", "orcinf", "randinf", "rr3inf", "elect", "electrr3", "loud"]
    ARMS_M1 += ["verify", "probeonly"]
    CANDIDATE_ARMS = ["orc1", "orcinf", "elect", "verify"]; ARMS_M2 = ["base", "orc1", "orcinf", "elect", "verify"]
    K_M2, F_M2, AGGS_M2 = 3, [2], ["cwmed"]
    if os.environ.get("WITNESS_TARGETS"): RUN_TARGETS = os.environ["WITNESS_TARGETS"].split(",")

KEY_COLS_M = ["exp", "target", "k", "f", "agg", "arm", "fhat", "attack", "seed", "rmult"]

# -----------------------------------------------------------------------------
#  WAA + attack + reports (unit-tested in PHASE 0-M)
# -----------------------------------------------------------------------------
def signflip(U, att_mask, scale=None):
    """Byzantine rows replaced by -scale x mean of the honest rows (update-level attack)."""
    scale = SIGNFLIP_SCALE if scale is None else scale
    m = torch.as_tensor(att_mask, device=U.device).bool()
    if not bool(m.any()) or bool(m.all()): return U
    U = U.clone(); U[m] = -scale * U[~m].mean(0)
    return U

WAA_DIAG = []   # per round: median over claimed witnesses of ||u_i - a_H|| / tau  (how far outside the honest radius)

def agg_waa(U, report, base, b=F_HAT, gen=None, prev=None, lam=1.0):
    """Witness-aware aggregation.
    Members that REPORT having seen the target class form the witness channel W; the rest form H.
      a_H  = base robust aggregator over H (tolerance b, capped at (|H|-1)//2)
      tau  = (|H| - b)-th smallest distance of H-updates to a_H  (an honest distance: at most b
             Byzantine members in H can only sit above it)
      out  = a_H + (1/N) * sum_{i in W} clip_{lam*tau}(u_i - a_H)
    Each claimed witness keeps FedAvg weight 1/N and can move the model by at most lam*tau/N.
    lam = 1: no more than an honest member; lam = inf: unclipped (coverage upper bound, liars unbounded).
    Non-finite rows are dropped from both sets."""
    n = U.shape[0]
    rep = torch.as_tensor(report, device=U.device).bool()
    fin = torch.isfinite(U).all(1)
    H, W = (~rep) & fin, rep & fin
    nH = int(H.sum())
    if nH < 3:                                    # degenerate: almost everyone claims -> plain base rule
        return AGG_FN[base](U[fin] if int(fin.sum()) else U, b=b, gen=gen, prev=prev)
    bH = min(int(b), (nH - 1) // 2)
    aH = AGG_FN[base](U[H], b=bH, gen=gen, prev=prev)
    if int(W.sum()) == 0: return aH
    dH = torch.sort(torch.norm(U[H] - aH, dim=1)).values
    tau = dH[nH - 1 - bH]
    Dw = U[W] - aH; nr = torch.norm(Dw, dim=1)
    WAA_DIAG.append(float(torch.median(nr / torch.clamp(tau, min=1e-12))))
    if not math.isfinite(lam): return aH + Dw.sum(0) / n
    scale = torch.clamp(lam * tau / torch.clamp(nr, min=1e-12), max=1.0)
    return aH + (Dw * scale[:, None]).sum(0) / n

def head_row_index(params, c):
    """Flat indices (same order as flat()) of class c's output-layer weight row and bias."""
    items, off = list(params.items()), 0
    offs = []
    for k_, v in items: offs.append((k_, off, v.shape)); off += v.numel()
    wk = [o for o in offs if len(o[2]) == 2][-1]; bk = [o for o in offs if len(o[2]) == 1][-1]
    d_in = wk[2][1]
    idx = list(range(wk[1] + c * d_in, wk[1] + (c + 1) * d_in)) + [bk[1] + c]
    return torch.tensor(idx, dtype=torch.long)

def agg_elect(U, a, report, idx, base, b=F_HAT, gen=None):
    """Replace a[idx] by the base robust rule over CLAIMANTS only (tolerance capped at (n_claim-1)//2).
    No claimant -> a unchanged.  Non-finite claimant rows are dropped."""
    rep = torch.as_tensor(report, device=U.device).bool() & torch.isfinite(U).all(1)
    nC = int(rep.sum())
    if nC == 0: return a
    base_e = "cwmed" if base == "cclip" else base            # cclip's centre is a full-vector state
    v = AGG_FN[base_e](U[rep][:, idx.to(U.device)], b=min(int(b), (nC - 1) // 2), gen=gen)
    a = a.clone(); a[idx.to(U.device)] = v
    return a

VERIFY_LOG = []   # per round: bool array of members accepted into the verified electorate

def probe_signals(model, params, X, y, probe, lr):
    """probe = {'t': target idx, 'b': benign idx} into X/y.  Returns
    dir_t : -grad of CE on the TARGET probe flows (flat, same order as flat()) -> used for verification
    sdel  : server update = lr * LOCAL_STEPS * (-grad of CE on target + benign probe) -> probeonly control"""
    def g_of(ix):
        ix = torch.as_tensor(ix, device=X.device, dtype=torch.long)
        gd = grad(lambda p: F.cross_entropy(functional_call(model, p, (X[ix],)), y[ix]))(params)
        return -torch.cat([v.reshape(-1) for v in gd.values()])
    return g_of(probe["t"]), lr * LOCAL_STEPS * g_of(np.r_[probe["t"], probe["b"]])

def verify_report(U, d, idx):
    """Accept member i iff cos(u_i[idx], d[idx]) > 0; non-finite or zero rows rejected."""
    idx = idx.to(U.device); Ui = U[:, idx]; di = d[idx]
    fin = torch.isfinite(Ui).all(1)
    num = torch.nan_to_num(Ui) @ di
    den = torch.norm(torch.nan_to_num(Ui), dim=1) * torch.norm(di)
    return (fin & (den > 0) & (num > 0)).cpu().numpy()

def aggregate_round(U, agg, fhat, gen, prev, report, lam, elect_idx, vdir=None, sdel=None, pmode=None, sra_lam=None):
    """One server step: base rule | WAA (report, lambda) | electorate (report, elect_idx) |
    verified electorate (pmode='verify') | base + server probe update (pmode='server')."""
    if pmode == "verify":
        acc = verify_report(U, vdir, elect_idx); VERIFY_LOG.append(acc)
        return agg_elect(U, AGG_FN[agg](U, gen=gen, prev=prev, b=fhat), acc, elect_idx, agg, b=fhat, gen=gen)
    if sra_lam is not None and report is not None:          # mit-2.0: split robust aggregation
        return agg_sra(U, report, agg, b=fhat, gen=gen, prev=prev, lam=sra_lam)
    if report is not None and elect_idx is None:
        return agg_waa(U, report, agg, b=fhat, gen=gen, prev=prev, lam=lam)
    a = AGG_FN[agg](U, gen=gen, prev=prev, b=fhat)
    if report is not None and elect_idx is not None:
        a = agg_elect(U, a, report, elect_idx, agg, b=fhat, gen=gen)
    if pmode == "server":
        a = a + sdel / U.shape[0]
    return a

def acc_rates(log, roles):
    """Share of rounds each role was accepted into the verified electorate."""
    if not log: return {"W": float("nan"), "H": float("nan"), "A": float("nan")}
    M = np.stack(log).astype(float); r = np.asarray(roles)
    return {z: (float(M[:, r == z].mean()) if (r == z).any() else float("nan")) for z in ("W", "H", "A")}

def make_probe(D, ti, seed):
    """Server probe: N_PROBE_T target + N_PROBE_B benign TRAINING flows (may overlap members' data;
    a same-distribution probe is the optimistic case -- state it)."""
    r = np.random.default_rng(4242 + seed)
    tp, bp = np.where(D["ytr"] == ti)[0], np.where(D["ytr"] == 0)[0]
    return {"t": r.choice(tp, min(N_PROBE_T, len(tp)), replace=False), "b": r.choice(bp, min(N_PROBE_B, len(bp)), replace=False)}

def make_report(arm, roles, rng):
    """arm: 'base' | 'oracle' | 'rand' | 'rr1' | 'rr3'  (the WHO part of an M-arm; see ARMS)."""
    """One-shot witness report per member (drawn once per run, not per round).
    base   -> None (no report used)
    oracle -> honest members report truthfully
    rand   -> the same NUMBER of honest members as true witnesses, chosen at random (routing control:
              isolates 'knowing WHO' from 'sending some members around the robust rule')
    rrX    -> randomized response: truth with p = e^eps/(1+e^eps) (local DP, eps = RR_EPS[arm])
    Byzantine members (role 'A') ALWAYS claim to be witnesses (worst case for WAA)."""
    roles = np.asarray(roles); Wt = roles == "W"; A = roles == "A"
    if arm == "base": return None
    if arm == "oracle":
        rep = Wt.copy()
    elif arm == "rand":
        rep = np.zeros(len(roles), bool); cand = np.where(~A)[0]
        rep[rng.choice(cand, size=min(int(Wt.sum()), len(cand)), replace=False)] = True
    elif arm in RR_EPS:
        p = math.exp(RR_EPS[arm]) / (1.0 + math.exp(RR_EPS[arm]))
        rep = np.where(rng.random(len(roles)) < p, Wt, ~Wt)
    else:
        raise ValueError(f"unknown arm {arm}")
    return rep | A

# -----------------------------------------------------------------------------
#  DECISION LOGIC (pure functions, tested on messy synthetic inputs in PHASE 0-M)
# -----------------------------------------------------------------------------
def k_num(ks, kmax):
    """k* as a number: 'never' -> kmax + 1 (a lower bound); None/NaN -> None."""
    if ks == "never": return kmax + 1
    if ks is None: return None
    try:
        v = float(ks)
    except (TypeError, ValueError):
        return None
    return int(v) if np.isfinite(v) else None

def tax_of(ks, f, kmax):
    v = k_num(ks, kmax)
    return None if v is None else v - (f + 1)

def spearman(x, y):
    x, y = pd.Series(np.asarray(x, float)), pd.Series(np.asarray(y, float))
    if x.nunique() < 2 or y.nunique() < 2: return float("nan")
    return float(np.corrcoef(x.rank().values, y.rank().values)[0, 1])

def m0_agg_verdict(wall_by_fhat, censored=None):
    """wall_by_fhat {fhat: wall edge}.  wall edge = k*(3R) - 1 (largest k NOT learned even at 3R).
    censored {fhat: True} where k*(3R) = 'never' (edge >= largest grid k: a lower bound).
    TRACKS      : edge rises by >= 2 from smallest to largest F_HAT AND Spearman >= 0.8 (censored = lower bound)
    INDEPENDENT : edge moves by <= 1 across all F_HAT and NO value is censored
    CENSORED    : every value censored -> grid too small, no verdict
    MIXED       : anything else;  INSUFFICIENT: < 3 usable F_HAT values"""
    censored = censored or {}
    it = sorted((float(f), float(w), bool(censored.get(f, False))) for f, w in wall_by_fhat.items()
                if w is not None and np.isfinite(w))
    if len(it) < 3: return "INSUFFICIENT", float("nan")
    fh = [a for a, _, _ in it]; w = np.array([b for _, b, _ in it]); cz = [c for _, _, c in it]
    if all(cz): return "CENSORED (extend K grid)", float("nan")
    rho = spearman(fh, w)
    if w.max() - w.min() <= 1 and not any(cz): return "INDEPENDENT", rho
    if w[-1] - w[0] >= 2 and np.isfinite(rho) and rho >= 0.8 - 1e-9: return "TRACKS", rho
    return "MIXED", rho

def m0_overall(verdicts, maj=CELL_MAJ):
    v = [x for x in verdicts if x != "INSUFFICIENT" and not str(x).startswith("CENSORED")]
    if not v: return "INSUFFICIENT"
    need = math.ceil(maj * len(v) - 1e-9)
    if sum(x == "TRACKS" for x in v) >= need: return "WALL_TRACKS_FHAT"
    if sum(x == "INDEPENDENT" for x in v) >= need: return "WALL_INDEPENDENT_OF_FHAT (mechanism refuted)"
    return "MIXED"

def m1_verdict(cells, tol=TAX_TOL, gain=TAX_GAIN, maj=CELL_MAJ):
    """cells: [{base_tax, oracle_tax}] one per (aggregator, f).  Missing values skipped.
    NO_TAX_TO_REMOVE : every base tax already <= tol
    REMOVES_TAX      : every oracle tax <= tol
    REDUCES_TAX      : oracle tax <= base tax - gain in >= maj of the cells that HAD a tax
    NO_EFFECT        : otherwise.   '+HARM' appended if any oracle tax exceeds base tax by > tol."""
    c = [x for x in cells if x.get("base_tax") is not None and x.get("oracle_tax") is not None]
    if not c: return "INSUFFICIENT"
    harm = any(x["oracle_tax"] > x["base_tax"] + tol for x in c)
    taxed = [x for x in c if x["base_tax"] > tol]
    if not taxed: v = "NO_TAX_TO_REMOVE"
    elif all(x["oracle_tax"] <= tol for x in c): v = "REMOVES_TAX"
    elif np.mean([x["base_tax"] - x["oracle_tax"] >= gain for x in taxed]) >= maj - 1e-9: v = "REDUCES_TAX"
    else: v = "NO_EFFECT"
    return v + ("+HARM" if harm else "")

def identity_verdict(cells, tol=TAX_TOL, gain=TAX_GAIN, maj=CELL_MAJ):
    """Only over cells where the oracle helped (base - oracle >= gain).
    IDENTITY_MATTERS : random routing of the same number of members is worse by >= gain
    ROUTING_ONLY     : random routing is within tol of the oracle (the gain came from bypassing the rule)"""
    c = [x for x in cells if None not in (x.get("base_tax"), x.get("oracle_tax"), x.get("rand_tax"))
         and x["base_tax"] - x["oracle_tax"] >= gain]
    if not c: return "NA (oracle did not help)"
    if np.mean([x["rand_tax"] - x["oracle_tax"] >= gain for x in c]) >= maj - 1e-9: return "IDENTITY_MATTERS"
    if np.mean([x["rand_tax"] - x["oracle_tax"] <= tol for x in c]) >= maj - 1e-9: return "ROUTING_ONLY"
    return "MIXED"

def rr_verdict(pairs, tol=RR_TOL, maj=CELL_MAJ):
    """pairs: [(k*_oracle, k*_rr)] numeric (never already mapped to kmax+1).
    CHEAP: k*_rr <= k*_oracle + tol in >= maj of cells; COSTLY: in <= 1-maj; else MIXED."""
    p = [(a, b) for a, b in pairs if a is not None and b is not None]
    if not p: return "INSUFFICIENT"
    s = float(np.mean([b - a <= tol for a, b in p]))
    return "CHEAP" if s >= maj - 1e-9 else ("COSTLY" if s <= 1 - maj + 1e-9 else "MIXED")

def floor_flags(cells):
    """Oracle k* <= f would mean the channel beat perfect mimicry -- impossible by P1 -> flag a bug."""
    return [x for x in cells if x.get("oracle_k") is not None and x["oracle_k"] <= x["f"]]

def m2_verdict(fed_att, arm_att, clean, fpr_max=FPR_MAX, tol=COLLATERAL_TOL, drop=ATTACK_DROP):
    """Each argument: {'benign_fpr', 'other_mean'} (seed means).  clean = attack-free FedAvg at the same k.
    INCONCLUSIVE_ATTACK_TOO_WEAK if FedAvg itself is not hurt (the attack proves nothing).
    HOLDS if the arm keeps FPR <= fpr_max and other-attack recall within tol of clean; else BREAKS."""
    vals = [d.get(k) for d in (fed_att, arm_att, clean) for k in ("benign_fpr", "other_mean")]
    if any(v is None or not np.isfinite(v) for v in vals): return "NA"
    effective = fed_att["benign_fpr"] > fpr_max or clean["other_mean"] - fed_att["other_mean"] >= drop
    if not effective: return "INCONCLUSIVE_ATTACK_TOO_WEAK"
    ok = arm_att["benign_fpr"] <= fpr_max and arm_att["other_mean"] >= clean["other_mean"] - tol
    return "HOLDS" if ok else "BREAKS"

def frontier_verdict(per_lambda):
    """per_lambda {arm: (m1 verdict, [m2 verdicts over aggregators x f])}.
    SAFE_POINT at <arm>: M1 REMOVES or REDUCES the tax AND every M2 verdict is HOLDS or INCONCLUSIVE.
    If M2 is inconclusive everywhere the attack is too weak to judge -> UNTESTED.
    NO_SAFE_POINT: every lambda that helps coverage is broken by liars (coverage needs verified identity)."""
    safe, helps, judged = [], [], False
    for arm, (v1, v2s) in per_lambda.items():
        ok1 = str(v1).startswith(("REMOVES", "REDUCES")) and "HARM" not in str(v1)
        if ok1: helps.append(arm)
        judged |= any(v in ("HOLDS", "BREAKS") for v in v2s)
        if ok1 and v2s and all(v in ("HOLDS", "INCONCLUSIVE_ATTACK_TOO_WEAK") for v in v2s) and \
           any(v == "HOLDS" for v in v2s): safe.append(arm)
    if not helps: return "NO_CANDIDATE_HELPS (identity alone does not remove the tax)"
    if not judged: return "UNTESTED (attack too weak everywhere)"
    if safe: return "SAFE_POINT at " + ", ".join(safe)
    return "NO_SAFE_POINT (every candidate that restores coverage lets liars in)"

# -----------------------------------------------------------------------------
#  PHASE 0-M  -- self-tests for everything new (messy / adversarial synthetic inputs)
# -----------------------------------------------------------------------------
def phase0_mitigation_tests():
    banner("PHASE 0-M -- SELF-TESTS FOR WAA, ATTACKS AND NEW DECISION LOGIC (must all pass)")
    fails = []
    def check(name, cond, detail=""):
        print(f"    [{'PASS' if cond else 'FAIL'}] {name} {detail}")
        if not cond: fails.append(name)

    sub("TM1 WAA on synthetic update matrices (heterogeneous honest noise, liars, NaN)")
    g = torch.Generator().manual_seed(0)
    n, P = 20, 60
    scales = torch.linspace(0.05, 0.3, n)[:, None]                  # heterogeneous honest spread
    Ub = torch.randn(n, P, generator=g) * scales
    for base_ in ["cwmed", "trmean", "mkrum"]:
        for k in [1, 2]:
            Uw = Ub.clone(); Uw[:k, 0] += 30.0                          # witness far outside the honest radius
            rep = np.zeros(n, bool); rep[:k] = True
            a0 = float(AGG_FN[base_](Uw, b=2)[0]); a1 = float(agg_waa(Uw, rep, base_, b=2, lam=1.0)[0])
            ai = float(agg_waa(Uw, rep, base_, b=2, lam=INF)[0]); fa = float(Uw.mean(0)[0])
            check(f"{base_} k={k}: base ~0 < WAA(lam=1) << WAA(lam=inf) ~ FedAvg", a0 < 0.1 and a0 < a1 < 0.5 * ai
                  and abs(ai - fa) < 0.15 * fa, f"(base {a0:.3f}, lam1 {a1:.3f}, laminf {ai:.3f}, fedavg {fa:.3f})")
    Uw = Ub.clone(); Uw[:2, 0] += 30.0; rep = np.zeros(n, bool); rep[:2] = True
    a_l = [float(agg_waa(Uw, rep, "cwmed", b=2, lam=l)[0]) for l in (1.0, 10.0, INF)]
    check("witness signal non-decreasing in lambda", a_l[0] <= a_l[1] <= a_l[2] + 1e-6, f"({np.round(a_l, 3)})")
    WAA_DIAG.clear(); agg_waa(Uw, rep, "cwmed", b=2)
    check("diagnostic logs witness distance / tau (>> 1 here)", len(WAA_DIAG) == 1 and WAA_DIAG[0] > 5, f"({WAA_DIAG})")
    Ul = Ub.clone(); Ul[18:] = 1e4                                     # two huge liars CLAIM witness
    rep = np.zeros(n, bool); rep[18:] = True
    aH = agg_cwmed(Ul[:18], b=2); out = agg_waa(Ul, rep, "cwmed", b=2)
    dH = torch.sort(torch.norm(Ul[:18] - aH, dim=1)).values; tau = float(dH[18 - 1 - 2])
    check("liars in W move the model by <= (#W) * tau / N", float(torch.norm(out - aH)) <= 2 * tau / n + 1e-5,
          f"({float(torch.norm(out - aH)):.4f} <= {2 * tau / n:.4f})")
    out10 = agg_waa(Ul, rep, "cwmed", b=2, lam=10.0)
    check("lambda=10: liars bounded by 10 x (#W) * tau / N", float(torch.norm(out10 - aH)) <= 20 * tau / n + 1e-4)
    check("lambda=inf: liars unbounded (documents the cost)", float(torch.norm(agg_waa(Ul, rep, "cwmed", b=2, lam=INF) - aH)) > 100)
    Ul2 = Ub.clone(); Ul2[0] = 1e4; Ul2[1] = 1e4                       # two huge liars stay in H, 1 witness
    Ul2[5, 0] += 3.0; rep2 = np.zeros(n, bool); rep2[5] = True
    dH2 = torch.norm(Ul2[~torch.as_tensor(rep2)] - agg_cwmed(Ul2[~torch.as_tensor(rep2)]), dim=1)
    tau2 = float(torch.sort(dH2).values[19 - 1 - 2])
    check("liars in H cannot inflate tau (trimmed by b)", tau2 < 10.0, f"(tau={tau2:.3f})")
    check("no reports -> equals base rule on everyone", torch.allclose(agg_waa(Ub, np.zeros(n, bool), "trmean", b=2),
                                                                     agg_trmean(Ub, b=2)))
    check("everyone reports -> fallback, finite", torch.isfinite(agg_waa(Ub, np.ones(n, bool), "cwmed")).all())
    Un = Ub.clone(); Un[3, 7] = float("nan"); rep3 = np.zeros(n, bool); rep3[3] = True; rep3[4] = True
    check("NaN row in W dropped, output finite", torch.isfinite(agg_waa(Un, rep3, "mkrum")).all())
    Un2 = Ub.clone(); Un2[9, 1] = float("inf")
    check("inf row in H dropped, output finite", torch.isfinite(agg_waa(Un2, rep3 & False, "trmean")).all())
    for base_ in ["cclip", "nnm_cwmed", "geomed", "bucket_cwmed", "fedavg"]:
        check(f"WAA wraps {base_} without crashing", agg_waa(Ub, rep, base_, gen=torch.Generator().manual_seed(1)).shape == (P,))
    check("ARMS table: every arm maps to a known reporter/mode", all((w is None or w in ("oracle", "rand", *RR_EPS)) and
          m in (None, "waa", "elect", "loud", "verify", "server") and (m != "waa" or l is not None) for w, l, m in ARMS.values()))

    sub("TM1b electorate restriction + head index")
    mdl = MLP(12, 5); prm = {k: v for k, v in mdl.named_parameters()}
    idx = head_row_index(prm, 3)
    marked = {k: torch.zeros_like(v) for k, v in prm.items()}
    marked["net.4.weight"][3] = 1.0; marked["net.4.bias"][3] = 1.0
    fl = torch.cat([v.reshape(-1) for v in marked.values()])
    check("head_row_index hits exactly class-3 row + bias (65 params)", len(idx) == 65 and bool((fl[idx] == 1).all())
          and float(fl.sum()) == 65.0)
    Pd = int(fl.numel()); Ue = torch.randn(20, Pd, generator=g) * 0.05
    Ue[:, idx] -= 1.0                                                  # non-witnesses push class 3 DOWN (softmax)
    Ue[:2][:, idx] += 0.0; Ue[0, idx] = 2.0; Ue[1, idx] = 2.0          # two witnesses push it UP
    rep = np.zeros(20, bool); rep[:2] = True
    a0 = agg_cwmed(Ue); ae = agg_elect(Ue, a0, rep, idx, "cwmed")
    check("cwmed: class row follows the majority (-1) without, the claimants (+2) with electorate",
          float(a0[idx].mean()) < -0.5 and abs(float(ae[idx].mean()) - 2.0) < 0.1)
    other = torch.ones(Pd, dtype=torch.bool); other[idx] = False
    check("electorate leaves every other parameter untouched", torch.equal(ae[other], a0[other]))
    Ul = Ue.clone(); rep_l = rep.copy(); rep_l[2:5] = True; Ul[2:5, idx] = -50.0     # 2 witnesses, 3 liars claim
    check("liars out-vote witnesses among claimants when k <= f (floor, documented)",
          float(agg_elect(Ul, a0, rep_l, idx, "cwmed")[idx].mean()) < -10)
    Uh = Ue.clone(); rep_h = rep.copy(); rep_h[2] = True; Uh[2, idx] = -50.0; Uh[3, idx] = 2.0; rep_h[3] = True
    check("honest claimants out-vote liars when k > f (3 vs 1)", abs(float(agg_elect(Uh, a0, rep_h, idx, "cwmed")[idx].mean()) - 2.0) < 0.1)
    check("no claimants -> unchanged", torch.equal(agg_elect(Ue, a0, np.zeros(20, bool), idx, "cwmed"), a0))
    Un = Ue.clone(); Un[0, 5] = float("nan")
    check("NaN claimant dropped, finite", torch.isfinite(agg_elect(Un, a0, rep, idx, "cwmed")).all())
    dv = torch.zeros(Pd); dv[idx] = torch.rand(len(idx), generator=g) + 0.1        # probe direction: class row UP
    Uv = torch.randn(20, Pd, generator=g) * 0.05; Uv[:, idx] = -0.5                # non-witnesses: DOWN
    Uv[0, idx] = 1.0; Uv[1, idx] = 0.8                                              # witnesses: UP
    Uv[2, idx] = -3.0                                                               # mimic liar: DOWN
    Uv[3] = -10 * Uv[4:].mean(0)                                                    # sign-flip liar: UP by accident
    Uv[5, 7] = float("nan"); Uv[6] = 0.0
    acc = verify_report(Uv, dv, idx)
    check("verify accepts witnesses, rejects non-witnesses + mimic, admits sign-flip (documented), drops NaN/zero rows",
          acc[0] and acc[1] and not acc[2] and acc[3] and not acc[5] and not acc[6] and acc[4:].sum() == 0, f"({np.where(acc)[0]})")
    mdl2 = MLP(12, 5).to(DEV); prm2 = {k: v.detach() for k, v in mdl2.named_parameters()}
    Xp = torch.randn(300, 12, device=DEV); yp = torch.zeros(300, dtype=torch.long, device=DEV); yp[:20] = 3
    dt, sd = probe_signals(mdl2, prm2, Xp, yp, {"t": np.arange(20), "b": np.arange(20, 300)}, 0.1)
    ih = head_row_index(prm2, 3).to(DEV)
    check("probe direction on the class row is non-negative (ReLU features x (1 - p) >= 0)", bool((dt[ih] >= -1e-7).all())
          and dt.shape == sd.shape and bool(torch.isfinite(sd).all()))
    for base_ in ["trmean", "mkrum", "geomed", "nnm_cwmed", "bucket_cwmed", "cclip", "fedavg"]:
        check(f"electorate wraps {base_} (1 claimant) without crashing",
              agg_elect(Ue, a0, np.eye(20, dtype=bool)[0], idx, base_, gen=torch.Generator().manual_seed(1)).shape == (Pd,))

    sub("TM2 reports and attack")
    roles = np.array(["W"] * 3 + ["A"] * 2 + ["H"] * 15, dtype=object)
    r = make_report("oracle", roles, np.random.default_rng(0))
    check("oracle: witnesses + attackers report, nobody else", list(np.where(r)[0]) == [0, 1, 2, 3, 4])
    check("base -> None", make_report("base", roles, np.random.default_rng(0)) is None)
    rr = [make_report("rand", roles, np.random.default_rng(s)) for s in range(300)]
    check("rand: exactly k honest + all attackers every draw", all(x.sum() == 5 and x[3] and x[4] for x in rr))
    hit = np.mean([x[:3].sum() / 3 for x in rr])
    check("rand: witnesses hit at chance rate (~3/18)", abs(hit - 3 / 18) < 0.05, f"({hit:.3f})")
    for arm, e in RR_EPS.items():
        p = math.exp(e) / (1 + math.exp(e))
        R = np.stack([make_report(arm, roles, np.random.default_rng(s)) for s in range(4000)])
        tw, fh = R[:, :3].mean(), R[:, 5:].mean()
        check(f"{arm}: P(report|W)~{p:.2f}, P(report|H)~{1-p:.2f}, attackers always 1",
              abs(tw - p) < 0.03 and abs(fh - (1 - p)) < 0.03 and R[:, 3:5].all(), f"({tw:.3f}, {fh:.3f})")
    try: make_report("bogus", roles, np.random.default_rng(0)); check("unknown arm raises", False)
    except ValueError: check("unknown arm raises", True)
    U = torch.randn(6, 4, generator=g); m = np.array([0, 0, 1, 0, 1, 0], bool)
    S = signflip(U, m, scale=5.0)
    check("signflip: attacker rows = -5 x honest mean, honest untouched",
          torch.allclose(S[2], -5 * U[~torch.as_tensor(m)].mean(0)) and torch.equal(S[~torch.as_tensor(m)], U[~torch.as_tensor(m)]))
    check("signflip: no attackers -> unchanged", torch.equal(signflip(U, np.zeros(6, bool)), U))

    sub("TM3 decision logic on messy inputs")
    check("k_num: never -> kmax+1, NaN -> None, str int ok", k_num("never", 8) == 9 and k_num(float("nan"), 8) is None
          and k_num("3", 8) == 3 and k_num(None, 8) is None)
    check("tax_of(4, f=2) = 1", tax_of(4, 2, 8) == 1)
    check("M0 clean tracking", m0_agg_verdict({1: 1, 2: 2, 3: 3, 4: 4})[0] == "TRACKS")
    check("M0 flat -> INDEPENDENT", m0_agg_verdict({1: 2, 2: 2, 3: 3, 4: 2})[0] == "INDEPENDENT")
    check("M0 non-monotone big swing -> MIXED", m0_agg_verdict({1: 4, 2: 1, 3: 5, 4: 2})[0] == "MIXED")
    check("M0 rises but one dip (rho>=0.8) -> TRACKS", m0_agg_verdict({1: 1, 2: 3, 3: 2, 4: 4})[0] == "TRACKS")
    check("M0 falling -> MIXED (not TRACKS)", m0_agg_verdict({1: 4, 2: 3, 3: 2, 4: 1})[0] == "MIXED")
    check("M0 NaN/None cells skipped; <3 -> INSUFFICIENT", m0_agg_verdict({1: None, 2: float("nan"), 3: 3, 4: 4})[0] == "INSUFFICIENT")
    check("M0 censored ceiling is never INDEPENDENT", m0_agg_verdict({1: 2, 3: 3, 4: 3}, {3: True, 4: True})[0] != "INDEPENDENT")
    check("M0 rise into ceiling (censored lower bound) -> TRACKS", m0_agg_verdict({1: 1, 2: 2, 3: 3, 4: 9}, {4: True})[0] == "TRACKS")
    check("M0 all censored -> CENSORED", m0_agg_verdict({1: 9, 2: 9, 3: 9}, {1: True, 2: True, 3: True})[0].startswith("CENSORED"))
    check("M0 overall ignores CENSORED", m0_overall(["TRACKS", "CENSORED (extend K grid)", "TRACKS"]) == "WALL_TRACKS_FHAT")
    check("M0 overall 2/3 tracks", m0_overall(["TRACKS", "TRACKS", "MIXED"]) == "WALL_TRACKS_FHAT")
    check("M0 overall 2/3 independent", m0_overall(["INDEPENDENT", "INDEPENDENT", "TRACKS"]).startswith("WALL_INDEPENDENT"))
    check("M0 overall split -> MIXED", m0_overall(["TRACKS", "INDEPENDENT", "MIXED"]) == "MIXED")
    check("M0 overall ignores INSUFFICIENT", m0_overall(["TRACKS", "INSUFFICIENT", "TRACKS"]) == "WALL_TRACKS_FHAT")
    C = lambda b, o, r=None: {"base_tax": b, "oracle_tax": o, "rand_tax": r}
    check("M1 removes", m1_verdict([C(6, 0), C(3, 1), C(8, 1)]) == "REMOVES_TAX")
    check("M1 reduces", m1_verdict([C(6, 2), C(3, 1), C(8, 5), C(2, 2)]) == "REDUCES_TAX")
    check("M1 no effect", m1_verdict([C(6, 5), C(3, 3), C(8, 7)]) == "NO_EFFECT")
    check("M1 nothing to remove", m1_verdict([C(1, 0), C(0, 0)]) == "NO_TAX_TO_REMOVE")
    check("M1 harm flagged", m1_verdict([C(6, 0), C(1, 4)]).endswith("+HARM"))
    check("M1 missing cells skipped", m1_verdict([C(None, 0), C(6, 0)]) == "REMOVES_TAX")
    check("M1 all missing -> INSUFFICIENT", m1_verdict([C(None, None)]) == "INSUFFICIENT")
    check("identity matters", identity_verdict([C(6, 0, 6), C(5, 1, 5), C(8, 1, 3)]) == "IDENTITY_MATTERS")
    check("routing only", identity_verdict([C(6, 0, 1), C(5, 1, 1), C(8, 1, 2)]) == "ROUTING_ONLY")
    check("identity NA when oracle did not help", identity_verdict([C(6, 6, 6)]).startswith("NA"))
    check("RR cheap", rr_verdict([(1, 2), (3, 3), (2, 2)]) == "CHEAP")
    check("RR costly", rr_verdict([(1, 5), (3, 9), (2, 2)]) == "COSTLY")
    check("RR None skipped", rr_verdict([(1, None), (None, 2)]) == "INSUFFICIENT")
    check("floor flag when oracle k* <= f", len(floor_flags([{"oracle_k": 2, "f": 2}, {"oracle_k": 3, "f": 2}])) == 1)
    cl_ = {"benign_fpr": 0.01, "other_mean": 0.95}
    check("M2 weak attack -> INCONCLUSIVE", m2_verdict({"benign_fpr": .01, "other_mean": .94}, {"benign_fpr": .01, "other_mean": .94}, cl_).startswith("INCONCLUSIVE"))
    check("M2 holds", m2_verdict({"benign_fpr": .4, "other_mean": .5}, {"benign_fpr": .02, "other_mean": .93}, cl_) == "HOLDS")
    check("M2 breaks on FPR", m2_verdict({"benign_fpr": .4, "other_mean": .5}, {"benign_fpr": .2, "other_mean": .93}, cl_) == "BREAKS")
    check("M2 breaks on collateral", m2_verdict({"benign_fpr": .01, "other_mean": .5}, {"benign_fpr": .01, "other_mean": .85}, cl_) == "BREAKS")
    check("M2 NaN -> NA", m2_verdict({"benign_fpr": float("nan"), "other_mean": .5}, cl_, cl_) == "NA")
    fv = frontier_verdict
    check("frontier: safe point", fv({"orc1": ("NO_EFFECT", ["HOLDS"]), "orc10": ("REDUCES_TAX", ["HOLDS", "INCONCLUSIVE_ATTACK_TOO_WEAK"]),
                                      "orcinf": ("REMOVES_TAX", ["BREAKS"])}) == "SAFE_POINT at orc10")
    check("frontier: no safe point", fv({"orc1": ("NO_EFFECT", ["HOLDS"]), "orcinf": ("REMOVES_TAX", ["BREAKS", "HOLDS"])}).startswith("NO_SAFE_POINT"))
    check("frontier: nothing helps", fv({"orc1": ("NO_EFFECT", ["HOLDS"]), "orcinf": ("NO_EFFECT", ["BREAKS"])}).startswith("NO_CANDIDATE_HELPS"))
    check("frontier: HARM never counts as help", fv({"orcinf": ("REMOVES_TAX+HARM", ["HOLDS"])}).startswith("NO_CANDIDATE_HELPS"))
    check("frontier: attack too weak everywhere -> UNTESTED", fv({"orcinf": ("REMOVES_TAX", ["INCONCLUSIVE_ATTACK_TOO_WEAK"])}).startswith("UNTESTED"))
    check("frontier: missing M2 -> not safe", fv({"orcinf": ("REMOVES_TAX", [])}).startswith("UNTESTED"))

    sub("TM4 end-to-end on synthetic data (includes mimic + sign-flip attackers)")
    r3 = np.random.default_rng(1); d, Cc = 12, 4; mus = r3.normal(0, 3, (Cc, d))
    ytr = r3.choice(Cc, 20000, p=[.6, .2, .15, .05]); Xtr = mus[ytr] + r3.normal(0, 1.5, (20000, d))
    yte = r3.choice(Cc, 4000, p=[.4, .2, .2, .2]); Xte = mus[yte] + r3.normal(0, 1.5, (4000, d))
    T = lambda a, dt=torch.float32: torch.tensor(a, dtype=dt, device=DEV)
    Xt, yt, Xe, ye = T(Xtr), T(ytr, torch.long), T(Xte), T(yte, torch.long)
    def go(agg, k, f, arm, attack="mimic", fhat=F_HAT, rounds=25):
        cl, ro, _ = build_witness_partition(ytr, 3, k, f, 20, 400, 300, 0.5, np.random.default_rng(0))
        who, lam, mode = ARMS[arm]
        rep = None if who is None else make_report(who, ro, np.random.default_rng(5))
        pr = make_probe({"ytr": ytr}, 3, 0) if mode in ("verify", "server") else None
        VERIFY_LOG.clear()
        s = summarise_hist(run_federated(Xt, yt, Xe, ye, cl, ro, agg, Cc, 0, rounds=rounds, fhat=fhat,
                                         report=rep, attack=attack, waa_lam=lam if lam is not None else 1.0,
                                         elect_cls=3 if mode in ("elect", "verify") else None,
                                         loud=(3, LOUD_W) if mode == "loud" else None,
                                         probe=pr, probe_mode=mode if mode in ("verify", "server") else None))
        s["acc"] = acc_rates(VERIFY_LOG, ro)
        oth = float(np.mean([s["rec_1"], s["rec_2"]]))
        print(f"      {agg:7s} k={k} f={f} {arm:6s} {attack:8s} fhat={fhat}: target {s['rec_3']:.3f} | "
              f"other {oth:.3f} | FPR {1 - s['rec_0']:.3f}")
        return s, oth
    s_b, _ = go("cwmed", 2, 0, "base"); s_1, _ = go("cwmed", 2, 0, "orc1"); s_i, _ = go("cwmed", 2, 0, "orcinf")
    check("cwmed k=2: base suppressed, oracle lam=inf learns", s_b["rec_3"] < 0.3 and s_i["rec_3"] > 0.6)
    print(f"      (mechanism note: oracle lam=1 target = {s_1['rec_3']:.3f} -- honest witnesses sit far outside the honest radius)")
    s_b, _ = go("trmean", 2, 0, "base"); s_i, _ = go("trmean", 2, 0, "orcinf")
    check("trmean k=2 (b=2): base suppressed, oracle lam=inf learns", s_b["rec_3"] < 0.3 and s_i["rec_3"] > 0.6)
    s_f, _ = go("cwmed", 2, 3, "orcinf")
    check("oracle lam=inf respects the floor: k=2 <= f=3 mimics claiming witness -> suppressed", s_f["rec_3"] < 0.3)
    s_6, _ = go("cwmed", 6, 2, "orcinf")
    check("oracle lam=inf, k=6 > f=2 mimics -> learns", s_6["rec_3"] > 0.6)
    s_t1, _ = go("trmean", 2, 0, "base", fhat=1); s_t4, _ = go("trmean", 2, 0, "base", fhat=4)
    check("F_HAT plumbed: trmean k=2 learns at fhat=1, suppressed at fhat=4", s_t1["rec_3"] > 0.6 and s_t4["rec_3"] < 0.3)
    _, o_clean = go("fedavg", 4, 0, "base")
    s_fa, o_fa = go("fedavg", 4, 3, "base", attack="signflip")
    check("sign-flip f=3 breaks FedAvg (attack is effective on synthetic data)",
          (1 - s_fa["rec_0"]) > FPR_MAX or o_clean - o_fa >= ATTACK_DROP, f"(other {o_clean:.3f} -> {o_fa:.3f})")
    s_w, o_w = go("cwmed", 4, 3, "orc1", attack="signflip")
    check("lam=1 + sign-flip liars claiming witness: FPR and other-class recall hold",
          (1 - s_w["rec_0"]) <= FPR_MAX and o_w >= o_clean - 0.1, f"(other {o_w:.3f}, FPR {1 - s_w['rec_0']:.3f})")
    s_e15, _ = go("cwmed", 15, 0, "elect")
    check("electorate sanity: k=15 learns", s_e15["rec_3"] > 0.6)
    s_e2, _ = go("cwmed", 2, 0, "elect"); s_l2, _ = go("cwmed", 2, 0, "loud"); s_lf, _ = go("fedavg", 1, 0, "loud")
    print(f"      (outcome, not asserted: cwmed k=2 electorate {s_e2['rec_3']:.3f}, loud {s_l2['rec_3']:.3f})")
    check("loud path runs and FedAvg still learns at k=1", s_lf["rec_3"] > 0.6)
    s_ef, _ = go("cwmed", 2, 3, "elect")
    check("electorate respects the floor: k=2 <= f=3 mimics claiming -> suppressed", s_ef["rec_3"] < 0.3)
    s_es, o_es = go("cwmed", 4, 3, "elect", attack="signflip")
    check("electorate + sign-flip liars claiming (k=4 > f=3): FPR and other-class recall hold",
          (1 - s_es["rec_0"]) <= FPR_MAX and o_es >= o_clean - 0.1, f"(other {o_es:.3f}, FPR {1 - s_es['rec_0']:.3f})")
    s_v15, _ = go("cwmed", 15, 0, "verify")
    check("verify sanity: k=15 learns", s_v15["rec_3"] > 0.6)
    s_vf, _ = go("cwmed", 2, 3, "verify")
    check("verify diagnostics: true witnesses accepted more often than mimics", s_vf["acc"]["W"] > s_vf["acc"]["A"],
          f"({s_vf['acc']})")
    s_v2, _ = go("cwmed", 2, 0, "verify"); s_p0, _ = go("cwmed", 0, 0, "probeonly"); s_v0, _ = go("cwmed", 0, 0, "verify")
    print(f"      (outcomes, not asserted: verify k=2 f=0 {s_v2['rec_3']:.3f} | verify k=2 f=3 mimic {s_vf['rec_3']:.3f} | "
          f"probeonly k=0 {s_p0['rec_3']:.3f} | verify k=0 {s_v0['rec_3']:.3f})")
    s_x, o_x = go("cwmed", 4, 3, "orcinf", attack="signflip")
    check("lam=inf + sign-flip liars claiming witness: damage like FedAvg (the cost is real, implementation passes liars)",
          (1 - s_x["rec_0"]) > FPR_MAX or o_clean - o_x >= ATTACK_DROP, f"(other {o_x:.3f}, FPR {1 - s_x['rec_0']:.3f})")
    print(f"\n  PHASE 0-M RESULT: {'ALL PASSED' if not fails else f'{len(fails)} FAILED -> {fails}'}")
    return not fails

# =============================================================================
#  mit-2.0  --  SPLIT ROBUST AGGREGATION (SRA)   -- everything below is new
# =============================================================================
#  M3  coverage   : can SRA reach the P1 floor k* = f + 1?   arms base | orcinf | elect | sra | sra_rr1 |
#                   sra_rr3 | sra_rand, f in {0, 2, 4}.  Byzantine (mimic) members ALWAYS claim evidence.
#  M4  robustness : sign-flip x10 and ALIE (z = 1), attackers claiming W and not claiming.  PAIRED verdict:
#                   arm vs the BASE RULE under the SAME attack (primary); vs clean FedAvg (secondary).
#  M5  DP         : eps = 3, f = 0, base vs sra.
#  Last mitigation experiment (stop rule): whatever the headline, consolidate and write.
# =============================================================================
LAMBDA_W = 3.0            # PRE-REGISTERED W-stratum clip multiplier (real per-witness ratio measured 1.4-1.9) -> headline
LAMBDA_W_DIAG = 10.0      # POST-HOC diagnostic arm sra_l10 (option B): on realistic synthetic data the STRATUM ratio was
                          # 3.2-3.6 and lambda=3 clipped 84% of rounds -> separates "SRA fails" from "lambda=3 too tight"
ALIE_Z = 1.0              # Baruch et al. 2019: u = mu - z * sigma over honest updates
RUN_M3, RUN_M4, RUN_M5 = True, True, True
K_M3 = [1, 2, 3, 4, 6, 8]
F_M3 = [0, 2, 4]
AGGS_M3 = ["cwmed", "trmean", "mkrum"]
# arm -> (who reports, lambda, mode)   mode: None | "waa" | "elect" | "sra"
ARMS2 = {"base": (None, None, None),
         "orcinf": ("oracle", INF, "waa"),        # anchor from mit-1.0 (coverage upper bound, exploitable)
         "elect": ("oracle", None, "elect"),      # anchor from mit-1.0 (robust, output row only)
         "sra": ("oracle", LAMBDA_W, "sra"),      # truthful bit (pre-registered, headline)
         "sra_l10": ("oracle", LAMBDA_W_DIAG, "sra"),   # truthful bit, lambda_W = 10 (post-hoc diagnostic)
         "sra_rr1": ("rr1", LAMBDA_W, "sra"),     # randomized-response bit, eps_w = 1
         "sra_rr3": ("rr3", LAMBDA_W, "sra"),     # randomized-response bit, eps_w = 3
         "sra_rand": ("rand", LAMBDA_W, "sra")}   # same NUMBER of members placed in W at random
ARMS_M3 = list(ARMS2)
M4_CELLS = [(6, 2), (6, 4), (2, 4)]              # (k, f); k > f cells enter the headline, (2, 4) = bounded damage
ATTACKS_M4 = ["signflip", "alie"]
CLAIM_ARMS_M4 = ["sra", "sra_l10", "orcinf", "elect"]
AGGS_M4 = ["cwmed", "trmean", "mkrum"]
M4_TOL = 0.05
EPS_M5 = 3.0
K_M5 = [1, 2, 3, 4, 6, 8]
AGGS_M5 = ["cwmed", "trmean", "mkrum"]
ARMS_M5 = ["base", "sra"]
ATTACKS = ("mimic", "signflip", "alie", "signflip_nc", "alie_nc")   # _nc = attackers do NOT claim evidence
KEY_COLS_M2 = ["exp", "target", "k", "f", "agg", "arm", "attack", "eps", "seed"]

if os.environ.get("WITNESS_SMOKE"):
    K_M3, F_M3, AGGS_M3 = [1, 3, 8], [0, 2], ["cwmed", "trmean"]
    ARMS_M3 = ["base", "orcinf", "sra", "sra_l10", "sra_rr3", "sra_rand"]
    M4_CELLS, AGGS_M4, CLAIM_ARMS_M4 = [(3, 2), (2, 3)], ["cwmed"], ["sra", "sra_l10"]
    K_M5, AGGS_M5 = [1, 3], ["cwmed"]
    REF_MIN = float(os.environ.get("WITNESS_REFMIN", REF_MIN))     # dev smoke only: let reports run on toy data

# -----------------------------------------------------------------------------
#  SRA + ALIE + reports (unit-tested in PHASE 0-S)
# -----------------------------------------------------------------------------
SRA_DIAG = []   # per round: {"ratio": ||a_W - a_H|| / tau, "hit": clip bound hit, "nW": |W|, "fallback": bool}

def agg_sra(U, report, base, b=F_HAT, gen=None, prev=None, lam=LAMBDA_W):
    """Split robust aggregation.
      H = members that do NOT claim evidence, W = members that claim (non-finite rows dropped from both)
      a_H = base robust rule over H (tolerance capped at (|H|-1)//2)
      a_W = coordinate-wise median over W (breakdown 1/2: liars must OUTNUMBER honest claimants)
      tau = (|H| - b_H)-th smallest distance of H rows to a_H (honest radius, as in mit-1.0 WAA)
      out = a_H + (|W| / N) * clip_{lam * tau}(a_W - a_H)
    Damage bound: ||out - a_H|| <= (|W| / N) * lam * tau, whoever sits in W.
    |H| < 3 (almost everyone claims) -> base rule over all finite rows (logged as fallback)."""
    n = U.shape[0]
    rep = torch.as_tensor(np.asarray(report, bool), device=U.device)
    fin = torch.isfinite(U).all(1)
    H, W = (~rep) & fin, rep & fin
    nH, nW = int(H.sum()), int(W.sum())
    if nH < 3:
        SRA_DIAG.append({"ratio": float("nan"), "hit": False, "nW": nW, "fallback": True})
        return AGG_FN[base](U[fin] if int(fin.sum()) else torch.nan_to_num(U), b=b, gen=gen, prev=prev)
    bH = min(int(b), (nH - 1) // 2)
    aH = AGG_FN[base](U[H], b=bH, gen=gen, prev=prev)
    if nW == 0:
        SRA_DIAG.append({"ratio": float("nan"), "hit": False, "nW": 0, "fallback": False})
        return aH
    aW = agg_cwmed(U[W])
    tau = torch.sort(torch.norm(U[H] - aH, dim=1)).values[nH - 1 - bH]
    diff = aW - aH; nr = torch.norm(diff)
    ratio = float(nr / torch.clamp(tau, min=1e-12))
    if math.isfinite(lam):
        hit = bool(nr > lam * tau)
        diff = diff * torch.clamp(lam * tau / torch.clamp(nr, min=1e-12), max=1.0)
    else:
        hit = False
    SRA_DIAG.append({"ratio": ratio, "hit": hit, "nW": nW, "fallback": False})
    return aH + (nW / n) * diff

def alie(U, att_mask, z=None):
    """ALIE (Baruch et al., NeurIPS 2019): attacker rows = mu - z * sigma, coordinate-wise over honest rows."""
    z = ALIE_Z if z is None else z
    m = torch.as_tensor(np.asarray(att_mask, bool), device=U.device)
    if not bool(m.any()) or bool(m.all()): return U
    Hn = U[~m]
    sd = Hn.std(0, correction=0) if Hn.shape[0] > 1 else torch.zeros_like(Hn[0])
    U = U.clone(); U[m] = Hn.mean(0) - z * sd
    return U

def make_report2(who, roles, rng, att_claims=True):
    """mit-1.0 make_report (attackers always claim), optionally with attackers NOT claiming (att_claims=False)."""
    rep = make_report(who, roles, rng)
    if rep is None or att_claims: return rep
    return rep & (np.asarray(roles) != "A")

# -----------------------------------------------------------------------------
#  DECISION LOGIC (pure functions, tested on messy inputs in PHASE 0-S)
# -----------------------------------------------------------------------------
def rr_predicted_kstar(eps, f, n=N_CLIENTS):
    """Smallest k with k*p > (n-k-f)(1-p) + f, p = e^eps/(1+e^eps).  W holds k*p honest witnesses,
    (n-k-f)(1-p) honest non-witnesses (push the class DOWN) and f liars.  None if no k <= n-f works."""
    p = math.exp(eps) / (1.0 + math.exp(eps)) if math.isfinite(eps) else 1.0
    for k in range(1, n - f + 1):
        if k * p > (n - k - f) * (1 - p) + f + 1e-12: return k
    return None

def rr_match(measured, pred, grid, tol=1):
    """Censoring-aware: the grid k* 'measured' means true k* is in (previous grid k, measured];
    'never' means true k* > max(grid).  Match if that interval meets [pred - tol, pred + tol].
    pred None = formula says never.  Unusable measured -> None."""
    grid = sorted(grid); kmax = grid[-1]
    if measured == "never":
        return True if pred is None else bool(pred + tol > kmax)
    m = k_num(measured, kmax)
    if m is None: return None
    if pred is None: return False
    lower = max([g for g in grid if g < m], default=0)
    return bool(max(lower + 1, pred - tol) <= min(m, pred + tol))

def rr_formula_verdict(items, maj=CELL_MAJ):
    """items: [(match at tol 1, match at tol 2)].  None skipped."""
    v = [(a, b) for a, b in items if a is not None and b is not None]
    if not v: return "INSUFFICIENT"
    if np.mean([a for a, _ in v]) >= maj - 1e-9: return "FORMULA_HOLDS"
    if np.mean([b for _, b in v]) >= maj - 1e-9: return "FORMULA_ROUGH (within +-2 only)"
    return "FORMULA_FAILS (report the measured curve)"

def floor_reach_verdict(cells, maj=CELL_MAJ):
    """cells: [(k* numeric or None, f)].  REACHES_FLOOR if k* <= f + 1 in >= maj of usable cells."""
    c = [(k, f) for k, f in cells if k is not None]
    if not c: return "INSUFFICIENT", float("nan")
    share = float(np.mean([k <= f + 1 for k, f in c]))
    return ("REACHES_FLOOR" if share >= maj - 1e-9 else "ABOVE_FLOOR"), share

def m4_paired_verdict(base_att, arm_att, tol=M4_TOL, fpr_max=FPR_MAX):
    """Primary M4 rule.  Both dicts {'benign_fpr', 'other_mean'} under the SAME attack.
    HOLDS if arm FPR <= base FPR + tol AND arm other-attack recall >= base - tol, AND (where base keeps
    FPR <= fpr_max) the arm does too.  Being better than base is always fine."""
    vals = [d.get(k) for d in (base_att, arm_att) for k in ("benign_fpr", "other_mean")]
    if any(v is None or not np.isfinite(v) for v in vals): return "NA"
    ok = arm_att["benign_fpr"] <= base_att["benign_fpr"] + tol + 1e-12 and \
         arm_att["other_mean"] >= base_att["other_mean"] - tol - 1e-12
    if base_att["benign_fpr"] <= fpr_max + 1e-12: ok = ok and arm_att["benign_fpr"] <= fpr_max + 1e-12
    return "HOLDS" if ok else "BREAKS"

def headline_m2(coverage, reach, m4_verdicts):
    """coverage: m1_verdict of sra; reach: floor_reach_verdict label; m4_verdicts: PAIRED verdicts of sra in
    every k > f cell (all attacks, claim + no-claim, all aggregators)."""
    v = [x for x in m4_verdicts if x != "NA"]
    if not v: return "UNTESTED (no usable M4 verdicts)"
    holds = all(x == "HOLDS" for x in v)
    if reach == "REACHES_FLOOR" and holds: return "TIGHT_FIX"
    if str(coverage).startswith(("REMOVES", "REDUCES")) and "HARM" not in str(coverage) and holds: return "PARTIAL"
    return "NO_SAFE_POINT_CONFIRMED"

HEAD_ORDER = {"TIGHT_FIX": 2, "PARTIAL": 1, "NO_SAFE_POINT_CONFIRMED": 0}
def dataset_headline(per_target):
    v = [h for h in per_target if h in HEAD_ORDER]
    return min(v, key=HEAD_ORDER.get) if v else "UNTESTED"

# -----------------------------------------------------------------------------
#  PHASE 0-S  -- self-tests for everything new (messy / adversarial synthetic inputs)
# -----------------------------------------------------------------------------
def phase0_sra_tests():
    banner("PHASE 0-S -- SELF-TESTS FOR SRA, ALIE, mit-2 DECISION LOGIC (must all pass)")
    fails = []
    def check(name, cond, detail=""):
        print(f"    [{'PASS' if cond else 'FAIL'}] {name} {detail}")
        if not cond: fails.append(name)
    g = torch.Generator().manual_seed(3)
    n, P = 20, 60
    Ub = torch.randn(n, P, generator=g) * torch.linspace(0.05, 0.3, n)[:, None]   # heterogeneous honest spread
    def parts(U, rep, base="cwmed", b=2):
        H = ~torch.as_tensor(rep) & torch.isfinite(U).all(1); nH = int(H.sum()); bH = min(b, (nH - 1) // 2)
        aH = AGG_FN[base](U[H], b=bH)
        tau = float(torch.sort(torch.norm(U[H] - aH, dim=1)).values[nH - 1 - bH])
        return aH, tau

    sub("TS1 SRA unit tests")
    for base_ in ["cwmed", "trmean", "mkrum"]:
        U = Ub.clone(); U[:3, 0] += 0.4; U[3, 0] = -1e3                      # 3 witnesses + 1 huge liar in W
        rep = np.zeros(n, bool); rep[:4] = True
        aH, tau = parts(U, rep, base_); out = agg_sra(U, rep, base_, b=2, lam=INF)
        check(f"{base_}: honest-majority W -> witness side wins (out[0] > a_H[0], liar ignored)",
              float(out[0]) > float(aH[0]) + 0.02 and float(out[0]) < 1.0, f"({float(aH[0]):.3f} -> {float(out[0]):.3f})")
        check(f"{base_}: base rule alone suppresses the same signal", abs(float(AGG_FN[base_](U, b=2)[0])) < 0.1)
    U = Ub.clone(); U[:2, :] += 0.5; U[2:6] = 1e4                            # 2 witnesses, 4 liars claim
    rep = np.zeros(n, bool); rep[:6] = True
    aH, tau = parts(U, rep); out = agg_sra(U, rep, "cwmed", b=2, lam=LAMBDA_W)
    bound = 6 / n * LAMBDA_W * tau
    check("liar-majority W: damage <= (|W|/N) * lambda * tau", float(torch.norm(out - aH)) <= bound * (1 + 1e-4),
          f"({float(torch.norm(out - aH)):.4f} <= {bound:.4f})")
    check("liar-majority W: clip-hit logged", SRA_DIAG[-1]["hit"] and SRA_DIAG[-1]["nW"] == 6)
    check("liar-majority W, lambda=inf: unbounded (documents why lambda is needed)",
          float(torch.norm(agg_sra(U, rep, "cwmed", b=2, lam=INF) - aH)) > 100)
    for base_ in ["cwmed", "trmean", "mkrum"]:
        check(f"{base_}: empty W == base rule on everyone",
              torch.allclose(agg_sra(Ub, np.zeros(n, bool), base_, b=2), AGG_FN[base_](Ub, b=2)))
    SRA_DIAG.clear(); oa = agg_sra(Ub, np.ones(n, bool), "cwmed", b=2)
    check("everyone in W -> fallback to base over all, finite, logged", torch.isfinite(oa).all()
          and torch.allclose(oa, agg_cwmed(Ub)) and SRA_DIAG[-1]["fallback"])
    rep17 = np.ones(n, bool); rep17[:3] = False
    check("|H| = 3 exactly -> no fallback, finite", torch.isfinite(agg_sra(Ub, rep17, "trmean", b=2)).all()
          and not SRA_DIAG[-1]["fallback"])
    Un = Ub.clone(); Un[1, 4] = float("nan"); Un[10, 2] = float("inf"); Un[11] = float("-inf")
    rep = np.zeros(n, bool); rep[:3] = True
    SRA_DIAG.clear(); on = agg_sra(Un, rep, "mkrum", b=2)
    check("NaN row in W and inf rows in H dropped, output finite, |W| counts finite rows only",
          torch.isfinite(on).all() and SRA_DIAG[-1]["nW"] == 2)
    Uf = Ub.clone(); Uf[:2, 0] += 0.5; Uf[2:5, 0] -= 0.3                   # 2 witnesses + 3 RR false positives
    rep = np.zeros(n, bool); rep[:5] = True
    aH, _ = parts(Uf, rep); o_fp = agg_sra(Uf, rep, "cwmed", lam=INF)
    check("RR false positives outnumber witnesses in W -> signal suppressed (the formula's mechanism)",
          float(o_fp[0]) < float(aH[0]) + 0.01, f"({float(aH[0]):.3f} -> {float(o_fp[0]):.3f})")
    Uf2 = Ub.clone(); Uf2[:4, 0] += 0.5; Uf2[4:7, 0] -= 0.3; rep = np.zeros(n, bool); rep[:7] = True
    aH, _ = parts(Uf2, rep); o_fp2 = agg_sra(Uf2, rep, "cwmed", lam=INF)
    check("4 witnesses vs 3 false positives -> witness side wins", float(o_fp2[0]) > float(aH[0]) + 0.02)
    Ul = Ub.clone(); Ul[:3] += 1e3; rep = np.zeros(n, bool); rep[:3] = True
    aH, tau = parts(Ul, rep); SRA_DIAG.clear(); ol = agg_sra(Ul, rep, "cwmed", lam=LAMBDA_W)
    check("honest but far witnesses: clip binds, bound holds", SRA_DIAG[-1]["hit"] and
          float(torch.norm(ol - aH)) <= 3 / n * LAMBDA_W * tau * (1 + 1e-4))
    Um = Ub.clone(); Um[:3, 0] += 0.2; rep = np.zeros(n, bool); rep[:3] = True
    aH, _ = parts(Um, rep)
    check("lambda=inf: out == a_H + (|W|/N)(median_W - a_H)",
          torch.allclose(agg_sra(Um, rep, "cwmed", lam=INF), aH + 3 / n * (agg_cwmed(Um[:3]) - aH), atol=1e-6))
    Uz = Ub.clone(); Uz[:3] += 0.8; rep3 = np.zeros(n, bool); rep3[:3] = True
    aHz, _ = parts(Uz, rep3)
    mv = [float(torch.norm(agg_sra(Uz, rep3, "cwmed", lam=l) - aHz)) for l in (1.0, LAMBDA_W, LAMBDA_W_DIAG, INF)]
    check("SRA step size non-decreasing in lambda (1, 3, 10, inf)", all(a <= b + 1e-6 for a, b in zip(mv, mv[1:])), f"({np.round(mv, 4)})")
    for base_ in ["cclip", "nnm_cwmed", "geomed", "bucket_cwmed", "fedavg"]:
        check(f"SRA wraps {base_} without crashing",
              agg_sra(Ub, rep, base_, gen=torch.Generator().manual_seed(1)).shape == (P,))
    SRA_DIAG.clear()
    check("aggregate_round routes to SRA when sra_lam is set", torch.allclose(
        aggregate_round(Um, "trmean", 2, None, None, rep, 1.0, None, sra_lam=INF), agg_sra(Um, rep, "trmean", b=2, lam=INF)))
    check("aggregate_round without sra_lam still routes to WAA (mit-1.0 unchanged)", torch.allclose(
        aggregate_round(Um, "trmean", 2, None, None, rep, INF, None), agg_waa(Um, rep, "trmean", b=2, lam=INF)))
    check("ARMS2 table well-formed", all((w is None or w in ("oracle", "rand", *RR_EPS)) and m in (None, "waa", "elect", "sra")
                                         and (m not in ("waa", "sra") or l is not None) for w, l, m in ARMS2.values()))

    sub("TS2 ALIE and reports")
    U = torch.randn(8, 5, generator=g); m = np.array([0, 1, 0, 0, 1, 0, 0, 0], bool); mt = torch.as_tensor(m)
    A = alie(U, m, z=1.0); Hn = U[~mt]
    check("ALIE rows == mu - z*sigma (population sd), honest untouched",
          torch.allclose(A[1], Hn.mean(0) - Hn.std(0, correction=0)) and torch.allclose(A[4], A[1])
          and torch.equal(A[~mt], U[~mt]))
    check("ALIE z plumbed", torch.allclose(alie(U, m, z=2.5)[1], Hn.mean(0) - 2.5 * Hn.std(0, correction=0)))
    check("ALIE: no attackers / all attackers -> unchanged", torch.equal(alie(U, np.zeros(8, bool)), U)
          and torch.equal(alie(U, np.ones(8, bool)), U))
    m1 = np.ones(8, bool); m1[0] = False
    check("ALIE with ONE honest row -> sigma 0, finite", torch.allclose(alie(U, m1)[3], U[0]))
    roles = np.array(["W"] * 3 + ["A"] * 2 + ["H"] * 15, dtype=object)
    check("make_report2 claim: attackers in W", list(np.where(make_report2("oracle", roles, np.random.default_rng(0)))[0]) == [0, 1, 2, 3, 4])
    check("make_report2 no-claim: attackers out of W", list(np.where(make_report2("oracle", roles, np.random.default_rng(0), False))[0]) == [0, 1, 2])
    R = np.stack([make_report2("rr3", roles, np.random.default_rng(s), False) for s in range(500)])
    check("make_report2 rr3 no-claim: attackers never report", not R[:, 3:5].any())
    check("make_report2 base -> None", make_report2("base", roles, np.random.default_rng(0)) is None)

    sub("TS3 decision logic on messy inputs")
    check("RR formula: eps=3 f=0 -> 1, eps=3 f=2 -> 3, eps=1 f=0 -> 6 (handoff numbers)",
          (rr_predicted_kstar(3, 0), rr_predicted_kstar(3, 2), rr_predicted_kstar(1, 0)) == (1, 3, 6),
          f"({rr_predicted_kstar(3, 0)}, {rr_predicted_kstar(3, 2)}, {rr_predicted_kstar(1, 0)})")
    check("RR formula: eps=1 f=4 -> 9 (beyond grid), eps=inf f=2 -> 3 (= oracle floor)",
          rr_predicted_kstar(1, 4) == 9 and rr_predicted_kstar(INF, 2) == 3)
    ks_e = [rr_predicted_kstar(e, 2) or 99 for e in (0.1, 0.5, 1, 2, 3, 5)]
    ks_f = [rr_predicted_kstar(1, f) or 99 for f in (0, 1, 2, 3, 4)]
    check("RR formula non-increasing in eps, non-decreasing in f", all(a >= b for a, b in zip(ks_e, ks_e[1:]))
          and all(a <= b for a, b in zip(ks_f, ks_f[1:])), f"({ks_e}, {ks_f})")
    check("RR formula eps=0 -> None or large (p = 1/2: bit is noise)", (rr_predicted_kstar(0.0, 0) or 99) >= 10)
    G = [1, 2, 3, 4, 6, 8]
    check("rr_match: measured 6 vs pred 5 (true k* in (4,6]) -> match", rr_match(6, 5, G) is True)
    check("rr_match: measured 8 vs pred 6 -> match (7 is common)", rr_match(8, 6, G) is True)
    check("rr_match: measured 8 vs pred 4 -> miss at tol 1, hit at tol 2... (miss)", rr_match(8, 4, G) is False and rr_match(8, 4, G, 2) is False)
    check("rr_match: measured 8 vs pred 5 -> miss tol 1, hit tol 2", rr_match(8, 5, G) is False and rr_match(8, 5, G, 2) is True)
    check("rr_match: never vs pred 9 (> kmax) -> match; never vs pred 3 -> miss",
          rr_match("never", 9, G) is True and rr_match("never", 3, G) is False)
    check("rr_match: never vs pred None -> match; 1 vs None -> miss", rr_match("never", None, G) is True and rr_match(1, None, G) is False)
    check("rr_match: NaN / None measured -> None", rr_match(float("nan"), 3, G) is None and rr_match(None, 3, G) is None)
    check("rr_match: measured 1 vs pred 1 -> match; measured 3 (true k* = 3) vs pred 1 -> miss tol 1, hit tol 2",
          rr_match(1, 1, G) is True and rr_match(3, 1, G) is False and rr_match(3, 1, G, 2) is True)
    check("RR verdict holds / rough / fails / insufficient",
          rr_formula_verdict([(True, True), (True, True), (False, True)]) == "FORMULA_HOLDS"
          and rr_formula_verdict([(False, True), (False, True), (True, True)]).startswith("FORMULA_ROUGH")
          and rr_formula_verdict([(False, False), (False, False), (True, True)]).startswith("FORMULA_FAILS")
          and rr_formula_verdict([(None, None)]) == "INSUFFICIENT")
    check("floor reach: [(1,0),(3,2),(5,4)] -> REACHES", floor_reach_verdict([(1, 0), (3, 2), (5, 4)])[0] == "REACHES_FLOOR")
    check("floor reach: k* = f+2 everywhere -> ABOVE", floor_reach_verdict([(2, 0), (4, 2), (6, 4)])[0] == "ABOVE_FLOOR")
    check("floor reach: 2/3 rule, None skipped", floor_reach_verdict([(1, 0), (3, 2), (9, 4), (None, 2)])[0] == "REACHES_FLOOR")
    check("floor reach: empty -> INSUFFICIENT", floor_reach_verdict([(None, 0)])[0] == "INSUFFICIENT")
    S = lambda fpr, oth: {"benign_fpr": fpr, "other_mean": oth}
    check("paired: both fine -> HOLDS", m4_paired_verdict(S(.01, .95), S(.02, .93)) == "HOLDS")
    check("paired: arm breaks FPR where base held -> BREAKS", m4_paired_verdict(S(.01, .95), S(.20, .95)) == "BREAKS")
    check("paired: base itself broken, arm no worse -> HOLDS", m4_paired_verdict(S(.52, .07), S(.55, .05)) == "HOLDS")
    check("paired: base broken, arm much worse -> BREAKS", m4_paired_verdict(S(.30, .40), S(.90, .40)) == "BREAKS")
    check("paired: within tol but crosses FPR_MAX where base met it -> BREAKS", m4_paired_verdict(S(.03, .95), S(.06, .95)) == "BREAKS")
    check("paired: collateral drop > tol -> BREAKS", m4_paired_verdict(S(.01, .95), S(.01, .89)) == "BREAKS")
    check("paired: arm better than base -> HOLDS", m4_paired_verdict(S(.40, .30), S(.01, .95)) == "HOLDS")
    check("paired: NaN -> NA", m4_paired_verdict(S(float("nan"), .9), S(.01, .9)) == "NA")
    check("headline TIGHT_FIX", headline_m2("REMOVES_TAX", "REACHES_FLOOR", ["HOLDS", "HOLDS"]) == "TIGHT_FIX")
    check("headline PARTIAL", headline_m2("REDUCES_TAX", "ABOVE_FLOOR", ["HOLDS", "NA"]) == "PARTIAL")
    check("headline one BREAKS -> NO_SAFE_POINT", headline_m2("REMOVES_TAX", "REACHES_FLOOR", ["HOLDS", "BREAKS"]) == "NO_SAFE_POINT_CONFIRMED")
    check("headline HARM never PARTIAL", headline_m2("REDUCES_TAX+HARM", "ABOVE_FLOOR", ["HOLDS"]) == "NO_SAFE_POINT_CONFIRMED")
    check("headline no M4 -> UNTESTED", headline_m2("REMOVES_TAX", "REACHES_FLOOR", ["NA"]).startswith("UNTESTED"))
    check("dataset headline = weakest target", dataset_headline(["TIGHT_FIX", "PARTIAL"]) == "PARTIAL"
          and dataset_headline(["UNTESTED (x)"]) == "UNTESTED")

    sub("TS4 end-to-end on MESSY synthetic data (heavy tails, label noise, constant + duplicate column, real proportions)")
    r3 = np.random.default_rng(11); d0, Cc = 12, 4; mus = r3.normal(0, 2.5, (Cc, d0))
    def make(nrow, p):
        y = r3.choice(Cc, nrow, p=p)
        X = mus[y] + r3.standard_t(3, (nrow, d0)) * 1.3                     # heavy-tailed noise
        X = np.c_[X, np.full(nrow, 7.0), X[:, 0]]                            # constant + duplicated column
        return X, y
    Xtr, ytr = make(40000, [.62, .2, .15, .03]); Xte, yte = make(4000, [.4, .2, .2, .2])
    flip = r3.random(len(ytr)) < 0.03; ytr_n = ytr.copy(); ytr_n[flip] = r3.choice(Cc, int(flip.sum()))   # 3% label noise
    Xtr, Xte = fit_transform_numeric(Xtr, Xte)
    T = lambda a, dt=torch.float32: torch.tensor(a, dtype=dt, device=DEV)
    Xt, yt, Xe, ye = T(Xtr), T(ytr_n, torch.long), T(Xte), T(yte, torch.long)
    def go(agg, k, f, arm, attack="mimic", lam=None, eps=INF, rounds=25):
        cl, ro, _ = build_witness_partition(ytr_n, 3, k, f, 20, 500, 3000, 0.5, np.random.default_rng(0))
        who, l0, mode = ARMS2[arm]; l0 = lam if lam is not None else l0
        rep = None if who is None else make_report2(who, ro, np.random.default_rng(5), not attack.endswith("_nc"))
        SRA_DIAG.clear()
        s = summarise_hist(run_federated(Xt, yt, Xe, ye, cl, ro, agg, Cc, 0, eps=eps, rounds=rounds,
                                         lr=0.5 if np.isfinite(eps) else 0.3, clip=5.0, report=rep, attack=attack,
                                         waa_lam=l0 if mode == "waa" else 1.0, elect_cls=3 if mode == "elect" else None,
                                         sra_lam=l0 if mode == "sra" else None))
        st = {"benign_fpr": 1 - s["rec_0"], "other_mean": float(np.mean([s["rec_1"], s["rec_2"]]))}
        rr = [x["ratio"] for x in SRA_DIAG if np.isfinite(x["ratio"])]
        hr = float(np.mean([x["hit"] for x in SRA_DIAG])) if SRA_DIAG else float("nan")
        print(f"      {agg:7s} k={k} f={f} {arm:8s} lam={l0} {attack:11s} eps={eps}: target {s['rec_3']:.3f} | "
              f"other {st['other_mean']:.3f} | FPR {st['benign_fpr']:.3f} | ratio {np.median(rr) if rr else float('nan'):.1f} clip-hit {hr:.2f}")
        return s, st
    s_b, _ = go("cwmed", 2, 0, "base")
    check("precondition: cwmed k=2 base suppressed", s_b["rec_3"] < 0.3)
    s_i, _ = go("cwmed", 2, 0, "sra", lam=INF); s_it, _ = go("trmean", 2, 0, "sra", lam=INF)
    s_o, _ = go("cwmed", 2, 0, "orcinf"); s_f2, _ = go("fedavg", 2, 0, "base"); s_bt, _ = go("trmean", 2, 0, "base")
    check("SRA(lambda=inf, k=2) == mit-1.0 orcinf (median of 2 = mean): identical target recall",
          abs(s_i["rec_3"] - s_o["rec_3"]) < 0.02, f"({s_i['rec_3']:.3f} vs {s_o['rec_3']:.3f})")
    check("SRA(lambda=inf) k=2 lifts target above base (cwmed, trmean) and to within 0.15 of FedAvg k=2",
          s_i["rec_3"] > s_b["rec_3"] + 0.1 and s_it["rec_3"] > s_bt["rec_3"] + 0.1 and s_i["rec_3"] >= s_f2["rec_3"] - 0.15,
          f"(fedavg {s_f2['rec_3']:.3f})")
    s_3, _ = go("cwmed", 2, 0, "sra"); s_3m, _ = go("mkrum", 2, 0, "sra")
    print(f"      (outcome, not asserted: pre-registered lambda={LAMBDA_W}: cwmed {s_3['rec_3']:.3f}, mkrum {s_3m['rec_3']:.3f};"
          " synthetic witness/tau ratios are not the real 1.4-1.9)")
    check(f"SRA lambda={LAMBDA_W} is never worse than base at k=2", s_3["rec_3"] >= s_b["rec_3"] - 0.05)
    s_10, _ = go("cwmed", 2, 0, "sra_l10"); hit10 = float(np.mean([x["hit"] for x in SRA_DIAG])) if SRA_DIAG else 1.0
    check("sra_l10 arm: lambda=10 reaches the aggregator (no clip here -> identical to lambda=inf)",
          hit10 == 0.0 and abs(s_10["rec_3"] - s_i["rec_3"]) < 0.02, f"(l10 {s_10['rec_3']:.3f}, inf {s_i['rec_3']:.3f}, hit {hit10:.2f})")
    check("coverage ordered in lambda: lambda=3 <= lambda=10 (+0.02)", s_3["rec_3"] <= s_10["rec_3"] + 0.02)
    s_f, _ = go("cwmed", 2, 3, "sra", lam=INF); s_f3, _ = go("cwmed", 2, 3, "sra")
    check("SRA respects the floor: k=2 <= f=3 mimics claiming -> suppressed (lambda inf and 3)", s_f["rec_3"] < 0.3 and s_f3["rec_3"] < 0.3)
    s_6, _ = go("cwmed", 6, 2, "sra", lam=INF)
    check("SRA (lambda=inf) k=6 > f=2 mimics -> learns", s_6["rec_3"] > 0.6)
    _, cl6 = go("fedavg", 6, 0, "base")
    for att in ["signflip", "alie", "signflip_nc", "alie_nc"]:
        u = att.replace("_nc", "")
        _, fa = go("fedavg", 6, 2, "base", attack=u); _, ba = go("cwmed", 6, 2, "base", attack=u)
        _, sa = go("cwmed", 6, 2, "sra", attack=att)
        pv = m4_paired_verdict(ba, sa); av = m2_verdict(fa, sa, cl6)
        check(f"SRA + {att} (k=6 > f=2): PAIRED verdict HOLDS", pv == "HOLDS", f"(absolute: {av})")
    _, bl = go("cwmed", 2, 4, "base", attack="signflip"); _, sl = go("cwmed", 2, 4, "sra", attack="signflip")
    print(f"      (outcome, not asserted: liar-majority W k=2 f=4 sign-flip: base FPR {bl['benign_fpr']:.3f} vs sra "
          f"{sl['benign_fpr']:.3f}; paired {m4_paired_verdict(bl, sl)})")
    s_r3, _ = go("cwmed", 2, 0, "sra_rr3"); s_rd, _ = go("cwmed", 2, 0, "sra_rand")
    print(f"      (outcomes, not asserted: sra_rr3 k=2 {s_r3['rec_3']:.3f} | sra_rand k=2 {s_rd['rec_3']:.3f})")
    if HAVE_OPACUS:
        s_dp, _ = go("cwmed", 6, 0, "sra", eps=3.0, rounds=15)
        check("DP (eps=3) + SRA runs, finite outputs", np.isfinite(s_dp["rec_3"]) and np.isfinite(s_dp["rec_0"]))
    print(f"\n  PHASE 0-S RESULT: {'ALL PASSED' if not fails else f'{len(fails)} FAILED -> {fails}'}")
    return not fails

# -----------------------------------------------------------------------------
#  RUNNER
# -----------------------------------------------------------------------------
def cfg_id_m2(cal):
    s = json.dumps({"v": VERSION, "cal": {k: cal[k] for k in ("lr", "rounds") if k in cal},
                    "dp": [cal.get("dp_clip"), cal.get("dp_lr")], "M": M_TARGET, "NBG": N_BG, "N": N_CLIENTS,
                    "B": BATCH, "LS": LOCAL_STEPS, "att": ATTEMPTED_POLICY, "T": BG_TEMPER, "SF": SIGNFLIP_SCALE,
                    "RR": RR_EPS, "LW": LAMBDA_W, "Z": ALIE_Z}, sort_keys=True)
    return hashlib.md5(s.encode()).hexdigest()[:8]

def run_one_m2(c, Xt, yt, Xe, ye, D, cal):
    ti = CLASSES.index(c["target"]); C = len(CLASSES)
    rng = np.random.default_rng(1000 * c["seed"] + 17 * c["k"] + c["f"])          # same partitions as v3.2 / mit-1.0
    cl, roles, m_eff = build_witness_partition(D["ytr"], ti, c["k"], c["f"], N_CLIENTS, M_TARGET, N_BG, BG_TEMPER,
                                               rng, bg_counts=D["bg_counts"])
    who, lam, mode = ARMS2[c["arm"]]
    claims = not str(c["attack"]).endswith("_nc")
    rep = None if who is None else make_report2(who, roles, np.random.default_rng(7919 * c["seed"] + 31 * c["k"] + c["f"] + 1), claims)
    dp = np.isfinite(float(c["eps"])); R = int(cal["rounds"])
    WAA_DIAG.clear(); SRA_DIAG.clear()
    h = run_federated(Xt, yt, Xe, ye, cl, roles, c["agg"], C, c["seed"], eps=float(c["eps"]), rounds=R,
                      lr=cal["dp_lr"] if dp else cal["lr"], clip=cal.get("dp_clip", 1.0), fhat=F_HAT, report=rep,
                      attack=c["attack"], waa_lam=lam if mode == "waa" else 1.0,
                      elect_cls=ti if mode == "elect" else None, sra_lam=lam if mode == "sra" else None)
    s = summarise_hist(h)
    other = [s[f"rec_{j}"] for j in range(1, C) if j != ti and np.isfinite(s[f"rec_{j}"])]
    r = np.asarray(roles)
    inW = rep if rep is not None else np.zeros(len(r), bool)
    fin = [x for x in SRA_DIAG if not x["fallback"]]
    rat = [x["ratio"] for x in fin if np.isfinite(x["ratio"])]
    return {**c, "m_eff": m_eff, "target_recall": s[f"rec_{ti}"], "target_to_normal": float(s["M"][ti, 0]),
            "benign_fpr": 1 - s["rec_0"],
            "other_attack_recall_mean": float(np.mean(other)) if other else float("nan"),
            "other_attack_recall_min": float(np.min(other)) if other else float("nan"),
            "nW": int(inW.sum()), "nW_witness": int((inW & (r == "W")).sum()),
            "nW_honest_nonwitness": int((inW & (r == "H")).sum()), "nW_liar": int((inW & (r == "A")).sum()),
            "sra_clip_hit_rate": float(np.mean([x["hit"] for x in fin])) if fin else float("nan"),
            "sra_ratio_median": float(np.median(rat)) if rat else float("nan"),
            "sra_fallback_rate": float(np.mean([x["fallback"] for x in SRA_DIAG])) if SRA_DIAG else float("nan"),
            "witness_dist_over_tau": float(np.median(WAA_DIAG)) if WAA_DIAG else float("nan"),
            **{f"recall_{CLASSES[j]}": s[f"rec_{j}"] for j in range(C)}}

def exp_grid_m2(name, configs, csv, Xt, yt, Xe, ye, D, cal):
    cid = cfg_id_m2(cal)
    norm = lambda c: tuple(str(c[k]) for k in KEY_COLS_M2)
    done = pd.read_csv(csv) if os.path.exists(csv) else pd.DataFrame()
    keys = set()
    if len(done) and "cfg_id" in done:
        dd = done[done.cfg_id.astype(str) == cid]
        keys = set(tuple(r) for r in dd[KEY_COLS_M2].astype(str).values)
    todo = [c for c in configs if norm(c) not in keys]
    print(f"  {name}: {len(configs)} configs, {len(configs)-len(todo)} done (cfg {cid}), {len(todo)} to run")
    t0 = time.time()
    for i, c in enumerate(todo, 1):
        if out_of_time():
            STOPPED["flag"] = True
            print(f"  [TIME BUDGET] {TIME_BUDGET_H} h reached: {i-1}/{len(todo)} done. Save this version, attach its"
                  f" output as an input, re-run -> resumes here."); break
        row = {**run_one_m2(c, Xt, yt, Xe, ye, D, cal), "cfg_id": cid}
        append_row(csv, row)
        if i in (1, 2) or i % 10 == 0 or i == len(todo):
            el = time.time() - t0
            print(f"    [{i}/{len(todo)}] {el/60:.1f} min, ETA {el/i*(len(todo)-i)/60:.1f} min | {c['exp']} {c['agg']} "
                  f"{c['arm']} k={c['k']} f={c['f']} {c['attack']} {eps_name(float(c['eps']))} -> tgt {row['target_recall']:.3f}",
                  flush=True)
    out = pd.read_csv(csv); out = out[out.cfg_id.astype(str) == cid].copy()
    have = set(tuple(r) for r in out[KEY_COLS_M2].astype(str).values)
    complete = all(norm(c) in have for c in configs)
    if not complete: print(f"  {name}: INCOMPLETE -> report skipped until resumed")
    return out, complete

def cfg2(exp, target, k, f, agg, arm="base", attack="mimic", eps=INF, seed=0):
    return dict(exp=exp, target=target, k=k, f=f, agg=agg, arm=arm, attack=attack, eps=float(eps), seed=seed)

def plan_m3(target):
    c = [cfg2("M3", target, k, f, a, arm=arm, seed=s) for f in F_M3 for k in K_M3 for s in SEEDS_M
         for a in AGGS_M3 for arm in ARMS_M3]
    return c + [cfg2("M3", target, k, f, "fedavg", seed=s) for f in F_M3 for k in K_M3 for s in SEEDS_M]

def plan_m4(target):
    c = [cfg2("M4", target, k, 0, "fedavg", seed=s) for k in sorted({k for k, _ in M4_CELLS}) for s in SEEDS_M]
    for k, f in M4_CELLS:
        for a in ATTACKS_M4:
            c += [cfg2("M4", target, k, f, "fedavg", attack=a, seed=s) for s in SEEDS_M]
            c += [cfg2("M4", target, k, f, g, attack=a, seed=s) for g in AGGS_M4 for s in SEEDS_M]
            c += [cfg2("M4", target, k, f, g, arm=arm, attack=att, seed=s) for g in AGGS_M4 for arm in CLAIM_ARMS_M4
                  for att in (a, a + "_nc") for s in SEEDS_M]
    return c

def plan_m5(target):
    c = [cfg2("M5", target, REF_K, 0, "fedavg", eps=EPS_M5, seed=s) for s in SEEDS_M]                  # DP reference
    c += [cfg2("M5", target, k, 0, "fedavg", eps=EPS_M5, seed=s) for k in K_M5 for s in SEEDS_M]
    return c + [cfg2("M5", target, k, 0, a, arm=arm, eps=EPS_M5, seed=s) for k in K_M5 for a in AGGS_M5
                for arm in ARMS_M5 for s in SEEDS_M]

# -----------------------------------------------------------------------------
#  REPORTS
# -----------------------------------------------------------------------------
SUMMARY = []
def emit(title, txt):
    print(f"\n  {title}\n" + "\n".join("    " + l for l in str(txt).splitlines()))
    SUMMARY.append(f"\n## {title}\n```\n{txt}\n```\n")

def ks_from(df, col, ref, kmax):
    m = df.groupby("k")[col].mean()
    return estimate_kstar(m.index.values, m.values, ref) if len(m) else None

def m3_cells(d, ref, arms, aggs, fs, kmax):
    rows, cells = [], []
    for f in fs:
        fa = ks_from(d[(d["agg"] == "fedavg") & (d.arm == "base") & (d.f == f)], "target_recall", ref, kmax)
        fa_k = k_num(fa, kmax)
        rtax = lambda ks_: None if (k_num(ks_, kmax) is None or fa_k is None) else max(0, k_num(ks_, kmax) - fa_k)
        rows.append({"f": f, "agg": "fedavg", **{a: (f"{fa} (floor {f+1})" if a == "base" else "") for a in arms}})
        for agg in aggs:
            ks = {a: ks_from(d[(d["agg"] == agg) & (d.arm == a) & (d.f == f)], "target_recall", ref, kmax) for a in arms}
            rows.append({"f": f, "agg": agg, **{a: f"{ks[a]} (tax {rtax(ks[a])})" for a in arms}})
            cells.append({"f": f, "agg": agg, "fedavg_k": fa_k, "base_tax": rtax(ks.get("base")),
                          **{f"{a}_tax": rtax(ks.get(a)) for a in arms}, **{f"{a}_k": k_num(ks.get(a), kmax) for a in arms},
                          **{f"{a}_raw": ks.get(a) for a in arms}})
    return rows, cells

def report_M3(d, ref, target):
    banner(f"M3 RESULTS -- split robust aggregation, coverage -- {target}")
    kmax = max(K_M3)
    rows, cells = m3_cells(d, ref, ARMS_M3, AGGS_M3, F_M3, kmax)
    emit(f"{target} | M3 k* by arm (robustness tax = k*(arm) - k*(FedAvg, same f)); grid k={K_M3}, 'never' = > {kmax}",
         pd.DataFrame(rows).to_string(index=False))
    piv = d.groupby(["f", "agg", "arm", "k"]).target_recall.mean().unstack("k").round(2)
    emit(f"{target} | M3 full breakdown: mean target recall by (f, agg, arm) x k  (learnable line {LEARNABLE_FRAC*ref:.3f})",
         piv.to_string())
    view = lambda a, r="sra_rand": [{"base_tax": x["base_tax"], "oracle_tax": x.get(f"{a}_tax"), "rand_tax": x.get(f"{r}_tax")}
                                     for x in cells]
    v_cov = {a: m1_verdict(view(a)) for a in ARMS_M3 if a != "base"}
    reach, share = floor_reach_verdict([(x.get("sra_k"), x["f"]) for x in cells]) if "sra" in ARMS_M3 else ("not run", float("nan"))
    reach10, share10 = floor_reach_verdict([(x.get("sra_l10_k"), x["f"]) for x in cells]) if "sra_l10" in ARMS_M3 else ("not run", float("nan"))
    if "sra_l10" in ARMS_M3:
        lam_diag = ("LAMBDA_BINDS (lambda=3 costs coverage; lambda=10 better by >= 2 in >= 2/3 of cells)"
                    if np.mean([(x.get("sra_k") or 99) - (x.get("sra_l10_k") or 99) >= TAX_GAIN for x in cells] or [0]) >= CELL_MAJ - 1e-9
                    else "LAMBDA_NOT_THE_ISSUE (lambda=10 does not beat lambda=3 by >= 2 in >= 2/3 of cells)")
    else:
        lam_diag = "not run"
    vid = identity_verdict(view("sra")) if {"sra", "sra_rand"} <= set(ARMS_M3) else "not run"
    rr_rows, rr_v = [], {}
    for arm in [a for a in ("sra_rr1", "sra_rr3") if a in ARMS_M3]:
        eps = RR_EPS[arm.replace("sra_", "")]; items = []
        for x in cells:
            pr = rr_predicted_kstar(eps, x["f"]); meas = x.get(f"{arm}_raw")
            m1, m2 = rr_match(meas, pr, K_M3, 1), rr_match(meas, pr, K_M3, 2); items.append((m1, m2))
            rr_rows.append({"arm": arm, "eps_w": eps, "f": x["f"], "agg": x["agg"], "predicted k*": pr if pr else "never",
                            "measured k*": meas, "sra (oracle) k*": x.get("sra_raw"), "within 1": m1, "within 2": m2})
        rr_v[arm] = rr_formula_verdict(items)
    if rr_rows: emit(f"{target} | M3 RR formula k*: smallest k with k p > (N-k-f)(1-p) + f   (grid-censored comparison)",
                     pd.DataFrame(rr_rows).to_string(index=False))
    ff = [dict(arm=a, **z) for a in ("sra", "orcinf", "elect") if a in ARMS_M3
          for z in floor_flags([{"oracle_k": x.get(f"{a}_k"), "f": x["f"], "agg": x["agg"]} for x in cells])]
    worst = max(cells, key=lambda x: -1 if x.get("sra_tax") is None else x["sra_tax"]) if cells else None
    comp = d[d.arm != "base"].groupby(["arm", "f"])[["nW", "nW_witness", "nW_honest_nonwitness", "nW_liar",
                                                     "sra_clip_hit_rate", "sra_ratio_median", "sra_fallback_rate"]].mean().round(2)
    emit(f"{target} | M3 W-stratum composition + clip diagnostics (means over k, seeds)", comp.to_string())
    kc = 6 if 6 in K_M3 else kmax
    col = d[(d.f == 0) & (d.k == kc)].groupby(["agg", "arm"])[
        ["benign_fpr", "other_attack_recall_mean", "other_attack_recall_min"] +
        [c for c in d.columns if c.startswith("recall_")]].mean().round(3)
    emit(f"{target} | M3 per-class recall at f=0, k={kc} (what else moves)", col.to_string())
    emit(f"{target} | M3 verdicts",
         f"COVERAGE (sra)        : {v_cov.get('sra')}\n"
         f"FLOOR (sra k* <= f+1) : {reach} (share {share:.2f})\n"
         f"IDENTITY (sra_rand)   : {vid}\n"
         f"-- post-hoc lambda diagnostic (NOT the headline) --\n"
         f"COVERAGE (sra_l10)    : {v_cov.get('sra_l10')}\n"
         f"FLOOR (sra_l10)       : {reach10} (share {share10:.2f})\n"
         f"LAMBDA DIAGNOSTIC     : {lam_diag}\n" +
         "".join(f"RR formula {a:8s}   : {v}\n" for a, v in rr_v.items()) +
         "".join(f"coverage {a:10s}   : {v}\n" for a, v in v_cov.items() if a not in ("sra", "sra_l10")) +
         f"floor violations      : {ff if ff else 'none'}\n" +
         (f"worst sra cell        : {worst['agg']} f={worst['f']} k*={worst.get('sra_raw')} tax={worst.get('sra_tax')}" if worst else ""))
    try:
        fig, axs = plt.subplots(len(F_M3), len(AGGS_M3), figsize=(3.2 * len(AGGS_M3), 2.6 * len(F_M3)), squeeze=False)
        for i, f in enumerate(F_M3):
            for j, agg in enumerate(AGGS_M3):
                ax = axs[i][j]
                for arm in ARMS_M3:
                    t = d[(d["agg"] == agg) & (d.arm == arm) & (d.f == f)].groupby("k").target_recall.mean()
                    ax.plot(t.index, t.values, "o-", ms=3, label=arm)
                t = d[(d["agg"] == "fedavg") & (d.f == f)].groupby("k").target_recall.mean()
                ax.plot(t.index, t.values, "k--", lw=1, label="fedavg")
                ax.axhline(LEARNABLE_FRAC * ref, color="grey", lw=0.6); ax.axvline(f + 1, color="red", lw=0.6)
                ax.set_title(f"{agg}, f={f}", fontsize=8); ax.set_ylim(-0.02, 1.02)
        axs[0][0].legend(fontsize=5); fig.suptitle(f"{DATASET} {target} -- M3 (red = floor f+1)", fontsize=9)
        fig.tight_layout(); fig.savefig(os.path.join(FIG_DIR, f"M3_coverage_{fname(target)}.pdf")); plt.close(fig)
    except Exception as e:
        print(f"  [WARN] M3 figure failed ({type(e).__name__})")
    return {"M3_coverage_sra": v_cov.get("sra"), "M3_floor": reach, "M3_identity": vid,
            "M3_coverage_sra_l10": v_cov.get("sra_l10"), "M3_floor_l10": reach10, "M3_lambda_diag": lam_diag,
            **{f"M3_rr_{a}": v for a, v in rr_v.items()}, **{f"M3_cov_{a}": v for a, v in v_cov.items() if a not in ("sra", "sra_l10")},
            "M3_floor_flags": len(ff)}

def report_M4(d, target):
    banner(f"M4 RESULTS -- robustness (PAIRED vs base rule under the same attack) -- {target}")
    stat = lambda g: {"benign_fpr": float(g.benign_fpr.mean()) if len(g) else float("nan"),
                      "other_mean": float(g.other_attack_recall_mean.mean()) if len(g) else float("nan"),
                      "other_min": float(g.other_attack_recall_min.mean()) if len(g) else float("nan")}
    rows, verdicts = [], []
    for k, f in M4_CELLS:
        clean = stat(d[(d["agg"] == "fedavg") & (d.f == 0) & (d.k == k)])
        for a in ATTACKS_M4:
            sel = (d.k == k) & (d.f == f)
            fed = stat(d[sel & (d["agg"] == "fedavg") & (d.attack == a)])
            eff = (fed["benign_fpr"] > FPR_MAX) or (clean["other_mean"] - fed["other_mean"] >= ATTACK_DROP)
            rows.append({"k": k, "f": f, "attack": a, "agg": "fedavg", "arm": "base", **{x: round(y, 3) for x, y in fed.items()},
                         "paired": "", "absolute": "effective" if eff else "attack too weak"})
            for g in AGGS_M4:
                base = stat(d[sel & (d["agg"] == g) & (d.arm == "base") & (d.attack == a)])
                rows.append({"k": k, "f": f, "attack": a, "agg": g, "arm": "base", **{x: round(y, 3) for x, y in base.items()},
                             "paired": "(reference)", "absolute": m2_verdict(fed, base, clean)})
                for arm in CLAIM_ARMS_M4:
                    for att in (a, a + "_nc"):
                        st = stat(d[sel & (d["agg"] == g) & (d.arm == arm) & (d.attack == att)])
                        pv = m4_paired_verdict(base, st); av = m2_verdict(fed, st, clean)
                        verdicts.append({"k": k, "f": f, "attack": att, "agg": g, "arm": arm, "paired": pv, "absolute": av})
                        rows.append({"k": k, "f": f, "attack": att, "agg": g, "arm": arm, **{x: round(y, 3) for x, y in st.items()},
                                     "paired": pv, "absolute": av})
    emit(f"{target} | M4 sign-flip x{SIGNFLIP_SCALE:g} / ALIE z={ALIE_Z:g}  ('_nc' = attackers do NOT claim evidence)",
         pd.DataFrame(rows).to_string(index=False))
    comp = d[d.arm.isin(["sra", "sra_l10"])].groupby(["arm", "k", "f", "attack"])[["nW", "nW_witness", "nW_liar", "sra_clip_hit_rate",
                                                             "sra_ratio_median"]].mean().round(2)
    emit(f"{target} | M4 SRA W-stratum composition + clip-hit rate", comp.to_string())
    per = d[d.exp == "M4"].groupby(["k", "f", "attack", "agg", "arm"])[[c for c in d.columns if c.startswith("recall_")]].mean().round(3)
    emit(f"{target} | M4 full per-class recall", per.to_string())
    V = pd.DataFrame(verdicts)
    if len(V):
        emit(f"{target} | M4 paired verdict counts (HOLDS / BREAKS) by arm and cell type",
             V.assign(cell=np.where(V.k > V.f, "k>f", "k<=f (bounded damage)")).groupby(["arm", "cell"]).paired
              .value_counts().unstack(fill_value=0).to_string())
    return verdicts

def report_M5(d, target):
    banner(f"M5 RESULTS -- DP interaction (eps={EPS_M5:g}, f=0) -- {target}")
    kmax = max(K_M5)
    ref_dp = float(d[(d["agg"] == "fedavg") & (d.k == REF_K)].target_recall.mean())
    dd = d[d.k != REF_K] if REF_K not in K_M5 else d
    piv = dd.groupby(["agg", "arm", "k"]).target_recall.mean().unstack("k").round(2)
    emit(f"{target} | M5 mean target recall under DP (DP reference FedAvg k={REF_K}: {ref_dp:.3f})", piv.to_string())
    if not (np.isfinite(ref_dp) and ref_dp >= REF_MIN):
        emit(f"{target} | M5 verdict", f"UNDEFINED (DP reference {ref_dp:.3f} < REF_MIN {REF_MIN}) -- report raw recalls")
        return {"M5_sra_under_dp": "UNDEFINED (DP reference too low)"}
    rows, cells = m3_cells(dd, ref_dp, ARMS_M5, AGGS_M5, [0], kmax)
    emit(f"{target} | M5 k* under DP (learnable line {LEARNABLE_FRAC}x DP reference = {LEARNABLE_FRAC*ref_dp:.3f})",
         pd.DataFrame(rows).to_string(index=False))
    v = m1_verdict([{"base_tax": x["base_tax"], "oracle_tax": x.get("sra_tax")} for x in cells])
    col = dd[dd.k == (6 if 6 in K_M5 else kmax)].groupby(["agg", "arm"])[["benign_fpr", "other_attack_recall_mean"] +
          [c for c in dd.columns if c.startswith("recall_")]].mean().round(3)
    emit(f"{target} | M5 per-class recall under DP", col.to_string())
    emit(f"{target} | M5 verdict", f"SRA under DP (tax vs FedAvg-DP): {v}")
    return {"M5_sra_under_dp": v}

def print_rules_m2():
    banner("PRE-REGISTERED RULES (mit-2.0) -- fixed before any run")
    print(f"    SRA: a = a_H + (|W|/N) clip_(lambda_W tau)(median_W - a_H), lambda_W = {LAMBDA_W} (fixed).  Attackers always claim in M3.")
    print(f"    learnable line = {LEARNABLE_FRAC} x reference (FedAvg, f=0, k={REF_K}, non-private).")
    print(f"    M3 robustness tax = k*(arm) - k*(FedAvg, same f).  REMOVES if every sra tax <= {TAX_TOL}; REDUCES if it falls by")
    print(f"       >= {TAX_GAIN} in >= {CELL_MAJ:.0%} of taxed cells.  REACHES_FLOOR if sra k* <= f+1 in >= {CELL_MAJ:.0%} of cells.")
    print(f"       IDENTITY_MATTERS if sra_rand is worse than sra by >= {TAX_GAIN} in >= {CELL_MAJ:.0%} of helped cells.")
    print(f"       RR: FORMULA_HOLDS if measured k* is within +-1 of the formula (grid-censored) in >= {CELL_MAJ:.0%} of cells;")
    print("       ROUGH if only within +-2; else FAILS (report the measured curve).")
    print(f"    M4 (primary, paired): HOLDS if FPR <= base FPR + {M4_TOL} and other-attack recall >= base - {M4_TOL} under the")
    print(f"       SAME attack, and FPR <= {FPR_MAX} wherever base keeps it.  Secondary: mit-1.0 absolute rule vs clean FedAvg.")
    print(f"    M5: learnable line from the DP reference (FedAvg, eps={EPS_M5:g}, k={REF_K}); SRA tax vs FedAvg-DP, mit-1.0 rule.")
    print("    HEADLINE per target: TIGHT_FIX if REACHES_FLOOR and every sra PAIRED verdict in k > f cells HOLDS;")
    print("       PARTIAL if coverage REMOVES/REDUCES (no HARM) and HOLDS; else NO_SAFE_POINT_CONFIRMED.")
    print("       Dataset headline = weakest target.  STOP RULE: last mitigation experiment -- consolidate and write.")
    print(f"    POST-HOC (added after synthetic tests, labelled so): sra_l10 = SRA with lambda_W = {LAMBDA_W_DIAG:g}. Same verdicts,")
    print("       reported as a SECONDARY headline.  LAMBDA_BINDS if sra_l10 k* beats sra k* by >= 2 in >= 2/3 of M3 cells.")

def claims_summary_m2(results):
    p = os.path.join(OUT_DIR, f"CLAIMS_SUMMARY_MIT2_{TAG}.md")
    head = [f"# mit-2 (SRA) summary -- {DATASET} (script {SCRIPT_VERSION})\n",
            f"DATASET HEADLINE: {dataset_headline([r.get('HEADLINE') for r in results.values()])}\n",
            f"secondary (POST-HOC lambda={LAMBDA_W_DIAG:g}): {dataset_headline([r.get('HEADLINE_l10_posthoc') for r in results.values()])}\n"]
    for t, r in results.items():
        head.append(f"\n## {t} | verdicts\n```\n" + "\n".join(f"{k}: {v}" for k, v in r.items() if k != "M4_list") + "\n```\n")
    open(p, "w").write("\n".join(head + SUMMARY))
    banner(f"mit-2 SUMMARY written: {p}")
    for t, r in results.items():
        print(f"  {t}: " + " | ".join(f"{k}={v}" for k, v in r.items() if k != "M4_list"))
    print(f"  DATASET HEADLINE ({DATASET}): {dataset_headline([r.get('HEADLINE') for r in results.values()])}")
    print(f"  secondary (POST-HOC lambda={LAMBDA_W_DIAG:g}): {dataset_headline([r.get('HEADLINE_l10_posthoc') for r in results.values()])}")

# -----------------------------------------------------------------------------
#  SESSION HELPERS + MAIN
# -----------------------------------------------------------------------------
MIT1_BASENAME = f"witness_mit1_{TAG}"

def import_previous_outputs():
    n = 0
    for h in [p for p in glob.glob(f"/kaggle/input/**/{OUT_BASENAME}", recursive=True) if os.path.isdir(p)]:
        for fpath in glob.glob(os.path.join(h, "*.csv")) + glob.glob(os.path.join(h, "*.json")):
            dst = os.path.join(OUT_DIR, os.path.basename(fpath))
            if not os.path.exists(dst): shutil.copy(fpath, dst); n += 1
    for base in (PREV_BASENAME, MIT1_BASENAME):          # v3.2 calibration first, mit-1.0 copy as fallback
        for h in [p for p in glob.glob(f"/kaggle/input/**/{base}", recursive=True) if os.path.isdir(p)]:
            for fpath in glob.glob(os.path.join(h, "calibration_*.json")):
                dst = os.path.join(OUT_DIR, os.path.basename(fpath))
                if not os.path.exists(dst): shutil.copy(fpath, dst); n += 1; print(f"  calibration imported: {fpath}")
    print(f"  imported {n} files from previous sessions / earlier outputs")

def main():
    banner(f"WITNESS mit-2 (SRA) {SCRIPT_VERSION} | {DATASET} | device={DEV} | out={OUT_DIR}")
    if DEV.type == "cpu": print("  [WARN] CPU run. Kaggle: Accelerator -> GPU.")
    import_previous_outputs()
    json.dump({k: v for k, v in globals().items() if k.isupper() and isinstance(v, (int, float, str, list, bool, dict))},
              open(os.path.join(OUT_DIR, "config_mit2.json"), "w"), indent=1, default=str)
    if os.environ.get("WITNESS_SMOKE") and os.environ.get("WITNESS_SKIP_P0"):     # developer smoke only, never on Kaggle
        ok0 = okm = oks = True; print("  [DEV] Phase 0 skipped (smoke)")
    else:
        ok0 = phase0_self_tests(); okm = phase0_mitigation_tests(); oks = phase0_sra_tests()
    if not (ok0 and okm and oks): print("\n  STOP: fix failing self-tests first."); return
    if ONLY_SELF_TEST: return
    run_m5 = RUN_M5 and HAVE_OPACUS
    if RUN_M5 and not HAVE_OPACUS: print("  [WARN] opacus missing -> M5 (DP) skipped. Turn Kaggle Internet ON.")
    D = load_data()
    elig, rep = select_targets(D["class_counts"], D["ytr"], D["yte"], CLASSES, M_TARGET, MIN_TEST, RARE_SHARE)
    print(rep.to_string(index=False))
    if not elig: print("  no eligible target -> stop"); return
    targets = [t for t in elig if t in RUN_TARGETS] if RUN_TARGETS else elig[:M_TARGETS_N]
    print(f"  eligible (rarest first): {elig} -> this session: {targets}")
    t0 = targets[0]
    print(f"  plan per target: REF {len(SEEDS_M)} | M3 {len(plan_m3(t0)) if RUN_M3 else 0} | M4 {len(plan_m4(t0)) if RUN_M4 else 0}"
          f" | M5 {len(plan_m5(t0)) if run_m5 else 0}")
    print_rules_m2()
    Xt, yt = torch.tensor(D["Xtr"], device=DEV), torch.tensor(D["ytr"], device=DEV, dtype=torch.long)
    Xe, ye = torch.tensor(D["Xte"], device=DEV), torch.tensor(D["yte"], device=DEV, dtype=torch.long)
    csv = os.path.join(OUT_DIR, "mit2_runs.csv"); results = {}
    for target in targets:
        if STOPPED["flag"]: break
        had_cal = os.path.exists(os.path.join(OUT_DIR, f"calibration_{fname(target)}_M{M_TARGET}.json"))
        cal = calibrate(Xt, yt, Xe, ye, D, target)
        if not had_cal: print("  [WARN] no v3.2 calibration attached -> recalibrated here. Attach the v3.2 output to reuse it.")
        pre = preflight_gate(cal["conv"], cal["ref_recall"], target, CLASSES)
        banner(f"PRE-FLIGHT GATE -- {'GO' if pre['GO'] else 'NO-GO'} ({DATASET}, {target})")
        for r in pre["reasons"]: print("    " + r)
        if not pre["GO"] and not FORCE_PAST_PREFLIGHT: continue
        print(f"  calibration: lr={cal['lr']} rounds R={cal['rounds']} dp_lr={cal.get('dp_lr')} dp_clip={cal.get('dp_clip')}")
        dR, okR = exp_grid_m2("REF", [cfg2("REF", target, REF_K, 0, "fedavg", seed=s) for s in SEEDS_M], csv, Xt, yt, Xe, ye, D, cal)
        if not okR: break
        ref = float(dR[(dR.exp == "REF") & (dR.target == target)].target_recall.mean())
        print(f"  reference (FedAvg, f=0, k={REF_K}): {ref:.3f} -> learnable line {LEARNABLE_FRAC*ref:.3f}")
        if not (np.isfinite(ref) and ref >= REF_MIN):
            print(f"  [STOP target] reference {ref:.3f} < REF_MIN {REF_MIN} -> no runs for {target}"); continue
        res = {}
        if RUN_M3 and not STOPPED["flag"]:
            banner(f"M3 -- SRA coverage -- {target}")
            d3, ok = exp_grid_m2("M3", plan_m3(target), csv, Xt, yt, Xe, ye, D, cal)
            if ok: res.update(report_M3(d3[(d3.exp == "M3") & (d3.target == target)], ref, target))
        if RUN_M4 and not STOPPED["flag"]:
            banner(f"M4 -- SRA robustness -- {target}")
            d4, ok = exp_grid_m2("M4", plan_m4(target), csv, Xt, yt, Xe, ye, D, cal)
            if ok:
                v4 = report_M4(d4[(d4.exp == "M4") & (d4.target == target)], target)
                res["M4_list"] = v4
                for arm in CLAIM_ARMS_M4:
                    vv = [x["paired"] for x in v4 if x["arm"] == arm and x["k"] > x["f"]]
                    res[f"M4_{arm}_k>f"] = f"{sum(v == 'HOLDS' for v in vv)}/{len(vv)} HOLDS (paired)"
                vb = [x["paired"] for x in v4 if x["arm"] == "sra" and x["k"] <= x["f"]]
                res["M4_sra_k<=f"] = f"{sum(v == 'HOLDS' for v in vb)}/{len(vb)} HOLDS (bounded-damage cell, not in headline)"
        if run_m5 and not STOPPED["flag"]:
            if cal.get("dp_lr") is None:
                print("  [WARN] calibration has no dp_lr/dp_clip -> M5 skipped (attach the v3.2 calibration)")
            else:
                banner(f"M5 -- SRA under DP -- {target}")
                d5, ok = exp_grid_m2("M5", plan_m5(target), csv, Xt, yt, Xe, ye, D, cal)
                if ok: res.update(report_M5(d5[(d5.exp == "M5") & (d5.target == target)], target))
        if "M3_coverage_sra" in res and "M4_list" in res:
            res["HEADLINE"] = headline_m2(res["M3_coverage_sra"], res["M3_floor"],
                                          [x["paired"] for x in res["M4_list"] if x["arm"] == "sra" and x["k"] > x["f"]])
            banner(f"HEADLINE (pre-registered, lambda_W={LAMBDA_W:g}) -- {target}: {res['HEADLINE']}")
            if "M3_coverage_sra_l10" in res and res["M3_coverage_sra_l10"] is not None:
                res["HEADLINE_l10_posthoc"] = headline_m2(res["M3_coverage_sra_l10"], res["M3_floor_l10"],
                    [x["paired"] for x in res["M4_list"] if x["arm"] == "sra_l10" and x["k"] > x["f"]])
                print(f"  secondary headline (POST-HOC, lambda_W={LAMBDA_W_DIAG:g}): {res['HEADLINE_l10_posthoc']}")
        results[target] = res
    try: claims_summary_m2(results)
    except Exception as e: print(f"  [WARN] summary failed ({type(e).__name__}: {e}) -- raw CSV intact")
    banner("STOPPED EARLY (time budget) -- resume next session" if STOPPED["flag"] else "DONE")
    print(f"  outputs: {OUT_DIR}")

if __name__ == "__main__":
    main()
