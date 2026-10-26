# mit-3 (final) summary -- CICIDS2017

## Botnet | verdicts
```
M8_base: FLOOR_NOT_REACHED
M8_sra: FLOOR_MEASURED
M8_sra_l10: FLOOR_MEASURED
M8_sra_cap: FLOOR_MEASURED
M8_fedavg_recall: 0.623
M3c_sra_cap_floor: ABOVE_FLOOR
M3c_sra_cap_censored_share: 0.67
M6_sra: SURVIVES_ADAPTIVE
M6_sra_l10: SURVIVES_ADAPTIVE
M6_sra_cap: SURVIVES_ADAPTIVE
M6_sra_detail: 36/36 paired HOLDS; coverage 35/36
M6_sra_l10_detail: 36/36 paired HOLDS; coverage 36/36
M6_sra_cap_detail: 36/36 paired HOLDS; coverage 35/36
M7_base_dp: DP_ERODES_ROBUSTNESS (share 0.42)
M7_sra_vs_base_under_dp: 11/12 HOLDS (paired)
M9_seeds: seeds 0-2 (mit-2) + 3-4 (mit-3)
```

## Portscan | verdicts
```
M8_base: FLOOR_NOT_REACHED
M8_sra: FLOOR_MEASURED
M8_sra_l10: FLOOR_MEASURED
M8_sra_cap: FLOOR_MEASURED
M8_fedavg_recall: 0.358
M3c_sra_cap_floor: ABOVE_FLOOR
M3c_sra_cap_censored_share: 0.89
M6_sra: SURVIVES_ADAPTIVE
M6_sra_l10: SURVIVES_ADAPTIVE
M6_sra_cap: SURVIVES_ADAPTIVE
M6_sra_detail: 36/36 paired HOLDS; coverage 36/36
M6_sra_l10_detail: 36/36 paired HOLDS; coverage 36/36
M6_sra_cap_detail: 36/36 paired HOLDS; coverage 36/36
M7_base_dp: DP_ERODES_ROBUSTNESS (share 0.58)
M7_sra_vs_base_under_dp: 11/12 HOLDS (paired)
M9_seeds: seeds 0-2 (mit-2) + 3-4 (mit-3)
```

## Botnet | M8 target recall at k=5, f=4 (floor = 5; learnable line 0.754)
```
                 mean    std
agg    arm                  
cwmed  base     0.000  0.000
       sra      0.898  0.000
       sra_cap  0.836  0.035
       sra_l10  0.898  0.000
fedavg base     0.623  0.099
mkrum  base     0.487  0.287
       sra      0.898  0.001
       sra_cap  0.837  0.027
       sra_l10  0.898  0.001
trmean base     0.564  0.118
       sra      0.899  0.003
       sra_cap  0.841  0.031
       sra_l10  0.899  0.003
```


## Botnet | M8 verdicts
```
M8_base: FLOOR_NOT_REACHED
M8_sra: FLOOR_MEASURED
M8_sra_l10: FLOOR_MEASURED
M8_sra_cap: FLOOR_MEASURED
M8_fedavg_recall: 0.623
```


