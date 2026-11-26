# PEV_L_RECORDS_v1: certified Pev entries on S8's L graph (option B; the P0_LOG rows 4409, 4422, 4435)

Written by pk23 at 2026-11-21T15:08:25Z (date -u) with pk23/pev/make_pev_summary_v1.py (sha256 716d2388eb76ea0c). Every number below is read from the six records or computed from them by that script in exact rational arithmetic, rounded outward.

## 1. What the records certify
- The entries are <psi_0, T M_e^k T psi_0> / lambda_0^2 for k = 0, 1, 2, on S8's L graph [vac|int|int|vac] (12 vertices), with
  xi^k on the middle bond: h = (4,7) (graph LH, keys Mh,0,0 and Mhh,0,0) and t = (3,6) (graph LT, keys Mt,0,0 and Mtt,0,0); k = 0 is
  TT,0,0 on L. TTh,0,0 is TT on LH, a control. psi_0 is state 0 of the z9sym trial set, the TRIAL_SET of pk25/mr/v3/MR_LEMMAP.kv.
- The records' claim (one text in all six): "for every J >= J_REF, t = 1/J, t = 0 included: I(J)/main(J) lies in sum_k [ak_k - ak_rad_k, ak_k + ak_rad_k] t^k + [-sum Bp, sum Bp] (Lemma U: PLAN_M3_CODE_v1 l.125, v1_2 U4)". Here t = 1/J and J_REF = 300.

## 2. Records

| record | sha256 | N | graph | keys |
|---|---|---|---|---|
| m3_hl_L_N4_J300_hl.json | c4bee75a7b224a4893b33138a9d7d6de5c76fa3ae18ac1ba5cdd09d03d700a7d | 4 | L | TT,0,0 |
| m3_hl_LH_N4_J300_hl.json | cb539044caeacfcb72aa70cddcf332a026d1f388cb6e51be72e8bee72b0b9bbb | 4 | LH | Mh,0,0, Mhh,0,0, TTh,0,0 |
| m3_hl_LT_N4_J300_hl.json | a14b76056962fc35cae228064863c0297faed269a12e0030b11279bc3c7f6ead | 4 | LT | Mt,0,0, Mtt,0,0 |
| m3_hl_L_N3_J300_hl.json | 2926e9fe24a6ce8b3b9a7b6021b9c3f5a049b5142b2c52ac23377f5b5e1218e6 | 3 | L | TT,0,0 |
| m3_hl_LH_N3_J300_hl.json | b7d03024fdda4c5e522b01621ee377b87a6fe5ff02ca5f33d5908531b313742f | 3 | LH | Mh,0,0, Mhh,0,0, TTh,0,0 |
| m3_hl_LT_N3_J300_hl.json | 4137b0548286aae88384cb2a8594704264bcca7dfdca385831b256ce63ce3cb2 | 3 | LT | Mt,0,0, Mtt,0,0 |

Runner pk23/pev/m3_run_v1_9_3_hl_v1.py (sha256 2c81e6bc439d8fa8aa0f7cf782c6a3bad3f6fa1ea22610031d1ddde149b240b7); entry list pk23/pev/HL_ENTRY_LIST_v1.json (sha256 2d115b6de96e5d8da01bb20ca11ccda6c7d650eb74faed1262f24be619e3ed42).

