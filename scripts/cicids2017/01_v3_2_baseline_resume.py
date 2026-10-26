# Exported verbatim from notebooks/cicids2017/01_v3_2_baseline_resume.ipynb (single code cell). The notebook is the canonical source.
# =============================================================================
#  WITNESS-COUNT PHASE DIAGRAM  v3  --  CICIDS2017  --  standalone, Kaggle-ready
# =============================================================================
#  THE QUESTION
#    N organisations train one intrusion detector with federated learning.
#    A rare attack is seen by only k of them ("witnesses"); f members are
#    attackers who copy that traffic but label it Normal (perfect mimicry).
#    k* = smallest k at which the shared model detects the attack.
#    How do Byzantine-robust aggregation and DP move k*?
#
#  WHAT CHANGED IN v3
#    1. G1 FIX. A calibration curve counts as converged only if (a) its plateau
#       is reached by PLATEAU_FRAC_MAX x R_CAL and (b) its last 20% is flat
#       (rise vs the preceding 20% <= RISE_TOL).  v2 accepted a curve still
#       rising at round 140/150.  Curves are 3-point smoothed first so eval
#       noise does not fake a late plateau.  If a curve fails at R_CAL,
#       calibration retries at the next value of R_CAL_LIST.
#    2. G6 FLOOR GATE, run BEFORE any grid: at the calibrated reference
#       (FedAvg, f=0, k=max, non-private) benign FPR <= FPR_MAX, no non-target
#       class dead (recall < DEAD_RECALL), target recall >= REF_MIN.
#    3. Q-A (missed vs mislabelled). Every run logs where the target's test
#       flows go (share predicted as each class).  EXP-QA adds a BINARY-trained
#       model on the f = 0 grid with the same partitions and seeds (paired).
#    4. EXP-D (wall or delay). For each robust aggregator the grid cell just
#       below k* (f = 0) is re-run for LONG_MULT x rounds.
#    5. EXP-B reuses EXP-A's non-private runs (identical seeds and partitions).
#    6. D3 (cosine alignment) removed: uninformative in the pilot.
#    8. (v3.1) SOTA heterogeneity-aware aggregators added: cclip, nnm_cwmed.
#    9. (v3.1) EXP-D now covers EVERY tax cell (k < k*, f = 0), not only the cell below k*:
#       reports k*(R) vs k*(3R) and the "wall" region per aggregator.
#   10. (v3.1) EXP-K0: zero-witness control (k = 0).  If the target is detected with no
#       witnesses, detection comes from other attack classes, not from witnesses.
#   11. (v3.1) EXP-B report adds per-class recall under each privacy setting (DP collateral).
#    7. Session-friendly: TIME_BUDGET_H stops cleanly and the next session
#       resumes; RUN_TARGETS picks targets per session; outputs of a previous
#       session attached as a Kaggle input are imported automatically.
#
#  NUMBERS AND WHERE THEY COME FROM
#    eps grid : Ponomareva et al. (JAIR 2023): eps <= 1 strong, eps <= 10
#               reasonable.  inf = non-private, -1 = clip-only control.
#               Privacy unit = one flow record (state this in the paper).
#    delta    : 1e-5, below 1/n_i for every client (n_i ~ 3,500).
#    f / N    : 0, 5, 10, 20 %.  F_HAT = 2 (aggregators configured for 10%).
#    LEARNABLE: 0.8 x reference (four-fifths); 0.5 reported as sensitivity.
#    LR, ROUNDS, DP_LR, DP_CLIP : set by calibration (printed + saved).
#
#  WORKFLOW
#    QUICK = pilot, ends in pre-flight + post-EXP-A gates.   FULL = paper grade.
#    Kaggle: Accelerator = GPU, Internet = ON (pip install opacus).
#    Long FULL runs: set RUN_TARGETS to one target per session; when a session
#    hits TIME_BUDGET_H, save the version, add its output as an input to the
#    next session, and re-run -- finished configs are skipped.
# =============================================================================

import os, sys, glob, time, math, json, warnings, hashlib, subprocess, shutil, tempfile
import numpy as np
import pandas as pd
warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=FutureWarning)

# -----------------------------------------------------------------------------
# CONFIG
# -----------------------------------------------------------------------------
DATASET = "CICIDS2017"
VERSION = "v3"                # part of the resume key -- do NOT change (finished runs would be ignored)
SCRIPT_VERSION = "v3.2"       # display only
MODE = "FULL"                 # "QUICK" | "FULL"  (final v3.2 run = FULL)
RUN_TARGETS = None            # None = all eligible (up to N_TARGETS); or e.g. ["Botnet"]
RUN_EXP_A, RUN_EXP_QA, RUN_EXP_D, RUN_EXP_K0, RUN_EXP_B, RUN_EXP_C = True, True, True, True, True, True
FORCE_PAST_PREFLIGHT = False  # True = run grids even if G1/G6 fail (NOT for paper numbers)
ONLY_SELF_TEST = False
DATA_PATH = None              # None -> auto-resolve under /kaggle/input
TIME_BUDGET_H = 11.0          # Kaggle sessions stop at 12 h; stop cleanly before that

ATTEMPTED_POLICY = "drop"     # "Attempted" flows (Engelen et al. 2021) are dropped
DROP_PORTS = True             # ports are a known shortcut (Arp et al., USENIX Sec 2022)
MAX_MISSING_FRAC = 0.5

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
TAG = "cicids2017"
OUT_BASENAME = f"witness_{VERSION}_{TAG}"
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

