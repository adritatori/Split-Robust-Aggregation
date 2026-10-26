# Claims summary -- CSE-CIC-IDS2018 (script v3.2)


## Brute Force | C1a floor P1 (held = never reaches half the learnable line)
```
bucket_cwmed  held=True  max recall at k<=f = 0.000
cclip         held=True  max recall at k<=f = 0.000
cwmed         held=True  max recall at k<=f = 0.000
fedavg        held=True  max recall at k<=f = 0.217
geomed        held=True  max recall at k<=f = 0.000
mkrum         held=True  max recall at k<=f = 0.000
nnm_cwmed     held=True  max recall at k<=f = 0.000
trmean        held=True  max recall at k<=f = 0.096
```


## Brute Force | C1b witness tax (k* and tax, f=0)
```
         agg  kstar  kstar_05  tax
      fedavg      1         1    0
       cwmed     10        10    9
      trmean      3         3    2
       mkrum      4         4    3
      geomed      5         5    4
bucket_cwmed      5         5    4
       cclip      4         4    3
   nnm_cwmed      4         4    3
```


## Brute Force | C1c missed vs mislabelled (Q-A) + zero-witness control
```
{"multiclass_any": ["MIXED", 0.2692307692307692], "binary": ["DETECTED", 1.0], "n_tax_cells": 26}
K0:    agg                  model  k=0 detection                      verdict
 cwmed multiclass(any-attack)          0.016              NEEDS_WITNESSES
 cwmed                 binary          1.000 DETECTABLE_WITHOUT_WITNESSES
fedavg multiclass(any-attack)          0.030              NEEDS_WITNESSES
fedavg                 binary          1.000 DETECTABLE_WITHOUT_WITNESSES
```


## Brute Force | C2 wall or delay (k* vs round budget)
```
         agg  k*(R)  k*(2R)  k*(3R)             WALL at k
bucket_cwmed      5       5       5          [1, 2, 3, 4]
       cclip      4       3       3                [1, 2]
       cwmed     10       9       9 [1, 2, 3, 4, 5, 6, 7]
      geomed      5       4       3                [1, 2]
       mkrum      4       4       3                [1, 2]
   nnm_cwmed      4       3       3                [1, 2]
      trmean      3       3       3                [1, 2]
```


## Brute Force | C3 privacy interaction (f=0)
```
cwmed    k* non-private/eps10/eps3/eps1 = [12, 2, 2, 4]  clip-only=12  P3 monotone=False
fedavg   k* non-private/eps10/eps3/eps1 = [1, 2, 2, 4]  clip-only=2  P3 monotone=True
mkrum    k* non-private/eps10/eps3/eps1 = [4, 2, 2, 4]  clip-only=4  P3 monotone=False
trmean   k* non-private/eps10/eps3/eps1 = [3, 2, 2, 4]  clip-only=4  P3 monotone=False
```


## Botnet | C1a floor P1 (held = never reaches half the learnable line)
```
bucket_cwmed  held=True  max recall at k<=f = 0.000
cclip         held=True  max recall at k<=f = 0.000
cwmed         held=True  max recall at k<=f = 0.000
fedavg        held=True  max recall at k<=f = 0.020
geomed        held=True  max recall at k<=f = 0.000
mkrum         held=True  max recall at k<=f = 0.000
nnm_cwmed     held=True  max recall at k<=f = 0.000
trmean        held=True  max recall at k<=f = 0.000
```


## Botnet | C1b witness tax (k* and tax, f=0)
```
         agg  kstar  kstar_05  tax
      fedavg      1         1    0
       cwmed      9         9    8
      trmean      4         3    3
       mkrum      4         4    3
      geomed      6         6    5
bucket_cwmed      5         5    4
       cclip      5         5    4
   nnm_cwmed      4         4    3
```


## Botnet | C1c missed vs mislabelled (Q-A) + zero-witness control
```
{"multiclass_any": ["MISSED", 0.0], "binary": ["MIXED", 0.4827586206896552], "n_tax_cells": 29}
K0:    agg                  model  k=0 detection         verdict
 cwmed multiclass(any-attack)            0.0 NEEDS_WITNESSES
 cwmed                 binary            0.0 NEEDS_WITNESSES
fedavg multiclass(any-attack)            0.0 NEEDS_WITNESSES
fedavg                 binary            0.0 NEEDS_WITNESSES
```


## Botnet | C2 wall or delay (k* vs round budget)
```
         agg  k*(R)  k*(2R)  k*(3R)       WALL at k
bucket_cwmed      5       5       4       [1, 2, 3]
       cclip      5       4       3          [1, 2]
       cwmed      9       8       7 [1, 2, 3, 4, 5]
      geomed      6       5       4       [1, 2, 3]
       mkrum      4       3       3          [1, 2]
   nnm_cwmed      4       3       3          [1, 2]
      trmean      4       3       3          [1, 2]
```


## Botnet | C3 privacy interaction (f=0)
```
cwmed    k* non-private/eps10/eps3/eps1 = [12, 2, 3, 6]  clip-only=12  P3 monotone=False
fedavg   k* non-private/eps10/eps3/eps1 = [2, 2, 3, 4]  clip-only=2  P3 monotone=True
mkrum    k* non-private/eps10/eps3/eps1 = [4, 2, 2, 4]  clip-only=4  P3 monotone=False
trmean   k* non-private/eps10/eps3/eps1 = [4, 2, 2, 4]  clip-only=4  P3 monotone=False
```


## Natural structure (day-lock): multiclass recall per class
```
                DoS   DDoS  Brute Force  Botnet  Web Attack
agg                                                        
bucket_cwmed  0.134  0.000        0.042   0.000       0.000
cclip         0.980  0.216        1.000   0.665       0.761
cwmed         0.000  0.000        0.000   0.000       0.000
fedavg        0.992  0.434        1.000   0.995       0.310
geomed        0.000  0.000        0.000   0.000       0.849
mkrum         0.948  0.621        1.000   0.995       0.554
nnm_cwmed     0.952  0.619        0.800   0.995       0.486
trmean        0.941  0.047        0.000   0.000       0.000
```


## Natural structure (day-lock): BINARY detection per class
```
                DoS   DDoS  Brute Force  Botnet  Web Attack
agg                                                        
bucket_cwmed  0.980  0.308        1.000   0.994       0.043
cclip         0.981  0.265        1.000   0.995       0.835
cwmed         0.551  0.000        0.009   0.001       0.000
fedavg        0.995  0.808        1.000   0.997       0.779
geomed        0.627  0.004        1.000   0.072       0.857
mkrum         0.981  0.859        1.000   0.997       0.807
nnm_cwmed     0.979  0.860        1.000   0.997       0.823
trmean        0.985  0.404        1.000   0.996       0.288
```