Checks by this script (trial set = MR_LEMMAP.kv TRIAL_SET for N; entry list and runner by sha256; keys = the list's keys of the graph; J_REF 300, N, graph and format): m3_hl_L_N4_J300_hl.json PASS, m3_hl_LH_N4_J300_hl.json PASS, m3_hl_LT_N4_J300_hl.json PASS, m3_hl_L_N3_J300_hl.json PASS, m3_hl_LH_N3_J300_hl.json PASS, m3_hl_LT_N3_J300_hl.json PASS.

## 3. Values at N = 4

Columns: a_k as mid +- rad; sum Bp; the enclosure of I(J)/main(J) at J = 300; the enclosure for every J >= 300 (t in [0, 1/300], each a_k t^k between 0 and its value at t = 1/300); the exact order-0 value (Gaussian free field of the infinite 3-row strip, as in rtwin_hl_v1's C-T0) and a_0 minus it (float).

| key | bond, k | a_0 | a_1 | a_2 | a_3 | sum Bp | at J = 300 | every J >= 300 | exact a_0 | a_0 - exact |
|---|---|---|---|---|---|---|---|---|---|---|
| TT,0,0 | -, 0 | 1 +- 0.0e+00 | 1.994023698088 +- 3.6e-13 | 3.098890043689 +- 6.3e-11 | 4.304426704022 +- 1.4e-08 | 0.00000545008762173 | [1.00667588710, 1.00668678729] | [0.999994549912, 1.00668678729] | 1.0000000000000 | 0.00e+00 |
| Mh,0,0 | h (4,7), 1 | 0.845346329292 +- 6.0e-15 | 1.785420864597 +- 1.3e-12 | 2.89305368805 +- 3.3e-10 | 4.1652153607 +- 9.4e-08 | 0.00000639560441505 | [0.851323635877, 0.851336427087] | [0.845339933687, 0.851336427087] | 0.8453463292920 | 0.00e+00 |
| Mhh,0,0 | h (4,7), 2 | 1.191017360746 +- 1.1e-14 | 2.568748712911 +- 4.9e-12 | 4.244872058198 +- 1.8e-09 | 6.229123616101 +- 6.6e-07 | 0.0000167777620063 | [1.19961047464, 1.19964403018] | [1.19100058298, 1.19964403018] | 1.1910173607458 | 0.00e+00 |
| TTh,0,0 | - (control on LH), 0 | 1 +- 0.0e+00 | 1.994023698088 +- 3.6e-13 | 3.098890043689 +- 6.3e-11 | 4.304426704022 +- 1.4e-08 | 0.00000545008762173 | [1.00667588710, 1.00668678729] | [0.999994549912, 1.00668678729] | 1.0000000000000 | 0.00e+00 |
| Mt,0,0 | t (3,6), 1 | 1.000926385698 +- 7.1e-15 | 2.026383823043 +- 1.6e-12 | 3.16862789476 +- 4.0e-10 | 4.404710669919 +- 1.1e-07 | 0.00000782342260857 | [1.00770854513, 1.00772419198] | [1.00091856227, 1.00772419198] | 1.0009263856980 | 0.00e+00 |
| Mtt,0,0 | t (3,6), 2 | 1.669756049311 +- 1.6e-14 | 3.317653462377 +- 7.0e-12 | 5.073215953392 +- 2.5e-09 | 6.844055668336 +- 9.4e-07 | 0.0000269256510168 | [1.68084459108, 1.68089844239] | [1.66972912365, 1.68089844239] | 1.6697560493109 | -2.22e-16 |

Ratios to TT,0,0 at J = 300 (enclosures from the J = 300 columns, all positive): TTh,0,0 / TT,0,0 in [0.999989172227, 1.00001082789]; Mh,0,0 / TT,0,0 in [0.845668828311, 0.845690691503]; Mhh,0,0 / TT,0,0 in [1.19164221662, 1.19168845260]; Mt,0,0 / TT,0,0 in [1.00101497095, 1.00104135292]; Mtt,0,0 / TT,0,0 in [1.66967979744, 1.66975137074].

## 4. Values at N = 3

Columns: a_k as mid +- rad; sum Bp; the enclosure of I(J)/main(J) at J = 300; the enclosure for every J >= 300 (t in [0, 1/300], each a_k t^k between 0 and its value at t = 1/300); the exact order-0 value (Gaussian free field of the infinite 3-row strip, as in rtwin_hl_v1's C-T0) and a_0 minus it (float).

| key | bond, k | a_0 | a_1 | a_2 | a_3 | sum Bp | at J = 300 | every J >= 300 | exact a_0 | a_0 - exact |
|---|---|---|---|---|---|---|---|---|---|---|
| TT,0,0 | -, 0 | 1 +- 0.0e+00 | 1.550829051181 +- 2.1e-13 | 1.888434866338 +- 2.8e-11 | 2.16831833301 +- 5.3e-09 | 0.00000258677952512 | [1.00518790630, 1.00519307987] | [0.999997413220, 1.00519307987] | 1.0000000000000 | 0.00e+00 |
| Mh,0,0 | h (4,7), 1 | 0.563564219528 +- 4.0e-15 | 0.9492531528259 +- 6.7e-13 | 1.233527413422 +- 1.4e-10 | 1.495868441629 +- 3.3e-08 | 0.00000234794817107 | [0.566739810018, 0.566744505915] | [0.563561871579, 0.566744505915] | 0.5635642195280 | 0.00e+00 |
| Mhh,0,0 | h (4,7), 2 | 0.6352092590644 +- 6.1e-15 | 1.108182929434 +- 2.2e-12 | 1.493698074031 +- 6.7e-10 | 1.881060303346 +- 2.2e-07 | 0.00000567594084026 | [0.638914192535, 0.638925544418] | [0.635203583123, 0.638925544418] | 0.6352092590644 | 0.00e+00 |
| TTh,0,0 | - (control on LH), 0 | 1 +- 0.0e+00 | 1.550829051181 +- 2.1e-13 | 1.888434866338 +- 2.8e-11 | 2.16831833301 +- 5.3e-09 | 0.00000258677952512 | [1.00518790630, 1.00519307987] | [0.999997413220, 1.00519307987] | 1.0000000000000 | 0.00e+00 |
| Mt,0,0 | t (3,6), 1 | 0.667284257132 +- 4.7e-15 | 1.095817616284 +- 8.0e-13 | 1.395090628543 +- 1.6e-10 | 1.661989345781 +- 4.0e-08 | 0.00000291545768665 | [0.670949629624, 0.670955460540] | [0.667281341674, 0.670955460540] | 0.6672842571320 | 0.00e+00 |
| Mtt,0,0 | t (3,6), 2 | 0.8905365596325 +- 8.6e-15 | 1.48318619478 +- 3.1e-12 | 1.914450670368 +- 9.6e-10 | 2.310214828305 +- 3.2e-07 | 0.00000961610328168 | [0.895492254749, 0.895511486957] | [0.890526943529, 0.895511486957] | 0.8905365596325 | 0.00e+00 |

Ratios to TT,0,0 at J = 300 (enclosures from the J = 300 columns, all positive): TTh,0,0 / TT,0,0 in [0.999994853168, 1.00000514686]; Mh,0,0 / TT,0,0 in [0.563811889844, 0.563819463364]; Mhh,0,0 / TT,0,0 in [0.635613401377, 0.635627966083]; Mt,0,0 / TT,0,0 in [0.667483335353, 0.667492571617]; Mtt,0,0 / TT,0,0 in [0.890865916891, 0.890889634999].

