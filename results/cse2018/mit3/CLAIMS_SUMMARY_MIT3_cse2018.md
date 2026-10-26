# mit-3 (final) summary -- CSE-CIC-IDS2018

## Brute Force | verdicts
```
M8_base: FLOOR_NOT_REACHED
M8_sra: FLOOR_MEASURED
M8_sra_l10: FLOOR_MEASURED
M8_sra_cap: FLOOR_MEASURED
M8_fedavg_recall: 0.67
M3c_sra_cap_floor: ABOVE_FLOOR
M3c_sra_cap_censored_share: 0.67
M6_sra: SURVIVES_ADAPTIVE
M6_sra_l10: SURVIVES_ADAPTIVE
M6_sra_cap: SURVIVES_ADAPTIVE
M6_sra_detail: 36/36 paired HOLDS; coverage 36/36
M6_sra_l10_detail: 36/36 paired HOLDS; coverage 36/36
M6_sra_cap_detail: 36/36 paired HOLDS; coverage 36/36
M7_base_dp: DP_KEEPS_ROBUSTNESS (share 0.00)
M7_sra_vs_base_under_dp: 11/12 HOLDS (paired)
M9_seeds: seeds 0-2 (mit-2) + 3-4 (mit-3)
```

## Botnet | verdicts
```
M8_base: FLOOR_NOT_REACHED
M8_sra: FLOOR_MEASURED
M8_sra_l10: FLOOR_MEASURED
M8_sra_cap: FLOOR_MEASURED
M8_fedavg_recall: 0.45
M3c_sra_cap_floor: ABOVE_FLOOR
M3c_sra_cap_censored_share: 0.67
M6_sra: SURVIVES_ADAPTIVE
M6_sra_l10: SURVIVES_ADAPTIVE
M6_sra_cap: SURVIVES_ADAPTIVE
M6_sra_detail: 36/36 paired HOLDS; coverage 36/36
M6_sra_l10_detail: 36/36 paired HOLDS; coverage 36/36
M6_sra_cap_detail: 36/36 paired HOLDS; coverage 36/36
M7_base_dp: DP_KEEPS_ROBUSTNESS (share 0.17)
M7_sra_vs_base_under_dp: 12/12 HOLDS (paired)
M9_seeds: seeds 0-2 (mit-2) + 3-4 (mit-3)
```

## Brute Force | M8 target recall at k=5, f=4 (floor = 5; learnable line 0.800)
```
                 mean    std
agg    arm                  
cwmed  base     0.000  0.000
       sra      1.000  0.000
       sra_cap  1.000  0.000
       sra_l10  1.000  0.000
fedavg base     0.670  0.280
mkrum  base     0.297  0.474
       sra      1.000  0.000
       sra_cap  1.000  0.000
       sra_l10  1.000  0.000
trmean base     0.858  0.140
       sra      1.000  0.000
       sra_cap  1.000  0.000
       sra_l10  1.000  0.000
```


## Brute Force | M8 verdicts
```
M8_base: FLOOR_NOT_REACHED
M8_sra: FLOOR_MEASURED
M8_sra_l10: FLOOR_MEASURED
M8_sra_cap: FLOOR_MEASURED
M8_fedavg_recall: 0.67
```


## Brute Force | M3c k* of sra_cap (cap = 5 members)
```
 f    agg  FedAvg  sra_cap  tax  sra (mit-2)
 0  cwmed       1        2    1            2
 0 trmean       1        2    1            2
 0  mkrum       1        2    1            2
 2  cwmed       3        3    0            3
 2 trmean       3        3    0            3
 2  mkrum       3        3    0            3
 4  cwmed       6        6    0            6
 4 trmean       6        6    0            6
 4  mkrum       6        6    0            6
```


## Brute Force | M3c verdict
```
floor (pre-registered rule): ABOVE_FLOOR | grid-censored share: 0.67
```


