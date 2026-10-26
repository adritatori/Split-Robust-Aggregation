# Claims summary -- CICIDS2017 (script v3.2)


## Botnet | C1a floor P1 (held = never reaches half the learnable line)
```
bucket_cwmed  held=True  max recall at k<=f = 0.000
cclip         held=True  max recall at k<=f = 0.000
cwmed         held=True  max recall at k<=f = 0.000
fedavg        held=True  max recall at k<=f = 0.090
geomed        held=True  max recall at k<=f = 0.000
mkrum         held=True  max recall at k<=f = 0.000
nnm_cwmed     held=True  max recall at k<=f = 0.000
trmean        held=True  max recall at k<=f = 0.001
```


## Botnet | C1b witness tax (k* and tax, f=0)
```
         agg  kstar  kstar_05  tax
      fedavg      2         1    1
       cwmed      7         7    6
      trmean      3         3    2
       mkrum      4         4    3
      geomed      5         4    4
bucket_cwmed      5         5    4
       cclip      4         4    3
   nnm_cwmed      4         3    3
```


## Botnet | C1c missed vs mislabelled (Q-A) + zero-witness control
```
{"multiclass_any": ["MISSED", 0.0], "binary": ["MIXED", 0.32], "n_tax_cells": 25}
K0:    agg                  model  k=0 detection         verdict
 cwmed multiclass(any-attack)            0.0 NEEDS_WITNESSES
 cwmed                 binary            0.0 NEEDS_WITNESSES
fedavg multiclass(any-attack)            0.0 NEEDS_WITNESSES
fedavg                 binary            0.0 NEEDS_WITNESSES
```


## Botnet | C2 wall or delay (k* vs round budget)
```
         agg  k*(R)  k*(2R)  k*(3R) WALL at k
bucket_cwmed      5       5       3    [1, 2]
       cclip      4       3       3       [1]
       cwmed      7       7       5 [1, 2, 3]
      geomed      5       5       3    [1, 2]
       mkrum      4       4       3    [1, 2]
   nnm_cwmed      4       3       3    [1, 2]
      trmean      3       3       3    [1, 2]
```


## Botnet | C3 privacy interaction (f=0)
```
cwmed    k* non-private/eps10/eps3/eps1 = ['8', '3', '3', '16']  clip-only=8  P3 monotone=False
fedavg   k* non-private/eps10/eps3/eps1 = ['1', '3', '4', '6']  clip-only=2  P3 monotone=True
mkrum    k* non-private/eps10/eps3/eps1 = ['4', '2', '3', '12']  clip-only=4  P3 monotone=False
trmean   k* non-private/eps10/eps3/eps1 = ['3', '3', '3', '6']  clip-only=3  P3 monotone=True
```


## Portscan | C1a floor P1 (held = never reaches half the learnable line)
```
bucket_cwmed  held=True  max recall at k<=f = 0.000
cclip         held=True  max recall at k<=f = 0.000
cwmed         held=True  max recall at k<=f = 0.000
fedavg        held=True  max recall at k<=f = 0.187
geomed        held=True  max recall at k<=f = 0.000
mkrum         held=True  max recall at k<=f = 0.000
nnm_cwmed     held=True  max recall at k<=f = 0.000
trmean        held=True  max recall at k<=f = 0.030
```


## Portscan | C1b witness tax (k* and tax, f=0)
```
         agg  kstar  kstar_05  tax
      fedavg      1         1    0
       cwmed      7         6    6
      trmean      4         3    3
       mkrum      4         4    3
      geomed      5         4    4
bucket_cwmed      5         4    4
       cclip      4         4    3
   nnm_cwmed      4         4    3
```


## Portscan | C1c missed vs mislabelled (Q-A) + zero-witness control
```
{"multiclass_any": ["MISSED", 0.038461538461538464], "binary": ["MIXED", 0.38461538461538464], "n_tax_cells": 26}
K0:    agg                  model  k=0 detection         verdict
 cwmed multiclass(any-attack)           0.06 NEEDS_WITNESSES
 cwmed                 binary           0.06 NEEDS_WITNESSES
fedavg multiclass(any-attack)           0.06 NEEDS_WITNESSES
fedavg                 binary           0.06 NEEDS_WITNESSES
```


