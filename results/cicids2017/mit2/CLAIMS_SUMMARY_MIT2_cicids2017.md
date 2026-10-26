# mit-2 (SRA) summary -- CICIDS2017 (script mit-2.0)

DATASET HEADLINE: NO_SAFE_POINT_CONFIRMED

secondary (POST-HOC lambda=10): NO_SAFE_POINT_CONFIRMED


## Botnet | verdicts
```
M3_coverage_sra: REMOVES_TAX
M3_floor: ABOVE_FLOOR
M3_identity: IDENTITY_MATTERS
M3_coverage_sra_l10: REMOVES_TAX
M3_floor_l10: REACHES_FLOOR
M3_lambda_diag: LAMBDA_NOT_THE_ISSUE (lambda=10 does not beat lambda=3 by >= 2 in >= 2/3 of cells)
M3_rr_sra_rr1: FORMULA_HOLDS
M3_rr_sra_rr3: FORMULA_HOLDS
M3_cov_orcinf: REMOVES_TAX
M3_cov_elect: NO_EFFECT
M3_cov_sra_rr1: NO_EFFECT+HARM
M3_cov_sra_rr3: REDUCES_TAX
M3_cov_sra_rand: NO_EFFECT+HARM
M3_floor_flags: 0
M4_sra_k>f: 22/24 HOLDS (paired)
M4_sra_l10_k>f: 22/24 HOLDS (paired)
M4_orcinf_k>f: 16/24 HOLDS (paired)
M4_elect_k>f: 20/24 HOLDS (paired)
M4_sra_k<=f: 8/12 HOLDS (bounded-damage cell, not in headline)
M5_sra_under_dp: NO_TAX_TO_REMOVE
HEADLINE: NO_SAFE_POINT_CONFIRMED
HEADLINE_l10_posthoc: NO_SAFE_POINT_CONFIRMED
```


## Portscan | verdicts
```
M3_coverage_sra: REMOVES_TAX
M3_floor: ABOVE_FLOOR
M3_identity: IDENTITY_MATTERS
M3_coverage_sra_l10: REMOVES_TAX
M3_floor_l10: REACHES_FLOOR
M3_lambda_diag: LAMBDA_NOT_THE_ISSUE (lambda=10 does not beat lambda=3 by >= 2 in >= 2/3 of cells)
M3_rr_sra_rr1: FORMULA_HOLDS
M3_rr_sra_rr3: FORMULA_HOLDS
M3_cov_orcinf: REMOVES_TAX
M3_cov_elect: NO_EFFECT
M3_cov_sra_rr1: NO_EFFECT+HARM
M3_cov_sra_rr3: NO_EFFECT
M3_cov_sra_rand: NO_EFFECT+HARM
M3_floor_flags: 0
M4_sra_k>f: 22/24 HOLDS (paired)
M4_sra_l10_k>f: 22/24 HOLDS (paired)
M4_orcinf_k>f: 16/24 HOLDS (paired)
M4_elect_k>f: 20/24 HOLDS (paired)
M4_sra_k<=f: 7/12 HOLDS (bounded-damage cell, not in headline)
M5_sra_under_dp: NO_EFFECT
HEADLINE: NO_SAFE_POINT_CONFIRMED
HEADLINE_l10_posthoc: NO_SAFE_POINT_CONFIRMED
```


## Botnet | M3 k* by arm (robustness tax = k*(arm) - k*(FedAvg, same f)); grid k=[1, 2, 3, 4, 6, 8], 'never' = > 8
```
 f    agg          base    orcinf     elect       sra   sra_l10   sra_rr1   sra_rr3  sra_rand
 0 fedavg   1 (floor 1)                                                                      
 0  cwmed     8 (tax 7) 1 (tax 0) 6 (tax 5) 2 (tax 1) 1 (tax 0) 8 (tax 7) 3 (tax 2) 8 (tax 7)
 0 trmean     3 (tax 2) 1 (tax 0) 3 (tax 2) 2 (tax 1) 1 (tax 0) 6 (tax 5) 3 (tax 2) 3 (tax 2)
 0  mkrum     4 (tax 3) 1 (tax 0) 3 (tax 2) 2 (tax 1) 1 (tax 0) 6 (tax 5) 3 (tax 2) 4 (tax 3)
 2 fedavg   4 (floor 3)                                                                      
 2  cwmed     8 (tax 4) 4 (tax 0) 6 (tax 2) 3 (tax 0) 3 (tax 0) 8 (tax 4) 3 (tax 0) 8 (tax 4)
 2 trmean     4 (tax 0) 4 (tax 0) 4 (tax 0) 3 (tax 0) 3 (tax 0) 6 (tax 2) 3 (tax 0) 6 (tax 2)
 2  mkrum     6 (tax 2) 4 (tax 0) 4 (tax 0) 3 (tax 0) 3 (tax 0) 6 (tax 2) 3 (tax 0) 6 (tax 2)
 4 fedavg   6 (floor 5)                                                                      
 4  cwmed never (tax 3) 6 (tax 0) 8 (tax 2) 6 (tax 0) 6 (tax 0) 8 (tax 2) 6 (tax 0) 8 (tax 2)
 4 trmean     6 (tax 0) 6 (tax 0) 6 (tax 0) 6 (tax 0) 6 (tax 0) 8 (tax 2) 6 (tax 0) 8 (tax 2)
 4  mkrum     6 (tax 0) 6 (tax 0) 6 (tax 0) 6 (tax 0) 6 (tax 0) 8 (tax 2) 6 (tax 0) 8 (tax 2)
```


## Botnet | M3 full breakdown: mean target recall by (f, agg, arm) x k  (learnable line 0.752)
```
k                     1     2     3     4     6     8
f agg    arm                                         
0 cwmed  base      0.00  0.00  0.00  0.00  0.26  0.87
         elect     0.00  0.00  0.00  0.65  0.88  0.93
         orcinf    0.78  0.87  0.90  0.90  0.93  0.94
         sra       0.75  0.87  0.90  0.90  0.93  0.94
         sra_l10   0.78  0.87  0.90  0.90  0.93  0.94
         sra_rand  0.00  0.26  0.00  0.56  0.36  0.92
         sra_rr1   0.00  0.00  0.00  0.00  0.63  0.93
         sra_rr3   0.27  0.54  0.89  0.91  0.93  0.94
  fedavg base      0.77  0.87  0.89  0.90  0.93  0.94
  mkrum  base      0.00  0.00  0.36  0.86  0.92  0.93
         elect     0.00  0.00  0.84  0.91  0.93  0.94
         orcinf    0.77  0.87  0.90  0.90  0.92  0.94
         sra       0.61  0.87  0.89  0.90  0.93  0.94
         sra_l10   0.77  0.87  0.90  0.90  0.93  0.94
         sra_rand  0.00  0.23  0.47  0.82  0.91  0.94
         sra_rr1   0.00  0.00  0.00  0.00  0.91  0.93
         sra_rr3   0.27  0.43  0.87  0.91  0.92  0.94
  trmean base      0.00  0.00  0.81  0.88  0.91  0.93
         elect     0.00  0.39  0.86  0.89  0.93  0.94
         orcinf    0.77  0.87  0.90  0.90  0.93  0.94
         sra       0.67  0.87  0.89  0.90  0.92  0.94
         sra_l10   0.77  0.87  0.89  0.90  0.92  0.94
         sra_rand  0.00  0.27  0.81  0.87  0.91  0.93
         sra_rr1   0.00  0.00  0.00  0.00  0.92  0.93
         sra_rr3   0.27  0.55  0.89  0.91  0.92  0.94
2 cwmed  base      0.00  0.00  0.00  0.00  0.00  0.85
         elect     0.00  0.00  0.00  0.00  0.84  0.90
         orcinf    0.00  0.01  0.67  0.84  0.89  0.90
         sra       0.00  0.00  0.90  0.90  0.93  0.94
         sra_l10   0.00  0.00  0.90  0.90  0.93  0.94
         sra_rand  0.00  0.00  0.00  0.30  0.06  0.88
         sra_rr1   0.00  0.00  0.00  0.00  0.61  0.91
         sra_rr3   0.00  0.00  0.86  0.90  0.92  0.93
  fedavg base      0.00  0.04  0.68  0.85  0.89  0.90
  mkrum  base      0.00  0.00  0.00  0.69  0.91  0.93
         elect     0.00  0.00  0.00  0.87  0.92  0.94
         orcinf    0.00  0.02  0.70  0.84  0.89  0.90
         sra       0.00  0.00  0.90  0.90  0.93  0.94
         sra_l10   0.00  0.00  0.90  0.90  0.93  0.94
         sra_rand  0.00  0.00  0.00  0.30  0.89  0.91
         sra_rr1   0.00  0.00  0.00  0.00  0.91  0.92
         sra_rr3   0.00  0.00  0.86  0.90  0.92  0.93
  trmean base      0.00  0.00  0.12  0.83  0.90  0.92
         elect     0.00  0.00  0.44  0.86  0.90  0.92
         orcinf    0.00  0.01  0.68  0.85  0.89  0.90
         sra       0.00  0.00  0.90  0.90  0.93  0.94
         sra_l10   0.00  0.00  0.90  0.90  0.93  0.94
         sra_rand  0.00  0.00  0.12  0.36  0.88  0.91
         sra_rr1   0.00  0.00  0.00  0.00  0.90  0.92
         sra_rr3   0.00  0.00  0.86  0.90  0.92  0.93
4 cwmed  base      0.00  0.00  0.00  0.00  0.00  0.55
         elect     0.00  0.00  0.00  0.00  0.04  0.87
         orcinf    0.00  0.00  0.00  0.09  0.81  0.88
         sra       0.00  0.00  0.00  0.05  0.91  0.92
         sra_l10   0.00  0.00  0.00  0.05  0.91  0.92
         sra_rand  0.00  0.00  0.00  0.00  0.00  0.83
         sra_rr1   0.00  0.00  0.00  0.00  0.00  0.78
         sra_rr3   0.00  0.00  0.00  0.00  0.91  0.92
  fedavg base      0.00  0.00  0.00  0.08  0.82  0.88
  mkrum  base      0.00  0.00  0.00  0.00  0.87  0.89
         elect     0.00  0.00  0.00  0.00  0.87  0.89
         orcinf    0.00  0.00  0.00  0.08  0.82  0.88
         sra       0.00  0.00  0.00  0.03  0.91  0.92
         sra_l10   0.00  0.00  0.00  0.03  0.91  0.92
         sra_rand  0.00  0.00  0.00  0.00  0.56  0.87
         sra_rr1   0.00  0.00  0.00  0.00  0.00  0.88
         sra_rr3   0.00  0.00  0.00  0.00  0.91  0.92
  trmean base      0.00  0.00  0.00  0.00  0.82  0.88
         elect     0.00  0.00  0.00  0.00  0.83  0.88
         orcinf    0.00  0.00  0.00  0.09  0.81  0.88
         sra       0.00  0.00  0.00  0.03  0.91  0.92
         sra_l10   0.00  0.00  0.00  0.03  0.91  0.92
         sra_rand  0.00  0.00  0.00  0.00  0.60  0.88
         sra_rr1   0.00  0.00  0.00  0.00  0.00  0.88
         sra_rr3   0.00  0.00  0.00  0.00  0.91  0.92
```


## Botnet | M3 RR formula k*: smallest k with k p > (N-k-f)(1-p) + f   (grid-censored comparison)
```
    arm  eps_w  f    agg  predicted k*  measured k*  sra (oracle) k*  within 1  within 2
sra_rr1    1.0  0  cwmed             6            8                2      True      True
sra_rr1    1.0  0 trmean             6            6                2      True      True
sra_rr1    1.0  0  mkrum             6            6                2      True      True
sra_rr1    1.0  2  cwmed             7            8                3      True      True
sra_rr1    1.0  2 trmean             7            6                3      True      True
sra_rr1    1.0  2  mkrum             7            6                3      True      True
sra_rr1    1.0  4  cwmed             9            8                6      True      True
sra_rr1    1.0  4 trmean             9            8                6      True      True
sra_rr1    1.0  4  mkrum             9            8                6      True      True
sra_rr3    3.0  0  cwmed             1            3                2     False      True
sra_rr3    3.0  0 trmean             1            3                2     False      True
sra_rr3    3.0  0  mkrum             1            3                2     False      True
sra_rr3    3.0  2  cwmed             3            3                3      True      True
sra_rr3    3.0  2 trmean             3            3                3      True      True
sra_rr3    3.0  2  mkrum             3            3                3      True      True
sra_rr3    3.0  4  cwmed             5            6                6      True      True
sra_rr3    3.0  4 trmean             5            6                6      True      True
sra_rr3    3.0  4  mkrum             5            6                6      True      True
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
sra      0  4.00        4.00                  0.00      0.0               0.15              1.57                0.0
         2  6.00        4.00                  0.00      2.0               0.00              0.77                0.0
         4  8.00        4.00                  0.00      4.0               0.00              0.60                0.0
sra_l10  0  4.00        4.00                  0.00      0.0               0.00              1.47                0.0
         2  6.00        4.00                  0.00      2.0               0.00              0.77                0.0
         4  8.00        4.00                  0.00      4.0               0.00              0.60                0.0
sra_rand 0  4.00        1.33                  2.67      0.0               0.00              0.50                0.0
         2  6.00        1.56                  2.44      2.0               0.00              0.39                0.0
         4  8.00        1.28                  2.72      4.0               0.00              0.40                0.0
sra_rr1  0  6.28        2.39                  3.89      0.0               0.00              0.47                0.0
         2  8.33        2.67                  3.67      2.0               0.00              0.48                0.0
         4  9.39        2.72                  2.67      4.0               0.00              0.43                0.0
sra_rr3  0  4.72        3.78                  0.94      0.0               0.01              0.97                0.0
         2  6.33        3.78                  0.56      2.0               0.00              0.70                0.0
         4  8.22        3.83                  0.39      4.0               0.00              0.58                0.0
```


