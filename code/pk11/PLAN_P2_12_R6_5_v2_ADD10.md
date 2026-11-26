# PLAN_P2_12_R6_5_v2_ADD10: all-piece break-evens from R6.5's stride-1 mock sweep (replaces ADD9's grid-only values)

pk11, 2026-11-08, the approval of 18:47Z (mock and float; cap 0.3 h, raised to 0.6 h at 19:10Z). Amends PLAN_P2_12_R6_5_v2
(d4361948) with ADD1 (a5f9800a) to ADD9 (d6bcb64d). Sect. 5 replaces the table in ADD9 sect. 2. ADD4's rules stand: q_tol is primary,
L0_tol = q_tol^2, each tolerance holds with the other window at its own tolerance, and the corner covers the box below it.

## 1. Sources
- Engine kt_p212_cert_v1_2_2.py 24a59e32, mock mode: v1_2_1 (57de10b0) with the new mock pins and the break-even outputs added; the diff
  is out/diff_kt_p212_cert_v1_2_1_to_v1_2_2.txt abfe719b.
- Run outputs in mocks/out/p212_v1_2/, each VERDICT VALID: pre b3d73b0a; chunk N4, pieces 61..903 at stride 1, a7a4e43b; chunk N3,
  pieces 0..903 at stride 1, cf163d76; final 942cc537; record P2_12_JOINT_RECORD_v1_MOCK_kt_p212_cert_v1_2_2.kv 1abeb699.
  C-COVER reads COMPLETE at both N (843 and 904 pieces), and C-FINAL-REPRO passes.
- MOCK inputs:
  - the u-hat records UHAT_ASM_v1_1_1_MOCK_N4.kv 07143f9e and UHAT_ASM_v1_1_1_MOCK_N3.kv d1135799, written by kt_uhat_mock_v1_1_1
    (2a2bfb48), with route0b_hat.D3 from the route R + E-R floats in pk02's uhat_fhc_r_v1_2.out (63407283), and the L0 windows and
    B' as in v1;
  - sigma_g's kappa and Phi_eps from pk15's MOCK covtest2 output (bf45982b). The values equal the certified upper ends: Phi_eps as
    in v1_37_1's PHI-EPS lines, kappa as in the joint export's AUDIT line.
- Every other input is certified: S8 v1_14_3's chain, R4 v1_37's exports, record 895634f5, and the HS records v2 and v3.
- Record values in the sweep:

| N | U_D3 (route P) | q_use D4-L0 | q_use D4M-L0 |
|---|---|---|---|
| 4 | 0.034328 | 0.0999027 | 0.0368109 |
| 3 | 0.01259 | 0.0655390 | 0.0131945 |

## 2. Break-evens
- At one piece, a row's break-even x* for one input is the largest value of that input that keeps lo_lo >= Cov_hi / 2, with every
  other input at the record's value.
- lo is affine in each input, so x* has a closed form in balls, on the safe side:
  - B3 and A2, lo = a - b x: x* = (a_lo - Cov_hi/2) / b_hi.
  - d_L <= 0, R = (c1 x + c0) / den: x* = ((Cov_lo - Cov_hi/2) den_lo - c0_hi) / c1_hi.
  - TB reads q = min(QB_CRUDE, U + QB_SLOPE). So U* = q* - QB_SLOPE when q* < QB_CRUDE, and U has no limit otherwise.
  - TC and TD read q = U + nX Qa. So U* = q* - (nX Qa)_hi. In N3 D3 (0,1) (beta form), E_semi is linear in U as well and enters c1.
- The tables give each row's minimum over all evaluated pieces, with its piece, rounded down at 6 significant digits. A negative value
  means that the row fails even with that input at 0; "none" means no limit at any piece.
- U_D3* covers the D3 route-0 rows: B3 (d_L >= 1), TB (d_L = -1) and TD (d_L = 0). U_D3* reads no u-hat value: S8's chain, the R4
  exports, record 895634f5, the HS records, and for TD sigma_g with the constants above.
- D4M-L0 q* covers the A2 rows that are not wait-W and D4's type C rows, in two columns: D4-L0 at the record's q_use ("rec") and
  D4-L0 at ADD9's 0.200 ("at 0.200"). A type C row of D4 does not read D4-L0, so both columns agree there.
- D4-L0 q* covers the rows that read only D4-L0: D4 (d,inf) and D4M's type C rows.

## 3. Outcome at the record's values, every piece

| N | pass | fail | wait-W | out |
|---|---|---|---|---|
| 4 | 95 | 5 | 2 | 2 |
| 3 | 82 | 2 | 2 | 0 |

- N4 failing rows, smallest headroom: D3 (1,2) 1.716 (below 2 at every piece), D4M (1,2) 1.522 (every piece), D4M (1,3) 1.917,
  D4 (1,2) 1.990 and D4M (1,4) 1.992. All five minima are at piece 116 (J about 400.8), where the certified Cov_inf_lo dips.
