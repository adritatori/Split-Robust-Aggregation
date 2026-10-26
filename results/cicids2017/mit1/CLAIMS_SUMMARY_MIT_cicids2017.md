# Mitigation + mechanism summary -- CICIDS2017 (script mit-1.0)


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
rr_electrr1: COSTLY
rr_electrr3: CHEAP
floor_flags: 0
witness_dist_over_tau: {'cwmed': 1.4, 'mkrum': 1.5, 'trmean': 1.4}
M2_base: cwmed f=2: HOLDS, trmean f=2: HOLDS, mkrum f=2: HOLDS, cwmed f=4: HOLDS, trmean f=4: BREAKS, mkrum f=4: BREAKS
M2_orc1: cwmed f=2: HOLDS, trmean f=2: HOLDS, mkrum f=2: HOLDS, cwmed f=4: HOLDS, trmean f=4: HOLDS, mkrum f=4: HOLDS
M2_orc10: cwmed f=2: BREAKS, trmean f=2: BREAKS, mkrum f=2: BREAKS, cwmed f=4: BREAKS, trmean f=4: BREAKS, mkrum f=4: BREAKS
M2_orcinf: cwmed f=2: BREAKS, trmean f=2: BREAKS, mkrum f=2: BREAKS, cwmed f=4: BREAKS, trmean f=4: BREAKS, mkrum f=4: BREAKS
M2_elect: cwmed f=2: HOLDS, trmean f=2: HOLDS, mkrum f=2: HOLDS, cwmed f=4: HOLDS, trmean f=4: BREAKS, mkrum f=4: BREAKS
M2_verify: cwmed f=2: BREAKS, trmean f=2: BREAKS, mkrum f=2: BREAKS, cwmed f=4: BREAKS, trmean f=4: BREAKS, mkrum f=4: BREAKS
FRONTIER: NO_SAFE_POINT (every candidate that restores coverage lets liars in)
```


## Portscan | verdicts
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
witness_dist_over_tau: {'cwmed': 1.7, 'mkrum': 1.9, 'trmean': 1.8}
M2_base: cwmed f=2: HOLDS, trmean f=2: HOLDS, mkrum f=2: HOLDS, cwmed f=4: HOLDS, trmean f=4: BREAKS, mkrum f=4: BREAKS
M2_orc1: cwmed f=2: HOLDS, trmean f=2: HOLDS, mkrum f=2: HOLDS, cwmed f=4: HOLDS, trmean f=4: HOLDS, mkrum f=4: HOLDS
M2_orc10: cwmed f=2: BREAKS, trmean f=2: BREAKS, mkrum f=2: BREAKS, cwmed f=4: BREAKS, trmean f=4: BREAKS, mkrum f=4: BREAKS
M2_orcinf: cwmed f=2: BREAKS, trmean f=2: BREAKS, mkrum f=2: BREAKS, cwmed f=4: BREAKS, trmean f=4: BREAKS, mkrum f=4: BREAKS
M2_elect: cwmed f=2: HOLDS, trmean f=2: HOLDS, mkrum f=2: HOLDS, cwmed f=4: HOLDS, trmean f=4: BREAKS, mkrum f=4: BREAKS
M2_verify: cwmed f=2: BREAKS, trmean f=2: BREAKS, mkrum f=2: BREAKS, cwmed f=4: BREAKS, trmean f=4: BREAKS, mkrum f=4: BREAKS
FRONTIER: NO_SAFE_POINT (every candidate that restores coverage lets liars in)
```