## Brute Force | M6 all cells (target = rare-class recall under attack; learnable line 0.800)
```
 k  f   attack    agg     arm  benign_fpr  other_mean  target paired                     absolute
 3  2   fang_w  cwmed    base       0.004       0.914   0.000  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2   fang_w  cwmed     sra       0.003       0.959   1.000  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2   fang_w  cwmed sra_l10       0.003       0.959   1.000  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2   fang_w  cwmed sra_cap       0.003       0.959   1.000  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2   fang_w trmean    base       0.003       0.960   0.327  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2   fang_w trmean     sra       0.003       0.960   1.000  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2   fang_w trmean sra_l10       0.003       0.960   1.000  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2   fang_w trmean sra_cap       0.003       0.960   1.000  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2   fang_w  mkrum    base       0.003       0.960   1.000  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2   fang_w  mkrum     sra       0.003       0.960   1.000  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2   fang_w  mkrum sra_l10       0.003       0.960   1.000  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2   fang_w  mkrum sra_cap       0.003       0.960   1.000  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2 minmax_w  cwmed    base       0.004       0.923   0.000  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2 minmax_w  cwmed     sra       0.003       0.959   1.000  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2 minmax_w  cwmed sra_l10       0.003       0.959   1.000  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2 minmax_w  cwmed sra_cap       0.003       0.959   1.000  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2 minmax_w trmean    base       0.003       0.960   0.803  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2 minmax_w trmean     sra       0.003       0.960   1.000  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2 minmax_w trmean sra_l10       0.003       0.960   1.000  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2 minmax_w trmean sra_cap       0.003       0.960   1.000  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2 minmax_w  mkrum    base       0.003       0.960   0.000  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2 minmax_w  mkrum     sra       0.003       0.960   1.000  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2 minmax_w  mkrum sra_l10       0.003       0.960   1.000  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2 minmax_w  mkrum sra_cap       0.003       0.960   1.000  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2   alie_w  cwmed    base       0.003       0.929   0.000  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2   alie_w  cwmed     sra       0.003       0.959   1.000  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2   alie_w  cwmed sra_l10       0.003       0.959   1.000  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2   alie_w  cwmed sra_cap       0.003       0.959   1.000  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2   alie_w trmean    base       0.003       0.960   1.000  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2   alie_w trmean     sra       0.003       0.960   1.000  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2   alie_w trmean sra_l10       0.003       0.960   1.000  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2   alie_w trmean sra_cap       0.003       0.960   1.000  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2   alie_w  mkrum    base       0.003       0.961   0.847  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2   alie_w  mkrum     sra       0.003       0.960   1.000  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2   alie_w  mkrum sra_l10       0.003       0.960   1.000  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2   alie_w  mkrum sra_cap       0.003       0.960   1.000  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2 minmax_h  cwmed    base       0.005       0.822   0.000  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2 minmax_h  cwmed     sra       0.004       0.897   1.000  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2 minmax_h  cwmed sra_l10       0.004       0.897   1.000  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2 minmax_h  cwmed sra_cap       0.004       0.897   1.000  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2 minmax_h trmean    base       0.004       0.930   0.998  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2 minmax_h trmean     sra       0.004       0.924   1.000  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2 minmax_h trmean sra_l10       0.004       0.924   1.000  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2 minmax_h trmean sra_cap       0.004       0.924   1.000  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2 minmax_h  mkrum    base       0.004       0.925   0.003  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2 minmax_h  mkrum     sra       0.004       0.924   1.000  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2 minmax_h  mkrum sra_l10       0.004       0.924   1.000  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2 minmax_h  mkrum sra_cap       0.004       0.924   1.000  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2   fang_h  cwmed    base       0.004       0.914   0.000  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2   fang_h  cwmed     sra       0.003       0.960   1.000  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2   fang_h  cwmed sra_l10       0.003       0.960   1.000  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2   fang_h  cwmed sra_cap       0.003       0.960   1.000  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2   fang_h trmean    base       0.003       0.960   0.327  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2   fang_h trmean     sra       0.003       0.960   1.000  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2   fang_h trmean sra_l10       0.003       0.960   1.000  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2   fang_h trmean sra_cap       0.003       0.960   1.000  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2   fang_h  mkrum    base       0.003       0.960   1.000  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2   fang_h  mkrum     sra       0.003       0.960   1.000  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2   fang_h  mkrum sra_l10       0.003       0.960   1.000  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2   fang_h  mkrum sra_cap       0.003       0.960   1.000  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2    split  cwmed    base       0.004       0.871   0.000  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2    split  cwmed     sra       0.004       0.952   1.000  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2    split  cwmed sra_l10       0.004       0.952   1.000  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2    split  cwmed sra_cap       0.004       0.952   1.000  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2    split trmean    base       0.004       0.952   0.825  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2    split trmean     sra       0.004       0.960   1.000  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2    split trmean sra_l10       0.004       0.960   1.000  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2    split trmean sra_cap       0.004       0.960   1.000  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2    split  mkrum    base       0.004       0.960   1.000  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2    split  mkrum     sra       0.004       0.960   1.000  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2    split  mkrum sra_l10       0.004       0.960   1.000  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2    split  mkrum sra_cap       0.004       0.960   1.000  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2   fang_w  cwmed    base       0.004       0.960   0.000  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2   fang_w  cwmed     sra       0.004       0.960   1.000  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2   fang_w  cwmed sra_l10       0.004       0.960   1.000  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2   fang_w  cwmed sra_cap       0.004       0.960   1.000  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2   fang_w trmean    base       0.004       0.960   1.000  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2   fang_w trmean     sra       0.004       0.960   1.000  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2   fang_w trmean sra_l10       0.004       0.960   1.000  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2   fang_w trmean sra_cap       0.004       0.960   1.000  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2   fang_w  mkrum    base       0.003       0.961   1.000  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2   fang_w  mkrum     sra       0.003       0.960   1.000  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2   fang_w  mkrum sra_l10       0.003       0.960   1.000  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2   fang_w  mkrum sra_cap       0.004       0.960   1.000  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2 minmax_w  cwmed    base       0.004       0.961   0.000  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2 minmax_w  cwmed     sra       0.004       0.960   1.000  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2 minmax_w  cwmed sra_l10       0.004       0.960   1.000  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2 minmax_w  cwmed sra_cap       0.004       0.960   1.000  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2 minmax_w trmean    base       0.003       0.960   1.000  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2 minmax_w trmean     sra       0.003       0.960   1.000  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2 minmax_w trmean sra_l10       0.003       0.960   1.000  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2 minmax_w trmean sra_cap       0.004       0.960   1.000  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2 minmax_w  mkrum    base       0.003       0.961   1.000  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2 minmax_w  mkrum     sra       0.003       0.960   1.000  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2 minmax_w  mkrum sra_l10       0.003       0.960   1.000  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2 minmax_w  mkrum sra_cap       0.004       0.961   1.000  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2   alie_w  cwmed    base       0.003       0.961   0.000  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2   alie_w  cwmed     sra       0.003       0.960   1.000  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2   alie_w  cwmed sra_l10       0.003       0.960   1.000  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2   alie_w  cwmed sra_cap       0.004       0.960   1.000  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2   alie_w trmean    base       0.003       0.961   1.000  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2   alie_w trmean     sra       0.003       0.960   1.000  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2   alie_w trmean sra_l10       0.003       0.960   1.000  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2   alie_w trmean sra_cap       0.003       0.960   1.000  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2   alie_w  mkrum    base       0.003       0.961   1.000  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2   alie_w  mkrum     sra       0.003       0.961   1.000  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2   alie_w  mkrum sra_l10       0.003       0.961   1.000  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2   alie_w  mkrum sra_cap       0.003       0.961   1.000  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2 minmax_h  cwmed    base       0.004       0.959   0.000  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2 minmax_h  cwmed     sra       0.004       0.960   1.000  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2 minmax_h  cwmed sra_l10       0.004       0.960   1.000  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2 minmax_h  cwmed sra_cap       0.004       0.960   1.000  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2 minmax_h trmean    base       0.004       0.960   1.000  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2 minmax_h trmean     sra       0.004       0.960   1.000  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2 minmax_h trmean sra_l10       0.004       0.960   1.000  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2 minmax_h trmean sra_cap       0.004       0.960   1.000  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2 minmax_h  mkrum    base       0.004       0.960   1.000  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2 minmax_h  mkrum     sra       0.004       0.960   1.000  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2 minmax_h  mkrum sra_l10       0.004       0.960   1.000  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2 minmax_h  mkrum sra_cap       0.004       0.960   1.000  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2   fang_h  cwmed    base       0.004       0.960   0.000  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2   fang_h  cwmed     sra       0.004       0.960   1.000  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2   fang_h  cwmed sra_l10       0.004       0.960   1.000  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2   fang_h  cwmed sra_cap       0.004       0.960   1.000  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2   fang_h trmean    base       0.004       0.960   1.000  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2   fang_h trmean     sra       0.004       0.960   1.000  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2   fang_h trmean sra_l10       0.004       0.960   1.000  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2   fang_h trmean sra_cap       0.004       0.961   1.000  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2   fang_h  mkrum    base       0.003       0.961   1.000  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2   fang_h  mkrum     sra       0.003       0.961   1.000  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2   fang_h  mkrum sra_l10       0.003       0.961   1.000  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2   fang_h  mkrum sra_cap       0.003       0.961   1.000  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2    split  cwmed    base       0.004       0.959   0.000  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2    split  cwmed     sra       0.004       0.960   1.000  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2    split  cwmed sra_l10       0.004       0.960   1.000  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2    split  cwmed sra_cap       0.004       0.960   1.000  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2    split trmean    base       0.004       0.960   1.000  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2    split trmean     sra       0.004       0.960   1.000  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2    split trmean sra_l10       0.004       0.960   1.000  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2    split trmean sra_cap       0.004       0.960   1.000  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2    split  mkrum    base       0.004       0.960   1.000  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2    split  mkrum     sra       0.004       0.960   1.000  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2    split  mkrum sra_l10       0.004       0.960   1.000  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2    split  mkrum sra_cap       0.004       0.960   1.000  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4   fang_w  cwmed    base       0.004       0.960   0.000  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4   fang_w  cwmed     sra       0.003       0.959   1.000  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4   fang_w  cwmed sra_l10       0.003       0.959   1.000  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4   fang_w  cwmed sra_cap       0.003       0.960   1.000  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4   fang_w trmean    base       0.004       0.961   0.000  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4   fang_w trmean     sra       0.003       0.960   1.000  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4   fang_w trmean sra_l10       0.003       0.960   1.000  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4   fang_w trmean sra_cap       0.003       0.961   1.000  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4   fang_w  mkrum    base       0.003       0.962   1.000  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4   fang_w  mkrum     sra       0.003       0.960   1.000  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4   fang_w  mkrum sra_l10       0.003       0.960   1.000  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4   fang_w  mkrum sra_cap       0.003       0.961   1.000  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4 minmax_w  cwmed    base       0.004       0.961   0.000  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4 minmax_w  cwmed     sra       0.003       0.960   1.000  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4 minmax_w  cwmed sra_l10       0.003       0.960   1.000  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4 minmax_w  cwmed sra_cap       0.003       0.960   1.000  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4 minmax_w trmean    base       0.003       0.961   1.000  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4 minmax_w trmean     sra       0.003       0.960   1.000  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4 minmax_w trmean sra_l10       0.003       0.960   1.000  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4 minmax_w trmean sra_cap       0.003       0.961   1.000  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4 minmax_w  mkrum    base       0.003       0.962   1.000  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4 minmax_w  mkrum     sra       0.003       0.960   1.000  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4 minmax_w  mkrum sra_l10       0.003       0.960   1.000  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4 minmax_w  mkrum sra_cap       0.003       0.960   1.000  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4   alie_w  cwmed    base       0.004       0.961   1.000  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4   alie_w  cwmed     sra       0.003       0.959   1.000  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4   alie_w  cwmed sra_l10       0.003       0.959   1.000  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4   alie_w  cwmed sra_cap       0.004       0.960   1.000  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4   alie_w trmean    base       0.003       0.961   1.000  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4   alie_w trmean     sra       0.003       0.959   1.000  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4   alie_w trmean sra_l10       0.003       0.959   1.000  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4   alie_w trmean sra_cap       0.003       0.960   1.000  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4   alie_w  mkrum    base       0.003       0.962   1.000  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4   alie_w  mkrum     sra       0.003       0.960   1.000  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4   alie_w  mkrum sra_l10       0.003       0.960   1.000  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4   alie_w  mkrum sra_cap       0.003       0.961   1.000  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4 minmax_h  cwmed    base       0.005       0.916   0.000  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4 minmax_h  cwmed     sra       0.005       0.847   1.000 BREAKS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4 minmax_h  cwmed sra_l10       0.005       0.847   1.000 BREAKS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4 minmax_h  cwmed sra_cap       0.005       0.836   1.000 BREAKS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4 minmax_h trmean    base       0.005       0.828   1.000  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4 minmax_h trmean     sra       0.005       0.827   1.000  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4 minmax_h trmean sra_l10       0.005       0.827   1.000  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4 minmax_h trmean sra_cap       0.005       0.818   1.000  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4 minmax_h  mkrum    base       0.005       0.854   1.000  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4 minmax_h  mkrum     sra       0.005       0.818   1.000  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4 minmax_h  mkrum sra_l10       0.005       0.818   1.000  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4 minmax_h  mkrum sra_cap       0.005       0.799   1.000 BREAKS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4   fang_h  cwmed    base       0.004       0.960   0.000  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4   fang_h  cwmed     sra       0.003       0.960   1.000  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4   fang_h  cwmed sra_l10       0.003       0.960   1.000  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4   fang_h  cwmed sra_cap       0.003       0.960   1.000  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4   fang_h trmean    base       0.004       0.961   0.000  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4   fang_h trmean     sra       0.003       0.960   0.893  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4   fang_h trmean sra_l10       0.003       0.960   0.893  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4   fang_h trmean sra_cap       0.003       0.961   0.387  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4   fang_h  mkrum    base       0.003       0.962   1.000  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4   fang_h  mkrum     sra       0.003       0.961   1.000  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4   fang_h  mkrum sra_l10       0.003       0.961   1.000  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4   fang_h  mkrum sra_cap       0.003       0.961   1.000  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4    split  cwmed    base       0.004       0.959   0.000  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4    split  cwmed     sra       0.004       0.958   1.000  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4    split  cwmed sra_l10       0.004       0.958   1.000  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4    split  cwmed sra_cap       0.004       0.959   1.000  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4    split trmean    base       0.004       0.960   1.000  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4    split trmean     sra       0.004       0.959   1.000  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4    split trmean sra_l10       0.004       0.959   1.000  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4    split trmean sra_cap       0.004       0.959   1.000  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4    split  mkrum    base       0.004       0.921   1.000  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4    split  mkrum     sra       0.004       0.959   1.000  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4    split  mkrum sra_l10       0.004       0.959   1.000  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4    split  mkrum sra_cap       0.004       0.957   1.000  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4   fang_w  cwmed    base       0.003       0.837   0.000  (ref)                       BREAKS
 2  4   fang_w  cwmed     sra       0.003       0.959   1.000  HOLDS                        HOLDS
 2  4   fang_w  cwmed sra_l10       0.003       0.959   1.000  HOLDS                        HOLDS
 2  4   fang_w  cwmed sra_cap       0.003       0.959   1.000  HOLDS                        HOLDS
 2  4   fang_w trmean    base       0.532       0.183   0.000  (ref)                       BREAKS
 2  4   fang_w trmean     sra       0.003       0.959   1.000  HOLDS                        HOLDS
 2  4   fang_w trmean sra_l10       0.003       0.959   1.000  HOLDS                        HOLDS
 2  4   fang_w trmean sra_cap       0.003       0.959   1.000  HOLDS                        HOLDS
 2  4   fang_w  mkrum    base       0.007       0.670   0.000  (ref)                       BREAKS
 2  4   fang_w  mkrum     sra       0.003       0.959   1.000  HOLDS                        HOLDS
 2  4   fang_w  mkrum sra_l10       0.003       0.959   1.000  HOLDS                        HOLDS
 2  4   fang_w  mkrum sra_cap       0.003       0.959   1.000  HOLDS                        HOLDS
 2  4 minmax_w  cwmed    base       0.003       0.893   0.000  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4 minmax_w  cwmed     sra       0.003       0.959   1.000  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4 minmax_w  cwmed sra_l10       0.003       0.959   1.000  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4 minmax_w  cwmed sra_cap       0.003       0.959   1.000  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4 minmax_w trmean    base       0.003       0.960   0.000  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4 minmax_w trmean     sra       0.003       0.959   1.000  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4 minmax_w trmean sra_l10       0.003       0.959   1.000  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4 minmax_w trmean sra_cap       0.003       0.959   1.000  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4 minmax_w  mkrum    base       0.003       0.959   0.000  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4 minmax_w  mkrum     sra       0.003       0.960   1.000  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4 minmax_w  mkrum sra_l10       0.003       0.960   1.000  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4 minmax_w  mkrum sra_cap       0.003       0.960   1.000  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4   alie_w  cwmed    base       0.003       0.928   0.000  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4   alie_w  cwmed     sra       0.002       0.959   1.000  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4   alie_w  cwmed sra_l10       0.002       0.959   1.000  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4   alie_w  cwmed sra_cap       0.002       0.959   1.000  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4   alie_w trmean    base       0.003       0.960   0.000  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4   alie_w trmean     sra       0.002       0.960   1.000  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4   alie_w trmean sra_l10       0.002       0.960   1.000  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4   alie_w trmean sra_cap       0.002       0.960   1.000  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4   alie_w  mkrum    base       0.003       0.960   0.000  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4   alie_w  mkrum     sra       0.002       0.960   1.000  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4   alie_w  mkrum sra_l10       0.002       0.960   1.000  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4   alie_w  mkrum sra_cap       0.002       0.960   1.000  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4 minmax_h  cwmed    base       0.005       0.747   0.000  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4 minmax_h  cwmed     sra       0.005       0.828   1.000  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4 minmax_h  cwmed sra_l10       0.005       0.847   1.000  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4 minmax_h  cwmed sra_cap       0.005       0.828   1.000  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4 minmax_h trmean    base       0.005       0.836   0.000  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4 minmax_h trmean     sra       0.005       0.824   1.000  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4 minmax_h trmean sra_l10       0.005       0.828   1.000  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4 minmax_h trmean sra_cap       0.005       0.824   1.000  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4 minmax_h  mkrum    base       0.005       0.806   0.000  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4 minmax_h  mkrum     sra       0.005       0.818   1.000  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4 minmax_h  mkrum sra_l10       0.005       0.824   1.000  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4 minmax_h  mkrum sra_cap       0.005       0.818   1.000  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4   fang_h  cwmed    base       0.003       0.837   0.000  (ref)                       BREAKS
 2  4   fang_h  cwmed     sra       0.003       0.959   0.982  HOLDS                        HOLDS
 2  4   fang_h  cwmed sra_l10       0.003       0.959   0.982  HOLDS                        HOLDS
 2  4   fang_h  cwmed sra_cap       0.003       0.959   0.982  HOLDS                        HOLDS
 2  4   fang_h trmean    base       0.532       0.183   0.000  (ref)                       BREAKS
 2  4   fang_h trmean     sra       0.003       0.871   0.000  HOLDS                       BREAKS
 2  4   fang_h trmean sra_l10       0.003       0.871   0.000  HOLDS                       BREAKS
 2  4   fang_h trmean sra_cap       0.003       0.871   0.000  HOLDS                       BREAKS
 2  4   fang_h  mkrum    base       0.007       0.670   0.000  (ref)                       BREAKS
 2  4   fang_h  mkrum     sra       0.002       0.963   0.185  HOLDS                        HOLDS
 2  4   fang_h  mkrum sra_l10       0.002       0.963   0.185  HOLDS                        HOLDS
 2  4   fang_h  mkrum sra_cap       0.002       0.963   0.185  HOLDS                        HOLDS
 2  4    split  cwmed    base       0.004       0.783   0.000  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4    split  cwmed     sra       0.004       0.959   1.000  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4    split  cwmed sra_l10       0.004       0.959   1.000  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4    split  cwmed sra_cap       0.004       0.959   1.000  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4    split trmean    base       0.004       0.858   0.000  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4    split trmean     sra       0.004       0.959   1.000  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4    split trmean sra_l10       0.004       0.959   1.000  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4    split trmean sra_cap       0.004       0.959   1.000  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4    split  mkrum    base       0.004       0.960   1.000  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4    split  mkrum     sra       0.004       0.959   1.000  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4    split  mkrum sra_l10       0.004       0.959   1.000  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4    split  mkrum sra_cap       0.004       0.959   1.000  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
```


