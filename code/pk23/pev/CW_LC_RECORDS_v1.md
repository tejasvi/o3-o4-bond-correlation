# CW_LC_RECORDS_v1: certified C_w entries on the LC graph (variant B of pk25's D2_DESIGN_v1_3; the P0_LOG rows 4589, 4598, 4610)

Written by pk23 at 2026-11-21T16:17:43Z (date -u) with pk23/pev/make_cw_summary_v1.py (sha256 5eb5abfc2609d5ca). Every number below is read from the two records, their certificates and job outputs, or computed from them by that script in exact rational arithmetic, rounded outward.

## 1. What the records certify
- The entries of the (1,1) block of |Q S M_c u~_x|^2 (variant B): on the LC graph, which is S8's L graph [vac|int|int|vac] with only the
  pairs its entries use, (0,2), (9,11), (1,4), (7,10); trial state 1 of the z9sym trial set (the TRIAL_SET of pk25/mr/v3/MR_LEMMAP.kv) on
  both vac columns; xi on the outer middle-row bonds (1,4) and (7,10). The prep is L's certified D16 prep of m3_run_v1_9_3_hl_v1 (the Pev
  release), shared by C-PREP-SHARE. The entry list's notes:
  - Cxx,1,1: <M_h psi_1, S^2 M_h psi_1>: xi on the outer bonds (1,4) and (7,10)
  - Cx1,1,1: <M_h psi_1, S^2 psi_1>: xi on (1,4), next to the left psi_1
  - C1x,1,1: <psi_1, S^2 M_h psi_1>: xi on (7,10); equal to Cx1,1,1 by the left-right reflection of LC
  - C11,1,1: <psi_1, S^2 psi_1>: no insertion (TT on states 1)
- The records' claim (one text in both): "for every J >= J_REF, t = 1/J, t = 0 included: I(J)/main(J) lies in sum_k [ak_k - ak_rad_k, ak_k + ak_rad_k] t^k + [-sum Bp, sum Bp] (Lemma U: PLAN_M3_CODE_v1 l.125, v1_2 U4)". Here t = 1/J and J_REF = 300.

## 2. Records, certificates, reader

| file | sha256 | N | what |
|---|---|---|---|
| out/m3_cw_LC_N4_J300_cw.json | 96801954dfba43a8305bc7538d4409f3d47d6c3c02b8354127e6bc8c2b9515f9 | 4 | record; keys C11,1,1, C1x,1,1, Cx1,1,1, Cxx,1,1 |
| out/m3_cw_LC_N3_J300_cw.json | 1a74aa85f6ff8b1b3398633eeb92ee7a4b9924d00422797f68a9f621b0548108 | 3 | record; keys C11,1,1, C1x,1,1, Cx1,1,1, Cxx,1,1 |
| out/m3_lawcert_cw_v1_N4.json | 48affac48b501ae7cc1b5488e9a66d80fab611c82884dff7fc876fe240428fa2 | 4 | law certificate (M3_LAWCERT_v1; asm m3_run_v1_9_3_asmc.4.out 6476a33ccae73793) |
| out/m3_lawcert_cw_v1_4.out | 01961b2af4c1e6cf6d19d2a4a7eecde7deb307c5da4d4c6c52da5479220cbbba | 4 | its job output: 14 gates PASS, 51 plants FIRES, 0 not firing |
| out/m3_lawcert_cw_v1_N3.json | 66f6f89421d51d51596d2a1f389e6e930b44f3ad5476db54c7188d972be78cb7 | 3 | law certificate (M3_LAWCERT_v1; asm m3_run_v1_9_3_asmc.3.out 9dc10d04cb41a4d4) |
| out/m3_lawcert_cw_v1_3.out | b23de290777a5d935e00027d00ad5001cb83a3602653cf67087476a10eece8fd | 3 | its job output: 14 gates PASS, 51 plants FIRES, 0 not firing |