## Botnet | M0 wall edge vs F_HAT (f=0, learnable line 0.8x ref = 0.754)
```
      agg    fhat  k*(R)   k*(2R) k*(3R) wall_edge(<=k)
   trmean       1      2        2      2              1
   trmean       2      3        3      3              2
   trmean       3      4        4      3              2
   trmean       4      5        4      4              3
   trmean verdict TRACKS rho=0.95                      
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
 f    agg      base      orc1     orc10    orcinf   randinf    rr3inf     elect  electrr1  electrr3      loud    verify  probeonly
 0 fedavg 1 (tax 0)                                                                                                               
 0  cwmed 8 (tax 7) 3 (tax 2) 1 (tax 0) 1 (tax 0) 4 (tax 3) 1 (tax 0) 6 (tax 5) 8 (tax 7) 6 (tax 5) 8 (tax 7) 6 (tax 5)  1 (tax 0)
 0 trmean 3 (tax 2) 4 (tax 3) 1 (tax 0) 1 (tax 0) 3 (tax 2) 1 (tax 0) 3 (tax 2) 4 (tax 3) 3 (tax 2) 3 (tax 2) 3 (tax 2)  1 (tax 0)
 0  mkrum 4 (tax 3) 4 (tax 3) 1 (tax 0) 1 (tax 0) 4 (tax 3) 3 (tax 2) 3 (tax 2) 6 (tax 5) 3 (tax 2) 3 (tax 2) 3 (tax 2)  1 (tax 0)
 2 fedavg 4 (tax 1)                                                                                                               
 2  cwmed 8 (tax 5) 6 (tax 3) 4 (tax 1) 4 (tax 1) 8 (tax 5) 4 (tax 1) 6 (tax 3) 8 (tax 5) 6 (tax 3) 8 (tax 5) 6 (tax 3) 1 (tax -2)
 2 trmean 4 (tax 1) 6 (tax 3) 4 (tax 1) 4 (tax 1) 6 (tax 3) 4 (tax 1) 4 (tax 1) 6 (tax 3) 4 (tax 1) 3 (tax 0) 4 (tax 1) 1 (tax -2)
 2  mkrum 6 (tax 3) 6 (tax 3) 4 (tax 1) 4 (tax 1) 6 (tax 3) 4 (tax 1) 4 (tax 1) 8 (tax 5) 4 (tax 1) 3 (tax 0) 4 (tax 1) 1 (tax -2)
```


## Botnet | M1 verification acceptance rates (share of rounds accepted, by true role)
```
   verify_acc_witness  verify_acc_honest  verify_acc_attacker
f                                                            
0               0.806                0.0                  NaN
2               0.808                0.0                  0.0
```


## Botnet | M1 k=0 control (no witnesses at all): target recall
```
agg        cwmed  mkrum  trmean
arm                            
base       0.000  0.000   0.000
probeonly  0.904  0.897   0.902
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
randomized response electrr1 vs elect : COSTLY
randomized response electrr3 vs elect : CHEAP
honest witness distance / honest radius tau (median, oracle lambda=inf): {'cwmed': 1.4, 'mkrum': 1.5, 'trmean': 1.4}
floor violations    : none (oracle never beats k > f -- consistent with P1)
worst oracle cell   : cwmed f=0 tax=0
```