## Brute Force | M6 clean reference (mimic, no model poisoning): target recall
```
arm          base  sra  sra_cap  sra_l10
k f agg                                 
2 0 fedavg  1.000  NaN      NaN      NaN
  4 cwmed   0.000  0.0      0.0      0.0
    mkrum   0.000  0.0      0.0      0.0
    trmean  0.000  0.0      0.0      0.0
3 0 fedavg  1.000  NaN      NaN      NaN
  2 cwmed   0.000  1.0      1.0      1.0
    mkrum   0.000  1.0      1.0      1.0
    trmean  0.684  1.0      1.0      1.0
6 0 fedavg  1.000  NaN      NaN      NaN
  2 cwmed   0.000  1.0      1.0      1.0
    mkrum   1.000  1.0      1.0      1.0
    trmean  1.000  1.0      1.0      1.0
  4 cwmed   0.000  1.0      1.0      1.0
    mkrum   1.000  1.0      1.0      1.0
    trmean  0.999  1.0      1.0      1.0
```


## Brute Force | M6 paired verdict counts by arm, zone, attack
```
paired                     BREAKS  HOLDS
arm     zone     attack                 
sra     f<=F_HAT alie_w         0      6
                 fang_h         0      6
                 fang_w         0      6
                 minmax_h       0      6
                 minmax_w       0      6
                 split          0      6
        f>F_HAT  alie_w         0      6
                 fang_h         0      6
                 fang_w         0      6
                 minmax_h       1      5
                 minmax_w       0      6
                 split          0      6
sra_cap f<=F_HAT alie_w         0      6
                 fang_h         0      6
                 fang_w         0      6
                 minmax_h       0      6
                 minmax_w       0      6
                 split          0      6
        f>F_HAT  alie_w         0      6
                 fang_h         0      6
                 fang_w         0      6
                 minmax_h       2      4
                 minmax_w       0      6
                 split          0      6
sra_l10 f<=F_HAT alie_w         0      6
                 fang_h         0      6
                 fang_w         0      6
                 minmax_h       0      6
                 minmax_w       0      6
                 split          0      6
        f>F_HAT  alie_w         0      6
                 fang_h         0      6
                 fang_w         0      6
                 minmax_h       1      5
                 minmax_w       0      6
                 split          0      6
```


