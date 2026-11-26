"""s8core_v1_11.py -- pk11 (code/pk11/). REVISION of s8core_v1_10.py (c43eef9e) on the word of 2026-11-08: sf_pair's
class-level form gets the thin and C1 checks of the other centered instances (Lemma M v2's per-instance target check
sect. 5 had left it uncovered), which need its internal constants. No bound changes: sf_pair(..., info=None) takes an optional dict and,
when one is given, records into it what it computes anyway:
- always: 'k' (= m - 1), 't1' (the lemma term used in Num's lower end), 't1s' (the one used in its upper end), 'ddet', 'dz', 'C1' =
  t1 + ddet (the class-level form's shift), 'Zz' and 'num' (cov2's Z and Num on ch), 'plain_lo' (cov_lo before the class-level form);
- in the class-level branch ('dual' in ch, not zero, Zz of one sign): 'sg', 'topc' (the centered ball of Num - C1), 'cen' {'+dz' or
  '-dz': the centered ball of (Num - C1)/(sg Z + dd)^2 with dd = dz or -dz} for every dd it evaluates (one or both; a dd with |Z| + dd
  not certainly > 0 is recorded as None), 'cl2' and 'used' (cl2 > plain_lo, so the class-level lower end is the one returned). gl takes
  the record's key as a second argument; its value is v1_10's.
The returned tuple is v1_10's in every case.
s8core_v1_10.py -- pk11 (code/pk11/). REVISION of s8core_v1_9_1.py (22bc96f2) for S8's cert-mode version, on the word of
2026-11-08: the gaps the review found in CHECK_O3_LEMMA_M_S8_rv03.md (0226c38c) against the Lemma M conditions
(NOTE_LEMMA_CENTERED_FORM_V2_rv01.md 8ca6c894). No bound changes.
- C5 (the centered form needs G(., theta) C^1 near the box): _pos(x, what) and _nz(x, what) require a square root's argument certainly
  positive and a divisor certainly nonzero with a known sign over the whole input box (a ball's ends; a dual's value ball); otherwise
  ValueError, which the cert module turns into a failing piece (KILL), never a value. Gated: g00 (sqrt(g00) and a divisor), T00, e_0,
  rmain and lambda_0 in chain(), chain_B() and chain_RB() (every divisor there is one of these or a product of them, or sqrt(g00) > 0);
  D.sqrt's argument and every dual division (D.__truediv__, D.__rtruediv__); the strip's Z in strip_cov_t. Only chol_inv's pivots were
  gated before (l.258).
- C6: _cen raises ValueError when the centered ball and the dual's own value ball are disjoint (both hold the true value, so this is a
  bug signal), instead of returning the ball between the two disjoint ends.
Everything else is v1_9_1; v1_9_1's docstring follows.
s8core_v1_9_1.py -- pk11 (code/pk11/). REVISION of s8core_v1_9.py (1f2d4014
f812727a: the route (b) design SOUND), docstrings only, no code change: setup()'s docstring states the condition under
which its sector split of Gl (eta+ and eta- from the even and odd principal blocks) is valid for route (b): both chains exactly
parity-pure (the W3 chain's and the B chain's par_exact True). Then S commutes with the T <-> B parity and u is even, so every true
cross-parity entry of R_BB and of Gl is exactly 0 (the place-2 balls only enclose it) and Gl_true is block-diagonal; the cert module
gates par_exact on both chains (C-PAREXACT, KILL). The joint-budget note (the joint budget 2 sum + |Q_B S Q_B|_HS^2 <= 2 tau_B could tighten
the block bound) is optional and not taken. Everything else is v1_9; v1_9's docstring follows.
s8core_v1_9.py -- pk11 (code/pk11/). REVISION of s8core_v1_8_2.py (4805cf70) for the S8 route (b) (2026-11-07: the TT
route is out; S8 is route (b) only, U9 from a trial-basis chain, H and S4 from D16, and per piece the best of the nested bases B4
(states 0..4), B5 (0..5) and B6 (0..6)). DRAFT (freeze nothing certified yet). Changes:
- chain(..., tt=True) and chain_dual_t(..., tt=True): with tt=False (route (b)) the W3 chain reads no TT entry, so it has no M2 and no
  Gl (route (b) supplies Gl), and the parity-forced keys for par_exact are those of g, T, e, f and h. Everything else is v1_8_2's chain,
  so route (b)'s W3 chain carries the place-2 allowance on beta and AXm (the diagnostics kt_s8_diag_K9_v1_7 .. v1_11 built their W3
  chain with s8core_v1_6's chain(), which has no place-2 allowance);
- setup(..., Gl=None, sblk=None): route (b) passes routeb_leak's Gl, and s_perp is the smaller of the K = 3 value sqrt((U_hi/lambda_0^2)^up
  - 1 - tr R^2) and routeb_leak's block bound; with both None, setup is v1_8_2's;
- chain_RB and chain_dual_t_RB (new): the reduced B chain, from g and T over the trial states only. The caller renames the trial states
  0..nst in order (an order-preserving map, the odd states with them); C0 is its binary64 basis over states 1..nst, the first three rows
  W3's padded with zeros, every row exactly parity-pure. It computes lambda_0 (place 1), C = chol_inv(C0 G'' C0^T) C0, R_BB = C T''
  C^T / lambda_0 + pm(4 s^2) (place 2, as chain()), |R_BB|_F^2, each basis vector's parity and par_exact on the g and T parity-forced
  keys, and nothing else: it reads no TX, TXX, e, eX, f, fX, DY, F3 or fXX key (a narrowed N record with T and TX,a,b for a, b <= 3
  suffices). Cholesky keeps the order of C0's rows, so C's first three rows are W3's orthonormal basis (the same exact vectors as the W3
  chain's C, which uses the same g entries) and R_BB's rows 3.. against its first three columns are the in-B leakage of W3's modes;
- routeb_leak (new): from a chain_RB on B and S4-U's U_hi, U9 refined (the review NOTE_S8_4COL_ROUTES_rv01.md 0a6cd86d sect. 1(b)-(c);
  T-2): tau_B = ((U_hi/lambda_0^2)^up - 1 - |R_BB|_F^2 lo)/2, upper end, bounds the trace of the leakage Gram of W_B out of B (tr_H S^2
  = 1 + |R_BB|_F^2 + 2 sum_{y in W_B} |Q_B S y|^2 + |Q_B S Q_B|_HS^2 <= U_hi/lambda_0^2), so W3's leakage Gram out of W3 is at most
  Gl = R_B3^T R_B3 + tau_B I; |Q_3 S Q_3| is at most the largest eigenvalue of [[r_bb, sqrt(tau_B)], [sqrt(tau_B), sqrt(2 tau_B)]]
  (r_bb: the Gershgorin norm of R_BB's block 3..; sqrt(tau_B) bounds Q_B S on W_B and sqrt(2 tau_B) bounds Q_B S Q_B), sblk = (r_bb +
  s)/2 + sqrt(((r_bb - s)/2)^2 + tau_B) with s = sqrt(2 tau_B). None when tau_B's upper end is not > 0 (no bound from this basis on the
  piece); tau= is a plant's override, never a bound;
- route_b_keys (new): the M3 record keys route (b)'s two chains read for a trial set (S8-3's S4 strips are the cert module's), for the
  cert module's scope gate.
Everything else is v1_8_2; v1_8_2's docstring follows.
s8core_v1_8_2.py -- pk11 (code/pk11/). REVISION of s8core_v1_8_1.py with
the tightening T-1 (b28d0555 sect. 3; the low-J note 320ff8fd's first step): in setup_B's rnX[d] (d >= 1) the X-leakage of the
known in-B part of w_(d-1), bounded so far by xleak (the operator norm) times |P_W_B w_(d-1)| + dlp, may instead take the per-vector K
form kvec(w, dlp) = (|gamma_w| sqrt(tau_B) |w_c| + qt sqrt(w_c^T M(gamma_w) w_c) + (|gamma_w| sqrt(tau_B) + qt sqrt(lambda_max M(gamma_w)))
dlp + s pc (|w_c| + dlp)) (1 + s^2), gamma_w = (w^T M_1 w)/(w^T M_0 w) per vector (binary64), w_c the computed components (balls, with
place 2's allowance); the smaller of the two is used (both valid). The same y = Q0 y0 argument as v1_8_1's xleak gives the s pc term.
xleak (the operator norm) stays in cerr, whose input is Q_B v. Everything else is v1_8_1; v1_8_1's docstring follows.
s8core_v1_8_1.py -- pk11 (code/pk11/). REVISION of s8core_v1_8.py (e923ed86) on the review REVIEW_S8CORE_V1_8_K9_rv01.md
(b28d0555: the K = 9 design; three items fixed here, two left for later):
- (place 2 for the A_X blocks; also in v1_6's chain): u is not an eigenvector of A_X, so on W' = Q0 W0 each entry of B_X's W block
  moves by -<e_k,u><p_X,e_l> - <e_k,p_X><u,e_l>: chain() and chain_B() add a1 = 2 s |p_W| + 4 (|B+| + |c|) s^2 to every entry of beta
  (hence of AXm), with |p_W| = |BTM| and |B+| = vac['Bp'], the dual run's constant passed to the midpoint run (allow['AX']).
  For the K form, setup_B's xleak bounds |Q_B A_X y| for y in W'_B through y = Q0 y0, y0 in W0_B (where the form M lives): Q_B A_X y =
  Q_B A_X y0 - <u, y0> Q_B p_X, so xleak = (|gx| sqrt(tau_B) + qt sqrt(lambda_max M(gx)) + s pc)(1 + s^2) (|y0| <= (1 + s^2) |y|); this
  uses A_X u = c u + p_X exactly, so no xi^2 form on u (the Phi_u) is needed;
- (dk_setup with several odd modes): top_o = max(s_perp, hi_k of the odd modes other than ko); go = lo[ko] - top_o - eta-; q_r uses
  max(top3, top_o); g1 keeps the even rest only. With one odd mode (v1_6, K = 3) top_o = s_perp and nothing changes;
- rnX[d] and rnXo[d] carry |l_u| pc (l_u = L[d-1]'s u component, 1 +- O(s)) in setup() and setup_B().
Everything else is v1_8; v1_8's docstring follows.
s8core_v1_8.py -- pk11 (code/pk11/). REVISION of s8core_v1_6.py (7b711c8b): S8 with no 4-column entry, on the ten-state trial
basis B (the rules of 2026-11-07: every 4-column entry dropped; the K = 9 core approved). Every v1_6 function is unchanged (the W3
path with TT, H and S4 stays as it was); v1_8 adds:
- chain_B and chain_dual_t_B: the chain on B = span(u) + W_B, W_B the Q0-projected z9sym states 1..9 (K = 9), from 3-column entries
  only (g, T, TX for the ten states; e, eX, f, fX, DY; DYY; FF's z, wXw, wXwX; the K form's TXX, fXX,0 and the F3 graph free | int |
  free with xi_TM^j, j = 0, 1, 2). R = R_99 (place 2's 4 s^2), the components of every vector on all nine B modes, L[1..7] the B
  steps of L[0] (no H entry), the d = -1 norms relative to B, p_X's components on W_B; plus |R_99|_F^2 (U9), the K form's quadratic
  forms Phi_j (d = 0) and M_j (9 x 9, d >= 1), and gam0 = x_u/l_u at d = 0;
- setup_B: setup()'s dict for a chain_B, so the lemma, sf_pair, far_lo2, dk_setup, dk_class, s81_cert and rows_cert run unchanged
  with K = 9:
  - U9 (the review NOTE_S8_4COL_ROUTES_rv01.md 0a6cd86d sect. 1(b)-(c)): tr_H S^2 = 1 + |R_99|_F^2 + 2 sum_{y in W_B} |Q_B S y|^2 +
    |Q_B S Q_B|_HS^2 <= U_hi/lambda_0^2, so the leakage Gram of W_B out of B (PSD) has trace <= tau_B = (U_hi/lambda_0^2 - 1 -
    |R_99|_F^2)/2: Gl = tau_B I, eta = sqrt(tau_B); |Q_B S Q_B| <= sqrt(2 tau_B) = s_perp; a stop when tau_B's upper end is not > 0.
    Like v1_6's s_perp, this uses S4-U's trace over H (S4_U_CERTIFIED's H holds u, all ten trial states of both T <-> B parities and
    every chain vector, and S = T/lambda_0 maps H to itself);
  - the K form for the X kind: with T = K K* and T_xi = K xi K* (K zeta = V^(1/2)
    zeta from the int column's functions into H, V the int column's weight; T_xi^2 = K xi^2 K* is N with xi_TM^2 on column 1),
    |Q_B K|^2 = |Q_B S Q_B| <= sqrt(2 tau_B), so for any gamma Q_B A_X y = gamma Q_B S y + Q_B K (xi - gamma) K* y is bounded by
    |gamma| |Q_B S y| + (2 tau_B)^(1/4) |(xi - gamma) K* y|, and |(xi - gamma) K* y|^2 is a quadratic form in 3-column entries. At
    d = 0 (x(0) = A_X w-hat, A(0) = l_u x(0) - x_u l(0)) the form is Phi(gamma) = <r, T_(xi - gamma)^2 r>/lambda_0 for r = w-hat -
    psi-hat_n, and with gamma = x_u/l_u the Q_B l(0) terms of Q_B A(0) cancel exactly; at d >= 1 the form is M_2 - 2 gamma M_1 +
    gamma^2 M_0 on W_B (xleak, the operator norm of Q_B A_X P_W_B);
  - the d >= 1 errors and residuals of the B steps (setup_B's docstring), |A_X| <= |B+| + |c| for Q_B -> Q_B;
  - the gates: upper ends under every square root, and a stop when a squared-norm form is certainly negative (_nonneg);
    setup_B(kzero=True) takes (2 tau_B)^(1/4) as 0, PLANT-KFORM's input, never a bound.
Everything else is v1_6; v1_6's docstring follows.
s8core_v1_6.py -- pk11 (code/pk11/). REVISION of s8core_v1_5.py (6d12a691) on the stage C review (REVIEW_KT_S8_CERT_STAGEC_
The review.md ea6ff691). In chain(), the W-component allowance of the vectors at d = -1, 0, 1 (place 2 for vectors, +- s |x_u|) was
s |x_u|_box in the dual run (D.__abs__ gives the box value) but s |x_u(t_m)| in the midpoint run, and it carries no gradient, so a
centered component covered x(t) +- s |x_u(t_m)| but not +- s |x_u(t)| where |x_u(t)| > |x_u(t_m)| (a second-order gap). v1_6:
- chain(..., allow=None) takes the allowance constants to use and returns those it used (ch['allow']); chain_dual_t, chain_dual and
  chain_centered pass the dual run's constants, s |x_u| upper over the whole box, to the midpoint run, so the centered component holds
  +- s |x_u(t)| at every point of the box;
- an odd basis vector gets no allowance when the parity is exact (ch['par_exact']: C0's rows exactly F-pure and every parity-forced
  entry of the graphs g, T, TT, e, f, h exactly 0 on the box, so C is F-pure and <e_k, u> = 0 for an odd e_k, u being F-even); otherwise
  (stage B's raw entries) every component keeps it. The decision is the dual run's (on the box) and is passed to the midpoint run with
  the allowances (par), since a midpoint can be exactly parity-pure where the box is not;
- leaves() skips 'allow' (constants of the run, not values to compare).
Everything else is v1_5; v1_5's docstring follows.
s8core_v1_5.py -- pk11 (code/pk11/). REVISION of s8core_v1_4.py (6421e5b4) on the stage B review (REVIEW_KT_S8_CERT_V1_4_
STAGEB_rv01.md 59597e89): head() returned inf whenever Cov_lo >= Cov, whatever the sign of Cov_lo; it now returns inf only
when Cov_lo > 0 and 0 (a failing value) otherwise. A headroom is a diagnostic (minima, RISK lines, the binding rows of the plants); the
kill rule reads each row's certified lower end itself (rows_cert). Everything else is v1_4; v1_4's docstring follows.
s8core_v1_4.py -- pk11 (code/pk11/). REVISION of s8core_v1_3.py (71b3e8d5) for stage C of kt_s8_cert, the pieces in J. The
v1_3 functions are unchanged; v1_4 adds:
- entry_duals: the entries on a piece box (t = 1/J in the piece's ball T, each bar offset in [-err_b, err_b]) as duals with t as slot 0:
  value sum_k [LO_k, HI_k] T^k + [-err_b, err_b], t-gradient sum_k k [LO_k, HI_k] T^(k-1), a unit in its own bar slot; the center is the
  bar-free value at t_m = mid(T). So f over the box lies in f(center) + g_t [-rad T, rad T] + sum_i g_i [-err_i, err_i] for every a_k
  of its interval (the mean-value theorem in (t, bars), with g enclosing the gradient over the box and the a_k intervals);
- chain_dual_t and strip_cov_t: the chain and S8-3's strip on a piece in that form (sf_pair's class-level form reads ch['dual'] as
  before, now with the t slot among its radii);
- tpoints, entry_points, leaves, inside, mv_check, unif_check: the 9 sample points of a piece, the bar-free entries at a point, the
  ball leaves of a chain, ball containment, C-MV (the bar-free centered chain contains the point chains, leaf by leaf) and C-UNIF's
  entry part;
- s81_cert and rows_cert: head_s81 and rows_for with each row's certified lower end, for the kill rule (a row fails only when its lower
  end is not > 0). S8-1 takes max(route A, min over route B), since each route covers every d_R >= D_far; S8-3 passes on its strip or
  on its chain; a top-mode class passes with a cover (C-SIGN-C4 included) and m0 <= 8.
Everything else is v1_3; v1_3's docstring follows.
s8core_v1_3.py -- pk11 (code/pk11/). REVISION of s8core_v1_2.py (5c33a874). kt_s8_cert_v1_3's like-for-like C-REPF agreed with
3g v1_2 to 1.4% on 15 of 18 rows; the three others use |A_perp(0)|, which setup assembled from separately centered chain outputs
(A2 - |A_W|^2 cancels from O(0.1) to O(1e-4), so their dependency doubled its width). v1_3 computes |A_perp|^2 at d = -1, 0 inside
chain() (ch['Ap2'], one centered quantity, as 3g's quants did); setup takes its square root. Everything else is v1_2.
s8core_v1_2.py -- pk11 (code/pk11/). REVISION of s8core_v1_1.py (24729c28). Against 3g v1_2's corrected reference (cda500ca)
the centered chain matched to 1% except two places: S8-2 m1 rows 11% looser (Num and Z bounded separately, losing their correlation)
and the m >= 2 rows tighter (the ball's eta). v1_2 adds:
- chain_dual: the centered chain plus the chain in duals and at the midpoints (ch['dual']);
- sf_pair's class-level mean-value form: with C1 = t1 + ddet and dz fixed upper ends over the box, Cov >= (Num - C1)/(|Z| + dz)^2 for
  a nonnegative numerator (|Z| - dz for a negative one; the smaller of both when it straddles 0), with Num and Z as duals, so their
  correlation is kept; the larger of this and the plain bound is used;
- setup(eta_override=...): C-REPF's like-for-like mode only.
Everything else is v1_1; v1_1's docstring follows.
s8core_v1_1.py -- pk11 (code/pk11/). REVISION of s8core_v1.py (93b81575): kt_s8_cert_v1_1's mock run (807d4d7c) showed the
naive balls up to 27% looser than 3g's first-order bars (interval dependency, mostly in |p_perp|, which enters the d >= 1 residuals
twice). v1_1 adds the mean-value form: chain_centered runs chain() once in forward-mode duals over the entry box (value and gradient
balls) and once at the exact midpoints, and returns per quantity f(x_mid) + sum_i g_i [-r_i, r_i], intersected with the naive ball;
strip_cov does the same for S8-3's strip; dual_selftest is C-DUAL. Everything else is v1; v1's docstring follows.
s8core_v1.py -- pk11 (code/pk11/). The interval core of kt_s8_cert (stage B): S8's chain bounds of SPEC_S8_CERT_v1 (c0f95398)
with ADD1 (9f38c5e7), in python-flint arb balls, for one piece of J. Not a script: kt_s8_cert imports it by its pinned sha256.
It is the port of kt_s8f3g_v1_1's float chain (80c401df, VALID) to balls:
- an entry's value on a piece is the ball sum_k [LO_k, HI_k] t^k + [-err_b, err_b] over the piece's t-range (m3_reader_v4_4's
  entry_ball), so every derived ball holds the true value for every J of the piece; no linear propagation of bars remains;
- the Ritz basis is fixed per piece: the float Ritz vectors of the midpoints, rounded to binary64 (C0), then orthonormalized in balls
  (C = L^-1 C0 with L the ball Cholesky factor of C0 G'' C0^T), so R = C T'' C^T / lambda_0 is a full ball matrix, not a diagonal;
  every place where 3g used the diagonal rho now uses R (matrix powers in the lemma, the Ritz steps, Gershgorin discs for the
  eigenvalue bounds of the top-mode form);
- the five vacuum places of SPEC sect. 7, each a review item of this stage:
  1. lambda_0 = m-hat (1 + theta delta), |theta| <= 1, delta = eps_r / sqrt(1 - s^2);
  2. setting 1 (W' = Q0 W0): R and M2 entries move by at most 4 s^2 (the rank-one terms and the re-orthonormalization); a vector's
     W components carry +- s |x_u|;
  3. c = c~ + [-4 sp, 4 sp] (c~ = TX00/T00, the trial ratio), and the components <f_k, p_X> carry +- |B+| sp (K-1's whole-operator
     bound on B_X (u - psi-hat));
  4. Cov is invariant under the scale of each end, so the trial normalization w / <psi-hat, w> is kept for every vector of that end;
  5. |p_perp| <= |p~_perp| + eps_a + |B+| sp + s |p_W| and |p_Y| <= |p~| + eps_a + |B+| sp;
- K-1: ||B_X eps|| <= |B+| |eps| wherever 3g had sqrt(|B+|^2 + |B-|^2); |B-| stays on the odd part.
Integer powers are repeated products (arb ** int is NaN on a ball holding 0). Square roots of balls that may dip below 0 take the end
they need, clipped at 0 (sqrt_up, sqrt_lo)."""
import math
from fractions import Fraction
from flint import arb