## Botnet | M1 collateral at f=0, k=6 (what else moves when WAA is on)
```
                  benign_fpr  other_attack_recall_mean  other_attack_recall_min  recall_Normal  recall_DoS  recall_DDoS  recall_Portscan  recall_Brute Force  recall_Web Attack
agg    arm                                                                                                                                                                     
cwmed  base            0.001                     0.956                    0.871          0.999       0.997        0.999            0.919               0.994              0.871
       elect           0.001                     0.957                    0.871          0.999       0.997        0.999            0.923               0.994              0.871
       electrr1        0.001                     0.956                    0.871          0.999       0.997        0.999            0.919               0.994              0.871
       electrr3        0.001                     0.957                    0.871          0.999       0.997        0.999            0.922               0.994              0.871
       loud            0.001                     0.956                    0.871          0.999       0.997        0.999            0.918               0.993              0.871
       orc1            0.001                     0.959                    0.876          0.999       0.998        0.999            0.930               0.994              0.876
       orc10           0.001                     0.960                    0.871          0.999       0.998        0.999            0.936               0.994              0.871
       orcinf          0.001                     0.960                    0.871          0.999       0.998        0.999            0.936               0.994              0.871
       probeonly       0.001                     0.956                    0.871          0.999       0.997        0.999            0.919               0.994              0.871
       randinf         0.001                     0.959                    0.871          0.999       0.998        0.999            0.931               0.994              0.871
       rr3inf          0.001                     0.959                    0.871          0.999       0.998        0.999            0.934               0.994              0.871
       verify          0.001                     0.957                    0.871          0.999       0.997        0.999            0.923               0.994              0.871
fedavg base            0.001                     0.963                    0.882          0.999       0.998        0.999            0.941               0.995              0.882
mkrum  base            0.001                     0.964                    0.887          0.999       0.998        0.999            0.941               0.994              0.887
       elect           0.001                     0.963                    0.882          0.999       0.998        0.999            0.942               0.995              0.882
       electrr1        0.001                     0.963                    0.882          0.999       0.998        0.999            0.942               0.995              0.882
       electrr3        0.001                     0.964                    0.882          0.999       0.998        0.999            0.943               0.995              0.882
       loud            0.001                     0.961                    0.871          0.999       0.998        0.999            0.943               0.995              0.871
       orc1            0.001                     0.963                    0.882          0.999       0.998        0.999            0.940               0.994              0.882
       orc10           0.001                     0.963                    0.882          0.999       0.998        0.999            0.941               0.995              0.882
       orcinf          0.001                     0.963                    0.882          0.999       0.998        0.999            0.941               0.995              0.882
       probeonly       0.001                     0.963                    0.882          0.999       0.998        0.999            0.941               0.995              0.882
       randinf         0.001                     0.964                    0.887          0.999       0.998        0.999            0.940               0.995              0.887
       rr3inf          0.001                     0.963                    0.882          0.999       0.998        0.999            0.941               0.995              0.882
       verify          0.001                     0.963                    0.882          0.999       0.998        0.999            0.941               0.995              0.882
trmean base            0.001                     0.961                    0.876          0.999       0.998        0.999            0.939               0.994              0.876
       elect           0.001                     0.960                    0.871          0.999       0.998        0.999            0.938               0.995              0.871
       electrr1        0.001                     0.960                    0.871          0.999       0.998        0.999            0.939               0.995              0.871
       electrr3        0.001                     0.960                    0.871          0.999       0.998        0.999            0.938               0.995              0.871
       loud            0.001                     0.959                    0.871          0.999       0.998        0.999            0.933               0.994              0.871
       orc1            0.001                     0.961                    0.876          0.999       0.998        0.999            0.940               0.994              0.876
       orc10           0.001                     0.961                    0.876          0.999       0.998        0.999            0.937               0.994              0.876
       orcinf          0.001                     0.961                    0.876          0.999       0.998        0.999            0.937               0.994              0.876
       probeonly       0.001                     0.961                    0.876          0.999       0.998        0.999            0.936               0.995              0.876
       randinf         0.001                     0.962                    0.876          0.999       0.998        0.999            0.940               0.994              0.876
       rr3inf          0.001                     0.961                    0.876          0.999       0.998        0.999            0.938               0.994              0.876
       verify          0.001                     0.960                    0.871          0.999       0.998        0.999            0.939               0.995              0.871
```


