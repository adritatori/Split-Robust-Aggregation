# mit-2 (SRA) summary -- CSE-CIC-IDS2018 (script mit-2.0)

DATASET HEADLINE: NO_SAFE_POINT_CONFIRMED

secondary (POST-HOC lambda=10): NO_SAFE_POINT_CONFIRMED


## Brute Force | verdicts
```
M3_coverage_sra: REMOVES_TAX
M3_floor: ABOVE_FLOOR
M3_identity: IDENTITY_MATTERS
M3_coverage_sra_l10: REMOVES_TAX
M3_floor_l10: REACHES_FLOOR
M3_lambda_diag: LAMBDA_NOT_THE_ISSUE (lambda=10 does not beat lambda=3 by >= 2 in >= 2/3 of cells)
M3_rr_sra_rr1: FORMULA_HOLDS
M3_rr_sra_rr3: FORMULA_ROUGH (within +-2 only)
M3_cov_orcinf: REMOVES_TAX
M3_cov_elect: REMOVES_TAX
M3_cov_sra_rr1: NO_EFFECT+HARM
M3_cov_sra_rr3: NO_EFFECT+HARM
M3_cov_sra_rand: NO_EFFECT+HARM
M3_floor_flags: 0
M4_sra_k>f: 20/24 HOLDS (paired)
M4_sra_l10_k>f: 20/24 HOLDS (paired)
M4_orcinf_k>f: 15/24 HOLDS (paired)
M4_elect_k>f: 17/24 HOLDS (paired)
M4_sra_k<=f: 7/12 HOLDS (bounded-damage cell, not in headline)
M5_sra_under_dp: NO_TAX_TO_REMOVE
HEADLINE: NO_SAFE_POINT_CONFIRMED
HEADLINE_l10_posthoc: NO_SAFE_POINT_CONFIRMED
```


## Botnet | verdicts
```
M3_coverage_sra: REMOVES_TAX
M3_floor: ABOVE_FLOOR
M3_identity: IDENTITY_MATTERS
M3_coverage_sra_l10: REMOVES_TAX
M3_floor_l10: ABOVE_FLOOR
M3_lambda_diag: LAMBDA_NOT_THE_ISSUE (lambda=10 does not beat lambda=3 by >= 2 in >= 2/3 of cells)
M3_rr_sra_rr1: FORMULA_HOLDS
M3_rr_sra_rr3: FORMULA_HOLDS
M3_cov_orcinf: REMOVES_TAX
M3_cov_elect: NO_EFFECT
M3_cov_sra_rr1: NO_EFFECT+HARM
M3_cov_sra_rr3: REMOVES_TAX
M3_cov_sra_rand: NO_EFFECT+HARM
M3_floor_flags: 0
M4_sra_k>f: 22/24 HOLDS (paired)
M4_sra_l10_k>f: 22/24 HOLDS (paired)
M4_orcinf_k>f: 17/24 HOLDS (paired)
M4_elect_k>f: 23/24 HOLDS (paired)
M4_sra_k<=f: 9/12 HOLDS (bounded-damage cell, not in headline)
M5_sra_under_dp: NO_TAX_TO_REMOVE
HEADLINE: NO_SAFE_POINT_CONFIRMED
HEADLINE_l10_posthoc: NO_SAFE_POINT_CONFIRMED
```


## Brute Force | M3 k* by arm (robustness tax = k*(arm) - k*(FedAvg, same f)); grid k=[1, 2, 3, 4, 6, 8], 'never' = > 8
```
 f    agg          base    orcinf     elect       sra   sra_l10       sra_rr1   sra_rr3      sra_rand
 0 fedavg   1 (floor 1)                                                                              
 0  cwmed never (tax 8) 1 (tax 0) 1 (tax 0) 2 (tax 1) 1 (tax 0)     8 (tax 7) 3 (tax 2) never (tax 8)
 0 trmean     3 (tax 2) 1 (tax 0) 1 (tax 0) 2 (tax 1) 1 (tax 0)     8 (tax 7) 3 (tax 2)     6 (tax 5)
 0  mkrum     4 (tax 3) 1 (tax 0) 1 (tax 0) 2 (tax 1) 1 (tax 0)     8 (tax 7) 3 (tax 2)     6 (tax 5)
 2 fedavg   3 (floor 3)                                                                              
 2  cwmed never (tax 6) 3 (tax 0) 3 (tax 0) 3 (tax 0) 3 (tax 0)     8 (tax 5) 4 (tax 1) never (tax 6)
 2 trmean     4 (tax 1) 3 (tax 0) 3 (tax 0) 3 (tax 0) 3 (tax 0)     8 (tax 5) 4 (tax 1)     4 (tax 1)
 2  mkrum     6 (tax 3) 3 (tax 0) 4 (tax 1) 3 (tax 0) 3 (tax 0)     8 (tax 5) 4 (tax 1)     8 (tax 5)
 4 fedavg   6 (floor 5)                                                                              
 4  cwmed never (tax 3) 6 (tax 0) 6 (tax 0) 6 (tax 0) 6 (tax 0) never (tax 3) 8 (tax 2) never (tax 3)
 4 trmean     6 (tax 0) 6 (tax 0) 6 (tax 0) 6 (tax 0) 6 (tax 0) never (tax 3) 8 (tax 2)     6 (tax 0)
 4  mkrum     6 (tax 0) 6 (tax 0) 6 (tax 0) 6 (tax 0) 6 (tax 0) never (tax 3) 8 (tax 2)     6 (tax 0)
```


## Brute Force | M3 full breakdown: mean target recall by (f, agg, arm) x k  (learnable line 0.800)
```
k                     1     2     3     4     6     8
f agg    arm                                         
0 cwmed  base      0.00  0.00  0.00  0.00  0.00  0.00
         elect     0.99  1.00  1.00  1.00  1.00  1.00
         orcinf    1.00  1.00  1.00  1.00  1.00  1.00
         sra       0.61  1.00  1.00  1.00  1.00  1.00
         sra_l10   1.00  1.00  1.00  1.00  1.00  1.00
         sra_rand  0.00  0.00  0.00  0.00  0.00  0.33
         sra_rr1   0.00  0.00  0.00  0.00  0.67  1.00
         sra_rr3   0.33  0.67  1.00  1.00  1.00  1.00
  fedavg base      0.99  1.00  1.00  1.00  1.00  1.00
  mkrum  base      0.00  0.00  0.00  1.00  1.00  1.00
         elect     0.83  1.00  1.00  1.00  1.00  1.00
         orcinf    1.00  1.00  1.00  1.00  1.00  1.00
         sra       0.00  1.00  1.00  1.00  1.00  1.00
         sra_l10   1.00  1.00  1.00  1.00  1.00  1.00
         sra_rand  0.00  0.00  0.00  0.33  1.00  1.00
         sra_rr1   0.00  0.00  0.00  0.00  0.67  1.00
         sra_rr3   0.33  0.67  1.00  1.00  1.00  1.00
  trmean base      0.00  0.00  0.99  1.00  1.00  1.00
         elect     1.00  1.00  1.00  1.00  1.00  1.00
         orcinf    1.00  1.00  1.00  1.00  1.00  1.00
         sra       0.00  1.00  1.00  1.00  1.00  1.00
         sra_l10   1.00  1.00  1.00  1.00  1.00  1.00
         sra_rand  0.00  0.00  0.67  0.72  1.00  1.00
         sra_rr1   0.00  0.00  0.00  0.00  0.67  1.00
         sra_rr3   0.33  0.67  1.00  1.00  1.00  1.00
2 cwmed  base      0.00  0.00  0.00  0.00  0.00  0.00
         elect     0.00  0.55  1.00  1.00  1.00  1.00
         orcinf    0.00  0.09  0.98  1.00  1.00  1.00
         sra       0.00  0.11  1.00  1.00  1.00  1.00
         sra_l10   0.00  0.11  1.00  1.00  1.00  1.00
         sra_rand  0.00  0.00  0.00  0.00  0.00  0.67
         sra_rr1   0.00  0.00  0.00  0.00  0.67  1.00
         sra_rr3   0.00  0.02  0.67  1.00  1.00  1.00
  fedavg base      0.00  0.06  0.96  1.00  1.00  1.00
  mkrum  base      0.00  0.00  0.00  0.55  1.00  1.00
         elect     0.00  0.00  0.67  1.00  1.00  1.00
         orcinf    0.00  0.07  0.96  1.00  1.00  1.00
         sra       0.00  0.06  1.00  1.00  1.00  1.00
         sra_l10   0.00  0.06  1.00  1.00  1.00  1.00
         sra_rand  0.00  0.00  0.00  0.67  0.67  1.00
         sra_rr1   0.00  0.00  0.00  0.00  0.67  1.00
         sra_rr3   0.00  0.01  0.67  1.00  1.00  1.00
  trmean base      0.00  0.00  0.68  1.00  1.00  1.00
         elect     0.00  0.66  1.00  1.00  1.00  1.00
         orcinf    0.00  0.07  0.97  1.00  1.00  1.00
         sra       0.00  0.09  1.00  1.00  1.00  1.00
         sra_l10   0.00  0.09  1.00  1.00  1.00  1.00
         sra_rand  0.00  0.00  0.52  0.85  1.00  1.00
         sra_rr1   0.00  0.00  0.00  0.21  0.67  1.00
         sra_rr3   0.00  0.01  0.67  1.00  1.00  1.00
4 cwmed  base      0.00  0.00  0.00  0.00  0.00  0.00
         elect     0.00  0.00  0.00  0.64  1.00  1.00
         orcinf    0.00  0.00  0.00  0.26  0.99  1.00
         sra       0.00  0.00  0.00  0.33  1.00  1.00
         sra_l10   0.00  0.00  0.00  0.33  1.00  1.00
         sra_rand  0.00  0.00  0.00  0.00  0.33  0.33
         sra_rr1   0.00  0.00  0.00  0.00  0.00  0.67
         sra_rr3   0.00  0.00  0.00  0.12  0.71  1.00
  fedavg base      0.00  0.00  0.00  0.23  0.99  1.00
  mkrum  base      0.00  0.00  0.00  0.00  1.00  1.00
         elect     0.00  0.00  0.00  0.33  1.00  1.00
         orcinf    0.00  0.00  0.01  0.23  0.99  1.00
         sra       0.00  0.00  0.00  0.30  1.00  1.00
         sra_l10   0.00  0.00  0.00  0.30  1.00  1.00
         sra_rand  0.00  0.00  0.00  0.00  0.99  0.88
         sra_rr1   0.00  0.00  0.00  0.00  0.00  0.67
         sra_rr3   0.00  0.00  0.00  0.08  0.69  1.00
  trmean base      0.00  0.00  0.00  0.14  1.00  1.00
         elect     0.00  0.00  0.00  0.66  1.00  1.00
         orcinf    0.00  0.00  0.00  0.24  0.99  1.00
         sra       0.00  0.00  0.00  0.33  1.00  1.00
         sra_l10   0.00  0.00  0.00  0.33  1.00  1.00
         sra_rand  0.00  0.00  0.00  0.00  1.00  1.00
         sra_rr1   0.00  0.00  0.00  0.00  0.00  0.67
         sra_rr3   0.00  0.00  0.00  0.10  0.73  1.00
```


## Brute Force | M3 RR formula k*: smallest k with k p > (N-k-f)(1-p) + f   (grid-censored comparison)
```
    arm  eps_w  f    agg  predicted k* measured k*  sra (oracle) k*  within 1  within 2
sra_rr1    1.0  0  cwmed             6           8                2      True      True
sra_rr1    1.0  0 trmean             6           8                2      True      True
sra_rr1    1.0  0  mkrum             6           8                2      True      True
sra_rr1    1.0  2  cwmed             7           8                3      True      True
sra_rr1    1.0  2 trmean             7           8                3      True      True
sra_rr1    1.0  2  mkrum             7           8                3      True      True
sra_rr1    1.0  4  cwmed             9       never                6      True      True
sra_rr1    1.0  4 trmean             9       never                6      True      True
sra_rr1    1.0  4  mkrum             9       never                6      True      True
sra_rr3    3.0  0  cwmed             1           3                2     False      True
sra_rr3    3.0  0 trmean             1           3                2     False      True
sra_rr3    3.0  0  mkrum             1           3                2     False      True
sra_rr3    3.0  2  cwmed             3           4                3      True      True
sra_rr3    3.0  2 trmean             3           4                3      True      True
sra_rr3    3.0  2  mkrum             3           4                3      True      True
sra_rr3    3.0  4  cwmed             5           8                6     False      True
sra_rr3    3.0  4 trmean             5           8                6     False      True
sra_rr3    3.0  4  mkrum             5           8                6     False      True
```


