# Mitigation + mechanism summary -- CSE-CIC-IDS2018 (script mit-1.0)


## Brute Force | verdicts
```
M0: WALL_TRACKS_FHAT
M1_orc1: NO_EFFECT+HARM
M1_orc10: REMOVES_TAX
M1_orcinf: REMOVES_TAX
M1_elect: REMOVES_TAX
M1_verify: REMOVES_TAX
M1_loud: NO_EFFECT
M1_probeonly: REMOVES_TAX
identity: IDENTITY_MATTERS
rr_rr3inf: CHEAP
rr_electrr1: COSTLY
rr_electrr3: MIXED
floor_flags: 0
witness_dist_over_tau: {'cwmed': 1.7, 'mkrum': 1.9, 'trmean': 1.8}
M2_base: cwmed f=2: HOLDS, trmean f=2: HOLDS, mkrum f=2: HOLDS, cwmed f=4: BREAKS, trmean f=4: BREAKS, mkrum f=4: BREAKS
M2_orc1: cwmed f=2: HOLDS, trmean f=2: HOLDS, mkrum f=2: HOLDS, cwmed f=4: HOLDS, trmean f=4: HOLDS, mkrum f=4: HOLDS
M2_orc10: cwmed f=2: BREAKS, trmean f=2: BREAKS, mkrum f=2: BREAKS, cwmed f=4: BREAKS, trmean f=4: BREAKS, mkrum f=4: BREAKS
M2_orcinf: cwmed f=2: BREAKS, trmean f=2: BREAKS, mkrum f=2: BREAKS, cwmed f=4: BREAKS, trmean f=4: BREAKS, mkrum f=4: BREAKS
M2_elect: cwmed f=2: HOLDS, trmean f=2: BREAKS, mkrum f=2: HOLDS, cwmed f=4: BREAKS, trmean f=4: BREAKS, mkrum f=4: BREAKS
M2_verify: cwmed f=2: BREAKS, trmean f=2: BREAKS, mkrum f=2: BREAKS, cwmed f=4: BREAKS, trmean f=4: BREAKS, mkrum f=4: BREAKS
FRONTIER: NO_SAFE_POINT (every candidate that restores coverage lets liars in)
```


## Botnet | verdicts
```
M0: WALL_TRACKS_FHAT
M1_orc1: NO_EFFECT+HARM
M1_orc10: REMOVES_TAX
M1_orcinf: REMOVES_TAX
M1_elect: NO_EFFECT
M1_verify: NO_EFFECT
M1_loud: NO_EFFECT
M1_probeonly: REMOVES_TAX
identity: IDENTITY_MATTERS
rr_rr3inf: CHEAP
rr_electrr1: MIXED
rr_electrr3: CHEAP
floor_flags: 0
witness_dist_over_tau: {'cwmed': 1.5, 'mkrum': 1.7, 'trmean': 1.6}
M2_base: cwmed f=2: HOLDS, trmean f=2: HOLDS, mkrum f=2: HOLDS, cwmed f=4: HOLDS, trmean f=4: BREAKS, mkrum f=4: BREAKS
M2_orc1: cwmed f=2: HOLDS, trmean f=2: HOLDS, mkrum f=2: HOLDS, cwmed f=4: HOLDS, trmean f=4: HOLDS, mkrum f=4: HOLDS
M2_orc10: cwmed f=2: BREAKS, trmean f=2: BREAKS, mkrum f=2: BREAKS, cwmed f=4: BREAKS, trmean f=4: BREAKS, mkrum f=4: BREAKS
M2_orcinf: cwmed f=2: BREAKS, trmean f=2: BREAKS, mkrum f=2: BREAKS, cwmed f=4: BREAKS, trmean f=4: BREAKS, mkrum f=4: BREAKS
M2_elect: cwmed f=2: HOLDS, trmean f=2: HOLDS, mkrum f=2: HOLDS, cwmed f=4: HOLDS, trmean f=4: BREAKS, mkrum f=4: BREAKS
M2_verify: cwmed f=2: BREAKS, trmean f=2: BREAKS, mkrum f=2: BREAKS, cwmed f=4: BREAKS, trmean f=4: BREAKS, mkrum f=4: BREAKS
FRONTIER: NO_SAFE_POINT (every candidate that restores coverage lets liars in)
```