## Botnet | M2 sign-flip x10, k=6  (clean FedAvg f=0: FPR 0.001, other 0.963)
```
 f    agg    arm  benign_fpr  other_mean  other_min        verdict
 2 fedavg   base       0.194       0.000      0.000 (attack check)
 2  cwmed   base       0.001       0.955      0.871          HOLDS
 2  cwmed   orc1       0.001       0.955      0.871          HOLDS
 2  cwmed  orc10       0.009       0.740      0.000         BREAKS
 2  cwmed orcinf       0.004       0.000      0.000         BREAKS
 2  cwmed  elect       0.001       0.955      0.871          HOLDS
 2  cwmed verify       1.000       0.000      0.000         BREAKS
 2 trmean   base       0.001       0.955      0.871          HOLDS
 2 trmean   orc1       0.001       0.959      0.871          HOLDS
 2 trmean  orc10       0.007       0.767      0.000         BREAKS
 2 trmean orcinf       0.333       0.000      0.000         BREAKS
 2 trmean  elect       0.001       0.957      0.871          HOLDS
 2 trmean verify       1.000       0.000      0.000         BREAKS
 2  mkrum   base       0.001       0.964      0.882          HOLDS
 2  mkrum   orc1       0.001       0.961      0.871          HOLDS
 2  mkrum  orc10       0.007       0.827      0.296         BREAKS
 2  mkrum orcinf       0.845       0.095      0.000         BREAKS
 2  mkrum  elect       0.001       0.961      0.882          HOLDS
 2  mkrum verify       1.000       0.000      0.000         BREAKS
 4 fedavg   base       0.351       0.068      0.000 (attack check)
 4  cwmed   base       0.001       0.953      0.871          HOLDS
 4  cwmed   orc1       0.001       0.958      0.871          HOLDS
 4  cwmed  orc10       0.018       0.481      0.000         BREAKS
 4  cwmed orcinf       0.320       0.066      0.000         BREAKS
 4  cwmed  elect       0.001       0.953      0.871          HOLDS
 4  cwmed verify       1.000       0.000      0.000         BREAKS
 4 trmean   base       0.771       0.132      0.000         BREAKS
 4 trmean   orc1       0.001       0.959      0.871          HOLDS
 4 trmean  orc10       0.010       0.670      0.000         BREAKS
 4 trmean orcinf       0.333       0.104      0.000         BREAKS
 4 trmean  elect       0.667       0.133      0.000         BREAKS
 4 trmean verify       0.943       0.131      0.000         BREAKS
 4  mkrum   base       0.144       0.066      0.000         BREAKS
 4  mkrum   orc1       0.001       0.961      0.871          HOLDS
 4  mkrum  orc10       0.011       0.213      0.000         BREAKS
 4  mkrum orcinf       0.667       0.134      0.000         BREAKS
 4  mkrum  elect       0.516       0.067      0.000         BREAKS
 4  mkrum verify       1.000       0.067      0.000         BREAKS
```


## Portscan | M0 wall edge vs F_HAT (f=0, learnable line 0.8x ref = 0.727)
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


## Portscan | M1 k* (tax vs floor f+1) by arm  ['never' -> lower bound; grid k=[1, 2, 3, 4, 6, 8]]
  verdicts below use the robustness tax = k*(agg, arm) - k*(FedAvg, same f)
```
 f    agg      base      orc1     orc10    orcinf   randinf    rr3inf     elect  electrr1  electrr3      loud    verify  probeonly
 0 fedavg 1 (tax 0)                                                                                                               
 0  cwmed 8 (tax 7) 3 (tax 2) 1 (tax 0) 1 (tax 0) 6 (tax 5) 1 (tax 0) 6 (tax 5) 8 (tax 7) 6 (tax 5) 8 (tax 7) 6 (tax 5)  1 (tax 0)
 0 trmean 3 (tax 2) 6 (tax 5) 1 (tax 0) 1 (tax 0) 3 (tax 2) 1 (tax 0) 3 (tax 2) 4 (tax 3) 3 (tax 2) 3 (tax 2) 3 (tax 2)  1 (tax 0)
 0  mkrum 4 (tax 3) 6 (tax 5) 1 (tax 0) 1 (tax 0) 4 (tax 3) 1 (tax 0) 3 (tax 2) 6 (tax 5) 4 (tax 3) 3 (tax 2) 3 (tax 2)  1 (tax 0)
 2 fedavg 6 (tax 3)                                                                                                               
 2  cwmed 8 (tax 5) 6 (tax 3) 6 (tax 3) 6 (tax 3) 8 (tax 5) 6 (tax 3) 8 (tax 5) 8 (tax 5) 8 (tax 5) 8 (tax 5) 8 (tax 5) 1 (tax -2)
 2 trmean 6 (tax 3) 6 (tax 3) 6 (tax 3) 6 (tax 3) 8 (tax 5) 6 (tax 3) 6 (tax 3) 6 (tax 3) 6 (tax 3) 3 (tax 0) 6 (tax 3) 1 (tax -2)
 2  mkrum 6 (tax 3) 8 (tax 5) 6 (tax 3) 6 (tax 3) 8 (tax 5) 6 (tax 3) 4 (tax 1) 6 (tax 3) 4 (tax 1) 3 (tax 0) 4 (tax 1) 1 (tax -2)
```