## Brute Force | M3 W-stratum composition + clip diagnostics (means over k, seeds)
```
              nW  nW_witness  nW_honest_nonwitness  nW_liar  sra_clip_hit_rate  sra_ratio_median  sra_fallback_rate
arm      f                                                                                                         
elect    0  4.00        4.00                  0.00      0.0                NaN               NaN                NaN
         2  6.00        4.00                  0.00      2.0                NaN               NaN                NaN
         4  8.00        4.00                  0.00      4.0                NaN               NaN                NaN
orcinf   0  4.00        4.00                  0.00      0.0                NaN               NaN                NaN
         2  6.00        4.00                  0.00      2.0                NaN               NaN                NaN
         4  8.00        4.00                  0.00      4.0                NaN               NaN                NaN
sra      0  4.00        4.00                  0.00      0.0               0.22              1.93                0.0
         2  6.00        4.00                  0.00      2.0               0.01              1.03                0.0
         4  8.00        4.00                  0.00      4.0               0.00              0.75                0.0
sra_l10  0  4.00        4.00                  0.00      0.0               0.00              1.78                0.0
         2  6.00        4.00                  0.00      2.0               0.00              1.03                0.0
         4  8.00        4.00                  0.00      4.0               0.00              0.75                0.0
sra_rand 0  4.00        0.94                  3.06      0.0               0.00              0.38                0.0
         2  6.00        1.06                  2.94      2.0               0.00              0.47                0.0
         4  8.00        1.39                  2.61      4.0               0.00              0.49                0.0
sra_rr1  0  7.50        3.00                  4.50      0.0               0.00              0.54                0.0
         2  9.50        3.22                  4.28      2.0               0.00              0.55                0.0
         4  9.83        2.89                  2.94      4.0               0.00              0.54                0.0
sra_rr3  0  4.83        3.83                  1.00      0.0               0.02              1.11                0.0
         2  6.61        3.83                  0.78      2.0               0.00              0.89                0.0
         4  8.06        3.78                  0.28      4.0               0.00              0.70                0.0
```


## Brute Force | M3 per-class recall at f=0, k=6 (what else moves)
```
                 benign_fpr  other_attack_recall_mean  other_attack_recall_min  recall_Normal  recall_DoS  recall_DDoS  recall_Portscan  recall_Brute Force  recall_Botnet  recall_Web Attack
agg    arm                                                                                                                                                                                   
cwmed  base           0.003                     0.948                    0.802          0.997       0.997        0.996              NaN               0.000          0.998              0.802
       elect          0.003                     0.925                    0.706          0.997       0.997        0.996              NaN               1.000          0.998              0.706
       orcinf         0.003                     0.931                    0.730          0.997       0.997        0.997              NaN               1.000          0.998              0.730
       sra            0.003                     0.924                    0.706          0.997       0.997        0.996              NaN               1.000          0.997              0.706
       sra_l10        0.003                     0.924                    0.706          0.997       0.997        0.996              NaN               1.000          0.997              0.706
       sra_rand       0.003                     0.961                    0.851          0.997       0.997        0.997              NaN               0.000          0.998              0.851
       sra_rr1        0.003                     0.960                    0.849          0.997       0.997        0.997              NaN               0.667          0.998              0.849
       sra_rr3        0.003                     0.924                    0.706          0.997       0.997        0.996              NaN               1.000          0.998              0.706
fedavg base           0.003                     0.961                    0.849          0.997       0.998        0.998              NaN               1.000          1.000              0.849
mkrum  base           0.003                     0.961                    0.849          0.997       0.998        0.997              NaN               1.000          1.000              0.849
       elect          0.003                     0.925                    0.706          0.997       0.998        0.997              NaN               1.000          0.999              0.706
       orcinf         0.003                     0.961                    0.849          0.997       0.998        0.997              NaN               1.000          0.999              0.849
       sra            0.003                     0.936                    0.750          0.997       0.998        0.997              NaN               1.000          0.999              0.750
       sra_l10        0.003                     0.936                    0.750          0.997       0.998        0.997              NaN               1.000          0.999              0.750
       sra_rand       0.003                     0.960                    0.847          0.997       0.998        0.997              NaN               1.000          0.999              0.847
       sra_rr1        0.003                     0.961                    0.849          0.997       0.998        0.997              NaN               0.667          0.999              0.849
       sra_rr3        0.003                     0.942                    0.774          0.997       0.998        0.997              NaN               1.000          0.999              0.774
trmean base           0.003                     0.938                    0.760          0.997       0.998        0.997              NaN               1.000          0.998              0.760
       elect          0.003                     0.925                    0.706          0.997       0.998        0.997              NaN               1.000          0.999              0.706
       orcinf         0.003                     0.939                    0.764          0.997       0.998        0.997              NaN               1.000          0.998              0.764
       sra            0.003                     0.925                    0.708          0.997       0.998        0.997              NaN               1.000          0.998              0.708
       sra_l10        0.003                     0.925                    0.708          0.997       0.998        0.997              NaN               1.000          0.998              0.708
       sra_rand       0.003                     0.960                    0.849          0.997       0.997        0.997              NaN               1.000          0.998              0.849
       sra_rr1        0.003                     0.960                    0.849          0.997       0.998        0.997              NaN               0.667          0.998              0.849
       sra_rr3        0.003                     0.925                    0.708          0.997       0.998        0.997              NaN               1.000          0.998              0.708
```


## Brute Force | M3 verdicts
```
COVERAGE (sra)        : REMOVES_TAX
FLOOR (sra k* <= f+1) : ABOVE_FLOOR (share 0.33)
IDENTITY (sra_rand)   : IDENTITY_MATTERS
-- post-hoc lambda diagnostic (NOT the headline) --
COVERAGE (sra_l10)    : REMOVES_TAX
FLOOR (sra_l10)       : REACHES_FLOOR (share 0.67)
LAMBDA DIAGNOSTIC     : LAMBDA_NOT_THE_ISSUE (lambda=10 does not beat lambda=3 by >= 2 in >= 2/3 of cells)
RR formula sra_rr1    : FORMULA_HOLDS
RR formula sra_rr3    : FORMULA_ROUGH (within +-2 only)
coverage orcinf       : REMOVES_TAX
coverage elect        : REMOVES_TAX
coverage sra_rr1      : NO_EFFECT+HARM
coverage sra_rr3      : NO_EFFECT+HARM
coverage sra_rand     : NO_EFFECT+HARM
floor violations      : none
worst sra cell        : cwmed f=0 k*=2 tax=1
```