## Botnet | M3 per-class recall at f=0, k=6 (what else moves)
```
                 benign_fpr  other_attack_recall_mean  other_attack_recall_min  recall_Normal  recall_DoS  recall_DDoS  recall_Portscan  recall_Brute Force  recall_Botnet  recall_Web Attack
agg    arm                                                                                                                                                                                   
cwmed  base           0.001                     0.957                    0.871          0.999       0.998        0.999            0.923               0.994          0.264              0.871
       elect          0.001                     0.957                    0.871          0.999       0.998        0.999            0.925               0.994          0.879              0.871
       orcinf         0.001                     0.959                    0.871          0.999       0.998        0.999            0.934               0.994          0.927              0.871
       sra            0.001                     0.958                    0.871          0.999       0.998        0.999            0.928               0.994          0.927              0.871
       sra_l10        0.001                     0.958                    0.871          0.999       0.998        0.999            0.928               0.994          0.927              0.871
       sra_rand       0.001                     0.957                    0.871          0.999       0.998        0.999            0.923               0.994          0.362              0.871
       sra_rr1        0.001                     0.958                    0.871          0.999       0.998        0.999            0.927               0.994          0.634              0.871
       sra_rr3        0.001                     0.958                    0.871          0.999       0.998        0.999            0.927               0.994          0.925              0.871
fedavg base           0.001                     0.963                    0.882          0.999       0.998        0.999            0.943               0.995          0.926              0.882
mkrum  base           0.001                     0.965                    0.887          0.999       0.998        0.999            0.947               0.995          0.920              0.887
       elect          0.001                     0.965                    0.887          0.999       0.998        0.999            0.947               0.995          0.930              0.887
       orcinf         0.001                     0.964                    0.882          0.999       0.998        0.999            0.946               0.995          0.925              0.882
       sra            0.001                     0.964                    0.882          0.999       0.998        0.999            0.945               0.994          0.927              0.882
       sra_l10        0.001                     0.964                    0.882          0.999       0.998        0.999            0.945               0.994          0.927              0.882
       sra_rand       0.001                     0.965                    0.887          0.999       0.998        0.999            0.945               0.994          0.908              0.887
       sra_rr1        0.001                     0.964                    0.882          0.999       0.998        0.999            0.945               0.995          0.914              0.882
       sra_rr3        0.001                     0.964                    0.882          0.999       0.998        0.999            0.946               0.995          0.920              0.882
trmean base           0.001                     0.962                    0.876          0.999       0.998        0.999            0.941               0.994          0.914              0.876
       elect          0.001                     0.960                    0.871          0.999       0.998        0.999            0.938               0.994          0.928              0.871
       orcinf         0.001                     0.961                    0.871          0.999       0.998        0.999            0.943               0.994          0.926              0.871
       sra            0.001                     0.960                    0.871          0.999       0.998        0.999            0.937               0.994          0.925              0.871
       sra_l10        0.001                     0.960                    0.871          0.999       0.998        0.999            0.937               0.994          0.925              0.871
       sra_rand       0.001                     0.960                    0.871          0.999       0.998        0.999            0.937               0.994          0.909              0.871
       sra_rr1        0.001                     0.960                    0.871          0.999       0.998        0.999            0.937               0.994          0.915              0.871
       sra_rr3        0.001                     0.960                    0.871          0.999       0.998        0.999            0.937               0.994          0.922              0.871
```


## Botnet | M3 verdicts
```
COVERAGE (sra)        : REMOVES_TAX
FLOOR (sra k* <= f+1) : ABOVE_FLOOR (share 0.33)
IDENTITY (sra_rand)   : IDENTITY_MATTERS
-- post-hoc lambda diagnostic (NOT the headline) --
COVERAGE (sra_l10)    : REMOVES_TAX
FLOOR (sra_l10)       : REACHES_FLOOR (share 0.67)
LAMBDA DIAGNOSTIC     : LAMBDA_NOT_THE_ISSUE (lambda=10 does not beat lambda=3 by >= 2 in >= 2/3 of cells)
RR formula sra_rr1    : FORMULA_HOLDS
RR formula sra_rr3    : FORMULA_HOLDS
coverage orcinf       : REMOVES_TAX
coverage elect        : NO_EFFECT
coverage sra_rr1      : NO_EFFECT+HARM
coverage sra_rr3      : REDUCES_TAX
coverage sra_rand     : NO_EFFECT+HARM
floor violations      : none
worst sra cell        : cwmed f=0 k*=2 tax=1
```