ZERO, ONE = arb(0), arb(1)
POSINF, NEGINF = arb(float('inf')), arb(float('-inf'))


def fr(q):
    """the ball holding the exact rational q (Fraction or int)."""
    q = Fraction(q)
    return arb(q.numerator) / arb(q.denominator)


def span(lo, hi):
    """the ball holding [lo, hi] (balls or Fractions)."""
    a = lo if isinstance(lo, arb) else fr(lo)
    b = hi if isinstance(hi, arb) else fr(hi)
    return a.lower().union(b.upper())


def pm(r):
    """the ball [-r, r] for r >= 0 (ball, Fraction or float)."""
    r = r if isinstance(r, arb) else fr(Fraction(r))
    u = abs(r).upper()
    return (-u).union(u)


def _pos(x, what):
    """v1_10 (C5): x (a ball, or a dual's value ball) must be
    certainly positive over the whole input box, its lower end > 0 (a NaN fails too); otherwise ValueError, so that no piece takes a
    value from a square root or a divisor that is not C^1 on the box. Returns x."""
    v = x.v if isinstance(x, D) else x
    if not (v > 0):
        raise ValueError('C5: %s is not certainly positive (%s)' % (what, v))
    return x


def _nz(x, what):
    """v1_10 (C5): the divisor x must be certainly nonzero with a known sign over the whole input box (certainly > 0 or certainly < 0; a
    NaN fails); otherwise ValueError. Returns x."""
    v = x.v if isinstance(x, D) else x
    if not (v > 0 or v < 0):
        raise ValueError('C5: the divisor %s is not certainly nonzero (%s)' % (what, v))
    return x


def up(x):
    return x.upper()


def lo(x):
    return x.lower()


def sqrt_up(x):
    """an upper end of sqrt(max(x, 0)) for every point of x."""
    u = x.upper()
    return (u if u > 0 else ZERO).sqrt().upper()


def sqrt_lo(x):
    """a lower end of sqrt(max(x, 0))."""
    v = x.lower()
    return (v if v > 0 else ZERO).sqrt().lower()


def ipow(x, n):
    y = ONE
    for _ in range(n):
        y = y * x
    return y


def tball(jlo, jhi):
    """the t = 1/J range of a piece [jlo, jhi] (floats; jhi may be inf), as one ball."""
    thi = ONE / arb(jlo)
    tlo = ZERO if math.isinf(jhi) else ONE / arb(jhi)
    return tlo.lower().union(thi.upper())


def entry_vals(E, t):
    """{key: ball} of I(J)/main(J) over the piece, from entry_ball's (LO, HI, err_b)."""
    tk = [ONE, t, t * t, t * t * t]
    res = {}
    for key, (LO, HI, err) in E.items():
        v = pm(err)
        for k in range(4):
            v = v + span(LO[k], HI[k]) * tk[k]
        res[key] = v
    return res


# ---- small matrices of balls
def mzero(n, m):
    return [[ZERO] * m for _ in range(n)]


def mmul(A, B):
    return [[sum((A[i][k] * B[k][j] for k in range(len(B))), ZERO) for j in range(len(B[0]))] for i in range(len(A))]


def mT(A):
    return [list(r) for r in zip(*A)]


def mv(A, v):
    return [sum((A[i][k] * v[k] for k in range(len(v))), ZERO) for i in range(len(A))]


def dot(u, v):
    return sum((a * b for a, b in zip(u, v)), ZERO)


def norm_up(v):
    """an upper end of the Euclidean norm of a ball vector."""
    return sqrt_up(sum((x * x for x in v), ZERO))


def chol_inv(G):
    """L^-1 for the ball Cholesky factor L of a ball s.p.d. matrix G (lower triangular); ValueError if a pivot is not positive."""
    n = len(G)
    L = mzero(n, n)
    for i in range(n):
        for j in range(i + 1):
            s = G[i][j] - sum((L[i][k] * L[j][k] for k in range(j)), ZERO)
            if i == j:
                if not s.lower() > 0:
                    raise ValueError('Cholesky pivot %d not positive' % i)
                L[i][i] = s.sqrt()
            else:
                L[i][j] = s / L[j][j]
    Li = mzero(n, n)
    for i in range(n):
        Li[i][i] = ONE / L[i][i]
        for j in range(i):
            Li[i][j] = -sum((L[i][k] * Li[k][j] for k in range(j, i)), ZERO) / L[i][i]
    return Li


def gersh(R):
    """per row k: (R_kk, the Gershgorin radius sum_{l != k} |R_kl| upper end)."""
    return [(R[k][k], sum((abs(R[k][l]).upper() for l in range(len(R)) if l != k), ZERO)) for k in range(len(R))]