## Botnet | M3c k* of sra_cap (cap = 5 members)
```
 f    agg  FedAvg  sra_cap  tax  sra (mit-2)
 0  cwmed       1        2    1            2
 0 trmean       1        2    1            2
 0  mkrum       1        2    1            2
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


## Botnet | M6 all cells (target = rare-class recall under attack; learnable line 0.754)
```
 k  f   attack    agg     arm  benign_fpr  other_mean  target paired                     absolute
 3  2   fang_w  cwmed    base       0.001       0.957   0.000  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2   fang_w  cwmed     sra       0.001       0.959   0.887  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2   fang_w  cwmed sra_l10       0.001       0.959   0.887  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2   fang_w  cwmed sra_cap       0.001       0.959   0.887  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2   fang_w trmean    base       0.001       0.961   0.000  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2   fang_w trmean     sra       0.001       0.961   0.883  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2   fang_w trmean sra_l10       0.001       0.961   0.883  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2   fang_w trmean sra_cap       0.001       0.961   0.883  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2   fang_w  mkrum    base       0.001       0.961   0.897  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2   fang_w  mkrum     sra       0.001       0.964   0.880  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2   fang_w  mkrum sra_l10       0.001       0.964   0.880  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2   fang_w  mkrum sra_cap       0.001       0.964   0.880  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2 minmax_w  cwmed    base       0.001       0.958   0.000  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2 minmax_w  cwmed     sra       0.001       0.959   0.896  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2 minmax_w  cwmed sra_l10       0.001       0.959   0.896  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2 minmax_w  cwmed sra_cap       0.001       0.959   0.896  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2 minmax_w trmean    base       0.001       0.959   0.183  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2 minmax_w trmean     sra       0.001       0.961   0.896  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2 minmax_w trmean sra_l10       0.001       0.961   0.896  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2 minmax_w trmean sra_cap       0.001       0.961   0.896  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2 minmax_w  mkrum    base       0.001       0.963   0.000  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2 minmax_w  mkrum     sra       0.001       0.963   0.897  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2 minmax_w  mkrum sra_l10       0.001       0.963   0.897  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2 minmax_w  mkrum sra_cap       0.001       0.963   0.897  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2   alie_w  cwmed    base       0.001       0.957   0.000  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2   alie_w  cwmed     sra       0.001       0.959   0.898  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2   alie_w  cwmed sra_l10       0.001       0.959   0.898  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2   alie_w  cwmed sra_cap       0.001       0.959   0.898  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2   alie_w trmean    base       0.001       0.959   0.829  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2   alie_w trmean     sra       0.001       0.961   0.898  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2   alie_w trmean sra_l10       0.001       0.961   0.898  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2   alie_w trmean sra_cap       0.001       0.961   0.898  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2   alie_w  mkrum    base       0.001       0.963   0.733  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2   alie_w  mkrum     sra       0.001       0.962   0.898  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2   alie_w  mkrum sra_l10       0.001       0.962   0.898  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2   alie_w  mkrum sra_cap       0.001       0.962   0.898  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2 minmax_h  cwmed    base       0.001       0.955   0.000  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2 minmax_h  cwmed     sra       0.001       0.955   0.897  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2 minmax_h  cwmed sra_l10       0.001       0.955   0.898  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2 minmax_h  cwmed sra_cap       0.001       0.955   0.897  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2 minmax_h trmean    base       0.001       0.956   0.567  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2 minmax_h trmean     sra       0.001       0.956   0.898  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2 minmax_h trmean sra_l10       0.001       0.956   0.898  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2 minmax_h trmean sra_cap       0.001       0.956   0.898  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2 minmax_h  mkrum    base       0.001       0.958   0.000  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2 minmax_h  mkrum     sra       0.001       0.957   0.898  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2 minmax_h  mkrum sra_l10       0.001       0.957   0.898  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2 minmax_h  mkrum sra_cap       0.001       0.957   0.898  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2   fang_h  cwmed    base       0.001       0.957   0.000  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2   fang_h  cwmed     sra       0.001       0.960   0.865  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2   fang_h  cwmed sra_l10       0.001       0.960   0.866  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2   fang_h  cwmed sra_cap       0.001       0.960   0.865  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2   fang_h trmean    base       0.001       0.961   0.000  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2   fang_h trmean     sra       0.001       0.963   0.754  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2   fang_h trmean sra_l10       0.001       0.963   0.759  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2   fang_h trmean sra_cap       0.001       0.963   0.754  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2   fang_h  mkrum    base       0.001       0.961   0.897  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2   fang_h  mkrum     sra       0.001       0.960   0.891  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2   fang_h  mkrum sra_l10       0.001       0.961   0.891  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2   fang_h  mkrum sra_cap       0.001       0.960   0.891  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2    split  cwmed    base       0.001       0.956   0.000  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2    split  cwmed     sra       0.001       0.957   0.897  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2    split  cwmed sra_l10       0.001       0.957   0.897  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2    split  cwmed sra_cap       0.001       0.957   0.897  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2    split trmean    base       0.001       0.958   0.123  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2    split trmean     sra       0.001       0.958   0.897  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2    split trmean sra_l10       0.001       0.958   0.897  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2    split trmean sra_cap       0.001       0.958   0.897  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2    split  mkrum    base       0.001       0.958   0.861  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2    split  mkrum     sra       0.001       0.958   0.898  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2    split  mkrum sra_l10       0.001       0.958   0.898  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2    split  mkrum sra_cap       0.001       0.958   0.898  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2   fang_w  cwmed    base       0.001       0.958   0.000  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2   fang_w  cwmed     sra       0.001       0.960   0.920  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2   fang_w  cwmed sra_l10       0.001       0.960   0.920  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2   fang_w  cwmed sra_cap       0.001       0.961   0.880  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2   fang_w trmean    base       0.001       0.966   0.867  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2   fang_w trmean     sra       0.001       0.964   0.917  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2   fang_w trmean sra_l10       0.001       0.964   0.917  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2   fang_w trmean sra_cap       0.001       0.964   0.880  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2   fang_w  mkrum    base       0.001       0.966   0.930  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2   fang_w  mkrum     sra       0.001       0.965   0.917  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2   fang_w  mkrum sra_l10       0.001       0.965   0.917  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2   fang_w  mkrum sra_cap       0.001       0.962   0.879  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2 minmax_w  cwmed    base       0.001       0.959   0.000  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2 minmax_w  cwmed     sra       0.001       0.961   0.920  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2 minmax_w  cwmed sra_l10       0.001       0.961   0.920  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2 minmax_w  cwmed sra_cap       0.001       0.961   0.886  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2 minmax_w trmean    base       0.001       0.964   0.883  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2 minmax_w trmean     sra       0.001       0.964   0.915  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2 minmax_w trmean sra_l10       0.001       0.964   0.915  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2 minmax_w trmean sra_cap       0.001       0.964   0.883  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2 minmax_w  mkrum    base       0.001       0.966   0.879  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2 minmax_w  mkrum     sra       0.001       0.964   0.913  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2 minmax_w  mkrum sra_l10       0.001       0.964   0.913  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2 minmax_w  mkrum sra_cap       0.001       0.962   0.880  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2   alie_w  cwmed    base       0.001       0.960   0.840  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2   alie_w  cwmed     sra       0.001       0.961   0.933  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2   alie_w  cwmed sra_l10       0.001       0.961   0.933  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2   alie_w  cwmed sra_cap       0.001       0.961   0.897  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2   alie_w trmean    base       0.001       0.964   0.916  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2   alie_w trmean     sra       0.001       0.964   0.934  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2   alie_w trmean sra_l10       0.001       0.964   0.934  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2   alie_w trmean sra_cap       0.001       0.964   0.897  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2   alie_w  mkrum    base       0.001       0.966   0.917  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2   alie_w  mkrum     sra       0.001       0.966   0.933  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2   alie_w  mkrum sra_l10       0.001       0.966   0.933  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2   alie_w  mkrum sra_cap       0.001       0.962   0.897  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2 minmax_h  cwmed    base       0.001       0.955   0.000  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2 minmax_h  cwmed     sra       0.001       0.957   0.930  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2 minmax_h  cwmed sra_l10       0.001       0.957   0.930  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2 minmax_h  cwmed sra_cap       0.001       0.956   0.912  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2 minmax_h trmean    base       0.001       0.957   0.895  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2 minmax_h trmean     sra       0.001       0.958   0.932  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2 minmax_h trmean sra_l10       0.001       0.958   0.932  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2 minmax_h trmean sra_cap       0.001       0.957   0.914  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2 minmax_h  mkrum    base       0.001       0.959   0.902  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2 minmax_h  mkrum     sra       0.001       0.961   0.937  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2 minmax_h  mkrum sra_l10       0.001       0.961   0.937  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2 minmax_h  mkrum sra_cap       0.001       0.960   0.918  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2   fang_h  cwmed    base       0.001       0.958   0.000  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2   fang_h  cwmed     sra       0.001       0.962   0.900  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2   fang_h  cwmed sra_l10       0.001       0.962   0.900  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2   fang_h  cwmed sra_cap       0.001       0.961   0.893  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2   fang_h trmean    base       0.001       0.966   0.867  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2   fang_h trmean     sra       0.001       0.966   0.889  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2   fang_h trmean sra_l10       0.001       0.966   0.889  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2   fang_h trmean sra_cap       0.001       0.966   0.864  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2   fang_h  mkrum    base       0.001       0.966   0.930  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2   fang_h  mkrum     sra       0.001       0.966   0.919  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2   fang_h  mkrum sra_l10       0.001       0.966   0.919  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2   fang_h  mkrum sra_cap       0.001       0.966   0.905  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2    split  cwmed    base       0.001       0.956   0.000  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2    split  cwmed     sra       0.001       0.957   0.923  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2    split  cwmed sra_l10       0.001       0.957   0.923  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2    split  cwmed sra_cap       0.001       0.957   0.898  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2    split trmean    base       0.001       0.961   0.882  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2    split trmean     sra       0.001       0.961   0.924  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2    split trmean sra_l10       0.001       0.961   0.924  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2    split trmean sra_cap       0.001       0.960   0.898  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2    split  mkrum    base       0.001       0.961   0.917  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2    split  mkrum     sra       0.001       0.961   0.928  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2    split  mkrum sra_l10       0.001       0.961   0.928  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2    split  mkrum sra_cap       0.001       0.961   0.897  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4   fang_w  cwmed    base       0.001       0.960   0.000  (ref)                        HOLDS
 6  4   fang_w  cwmed     sra       0.001       0.960   0.849  HOLDS                        HOLDS
 6  4   fang_w  cwmed sra_l10       0.001       0.960   0.849  HOLDS                        HOLDS
 6  4   fang_w  cwmed sra_cap       0.001       0.961   0.789  HOLDS                        HOLDS
 6  4   fang_w trmean    base       0.025       0.000   0.000  (ref)                       BREAKS
 6  4   fang_w trmean     sra       0.001       0.962   0.852  HOLDS                        HOLDS
 6  4   fang_w trmean sra_l10       0.001       0.962   0.852  HOLDS                        HOLDS
 6  4   fang_w trmean sra_cap       0.001       0.962   0.795  HOLDS                        HOLDS
 6  4   fang_w  mkrum    base       0.002       0.960   0.089  (ref)                        HOLDS
 6  4   fang_w  mkrum     sra       0.001       0.965   0.864  HOLDS                        HOLDS
 6  4   fang_w  mkrum sra_l10       0.001       0.965   0.864  HOLDS                        HOLDS
 6  4   fang_w  mkrum sra_cap       0.001       0.963   0.810  HOLDS                        HOLDS
 6  4 minmax_w  cwmed    base       0.001       0.960   0.000  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4 minmax_w  cwmed     sra       0.001       0.960   0.879  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4 minmax_w  cwmed sra_l10       0.001       0.960   0.879  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4 minmax_w  cwmed sra_cap       0.001       0.960   0.827  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4 minmax_w trmean    base       0.001       0.961   0.830  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4 minmax_w trmean     sra       0.001       0.961   0.877  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4 minmax_w trmean sra_l10       0.001       0.961   0.877  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4 minmax_w trmean sra_cap       0.001       0.961   0.824  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4 minmax_w  mkrum    base       0.001       0.963   0.832  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4 minmax_w  mkrum     sra       0.001       0.963   0.893  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4 minmax_w  mkrum sra_l10       0.001       0.963   0.893  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4 minmax_w  mkrum sra_cap       0.001       0.963   0.834  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4   alie_w  cwmed    base       0.001       0.961   0.817  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4   alie_w  cwmed     sra       0.001       0.960   0.914  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4   alie_w  cwmed sra_l10       0.001       0.960   0.914  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4   alie_w  cwmed sra_cap       0.001       0.960   0.845  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4   alie_w trmean    base       0.001       0.961   0.906  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4   alie_w trmean     sra       0.001       0.962   0.912  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4   alie_w trmean sra_l10       0.001       0.962   0.912  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4   alie_w trmean sra_cap       0.001       0.961   0.840  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4   alie_w  mkrum    base       0.001       0.962   0.911  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4   alie_w  mkrum     sra       0.001       0.963   0.916  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4   alie_w  mkrum sra_l10       0.001       0.963   0.916  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4   alie_w  mkrum sra_cap       0.001       0.963   0.845  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4 minmax_h  cwmed    base       0.001       0.954   0.000  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4 minmax_h  cwmed     sra       0.002       0.953   0.941  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4 minmax_h  cwmed sra_l10       0.002       0.953   0.941  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4 minmax_h  cwmed sra_cap       0.002       0.953   0.937  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4 minmax_h trmean    base       0.002       0.952   0.857  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4 minmax_h trmean     sra       0.002       0.953   0.945  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4 minmax_h trmean sra_l10       0.002       0.953   0.945  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4 minmax_h trmean sra_cap       0.002       0.953   0.940  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4 minmax_h  mkrum    base       0.002       0.955   0.858  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4 minmax_h  mkrum     sra       0.002       0.954   0.945  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4 minmax_h  mkrum sra_l10       0.002       0.954   0.945  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4 minmax_h  mkrum sra_cap       0.002       0.954   0.942  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4   fang_h  cwmed    base       0.001       0.960   0.000  (ref)                        HOLDS
 6  4   fang_h  cwmed     sra       0.001       0.962   0.886  HOLDS                        HOLDS
 6  4   fang_h  cwmed sra_l10       0.001       0.962   0.886  HOLDS                        HOLDS
 6  4   fang_h  cwmed sra_cap       0.001       0.963   0.840  HOLDS                        HOLDS
 6  4   fang_h trmean    base       0.025       0.000   0.000  (ref)                       BREAKS
 6  4   fang_h trmean     sra       0.006       0.948   0.000  HOLDS                        HOLDS
 6  4   fang_h trmean sra_l10       0.006       0.948   0.000  HOLDS                        HOLDS
 6  4   fang_h trmean sra_cap       0.174       0.728   0.000 BREAKS                       BREAKS
 6  4   fang_h  mkrum    base       0.002       0.960   0.089  (ref)                        HOLDS
 6  4   fang_h  mkrum     sra       0.002       0.962   0.536  HOLDS                        HOLDS
 6  4   fang_h  mkrum sra_l10       0.002       0.962   0.536  HOLDS                        HOLDS
 6  4   fang_h  mkrum sra_cap       0.001       0.963   0.311  HOLDS                        HOLDS
 6  4    split  cwmed    base       0.001       0.956   0.000  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4    split  cwmed     sra       0.001       0.958   0.927  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4    split  cwmed sra_l10       0.001       0.958   0.927  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4    split  cwmed sra_cap       0.001       0.957   0.895  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4    split trmean    base       0.001       0.960   0.812  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4    split trmean     sra       0.001       0.959   0.927  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4    split trmean sra_l10       0.001       0.959   0.927  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4    split trmean sra_cap       0.001       0.959   0.892  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4    split  mkrum    base       0.002       0.957   0.922  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4    split  mkrum     sra       0.002       0.959   0.936  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4    split  mkrum sra_l10       0.002       0.959   0.936  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4    split  mkrum sra_cap       0.001       0.960   0.900  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4   fang_w  cwmed    base       0.001       0.963   0.000  (ref)                        HOLDS
 2  4   fang_w  cwmed     sra       0.002       0.929   0.886  HOLDS                        HOLDS
 2  4   fang_w  cwmed sra_l10       0.002       0.933   0.736  HOLDS                        HOLDS
 2  4   fang_w  cwmed sra_cap       0.001       0.960   0.865  HOLDS                        HOLDS
 2  4   fang_w trmean    base       0.333       0.067   0.000  (ref)                       BREAKS
 2  4   fang_w trmean     sra       0.001       0.959   0.873  HOLDS                        HOLDS
 2  4   fang_w trmean sra_l10       0.002       0.913   0.883  HOLDS                        HOLDS
 2  4   fang_w trmean sra_cap       0.001       0.963   0.866  HOLDS                        HOLDS
 2  4   fang_w  mkrum    base       0.333       0.067   0.000  (ref)                       BREAKS
 2  4   fang_w  mkrum     sra       0.001       0.961   0.870  HOLDS                        HOLDS
 2  4   fang_w  mkrum sra_l10       0.001       0.962   0.888  HOLDS                        HOLDS
 2  4   fang_w  mkrum sra_cap       0.002       0.869   0.848  HOLDS                       BREAKS
 2  4 minmax_w  cwmed    base       0.001       0.963   0.000  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4 minmax_w  cwmed     sra       0.001       0.961   0.866  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4 minmax_w  cwmed sra_l10       0.001       0.961   0.866  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4 minmax_w  cwmed sra_cap       0.001       0.960   0.845  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4 minmax_w trmean    base       0.001       0.963   0.000  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4 minmax_w trmean     sra       0.001       0.961   0.864  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4 minmax_w trmean sra_l10       0.001       0.961   0.864  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4 minmax_w trmean sra_cap       0.001       0.961   0.850  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4 minmax_w  mkrum    base       0.001       0.967   0.000  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4 minmax_w  mkrum     sra       0.001       0.966   0.860  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4 minmax_w  mkrum sra_l10       0.001       0.966   0.860  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4 minmax_w  mkrum sra_cap       0.001       0.966   0.843  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4   alie_w  cwmed    base       0.001       0.963   0.000  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4   alie_w  cwmed     sra       0.003       0.954   0.229  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4   alie_w  cwmed sra_l10       0.002       0.961   0.664  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4   alie_w  cwmed sra_cap       0.001       0.959   0.314  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4   alie_w trmean    base       0.001       0.963   0.000  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4   alie_w trmean     sra       0.002       0.923   0.392  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4   alie_w trmean sra_l10       0.002       0.960   0.460  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4   alie_w trmean sra_cap       0.002       0.960   0.193  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4   alie_w  mkrum    base       0.001       0.966   0.000  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4   alie_w  mkrum     sra       0.031       0.783   0.033 BREAKS INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4   alie_w  mkrum sra_l10       0.002       0.958   0.147  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4   alie_w  mkrum sra_cap       0.001       0.966   0.123  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4 minmax_h  cwmed    base       0.001       0.955   0.000  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4 minmax_h  cwmed     sra       0.001       0.954   0.893  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4 minmax_h  cwmed sra_l10       0.001       0.954   0.893  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4 minmax_h  cwmed sra_cap       0.001       0.954   0.893  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4 minmax_h trmean    base       0.001       0.957   0.000  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4 minmax_h trmean     sra       0.002       0.954   0.903  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4 minmax_h trmean sra_l10       0.002       0.954   0.905  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4 minmax_h trmean sra_cap       0.002       0.954   0.903  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4 minmax_h  mkrum    base       0.001       0.960   0.000  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4 minmax_h  mkrum     sra       0.002       0.955   0.905  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4 minmax_h  mkrum sra_l10       0.002       0.955   0.905  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4 minmax_h  mkrum sra_cap       0.002       0.955   0.905  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4   fang_h  cwmed    base       0.001       0.963   0.000  (ref)                        HOLDS
 2  4   fang_h  cwmed     sra       0.001       0.964   0.227  HOLDS                        HOLDS
 2  4   fang_h  cwmed sra_l10       0.001       0.964   0.227  HOLDS                        HOLDS
 2  4   fang_h  cwmed sra_cap       0.001       0.964   0.227  HOLDS                        HOLDS
 2  4   fang_h trmean    base       0.333       0.067   0.000  (ref)                       BREAKS
 2  4   fang_h trmean     sra       0.107       0.799   0.000  HOLDS                       BREAKS
 2  4   fang_h trmean sra_l10       0.065       0.779   0.000  HOLDS                       BREAKS
 2  4   fang_h trmean sra_cap       0.107       0.799   0.000  HOLDS                       BREAKS
 2  4   fang_h  mkrum    base       0.333       0.067   0.000  (ref)                       BREAKS
 2  4   fang_h  mkrum     sra       0.001       0.968   0.000  HOLDS                        HOLDS
 2  4   fang_h  mkrum sra_l10       0.001       0.968   0.000  HOLDS                        HOLDS
 2  4   fang_h  mkrum sra_cap       0.001       0.968   0.000  HOLDS                        HOLDS
 2  4    split  cwmed    base       0.001       0.957   0.000  (ref)                        HOLDS
 2  4    split  cwmed     sra       0.001       0.956   0.891  HOLDS                        HOLDS
 2  4    split  cwmed sra_l10       0.001       0.956   0.892  HOLDS                        HOLDS
 2  4    split  cwmed sra_cap       0.001       0.956   0.891  HOLDS                        HOLDS
 2  4    split trmean    base       0.001       0.963   0.000  (ref)                        HOLDS
 2  4    split trmean     sra       0.001       0.959   0.892  HOLDS                        HOLDS
 2  4    split trmean sra_l10       0.001       0.959   0.892  HOLDS                        HOLDS
 2  4    split trmean sra_cap       0.001       0.959   0.892  HOLDS                        HOLDS
 2  4    split  mkrum    base       0.001       0.957   0.850  (ref)                        HOLDS
 2  4    split  mkrum     sra       0.001       0.959   0.893  HOLDS                        HOLDS
 2  4    split  mkrum sra_l10       0.001       0.958   0.892  HOLDS                        HOLDS
 2  4    split  mkrum sra_cap       0.001       0.959   0.893  HOLDS                        HOLDS