## Brute Force | M4 sign-flip x10 / ALIE z=1  ('_nc' = attackers do NOT claim evidence)
```
 k  f      attack    agg     arm  benign_fpr  other_mean  other_min      paired                     absolute
 6  2    signflip fedavg    base       1.000       0.167      0.000                                effective
 6  2    signflip  cwmed    base       0.004       0.959      0.845 (reference)                        HOLDS
 6  2    signflip  cwmed     sra       0.004       0.959      0.845       HOLDS                        HOLDS
 6  2 signflip_nc  cwmed     sra       0.004       0.960      0.845       HOLDS                        HOLDS
 6  2    signflip  cwmed sra_l10       0.004       0.959      0.845       HOLDS                        HOLDS
 6  2 signflip_nc  cwmed sra_l10       0.004       0.960      0.845       HOLDS                        HOLDS
 6  2    signflip  cwmed  orcinf       0.546       0.083      0.000      BREAKS                       BREAKS
 6  2 signflip_nc  cwmed  orcinf       0.004       0.960      0.845       HOLDS                        HOLDS
 6  2    signflip  cwmed   elect       0.004       0.924      0.704       HOLDS                        HOLDS
 6  2 signflip_nc  cwmed   elect       0.004       0.924      0.704       HOLDS                        HOLDS
 6  2    signflip trmean    base       0.004       0.960      0.845 (reference)                        HOLDS
 6  2    signflip trmean     sra       0.004       0.960      0.845       HOLDS                        HOLDS
 6  2 signflip_nc trmean     sra       0.004       0.960      0.845       HOLDS                        HOLDS
 6  2    signflip trmean sra_l10       0.004       0.960      0.845       HOLDS                        HOLDS
 6  2 signflip_nc trmean sra_l10       0.004       0.960      0.845       HOLDS                        HOLDS
 6  2    signflip trmean  orcinf       0.643       0.042      0.000      BREAKS                       BREAKS
 6  2 signflip_nc trmean  orcinf       0.004       0.960      0.845       HOLDS                        HOLDS
 6  2    signflip trmean   elect       0.004       0.906      0.629      BREAKS                       BREAKS
 6  2 signflip_nc trmean   elect       0.004       0.949      0.802       HOLDS                        HOLDS
 6  2    signflip  mkrum    base       0.003       0.961      0.847 (reference)                        HOLDS
 6  2    signflip  mkrum     sra       0.004       0.943      0.780       HOLDS                        HOLDS
 6  2 signflip_nc  mkrum     sra       0.003       0.961      0.847       HOLDS                        HOLDS
 6  2    signflip  mkrum sra_l10       0.004       0.943      0.780       HOLDS                        HOLDS
 6  2 signflip_nc  mkrum sra_l10       0.003       0.961      0.847       HOLDS                        HOLDS
 6  2    signflip  mkrum  orcinf       0.864       0.083      0.000      BREAKS                       BREAKS
 6  2 signflip_nc  mkrum  orcinf       0.003       0.961      0.847       HOLDS                        HOLDS
 6  2    signflip  mkrum   elect       0.003       0.962      0.851       HOLDS                        HOLDS
 6  2 signflip_nc  mkrum   elect       0.003       0.962      0.851       HOLDS                        HOLDS
 6  2        alie fedavg    base       0.003       0.961      0.847                          attack too weak
 6  2        alie  cwmed    base       0.003       0.960      0.845 (reference) INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2        alie  cwmed     sra       0.003       0.960      0.845       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2     alie_nc  cwmed     sra       0.003       0.960      0.847       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2        alie  cwmed sra_l10       0.003       0.960      0.845       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2     alie_nc  cwmed sra_l10       0.003       0.960      0.847       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2        alie  cwmed  orcinf       0.003       0.960      0.845       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2     alie_nc  cwmed  orcinf       0.003       0.960      0.847       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2        alie  cwmed   elect       0.004       0.934      0.742       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2     alie_nc  cwmed   elect       0.004       0.924      0.704       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2        alie trmean    base       0.003       0.961      0.847 (reference) INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2        alie trmean     sra       0.003       0.960      0.847       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2     alie_nc trmean     sra       0.003       0.960      0.847       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2        alie trmean sra_l10       0.003       0.960      0.847       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2     alie_nc trmean sra_l10       0.003       0.960      0.847       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2        alie trmean  orcinf       0.003       0.961      0.847       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2     alie_nc trmean  orcinf       0.003       0.961      0.847       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2        alie trmean   elect       0.003       0.961      0.847       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2     alie_nc trmean   elect       0.003       0.961      0.847       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2        alie  mkrum    base       0.003       0.961      0.847 (reference) INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2        alie  mkrum     sra       0.003       0.961      0.847       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2     alie_nc  mkrum     sra       0.003       0.961      0.847       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2        alie  mkrum sra_l10       0.003       0.961      0.847       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2     alie_nc  mkrum sra_l10       0.003       0.961      0.847       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2        alie  mkrum  orcinf       0.003       0.960      0.845       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2     alie_nc  mkrum  orcinf       0.003       0.961      0.847       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2        alie  mkrum   elect       0.003       0.962      0.851       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2     alie_nc  mkrum   elect       0.003       0.962      0.851       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4    signflip fedavg    base       0.709       0.123      0.000                                effective
 6  4    signflip  cwmed    base       0.005       0.899      0.607 (reference)                       BREAKS
 6  4    signflip  cwmed     sra       0.006       0.774      0.107      BREAKS                       BREAKS
 6  4 signflip_nc  cwmed     sra       0.005       0.853      0.423       HOLDS                       BREAKS
 6  4    signflip  cwmed sra_l10       0.006       0.774      0.107      BREAKS                       BREAKS
 6  4 signflip_nc  cwmed sra_l10       0.005       0.853      0.423       HOLDS                       BREAKS
 6  4    signflip  cwmed  orcinf       0.344       0.132      0.000      BREAKS                       BREAKS
 6  4 signflip_nc  cwmed  orcinf       0.005       0.860      0.448       HOLDS                       BREAKS
 6  4    signflip  cwmed   elect       0.005       0.783      0.141      BREAKS                       BREAKS
 6  4 signflip_nc  cwmed   elect       0.005       0.783      0.141      BREAKS                       BREAKS
 6  4    signflip trmean    base       0.742       0.167      0.000 (reference)                       BREAKS
 6  4    signflip trmean     sra       0.005       0.776      0.113       HOLDS                       BREAKS
 6  4 signflip_nc trmean     sra       0.767       0.167      0.000       HOLDS                       BREAKS
 6  4    signflip trmean sra_l10       0.005       0.776      0.113       HOLDS                       BREAKS
 6  4 signflip_nc trmean sra_l10       0.767       0.167      0.000       HOLDS                       BREAKS
 6  4    signflip trmean  orcinf       0.667       0.084      0.000      BREAKS                       BREAKS
 6  4 signflip_nc trmean  orcinf       0.666       0.083      0.000      BREAKS                       BREAKS
 6  4    signflip trmean   elect       0.557       0.089      0.000      BREAKS                       BREAKS
 6  4 signflip_nc trmean   elect       0.712       0.166      0.000       HOLDS                       BREAKS
 6  4    signflip  mkrum    base       0.643       0.166      0.000 (reference)                       BREAKS
 6  4    signflip  mkrum     sra       0.005       0.764      0.067       HOLDS                       BREAKS
 6  4 signflip_nc  mkrum     sra       0.225       0.083      0.000      BREAKS                       BREAKS
 6  4    signflip  mkrum sra_l10       0.005       0.764      0.067       HOLDS                       BREAKS
 6  4 signflip_nc  mkrum sra_l10       0.225       0.083      0.000      BREAKS                       BREAKS
 6  4    signflip  mkrum  orcinf       0.357       0.000      0.000      BREAKS                       BREAKS
 6  4 signflip_nc  mkrum  orcinf       0.333       0.000      0.000      BREAKS                       BREAKS
 6  4    signflip  mkrum   elect       0.654       0.167      0.000       HOLDS                       BREAKS
 6  4 signflip_nc  mkrum   elect       0.885       0.201      0.000      BREAKS                       BREAKS
 6  4        alie fedavg    base       0.003       0.924      0.700                          attack too weak
 6  4        alie  cwmed    base       0.003       0.960      0.847 (reference) INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4        alie  cwmed     sra       0.004       0.899      0.603      BREAKS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4     alie_nc  cwmed     sra       0.004       0.854      0.425      BREAKS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4        alie  cwmed sra_l10       0.004       0.899      0.603      BREAKS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4     alie_nc  cwmed sra_l10       0.004       0.854      0.425      BREAKS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4        alie  cwmed  orcinf       0.003       0.916      0.669       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4     alie_nc  cwmed  orcinf       0.004       0.890      0.563      BREAKS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4        alie  cwmed   elect       0.004       0.829      0.323      BREAKS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4     alie_nc  cwmed   elect       0.004       0.795      0.188      BREAKS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4        alie trmean    base       0.003       0.891      0.567 (reference) INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4        alie trmean     sra       0.004       0.900      0.605       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4     alie_nc trmean     sra       0.003       0.867      0.474       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4        alie trmean sra_l10       0.004       0.900      0.605       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4     alie_nc trmean sra_l10       0.003       0.867      0.474       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4        alie trmean  orcinf       0.003       0.913      0.657       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4     alie_nc trmean  orcinf       0.003       0.893      0.577       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4        alie trmean   elect       0.003       0.890      0.565       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4     alie_nc trmean   elect       0.003       0.890      0.565       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4        alie  mkrum    base       0.003       0.904      0.621 (reference) INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4        alie  mkrum     sra       0.004       0.902      0.613       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4     alie_nc  mkrum     sra       0.003       0.868      0.476       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4        alie  mkrum sra_l10       0.004       0.902      0.613       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4     alie_nc  mkrum sra_l10       0.003       0.868      0.476       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4        alie  mkrum  orcinf       0.003       0.911      0.647       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4     alie_nc  mkrum  orcinf       0.003       0.891      0.567       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4        alie  mkrum   elect       0.003       0.960      0.845       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4     alie_nc  mkrum   elect       0.003       0.899      0.601       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4    signflip fedavg    base       0.995       0.250      0.000                                effective
 2  4    signflip  cwmed    base       0.005       0.747      0.000 (reference)                       BREAKS
 2  4    signflip  cwmed     sra       0.105       0.666      0.147      BREAKS                       BREAKS
 2  4 signflip_nc  cwmed     sra       0.005       0.822      0.298       HOLDS                       BREAKS
 2  4    signflip  cwmed sra_l10       0.246       0.074      0.000      BREAKS                       BREAKS
 2  4 signflip_nc  cwmed sra_l10       0.005       0.822      0.298       HOLDS                       BREAKS
 2  4    signflip  cwmed  orcinf       0.667       0.000      0.000      BREAKS                       BREAKS
 2  4 signflip_nc  cwmed  orcinf       0.005       0.822      0.298       HOLDS                       BREAKS
 2  4    signflip  cwmed   elect       1.000       0.000      0.000      BREAKS                       BREAKS
 2  4 signflip_nc  cwmed   elect       0.005       0.747      0.000       HOLDS                       BREAKS
 2  4    signflip trmean    base       0.506       0.107      0.000 (reference)                       BREAKS
 2  4    signflip trmean     sra       0.185       0.728      0.000       HOLDS                       BREAKS
 2  4 signflip_nc trmean     sra       0.623       0.083      0.000      BREAKS                       BREAKS
 2  4    signflip trmean sra_l10       0.167       0.042      0.000      BREAKS                       BREAKS
 2  4 signflip_nc trmean sra_l10       0.623       0.083      0.000      BREAKS                       BREAKS
 2  4    signflip trmean  orcinf       0.667       0.069      0.000      BREAKS                       BREAKS
 2  4 signflip_nc trmean  orcinf       0.956       0.166      0.000      BREAKS                       BREAKS
 2  4    signflip trmean   elect       0.667       0.000      0.000      BREAKS                       BREAKS
 2  4 signflip_nc trmean   elect       0.270       0.082      0.000       HOLDS                       BREAKS
 2  4    signflip  mkrum    base       0.352       0.084      0.000 (reference)                       BREAKS
 2  4    signflip  mkrum     sra       0.103       0.729      0.000       HOLDS                       BREAKS
 2  4 signflip_nc  mkrum     sra       0.333       0.083      0.000       HOLDS                       BREAKS
 2  4    signflip  mkrum sra_l10       0.027       0.000      0.000      BREAKS                       BREAKS
 2  4 signflip_nc  mkrum sra_l10       0.333       0.083      0.000       HOLDS                       BREAKS
 2  4    signflip  mkrum  orcinf       0.819       0.099      0.000      BREAKS                       BREAKS
 2  4 signflip_nc  mkrum  orcinf       0.667       0.083      0.000      BREAKS                       BREAKS
 2  4    signflip  mkrum   elect       1.000       0.000      0.000      BREAKS                       BREAKS
 2  4 signflip_nc  mkrum   elect       0.378       0.083      0.000       HOLDS                       BREAKS
 2  4        alie fedavg    base       0.003       0.960      0.845                          attack too weak
 2  4        alie  cwmed    base       0.003       0.810      0.250 (reference) INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4        alie  cwmed     sra       0.003       0.748      0.000      BREAKS INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4     alie_nc  cwmed     sra       0.003       0.924      0.702       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4        alie  cwmed sra_l10       0.003       0.748      0.000      BREAKS INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4     alie_nc  cwmed sra_l10       0.003       0.924      0.702       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4        alie  cwmed  orcinf       0.003       0.960      0.845       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4     alie_nc  cwmed  orcinf       0.003       0.924      0.702       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4        alie  cwmed   elect       0.003       0.782      0.137       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4     alie_nc  cwmed   elect       0.003       0.748      0.000      BREAKS INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4        alie trmean    base       0.003       0.884      0.540 (reference) INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4        alie trmean     sra       0.003       0.749      0.000      BREAKS INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4     alie_nc trmean     sra       0.003       0.960      0.845       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4        alie trmean sra_l10       0.003       0.749      0.000      BREAKS INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4     alie_nc trmean sra_l10       0.003       0.960      0.845       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4        alie trmean  orcinf       0.003       0.960      0.845       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4     alie_nc trmean  orcinf       0.003       0.960      0.845       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4        alie trmean   elect       0.003       0.749      0.000      BREAKS INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4     alie_nc trmean   elect       0.003       0.821      0.290      BREAKS INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4        alie  mkrum    base       0.003       0.835      0.343 (reference) INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4        alie  mkrum     sra       0.003       0.754      0.022      BREAKS INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4     alie_nc  mkrum     sra       0.003       0.960      0.845       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4        alie  mkrum sra_l10       0.003       0.754      0.022      BREAKS INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4     alie_nc  mkrum sra_l10       0.003       0.960      0.845       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4        alie  mkrum  orcinf       0.003       0.960      0.845       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4     alie_nc  mkrum  orcinf       0.003       0.960      0.845       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4        alie  mkrum   elect       0.002       0.749      0.000      BREAKS INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4     alie_nc  mkrum   elect       0.003       0.783      0.137      BREAKS INCONCLUSIVE_ATTACK_TOO_WEAK
```


## Brute Force | M4 SRA W-stratum composition + clip-hit rate
```
                           nW  nW_witness  nW_liar  sra_clip_hit_rate  sra_ratio_median
arm     k f attack                                                                     
sra     2 4 alie          6.0         2.0      4.0               0.00              1.28
            alie_nc       2.0         2.0      0.0               0.28              2.55
            signflip      6.0         2.0      4.0               1.00             16.69
            signflip_nc   2.0         2.0      0.0               0.00              0.20
        6 2 alie          8.0         6.0      2.0               0.00              1.08
            alie_nc       6.0         6.0      0.0               0.00              1.26
            signflip      8.0         6.0      2.0               0.00              1.02
            signflip_nc   6.0         6.0      0.0               0.00              0.95
          4 alie         10.0         6.0      4.0               0.00              1.12
            alie_nc       6.0         6.0      0.0               0.00              1.25
            signflip     10.0         6.0      4.0               0.00              1.15
            signflip_nc   6.0         6.0      0.0               0.00              0.20
sra_l10 2 4 alie          6.0         2.0      4.0               0.00              1.28
            alie_nc       2.0         2.0      0.0               0.00              2.48
            signflip      6.0         2.0      4.0               0.93             33.65
            signflip_nc   2.0         2.0      0.0               0.00              0.20
        6 2 alie          8.0         6.0      2.0               0.00              1.08
            alie_nc       6.0         6.0      0.0               0.00              1.26
            signflip      8.0         6.0      2.0               0.00              1.02
            signflip_nc   6.0         6.0      0.0               0.00              0.95
          4 alie         10.0         6.0      4.0               0.00              1.12
            alie_nc       6.0         6.0      0.0               0.00              1.25
            signflip     10.0         6.0      4.0               0.00              1.15
            signflip_nc   6.0         6.0      0.0               0.00              0.20
```


