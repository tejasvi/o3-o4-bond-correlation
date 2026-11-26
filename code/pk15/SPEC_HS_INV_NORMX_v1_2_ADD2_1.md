# SPEC_HS_INV_NORMX_v1_2_ADD2_1: type-B lemma rows (D3 at d_L = -1) in the combined HS record

pk15, 2026-11-08T11:05:10Z (date -u). Addendum to SPEC_HS_INV_NORMX_v1_2 (84f6a3e0) and its ADD1 (f2ad58c9), which stand. It replaces
SPEC_HS_INV_NORMX_v1_2_ADD2.md (14144203), frozen against the type-B note's v1 and never sent; only the note pin and a's form differ.
Context: the approval for type-B lemma rows in the combined record (consumer: pk11's P2-12 engine R6, kt_p212_cert, which reads the
record directly; kt_p2_assembly has no D3B reader); pk08's Lemma B in pk08/HS_TYPEB_LEMMA_NOTE_v1_1.md (6d0864e5, manifest
8d1049f9), the review SOUND in both forms (REVIEW_HS_TYPEB_LEMMA_NOTE_V1_rv01.md 3684b492; v1_1 adds that a is in L^2).

## 1. The quantity and the exact OPERATOR string (L-2, C-HS-OP)
One line, compared symbol by symbol; it follows the note's sect. 0-2 (Lemma B, B1-B6):
```
OPERATOR_D3B = X = Z G_t G_bb Z*/lambda_0^3 (OPERATOR_D3, true lambda_0); u = top eigenvector of T = Z Z* in H, ||u|| = 1, Z* u > 0; w = Z V^(1/2) = K^(1/2) V 1; a = S'^-1 w/<u,w> = (lambda_0/(<u,w> v_0^(3/2))) 1, S' = T/lambda_0, so Z* a = (lambda_0/<u,w>) V^(1/2); X* a = Z G_bb G_t Z* a/lambda_0^3; Q0 = 1 - |u><u|; q = ||Q0 X* a|| <= QB_CRUDE and q <= ||Q0 X* u|| + QB_SLOPE, with no lambda factor; tau^2 = lambda_0 v_0^2/<u,w>^2 - 1 at tau's certified upper end
```
- The row fields are the note's two forms at tau's upper end, sup over the row's box: QB_CRUDE >= (A + |c_t|)(A + |c_bb|)(1 + tau_hi^2)^(1/2)
  and QB_SLOPE >= (A + |c_t|)(A + |c_bb|) tau_hi, A = (N-1)/2 (the record's N*_A), rounded up.

## 2. Keys in the combined record (the D3, D4 and D4M keys unchanged, as ADD1 requires)
```
LEMMA_NOTE_D3B = pk08/HS_TYPEB_LEMMA_NOTE_v1_1.md:801099463aa4dff112c1bc2078c943f8aff15ecdcf9738aed1a7d9f2f03f0e53
OPERATOR_D3B = <sect. 1>
LAMBDA_POWER_D3B = 0
FIELDS_D3B = jlo jhi ce_lo ce_hi cf_lo cf_hi QB_CRUDE QB_SLOPE
TAU_SOURCE = <path>:<full sha256> of tau's certified record (bound by its run output, rule V2)
N4_TAU_HI = <exact decimal used>
N3_TAU_HI = <exact decimal used>
N4_D3B_ROWS = 1
N4_D3B_R000 = 300 inf 0.94 1.06 0.94 1.06 <QB_CRUDE> <QB_SLOPE>
N4_D3B_METHOD = LEMMA
N3_D3B_ROWS = 1
N3_D3B_R000 = 300 inf 0.62 0.72 0.62 0.72 <QB_CRUDE> <QB_SLOPE>
N3_D3B_METHOD = LEMMA
```
- Class D3B; its N*_D3B_* keys are distinct from the N*_D3_* keys that C-HS-D3-SAME compares with 6b82dc63. The shared LEMMA_NOTE and
  FIELDS keys stay as in 6b82dc63, so Lemma B's note and the D3B layout get their own keys.
- LAMBDA_POWER_D3B = 0: Lemma B's bounds carry no (lambda_h/lambda_0) factor; lambda_0 enters only through tau_hi, a certified J-uniform
  upper end (from lambda_0's upper end and <u,w>'s lower end).
- One row per N, J-uniform over J >= 300 (J_CLAIM). The 14 near-end rows (d_R = 2..6, far, inf at both N) are R6's comparisons against
  these bounds, with R6's own q_need (DESIGN_P2_12_v1_5 1713cce3).
- The rows cannot be certified before tau's certified source exists (open with pk11).

## 3. For the consumer (R6), as the v1_2 gates read for this class
- C-HS-SRC and C-HS-D3-SAME (ADD1); C-HS-NOTE on LEMMA_NOTE_D3B; C-HS-OP on OPERATOR_D3B; C-HS-LAMBDA with p = 0; C-HS-J (METHOD LEMMA,
  every piece inside the row's J range); C-HS-CBOX (the piece's centre balls inside the box).
- C-HS-TAU: TAU_SOURCE pinned and bound; N*_TAU_HI equal to that record's upper end.
- C-HS-BFORM: QB_CRUDE and QB_SLOPE at least the sect. 1 formulas from N*_A, the box's largest |c| and N*_TAU_HI.
- The u-term ||Q0 X* u||_hi of the split form: the D3 pX_hi at the piece is valid by the top-bottom flip (
  ||Q0 X_c(c_t, c_bb)* u|| = ||Q0 X_c(c_bb, c_t) u||, so the pX bound must cover the swapped centres, which the symmetric D3 box does),
  and so is route 0's certified L0 (R6.4), which N4 (-1,2) needs (<= 1.99 there).
- Per piece, q_hi = min(QB_CRUDE, u-term + QB_SLOPE).

## 4. Correction to ADD1
- ADD1 sect. 4's "A" in the COEF formula is the note's a = (N-1)/2, the value the record's N*_A keys carry.