## Brute Force | M0 wall edge vs F_HAT (f=0, learnable line 0.8x ref = 0.800)
```
      agg    fhat  k*(R)   k*(2R) k*(3R) wall_edge(<=k)
   trmean       1      2        2      2              1
   trmean       2      3        3      3              2
   trmean       3      4        4      4              3
   trmean       4      5        5      5              4
   trmean verdict TRACKS rho=1.00                      
    mkrum       1      3        2      2              1
    mkrum       2      4        3      3              2
    mkrum       3      5        4      4              3
    mkrum       4      6        5      5              4
    mkrum verdict TRACKS rho=1.00                      
nnm_cwmed       1      3        2      2              1
nnm_cwmed       2      4        3      3              2
nnm_cwmed       3      5        4      4              3
nnm_cwmed       4      6        5      5              4
nnm_cwmed verdict TRACKS rho=1.00                      

OVERALL: WALL_TRACKS_FHAT
Controls by construction: cwmed, geomed, cclip, bucket_cwmed do not use F_HAT, so their v3.2 walls
cannot be explained by this lever (report them separately).
```


## Brute Force | M1 k* (tax vs floor f+1) by arm  ['never' -> lower bound; grid k=[1, 2, 3, 4, 6, 8]]
  verdicts below use the robustness tax = k*(agg, arm) - k*(FedAvg, same f)
```
 f    agg          base      orc1     orc10    orcinf   randinf    rr3inf     elect  electrr1  electrr3          loud     verify  probeonly
 0 fedavg     1 (tax 0)                                                                                                                    
 0  cwmed never (tax 8) 4 (tax 3) 1 (tax 0) 1 (tax 0) 8 (tax 7) 1 (tax 0) 1 (tax 0) 8 (tax 7) 3 (tax 2) never (tax 8)  1 (tax 0)  1 (tax 0)
 0 trmean     3 (tax 2) 4 (tax 3) 1 (tax 0) 1 (tax 0) 3 (tax 2) 1 (tax 0) 1 (tax 0) 6 (tax 5) 3 (tax 2)     3 (tax 2)  1 (tax 0)  1 (tax 0)
 0  mkrum     4 (tax 3) 6 (tax 5) 1 (tax 0) 1 (tax 0) 4 (tax 3) 1 (tax 0) 1 (tax 0) 6 (tax 5) 3 (tax 2)     3 (tax 2)  1 (tax 0)  1 (tax 0)
 2 fedavg     3 (tax 0)                                                                                                                    
 2  cwmed never (tax 6) 6 (tax 3) 3 (tax 0) 3 (tax 0) 8 (tax 5) 3 (tax 0) 3 (tax 0) 8 (tax 5) 4 (tax 1)     8 (tax 5) 2 (tax -1) 1 (tax -2)
 2 trmean     4 (tax 1) 6 (tax 3) 3 (tax 0) 3 (tax 0) 4 (tax 1) 3 (tax 0) 3 (tax 0) 6 (tax 3) 3 (tax 0)     3 (tax 0) 2 (tax -1) 1 (tax -2)
 2  mkrum     6 (tax 3) 8 (tax 5) 3 (tax 0) 3 (tax 0) 6 (tax 3) 3 (tax 0) 4 (tax 1) 6 (tax 3) 4 (tax 1)     3 (tax 0)  3 (tax 0) 1 (tax -2)
```


## Brute Force | M1 verification acceptance rates (share of rounds accepted, by true role)
```
   verify_acc_witness  verify_acc_honest  verify_acc_attacker
f                                                            
0               0.947                0.0                  NaN
2               0.937                0.0                  0.0
```


## Brute Force | M1 k=0 control (no witnesses at all): target recall
```
agg        cwmed  mkrum  trmean
arm                            
base         0.0    0.0     0.0
probeonly    1.0    1.0     1.0
verify       0.0    0.0     0.0
verdict: PROBE_ALONE_DETECTS
```