```


## Botnet | M6 clean reference (mimic, no model poisoning): target recall
```
arm          base    sra  sra_cap  sra_l10
k f agg                                   
2 0 fedavg  0.874    NaN      NaN      NaN
  4 cwmed   0.000  0.000    0.000    0.000
    mkrum   0.000  0.000    0.000    0.000
    trmean  0.000  0.000    0.000    0.000
3 0 fedavg  0.895    NaN      NaN      NaN
  2 cwmed   0.000  0.896    0.896    0.896
    mkrum   0.000  0.897    0.897    0.897
    trmean  0.011  0.897    0.897    0.897
6 0 fedavg  0.918    NaN      NaN      NaN
  2 cwmed   0.000  0.918    0.895    0.918
    mkrum   0.907  0.916    0.890    0.916
    trmean  0.895  0.916    0.893    0.916
  4 cwmed   0.000  0.905    0.844    0.905
    mkrum   0.858  0.905    0.847    0.905
    trmean  0.813  0.905    0.842    0.905
```


## Botnet | M6 paired verdict counts by arm, zone, attack
```
paired                     BREAKS  HOLDS
arm     zone     attack                 
sra     f<=F_HAT alie_w         0      6
                 fang_h         0      6
                 fang_w         0      6
                 minmax_h       0      6
                 minmax_w       0      6
                 split          0      6
        f>F_HAT  alie_w         1      5
                 fang_h         0      6
                 fang_w         0      6
                 minmax_h       0      6
                 minmax_w       0      6
                 split          0      6