- N3 failing rows: D3 (1,1) 1.475 (below 2 at every piece) and D3 (0,1) 1.599 (below 2 at pieces 0 to 62, J below about 351; above 2
  from piece 63). Both minima are at piece 0.

## 4. Per-row break-evens

### 4.1 U_D3* (D3 route-0 rows)

| N | row | type | U_D3* | piece |
|---|---|---|---|---|
| 4 | D3 (1,2) | B3 | 0.0203993 | 116 |
| 4 | D3 (1,3) | B3 | 0.0451397 | 116 |
| 4 | D3 (1,4) | B3 | 0.0491856 | 116 |
| 4 | D3 (1,5) | B3 | 0.0497869 | 116 |
| 4 | D3 (1,6) | B3 | 0.0498749 | 116 |
| 4 | D3 (1,far) | B3 | 0.0498851 | 116 |
| 4 | D3 (1,inf) | B3 | 0.0498900 | 116 |
| 4 | D3 (2,2) | B3 | 0.164641 | 116 |
| 4 | D3 (2,3) .. (2,inf) | B3 | 0.307070 .. 0.355131 | 116 |
| 4 | D3 (3,3) .. (3,inf) | B3 | 1.22586 .. 2.45471 | 116 |
| 4 | D3 (-1,2) | TB | 0.723122 | 61 |
| 4 | D3 (-1,3) .. (-1,inf) | TB | none | - |
| 4 | D3 (0,2) | TD | 1.98898 | 61 |
| 4 | D3 (0,3) .. (0,inf) | TD | 33.3218 or more | 61 |
| 3 | D3 (1,1) | B3 | -0.00104408 | 0 |
| 3 | D3 (0,1) | TD, beta | -0.105227 | 0 |
| 3 | D3 (1,2) | B3 | 0.0520571 | 0 |
| 3 | D3 (1,3) | B3 | 0.0660993 | 0 |
| 3 | D3 (1,4) | B3 | 0.0683851 | 0 |
| 3 | D3 (1,5) | B3 | 0.0687244 | 0 |
| 3 | D3 (1,6) | B3 | 0.0687741 | 0 |
| 3 | D3 (1,far) | B3 | 0.0687798 | 0 |
| 3 | D3 (1,inf) | B3 | 0.0687826 | 0 |
| 3 | D3 (2,2) | B3 | 0.241925 | 116 |
| 3 | D3 (2,3) .. (2,inf) | B3 | 0.429271 .. 0.492677 | 116 |
| 3 | D3 (-1,2) .. (-1,inf) | TB | none | - |
| 3 | D3 (0,2) | TD | 4.10119 | 0 |
| 3 | D3 (0,3) .. (0,inf) | TD | 37.6819 or more | 0 |

- N4 D3 (0,1) and N4 D3 (1,1) are out (O5).
- At N3, D3 (1,1) and D3 (0,1) are below 2 at piece 0 even with U_D3 = 0, so no route-0 value lifts either row. The other terms decide
  both rows; in D3 (0,1), sigma_g alone is 2.56e-4 at piece 0, against a shortfall in lo of 4.6e-4.

### 4.2 D4M-L0 q*

| N | row | rec | at 0.200 | piece |
|---|---|---|---|---|
| 4 | D4M (1,2) | 0.0162087 | 0.0149347 | 116 |
| 4 | D4M (1,3) | 0.0339923 | 0.0338280 | 116 |
| 4 | D4 (1,2) | 0.0343306 | -0.0677830 | 116 |
| 4 | D4M (1,4) | 0.0365349 | 0.0365113 | 116 |
| 4 | D4M (1,5) | 0.0369051 | 0.0369016 | 116 |
| 4 | D4M (1,6) | 0.0369591 | 0.0369586 | 116 |
| 4 | D4M (1,far) | 0.0369635 | 0.0369615 | 116 |
| 4 | D4M (1,inf) | 0.0369684 | 0.0369684 | 116 |
| 4 | D4 (2,2) and D4M (2,2) | 0.234068 | 0.224872 | 116 |
| 4 | every other row | 0.256623 or more | 0.255437 or more | - |
| 3 | D4M (1,2) | 0.0393891 | 0.0379029 | 116 |
| 3 | D4M (1,3) | 0.0466928 | 0.0464979 | 116 |
| 3 | D4M (1,4) | 0.0477380 | 0.0477099 | 116 |
| 3 | D4M (1,5) | 0.0478901 | 0.0478860 | 116 |
| 3 | D4M (1,6) | 0.0479123 | 0.0479117 | 116 |
| 3 | D4M (1,far) | 0.0479136 | 0.0479109 | 116 |
| 3 | D4M (1,inf) | 0.0479161 | 0.0479161 | 116 |
| 3 | D4 (1,2) | 0.234315 | 0.0861176 | 0 |
| 3 | D4 (2,2) and D4M (2,2) | 0.326023 | 0.315403 | 116 |
| 3 | every other row | 0.335402 or more | 0.334009 or more | - |