## Brute Force | M1 verdicts
```
orc1      (waa, lambda=1) : NO_EFFECT+HARM
orc10     (waa, lambda=10) : REMOVES_TAX
orcinf    (waa, lambda=inf) : REMOVES_TAX
elect     (elect) : REMOVES_TAX
verify    (verify) : REMOVES_TAX
loud      (loud) : NO_EFFECT
probeonly (server) : REMOVES_TAX
  (loud is the client-side control; predicted NO_EFFECT: robust rules count votes, not volume)
  (probeonly is the trap control: if it matches verify, verification adds nothing)
identity control (WAA lambda=inf) : IDENTITY_MATTERS   (rand = same number of members routed, chosen at random)
randomized response rr3inf vs orcinf : CHEAP
randomized response electrr1 vs elect : COSTLY
randomized response electrr3 vs elect : MIXED
honest witness distance / honest radius tau (median, oracle lambda=inf): {'cwmed': 1.7, 'mkrum': 1.9, 'trmean': 1.8}
floor violations    : none (oracle never beats k > f -- consistent with P1)
worst oracle cell   : cwmed f=0 tax=0
```


## Brute Force | M1 collateral at f=0, k=6 (what else moves when WAA is on)
```
                  benign_fpr  other_attack_recall_mean  other_attack_recall_min  recall_Normal  recall_DoS  recall_DDoS  recall_Portscan  recall_Botnet  recall_Web Attack
agg    arm                                                                                                                                                                
cwmed  base            0.003                     0.948                    0.802          0.997       0.997        0.996              NaN          0.998              0.802
       elect           0.003                     0.925                    0.706          0.997       0.997        0.996              NaN          0.998              0.706
       electrr1        0.003                     0.948                    0.800          0.997       0.997        0.996              NaN          0.998              0.800
       electrr3        0.003                     0.925                    0.706          0.997       0.997        0.996              NaN          0.998              0.706
       loud            0.003                     0.926                    0.712          0.997       0.997        0.996              NaN          0.998              0.712
       orc1            0.003                     0.960                    0.847          0.997       0.997        0.997              NaN          0.998              0.847
       orc10           0.003                     0.931                    0.730          0.997       0.997        0.997              NaN          0.998              0.730
       orcinf          0.003                     0.931                    0.730          0.997       0.997        0.997              NaN          0.998              0.730
       probeonly       0.002                     0.846                    0.395          0.998       0.997        0.996              NaN          0.998              0.395
       randinf         0.003                     0.961                    0.853          0.997       0.997        0.997              NaN          0.999              0.853
       rr3inf          0.003                     0.934                    0.744          0.997       0.997        0.997              NaN          0.998              0.744
       verify          0.003                     0.910                    0.647          0.997       0.997        0.996              NaN          0.998              0.647
fedavg base            0.003                     0.961                    0.849          0.997       0.998        0.998              NaN          1.000              0.849
mkrum  base            0.003                     0.961                    0.849          0.997       0.998        0.997              NaN          1.000              0.849
       elect           0.003                     0.925                    0.706          0.997       0.998        0.997              NaN          0.999              0.706
       electrr1        0.003                     0.961                    0.849          0.997       0.998        0.997              NaN          0.999              0.849
       electrr3        0.003                     0.925                    0.706          0.997       0.998        0.997              NaN          0.999              0.706
       loud            0.003                     0.960                    0.847          0.997       0.998        0.997              NaN          1.000              0.847
       orc1            0.003                     0.961                    0.849          0.997       0.998        0.997              NaN          0.999              0.849
       orc10           0.003                     0.961                    0.849          0.997       0.998        0.997              NaN          0.999              0.849
       orcinf          0.003                     0.961                    0.849          0.997       0.998        0.997              NaN          0.999              0.849
       probeonly       0.002                     0.924                    0.700          0.998       0.998        0.997              NaN          0.999              0.700
       randinf         0.003                     0.961                    0.849          0.997       0.998        0.997              NaN          0.999              0.849
       rr3inf          0.003                     0.961                    0.849          0.997       0.998        0.997              NaN          0.999              0.849
       verify          0.003                     0.925                    0.706          0.997       0.998        0.997              NaN          0.999              0.706
trmean base            0.003                     0.938                    0.760          0.997       0.998        0.997              NaN          0.998              0.760
       elect           0.003                     0.925                    0.706          0.997       0.998        0.997              NaN          0.999              0.706
       electrr1        0.003                     0.925                    0.708          0.997       0.998        0.997              NaN          0.998              0.708
       electrr3        0.003                     0.925                    0.706          0.997       0.998        0.997              NaN          0.999              0.706
       loud            0.003                     0.959                    0.845          0.997       0.998        0.997              NaN          0.998              0.845
       orc1            0.003                     0.961                    0.851          0.997       0.998        0.997              NaN          0.999              0.851
       orc10           0.003                     0.939                    0.764          0.997       0.998        0.997              NaN          0.998              0.764
       orcinf          0.003                     0.939                    0.764          0.997       0.998        0.997              NaN          0.998              0.764
       probeonly       0.002                     0.919                    0.685          0.998       0.997        0.997              NaN          0.998              0.685
       randinf         0.003                     0.944                    0.784          0.997       0.998        0.997              NaN          0.999              0.784
       rr3inf          0.003                     0.940                    0.768          0.997       0.998        0.997              NaN          0.998              0.768
       verify          0.003                     0.925                    0.706          0.997       0.998        0.997              NaN          0.999              0.706
```