## Portscan | M1 verification acceptance rates (share of rounds accepted, by true role)
```
   verify_acc_witness  verify_acc_honest  verify_acc_attacker
f                                                            
0               0.656                0.0                  NaN
2               0.690                0.0                  0.0
```


## Portscan | M1 k=0 control (no witnesses at all): target recall
```
agg        cwmed  mkrum  trmean
arm                            
base       0.000  0.000   0.000
probeonly  0.893  0.888   0.888
verify     0.000  0.000   0.000
verdict: PROBE_ALONE_DETECTS
```


## Portscan | M1 verdicts
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
honest witness distance / honest radius tau (median, oracle lambda=inf): {'cwmed': 1.7, 'mkrum': 1.9, 'trmean': 1.8}
floor violations    : none (oracle never beats k > f -- consistent with P1)
worst oracle cell   : cwmed f=0 tax=0
```


## Portscan | M1 collateral at f=0, k=6 (what else moves when WAA is on)
```
                  benign_fpr  other_attack_recall_mean  other_attack_recall_min  recall_Normal  recall_DoS  recall_DDoS  recall_Brute Force  recall_Botnet  recall_Web Attack
agg    arm                                                                                                                                                                   
cwmed  base            0.001                     0.964                    0.871          0.999       0.998        0.999               0.993          0.959              0.871
       elect           0.002                     0.965                    0.871          0.998       0.998        0.999               0.993          0.964              0.871
       electrr1        0.002                     0.964                    0.871          0.998       0.998        0.999               0.992          0.959              0.871
       electrr3        0.002                     0.965                    0.871          0.998       0.998        0.999               0.993          0.964              0.871
       loud            0.001                     0.962                    0.871          0.999       0.998        0.999               0.993          0.951              0.871
       orc1            0.001                     0.966                    0.876          0.999       0.998        0.999               0.993          0.963              0.876
       orc10           0.001                     0.965                    0.871          0.999       0.998        0.999               0.993          0.961              0.871
       orcinf          0.001                     0.965                    0.871          0.999       0.998        0.999               0.993          0.962              0.871
       probeonly       0.001                     0.966                    0.871          0.999       0.998        0.999               0.993          0.967              0.871
       randinf         0.001                     0.966                    0.876          0.999       0.998        0.999               0.993          0.964              0.876
       rr3inf          0.001                     0.966                    0.876          0.999       0.998        0.999               0.993          0.961              0.876
       verify          0.002                     0.965                    0.871          0.998       0.998        0.999               0.993          0.964              0.871
fedavg base            0.001                     0.969                    0.887          0.999       0.998        0.999               0.994          0.968              0.887
mkrum  base            0.001                     0.971                    0.892          0.999       0.998        0.999               0.994          0.971              0.892
       elect           0.001                     0.969                    0.882          0.999       0.998        0.999               0.993          0.973              0.882
       electrr1        0.001                     0.969                    0.882          0.999       0.998        0.999               0.994          0.973              0.882
       electrr3        0.001                     0.969                    0.882          0.999       0.998        0.999               0.993          0.973              0.882
       loud            0.001                     0.970                    0.887          0.999       0.998        0.999               0.994          0.972              0.887
       orc1            0.001                     0.971                    0.892          0.999       0.998        0.999               0.994          0.971              0.892
       orc10           0.001                     0.968                    0.882          0.999       0.998        0.999               0.994          0.967              0.882
       orcinf          0.001                     0.968                    0.882          0.999       0.998        0.999               0.994          0.966              0.882
       probeonly       0.001                     0.970                    0.887          0.999       0.998        0.999               0.994          0.970              0.887
       randinf         0.001                     0.970                    0.887          0.999       0.998        0.999               0.994          0.970              0.887
       rr3inf          0.001                     0.968                    0.882          0.999       0.998        0.999               0.994          0.965              0.882
       verify          0.001                     0.968                    0.876          0.999       0.998        0.999               0.993          0.972              0.876