Runner pk23/pev/m3_run_v1_9_3_cw_v1.py (sha256 75966615e40424fba5a36ad6d48e3b5e9e3c5c61b3e14b3508e1e551c883e8e4); entry list pk23/pev/HL_CW_ENTRY_LIST_v1.json (sha256 93b417e7d7788fbb1d229690d8f4db1460d7fc5411231e68f67254182f0de212); law-certificate producer pk23/pev/m3_lawcert_cw_v1.py (sha256 9087afc244749905432cfe72f5b656257d6552154d363a02e99441674f2fa6c5); reader fork pk23/pev/m3_reader_cw_v1.py (sha256 876b61841b5193af3dcb0798292d9e3060d1b5b56408219d925e79e4771c23de), check job output pk23/pev/out/m3_reader_cw_check_v1_1.out (sha256 7f885211ec4f1e35d6fbbd079a9023617f1e94ff603b7dcdd68bb5521ff6586d); run manifest pk23/pev/MANIFEST_CW_RUN_ABS_v1.sha256 (sha256 921a17a1f25bf1a65a8afd04ae98e235bf48bbc82806473b7153e735a010ec46, 34 rows).

Checks by this script (trial set = MR_LEMMAP.kv TRIAL_SET for N; entry list and runner by sha256; keys = the list's keys; J_REF 300, N, graph and format; the asm output's RECORD line and VERDICT; each certificate job's producer line, RECORD line, VERDICT and records map; the static job's and the reader check's VERDICT; sha256sum -c of the run manifest): m3_cw_LC_N4_J300_cw.json PASS, m3_lawcert_cw_v1_N4.json PASS, m3_cw_LC_N3_J300_cw.json PASS, m3_lawcert_cw_v1_N3.json PASS, m3_lawcert_cw_v1_static.out PASS, m3_reader_cw_check_v1_1.out PASS, MANIFEST_CW_RUN_ABS_v1.sha256 PASS.

Consumers load the records with m3_reader_cw_v1.load (bound to m3_run_v1_9_3_asmc.<N>.out) and the laws with load_lawcert (bound to m3_lawcert_cw_v1_<N>.out), then entry_law(cert, 'LC', key).

## 3. Values at N = 4

Columns: a_k as mid +- rad; sum Bp; the enclosure of I(J)/main(J) at J = 300; the enclosure for every J >= 300 (t in [0, 1/300], each a_k t^k between 0 and its value at t = 1/300); the exact order-0 value (rtwin_cw_v1's C-T0 closed forms) and a_0 minus it (float).

| key | a_0 | a_1 | a_2 | a_3 | sum Bp | at J = 300 | every J >= 300 | exact a_0 | a_0 - exact |
|---|---|---|---|---|---|---|---|---|---|
| Cxx,1,1 | 0.01522290657705 +- 5.9e-12 | 0.02582335856965 +- 3.7e-09 | 0.05567013800645 +- 1.8e-06 | 0.07654714713331 +- 5.3e-05 | 0.00125610705259 | [0.0140534987378, 0.0165657129244] | [0.0139667995185, 0.0165657129244] | 0.0152229065772 | -1.94e-13 |
| Cx1,1,1 | 0.01799424168002 +- 1.4e-12 | 0.02521322034834 +- 6.2e-10 | 0.09324474156627 +- 2.4e-07 | 0.1457611131261 +- 1.0e-04 | 0.000162947204429 | [0.0179163799846, 0.0182422744136] | [0.0178312944741, 0.0182422744136] | 0.0179942416802 | -2.27e-13 |
| C1x,1,1 | 0.01799424168002 +- 1.4e-12 | 0.02521322034832 +- 6.2e-10 | 0.09324474156585 +- 2.4e-07 | 0.1457611131236 +- 1.0e-04 | 0.000162947204429 | [0.0179163799846, 0.0182422744135] | [0.0178312944741, 0.0182422744135] | 0.0179942416802 | -2.27e-13 |
| C11,1,1 | 0.02128623625194 +- 4.7e-13 | 0.02354856591255 +- 1.2e-10 | 0.1917556313077 +- 3.6e-08 | 0.3178715172348 +- 1.2e-05 | 0.0000500140602790 | [0.0213168598007, 0.0214168879248] | [0.0212362221911, 0.0214168879248] | 0.0212862362522 | -2.68e-13 |

Bar parts at J = 300 (B, from the record) and the certificate's far rate:

| key | rem | tail | ann | far | rnd | far_rate |
|---|---|---|---|---|---|---|
| Cxx,1,1 | 0.00117892982982 | 0.0000606846513123 | 0.0000164925714611 | 6.77965950634E-19 | 4.06504971102E-11 | 0.320278424939 |
| Cx1,1,1 | 0.000156312589025 | 0.00000258864135323 | 0.00000404597405123 | 1.12994325106E-21 | 9.99308157680E-12 | 0.323611758272 |
| C1x,1,1 | 0.000156312589025 | 0.00000258864135323 | 0.00000404597405123 | 1.12994325106E-21 | 9.97582724965E-12 | 0.323611758272 |
| C11,1,1 | 0.0000483109927513 | 2.62704995843E-7 | 0.00000144036253186 | 1.88323875177E-24 | 1.72258775984E-12 | 0.326945091605 |

## 4. Values at N = 3

Columns: a_k as mid +- rad; sum Bp; the enclosure of I(J)/main(J) at J = 300; the enclosure for every J >= 300 (t in [0, 1/300], each a_k t^k between 0 and its value at t = 1/300); the exact order-0 value (rtwin_cw_v1's C-T0 closed forms) and a_0 minus it (float).

| key | a_0 | a_1 | a_2 | a_3 | sum Bp | at J = 300 | every J >= 300 | exact a_0 | a_0 - exact |
|---|---|---|---|---|---|---|---|---|---|
| Cxx,1,1 | 0.006768300795323 +- 3.7e-12 | 0.01243345238104 +- 2.0e-09 | 0.02147480967529 +- 8.9e-07 | 0.04130298575404 +- 2.5e-05 | 0.000624970778101 | [0.00618501497595, 0.00743495657471] | [0.00614333001347, 0.00743495657471] | 0.0067683007953 | 6.00e-15 |
| Cx1,1,1 | 0.01199616112018 +- 9.7e-13 | 0.01871310630929 +- 3.5e-10 | 0.01977553070381 +- 1.2e-07 | 0.02441124319045 +- 4.7e-05 | 0.0000798155481703 | [0.0119789432200, 0.0121385743269] | [0.0119163455710, 0.0121385743269] | 0.0119961611202 | 1.07e-14 |
| C1x,1,1 | 0.01199616112018 +- 9.7e-13 | 0.01871310630928 +- 3.5e-10 | 0.01977553070379 +- 1.2e-07 | 0.02441124319091 +- 4.7e-05 | 0.0000798155481703 | [0.0119789432200, 0.0121385743269] | [0.0119163455710, 0.0121385743269] | 0.0119961611202 | 1.07e-14 |
| C11,1,1 | 0.02128623625223 +- 3.5e-13 | 0.02732237545665 +- 7.4e-11 | 0.03122406238377 +- 1.9e-08 | 0.03149995126207 +- 5.8e-06 | 0.0000256373221455 | [0.0213520216146, 0.0214032962610] | [0.0212605989297, 0.0214032962610] | 0.0212862362522 | 1.84e-14 |

Bar parts at J = 300 (B, from the record) and the certificate's far rate:

| key | rem | tail | ann | far | rnd | far_rate |
|---|---|---|---|---|---|---|
| Cxx,1,1 | 0.000600897885105 | 0.0000195658612842 | 0.00000450703171110 | 7.96408601943E-26 | 2.12753627073E-11 | 0.356376867222 |
| Cx1,1,1 | 0.0000777836453731 | 8.77241526830E-7 | 0.00000115466127038 | 1.32734766991E-28 | 5.23662683755E-12 | 0.359710200555 |
| C1x,1,1 | 0.0000777836453731 | 8.77241526830E-7 | 0.00000115466127038 | 1.32734766991E-28 | 5.23154754544E-12 | 0.359710200555 |
| C11,1,1 | 0.0000251026026443 | 9.60685382881E-8 | 4.38650962923E-7 | 2.21224611651E-31 | 1.02437838249E-12 | 0.363043533888 |