## Brute Force | M2 sign-flip x10, k=6  (clean FedAvg f=0: FPR 0.003, other 0.961)
```
 f    agg    arm  benign_fpr  other_mean  other_min        verdict
 2 fedavg   base       1.000       0.167      0.000 (attack check)
 2  cwmed   base       0.004       0.959      0.845          HOLDS
 2  cwmed   orc1       0.004       0.959      0.845          HOLDS
 2  cwmed  orc10       0.009       0.743      0.000         BREAKS
 2  cwmed orcinf       0.546       0.083      0.000         BREAKS
 2  cwmed  elect       0.004       0.924      0.704          HOLDS
 2  cwmed verify       1.000       0.000      0.000         BREAKS
 2 trmean   base       0.004       0.960      0.845          HOLDS
 2 trmean   orc1       0.004       0.960      0.847          HOLDS
 2 trmean  orc10       0.009       0.743      0.000         BREAKS
 2 trmean orcinf       0.643       0.042      0.000         BREAKS
 2 trmean  elect       0.004       0.906      0.629         BREAKS
 2 trmean verify       1.000       0.000      0.000         BREAKS
 2  mkrum   base       0.003       0.961      0.847          HOLDS
 2  mkrum   orc1       0.004       0.960      0.845          HOLDS
 2  mkrum  orc10       0.008       0.744      0.000         BREAKS
 2  mkrum orcinf       0.864       0.083      0.000         BREAKS
 2  mkrum  elect       0.003       0.962      0.851          HOLDS
 2  mkrum verify       1.000       0.000      0.000         BREAKS
 4 fedavg   base       0.709       0.123      0.000 (attack check)
 4  cwmed   base       0.005       0.899      0.607         BREAKS
 4  cwmed   orc1       0.005       0.959      0.845          HOLDS
 4  cwmed  orc10       0.009       0.636      0.000         BREAKS
 4  cwmed orcinf       0.344       0.132      0.000         BREAKS
 4  cwmed  elect       0.005       0.783      0.141         BREAKS
 4  cwmed verify       0.682       0.000      0.000         BREAKS
 4 trmean   base       0.742       0.167      0.000         BREAKS
 4 trmean   orc1       0.004       0.959      0.847          HOLDS
 4 trmean  orc10       0.009       0.701      0.000         BREAKS
 4 trmean orcinf       0.667       0.084      0.000         BREAKS
 4 trmean  elect       0.557       0.089      0.000         BREAKS
 4 trmean verify       0.345       0.083      0.000         BREAKS
 4  mkrum   base       0.643       0.166      0.000         BREAKS
 4  mkrum   orc1       0.004       0.960      0.847          HOLDS
 4  mkrum  orc10       0.009       0.701      0.000         BREAKS
 4  mkrum orcinf       0.357       0.000      0.000         BREAKS
 4  mkrum  elect       0.654       0.167      0.000         BREAKS
 4  mkrum verify       0.667       0.167      0.000         BREAKS
```


