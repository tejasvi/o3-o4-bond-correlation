# CLOSE_ARBENG_MA_V1_3_rv01: the M-a layer arbeng_ma_v1_3 is closed for certified use (validation of record kt_ma_val_v1_5, VALID on v1-v4)

Close. Nothing was run. I used sha256sum and awk reads of the outputs.

## 0. Files
- **The layer:** pk02/arbeng_ma_v1_3.py 075e3586. My code read is DELTA_ARBENG_MA_V1_3_rv01.md 5cfc221f: SOUND, certified use once the validation passes.
- **The validation of record:** kt_ma_val_v1_5.py cdc01d56. Its diff from v1_4 is DIFF_kt_ma_val_v1_4_to_v1_5.txt 9942e3f8. The bundle MANIFEST_MA_LAYER_v1_3_b.sha256 b5d0cc5a gives 39 OK on sha256sum -c.
- **The outputs** (444, pk02/out/):
  - out_kt_ma_val_v1_5_v1.out 5ccbb6d0;
  - out_kt_ma_val_v1_5_v2.out a61d893e;
  - out_kt_ma_val_v1_5_v3.out d613fe80;
  - out_kt_ma_val_v1_5_v4.out 2ad13ec3.
- **The run records:** chain log run_kt_ma_val_v1_5_v1.log ab67023b; driver run_kt_ma_val_v1_5_v1.sh 228152c2.

## 1. Answer: CLOSED. arbeng_ma_v1_3 (075e3586) may carry certified M3 and M2(b) records
- **The verdict lines.**
  - Each output has exactly one VERDICT line, "VERDICT VALID".
  - Each prints the script's sha cdc01d56 with its own piece.
  - The chain log checks the bundle's sha first. It then shows rc 0 for v3, v4, v1 and v2, with out sha8s equal to the files'.
- **Every gate passed and every plant fired, for its stated reason** (Section 2). That covers ADD3's rule, my two points (by code read), D-1's fix, T-a, C-FLOOR, C-COUNT and the int64 guard.
- **The docstring overstatement does not touch the verdict.** v1_5's docstring says E2 also fails under v1_1, and pk02 has noted that this is wrong. PLANT-ZMID fired through npoly_mul, npoly_pow, lp_norm, condE and CondTable. E2 and 'E2 two parts' stayed ok under v1_1, as they should, since v1_1's E2 had no drop site.
- **Conditions of use:**
  - (i) A certified caller pins 075e3586 and runs at ctx.prec 512. The layer refuses any other precision.
    - pk03's three pins (ctx.prec 256, the stub_v1 import, and VALIDATED naming arbeng_ma_v2) must be fixed in the revision that adopts the layer.
  - (ii) MAFallback is the only exception a caller may catch, and catching it means recomputing in arb. C-FALLBACK shows it raised as designed.
  - (iii) The two stub departures stay deferred to the next layer revision. They are not on the certified path.

## 2. The readings
| piece | gates and plants (all as stated in the code) |
|---|---|
| v3 | **C-CROSS on the layer and the stub:** 12 intervals, including [-0.25, 0.25] and two iv.dps 40 quotients with 136- and 134-bit ends, plus 7 balls both ways, all contained. **PLANT-SIGN** misses 10 of 12. **C-TINY:** 246961 entries, 0 failures, 101784 error-only terms, largest allowance 1.897e-320, Smax 1.0. **PLANT-TINY:** v1_1 raises at 5.563e-309. **C-ZMID** passes all 7 cases, with T-a's endpoints. **C-FALLBACK** passes. **PLANT-ZMID** fires. **C-COUNT** gives k 6 and sr 1.25; **PLANT-COUNT** gives k 3. **C-FLOOR:** ±4.01e-292 contains 1e-400; **PLANT-FLOOR** gives {}. **C-INT64** and **PLANT-INT64** behave as stated. **C-AK:** 2810 moments, 0 outside; **PLANT-MA-AK** fires. |
| v1 | **CondTable Dc 10** on e1n4's symmetric A: 7677098 entries, 4273190 error-only terms, largest allowance 3.44e-319. **V1 (a):** 0 failures either way. **PLANT-MA-ROUND** fires (2 entries miss). **INFO count-0:** 0 miss. **V1 (b):** condE, 8008 coefficients, 0 mismatches. **V1 (c):** nD's M-a ball (relative 3.0e-11) agrees with arb and with the c hand-off. **C-REPRO** passes. |
| v2 | **X0, X1, X2** against kt_cert_v1_5's hand-offs, at relative widths 1.0-2.0e-11. **C-SING:** 511 kept, 512 dropped, every dropped det ball containing 0. **C-REPRO tailX** passes. |
| v4 | **B0** at relative width 5.7e-12. **C-SING** passes. **PLANT-MA-SING** and **PLANT-MA-W** fire. **C-ERRORS:** the 1e-320 product goes through the tiny rule to ±4.01e-292. **K3 E, K5 lp_norm p = 2 and pos_norm p = 1** pass against arb. **PLANT-MA-INPUT** fires. **K4 npoly_mul:** 18170 coefficients, 0 mismatches. **SPoly + AllMom2 (mp.iv)** passes against the stub. |
- Costs from the chain log: v1 387.7 s CPU at 7.8 GB; v2 78.3 s; v3 4.3 s; v4 28.4 s.

## 3. Notes
- **N-1. The docstring.** pk02's next revision fixes v1_5's PLANT-ZMID wording.
- **N-2. The wide relative widths in v1.** The largest are 9.05e+156, and C-SHADOW is 1.24e+143. They come from entries whose midpoints sit near 0, the symmetric A's structural zeros. They do not signal a precision problem: every such entry contains its arb ball, and every one-sided entry contains 0.
- **N-3. For readers of the records.** PLANT-MA-COUNT is now an INFO line, because a count-0 radius already covers this table. C-TREE and C-COUNT check the counts structurally, and PLANT-MA-ROUND shows the rounding allowance is live.