sra_cap f<=F_HAT alie_w         0      6
                 fang_h         0      6
                 fang_w         0      6
                 minmax_h       0      6
                 minmax_w       0      6
                 split          0      6
        f>F_HAT  alie_w         0      6
                 fang_h         1      5
                 fang_w         0      6
                 minmax_h       0      6
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
                 minmax_h       0      6
                 minmax_w       0      6
                 split          0      6
```


## Botnet | M6 verdicts (f <= F_HAT, k > f cells: (3,2) and (6,2))
```
M6_sra: SURVIVES_ADAPTIVE
M6_sra_l10: SURVIVES_ADAPTIVE
M6_sra_cap: SURVIVES_ADAPTIVE
M6_sra_detail: 36/36 paired HOLDS; coverage 35/36
M6_sra_l10_detail: 36/36 paired HOLDS; coverage 36/36
M6_sra_cap_detail: 36/36 paired HOLDS; coverage 35/36
worst SRA cells by target recall:
 k  f attack    agg  target  benign_fpr  other_mean
 3  2 fang_h trmean   0.754       0.001       0.963
 3  2 fang_h  cwmed   0.865       0.001       0.960
 3  2 fang_w  mkrum   0.880       0.001       0.964
```


## Botnet | M7 attack damage with and without DP (k=6, f=2)
```
   agg  arm   attack FPR clean/att (non-DP) FPR clean/att (DP) other clean/att (non-DP) other clean/att (DP) target att non-DP / DP
 cwmed base signflip            0.001/0.001        0.008/0.014              0.957/0.955          0.936/0.873            0.000/0.885
 cwmed base     alie            0.001/0.001        0.008/0.009              0.957/0.958          0.936/0.567            0.791/0.000
 cwmed base   fang_w            0.001/0.001        0.008/0.011              0.957/0.958          0.936/0.900            0.000/0.602
 cwmed base minmax_h            0.001/0.001        0.008/0.014              0.957/0.955          0.936/0.886            0.000/0.887
 cwmed  sra signflip            0.001/0.001        0.009/0.014              0.961/0.956          0.938/0.878            0.928/0.895
 cwmed  sra     alie            0.001/0.001        0.009/0.006              0.961/0.959          0.938/0.495            0.932/0.000
 cwmed  sra   fang_w            0.001/0.001        0.009/0.011              0.961/0.960          0.938/0.882            0.920/0.522
 cwmed  sra minmax_h            0.001/0.001        0.009/0.012              0.961/0.957          0.938/0.919            0.930/0.890
trmean base signflip            0.001/0.001        0.007/0.014              0.962/0.955          0.947/0.818            0.883/0.894
trmean base     alie            0.001/0.001        0.007/0.009              0.962/0.961          0.947/0.575            0.917/0.000
trmean base   fang_w            0.001/0.001        0.007/0.008              0.962/0.966          0.947/0.912            0.867/0.000
trmean base minmax_h            0.001/0.001        0.007/0.011              0.962/0.957          0.947/0.918            0.895/0.893
trmean  sra signflip            0.001/0.001        0.008/0.015              0.962/0.957          0.946/0.889            0.930/0.895
trmean  sra     alie            0.001/0.001        0.008/0.009              0.962/0.961          0.946/0.560            0.931/0.000
trmean  sra   fang_w            0.001/0.001        0.008/0.007              0.962/0.964          0.946/0.914            0.917/0.164
trmean  sra minmax_h            0.001/0.001        0.008/0.011              0.962/0.958          0.946/0.943            0.932/0.903
 mkrum base signflip            0.001/0.001        0.007/0.008              0.967/0.964          0.949/0.949            0.926/0.876
 mkrum base     alie            0.001/0.001        0.007/0.007              0.967/0.962          0.949/0.579            0.918/0.000
 mkrum base   fang_w            0.001/0.001        0.007/0.008              0.967/0.966          0.949/0.949            0.930/0.876
 mkrum base minmax_h            0.001/0.001        0.007/0.011              0.967/0.959          0.949/0.925            0.902/0.895
 mkrum  sra signflip            0.001/0.001        0.008/0.015              0.962/0.961          0.947/0.908            0.928/0.895
 mkrum  sra     alie            0.001/0.001        0.008/0.009              0.962/0.961          0.947/0.561            0.931/0.000
 mkrum  sra   fang_w            0.001/0.001        0.008/0.009              0.962/0.965          0.947/0.939            0.917/0.674
 mkrum  sra minmax_h            0.001/0.001        0.008/0.010              0.962/0.961          0.947/0.941            0.937/0.904
```


## Botnet | M7 verdicts
```
M7_base_dp: DP_ERODES_ROBUSTNESS (share 0.42)
M7_sra_vs_base_under_dp: 11/12 HOLDS (paired)
```


## Botnet | M9 k* point [5%, 95%] bootstrap over seeds -- seeds 0-2 (mit-2) + 3-4 (mit-3) ('9' = never)
```
 f    agg  FedAvg    base     sra sra_l10
 0  cwmed 1 [1,2] 8 [8,8] 2 [1,2] 1 [1,1]
 0 trmean 1 [1,2] 3 [3,3] 2 [2,2] 1 [1,2]
 0  mkrum 1 [1,2] 4 [4,4] 2 [2,2] 1 [1,2]
 2  cwmed 4 [4,4] 8 [8,8] 3 [3,3] 3 [3,3]
 2 trmean 4 [4,4] 4 [4,4] 3 [3,3] 3 [3,3]
 2  mkrum 4 [4,4] 6 [6,6] 3 [3,3] 3 [3,3]
 4  cwmed 6 [6,6] 9 [9,9] 6 [6,6] 6 [6,6]
 4 trmean 6 [6,6] 6 [6,6] 6 [6,6] 6 [6,6]
 4  mkrum 6 [6,6] 6 [6,6] 6 [6,6] 6 [6,6]