## Botnet | M0 wall edge vs F_HAT (f=0, learnable line 0.8x ref = 0.796)
```
      agg    fhat  k*(R)   k*(2R) k*(3R) wall_edge(<=k)
   trmean       1      3        2      2              1
   trmean       2      4        3      3              2
   trmean       3      4        4      4              3
   trmean       4      5        5      5              4
   trmean verdict TRACKS rho=1.00                      
    mkrum       1      3        2      2              1
    mkrum       2      4        3      3              2
    mkrum       3      5        4      4              3
    mkrum       4      6        5      5              4
    mkrum verdict TRACKS rho=1.00                      
nnm_cwmed       1      3        2      2              1
nnm_cwmed       2      4        3      3              2
nnm_cwmed       3      5        4      4              3
nnm_cwmed       4      6        5      5              4
nnm_cwmed verdict TRACKS rho=1.00                      

OVERALL: WALL_TRACKS_FHAT
Controls by construction: cwmed, geomed, cclip, bucket_cwmed do not use F_HAT, so their v3.2 walls
cannot be explained by this lever (report them separately).
```


## Botnet | M1 k* (tax vs floor f+1) by arm  ['never' -> lower bound; grid k=[1, 2, 3, 4, 6, 8]]
  verdicts below use the robustness tax = k*(agg, arm) - k*(FedAvg, same f)
```
 f    agg          base      orc1     orc10    orcinf   randinf    rr3inf     elect  electrr1  electrr3          loud    verify  probeonly
 0 fedavg     2 (tax 1)                                                                                                                   
 0  cwmed never (tax 8) 4 (tax 3) 2 (tax 1) 2 (tax 1) 8 (tax 7) 2 (tax 1) 6 (tax 5) 8 (tax 7) 6 (tax 5)     8 (tax 7) 6 (tax 5)  1 (tax 0)
 0 trmean     4 (tax 3) 6 (tax 5) 2 (tax 1) 2 (tax 1) 3 (tax 2) 2 (tax 1) 3 (tax 2) 4 (tax 3) 3 (tax 2)     3 (tax 2) 3 (tax 2)  1 (tax 0)
 0  mkrum     4 (tax 3) 6 (tax 5) 2 (tax 1) 2 (tax 1) 4 (tax 3) 2 (tax 1) 3 (tax 2) 4 (tax 3) 4 (tax 3)     3 (tax 2) 3 (tax 2)  1 (tax 0)
 2 fedavg     4 (tax 1)                                                                                                                   
 2  cwmed never (tax 6) 8 (tax 5) 4 (tax 1) 4 (tax 1) 8 (tax 5) 4 (tax 1) 6 (tax 3) 8 (tax 5) 6 (tax 3) never (tax 6) 6 (tax 3) 1 (tax -2)
 2 trmean     4 (tax 1) 8 (tax 5) 4 (tax 1) 4 (tax 1) 6 (tax 3) 4 (tax 1) 3 (tax 0) 6 (tax 3) 4 (tax 1)     3 (tax 0) 3 (tax 0) 1 (tax -2)
 2  mkrum     6 (tax 3) 8 (tax 5) 4 (tax 1) 4 (tax 1) 6 (tax 3) 6 (tax 3) 6 (tax 3) 6 (tax 3) 6 (tax 3)     3 (tax 0) 6 (tax 3) 1 (tax -2)
```


## Botnet | M1 verification acceptance rates (share of rounds accepted, by true role)
```
   verify_acc_witness  verify_acc_honest  verify_acc_attacker
f                                                            
0               0.927                0.0                  NaN
2               0.899                0.0                  0.0
```


## Botnet | M1 k=0 control (no witnesses at all): target recall
```
agg        cwmed  mkrum  trmean
arm                            
base       0.000  0.000   0.000
probeonly  0.995  0.995   0.995
verify     0.000  0.000   0.000
verdict: PROBE_ALONE_DETECTS
```


