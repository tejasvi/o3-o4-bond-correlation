# SPEC_HS_INV_NORMX_v1_2_ADD3: type-A lemma rows (D4 and D4M at d_L = -1) in the combined HS record

pk15, 2026-11-08T13:37:20Z (date -u). Addendum to SPEC_HS_INV_NORMX_v1_2 (84f6a3e0), ADD1 (f2ad58c9) and ADD2_1 (2ad2cc4c), which stand.
Context: the approval for type-A certified rows; consumer pk11's P2-12 engine R6 (R6.5's reader, which takes the power 1/2);
pk08's Lemmas A-D4 and A-D4M in pk08/HS_TYPEB_LEMMA_NOTE_v1_1_ADD1.md (8aadb7e8, manifest ffa098d6)
(REVIEW_HS_TYPEB_LEMMA_NOTE_V1_1_ADD1_rv01.md c833d21b, with its reader notes in sect. 3).

## 1. The quantities and the exact OPERATOR strings (L-2, C-HS-OP)
One line each, compared symbol by symbol; they follow the note's Lemma A-D4 and Lemma A-D4M, with X the X_c of OPERATOR_D4 or
OPERATOR_D4M and a, Z* a and tau as in OPERATOR_D3B (ADD2_1):
```
OPERATOR_D4A = X = Z M G_t Z*/lambda_0^2 (OPERATOR_D4, true lambda_0); a = S'^-1 w/<u,w> as in OPERATOR_D3B, so Z* a = (lambda_0/<u,w>) V^(1/2); X* a = Z G_t M Z* a/lambda_0^2; Q0 = 1 - |u><u|; q = ||Q0 X* a|| <= QA_CRUDE, with no lambda factor; tau as in OPERATOR_D3B at its certified upper end
OPERATOR_D4MA = X = Z G_t M Z*/lambda_0^2 (OPERATOR_D4M, true lambda_0); a = S'^-1 w/<u,w> as in OPERATOR_D3B, so Z* a = (lambda_0/<u,w>) V^(1/2); X* a = Z M G_t Z* a/lambda_0^2; Q0 = 1 - |u><u|; q = ||Q0 X* a|| <= QA_CRUDE (lambda_h/lambda_0)^(1/2), lambda_0 by its certified lower end; tau as in OPERATOR_D3B at its certified upper end
```
- QA_CRUDE is the note's bound at the box's sup, the smallest 12-digit decimal above it, in exact rationals, with A = N*_A,
  TAU_HI = N*_TAU_HI, A2 = N*_A2 and A0_HI = N*_A0_HI (v2's keys), and |c_t| at most ce_hi on boxes with ce_lo >= 0:
  - D4A: QA_CRUDE^2 >= (A + ce_hi)^2 (1 + TAU_HI^2) ((A - cf_lo)^2 + A^2). This is the sup over the box because cf_hi <= A
   
  - D4MA: QA_CRUDE^2 >= (A + ce_hi)^2 (1 + TAU_HI^2) (A2 + cf_hi^2 A0_HI), which needs cf_lo >= 0.

## 2. Record shape and keys
- A v3 combined record: a new file (pk08 names it), RECORD = END = HS_INV_NORMX_v1, bound by its own run output (rule V2). It
  repeats every line of v2 (pk08/out/HS_INV_NORMX_v1_d3d4b.kv f8e3d5e0) token for token, except CODE and the header comments, then
  the type-A block below. kt_p2_assembly v1_37 keeps v2 as its HS_RECORD.
```
LEMMA_NOTE_D4A = pk08/HS_TYPEB_LEMMA_NOTE_v1_1_ADD1.md:799cf99e7386dbf04dabbcb8b8bb49bff20cd498d9b8913a7ca949743c9c9ce3
LEMMA_NOTE_D4MA = pk08/HS_TYPEB_LEMMA_NOTE_v1_1_ADD1.md:799cf99e7386dbf04dabbcb8b8bb49bff20cd498d9b8913a7ca949743c9c9ce3
OPERATOR_D4A = <sect. 1>
OPERATOR_D4MA = <sect. 1>
LAMBDA_POWER_D4A = 0
LAMBDA_POWER_D4MA = 1/2
FIELDS_D4A = jlo jhi ce_lo ce_hi cf_lo cf_hi QA_CRUDE
FIELDS_D4MA = jlo jhi ce_lo ce_hi cf_lo cf_hi QA_CRUDE
N4_D4A_ROWS = 1
N4_D4A_R000 = 300 inf 0.94 1.06 0.77 0.89 <QA_CRUDE>
N4_D4A_METHOD = LEMMA
N4_D4MA_ROWS = 1
N4_D4MA_R000 = 300 inf 0.94 1.06 0.77 0.89 <QA_CRUDE>
N4_D4MA_METHOD = LEMMA
(the same keys for N3, with the boxes 0.62 0.72 and 0.50 0.60)
```
- Class names D4A and D4MA; the keys are per class, so a reader looks up <KEY>_<class> for every class. TAU_SOURCE, N*_TAU_HI, N*_A,
  N*_A2 and N*_A0_HI are v2's keys and are not repeated.
- The LAMBDA_POWER values are exact strings, "0" and "1/2" (R6.5 parses them as fractions in {0, 1/2, 1, 2}, pk11).
- There is no mirror rule: the D4A and D4MA rows come from different lemmas and differ.
- One row per N, J-uniform over J >= 300 (J_CLAIM); R6 compares the bounds with its own q_need.

## 3. For the consumer (R6.5), as the v1_2 gates read for these classes
- C-HS-SRC (v3 bound by its run output) and C-HS-V2-SAME (every key of v2 except CODE and END unchanged in v3).
- C-HS-NOTE on LEMMA_NOTE_D4A and LEMMA_NOTE_D4MA; C-HS-OP on both strings; C-HS-J (METHOD LEMMA, every piece inside the row's J range).
- C-HS-LAMBDA: LAMBDA_POWER_D4A = 0 and LAMBDA_POWER_D4MA = 1/2. Per piece the D4MA bound is QA_CRUDE times the upper end of
  (lambda_h/lambda_0,lo)^(1/2), lambda_0 by its certified lower end (S8's chain) and lambda_h by LAMBDA_H_DEF. The required plant:
  a D4MA row read with LAMBDA_POWER_D4MA = 0 is refused.
- C-HS-CBOX: each piece's c_t and c_b balls inside the row's box; on D4A rows cf_hi <= A (or else take the larger of
  |A - cf_lo| and |A - cf_hi|), on D4MA rows cf_lo >= 0.
- C-HS-AFORM: QA_CRUDE at least the sect. 1 formula from N*_A, N*_TAU_HI, N*_A2, N*_A0_HI and the box ends.
- C-HS-TAU as in ADD2_1 (TAU_SOURCE pinned and bound, N*_TAU_HI equal to that record's upper ends).