## Botnet | M4 sign-flip x10 / ALIE z=1  ('_nc' = attackers do NOT claim evidence)
```
 k  f      attack    agg     arm  benign_fpr  other_mean  other_min      paired                     absolute
 6  2    signflip fedavg    base       0.154       0.066      0.000                                effective
 6  2    signflip  cwmed    base       0.001       0.957      0.871 (reference)                        HOLDS
 6  2    signflip  cwmed     sra       0.001       0.957      0.871       HOLDS                        HOLDS
 6  2 signflip_nc  cwmed     sra       0.001       0.957      0.871       HOLDS                        HOLDS
 6  2    signflip  cwmed sra_l10       0.001       0.957      0.871       HOLDS                        HOLDS
 6  2 signflip_nc  cwmed sra_l10       0.001       0.957      0.871       HOLDS                        HOLDS
 6  2    signflip  cwmed  orcinf       1.000       0.200      0.000      BREAKS                       BREAKS
 6  2 signflip_nc  cwmed  orcinf       0.001       0.958      0.871       HOLDS                        HOLDS
 6  2    signflip  cwmed   elect       0.001       0.957      0.871       HOLDS                        HOLDS
 6  2 signflip_nc  cwmed   elect       0.001       0.957      0.871       HOLDS                        HOLDS
 6  2    signflip trmean    base       0.001       0.956      0.871 (reference)                        HOLDS
 6  2    signflip trmean     sra       0.001       0.958      0.871       HOLDS                        HOLDS
 6  2 signflip_nc trmean     sra       0.001       0.957      0.871       HOLDS                        HOLDS
 6  2    signflip trmean sra_l10       0.001       0.958      0.871       HOLDS                        HOLDS
 6  2 signflip_nc trmean sra_l10       0.001       0.957      0.871       HOLDS                        HOLDS
 6  2    signflip trmean  orcinf       0.668       0.067      0.000      BREAKS                       BREAKS
 6  2 signflip_nc trmean  orcinf       0.001       0.958      0.871       HOLDS                        HOLDS
 6  2    signflip trmean   elect       0.001       0.958      0.871       HOLDS                        HOLDS
 6  2 signflip_nc trmean   elect       0.001       0.958      0.871       HOLDS                        HOLDS
 6  2    signflip  mkrum    base       0.001       0.965      0.876 (reference)                        HOLDS
 6  2    signflip  mkrum     sra       0.001       0.961      0.871       HOLDS                        HOLDS
 6  2 signflip_nc  mkrum     sra       0.001       0.964      0.871       HOLDS                        HOLDS
 6  2    signflip  mkrum sra_l10       0.001       0.961      0.871       HOLDS                        HOLDS
 6  2 signflip_nc  mkrum sra_l10       0.001       0.964      0.871       HOLDS                        HOLDS
 6  2    signflip  mkrum  orcinf       0.667       0.067      0.000      BREAKS                       BREAKS
 6  2 signflip_nc  mkrum  orcinf       0.001       0.965      0.876       HOLDS                        HOLDS
 6  2    signflip  mkrum   elect       0.001       0.964      0.876       HOLDS                        HOLDS
 6  2 signflip_nc  mkrum   elect       0.001       0.963      0.871       HOLDS                        HOLDS
 6  2        alie fedavg    base       0.001       0.964      0.876                          attack too weak
 6  2        alie  cwmed    base       0.001       0.959      0.871 (reference) INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2        alie  cwmed     sra       0.001       0.960      0.871       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2     alie_nc  cwmed     sra       0.001       0.960      0.871       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2        alie  cwmed sra_l10       0.001       0.960      0.871       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2     alie_nc  cwmed sra_l10       0.001       0.960      0.871       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2        alie  cwmed  orcinf       0.001       0.961      0.871       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2     alie_nc  cwmed  orcinf       0.001       0.961      0.871       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2        alie  cwmed   elect       0.001       0.959      0.871       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2     alie_nc  cwmed   elect       0.001       0.959      0.871       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2        alie trmean    base       0.001       0.962      0.871 (reference) INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2        alie trmean     sra       0.001       0.961      0.871       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2     alie_nc trmean     sra       0.001       0.962      0.871       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2        alie trmean sra_l10       0.001       0.961      0.871       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2     alie_nc trmean sra_l10       0.001       0.962      0.871       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2        alie trmean  orcinf       0.001       0.962      0.871       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2     alie_nc trmean  orcinf       0.001       0.962      0.871       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2        alie trmean   elect       0.001       0.962      0.871       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2     alie_nc trmean   elect       0.001       0.962      0.871       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2        alie  mkrum    base       0.001       0.963      0.871 (reference) INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2        alie  mkrum     sra       0.001       0.963      0.871       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2     alie_nc  mkrum     sra       0.001       0.963      0.871       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2        alie  mkrum sra_l10       0.001       0.963      0.871       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2     alie_nc  mkrum sra_l10       0.001       0.963      0.871       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2        alie  mkrum  orcinf       0.001       0.963      0.871       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2     alie_nc  mkrum  orcinf       0.001       0.963      0.871       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2        alie  mkrum   elect       0.001       0.963      0.871       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2     alie_nc  mkrum   elect       0.001       0.963      0.871       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4    signflip fedavg    base       0.667       0.133      0.000                                effective
 6  4    signflip  cwmed    base       0.001       0.954      0.871 (reference)                        HOLDS
 6  4    signflip  cwmed     sra       0.004       0.951      0.871       HOLDS                        HOLDS
 6  4 signflip_nc  cwmed     sra       0.002       0.953      0.871       HOLDS                        HOLDS
 6  4    signflip  cwmed sra_l10       0.004       0.951      0.871       HOLDS                        HOLDS
 6  4 signflip_nc  cwmed sra_l10       0.002       0.953      0.871       HOLDS                        HOLDS
 6  4    signflip  cwmed  orcinf       0.189       0.042      0.000      BREAKS                       BREAKS
 6  4 signflip_nc  cwmed  orcinf       0.002       0.953      0.871       HOLDS                        HOLDS
 6  4    signflip  cwmed   elect       0.001       0.955      0.871       HOLDS                        HOLDS
 6  4 signflip_nc  cwmed   elect       0.001       0.953      0.871       HOLDS                        HOLDS
 6  4    signflip trmean    base       0.124       0.000      0.000 (reference)                       BREAKS
 6  4    signflip trmean     sra       0.003       0.951      0.871       HOLDS                        HOLDS
 6  4 signflip_nc trmean     sra       0.667       0.067      0.000      BREAKS                       BREAKS
 6  4    signflip trmean sra_l10       0.003       0.951      0.871       HOLDS                        HOLDS
 6  4 signflip_nc trmean sra_l10       0.667       0.067      0.000      BREAKS                       BREAKS
 6  4    signflip trmean  orcinf       0.531       0.069      0.000      BREAKS                       BREAKS
 6  4 signflip_nc trmean  orcinf       1.000       0.258      0.000      BREAKS                       BREAKS
 6  4    signflip trmean   elect       0.452       0.067      0.000      BREAKS                       BREAKS
 6  4 signflip_nc trmean   elect       0.215       0.001      0.000      BREAKS                       BREAKS
 6  4    signflip  mkrum    base       0.538       0.067      0.000 (reference)                       BREAKS
 6  4    signflip  mkrum     sra       0.003       0.953      0.871       HOLDS                        HOLDS
 6  4 signflip_nc  mkrum     sra       0.667       0.067      0.000      BREAKS                       BREAKS
 6  4    signflip  mkrum sra_l10       0.003       0.953      0.871       HOLDS                        HOLDS
 6  4 signflip_nc  mkrum sra_l10       0.667       0.067      0.000      BREAKS                       BREAKS
 6  4    signflip  mkrum  orcinf       0.669       0.134      0.000      BREAKS                       BREAKS
 6  4 signflip_nc  mkrum  orcinf       0.667       0.133      0.000      BREAKS                       BREAKS
 6  4    signflip  mkrum   elect       0.432       0.000      0.000      BREAKS                       BREAKS
 6  4 signflip_nc  mkrum   elect       0.860       0.194      0.000      BREAKS                       BREAKS
 6  4        alie fedavg    base       0.001       0.960      0.871                          attack too weak
 6  4        alie  cwmed    base       0.001       0.958      0.871 (reference) INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4        alie  cwmed     sra       0.001       0.958      0.871       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4     alie_nc  cwmed     sra       0.001       0.959      0.871       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4        alie  cwmed sra_l10       0.001       0.958      0.871       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4     alie_nc  cwmed sra_l10       0.001       0.959      0.871       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4        alie  cwmed  orcinf       0.001       0.959      0.871       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4     alie_nc  cwmed  orcinf       0.001       0.959      0.871       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4        alie  cwmed   elect       0.001       0.957      0.871       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4     alie_nc  cwmed   elect       0.001       0.957      0.871       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4        alie trmean    base       0.001       0.959      0.871 (reference) INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4        alie trmean     sra       0.001       0.958      0.871       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4     alie_nc trmean     sra       0.001       0.959      0.871       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4        alie trmean sra_l10       0.001       0.958      0.871       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4     alie_nc trmean sra_l10       0.001       0.959      0.871       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4        alie trmean  orcinf       0.001       0.959      0.871       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4     alie_nc trmean  orcinf       0.001       0.959      0.871       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4        alie trmean   elect       0.001       0.959      0.871       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4     alie_nc trmean   elect       0.001       0.959      0.871       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4        alie  mkrum    base       0.001       0.960      0.871 (reference) INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4        alie  mkrum     sra       0.001       0.959      0.871       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4     alie_nc  mkrum     sra       0.001       0.959      0.871       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4        alie  mkrum sra_l10       0.001       0.959      0.871       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4     alie_nc  mkrum sra_l10       0.001       0.959      0.871       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4        alie  mkrum  orcinf       0.001       0.960      0.871       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4     alie_nc  mkrum  orcinf       0.001       0.960      0.871       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4        alie  mkrum   elect       0.001       0.961      0.871       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4     alie_nc  mkrum   elect       0.001       0.961      0.871       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4    signflip fedavg    base       0.124       0.067      0.000                                effective
 2  4    signflip  cwmed    base       0.001       0.957      0.871 (reference)                        HOLDS
 2  4    signflip  cwmed     sra       0.333       0.070      0.000      BREAKS                       BREAKS
 2  4 signflip_nc  cwmed     sra       0.001       0.952      0.871       HOLDS                        HOLDS
 2  4    signflip  cwmed sra_l10       0.667       0.133      0.000      BREAKS                       BREAKS
 2  4 signflip_nc  cwmed sra_l10       0.001       0.952      0.871       HOLDS                        HOLDS
 2  4    signflip  cwmed  orcinf       0.469       0.055      0.000      BREAKS                       BREAKS
 2  4 signflip_nc  cwmed  orcinf       0.001       0.952      0.871       HOLDS                        HOLDS
 2  4    signflip  cwmed   elect       1.000       0.000      0.000      BREAKS                       BREAKS
 2  4 signflip_nc  cwmed   elect       0.001       0.956      0.871       HOLDS                        HOLDS
 2  4    signflip trmean    base       0.464       0.070      0.000 (reference)                       BREAKS
 2  4    signflip trmean     sra       0.333       0.067      0.000       HOLDS                       BREAKS
 2  4 signflip_nc trmean     sra       0.910       0.161      0.000      BREAKS                       BREAKS
 2  4    signflip trmean sra_l10       0.195       0.000      0.000      BREAKS                       BREAKS
 2  4 signflip_nc trmean sra_l10       0.910       0.161      0.000      BREAKS                       BREAKS
 2  4    signflip trmean  orcinf       0.669       0.195      0.000      BREAKS                       BREAKS
 2  4 signflip_nc trmean  orcinf       0.431       0.096      0.000       HOLDS                       BREAKS
 2  4    signflip trmean   elect       1.000       0.006      0.000      BREAKS                       BREAKS
 2  4 signflip_nc trmean   elect       0.116       0.066      0.000       HOLDS                       BREAKS
 2  4    signflip  mkrum    base       0.538       0.067      0.000 (reference)                       BREAKS
 2  4    signflip  mkrum     sra       0.000       0.000      0.000      BREAKS                       BREAKS
 2  4 signflip_nc  mkrum     sra       0.667       0.067      0.000      BREAKS                       BREAKS
 2  4    signflip  mkrum sra_l10       0.000       0.000      0.000      BREAKS                       BREAKS
 2  4 signflip_nc  mkrum sra_l10       0.667       0.067      0.000      BREAKS                       BREAKS
 2  4    signflip  mkrum  orcinf       0.532       0.067      0.000       HOLDS                       BREAKS
 2  4 signflip_nc  mkrum  orcinf       0.787       0.199      0.000      BREAKS                       BREAKS
 2  4    signflip  mkrum   elect       0.667       0.000      0.000      BREAKS                       BREAKS
 2  4 signflip_nc  mkrum   elect       0.333       0.067      0.000       HOLDS                       BREAKS
 2  4        alie fedavg    base       0.001       0.962      0.871                          attack too weak
 2  4        alie  cwmed    base       0.001       0.957      0.871 (reference) INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4        alie  cwmed     sra       0.001       0.956      0.871       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4     alie_nc  cwmed     sra       0.001       0.958      0.871       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4        alie  cwmed sra_l10       0.001       0.956      0.871       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4     alie_nc  cwmed sra_l10       0.001       0.958      0.871       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4        alie  cwmed  orcinf       0.001       0.959      0.871       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4     alie_nc  cwmed  orcinf       0.001       0.958      0.871       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4        alie  cwmed   elect       0.001       0.957      0.871       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4     alie_nc  cwmed   elect       0.001       0.957      0.871       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4        alie trmean    base       0.001       0.960      0.871 (reference) INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4        alie trmean     sra       0.001       0.958      0.871       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4     alie_nc trmean     sra       0.001       0.960      0.871       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4        alie trmean sra_l10       0.001       0.958      0.871       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4     alie_nc trmean sra_l10       0.001       0.960      0.871       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4        alie trmean  orcinf       0.001       0.961      0.871       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4     alie_nc trmean  orcinf       0.001       0.960      0.871       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4        alie trmean   elect       0.001       0.959      0.871       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4     alie_nc trmean   elect       0.001       0.959      0.871       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4        alie  mkrum    base       0.001       0.960      0.871 (reference) INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4        alie  mkrum     sra       0.001       0.960      0.871       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4     alie_nc  mkrum     sra       0.001       0.961      0.871       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4        alie  mkrum sra_l10       0.001       0.960      0.871       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4     alie_nc  mkrum sra_l10       0.001       0.961      0.871       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4        alie  mkrum  orcinf       0.001       0.961      0.871       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4     alie_nc  mkrum  orcinf       0.001       0.961      0.871       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4        alie  mkrum   elect       0.001       0.960      0.871       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4     alie_nc  mkrum   elect       0.001       0.961      0.871       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
```


## Botnet | M4 SRA W-stratum composition + clip-hit rate
```
                           nW  nW_witness  nW_liar  sra_clip_hit_rate  sra_ratio_median
arm     k f attack                                                                     
sra     2 4 alie          6.0         2.0      4.0               0.00              1.44
            alie_nc       2.0         2.0      0.0               0.10              1.89
            signflip      6.0         2.0      4.0               0.94             15.10
            signflip_nc   2.0         2.0      0.0               0.00              0.28
        6 2 alie          8.0         6.0      2.0               0.00              0.80
            alie_nc       6.0         6.0      0.0               0.00              0.85
            signflip      8.0         6.0      2.0               0.00              0.84
            signflip_nc   6.0         6.0      0.0               0.00              0.67
          4 alie         10.0         6.0      4.0               0.00              1.03
            alie_nc       6.0         6.0      0.0               0.00              0.95
            signflip     10.0         6.0      4.0               0.00              1.27
            signflip_nc   6.0         6.0      0.0               0.00              0.24
sra_l10 2 4 alie          6.0         2.0      4.0               0.00              1.44
            alie_nc       2.0         2.0      0.0               0.00              1.88
            signflip      6.0         2.0      4.0               0.91             29.63
            signflip_nc   2.0         2.0      0.0               0.00              0.28
        6 2 alie          8.0         6.0      2.0               0.00              0.80
            alie_nc       6.0         6.0      0.0               0.00              0.85
            signflip      8.0         6.0      2.0               0.00              0.84
            signflip_nc   6.0         6.0      0.0               0.00              0.67
          4 alie         10.0         6.0      4.0               0.00              1.03
            alie_nc       6.0         6.0      0.0               0.00              0.95
            signflip     10.0         6.0      4.0               0.00              1.27
            signflip_nc   6.0         6.0      0.0               0.00              0.24
```


