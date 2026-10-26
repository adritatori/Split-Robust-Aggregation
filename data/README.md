# Data

No data files are stored in this repository (`data/*` is git-ignored except this file).

## Dataset

The notebooks read one dataset, referenced as

`ernie55ernie/improved-cicids2017-and-csecicids2018`

It contains the corrected releases of CICIDS2017 and CSE-CIC-IDS2018. The notebooks' code describes them as:

| notebook dataset | sub-folder used | what the code says about it |
|---|---|---|
| CICIDS2017 | `CICIDS2017_improved` | "corrected release (Engelen et al. 2021 / Liu et al. 2022)" |
| CSE-CIC-IDS2018 | `CSECICIDS2018_improved` | "corrected release (Liu et al., IEEE CNS 2022)", 63.2M flows, about 35 GB, streamed with pyarrow |

Input paths as printed in the notebook logs (`<input folder>` is the folder where the notebook environment mounts its inputs):

```
<input folder>/datasets/ernie55ernie/improved-cicids2017-and-csecicids2018/CICIDS2017_improved
<input folder>/datasets/ernie55ernie/improved-cicids2017-and-csecicids2018/CSECICIDS2018_improved
```

The notebooks find the folder themselves: they search the input folder recursively for `monday.csv` or `*Monday*.csv` (CICIDS2017) and for `Friday-02-03-2018.csv` or `*02-03-2018*.csv` (CSE-CIC-IDS2018). To bypass the search, set the Python constant `DATA_PATH` at the top of the notebook (it is a constant in the code, not an environment variable). File names containing `_plus` are skipped for CICIDS2017.

Files read (row counts from the logs):

- CICIDS2017: `friday.csv` 547,557 · `monday.csv` 371,624 · `thursday.csv` 362,076 · `tuesday.csv` 322,078 · `wednesday.csv` 496,641.
- CSE-CIC-IDS2018: ten day files, `Friday-02-03-2018.csv` (6,311,371 rows), `Friday-16-02-2018.csv`, `Friday-23-02-2018.csv`, `Thursday-01-03-2018.csv`, `Thursday-15-02-2018.csv`, `Thursday-22-02-2018.csv`, `Tuesday-20-02-2018.csv`, `Wednesday-14-02-2018.csv`, `Wednesday-21-02-2018.csv`, `Wednesday-28-02-2018.csv`.

## Cleaning steps (read from the code, same in all notebooks)

1. **Labels.** Raw labels are mapped to seven classes: Normal, DoS, DDoS, Portscan, Brute Force, Botnet, Web Attack. Infiltration, Heartbleed and unknown labels are dropped. Flows labelled "... - Attempted" are dropped (`ATTEMPTED_POLICY = "drop"`). CSE-CIC-IDS2018 has no Portscan class.
2. **Features.** Numeric columns only. ID columns and every column with "port" in its name are removed (`DROP_PORTS = True`). Host addresses never enter the model.
3. **Label conflicts and duplicates.** Rows with identical features but different labels are removed. Exact duplicate rows are removed.
4. **Split.** Stratified per class, 30 % test, seed 0, test set capped at 30,000 Normal and 5,000 per other class.
5. **Missing values.** Columns with more than 50 % missing values in the training part are dropped. Test rows identical to a training row are removed. Non-finite cells are replaced by the training median.
6. **Scaling.** Signed `log1p`, then z-score with training mean and standard deviation, clipped to [-10, 10].
7. **CSE-CIC-IDS2018 only.** All attack flows are kept. Benign flows are Bernoulli-sampled at rate 0.035 (about 2.1M of 59.4M). The rarity share uses the estimated full benign count (sampled clean count divided by the rate). Label-conflict detection only sees the sampled benign rows. Training pools are capped per class (Normal 1,000,000; every other class 300,000). The cleaned arrays are written to `data_cache.npz` (git-ignored) and reused by later notebooks if the earlier output is attached.

Class counts after cleaning (as printed in the logs): `tables/S3_class_counts.csv`.