## Brute Force | M4 full per-class recall
```
                                recall_Normal  recall_DoS  recall_DDoS  recall_Portscan  recall_Brute Force  recall_Botnet  recall_Web Attack
k f attack      agg    arm                                                                                                                   
2 0 mimic       fedavg base             0.997       0.998        0.997              NaN               1.000          1.000              0.851
  4 alie        cwmed  base             0.997       0.998        0.995              NaN               0.000          0.999              0.250
                       elect            0.997       0.998        0.995              NaN               0.000          0.999              0.137
                       orcinf           0.997       0.998        0.996              NaN               1.000          0.999              0.845
                       sra              0.997       0.998        0.996              NaN               0.000          1.000              0.000
                       sra_l10          0.997       0.998        0.996              NaN               0.000          1.000              0.000
                fedavg base             0.997       0.998        0.997              NaN               1.000          1.000              0.845
                mkrum  base             0.997       0.998        0.997              NaN               0.000          1.000              0.343
                       elect            0.998       0.998        0.997              NaN               0.000          1.000              0.000
                       orcinf           0.997       0.998        0.997              NaN               1.000          1.000              0.845
                       sra              0.997       0.998        0.997              NaN               0.000          1.000              0.022
                       sra_l10          0.997       0.998        0.997              NaN               0.000          1.000              0.022
                trmean base             0.997       0.998        0.997              NaN               0.000          1.000              0.540
                       elect            0.997       0.998        0.997              NaN               0.000          1.000              0.000
                       orcinf           0.997       0.998        0.996              NaN               1.000          1.000              0.845
                       sra              0.997       0.998        0.996              NaN               0.000          1.000              0.000
                       sra_l10          0.997       0.998        0.996              NaN               0.000          1.000              0.000
    alie_nc     cwmed  elect            0.997       0.998        0.995              NaN               1.000          0.998              0.000
                       orcinf           0.997       0.998        0.995              NaN               1.000          0.999              0.702
                       sra              0.997       0.998        0.995              NaN               1.000          0.999              0.702
                       sra_l10          0.997       0.998        0.995              NaN               1.000          0.999              0.702
                mkrum  elect            0.997       0.998        0.997              NaN               0.999          1.000              0.137
                       orcinf           0.997       0.998        0.997              NaN               1.000          1.000              0.845
                       sra              0.997       0.998        0.997              NaN               1.000          1.000              0.845
                       sra_l10          0.997       0.998        0.997              NaN               1.000          1.000              0.845
                trmean elect            0.997       0.998        0.996              NaN               1.000          1.000              0.290
                       orcinf           0.997       0.998        0.997              NaN               1.000          1.000              0.845
                       sra              0.997       0.998        0.997              NaN               1.000          1.000              0.845
                       sra_l10          0.997       0.998        0.997              NaN               1.000          1.000              0.845
    signflip    cwmed  base             0.995       0.996        0.995              NaN               0.000          0.997              0.000
                       elect            0.000       0.000        0.000              NaN               1.000          0.000              0.000
                       orcinf           0.333       0.000        0.000              NaN               0.000          0.000              0.000
                       sra              0.895       0.802        0.866              NaN               0.000          0.830              0.167
                       sra_l10          0.754       0.165        0.132              NaN               0.000          0.000              0.000
                fedavg base             0.005       0.000        0.333              NaN               0.333          0.667              0.000
                mkrum  base             0.648       0.333        0.001              NaN               0.000          0.000              0.000
                       elect            0.000       0.000        0.000              NaN               0.333          0.000              0.000
                       orcinf           0.181       0.333        0.064              NaN               0.000          0.000              0.000
                       sra              0.897       0.954        0.965              NaN               0.000          0.998              0.000
                       sra_l10          0.973       0.000        0.001              NaN               0.000          0.000              0.000
                trmean base             0.494       0.000        0.426              NaN               0.000          0.000              0.000
                       elect            0.333       0.000        0.000              NaN               0.667          0.000              0.000
                       orcinf           0.333       0.004        0.270              NaN               0.000          0.000              0.000
                       sra              0.815       0.990        0.928              NaN               0.000          0.994              0.000
                       sra_l10          0.833       0.167        0.000              NaN               0.000          0.000              0.000
    signflip_nc cwmed  elect            0.995       0.997        0.995              NaN               0.693          0.997              0.000
                       orcinf           0.995       0.997        0.995              NaN               1.000          0.997              0.298
                       sra              0.995       0.997        0.995              NaN               1.000          0.997              0.298
                       sra_l10          0.995       0.997        0.995              NaN               1.000          0.997              0.298
                mkrum  elect            0.622       0.333        0.000              NaN               0.000          0.000              0.000
                       orcinf           0.333       0.000        0.333              NaN               0.333          0.000              0.000
                       sra              0.667       0.000        0.000              NaN               0.000          0.000              0.333
                       sra_l10          0.667       0.000        0.000              NaN               0.000          0.000              0.333
                trmean elect            0.730       0.329        0.000              NaN               0.000          0.000              0.000
                       orcinf           0.044       0.331        0.333              NaN               0.333          0.000              0.000
                       sra              0.377       0.333        0.000              NaN               0.333          0.000              0.000
                       sra_l10          0.377       0.333        0.000              NaN               0.333          0.000              0.000
6 0 mimic       fedavg base             0.997       0.998        0.998              NaN               1.000          1.000              0.849
  2 alie        cwmed  base             0.997       0.998        0.995              NaN               0.000          1.000              0.845
                       elect            0.996       0.998        0.995              NaN               1.000          1.000              0.742
                       orcinf           0.997       0.998        0.996              NaN               1.000          1.000              0.845
                       sra              0.997       0.998        0.996              NaN               1.000          1.000              0.845
                       sra_l10          0.997       0.998        0.996              NaN               1.000          1.000              0.845
                fedavg base             0.997       0.998        0.997              NaN               1.000          1.000              0.847
                mkrum  base             0.997       0.998        0.997              NaN               1.000          1.000              0.847
                       elect            0.997       0.998        0.997              NaN               1.000          1.000              0.851
                       orcinf           0.997       0.998        0.997              NaN               1.000          1.000              0.845
                       sra              0.997       0.998        0.997              NaN               1.000          1.000              0.847
                       sra_l10          0.997       0.998        0.997              NaN               1.000          1.000              0.847
                trmean base             0.997       0.998        0.997              NaN               1.000          1.000              0.847
                       elect            0.997       0.998        0.997              NaN               1.000          1.000              0.847
                       orcinf           0.997       0.998        0.997              NaN               1.000          1.000              0.847
                       sra              0.997       0.998        0.996              NaN               1.000          1.000              0.847
                       sra_l10          0.997       0.998        0.996              NaN               1.000          1.000              0.847
    alie_nc     cwmed  elect            0.996       0.998        0.995              NaN               1.000          1.000              0.704
                       orcinf           0.997       0.998        0.996              NaN               1.000          1.000              0.847
                       sra              0.997       0.998        0.996              NaN               1.000          1.000              0.847
                       sra_l10          0.997       0.998        0.996              NaN               1.000          1.000              0.847
                mkrum  elect            0.997       0.998        0.997              NaN               1.000          1.000              0.851
                       orcinf           0.997       0.998        0.997              NaN               1.000          1.000              0.847
                       sra              0.997       0.998        0.997              NaN               1.000          1.000              0.847
                       sra_l10          0.997       0.998        0.997              NaN               1.000          1.000              0.847
                trmean elect            0.997       0.998        0.997              NaN               1.000          1.000              0.847
                       orcinf           0.997       0.998        0.997              NaN               1.000          1.000              0.847
                       sra              0.997       0.998        0.996              NaN               1.000          1.000              0.847
                       sra_l10          0.997       0.998        0.996              NaN               1.000          1.000              0.847
    signflip    cwmed  base             0.996       0.997        0.995              NaN               0.000          1.000              0.845
                       elect            0.996       0.997        0.995              NaN               1.000          1.000              0.704
                       orcinf           0.454       0.000        0.333              NaN               0.167          0.000              0.000
                       sra              0.996       0.998        0.995              NaN               1.000          1.000              0.845
                       sra_l10          0.996       0.998        0.995              NaN               1.000          1.000              0.845
                fedavg base             0.000       0.334        0.333              NaN               0.333          0.000              0.000
                mkrum  base             0.997       0.998        0.997              NaN               1.000          1.000              0.847
                       elect            0.997       0.999        0.997              NaN               1.000          1.000              0.851
                       orcinf           0.136       0.000        0.333              NaN               0.667          0.000              0.000
                       sra              0.996       0.998        0.996              NaN               1.000          1.000              0.780
                       sra_l10          0.996       0.998        0.996              NaN               1.000          1.000              0.780
                trmean base             0.996       0.998        0.996              NaN               1.000          1.000              0.845
                       elect            0.996       0.998        0.996              NaN               1.000          1.000              0.629
                       orcinf           0.357       0.003        0.000              NaN               0.333          0.167              0.000
                       sra              0.996       0.998        0.995              NaN               1.000          1.000              0.845
                       sra_l10          0.996       0.998        0.995              NaN               1.000          1.000              0.845
    signflip_nc cwmed  elect            0.996       0.998        0.995              NaN               1.000          1.000              0.704
                       orcinf           0.996       0.998        0.996              NaN               1.000          1.000              0.845
                       sra              0.996       0.998        0.995              NaN               1.000          1.000              0.845
                       sra_l10          0.996       0.998        0.995              NaN               1.000          1.000              0.845
                mkrum  elect            0.997       0.999        0.997              NaN               1.000          1.000              0.851
                       orcinf           0.997       0.998        0.997              NaN               1.000          1.000              0.847
                       sra              0.997       0.998        0.997              NaN               1.000          1.000              0.847
                       sra_l10          0.997       0.998        0.997              NaN               1.000          1.000              0.847
                trmean elect            0.996       0.998        0.996              NaN               1.000          1.000              0.802
                       orcinf           0.996       0.998        0.996              NaN               1.000          1.000              0.845
                       sra              0.996       0.998        0.996              NaN               1.000          1.000              0.845
                       sra_l10          0.996       0.998        0.996              NaN               1.000          1.000              0.845
  4 alie        cwmed  base             0.997       0.998        0.996              NaN               0.667          0.999              0.847
                       elect            0.996       0.998        0.996              NaN               1.000          0.999              0.323
                       orcinf           0.997       0.998        0.997              NaN               1.000          1.000              0.669
                       sra              0.996       0.998        0.997              NaN               1.000          0.999              0.603
                       sra_l10          0.996       0.998        0.997              NaN               1.000          0.999              0.603
                fedavg base             0.997       0.998        0.998              NaN               1.000          1.000              0.700
                mkrum  base             0.997       0.998        0.998              NaN               1.000          1.000              0.621
                       elect            0.997       0.998        0.998              NaN               1.000          1.000              0.845
                       orcinf           0.997       0.998        0.998              NaN               1.000          1.000              0.647
                       sra              0.996       0.998        0.997              NaN               1.000          0.999              0.613
                       sra_l10          0.996       0.998        0.997              NaN               1.000          0.999              0.613
                trmean base             0.997       0.998        0.997              NaN               1.000          1.000              0.567
                       elect            0.997       0.998        0.997              NaN               1.000          1.000              0.565
                       orcinf           0.997       0.998        0.997              NaN               1.000          1.000              0.657
                       sra              0.996       0.998        0.997              NaN               1.000          0.999              0.605
                       sra_l10          0.996       0.998        0.997              NaN               1.000          0.999              0.605
    alie_nc     cwmed  elect            0.996       0.998        0.996              NaN               1.000          0.999              0.188
                       orcinf           0.996       0.998        0.997              NaN               1.000          0.999              0.563
                       sra              0.996       0.998        0.996              NaN               1.000          0.999              0.425
                       sra_l10          0.996       0.998        0.996              NaN               1.000          0.999              0.425
                mkrum  elect            0.997       0.998        0.998              NaN               1.000          1.000              0.601
                       orcinf           0.997       0.998        0.998              NaN               1.000          1.000              0.567
                       sra              0.997       0.998        0.998              NaN               1.000          0.999              0.476
                       sra_l10          0.997       0.998        0.998              NaN               1.000          0.999              0.476
                trmean elect            0.997       0.998        0.998              NaN               1.000          1.000              0.565
                       orcinf           0.997       0.998        0.997              NaN               1.000          1.000              0.577
                       sra              0.997       0.998        0.997              NaN               1.000          0.999              0.474
                       sra_l10          0.997       0.998        0.997              NaN               1.000          0.999              0.474
    signflip    cwmed  base             0.995       0.997        0.995              NaN               0.000          0.997              0.607
                       elect            0.995       0.997        0.995              NaN               1.000          0.997              0.141
                       orcinf           0.656       0.333        0.194              NaN               0.000          0.000              0.000
                       sra              0.994       0.997        0.995              NaN               1.000          0.997              0.107
                       sra_l10          0.994       0.997        0.995              NaN               1.000          0.997              0.107
                fedavg base             0.291       0.354        0.139              NaN               0.000          0.000              0.000
                mkrum  base             0.357       0.332        0.333              NaN               0.000          0.000              0.000
                       elect            0.346       0.333        0.001              NaN               0.000          0.333              0.000
                       orcinf           0.643       0.000        0.000              NaN               0.000          0.000              0.000
                       sra              0.995       0.997        0.996              NaN               1.000          0.997              0.067
                       sra_l10          0.995       0.997        0.996              NaN               1.000          0.997              0.067
                trmean base             0.258       0.333        0.333              NaN               0.000          0.000              0.000
                       elect            0.443       0.026        0.332              NaN               0.000          0.000              0.000
                       orcinf           0.333       0.333        0.002              NaN               0.333          0.000              0.000
                       sra              0.995       0.997        0.996              NaN               1.000          0.998              0.113
                       sra_l10          0.995       0.997        0.996              NaN               1.000          0.998              0.113
    signflip_nc cwmed  elect            0.995       0.997        0.995              NaN               1.000          0.997              0.141
                       orcinf           0.995       0.998        0.996              NaN               1.000          0.998              0.448
                       sra              0.995       0.997        0.996              NaN               1.000          0.997              0.423
                       sra_l10          0.995       0.997        0.996              NaN               1.000          0.997              0.423
                mkrum  elect            0.115       0.667        0.137              NaN               0.000          0.000              0.000
                       orcinf           0.667       0.000        0.000              NaN               0.000          0.000              0.000
                       sra              0.775       0.333        0.000              NaN               0.000          0.000              0.000
                       sra_l10          0.775       0.333        0.000              NaN               0.000          0.000              0.000
                trmean elect            0.288       0.332        0.334              NaN               0.000          0.000              0.000
                       orcinf           0.334       0.333        0.000              NaN               0.000          0.000              0.000
                       sra              0.233       0.000        0.000              NaN               0.333          0.667              0.000
                       sra_l10          0.233       0.000        0.000              NaN               0.333          0.667              0.000
```


## Brute Force | M4 paired verdict counts (HOLDS / BREAKS) by arm and cell type
```
paired                         BREAKS  HOLDS
arm     cell                                
elect   k<=f (bounded damage)       8      4
        k>f                         7     17
orcinf  k<=f (bounded damage)       5      7
        k>f                         9     15
sra     k<=f (bounded damage)       5      7
        k>f                         4     20
sra_l10 k<=f (bounded damage)       7      5
        k>f                         4     20
```


## Brute Force | M5 mean target recall under DP (DP reference FedAvg k=16: 1.000)
```
k               1     2     3    4    6    8
agg    arm                                  
cwmed  base  0.17  0.83  0.88  1.0  1.0  1.0
       sra   0.31  0.83  1.00  1.0  1.0  1.0
fedavg base  0.16  1.00  1.00  1.0  1.0  1.0
mkrum  base  0.16  1.00  1.00  1.0  1.0  1.0
       sra   0.06  1.00  1.00  1.0  1.0  1.0
trmean base  0.02  0.88  1.00  1.0  1.0  1.0
       sra   0.00  0.92  1.00  1.0  1.0  1.0
```


