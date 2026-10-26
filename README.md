# Rare-Class Learning under Byzantine Robustness & Privacy in Federated Network Intrusion Detection: Coverage Bounds & Split Robust Aggregation

Code and results for the paper above. The notebooks train federated intrusion detectors on corrected CICIDS2017 and CSE-CIC-IDS2018 and measure, for each rare attack class, how many honest covering clients a federation needs before the global model learns the class, under Byzantine-robust aggregation, differential privacy and attacks.
The repository holds the notebooks (canonical source), verbatim `.py` exports, every saved result file, and the extra tables S1–S3 cited in the paper. No experiment has to be re-run to read the results.
<img width="951" height="201" alt="methodlogy drawio" src="https://github.com/user-attachments/assets/0c80dac3-d4fa-4e34-9047-41eb55b1479b" />

## Start here (first-time reader)

1. **The question.** A rare attack class is held by only `k` of the `N` = 20 clients. How large must `k` be before the global model learns that class? That number is the coverage threshold k̂\*. The paper measures it for eight aggregation rules, with and without attackers (f), with and without differential privacy, and proposes SRA to lower it.
2. **Find a number from the paper.** Open the table "Paper → code → results" below. Each row names the notebook that produced the numbers and the file and rows that hold them.
3. **Re-run an experiment.** See "How to run". The saved results make this optional.

### Reading the result CSVs

Columns that appear in the run files (`expA_runs.csv`, `mit_runs.csv`, `mit2_runs.csv`, `mit3_runs.csv`):

| column | meaning |
|---|---|
| `exp` | experiment id (EXP-A, M0 … M9). `REF` = the reference run: FedAvg, f = 0, k = 16, no privacy; L<sub>T</sub> is 0.8 × its mean recall |
| `target` | the rare attack class being learned |
| `k`, `f` | number of covering clients and of attackers |
| `agg` | aggregation rule (code names above); `arm` = SRA variant or `base` (the rule without SRA); `attack` = attacker strategy |
| `eps` | privacy setting: `inf` = no privacy, `-1` = clipping only (control), otherwise the DP budget ε |
| `seed` | random seed (0–4) |
| `target_recall` | recall on the target class, averaged over the last two evaluations of training (rounds R − 5 and R) |
| `target_to_normal` | share of target flows classified as Normal |
| `benign_fpr` | false-positive rate on benign flows |
| `other_attack_recall_mean`, `recall_<class>` | recall on the non-target attack classes (mean, or per class) |
| `sra_clip_hit_rate`, `witness_dist_over_tau` | share of rounds where the claimant correction was clipped; distance of covering clients' updates from a_H in units of τ |
| `target_recall_R`, `target_recall_2R` (`mit_runs.csv`, M0) | recall at R and 2R rounds; there `target_recall` is the recall at 3R |

The `kstar_*.csv` and `expD_*.csv` files are summary tables of these runs and carry their own column names.

## Layout

| path | content |
|---|---|
| `notebooks/<dataset>/` | the eight notebooks (`01_…` to `04_…`), numbered in run order (`cicids2017`, `cse2018`) |
| `scripts/<dataset>/` | verbatim `.py` export of each notebook's single code cell (same names; the notebooks stay canonical) |
| `results/<dataset>/{v3_2,mit1,mit2,mit3}/` | saved outputs of each stage: run CSVs, calibration JSONs, `CLAIMS_SUMMARY_*.md`, and a `figures` folder of PDFs |
| `analysis/` | the two scripts that turn the result CSVs into figures and tables (`witness_analysis.py`, `witness_analysis_mit3.py`) |
| `tables/` | tables S1–S3 and the scripts that built them (`tables/README.md`) |
| `data/README.md` | dataset source, input paths, cleaning steps (no data files) |
| `MAPPING.md` | old path → new path for every moved file |

Result file names inside `results/` are unchanged from the notebooks' own output names (mixed case), because the notebooks read and write those exact names when resuming and chaining. Only the folder names changed (`witness_mit2_cicids2017` → `results/cicids2017/mit2`).

## Terms: paper term (code name)

The paper's terms are used in the prose. The names that appear in the notebooks, logs and result files are given once in brackets.