### 4.3 D4-L0 q* (rows that read only D4-L0)
- N4: D4 (1,inf) 0.273149 (piece 116), D4 (2,inf) 2.85165, D4 (3,inf) 21.8992; D4M's type C rows 2.35764 or more (piece 61).
- N3: D4 (1,inf) 0.332137 (piece 0), D4 (2,inf) 3.91865; D4M's type C rows 3.04732 or more (piece 0).

### 4.4 Rows that read both windows
- An A2 row is affine in both windows, so the row's two values at one piece fix a line in the plane of the two windows. Over the
  pieces, the minimum of affine functions is concave, so the chord between the two minima lies at or below the true minimum: the chord
  is on the safe side.
- N4 lines, from the printed values by bc, with q_D4L0 = 0.0999027 + d:
  - D4 (1,2): q_D4ML0* = 0.0343306 - 1.020143 d;
  - D4M (1,2): q_D4ML0* = 0.0162087 - 0.012727 d;
  - D4M (1,3): q_D4ML0* = 0.0339923 - 0.001641 d.
- D4 (1,2) bounds D4-L0 at N4. With D4M-L0 at the record's 0.0368109, D4 (1,2) needs D4-L0 at most 0.09747; with D4M-L0 at 0, at
  most 0.1335. ADD9's D4-L0 tolerance of 0.200 leaves D4 (1,2) below 2 for every D4M-L0 value.

## 5. Tolerances (replace the table in ADD9 sect. 2)

| N | input | q_tol | L0_tol = q_tol^2 (exact) | binding rows |
|---|---|---|---|---|
| 4 | D4-L0 | 0.1178 | 1.387684e-2 | D4 (1,2) with D4M (1,2), piece 116 |
| 4 | D4M-L0 | 0.01597 | 2.550409e-4 | D4M (1,2) with D4 (1,2), piece 116 |
| 3 | D4-L0 | 0.200 | 4.0e-2 | unchanged; the D4-L0-only rows allow 0.332 |
| 3 | D4M-L0 | 0.03790 | 1.43641e-3 | D4M (1,2) with D4-L0 at 0.200, piece 116 |
| 4 | U_D3 | 0.02039 | - | D3 (1,2), piece 116 |
| 3 | U_D3 | 0.05205 | - | D3 (1,2), piece 0 |

- Each q_tol is rounded down at 4 significant digits. With both windows at q_tol, every counted row keeps headroom 2 at every piece.
  At the N4 corner, by the lines of sect. 4.4, D4 (1,2) allows D4M-L0 up to 0.016072 and D4M (1,2) up to 0.015980, both at least
  0.01597. At N3, D4 (1,2) allows D4M-L0 up to 0.0861 with D4-L0 at 0.200.
- Counted rows: every row that is neither wait-W nor out. The N3 U_D3 tolerance leaves out D3 (1,1) and D3 (0,1), which stay below 2
  at U_D3 = 0.
- The U_D3 tolerance and the window corner are independent: the D3 route-0 rows read no L0 window, and the D4 and D4M rows read no
  U_D3.
- Alternatives at N4, if main drops rows: without D4M (1,2), the corner is D4-L0 0.1002 and D4M-L0 0.03399 (binding D4 (1,2) with
  D4M (1,3)); without D3 (1,2), the U_D3 tolerance is 0.04513 (D3 (1,3)).
- ADD9's grid-only values, for comparison: D4M-L0 0.02255 (N4) and 0.04084 (N3), D4-L0 0.200 at both N.

## 6. Notes
- Piece 116 binds every failing row at N4 and most break-evens at both N. ADD9's grid had pieces 61, 62, 71, 101, 150, 250, 400,
  600, 800 and 903 at N4 (0, 1, 10, 40 and the same last six at N3), so piece 116 was not in ADD9's grid. The certified Cov_inf_lo
  dips about 5.5% at piece 116.
- Hand table and engine differ for N4 D4 (1,2) at a grid piece. At piece 61, the engine gives a D4M-L0 q* of 0.05844 with D4-L0 at 0.0999,
  and -0.05670 with D4-L0 at 0.200 (pre output, ROW line). The hand table d4ml0_breakeven_rows_v2 (397b6f09) gave 0.113 with D4-L0
  at 0.0948, and 0.02887 at 0.200. The D4-L0 slope differs as well: 1.15 in the engine, 0.80 in the hand table. So the hand table's chain values
  for D4 (1,2)'s left side differ from S8's chain at that piece. This item does not trace the cause; the review found the engine's
  readings term by term as plan v2 states them. ADD9's D4-L0 tolerance came from the hand table.
- In the rec column, the break-evens of the A2 rows read the record's D4-L0 q_use. The at-0.200 column and U_D3* read no u-hat value.
- The values are float planning values from a MOCK run, INFO only. R6.5's certified per-row gate decides each row at every piece.