## Brute Force | M5 k* under DP (learnable line 0.8x DP reference = 0.800)
```
 f    agg        base       sra
 0 fedavg 2 (floor 1)          
 0  cwmed   2 (tax 0) 2 (tax 0)
 0 trmean   2 (tax 0) 2 (tax 0)
 0  mkrum   2 (tax 0) 2 (tax 0)
```


## Brute Force | M5 per-class recall under DP
```
             benign_fpr  other_attack_recall_mean  recall_Normal  recall_DoS  recall_DDoS  recall_Portscan  recall_Brute Force  recall_Botnet  recall_Web Attack
agg    arm                                                                                                                                                      
cwmed  base       0.007                     0.745          0.993       0.987        0.995              NaN                 1.0          0.997                0.0
       sra        0.007                     0.745          0.993       0.989        0.995              NaN                 1.0          0.997                0.0
fedavg base       0.007                     0.746          0.993       0.989        0.996              NaN                 1.0          0.999                0.0
mkrum  base       0.007                     0.746          0.993       0.988        0.995              NaN                 1.0          0.999                0.0
       sra        0.007                     0.746          0.993       0.989        0.996              NaN                 1.0          0.998                0.0
trmean base       0.007                     0.746          0.993       0.989        0.995              NaN                 1.0          0.998                0.0
       sra        0.007                     0.746          0.993       0.989        0.996              NaN                 1.0          0.998                0.0
```


## Brute Force | M5 verdict
```
SRA under DP (tax vs FedAvg-DP): NO_TAX_TO_REMOVE
```


## Botnet | M3 k* by arm (robustness tax = k*(arm) - k*(FedAvg, same f)); grid k=[1, 2, 3, 4, 6, 8], 'never' = > 8
```
 f    agg          base    orcinf     elect       sra   sra_l10       sra_rr1   sra_rr3      sra_rand
 0 fedavg   2 (floor 1)                                                                              
 0  cwmed never (tax 7) 2 (tax 0) 6 (tax 4) 2 (tax 0) 2 (tax 0)     8 (tax 6) 3 (tax 1) never (tax 7)
 0 trmean     4 (tax 2) 2 (tax 0) 3 (tax 1) 2 (tax 0) 2 (tax 0)     6 (tax 4) 3 (tax 1)     3 (tax 1)
 0  mkrum     4 (tax 2) 2 (tax 0) 3 (tax 1) 2 (tax 0) 2 (tax 0)     8 (tax 6) 3 (tax 1)     6 (tax 4)
 2 fedavg   4 (floor 3)                                                                              
 2  cwmed never (tax 5) 4 (tax 0) 6 (tax 2) 3 (tax 0) 3 (tax 0)     8 (tax 4) 4 (tax 0) never (tax 5)
 2 trmean     4 (tax 0) 4 (tax 0) 3 (tax 0) 3 (tax 0) 3 (tax 0)     8 (tax 4) 4 (tax 0)     6 (tax 2)
 2  mkrum     6 (tax 2) 4 (tax 0) 6 (tax 2) 3 (tax 0) 3 (tax 0)     8 (tax 4) 4 (tax 0)     8 (tax 4)
 4 fedavg   6 (floor 5)                                                                              
 4  cwmed never (tax 3) 6 (tax 0) 8 (tax 2) 6 (tax 0) 6 (tax 0) never (tax 3) 6 (tax 0) never (tax 3)
 4 trmean     6 (tax 0) 6 (tax 0) 6 (tax 0) 6 (tax 0) 6 (tax 0)     8 (tax 2) 6 (tax 0)     8 (tax 2)
 4  mkrum     8 (tax 2) 6 (tax 0) 6 (tax 0) 6 (tax 0) 6 (tax 0)     8 (tax 2) 6 (tax 0)     8 (tax 2)
```


## Botnet | M3 full breakdown: mean target recall by (f, agg, arm) x k  (learnable line 0.796)
```
k                     1     2     3     4     6     8
f agg    arm                                         
0 cwmed  base      0.00  0.00  0.00  0.00  0.00  0.02
         elect     0.00  0.00  0.00  0.18  0.99  1.00
         orcinf    0.58  0.99  1.00  1.00  1.00  1.00
         sra       0.00  0.99  0.99  1.00  1.00  1.00
         sra_l10   0.58  0.99  0.99  1.00  1.00  1.00
         sra_rand  0.00  0.04  0.00  0.00  0.33  0.72
         sra_rr1   0.00  0.00  0.00  0.00  0.66  1.00
         sra_rr3   0.21  0.66  1.00  1.00  1.00  1.00
  fedavg base      0.69  0.99  0.99  1.00  1.00  1.00
  mkrum  base      0.00  0.00  0.00  0.99  0.99  1.00
         elect     0.00  0.00  0.92  1.00  1.00  1.00
         orcinf    0.59  0.99  0.99  1.00  1.00  1.00
         sra       0.00  0.99  0.99  1.00  1.00  1.00
         sra_l10   0.59  0.99  0.99  1.00  1.00  1.00
         sra_rand  0.00  0.00  0.00  0.33  0.99  0.99
         sra_rr1   0.00  0.00  0.00  0.00  0.79  1.00
         sra_rr3   0.24  0.66  1.00  1.00  1.00  1.00
  trmean base      0.00  0.00  0.67  0.99  1.00  1.00
         elect     0.00  0.00  1.00  1.00  1.00  1.00
         orcinf    0.57  0.99  0.99  1.00  1.00  1.00
         sra       0.00  0.99  0.99  1.00  1.00  1.00
         sra_l10   0.57  0.99  0.99  1.00  1.00  1.00
         sra_rand  0.00  0.08  0.86  0.89  0.99  0.99
         sra_rr1   0.00  0.00  0.00  0.00  0.99  1.00
         sra_rr3   0.24  0.66  1.00  1.00  1.00  1.00
2 cwmed  base      0.00  0.00  0.00  0.00  0.00  0.00
         elect     0.00  0.00  0.00  0.00  0.99  0.99
         orcinf    0.00  0.00  0.58  0.99  0.99  1.00
         sra       0.00  0.00  1.00  1.00  1.00  1.00
         sra_l10   0.00  0.00  1.00  1.00  1.00  1.00
         sra_rand  0.00  0.00  0.00  0.00  0.00  0.33
         sra_rr1   0.00  0.00  0.00  0.00  0.66  1.00
         sra_rr3   0.00  0.00  0.33  1.00  1.00  1.00
  fedavg base      0.00  0.00  0.60  0.99  0.99  1.00
  mkrum  base      0.00  0.00  0.00  0.00  1.00  1.00
         elect     0.00  0.00  0.00  0.75  1.00  1.00
         orcinf    0.00  0.00  0.54  0.99  0.99  1.00
         sra       0.00  0.00  1.00  1.00  1.00  1.00
         sra_l10   0.00  0.00  1.00  1.00  1.00  1.00
         sra_rand  0.00  0.00  0.00  0.18  0.33  0.99
         sra_rr1   0.00  0.00  0.00  0.00  0.66  1.00
         sra_rr3   0.00  0.00  0.33  1.00  1.00  1.00
  trmean base      0.00  0.00  0.00  0.99  0.99  0.99
         elect     0.00  0.00  0.94  1.00  1.00  1.00
         orcinf    0.00  0.00  0.56  0.99  0.99  1.00
         sra       0.00  0.00  1.00  1.00  1.00  1.00
         sra_l10   0.00  0.00  1.00  1.00  1.00  1.00
         sra_rand  0.00  0.00  0.00  0.33  0.84  0.99
         sra_rr1   0.00  0.00  0.00  0.00  0.66  1.00
         sra_rr3   0.00  0.00  0.33  1.00  1.00  1.00
4 cwmed  base      0.00  0.00  0.00  0.00  0.00  0.00
         elect     0.00  0.00  0.00  0.00  0.00  0.99
         orcinf    0.00  0.00  0.00  0.02  0.97  0.99
         sra       0.00  0.00  0.00  0.00  1.00  1.00
         sra_l10   0.00  0.00  0.00  0.00  1.00  1.00
         sra_rand  0.00  0.00  0.00  0.00  0.33  0.66
         sra_rr1   0.00  0.00  0.00  0.00  0.33  0.66
         sra_rr3   0.00  0.00  0.00  0.00  1.00  1.00
  fedavg base      0.00  0.00  0.00  0.02  0.97  0.99
  mkrum  base      0.00  0.00  0.00  0.00  0.75  1.00
         elect     0.00  0.00  0.00  0.00  1.00  1.00
         orcinf    0.00  0.00  0.00  0.01  0.96  0.99
         sra       0.00  0.00  0.00  0.00  1.00  1.00
         sra_l10   0.00  0.00  0.00  0.00  1.00  1.00
         sra_rand  0.00  0.00  0.00  0.00  0.50  0.82
         sra_rr1   0.00  0.00  0.00  0.00  0.33  0.88
         sra_rr3   0.00  0.00  0.00  0.00  1.00  1.00
  trmean base      0.00  0.00  0.00  0.00  0.99  0.99
         elect     0.00  0.00  0.00  0.00  0.99  0.99
         orcinf    0.00  0.00  0.00  0.01  0.97  0.99
         sra       0.00  0.00  0.00  0.00  1.00  1.00
         sra_l10   0.00  0.00  0.00  0.00  1.00  1.00
         sra_rand  0.00  0.00  0.00  0.00  0.67  0.99
         sra_rr1   0.00  0.00  0.00  0.00  0.33  0.99
         sra_rr3   0.00  0.00  0.00  0.00  1.00  1.00
```


## Botnet | M3 RR formula k*: smallest k with k p > (N-k-f)(1-p) + f   (grid-censored comparison)
```
    arm  eps_w  f    agg  predicted k* measured k*  sra (oracle) k*  within 1  within 2
sra_rr1    1.0  0  cwmed             6           8                2      True      True
sra_rr1    1.0  0 trmean             6           6                2      True      True
sra_rr1    1.0  0  mkrum             6           8                2      True      True
sra_rr1    1.0  2  cwmed             7           8                3      True      True
sra_rr1    1.0  2 trmean             7           8                3      True      True
sra_rr1    1.0  2  mkrum             7           8                3      True      True
sra_rr1    1.0  4  cwmed             9       never                6      True      True
sra_rr1    1.0  4 trmean             9           8                6      True      True
sra_rr1    1.0  4  mkrum             9           8                6      True      True
sra_rr3    3.0  0  cwmed             1           3                2     False      True
sra_rr3    3.0  0 trmean             1           3                2     False      True
sra_rr3    3.0  0  mkrum             1           3                2     False      True
sra_rr3    3.0  2  cwmed             3           4                3      True      True
sra_rr3    3.0  2 trmean             3           4                3      True      True
sra_rr3    3.0  2  mkrum             3           4                3      True      True
sra_rr3    3.0  4  cwmed             5           6                6      True      True
sra_rr3    3.0  4 trmean             5           6                6      True      True
sra_rr3    3.0  4  mkrum             5           6                6      True      True
```


## Botnet | M3 W-stratum composition + clip diagnostics (means over k, seeds)
```
              nW  nW_witness  nW_honest_nonwitness  nW_liar  sra_clip_hit_rate  sra_ratio_median  sra_fallback_rate
arm      f                                                                                                         
elect    0  4.00        4.00                  0.00      0.0                NaN               NaN                NaN
         2  6.00        4.00                  0.00      2.0                NaN               NaN                NaN
         4  8.00        4.00                  0.00      4.0                NaN               NaN                NaN
orcinf   0  4.00        4.00                  0.00      0.0                NaN               NaN                NaN
         2  6.00        4.00                  0.00      2.0                NaN               NaN                NaN
         4  8.00        4.00                  0.00      4.0                NaN               NaN                NaN
sra      0  4.00        4.00                  0.00      0.0               0.24              2.06                0.0
         2  6.00        4.00                  0.00      2.0               0.00              0.88                0.0
         4  8.00        4.00                  0.00      4.0               0.00              0.64                0.0
sra_l10  0  4.00        4.00                  0.00      0.0               0.00              1.82                0.0
         2  6.00        4.00                  0.00      2.0               0.00              0.88                0.0
         4  8.00        4.00                  0.00      4.0               0.00              0.64                0.0
sra_rand 0  4.00        1.00                  3.00      0.0               0.00              0.48                0.0
         2  6.00        1.44                  2.56      2.0               0.00              0.36                0.0
         4  8.00        1.22                  2.78      4.0               0.00              0.37                0.0
sra_rr1  0  7.17        2.83                  4.33      0.0               0.00              0.49                0.0
         2  8.72        2.83                  3.89      2.0               0.00              0.48                0.0
         4  9.67        2.94                  2.72      4.0               0.00              0.42                0.0
sra_rr3  0  4.94        3.89                  1.06      0.0               0.02              1.06                0.0
         2  6.50        3.78                  0.72      2.0               0.00              0.75                0.0
         4  8.50        4.00                  0.50      4.0               0.00              0.61                0.0
```


