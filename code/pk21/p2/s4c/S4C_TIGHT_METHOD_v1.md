# S4(c), tight half: the Hilbert-Schmidt bound over the four trial states (pk21, step 1, component S)

Nothing is claimed before the review. Paths are
relative to /mnt/g2/release/root/code/. Numbers are copied from the outputs named with them.

## 1. Claim

For N in {3, 4} and every J >= 300,

  ||Q_4 S Q_4|| <= tau_4(N),   tau_4(4) = 0.027702,   tau_4(3) = 0.026922,

where S = T/lambda_0, P_4 = span{psi-hat, e_1, e_2, e_3} is the paper's explicit trial space (e_2 flip-odd; paper l.2909), Q_4 = 1 - P_4,
and tau_4(N) is the largest per-piece bound of section 3, rounded up at the sixth decimal. The per-piece values are in the TSVs.

Uses:
- the connected short-strip engine (W1) needs a certified tau below about 0.059 on every piece (the read, 14351302);
- the middle-row sketch needs tau below s_y, the y level, about 0.0436 (M3 note, section 4);
- the supplement's S4(c), tau < s_x - c-bar, follows at once (the crude half already holds on disk, the ADD1 step 1).

## 2. Argument

- ||Q_4 T Q_4|| <= ||Q_4 T Q_4||_HS. With Pi the projection onto P_4 and an orthonormal basis u~_k of P_4,
  ||Q_4 T Q_4||_HS^2 = tr T^2 - 2 tr(Pi T^2 Pi) + tr((Pi T Pi)^2) <= tr T^2 - tr((Pi T Pi)^2),
  because tr(Pi T^2 Pi) = sum_k ||T u~_k||^2 >= sum_k ||Pi T u~_k||^2 = tr((Pi T Pi)^2). This is the supplement's route (v5b l.307).
- tr((Pi T Pi)^2) = ||A'||_F^2, with A' the Ritz matrix of T on P_4 in an orthonormal basis. T commutes with the flip that exchanges
  the top and bottom rows, and P_4 = P + span{e_2} with P = span{psi-hat, e_1, e_3} flip-even and e_2 flip-odd. So A' is the direct
  sum of the even Ritz matrix A'_even and the odd Rayleigh quotient a'_zz, and ||A'||_F^2 >= sum_i (A'_even)_ii^2 + a'_zz^2 in any
  orthonormal basis of P.
- S4(a): tr_H T^2 <= (U^(3)_N(t) + R_N) lambda_h^2 (paper l.2916).
- S6's data on each piece (paper l.3006-3027), in units of lambda_h:
  - rho2, the upper end of U^(3)_N(t) + R_N - sum_i (A'_even)_ii^2 (the number behind S6's rho = L_1^odd / lambda_0,lo);
  - mu_z, the lower end of a'_zz (the odd trial function's Ritz value, which S6 already uses in L_1^even);
  - lambda_0,lo <= lambda_0 / lambda_h.
- Hence ||Q_4 S Q_4|| <= sqrt(rho2 - mu_z^2) / lambda_0,lo, provided mu_z >= 0. The run certifies mu_z between 0.0797 and 0.0800 on
  every piece.

## 3. Computation

- Engine: pk21/p2/s4c/kt_s9h_tau4_pk21_v1.py (cc6f0a5f). It is a copy of pk07/kt_s9h_v1_2.py (848d7376, the file of the
  certified S_V run), with four changes (pk21/p2/s4c/diff_vs_kt_s9h_v1_2_v1.txt, 0d48880e, 57 lines):
  1. OWN is pk21's folder;
  2. the export's CODE line names the copy (two lines);
  3. per piece, tau4_row reads rho2, mu_z and lambda_0,lo from S6's quantities() and keeps the upper end of
     iv.sqrt([0, (rho2 - mu_z^2)_hi]) / lambda_0,lo;
  4. a summary line per N and a TSV of every piece.
  The verdict-path functions (C-MODULE's list) are not touched.
- Run: vsweep mode, LIM 300 (pk21/guard/S1_GUARD_job22_tau4.log, 0.030 core-h). Output pk21/p2/s4c/out/out_kt_s9h_tau4_pk21_v1_vsweep.out
  (1f3693f0): VERDICT VALID, every input tag certified, cpu 106.8 s. TSVs: tau4_kt_s9h_tau4_pk21_v1_N4.tsv (b6e65884) and
  tau4_kt_s9h_tau4_pk21_v1_N3.tsv (51deea98), 904 rows each.
- Control (pk21/p2/s4c/out/cmp_vs_original_v1.txt, acc002c4):
  - the 1808 piece rows of the copy's S_V export equal those of pk07's certified export (761084be) byte for byte;
  - the export headers differ only in the comment line and the CODE line;
  - the S5, S6, S7, INFO-HARM, C-MV and VERDICT lines of the run equal the original run's.
- Results:
  - largest tau4: 0.027701428 (N = 4) and 0.026921234 (N = 3), both on the first piece [300, 300.75];
  - last piece [1008859.42, inf): 0.027598475 and 0.026840747;
  - no piece reaches 0.04.

## 4. What the review should check

1. The Hilbert-Schmidt argument, in particular the parity split that lets the odd Rayleigh quotient be subtracted together with
   the even diagonal entries.
2. That rho2, mu_z and lambda_0,lo are the quantities S6 certifies (quantities() in the copy, from l.984; the run's rho_hi column
   equals S6's rho).
3. The diff.
4. Whether this run can stand as the record run, or whether a rerun of the frozen copy after the review is wanted.

## 5. Status and price

- the caveat (FEAS ADD1 V2, section 3) does not bite: S4(a)'s certified trace already gives a tau near 0.028, so S stays a
  last-mile step (2-4 planned h).
- Remaining after the review: the record entry, and the claim text as a module in pk21's folder (nothing goes into v4_39).