```


## Portscan | M8 target recall at k=5, f=4 (floor = 5; learnable line 0.727)
```
                 mean    std
agg    arm                  
cwmed  base     0.000  0.000
       sra      0.853  0.039
       sra_cap  0.777  0.011
       sra_l10  0.853  0.039
fedavg base     0.358  0.144
mkrum  base     0.348  0.340
       sra      0.817  0.090
       sra_cap  0.649  0.091
       sra_l10  0.817  0.090
trmean base     0.318  0.170
       sra      0.845  0.049
       sra_cap  0.734  0.027
       sra_l10  0.845  0.049
```


## Portscan | M8 verdicts
```
M8_base: FLOOR_NOT_REACHED
M8_sra: FLOOR_MEASURED
M8_sra_l10: FLOOR_MEASURED
M8_sra_cap: FLOOR_MEASURED
M8_fedavg_recall: 0.358
```


## Portscan | M3c k* of sra_cap (cap = 5 members)
```
 f    agg  FedAvg  sra_cap  tax  sra (mit-2)
 0  cwmed       1        1    0            1
 0 trmean       1        1    0            1
 0  mkrum       1        2    1            2
 2  cwmed       6        3    0            3
 2 trmean       6        3    0            3
 2  mkrum       6        3    0            3
 4  cwmed       8        6    0            6
 4 trmean       8        6    0            6
 4  mkrum       8        6    0            6