## Botnet | M3 per-class recall at f=0, k=6 (what else moves)
```
                 benign_fpr  other_attack_recall_mean  other_attack_recall_min  recall_Normal  recall_DoS  recall_DDoS  recall_Portscan  recall_Brute Force  recall_Botnet  recall_Web Attack
agg    arm                                                                                                                                                                                   
cwmed  base           0.001                     0.960                    0.845          0.999       0.998        0.997              NaN                 1.0          0.000              0.845
       elect          0.001                     0.961                    0.849          0.999       0.998        0.996              NaN                 1.0          0.995              0.849
       orcinf         0.001                     0.961                    0.849          0.999       0.998        0.998              NaN                 1.0          0.995              0.849
       sra            0.001                     0.960                    0.847          0.999       0.998        0.996              NaN                 1.0          0.995              0.847
       sra_l10        0.001                     0.960                    0.847          0.999       0.998        0.996              NaN                 1.0          0.995              0.847
       sra_rand       0.001                     0.960                    0.845          0.999       0.998        0.997              NaN                 1.0          0.331              0.845
       sra_rr1        0.001                     0.961                    0.847          0.999       0.998        0.997              NaN                 1.0          0.663              0.847
       sra_rr3        0.001                     0.961                    0.849          0.999       0.998        0.996              NaN                 1.0          0.995              0.849
fedavg base           0.001                     0.963                    0.855          0.999       0.999        0.998              NaN                 1.0          0.995              0.855
mkrum  base           0.001                     0.961                    0.847          0.999       0.999        0.998              NaN                 1.0          0.995              0.847
       elect          0.001                     0.962                    0.851          0.999       0.999        0.998              NaN                 1.0          0.995              0.851
       orcinf         0.001                     0.961                    0.847          0.999       0.999        0.998              NaN                 1.0          0.995              0.847
       sra            0.001                     0.961                    0.847          0.999       0.998        0.998              NaN                 1.0          0.995              0.847
       sra_l10        0.001                     0.961                    0.847          0.999       0.998        0.998              NaN                 1.0          0.995              0.847
       sra_rand       0.001                     0.961                    0.849          0.999       0.998        0.998              NaN                 1.0          0.995              0.849
       sra_rr1        0.001                     0.961                    0.847          0.999       0.999        0.998              NaN                 1.0          0.795              0.847
       sra_rr3        0.001                     0.961                    0.847          0.999       0.998        0.998              NaN                 1.0          0.995              0.847
trmean base           0.001                     0.962                    0.849          0.999       0.999        0.998              NaN                 1.0          0.995              0.849
       elect          0.001                     0.962                    0.851          0.999       0.999        0.998              NaN                 1.0          0.995              0.851
       orcinf         0.001                     0.962                    0.849          0.999       0.999        0.998              NaN                 1.0          0.995              0.849
       sra            0.001                     0.961                    0.849          0.999       0.998        0.998              NaN                 1.0          0.995              0.849
       sra_l10        0.001                     0.961                    0.849          0.999       0.998        0.998              NaN                 1.0          0.995              0.849
       sra_rand       0.001                     0.961                    0.849          0.999       0.998        0.998              NaN                 1.0          0.995              0.849
       sra_rr1        0.001                     0.961                    0.849          0.999       0.998        0.998              NaN                 1.0          0.992              0.849
       sra_rr3        0.001                     0.961                    0.849          0.999       0.998        0.998              NaN                 1.0          0.995              0.849
```


## Botnet | M3 verdicts
```
COVERAGE (sra)        : REMOVES_TAX
FLOOR (sra k* <= f+1) : ABOVE_FLOOR (share 0.33)
IDENTITY (sra_rand)   : IDENTITY_MATTERS
-- post-hoc lambda diagnostic (NOT the headline) --
COVERAGE (sra_l10)    : REMOVES_TAX
FLOOR (sra_l10)       : ABOVE_FLOOR (share 0.33)
LAMBDA DIAGNOSTIC     : LAMBDA_NOT_THE_ISSUE (lambda=10 does not beat lambda=3 by >= 2 in >= 2/3 of cells)
RR formula sra_rr1    : FORMULA_HOLDS
RR formula sra_rr3    : FORMULA_HOLDS
coverage orcinf       : REMOVES_TAX
coverage elect        : NO_EFFECT
coverage sra_rr1      : NO_EFFECT+HARM
coverage sra_rr3      : REMOVES_TAX
coverage sra_rand     : NO_EFFECT+HARM
floor violations      : none
worst sra cell        : cwmed f=0 k*=2 tax=0
```


## Botnet | M4 sign-flip x10 / ALIE z=1  ('_nc' = attackers do NOT claim evidence)
```
 k  f      attack    agg     arm  benign_fpr  other_mean  other_min      paired                     absolute
 6  2    signflip fedavg    base       0.984       0.300      0.000                                effective
 6  2    signflip  cwmed    base       0.001       0.960      0.847 (reference)                        HOLDS
 6  2    signflip  cwmed     sra       0.001       0.960      0.847       HOLDS                        HOLDS
 6  2 signflip_nc  cwmed     sra       0.001       0.960      0.847       HOLDS                        HOLDS
 6  2    signflip  cwmed sra_l10       0.001       0.960      0.847       HOLDS                        HOLDS
 6  2 signflip_nc  cwmed sra_l10       0.001       0.960      0.847       HOLDS                        HOLDS
 6  2    signflip  cwmed  orcinf       0.859       0.166      0.000      BREAKS                       BREAKS
 6  2 signflip_nc  cwmed  orcinf       0.001       0.960      0.847       HOLDS                        HOLDS
 6  2    signflip  cwmed   elect       0.001       0.961      0.849       HOLDS                        HOLDS
 6  2 signflip_nc  cwmed   elect       0.001       0.961      0.849       HOLDS                        HOLDS
 6  2    signflip trmean    base       0.001       0.960      0.847 (reference)                        HOLDS
 6  2    signflip trmean     sra       0.001       0.960      0.847       HOLDS                        HOLDS
 6  2 signflip_nc trmean     sra       0.001       0.960      0.847       HOLDS                        HOLDS
 6  2    signflip trmean sra_l10       0.001       0.960      0.847       HOLDS                        HOLDS
 6  2 signflip_nc trmean sra_l10       0.001       0.960      0.847       HOLDS                        HOLDS
 6  2    signflip trmean  orcinf       0.815       0.166      0.000      BREAKS                       BREAKS
 6  2 signflip_nc trmean  orcinf       0.001       0.962      0.851       HOLDS                        HOLDS
 6  2    signflip trmean   elect       0.001       0.962      0.853       HOLDS                        HOLDS
 6  2 signflip_nc trmean   elect       0.001       0.962      0.853       HOLDS                        HOLDS
 6  2    signflip  mkrum    base       0.001       0.965      0.863 (reference)                        HOLDS
 6  2    signflip  mkrum     sra       0.001       0.961      0.849       HOLDS                        HOLDS
 6  2 signflip_nc  mkrum     sra       0.001       0.964      0.861       HOLDS                        HOLDS
 6  2    signflip  mkrum sra_l10       0.001       0.961      0.849       HOLDS                        HOLDS
 6  2 signflip_nc  mkrum sra_l10       0.001       0.964      0.861       HOLDS                        HOLDS
 6  2    signflip  mkrum  orcinf       0.667       0.083      0.000      BREAKS                       BREAKS
 6  2 signflip_nc  mkrum  orcinf       0.001       0.965      0.861       HOLDS                        HOLDS
 6  2    signflip  mkrum   elect       0.001       0.965      0.863       HOLDS                        HOLDS
 6  2 signflip_nc  mkrum   elect       0.001       0.965      0.863       HOLDS                        HOLDS
 6  2        alie fedavg    base       0.001       0.965      0.861                          attack too weak
 6  2        alie  cwmed    base       0.001       0.961      0.849 (reference) INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2        alie  cwmed     sra       0.001       0.962      0.853       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2     alie_nc  cwmed     sra       0.001       0.961      0.851       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2        alie  cwmed sra_l10       0.001       0.962      0.853       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2     alie_nc  cwmed sra_l10       0.001       0.961      0.851       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2        alie  cwmed  orcinf       0.001       0.964      0.861       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2     alie_nc  cwmed  orcinf       0.001       0.964      0.859       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2        alie  cwmed   elect       0.001       0.961      0.851       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2     alie_nc  cwmed   elect       0.001       0.961      0.851       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2        alie trmean    base       0.001       0.964      0.861 (reference) INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2        alie trmean     sra       0.001       0.962      0.853       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2     alie_nc trmean     sra       0.001       0.964      0.861       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2        alie trmean sra_l10       0.001       0.962      0.853       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2     alie_nc trmean sra_l10       0.001       0.964      0.861       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2        alie trmean  orcinf       0.001       0.964      0.861       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2     alie_nc trmean  orcinf       0.001       0.964      0.861       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2        alie trmean   elect       0.001       0.964      0.861       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2     alie_nc trmean   elect       0.001       0.964      0.861       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2        alie  mkrum    base       0.001       0.965      0.861 (reference) INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2        alie  mkrum     sra       0.001       0.964      0.861       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2     alie_nc  mkrum     sra       0.001       0.964      0.861       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2        alie  mkrum sra_l10       0.001       0.964      0.861       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2     alie_nc  mkrum sra_l10       0.001       0.964      0.861       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2        alie  mkrum  orcinf       0.001       0.964      0.861       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2     alie_nc  mkrum  orcinf       0.001       0.965      0.861       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2        alie  mkrum   elect       0.001       0.965      0.861       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2     alie_nc  mkrum   elect       0.001       0.965      0.861       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4    signflip fedavg    base       0.667       0.167      0.000                                effective
 6  4    signflip  cwmed    base       0.001       0.960      0.845 (reference)                        HOLDS
 6  4    signflip  cwmed     sra       0.004       0.960      0.845       HOLDS                        HOLDS
 6  4 signflip_nc  cwmed     sra       0.002       0.960      0.845       HOLDS                        HOLDS
 6  4    signflip  cwmed sra_l10       0.004       0.960      0.845       HOLDS                        HOLDS
 6  4 signflip_nc  cwmed sra_l10       0.002       0.960      0.845       HOLDS                        HOLDS
 6  4    signflip  cwmed  orcinf       0.719       0.166      0.000      BREAKS                       BREAKS
 6  4 signflip_nc  cwmed  orcinf       0.002       0.960      0.845       HOLDS                        HOLDS
 6  4    signflip  cwmed   elect       0.001       0.960      0.845       HOLDS                        HOLDS
 6  4 signflip_nc  cwmed   elect       0.001       0.960      0.845       HOLDS                        HOLDS
 6  4    signflip trmean    base       0.333       0.083      0.000 (reference)                       BREAKS
 6  4    signflip trmean     sra       0.004       0.960      0.845       HOLDS                        HOLDS
 6  4 signflip_nc trmean     sra       0.667       0.083      0.000      BREAKS                       BREAKS
 6  4    signflip trmean sra_l10       0.004       0.960      0.845       HOLDS                        HOLDS
 6  4 signflip_nc trmean sra_l10       0.667       0.083      0.000      BREAKS                       BREAKS
 6  4    signflip trmean  orcinf       0.333       0.083      0.000       HOLDS                       BREAKS
 6  4 signflip_nc trmean  orcinf       0.822       0.000      0.000      BREAKS                       BREAKS
 6  4    signflip trmean   elect       0.333       0.083      0.000       HOLDS                       BREAKS
 6  4 signflip_nc trmean   elect       0.349       0.067      0.000       HOLDS                       BREAKS
 6  4    signflip  mkrum    base       0.665       0.167      0.000 (reference)                       BREAKS
 6  4    signflip  mkrum     sra       0.004       0.960      0.845       HOLDS                        HOLDS
 6  4 signflip_nc  mkrum     sra       0.667       0.000      0.000      BREAKS                       BREAKS
 6  4    signflip  mkrum sra_l10       0.004       0.960      0.845       HOLDS                        HOLDS
 6  4 signflip_nc  mkrum sra_l10       0.667       0.000      0.000      BREAKS                       BREAKS
 6  4    signflip  mkrum  orcinf       0.784       0.166      0.000      BREAKS                       BREAKS
 6  4 signflip_nc  mkrum  orcinf       0.974       0.008      0.000      BREAKS                       BREAKS
 6  4    signflip  mkrum   elect       0.667       0.167      0.000       HOLDS                       BREAKS
 6  4 signflip_nc  mkrum   elect       0.834       0.161      0.000      BREAKS                       BREAKS
 6  4        alie fedavg    base       0.001       0.962      0.851                          attack too weak
 6  4        alie  cwmed    base       0.001       0.960      0.845 (reference) INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4        alie  cwmed     sra       0.001       0.961      0.849       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4     alie_nc  cwmed     sra       0.001       0.961      0.849       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4        alie  cwmed sra_l10       0.001       0.961      0.849       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4     alie_nc  cwmed sra_l10       0.001       0.961      0.849       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4        alie  cwmed  orcinf       0.001       0.962      0.851       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4     alie_nc  cwmed  orcinf       0.001       0.961      0.849       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4        alie  cwmed   elect       0.001       0.960      0.845       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4     alie_nc  cwmed   elect       0.001       0.960      0.847       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4        alie trmean    base       0.001       0.961      0.849 (reference) INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4        alie trmean     sra       0.001       0.961      0.849       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4     alie_nc trmean     sra       0.001       0.961      0.849       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4        alie trmean sra_l10       0.001       0.961      0.849       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4     alie_nc trmean sra_l10       0.001       0.961      0.849       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4        alie trmean  orcinf       0.001       0.962      0.851       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4     alie_nc trmean  orcinf       0.001       0.962      0.851       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4        alie trmean   elect       0.001       0.962      0.851       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4     alie_nc trmean   elect       0.001       0.962      0.853       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4        alie  mkrum    base       0.001       0.962      0.851 (reference) INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4        alie  mkrum     sra       0.001       0.961      0.849       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4     alie_nc  mkrum     sra       0.001       0.961      0.849       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4        alie  mkrum sra_l10       0.001       0.961      0.849       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4     alie_nc  mkrum sra_l10       0.001       0.961      0.849       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4        alie  mkrum  orcinf       0.001       0.962      0.851       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4     alie_nc  mkrum  orcinf       0.001       0.961      0.849       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4        alie  mkrum   elect       0.001       0.962      0.853       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4     alie_nc  mkrum   elect       0.001       0.962      0.853       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4    signflip fedavg    base       0.667       0.133      0.000                                effective
 2  4    signflip  cwmed    base       0.001       0.961      0.849 (reference)                        HOLDS
 2  4    signflip  cwmed     sra       0.007       0.521      0.000      BREAKS                       BREAKS
 2  4 signflip_nc  cwmed     sra       0.001       0.960      0.845       HOLDS                        HOLDS
 2  4    signflip  cwmed sra_l10       0.666       0.183      0.000      BREAKS                       BREAKS
 2  4 signflip_nc  cwmed sra_l10       0.001       0.960      0.845       HOLDS                        HOLDS
 2  4    signflip  cwmed  orcinf       0.518       0.012      0.000      BREAKS                       BREAKS
 2  4 signflip_nc  cwmed  orcinf       0.001       0.960      0.845       HOLDS                        HOLDS
 2  4    signflip  cwmed   elect       1.000       0.000      0.000      BREAKS                       BREAKS
 2  4 signflip_nc  cwmed   elect       0.001       0.960      0.849       HOLDS                        HOLDS
 2  4    signflip trmean    base       0.602       0.000      0.000 (reference)                       BREAKS
 2  4    signflip trmean     sra       0.188       0.620      0.000       HOLDS                       BREAKS
 2  4 signflip_nc trmean     sra       1.000       0.083      0.000      BREAKS                       BREAKS
 2  4    signflip trmean sra_l10       0.667       0.083      0.000      BREAKS                       BREAKS
 2  4 signflip_nc trmean sra_l10       1.000       0.083      0.000      BREAKS                       BREAKS
 2  4    signflip trmean  orcinf       0.656       0.228      0.000      BREAKS                       BREAKS
 2  4 signflip_nc trmean  orcinf       1.000       0.083      0.000      BREAKS                       BREAKS
 2  4    signflip trmean   elect       1.000       0.083      0.000      BREAKS                       BREAKS
 2  4 signflip_nc trmean   elect       0.361       0.083      0.000       HOLDS                       BREAKS
 2  4    signflip  mkrum    base       0.787       0.159      0.000 (reference)                       BREAKS
 2  4    signflip  mkrum     sra       0.170       0.486      0.008       HOLDS                       BREAKS
 2  4 signflip_nc  mkrum     sra       1.000       0.167      0.000      BREAKS                       BREAKS
 2  4    signflip  mkrum sra_l10       0.000       0.000      0.000      BREAKS                       BREAKS
 2  4 signflip_nc  mkrum sra_l10       1.000       0.167      0.000      BREAKS                       BREAKS
 2  4    signflip  mkrum  orcinf       0.706       0.003      0.000      BREAKS                       BREAKS
 2  4 signflip_nc  mkrum  orcinf       0.826       0.166      0.000       HOLDS                       BREAKS
 2  4    signflip  mkrum   elect       0.333       0.000      0.000      BREAKS                       BREAKS
 2  4 signflip_nc  mkrum   elect       0.767       0.068      0.000      BREAKS                       BREAKS
 2  4        alie fedavg    base       0.001       0.963      0.853                          attack too weak
 2  4        alie  cwmed    base       0.001       0.961      0.849 (reference) INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4        alie  cwmed     sra       0.001       0.961      0.847       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4     alie_nc  cwmed     sra       0.001       0.961      0.849       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4        alie  cwmed sra_l10       0.001       0.961      0.847       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4     alie_nc  cwmed sra_l10       0.001       0.961      0.849       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4        alie  cwmed  orcinf       0.001       0.961      0.849       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4     alie_nc  cwmed  orcinf       0.001       0.961      0.849       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4        alie  cwmed   elect       0.001       0.961      0.849       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4     alie_nc  cwmed   elect       0.001       0.961      0.849       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4        alie trmean    base       0.001       0.962      0.849 (reference) INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4        alie trmean     sra       0.001       0.961      0.849       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4     alie_nc trmean     sra       0.001       0.962      0.851       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4        alie trmean sra_l10       0.001       0.961      0.849       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4     alie_nc trmean sra_l10       0.001       0.962      0.851       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4        alie trmean  orcinf       0.001       0.962      0.853       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4     alie_nc trmean  orcinf       0.001       0.962      0.851       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4        alie trmean   elect       0.001       0.962      0.853       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4     alie_nc trmean   elect       0.001       0.963      0.855       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4        alie  mkrum    base       0.001       0.963      0.853 (reference) INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4        alie  mkrum     sra       0.001       0.962      0.849       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4     alie_nc  mkrum     sra       0.001       0.963      0.853       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4        alie  mkrum sra_l10       0.001       0.962      0.849       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4     alie_nc  mkrum sra_l10       0.001       0.963      0.853       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4        alie  mkrum  orcinf       0.001       0.963      0.853       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4     alie_nc  mkrum  orcinf       0.001       0.963      0.853       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4        alie  mkrum   elect       0.001       0.962      0.851       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4     alie_nc  mkrum   elect       0.001       0.966      0.867       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
```