def load_data(path=None):
    """CICIDS2017, corrected release (Engelen et al. 2021 / Liu et al. 2022)."""
    global CLASSES
    CLASSES = CIC_CLASSES
    banner("SECTION 1 -- LOAD + CLEAN CICIDS2017 (corrected release)")
    path = path or resolve_path(["monday.csv", "*Monday*.csv"]); print(f"  DATA_PATH -> {path}")
    files = sorted(f for f in glob.glob(os.path.join(path, "*.csv")) if "_plus" not in os.path.basename(f).lower())
    if not files: raise FileNotFoundError(f"no CSV files in {path}")
    dfs = []
    for fp in files:
        df = read_csv_any(fp); df["_source_file"] = os.path.basename(fp).lower()
        dfs.append(df); print(f"    {os.path.basename(fp):28s} rows={len(df):>9,}")
    df = pd.concat(dfs, ignore_index=True); del dfs
    lab_col = next((c for c in df.columns if c.lower() == "label"), None) or \
              next(c for c in df.columns if "label" in c.lower() and "attempt" not in c.lower())
    raw_counts = df[lab_col].astype(str).value_counts()
    maps = {r: map_label(r) for r in raw_counts.index}
    df["macro"] = df[lab_col].astype(str).map(maps)
    print_label_table(raw_counts.to_dict())
    feat_cols = [c for c in df.columns if c.lower() not in CIC_ID_COLS and c not in (lab_col, "macro")
                 and pd.api.types.is_numeric_dtype(df[c])]
    if DROP_PORTS: feat_cols = [c for c in feat_cols if "port" not in c.lower()]
    n0 = len(df)
    df = df[df["macro"].isin(CLASSES)].reset_index(drop=True)
    print(f"\n  rows removed (DROP / probe / unknown): {n0-len(df):,}")
    keep, rep = remove_conflicts_and_dups(df[feat_cols], df["macro"].to_numpy())
    print(f"  conflicting-label rows removed: {rep['conflicting_rows']:,}  by class: {rep['conflict_by_class']}")
    print(f"  exact duplicates removed: {rep['exact_duplicates']:,}")
    df = df[keep].reset_index(drop=True)
    y = df["macro"].map({c: i for i, c in enumerate(CLASSES)}).to_numpy().astype(int)
    days = df["_source_file"].to_numpy()
    class_counts = {c: int(np.sum(y == i)) for i, c in enumerate(CLASSES)}
    tr, te = stratified_split(y, CLASSES, np.random.default_rng(0))
    Xtr, Xte, ytr, yte, feats = finish_split(df.loc[tr, feat_cols].reset_index(drop=True),
                                             df.loc[te, feat_cols].reset_index(drop=True),
                                             y[tr], y[te], feat_cols)
    return dict(Xtr=Xtr, Xte=Xte, ytr=ytr, yte=yte, days_tr=days[tr], class_counts=class_counts,
                bg_counts=None, feats=feats, subnet_tr=None, subnet_names=None)

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
                  eps=float("inf"), rounds=40, lr=0.1, clip=1.0, batch=BATCH, binary=False):
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
    for r in range(1, rounds + 1):
        P = {k: v.unsqueeze(0).repeat(N, *[1] * v.dim()).clone() for k, v in g_params.items()}
        for _ in range(LOCAL_STEPS):
            pos, mask, tr_ = poisson_batch(lens, L, batch, bmax, DEV); trunc_total += tr_
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
        a = AGG_FN[agg](U, gen=gen, prev=prev_a)
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
        truth = _synthetic_csvs(tmp, ["monday.csv", "tuesday.csv"], 1500, with_ips=True, seed=3)
        D = load_data(tmp)
        check("classes restricted to macro set", set(np.unique(np.r_[D["ytr"], D["yte"]])) <= set(range(len(CIC_CLASSES))))
        check("no ID / port / Attempted-Category features", not any(("port" in f.lower()) or f.lower() in CIC_ID_COLS for f in D["feats"]), f"({D['feats']})")
        check("inf strings parsed, features finite", np.isfinite(D["Xtr"]).all() and np.isfinite(D["Xte"]).all())
        full = pd.concat([read_csv_any(f) for f in sorted(glob.glob(os.path.join(tmp, "*.csv")))])
        n_valid = int(full.Label.map(map_label).isin(CIC_CLASSES).sum())
        n_kept = sum(D["class_counts"].values())
        check("attempted/probe/unknown dropped; only dups+conflicts removed beyond that",
              n_valid - truth["dups"] - truth["conflicts"] <= n_kept <= n_valid - truth["dups"], f"({n_kept} of {n_valid} valid)")
        check("2 days in day labels", len(np.unique(D["days_tr"])) == 2)
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
#  REPORTS
# =============================================================================
def cell_str(v): return f"{np.mean(v):>5.2f}+-{np.std(v):4.2f}[{np.min(v):.2f}-{np.max(v):.2f}]" if len(v) else " " * 22

def report_A(d, target):
    d = d[(d.target == target) & (d.eps.astype(float) == float("inf")) & (~d.binary) & (d.rmult == 1)]
    banner(f"EXP-A RESULTS -- {DATASET} -- target {target}")
    ref = d[(d["agg"] == "fedavg") & (d.f == 0) & (d.k == d.k.max())].target_recall.mean()
    print(f"  reference (FedAvg, f=0, k={d.k.max()}): {ref:.3f}  | learnable >= {LEARNABLE_FRAC}*ref = {LEARNABLE_FRAC*ref:.3f}")
    kst, kst05 = {}, {}
    for agg in AGGS:
        sub(f"{agg}: target recall mean+-sd [min-max over seeds]   rows=f, cols=k")
        print("    f\\k " + "".join(f"{k:>23d}" for k in sorted(d.k.unique())))
        for f in sorted(d.f.unique()):
            print(f"    {f:>3d} " + "".join(" " + cell_str(d[(d["agg"] == agg) & (d.f == f) & (d.k == k)].target_recall.values)
                                        for k in sorted(d.k.unique())))
            g = d[(d["agg"] == agg) & (d.f == f)].groupby("k").target_recall.mean()
            kst[(agg, f)] = estimate_kstar(g.index.values, g.values, ref)
            kst05[(agg, f)] = estimate_kstar(g.index.values, g.values, ref, 0.5)
    sub("D1 boundary k* vs floor  (tax = k* - (f+1): failure ABOVE the aggregator-independent floor)")
    print(f"    {'agg':13s} {'f':>2s} {'k*(0.8)':>8s} {'k*(0.5)':>8s} {'floor f+1':>9s} {'v2 pred':>7s} {'tax':>5s}")
    rows = []
    for agg in AGGS:
        for f in sorted(d.f.unique()):
            ks = kst[(agg, f)]; gap = (ks - (f + 1)) if isinstance(ks, int) else "inf"
            rows.append({"agg": agg, "f": f, "kstar": ks, "kstar_05": kst05[(agg, f)], "tax": gap})
            print(f"    {agg:13s} {f:>2d} {str(ks):>8s} {str(kst05[(agg,f)]):>8s} {f+1:>9d} {str(predicted_kstar(agg,f)):>7s} {str(gap):>5s}")
    pd.DataFrame(rows).to_csv(os.path.join(OUT_DIR, f"expA_kstar_{fname(target)}.csv"), index=False)
    sub("D2 collateral (mean over k,f): benign FPR, other-attack recall")
    print(d.groupby("agg")[["benign_fpr", "other_attack_recall_mean", "other_attack_recall_min"]].mean().round(4).to_string())
    sub("Q-A preview (multiclass, f=0): where do target test flows go?  mean share over seeds")
    d0 = d[d.f == 0]
    for col, lab in (("target_recall", "correct class"), ("target_any_attack", "any attack class"), ("target_to_normal", "-> Normal")):
        print(f"    {lab}:"); print("    " + d0.groupby(["agg", "k"])[col].mean().unstack().round(2).to_string().replace("\n", "\n    "))
    sub("WORST CASE + WHAT DID NOT MOVE")
    w = d.loc[d.target_recall.idxmin()]
    print(f"    worst: {w['agg']} k={w.k} f={w.f} seed={w.seed} recall={w.target_recall:.3f}")
    for c in CLASSES:
        if c == target or f"recall_{c}" not in d: continue
        s = d.groupby(["agg", "k", "f"])[f"recall_{c}"].mean()
        print(f"    {c:15s} recall range across configs: {s.min():.3f}-{s.max():.3f}{'  (did not move)' if s.max()-s.min()<0.02 else ''}")
    plot_A(d, target, ref, kst)
    return kst, ref, d