## Brute Force | M6 verdicts (f <= F_HAT, k > f cells: (3,2) and (6,2))
```
M6_sra: SURVIVES_ADAPTIVE
M6_sra_l10: SURVIVES_ADAPTIVE
M6_sra_cap: SURVIVES_ADAPTIVE
M6_sra_detail: 36/36 paired HOLDS; coverage 36/36
M6_sra_l10_detail: 36/36 paired HOLDS; coverage 36/36
M6_sra_cap_detail: 36/36 paired HOLDS; coverage 36/36
worst SRA cells by target recall:
 k  f attack    agg  target  benign_fpr  other_mean
 3  2 fang_w  cwmed     1.0       0.003       0.959
 3  2 fang_w trmean     1.0       0.003       0.960
 3  2 fang_w  mkrum     1.0       0.003       0.960
```


## Brute Force | M7 attack damage with and without DP (k=6, f=2)
```
   agg  arm   attack FPR clean/att (non-DP) FPR clean/att (DP) other clean/att (non-DP) other clean/att (DP) target att non-DP / DP
 cwmed base signflip            0.004/0.004        0.007/0.009              0.960/0.959          0.745/0.744            0.000/1.000
 cwmed base     alie            0.004/0.003        0.007/0.006              0.960/0.960          0.745/0.715            0.000/0.000
 cwmed base   fang_w            0.004/0.004        0.007/0.007              0.960/0.960          0.745/0.745            0.000/0.952
 cwmed base minmax_h            0.004/0.004        0.007/0.009              0.960/0.959          0.745/0.744            0.000/1.000
 cwmed  sra signflip            0.003/0.004        0.007/0.009              0.960/0.959          0.745/0.744            1.000/1.000
 cwmed  sra     alie            0.003/0.003        0.007/0.006              0.960/0.960          0.745/0.704            1.000/0.333
 cwmed  sra   fang_w            0.003/0.004        0.007/0.006              0.960/0.960          0.745/0.745            1.000/0.996
 cwmed  sra minmax_h            0.003/0.004        0.007/0.008              0.960/0.960          0.745/0.744            1.000/1.000
trmean base signflip            0.003/0.004        0.007/0.010              0.960/0.960          0.746/0.744            1.000/1.000
trmean base     alie            0.003/0.003        0.007/0.006              0.960/0.961          0.746/0.733            1.000/0.456
trmean base   fang_w            0.003/0.004        0.007/0.007              0.960/0.960          0.746/0.746            1.000/0.000
trmean base minmax_h            0.003/0.004        0.007/0.009              0.960/0.960          0.746/0.745            1.000/1.000
trmean  sra signflip            0.003/0.004        0.007/0.009              0.960/0.960          0.745/0.744            1.000/1.000
trmean  sra     alie            0.003/0.003        0.007/0.025              0.960/0.960          0.745/0.693            1.000/0.423
trmean  sra   fang_w            0.003/0.004        0.007/0.007              0.960/0.960          0.745/0.745            1.000/0.964
trmean  sra minmax_h            0.003/0.004        0.007/0.008              0.960/0.960          0.745/0.744            1.000/1.000
 mkrum base signflip            0.003/0.003        0.007/0.007              0.961/0.961          0.745/0.745            1.000/1.000
 mkrum base     alie            0.003/0.003        0.007/0.006              0.961/0.961          0.745/0.735            1.000/1.000
 mkrum base   fang_w            0.003/0.003        0.007/0.007              0.961/0.961          0.745/0.745            1.000/1.000
 mkrum base minmax_h            0.003/0.004        0.007/0.009              0.961/0.960          0.745/0.744            1.000/1.000
 mkrum  sra signflip            0.003/0.004        0.007/0.009              0.960/0.943          0.745/0.744            1.000/1.000
 mkrum  sra     alie            0.003/0.003        0.007/0.006              0.960/0.961          0.745/0.680            1.000/0.666
 mkrum  sra   fang_w            0.003/0.003        0.007/0.007              0.960/0.960          0.745/0.745            1.000/0.756
 mkrum  sra minmax_h            0.003/0.004        0.007/0.008              0.960/0.960          0.745/0.744            1.000/1.000
```


## Brute Force | M7 verdicts
```
M7_base_dp: DP_KEEPS_ROBUSTNESS (share 0.00)
M7_sra_vs_base_under_dp: 11/12 HOLDS (paired)
```