## Botnet | M4 SRA W-stratum composition + clip-hit rate
```
                           nW  nW_witness  nW_liar  sra_clip_hit_rate  sra_ratio_median
arm     k f attack                                                                     
sra     2 4 alie          6.0         2.0      4.0               0.00              1.64
            alie_nc       2.0         2.0      0.0               0.30              2.55
            signflip      6.0         2.0      4.0               1.00             14.19
            signflip_nc   2.0         2.0      0.0               0.00              0.24
        6 2 alie          8.0         6.0      2.0               0.00              0.84
            alie_nc       6.0         6.0      0.0               0.00              0.98
            signflip      8.0         6.0      2.0               0.00              0.78
            signflip_nc   6.0         6.0      0.0               0.00              0.78
          4 alie         10.0         6.0      4.0               0.00              0.94
            alie_nc       6.0         6.0      0.0               0.00              1.02
            signflip     10.0         6.0      4.0               0.00              1.02
            signflip_nc   6.0         6.0      0.0               0.00              0.21
sra_l10 2 4 alie          6.0         2.0      4.0               0.00              1.64
            alie_nc       2.0         2.0      0.0               0.00              2.45
            signflip      6.0         2.0      4.0               0.86             34.66
            signflip_nc   2.0         2.0      0.0               0.00              0.24
        6 2 alie          8.0         6.0      2.0               0.00              0.84
            alie_nc       6.0         6.0      0.0               0.00              0.98
            signflip      8.0         6.0      2.0               0.00              0.78
            signflip_nc   6.0         6.0      0.0               0.00              0.78
          4 alie         10.0         6.0      4.0               0.00              0.94
            alie_nc       6.0         6.0      0.0               0.00              1.02
            signflip     10.0         6.0      4.0               0.00              1.02
            signflip_nc   6.0         6.0      0.0               0.00              0.21
```


