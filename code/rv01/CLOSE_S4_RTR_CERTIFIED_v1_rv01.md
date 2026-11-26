# CLOSE_S4_RTR_CERTIFIED_v1_rv01: record close of pk08's S4_RTR_CERTIFIED_v1 (certified Rtr)

Check of the record against its asm outputs, its rules and my code review. Nothing was run except sha256sum and awk reads and arithmetic.

## 0. Files
- pk08/S4_RTR_CERTIFIED_v1.md 417cb603, 114 lines. MANIFEST_S4_RTR_CERTIFIED_v1.sha256 03b76880: sha256sum -c gives 6 OK.
- asm outputs pk08/out/px08_rtrcert_v1_n4_asm.out 6e43ca81 and _n3_asm.out c9379724.
  - Header: px08_rtrcert_v1 sha256 80726a83..., ITEM=n4/n3 asm.
  - Both: CHECKS all PASS, PLANTS 24 of 24 FIRED, VERDICT VALID.
- Against: my code review REVIEW_PX08_RTRCERT_V1_rv01.md 7ab2f551 (notes R-1..R-3), and the design v1_1 pk08/S4_RTR_DESIGN_v1_1.md 1f5c37a5.

## 1. Answer first: CLOSED. The record copies its asm outputs faithfully, its rules state what the code does, and R-1..R-3 are met
- **The bounds**, for every t in (0, 1/300]:
  - N4_RTR = 1.33103977243e+0 and N3_RTR = 1.33071322604e+0;
  - headroom against today's FLOAT (1.332042, 1.331271): 1.00222757367e-3 and 5.57773963701e-4.
- **Provenance.** All 27 path:sha8 tokens of the record match sha256sum of their files.
- **Values.** 52 of the 54 N*_ keys appear verbatim in their own asm output. The other two, N*_HEADROOM_REL, are bc ratios by the record's rule, and they check (Section 2).
- **Reasons.** All 9 REASON_* values appear verbatim in both asm outputs.
- **Point 1** is met: MHAT_SOURCE_N4/N3 as path:sha8, the exact m literals, and MHAT_RULE ending "M2 must use the same m's from the same file".
- **Point 3** is met: DESIGN cites v1_1 1f5c37a5 with its manifest 01ea7909.
- **Point 2** is moot: against twrig3's M32 leading, C-SCAN's I[1] difference is 2.938e-11, a 340x margin under 1e-8. My review's 4x came from TRB's comparison with twrig4's lead.

## 2. The checks
- **The asm lines** (both N, PASS):
  - C-PROP on Q_t and the three Chernoff families;
  - C-SCAN (worst 0.000e+00 <= 1e-5, lead 2.938e-11 <= 1e-8);
  - C-MHAT, with the m literals printed as the record writes them;
  - C-MONO, min D >= 2.10593450135e-1 (N = 4) and 1.44380919830e-1 (N = 3);
  - C-FAR (p = 1.5);
  - C-GATE.
- **The sums** [awk, float]:
  - ratio + R3 + R_cub + tail + far reproduces N4_RTR and N3_RTR to the 12 printed digits;
  - N*_RTR_MAIN / N*_RTR_MHAT_LOW reproduces N*_RTR_RATIO to within 1e-11.
- **HEADROOM_REL** [awk]: 1.00222757367e-3 / 1.332042 = 7.523994e-4 and 5.57773963701e-4 / 1.331271 = 4.189785e-4. Rounded down at 4 digits these are 7.523e-4 and 4.189e-4, as recorded.
- **The m literals** (N*_MHAT_M1..M3) are the strings of the symmetrized vacres JSONs (b40859de, e5a9b49f) and of the asm's C-MHAT lines, as I read them in my code review.
- **N*_PR and N*_TV** equal S4_TRB_CERTIFIED_v1's (same PR and same I[1] = 1.33018901674). TV = (1 - theta2)^(-d/2) I[1] gives 42.064 (d = 3) and 13.302 (d = 2), as expected.
- **The rules match the code:**
  - RTR_RULE: the READING's upper end, with mhat(1/300) as a ball;
  - MONO_RULE: 8 t-balls, v1_1's wording;
  - GATE_RULE;
  - CLAIM: mu-hat = lambda_h mhat, with lambda_h as in the TRB record;
  - CONSTANT_PER_N.

## 3. Notes (no action needed)
- The asm READING line names "S4_RTR_DESIGN_v1 item 3", the code's own text, while the record's DESIGN cites v1_1. They agree, because v1_1 only rewords C-MONO.
- USE: M2(b) pins this record by path:sha8 and reads N*_RTR. Under MHAT_RULE, M2's import must also read MHAT_SOURCE and the m literals, and use those same m's.