## Brute Force | M9 k* point [5%, 95%] bootstrap over seeds -- seeds 0-2 (mit-2) + 3-4 (mit-3) ('9' = never)
```
 f    agg  FedAvg    base     sra sra_l10
 0  cwmed 2 [1,2] 9 [9,9] 2 [2,2] 1 [1,2]
 0 trmean 2 [1,2] 3 [3,3] 2 [2,2] 1 [1,2]
 0  mkrum 2 [1,2] 4 [4,4] 2 [2,2] 1 [1,2]
 2  cwmed 3 [3,3] 9 [9,9] 3 [3,3] 3 [3,3]
 2 trmean 3 [3,3] 4 [3,4] 3 [3,3] 3 [3,3]
 2  mkrum 3 [3,3] 6 [6,6] 3 [3,3] 3 [3,3]
 4  cwmed 6 [6,6] 9 [9,9] 6 [6,6] 6 [6,6]
 4 trmean 6 [6,6] 6 [6,6] 6 [6,6] 6 [6,6]
 4  mkrum 6 [6,6] 6 [6,6] 6 [6,6] 6 [6,6]
```


## Botnet | M8 target recall at k=5, f=4 (floor = 5; learnable line 0.796)
```
                 mean    std
agg    arm                  
cwmed  base     0.000  0.000
       sra      0.995  0.000
       sra_cap  0.994  0.000
       sra_l10  0.995  0.000
fedavg base     0.450  0.055
mkrum  base     0.000  0.000
       sra      0.995  0.000
       sra_cap  0.994  0.000
       sra_l10  0.995  0.000
trmean base     0.288  0.101
       sra      0.995  0.000
       sra_cap  0.994  0.000
       sra_l10  0.995  0.000
```


## Botnet | M8 verdicts
```
M8_base: FLOOR_NOT_REACHED
M8_sra: FLOOR_MEASURED
M8_sra_l10: FLOOR_MEASURED
M8_sra_cap: FLOOR_MEASURED
M8_fedavg_recall: 0.45
```


## Botnet | M3c k* of sra_cap (cap = 5 members)
```
 f    agg  FedAvg  sra_cap  tax  sra (mit-2)
 0  cwmed       2        2    0            2
 0 trmean       2        2    0            2
 0  mkrum       2        2    0            2
 2  cwmed       4        3    0            3
 2 trmean       4        3    0            3
 2  mkrum       4        3    0            3
 4  cwmed       6        6    0            6
 4 trmean       6        6    0            6
 4  mkrum       6        6    0            6
```


## Botnet | M3c verdict
```
floor (pre-registered rule): ABOVE_FLOOR | grid-censored share: 0.67
```


