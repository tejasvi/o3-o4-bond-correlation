# SPEC_HS_INV_NORMX_v1_2_ADD1: D4 and D4m lemma rows for the normX_HS interface

pk15, 2026-11-08T10:42:16Z (date -u). Addendum to SPEC_HS_INV_NORMX_v1_2 (84f6a3e0), which stands. Context: the approval for (b), lemma-form
D4/D4m rows under Lemma D4/D4m of pk08/HS_NORMX_LEMMA_NOTE_v1.md (1340a52c) with v1_2's true-lambda_0 normalization, and pk08's four
questions for building the export.

## 1. The exact OPERATOR strings (L-2, C-HS-OP)
Each is one line, compared symbol by symbol:
```
OPERATOR_D4 = Z = K^(1/2) V^(1/2); M = (xi_b - c_b) on column 0, xi_b = J(1 - s_M.s_B); G_t = V^(1/2) (K_t - c_t K) V^(1/2); lambda_0^2 X_c = Z M G_t Z*; w = 2; t = gap-0 top horizontal, b = column-0 MB vertical; HS2 = tr_H(X_c* X_c) <= COEF (lambda_h/lambda_0)^1, lambda_0 by its certified lower end
OPERATOR_D4M = Z = K^(1/2) V^(1/2); M = (xi_b - c_b) on column 1, xi_b = J(1 - s_M.s_B); G_t = V^(1/2) (K_t - c_t K) V^(1/2); lambda_0^2 X_c = Z G_t M Z*, the adjoint of D4's; w = 2; t = gap-0 top horizontal, b = column-1 MB vertical; HS2 = tr_H(X_c* X_c) <= COEF (lambda_h/lambda_0)^1, lambda_0 by its certified lower end
```
- They follow the note's sect. 1 in OPERATOR_D3's form. D4: lambda_0^2 X_c = K^(1/2) V (xi_b - c_b) (K_t - c_t K) V K^(1/2) = Z M G_T(c_t) Z*,
  M commuting with V^(1/2). D4m: lambda_0^2 X_c = K^(1/2) V (K_t - c_t K) V (xi_b - c_b) K^(1/2) = Z G_T(c_t) M Z*, the adjoint.

## 2. Record shape: (ii), one combined record
- A new file (pk08 names it), RECORD = END = HS_INV_NORMX_v1 as before, bound by its own run output (rule V2, C-HS-SRC).
- Every D3 key (OPERATOR_D3, LAMBDA_POWER_D3, the N4_D3_* and N3_D3_* keys) and every shared header key (FORMAT, EXPORT_STATUS,
  INTERFACE, TRACE, NORMALIZATION, LEMMA_NOTE, J_CLAIM, FIELDS) stays token for token as in HS_INV_NORMX_v1.kv (6b82dc63), which remains
  frozen and cited. CODE and provenance keys may differ.
- Consumer side: HS_RECORD moves to the combined file, and a new gate C-HS-D3-SAME compares those keys with the pinned 6b82dc63, so the D3
  rows cannot move unnoticed.
- Why (ii): one record gives one rule-V2 binding, one LEMMA_NOTE and one J_CLAIM for every class, and the consumer changes one pin. A
  second record would need two bindings and a merge.

## 3. Keys added for D4 and D4m, and the confirmations
```
OPERATOR_D4 = <sect. 1>
OPERATOR_D4M = <sect. 1>
LAMBDA_POWER_D4 = 1
LAMBDA_POWER_D4M = 1
MIRROR_D4M = ADJOINT_OF_D4
N4_D4_ROWS = 1
N4_D4_R000 = 300 inf 0.94 1.06 0.77 0.89 <COEF>
N4_D4_METHOD = LEMMA
N4_D4M_ROWS = 1
N4_D4M_R000 = <N4_D4_R000, token for token>
N4_D4M_METHOD = LEMMA
(the same keys for N3, with the boxes 0.62 0.72 and 0.50 0.60)
```
- LAMBDA_POWER_D4 = 1, as v1_2 L-3 fixes it: per piece HS2_hi = COEF (1/lambda~_0,lo)^1. LAMBDA_POWER_D4M = 1 is written too, so the
  consumer reads LAMBDA_POWER_<class> for every class.
- MIRROR_D4M = ADJOINT_OF_D4, and the D4M rows equal the D4 rows token for token (C-HS-MIRROR; the note's D4m paragraph).
- C-HS-CBOX: every consumer piece's certified balls lie inside the row's box, with lower ends >= 0 . For D4 this is the
  c_b >= 0 that Lemma D4's step (xi_b - c_b)^2 <= xi_b^2 + c_b^2 needs; the box lower ends 0.77 and 0.50 keep it.
- N*_D4_SPOT and N*_D4M_SPOT (C-HS-SPOT, a control) only if a pinned kt_s8rf_v1 output gives a D4 spot value; otherwise the consumer's
  D4 line reads SKIPPED.

## 4. Boxes (as v1_1 and v1_2 sect. 6)
- N4: ce = c_t in [0.94, 1.06], cf = c_b in [0.77, 0.89]. N3: [0.62, 0.72] and [0.50, 0.60].
- In v1_36's MOCK run (export_p2_14_means_mock_kt_p2_assembly_v1_36.kv 7e04d114) the per-piece balls sit well inside: N4 c_t in
  [1.00052, 1.00131], c_b in [0.82617, 0.82701]; N3 c_t in [0.66719, 0.66756], c_b in [0.55087, 0.55127]. The certified Set A/C/W
  entries can move them a little; the boxes leave about 6%.
- COEF = (A + max|c_t|)^2 (A2 + max(c_b)^2 A0) over the box, with A2 an upper end (pk08's new certificate) and
  A0 <= N*_RTR mhat(1/300) (S4_RTR_CERTIFIED_v1), rounded up. It must hold for every J in the row's range (J >= 300, J_CLAIM).
  pk08's estimate is 22.3 (N4) and about 5.8 (N3), against a need of 86.5 for the (1,1) rows.

## 5. Consumer changes (a later kt_p2_assembly version, on the approval; not in v1_37)
- hs_rows reads the D4 and D4M keys: C-HS-OP for both strings, C-HS-LAMBDA with p = 1, C-HS-MIRROR's token equality, C-HS-J, and
  C-HS-D3-SAME. The current refusal of D4 keys ("while main holds them") goes.
- normX_hi(D4, D4M) = min(Lemma S', sqrt(COEF/lambda~_0,lo)) per piece.
- Plants: OPERATOR_D4 with w = 3; LAMBDA_POWER_D4 = 2; one D4M row changed; one D3 row changed against 6b82dc63.