def chain(V, mains, odd_states, vac, C0, nst=3, allow=None, par=None, tt=True):
    """the chain on one piece in balls. V: {chain key: ball}; mains: the five main-term ratios (balls); vac: {'delta', 's'} upper ends
    (balls); C0: the binary64 Ritz basis (rows; G''-orthonormal at the midpoints). Returns a dict as 3g's chain, with R the full
    ball Ritz matrix of S on W' and pi the parity of each basis vector (from C0). v1_6: allow = {(d, j): constant}, the W-component
    allowances of the vectors at d = -1, 0, 1, and par, the parity decision (both the dual run's, given to the midpoint run, so the two
    runs agree: a midpoint can be exactly parity-pure where the box is not); ch['allow'] and ch['par_exact'] the ones used."""
    rhoE, rmain, rho4, rhob, rhoH = mains
    rng = range(nst + 1)
    sym = lambda nm, a, b: V[(nm, min(a, b), max(a, b))]
    g = [[sym('g', a, b) for b in rng] for a in rng]
    T = [[sym('T', a, b) for b in rng] for a in rng]
    TX = [[sym('TX', a, b) for b in rng] for a in rng]
    e = [V[('e', a)] for a in rng]
    eX = [V[('eX', a)] for a in rng]
    f = [V[('f', a)] for a in rng]
    fX = [V[('fX', a)] for a in rng]
    K = nst
    g00 = _pos(g[0][0], 'g00')   # v1_10 (C5): sqrt(g00)'s argument and a divisor; T00, e_0, rmain and lam0 are divisors
    _nz(T[0][0], 'T00')
    _nz(e[0], 'e_0')
    _nz(rmain, 'rmain')
    sg = g00.sqrt()
    lam0 = _nz(T[0][0] / g00 * (ONE + pm(vac['delta'])), 'lam0')   # place 1: lambda_0 = m-hat (1 + theta delta)
    s2 = vac['s'] * vac['s']

    def p2(M, a, b):
        return M[a][b] - g[a][0] / g00 * M[0][b] - g[b][0] / g00 * M[a][0] + g[a][0] * g[b][0] / (g00 * g00) * M[0][0]
    idx = list(range(1, K + 1))
    G2 = [[p2(g, a, b) for b in idx] for a in idx]
    T2 = [[p2(T, a, b) for b in idx] for a in idx]
    C0b = [[arb(x) for x in row] for row in C0]
    Gf = mmul(mmul(C0b, G2), mT(C0b))
    C = mmul(chol_inv(Gf), C0b)   # rows: an orthonormal basis e_k of W0 (exact in balls)
    # place 2 (setting 1): on W' = Q0 W0 the rank-one terms <u,e_k><u,e_l> (|<u,e_k>| <= s) and the re-orthonormalization of Q0 e_k move
    # each entry of R and M2 by at most s^2 (1 + 2 |R| + |R|^2) <= 4 s^2, since |R|, |M2| <= 1; components in u-perp are unchanged
    R = [[x / lam0 + pm(4 * s2) for x in row] for row in mmul(mmul(C, T2), mT(C))]
    # place 3: c = <u, A_X u> against the trial ratio c~ = TX00/T00: |c - c~| <= 2 |p_X| sp + O(sp^2) <= 4 sp (|p_X| <= 1, |A_X| <= 2)
    c = TX[0][0] / T[0][0] + pm(4 * vac['sp'])
    odd = [1 if (a in odd_states) else 0 for a in idx]
    pi = [(-1 if sum(C0[k][i] ** 2 for i in range(K) if odd[i]) > sum(C0[k][i] ** 2 for i in range(K) if not odd[i]) else 1)
          for k in range(K)]
    p1 = lambda M, n: M[n][0] - g[n][0] / g00 * M[0][0]
    p1v = lambda vec, n: vec[n] - g[n][0] / g00 * vec[0]
    Tp = [p1(T, n) for n in idx]
    # place 3: <f_k, p_X> = <f_k, B_X u>, computed at psi-hat; |B_X (u - psi-hat)| <= |B+| sp (K-1)
    BTM = [sum((C[k][i] * (p1(TX, n) - c * Tp[i]) for i, n in enumerate(idx)), ZERO) / (lam0 * sg) + pm(vac['Bp'] * vac['sp'])
           for k in range(K)]
    B = {'TM': BTM, 'MB': [BTM[k] if pi[k] > 0 else -BTM[k] for k in range(K)]}
    X2 = [[p2(TX, a, b) for b in idx] for a in idx]
    beta = [[x / lam0 for x in row] for row in mmul(mmul(C, [[X2[i][j] - c * T2[i][j] for j in range(K)] for i in range(K)]), mT(C))]
    # v1_8_1: place 2 for the A_X block. u is not an eigenvector of A_X, so on W' = Q0 W0 each entry of B_X's W block moves
    # by -<e_k,u><p_X,e_l> - <e_k,p_X><u,e_l> (|.| <= 2 s |p_W|) plus second-order terms (<= 4 (|B+| + |c|) s^2); the dual run's
    # constant goes to the midpoint run (allow['AX']), as v1_6's allowances do
    a1 = allow['AX'] if allow is not None else (2 * vac['s'] * norm_up(BTM) + 4 * (vac['Bp'] + abs(c).upper()) * s2).upper()
    beta = [[x + pm(a1) for x in row] for row in beta]
    AXm = [[beta[i][j] + c * R[i][j] for j in range(K)] for i in range(K)]

    def comps(vec, scale):
        return [scale * sum((C[k][i] * p1v(vec, n) for i, n in enumerate(idx)), ZERO) for k in range(K)]
    L = {}
    L[-1] = ((ONE, comps(e, sg / e[0])), (eX[0] / e[0], comps(eX, sg / e[0])))
    L[0] = ((rhoE * f[0] / (lam0 * e[0]), comps(f, rhoE * sg / (lam0 * e[0]))),
            (rhoE * fX[0] / (lam0 * e[0]), comps(fX, rhoE * sg / (lam0 * e[0]))))
    h = [V[('h', a)] for a in rng]
    hX = [V[('hX', a)] for a in rng]
    L[1] = ((rhoH * h[0] / (lam0 * lam0 * e[0]), comps(h, rhoH * sg / (lam0 * lam0 * e[0]))),
            (rhoH * hX[0] / (lam0 * lam0 * e[0]), comps(hX, rhoH * sg / (lam0 * lam0 * e[0]))))

    # place 2 for vectors: the W components of a vector x in u-perp along Q0 e_k are <e_k, x> - x_u <e_k, u>, so the trial components
    # carry +- s |x_u|; place 4: Cov is invariant under the scale of each end, so the trial normalization w-hat = w / <psi-hat, w> is
    # used throughout, consistently for every vector of that end.
    # v1_6: one allowance constant per vector, s |x_u| upper over the whole box (the dual run's D.__abs__ gives the
    # box value), passed to the midpoint run as allow, so a centered component covers +- s |x_u(t)| at every point of the box. An odd
    # basis vector gets none when the parity is exact (par_exact: C0's rows F-pure and every parity-forced entry exactly 0 on the box, so
    # C is F-pure and <e_k, u> = 0 for an odd e_k, u being F-even).
    zero = lambda x: bool((x.v if isinstance(x, D) else x).mid() == 0 and (x.v if isinstance(x, D) else x).rad() == 0)
    oddst = [a for a in rng if a in odd_states]
    pzk = [(nm, a, b) for nm in (('g', 'T', 'TT') if tt else ('g', 'T')) for a in rng for b in rng if a <= b and ((a in oddst) != (b in oddst))] + \
        [(nm, a) for nm in ('e', 'f', 'h') for a in oddst]
    pure = all(C0[k][i] == 0.0 for k in range(K) for i in range(K) if (odd[i] == 1) != (pi[k] < 0))
    par_exact = par if par is not None else (pure and all(k in V and zero(V[k]) for k in pzk))
    alw = {'AX': a1}
    for d in (-1, 0, 1):
        vs = []
        for j, v in enumerate(L[d]):
            a_ = allow[(d, j)] if allow is not None else (vac['s'] * abs(v[0]).upper()).upper()
            alw[(d, j)] = a_
            vs.append((v[0], [x if (par_exact and pi[k] < 0) else x + pm(a_) for k, x in enumerate(v[1])]))
        L[d] = tuple(vs)

    def step(v1):
        u1, k1 = v1
        return (u1, mv(R, k1)), (c * u1 + dot(BTM, k1), [BTM[k] * u1 + dot(AXm[k], k1) for k in range(K)])
    for d in range(2, 8):
        L[d] = step(L[d - 1][0])
    L['inf'] = ((ONE, [ZERO] * K), (c, list(BTM)))
    ch = {'R': R, 'pi': pi, 'B': B, 'beta': beta, 'AXm': AXm, 'c': c, 'lam0': lam0, 'L': L, 'g00': g00, 'C': C, 'K': K}
    ch['allow'], ch['par_exact'] = alw, par_exact
    z, wXw, wXwX = V[('z',)], V[('wXw',)], V[('wXwX',)]
    Z4, X1, X12 = V[('Z4',)], V[('X1',)], V[('X1X2',)]
    F4 = rho4 * g00 / (lam0 * lam0 * e[0] * e[0])
    Rw2 = z * g00 / (rmain * e[0] * e[0]) - 1
    nwX2 = wXwX * g00 / (rmain * e[0] * e[0])
    sq = lambda v: v[0] * v[0] + sum((x * x for x in v[1]), ZERO)
    ch['res2'] = {(-1, '1'): (1 + Rw2) - sq(L[-1][0]), (-1, 'X'): nwX2 - sq(L[-1][1]), (0, '1'): F4 * Z4 - sq(L[0][0]),
                  (0, 'X'): F4 * X12 - sq(L[0][1])}
    ch['norm2'] = {(-1, '1'): 1 + Rw2, (-1, 'X'): nwX2, (0, '1'): F4 * Z4, (0, 'X'): F4 * X12}
    ch['cross'] = {-1: wXw * g00 / (rmain * e[0] * e[0]), 0: F4 * X1}
    ch['Rw2'], ch['nS2'] = Rw2, F4 * Z4
    # v1_3: |A_perp|^2 = |A|^2 - |A_W|^2 at d = -1, 0 as one quantity of the chain (centered as a whole), since its terms cancel from
    # O(0.1) to O(1e-4); setup takes its square root
    ch['Ap2'] = {}
    for d in (-1, 0):
        l1, lx = L[d]
        lu, xu = l1[0], lx[0]
        n2X, n21, crs = ch['norm2'][(d, 'X')], ch['norm2'][(d, '1')], ch['cross'][d]
        A2 = lu * lu * (n2X - xu * xu) - 2 * lu * xu * (crs - xu * lu) + xu * xu * (n21 - lu * lu)
        ch['Ap2'][d] = A2 - sum(((lu * lx[1][k] - xu * l1[1][k]) * (lu * lx[1][k] - xu * l1[1][k]) for k in range(K)), ZERO)
    if tt:   # v1_9: route (b) (tt=False) reads no TT; its Gl comes from routeb_leak
        TT = [[sym('TT', a, b) for b in rng] for a in rng]
        TT2 = [[p2(TT, a, b) for b in idx] for a in idx]
        M2 = [[x * rhob / (lam0 * lam0) + pm(4 * s2) for x in row] for row in mmul(mmul(C, TT2), mT(C))]
        RR = mmul(R, R)
        ch['M2'] = M2
        ch['Gl'] = [[M2[i][j] - RR[i][j] for j in range(K)] for i in range(K)]
    DY = [V[('DY', a)] for a in rng]
    DYY = V[('DYY',)]
    ct = DY[0] / g00
    Bt = [sum((C[k][i] * (DY[n] - ct * g[n][0]) for i, n in enumerate(idx)), ZERO) / sg for k in range(K)]
    p2n = (DYY - ct * ct * g00) / g00
    ch['pperp2'] = p2n - sum((v * v for v in Bt), ZERO)
    ch['pnorm2'] = p2n
    ch['pW'] = Bt
    return ch


# ---- the SPEC-form ingredients (3g's sf_setup_c, in balls)
def lmax_psd_up(G, ks):
    """an upper end of lambda_max of the PSD sector block G[ks][ks]: min(trace, Frobenius norm), from the balls' upper ends."""
    if not ks:
        return ZERO
    tr = sum((G[k][k] for k in ks), ZERO).upper()
    fr2 = ZERO
    for i in ks:
        for j in ks:
            a = abs(G[i][j]).upper()
            fr2 = fr2 + a * a
    fro = fr2.sqrt().upper()
    return tr if tr < fro else fro


def rnorm_up(R):
    """an upper end of the spectral norm of the symmetric ball matrix R (Gershgorin)."""
    best = ZERO
    for d, rad in gersh(R):
        v = (abs(d) + rad).upper()
        best = v if v > best else best
    return best


def setup(ch, P2r, U_hi, vac, DMAX=5, eta_override=None, Gl=None, sblk=None):
    """the ingredients of the bounds on one piece. P2r: the piece's P2 fields as balls (Bp_hi, Bm_hi, Rw_hi, rho1_hi); U_hi: S4-U's
    upper end at the piece's largest t; vac: {'delta', 's', 'sp', 'eps_a', 'Bp'} upper ends. Crude route only (AL is on hold).
    v1_9_1: with route (b)'s Gl (and also with the TT route's), eta+ and eta- come from Gl's even and odd
    principal blocks; that is valid exactly when the chains are exactly parity-pure (the W3 chain's and, for route (b), the B
    chain's par_exact True): then every true cross-parity entry of Gl is 0 and the place-2 balls on those entries only enclose it,
    so each sector's block bounds that sector. The caller gates par_exact (kt_s8_cert: C-PAREXACT and the KILL rule)."""
    K, R, pi, L = ch['K'], ch['R'], ch['pi'], ch['L']
    ev = [k for k in range(K) if pi[k] > 0]
    od = [k for k in range(K) if pi[k] < 0]
    Gl = ch['Gl'] if Gl is None else Gl   # v1_9: route (b) passes routeb_leak's Gl
    BN, Bm = P2r['Bp_hi'], P2r['Bm_hi']   # K-1: |B+| bounds the whole operator B_X
    Rw, rho1 = P2r['Rw_hi'], P2r['rho1_hi']
    etap, etam = lmax_psd_up(Gl, ev).sqrt().upper(), lmax_psd_up(Gl, od).sqrt().upper()
    if eta_override is not None:   # v1_2: C-REPF's like-for-like mode only (the reference's printed eta+, eta-); never in a bound
        etap, etam = eta_override
    eta = etap if etap > etam else etam
    etak = [sqrt_up(Gl[k][k]) for k in range(K)]
    # the Davis-Kahan residual of basis vector k: sqrt(Gl_kk + sum_{l != k} R_lk^2) (R is not diagonal in the fixed basis)
    etar = [sqrt_up(Gl[k][k] + sum((R[l][k] * R[l][k] for l in range(K) if l != k), ZERO)) for k in range(K)]
    trR2 = sum((R[i][j] * R[i][j] for i in range(K) for j in range(K)), ZERO)
    sperp = sqrt_up((U_hi / (ch['lam0'] * ch['lam0'])).upper() - 1 - trR2.lower())
    if sblk is not None:   # v1_9: route (b): the smaller of the K = 3 value and routeb_leak's block bound
        sperp = sperp if sperp < sblk else sblk
    Rn = rnorm_up(R)
    r_ = Rn if Rn > sperp else sperp
    cc = abs(ch['c']).upper()
    pW = ch['pW']
    vacp = vac['eps_a'] + vac['Bp'] * vac['sp']   # places 3 and 5: |p_Y - p~| <= eps_a + |B+| sp
    pc = (sqrt_up(ch['pperp2']) + vacp + vac['s'] * norm_up(pW)).upper()
    pn = (sqrt_up(ch['pnorm2']) + vacp).upper()
    rn1 = {-1: sqrt_up(ch['res2'][(-1, '1')]), 0: sqrt_up(ch['res2'][(0, '1')])}
    rnX = {-1: sqrt_up(ch['res2'][(-1, 'X')]), 0: sqrt_up(ch['res2'][(0, 'X')])}
    rnXo = dict(rnX)
    e0 = sqrt_up(ch['Rw2'])
    e1 = sqrt_up(ch['nS2'] - 1)
    capR = Rw.upper()
    e = {0: e0 if e0 < capR else capR, 1: e1 if e1 < (Rw * rho1).upper() else (Rw * rho1).upper()}
    zc = (ZERO, ZERO, ZERO)
    cerr = {-1: zc, 0: zc, 1: zc, 'inf': zc}
    AXW = sqrt_up(sum((x * x for row in ch['AXm'] for x in row), ZERO))   # Frobenius >= spectral norm
    pWn = norm_up(ch['B']['TM'])

    def gform(v):
        q = ZERO
        for a in range(K):
            for b in range(K):
                q = q + v[a] * v[b] * Gl[a][b]
        return sqrt_up(q)
    rn1[1] = (sperp * rn1[0] + gform(L[0][0][1])).upper()
    for d in range(2, DMAX + 1):
        dlp = cerr[d - 1][0]
        cerr[d] = ((Rn * dlp + etap * rn1[d - 1]).upper(), (AXW * dlp + (BN + cc * etap) * rn1[d - 1]).upper(),
                   (pWn * dlp + pc * rn1[d - 1]).upper())
        nl_ = norm_up(L[d - 1][0][1]) + dlp
        ed = (nl_ * nl_ + rn1[d - 1] * rn1[d - 1]).sqrt().upper()
        cap = (Rw * ipow(rho1, d)).upper()
        e[d] = ed if ed < cap else cap
        rn1[d] = (sperp * rn1[d - 1] + gform(L[d - 1][0][1]) + etap * dlp).upper()
    c = ch['c']
    lpc = lambda d: (abs(L[d - 1][0][0]).upper() * pc).upper()   # v1_8_1: x_d's p_X part is l_u p_X, l_u = 1 +- O(s)
    for d in range(1, DMAX + 1):
        if d <= 2:
            cd = cerr[d]
            l1, lx = L[d]
            kap = abs(lx[0] - c * L[d - 1][0][0]).lower() - cd[2]
            kap = kap if kap > 0 else ZERO
            unc = cd[1] + cc * cd[0]
            wB = [lx[1][k] - ch['B']['TM'][k] - c * l1[1][k] for k in range(K)]
            wn = sqrt_lo(sum((x * x for x in wB), ZERO)) - unc
            wn = wn if wn > 0 else ZERO
            wo = sqrt_lo(sum((wB[k] * wB[k] for k in od), ZERO)) - unc
            wo = wo if wo > 0 else ZERO
            rnX[d] = (lpc(d) + sqrt_up(BN * BN * e[d] * e[d] - kap * kap - wn * wn) + cc * rn1[d]).upper()
            rnXo[d] = (lpc(d) + sqrt_up(Bm * Bm * e[d] * e[d] - wo * wo)).upper()
        else:
            rnX[d] = (lpc(d) + BN * e[d] + cc * rn1[d]).upper()
            rnXo[d] = (lpc(d) + Bm * e[d]).upper()
    rn1['inf'], rnX['inf'], rnXo['inf'] = ZERO, pc, pc
    Ap = {d: sqrt_up(ch['Ap2'][d]) for d in (-1, 0)}   # v1_3: the chain's centered |A_perp|^2
    for d in range(1, DMAX + 1):
        Ap[d] = (abs(L[d][0][0]) * rnX[d] + abs(L[d][1][0]) * rn1[d]).upper()
    Ap['inf'] = pc
    return {'etap': etap, 'etam': etam, 'eta': eta, 'etak': etak, 'etar': etar, 'sperp': sperp, 'r': r_, 'Rn': Rn, 'pc': pc, 'pn': pn,
            'rn1': rn1, 'rnX': rnX, 'rnXo': rnXo, 'e': e, 'cerr': cerr, 'ev': ev, 'od': od, 'Ap': Ap, 'gform': gform, 'BN': BN,
            'Bm': Bm, 'Rw': Rw, 'rho1': rho1, 'cc': cc}