## Botnet | M4 full per-class recall
```
                                recall_Normal  recall_DoS  recall_DDoS  recall_Portscan  recall_Brute Force  recall_Botnet  recall_Web Attack
k f attack      agg    arm                                                                                                                   
2 0 mimic       fedavg base             0.999       0.998        0.999            0.946               0.994          0.870              0.876
  4 alie        cwmed  base             0.999       0.998        0.999            0.924               0.994          0.000              0.871
                       elect            0.999       0.998        0.999            0.922               0.994          0.000              0.871
                       orcinf           0.999       0.998        0.999            0.932               0.994          0.898              0.871
                       sra              0.999       0.998        0.999            0.922               0.992          0.000              0.871
                       sra_l10          0.999       0.998        0.999            0.922               0.992          0.000              0.871
                fedavg base             0.999       0.998        0.999            0.947               0.995          0.896              0.871
                mkrum  base             0.999       0.998        0.999            0.939               0.995          0.000              0.871
                       elect            0.999       0.998        0.999            0.939               0.994          0.000              0.871
                       orcinf           0.999       0.998        0.999            0.944               0.995          0.896              0.871
                       sra              0.999       0.998        0.999            0.937               0.993          0.000              0.871
                       sra_l10          0.999       0.998        0.999            0.937               0.993          0.000              0.871
                trmean base             0.999       0.998        0.999            0.937               0.994          0.000              0.871
                       elect            0.999       0.998        0.999            0.933               0.994          0.000              0.871
                       orcinf           0.999       0.998        0.999            0.941               0.995          0.898              0.871
                       sra              0.999       0.998        0.999            0.929               0.993          0.000              0.871
                       sra_l10          0.999       0.998        0.999            0.929               0.993          0.000              0.871
    alie_nc     cwmed  elect            0.999       0.998        0.999            0.924               0.994          0.199              0.871
                       orcinf           0.999       0.998        0.999            0.927               0.994          0.893              0.871
                       sra              0.999       0.998        0.999            0.927               0.994          0.893              0.871
                       sra_l10          0.999       0.998        0.999            0.927               0.994          0.893              0.871
                mkrum  elect            0.999       0.998        0.999            0.943               0.995          0.409              0.871
                       orcinf           0.999       0.998        0.999            0.944               0.995          0.898              0.871
                       sra              0.999       0.998        0.999            0.944               0.995          0.896              0.871
                       sra_l10          0.999       0.998        0.999            0.944               0.995          0.896              0.871
                trmean elect            0.999       0.998        0.999            0.934               0.994          0.726              0.871
                       orcinf           0.999       0.998        0.999            0.937               0.994          0.898              0.871
                       sra              0.999       0.998        0.999            0.937               0.994          0.898              0.871
                       sra_l10          0.999       0.998        0.999            0.937               0.994          0.897              0.871
    signflip    cwmed  base             0.999       0.997        0.999            0.922               0.993          0.000              0.871
                       elect            0.000       0.000        0.000            0.000               0.000          1.000              0.000
                       orcinf           0.531       0.005        0.271            0.000               0.000          0.114              0.000
                       sra              0.667       0.351        0.000            0.000               0.000          0.000              0.000
                       sra_l10          0.333       0.667        0.000            0.000               0.000          0.000              0.000
                fedavg base             0.876       0.000        0.000            0.000               0.333          0.000              0.000
                mkrum  base             0.462       0.337        0.000            0.000               0.000          0.000              0.000
                       elect            0.333       0.000        0.000            0.000               0.000          0.667              0.000
                       orcinf           0.468       0.001        0.333            0.000               0.000          0.000              0.000
                       sra              1.000       0.000        0.000            0.000               0.000          0.000              0.000
                       sra_l10          1.000       0.000        0.000            0.000               0.000          0.000              0.000
                trmean base             0.536       0.000        0.000            0.350               0.000          0.000              0.000
                       elect            0.000       0.000        0.000            0.030               0.000          0.667              0.000
                       orcinf           0.331       0.001        0.333            0.309               0.000          0.000              0.333
                       sra              0.667       0.333        0.000            0.000               0.000          0.000              0.000
                       sra_l10          0.805       0.000        0.000            0.000               0.000          0.000              0.000
    signflip_nc cwmed  elect            0.999       0.998        0.999            0.920               0.993          0.000              0.871
                       orcinf           0.999       0.996        0.999            0.901               0.993          0.786              0.871
                       sra              0.999       0.996        0.999            0.901               0.993          0.784              0.871
                       sra_l10          0.999       0.996        0.999            0.901               0.993          0.784              0.871
                mkrum  elect            0.667       0.333        0.000            0.000               0.000          0.000              0.000
                       orcinf           0.213       0.997        0.000            0.000               0.000          0.000              0.000
                       sra              0.333       0.333        0.000            0.000               0.000          0.333              0.000
                       sra_l10          0.333       0.333        0.000            0.000               0.000          0.333              0.000
                trmean elect            0.884       0.329        0.000            0.000               0.000          0.000              0.000
                       orcinf           0.569       0.333        0.000            0.000               0.145          0.000              0.000
                       sra              0.090       0.333        0.000            0.000               0.474          0.000              0.000
                       sra_l10          0.090       0.333        0.000            0.000               0.474          0.000              0.000
6 0 mimic       fedavg base             0.999       0.998        0.999            0.943               0.995          0.926              0.882
  2 alie        cwmed  base             0.999       0.998        0.999            0.931               0.994          0.792              0.871
                       elect            0.999       0.998        0.999            0.934               0.994          0.892              0.871
                       orcinf           0.999       0.998        0.999            0.944               0.994          0.927              0.871
                       sra              0.999       0.998        0.999            0.940               0.994          0.935              0.871
                       sra_l10          0.999       0.998        0.999            0.940               0.994          0.935              0.871
                fedavg base             0.999       0.998        0.999            0.952               0.995          0.929              0.876
                mkrum  base             0.999       0.998        0.999            0.950               0.995          0.924              0.871
                       elect            0.999       0.998        0.999            0.953               0.995          0.935              0.871
                       orcinf           0.999       0.998        0.999            0.950               0.995          0.927              0.871
                       sra              0.999       0.998        0.999            0.950               0.995          0.937              0.871
                       sra_l10          0.999       0.998        0.999            0.950               0.995          0.937              0.871
                trmean base             0.999       0.998        0.999            0.947               0.995          0.922              0.871
                       elect            0.999       0.998        0.999            0.949               0.995          0.933              0.871
                       orcinf           0.999       0.998        0.999            0.948               0.995          0.927              0.871
                       sra              0.999       0.998        0.999            0.943               0.994          0.936              0.871
                       sra_l10          0.999       0.998        0.999            0.943               0.994          0.936              0.871
    alie_nc     cwmed  elect            0.999       0.998        0.999            0.933               0.993          0.889              0.871
                       orcinf           0.999       0.998        0.999            0.940               0.994          0.922              0.871
                       sra              0.999       0.998        0.999            0.938               0.994          0.921              0.871
                       sra_l10          0.999       0.998        0.999            0.938               0.994          0.921              0.871
                mkrum  elect            0.999       0.998        0.999            0.952               0.995          0.935              0.871
                       orcinf           0.999       0.998        0.999            0.950               0.995          0.927              0.871
                       sra              0.999       0.998        0.999            0.949               0.995          0.927              0.871
                       sra_l10          0.999       0.998        0.999            0.949               0.995          0.927              0.871
                trmean elect            0.999       0.998        0.999            0.948               0.995          0.933              0.871
                       orcinf           0.999       0.998        0.999            0.946               0.995          0.925              0.871
                       sra              0.999       0.998        0.999            0.946               0.995          0.925              0.871
                       sra_l10          0.999       0.998        0.999            0.946               0.995          0.925              0.871
    signflip    cwmed  base             0.999       0.997        0.999            0.922               0.993          0.000              0.871
                       elect            0.999       0.998        0.999            0.925               0.992          0.867              0.871
                       orcinf           0.000       0.333        0.000            0.333               0.000          0.000              0.333
                       sra              0.999       0.998        0.999            0.922               0.993          0.930              0.871
                       sra_l10          0.999       0.998        0.999            0.922               0.993          0.930              0.871
                fedavg base             0.846       0.332        0.000            0.000               0.000          0.000              0.000
                mkrum  base             0.999       0.998        0.999            0.955               0.995          0.926              0.876
                       elect            0.999       0.997        0.999            0.951               0.994          0.936              0.876
                       orcinf           0.333       0.000        0.000            0.000               0.000          0.333              0.333
                       sra              0.999       0.998        0.999            0.943               0.994          0.938              0.871
                       sra_l10          0.999       0.998        0.999            0.943               0.994          0.938              0.871
                trmean base             0.999       0.998        0.999            0.921               0.993          0.887              0.871
                       elect            0.999       0.998        0.999            0.927               0.994          0.920              0.871
                       orcinf           0.332       0.333        0.000            0.000               0.000          0.333              0.000
                       sra              0.999       0.998        0.999            0.926               0.994          0.930              0.871
                       sra_l10          0.999       0.998        0.999            0.926               0.994          0.930              0.871
    signflip_nc cwmed  elect            0.999       0.998        0.999            0.923               0.992          0.865              0.871
                       orcinf           0.999       0.998        0.999            0.927               0.994          0.908              0.871
                       sra              0.999       0.998        0.999            0.922               0.994          0.907              0.871
                       sra_l10          0.999       0.998        0.999            0.922               0.994          0.907              0.871
                mkrum  elect            0.999       0.997        0.999            0.952               0.995          0.936              0.871
                       orcinf           0.999       0.998        0.999            0.956               0.995          0.916              0.876
                       sra              0.999       0.998        0.999            0.957               0.994          0.917              0.871
                       sra_l10          0.999       0.998        0.999            0.957               0.994          0.917              0.871
                trmean elect            0.999       0.998        0.999            0.926               0.994          0.919              0.871
                       orcinf           0.999       0.998        0.999            0.929               0.994          0.901              0.871
                       sra              0.999       0.998        0.999            0.926               0.993          0.901              0.871
                       sra_l10          0.999       0.998        0.999            0.926               0.993          0.901              0.871
  4 alie        cwmed  base             0.999       0.998        0.999            0.925               0.994          0.872              0.871
                       elect            0.999       0.998        0.999            0.924               0.994          0.923              0.871
                       orcinf           0.999       0.998        0.999            0.934               0.994          0.936              0.871
                       sra              0.999       0.998        0.999            0.927               0.994          0.942              0.871
                       sra_l10          0.999       0.998        0.999            0.927               0.994          0.942              0.871
                fedavg base             0.999       0.998        0.999            0.939               0.994          0.937              0.871
                mkrum  base             0.999       0.998        0.999            0.938               0.994          0.931              0.871
                       elect            0.999       0.998        0.999            0.941               0.995          0.936              0.871
                       orcinf           0.999       0.998        0.999            0.939               0.994          0.937              0.871
                       sra              0.999       0.998        0.999            0.934               0.994          0.942              0.871
                       sra_l10          0.999       0.998        0.999            0.934               0.994          0.942              0.871
                trmean base             0.999       0.998        0.999            0.932               0.994          0.930              0.871
                       elect            0.999       0.998        0.999            0.932               0.994          0.937              0.871
                       orcinf           0.999       0.998        0.999            0.935               0.994          0.936              0.871
                       sra              0.999       0.998        0.999            0.928               0.994          0.942              0.871
                       sra_l10          0.999       0.998        0.999            0.928               0.994          0.942              0.871
    alie_nc     cwmed  elect            0.999       0.998        0.999            0.925               0.994          0.918              0.871
                       orcinf           0.999       0.998        0.999            0.933               0.994          0.926              0.871
                       sra              0.999       0.998        0.999            0.931               0.994          0.926              0.871
                       sra_l10          0.999       0.998        0.999            0.931               0.994          0.926              0.871
                mkrum  elect            0.999       0.998        0.999            0.941               0.995          0.933              0.871
                       orcinf           0.999       0.998        0.999            0.935               0.994          0.939              0.871
                       sra              0.999       0.998        0.999            0.934               0.994          0.939              0.871
                       sra_l10          0.999       0.998        0.999            0.934               0.994          0.939              0.871
                trmean elect            0.999       0.998        0.999            0.934               0.994          0.934              0.871
                       orcinf           0.999       0.998        0.999            0.933               0.994          0.936              0.871
                       sra              0.999       0.998        0.999            0.932               0.994          0.936              0.871
                       sra_l10          0.999       0.998        0.999            0.932               0.994          0.936              0.871
    signflip    cwmed  base             0.999       0.997        0.999            0.910               0.993          0.000              0.871
                       elect            0.999       0.998        0.999            0.917               0.992          0.531              0.871
                       orcinf           0.811       0.211        0.000            0.000               0.000          0.047              0.000
                       sra              0.996       0.994        0.999            0.896               0.993          0.945              0.871
                       sra_l10          0.996       0.994        0.999            0.896               0.993          0.945              0.871
                fedavg base             0.333       0.000        0.334            0.000               0.333          0.000              0.000
                mkrum  base             0.462       0.333        0.000            0.000               0.000          0.000              0.000
                       elect            0.568       0.001        0.000            0.000               0.000          0.333              0.000
                       orcinf           0.331       0.671        0.000            0.000               0.000          0.000              0.000
                       sra              0.997       0.996        0.999            0.908               0.993          0.944              0.871
                       sra_l10          0.997       0.996        0.999            0.908               0.993          0.944              0.871
                trmean base             0.876       0.000        0.000            0.000               0.000          0.333              0.000
                       elect            0.548       0.336        0.000            0.000               0.000          0.000              0.000
                       orcinf           0.469       0.330        0.000            0.017               0.000          0.298              0.000
                       sra              0.997       0.993        0.999            0.900               0.993          0.946              0.871
                       sra_l10          0.997       0.993        0.999            0.900               0.993          0.946              0.871
    signflip_nc cwmed  elect            0.999       0.998        0.999            0.907               0.991          0.411              0.871
                       orcinf           0.998       0.996        0.999            0.907               0.993          0.892              0.871
                       sra              0.998       0.996        0.999            0.904               0.993          0.889              0.871
                       sra_l10          0.998       0.996        0.999            0.904               0.993          0.889              0.871
                mkrum  elect            0.140       0.003        0.333            0.635               0.000          0.000              0.000
                       orcinf           0.333       0.000        0.000            0.000               0.000          0.000              0.667
                       sra              0.333       0.000        0.000            0.000               0.000          0.333              0.333
                       sra_l10          0.333       0.000        0.000            0.000               0.000          0.333              0.333
                trmean elect            0.785       0.003        0.000            0.000               0.001          0.000              0.000
                       orcinf           0.000       0.333        0.667            0.292               0.000          0.000              0.000
                       sra              0.333       0.000        0.333            0.000               0.000          0.333              0.000
                       sra_l10          0.333       0.000        0.333            0.000               0.000          0.333              0.000
```


## Botnet | M4 paired verdict counts (HOLDS / BREAKS) by arm and cell type
```
paired                         BREAKS  HOLDS
arm     cell                                
elect   k<=f (bounded damage)       3      9
        k>f                         4     20
orcinf  k<=f (bounded damage)       3      9
        k>f                         8     16
sra     k<=f (bounded damage)       4      8
        k>f                         2     22
sra_l10 k<=f (bounded damage)       5      7
        k>f                         2     22
```


## Botnet | M5 mean target recall under DP (DP reference FedAvg k=16: 0.885)
```
k               1     2     3     4     6     8
agg    arm                                     
cwmed  base  0.07  0.59  0.78  0.84  0.87  0.87
       sra   0.00  0.48  0.71  0.84  0.88  0.86
fedavg base  0.01  0.39  0.65  0.78  0.87  0.88
mkrum  base  0.03  0.31  0.79  0.84  0.91  0.89
       sra   0.09  0.17  0.66  0.88  0.87  0.87
trmean base  0.01  0.47  0.79  0.87  0.89  0.89
       sra   0.01  0.47  0.67  0.86  0.89  0.87
```


## Botnet | M5 k* under DP (learnable line 0.8x DP reference = 0.708)
```
 f    agg        base       sra
 0 fedavg 4 (floor 1)          
 0  cwmed   3 (tax 0) 3 (tax 0)
 0 trmean   3 (tax 0) 4 (tax 0)
 0  mkrum   3 (tax 0) 4 (tax 0)
```