## Botnet | M4 full per-class recall
```
                                recall_Normal  recall_DoS  recall_DDoS  recall_Portscan  recall_Brute Force  recall_Botnet  recall_Web Attack
k f attack      agg    arm                                                                                                                   
2 0 mimic       fedavg base             0.999       0.999        0.998              NaN               1.000          0.994              0.859
  4 alie        cwmed  base             0.999       0.999        0.997              NaN               1.000          0.000              0.849
                       elect            0.999       0.999        0.997              NaN               1.000          0.000              0.849
                       orcinf           0.999       0.999        0.997              NaN               1.000          0.995              0.849
                       sra              0.999       0.999        0.997              NaN               1.000          0.000              0.847
                       sra_l10          0.999       0.999        0.997              NaN               1.000          0.000              0.847
                fedavg base             0.999       0.999        0.998              NaN               1.000          0.994              0.853
                mkrum  base             0.999       0.999        0.998              NaN               1.000          0.000              0.853
                       elect            0.999       0.999        0.998              NaN               1.000          0.000              0.851
                       orcinf           0.999       0.999        0.998              NaN               1.000          0.995              0.853
                       sra              0.999       0.999        0.998              NaN               1.000          0.000              0.849
                       sra_l10          0.999       0.999        0.998              NaN               1.000          0.000              0.849
                trmean base             0.999       0.999        0.998              NaN               1.000          0.000              0.849
                       elect            0.999       0.999        0.998              NaN               1.000          0.000              0.853
                       orcinf           0.999       0.999        0.998              NaN               1.000          0.995              0.853
                       sra              0.999       0.999        0.998              NaN               1.000          0.000              0.849
                       sra_l10          0.999       0.999        0.998              NaN               1.000          0.000              0.849
    alie_nc     cwmed  elect            0.999       0.999        0.996              NaN               1.000          0.000              0.849
                       orcinf           0.999       0.999        0.997              NaN               1.000          0.994              0.849
                       sra              0.999       0.999        0.997              NaN               1.000          0.994              0.849
                       sra_l10          0.999       0.999        0.997              NaN               1.000          0.994              0.849
                mkrum  elect            0.999       0.999        0.998              NaN               1.000          0.000              0.867
                       orcinf           0.999       0.999        0.998              NaN               1.000          0.995              0.853
                       sra              0.999       0.999        0.998              NaN               1.000          0.994              0.853
                       sra_l10          0.999       0.999        0.998              NaN               1.000          0.995              0.853
                trmean elect            0.999       0.999        0.998              NaN               1.000          0.893              0.855
                       orcinf           0.999       0.999        0.998              NaN               1.000          0.994              0.851
                       sra              0.999       0.999        0.998              NaN               1.000          0.994              0.851
                       sra_l10          0.999       0.999        0.998              NaN               1.000          0.994              0.851
    signflip    cwmed  base             0.999       0.997        0.996              NaN               1.000          0.000              0.849
                       elect            0.000       0.000        0.000              NaN               0.000          1.000              0.000
                       orcinf           0.482       0.047        0.000              NaN               0.000          0.333              0.000
                       sra              0.993       0.980        0.303              NaN               0.801          0.000              0.000
                       sra_l10          0.334       0.312        0.252              NaN               0.167          0.000              0.000
                fedavg base             0.333       0.008        0.525              NaN               0.000          0.000              0.000
                mkrum  base             0.213       0.000        0.636              NaN               0.000          0.000              0.000
                       elect            0.667       0.000        0.000              NaN               0.000          0.000              0.000
                       orcinf           0.294       0.013        0.000              NaN               0.000          0.333              0.000
                       sra              0.830       0.661        0.442              NaN               0.669          0.000              0.175
                       sra_l10          1.000       0.000        0.000              NaN               0.000          0.000              0.000
                trmean base             0.398       0.000        0.001              NaN               0.000          0.333              0.000
                       elect            0.000       0.333        0.000              NaN               0.000          0.667              0.000
                       orcinf           0.344       0.333        0.580              NaN               0.000          0.000              0.000
                       sra              0.812       0.988        0.660              NaN               0.832          0.000              0.000
                       sra_l10          0.333       0.000        0.333              NaN               0.000          0.333              0.000
    signflip_nc cwmed  elect            0.999       0.997        0.995              NaN               1.000          0.000              0.849
                       orcinf           0.999       0.998        0.996              NaN               1.000          0.993              0.845
                       sra              0.999       0.998        0.996              NaN               1.000          0.993              0.845
                       sra_l10          0.999       0.998        0.996              NaN               1.000          0.993              0.845
                mkrum  elect            0.233       0.002        0.269              NaN               0.000          0.333              0.000
                       orcinf           0.174       0.332        0.000              NaN               0.333          0.000              0.000
                       sra              0.000       0.000        0.333              NaN               0.333          0.000              0.000
                       sra_l10          0.000       0.000        0.333              NaN               0.333          0.000              0.000
                trmean elect            0.639       0.333        0.001              NaN               0.000          0.000              0.000
                       orcinf           0.000       0.000        0.000              NaN               0.333          0.333              0.000
                       sra              0.000       0.000        0.000              NaN               0.333          0.333              0.000
                       sra_l10          0.000       0.000        0.000              NaN               0.333          0.333              0.000
6 0 mimic       fedavg base             0.999       0.999        0.998              NaN               1.000          0.995              0.855
  2 alie        cwmed  base             0.999       0.999        0.996              NaN               1.000          0.000              0.849
                       elect            0.999       0.999        0.996              NaN               1.000          0.995              0.851
                       orcinf           0.999       0.999        0.996              NaN               1.000          0.997              0.861
                       sra              0.999       0.999        0.996              NaN               1.000          0.996              0.853
                       sra_l10          0.999       0.999        0.996              NaN               1.000          0.996              0.853
                fedavg base             0.999       0.999        0.998              NaN               1.000          0.995              0.861
                mkrum  base             0.999       0.999        0.998              NaN               1.000          0.995              0.861
                       elect            0.999       0.999        0.998              NaN               1.000          0.995              0.861
                       orcinf           0.999       0.999        0.998              NaN               1.000          0.996              0.861
                       sra              0.999       0.999        0.997              NaN               1.000          0.995              0.861
                       sra_l10          0.999       0.999        0.997              NaN               1.000          0.995              0.861
                trmean base             0.999       0.999        0.997              NaN               1.000          0.995              0.861
                       elect            0.999       0.999        0.997              NaN               1.000          0.995              0.861
                       orcinf           0.999       0.999        0.997              NaN               1.000          0.997              0.861
                       sra              0.999       0.999        0.996              NaN               1.000          0.995              0.853
                       sra_l10          0.999       0.999        0.996              NaN               1.000          0.995              0.853
    alie_nc     cwmed  elect            0.999       0.999        0.996              NaN               1.000          0.995              0.851
                       orcinf           0.999       0.999        0.996              NaN               1.000          0.997              0.859
                       sra              0.999       0.999        0.996              NaN               1.000          0.995              0.851
                       sra_l10          0.999       0.999        0.996              NaN               1.000          0.995              0.851
                mkrum  elect            0.999       0.999        0.998              NaN               1.000          0.995              0.861
                       orcinf           0.999       0.999        0.998              NaN               1.000          0.997              0.861
                       sra              0.999       0.999        0.997              NaN               1.000          0.995              0.861
                       sra_l10          0.999       0.999        0.997              NaN               1.000          0.995              0.861
                trmean elect            0.999       0.999        0.997              NaN               1.000          0.995              0.861
                       orcinf           0.999       0.999        0.997              NaN               1.000          0.996              0.861
                       sra              0.999       0.999        0.997              NaN               1.000          0.995              0.861
                       sra_l10          0.999       0.999        0.997              NaN               1.000          0.995              0.861
    signflip    cwmed  base             0.999       0.998        0.996              NaN               1.000          0.000              0.847
                       elect            0.999       0.998        0.996              NaN               1.000          0.994              0.849
                       orcinf           0.141       0.331        0.000              NaN               0.000          0.000              0.333
                       sra              0.999       0.998        0.996              NaN               1.000          0.995              0.847
                       sra_l10          0.999       0.998        0.996              NaN               1.000          0.995              0.847
                fedavg base             0.016       0.994        0.205              NaN               0.000          0.000              0.000
                mkrum  base             0.999       0.999        0.998              NaN               1.000          0.995              0.863
                       elect            0.999       0.999        0.998              NaN               1.000          0.996              0.863
                       orcinf           0.333       0.000        0.000              NaN               0.333          0.000              0.000
                       sra              0.999       0.998        0.996              NaN               1.000          0.995              0.849
                       sra_l10          0.999       0.998        0.996              NaN               1.000          0.995              0.849
                trmean base             0.999       0.998        0.996              NaN               1.000          0.995              0.847
                       elect            0.999       0.998        0.996              NaN               1.000          0.995              0.853
                       orcinf           0.185       0.664        0.000              NaN               0.000          0.333              0.000
                       sra              0.999       0.998        0.996              NaN               1.000          0.995              0.847
                       sra_l10          0.999       0.998        0.996              NaN               1.000          0.995              0.847
    signflip_nc cwmed  elect            0.999       0.998        0.996              NaN               1.000          0.994              0.849
                       orcinf           0.999       0.998        0.996              NaN               1.000          0.996              0.847
                       sra              0.999       0.998        0.996              NaN               1.000          0.995              0.847
                       sra_l10          0.999       0.998        0.996              NaN               1.000          0.995              0.847
                mkrum  elect            0.999       0.999        0.998              NaN               1.000          0.996              0.863
                       orcinf           0.999       0.999        0.998              NaN               1.000          0.995              0.861
                       sra              0.999       0.999        0.998              NaN               1.000          0.995              0.861
                       sra_l10          0.999       0.999        0.998              NaN               1.000          0.995              0.861
                trmean elect            0.999       0.998        0.996              NaN               1.000          0.995              0.853
                       orcinf           0.999       0.999        0.996              NaN               1.000          0.996              0.851
                       sra              0.999       0.998        0.996              NaN               1.000          0.995              0.847
                       sra_l10          0.999       0.998        0.996              NaN               1.000          0.995              0.847
  4 alie        cwmed  base             0.999       0.998        0.996              NaN               1.000          0.994              0.845
                       elect            0.999       0.998        0.996              NaN               1.000          0.995              0.845
                       orcinf           0.999       0.998        0.997              NaN               1.000          0.998              0.851
                       sra              0.999       0.998        0.997              NaN               1.000          0.998              0.849
                       sra_l10          0.999       0.998        0.997              NaN               1.000          0.998              0.849
                fedavg base             0.999       0.999        0.997              NaN               1.000          0.998              0.851
                mkrum  base             0.999       0.999        0.997              NaN               1.000          0.997              0.851
                       elect            0.999       0.999        0.997              NaN               1.000          0.997              0.853
                       orcinf           0.999       0.999        0.997              NaN               1.000          0.998              0.851
                       sra              0.999       0.999        0.997              NaN               1.000          0.997              0.849
                       sra_l10          0.999       0.999        0.997              NaN               1.000          0.997              0.849
                trmean base             0.999       0.999        0.997              NaN               1.000          0.996              0.849
                       elect            0.999       0.999        0.997              NaN               1.000          0.996              0.851
                       orcinf           0.999       0.999        0.997              NaN               1.000          0.998              0.851
                       sra              0.999       0.998        0.997              NaN               1.000          0.998              0.849
                       sra_l10          0.999       0.998        0.997              NaN               1.000          0.998              0.849
    alie_nc     cwmed  elect            0.999       0.998        0.996              NaN               1.000          0.995              0.847
                       orcinf           0.999       0.998        0.997              NaN               1.000          0.998              0.849
                       sra              0.999       0.998        0.997              NaN               1.000          0.996              0.849
                       sra_l10          0.999       0.998        0.997              NaN               1.000          0.996              0.849
                mkrum  elect            0.999       0.998        0.997              NaN               1.000          0.998              0.853
                       orcinf           0.999       0.999        0.997              NaN               1.000          0.998              0.849
                       sra              0.999       0.999        0.997              NaN               1.000          0.997              0.849
                       sra_l10          0.999       0.999        0.997              NaN               1.000          0.997              0.849
                trmean elect            0.999       0.999        0.997              NaN               1.000          0.997              0.853
                       orcinf           0.999       0.999        0.997              NaN               1.000          0.998              0.851
                       sra              0.999       0.998        0.997              NaN               1.000          0.996              0.849
                       sra_l10          0.999       0.998        0.997              NaN               1.000          0.996              0.849
    signflip    cwmed  base             0.999       0.998        0.996              NaN               1.000          0.000              0.845
                       elect            0.999       0.998        0.995              NaN               1.000          0.592              0.845
                       orcinf           0.281       0.665        0.000              NaN               0.000          0.000              0.000
                       sra              0.996       0.998        0.995              NaN               1.000          0.997              0.845
                       sra_l10          0.996       0.998        0.995              NaN               1.000          0.997              0.845
                fedavg base             0.333       0.000        0.667              NaN               0.000          0.000              0.000
                mkrum  base             0.335       0.667        0.000              NaN               0.000          0.000              0.000
                       elect            0.333       0.000        0.667              NaN               0.000          0.000              0.000
                       orcinf           0.216       0.331        0.000              NaN               0.000          0.000              0.333
                       sra              0.996       0.998        0.996              NaN               1.000          0.997              0.845
                       sra_l10          0.996       0.998        0.996              NaN               1.000          0.997              0.845
                trmean base             0.667       0.330        0.000              NaN               0.000          0.000              0.000
                       elect            0.667       0.330        0.000              NaN               0.000          0.000              0.000
                       orcinf           0.667       0.000        0.000              NaN               0.333          0.000              0.000
                       sra              0.996       0.998        0.995              NaN               1.000          0.997              0.845
                       sra_l10          0.996       0.998        0.995              NaN               1.000          0.997              0.845
    signflip_nc cwmed  elect            0.999       0.998        0.996              NaN               1.000          0.601              0.845
                       orcinf           0.998       0.998        0.996              NaN               1.000          0.996              0.845
                       sra              0.998       0.998        0.996              NaN               1.000          0.996              0.845
                       sra_l10          0.998       0.998        0.996              NaN               1.000          0.996              0.845
                mkrum  elect            0.166       0.002        0.333              NaN               0.000          0.000              0.310
                       orcinf           0.026       0.000        0.000              NaN               0.000          0.333              0.032
                       sra              0.333       0.000        0.000              NaN               0.000          0.333              0.000
                       sra_l10          0.333       0.000        0.000              NaN               0.000          0.333              0.000
                trmean elect            0.651       0.009        0.260              NaN               0.000          0.000              0.000
                       orcinf           0.178       0.000        0.000              NaN               0.000          0.000              0.000
                       sra              0.333       0.333        0.000              NaN               0.000          0.000              0.000
                       sra_l10          0.333       0.333        0.000              NaN               0.000          0.000              0.000
```


## Botnet | M4 paired verdict counts (HOLDS / BREAKS) by arm and cell type
```
paired                         BREAKS  HOLDS
arm     cell                                
elect   k<=f (bounded damage)       4      8
        k>f                         1     23
orcinf  k<=f (bounded damage)       4      8
        k>f                         7     17
sra     k<=f (bounded damage)       3      9
        k>f                         2     22
sra_l10 k<=f (bounded damage)       5      7
        k>f                         2     22
```


## Botnet | M5 mean target recall under DP (DP reference FedAvg k=16: 0.995)
```
k               1     2     3    4    6    8
agg    arm                                  
cwmed  base  0.26  0.66  0.98  1.0  1.0  1.0
       sra   0.10  0.61  0.84  1.0  1.0  1.0
fedavg base  0.16  0.77  0.99  1.0  1.0  1.0
mkrum  base  0.17  0.85  0.99  1.0  1.0  1.0
       sra   0.17  0.56  0.98  1.0  1.0  1.0
trmean base  0.17  0.88  0.98  1.0  1.0  1.0
       sra   0.17  0.88  0.93  1.0  1.0  1.0
```


## Botnet | M5 k* under DP (learnable line 0.8x DP reference = 0.796)
```
 f    agg        base       sra
 0 fedavg 3 (floor 1)          
 0  cwmed   3 (tax 0) 3 (tax 0)
 0 trmean   2 (tax 0) 2 (tax 0)
 0  mkrum   2 (tax 0) 3 (tax 0)
```


## Botnet | M5 per-class recall under DP
```
             benign_fpr  other_attack_recall_mean  recall_Normal  recall_DoS  recall_DDoS  recall_Portscan  recall_Brute Force  recall_Botnet  recall_Web Attack
agg    arm                                                                                                                                                      
cwmed  base       0.005                     0.782          0.995       0.991        0.995              NaN                 1.0          0.995              0.141
       sra        0.004                     0.766          0.996       0.991        0.995              NaN                 1.0          0.995              0.077
fedavg base       0.005                     0.747          0.995       0.991        0.995              NaN                 1.0          0.995              0.000
mkrum  base       0.005                     0.746          0.995       0.990        0.995              NaN                 1.0          0.995              0.000
       sra        0.004                     0.782          0.996       0.991        0.995              NaN                 1.0          0.995              0.143
trmean base       0.005                     0.751          0.995       0.992        0.995              NaN                 1.0          0.995              0.016
       sra        0.005                     0.783          0.995       0.992        0.995              NaN                 1.0          0.995              0.145
```


## Botnet | M5 verdict
```
SRA under DP (tax vs FedAvg-DP): NO_TAX_TO_REMOVE
```