- **covering clients** (code: "witnesses"): honest clients that hold the target class. **Coverage** `k`: their number. **f**: number of attackers who copy the target traffic but label it Normal. **N** = 20 clients.
- **coverage threshold** k̂\*<sub>R</sub> (code: `k*`, `kstar`): smallest `k` at which the global model learns the class within the round budget R.
- **learning threshold** L<sub>T</sub> (code: "learnable line"): 0.8 × the reference recall (FedAvg, f = 0, k = 16, non-private, same seeds).
- **lower bound** f + 1 (code: "P1 floor").
- **blind spot** (code: "wall") and **delay**: a cell that stays below L<sub>T</sub> even with 3R rounds (blind spot) versus one that learns with more rounds (delay); experiment EXP-D.
- **F̂** (code: `F_HAT`, = 2): the number of attackers the robust rules are configured to tolerate.
- The code's "witness tax" is `k* − (f+1)`, the distance above the lower bound. The paper's **robustness shift** (Definition 4) is `k*(A,0) − k*(FedAvg,0)`, rule A versus FedAvg at f = 0. These are different quantities.
- **SRA**, Split Robust Aggregation: each member sends one **coverage flag** `b` ("I have evidence of the target class"), optionally randomized. The **claimants** `W` (members whose flag is set) are aggregated by the coordinate-wise median; the **non-claimants** `H` (flag not set) by the base robust rule; the claimant result is clipped to the **cap multiplier** `λ_W` (= 3, pre-registered) times the **reference radius** `τ` (code: "honest radius") before it is added.
- **WAA**, witness-aware aggregation (mit-1 stage): members report one bit "I have seen this class"; reporting members bypass the robust rule and are clipped to lambda × the honest radius.
- Aggregation rules (code names): `fedavg`, `cwmed` (coordinate-wise median), `trmean` (trimmed mean), `mkrum` (Multi-Krum), `geomed` (geometric median), `bucket_cwmed` (bucketing), `cclip` (centered clipping), `nnm_cwmed` (nearest-neighbour mixing, then coordinate-wise median).
- SRA arms: `sra`, `sra_l10` (post-hoc diagnostic, λ_W = 10), `sra_rand` (random claimants), `sra_rr1` / `sra_rr3` (randomized-response flag, ε_w = 1 / 3), `sra_cap` (claimant weight capped at 2·F̂+1 members), `orcinf` (claimants summed without clipping), `elect` (only the class's own output row is aggregated over claimants).
- Attacks: `mimic`, `signflip` (×10), `alie` (z = 1), `fang_w` / `fang_h`, `minmax_w` / `minmax_h`, `alie_w`, `split`; `_w` = inside W, `_h` = inside H; the suffix `_nc` = attackers do not claim.

## Notebooks and stages

| stage | notebook (`notebooks/<dataset>/`) | experiments (the notebooks' own names) |
|---|---|---|
| v3.2 baseline | `01_v3_2_baseline_resume` (CICIDS2017), `01_v3_2_baseline_continue_full2` (CSE-CIC-IDS2018) | EXP-A (grid of target recall over k, f and 8 aggregation rules), EXP-QA (missed vs mislabelled), EXP-D (blind spot or delay), EXP-K0 (zero-coverage control), EXP-B (differential privacy), EXP-C (natural day-split clients) |
| mit-1 | `02_mit1_waa_mechanism` | M0 (mechanism check: does the blind-spot edge follow F̂?), M1 (mitigation: WAA), M2 (robustness cost of WAA) |
| mit-2 | `03_mit2_sra_continue` (CICIDS2017), `03_mit2_sra` (CSE-CIC-IDS2018) | SRA: M3 (coverage, with ablation arms), M4 (robustness), M5 (differential privacy, ε = 3) |
| mit-3 | `04_mit3_defense_aware` | M3c (`sra_cap`), M6 (defense-aware attacks on SRA), M7 (does moderate DP, ε = 3, let attackers in?), M8 (lower bound measured directly at k = 5, f = 4), M9 (seeds 3–4: 5-seed k* with bootstrap intervals), re-analysis of mit-2 |

Targets: CICIDS2017 v3.2 = Botnet, Portscan, Brute Force; mit-1/2/3 = Botnet, Portscan. CSE-CIC-IDS2018 = Brute Force, Botnet (all stages).

## Paper → code → results

Figs 1, 2, 7, 8 and Tables I–IV, VI are schematic or text only and have no data here. The numbers behind each paper figure are in the files and rows listed below. The scripts in `analysis/` regenerate figures and tables from these files; see "Paper figures → analysis scripts" for which paper figure each script figure corresponds to (Fig. 4 and the panels of Fig. 9 have no script figure). Fig. 4 and Fig. 3 come from different runs (mit-2, 3 seeds, versus v3.2, 5 seeds), so L<sub>T</sub> for CICIDS2017 Botnet differs slightly between them (0.752 in Fig. 4, 0.753 in the v3.2 runs, 0.754 in mit-3) and so can FedAvg's k̂\* (1 in Fig. 4, 2 in `expA_kstar_Botnet.csv`), as the paper states in Sec. V. Unless a row says otherwise, "`<ds>`" is `cicids2017` or `cse2018` and rule names are the code names above.

| Paper item | What it shows | Notebook | File and rows (filter) |
|---|---|---|---|
| **Sec. V** | | | |
| Table V (setup) | round budgets R = 105, 105, 85, 50, 30; calibration seed 99; grids; DP clip 5.0, lr 0.5, ε ∈ {10, 3, 1}, δ = 1e-5 | `01_v3_2_*` | `results/<ds>/v3_2/calibration_<target>_M500.json` (`rounds`, `dp_clip`, `dp_lr`), `config_FULL.json` (grids, seeds, ε grid, δ); calibration seed 99 is a constant in the notebook; class counts: Table S3 |
| Fig. 3, Sec. V-C | k̂\* at f = 0: FedAvg 1–2, seven robust rules 3–10; CICIDS2017 Botnet FedAvg 2, trimmed mean 3, Multi-Krum 4 | `01_v3_2_*` | `results/<ds>/v3_2/expA_kstar_<target>.csv`, `f = 0`, column `kstar` (data: `expA_runs.csv`) |
| Sec. V-C | CICIDS2017 benign FPR 0.0011–0.0015 for every rule | `01_v3_2_baseline_resume` | `results/cicids2017/v3_2/expA_runs.csv`, `f = 0`, `eps = inf`, `binary = False`, `rmult = 1`; mean `benign_fpr` per target and rule |
| **Fig. 4** | CICIDS2017 Botnet, target recall vs k at f = 0, grid {1,2,3,4,6,8}, 3 seeds, base rules: FedAvg k̂\* = 1, trimmed mean 3, Multi-Krum 4, coordinate median 8; L<sub>T</sub> = 0.752 | `notebooks/cicids2017/03_mit2_sra_continue.ipynb` | `results/cicids2017/mit2/mit2_runs.csv`: `exp = M3`, `target = Botnet`, `f = 0`, `arm = base`, `agg ∈ {fedavg, trmean, mkrum, cwmed}`, seeds 0–2. L<sub>T</sub> = 0.8 × mean of the `exp = REF` Botnet rows (0.9402) |
| Sec. V-C | below the coverage threshold, 80–97 % of target flows are classified Normal on four targets, 48 % on CSE-CIC-IDS2018 Brute Force | `01_v3_2_*` | `results/<ds>/v3_2/expQA_taxcells_<target>.csv`, column `to_normal` (mean over cells); data `expQA_runs.csv` |
| Sec. V-B (Assumption 7) | zero-coverage control: the target is flagged as some attack in at most 6 % of flows (multiclass model), 0 on three targets | `01_v3_2_*` | `results/<ds>/v3_2/expK0_<target>.csv`, model `multiclass(any-attack)`, column `k=0 detection` |
| Sec. V-C, Table S1 | coverage threshold for L<sub>T</sub> factors 0.5–0.9 over 160 combinations | `01_v3_2_*` | `tables/S1_coverage_thresholds.csv` |
| **Sec. V-D** | | | |
| Fig. 5 | blind-spot edge vs F̂ ∈ {1..4}, trimmed mean / Multi-Krum / NNM, 4 targets, 3R, grid {1..6,8,10}, 3 seeds: edge = F̂ in 46 of 48 (exceptions: trimmed mean, CICIDS2017 Botnet, F̂ = 3 and 4) | `02_mit1_waa_mechanism` | `results/<ds>/mit1/mit_runs.csv`, `exp = M0`; edge = k̂\*(3R) − 1 from column `target_recall` (`rmult = 3`) |
| Fig. 6, Sec. V-D | at F̂ = 2: blind-spot edge 2 and k̂\*<sub>3R</sub> = 3 for trimmed mean, Multi-Krum, NNM on all 5 targets; other rules' edges: centered clipping 1–2, geometric median 1–3, bucketing 2–4, coordinate median 3–7 | `01_v3_2_*` | `results/<ds>/v3_2/expD_summary_<target>.csv` (columns `k*(3R)`, `WALL at k`); `expD_<target>.csv`, `expD_runs.csv` |
| **Sec. VI-A** | | | |
| λ_W = 3 | development runs with oracle claimants; distance of covering clients' updates from a_H in units of τ | `02_mit1_waa_mechanism` | `results/<ds>/mit1/mit_runs.csv`, `exp = M1`, arms `orc1`, `orc10`, `orcinf`, column `witness_dist_over_tau`; also `results/<ds>/mit2/mit2_runs.csv`, arm `orcinf` |
| **Sec. VII-A and Figs 9–10** | | | |
| Fig. 10a, Sec. VII-A | 5 seeds; SRA k̂\* = 3 in 12 of 12 pairs at f = 2 (bootstrap [3,3]); base rules 4–8 in 10 pairs, never in 2; FedAvg 3–6; at f = 0 SRA 1–2, base rules 3–8 (never in 2), SRA = 1 in 2 of 12; at f = 4 SRA is 6 on the grid in 12 of 12 (k = 5 is not on the grid; k = 4 reaches L<sub>T</sub> in 0 of 12) | `03_mit2_*` (seeds 0–2), `04_mit3_defense_aware` (seeds 3–4) | `results/<ds>/mit2/mit2_runs.csv`, `exp = M3`, arms `base`, `sra`; `results/<ds>/mit3/mit3_runs.csv`, `exp = M9`; bootstrap table "M9 k\* point [5%, 95%]" in `results/<ds>/mit3/CLAIMS_SUMMARY_MIT3_<ds>.md` |
| Fig. 10b | k = 5, f = 4: SRA reaches L<sub>T</sub> in 12 of 12 (recall 0.817–1.000); FedAvg fails on 4 of 4; base rules reach it in 1 of 12; coordinate median 0 of 4 | `04_mit3_defense_aware` | `results/<ds>/mit3/mit3_runs.csv`, `exp = M8` |
| Fig. 9a | random claimants: f = 0 k̂\* 3–8 (never in 2 of 12); f = 2 4–8 (never in 2) | `03_mit2_*` | `results/<ds>/mit2/mit2_runs.csv`, `exp = M3`, `arm = sra_rand` |
| Fig. 9b | claimant vote vs sum: under claiming sign-flip at k = 6, SRA (median vote) is no worse than its base rule in 11–12 of 12 pairs, the sum in at most 1 of 12; over the 4 attacks at k = 6, f = 4: sum 28 of 48, SRA 38 of 48 | `03_mit2_*` | `results/<ds>/mit2/mit2_runs.csv`, `exp = M4`, `k = 6`, `f ∈ {2, 4}`, arms `sra` (median) and `orcinf` (sum, unclipped), attacks `signflip`, `signflip_nc`, `alie`, `alie_nc`. "No worse than base" is the notebook's paired verdict (function `m4_paired_verdict`): benign FPR not above base + 0.05 and other-class recall not below base − 0.05, with the 0.05 FPR cap; counted per (target, base rule) pair |
| Fig. 9c | cap multiplier λ_W = 3 vs 10: at k = 1, f = 0 learns in 2 vs 9 of 12; claimant result clipped in 15–24 % of rounds at f = 0; at k = 2, f = 4 no worse than base in 5 vs 0 of 12 | `03_mit2_*` | `results/<ds>/mit2/mit2_runs.csv`, arms `sra`, `sra_l10`, `exp = M3` and `M4`; column `sra_clip_hit_rate` |
| Fig. 9d | aggregating only the output row: k̂\* 1–6 at f = 0; reaches the lower bound in 3 of 12 vs 12 of 12 for SRA at f = 2 | `03_mit2_*` | `results/<ds>/mit2/mit2_runs.csv`, `exp = M3`, `arm = elect` (vs `sra`) |
| **Sec. VII-B** | | | |
| Sec. VII-B | SRA reaches L<sub>T</sub> in 40 of 48 at k = 6, f = 4 and 16 of 48 at k = 2, f = 4 | `03_mit2_*` | `results/<ds>/mit2/mit2_runs.csv`, `exp = M4`, `arm = sra`, attacks `signflip`, `signflip_nc`, `alie`, `alie_nc` |
| **Sec. VII-C** | | | |
| Sec. VII-C | 144 defense-aware cells at f = 2: SRA benign FPR 0.001–0.004, at most base + 0.001; other-class recall drop at most 0.006; CSE-CIC-IDS2018 coordinate median under Fang 0.914 → 0.959 | `04_mit3_defense_aware` | `results/<ds>/mit3/mit3_runs.csv`, `exp = M6`, `f = 2`, `k ∈ {3, 6}`, `arm ∈ {base, sra}` |
| Sec. VII-C | no attacker, CSE-CIC-IDS2018 Brute Force, coordinate median, k = 6: other-class recall 0.948 → 0.924, Web Attack 0.802 → 0.706 | `03_mit2_sra` | `results/cse2018/mit2/mit2_runs.csv`, `exp = M3`, `target = Brute Force`, `agg = cwmed`, `f = 0`, `k = 6`, `arm ∈ {base, sra}`; columns `other_attack_recall_mean`, `recall_Web Attack` |
| **Sec. VII-D** | | | |
| Fig. 11a, Sec. VII-D | privacy: k̂\* is U-shaped in ε; coordinate median CICIDS2017 Botnet 7–8 → 3, CSE-CIC-IDS2018 Brute Force 9–12 → 2; clip-only changes little; ε = 1: FedAvg 5–6, coordinate median 13–16 (CICIDS2017 Botnet) | `01_v3_2_*` | `results/<ds>/v3_2/expB_kstar_<target>.csv` (columns `setting`, `kstar`); data `expB_runs.csv`. The ranges (7–8, 9–12, 5–6, 13–16) are the k-grid cells {…6,8}, {…8,12}, {…4,6}, {…12,16} |
| Sec. VII-D, Table S2 | Portscan at ε = 3: coordinate median and Multi-Krum 5–6, FedAvg 4; DP reference recall 0.877 | `03_mit2_sra_continue` | `results/cicids2017/mit2/mit2_runs.csv`, `exp = M5`, `target = Portscan`; `tables/S2_portscan_dp_eps3.csv` |
| Fig. 11b | privacy cost of the coverage flag, 72 configurations: expected-majority prediction (Corollary 1) within one client in 57 and within two in 72; within one in all 36 at ε<sub>w</sub> = 1; at ε<sub>w</sub> = 3 the prediction is below the measured interval in 21 of 36. Binomial variant: above the measured interval in 24 of 36 at ε<sub>w</sub> = 1; the measured value lies between the two predictions in 59 of 72 | `03_mit2_*` and `04_mit3_defense_aware` (function `rr_prob_kstar`) | **Recomputed from `mit2_runs.csv`** with `tables/check_rr_kstar.py` (patched `rr_prob_kstar`); the numbers are stored in `tables/rr_kstar_check.csv`, one row per configuration. Source rows: `results/<ds>/mit2/mit2_runs.csv`, `exp = M3`, `arm = sra_rr1` (ε<sub>w</sub> = 1) and `sra_rr3` (ε<sub>w</sub> = 3), rules `cwmed`, `trmean`, `mkrum`, `f ∈ {0, 2, 4}`, seeds 0–2. Predicted k, expected-count / binomial, for f = 0, 2, 4: ε<sub>w</sub> = 3: 1, 3, 5 / 3, 5, 6; ε<sub>w</sub> = 1: 6, 7, 9 / 8, 9, 11. **Reading:** a measured k̂\* of m on the grid {1,2,3,4,6,8} means the true value lies in (previous grid point, m]; a predicted k of 9 or more, such as 11, is beyond the grid maximum of 8 and counts as "never". **Provenance:** the saved logs and the `CLAIMS_SUMMARY_MIT3_*.md` files still show the original re-analysis failing with an IndexError; the binomial numbers were not in those outputs and exist only through the recomputation above. The expected-count tables "M3 RR formula k\*" in `CLAIMS_SUMMARY_MIT2_<ds>.md` are original run output |
| Sec. VII-D | k = 6, f = 2, ε = 3: ALIE gives recall 0 on 3 of 4 targets (base and SRA); without DP base 0.663–0.875 and SRA 0.906–1.000 | `04_mit3_defense_aware` | `results/<ds>/mit3/mit3_runs.csv`, `exp = M7`, `attack = alie`, `eps ∈ {3.0, inf}`; per-target mean over `cwmed`, `trmean`, `mkrum` |
| **Sec. VII-E** | | | |
| Fig. 12, Sec. VII-E | f = 2, k ∈ {3, 6}: SRA mean target recall 0.938–0.953 per attack vs base 0.379–0.638; L<sub>T</sub> reached in 143 of 144, no worse than base in 144 of 144; the one miss is trimmed mean, CICIDS2017 Botnet, Fang from H, below L<sub>T</sub> by less than 0.001 | `04_mit3_defense_aware` | `results/<ds>/mit3/mit3_runs.csv`, `exp = M6`, `f = 2`, `k ∈ {3, 6}`; base for `fang_h` is the `fang_w` base run |
| Sec. VII-E | k = 6, f = 4: L<sub>T</sub> in 67 of 72, no worse than base in 71 of 72 (4 of 5 failures: Fang from H); k = 2, f = 4: L<sub>T</sub> in 55 of 72, no worse in 69 of 72 | `04_mit3_defense_aware` | `results/<ds>/mit3/mit3_runs.csv`, `exp = M6`, `(k, f) ∈ {(6, 4), (2, 4)}` |
| **Tables S1–S3** | | | |
| Table S1 (Sec. V-C) | coverage thresholds, 5 targets × 8 rules × f ∈ {0,1,2,4}, for L<sub>T</sub> factors 0.5–0.9 | `01_v3_2_*` | `tables/S1_coverage_thresholds.csv` |
| Table S2 (Sec. VII-D) | Portscan ε = 3: recall vs k for 4 rules, k̂\*, DP reference | `03_mit2_sra_continue` | `tables/S2_portscan_dp_eps3.csv` |
| Table S3 (Table V) | per-class train/test counts after cleaning (capped splits) | `01_v3_2_*` | `tables/S3_class_counts.csv` |

## Analysis scripts (`analysis/`)

Two scripts turn the result CSVs into figures and tables. They need `matplotlib` and `tabulate` and no GPU.

```
cd analysis
python witness_analysis.py \
  --csv17 ../results/cicids2017/mit2/mit2_runs.csv --csv18 ../results/cse2018/mit2/mit2_runs.csv \
  --out ../analysis_output
python witness_analysis_mit3.py \
  --m2_17 ../results/cicids2017/mit2/mit2_runs.csv --m2_18 ../results/cse2018/mit2/mit2_runs.csv \
  --m3_17 ../results/cicids2017/mit3/mit3_runs.csv --m3_18 ../results/cse2018/mit3/mit3_runs.csv \
  --out ../analysis_output
```

Use an output folder other than `results/` (the default `--out results` would write next to the saved results). The second script imports the first, so run both from `analysis/`. Output, inside the output folder (git-ignored and separate from the repository's `tables/` folder): a `figures` folder with `fig00` to `fig14` as PDF and PNG (300 dpi) and a `tables` folder with `T1` to `T9` as CSV and Markdown. Both scripts were run on the files in this repository without errors.

**Where each figure's numbers come from.** Computed means rows read from the CSVs. Transcribed means the numbers are typed into the script as constants, copied from the logs of the first two stages. Each transcribed constant was compared with the stored CSVs and is equal to them (counts below).

| script figure | what it plots | numbers come from |
|---|---|---|
| `fig00_story_arc` | summary strip of the study (the second script overwrites the first script's version) | text only; the counts in the boxes (for example 46/48, 48/48, 144/144) are typed in |
| `fig01_setup_and_sra` | schematic of the setting and of SRA | schematic |
| `fig02_floor_and_witness_tax` | k̂\* against f for FedAvg and three base rules | computed: `mit2_runs.csv`, `exp = M3`, `arm = base` |
| `fig03_witness_tax_8_aggregators` | heatmap of `k* − (f+1)` at f = 0, 8 rules × 5 targets | transcribed (`V3_TAX`); equal to `expA_kstar_<target>.csv`, `f = 0`, columns `kstar`, `tax` (10 of 10 comparisons) |
| `fig04_wall_not_delay_and_fhat` | (a) k̂\* at R, 2R, 3R; (b) blind-spot edge against F̂ | transcribed: (a) `V3_ROUNDS`, equal to `expD_summary_<target>.csv` (35 of 35); (b) `M0`, equal to a recomputation from `mit_runs.csv`, `exp = M0` (12 of 12); the "46/48" in the panel title is counted by the script from these constants |
| `fig05_dp_u_shape` | k̂\* by privacy setting at f = 0, three targets | transcribed (`V3_DP`); equal to `expB_kstar_<target>.csv` (12 of 12) |
| `fig06_sra_recovers_coverage` | target recall against k, f ∈ {0,2,4}, SRA and comparison arms | computed: `mit2_runs.csv`, `exp = M3` |
| `fig07_coverage_robustness_frontier` | coverage cost against worst-attack other-class recall | computed: `mit2_runs.csv`, `exp = M3` and `M4` |
| `fig08_rr_privacy_price` | (a) predicted k against ε<sub>w</sub>; (b) predicted against measured k̂\* | computed: `mit2_runs.csv`, `exp = M3`, arms `sra_rr1`, `sra_rr3`; the script carries its own copy of the prediction formula |
| `fig09_robustness_map` | share of cells where SRA and three other arms are no worse than the base rule, per attack | computed: `mit2_runs.csv`, `exp = M4` |
| `fig10_dp_times_sra` | target recall under ε = 3 | computed: `mit2_runs.csv`, `exp = M5` |
| `fig11_adaptive_attacks` | recall under six defense-aware attacks; robustness by zone | computed: `mit3_runs.csv`, `exp = M6` |
| `fig12_dp_arms_the_attacker` | recall under ALIE and Fang with and without ε = 3 | computed: `mit3_runs.csv`, `exp = M7` |
| `fig13_floor_measured_k5` | recall at k = 5, f = 4 | computed: `mit3_runs.csv`, `exp = M8` |
| `fig14_kstar_5_seeds` | k̂\* with 90% bootstrap interval, 5 seeds | computed: `mit2_runs.csv` (`M3`, seeds 0–2) and `mit3_runs.csv` (`M9`, seeds 3–4) |
| tables `T1 … T5` | k̂\* of all arms; lower-bound check; robustness by zone; SRA failures; k̂\* at ε = 3 | computed from `mit2_runs.csv` |
| tables `T6 … T9` | adaptive attacks; ALIE and Fang with DP; k = 5, f = 4; k̂\* with bootstrap interval | computed from `mit3_runs.csv` (and `mit2_runs.csv` for T9) |

## Paper figures → analysis scripts

"Same data" means the script figure is built from the same numbers as the paper figure; the layout may differ. The script figure files are not stored in the repository; they are created by the commands above.

| Paper figure | Script figure (file produced) | Relation | Source data |
|---|---|---|---|
| Figs 1, 2, 8 | none | schematic | none |
| Fig. 3 | `fig03_witness_tax_8_aggregators` | same data, heatmap instead of dots | `expA_kstar_<target>.csv`, `f = 0` |
| Fig. 4 | none | not produced by the scripts | `mit2_runs.csv`, rows listed in the table above |
| Fig. 5 | `fig04_wall_not_delay_and_fhat`, panel (b) | same data, one panel instead of three | `mit_runs.csv`, `exp = M0` |
| Fig. 6 | `fig04_wall_not_delay_and_fhat`, panel (a) | same data, mean and range over targets | `expD_summary_<target>.csv` |
| Fig. 7 | `fig01_setup_and_sra`, panel (b) | different drawing of the same method | none |
| Fig. 9a | table `T1`, column `sra_rand` | table only | `mit2_runs.csv`, `exp = M3`, `arm = sra_rand` |
| Fig. 9b | `fig09_robustness_map` | same counts, heatmap instead of bars | `mit2_runs.csv`, `exp = M4`, arms `orcinf`, `sra` |
| Fig. 9c | `fig09_robustness_map`, arms `sra` and `sra_l10` at k = 2, f = 4 | the k = 1 learning counts and the clip rates are not produced by the scripts | `mit2_runs.csv`, `exp = M3` and `M4`, column `sra_clip_hit_rate` |
| Fig. 9d | table `T1`, column `elect` | table only | `mit2_runs.csv`, `exp = M3`, `arm = elect` |
| Fig. 10a | `fig14_kstar_5_seeds`, table `T9` | same data; the figure shows SRA on the coordinate median, `T9` has all rules | `mit2_runs.csv` (`M3`) and `mit3_runs.csv` (`M9`) |
| Fig. 10b | `fig13_floor_measured_k5`, table `T8` | same data; the script averages the three base rules, the paper shows each | `mit3_runs.csv`, `exp = M8` |
| Fig. 11a | `fig05_dp_u_shape` | same data and panels | `expB_kstar_<target>.csv`, `f = 0` |
| Fig. 11b | `fig08_rr_privacy_price`, panel (b) | same data; the binomial variant is not in the script | `mit2_runs.csv`, `exp = M3`; `tables/rr_kstar_check.csv` |
| Fig. 12 | `fig11_adaptive_attacks`, panel (a), table `T6b` | same data | `mit3_runs.csv`, `exp = M6`, `f = 2` |

## Diagnostic figures saved by the notebooks

The PDFs in `results/<dataset>/<stage>/figures/` are run diagnostics, not the paper figures.

| file | stage | what it plots |
|---|---|---|
| `A1_phase_<target>.pdf` | v3.2 | target recall over k and f for each aggregation rule (EXP-A) |
| `A2_recall_vs_k_<target>.pdf` | v3.2 | target recall vs k per f, all rules (EXP-A) |
| `A3_tax_<target>.pdf` | v3.2 | `k* − (f+1)` per rule |
| `QA1_<target>.pdf` | v3.2 | detection (any attack) by the multiclass and the binary model (EXP-QA) |
| `B1_dp_<target>.pdf` | v3.2 | target recall vs k under differential privacy (EXP-B) |
| `C1_natural_daylock.pdf` | v3.2 | recall with natural day-split clients (EXP-C) |
| `M0_wall_vs_fhat_<target>.pdf` | mit-1 | blind-spot edge at 3R vs F̂ (M0) |
| `M3_coverage_<target>.pdf` | mit-2 | target recall vs k per rule and f, SRA arms against the base rule (M3) |
| `M6_adaptive_<target>.pdf` | mit-3 | share of M6 cells where SRA is no worse than base, per arm, k, f and attack |

## How to run

Each notebook is one self-contained code cell. It needs a GPU, internet access on the first run (it installs `opacus` if missing), the dataset attached as input (see `data/README.md`), and, for stages after v3.2, the output folder of the stage it builds on attached as an input.

1. **Phase 0 self-tests run first** in every notebook (synthetic, deliberately messy data) and print `PHASE 0 RESULT: ALL PASSED`. The notebooks also check their pre-flight gates (G1 calibration convergence, G6 floor gate) before any grid.
2. **Run order per dataset** (`notebooks/<dataset>/`): `01` → `02` → `03` → `04`.
   - `02` imports the calibration JSONs of `01`. `03` imports calibration JSONs from an attached `01` output (preferred) or `02` output (fallback); in the logged CSE-CIC-IDS2018 run they came from `02`. `04` imports calibration JSONs and `mit2_runs.csv` from the attached `03` output.
   - The CSE-CIC-IDS2018 notebooks also reuse `data_cache.npz` from an attached earlier output instead of re-reading the 35 GB source.
3. **Resumed notebooks.** `01_v3_2_baseline_resume`, `01_v3_2_baseline_continue_full2` and `03_mit2_sra_continue` are the last session of a run that was continued across sessions. A session stops cleanly after `TIME_BUDGET_H = 11.0` h. To continue, attach the previous output as an input and run again: all `*.csv` and `*.json` files of the earlier output are copied into the new output folder, and every configuration whose resume key (`VERSION` + `cfg_id`) is already present is skipped. The result folders in this repository are therefore the merged outputs of all sessions. `RUN_TARGETS = ["<target>"]` runs one target per session.
4. **Environment variables** (all optional): `WITNESS_OUT` (output folder; default `witness_<VERSION>_<TAG>` in the writable working directory), `WITNESS_TARGETS` (comma-separated targets; mit-1/2/3), `WITNESS_BUDGET_H` (time budget in hours), `WITNESS_FORCE` (run grids even if pre-flight gates fail; not for paper numbers). Developer switches: `WITNESS_SMOKE`, `WITNESS_DATA`, `WITNESS_REFMIN`, `WITNESS_SKIP_P0`. `DATA_PATH` is **not** an environment variable; it is a constant at the top of each notebook (`None` = search for the dataset automatically).

## Seeds

- **5 seeds (0–4)**: clean baselines (v3.2 EXP-A, both datasets) and the main SRA result: mit-2 M3 seeds 0–2 plus mit-3 M9 seeds 3–4 (`mit3_runs.csv`, `exp = M9`, arms `base`, `sra`, `sra_l10`, k ∈ {1,2,3,4,6,8}, f ∈ {0,2,4}). The SRA ablation arms (`orcinf`, `elect`, `sra_rand`, `sra_rr1`, `sra_rr3`) stay at 3 seeds.
- **3 seeds (0–2)**: everything else: EXP-B (DP), EXP-QA, EXP-D, EXP-K0, mit-1 M0/M1/M2, mit-2 M3/M4/M5, mit-3 M3c/M6/M7/M8.

## Feature scaling

Non-finite values are replaced by the training median, then signed `log1p`, then z-score with training mean and standard deviation (clipped to [-10, 10]).

## Known gaps

- Package versions are not pinned in `requirements.txt` (no log records them).
- Fig. 4 and the panels of Fig. 9 have no script figure (see "Paper figures → analysis scripts").

## License

MIT. See `LICENSE`.