## Botnet | M6 all cells (target = rare-class recall under attack; learnable line 0.796)
```
 k  f   attack    agg     arm  benign_fpr  other_mean  target paired                     absolute
 3  2   fang_w  cwmed    base       0.001       0.962   0.000  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2   fang_w  cwmed     sra       0.001       0.961   0.995  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2   fang_w  cwmed sra_l10       0.001       0.961   0.995  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2   fang_w  cwmed sra_cap       0.001       0.961   0.995  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2   fang_w trmean    base       0.001       0.963   0.000  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2   fang_w trmean     sra       0.001       0.962   0.995  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2   fang_w trmean sra_l10       0.001       0.962   0.995  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2   fang_w trmean sra_cap       0.001       0.962   0.995  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2   fang_w  mkrum    base       0.001       0.964   0.996  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2   fang_w  mkrum     sra       0.001       0.964   0.995  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2   fang_w  mkrum sra_l10       0.001       0.964   0.995  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2   fang_w  mkrum sra_cap       0.001       0.964   0.995  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2 minmax_w  cwmed    base       0.001       0.962   0.000  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2 minmax_w  cwmed     sra       0.001       0.962   0.995  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2 minmax_w  cwmed sra_l10       0.001       0.962   0.995  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2 minmax_w  cwmed sra_cap       0.001       0.962   0.995  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2 minmax_w trmean    base       0.001       0.962   0.118  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2 minmax_w trmean     sra       0.001       0.962   0.995  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2 minmax_w trmean sra_l10       0.001       0.962   0.995  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2 minmax_w trmean sra_cap       0.001       0.962   0.995  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2 minmax_w  mkrum    base       0.001       0.964   0.000  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2 minmax_w  mkrum     sra       0.001       0.963   0.995  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2 minmax_w  mkrum sra_l10       0.001       0.963   0.995  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2 minmax_w  mkrum sra_cap       0.001       0.963   0.995  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2   alie_w  cwmed    base       0.001       0.962   0.000  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2   alie_w  cwmed     sra       0.001       0.962   0.996  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2   alie_w  cwmed sra_l10       0.001       0.962   0.996  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2   alie_w  cwmed sra_cap       0.001       0.962   0.996  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2   alie_w trmean    base       0.001       0.962   0.985  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2   alie_w trmean     sra       0.001       0.962   0.995  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2   alie_w trmean sra_l10       0.001       0.962   0.995  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2   alie_w trmean sra_cap       0.001       0.962   0.995  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2   alie_w  mkrum    base       0.001       0.963   0.029  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2   alie_w  mkrum     sra       0.001       0.963   0.995  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2   alie_w  mkrum sra_l10       0.001       0.963   0.995  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2   alie_w  mkrum sra_cap       0.001       0.963   0.995  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2 minmax_h  cwmed    base       0.001       0.961   0.000  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2 minmax_h  cwmed     sra       0.001       0.961   0.995  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2 minmax_h  cwmed sra_l10       0.001       0.961   0.995  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2 minmax_h  cwmed sra_cap       0.001       0.961   0.995  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2 minmax_h trmean    base       0.001       0.961   0.384  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2 minmax_h trmean     sra       0.001       0.961   0.995  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2 minmax_h trmean sra_l10       0.001       0.961   0.995  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2 minmax_h trmean sra_cap       0.001       0.961   0.995  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2 minmax_h  mkrum    base       0.001       0.962   0.000  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2 minmax_h  mkrum     sra       0.001       0.961   0.995  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2 minmax_h  mkrum sra_l10       0.001       0.961   0.995  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2 minmax_h  mkrum sra_cap       0.001       0.961   0.995  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2   fang_h  cwmed    base       0.001       0.962   0.000  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2   fang_h  cwmed     sra       0.001       0.961   0.995  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2   fang_h  cwmed sra_l10       0.001       0.961   0.995  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2   fang_h  cwmed sra_cap       0.001       0.961   0.995  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2   fang_h trmean    base       0.001       0.963   0.000  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2   fang_h trmean     sra       0.001       0.961   0.994  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2   fang_h trmean sra_l10       0.001       0.961   0.994  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2   fang_h trmean sra_cap       0.001       0.961   0.994  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2   fang_h  mkrum    base       0.001       0.964   0.996  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2   fang_h  mkrum     sra       0.001       0.964   0.995  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2   fang_h  mkrum sra_l10       0.001       0.964   0.995  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2   fang_h  mkrum sra_cap       0.001       0.964   0.995  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2    split  cwmed    base       0.001       0.961   0.000  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2    split  cwmed     sra       0.001       0.962   0.995  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2    split  cwmed sra_l10       0.001       0.962   0.995  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2    split  cwmed sra_cap       0.001       0.962   0.995  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2    split trmean    base       0.001       0.961   0.001  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2    split trmean     sra       0.001       0.962   0.995  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2    split trmean sra_l10       0.001       0.962   0.995  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2    split trmean sra_cap       0.001       0.962   0.995  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2    split  mkrum    base       0.001       0.962   0.994  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2    split  mkrum     sra       0.001       0.963   0.995  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2    split  mkrum sra_l10       0.001       0.963   0.995  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2    split  mkrum sra_cap       0.001       0.963   0.995  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2   fang_w  cwmed    base       0.001       0.961   0.000  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2   fang_w  cwmed     sra       0.001       0.961   0.995  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2   fang_w  cwmed sra_l10       0.001       0.961   0.995  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2   fang_w  cwmed sra_cap       0.001       0.960   0.995  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2   fang_w trmean    base       0.001       0.964   0.995  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2   fang_w trmean     sra       0.001       0.961   0.995  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2   fang_w trmean sra_l10       0.001       0.961   0.995  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2   fang_w trmean sra_cap       0.001       0.961   0.995  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2   fang_w  mkrum    base       0.001       0.965   0.995  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2   fang_w  mkrum     sra       0.001       0.962   0.995  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2   fang_w  mkrum sra_l10       0.001       0.962   0.995  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2   fang_w  mkrum sra_cap       0.001       0.963   0.995  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2 minmax_w  cwmed    base       0.001       0.962   0.000  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2 minmax_w  cwmed     sra       0.001       0.961   0.995  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2 minmax_w  cwmed sra_l10       0.001       0.961   0.995  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2 minmax_w  cwmed sra_cap       0.001       0.960   0.995  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2 minmax_w trmean    base       0.001       0.962   0.995  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2 minmax_w trmean     sra       0.001       0.962   0.995  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2 minmax_w trmean sra_l10       0.001       0.962   0.995  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2 minmax_w trmean sra_cap       0.001       0.961   0.995  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2 minmax_w  mkrum    base       0.001       0.965   0.995  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2 minmax_w  mkrum     sra       0.001       0.963   0.995  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2 minmax_w  mkrum sra_l10       0.001       0.963   0.995  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2 minmax_w  mkrum sra_cap       0.001       0.963   0.995  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2   alie_w  cwmed    base       0.001       0.962   0.003  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2   alie_w  cwmed     sra       0.001       0.962   0.995  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2   alie_w  cwmed sra_l10       0.001       0.962   0.995  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2   alie_w  cwmed sra_cap       0.001       0.961   0.995  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2   alie_w trmean    base       0.001       0.962   0.995  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2   alie_w trmean     sra       0.001       0.962   0.995  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2   alie_w trmean sra_l10       0.001       0.962   0.995  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2   alie_w trmean sra_cap       0.001       0.962   0.995  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2   alie_w  mkrum    base       0.001       0.965   0.995  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2   alie_w  mkrum     sra       0.001       0.964   0.995  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2   alie_w  mkrum sra_l10       0.001       0.964   0.995  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2   alie_w  mkrum sra_cap       0.001       0.964   0.995  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2 minmax_h  cwmed    base       0.001       0.960   0.000  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2 minmax_h  cwmed     sra       0.001       0.960   0.995  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2 minmax_h  cwmed sra_l10       0.001       0.960   0.995  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2 minmax_h  cwmed sra_cap       0.001       0.960   0.995  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2 minmax_h trmean    base       0.001       0.961   0.995  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2 minmax_h trmean     sra       0.001       0.961   0.995  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2 minmax_h trmean sra_l10       0.001       0.961   0.995  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2 minmax_h trmean sra_cap       0.001       0.960   0.995  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2 minmax_h  mkrum    base       0.001       0.962   0.995  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2 minmax_h  mkrum     sra       0.001       0.960   0.995  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2 minmax_h  mkrum sra_l10       0.001       0.960   0.995  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2 minmax_h  mkrum sra_cap       0.001       0.961   0.995  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2   fang_h  cwmed    base       0.001       0.961   0.000  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2   fang_h  cwmed     sra       0.001       0.960   0.995  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2   fang_h  cwmed sra_l10       0.001       0.960   0.995  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2   fang_h  cwmed sra_cap       0.001       0.960   0.995  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2   fang_h trmean    base       0.001       0.964   0.995  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2   fang_h trmean     sra       0.001       0.963   0.995  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2   fang_h trmean sra_l10       0.001       0.963   0.995  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2   fang_h trmean sra_cap       0.001       0.962   0.995  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2   fang_h  mkrum    base       0.001       0.965   0.995  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2   fang_h  mkrum     sra       0.001       0.964   0.995  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2   fang_h  mkrum sra_l10       0.001       0.964   0.995  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2   fang_h  mkrum sra_cap       0.001       0.965   0.995  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2    split  cwmed    base       0.001       0.960   0.000  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2    split  cwmed     sra       0.001       0.961   0.995  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2    split  cwmed sra_l10       0.001       0.961   0.995  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2    split  cwmed sra_cap       0.001       0.960   0.995  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2    split trmean    base       0.001       0.962   0.995  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2    split trmean     sra       0.001       0.961   0.995  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2    split trmean sra_l10       0.001       0.961   0.995  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2    split trmean sra_cap       0.001       0.961   0.995  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2    split  mkrum    base       0.001       0.965   0.995  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2    split  mkrum     sra       0.001       0.963   0.995  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2    split  mkrum sra_l10       0.001       0.963   0.995  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2    split  mkrum sra_cap       0.001       0.964   0.995  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4   fang_w  cwmed    base       0.001       0.961   0.000  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4   fang_w  cwmed     sra       0.001       0.960   0.995  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4   fang_w  cwmed sra_l10       0.001       0.960   0.995  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4   fang_w  cwmed sra_cap       0.001       0.960   0.994  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4   fang_w trmean    base       0.001       0.960   0.000  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4   fang_w trmean     sra       0.001       0.960   0.995  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4   fang_w trmean sra_l10       0.001       0.960   0.995  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4   fang_w trmean sra_cap       0.001       0.960   0.994  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4   fang_w  mkrum    base       0.001       0.960   0.811  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4   fang_w  mkrum     sra       0.001       0.961   0.995  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4   fang_w  mkrum sra_l10       0.001       0.961   0.995  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4   fang_w  mkrum sra_cap       0.001       0.960   0.994  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4 minmax_w  cwmed    base       0.001       0.961   0.000  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4 minmax_w  cwmed     sra       0.001       0.960   0.995  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4 minmax_w  cwmed sra_l10       0.001       0.960   0.995  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4 minmax_w  cwmed sra_cap       0.001       0.960   0.995  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4 minmax_w trmean    base       0.001       0.961   0.995  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4 minmax_w trmean     sra       0.001       0.961   0.995  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4 minmax_w trmean sra_l10       0.001       0.961   0.995  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4 minmax_w trmean sra_cap       0.001       0.960   0.995  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4 minmax_w  mkrum    base       0.001       0.960   0.994  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4 minmax_w  mkrum     sra       0.001       0.961   0.995  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4 minmax_w  mkrum sra_l10       0.001       0.961   0.995  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4 minmax_w  mkrum sra_cap       0.001       0.960   0.995  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4   alie_w  cwmed    base       0.001       0.960   0.993  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4   alie_w  cwmed     sra       0.001       0.960   0.995  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4   alie_w  cwmed sra_l10       0.001       0.960   0.995  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4   alie_w  cwmed sra_cap       0.001       0.960   0.995  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4   alie_w trmean    base       0.001       0.961   0.995  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4   alie_w trmean     sra       0.001       0.961   0.995  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4   alie_w trmean sra_l10       0.001       0.961   0.995  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4   alie_w trmean sra_cap       0.001       0.960   0.995  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4   alie_w  mkrum    base       0.001       0.961   0.995  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4   alie_w  mkrum     sra       0.001       0.960   0.995  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4   alie_w  mkrum sra_l10       0.001       0.960   0.995  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4   alie_w  mkrum sra_cap       0.001       0.960   0.995  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4 minmax_h  cwmed    base       0.002       0.960   0.000  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4 minmax_h  cwmed     sra       0.002       0.960   0.997  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4 minmax_h  cwmed sra_l10       0.002       0.960   0.997  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4 minmax_h  cwmed sra_cap       0.002       0.960   0.996  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4 minmax_h trmean    base       0.003       0.960   0.995  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4 minmax_h trmean     sra       0.003       0.960   0.996  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4 minmax_h trmean sra_l10       0.003       0.960   0.996  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4 minmax_h trmean sra_cap       0.003       0.960   0.996  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4 minmax_h  mkrum    base       0.003       0.960   0.995  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4 minmax_h  mkrum     sra       0.003       0.960   0.996  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4 minmax_h  mkrum sra_l10       0.003       0.960   0.996  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4 minmax_h  mkrum sra_cap       0.003       0.960   0.996  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4   fang_h  cwmed    base       0.001       0.961   0.000  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4   fang_h  cwmed     sra       0.001       0.960   0.995  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4   fang_h  cwmed sra_l10       0.001       0.960   0.995  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4   fang_h  cwmed sra_cap       0.001       0.960   0.995  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4   fang_h trmean    base       0.001       0.960   0.000  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4   fang_h trmean     sra       0.001       0.961   0.466  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4   fang_h trmean sra_l10       0.001       0.961   0.466  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4   fang_h trmean sra_cap       0.001       0.961   0.049  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4   fang_h  mkrum    base       0.001       0.960   0.811  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4   fang_h  mkrum     sra       0.001       0.960   0.994  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4   fang_h  mkrum sra_l10       0.001       0.960   0.994  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4   fang_h  mkrum sra_cap       0.001       0.961   0.952  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4    split  cwmed    base       0.001       0.960   0.000  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4    split  cwmed     sra       0.001       0.960   0.995  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4    split  cwmed sra_l10       0.001       0.960   0.995  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4    split  cwmed sra_cap       0.001       0.960   0.995  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4    split trmean    base       0.001       0.960   0.995  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4    split trmean     sra       0.001       0.960   0.995  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4    split trmean sra_l10       0.001       0.960   0.995  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4    split trmean sra_cap       0.001       0.960   0.995  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4    split  mkrum    base       0.001       0.960   0.998  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4    split  mkrum     sra       0.001       0.960   0.995  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4    split  mkrum sra_l10       0.001       0.960   0.995  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4    split  mkrum sra_cap       0.001       0.960   0.995  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4   fang_w  cwmed    base       0.001       0.962   0.000  (ref)                        HOLDS
 2  4   fang_w  cwmed     sra       0.001       0.960   0.995  HOLDS                        HOLDS
 2  4   fang_w  cwmed sra_l10       0.001       0.960   0.995  HOLDS                        HOLDS
 2  4   fang_w  cwmed sra_cap       0.001       0.961   0.995  HOLDS                        HOLDS
 2  4   fang_w trmean    base       0.443       0.069   0.000  (ref)                       BREAKS
 2  4   fang_w trmean     sra       0.001       0.961   0.995  HOLDS                        HOLDS
 2  4   fang_w trmean sra_l10       0.001       0.961   0.995  HOLDS                        HOLDS
 2  4   fang_w trmean sra_cap       0.001       0.961   0.995  HOLDS                        HOLDS
 2  4   fang_w  mkrum    base       0.670       0.099   0.000  (ref)                       BREAKS
 2  4   fang_w  mkrum     sra       0.001       0.962   0.995  HOLDS                        HOLDS
 2  4   fang_w  mkrum sra_l10       0.001       0.962   0.995  HOLDS                        HOLDS
 2  4   fang_w  mkrum sra_cap       0.001       0.962   0.995  HOLDS                        HOLDS
 2  4 minmax_w  cwmed    base       0.001       0.962   0.000  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4 minmax_w  cwmed     sra       0.001       0.962   0.996  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4 minmax_w  cwmed sra_l10       0.001       0.962   0.996  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4 minmax_w  cwmed sra_cap       0.001       0.962   0.995  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4 minmax_w trmean    base       0.001       0.963   0.000  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4 minmax_w trmean     sra       0.001       0.963   0.995  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4 minmax_w trmean sra_l10       0.001       0.963   0.995  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4 minmax_w trmean sra_cap       0.001       0.962   0.995  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4 minmax_w  mkrum    base       0.001       0.964   0.000  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4 minmax_w  mkrum     sra       0.001       0.963   0.995  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4 minmax_w  mkrum sra_l10       0.001       0.963   0.995  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4 minmax_w  mkrum sra_cap       0.001       0.963   0.995  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4   alie_w  cwmed    base       0.001       0.962   0.000  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4   alie_w  cwmed     sra       0.001       0.959   0.994  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4   alie_w  cwmed sra_l10       0.001       0.959   0.992  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4   alie_w  cwmed sra_cap       0.001       0.959   0.994  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4   alie_w trmean    base       0.001       0.963   0.000  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4   alie_w trmean     sra       0.001       0.960   0.994  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4   alie_w trmean sra_l10       0.001       0.960   0.994  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4   alie_w trmean sra_cap       0.001       0.960   0.995  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4   alie_w  mkrum    base       0.001       0.964   0.000  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4   alie_w  mkrum     sra       0.001       0.960   0.994  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4   alie_w  mkrum sra_l10       0.001       0.960   0.993  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4   alie_w  mkrum sra_cap       0.001       0.960   0.995  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4 minmax_h  cwmed    base       0.001       0.960   0.000  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4 minmax_h  cwmed     sra       0.001       0.960   0.996  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4 minmax_h  cwmed sra_l10       0.001       0.960   0.996  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4 minmax_h  cwmed sra_cap       0.001       0.960   0.996  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4 minmax_h trmean    base       0.001       0.961   0.000  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4 minmax_h trmean     sra       0.002       0.960   0.996  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4 minmax_h trmean sra_l10       0.002       0.960   0.996  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4 minmax_h trmean sra_cap       0.002       0.960   0.996  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4 minmax_h  mkrum    base       0.001       0.962   0.000  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4 minmax_h  mkrum     sra       0.003       0.960   0.996  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4 minmax_h  mkrum sra_l10       0.003       0.960   0.996  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4 minmax_h  mkrum sra_cap       0.003       0.960   0.996  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4   fang_h  cwmed    base       0.001       0.962   0.000  (ref)                        HOLDS
 2  4   fang_h  cwmed     sra       0.001       0.962   0.466  HOLDS                        HOLDS
 2  4   fang_h  cwmed sra_l10       0.001       0.962   0.466  HOLDS                        HOLDS
 2  4   fang_h  cwmed sra_cap       0.001       0.962   0.466  HOLDS                        HOLDS
 2  4   fang_h trmean    base       0.443       0.069   0.000  (ref)                       BREAKS
 2  4   fang_h trmean     sra       0.001       0.967   0.000  HOLDS                        HOLDS
 2  4   fang_h trmean sra_l10       0.001       0.967   0.000  HOLDS                        HOLDS
 2  4   fang_h trmean sra_cap       0.001       0.967   0.000  HOLDS                        HOLDS
 2  4   fang_h  mkrum    base       0.670       0.099   0.000  (ref)                       BREAKS
 2  4   fang_h  mkrum     sra       0.001       0.968   0.000  HOLDS                        HOLDS
 2  4   fang_h  mkrum sra_l10       0.001       0.968   0.000  HOLDS                        HOLDS
 2  4   fang_h  mkrum sra_cap       0.001       0.968   0.000  HOLDS                        HOLDS
 2  4    split  cwmed    base       0.001       0.962   0.000  (ref)                        HOLDS
 2  4    split  cwmed     sra       0.001       0.960   0.995  HOLDS                        HOLDS
 2  4    split  cwmed sra_l10       0.001       0.960   0.995  HOLDS                        HOLDS
 2  4    split  cwmed sra_cap       0.001       0.960   0.995  HOLDS                        HOLDS
 2  4    split trmean    base       0.001       0.963   0.000  (ref)                        HOLDS
 2  4    split trmean     sra       0.001       0.962   0.995  HOLDS                        HOLDS
 2  4    split trmean sra_l10       0.001       0.962   0.995  HOLDS                        HOLDS
 2  4    split trmean sra_cap       0.001       0.962   0.995  HOLDS                        HOLDS
 2  4    split  mkrum    base       0.001       0.962   0.995  (ref)                        HOLDS
 2  4    split  mkrum     sra       0.001       0.961   0.995  HOLDS                        HOLDS
 2  4    split  mkrum sra_l10       0.001       0.961   0.995  HOLDS                        HOLDS
 2  4    split  mkrum sra_cap       0.001       0.961   0.995  HOLDS                        HOLDS
```