## Botnet | M5 per-class recall under DP
```
             benign_fpr  other_attack_recall_mean  recall_Normal  recall_DoS  recall_DDoS  recall_Portscan  recall_Brute Force  recall_Botnet  recall_Web Attack
agg    arm                                                                                                                                                      
cwmed  base       0.009                     0.935          0.991       0.985        0.999            0.893               0.993          0.870              0.806
       sra        0.010                     0.938          0.990       0.983        0.999            0.894               0.993          0.879              0.823
fedavg base       0.008                     0.948          0.992       0.986        0.999            0.898               0.993          0.865              0.866
mkrum  base       0.008                     0.944          0.992       0.988        0.999            0.894               0.993          0.906              0.844
       sra        0.009                     0.950          0.991       0.985        0.999            0.900               0.992          0.869              0.871
trmean base       0.008                     0.947          0.992       0.985        0.999            0.897               0.993          0.886              0.860
       sra        0.009                     0.947          0.991       0.984        0.999            0.901               0.993          0.888              0.860
```


## Botnet | M5 verdict
```
SRA under DP (tax vs FedAvg-DP): NO_TAX_TO_REMOVE
```


## Portscan | M3 k* by arm (robustness tax = k*(arm) - k*(FedAvg, same f)); grid k=[1, 2, 3, 4, 6, 8], 'never' = > 8
```
 f    agg          base    orcinf     elect       sra   sra_l10       sra_rr1   sra_rr3      sra_rand
 0 fedavg   1 (floor 1)                                                                              
 0  cwmed     8 (tax 7) 1 (tax 0) 6 (tax 5) 1 (tax 0) 1 (tax 0)     8 (tax 7) 3 (tax 2)     8 (tax 7)
 0 trmean     3 (tax 2) 1 (tax 0) 3 (tax 2) 1 (tax 0) 1 (tax 0)     6 (tax 5) 3 (tax 2)     4 (tax 3)
 0  mkrum     4 (tax 3) 1 (tax 0) 3 (tax 2) 2 (tax 1) 1 (tax 0)     6 (tax 5) 3 (tax 2)     6 (tax 5)
 2 fedavg   6 (floor 3)                                                                              
 2  cwmed     8 (tax 2) 6 (tax 0) 8 (tax 2) 3 (tax 0) 3 (tax 0)     8 (tax 2) 3 (tax 0)     8 (tax 2)
 2 trmean     6 (tax 0) 6 (tax 0) 6 (tax 0) 3 (tax 0) 3 (tax 0)     6 (tax 0) 3 (tax 0)     6 (tax 0)
 2  mkrum     6 (tax 0) 6 (tax 0) 4 (tax 0) 3 (tax 0) 3 (tax 0)     8 (tax 2) 3 (tax 0)     6 (tax 0)
 4 fedavg   8 (floor 5)                                                                              
 4  cwmed never (tax 1) 8 (tax 0) 8 (tax 0) 6 (tax 0) 6 (tax 0)     8 (tax 0) 6 (tax 0) never (tax 1)
 4 trmean     8 (tax 0) 8 (tax 0) 8 (tax 0) 6 (tax 0) 6 (tax 0)     8 (tax 0) 6 (tax 0)     6 (tax 0)
 4  mkrum     6 (tax 0) 8 (tax 0) 6 (tax 0) 6 (tax 0) 6 (tax 0) never (tax 1) 6 (tax 0) never (tax 1)
```


## Portscan | M3 full breakdown: mean target recall by (f, agg, arm) x k  (learnable line 0.727)
```
k                     1     2     3     4     6     8
f agg    arm                                         
0 cwmed  base      0.00  0.00  0.00  0.00  0.51  0.88
         elect     0.00  0.00  0.00  0.00  0.75  0.88
         orcinf    0.87  0.90  0.91  0.91  0.91  0.91
         sra       0.85  0.90  0.91  0.91  0.91  0.91
         sra_l10   0.87  0.90  0.91  0.91  0.91  0.91
         sra_rand  0.27  0.00  0.00  0.00  0.71  0.89
         sra_rr1   0.00  0.00  0.00  0.00  0.70  0.89
         sra_rr3   0.29  0.60  0.90  0.90  0.91  0.90
  fedavg base      0.86  0.89  0.88  0.90  0.91  0.91
  mkrum  base      0.00  0.00  0.58  0.78  0.89  0.90
         elect     0.00  0.00  0.74  0.75  0.89  0.92
         orcinf    0.86  0.88  0.90  0.90  0.91  0.91
         sra       0.64  0.88  0.90  0.90  0.90  0.90
         sra_l10   0.86  0.88  0.90  0.90  0.90  0.90
         sra_rand  0.20  0.00  0.45  0.58  0.88  0.89
         sra_rr1   0.00  0.00  0.00  0.12  0.88  0.89
         sra_rr3   0.28  0.58  0.90  0.89  0.90  0.89
  trmean base      0.00  0.00  0.76  0.83  0.90  0.90
         elect     0.00  0.00  0.76  0.82  0.90  0.91
         orcinf    0.87  0.89  0.90  0.91  0.91  0.91
         sra       0.77  0.89  0.90  0.91  0.91  0.90
         sra_l10   0.87  0.89  0.90  0.90  0.91  0.90
         sra_rand  0.22  0.00  0.51  0.83  0.89  0.89
         sra_rr1   0.00  0.00  0.00  0.27  0.90  0.89
         sra_rr3   0.29  0.59  0.90  0.89  0.91  0.90
2 cwmed  base      0.00  0.00  0.00  0.00  0.00  0.86
         elect     0.00  0.00  0.00  0.00  0.40  0.88
         orcinf    0.00  0.06  0.48  0.64  0.74  0.89
         sra       0.00  0.03  0.86  0.89  0.90  0.91
         sra_l10   0.00  0.03  0.86  0.89  0.90  0.91
         sra_rand  0.00  0.00  0.00  0.00  0.28  0.87
         sra_rr1   0.00  0.00  0.00  0.00  0.60  0.90
         sra_rr3   0.00  0.00  0.84  0.88  0.90  0.91
  fedavg base      0.00  0.04  0.41  0.48  0.74  0.89
  mkrum  base      0.00  0.00  0.00  0.67  0.90  0.91
         elect     0.00  0.00  0.00  0.88  0.91  0.92
         orcinf    0.00  0.04  0.43  0.47  0.73  0.89
         sra       0.00  0.02  0.86  0.88  0.89  0.91
         sra_l10   0.00  0.02  0.86  0.88  0.89  0.91
         sra_rand  0.00  0.00  0.00  0.21  0.82  0.88
         sra_rr1   0.00  0.00  0.00  0.00  0.64  0.90
         sra_rr3   0.00  0.01  0.79  0.84  0.89  0.90
  trmean base      0.00  0.00  0.17  0.57  0.87  0.90
         elect     0.00  0.00  0.28  0.60  0.86  0.90
         orcinf    0.00  0.05  0.43  0.56  0.74  0.89
         sra       0.00  0.02  0.86  0.88  0.89  0.91
         sra_l10   0.00  0.02  0.86  0.88  0.89  0.91
         sra_rand  0.00  0.00  0.34  0.28  0.87  0.89
         sra_rr1   0.00  0.00  0.00  0.00  0.80  0.90
         sra_rr3   0.00  0.00  0.83  0.86  0.89  0.91
4 cwmed  base      0.00  0.00  0.00  0.00  0.00  0.69
         elect     0.00  0.00  0.00  0.00  0.14  0.80
         orcinf    0.00  0.00  0.03  0.16  0.57  0.80
         sra       0.00  0.00  0.00  0.02  0.90  0.90
         sra_l10   0.00  0.00  0.00  0.02  0.90  0.90
         sra_rand  0.00  0.00  0.00  0.00  0.00  0.62
         sra_rr1   0.00  0.00  0.00  0.00  0.00  0.82
         sra_rr3   0.00  0.00  0.00  0.00  0.87  0.90
  fedavg base      0.00  0.00  0.01  0.09  0.55  0.79
  mkrum  base      0.00  0.00  0.00  0.00  0.86  0.85
         elect     0.00  0.00  0.00  0.00  0.89  0.87
         orcinf    0.00  0.00  0.02  0.13  0.51  0.80
         sra       0.00  0.00  0.00  0.01  0.89  0.90
         sra_l10   0.00  0.00  0.00  0.01  0.89  0.90
         sra_rand  0.00  0.00  0.00  0.00  0.43  0.72
         sra_rr1   0.00  0.00  0.00  0.00  0.00  0.63
         sra_rr3   0.00  0.00  0.00  0.00  0.86  0.90
  trmean base      0.00  0.00  0.00  0.00  0.65  0.83
         elect     0.00  0.00  0.00  0.01  0.67  0.84
         orcinf    0.00  0.00  0.02  0.12  0.56  0.80
         sra       0.00  0.00  0.00  0.01  0.89  0.90
         sra_l10   0.00  0.00  0.00  0.01  0.89  0.90
         sra_rand  0.00  0.00  0.00  0.00  0.77  0.85
         sra_rr1   0.00  0.00  0.00  0.00  0.00  0.82
         sra_rr3   0.00  0.00  0.00  0.00  0.87  0.90
```


## Portscan | M3 RR formula k*: smallest k with k p > (N-k-f)(1-p) + f   (grid-censored comparison)
```
    arm  eps_w  f    agg  predicted k* measured k*  sra (oracle) k*  within 1  within 2
sra_rr1    1.0  0  cwmed             6           8                1      True      True
sra_rr1    1.0  0 trmean             6           6                1      True      True
sra_rr1    1.0  0  mkrum             6           6                2      True      True
sra_rr1    1.0  2  cwmed             7           8                3      True      True
sra_rr1    1.0  2 trmean             7           6                3      True      True
sra_rr1    1.0  2  mkrum             7           8                3      True      True
sra_rr1    1.0  4  cwmed             9           8                6      True      True
sra_rr1    1.0  4 trmean             9           8                6      True      True
sra_rr1    1.0  4  mkrum             9       never                6      True      True
sra_rr3    3.0  0  cwmed             1           3                1     False      True
sra_rr3    3.0  0 trmean             1           3                1     False      True
sra_rr3    3.0  0  mkrum             1           3                2     False      True
sra_rr3    3.0  2  cwmed             3           3                3      True      True
sra_rr3    3.0  2 trmean             3           3                3      True      True
sra_rr3    3.0  2  mkrum             3           3                3      True      True
sra_rr3    3.0  4  cwmed             5           6                6      True      True
sra_rr3    3.0  4 trmean             5           6                6      True      True
sra_rr3    3.0  4  mkrum             5           6                6      True      True
```


## Portscan | M3 W-stratum composition + clip diagnostics (means over k, seeds)
```
               nW  nW_witness  nW_honest_nonwitness  nW_liar  sra_clip_hit_rate  sra_ratio_median  sra_fallback_rate
arm      f                                                                                                          
elect    0   4.00        4.00                  0.00      0.0                NaN               NaN                NaN
         2   6.00        4.00                  0.00      2.0                NaN               NaN                NaN
         4   8.00        4.00                  0.00      4.0                NaN               NaN                NaN
orcinf   0   4.00        4.00                  0.00      0.0                NaN               NaN                NaN
         2   6.00        4.00                  0.00      2.0                NaN               NaN                NaN
         4   8.00        4.00                  0.00      4.0                NaN               NaN                NaN
sra      0   4.00        4.00                  0.00      0.0               0.21              2.12                0.0
         2   6.00        4.00                  0.00      2.0               0.00              1.03                0.0
         4   8.00        4.00                  0.00      4.0               0.00              0.82                0.0
sra_l10  0   4.00        4.00                  0.00      0.0               0.00              1.70                0.0
         2   6.00        4.00                  0.00      2.0               0.00              1.03                0.0
         4   8.00        4.00                  0.00      4.0               0.00              0.82                0.0
sra_rand 0   4.00        0.72                  3.28      0.0               0.05              0.67                0.0
         2   6.00        1.22                  2.78      2.0               0.00              0.45                0.0
         4   8.00        1.11                  2.89      4.0               0.00              0.45                0.0
sra_rr1  0   6.61        2.56                  4.06      0.0               0.00              0.48                0.0
         2   8.72        3.00                  3.72      2.0               0.00              0.54                0.0
         4  10.56        3.28                  3.28      4.0               0.00              0.61                0.0
sra_rr3  0   4.61        3.72                  0.89      0.0               0.02              1.04                0.0
         2   6.28        3.78                  0.50      2.0               0.00              0.91                0.0
         4   8.61        4.00                  0.61      4.0               0.00              0.78                0.0
```