## Botnet | M1 verdicts
```
orc1      (waa, lambda=1) : NO_EFFECT+HARM
orc10     (waa, lambda=10) : REMOVES_TAX
orcinf    (waa, lambda=inf) : REMOVES_TAX
elect     (elect) : NO_EFFECT
verify    (verify) : NO_EFFECT
loud      (loud) : NO_EFFECT
probeonly (server) : REMOVES_TAX
  (loud is the client-side control; predicted NO_EFFECT: robust rules count votes, not volume)
  (probeonly is the trap control: if it matches verify, verification adds nothing)
identity control (WAA lambda=inf) : IDENTITY_MATTERS   (rand = same number of members routed, chosen at random)
randomized response rr3inf vs orcinf : CHEAP
randomized response electrr1 vs elect : MIXED
randomized response electrr3 vs elect : CHEAP
honest witness distance / honest radius tau (median, oracle lambda=inf): {'cwmed': 1.5, 'mkrum': 1.7, 'trmean': 1.6}
floor violations    : none (oracle never beats k > f -- consistent with P1)
worst oracle cell   : cwmed f=0 tax=0
```


## Botnet | M1 collateral at f=0, k=6 (what else moves when WAA is on)
```
                  benign_fpr  other_attack_recall_mean  other_attack_recall_min  recall_Normal  recall_DoS  recall_DDoS  recall_Portscan  recall_Brute Force  recall_Web Attack
agg    arm                                                                                                                                                                     
cwmed  base            0.001                     0.960                    0.845          0.999       0.998        0.997              NaN                 1.0              0.845
       elect           0.001                     0.961                    0.849          0.999       0.998        0.996              NaN                 1.0              0.849
       electrr1        0.001                     0.961                    0.849          0.999       0.998        0.997              NaN                 1.0              0.849
       electrr3        0.001                     0.961                    0.849          0.999       0.998        0.996              NaN                 1.0              0.849
       loud            0.001                     0.960                    0.845          0.999       0.998        0.997              NaN                 1.0              0.845
       orc1            0.001                     0.961                    0.849          0.999       0.998        0.997              NaN                 1.0              0.849
       orc10           0.001                     0.961                    0.849          0.999       0.998        0.998              NaN                 1.0              0.849
       orcinf          0.001                     0.961                    0.849          0.999       0.998        0.998              NaN                 1.0              0.849
       probeonly       0.001                     0.960                    0.845          0.999       0.998        0.996              NaN                 1.0              0.845
       randinf         0.001                     0.960                    0.845          0.999       0.998        0.998              NaN                 1.0              0.845
       rr3inf          0.001                     0.961                    0.849          0.999       0.998        0.997              NaN                 1.0              0.849
       verify          0.001                     0.961                    0.849          0.999       0.998        0.996              NaN                 1.0              0.849
fedavg base            0.001                     0.963                    0.855          0.999       0.999        0.998              NaN                 1.0              0.855
mkrum  base            0.001                     0.961                    0.847          0.999       0.999        0.998              NaN                 1.0              0.847
       elect           0.001                     0.962                    0.851          0.999       0.999        0.998              NaN                 1.0              0.851
       electrr1        0.001                     0.962                    0.849          0.999       0.999        0.998              NaN                 1.0              0.849
       electrr3        0.001                     0.962                    0.851          0.999       0.999        0.998              NaN                 1.0              0.851
       loud            0.001                     0.962                    0.849          0.999       0.999        0.998              NaN                 1.0              0.849
       orc1            0.001                     0.961                    0.847          0.999       0.998        0.998              NaN                 1.0              0.847
       orc10           0.001                     0.961                    0.847          0.999       0.999        0.998              NaN                 1.0              0.847
       orcinf          0.001                     0.961                    0.847          0.999       0.999        0.998              NaN                 1.0              0.847
       probeonly       0.001                     0.961                    0.849          0.999       0.999        0.998              NaN                 1.0              0.849
       randinf         0.001                     0.962                    0.849          0.999       0.999        0.998              NaN                 1.0              0.849
       rr3inf          0.001                     0.961                    0.847          0.999       0.999        0.998              NaN                 1.0              0.847
       verify          0.001                     0.962                    0.851          0.999       0.999        0.998              NaN                 1.0              0.851
trmean base            0.001                     0.962                    0.849          0.999       0.999        0.998              NaN                 1.0              0.849
       elect           0.001                     0.962                    0.851          0.999       0.999        0.998              NaN                 1.0              0.851
       electrr1        0.001                     0.962                    0.851          0.999       0.999        0.998              NaN                 1.0              0.851
       electrr3        0.001                     0.962                    0.851          0.999       0.999        0.998              NaN                 1.0              0.851
       loud            0.001                     0.961                    0.849          0.999       0.999        0.998              NaN                 1.0              0.849
       orc1            0.001                     0.961                    0.849          0.999       0.998        0.998              NaN                 1.0              0.849
       orc10           0.001                     0.962                    0.849          0.999       0.999        0.998              NaN                 1.0              0.849
       orcinf          0.001                     0.962                    0.849          0.999       0.999        0.998              NaN                 1.0              0.849
       probeonly       0.001                     0.961                    0.849          0.999       0.999        0.998              NaN                 1.0              0.849
       randinf         0.001                     0.962                    0.849          0.999       0.999        0.998              NaN                 1.0              0.849
       rr3inf          0.001                     0.962                    0.849          0.999       0.999        0.998              NaN                 1.0              0.849
       verify          0.001                     0.962                    0.851          0.999       0.999        0.998              NaN                 1.0              0.851
```