## Botnet | M6 clean reference (mimic, no model poisoning): target recall
```
arm          base    sra  sra_cap  sra_l10
k f agg                                   
2 0 fedavg  0.994    NaN      NaN      NaN
  4 cwmed   0.000  0.000    0.000    0.000
    mkrum   0.000  0.000    0.000    0.000
    trmean  0.000  0.000    0.000    0.000
3 0 fedavg  0.995    NaN      NaN      NaN
  2 cwmed   0.000  0.996    0.996    0.996
    mkrum   0.000  0.996    0.996    0.996
    trmean  0.000  0.996    0.996    0.996
6 0 fedavg  0.995    NaN      NaN      NaN
  2 cwmed   0.000  0.995    0.995    0.995
    mkrum   0.995  0.995    0.995    0.995
    trmean  0.995  0.995    0.995    0.995
  4 cwmed   0.000  0.996    0.994    0.996
    mkrum   0.745  0.996    0.994    0.996
    trmean  0.989  0.996    0.994    0.996
```


## Botnet | M6 paired verdict counts by arm, zone, attack
```
paired                     HOLDS
arm     zone     attack         
sra     f<=F_HAT alie_w        6
                 fang_h        6
                 fang_w        6
                 minmax_h      6
                 minmax_w      6
                 split         6
        f>F_HAT  alie_w        6
                 fang_h        6
                 fang_w        6
                 minmax_h      6
                 minmax_w      6
                 split         6
sra_cap f<=F_HAT alie_w        6
                 fang_h        6
                 fang_w        6
                 minmax_h      6
                 minmax_w      6
                 split         6
        f>F_HAT  alie_w        6
                 fang_h        6
                 fang_w        6
                 minmax_h      6
                 minmax_w      6
                 split         6
sra_l10 f<=F_HAT alie_w        6
                 fang_h        6
                 fang_w        6
                 minmax_h      6
                 minmax_w      6
                 split         6
        f>F_HAT  alie_w        6
                 fang_h        6
                 fang_w        6
                 minmax_h      6
                 minmax_w      6
                 split         6
```