# ---- the lemma, the pair bound, the far end (3g's lemma_g, cov2, sf_pair, far_lo2, in balls with the full R)
def hyp(a, b):
    return (a * a + b * b).sqrt().upper()


def mpow(R, n):
    K = len(R)
    M = [[ONE if i == j else ZERO for j in range(K)] for i in range(K)]
    for _ in range(n):
        M = mmul(M, R)
    return M


def powvecs(R, v, n):
    out = [v]
    for _ in range(n):
        out.append(mv(R, out[-1]))
    return out


def lemma(k, prm, R, xW, dx, xP, yW, dy, yP):
    """T1' (SPEC sect. 4) with the leakage Gram and the full R: an upper end of |<x, S^k y> - <x_W, R^k y_W>|."""
    if k == 0:
        return (xP * yP).upper()
    sp, eta, r, Rn, gform = prm['sperp'], prm['eta'], prm['r'], prm['Rn'], prm['gform']
    Px, Py = powvecs(R, xW, k - 1), powvecs(R, yW, k - 1)
    one = ZERO
    for i in range(k):
        j = k - 1 - i
        one = one + ipow(sp, i) * xP * (gform(Py[j]) + eta * ipow(Rn, j) * dy) + (gform(Px[i]) + eta * ipow(Rn, i) * dx) * ipow(sp, j) * yP
    nx = hyp(norm_up(xW) + dx, xP)
    ny = hyp(norm_up(yW) + dy, yP)
    tail = ipow(r + eta, k) - ipow(r, k) - k * ipow(r, k - 1) * eta
    return (ipow(sp, k) * xP * yP + one + tail * nx * ny).upper()


def mirror(v, kind, pi):
    return v if kind == 'same' else (v[0], [v[1][k] if pi[k] > 0 else -v[1][k] for k in range(len(v[1]))])


def vecs(ch, dL, dR, kind):
    K, pi = ch['K'], ch['pi']
    L1, LX = ch['L'][dL]
    if dR == 'inf':
        R1, RY = (ONE, [ZERO] * K), (ch['c'], list(ch['B']['TM' if kind == 'same' else 'MB']))
    else:
        R1, RY = ch['L'][dR][0], mirror(ch['L'][dR][1], kind, pi)
    return L1, LX, R1, RY


def cov2(ch, dL, dR, kind, Rk):
    """the cancellation-free main term in balls: Num = <A^L_W, R^k A^R_W> + (z xy - x1 y1), Z = L1_u R1_u + z."""
    L1, LX, R1, RY = vecs(ch, dL, dR, kind)
    K = ch['K']
    q = lambda a, b: dot(a, mv(Rk, b))
    z, xy, x1, y1 = q(L1[1], R1[1]), q(LX[1], RY[1]), q(LX[1], R1[1]), q(L1[1], RY[1])
    AL = [L1[0] * LX[1][k] - LX[0] * L1[1][k] for k in range(K)]
    AR = [R1[0] * RY[1][k] - RY[0] * R1[1][k] for k in range(K)]
    num = q(AL, AR) + (z * xy - x1 * y1)
    Zz = L1[0] * R1[0] + z
    return num, Zz, AL, AR, (z, xy, x1, y1), (L1, LX, R1, RY)


def dvec(prm, d, l1, lx):
    e1, eX, eu = prm['cerr'][d]
    return (abs(l1[0]) * eX + abs(lx[0]) * e1 + eu * (norm_up(l1[1]) + prm['rn1'][d])).upper()


def sf_pair(ch, prm, dL, dR, kind, m, RkC, parity=True, zero=False, info=None):
    """the SPEC-form bound (sect. 4 and 6.1) for one class: (Cov mid, Cov_lo, Num_lo, Z_hi, |A^L|, |Q0 l_L|, |Q0 x_L|, Cov_hi). v1_11:
    info, a dict or None: the constants and centered balls of the computation are recorded into it (module docstring); nothing else
    changes."""
    k = m - 1
    if k not in RkC:
        RkC[k] = mpow(ch['R'], k)
    num, Zz, AL, AR, (z, xy, x1, y1), (L1, LX, R1, RY) = cov2(ch, dL, dR, kind, RkC[k])
    R = ch['R']
    rn1, rnX, rnXo = prm['rn1'], prm['rnX'], prm['rnXo']
    ALp, ARp = prm['Ap'][dL], prm['Ap'][dR]
    ALW, ARW = norm_up(AL), norm_up(AR)
    dAL, dAR = dvec(prm, dL, L1, LX), dvec(prm, dR, R1, RY)
    r1k = ipow(prm['Rn'], k)
    e1L, eXL = prm['cerr'][dL][0], prm['cerr'][dL][1]
    e1R, eXR = prm['cerr'][dR][0], prm['cerr'][dR][1]
    lbv = lambda aW, da, aP, bW, db, bP: lemma(k, prm, R, aW, da, aP, bW, db, bP)
    ce = lambda aWn, da, bWn, db: (r1k * (da * bWn + aWn * db + da * db)).upper()
    t1s = lbv(AL, dAL, ALp, AR, dAR, ARp) + ce(ALW, dAL, ARW, dAR)
    if k == 0 and parity and dR != 'inf' and dL == dR:
        mo = (abs(L1[0]) * rnXo[dL]).upper()
        mo = mo if mo < ALp else ALp
        t1 = ZERO if kind == 'same' else mo * mo
    else:
        t1 = lbv(AL, dAL, ALp, AR, dAR, ARp)
    t1 = t1 + ce(ALW, dAL, ARW, dAR)
    nL1, nLX, nR1, nRY = norm_up(L1[1]), norm_up(LX[1]), norm_up(R1[1]), norm_up(RY[1])
    dz = lbv(L1[1], e1L, rn1[dL], R1[1], e1R, rn1[dR]) + ce(nL1, e1L, nR1, e1R)
    dxy = lbv(LX[1], eXL, rnX[dL], RY[1], eXR, rnX[dR]) + ce(nLX, eXL, nRY, eXR)
    dx1 = lbv(LX[1], eXL, rnX[dL], R1[1], e1R, rn1[dR]) + ce(nLX, eXL, nR1, e1R)
    dy1 = lbv(L1[1], e1L, rn1[dL], RY[1], eXR, rnX[dR]) + ce(nL1, e1L, nRY, eXR)
    az, axy, ax1, ay1 = abs(z).upper(), abs(xy).upper(), abs(x1).upper(), abs(y1).upper()
    ddet = (az * dxy + axy * dz + dz * dxy + ax1 * dy1 + ay1 * dx1 + dx1 * dy1).upper()
    if zero:
        t1, t1s, ddet, dz = ZERO, ZERO, ZERO, ZERO
    num_lo = (num.lower() - t1 - ddet).lower()
    num_hi = (num.upper() + t1s + ddet).upper()
    zhi = (abs(Zz).upper() + dz).upper()
    zlo = (abs(Zz).lower() - dz).lower()
    if num_lo >= 0:
        cov_lo = (num_lo / (zhi * zhi)).lower()
    else:
        cov_lo = (num_lo / (zlo * zlo)).lower() if zlo > 0 else NEGINF
    if num_hi >= 0:
        cov_hi = (num_hi / (zlo * zlo)).upper() if zlo > 0 else POSINF
    else:
        cov_hi = (num_hi / (zhi * zhi)).upper()
    v = float((num / (Zz * Zz)).mid())
    if info is not None:   # v1_11: a record only
        info.update({'k': k, 't1': t1, 't1s': t1s, 'ddet': ddet, 'dz': dz, 'C1': t1 + ddet, 'Zz': Zz, 'num': num, 'plain_lo': cov_lo})
    if 'dual' in ch and not zero:
        # v1_2: the class-level mean-value form. With C1 = t1 + ddet and dz fixed upper ends over the box, Cov >= (Num - C1)/(|Z| + dz)^2
        # when Num - C1 >= 0 (else with |Z| - dz); Num and Z are evaluated as duals over the entry box (their correlation kept), so
        # the bound's entry dependence is first order, as in 3g's per-class bars. The larger of this and the plain bound is kept.
        chd, chm, rad = ch['dual']
        if ('d', k) not in RkC:
            RkC[('d', k)] = mpow(chd['R'], k)
            RkC[('m', k)] = mpow(chm['R'], k)
        numd, Zd = cov2(chd, dL, dR, kind, RkC[('d', k)])[:2]
        numm, Zm = cov2(chm, dL, dR, kind, RkC[('m', k)])[:2]
        sg = ONE if Zz.lower() > 0 else -ONE
        C1 = t1 + ddet
        if Zz.lower() > 0 or Zz.upper() < 0:
            topc = _cen(numd - C1, numm - C1, rad)
            if info is not None:   # v1_11: a record only
                info.update({'sg': sg, 'topc': topc, 'cen': {}})

            def gl(dd, key):   # the lower end over the box of (Num - C1)/(|Z| + dd)^2, or None if |Z| + dd may vanish
                if not (abs(Zz).lower() + dd).lower() > 0:
                    if info is not None:   # v1_11: key '+dz' or '-dz', a record only
                        info['cen'][key] = None
                    return None
                cb = _cen((numd - C1) / ((sg * Zd + dd) * (sg * Zd + dd)), (numm - C1) / ((sg * Zm + dd) * (sg * Zm + dd)), rad)
                if info is not None:
                    info['cen'][key] = cb
                return cb.lower()
            if topc.lower() >= 0:          # Num - C1 >= 0 on the whole box: the + dz denominator
                cl2 = gl(dz, '+dz')
            elif topc.upper() <= 0:        # Num - C1 <= 0 on the whole box: the - dz denominator
                cl2 = gl(-dz, '-dz')
            else:                          # straddling: the smaller of both lower ends holds for every point of the box
                gp, gm = gl(dz, '+dz'), gl(-dz, '-dz')
                cl2 = None if (gp is None or gm is None) else (gp if gp < gm else gm)
            if info is not None:   # v1_11: a record only
                info.update({'cl2': cl2, 'used': bool(cl2 is not None and cl2 > cov_lo)})
            if cl2 is not None and cl2 > cov_lo:
                cov_lo = cl2
        v = float((numm / (Zm * Zm)).mid())
    nAL = hyp(ALW + dAL, ALp)
    nl = hyp(nL1 + e1L, rn1[dL])
    nx = hyp(nLX + eXL, rnX[dL])
    return v, cov_lo, num_lo, zhi, nAL, nl, nx, cov_hi


def far_lo2(ch, prm, dL, kind, m, base, dR):
    """S8-1 by the crude far-end perturbation at an explicit far exponent dR (SPEC sect. 2, T4; K-1's |B+|)."""
    v, cov_lo, num_lo, zhi, nAL, nl, nx = base[:7]
    k = m - 1
    eR = (prm['Rw'] * ipow(prm['rho1'], dR)).upper()
    eR1 = (prm['Rw'] * ipow(prm['rho1'], dR + 1)).upper()
    pn = prm['pn']
    dfar = (prm['BN'] * eR + pn * eR * eR1).upper()
    rk = ipow(prm['r'] + prm['eta'], k).upper()
    ny = (pn + dfar + prm['cc'] * eR1).upper()
    num2 = (num_lo - nAL * rk * dfar - 2 * rk * rk * nl * eR1 * nx * ny).lower()
    z2 = (zhi + rk * nl * eR1).upper()
    return v, ((num2 / (z2 * z2)).lower() if num2 >= 0 else NEGINF)


