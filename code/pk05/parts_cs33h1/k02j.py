# READINGS (fixed before any run), per interval [b0 - h, b0 + h], N and part:
#  Part A CERTIFIED iff (a) controls pass: C-CAS (every Casimir block's Davis-Kahan radius <= 1e-9), C-NODE (the float operator at the
#   K + 1 nodes lies in the TM enclosure, excess <= 1e-12 relative), C-PAR (the 8 node-0 eigenvectors have parity +-1 to 1e-6), C-FIN (every
#   bound finite), C-POS (inf p > 0 on the interval, NORM, rigorous enclosure), C-SLACK (the proved truncation slack slack_f of R9 TR5 is
#   finite); (b) on every subball: 8 KW intervals, sector trace bounds (+ eps_T), modes 1..6
#   certified (Davis-Kahan gap > 2 eps_T inside their
#   sector), nu1 nu2 isolated as the top of Lambda^2 (u_rem < nu2); (c) every FAR check (all pairs of objects {(e, p): p < P_e} u {(e, inf)},
#   every k >= K_EX) is positive on every subball. (v1_2: no same-column check; see the coverage table.)
#  Part B CERTIFIED iff (a) and (b) hold and every NEAR check (all pairs of objects, k < K_EX, n >= 4) is positive on every subball.
#   Parts Bh and Bv split part B: Bh takes the pairs with at least one horizontal object, Bv the pairs of two vertical objects; Bh and Bv
#   together certify exactly what B certifies.
#  An interval is CERTIFIED iff part A and part B (or both Bh and Bv) certify it (LEDGER lines tagged by part; the union check uses the
#   intervals tagged A and B, or A, Bh and Bv). FAILED otherwise. CONFLICT if some check value is certified negative (a counterexample
#   candidate; reported first, nothing else done).
#  Job: the first interval of every job runs the plants of its part and C-PROBE (cs30, same L, node 0: lam_s/lam1, s = 2..4, to 1e-8, and
#   c_mh/c_th to 1e-4). VALID iff every plant FIRES and C-PROBE passes. COVERED [a, b] (one part) iff VALID, every ledger interval of the
#   job is CERTIFIED for that part and their union contains [a, b] (exact endpoints, b0hex/hhex, rechecked by an independent union script).
#   VOID otherwise.
# PLANTS (first interval of a job; each must FIRE): every part: P6 (flint zero-centred ball), P-CAS (1% error in one Casimir off-diagonal:
#  radius > 1e-9), P-NODE (every float E~_m x (1 + 1e-6): C-NODE fails), P-TR (mode 2 left out of the trace bound: the identification
#  fails), P-L (eps_T at L/4: the identification fails), P-DELTA (every Delta bound x 1e8: a FAR (A) or NEAR (B) check fails); part A:
#  P-VEC (mode 2 replaced by mode 2 + 0.03 mode 4, residual by linearity: a FAR check fails), P-FAR (the leading amplitudes X_12 of (mh, inf)
#  negated: a FAR check fails); parts B, Bh: P-NEAR (the exact near value of the objects (th, 1), (mh, 1) at k = 0 (n = 4) negated: a NEAR
#  check fails); part Bv: P-NEAR on (tv, 1), (bv, 1).
# Usage: cs33h_1_rh_cert.py <item> <CAP_S> [K]. K = 3 (default) or 4 is the TM degree. Items: smoke (J = 20.2, N = 3, one interval of
#  relative width 1%, parts A and B in one process),
#  pilotA / pilotB / pilotBh / pilotBv (KT-P1: N = 4, one interval containing [300/1.01, 300]), coverP:N:a:b:q for P in A, B, Bh, Bv
#  (consecutive intervals of relative width q from a until b is covered, or the time cap; the next item resumes from the last LEDGER line).
