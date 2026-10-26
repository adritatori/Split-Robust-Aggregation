# MAPPING — old path → new path

Every file was moved with `git mv`, so `git log --follow <new path>` shows the full history. File contents are unchanged (byte-identical, SHA-256 verified), with these exceptions: `.gitignore` was rewritten in place (it keeps its path and is not listed below), and in the mit-2 and mit-3 notebooks and their `scripts/` exports (`03_mit2_sra*`, `04_mit3_defense_aware`, both datasets) the earlier name of SRA in comments, docstrings and printed banners was changed to "Split Robust Aggregation" (text only; no code, identifier or value changed). Their SHA-256 therefore differs from the original. In addition, `04_mit3_defense_aware` (both datasets, notebook and `scripts/` export) has one code fix in `rr_prob_kstar`: `cy[x - f - 1]` became `cy[min(x - f - 1, len(cy) - 1)]`, which removes an IndexError at epsilon_w = 1, f = 4. Seven notebooks (all except `03_mit2_sra_continue`) also had a user name inside input-folder paths in their saved log output replaced by `USER`; code cells and metadata are unchanged.

File names *inside* result folders were deliberately **not** changed (mixed case such as `CLAIMS_SUMMARY_MIT2_cicids2017.md`, `calibration_Brute_Force_M500.json`), because the notebooks read and write those exact names when resuming and chaining. Only folder names were lower-cased and the `witness_` prefix dropped.

At run time the notebooks still create `witness_<VERSION>_<TAG>` output folders (e.g. `witness_mit2_cicids2017`); those names are fixed inside the code and are unaffected by this repository layout.

## Folder renames

| old folder | new folder |
|---|---|
| `witness_v3_cicids2017/` | `results/cicids2017/v3_2/` |
| `witness_mit1_cicids2017/` | `results/cicids2017/mit1/` |
| `witness_mit2_cicids2017/` | `results/cicids2017/mit2/` |
| `witness_mit3_cicids2017/` | `results/cicids2017/mit3/` |
| `witness_v3_cse2018/` | `results/cse2018/v3_2/` |
| `witness_mit1_cse2018/` | `results/cse2018/mit1/` |
| `witness_mit2_cse2018/` | `results/cse2018/mit2/` |
| `witness_mit3_cse2018/` | `results/cse2018/mit3/` |

## Notebook renames

| old file | new file |
|---|---|
| `flcicidds-17-resume.ipynb` | `notebooks/cicids2017/01_v3_2_baseline_resume.ipynb` |
| `witness-mit1-cicids2017.ipynb` | `notebooks/cicids2017/02_mit1_waa_mechanism.ipynb` |
| `witness-mit2-cicids-2017-continue.ipynb` | `notebooks/cicids2017/03_mit2_sra_continue.ipynb` |
| `witness-count-mit-3-0-cicids2017.ipynb` | `notebooks/cicids2017/04_mit3_defense_aware.ipynb` |
| `flcicid-18-continue-full-2.ipynb` | `notebooks/cse2018/01_v3_2_baseline_continue_full2.ipynb` |
| `witness-mit1-cicids2018.ipynb` | `notebooks/cse2018/02_mit1_waa_mechanism.ipynb` |
| `witness-mit2-cse-cic-ids2018.ipynb` | `notebooks/cse2018/03_mit2_sra.ipynb` |
| `witness-count-mit-3-0-cicids2018.ipynb` | `notebooks/cse2018/04_mit3_defense_aware.ipynb` |

Note: the two old names ending in `cicids2018` (`witness-mit1-cicids2018`, `witness-count-mit-3-0-cicids2018`) run **CSE-CIC-IDS2018**, as do all notebooks under `notebooks/cse2018/`.

## Every file (141 files; `.gitignore` not listed)