def plot_A(d, target, ref, kst):
    ks, fs = sorted(d.k.unique()), sorted(d.f.unique())
    aggs = [a for a in AGGS if a in d["agg"].unique()]
    nc = 4 if len(aggs) > 6 else 3; nr = int(math.ceil(len(aggs) / nc))
    fig, axes = plt.subplots(nr, nc, figsize=(5 * nc, 4.2 * nr), sharex=True, sharey=True, squeeze=False)
    for ax, agg in zip(axes.flat, aggs):
        M = np.array([[d[(d["agg"] == agg) & (d.f == f) & (d.k == k)].target_recall.mean() for k in ks] for f in fs])
        im = ax.imshow(M, origin="lower", aspect="auto", vmin=0, vmax=1, cmap="viridis")
        ax.set_xticks(range(len(ks))); ax.set_xticklabels(ks); ax.set_yticks(range(len(fs))); ax.set_yticklabels(fs)
        for i in range(len(fs)):
            for j in range(len(ks)):
                ax.text(j, i, f"{M[i,j]:.2f}", ha="center", va="center", fontsize=6, color="w" if M[i, j] < .5 else "k")
            xs = [j for j, k in enumerate(ks) if k <= fs[i]]
            if fs[i] > 0 and xs: ax.plot([max(xs) + .5] * 2, [i - .5, i + .5], "r-", lw=2)
        ax.set_title(agg); ax.set_xlabel("k (witnesses)"); ax.set_ylabel("f (mimic attackers)")
    for ax in list(axes.flat)[len(aggs):]: ax.axis("off")
    fig.colorbar(im, ax=axes, shrink=.7, label=f"{target} recall")
    fig.suptitle(f"{DATASET} EXP-A phase diagram -- {target} (red: floor k<=f)")
    fig.savefig(os.path.join(FIG_DIR, f"A1_phase_{fname(target)}.pdf"), bbox_inches="tight"); plt.close(fig)
    fig, axes = plt.subplots(1, len(fs), figsize=(4.2 * len(fs), 3.8), sharey=True)
    for ax, f in zip(np.atleast_1d(axes), fs):
        for agg in aggs:
            g = d[(d["agg"] == agg) & (d.f == f)]; m = g.groupby("k").target_recall.mean()
            ax.plot(m.index, m.values, "-o", ms=3, label=agg); ax.scatter(g.k, g.target_recall, s=6, alpha=.3)
        ax.axhline(LEARNABLE_FRAC * ref, ls="--", c="gray"); ax.axvline(f + .5, ls=":", c="r")
        ax.set_title(f"f = {f}"); ax.set_xlabel("k"); ax.set_xscale("log", base=2)
    np.atleast_1d(axes)[0].set_ylabel(f"{target} recall"); np.atleast_1d(axes)[-1].legend(fontsize=7)
    fig.tight_layout(); fig.savefig(os.path.join(FIG_DIR, f"A2_recall_vs_k_{fname(target)}.pdf")); plt.close(fig)
    fig, ax = plt.subplots(figsize=(8, 4)); w = 0.8 / len(fs)
    for i, f in enumerate(fs):
        ax.bar(np.arange(len(aggs)) + i * w, [(kst[(a, f)] - (f + 1)) if isinstance(kst[(a, f)], int) else max(ks) for a in aggs], w, label=f"f={f}")
    ax.set_xticks(np.arange(len(aggs)) + w * (len(fs) - 1) / 2); ax.set_xticklabels(aggs, rotation=20)
    ax.set_ylabel("witness tax  k* - (f+1)"); ax.legend(); ax.set_title("Witness tax above the floor (bar at max k = never)")
    fig.tight_layout(); fig.savefig(os.path.join(FIG_DIR, f"A3_tax_{fname(target)}.pdf")); plt.close(fig)