## Portscan | C2 wall or delay (k* vs round budget)
```
         agg  k*(R)  k*(2R)  k*(3R)    WALL at k
bucket_cwmed      5       4       4       [1, 2]
       cclip      4       3       3          [1]
       cwmed      7       6       5 [1, 2, 3, 4]
      geomed      5       4       3       [1, 2]
       mkrum      4       3       3       [1, 2]
   nnm_cwmed      4       3       3       [1, 2]
      trmean      4       3       3       [1, 2]
```


## Portscan | C3 privacy interaction
```
EXP-B not run for this target
```


## Brute Force | C1a floor P1 (held = never reaches half the learnable line)
```
bucket_cwmed  held=True  max recall at k<=f = 0.000
cclip         held=True  max recall at k<=f = 0.000
cwmed         held=True  max recall at k<=f = 0.000
fedavg        held=True  max recall at k<=f = 0.288
geomed        held=True  max recall at k<=f = 0.000
mkrum         held=True  max recall at k<=f = 0.001
nnm_cwmed     held=True  max recall at k<=f = 0.002
trmean        held=True  max recall at k<=f = 0.094
```


## Brute Force | C1b witness tax (k* and tax, f=0)
```
         agg  kstar  kstar_05  tax
      fedavg      1         1    0
       cwmed      9         7    8
      trmean      3         3    2
       mkrum      4         3    3
      geomed      4         4    3
bucket_cwmed      5         5    4
       cclip      4         3    3
   nnm_cwmed      4         3    3
```


## Brute Force | C1c missed vs mislabelled (Q-A) + zero-witness control
```
{"multiclass_any": ["MISSED", 0.08], "binary": ["MIXED", 0.36], "n_tax_cells": 25}
K0:    agg                  model  k=0 detection         verdict
 cwmed multiclass(any-attack)            0.0 NEEDS_WITNESSES
 cwmed                 binary            0.0 NEEDS_WITNESSES
fedavg multiclass(any-attack)            0.0 NEEDS_WITNESSES
fedavg                 binary            0.0 NEEDS_WITNESSES
```


## Brute Force | C2 wall or delay (k* vs round budget)
```
         agg  k*(R)  k*(2R)  k*(3R) WALL at k
bucket_cwmed      5       4       4    [1, 2]
       cclip      4       3       2       [1]
       cwmed      9       6       5 [1, 2, 3]
      geomed      4       3       3       [1]
       mkrum      4       3       3    [1, 2]
   nnm_cwmed      4       3       3    [1, 2]
      trmean      3       3       3    [1, 2]
```


## Brute Force | C3 privacy interaction
```
EXP-B not run for this target
```


## Natural structure (day-lock): multiclass recall per class
```
                DoS   DDoS  Portscan  Brute Force  Botnet  Web Attack
agg                                                                  
bucket_cwmed  0.904  0.997     0.797        0.987   0.003       0.468
cclip         0.979  0.999     0.816        0.992   0.003       0.868
cwmed         0.000  0.585     0.000        0.115   0.000       0.000
fedavg        0.986  0.999     0.923        0.992   0.884       0.839
geomed        0.883  0.998     0.008        0.987   0.000       0.871
mkrum         0.988  0.999     0.849        0.992   0.410       0.855
nnm_cwmed     0.988  0.999     0.849        0.992   0.405       0.858
trmean        0.976  0.999     0.861        0.991   0.786       0.674
```


## Natural structure (day-lock): BINARY detection per class
```
                DoS   DDoS  Portscan  Brute Force  Botnet  Web Attack
agg                                                                  
bucket_cwmed  0.985  0.999     0.921        0.992   0.725       0.900
cclip         0.990  0.999     0.925        0.993   0.196       0.900
cwmed         0.230  0.991     0.102        0.375   0.000       0.000
fedavg        0.994  0.999     0.963        0.992   0.893       0.900
geomed        0.943  0.999     0.525        0.991   0.000       0.871
mkrum         0.995  0.999     0.938        0.992   0.786       0.903
nnm_cwmed     0.995  0.999     0.936        0.992   0.784       0.903
trmean        0.991  0.999     0.948        0.992   0.861       0.900
```