| old path | new path |
|---|---|
| `flcicid-18-continue-full-2.ipynb` | `notebooks/cse2018/01_v3_2_baseline_continue_full2.ipynb` |
| `flcicidds-17-resume.ipynb` | `notebooks/cicids2017/01_v3_2_baseline_resume.ipynb` |
| `witness-count-mit-3-0-cicids2017.ipynb` | `notebooks/cicids2017/04_mit3_defense_aware.ipynb` |
| `witness-count-mit-3-0-cicids2018.ipynb` | `notebooks/cse2018/04_mit3_defense_aware.ipynb` |
| `witness-mit1-cicids2017.ipynb` | `notebooks/cicids2017/02_mit1_waa_mechanism.ipynb` |
| `witness-mit1-cicids2018.ipynb` | `notebooks/cse2018/02_mit1_waa_mechanism.ipynb` |
| `witness-mit2-cicids-2017-continue.ipynb` | `notebooks/cicids2017/03_mit2_sra_continue.ipynb` |
| `witness-mit2-cse-cic-ids2018.ipynb` | `notebooks/cse2018/03_mit2_sra.ipynb` |
| `witness_mit1_cicids2017/CLAIMS_SUMMARY_MIT_cicids2017.md` | `results/cicids2017/mit1/CLAIMS_SUMMARY_MIT_cicids2017.md` |
| `witness_mit1_cicids2017/calibration_Botnet_M500.json` | `results/cicids2017/mit1/calibration_Botnet_M500.json` |
| `witness_mit1_cicids2017/calibration_Brute_Force_M500.json` | `results/cicids2017/mit1/calibration_Brute_Force_M500.json` |
| `witness_mit1_cicids2017/calibration_Portscan_M500.json` | `results/cicids2017/mit1/calibration_Portscan_M500.json` |
| `witness_mit1_cicids2017/config_mit.json` | `results/cicids2017/mit1/config_mit.json` |
| `witness_mit1_cicids2017/figures/M0_wall_vs_fhat_Botnet.pdf` | `results/cicids2017/mit1/figures/M0_wall_vs_fhat_Botnet.pdf` |
| `witness_mit1_cicids2017/figures/M0_wall_vs_fhat_Portscan.pdf` | `results/cicids2017/mit1/figures/M0_wall_vs_fhat_Portscan.pdf` |
| `witness_mit1_cicids2017/mit_runs.csv` | `results/cicids2017/mit1/mit_runs.csv` |
| `witness_mit1_cse2018/CLAIMS_SUMMARY_MIT_cse2018.md` | `results/cse2018/mit1/CLAIMS_SUMMARY_MIT_cse2018.md` |
| `witness_mit1_cse2018/calibration_Botnet_M500.json` | `results/cse2018/mit1/calibration_Botnet_M500.json` |
| `witness_mit1_cse2018/calibration_Brute_Force_M500.json` | `results/cse2018/mit1/calibration_Brute_Force_M500.json` |
| `witness_mit1_cse2018/config_mit.json` | `results/cse2018/mit1/config_mit.json` |
| `witness_mit1_cse2018/figures/M0_wall_vs_fhat_Botnet.pdf` | `results/cse2018/mit1/figures/M0_wall_vs_fhat_Botnet.pdf` |
| `witness_mit1_cse2018/figures/M0_wall_vs_fhat_Brute_Force.pdf` | `results/cse2018/mit1/figures/M0_wall_vs_fhat_Brute_Force.pdf` |
| `witness_mit1_cse2018/mit_runs.csv` | `results/cse2018/mit1/mit_runs.csv` |
| `witness_mit2_cicids2017/CLAIMS_SUMMARY_MIT2_cicids2017.md` | `results/cicids2017/mit2/CLAIMS_SUMMARY_MIT2_cicids2017.md` |
| `witness_mit2_cicids2017/calibration_Botnet_M500.json` | `results/cicids2017/mit2/calibration_Botnet_M500.json` |
| `witness_mit2_cicids2017/calibration_Brute_Force_M500.json` | `results/cicids2017/mit2/calibration_Brute_Force_M500.json` |
| `witness_mit2_cicids2017/calibration_Portscan_M500.json` | `results/cicids2017/mit2/calibration_Portscan_M500.json` |
| `witness_mit2_cicids2017/config_mit2.json` | `results/cicids2017/mit2/config_mit2.json` |
| `witness_mit2_cicids2017/figures/M3_coverage_Botnet.pdf` | `results/cicids2017/mit2/figures/M3_coverage_Botnet.pdf` |
| `witness_mit2_cicids2017/figures/M3_coverage_Portscan.pdf` | `results/cicids2017/mit2/figures/M3_coverage_Portscan.pdf` |
| `witness_mit2_cicids2017/mit2_runs.csv` | `results/cicids2017/mit2/mit2_runs.csv` |
| `witness_mit2_cse2018/CLAIMS_SUMMARY_MIT2_cse2018.md` | `results/cse2018/mit2/CLAIMS_SUMMARY_MIT2_cse2018.md` |
| `witness_mit2_cse2018/calibration_Botnet_M500.json` | `results/cse2018/mit2/calibration_Botnet_M500.json` |
| `witness_mit2_cse2018/calibration_Brute_Force_M500.json` | `results/cse2018/mit2/calibration_Brute_Force_M500.json` |
| `witness_mit2_cse2018/config_mit2.json` | `results/cse2018/mit2/config_mit2.json` |
| `witness_mit2_cse2018/figures/M3_coverage_Botnet.pdf` | `results/cse2018/mit2/figures/M3_coverage_Botnet.pdf` |
| `witness_mit2_cse2018/figures/M3_coverage_Brute_Force.pdf` | `results/cse2018/mit2/figures/M3_coverage_Brute_Force.pdf` |
| `witness_mit2_cse2018/mit2_runs.csv` | `results/cse2018/mit2/mit2_runs.csv` |
| `witness_mit3_cicids2017/CLAIMS_SUMMARY_MIT3_cicids2017.md` | `results/cicids2017/mit3/CLAIMS_SUMMARY_MIT3_cicids2017.md` |
| `witness_mit3_cicids2017/calibration_Botnet_M500.json` | `results/cicids2017/mit3/calibration_Botnet_M500.json` |
| `witness_mit3_cicids2017/calibration_Brute_Force_M500.json` | `results/cicids2017/mit3/calibration_Brute_Force_M500.json` |
| `witness_mit3_cicids2017/calibration_Portscan_M500.json` | `results/cicids2017/mit3/calibration_Portscan_M500.json` |
| `witness_mit3_cicids2017/figures/M6_adaptive_Botnet.pdf` | `results/cicids2017/mit3/figures/M6_adaptive_Botnet.pdf` |
| `witness_mit3_cicids2017/figures/M6_adaptive_Portscan.pdf` | `results/cicids2017/mit3/figures/M6_adaptive_Portscan.pdf` |
| `witness_mit3_cicids2017/mit3_runs.csv` | `results/cicids2017/mit3/mit3_runs.csv` |
| `witness_mit3_cse2018/CLAIMS_SUMMARY_MIT3_cse2018.md` | `results/cse2018/mit3/CLAIMS_SUMMARY_MIT3_cse2018.md` |
| `witness_mit3_cse2018/calibration_Botnet_M500.json` | `results/cse2018/mit3/calibration_Botnet_M500.json` |
| `witness_mit3_cse2018/calibration_Brute_Force_M500.json` | `results/cse2018/mit3/calibration_Brute_Force_M500.json` |
| `witness_mit3_cse2018/figures/M6_adaptive_Botnet.pdf` | `results/cse2018/mit3/figures/M6_adaptive_Botnet.pdf` |
| `witness_mit3_cse2018/figures/M6_adaptive_Brute_Force.pdf` | `results/cse2018/mit3/figures/M6_adaptive_Brute_Force.pdf` |
| `witness_mit3_cse2018/mit3_runs.csv` | `results/cse2018/mit3/mit3_runs.csv` |
| `witness_v3_cicids2017/CLAIMS_SUMMARY_cicids2017.md` | `results/cicids2017/v3_2/CLAIMS_SUMMARY_cicids2017.md` |
| `witness_v3_cicids2017/calibration_Botnet_M500.json` | `results/cicids2017/v3_2/calibration_Botnet_M500.json` |
| `witness_v3_cicids2017/calibration_Brute_Force_M500.json` | `results/cicids2017/v3_2/calibration_Brute_Force_M500.json` |
| `witness_v3_cicids2017/calibration_Portscan_M500.json` | `results/cicids2017/v3_2/calibration_Portscan_M500.json` |
| `witness_v3_cicids2017/config_FULL.json` | `results/cicids2017/v3_2/config_FULL.json` |
| `witness_v3_cicids2017/expA_kstar_Botnet.csv` | `results/cicids2017/v3_2/expA_kstar_Botnet.csv` |
| `witness_v3_cicids2017/expA_kstar_Brute_Force.csv` | `results/cicids2017/v3_2/expA_kstar_Brute_Force.csv` |
| `witness_v3_cicids2017/expA_kstar_Portscan.csv` | `results/cicids2017/v3_2/expA_kstar_Portscan.csv` |
| `witness_v3_cicids2017/expA_runs.csv` | `results/cicids2017/v3_2/expA_runs.csv` |
| `witness_v3_cicids2017/expB_kstar_Botnet.csv` | `results/cicids2017/v3_2/expB_kstar_Botnet.csv` |
| `witness_v3_cicids2017/expB_runs.csv` | `results/cicids2017/v3_2/expB_runs.csv` |
| `witness_v3_cicids2017/expC_natural.csv` | `results/cicids2017/v3_2/expC_natural.csv` |
| `witness_v3_cicids2017/expD_Botnet.csv` | `results/cicids2017/v3_2/expD_Botnet.csv` |
| `witness_v3_cicids2017/expD_Brute_Force.csv` | `results/cicids2017/v3_2/expD_Brute_Force.csv` |
| `witness_v3_cicids2017/expD_Portscan.csv` | `results/cicids2017/v3_2/expD_Portscan.csv` |
| `witness_v3_cicids2017/expD_runs.csv` | `results/cicids2017/v3_2/expD_runs.csv` |
| `witness_v3_cicids2017/expD_summary_Botnet.csv` | `results/cicids2017/v3_2/expD_summary_Botnet.csv` |
| `witness_v3_cicids2017/expD_summary_Brute_Force.csv` | `results/cicids2017/v3_2/expD_summary_Brute_Force.csv` |
| `witness_v3_cicids2017/expD_summary_Portscan.csv` | `results/cicids2017/v3_2/expD_summary_Portscan.csv` |
| `witness_v3_cicids2017/expK0_Botnet.csv` | `results/cicids2017/v3_2/expK0_Botnet.csv` |
| `witness_v3_cicids2017/expK0_Brute_Force.csv` | `results/cicids2017/v3_2/expK0_Brute_Force.csv` |
| `witness_v3_cicids2017/expK0_Portscan.csv` | `results/cicids2017/v3_2/expK0_Portscan.csv` |
| `witness_v3_cicids2017/expK0_runs.csv` | `results/cicids2017/v3_2/expK0_runs.csv` |
| `witness_v3_cicids2017/expQA_runs.csv` | `results/cicids2017/v3_2/expQA_runs.csv` |
| `witness_v3_cicids2017/expQA_taxcells_Botnet.csv` | `results/cicids2017/v3_2/expQA_taxcells_Botnet.csv` |
| `witness_v3_cicids2017/expQA_taxcells_Brute_Force.csv` | `results/cicids2017/v3_2/expQA_taxcells_Brute_Force.csv` |
| `witness_v3_cicids2017/expQA_taxcells_Portscan.csv` | `results/cicids2017/v3_2/expQA_taxcells_Portscan.csv` |
| `witness_v3_cicids2017/expQA_verdict_Botnet.json` | `results/cicids2017/v3_2/expQA_verdict_Botnet.json` |
| `witness_v3_cicids2017/expQA_verdict_Brute_Force.json` | `results/cicids2017/v3_2/expQA_verdict_Brute_Force.json` |
| `witness_v3_cicids2017/expQA_verdict_Portscan.json` | `results/cicids2017/v3_2/expQA_verdict_Portscan.json` |
| `witness_v3_cicids2017/figures/A1_phase_Botnet.pdf` | `results/cicids2017/v3_2/figures/A1_phase_Botnet.pdf` |
| `witness_v3_cicids2017/figures/A1_phase_Brute_Force.pdf` | `results/cicids2017/v3_2/figures/A1_phase_Brute_Force.pdf` |
| `witness_v3_cicids2017/figures/A1_phase_Portscan.pdf` | `results/cicids2017/v3_2/figures/A1_phase_Portscan.pdf` |
| `witness_v3_cicids2017/figures/A2_recall_vs_k_Botnet.pdf` | `results/cicids2017/v3_2/figures/A2_recall_vs_k_Botnet.pdf` |
| `witness_v3_cicids2017/figures/A2_recall_vs_k_Brute_Force.pdf` | `results/cicids2017/v3_2/figures/A2_recall_vs_k_Brute_Force.pdf` |
| `witness_v3_cicids2017/figures/A2_recall_vs_k_Portscan.pdf` | `results/cicids2017/v3_2/figures/A2_recall_vs_k_Portscan.pdf` |
| `witness_v3_cicids2017/figures/A3_tax_Botnet.pdf` | `results/cicids2017/v3_2/figures/A3_tax_Botnet.pdf` |
| `witness_v3_cicids2017/figures/A3_tax_Brute_Force.pdf` | `results/cicids2017/v3_2/figures/A3_tax_Brute_Force.pdf` |
| `witness_v3_cicids2017/figures/A3_tax_Portscan.pdf` | `results/cicids2017/v3_2/figures/A3_tax_Portscan.pdf` |
| `witness_v3_cicids2017/figures/B1_dp_Botnet.pdf` | `results/cicids2017/v3_2/figures/B1_dp_Botnet.pdf` |
| `witness_v3_cicids2017/figures/C1_natural_daylock.pdf` | `results/cicids2017/v3_2/figures/C1_natural_daylock.pdf` |
| `witness_v3_cicids2017/figures/QA1_Botnet.pdf` | `results/cicids2017/v3_2/figures/QA1_Botnet.pdf` |
| `witness_v3_cicids2017/figures/QA1_Brute_Force.pdf` | `results/cicids2017/v3_2/figures/QA1_Brute_Force.pdf` |
| `witness_v3_cicids2017/figures/QA1_Portscan.pdf` | `results/cicids2017/v3_2/figures/QA1_Portscan.pdf` |
| `witness_v3_cicids2017/gate_Botnet.json` | `results/cicids2017/v3_2/gate_Botnet.json` |
| `witness_v3_cicids2017/gate_Brute_Force.json` | `results/cicids2017/v3_2/gate_Brute_Force.json` |
| `witness_v3_cicids2017/gate_Portscan.json` | `results/cicids2017/v3_2/gate_Portscan.json` |
| `witness_v3_cicids2017/preflight_Botnet.json` | `results/cicids2017/v3_2/preflight_Botnet.json` |
| `witness_v3_cicids2017/preflight_Brute_Force.json` | `results/cicids2017/v3_2/preflight_Brute_Force.json` |
| `witness_v3_cicids2017/preflight_Portscan.json` | `results/cicids2017/v3_2/preflight_Portscan.json` |
| `witness_v3_cse2018/CLAIMS_SUMMARY_cse2018.md` | `results/cse2018/v3_2/CLAIMS_SUMMARY_cse2018.md` |
| `witness_v3_cse2018/calibration_Botnet_M500.json` | `results/cse2018/v3_2/calibration_Botnet_M500.json` |
| `witness_v3_cse2018/calibration_Brute_Force_M500.json` | `results/cse2018/v3_2/calibration_Brute_Force_M500.json` |
| `witness_v3_cse2018/config_FULL.json` | `results/cse2018/v3_2/config_FULL.json` |
| `witness_v3_cse2018/config_QUICK.json` | `results/cse2018/v3_2/config_QUICK.json` |
| `witness_v3_cse2018/expA_kstar_Botnet.csv` | `results/cse2018/v3_2/expA_kstar_Botnet.csv` |
| `witness_v3_cse2018/expA_kstar_Brute_Force.csv` | `results/cse2018/v3_2/expA_kstar_Brute_Force.csv` |
| `witness_v3_cse2018/expA_runs.csv` | `results/cse2018/v3_2/expA_runs.csv` |
| `witness_v3_cse2018/expB_kstar_Botnet.csv` | `results/cse2018/v3_2/expB_kstar_Botnet.csv` |
| `witness_v3_cse2018/expB_kstar_Brute_Force.csv` | `results/cse2018/v3_2/expB_kstar_Brute_Force.csv` |
| `witness_v3_cse2018/expB_runs.csv` | `results/cse2018/v3_2/expB_runs.csv` |
| `witness_v3_cse2018/expC_natural.csv` | `results/cse2018/v3_2/expC_natural.csv` |
| `witness_v3_cse2018/expD_Botnet.csv` | `results/cse2018/v3_2/expD_Botnet.csv` |
| `witness_v3_cse2018/expD_Brute_Force.csv` | `results/cse2018/v3_2/expD_Brute_Force.csv` |
| `witness_v3_cse2018/expD_runs.csv` | `results/cse2018/v3_2/expD_runs.csv` |
| `witness_v3_cse2018/expD_summary_Botnet.csv` | `results/cse2018/v3_2/expD_summary_Botnet.csv` |
| `witness_v3_cse2018/expD_summary_Brute_Force.csv` | `results/cse2018/v3_2/expD_summary_Brute_Force.csv` |
| `witness_v3_cse2018/expK0_Botnet.csv` | `results/cse2018/v3_2/expK0_Botnet.csv` |
| `witness_v3_cse2018/expK0_Brute_Force.csv` | `results/cse2018/v3_2/expK0_Brute_Force.csv` |
| `witness_v3_cse2018/expK0_runs.csv` | `results/cse2018/v3_2/expK0_runs.csv` |
| `witness_v3_cse2018/expQA_runs.csv` | `results/cse2018/v3_2/expQA_runs.csv` |
| `witness_v3_cse2018/expQA_taxcells_Botnet.csv` | `results/cse2018/v3_2/expQA_taxcells_Botnet.csv` |
| `witness_v3_cse2018/expQA_taxcells_Brute_Force.csv` | `results/cse2018/v3_2/expQA_taxcells_Brute_Force.csv` |
| `witness_v3_cse2018/expQA_verdict_Botnet.json` | `results/cse2018/v3_2/expQA_verdict_Botnet.json` |
| `witness_v3_cse2018/expQA_verdict_Brute_Force.json` | `results/cse2018/v3_2/expQA_verdict_Brute_Force.json` |
| `witness_v3_cse2018/figures/A1_phase_Botnet.pdf` | `results/cse2018/v3_2/figures/A1_phase_Botnet.pdf` |
| `witness_v3_cse2018/figures/A1_phase_Brute_Force.pdf` | `results/cse2018/v3_2/figures/A1_phase_Brute_Force.pdf` |
| `witness_v3_cse2018/figures/A2_recall_vs_k_Botnet.pdf` | `results/cse2018/v3_2/figures/A2_recall_vs_k_Botnet.pdf` |
| `witness_v3_cse2018/figures/A2_recall_vs_k_Brute_Force.pdf` | `results/cse2018/v3_2/figures/A2_recall_vs_k_Brute_Force.pdf` |
| `witness_v3_cse2018/figures/A3_tax_Botnet.pdf` | `results/cse2018/v3_2/figures/A3_tax_Botnet.pdf` |
| `witness_v3_cse2018/figures/A3_tax_Brute_Force.pdf` | `results/cse2018/v3_2/figures/A3_tax_Brute_Force.pdf` |
| `witness_v3_cse2018/figures/B1_dp_Botnet.pdf` | `results/cse2018/v3_2/figures/B1_dp_Botnet.pdf` |
| `witness_v3_cse2018/figures/B1_dp_Brute_Force.pdf` | `results/cse2018/v3_2/figures/B1_dp_Brute_Force.pdf` |
| `witness_v3_cse2018/figures/C1_natural_daylock.pdf` | `results/cse2018/v3_2/figures/C1_natural_daylock.pdf` |
| `witness_v3_cse2018/figures/QA1_Botnet.pdf` | `results/cse2018/v3_2/figures/QA1_Botnet.pdf` |
| `witness_v3_cse2018/figures/QA1_Brute_Force.pdf` | `results/cse2018/v3_2/figures/QA1_Brute_Force.pdf` |
| `witness_v3_cse2018/gate_Botnet.json` | `results/cse2018/v3_2/gate_Botnet.json` |
| `witness_v3_cse2018/gate_Brute_Force.json` | `results/cse2018/v3_2/gate_Brute_Force.json` |
| `witness_v3_cse2018/preflight_Botnet.json` | `results/cse2018/v3_2/preflight_Botnet.json` |
| `witness_v3_cse2018/preflight_Brute_Force.json` | `results/cse2018/v3_2/preflight_Brute_Force.json` |

## New files (no old path)

`README.md`, `LICENSE`, `requirements.txt`, `MAPPING.md`, `analysis/**` (two analysis scripts), `data/README.md`, `scripts/**` (8 verbatim exports of the notebooks' code cells), `tables/**`.