def report_QA(dA, dQ, kst, target):
    banner(f"EXP-QA RESULTS -- missed or mislabelled? -- {DATASET} -- target {target}")
    mc = dA[(dA.target == target) & (dA.f == 0) & (~dA.binary) & (dA.rmult == 1) & (dA.eps.astype(float) == float("inf"))
            & dA.seed.isin(SEEDS_QA) & dA.k.isin(K_GRID_QA)]
    bn = dQ[(dQ.target == target) & dQ.binary]
    kmax = max(K_GRID_QA)
    ref_any = mc[(mc["agg"] == "fedavg") & (mc.k == kmax)].target_any_attack.mean()
    ref_bin = bn[(bn["agg"] == "fedavg") & (bn.k == kmax)].target_recall.mean()
    print(f"  references (FedAvg, f=0, k={kmax}): multiclass any-attack {ref_any:.3f} | binary detection {ref_bin:.3f}")
    sub("per cell (f=0): multiclass correct / multiclass any-attack / BINARY detection   (mean over seeds)")
    for agg in AGGS:
        cells = []
        for k in K_GRID_QA:
            a = mc[(mc["agg"] == agg) & (mc.k == k)]; b = bn[(bn["agg"] == agg) & (bn.k == k)]
            cells.append(f"k={k}:{a.target_recall.mean():.2f}/{a.target_any_attack.mean():.2f}/{b.target_recall.mean():.2f}")
        print(f"    {agg:13s} " + "  ".join(cells))
    kf0 = {a: kst.get((a, 0)) for a in AGGS}
    tc = tax_cells(kf0, K_GRID_QA)
    v_any = [mc[(mc["agg"] == a) & (mc.k == k)].target_any_attack.mean() for a, k in tc]
    v_bin = [bn[(bn["agg"] == a) & (bn.k == k)].target_recall.mean() for a, k in tc]
    v_nrm = [mc[(mc["agg"] == a) & (mc.k == k)].target_to_normal.mean() for a, k in tc]
    va, sa = qa_classify(v_any, ref_any); vb, sb = qa_classify(v_bin, ref_bin)
    sub(f"VERDICT (pre-registered: >= {QA_MAJORITY:.0%} of {len(tc)} tax cells agree)")
    print(f"    multiclass model, target flagged as SOME attack: {va}  (share of tax cells detected = {sa:.2f})")
    print(f"    binary model, target detected:                  {vb}  (share = {sb:.2f})")
    if len(v_nrm): print(f"    mean share of target flows sent to Normal in tax cells: {np.nanmean(v_nrm):.2f}")
    print(f"    binary benign FPR by aggregator: " + ", ".join(f"{a}={bn[bn['agg']==a].benign_fpr.mean():.4f}" for a in AGGS if (bn['agg']==a).any()))
    print("    reading: MISSED/MISSED  -> the tax causes missed attacks (strong claim).")
    print("             DETECTED (multiclass any) -> tax = attribution loss in the multiclass model.")
    print("             binary DETECTED but multiclass MISSED -> a binary detector escapes the tax (design lever).")
    tcs = pd.DataFrame(tc, columns=["agg", "k"]).assign(mc_any=v_any, bin_detect=v_bin, to_normal=v_nrm)
    tcs.to_csv(os.path.join(OUT_DIR, f"expQA_taxcells_{fname(target)}.csv"), index=False)
    json.dump({"multiclass_any": [va, sa], "binary": [vb, sb], "n_tax_cells": len(tc)},
              open(os.path.join(OUT_DIR, f"expQA_verdict_{fname(target)}.json"), "w"), indent=1)
    fig, axes = plt.subplots(1, len(AGGS), figsize=(3.2 * len(AGGS), 3.2), sharey=True)
    for ax, agg in zip(np.atleast_1d(axes), AGGS):
        a = mc[mc["agg"] == agg].groupby("k"); b = bn[bn["agg"] == agg].groupby("k")
        ax.plot(a.target_recall.mean(), "-o", ms=3, label="multi: correct")
        ax.plot(a.target_any_attack.mean(), "-s", ms=3, label="multi: any attack")
        ax.plot(b.target_recall.mean(), "--^", ms=3, label="binary")
        ax.set_title(agg); ax.set_xlabel("k"); ax.set_xscale("log", base=2)
    np.atleast_1d(axes)[0].set_ylabel(f"{target} detection"); np.atleast_1d(axes)[-1].legend(fontsize=6)
    fig.tight_layout(); fig.savefig(os.path.join(FIG_DIR, f"QA1_{fname(target)}.pdf")); plt.close(fig)

def expD_configs(kst, target):
    cfg = []
    for agg in AGGS:
        if agg == "fedavg": continue
        ks = kst.get((agg, 0))
        below = [k for k in K_GRID if ks == "never" or (isinstance(ks, int) and k < ks)]
        cfg += [dict(target=target, k=k, f=0, agg=agg, eps=float("inf"), seed=s, binary=False, rmult=LONG_MULT)
                for k in below for s in SEEDS_D]
    return cfg

def report_D(dD, ref, target, kst):
    banner(f"EXP-D RESULTS -- wall or delay? ({LONG_MULT}x rounds, EVERY tax cell, f=0) -- {target}")
    if not len(dD): print("  no robust aggregator had a tax at f=0 -> nothing to test"); return
    rows, summ = [], []
    for agg, ga in dD.groupby("agg"):
        tk, tl, t2 = [], [], []
        for k, g in ga.groupby("k"):
            b, l = g.target_recall_base.mean(), g.target_recall.mean()
            m2 = g["target_recall_2R"].mean() if "target_recall_2R" in g else float("nan")
            per_seed = [delay_verdict(x, y, ref) for x, y in zip(g.target_recall_base, g.target_recall)]
            rows.append({"agg": agg, "k": k, "recall_at_R": round(b, 3), "recall_at_2R": round(m2, 3),
                         f"recall_at_{LONG_MULT}R": round(l, 3),
                         "verdict(mean)": delay_verdict(b, l, ref), "per_seed": ",".join(per_seed)})
            tk.append(k); tl.append(l); t2.append(m2)
        kR = kst.get((agg, 0))
        walls = [r["k"] for r in rows if r["agg"] == agg and r["verdict(mean)"] == "WALL"]
        rowS = {"agg": agg, "k*(R)": kR}
        if LONG_MULT != 2: rowS["k*(2R)"] = kstar_long(tk, t2, kR, ref) if np.isfinite(t2).any() else "n/a"
        rowS.update({f"k*({LONG_MULT}R)": kstar_long(tk, tl, kR, ref), "WALL at k": walls if walls else "-"})
        summ.append(rowS)
    t = pd.DataFrame(rows); print(t.to_string(index=False))
    sub(f"SUMMARY: boundary at the calibrated budget R vs {LONG_MULT}R")
    ts = pd.DataFrame(summ); print(ts.to_string(index=False))
    t.to_csv(os.path.join(OUT_DIR, f"expD_{fname(target)}.csv"), index=False)
    ts.to_csv(os.path.join(OUT_DIR, f"expD_summary_{fname(target)}.csv"), index=False)
    print("    reading: k*(3R) << k*(R) -> tax is mostly a rounds-to-detect cost (report k* vs budget).")
    print("             WALL cells that stay walls at 3R -> structural region (e.g. trmean at k <= b).")