```


## Portscan | M3c verdict
```
floor (pre-registered rule): ABOVE_FLOOR | grid-censored share: 0.89
```


## Portscan | M6 all cells (target = rare-class recall under attack; learnable line 0.727)
```
 k  f   attack    agg     arm  benign_fpr  other_mean  target paired                     absolute
 3  2   fang_w  cwmed    base       0.001       0.962   0.000  (ref)                        HOLDS
 3  2   fang_w  cwmed     sra       0.001       0.963   0.869  HOLDS                        HOLDS
 3  2   fang_w  cwmed sra_l10       0.001       0.962   0.869  HOLDS                        HOLDS
 3  2   fang_w  cwmed sra_cap       0.001       0.963   0.869  HOLDS                        HOLDS
 3  2   fang_w trmean    base       0.001       0.963   0.057  (ref)                        HOLDS
 3  2   fang_w trmean     sra       0.001       0.963   0.855  HOLDS                        HOLDS
 3  2   fang_w trmean sra_l10       0.001       0.963   0.856  HOLDS                        HOLDS
 3  2   fang_w trmean sra_cap       0.001       0.963   0.855  HOLDS                        HOLDS
 3  2   fang_w  mkrum    base       0.001       0.964   0.897  (ref)                        HOLDS
 3  2   fang_w  mkrum     sra       0.001       0.963   0.848  HOLDS                        HOLDS
 3  2   fang_w  mkrum sra_l10       0.001       0.963   0.850  HOLDS                        HOLDS
 3  2   fang_w  mkrum sra_cap       0.001       0.963   0.848  HOLDS                        HOLDS
 3  2 minmax_w  cwmed    base       0.001       0.962   0.000  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2 minmax_w  cwmed     sra       0.001       0.962   0.887  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2 minmax_w  cwmed sra_l10       0.001       0.962   0.887  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2 minmax_w  cwmed sra_cap       0.001       0.962   0.887  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2 minmax_w trmean    base       0.001       0.963   0.406  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2 minmax_w trmean     sra       0.001       0.963   0.875  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2 minmax_w trmean sra_l10       0.001       0.963   0.875  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2 minmax_w trmean sra_cap       0.001       0.963   0.875  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2 minmax_w  mkrum    base       0.001       0.963   0.094  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2 minmax_w  mkrum     sra       0.001       0.963   0.876  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2 minmax_w  mkrum sra_l10       0.001       0.963   0.876  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2 minmax_w  mkrum sra_cap       0.001       0.963   0.876  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2   alie_w  cwmed    base       0.001       0.962   0.000  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2   alie_w  cwmed     sra       0.001       0.962   0.894  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2   alie_w  cwmed sra_l10       0.001       0.962   0.894  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2   alie_w  cwmed sra_cap       0.001       0.962   0.894  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2   alie_w trmean    base       0.001       0.963   0.824  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2   alie_w trmean     sra       0.001       0.963   0.892  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2   alie_w trmean sra_l10       0.001       0.963   0.892  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2   alie_w trmean sra_cap       0.001       0.963   0.892  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2   alie_w  mkrum    base       0.001       0.964   0.737  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2   alie_w  mkrum     sra       0.001       0.963   0.890  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2   alie_w  mkrum sra_l10       0.001       0.963   0.890  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2   alie_w  mkrum sra_cap       0.001       0.963   0.890  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2 minmax_h  cwmed    base       0.001       0.961   0.000  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2 minmax_h  cwmed     sra       0.002       0.961   0.900  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2 minmax_h  cwmed sra_l10       0.002       0.961   0.900  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2 minmax_h  cwmed sra_cap       0.002       0.961   0.900  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2 minmax_h trmean    base       0.001       0.962   0.464  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2 minmax_h trmean     sra       0.001       0.961   0.899  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2 minmax_h trmean sra_l10       0.001       0.961   0.899  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2 minmax_h trmean sra_cap       0.001       0.961   0.899  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2 minmax_h  mkrum    base       0.001       0.963   0.035  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2 minmax_h  mkrum     sra       0.001       0.961   0.899  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2 minmax_h  mkrum sra_l10       0.001       0.961   0.899  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2 minmax_h  mkrum sra_cap       0.001       0.961   0.899  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2   fang_h  cwmed    base       0.001       0.962   0.000  (ref)                        HOLDS
 3  2   fang_h  cwmed     sra       0.001       0.962   0.888  HOLDS                        HOLDS
 3  2   fang_h  cwmed sra_l10       0.001       0.962   0.888  HOLDS                        HOLDS
 3  2   fang_h  cwmed sra_cap       0.001       0.962   0.888  HOLDS                        HOLDS
 3  2   fang_h trmean    base       0.001       0.963   0.057  (ref)                        HOLDS
 3  2   fang_h trmean     sra       0.001       0.963   0.856  HOLDS                        HOLDS
 3  2   fang_h trmean sra_l10       0.001       0.963   0.856  HOLDS                        HOLDS
 3  2   fang_h trmean sra_cap       0.001       0.963   0.856  HOLDS                        HOLDS
 3  2   fang_h  mkrum    base       0.001       0.964   0.897  (ref)                        HOLDS
 3  2   fang_h  mkrum     sra       0.001       0.963   0.896  HOLDS                        HOLDS
 3  2   fang_h  mkrum sra_l10       0.001       0.963   0.897  HOLDS                        HOLDS
 3  2   fang_h  mkrum sra_cap       0.001       0.963   0.896  HOLDS                        HOLDS
 3  2    split  cwmed    base       0.001       0.961   0.000  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2    split  cwmed     sra       0.001       0.962   0.899  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2    split  cwmed sra_l10       0.001       0.962   0.899  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2    split  cwmed sra_cap       0.001       0.962   0.899  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2    split trmean    base       0.001       0.962   0.314  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2    split trmean     sra       0.001       0.962   0.894  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2    split trmean sra_l10       0.001       0.962   0.894  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2    split trmean sra_cap       0.001       0.962   0.894  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2    split  mkrum    base       0.001       0.963   0.823  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2    split  mkrum     sra       0.001       0.962   0.895  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2    split  mkrum sra_l10       0.001       0.962   0.895  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 3  2    split  mkrum sra_cap       0.001       0.962   0.895  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2   fang_w  cwmed    base       0.001       0.963   0.000  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2   fang_w  cwmed     sra       0.002       0.964   0.897  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2   fang_w  cwmed sra_l10       0.002       0.964   0.897  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2   fang_w  cwmed sra_cap       0.002       0.965   0.884  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2   fang_w trmean    base       0.001       0.969   0.849  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2   fang_w trmean     sra       0.001       0.965   0.896  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2   fang_w trmean sra_l10       0.001       0.965   0.896  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2   fang_w trmean sra_cap       0.001       0.965   0.874  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2   fang_w  mkrum    base       0.001       0.967   0.907  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2   fang_w  mkrum     sra       0.001       0.967   0.896  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2   fang_w  mkrum sra_l10       0.001       0.967   0.896  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2   fang_w  mkrum sra_cap       0.001       0.968   0.859  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2 minmax_w  cwmed    base       0.001       0.964   0.000  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2 minmax_w  cwmed     sra       0.002       0.964   0.897  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2 minmax_w  cwmed sra_l10       0.002       0.964   0.897  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2 minmax_w  cwmed sra_cap       0.002       0.965   0.884  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2 minmax_w trmean    base       0.001       0.967   0.875  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2 minmax_w trmean     sra       0.001       0.965   0.897  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2 minmax_w trmean sra_l10       0.001       0.965   0.897  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2 minmax_w trmean sra_cap       0.002       0.966   0.876  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2 minmax_w  mkrum    base       0.001       0.969   0.873  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2 minmax_w  mkrum     sra       0.001       0.967   0.896  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2 minmax_w  mkrum sra_l10       0.001       0.967   0.896  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2 minmax_w  mkrum sra_cap       0.001       0.968   0.864  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2   alie_w  cwmed    base       0.001       0.964   0.853  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2   alie_w  cwmed     sra       0.001       0.964   0.907  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2   alie_w  cwmed sra_l10       0.001       0.964   0.907  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2   alie_w  cwmed sra_cap       0.001       0.965   0.899  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2   alie_w trmean    base       0.001       0.967   0.896  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2   alie_w trmean     sra       0.001       0.965   0.905  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2   alie_w trmean sra_l10       0.001       0.965   0.905  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2   alie_w trmean sra_cap       0.001       0.965   0.897  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2   alie_w  mkrum    base       0.001       0.968   0.906  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2   alie_w  mkrum     sra       0.001       0.967   0.905  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2   alie_w  mkrum sra_l10       0.001       0.967   0.905  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2   alie_w  mkrum sra_cap       0.001       0.967   0.889  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2 minmax_h  cwmed    base       0.001       0.962   0.000  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2 minmax_h  cwmed     sra       0.002       0.962   0.902  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2 minmax_h  cwmed sra_l10       0.002       0.962   0.902  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2 minmax_h  cwmed sra_cap       0.002       0.962   0.900  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2 minmax_h trmean    base       0.002       0.961   0.882  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2 minmax_h trmean     sra       0.002       0.962   0.902  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2 minmax_h trmean sra_l10       0.002       0.962   0.902  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2 minmax_h trmean sra_cap       0.002       0.962   0.897  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2 minmax_h  mkrum    base       0.002       0.962   0.860  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2 minmax_h  mkrum     sra       0.002       0.962   0.902  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2 minmax_h  mkrum sra_l10       0.002       0.962   0.902  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2 minmax_h  mkrum sra_cap       0.002       0.962   0.898  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2   fang_h  cwmed    base       0.001       0.963   0.000  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2   fang_h  cwmed     sra       0.002       0.965   0.899  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2   fang_h  cwmed sra_l10       0.002       0.965   0.899  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2   fang_h  cwmed sra_cap       0.002       0.965   0.891  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2   fang_h trmean    base       0.001       0.969   0.849  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2   fang_h trmean     sra       0.001       0.969   0.890  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2   fang_h trmean sra_l10       0.001       0.969   0.890  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2   fang_h trmean sra_cap       0.001       0.968   0.860  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2   fang_h  mkrum    base       0.001       0.967   0.907  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2   fang_h  mkrum     sra       0.001       0.968   0.899  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2   fang_h  mkrum sra_l10       0.001       0.968   0.899  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2   fang_h  mkrum sra_cap       0.001       0.969   0.894  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2    split  cwmed    base       0.001       0.962   0.000  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2    split  cwmed     sra       0.002       0.963   0.897  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2    split  cwmed sra_l10       0.002       0.963   0.897  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2    split  cwmed sra_cap       0.002       0.963   0.896  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2    split trmean    base       0.002       0.963   0.872  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2    split trmean     sra       0.002       0.964   0.897  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2    split trmean sra_l10       0.002       0.964   0.897  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2    split trmean sra_cap       0.002       0.963   0.893  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2    split  mkrum    base       0.002       0.964   0.905  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2    split  mkrum     sra       0.001       0.965   0.897  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2    split  mkrum sra_l10       0.001       0.965   0.897  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2    split  mkrum sra_cap       0.001       0.964   0.887  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4   fang_w  cwmed    base       0.001       0.967   0.000  (ref)                        HOLDS
 6  4   fang_w  cwmed     sra       0.002       0.969   0.811  HOLDS                        HOLDS
 6  4   fang_w  cwmed sra_l10       0.002       0.969   0.811  HOLDS                        HOLDS
 6  4   fang_w  cwmed sra_cap       0.002       0.968   0.707  HOLDS                        HOLDS
 6  4   fang_w trmean    base       0.699       0.235   0.000  (ref)                       BREAKS
 6  4   fang_w trmean     sra       0.002       0.969   0.737  HOLDS                        HOLDS
 6  4   fang_w trmean sra_l10       0.002       0.970   0.761  HOLDS                        HOLDS
 6  4   fang_w trmean sra_cap       0.002       0.969   0.685  HOLDS                        HOLDS
 6  4   fang_w  mkrum    base       0.453       0.390   0.000  (ref)                       BREAKS
 6  4   fang_w  mkrum     sra       0.004       0.964   0.657  HOLDS                        HOLDS
 6  4   fang_w  mkrum sra_l10       0.002       0.968   0.802  HOLDS                        HOLDS
 6  4   fang_w  mkrum sra_cap       0.001       0.969   0.527  HOLDS                        HOLDS
 6  4 minmax_w  cwmed    base       0.001       0.967   0.000  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4 minmax_w  cwmed     sra       0.002       0.967   0.872  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4 minmax_w  cwmed sra_l10       0.002       0.967   0.872  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4 minmax_w  cwmed sra_cap       0.002       0.966   0.796  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4 minmax_w trmean    base       0.001       0.968   0.816  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4 minmax_w trmean     sra       0.002       0.968   0.871  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4 minmax_w trmean sra_l10       0.002       0.968   0.871  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4 minmax_w trmean sra_cap       0.001       0.968   0.786  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4 minmax_w  mkrum    base       0.001       0.969   0.851  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4 minmax_w  mkrum     sra       0.002       0.969   0.874  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4 minmax_w  mkrum sra_l10       0.002       0.969   0.874  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4 minmax_w  mkrum sra_cap       0.001       0.969   0.767  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4   alie_w  cwmed    base       0.002       0.968   0.799  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4   alie_w  cwmed     sra       0.002       0.967   0.904  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4   alie_w  cwmed sra_l10       0.002       0.967   0.904  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4   alie_w  cwmed sra_cap       0.002       0.966   0.847  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4   alie_w trmean    base       0.001       0.968   0.896  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4   alie_w trmean     sra       0.001       0.969   0.900  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4   alie_w trmean sra_l10       0.001       0.969   0.900  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4   alie_w trmean sra_cap       0.002       0.968   0.837  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4   alie_w  mkrum    base       0.001       0.969   0.899  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4   alie_w  mkrum     sra       0.001       0.970   0.906  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4   alie_w  mkrum sra_l10       0.002       0.969   0.903  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4   alie_w  mkrum sra_cap       0.002       0.969   0.813  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4 minmax_h  cwmed    base       0.002       0.961   0.000  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4 minmax_h  cwmed     sra       0.002       0.961   0.901  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4 minmax_h  cwmed sra_l10       0.002       0.961   0.901  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4 minmax_h  cwmed sra_cap       0.002       0.961   0.897  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4 minmax_h trmean    base       0.002       0.960   0.857  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4 minmax_h trmean     sra       0.002       0.961   0.909  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4 minmax_h trmean sra_l10       0.002       0.961   0.909  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4 minmax_h trmean sra_cap       0.002       0.961   0.897  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4 minmax_h  mkrum    base       0.002       0.961   0.774  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4 minmax_h  mkrum     sra       0.002       0.961   0.912  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4 minmax_h  mkrum sra_l10       0.002       0.961   0.912  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4 minmax_h  mkrum sra_cap       0.002       0.961   0.901  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4   fang_h  cwmed    base       0.001       0.967   0.000  (ref)                        HOLDS
 6  4   fang_h  cwmed     sra       0.001       0.969   0.884  HOLDS                        HOLDS
 6  4   fang_h  cwmed sra_l10       0.001       0.969   0.884  HOLDS                        HOLDS
 6  4   fang_h  cwmed sra_cap       0.001       0.969   0.862  HOLDS                        HOLDS
 6  4   fang_h trmean    base       0.699       0.235   0.000  (ref)                       BREAKS
 6  4   fang_h trmean     sra       0.002       0.967   0.451  HOLDS                        HOLDS
 6  4   fang_h trmean sra_l10       0.002       0.967   0.451  HOLDS                        HOLDS
 6  4   fang_h trmean sra_cap       0.002       0.972   0.096  HOLDS                        HOLDS
 6  4   fang_h  mkrum    base       0.453       0.390   0.000  (ref)                       BREAKS
 6  4   fang_h  mkrum     sra       0.002       0.965   0.742  HOLDS                        HOLDS
 6  4   fang_h  mkrum sra_l10       0.002       0.965   0.742  HOLDS                        HOLDS
 6  4   fang_h  mkrum sra_cap       0.004       0.961   0.417  HOLDS                        HOLDS
 6  4    split  cwmed    base       0.002       0.963   0.000  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4    split  cwmed     sra       0.002       0.962   0.900  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4    split  cwmed sra_l10       0.002       0.962   0.900  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4    split  cwmed sra_cap       0.002       0.962   0.893  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4    split trmean    base       0.002       0.964   0.743  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4    split trmean     sra       0.002       0.962   0.902  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4    split trmean sra_l10       0.002       0.962   0.902  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4    split trmean sra_cap       0.002       0.962   0.893  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4    split  mkrum    base       0.002       0.961   0.901  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4    split  mkrum     sra       0.002       0.962   0.905  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4    split  mkrum sra_l10       0.002       0.962   0.905  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4    split  mkrum sra_cap       0.002       0.962   0.893  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4   fang_w  cwmed    base       0.001       0.966   0.000  (ref)                        HOLDS
 2  4   fang_w  cwmed     sra       0.002       0.962   0.853  HOLDS                        HOLDS
 2  4   fang_w  cwmed sra_l10       0.002       0.962   0.869  HOLDS                        HOLDS
 2  4   fang_w  cwmed sra_cap       0.006       0.962   0.599  HOLDS                        HOLDS
 2  4   fang_w trmean    base       0.149       0.068   0.000  (ref)                       BREAKS
 2  4   fang_w trmean     sra       0.002       0.965   0.849  HOLDS                        HOLDS
 2  4   fang_w trmean sra_l10       0.002       0.963   0.843  HOLDS                        HOLDS
 2  4   fang_w trmean sra_cap       0.002       0.966   0.816  HOLDS                        HOLDS
 2  4   fang_w  mkrum    base       0.997       0.197   0.000  (ref)                       BREAKS
 2  4   fang_w  mkrum     sra       0.002       0.965   0.823  HOLDS                        HOLDS
 2  4   fang_w  mkrum sra_l10       0.002       0.965   0.844  HOLDS                        HOLDS
 2  4   fang_w  mkrum sra_cap       0.002       0.964   0.677  HOLDS                        HOLDS
 2  4 minmax_w  cwmed    base       0.001       0.966   0.000  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4 minmax_w  cwmed     sra       0.002       0.964   0.841  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4 minmax_w  cwmed sra_l10       0.002       0.964   0.841  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4 minmax_w  cwmed sra_cap       0.002       0.964   0.796  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4 minmax_w trmean    base       0.001       0.965   0.000  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4 minmax_w trmean     sra       0.001       0.965   0.771  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4 minmax_w trmean sra_l10       0.001       0.965   0.771  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4 minmax_w trmean sra_cap       0.001       0.966   0.733  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4 minmax_w  mkrum    base       0.001       0.969   0.000  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4 minmax_w  mkrum     sra       0.001       0.969   0.701  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4 minmax_w  mkrum sra_l10       0.001       0.969   0.701  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4 minmax_w  mkrum sra_cap       0.001       0.968   0.609  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4   alie_w  cwmed    base       0.001       0.966   0.000  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4   alie_w  cwmed     sra       0.006       0.883   0.151 BREAKS INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4   alie_w  cwmed sra_l10       0.003       0.960   0.048  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4   alie_w  cwmed sra_cap       0.003       0.765   0.000 BREAKS INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4   alie_w trmean    base       0.001       0.967   0.000  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4   alie_w trmean     sra       0.002       0.963   0.130  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4   alie_w trmean sra_l10       0.002       0.960   0.105  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4   alie_w trmean sra_cap       0.003       0.961   0.094  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4   alie_w  mkrum    base       0.001       0.968   0.000  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4   alie_w  mkrum     sra       0.001       0.643   0.000 BREAKS INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4   alie_w  mkrum sra_l10       0.003       0.962   0.000  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4   alie_w  mkrum sra_cap       0.004       0.961   0.000  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4 minmax_h  cwmed    base       0.002       0.962   0.000  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4 minmax_h  cwmed     sra       0.002       0.960   0.900  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4 minmax_h  cwmed sra_l10       0.002       0.960   0.900  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4 minmax_h  cwmed sra_cap       0.002       0.960   0.900  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4 minmax_h trmean    base       0.002       0.962   0.000  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4 minmax_h trmean     sra       0.002       0.961   0.900  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4 minmax_h trmean sra_l10       0.002       0.961   0.900  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4 minmax_h trmean sra_cap       0.002       0.961   0.900  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4 minmax_h  mkrum    base       0.001       0.962   0.000  (ref) INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4 minmax_h  mkrum     sra       0.002       0.961   0.903  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4 minmax_h  mkrum sra_l10       0.002       0.961   0.903  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4 minmax_h  mkrum sra_cap       0.002       0.961   0.903  HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4   fang_h  cwmed    base       0.001       0.966   0.000  (ref)                        HOLDS
 2  4   fang_h  cwmed     sra       0.001       0.964   0.820  HOLDS                        HOLDS
 2  4   fang_h  cwmed sra_l10       0.001       0.964   0.820  HOLDS                        HOLDS
 2  4   fang_h  cwmed sra_cap       0.001       0.964   0.820  HOLDS                        HOLDS
 2  4   fang_h trmean    base       0.149       0.068   0.000  (ref)                       BREAKS
 2  4   fang_h trmean     sra       0.003       0.965   0.001  HOLDS                        HOLDS
 2  4   fang_h trmean sra_l10       0.002       0.967   0.006  HOLDS                        HOLDS
 2  4   fang_h trmean sra_cap       0.003       0.965   0.001  HOLDS                        HOLDS
 2  4   fang_h  mkrum    base       0.997       0.197   0.000  (ref)                       BREAKS
 2  4   fang_h  mkrum     sra       0.007       0.935   0.210  HOLDS                        HOLDS
 2  4   fang_h  mkrum sra_l10       0.012       0.962   0.164  HOLDS                        HOLDS
 2  4   fang_h  mkrum sra_cap       0.007       0.935   0.210  HOLDS                        HOLDS
 2  4    split  cwmed    base       0.002       0.962   0.000  (ref)                        HOLDS
 2  4    split  cwmed     sra       0.002       0.962   0.878  HOLDS                        HOLDS
 2  4    split  cwmed sra_l10       0.002       0.962   0.878  HOLDS                        HOLDS
 2  4    split  cwmed sra_cap       0.002       0.962   0.878  HOLDS                        HOLDS
 2  4    split trmean    base       0.001       0.966   0.000  (ref)                        HOLDS
 2  4    split trmean     sra       0.002       0.962   0.870  HOLDS                        HOLDS
 2  4    split trmean sra_l10       0.002       0.962   0.873  HOLDS                        HOLDS
 2  4    split trmean sra_cap       0.002       0.962   0.870  HOLDS                        HOLDS
 2  4    split  mkrum    base       0.002       0.961   0.854  (ref)                        HOLDS
 2  4    split  mkrum     sra       0.002       0.962   0.844  HOLDS                        HOLDS
 2  4    split  mkrum sra_l10       0.002       0.962   0.848  HOLDS                        HOLDS
 2  4    split  mkrum sra_cap       0.002       0.962   0.844  HOLDS                        HOLDS