trmean base            0.001                     0.968                    0.882          0.999       0.998        0.999               0.994          0.966              0.882
       elect           0.001                     0.967                    0.876          0.999       0.998        0.999               0.993          0.970              0.876
       electrr1        0.001                     0.967                    0.876          0.999       0.998        0.999               0.994          0.969              0.876
       electrr3        0.001                     0.967                    0.876          0.999       0.998        0.999               0.993          0.970              0.876
       loud            0.001                     0.966                    0.871          0.999       0.998        0.999               0.994          0.965              0.871
       orc1            0.001                     0.968                    0.882          0.999       0.998        0.999               0.993          0.967              0.882
       orc10           0.001                     0.966                    0.876          0.999       0.998        0.999               0.994          0.964              0.876
       orcinf          0.001                     0.966                    0.876          0.999       0.998        0.999               0.994          0.964              0.876
       probeonly       0.001                     0.967                    0.876          0.999       0.998        0.999               0.994          0.968              0.876
       randinf         0.001                     0.968                    0.882          0.999       0.998        0.999               0.994          0.968              0.882
       rr3inf          0.001                     0.966                    0.876          0.999       0.998        0.999               0.994          0.964              0.876
       verify          0.001                     0.966                    0.871          0.999       0.998        0.999               0.993          0.969              0.871
```


## Portscan | M2 sign-flip x10, k=6  (clean FedAvg f=0: FPR 0.001, other 0.969)
```
 f    agg    arm  benign_fpr  other_mean  other_min        verdict
 2 fedavg   base       0.667       0.133      0.000 (attack check)
 2  cwmed   base       0.001       0.962      0.871          HOLDS
 2  cwmed   orc1       0.002       0.962      0.871          HOLDS
 2  cwmed  orc10       0.008       0.694      0.000         BREAKS
 2  cwmed orcinf       0.795       0.133      0.000         BREAKS
 2  cwmed  elect       0.001       0.961      0.871          HOLDS
 2  cwmed verify       1.000       0.000      0.000         BREAKS
 2 trmean   base       0.002       0.961      0.871          HOLDS
 2 trmean   orc1       0.002       0.962      0.871          HOLDS
 2 trmean  orc10       0.005       0.622      0.000         BREAKS
 2 trmean orcinf       0.731       0.067      0.000         BREAKS
 2 trmean  elect       0.002       0.962      0.871          HOLDS
 2 trmean verify       0.667       0.320      0.290         BREAKS
 2  mkrum   base       0.001       0.966      0.876          HOLDS
 2  mkrum   orc1       0.001       0.964      0.871          HOLDS
 2  mkrum  orc10       0.004       0.824      0.320         BREAKS
 2  mkrum orcinf       0.812       0.252      0.000         BREAKS
 2  mkrum  elect       0.001       0.966      0.876          HOLDS
 2  mkrum verify       1.000       0.000      0.000         BREAKS
 4 fedavg   base       0.333       0.067      0.000 (attack check)
 4  cwmed   base       0.002       0.962      0.871          HOLDS
 4  cwmed   orc1       0.001       0.964      0.871          HOLDS
 4  cwmed  orc10       0.003       0.442      0.000         BREAKS
 4  cwmed orcinf       0.340       0.067      0.000         BREAKS
 4  cwmed  elect       0.002       0.961      0.871          HOLDS
 4  cwmed verify       1.000       0.000      0.000         BREAKS
 4 trmean   base       0.522       0.067      0.000         BREAKS
 4 trmean   orc1       0.001       0.966      0.876          HOLDS
 4 trmean  orc10       0.005       0.644      0.000         BREAKS
 4 trmean orcinf       1.000       0.133      0.000         BREAKS
 4 trmean  elect       0.772       0.032      0.000         BREAKS
 4 trmean verify       1.000       0.200      0.000         BREAKS
 4  mkrum   base       0.125       0.067      0.000         BREAKS
 4  mkrum   orc1       0.001       0.967      0.876          HOLDS
 4  mkrum  orc10       0.007       0.371      0.005         BREAKS
 4  mkrum orcinf       0.882       0.134      0.000         BREAKS
 4  mkrum  elect       1.000       0.067      0.000         BREAKS
 4  mkrum verify       1.000       0.133      0.000         BREAKS
```