## Portscan | M3 per-class recall at f=0, k=6 (what else moves)
```
                 benign_fpr  other_attack_recall_mean  other_attack_recall_min  recall_Normal  recall_DoS  recall_DDoS  recall_Portscan  recall_Brute Force  recall_Botnet  recall_Web Attack
agg    arm                                                                                                                                                                                   
cwmed  base           0.001                     0.964                    0.871          0.999       0.998        0.999            0.507               0.993          0.959              0.871
       elect          0.002                     0.965                    0.871          0.998       0.998        0.999            0.753               0.993          0.964              0.871
       orcinf         0.001                     0.965                    0.871          0.999       0.998        0.999            0.907               0.993          0.962              0.871
       sra            0.001                     0.964                    0.871          0.999       0.998        0.999            0.907               0.993          0.961              0.871
       sra_l10        0.001                     0.964                    0.871          0.999       0.998        0.999            0.907               0.993          0.961              0.871
       sra_rand       0.001                     0.964                    0.871          0.999       0.998        0.999            0.707               0.994          0.959              0.871
       sra_rr1        0.001                     0.965                    0.871          0.999       0.998        0.999            0.701               0.993          0.961              0.871
       sra_rr3        0.001                     0.965                    0.871          0.999       0.998        0.999            0.907               0.993          0.961              0.871
fedavg base           0.001                     0.969                    0.887          0.999       0.998        0.999            0.907               0.994          0.968              0.887
mkrum  base           0.001                     0.971                    0.892          0.999       0.998        0.999            0.894               0.994          0.971              0.892
       elect          0.001                     0.969                    0.882          0.999       0.998        0.999            0.891               0.993          0.973              0.882
       orcinf         0.001                     0.968                    0.882          0.999       0.998        0.999            0.907               0.994          0.966              0.882
       sra            0.001                     0.969                    0.887          0.999       0.998        0.999            0.900               0.994          0.969              0.887
       sra_l10        0.001                     0.969                    0.887          0.999       0.998        0.999            0.900               0.994          0.969              0.887
       sra_rand       0.001                     0.969                    0.887          0.999       0.998        0.999            0.882               0.993          0.968              0.887
       sra_rr1        0.001                     0.971                    0.892          0.999       0.998        0.999            0.885               0.994          0.971              0.892
       sra_rr3        0.001                     0.968                    0.882          0.999       0.998        0.999            0.896               0.994          0.969              0.882
trmean base           0.001                     0.968                    0.882          0.999       0.998        0.999            0.896               0.994          0.966              0.882
       elect          0.001                     0.967                    0.876          0.999       0.998        0.999            0.901               0.993          0.970              0.876
       orcinf         0.001                     0.966                    0.876          0.999       0.998        0.999            0.907               0.994          0.964              0.876
       sra            0.001                     0.968                    0.882          0.999       0.998        0.999            0.906               0.993          0.966              0.882
       sra_l10        0.001                     0.968                    0.882          0.999       0.998        0.999            0.906               0.993          0.966              0.882
       sra_rand       0.001                     0.966                    0.876          0.999       0.998        0.999            0.894               0.994          0.964              0.876
       sra_rr1        0.001                     0.967                    0.876          0.999       0.998        0.999            0.897               0.993          0.967              0.876
       sra_rr3        0.001                     0.968                    0.882          0.999       0.998        0.999            0.906               0.993          0.966              0.882
```


## Portscan | M3 verdicts
```
COVERAGE (sra)        : REMOVES_TAX
FLOOR (sra k* <= f+1) : ABOVE_FLOOR (share 0.56)
IDENTITY (sra_rand)   : IDENTITY_MATTERS
-- post-hoc lambda diagnostic (NOT the headline) --
COVERAGE (sra_l10)    : REMOVES_TAX
FLOOR (sra_l10)       : REACHES_FLOOR (share 0.67)
LAMBDA DIAGNOSTIC     : LAMBDA_NOT_THE_ISSUE (lambda=10 does not beat lambda=3 by >= 2 in >= 2/3 of cells)
RR formula sra_rr1    : FORMULA_HOLDS
RR formula sra_rr3    : FORMULA_HOLDS
coverage orcinf       : REMOVES_TAX
coverage elect        : NO_EFFECT
coverage sra_rr1      : NO_EFFECT+HARM
coverage sra_rr3      : NO_EFFECT
coverage sra_rand     : NO_EFFECT+HARM
floor violations      : none
worst sra cell        : mkrum f=0 k*=2 tax=1
```


## Portscan | M4 sign-flip x10 / ALIE z=1  ('_nc' = attackers do NOT claim evidence)
```
 k  f      attack    agg     arm  benign_fpr  other_mean  other_min      paired                     absolute
 6  2    signflip fedavg    base       0.667       0.133      0.000                                effective
 6  2    signflip  cwmed    base       0.001       0.962      0.871 (reference)                        HOLDS
 6  2    signflip  cwmed     sra       0.002       0.961      0.871       HOLDS                        HOLDS
 6  2 signflip_nc  cwmed     sra       0.002       0.962      0.871       HOLDS                        HOLDS
 6  2    signflip  cwmed sra_l10       0.002       0.961      0.871       HOLDS                        HOLDS
 6  2 signflip_nc  cwmed sra_l10       0.002       0.962      0.871       HOLDS                        HOLDS
 6  2    signflip  cwmed  orcinf       0.795       0.133      0.000      BREAKS                       BREAKS
 6  2 signflip_nc  cwmed  orcinf       0.002       0.962      0.871       HOLDS                        HOLDS
 6  2    signflip  cwmed   elect       0.001       0.961      0.871       HOLDS                        HOLDS
 6  2 signflip_nc  cwmed   elect       0.001       0.961      0.871       HOLDS                        HOLDS
 6  2    signflip trmean    base       0.002       0.961      0.871 (reference)                        HOLDS
 6  2    signflip trmean     sra       0.002       0.961      0.871       HOLDS                        HOLDS
 6  2 signflip_nc trmean     sra       0.002       0.961      0.871       HOLDS                        HOLDS
 6  2    signflip trmean sra_l10       0.002       0.961      0.871       HOLDS                        HOLDS
 6  2 signflip_nc trmean sra_l10       0.002       0.961      0.871       HOLDS                        HOLDS
 6  2    signflip trmean  orcinf       0.731       0.067      0.000      BREAKS                       BREAKS
 6  2 signflip_nc trmean  orcinf       0.002       0.961      0.871       HOLDS                        HOLDS
 6  2    signflip trmean   elect       0.002       0.962      0.871       HOLDS                        HOLDS
 6  2 signflip_nc trmean   elect       0.002       0.961      0.871       HOLDS                        HOLDS
 6  2    signflip  mkrum    base       0.001       0.966      0.876 (reference)                        HOLDS
 6  2    signflip  mkrum     sra       0.002       0.962      0.871       HOLDS                        HOLDS
 6  2 signflip_nc  mkrum     sra       0.001       0.968      0.882       HOLDS                        HOLDS
 6  2    signflip  mkrum sra_l10       0.002       0.962      0.871       HOLDS                        HOLDS
 6  2 signflip_nc  mkrum sra_l10       0.001       0.968      0.882       HOLDS                        HOLDS
 6  2    signflip  mkrum  orcinf       0.812       0.252      0.000      BREAKS                       BREAKS
 6  2 signflip_nc  mkrum  orcinf       0.001       0.968      0.882       HOLDS                        HOLDS
 6  2    signflip  mkrum   elect       0.001       0.966      0.876       HOLDS                        HOLDS
 6  2 signflip_nc  mkrum   elect       0.001       0.966      0.876       HOLDS                        HOLDS
 6  2        alie fedavg    base       0.001       0.967      0.876                          attack too weak
 6  2        alie  cwmed    base       0.002       0.964      0.871 (reference) INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2        alie  cwmed     sra       0.002       0.965      0.871       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2     alie_nc  cwmed     sra       0.001       0.965      0.871       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2        alie  cwmed sra_l10       0.002       0.965      0.871       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2     alie_nc  cwmed sra_l10       0.001       0.965      0.871       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2        alie  cwmed  orcinf       0.001       0.965      0.871       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2     alie_nc  cwmed  orcinf       0.001       0.965      0.871       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2        alie  cwmed   elect       0.002       0.964      0.871       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2     alie_nc  cwmed   elect       0.002       0.963      0.871       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2        alie trmean    base       0.001       0.965      0.871 (reference) INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2        alie trmean     sra       0.001       0.965      0.871       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2     alie_nc trmean     sra       0.001       0.965      0.871       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2        alie trmean sra_l10       0.001       0.965      0.871       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2     alie_nc trmean sra_l10       0.001       0.965      0.871       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2        alie trmean  orcinf       0.001       0.965      0.871       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2     alie_nc trmean  orcinf       0.001       0.965      0.871       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2        alie trmean   elect       0.001       0.965      0.871       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2     alie_nc trmean   elect       0.001       0.965      0.871       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2        alie  mkrum    base       0.001       0.966      0.871 (reference) INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2        alie  mkrum     sra       0.001       0.966      0.871       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2     alie_nc  mkrum     sra       0.001       0.965      0.871       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2        alie  mkrum sra_l10       0.001       0.966      0.871       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2     alie_nc  mkrum sra_l10       0.001       0.965      0.871       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2        alie  mkrum  orcinf       0.001       0.966      0.871       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2     alie_nc  mkrum  orcinf       0.001       0.966      0.871       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2        alie  mkrum   elect       0.001       0.966      0.871       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  2     alie_nc  mkrum   elect       0.001       0.966      0.871       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4    signflip fedavg    base       0.333       0.067      0.000                                effective
 6  4    signflip  cwmed    base       0.002       0.962      0.871 (reference)                        HOLDS
 6  4    signflip  cwmed     sra       0.003       0.958      0.871       HOLDS                        HOLDS
 6  4 signflip_nc  cwmed     sra       0.002       0.960      0.871       HOLDS                        HOLDS
 6  4    signflip  cwmed sra_l10       0.003       0.958      0.871       HOLDS                        HOLDS
 6  4 signflip_nc  cwmed sra_l10       0.002       0.960      0.871       HOLDS                        HOLDS
 6  4    signflip  cwmed  orcinf       0.340       0.067      0.000      BREAKS                       BREAKS
 6  4 signflip_nc  cwmed  orcinf       0.002       0.960      0.871       HOLDS                        HOLDS
 6  4    signflip  cwmed   elect       0.002       0.961      0.871       HOLDS                        HOLDS
 6  4 signflip_nc  cwmed   elect       0.002       0.960      0.871       HOLDS                        HOLDS
 6  4    signflip trmean    base       0.522       0.067      0.000 (reference)                       BREAKS
 6  4    signflip trmean     sra       0.003       0.960      0.871       HOLDS                        HOLDS
 6  4 signflip_nc trmean     sra       0.016       0.000      0.000      BREAKS                       BREAKS
 6  4    signflip trmean sra_l10       0.003       0.960      0.871       HOLDS                        HOLDS
 6  4 signflip_nc trmean sra_l10       0.016       0.000      0.000      BREAKS                       BREAKS
 6  4    signflip trmean  orcinf       1.000       0.133      0.000      BREAKS                       BREAKS
 6  4 signflip_nc trmean  orcinf       0.869       0.133      0.000      BREAKS                       BREAKS
 6  4    signflip trmean   elect       0.772       0.032      0.000      BREAKS                       BREAKS
 6  4 signflip_nc trmean   elect       1.000       0.200      0.000      BREAKS                       BREAKS
 6  4    signflip  mkrum    base       0.125       0.067      0.000 (reference)                       BREAKS
 6  4    signflip  mkrum     sra       0.002       0.959      0.871       HOLDS                        HOLDS
 6  4 signflip_nc  mkrum     sra       0.667       0.067      0.000      BREAKS                       BREAKS
 6  4    signflip  mkrum sra_l10       0.002       0.959      0.871       HOLDS                        HOLDS
 6  4 signflip_nc  mkrum sra_l10       0.667       0.067      0.000      BREAKS                       BREAKS
 6  4    signflip  mkrum  orcinf       0.882       0.134      0.000      BREAKS                       BREAKS
 6  4 signflip_nc  mkrum  orcinf       0.333       0.067      0.000      BREAKS                       BREAKS
 6  4    signflip  mkrum   elect       1.000       0.067      0.000      BREAKS                       BREAKS
 6  4 signflip_nc  mkrum   elect       0.667       0.133      0.000      BREAKS                       BREAKS
 6  4        alie fedavg    base       0.001       0.965      0.871                          attack too weak
 6  4        alie  cwmed    base       0.002       0.963      0.871 (reference) INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4        alie  cwmed     sra       0.002       0.964      0.871       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4     alie_nc  cwmed     sra       0.002       0.964      0.871       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4        alie  cwmed sra_l10       0.002       0.964      0.871       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4     alie_nc  cwmed sra_l10       0.002       0.964      0.871       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4        alie  cwmed  orcinf       0.002       0.964      0.871       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4     alie_nc  cwmed  orcinf       0.002       0.965      0.871       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4        alie  cwmed   elect       0.002       0.963      0.871       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4     alie_nc  cwmed   elect       0.002       0.963      0.871       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4        alie trmean    base       0.001       0.964      0.871 (reference) INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4        alie trmean     sra       0.002       0.964      0.871       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4     alie_nc trmean     sra       0.002       0.964      0.871       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4        alie trmean sra_l10       0.002       0.964      0.871       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4     alie_nc trmean sra_l10       0.002       0.964      0.871       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4        alie trmean  orcinf       0.001       0.964      0.871       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4     alie_nc trmean  orcinf       0.002       0.965      0.871       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4        alie trmean   elect       0.001       0.965      0.871       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4     alie_nc trmean   elect       0.001       0.965      0.871       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4        alie  mkrum    base       0.001       0.965      0.871 (reference) INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4        alie  mkrum     sra       0.001       0.965      0.871       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4     alie_nc  mkrum     sra       0.001       0.964      0.871       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4        alie  mkrum sra_l10       0.001       0.965      0.871       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4     alie_nc  mkrum sra_l10       0.001       0.964      0.871       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4        alie  mkrum  orcinf       0.001       0.965      0.871       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4     alie_nc  mkrum  orcinf       0.002       0.965      0.871       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4        alie  mkrum   elect       0.001       0.966      0.871       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 6  4     alie_nc  mkrum   elect       0.002       0.966      0.871       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4    signflip fedavg    base       0.000       0.000      0.000                                effective
 2  4    signflip  cwmed    base       0.002       0.963      0.871 (reference)                        HOLDS
 2  4    signflip  cwmed     sra       0.000       0.000      0.000      BREAKS                       BREAKS
 2  4 signflip_nc  cwmed     sra       0.002       0.960      0.871       HOLDS                        HOLDS
 2  4    signflip  cwmed sra_l10       0.332       0.066      0.000      BREAKS                       BREAKS
 2  4 signflip_nc  cwmed sra_l10       0.002       0.960      0.871       HOLDS                        HOLDS
 2  4    signflip  cwmed  orcinf       0.333       0.067      0.000      BREAKS                       BREAKS
 2  4 signflip_nc  cwmed  orcinf       0.002       0.960      0.871       HOLDS                        HOLDS
 2  4    signflip  cwmed   elect       1.000       0.000      0.000      BREAKS                       BREAKS
 2  4 signflip_nc  cwmed   elect       0.002       0.963      0.871       HOLDS                        HOLDS
 2  4    signflip trmean    base       0.156       0.126      0.000 (reference)                       BREAKS
 2  4    signflip trmean     sra       0.020       0.004      0.000      BREAKS                       BREAKS
 2  4 signflip_nc trmean     sra       0.374       0.001      0.000      BREAKS                       BREAKS
 2  4    signflip trmean sra_l10       1.000       0.133      0.000      BREAKS                       BREAKS
 2  4 signflip_nc trmean sra_l10       0.374       0.001      0.000      BREAKS                       BREAKS
 2  4    signflip trmean  orcinf       0.333       0.000      0.000      BREAKS                       BREAKS
 2  4 signflip_nc trmean  orcinf       0.667       0.133      0.000      BREAKS                       BREAKS
 2  4    signflip trmean   elect       0.668       0.000      0.000      BREAKS                       BREAKS
 2  4 signflip_nc trmean   elect       0.619       0.067      0.000      BREAKS                       BREAKS
 2  4    signflip  mkrum    base       0.687       0.133      0.000 (reference)                       BREAKS
 2  4    signflip  mkrum     sra       0.333       0.065      0.000      BREAKS                       BREAKS
 2  4 signflip_nc  mkrum     sra       1.000       0.200      0.000      BREAKS                       BREAKS
 2  4    signflip  mkrum sra_l10       0.000       0.000      0.000      BREAKS                       BREAKS
 2  4 signflip_nc  mkrum sra_l10       1.000       0.200      0.000      BREAKS                       BREAKS
 2  4    signflip  mkrum  orcinf       0.333       0.067      0.000      BREAKS                       BREAKS
 2  4 signflip_nc  mkrum  orcinf       0.778       0.067      0.000      BREAKS                       BREAKS
 2  4    signflip  mkrum   elect       1.000       0.000      0.000      BREAKS                       BREAKS
 2  4 signflip_nc  mkrum   elect       0.663       0.133      0.000       HOLDS                       BREAKS
 2  4        alie fedavg    base       0.001       0.964      0.871                          attack too weak
 2  4        alie  cwmed    base       0.001       0.963      0.871 (reference) INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4        alie  cwmed     sra       0.002       0.963      0.871       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4     alie_nc  cwmed     sra       0.002       0.964      0.871       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4        alie  cwmed sra_l10       0.002       0.963      0.871       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4     alie_nc  cwmed sra_l10       0.002       0.964      0.871       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4        alie  cwmed  orcinf       0.002       0.964      0.871       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4     alie_nc  cwmed  orcinf       0.002       0.964      0.871       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4        alie  cwmed   elect       0.001       0.963      0.871       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4     alie_nc  cwmed   elect       0.001       0.962      0.871       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4        alie trmean    base       0.001       0.963      0.871 (reference) INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4        alie trmean     sra       0.002       0.964      0.871       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4     alie_nc trmean     sra       0.002       0.963      0.871       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4        alie trmean sra_l10       0.001       0.964      0.871       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4     alie_nc trmean sra_l10       0.002       0.964      0.871       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4        alie trmean  orcinf       0.002       0.964      0.871       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4     alie_nc trmean  orcinf       0.002       0.964      0.871       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4        alie trmean   elect       0.001       0.963      0.871       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4     alie_nc trmean   elect       0.002       0.964      0.871       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4        alie  mkrum    base       0.001       0.964      0.871 (reference) INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4        alie  mkrum     sra       0.001       0.964      0.871       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4     alie_nc  mkrum     sra       0.002       0.964      0.871       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4        alie  mkrum sra_l10       0.001       0.964      0.871       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4     alie_nc  mkrum sra_l10       0.002       0.964      0.871       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4        alie  mkrum  orcinf       0.002       0.964      0.871       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4     alie_nc  mkrum  orcinf       0.002       0.964      0.871       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4        alie  mkrum   elect       0.002       0.965      0.871       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
 2  4     alie_nc  mkrum   elect       0.002       0.964      0.871       HOLDS INCONCLUSIVE_ATTACK_TOO_WEAK
```