```


## Portscan | M6 clean reference (mimic, no model poisoning): target recall
```
arm          base    sra  sra_cap  sra_l10
k f agg                                   
2 0 fedavg  0.886    NaN      NaN      NaN
  4 cwmed   0.000  0.000    0.000    0.000
    mkrum   0.000  0.000    0.000    0.000
    trmean  0.000  0.000    0.000    0.000
3 0 fedavg  0.881    NaN      NaN      NaN
  2 cwmed   0.000  0.864    0.864    0.864
    mkrum   0.000  0.857    0.857    0.857
    trmean  0.166  0.860    0.860    0.860
6 0 fedavg  0.907    NaN      NaN      NaN
  2 cwmed   0.000  0.897    0.889    0.897
    mkrum   0.904  0.893    0.863    0.893
    trmean  0.866  0.895    0.879    0.895
  4 cwmed   0.000  0.895    0.820    0.895
    mkrum   0.864  0.891    0.769    0.891
    trmean  0.647  0.894    0.806    0.894
```


## Portscan | M6 paired verdict counts by arm, zone, attack
```
paired                     BREAKS  HOLDS
arm     zone     attack                 
sra     f<=F_HAT alie_w         0      6
                 fang_h         0      6
                 fang_w         0      6
                 minmax_h       0      6
                 minmax_w       0      6
                 split          0      6
        f>F_HAT  alie_w         2      4
                 fang_h         0      6
                 fang_w         0      6
                 minmax_h       0      6
                 minmax_w       0      6
                 split          0      6