## Botnet | M2 sign-flip x10, k=6  (clean FedAvg f=0: FPR 0.001, other 0.963)
```
 f    agg    arm  benign_fpr  other_mean  other_min        verdict
 2 fedavg   base       0.984       0.300      0.000 (attack check)
 2  cwmed   base       0.001       0.960      0.847          HOLDS
 2  cwmed   orc1       0.001       0.960      0.847          HOLDS
 2  cwmed  orc10       0.010       0.744      0.000         BREAKS
 2  cwmed orcinf       0.859       0.166      0.000         BREAKS
 2  cwmed  elect       0.001       0.961      0.849          HOLDS
 2  cwmed verify       1.000       0.000      0.000         BREAKS
 2 trmean   base       0.001       0.960      0.847          HOLDS
 2 trmean   orc1       0.001       0.961      0.847          HOLDS
 2 trmean  orc10       0.009       0.744      0.000         BREAKS
 2 trmean orcinf       0.815       0.166      0.000         BREAKS
 2 trmean  elect       0.001       0.962      0.853          HOLDS
 2 trmean verify       1.000       0.000      0.000         BREAKS
 2  mkrum   base       0.001       0.965      0.863          HOLDS
 2  mkrum   orc1       0.001       0.964      0.859          HOLDS
 2  mkrum  orc10       0.009       0.744      0.000         BREAKS
 2  mkrum orcinf       0.667       0.083      0.000         BREAKS
 2  mkrum  elect       0.001       0.965      0.863          HOLDS
 2  mkrum verify       1.000       0.000      0.000         BREAKS
 4 fedavg   base       0.667       0.167      0.000 (attack check)
 4  cwmed   base       0.001       0.960      0.845          HOLDS
 4  cwmed   orc1       0.001       0.960      0.845          HOLDS
 4  cwmed  orc10       0.008       0.526      0.000         BREAKS
 4  cwmed orcinf       0.719       0.166      0.000         BREAKS
 4  cwmed  elect       0.001       0.960      0.845          HOLDS
 4  cwmed verify       1.000       0.000      0.000         BREAKS
 4 trmean   base       0.333       0.083      0.000         BREAKS
 4 trmean   orc1       0.001       0.960      0.845          HOLDS
 4 trmean  orc10       0.009       0.684      0.000         BREAKS
 4 trmean orcinf       0.333       0.083      0.000         BREAKS
 4 trmean  elect       0.333       0.083      0.000         BREAKS
 4 trmean verify       0.667       0.167      0.000         BREAKS
 4  mkrum   base       0.665       0.167      0.000         BREAKS
 4  mkrum   orc1       0.001       0.960      0.845          HOLDS
 4  mkrum  orc10       0.015       0.578      0.000         BREAKS
 4  mkrum orcinf       0.784       0.166      0.000         BREAKS
 4  mkrum  elect       0.667       0.167      0.000         BREAKS
 4  mkrum verify       0.667       0.083      0.000         BREAKS
```