def run_exp_K0(target, Xt, yt, Xe, ye, D, cal, dA):
    banner(f"EXP-K0 -- zero-witness control (k = 0, f = 0) -- {target}")
    cfg = [dict(target=target, k=0, f=0, agg=a, eps=float("inf"), seed=s, binary=b)
           for a in K0_AGGS for s in SEEDS_QA for b in (False, True)]
    d0, ok = exp_grid("EXP-K0", cfg, os.path.join(OUT_DIR, "expK0_runs.csv"), Xt, yt, Xe, ye, D, cal)
    if not ok: return
    d0 = d0[d0.target == target]
    mc = dA[(dA.target == target) & (dA["agg"] == "fedavg") & (dA.f == 0) & (dA.k == max(K_GRID)) & (~dA.binary)]
    ref_any = mc.target_any_attack.mean()
    qa = os.path.join(OUT_DIR, "expQA_runs.csv")
    bq = pd.read_csv(qa) if os.path.exists(qa) else pd.DataFrame()
    if len(bq):
        bq["binary"] = bq["binary"].astype(str).str.lower().isin(["true", "1"])
        bq = bq[(bq.target == target) & bq.binary & (bq["agg"] == "fedavg") & (bq.k == max(K_GRID_QA))]
    ref_bin = bq.target_recall.mean() if len(bq) else float("nan")
    rows = []
    for (agg, b), g in d0.groupby(["agg", "binary"]):
        v = g.target_any_attack.mean() if not b else g.target_recall.mean()
        r_ = ref_bin if b else ref_any
        rows.append({"agg": agg, "model": "binary" if b else "multiclass(any-attack)", "k=0 detection": round(v, 3),
                     "reference": round(r_, 3), "verdict": k0_verdict(v, r_),
                     "-> Normal": round(g.target_to_normal.mean(), 3)})
    t = pd.DataFrame(rows); print(t.to_string(index=False))
    t.to_csv(os.path.join(OUT_DIR, f"expK0_{fname(target)}.csv"), index=False)
    print("    reading: DETECTABLE_WITHOUT_WITNESSES (binary) -> binary 'escapes the tax' only because the")
    print("             target resembles other attacks; do not claim a binary-head fix for this target.")

def report_B(dB, dA, target, ref):
    a = dA[(dA.target == target) & (~dA.binary) & (dA.rmult == 1) & (dA.eps.astype(float) == float("inf"))
           & dA["agg"].isin(AGGS_DP) & dA.k.isin(K_GRID_DP) & dA.f.isin([0, F_HAT]) & dA.seed.isin(SEEDS_DP)]
    d = pd.concat([dB[dB.target == target], a], ignore_index=True); d["eps"] = d.eps.astype(float)
    banner(f"EXP-B RESULTS (DP-SGD) -- {DATASET} -- target {target}  (non-private rows reused from EXP-A)")
    rows = []
    for agg in AGGS_DP:
        for f in sorted(d.f.unique()):
            sub(f"{agg}, f={f}: target recall  rows=privacy setting, cols=k")
            for eps in sorted(d.eps.unique(), key=lambda e: (e < 0, e)):
                g = d[(d["agg"] == agg) & (d.f == f) & (d.eps == eps)]
                if not len(g): continue
                m = g.groupby("k").target_recall
                print(f"    {eps_name(eps):12s} " + "  ".join(f"k={k}:{cell_str(v.values)}" for k, v in m))
                mm = m.mean(); rows.append({"agg": agg, "f": f, "setting": eps_name(eps), "eps": eps,
                                            "kstar": estimate_kstar(mm.index.values, mm.values, ref),
                                            "benign_fpr": g.benign_fpr.mean(), "other_attack_recall": g.other_attack_recall_mean.mean(),
                                            "target_any_attack": g.target_any_attack.mean()})
    kd = pd.DataFrame(rows); kd.to_csv(os.path.join(OUT_DIR, f"expB_kstar_{fname(target)}.csv"), index=False)
    sub("D4 k* by privacy setting (P3: k* non-decreasing as eps falls)"); print(kd.to_string(index=False))
    sub("D6 DP collateral: mean recall per class, f=0, pooled over k (which class pays for privacy?)")
    pc = [c for c in CLASSES if f"recall_{c}" in d and d[f"recall_{c}"].notna().any()]
    tab = d[d.f == 0].groupby(["agg", "eps"])[[f"recall_{c}" for c in pc]].mean().round(3)
    tab.columns = pc
    tab.index = [f"{a} {eps_name(e)}" for a, e in tab.index]
    print("    " + tab.to_string().replace("\n", "\n    "))
    sub("D5 clipping vs noise")
    for (agg, f), g in kd.groupby(["agg", "f"]):
        get = lambda nm: g[g.setting == nm].kstar.values[0] if (g.setting == nm).any() else None
        print(f"    {agg:8s} f={f}: non-private k*={get('non-private')}  clip-only k*={get('clip-only')}  "
              + "  ".join(f"{r.setting}:{r.kstar}" for r in g[(g.eps > 0) & np.isfinite(g.eps)].sort_values('eps', ascending=False).itertuples()))
    fig, axes = plt.subplots(1, len(AGGS_DP), figsize=(4.5 * len(AGGS_DP), 3.8), sharey=True)
    for ax, agg in zip(np.atleast_1d(axes), AGGS_DP):
        for eps in sorted(d.eps.unique(), key=lambda e: (e < 0, e)):
            g = d[(d["agg"] == agg) & (d.f == 0) & (d.eps == eps)].groupby("k").target_recall.mean()
            ax.plot(g.index, g.values, "-o", ms=3, label=eps_name(eps))
        ax.set_title(f"{agg}, f=0"); ax.set_xlabel("k"); ax.axhline(LEARNABLE_FRAC * ref, ls="--", c="gray")
    np.atleast_1d(axes)[0].set_ylabel(f"{target} recall"); np.atleast_1d(axes)[-1].legend(fontsize=7)
    fig.tight_layout(); fig.savefig(os.path.join(FIG_DIR, f"B1_dp_{fname(target)}.pdf")); plt.close(fig)

