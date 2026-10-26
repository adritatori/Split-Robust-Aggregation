# Tables S1–S3

Every table is extracted from files already in the repository. Scripts: `make_S1.py` (S1) and `make_S2_S3.py` (S2, S3). Run from the repository root with `python3 tables/<script>.py`.

| table | cited in the paper at | file | rows |
|---|---|---|---:|
| S1 | Sec. V-C | `S1_coverage_thresholds.csv` | 160 |
| S2 | Sec. VII-D | `S2_portscan_dp_eps3.csv` | 43 |
| S3 | Table V | `S3_class_counts.csv` | 14 |
| (check for Fig. 11b) | Fig. 11b | `rr_kstar_check.csv` | 72 |

## Table S1 (Sec. V-C): coverage thresholds for L<sub>T</sub> factors 0.5–0.9

- **Source:** `results/{cicids2017,cse2018}/v3_2/expA_kstar_<target>.csv` (5 files × 32 rows: 5 target/dataset pairs × 8 aggregation rules × f ∈ {0,1,2,4}) and `results/{cicids2017,cse2018}/v3_2/expA_runs.csv` (filter: `eps = inf`, `binary = False`, `rmult = 1`; 5 seeds in every cell).
- **Columns:** `dataset`, `target`, `rule` (code names, see the main README), `f`, `kstar_0.5`, `kstar_0.6`, `kstar_0.7`, `kstar_0.8`, `kstar_0.9` (coverage threshold k̂\* at learning threshold L<sub>T</sub> = factor × reference recall; `never` = not reached on the grid).
- **Origin of each column:**
  - `kstar_0.5`, `kstar_0.8`: stored by the notebook (`kstar_05` and `kstar` in `expA_kstar_<target>.csv`).
  - `kstar_0.6`, `kstar_0.7`, `kstar_0.9`: derived from `expA_runs.csv` with the notebook's own function.
- **How the derived columns were made:** `make_S1.py` contains the notebook's `estimate_kstar`, copied verbatim, and checks at run time that it is identical to the exported v3.2 scripts. Per target, rule and f it averages target recall over the 5 seeds at each k, as the notebook does, and takes the reference recall of FedAvg at f = 0, k = 16. It first reproduces the stored `kstar_0.5` and `kstar_0.8` and stops unless all 160 rows match exactly (they do). `python3 tables/make_S1.py --selftest` runs the function on small synthetic curves (non-monotone recall, a tie at L<sub>T</sub>, a missing k, a missing seed, NaN values, empty input).

## Table S2 (Sec. VII-D): Portscan under differential privacy, ε = 3

- **Source:** `results/cicids2017/mit2/mit2_runs.csv` (`exp = M5`, `target = Portscan`, `f = 0`, `eps = 3`, seeds 0–2) and the "M5" tables of `results/cicids2017/mit2/CLAIMS_SUMMARY_MIT2_cicids2017.md`.
- **Columns:** `dataset`, `target`, `eps`, `f`, `agg` (rule), `arm` (`base` or `sra`), `k`, `n_seeds`, `mean_target_recall`, `recall_seed0`, `recall_seed1`, `recall_seed2`, `kstar_stored` (coverage threshold k̂\* copied from the notebook's printed table; on the grid {1,2,3,4,6,8,16} a value of 6 means 5–6), `tax_vs_fedavg_dp_stored`, `kstar_note`, `dp_reference_recall`, `learnable_line_stored`, `source_runs`, `source_summary`.
- **Reference:** DP reference recall (FedAvg, ε = 3, k = 16) is 0.8770 in the runs file and 0.877 in the summary; the learning threshold printed by the notebook is 0.702. FedAvg has only the `base` arm; its `k = 16` row is the reference. `mean_target_recall` matches the printed two-decimal table for all 42 (rule, arm, k) cells.

## Table S3 (Table V): class counts after cleaning

- **Source:** the "Final class counts (train / test)" lines in the saved output of `notebooks/cicids2017/01_v3_2_baseline_resume.ipynb` and `notebooks/cse2018/01_v3_2_baseline_continue_full2.ipynb`.
- **Columns:** `dataset`, `class`, `final_train`, `final_test`, `source_file`.
- **Note:** these are the capped splits, not the full cleaned counts: stratified 30 % test split with the test set capped at 30,000 Normal and 5,000 per other class, and, for CSE-CIC-IDS2018, training pools capped at 1,000,000 Normal and 300,000 per other class after benign flows were sampled at rate 0.035. CSE-CIC-IDS2018 has no Portscan class.

## Check for Fig. 11b: randomized coverage flag

- **Script:** `check_rr_kstar.py`. It reads `results/{cicids2017,cse2018}/mit2/mit2_runs.csv` (`exp = M3`, arms `sra_rr1` and `sra_rr3`, seeds 0–2) and writes `rr_kstar_check.csv`. It executes the notebook functions `ks_from`, `estimate_kstar`, `rr_predicted_kstar`, `rr_prob_kstar` (with the one-line fix) and `rr_match` verbatim from `scripts/cicids2017/04_mit3_defense_aware.py`; it adds no logic.
- **Columns:** `dataset`, `target`, `eps_w`, `f`, `rule`, `n_seeds`, `reference_recall`, `measured_kstar`, `interval_low`, `interval_high`, `pred_expected`, `pred_binomial`, and boolean columns for within one or two clients and below, above or between the predictions.
- **Reading:** a measured k̂\* of m on the grid {1,2,3,4,6,8} means the interval (previous grid point, m]; a predicted k of 9 or more is beyond the grid and counts as "never".
- **Provenance:** recomputed, not a stored run output. The saved logs and `CLAIMS_SUMMARY` files still show the original failed re-analysis.