def head(v, lo):
    """the headroom Cov / (Cov - Cov_lo) as a float; when Cov_lo >= Cov: inf if Cov_lo > 0, else 0, a failing value (v1_5)."""
    lo_f = float(lo.mid())
    lo_f = lo_f if math.isfinite(lo_f) else -1e300
    if v > lo_f:
        return v / (v - lo_f)
    return float('inf') if lo_f > 0 else 0.0


# ---- the top-mode form (3g's dk_setup and dk_class: Weyl, Davis-Kahan, Lemma C4 with the sign condition C-SIGN-C4)
SQ2 = ONE.__class__(2).sqrt()
DFAR = {'flip': 3, 'same': 1}
DNEAR = {'flip': (-1, 0, 1, 2), 'same': (-1, 0)}
MM, M1 = 16, 4


def dk_setup(ch, prm):
    R = ch['R']
    ev, od = prm['ev'], prm['od']
    gd = gersh(R)
    lo_k = [(gd[k][0] - gd[k][1]).lower() for k in range(len(R))]
    hi_k = [(gd[k][0] + gd[k][1]).upper() for k in range(len(R))]
    k1 = max(ev, key=lambda k: float(gd[k][0].mid()))
    ko = max(od, key=lambda k: float(gd[k][0].mid()))
    k3 = [k for k in ev if k != k1]
    sp_, etap, etam = prm['sperp'], prm['etap'], prm['etam']
    top3 = sp_
    for k in k3:
        top3 = hi_k[k] if hi_k[k] > top3 else top3
    topo = sp_   # v1_8_1: with K = 9, W holds odd modes besides ko; in v1_6 (one odd mode) topo = s_perp
    for k in od:
        if k != ko and hi_k[k] > topo:
            topo = hi_k[k]
    g1 = (lo_k[k1] - top3 - etap).lower()
    go = (lo_k[ko] - topo - etam).lower()
    s1 = (prm['etar'][k1] / g1).upper() if g1 > 0 else ONE
    s1 = s1 if s1 < ONE else ONE
    so = (prm['etar'][ko] / go).upper() if go > 0 else ONE
    so = so if so < ONE else ONE
    rx = (lo_k[k1] - etap).lower()
    emax = etap if etap > etam else etam
    qo = ((hi_k[ko] + etam) / rx).upper() if rx > 0 else POSINF
    qr = (((top3 if top3 > topo else topo) + emax) / rx).upper() if rx > 0 else POSINF
    qd = (ipow(prm['r'] + prm['eta'], 2) / rx).upper() if rx > 0 else POSINF
    ok = g1 > 0 and go > 0 and qo < 1 and qr < 1 and qd < 1
    return {'k1': k1, 'ko': ko, 's1': s1, 'so': so, 'g1': g1, 'go': go, 'qo': qo, 'qr': qr, 'qd': qd, 'ok': ok}


def dk_class(ch, prm, dk, dL, dR, kind, kmax=400):
    """R(k) = P_lo - q_o^k O - q_r^k Rr - q_d^k Dc; returns (k0 or None, P_lo, R(MM), R(M1), A^L_1, A^R_1, u_a, u_b). The class has
    a top-mode cover only if A^L_1 and A^R_1 have one certified sign with |A^L_1| > u_a and |A^R_1| > u_b (C-SIGN-C4)."""
    far = dR == 'far'
    dRr = 'inf' if far else dR
    L1, LX, R1, RY = vecs(ch, dL, dRr, kind)
    K = ch['K']
    AL = [L1[0] * LX[1][k] - LX[0] * L1[1][k] for k in range(K)]
    AR = [R1[0] * RY[1][k] - RY[0] * R1[1][k] for k in range(K)]
    rn1, rnX, cerr = prm['rn1'], prm['rnX'], prm['cerr']
    ALp, ARp = prm['Ap'][dL], prm['Ap'][dRr]
    dAL, dAR = dvec(prm, dL, L1, LX), dvec(prm, dRr, R1, RY)
    dfar, Dc = ZERO, ZERO
    nl = hyp(norm_up(L1[1]) + cerr[dL][0], rn1[dL])
    nx = hyp(norm_up(LX[1]) + cerr[dL][1], rnX[dL])
    if far:
        dRf = DFAR[kind]
        eR = (prm['Rw'] * ipow(prm['rho1'], dRf)).upper()
        eR1 = (prm['Rw'] * ipow(prm['rho1'], dRf + 1)).upper()
        pn = prm['pn']
        dfar = (prm['BN'] * eR + pn * eR * eR1).upper()
        Dc = (2 * nl * eR1 * nx * (pn + dfar + prm['cc'] * eR1)).upper()
    elif dR != 'inf':
        nlr = hyp(norm_up(R1[1]) + cerr[dR][0], rn1[dR])
        nyr = hyp(norm_up(RY[1]) + cerr[dR][1], rnX[dR])
        Dc = (2 * nl * nlr * nx * nyr).upper()
    nAL = hyp(norm_up(AL) + dAL, ALp)
    nAR = (hyp(norm_up(AR) + dAR, ARp) + dfar).upper()
    k1, ko = dk['k1'], dk['ko']
    ua = (SQ2 * dk['s1'] * nAL + dAL).upper()
    ub = (SQ2 * dk['s1'] * nAR + dAR + dfar).upper()
    a, b = AL[k1], AR[k1]
    same_sign = (a.lower() > 0 and b.lower() > 0) or (a.upper() < 0 and b.upper() < 0)
    if not dk['ok'] or not same_sign or not abs(a).lower() > ua or not abs(b).lower() > ub:
        return None, arb(-1), arb(-1), arb(-1), a, b, ua, ub
    alo, blo = (abs(a).lower() - ua).lower(), (abs(b).lower() - ub).lower()
    P = (alo * blo).lower()
    O = ((abs(AL[ko]).upper() + SQ2 * dk['so'] * nAL + dAL) * (abs(AR[ko]).upper() + SQ2 * dk['so'] * nAR + dAR + dfar)).upper()
    Rr = (sqrt_up(nAL * nAL - alo * alo) * sqrt_up(nAR * nAR - blo * blo)).upper()
    Rk = lambda k: (P - ipow(dk['qo'], k) * O - ipow(dk['qr'], k) * Rr - ipow(dk['qd'], k) * Dc).lower()
    k0 = next((k for k in range(kmax + 1) if Rk(k) > 0), None)
    return k0, P, Rk(MM), Rk(M1), a, b, ua, ub


def head_s81(ch, prm, dL, kind, m, RkC):
    """S8-1 at (dL, kind, m): the better of route A (crude far end at D_far) and route B (two-sided chain at D_far .. D_far + 2 and the
    crude term at D_far + 3); each holds for every d_R >= D_far."""
    base = sf_pair(ch, prm, dL, 'inf', kind, m, RkC)
    fa = far_lo2(ch, prm, dL, kind, m, base, DFAR[kind])
    hA = head(fa[0], fa[1])
    if m > 7:
        return hA, hA, float('nan')
    hB = head(fa[0], far_lo2(ch, prm, dL, kind, m, base, DFAR[kind] + 3)[1])
    for j in (0, 1, 2):
        b = sf_pair(ch, prm, dL, DFAR[kind] + j, kind, m, RkC)
        h = head(b[0], b[1])
        hB = h if h < hB else hB
    return (hA if hA > hB else hB), hA, hB


def rows_for(ch, prm, two_cls, s83_rows, RkC):
    """every row of the route rule on one piece: S8-1 and S8-2 below each class's m0, the one-sided lemma rows at m = 2..M1, and
    S8-3 per n = 4 pair as max(strip, chain), the chain counted only with its own bound (no top mode below m0). s83_rows: [(label,
    strip headroom or None, chain class or None)]. A class whose top mode fails or has m0 > 8 is a 'top' row at 0."""
    dkf = dk_setup(ch, prm)
    m0, top = {}, {}
    for kind in ('flip', 'same'):
        for dL in DNEAR[kind]:
            r_ = dk_class(ch, prm, dkf, dL, 'far', kind)
            m0[('S8-1', dL, kind)] = (r_[0] + 1) if r_[0] is not None else None
            top[('S8-1', dL, kind)] = r_
            for dR in DNEAR[kind]:
                r_ = dk_class(ch, prm, dkf, dL, dR, kind)
                m0[('S8-2', dL, dR, kind)] = (r_[0] + 1) if r_[0] is not None else None
                top[('S8-2', dL, dR, kind)] = r_
    fam = {f_: [] for f_ in ('S8-1', 'S8-2', 'S8-3', 'lemma', 'top')}
    for key_, v in sorted(m0.items(), key=str):
        if v is None or v > 8:
            fam['top'].append((0.0, key_))
    for cl in two_cls:
        dL, dR, kind, m = cl
        mm0 = m0[('S8-2', dL, dR, kind)]
        if dL + dR + m + 3 < 5 or (mm0 is not None and m >= mm0):
            continue
        b = sf_pair(ch, prm, dL, dR, kind, m, RkC)
        fam['S8-2'].append((head(b[0], b[1]), cl))
    for kind in ('flip', 'same'):
        for dL in DNEAR[kind]:
            mm0 = m0[('S8-1', dL, kind)]
            for m in range(1, mm0 if mm0 is not None else 9):
                fam['S8-1'].append((head_s81(ch, prm, dL, kind, m, RkC)[0], (dL, kind, m)))
            for m in range(2, M1 + 1):
                b = sf_pair(ch, prm, dL, 'inf', kind, m, RkC)
                fam['lemma'].append((head(b[0], b[1]), (dL, 'inf', kind, m)))
    for lab, hs, cl in s83_rows:
        hc = None
        if cl is not None:
            b = sf_pair(ch, prm, *cl, RkC)
            hc = head(b[0], b[1])
        best = max(x for x in (hs, hc, 0.0) if x is not None)
        fam['S8-3'].append((best, lab, hs, hc, cl))
    return fam, m0, top, dkf


# ---- v1_1: the centered (mean-value) form of the chain, against interval dependency
class D:
    """forward-mode dual for the mean-value form: v = the value ball over the entry box, g = the gradient balls over the box (one per
    entry variable). f(x) lies in f(x_mid) + sum_i g_i [-r_i, r_i] for every x in the box (the mean-value theorem, g enclosing the
    gradient at every point of the box)."""
    __slots__ = ('v', 'g')

    def __init__(self, v, g):
        self.v, self.g = v, g

    @staticmethod
    def var(v, i, n):
        g = [ZERO] * n
        g[i] = ONE
        return D(v, g)

    def __add__(self, o):
        if isinstance(o, D):
            return D(self.v + o.v, [a + b for a, b in zip(self.g, o.g)])
        return D(self.v + o, self.g)

    __radd__ = __add__

    def __neg__(self):
        return D(-self.v, [-a for a in self.g])

    def __sub__(self, o):
        if isinstance(o, D):
            return D(self.v - o.v, [a - b for a, b in zip(self.g, o.g)])
        return D(self.v - o, self.g)

    def __rsub__(self, o):
        return D(o - self.v, [-a for a in self.g])

    def __mul__(self, o):
        if isinstance(o, D):
            return D(self.v * o.v, [a * o.v + self.v * b for a, b in zip(self.g, o.g)])
        return D(self.v * o, [a * o for a in self.g])

    __rmul__ = __mul__

    def __truediv__(self, o):
        if isinstance(o, D):
            inv = ONE / _nz(o.v, 'a dual divisor')   # v1_10 (C5)
            q = self.v * inv
            return D(q, [(a - q * b) * inv for a, b in zip(self.g, o.g)])
        inv = ONE / _nz(o, 'a divisor of a dual')
        return D(self.v * inv, [a * inv for a in self.g])

    def __rtruediv__(self, o):
        inv = ONE / _nz(self.v, 'a dual divisor')   # v1_10 (C5)
        q = o * inv
        return D(q, [-(q * a) * inv for a in self.g])

    def sqrt(self):
        _pos(self.v, 'a dual\'s square-root argument')   # v1_10 (C5)
        r = self.v.sqrt()
        h = ONE / (2 * r)
        return D(r, [a * h for a in self.g])

    def lower(self):
        return self.v.lower()

    def upper(self):
        return self.v.upper()

    def mid(self):
        return self.v.mid()

    def __abs__(self):
        return abs(self.v)   # a constant: used only where 3g's code takes an end of |x| for a radius


def _cen(qd, qm, rad):
    """the centered ball of a dual qd (qm: the same quantity at the midpoints), intersected with the dual's own value ball. v1_10 (C6;
    The review CHECK_O3 0226c38c): both balls hold the true value, so an empty intersection is a bug signal and raises ValueError instead of
    returning the ball between the two disjoint ends."""
    if isinstance(qd, D):
        c = qm + sum((g * pm(r) for g, r in zip(qd.g, rad)), ZERO)
        lo_ = c.lower() if c.lower() > qd.v.lower() else qd.v.lower()
        hi_ = c.upper() if c.upper() < qd.v.upper() else qd.v.upper()
        if not (lo_ <= hi_):
            raise ValueError('C6: the centered ball %s and the dual\'s value ball %s are disjoint' % (c, qd.v))
        return span(lo_, hi_)
    if isinstance(qd, tuple):
        return tuple(_cen(a, b, rad) for a, b in zip(qd, qm))
    if isinstance(qd, list):
        return [_cen(a, b, rad) for a, b in zip(qd, qm)]
    if isinstance(qd, dict):
        return {k: _cen(qd[k], qm[k], rad) for k in qd}
    return qd


def centered(fun, V, *args):
    """fun(V, *args) in its mean-value form over the entry box V ({key: ball}): one evaluation in duals over the box, one at the exact
    midpoints, combined leaf by leaf (_cen). Every leaf holds the true value for every point of the box."""
    keys = sorted(V, key=str)
    n = len(keys)
    Vd = {k: D.var(V[k], i, n) for i, k in enumerate(keys)}
    Vm = {k: arb(V[k].mid()) for k in keys}
    rad = [V[k].rad() for k in keys]
    return _cen(fun(Vd, *args), fun(Vm, *args), rad)