sra_cap f<=F_HAT alie_w         0      6
                 fang_h         0      6
                 fang_w         0      6
                 minmax_h       0      6
                 minmax_w       0      6
                 split          0      6
        f>F_HAT  alie_w         1      5
                 fang_h         0      6
                 fang_w         0      6
                 minmax_h       0      6
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
                 minmax_h       0      6
                 minmax_w       0      6
                 split          0      6
```


## Portscan | M6 verdicts (f <= F_HAT, k > f cells: (3,2) and (6,2))
```
M6_sra: SURVIVES_ADAPTIVE
M6_sra_l10: SURVIVES_ADAPTIVE
M6_sra_cap: SURVIVES_ADAPTIVE
M6_sra_detail: 36/36 paired HOLDS; coverage 36/36
M6_sra_l10_detail: 36/36 paired HOLDS; coverage 36/36
M6_sra_cap_detail: 36/36 paired HOLDS; coverage 36/36
worst SRA cells by target recall:
 k  f attack    agg  target  benign_fpr  other_mean
 3  2 fang_w  mkrum   0.848       0.001       0.963
 3  2 fang_w trmean   0.855       0.001       0.963
 3  2 fang_h trmean   0.856       0.001       0.963
```


## Portscan | M7 attack damage with and without DP (k=6, f=2)
```
   agg  arm   attack FPR clean/att (non-DP) FPR clean/att (DP) other clean/att (non-DP) other clean/att (DP) target att non-DP / DP
 cwmed base signflip            0.001/0.001        0.009/0.013              0.964/0.962          0.940/0.900            0.000/0.837
 cwmed base     alie            0.001/0.002        0.009/0.012              0.964/0.964          0.940/0.566            0.790/0.000
 cwmed base   fang_w            0.001/0.001        0.009/0.013              0.964/0.963          0.940/0.883            0.000/0.140
 cwmed base minmax_h            0.001/0.001        0.009/0.013              0.964/0.962          0.940/0.879            0.000/0.857
 cwmed  sra signflip            0.002/0.002        0.009/0.015              0.964/0.961          0.900/0.882            0.897/0.813
 cwmed  sra     alie            0.002/0.002        0.009/0.013              0.964/0.965          0.900/0.562            0.907/0.000
 cwmed  sra   fang_w            0.002/0.002        0.009/0.013              0.964/0.964          0.900/0.876            0.897/0.193
 cwmed  sra minmax_h            0.002/0.002        0.009/0.012              0.964/0.962          0.900/0.944            0.902/0.885
trmean base signflip            0.001/0.002        0.007/0.012              0.965/0.961          0.948/0.775            0.875/0.862
trmean base     alie            0.001/0.001        0.007/0.011              0.965/0.965          0.948/0.572            0.902/0.000
trmean base   fang_w            0.001/0.001        0.007/0.010              0.965/0.969          0.948/0.860            0.849/0.000
trmean base minmax_h            0.001/0.002        0.007/0.010              0.965/0.961          0.948/0.924            0.882/0.876
trmean  sra signflip            0.001/0.002        0.009/0.013              0.965/0.961          0.951/0.846            0.897/0.874
trmean  sra     alie            0.001/0.001        0.009/0.014              0.965/0.965          0.951/0.562            0.905/0.000
trmean  sra   fang_w            0.001/0.001        0.009/0.010              0.965/0.965          0.951/0.894            0.896/0.195
trmean  sra minmax_h            0.001/0.002        0.009/0.011              0.965/0.962          0.951/0.950            0.902/0.887
 mkrum base signflip            0.001/0.001        0.008/0.009              0.967/0.966          0.951/0.943            0.907/0.827
 mkrum base     alie            0.001/0.001        0.008/0.007              0.967/0.966          0.951/0.575            0.901/0.000
 mkrum base   fang_w            0.001/0.001        0.008/0.009              0.967/0.967          0.951/0.943            0.907/0.827
 mkrum base minmax_h            0.001/0.002        0.008/0.010              0.967/0.962          0.951/0.946            0.860/0.884
 mkrum  sra signflip            0.001/0.002        0.009/0.014              0.965/0.962          0.953/0.872            0.897/0.877
 mkrum  sra     alie            0.001/0.001        0.009/0.011              0.965/0.966          0.953/0.560            0.905/0.000
 mkrum  sra   fang_w            0.001/0.001        0.009/0.010              0.965/0.967          0.953/0.947            0.896/0.232
 mkrum  sra minmax_h            0.001/0.002        0.009/0.013              0.965/0.962          0.953/0.950            0.902/0.892
```


## Portscan | M7 verdicts
```
M7_base_dp: DP_ERODES_ROBUSTNESS (share 0.58)
M7_sra_vs_base_under_dp: 11/12 HOLDS (paired)
```


## Portscan | M9 k* point [5%, 95%] bootstrap over seeds -- seeds 0-2 (mit-2) + 3-4 (mit-3) ('9' = never)
```
 f    agg  FedAvg    base     sra sra_l10
 0  cwmed 1 [1,1] 8 [8,8] 1 [1,1] 1 [1,1]
 0 trmean 1 [1,1] 4 [3,4] 1 [1,1] 1 [1,1]
 0  mkrum 1 [1,1] 4 [4,4] 2 [1,2] 1 [1,1]
 2  cwmed 6 [6,8] 8 [8,8] 3 [3,3] 3 [3,3]
 2 trmean 6 [6,8] 6 [6,6] 3 [3,3] 3 [3,3]
 2  mkrum 6 [6,8] 6 [4,6] 3 [3,3] 3 [3,3]
 4  cwmed 8 [8,8] 9 [8,9] 6 [6,6] 6 [6,6]
 4 trmean 8 [8,8] 8 [8,8] 6 [6,6] 6 [6,6]
 4  mkrum 8 [8,8] 6 [6,8] 6 [6,6] 6 [6,6]
```