## Portscan | M4 SRA W-stratum composition + clip-hit rate
```
                           nW  nW_witness  nW_liar  sra_clip_hit_rate  sra_ratio_median
arm     k f attack                                                                     
sra     2 4 alie          6.0         2.0      4.0               0.06              2.08
            alie_nc       2.0         2.0      0.0               0.06              2.32
            signflip      6.0         2.0      4.0               0.90             19.89
            signflip_nc   2.0         2.0      0.0               0.01              0.27
        6 2 alie          8.0         6.0      2.0               0.00              0.95
            alie_nc       6.0         6.0      0.0               0.00              0.96
            signflip      8.0         6.0      2.0               0.00              0.93
            signflip_nc   6.0         6.0      0.0               0.00              0.82
          4 alie         10.0         6.0      4.0               0.00              1.13
            alie_nc       6.0         6.0      0.0               0.00              0.97
            signflip     10.0         6.0      4.0               0.00              1.39
            signflip_nc   6.0         6.0      0.0               0.00              0.23
sra_l10 2 4 alie          6.0         2.0      4.0               0.00              2.09
            alie_nc       2.0         2.0      0.0               0.00              2.33
            signflip      6.0         2.0      4.0               0.64             34.23
            signflip_nc   2.0         2.0      0.0               0.01              0.27
        6 2 alie          8.0         6.0      2.0               0.00              0.95
            alie_nc       6.0         6.0      0.0               0.00              0.96
            signflip      8.0         6.0      2.0               0.00              0.93
            signflip_nc   6.0         6.0      0.0               0.00              0.82
          4 alie         10.0         6.0      4.0               0.00              1.13
            alie_nc       6.0         6.0      0.0               0.00              0.97
            signflip     10.0         6.0      4.0               0.00              1.39
            signflip_nc   6.0         6.0      0.0               0.00              0.23
```