def chain_dual(V, mains, odd_states, vac, C0, nst=3):
    """v1_2: chain_centered's balls, plus ch['dual'] = (the chain in duals over the entry box, the chain at the midpoints, the radii)
    for sf_pair's class-level mean-value form."""
    keys = sorted(V, key=str)
    n = len(keys)
    Vd = {k: D.var(V[k], i, n) for i, k in enumerate(keys)}
    Vm = {k: arb(V[k].mid()) for k in keys}
    rad = [V[k].rad() for k in keys]
    chd = chain(Vd, mains, odd_states, vac, C0, nst)
    chm = chain(Vm, mains, odd_states, vac, C0, nst, allow=chd['allow'], par=chd['par_exact'])   # v1_6: the dual run's
    chc = _cen(chd, chm, rad)
    chc['dual'] = (chd, chm, rad)
    return chc


def chain_centered(V, mains, odd_states, vac, C0, nst=3):
    """chain() in the mean-value form over the entry box (v1_1; v1_6: the midpoint run takes the dual run's allowances)."""
    keys = sorted(V, key=str)
    n = len(keys)
    chd = chain({k: D.var(V[k], i, n) for i, k in enumerate(keys)}, mains, odd_states, vac, C0, nst)
    chm = chain({k: arb(V[k].mid()) for k in keys}, mains, odd_states, vac, C0, nst, allow=chd['allow'], par=chd['par_exact'])
    return _cen(chd, chm, [V[k].rad() for k in keys])


def strip_cov(V4):
    """S8-3's whole strip in the mean-value form: Cov J^2 = N_XY/Z - N_X N_Y/Z^2; V4 = {'Z', 'X', 'Y', 'XY'} balls."""
    f = lambda W: W['XY'] / W['Z'] - W['X'] * W['Y'] / (W['Z'] * W['Z'])
    return centered(f, V4)


def dual_selftest():
    """C-DUAL: the dual's gradient of f = sqrt(x y + 1/z) - x/(1 + y) against central differences at a point, and an arb + dual sum."""
    x, y, z = arb('0.3'), arb('1.7'), arb('2.9')
    f = lambda a, b, c: (a * b + ONE / c).sqrt() - a / (1 + b)
    d = f(D.var(x, 0, 3), D.var(y, 1, 3), D.var(z, 2, 3))
    h = arb('1e-30')
    fd = [(f(x + h, y, z) - f(x - h, y, z)) / (2 * h), (f(x, y + h, z) - f(x, y - h, z)) / (2 * h), (f(x, y, z + h) - f(x, y, z - h)) / (2 * h)]
    err = max(float(abs(a - b).upper()) for a, b in zip(d.g, fd))
    s = sum((D.var(x, 0, 1) * k for k in (ONE, arb(2))), ZERO)
    ok = err < 1e-25 and isinstance(s, D) and abs(float(s.g[0].mid()) - 3.0) < 1e-30
    return ok, err


# ---- v1_4 (stage C): pieces in J with t as one more slot of the mean-value form; the rows with their certified lower ends
def tpoints(jlo, jhi, n=9):
    """n equispaced exact points of the piece's t-range [1/jhi, 1/jlo] (jhi may be inf: t from 0), as balls (C-UNIF, C-MV)."""
    tl = Fraction(0) if math.isinf(jhi) else 1 / Fraction(jhi)
    th = 1 / Fraction(jlo)
    return [fr(tl + (th - tl) * j / (n - 1)) for j in range(n)]


def entry_points(E, t):
    """the bar-free entry values at t (a ball): {key: sum_k [LO_k, HI_k] t^k}."""
    tk = [ONE, t, t * t, t * t * t]
    return {key: sum((span(LO[k], HI[k]) * tk[k] for k in range(4)), ZERO) for key, (LO, HI, err) in E.items()}


def entry_duals(E, T, zero_bars=False, zero_tgrad=False):
    """the entries on a piece box (t in the ball T, each bar offset in [-err_b, err_b]) as duals: slot 0 is t, slot i + 1 the bar
    offset of the i-th key (sorted by str). Returns (keys, Vd, Vm, rad): Vd[key] = D(sum_k [LO_k, HI_k] T^k + [-err_b, err_b],
    [sum_k k [LO_k, HI_k] T^(k-1)] + unit), Vm[key] = sum_k [LO_k, HI_k] t_m^k at the center t_m = mid(T), rad = [rad(T), err_b...].
    For every a_k of its interval, f over the box lies in f(Vm) + sum_j g_j [-rad_j, rad_j] (the mean-value theorem in (t, bars)).
    zero_bars: every err_b taken as 0 (C-MV); zero_tgrad: the t-gradients set to 0 (PLANT-MV)."""
    keys = sorted(E, key=str)
    n = len(keys) + 1
    tm = arb(T.mid())
    tk = [ONE, T, T * T, T * T * T]
    tmk = [ONE, tm, tm * tm, tm * tm * tm]
    Vd, Vm, rad = {}, {}, [arb(T.rad())]
    for i, key in enumerate(keys):
        LO, HI, err = E[key]
        a = [span(LO[k], HI[k]) for k in range(4)]
        b = ZERO if zero_bars else fr(err)
        g = [ZERO] * n
        g[0] = ZERO if zero_tgrad else (a[1] + 2 * a[2] * T + 3 * a[3] * T * T)
        g[i + 1] = ONE
        Vd[key] = D(sum((a[k] * tk[k] for k in range(4)), ZERO) + pm(b), g)
        Vm[key] = sum((a[k] * tmk[k] for k in range(4)), ZERO)
        rad.append(b)
    return keys, Vd, Vm, rad


def chain_dual_t(E, T, mains, odd_states, vac, C0, nst=3, zero_bars=False, zero_tgrad=False, tt=True):
    """the chain on a piece box in the mean-value form with t as slot 0 (E: {chain key: (LO, HI, err_b)}); ch['dual'] = (the chain in
    duals, the chain at the center, the radii) for sf_pair's class-level form, as chain_dual."""
    keys, Vd, Vm, rad = entry_duals(E, T, zero_bars, zero_tgrad)
    chd = chain(Vd, mains, odd_states, vac, C0, nst, tt=tt)
    chm = chain(Vm, mains, odd_states, vac, C0, nst, allow=chd['allow'], par=chd['par_exact'], tt=tt)   # v1_6: the dual run's
    chc = _cen(chd, chm, rad)
    chc['dual'] = (chd, chm, rad)
    return chc


def strip_cov_t(E4, T):
    """S8-3's whole strip on a piece box in the mean-value form with t as slot 0: Cov J^2 = N_XY/Z - N_X N_Y/Z^2; E4 = {'Z', 'X', 'Y',
    'XY'}: (LO, HI, err_b)."""
    def f(W):
        Z = _nz(W['Z'], 'the strip\'s Z')   # v1_10 (C5)
        return W['XY'] / Z - W['X'] * W['Y'] / (Z * Z)
    keys, Vd, Vm, rad = entry_duals(E4, T)
    return _cen(f(Vd), f(Vm), rad)


def leaves(q, path=''):
    """the ball leaves of a chain dict, by path (C-MV, C-PIECE); 'dual' and 'allow' (v1_6) are skipped, integers are not leaves."""
    if isinstance(q, arb):
        yield path, q
    elif isinstance(q, dict):
        for k in sorted(q, key=str):
            if k not in ('dual', 'allow', 'par_exact'):
                yield from leaves(q[k], '%s/%s' % (path, k))
    elif isinstance(q, (list, tuple)):
        for i, x in enumerate(q):
            yield from leaves(x, '%s/%d' % (path, i))


def inside(outer, inner, rel=0):
    """the ball inner inside the ball outer, with a slack of rel |outer| on each side (False for NaN or infinite ends)."""
    s = ZERO if rel == 0 else abs(outer).upper() * rel
    return bool(inner.lower() >= (outer.lower() - s).lower() and inner.upper() <= (outer.upper() + s).upper())


def mv_check(E, T, tpts, mains, odd_states, vac, C0, zero_tgrad=False):
    """C-MV: the bar-free chain on the piece in the mean-value form (the t slot only) contains, leaf by leaf, the bar-free point chains
    at the points tpts (balls inside T). Returns (the number of leaves, the failing leaf paths). zero_tgrad is PLANT-MV."""
    cen = chain_dual_t(E, T, mains, odd_states, vac, C0, zero_bars=True, zero_tgrad=zero_tgrad)
    cl = dict(leaves(cen))
    bad = set()
    for t in tpts:
        for p, v in leaves(chain(entry_points(E, t), mains, odd_states, vac, C0)):
            if p not in cl or not inside(cl[p], v):
                bad.add(p)
    return len(cl), sorted(bad)


def unif_check(E, T, tpts):
    """C-UNIF (entries): the bar-free entry balls on T contain their values at the points tpts; returns the failing keys."""
    enc = entry_points(E, T)
    bad = set()
    for t in tpts:
        for k, v in entry_points(E, t).items():
            if not inside(enc[k], v):
                bad.add(k)
    return sorted(bad, key=str)


def s81_cert(ch, prm, dL, kind, m, RkC):
    """head_s81 with the certified lower end: (headroom, lo), lo = max(route A, min over route B), a lower end of Cov for every
    d_R >= D_far, since each route covers every such d_R."""
    base = sf_pair(ch, prm, dL, 'inf', kind, m, RkC)
    fa = far_lo2(ch, prm, dL, kind, m, base, DFAR[kind])
    hA, loA = head(fa[0], fa[1]), fa[1]
    if m > 7:
        return hA, loA
    fb = far_lo2(ch, prm, dL, kind, m, base, DFAR[kind] + 3)
    hB, loB = head(fa[0], fb[1]), fb[1]
    for j in (0, 1, 2):
        b = sf_pair(ch, prm, dL, DFAR[kind] + j, kind, m, RkC)
        h = head(b[0], b[1])
        hB = h if h < hB else hB
        loB = b[1] if b[1] < loB else loB
    return (hA if hA > hB else hB), (loA if loA > loB else loB)


def rows_cert(ch, prm, two_cls, s83, RkC, m0max=8):
    """rows_for with each row's certified lower end, for stage C's kill rule. Returns (rows, tops, m0, top, dkf):
    rows = [(family, class, headroom, lo, ok)] with ok = lo > 0 for S8-1, S8-2 and the lemma rows; for S8-3 lo = (strip lower end or
    None, chain lower end or None) and ok when either is > 0; tops = [(class key, m0, ok)] with ok = a top-mode cover (C-SIGN-C4
    included) and m0 <= m0max. s83: [(label, the strip ball or None, the chain class or None)]."""
    dkf = dk_setup(ch, prm)
    m0, top = {}, {}
    for kind in ('flip', 'same'):
        for dL in DNEAR[kind]:
            r_ = dk_class(ch, prm, dkf, dL, 'far', kind)
            m0[('S8-1', dL, kind)] = (r_[0] + 1) if r_[0] is not None else None
            top[('S8-1', dL, kind)] = r_
            for dR in DNEAR[kind]:
                r_ = dk_class(ch, prm, dkf, dL, dR, kind)
                m0[('S8-2', dL, dR, kind)] = (r_[0] + 1) if r_[0] is not None else None
                top[('S8-2', dL, dR, kind)] = r_
    tops = [(k, v, v is not None and v <= m0max) for k, v in sorted(m0.items(), key=str)]
    rows = []
    for cl in two_cls:
        dL, dR, kind, m = cl
        mm0 = m0[('S8-2', dL, dR, kind)]
        if dL + dR + m + 3 < 5 or (mm0 is not None and m >= mm0):
            continue
        b = sf_pair(ch, prm, dL, dR, kind, m, RkC)
        rows.append(('S8-2', cl, head(b[0], b[1]), b[1], bool(b[1] > 0)))
    for kind in ('flip', 'same'):
        for dL in DNEAR[kind]:
            mm0 = m0[('S8-1', dL, kind)]
            for m in range(1, mm0 if mm0 is not None else 9):
                h, lo_ = s81_cert(ch, prm, dL, kind, m, RkC)
                rows.append(('S8-1', (dL, kind, m), h, lo_, bool(lo_ > 0)))
            for m in range(2, M1 + 1):
                b = sf_pair(ch, prm, dL, 'inf', kind, m, RkC)
                rows.append(('lemma', (dL, 'inf', kind, m), head(b[0], b[1]), b[1], bool(b[1] > 0)))
    for lab, sb, cl in s83:
        hs, ls = (head(float(sb.mid()), sb.lower()), sb.lower()) if sb is not None else (None, None)
        hc, lc = None, None
        if cl is not None:
            b = sf_pair(ch, prm, *cl, RkC)
            hc, lc = head(b[0], b[1]), b[1]
        ok = bool((ls is not None and ls > 0) or (lc is not None and lc > 0))
        rows.append(('S8-3', lab, max(x for x in (hs, hc, 0.0) if x is not None), (ls, lc), ok))
    return rows, tops, m0, top, dkf