## Botnet | M6 verdicts (f <= F_HAT, k > f cells: (3,2) and (6,2))
```
M6_sra: SURVIVES_ADAPTIVE
M6_sra_l10: SURVIVES_ADAPTIVE
M6_sra_cap: SURVIVES_ADAPTIVE
M6_sra_detail: 36/36 paired HOLDS; coverage 36/36
M6_sra_l10_detail: 36/36 paired HOLDS; coverage 36/36
M6_sra_cap_detail: 36/36 paired HOLDS; coverage 36/36
worst SRA cells by target recall:
 k  f attack    agg  target  benign_fpr  other_mean
 3  2 fang_h trmean   0.994       0.001       0.961
 3  2 fang_w  cwmed   0.995       0.001       0.961
 3  2 fang_w  mkrum   0.995       0.001       0.964
```


## Botnet | M7 attack damage with and without DP (k=6, f=2)
```
   agg  arm   attack FPR clean/att (non-DP) FPR clean/att (DP) other clean/att (non-DP) other clean/att (DP) target att non-DP / DP
 cwmed base signflip            0.001/0.001        0.004/0.008              0.961/0.960          0.783/0.745            0.000/0.996
 cwmed base     alie            0.001/0.001        0.004/0.004              0.961/0.961          0.783/0.724            0.000/0.000
 cwmed base   fang_w            0.001/0.001        0.004/0.005              0.961/0.961          0.783/0.766            0.000/0.617
 cwmed base minmax_h            0.001/0.001        0.004/0.008              0.961/0.960          0.783/0.745            0.000/0.996
 cwmed  sra signflip            0.001/0.001        0.005/0.008              0.962/0.960          0.818/0.745            0.995/0.997
 cwmed  sra     alie            0.001/0.001        0.005/0.004              0.962/0.962          0.818/0.720            0.996/0.000
 cwmed  sra   fang_w            0.001/0.001        0.005/0.005              0.962/0.961          0.818/0.757            0.995/0.847
 cwmed  sra minmax_h            0.001/0.001        0.005/0.007              0.962/0.960          0.818/0.745            0.995/0.996
trmean base signflip            0.001/0.001        0.005/0.008              0.962/0.960          0.780/0.745            0.995/0.995
trmean base     alie            0.001/0.001        0.005/0.005              0.962/0.964          0.780/0.730            0.995/0.000
trmean base   fang_w            0.001/0.001        0.005/0.005              0.962/0.964          0.780/0.745            0.995/0.000
trmean base minmax_h            0.001/0.001        0.005/0.007              0.962/0.961          0.780/0.746            0.995/0.996
trmean  sra signflip            0.001/0.001        0.005/0.007              0.962/0.960          0.787/0.745            0.995/0.996
trmean  sra     alie            0.001/0.001        0.005/0.005              0.962/0.962          0.787/0.721            0.995/0.000
trmean  sra   fang_w            0.001/0.001        0.005/0.005              0.962/0.961          0.787/0.746            0.995/0.684
trmean  sra minmax_h            0.001/0.001        0.005/0.007              0.962/0.961          0.787/0.745            0.995/0.996
 mkrum base signflip            0.001/0.001        0.005/0.005              0.965/0.965          0.783/0.753            0.995/0.995
 mkrum base     alie            0.001/0.001        0.005/0.005              0.965/0.965          0.783/0.733            0.995/0.000
 mkrum base   fang_w            0.001/0.001        0.005/0.005              0.965/0.965          0.783/0.753            0.995/0.995
 mkrum base minmax_h            0.001/0.001        0.005/0.008              0.965/0.962          0.783/0.746            0.995/0.995
 mkrum  sra signflip            0.001/0.001        0.005/0.008              0.964/0.961          0.782/0.745            0.995/0.996
 mkrum  sra     alie            0.001/0.001        0.005/0.004              0.964/0.964          0.782/0.719            0.995/0.000
 mkrum  sra   fang_w            0.001/0.001        0.005/0.004              0.964/0.962          0.782/0.746            0.995/0.970
 mkrum  sra minmax_h            0.001/0.001        0.005/0.008              0.964/0.960          0.782/0.745            0.995/0.995
```


## Botnet | M7 verdicts
```
M7_base_dp: DP_KEEPS_ROBUSTNESS (share 0.17)
M7_sra_vs_base_under_dp: 12/12 HOLDS (paired)
```


## Botnet | M9 k* point [5%, 95%] bootstrap over seeds -- seeds 0-2 (mit-2) + 3-4 (mit-3) ('9' = never)
```
 f    agg  FedAvg    base     sra sra_l10
 0  cwmed 1 [1,2] 9 [9,9] 2 [2,2] 2 [1,2]
 0 trmean 1 [1,2] 4 [3,4] 2 [2,2] 2 [1,2]
 0  mkrum 1 [1,2] 4 [4,4] 2 [2,2] 2 [1,2]
 2  cwmed 4 [4,4] 9 [9,9] 3 [3,3] 3 [3,3]
 2 trmean 4 [4,4] 4 [4,4] 3 [3,3] 3 [3,3]
 2  mkrum 4 [4,4] 6 [6,6] 3 [3,3] 3 [3,3]
 4  cwmed 6 [6,6] 9 [9,9] 6 [6,6] 6 [6,6]
 4 trmean 6 [6,6] 6 [6,6] 6 [6,6] 6 [6,6]
 4  mkrum 6 [6,6] 6 [6,8] 6 [6,6] 6 [6,6]
```