## Portscan | M4 full per-class recall
```
                                recall_Normal  recall_DoS  recall_DDoS  recall_Portscan  recall_Brute Force  recall_Botnet  recall_Web Attack
k f attack      agg    arm                                                                                                                   
2 0 mimic       fedavg base             0.999       0.998        0.999            0.886               0.994          0.952              0.876
  4 alie        cwmed  base             0.999       0.998        0.999            0.000               0.993          0.955              0.871
                       elect            0.999       0.998        0.999            0.000               0.994          0.955              0.871
                       orcinf           0.998       0.998        0.999            0.888               0.994          0.956              0.871
                       sra              0.998       0.998        0.999            0.000               0.993          0.953              0.871
                       sra_l10          0.998       0.998        0.999            0.000               0.993          0.952              0.871
                fedavg base             0.999       0.998        0.999            0.854               0.994          0.957              0.871
                mkrum  base             0.999       0.999        0.999            0.000               0.994          0.955              0.871
                       elect            0.998       0.999        0.999            0.000               0.994          0.961              0.871
                       orcinf           0.998       0.998        0.999            0.861               0.995          0.958              0.871
                       sra              0.999       0.999        0.999            0.000               0.994          0.958              0.871
                       sra_l10          0.999       0.999        0.999            0.000               0.994          0.955              0.871
                trmean base             0.999       0.998        0.999            0.000               0.994          0.952              0.871
                       elect            0.999       0.998        0.999            0.000               0.994          0.955              0.871
                       orcinf           0.998       0.998        0.999            0.871               0.994          0.956              0.871
                       sra              0.998       0.998        0.999            0.000               0.994          0.958              0.871
                       sra_l10          0.999       0.998        0.999            0.000               0.994          0.956              0.871
    alie_nc     cwmed  elect            0.999       0.998        0.999            0.000               0.994          0.949              0.871
                       orcinf           0.998       0.998        0.999            0.883               0.994          0.956              0.871
                       sra              0.998       0.998        0.999            0.885               0.994          0.956              0.871
                       sra_l10          0.998       0.998        0.999            0.884               0.994          0.956              0.871
                mkrum  elect            0.998       0.998        0.999            0.123               0.995          0.958              0.871
                       orcinf           0.998       0.998        0.999            0.849               0.994          0.957              0.871
                       sra              0.998       0.998        0.999            0.849               0.995          0.957              0.871
                       sra_l10          0.998       0.998        0.999            0.848               0.994          0.957              0.871
                trmean elect            0.998       0.998        0.999            0.508               0.995          0.956              0.871
                       orcinf           0.998       0.998        0.999            0.857               0.994          0.955              0.871
                       sra              0.998       0.998        0.999            0.858               0.994          0.954              0.871
                       sra_l10          0.998       0.998        0.999            0.855               0.994          0.955              0.871
    signflip    cwmed  base             0.998       0.998        0.999            0.000               0.992          0.952              0.871
                       elect            0.000       0.000        0.000            1.000               0.000          0.000              0.000
                       orcinf           0.667       0.333        0.000            0.000               0.000          0.000              0.000
                       sra              1.000       0.000        0.000            0.000               0.000          0.000              0.000
                       sra_l10          0.668       0.332        0.000            0.000               0.000          0.000              0.000
                fedavg base             1.000       0.000        0.000            0.000               0.000          0.000              0.000
                mkrum  base             0.313       0.333        0.333            0.000               0.000          0.000              0.000
                       elect            0.000       0.000        0.000            1.000               0.000          0.000              0.000
                       orcinf           0.667       0.000        0.000            0.000               0.000          0.333              0.000
                       sra              0.667       0.325        0.000            0.000               0.000          0.000              0.000
                       sra_l10          1.000       0.000        0.000            0.000               0.000          0.000              0.000
                trmean base             0.844       0.330        0.000            0.000               0.000          0.298              0.000
                       elect            0.332       0.001        0.000            0.667               0.000          0.000              0.000
                       orcinf           0.667       0.000        0.000            0.026               0.000          0.000              0.000
                       sra              0.980       0.020        0.000            0.000               0.000          0.000              0.000
                       sra_l10          0.000       0.000        0.333            0.333               0.000          0.333              0.000
    signflip_nc cwmed  elect            0.998       0.998        0.999            0.000               0.993          0.954              0.871
                       orcinf           0.998       0.996        0.999            0.874               0.992          0.942              0.871
                       sra              0.998       0.996        0.999            0.874               0.992          0.942              0.871
                       sra_l10          0.998       0.996        0.999            0.874               0.992          0.942              0.871
                mkrum  elect            0.337       0.333        0.000            0.000               0.333          0.000              0.000
                       orcinf           0.222       0.333        0.000            0.354               0.000          0.000              0.000
                       sra              0.000       0.333        0.000            0.000               0.000          0.333              0.333
                       sra_l10          0.000       0.333        0.000            0.000               0.000          0.333              0.333
                trmean elect            0.381       0.333        0.000            0.017               0.000          0.000              0.000
                       orcinf           0.333       0.000        0.333            0.000               0.000          0.333              0.000
                       sra              0.626       0.005        0.000            0.000               0.000          0.000              0.000
                       sra_l10          0.626       0.005        0.000            0.000               0.000          0.000              0.000
6 0 mimic       fedavg base             0.999       0.998        0.999            0.907               0.994          0.968              0.887
  2 alie        cwmed  base             0.998       0.998        0.999            0.790               0.993          0.958              0.871
                       elect            0.998       0.998        0.999            0.811               0.993          0.959              0.871
                       orcinf           0.999       0.998        0.999            0.907               0.994          0.961              0.871
                       sra              0.998       0.998        0.999            0.907               0.994          0.961              0.871
                       sra_l10          0.998       0.998        0.999            0.907               0.994          0.961              0.871
                fedavg base             0.999       0.998        0.999            0.907               0.995          0.967              0.876
                mkrum  base             0.999       0.998        0.999            0.901               0.995          0.967              0.871
                       elect            0.999       0.998        0.999            0.888               0.995          0.967              0.871
                       orcinf           0.999       0.998        0.999            0.907               0.995          0.966              0.871
                       sra              0.999       0.998        0.999            0.905               0.995          0.965              0.871
                       sra_l10          0.999       0.998        0.999            0.905               0.995          0.965              0.871
                trmean base             0.999       0.998        0.999            0.902               0.994          0.963              0.871
                       elect            0.999       0.998        0.999            0.897               0.994          0.964              0.871
                       orcinf           0.999       0.998        0.999            0.907               0.994          0.964              0.871
                       sra              0.999       0.998        0.999            0.905               0.994          0.964              0.871
                       sra_l10          0.999       0.998        0.999            0.905               0.994          0.964              0.871
    alie_nc     cwmed  elect            0.998       0.998        0.999            0.800               0.993          0.956              0.871
                       orcinf           0.999       0.998        0.999            0.907               0.994          0.964              0.871
                       sra              0.999       0.998        0.999            0.902               0.994          0.962              0.871
                       sra_l10          0.999       0.998        0.999            0.902               0.994          0.962              0.871
                mkrum  elect            0.999       0.998        0.999            0.885               0.994          0.967              0.871
                       orcinf           0.999       0.998        0.999            0.907               0.995          0.967              0.871
                       sra              0.999       0.998        0.999            0.903               0.994          0.964              0.871
                       sra_l10          0.999       0.998        0.999            0.903               0.994          0.964              0.871
                trmean elect            0.999       0.998        0.999            0.895               0.994          0.964              0.871
                       orcinf           0.999       0.998        0.999            0.907               0.994          0.964              0.871
                       sra              0.999       0.998        0.999            0.900               0.994          0.962              0.871
                       sra_l10          0.999       0.998        0.999            0.900               0.994          0.962              0.871
    signflip    cwmed  base             0.999       0.997        0.999            0.000               0.993          0.947              0.871
                       elect            0.999       0.997        0.999            0.310               0.992          0.945              0.871
                       orcinf           0.205       0.000        0.000            0.333               0.332          0.333              0.000
                       sra              0.998       0.997        0.999            0.897               0.993          0.946              0.871
                       sra_l10          0.998       0.997        0.999            0.897               0.993          0.946              0.871
                fedavg base             0.333       0.667        0.000            0.000               0.000          0.000              0.000
                mkrum  base             0.999       0.998        0.999            0.907               0.994          0.960              0.876
                       elect            0.999       0.998        0.999            0.908               0.994          0.964              0.876
                       orcinf           0.188       0.624        0.000            0.000               0.304          0.333              0.000
                       sra              0.998       0.997        0.999            0.897               0.993          0.948              0.871
                       sra_l10          0.998       0.997        0.999            0.897               0.993          0.948              0.871
                trmean base             0.998       0.997        0.999            0.875               0.993          0.945              0.871
                       elect            0.998       0.998        0.999            0.889               0.993          0.947              0.871
                       orcinf           0.269       0.000        0.000            0.000               0.000          0.333              0.000
                       sra              0.998       0.997        0.999            0.897               0.993          0.946              0.871
                       sra_l10          0.998       0.997        0.999            0.897               0.993          0.946              0.871
    signflip_nc cwmed  elect            0.999       0.997        0.999            0.294               0.993          0.945              0.871
                       orcinf           0.998       0.997        0.999            0.907               0.993          0.948              0.871
                       sra              0.998       0.997        0.999            0.900               0.993          0.948              0.871
                       sra_l10          0.998       0.997        0.999            0.900               0.993          0.948              0.871
                mkrum  elect            0.999       0.998        0.999            0.908               0.994          0.962              0.876
                       orcinf           0.999       0.998        0.999            0.907               0.995          0.967              0.882
                       sra              0.999       0.998        0.999            0.899               0.995          0.967              0.882
                       sra_l10          0.999       0.998        0.999            0.899               0.995          0.967              0.882
                trmean elect            0.998       0.998        0.999            0.887               0.993          0.946              0.871
                       orcinf           0.998       0.997        0.999            0.901               0.993          0.945              0.871
                       sra              0.998       0.997        0.999            0.895               0.993          0.945              0.871
                       sra_l10          0.998       0.997        0.999            0.895               0.993          0.945              0.871
  4 alie        cwmed  base             0.998       0.997        0.999            0.890               0.994          0.953              0.871
                       elect            0.998       0.998        0.999            0.882               0.994          0.954              0.871
                       orcinf           0.998       0.998        0.999            0.915               0.994          0.957              0.871
                       sra              0.998       0.998        0.999            0.913               0.994          0.958              0.871
                       sra_l10          0.998       0.998        0.999            0.913               0.994          0.958              0.871
                fedavg base             0.999       0.998        0.999            0.914               0.994          0.962              0.871
                mkrum  base             0.999       0.998        0.999            0.899               0.994          0.965              0.871
                       elect            0.999       0.998        0.999            0.904               0.994          0.967              0.871
                       orcinf           0.999       0.998        0.999            0.915               0.995          0.962              0.871
                       sra              0.999       0.998        0.999            0.912               0.994          0.961              0.871
                       sra_l10          0.999       0.998        0.999            0.912               0.994          0.961              0.871
                trmean base             0.999       0.998        0.999            0.900               0.994          0.958              0.871
                       elect            0.999       0.998        0.999            0.909               0.994          0.962              0.871
                       orcinf           0.999       0.998        0.999            0.915               0.994          0.959              0.871
                       sra              0.998       0.998        0.999            0.913               0.994          0.961              0.871
                       sra_l10          0.998       0.998        0.999            0.913               0.994          0.961              0.871
    alie_nc     cwmed  elect            0.998       0.998        0.999            0.859               0.994          0.952              0.871
                       orcinf           0.998       0.998        0.999            0.906               0.994          0.965              0.871
                       sra              0.998       0.998        0.999            0.900               0.994          0.961              0.871
                       sra_l10          0.998       0.998        0.999            0.900               0.994          0.961              0.871
                mkrum  elect            0.998       0.998        0.999            0.907               0.994          0.969              0.871
                       orcinf           0.998       0.998        0.999            0.915               0.994          0.962              0.871
                       sra              0.999       0.998        0.999            0.913               0.994          0.958              0.871
                       sra_l10          0.999       0.998        0.999            0.913               0.994          0.958              0.871
                trmean elect            0.999       0.998        0.999            0.913               0.994          0.964              0.871
                       orcinf           0.998       0.998        0.999            0.915               0.994          0.961              0.871
                       sra              0.998       0.998        0.999            0.910               0.994          0.958              0.871
                       sra_l10          0.998       0.998        0.999            0.910               0.994          0.958              0.871
    signflip    cwmed  base             0.998       0.997        0.999            0.000               0.992          0.952              0.871
                       elect            0.998       0.997        0.999            0.170               0.992          0.943              0.871
                       orcinf           0.660       0.000        0.000            0.049               0.000          0.000              0.333
                       sra              0.997       0.993        0.999            0.897               0.992          0.937              0.871
                       sra_l10          0.997       0.993        0.999            0.897               0.992          0.937              0.871
                fedavg base             0.667       0.000        0.000            0.000               0.000          0.333              0.000
                mkrum  base             0.875       0.000        0.333            0.000               0.000          0.000              0.000
                       elect            0.000       0.333        0.000            0.667               0.000          0.000              0.000
                       orcinf           0.118       0.338        0.000            0.000               0.000          0.000              0.333
                       sra              0.998       0.994        0.999            0.901               0.993          0.939              0.871
                       sra_l10          0.998       0.994        0.999            0.901               0.993          0.939              0.871
                trmean base             0.478       0.333        0.000            0.001               0.000          0.000              0.000
                       elect            0.228       0.000        0.159            0.671               0.000          0.000              0.000
                       orcinf           0.000       0.000        0.000            0.333               0.000          0.333              0.333
                       sra              0.997       0.994        0.999            0.904               0.993          0.942              0.871
                       sra_l10          0.997       0.994        0.999            0.904               0.993          0.942              0.871
    signflip_nc cwmed  elect            0.998       0.996        0.999            0.096               0.992          0.942              0.871
                       orcinf           0.998       0.995        0.999            0.902               0.993          0.940              0.871
                       sra              0.998       0.995        0.999            0.896               0.992          0.940              0.871
                       sra_l10          0.998       0.995        0.999            0.896               0.992          0.940              0.871
                mkrum  elect            0.333       0.333        0.333            0.000               0.000          0.000              0.000
                       orcinf           0.667       0.333        0.000            0.000               0.000          0.000              0.000
                       sra              0.333       0.000        0.333            0.333               0.000          0.000              0.000
                       sra_l10          0.333       0.000        0.333            0.333               0.000          0.000              0.000
                trmean elect            0.000       0.667        0.000            0.000               0.333          0.000              0.000
                       orcinf           0.131       0.333        0.333            0.000               0.000          0.000              0.000
                       sra              0.984       0.000        0.000            0.000               0.000          0.000              0.000
                       sra_l10          0.984       0.000        0.000            0.000               0.000          0.000              0.000
```


## Portscan | M4 paired verdict counts (HOLDS / BREAKS) by arm and cell type
```
paired                         BREAKS  HOLDS
arm     cell                                
elect   k<=f (bounded damage)       4      8
        k>f                         4     20
orcinf  k<=f (bounded damage)       5      7
        k>f                         8     16
sra     k<=f (bounded damage)       5      7
        k>f                         2     22
sra_l10 k<=f (bounded damage)       5      7
        k>f                         2     22
```


## Portscan | M5 mean target recall under DP (DP reference FedAvg k=16: 0.877)
```
k               1     2     3     4     6     8
agg    arm                                     
cwmed  base  0.01  0.03  0.32  0.53  0.71  0.81
       sra   0.01  0.12  0.29  0.56  0.73  0.80
fedavg base  0.00  0.22  0.65  0.82  0.86  0.87
mkrum  base  0.16  0.36  0.54  0.66  0.80  0.87
       sra   0.01  0.36  0.45  0.58  0.81  0.81
trmean base  0.01  0.27  0.65  0.82  0.88  0.88
       sra   0.00  0.27  0.79  0.83  0.84  0.84
```


## Portscan | M5 k* under DP (learnable line 0.8x DP reference = 0.702)
```
 f    agg        base       sra
 0 fedavg 4 (floor 1)          
 0  cwmed   6 (tax 2) 6 (tax 2)
 0 trmean   4 (tax 0) 3 (tax 0)
 0  mkrum   6 (tax 2) 6 (tax 2)
```


## Portscan | M5 per-class recall under DP
```
             benign_fpr  other_attack_recall_mean  recall_Normal  recall_DoS  recall_DDoS  recall_Portscan  recall_Brute Force  recall_Botnet  recall_Web Attack
agg    arm                                                                                                                                                      
cwmed  base       0.010                     0.938          0.990       0.984        0.999            0.706               0.993          0.898              0.817
       sra        0.009                     0.948          0.991       0.987        0.999            0.728               0.992          0.905              0.855
fedavg base       0.008                     0.949          0.992       0.986        0.999            0.861               0.993          0.905              0.860
mkrum  base       0.009                     0.953          0.991       0.989        0.999            0.796               0.993          0.914              0.871
       sra        0.009                     0.950          0.991       0.986        0.999            0.810               0.993          0.905              0.866
trmean base       0.008                     0.951          0.992       0.986        0.999            0.883               0.992          0.910              0.866
       sra        0.008                     0.951          0.992       0.985        0.999            0.837               0.992          0.913              0.866
```


## Portscan | M5 verdict
```
SRA under DP (tax vs FedAvg-DP): NO_EFFECT
```