# ---- v1_8: S8 on the ten-state basis B (K = 9), no 4-column entry (the rules of 2026-11-07
# sect. 1-2, REVIEW_XKIND_KFACTOR 210303a9)
def chain_B(V, mains, rhoF3, odd_states, vac, C0, allow=None, par=None, nst=9):
    """the chain on one piece on B = span(u) + W_B, W_B the Q0-projected trial states 1..9 (K = 9), in balls (or duals). V: {chain
    key: value} with the 3-column entries g, T, TX, TXX (states 0..9), e, eX, f, fX, DY (0..9), DYY, z, wXw, wXwX, fXX,0 and the F3
    entries wTw, wTXw, wTXXw; mains: chain()'s five ratios (rhoE and rmain are used); rhoF3: main(F3) main(D)^2 / (main(E2)^2 main(N));
    C0: the binary64 basis, 9 rows over states 1..9 (each row exactly parity-pure). Returns chain()'s dict for K = 9 (R = R_99 with
    place 2's 4 s^2; L[d] with nine components, L[1..7] the B steps of L[0]; the d = -1 norms relative to B; p_X's components on W_B),
    plus R99F2 = |R_99|_F^2 (U9), Phi = (Phi_0, Phi_1, Phi_2) and M = (M_0, M_1, M_2) (the K form) and gam0 = x_u/l_u at d = 0:
    - Phi_j = <r, T_xi^j r>/lambda_0 with r = w-hat - psi-hat_n (the trial normalization: w-hat's psi-hat component is 1), from the
      F3 entry, E3's f/fX/fXX at state 0 and N's T/TX/TXX at (0, 0):
        Phi_j = rhoF3 wT(xi^j)w g00/(e0^2 lambda_0) - 2 rhoE f(xi^j)_0/(lambda_0 e0) + T(xi^j)_00/(g00 lambda_0);
    - M_j = C [T_xi^j]'' C^T / lambda_0 (9 x 9; M_0 is R before place 2's allowance), so that for y in W_B,
      |(xi - gamma) K* y|^2 = y^T (M_2 - 2 gamma M_1 + gamma^2 M_0) y (T_xi^j = K xi^j K*, K = V^(1/2) on the int column)."""
    rhoE, rmain = mains[0], mains[1]
    rng = range(nst + 1)
    K = nst
    sym = lambda nm, a, b: V[(nm, min(a, b), max(a, b))]
    g = [[sym('g', a, b) for b in rng] for a in rng]
    T = [[sym('T', a, b) for b in rng] for a in rng]
    TX = [[sym('TX', a, b) for b in rng] for a in rng]
    TXX = [[sym('TXX', a, b) for b in rng] for a in rng]
    e = [V[('e', a)] for a in rng]
    eX = [V[('eX', a)] for a in rng]
    f = [V[('f', a)] for a in rng]
    fX = [V[('fX', a)] for a in rng]
    g00 = _pos(g[0][0], 'g00')   # v1_10 (C5), as chain()
    _nz(T[0][0], 'T00')
    _nz(e[0], 'e_0')
    _nz(rmain, 'rmain')
    sg = g00.sqrt()
    lam0 = _nz(T[0][0] / g00 * (ONE + pm(vac['delta'])), 'lam0')   # place 1
    s2 = vac['s'] * vac['s']

    def p2(M, a, b):
        return M[a][b] - g[a][0] / g00 * M[0][b] - g[b][0] / g00 * M[a][0] + g[a][0] * g[b][0] / (g00 * g00) * M[0][0]
    idx = list(range(1, K + 1))
    G2 = [[p2(g, a, b) for b in idx] for a in idx]
    T2 = [[p2(T, a, b) for b in idx] for a in idx]
    X2 = [[p2(TX, a, b) for b in idx] for a in idx]
    XX2 = [[p2(TXX, a, b) for b in idx] for a in idx]
    C0b = [[arb(x) for x in row] for row in C0]
    Gf = mmul(mmul(C0b, G2), mT(C0b))
    C = mmul(chol_inv(Gf), C0b)   # rows: an orthonormal basis e_1..e_9 of W0_B (exact in balls)
    sand = lambda M: [[x / lam0 for x in row] for row in mmul(mmul(C, M), mT(C))]
    M0 = sand(T2)
    M1 = sand(X2)
    M2 = sand(XX2)
    R = [[x + pm(4 * s2) for x in row] for row in M0]   # place 2, as chain()
    c = TX[0][0] / T[0][0] + pm(4 * vac['sp'])          # place 3
    odd = [1 if (a in odd_states) else 0 for a in idx]
    pi = [(-1 if sum(C0[k][i] ** 2 for i in range(K) if odd[i]) > sum(C0[k][i] ** 2 for i in range(K) if not odd[i]) else 1)
          for k in range(K)]
    p1 = lambda M, n: M[n][0] - g[n][0] / g00 * M[0][0]
    p1v = lambda vec, n: vec[n] - g[n][0] / g00 * vec[0]
    Tp = [p1(T, n) for n in idx]
    BTM = [sum((C[k][i] * (p1(TX, n) - c * Tp[i]) for i, n in enumerate(idx)), ZERO) / (lam0 * sg) + pm(vac['Bp'] * vac['sp'])
           for k in range(K)]
    B = {'TM': BTM, 'MB': [BTM[k] if pi[k] > 0 else -BTM[k] for k in range(K)]}
    # v1_8_1: place 2 for the A_X block, as in chain(): 2 s |p_W| + 4 (|B+| + |c|) s^2 per entry, the dual run's constant
    a1 = allow['AX'] if allow is not None else (2 * vac['s'] * norm_up(BTM) + 4 * (vac['Bp'] + abs(c).upper()) * s2).upper()
    beta = [[M1[i][j] - c * M0[i][j] + pm(a1) for j in range(K)] for i in range(K)]
    AXm = [[beta[i][j] + c * R[i][j] for j in range(K)] for i in range(K)]

    def comps(vec, scale):
        return [scale * sum((C[k][i] * p1v(vec, n) for i, n in enumerate(idx)), ZERO) for k in range(K)]
    L = {}
    L[-1] = ((ONE, comps(e, sg / e[0])), (eX[0] / e[0], comps(eX, sg / e[0])))
    L[0] = ((rhoE * f[0] / (lam0 * e[0]), comps(f, rhoE * sg / (lam0 * e[0]))),
            (rhoE * fX[0] / (lam0 * e[0]), comps(fX, rhoE * sg / (lam0 * e[0]))))
    # place 2 for vectors (as chain(), v1_6's form): the W_B components of the vectors at d = -1, 0 carry +- s |x_u| (the dual
    # run's box constants, passed to the midpoint run), none on an odd basis vector when the parity is exact on the ten states
    zero = lambda x: bool((x.v if isinstance(x, D) else x).mid() == 0 and (x.v if isinstance(x, D) else x).rad() == 0)
    oddst = [a for a in rng if a in odd_states]
    pzk = [(nm, a, b) for nm in ('g', 'T') for a in rng for b in rng if a <= b and ((a in oddst) != (b in oddst))] + \
        [(nm, a) for nm in ('e', 'f') for a in oddst]
    pure = all(C0[k][i] == 0.0 for k in range(K) for i in range(K) if (odd[i] == 1) != (pi[k] < 0))
    par_exact = par if par is not None else (pure and all(k in V and zero(V[k]) for k in pzk))
    alw = {'AX': a1}
    for d in (-1, 0):
        vs = []
        for j, v in enumerate(L[d]):
            a_ = allow[(d, j)] if allow is not None else (vac['s'] * abs(v[0]).upper()).upper()
            alw[(d, j)] = a_
            vs.append((v[0], [x if (par_exact and pi[k] < 0) else x + pm(a_) for k, x in enumerate(v[1])]))
        L[d] = tuple(vs)

    def step(v1):
        u1, k1 = v1
        return (u1, mv(R, k1)), (c * u1 + dot(BTM, k1), [BTM[k] * u1 + dot(AXm[k], k1) for k in range(K)])
    for d in range(1, 8):
        L[d] = step(L[d - 1][0])
    L['inf'] = ((ONE, [ZERO] * K), (c, list(BTM)))
    ch = {'R': R, 'pi': pi, 'B': B, 'beta': beta, 'AXm': AXm, 'c': c, 'lam0': lam0, 'L': L, 'g00': g00, 'C': C, 'K': K, 'mode': 'B'}
    ch['allow'], ch['par_exact'] = alw, par_exact
    z, wXw, wXwX = V[('z',)], V[('wXw',)], V[('wXwX',)]
    Rw2 = z * g00 / (rmain * e[0] * e[0]) - 1
    nwX2 = wXwX * g00 / (rmain * e[0] * e[0])
    sq = lambda v: v[0] * v[0] + sum((x * x for x in v[1]), ZERO)
    ch['res2'] = {(-1, '1'): (1 + Rw2) - sq(L[-1][0]), (-1, 'X'): nwX2 - sq(L[-1][1])}   # |Q_B w-hat|^2, |Q_B x(-1)|^2
    ch['norm2'] = {(-1, '1'): 1 + Rw2, (-1, 'X'): nwX2}
    ch['cross'] = {-1: wXw * g00 / (rmain * e[0] * e[0])}
    ch['Rw2'] = Rw2
    l1, lx = L[-1]
    lu, xu = l1[0], lx[0]
    n2X, n21, crs = ch['norm2'][(-1, 'X')], ch['norm2'][(-1, '1')], ch['cross'][-1]
    A2 = lu * lu * (n2X - xu * xu) - 2 * lu * xu * (crs - xu * lu) + xu * xu * (n21 - lu * lu)
    ch['Ap2'] = {-1: A2 - sum(((lu * lx[1][k] - xu * l1[1][k]) * (lu * lx[1][k] - xu * l1[1][k]) for k in range(K)), ZERO)}
    DY = [V[('DY', a)] for a in rng]
    DYY = V[('DYY',)]
    ct = DY[0] / g00
    Bt = [sum((C[k][i] * (DY[n] - ct * g[n][0]) for i, n in enumerate(idx)), ZERO) / sg for k in range(K)]
    p2n = (DYY - ct * ct * g00) / g00
    ch['pperp2'] = p2n - sum((v * v for v in Bt), ZERO)   # |Q_B p_X|^2 (place 5's terms in setup_B)
    ch['pnorm2'] = p2n
    ch['pW'] = Bt
    ch['R99F2'] = sum((R[i][j] * R[i][j] for i in range(K) for j in range(K)), ZERO)
    wT = [V[('wTw',)], V[('wTXw',)], V[('wTXXw',)]]
    f0 = [f[0], fX[0], V[('fXX', 0)]]
    T00 = [T[0][0], TX[0][0], TXX[0][0]]
    ch['Phi'] = tuple(rhoF3 * wT[j] * g00 / (e[0] * e[0] * lam0) - 2 * rhoE * f0[j] / (lam0 * e[0]) + T00[j] / (g00 * lam0)
                      for j in range(3))
    ch['M'] = (M0, M1, M2)
    ch['gam0'] = L[0][1][0] / L[0][0][0]
    return ch


def chain_dual_t_B(E, T, mains, rhoF3, odd_states, vac, C0, zero_bars=False, zero_tgrad=False):
    """chain_B on a piece box in the mean-value form with t as slot 0, as chain_dual_t (ch['dual'] for sf_pair's class-level form;
    the midpoint run takes the dual run's allowances and parity decision)."""
    keys, Vd, Vm, rad = entry_duals(E, T, zero_bars, zero_tgrad)
    chd = chain_B(Vd, mains, rhoF3, odd_states, vac, C0)
    chm = chain_B(Vm, mains, rhoF3, odd_states, vac, C0, allow=chd['allow'], par=chd['par_exact'])
    chc = _cen(chd, chm, rad)
    chc['dual'] = (chd, chm, rad)
    return chc


def _nonneg(x, what):
    """the gate: stop when a squared-norm form is certainly negative (the entries contradict each other)."""
    if x.upper() < 0:
        raise ValueError('a squared-norm form is certainly negative: %s (upper end %s)' % (what, x.upper()))
    return x