def run_exp_C(D, Xt, yt, Xe, ye, cal):
    banner(f"EXP-C -- NATURAL WITNESS STRUCTURE ({DATASET} day-lock, f = 0) -- multiclass + binary")
    C = len(CLASSES)
    clients, wk, comp = build_daylock_clients(D["ytr"], D["days_tr"], N_CLIENTS, C, np.random.default_rng(0))
    print(f"  {len(np.unique(D['days_tr']))} capture days -> {len(clients)} clients.  CAVEAT: days are capture sessions")
    print("  of one testbed, not independent organisations -- structural analogue only.")
    print(pd.DataFrame(comp).rename(columns={i: c for i, c in enumerate(CLASSES)}).to_string(index=False))
    print(f"\n  witnesses per class: { {CLASSES[c]: v for c, v in wk.items()} }  (N = {len(clients)})")
    roles = np.array(["H"] * len(clients), dtype=object)
    csv = os.path.join(OUT_DIR, "expC_natural.csv"); cid = cfg_id(cal)
    done = pd.read_csv(csv) if os.path.exists(csv) else pd.DataFrame()
    have = set(tuple(r) for r in done[done.cfg_id.astype(str) == cid][["agg", "seed", "binary"]].astype(str).values) if len(done) else set()
    for b in (False, True):
        for agg in AGGS:
            for seed in SEEDS:
                if (agg, str(seed), str(b)) in have: continue
                if out_of_time(): STOPPED["flag"] = True; print("  [TIME BUDGET] EXP-C incomplete -> resume next session"); return
                s = summarise_hist(run_federated(Xt, yt, Xe, ye, clients, roles, agg, C, seed,
                                                 rounds=cal["rounds"], lr=cal["lr"], binary=b))
                row = {"agg": agg, "seed": seed, "binary": b, "cfg_id": cid,
                       **{c: s[f"rec_{i}"] for i, c in enumerate(CLASSES)},
                       **{f"any_{c}": s[f"any_{i}"] for i, c in enumerate(CLASSES)}}
                append_row(csv, row)
    res = pd.read_csv(csv); res = res[res.cfg_id.astype(str) == cid]
    res["binary"] = res["binary"].astype(str).str.lower().isin(["true", "1"])
    present = [c for c in CLASSES if res[c].notna().any()]
    m = res[~res.binary]; bb = res[res.binary]
    sub("multiclass: mean recall per class (Normal column = 1 - FPR)"); print(m.groupby("agg")[present].mean().round(3).to_string())
    sub("multiclass: share flagged as ANY attack"); print(m.groupby("agg")[[f"any_{c}" for c in present[1:]]].mean().round(3).to_string())
    sub("BINARY model: detection rate per class (Normal column = 1 - FPR)"); print(bb.groupby("agg")[present].mean().round(3).to_string())
    sub("worst seed per class (multiclass)"); print(m.groupby("agg")[present].min().round(3).to_string())
    mm = m.groupby("agg")[present].mean(); bm = bb.groupby("agg")[present].mean()
    fig, axes = plt.subplots(1, 2, figsize=(16, 4), sharey=True); atk = present[1:]; w = .8 / len(AGGS)
    for ax, tab, ttl in ((axes[0], mm, "multiclass recall"), (axes[1], bm, "binary detection")):
        for i, agg in enumerate(AGGS):
            if agg in tab.index: ax.bar(np.arange(len(atk)) + i * w, tab.loc[agg, atk], w, label=agg)
        ax.set_xticks(np.arange(len(atk)) + w * (len(AGGS) - 1) / 2)
        ax.set_xticklabels([f"{c}\n(k={wk[CLASSES.index(c)]})" for c in atk]); ax.set_title(ttl)
    axes[0].set_ylabel("recall"); axes[1].legend(fontsize=7)
    fig.tight_layout(); fig.savefig(os.path.join(FIG_DIR, "C1_natural_daylock.pdf")); plt.close(fig)