def setup_B(ch, P2r, U_hi, vac, DMAX=5, kzero=False):
    """the ingredients of the bounds on one piece for a chain_B (K = 9), in setup()'s dict form, so that the lemma, sf_pair, far_lo2,
    dk_setup, dk_class and rows_cert run unchanged on B:
    - U9 (the review 0a6cd86d sect. 1(b)-(c)): tau_B = ((U_hi/lambda_0^2)^up - 1 - |R_99|_F^2 low)/2, a stop if its upper end is not > 0;
      the leakage Gram of W_B out of B is PSD with trace <= tau_B, so Gl = tau_B I, eta+- = sqrt(tau_B), etak = sqrt(tau_B);
    - s_perp = sqrt(2 tau_B) (|Q_B S Q_B|_HS^2 <= 2 tau_B, sect. 1(b));
    - the K form (REVIEW_XKIND_KFACTOR 210303a9): |Q_B K| <= qt = (2 tau_B)^(1/4); for y in W_B, |Q_B A_X y| <= |gamma| |Q_B S y| +
      qt |(xi - gamma) K* y|, so xleak = |gx| sqrt(tau_B) + qt sqrt(lambda_max(M_2 - 2 gx M_1 + gx^2 M_0)) bounds |Q_B A_X P_W_B|,
      gx = tr M_1 / tr M_0 (any gamma is valid; lambda_max by min(trace, Frobenius) of the PSD form); |A_X| <= |B+| + |c|;
    - d = -1: rn1, rnX, Ap relative to B from the FF/E2 norms; d = 0: rn1[0] = q_B[0] = sqrt(tau_B) |P_W_B w-hat| + sqrt(2 tau_B)
      |Q_B w-hat|; rnX[0] = min over gamma in {0, gamma*} of (pc + |A_X| sp) + |gamma| (q_B[0] + sp) + qt sqrt(Phi(gamma)) (x(0) =
      A_X w-hat, w-hat = psi-hat_n + r, Q_B A_X r = gamma Q_B S r + Q_B K (xi - gamma) K* r, Q_B S r = Q_B w_0 - Q_B S delta);
      Ap[0] = min(|l_u| (pc + (|B+| + |c - g0|) sp + qt sqrt(Phi(g0))), the triangle form), g0 = x_u/l_u (A(0) = l_u (A_X - g0 S)
      w-hat: the Q_B w_0 terms cancel); pc = |Q_B p_X| from DY, DYY on B plus place 5's terms;
    - d >= 1: the B step's errors (cerr): '1' Rn dlp + sqrt(tau_B) rn1[d-1], X AXW dlp + xleak rn1[d-1], X's u component pWn dlp +
      pc rn1[d-1] (dlp = cerr[d-1][0], cerr[0] = 0); rn1[d] = sqrt(tau_B) (|P_W_B w_(d-1)| + dlp) + sqrt(2 tau_B) rn1[d-1]; rnX[d] =
      |l_u| pc + xleak (|P_W_B w_(d-1)| + dlp) + |A_X| rn1[d-1]; rnXo[d] = min(rnX[d], pc + |B-| e[d]); Ap[d] by the triangle form;
    - kzero (PLANT-KFORM only, never a bound): qt taken as 0, which must change rows.
    Every square root takes the upper end of a ball whose certainly negative values stop the piece (_nonneg)."""
    K, R, pi, L = ch['K'], ch['R'], ch['pi'], ch['L']
    ev = [k for k in range(K) if pi[k] > 0]
    od = [k for k in range(K) if pi[k] < 0]
    BN, Bm = P2r['Bp_hi'], P2r['Bm_hi']
    Rw, rho1 = P2r['Rw_hi'], P2r['rho1_hi']
    lam0 = ch['lam0']
    num = (U_hi / (lam0 * lam0)).upper() - 1 - ch['R99F2'].lower()
    tauB = (num / 2).upper()
    if not tauB > 0:
        raise ValueError('U9: the upper end of tau_B is not positive (S4-U and the 3-column entries contradict each other)')
    st = tauB.sqrt().upper()
    s2t = (2 * tauB).sqrt().upper()
    qt = ZERO if kzero else s2t.sqrt().upper()
    Gl = [[(tauB if i == j else ZERO) for j in range(K)] for i in range(K)]
    etap = etam = eta = st
    etak = [st] * K
    etar = [sqrt_up(tauB + sum((R[l][k] * R[l][k] for l in range(K) if l != k), ZERO)) for k in range(K)]
    sperp = s2t
    Rn = rnorm_up(R)
    r_ = Rn if Rn > sperp else sperp
    c = ch['c']
    cc = abs(c).upper()
    AXn = (BN + cc).upper()
    sp = vac['sp']
    pW = ch['pW']
    vacp = vac['eps_a'] + vac['Bp'] * sp
    pc = (sqrt_up(_nonneg(ch['pperp2'], '|Q_B p_X|^2')) + vacp + vac['s'] * norm_up(pW)).upper()
    pn = (sqrt_up(ch['pnorm2']) + vacp).upper()
    M0, M1, M2 = ch['M']
    tr0 = sum((M0[k][k] for k in range(K)), ZERO)
    tr1 = sum((M1[k][k] for k in range(K)), ZERO)
    gx = arb(float((tr1 / tr0).mid()))
    Mg = [[M2[i][j] - 2 * gx * M1[i][j] + gx * gx * M0[i][j] for j in range(K)] for i in range(K)]
    for k in range(K):
        _nonneg(Mg[k][k], 'the K form on basis vector %d' % k)
    # v1_8_1 (the K form's place 2): M is the form on W0_B; a y in W'_B = Q0 W0_B is Q0 y0 with y0 in W0_B, |y0| <= |y| / sqrt(1 -
    # s^2) <= (1 + s^2) |y|, and Q_B A_X y = Q_B A_X y0 - <u, y0> Q_B p_X (A_X u = c u + p_X, Q_B u = 0), so the u part costs s pc per unit
    # of |y0|; no xi^2 form on u is needed
    s_ = vac['s']
    xleak = ((abs(gx) * st + qt * sqrt_up(lmax_psd_up(Mg, list(range(K)))) + s_ * pc) * (1 + s_ * s_)).upper()

    def kvec(w, dl):
        """v1_8_2: |Q_B A_X y| for the true y = Q0 (w_c + e) in W'_B, w_c the computed components (balls, place 2's
        allowance included) and |e| <= dl, by the K form at gamma_w = (w^T M_1 w)/(w^T M_0 w) per vector (binary64; any gamma is valid):
        (|gamma_w| sqrt(tau_B) |w_c| + qt sqrt(w_c^T M(gamma_w) w_c) + (|gamma_w| sqrt(tau_B) + qt sqrt(lambda_max M(gamma_w))) dl +
        s pc (|w_c| + dl)) (1 + s^2); the high-mode bars of M then enter weighted by w's components on those modes."""
        q0_ = sum((w[i] * w[j] * M0[i][j] for i in range(K) for j in range(K)), ZERO)
        q1_ = sum((w[i] * w[j] * M1[i][j] for i in range(K) for j in range(K)), ZERO)
        gw = arb(float((q1_ / q0_).mid())) if q0_.lower() > 0 else gx
        Mw = [[M2[i][j] - 2 * gw * M1[i][j] + gw * gw * M0[i][j] for j in range(K)] for i in range(K)]
        qf = _nonneg(sum((w[i] * w[j] * Mw[i][j] for i in range(K) for j in range(K)), ZERO), 'the K form on a chain vector')
        nw = norm_up(w)
        k2 = (abs(gw) * st + qt * sqrt_up(lmax_psd_up(Mw, list(range(K))))).upper()
        return ((abs(gw) * st * nw + qt * sqrt_up(qf) + k2 * dl + s_ * pc * (nw + dl)) * (1 + s_ * s_)).upper()
    AXW = sqrt_up(sum((x * x for row in ch['AXm'] for x in row), ZERO))
    pWn = norm_up(ch['B']['TM'])

    def gform(v):
        q = ZERO
        for a in range(K):
            for b in range(K):
                q = q + v[a] * v[b] * Gl[a][b]
        return sqrt_up(q)
    Phi = ch['Phi']

    def phig(gm, what):
        return sqrt_up(_nonneg(Phi[2] - 2 * gm * Phi[1] + gm * gm * Phi[0], 'Phi(%s)' % what))
    zc = (ZERO, ZERO, ZERO)
    rn1 = {-1: sqrt_up(_nonneg(ch['res2'][(-1, '1')], '|Q_B w-hat|^2'))}
    rnX = {-1: sqrt_up(_nonneg(ch['res2'][(-1, 'X')], '|Q_B x(-1)|^2'))}
    rnXo = dict(rnX)
    capR = Rw.upper()
    e0 = sqrt_up(_nonneg(ch['Rw2'], 'R_w^2'))
    e = {0: e0 if e0 < capR else capR}
    cerr = {-1: zc, 0: zc, 'inf': zc}
    nW1 = norm_up(L[-1][0][1])
    q0 = (st * nW1 + s2t * rn1[-1]).upper()
    rn1[0] = q0
    gstar = arb(float((Phi[1] / Phi[0]).mid())) if Phi[0].lower() > 0 else ZERO
    cands = [((pc + AXn * sp) + abs(gm) * (q0 + sp) + qt * phig(gm, w_)).upper() for gm, w_ in ((ZERO, '0'), (gstar, 'gamma*'))]
    rnX[0] = cands[0] if cands[0] < cands[1] else cands[1]
    rnXo[0] = rnX[0]
    g0 = ch['gam0']
    Ap0k = (abs(L[0][0][0]) * (pc + (BN + abs(c - g0)) * sp + qt * phig(g0, 'g0'))).upper()
    Ap0t = (abs(L[0][0][0]) * rnX[0] + abs(L[0][1][0]) * rn1[0]).upper()
    nW0 = norm_up(L[0][0][1])
    e1 = (nW0 * nW0 + q0 * q0).sqrt().upper()
    cap1 = (Rw * rho1).upper()
    e[1] = e1 if e1 < cap1 else cap1
    cerr[1] = ((st * q0).upper(), (xleak * q0).upper(), (pc * q0).upper())
    for d in range(1, DMAX + 1):
        dlp = cerr[d - 1][0]
        if d >= 2:
            cerr[d] = ((Rn * dlp + st * rn1[d - 1]).upper(), (AXW * dlp + xleak * rn1[d - 1]).upper(), (pWn * dlp + pc * rn1[d - 1]).upper())
        nWd = (norm_up(L[d - 1][0][1]) + dlp).upper()
        rn1[d] = (st * nWd + s2t * rn1[d - 1]).upper()
        if d >= 2:
            ed = (nWd * nWd + rn1[d - 1] * rn1[d - 1]).sqrt().upper()
            cap = (Rw * ipow(rho1, d)).upper()
            e[d] = ed if ed < cap else cap
        kv = kvec(L[d - 1][0][1], dlp)   # v1_8_2: the per-vector K form, kept when it beats xleak nWd
        xw = (xleak * nWd).upper()
        rnX[d] = (abs(L[d - 1][0][0]) * pc + (kv if kv < xw else xw) + AXn * rn1[d - 1]).upper()
        ro = (abs(L[d - 1][0][0]) * pc + Bm * e[d]).upper()   # v1_8_1: |l_u| pc, as rnX
        rnXo[d] = rnX[d] if rnX[d] < ro else ro
    rn1['inf'], rnX['inf'], rnXo['inf'] = ZERO, pc, pc
    Ap = {-1: sqrt_up(_nonneg(ch['Ap2'][-1], '|Q_B A(-1)|^2')), 0: (Ap0k if Ap0k < Ap0t else Ap0t)}
    for d in range(1, DMAX + 1):
        Ap[d] = (abs(L[d][0][0]) * rnX[d] + abs(L[d][1][0]) * rn1[d]).upper()
    Ap['inf'] = pc
    return {'etap': etap, 'etam': etam, 'eta': eta, 'etak': etak, 'etar': etar, 'sperp': sperp, 'r': r_, 'Rn': Rn, 'pc': pc, 'pn': pn,
            'rn1': rn1, 'rnX': rnX, 'rnXo': rnXo, 'e': e, 'cerr': cerr, 'ev': ev, 'od': od, 'Ap': Ap, 'gform': gform, 'BN': BN,
            'Bm': Bm, 'Rw': Rw, 'rho1': rho1, 'cc': cc, 'tau': tauB, 'qt': qt, 'xleak': xleak, 'Ap0': (Ap0k, Ap0t), 'gx': gx,
            'gstar': gstar}


# ---- v1_9: route (b) (U9 from a trial-basis chain on g and T only; W3 with H and S4 and no TT)
def chain_RB(V, vac, C0, odd_states, nst, allow=None, par=None):
    """route (b)'s reduced B chain on one piece in balls (or duals): V holds g and T over the trial states renamed 0..nst; C0 the binary64
    basis over states 1..nst (first three rows W3's, padded; each row exactly parity-pure). Returns R (R_BB with place 2's 4 s^2),
    lam0, C, K = nst, pi, R99F2 = |R_BB|_F^2, par_exact and allow ({}: R carries no vector allowance; kept for _cen's protocol)."""
    rng = range(nst + 1)
    K = nst
    sym = lambda nm, a, b: V[(nm, min(a, b), max(a, b))]
    g = [[sym('g', a, b) for b in rng] for a in rng]
    T = [[sym('T', a, b) for b in rng] for a in rng]
    g00 = _pos(g[0][0], 'g00')   # v1_10 (C5), as chain()
    _nz(T[0][0], 'T00')
    lam0 = _nz(T[0][0] / g00 * (ONE + pm(vac['delta'])), 'lam0')   # place 1, as chain()
    s2 = vac['s'] * vac['s']

    def p2(M, a, b):
        return M[a][b] - g[a][0] / g00 * M[0][b] - g[b][0] / g00 * M[a][0] + g[a][0] * g[b][0] / (g00 * g00) * M[0][0]
    idx = list(range(1, K + 1))
    G2 = [[p2(g, a, b) for b in idx] for a in idx]
    T2 = [[p2(T, a, b) for b in idx] for a in idx]
    C0b = [[arb(x) for x in row] for row in C0]
    C = mmul(chol_inv(mmul(mmul(C0b, G2), mT(C0b))), C0b)   # rows: an orthonormal basis of W0_B, C0's row order kept
    R = [[x / lam0 + pm(4 * s2) for x in row] for row in mmul(mmul(C, T2), mT(C))]   # place 2, as chain()
    odd = [1 if (a in odd_states) else 0 for a in idx]
    pi = [(-1 if sum(C0[k][i] ** 2 for i in range(K) if odd[i]) > sum(C0[k][i] ** 2 for i in range(K) if not odd[i]) else 1)
          for k in range(K)]
    zero = lambda x: bool((x.v if isinstance(x, D) else x).mid() == 0 and (x.v if isinstance(x, D) else x).rad() == 0)
    oddst = [a for a in rng if a in odd_states]
    pzk = [(nm, a, b) for nm in ('g', 'T') for a in rng for b in rng if a <= b and ((a in oddst) != (b in oddst))]
    pure = all(C0[k][i] == 0.0 for k in range(K) for i in range(K) if (odd[i] == 1) != (pi[k] < 0))
    par_exact = par if par is not None else (pure and all(k in V and zero(V[k]) for k in pzk))
    ch = {'R': R, 'lam0': lam0, 'C': C, 'K': K, 'g00': g00, 'pi': pi, 'mode': 'RB', 'allow': {}, 'par_exact': par_exact}
    ch['R99F2'] = sum((R[i][j] * R[i][j] for i in range(K) for j in range(K)), ZERO)
    return ch


def chain_dual_t_RB(E, T, vac, C0, odd_states, nst, zero_bars=False, zero_tgrad=False):
    """chain_RB on a piece box in the mean-value form with t as slot 0 (E: {chain key: (LO, HI, err_b)}, g and T on the renamed trial
    states), as chain_dual_t: ch['dual'] = (duals, center, radii), ch['keys'] the dual slots' keys (slot i + 1 is keys[i])."""
    keys, Vd, Vm, rad = entry_duals(E, T, zero_bars, zero_tgrad)
    chd = chain_RB(Vd, vac, C0, odd_states, nst)
    chm = chain_RB(Vm, vac, C0, odd_states, nst, par=chd['par_exact'])
    chc = _cen(chd, chm, rad)
    chc['dual'] = (chd, chm, rad)
    chc['keys'] = keys
    return chc


def routeb_leak(chB, U_hi, K3=3, tau=None):
    """route (b)'s leakage inputs from a chain_RB on B (module docstring): {'tau': tau_B, 'Gl': R_B3^T R_B3 + tau_B I (K3 x K3), 'sblk':
    the block bound on |Q_3 S Q_3|, 'r_bb': R_BB's block norm, 'K3': K3}, or None when tau_B's upper end is not > 0. tau: a plant's
    override of tau_B, never a bound."""
    lam0 = chB['lam0']
    K = chB['K']
    tb = (((U_hi / (lam0 * lam0)).upper() - 1 - chB['R99F2'].lower()) / 2).upper() if tau is None else tau
    if not tb > 0:
        return None
    Rb = chB['R']
    Gl = [[sum((Rb[j][a] * Rb[j][b] for j in range(K3, K)), ZERO) + (tb if a == b else ZERO) for b in range(K3)] for a in range(K3)]
    rbb = rnorm_up([[Rb[a][b] for b in range(K3, K)] for a in range(K3, K)])
    s2t = (2 * tb).sqrt().upper()
    sblk = ((rbb + s2t) / 2 + (((rbb - s2t) / 2) * ((rbb - s2t) / 2) + tb).sqrt()).upper()
    return {'tau': tb, 'Gl': Gl, 'sblk': sblk, 'r_bb': rbb, 'K3': K3}


def route_b_keys(SL, w3=3):
    """the M3 record keys route (b)'s two chains read, for the trial set SL (trial states, 0 first, W3's 0..w3 included): the W3 chain
    (chain(..., tt=False)): g, T and TX for a <= b <= w3; e, eX, f, fX, h, hX and DY for a <= w3; DYY, z, wXw, wXwX; S4,Z, S4,x,1,TM and
    S4,xy,1,TM,2,TM; the B chain (chain_RB): g and T for a <= b in SL. Sorted record-key strings."""
    w = range(w3 + 1)
    ks = set('%s,%d,%d' % (nm, a, b) for nm in ('g', 'T', 'TX') for a in w for b in w if a <= b)
    ks |= set('%s,%d' % (nm, a) for nm in ('e', 'eX', 'f', 'fX', 'h', 'hX', 'DY') for a in w)
    ks |= set(('DYY', 'z', 'wXw', 'wXwX', 'S4,Z', 'S4,x,1,TM', 'S4,xy,1,TM,2,TM'))
    ks |= set('%s,%d,%d' % (nm, a, b) for nm in ('g', 'T') for a in SL for b in SL if a <= b)
    return sorted(ks)