# =============================================================================
#  CLAIMS SUMMARY -- the log's last section is the paper's evidence table
# =============================================================================
def claims_summary(targets):
    banner(f"CLAIMS SUMMARY -- {DATASET}  (also written to CLAIMS_SUMMARY_{TAG}.md)")
    out = [f"# Claims summary -- {DATASET} (script {SCRIPT_VERSION})\n"]
    def emit(title, txt):
        print(f"\n  {title}\n" + "\n".join("    " + l for l in str(txt).splitlines()))
        out.append(f"\n## {title}\n```\n{txt}\n```\n")
    rd = lambda n: os.path.join(OUT_DIR, n)
    A = pd.read_csv(rd("expA_runs.csv")) if os.path.exists(rd("expA_runs.csv")) else pd.DataFrame()
    if len(A):
        A["binary"] = A["binary"].astype(str).str.lower().isin(["true", "1"])
        A = A[(~A.binary) & (A.rmult == 1) & (A.eps.astype(float) == float("inf"))]
    for t in targets:
        ks = rd(f"expA_kstar_{fname(t)}.csv")
        if not os.path.exists(ks): emit(f"{t}: no EXP-A results yet", "-"); continue
        k = pd.read_csv(ks)
        # C1: floor + tax + missed-vs-mislabelled
        a = A[A.target == t]
        ref = a[(a["agg"] == "fedavg") & (a.f == 0) & (a.k == a.k.max())].target_recall.mean()
        fl = []
        for agg, g in a.groupby("agg"):
            cells = g[g.k <= g.f].groupby(["k", "f"]).target_recall.mean().values
            held, mx = floor_held(cells, ref)
            fl.append(f"{agg:13s} held={held}  max recall at k<=f = {mx:.3f}")
        emit(f"{t} | C1a floor P1 (held = never reaches half the learnable line)", "\n".join(fl))
        emit(f"{t} | C1b witness tax (k* and tax, f=0)", k[k.f == 0][["agg", "kstar", "kstar_05", "tax"]].to_string(index=False))
        qv = rd(f"expQA_verdict_{fname(t)}.json")
        k0 = rd(f"expK0_{fname(t)}.csv")
        txt = json.dumps(json.load(open(qv))) if os.path.exists(qv) else "EXP-QA not run"
        if os.path.exists(k0): txt += "\nK0: " + pd.read_csv(k0)[["agg", "model", "k=0 detection", "verdict"]].to_string(index=False)
        emit(f"{t} | C1c missed vs mislabelled (Q-A) + zero-witness control", txt)
        # C2: delay vs wall
        dsum = rd(f"expD_summary_{fname(t)}.csv")
        emit(f"{t} | C2 wall or delay (k* vs round budget)", pd.read_csv(dsum).to_string(index=False) if os.path.exists(dsum) else "EXP-D not run")
        # C3: DP
        bk = rd(f"expB_kstar_{fname(t)}.csv")
        if os.path.exists(bk):
            b = pd.read_csv(bk); b0 = b[b.f == 0]
            lines = []
            for agg, g in b0.groupby("agg"):
                order = [g[g.eps == e].kstar.values[0] if (g.eps == e).any() else None for e in (float("inf"), 10.0, 3.0, 1.0)]
                order = [int(x) if isinstance(x, (int, float, np.integer, np.floating)) and np.isfinite(x) else x for x in order]
                cl = g[g.eps < 0].kstar.values
                lines.append(f"{agg:8s} k* non-private/eps10/eps3/eps1 = {order}  clip-only={cl[0] if len(cl) else '-'}  "
                             f"P3 monotone={p3_monotone([o for o in order if o is not None])}")
            emit(f"{t} | C3 privacy interaction (f=0)", "\n".join(lines))
        else:
            emit(f"{t} | C3 privacy interaction", "EXP-B not run for this target")
    cp = rd("expC_natural.csv")
    if os.path.exists(cp):
        c = pd.read_csv(cp); c["binary"] = c["binary"].astype(str).str.lower().isin(["true", "1"])
        pres = [x for x in CLASSES[1:] if x in c and c[x].notna().any()]
        emit("Natural structure (day-lock): multiclass recall per class", c[~c.binary].groupby("agg")[pres].mean().round(3).to_string())
        emit("Natural structure (day-lock): BINARY detection per class", c[c.binary].groupby("agg")[pres].mean().round(3).to_string())
    open(rd(f"CLAIMS_SUMMARY_{TAG}.md"), "w").write("\n".join(out))

# =============================================================================
#  SESSION HELPERS
# =============================================================================
def import_previous_outputs():
    hits = [p for p in glob.glob(f"/kaggle/input/**/{OUT_BASENAME}", recursive=True) if os.path.isdir(p)]
    n = 0
    for h in hits:
        for fpath in glob.glob(os.path.join(h, "*.csv")) + glob.glob(os.path.join(h, "*.json")):
            dst = os.path.join(OUT_DIR, os.path.basename(fpath))
            if not os.path.exists(dst): shutil.copy(fpath, dst); n += 1
    if hits: print(f"  imported {n} result files from previous session(s): {hits}")

def print_plan(targets, b_targets):
    sub("RUN PLAN (configs per experiment)")
    nA = len([1 for k in K_GRID for f in F_GRID for a in AGGS for s in SEEDS if k + f <= N_CLIENTS])
    nQ = len(K_GRID_QA) * len(AGGS) * len(SEEDS_QA)
    nB = len([1 for k in K_GRID_DP for f in [0, F_HAT] for a in AGGS_DP for e in EPS_GRID for s in SEEDS_DP
              if k + f <= N_CLIENTS and np.isfinite(e)]) if RUN_EXP_B else 0
    nD = (len(AGGS) - 1) * len(SEEDS_D) * 6
    print(f"    per target: EXP-A {nA if RUN_EXP_A else 0} | EXP-QA {nQ if RUN_EXP_QA else 0} (binary) | "
          f"EXP-D ~{nD if RUN_EXP_D else 0} (x{LONG_MULT} rounds, depends on k*) | EXP-K0 {2*len(K0_AGGS)*len(SEEDS_QA) if RUN_EXP_K0 else 0}")
    print(f"    EXP-B {nB} per target on {b_targets} (DP runs ~3x slower) | EXP-C {2*len(AGGS)*len(SEEDS)} once")
    print(f"    targets this session: {targets}.  Time budget {TIME_BUDGET_H} h -> resumable.")

# =============================================================================
#  MAIN
# =============================================================================
def main():
    banner(f"WITNESS PHASE {SCRIPT_VERSION} | {DATASET} | MODE={MODE} | device={DEV} | out={OUT_DIR}")
    if DEV.type == "cpu": print("  [WARN] CPU run. Kaggle: Accelerator -> GPU.")
    import_previous_outputs()
    json.dump({k: v for k, v in globals().items() if k.isupper() and isinstance(v, (int, float, str, list, bool, dict))},
              open(os.path.join(OUT_DIR, f"config_{MODE}.json"), "w"), indent=1, default=str)
    if not phase0_self_tests():
        print("\n  STOP: fix failing self-tests first."); return
    if ONLY_SELF_TEST: return
    D = load_data()
    sub("Final class counts (train / test)")
    for i, c in enumerate(CLASSES): print(f"    {c:15s} {np.sum(D['ytr']==i):>9,} / {np.sum(D['yte']==i):>7,}")
    elig, rep = select_targets(D["class_counts"], D["ytr"], D["yte"], CLASSES, M_TARGET, MIN_TEST, RARE_SHARE)
    sub(f"TARGET SELECTION (rare < {100*RARE_SHARE:.0f}% of clean flows, train >= {M_TARGET}, test >= {MIN_TEST})")
    print(rep.to_string(index=False))
    if not elig: print("  no eligible target -> stop"); return
    targets = elig[:N_TARGETS]
    if RUN_TARGETS: targets = [t for t in targets if t in RUN_TARGETS]
    if isinstance(B_TARGETS, (list, tuple)): b_targets = [t for t in B_TARGETS if t in elig]
    else: b_targets = elig[:1] if B_TARGETS == "first" else targets
    print(f"  eligible (rarest first): {elig} -> this session: {targets}")
    print_plan(targets, b_targets)
    Xt, yt = torch.tensor(D["Xtr"], device=DEV), torch.tensor(D["ytr"], device=DEV, dtype=torch.long)
    Xe, ye = torch.tensor(D["Xte"], device=DEV), torch.tensor(D["yte"], device=DEV, dtype=torch.long)
    banner("PRE-REGISTERED RULES")
    print("    P1 floor: no aggregator learns at k <= f.")
    print(f"    G1: plateau by {PLATEAU_FRAC_MAX}xR_CAL and last-20% rise <= {RISE_TOL}.  G6: FPR <= {FPR_MAX}, "
          f"non-target recall >= {DEAD_RECALL}, target ref >= {REF_MIN}.")
    print(f"    Q-A: over tax cells, >= {QA_MAJORITY:.0%} detected -> DETECTED; <= {1-QA_MAJORITY:.0%} -> MISSED; else MIXED.")
    print(f"    EXP-D: {LONG_MULT}x rounds reaches {LEARNABLE_FRAC}xref -> DELAY; gains >= {DELAY_GAIN} -> PARTIAL; else WALL.")
    cal0 = None
    for target in targets:
        if STOPPED["flag"]: break
        cal = calibrate(Xt, yt, Xe, ye, D, target)
        pre = preflight_gate(cal["conv"], cal["ref_recall"], target, CLASSES)
        banner(f"PRE-FLIGHT GATE -- {'GO' if pre['GO'] else 'NO-GO'} ({DATASET}, {target})")
        for r in pre["reasons"]: print("    " + r)
        json.dump(pre, open(os.path.join(OUT_DIR, f"preflight_{fname(target)}.json"), "w"), indent=1)
        if not pre["GO"] and not FORCE_PAST_PREFLIGHT:
            print("    -> grids for this target skipped (set FORCE_PAST_PREFLIGHT=True only for diagnosis)."); continue
        cal0 = cal0 or cal
        kst, ref, dA = None, None, None
        if RUN_EXP_A:
            banner(f"EXP-A -- k x f x aggregator (non-private) -- {target}")
            cfg = [dict(target=target, k=k, f=f, agg=a, eps=float("inf"), seed=s)
                   for k in K_GRID for f in F_GRID for a in AGGS for s in SEEDS if k + f <= N_CLIENTS]
            dA, okA = exp_grid("EXP-A", cfg, os.path.join(OUT_DIR, "expA_runs.csv"), Xt, yt, Xe, ye, D, cal)
            if okA:
                kst, ref, _ = report_A(dA, target)
                g = gate_decision(dA[(dA.target == target) & (~dA.binary)], kst, ref)
                banner(f"POST-EXP-A GATE -- {'GO' if g['GO'] else 'FLAGGED'} ({DATASET}, {target})")
                for r in g["reasons"]: print("    " + r)
                json.dump(g, open(os.path.join(OUT_DIR, f"gate_{fname(target)}.json"), "w"), indent=1)
        if RUN_EXP_QA and kst is not None and not STOPPED["flag"]:
            banner(f"EXP-QA -- binary-trained model, f=0 -- {target}")
            cfg = [dict(target=target, k=k, f=0, agg=a, eps=float("inf"), seed=s, binary=True)
                   for k in K_GRID_QA for a in AGGS for s in SEEDS_QA]
            dQ, okQ = exp_grid("EXP-QA", cfg, os.path.join(OUT_DIR, "expQA_runs.csv"), Xt, yt, Xe, ye, D, cal)
            if okQ: report_QA(dA, dQ, kst, target)
        if RUN_EXP_D and kst is not None and not STOPPED["flag"]:
            banner(f"EXP-D -- wall or delay -- {target}")
            cfg = expD_configs(kst, target)
            dD, okD = exp_grid("EXP-D", cfg, os.path.join(OUT_DIR, "expD_runs.csv"), Xt, yt, Xe, ye, D, cal)
            if okD: report_D(dD[dD.target == target], ref, target, kst)
        if RUN_EXP_K0 and kst is not None and not STOPPED["flag"]:
            run_exp_K0(target, Xt, yt, Xe, ye, D, cal, dA)
        if RUN_EXP_B and HAVE_OPACUS and target in b_targets and not STOPPED["flag"]:
            banner(f"EXP-B -- k x privacy x aggregator -- {target}")
            cfg = [dict(target=target, k=k, f=f, agg=a, eps=e, seed=s)
                   for k in K_GRID_DP for f in [0, F_HAT] for a in AGGS_DP for e in EPS_GRID for s in SEEDS_DP
                   if k + f <= N_CLIENTS and (np.isfinite(e) or not RUN_EXP_A)]
            dB, okB = exp_grid("EXP-B", cfg, os.path.join(OUT_DIR, "expB_runs.csv"), Xt, yt, Xe, ye, D, cal)
            if okB:
                if ref is None:
                    ref = dB[(dB["agg"] == "fedavg") & (dB.f == 0) & (dB.eps.astype(float) == float("inf")) & (dB.k == max(K_GRID_DP))].target_recall.mean()
                report_B(dB, dA if dA is not None else dB.iloc[:0], target, ref)
    if RUN_EXP_C and not STOPPED["flag"]:
        if cal0 is None: print("\n  EXP-C skipped: no calibrated target passed pre-flight.")
        else: run_exp_C(D, Xt, yt, Xe, ye, cal0)
    try: claims_summary(targets)
    except Exception as e: print(f"  [WARN] claims summary failed ({type(e).__name__}: {e}) -- raw CSVs are intact")
    banner("STOPPED EARLY (time budget) -- resume next session" if STOPPED["flag"] else "DONE")
    print(f"  outputs: {OUT_DIR}")
    for p in sorted(glob.glob(os.path.join(FIG_DIR, "*.pdf"))): print("   ", p)

if __name__ == "__main__":
    main()
