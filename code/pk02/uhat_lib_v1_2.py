#!/usr/bin/env python3
"""uhat_lib_v1_2.py -- pk02 (code/pk02/). The library of kt_uhat_asm_v1_2, the u-hat assembler (DESIGN_UHAT_ASM_v1_3 faa09e23 with
ADD1 03f73445, ADD2 60de6595, ADD3 5e8bce50, ADD4 22e8469f, ADD5 71aac1ed and ADD6 e6125835; after uhat_lib_v1_1 f5867205). v1_2: FA's
rest by operators (ADD5; fa_rest, fa_check for C-FA-OPS), the A4 path removed (A4 cancelled; the A4 spot keeps the 2J form), B' over
j = 0..3 only. No file I/O; the driver pins this file by its full sha256.
Every number is an arb ball (the driver sets ctx.prec); an upper end is taken by .upper() and a lower end by .lower(), so every bound is
outward. Columns are numbered from 0, as in the records (ADD1 sect. 5: the spec's f_j sits on record column j - 1).
v1_1 (ADD3): k = 3 rests by operator factors with the three-term T2 (sect. 6 below); the W2M row in the k table; k3_check (C-K3-DECOMP,
C-K3-OP with routes recomputed from the factors, C-K3-A4); C-K3-JLAW dropped (C-K3-MONO covers every 2J term).

1. Windows. A 'vac' column is a modelled outer V column (p = phi_0 in the model window), 'int' an exact V column, 'cp' an exact boundary
   state. Modelled ends: W2 columns 0 and 1; W3e, W3f, D4L0, D4ML0 columns 0 and 2; FA, FB column 2 (cp on column 0). BASIS9 is m3_cak's:
   index 0 = xi(T,M), 1 = xi(M,B), 2 = xi(T,B); S rows 1..9 = [TM, MB, TB, TM^2, MB^2, TB^2, TM MB, MB TB, TM TB].
2. The u-hat k by (family, key, role) (C-KTAB): W2 G,a,b -> 1 in the Gram role, 2 as v's centring companion ('vcomp'); other W2 keys 2;
   W3e, W3f, D4L0, D4ML0 3; FA, FB 2 after the one-cp-on-column-0 check. F_k = [1 - s^2, (1 - s^2)^-k] for k >= 2, F_0 = F_1 = 1.
3. Insertions: a column's polynomial from its st factors (S rows) and vertical xi factors; p and cp are not insertions. Junction bonds are
   horizontal xi factors between two adjacent columns; a non-row link is refused (C-R1), and so is a second bond at one junction
   (C-SAMEROW).
4. eps(f) in units of mu-hat ||psi-hat||: the linear part c_0 + c_1 xi_TM + c_2 xi_MB by M2B's identity
   |c_1 + c_2| eps_w + |c_1 - c_2| eps_d + |c_0 + (c_1 + c_2) kbar| eps_r; xi_TB and the degree-2 monomials by the xi-only keys of
   M2B_W_KV_v1 with the T <-> B images; Minkowski. Degree > 2 is refused (G-BAR's degree gate).
5. Route R (R1, R2, E-R): with m = A + |A - c| (m_hi over a centre ball), the end factor is (m + A)^(1/2) eps(f), the
   rest form m R[mirror] - R[mirror + pair] (C-R2-POS: a negative upper end is an error), plus |c| eps(f) R[mirror]^(1/2). The bond-free
   form is eps(f) R[mirror]^(1/2). R values are the engine's mirror ratios over their own empty mirror, times F_(2(k-1)) (or F_2 for an
   exact two-column mirror).
6. Bars per (entry, role), in units of W_0 mu_R^k. FA (ADD5): one modelled end of weight 1, the exact cp-ended rest by operators, Lemma
   T for 1,j and B,j and the signed F4 form for T,j and X,j, with g = g_jj/g_00 (fa_rest). W2: the two-term identity
   W - W~ = <Delta_e1, A F_e2> + <F~_e1, A Delta_e2> over
   its mirrors (cross term 1 with the model term, cross term 2 exact). k = 3 (ADD3 sect. 1): the three-term identity W - W~ =
   <Delta_1, R F_3> + <F_1, R Delta_3> - <Delta_1, R Delta_3>; each first-order rest ends in the true far V column and is bounded by
   operators: the end's junction bond by route R + E-R, (m + A + |c|); a bonded far link by (beta_2 of f_2^2)^(1/2) (F4) A lambda_0
   G_33^(1/2); a free far link by beta_2 lambda_0^(1/2) G_33^(1/2). The Delta-Delta term is beta_2 eps eps times 1, (m + A + |c|) or
   (m + A + |c|)(2 J_W + |c|) by the bond count. The sources (beta_2 by k and the pin 965f72f0; the A4 spot's 2J form) come from the
   driver and are checked by k3_check. The value at J_W = 300 bounds every piece by C-K3-MONO (rate conditions with n + 1).
   (mu-hat/mu_R)^j <= MU^j, MU = 1/(1 - eps_r).
7. The entry ball E = R~ (F_k + [-b_0, b_0]) + [-b_e, b_e] (sect. 2 of the spec) and the u-hat route-0 chain (U3 at the site, one
   normalization per quantity, one certified centre ball per piece, ADD1 sect. 2): G (k = 1; G_00 = 1 exactly), v = V - c_f G0a(vcomp)
   and KE = KE - c_e K1 (k = 2), M and E[h^2] (k = 3), q-hat_b = (b^T M b)^(1/2) + ||P_s|| ||h_perp||, ||P_s|| <= (A + |c_e|)/(1 - s^2).
8. Transfers: U4's T; route H and route P; the L0 Cov forms (16 and 12 terms) over the centre balls; B''s raw overlaps
   E_j[X_c] = E(X,j) - c_b E(T,j) - c_t E(B,j) + c_t c_b E(1,j) and T_v = beta-hat s'; beta-hat (D4, D4M) = (1 - s^2)^-2 (A + |c_t|)
   (A2/mhat_lo + c_b^2 N*_RTR)^(1/2) (ADD1 sect. 3); W's factor [(1 - s^2)^p, 1]."""
import re
from fractions import Fraction
from flint import arb

UNIT = arb(0, 1)
ZERO = arb(0)
BASIS9 = [(0,), (1,), (2,), (0, 0), (1, 1), (2, 2), (0, 1), (1, 2), (0, 2)]
PAIR_INDEX = {(0, 1): 0, (1, 2): 1, (0, 2): 2}
FAM_NCOL = {'W2': 2, 'W2M': 2, 'W3e': 3, 'W3f': 3, 'D4L0': 3, 'D4ML0': 3, 'FA': 3, 'FB': 3}
FAM_ENDS = {'W2': (0, 1), 'W3e': (0, 2), 'W3f': (0, 2), 'D4L0': (0, 2), 'D4ML0': (0, 2), 'FA': (2,), 'FB': (2,)}
FAM_INT = {'W3e': 1, 'W3f': 1, 'D4L0': 1, 'D4ML0': 1, 'FA': 1, 'FB': 1}
G_RE = re.compile(r'^G,(\d+),(\d+)$')
KEYMAP = {(2,): 'XITB', (0, 0): 'XITM2', (1, 1): 'XITM2', (2, 2): 'XITB2', (0, 1): 'XITM_XIMB', (1, 2): 'XITM_XITB',
          (0, 2): 'XITM_XITB'}


class UhatError(ValueError):
    """a refusal by one of the library's gates; the message names the gate."""


def farb(q):
    """an exact arb of a Fraction (or int)."""
    q = Fraction(q)
    return arb(q.numerator) / q.denominator


def up(x):
    return arb(x.upper())


def lo(x):
    return arb(x.lower())


def amax_up(*xs):
    """the largest upper end, as an exact arb point."""
    best = None
    for x in xs:
        u = arb(x.upper())
        if best is None or bool(u > best):
            best = u
    return best


def ipow(x, k):
    r = arb(1)
    for _ in range(k):
        r = r * x
    return r


# ------------------------------------------------------------------------------------------------ 2. the u-hat k and F_k
def uhat_k(fam, key, columns, factors, role='entry'):
    """C-KTAB: the u-hat k of an item by family, key pattern and role, after its graph checks."""
    if fam not in FAM_NCOL:
        raise UhatError('C-KTAB: unknown family %s' % fam)
    if len(columns) != FAM_NCOL[fam]:
        raise UhatError('C-KTAB: %s:%s has %d columns, the table says %d' % (fam, key, len(columns), FAM_NCOL[fam]))
    if fam == 'W2':
        if G_RE.match(key):
            if role == 'gram':
                return 1
            if role == 'vcomp':
                return 2
            raise UhatError('C-KTAB: W2 %s needs the role gram or vcomp, not %s' % (key, role))
        if role == 'gram':
            raise UhatError('C-KTAB: the non-G key W2 %s in the Gram role' % key)
        return 2
    if fam == 'W2M':                                 # ADD3 sect. 5: the only mirror row (m3_run_r0m_v1 475e5e94), two columns, k = 2
        if role != 'entry':
            raise UhatError('C-KTAB: the mirror window W2M %s takes the role entry only' % key)
        return 2
    if fam in ('FA', 'FB'):
        cps = [f for f in factors if f[0] == 'cp']
        if len(cps) != 1 or cps[0][2] != 0:
            raise UhatError('C-KTAB: %s:%s must carry exactly one cp factor, on column 0' % (fam, key))
        return 2
    if role not in ('entry',):
        raise UhatError('C-KTAB: %s:%s takes the role entry only' % (fam, key))
    return 3


def ktab_role_check(fam, key, columns, factors, role, k_used):
    """C-KTAB's role record (ADD1 sect. 1): the k a quantity was read with must be the table's k for its (family, key, role)."""
    k_tab = uhat_k(fam, key, columns, factors, role)
    if k_used != k_tab:
        raise UhatError('C-KTAB: %s:%s in the role %s was read with k = %s; the table says %d' % (fam, key, role, k_used, k_tab))
    return k_tab


def fk_ball(k, s2_hi):
    """F_k = <u-hat, T^k u-hat>/mu_R^k: exactly 1 for k <= 1, else in [1 - s^2, (1 - s^2)^-k] (s^2 <= s2_hi)."""
    if k <= 1:
        return arb(1)
    om = 1 - s2_hi
    return lo(om).union(up(1 / ipow(lo(om), k)))


# ------------------------------------------------------------------------------------------------ 3. insertions and junctions
def st_poly(S, a):
    P = {(): Fraction(S[0][a])} if S[0][a] != 0 else {}
    for i in range(1, 10):
        if S[i][a] != 0:
            P[BASIS9[i - 1]] = P.get(BASIS9[i - 1], Fraction(0)) + Fraction(S[i][a])
    return P


def pmul(P, Q):
    R = {}
    for m1, c1 in P.items():
        for m2, c2 in Q.items():
            m = tuple(sorted(m1 + m2))
            R[m] = R.get(m, Fraction(0)) + c1 * c2
    return {m: c for m, c in R.items() if c != 0}


def column_poly(factors, col, S):
    """the insertion polynomial on column col: its st factors times its vertical xi factors ({monomial: Fraction})."""
    P = {(): Fraction(1)}
    for f in factors:
        if f[0] == 'st' and f[2] == col:
            P = pmul(P, st_poly(S, f[1]))
        elif f[0] == 'xi':
            u, v = f[1]
            if u // 3 == col and v // 3 == col:
                if u == v:
                    raise UhatError('C-R1: a degenerate xi factor %s' % (f[1],))
                P = pmul(P, {(PAIR_INDEX[tuple(sorted((u % 3, v % 3)))],): Fraction(1)})
    return P


def junction_bonds(factors, ca, cb):
    """rows of the horizontal xi factors between adjacent columns ca and cb; C-R1 refuses a non-row link, C-SAMEROW a second bond."""
    rows = []
    for f in factors:
        if f[0] != 'xi':
            continue
        u, v = f[1]
        if {u // 3, v // 3} == {ca, cb} and ca != cb:
            if u % 3 != v % 3:
                raise UhatError('C-R1: the bond %s is not a row link' % (f[1],))
            rows.append(u % 3)
    if len(rows) > 1:
        raise UhatError('C-SAMEROW: %d bonds at the junction (%d, %d)' % (len(rows), ca, cb))
    return rows


def poly_degree(P):
    return max((len(m) for m in P), default=0)


# ------------------------------------------------------------------------------------------------ 4. eps(f)
def eps_insertion(P, EK):
    """eps(f) for the column polynomial P (units mu-hat ||psi-hat||), as an exact upper point. EK holds arb upper points eps_r, eps_w,
    eps_d, the xi-only keys (KEYMAP's names) and kbar as a ball."""
    if poly_degree(P) > 2:
        raise UhatError('G-BAR: an end weight of degree %d (> 2)' % poly_degree(P))
    c0, c1, c2 = (farb(P.get(m, 0)) for m in ((), (0,), (1,)))
    tot = abs(c1 + c2) * EK['eps_w'] + abs(c1 - c2) * EK['eps_d'] + up(abs(c0 + (c1 + c2) * EK['kbar'])) * EK['eps_r']
    for m, c in P.items():
        if m in ((), (0,), (1,)):
            continue
        tot = tot + abs(farb(c)) * EK[KEYMAP[m]]
    return up(tot)


# ------------------------------------------------------------------------------------------------ 5. route R and the signed form
def m_hi(c, A):
    """m = A + |A - c| over a centre ball c (its sup), an exact upper point."""
    return up(A + amax_up(abs(A - lo(c)), abs(A - up(c))))


def rest_P(m, Rm, Rxi, F):
    """C-R2-POS: the P_c rest m R[mirror] - R[mirror + pair], times F; its upper end, refused if negative."""
    v = (m * Rm - Rxi) * F
    if bool(up(v) < 0):
        raise UhatError('C-R2-POS: the rest form has a negative upper end %s' % up(v))
    return up(v)


def bond_free_term(eps_f, Rm, F, model_add):
    """eps(f) (R[mirror] F)^(1/2) + eps(f) model_add (the bond-free signed form with its model term)."""
    return up(eps_f * (up(Rm * F).sqrt() + model_add))


def bond_term(eps_f, m, A, c_abs, Rm, Rxi, F, model_add_P, model_add_K):
    """route R at a bond end: (m + A)^(1/2) eps(f) [(m R - R_xi)^(1/2) F^(1/2) + model_add_P] + |c| eps(f) [(R F)^(1/2) + model_add_K]."""
    er = up(m + A).sqrt()
    return up(er * eps_f * (rest_P(m, Rm, Rxi, F).sqrt() + model_add_P) + c_abs * eps_f * (up(Rm * F).sqrt() + model_add_K))


# ------------------------------------------------------------------------------------------------ 6. bars per entry and role
def end_data(fam, factors, S, EK, end):
    """(eps(f_end), polynomial, junction bond rows at the end's junction) for one modelled end."""
    P = column_poly(factors, end, S)
    if fam == 'W2':
        adj = 1 - end
    else:
        adj = FAM_INT[fam]
    rows = junction_bonds(factors, end, adj)
    return eps_insertion(P, EK), P, rows


def far_bonds(fam, factors, end):
    """bond rows at the junction beyond the int column (k = 3 shapes), seen from the modelled end end."""
    if fam not in ('W3e', 'W3f', 'D4L0', 'D4ML0'):
        return []
    other = 2 if end == 0 else 0
    return junction_bonds(factors, FAM_INT[fam], other)


def int_degree(fam, factors):
    """the number of vertical xi factors on the int column (column 1) of a k = 3 shape: D4L0's k in xi(4,5)^k, 0 elsewhere."""
    if fam not in FAM_INT:
        return 0
    c = FAM_INT[fam]
    return sum(1 for f in factors if f[0] == 'xi' and f[1][0] // 3 == c and f[1][1] // 3 == c)


def both_bonds(fam, factors):
    """True when a k = 3 item carries a bond at both junctions (04dc9e2d sect. 1; C-K3-COUNT)."""
    if fam not in ('W3e', 'W3f', 'D4L0', 'D4ML0'):
        return False
    return bool(junction_bonds(factors, 0, 1)) and bool(junction_bonds(factors, 1, 2))


K3_FAMS = ('W3e', 'W3f', 'D4L0', 'D4ML0')


def a4_spot(fam, factors, end):
    """ADD3 sect. 3: the first-order rest of the end at record column end has xi(4,5)^2 next to a bond (column 2 of degree 2 and a bonded
    far link): D4L0 E012 (end 2), E102 (end 0), E112 (both ends)."""
    return fam in K3_FAMS and int_degree(fam, factors) == 2 and bool(far_bonds(fam, factors, end))


def k3_src_ok(fam, key, factors, src, pinned):
    """C-K3-OP's source rule (ADD3 sect. 2): beta_2's source by column 2's degree k and the pin on 965f72f0."""
    k = int_degree(fam, factors)
    if k == 0:
        return src == 'beta(1)'
    return src == ({1: 'N*_TRB', 2: 'N*_A2'}[k] if pinned else 'sup(2J)^%d' % k)


def k3_sq_src_ok(fam, key, factors, end, src, pinned):
    """the bonded-far-link source rule and C-K3-A4 (ADD3 sect. 2-3; A4 cancelled): (beta_2 of f_2^2)^(1/2) by k and the
    pin; the A4 spot (k = 2) takes 2 J_W (N*_A2/(1 - eps_r))^(1/2) with the pin and nothing else (no xi^4 trace is accepted)."""
    k = int_degree(fam, factors)
    if k == 0:
        return src == 'beta(1)^1/2'
    if k == 1:
        return src == ('N*_A2^1/2' if pinned else 'sup(2J)^1')
    return pinned and src == '2J N*_A2^1/2'


def k3_route(fam, factors, end):
    """(junction bonded, far link bonded) for the end at record column end, recomputed from the factors."""
    return bool(junction_bonds(factors, end, FAM_INT[fam])), bool(far_bonds(fam, factors, end))


def k3_dd_route(fam, factors):
    """the Delta-Delta term's bond count over the two junctions: 0, 1 or 2."""
    return int(bool(junction_bonds(factors, 0, 1))) + int(bool(junction_bonds(factors, 1, 2)))


def k3_check(fam, key, factors, det, pinned):
    """C-K3-DECOMP, C-K3-OP and C-K3-A4 on one k = 3 detail (ADD3 sect. 4): every first-order rest ends in the true far V column, its
    labels equal the ones recomputed from the factors, and its sources follow the rules. Raises UhatError naming the gate."""
    for e_end, d in det['ends'].items():
        if d.get('rest_end') != 'true-V':
            raise UhatError('C-K3-DECOMP: %s:%s end %d has a rest ending in %s, not the true V column' % (fam, key, e_end, d.get('rest_end')))
        jb, fl = k3_route(fam, factors, e_end)
        if (d['jbond'], d['farlink']) != (jb, fl):
            raise UhatError('C-K3-OP: %s:%s end %d is labelled (junction %s, far link %s); the factors give (%s, %s)' % (
                fam, key, e_end, d['jbond'], d['farlink'], jb, fl))
        if not k3_src_ok(fam, key, factors, d['b2_src'], pinned):
            raise UhatError('C-K3-OP: %s:%s beta_2 source %s is not allowed (k %d, pin %s)' % (
                fam, key, d['b2_src'], int_degree(fam, factors), pinned))
        if fl and not k3_sq_src_ok(fam, key, factors, e_end, d['b2sq_src'], pinned):
            raise UhatError('C-K3-A4: %s:%s end %d: the source %s of (beta_2 of f_2^2)^(1/2) is not allowed' % (fam, key, e_end, d['b2sq_src']))
    if det['dd_bonds'] != k3_dd_route(fam, factors):
        raise UhatError('C-K3-OP: %s:%s Delta-Delta term labelled %d bonds; the factors give %d' % (
            fam, key, det['dd_bonds'], k3_dd_route(fam, factors)))
    return True


def fa_rest(A, form, Tf1, Tf1sq, g, lam0):
    """ADD5 sect. 1, FA's rest per unit eps_r over mu_R: 'FA-T' (1,j and B,j, Lemma T) ||T_{f_1}|| g^(1/2); 'FA-F4' (T,j and X,j, route R at
    the (3,6) bond, the signed F4 form) min over c in [0, A] of (2A + |A - c|) (lambda_0 ||T_{f_1^2}|| g)^(1/2) + |c| ||T_{f_1}|| g^(1/2),
    linear in c on [0, A], so at c = 0 (3A a) or c = A (2A a + A b). Returns (rest, c tag, a, b)."""
    b_ = up(Tf1 * up(g).sqrt())
    if form == 'FA-T':
        return b_, '-', None, b_
    if form != 'FA-F4':
        raise UhatError('C-FA-OPS: the form %s is not ADD5\'s (FA-T or FA-F4; E-R is never used on FA)' % form)
    a_ = up((lam0 * Tf1sq * g).sqrt())
    c0, cA = up(3 * A * a_), up(2 * A * a_ + A * b_)
    return (c0, 'c=0', a_, b_) if bool(c0 <= cA) else (cA, 'c=A', a_, b_)


def fa_check(fam, key, factors, det, pinned, Tf1, Tf1sq, g, lam0, A):
    """C-FA-OPS (ADD5 sect. 2): FA's bar names its form from its factors (a bond at (3,6): FA-F4; else FA-T), its T sources by xi(4,5)
    (the J-free traces only with the pin), its g source, and its rest is at least ADD5's value recomputed from the pinned inputs."""
    d = det['ends'][2]
    form = 'FA-F4' if junction_bonds(factors, 2, FAM_INT[fam]) else 'FA-T'
    if d.get('form') != form:
        raise UhatError('C-FA-OPS: %s:%s has the form %s; its factors give %s' % (fam, key, d.get('form'), form))
    xi45 = int_degree(fam, factors) == 1
    want = ('N*_TRB,N*_A2' if pinned else None) if xi45 else 'beta(1)'
    if want is None or d.get('T_src') != want:
        raise UhatError('C-FA-OPS: %s:%s T source %s; the rule gives %s' % (fam, key, d.get('T_src'), want or 'a refusal (no pin)'))
    if not d.get('g_src'):
        raise UhatError('C-FA-OPS: %s:%s names no g source' % (fam, key))
    rest_need, _, _, _ = fa_rest(A, form, Tf1, Tf1sq, g, lam0)
    if not bool(d['rest'] >= lo(rest_need)):
        raise UhatError('C-FA-OPS: %s:%s rest %s is below ADD5\'s value %s' % (fam, key, d['rest'].str(6), rest_need.str(6)))
    return True


MIRROR_NORM = {'W2': (2, 0)}
# (power of MU = number of modelled columns met by a cross term, index of F over the mirror's exact V columns); FA and k = 3 read no mirror


def entry_bars(fam, key, role, factors, S, EK, MIR, ctx_):
    """(b_e, detail) for one (entry, role) in units of W_0 mu_R^k. W2 and FA: route R / the signed form over the engine's mirror ratio
    balls MIR(fam, key, end, kind, truth) (kind 'K' or 'Kxi'; truth 'model' for W2's cross term 1, 'exact' otherwise). k = 3 (ADD3 sect.
    1): the three-term identity with true rests at both ends, each rest by operator factors from ctx_: beta2(fam, key) -> (beta_2,
    source); beta2sq(fam, key, end) -> ((beta_2 of f_2^2)^(1/2), source) for a bonded far link; farf(fam, key, end) -> G_33^(1/2) of the
    far end; hb = A lambda_0/mu_R (F4 for the raw far-link bond); om_half = lambda_0^(1/2)/mu_R^(1/2); then the Delta-Delta term. ctx_
    also holds columns, A, MU, s2, eps_r, J_W (= 300; C-K3-MONO), c_R (route R's centre ball) and c_far (|c| on a 2J bond). b_0 of a family
    is b_e of its empty key in the same role (the driver forms it)."""
    A, MU, s2 = ctx_['A'], ctx_['MU'], ctx_['s2']
    cR = ctx_['c_R']
    mR = m_hi(cR, A)
    cabs = up(abs(cR))
    k = uhat_k(fam, key, ctx_['columns'], factors, role)
    det = {'k': k, 'role': role, 'ends': {}}
    if k == 1:                                       # W2 G,a,b in the Gram role: the k = 1 model (cd7ddb86 (a))
        P = column_poly(factors, 0, S)
        if column_poly(factors, 1, S) != {(): Fraction(1)} or junction_bonds(factors, 0, 1):
            raise UhatError('G-BAR: a Gram key with an insertion off column 0 or a bond')
        e = eps_insertion(P, EK)
        det['ends'][0] = {'form': 'k1-model', 'eps': e, 'deg': poly_degree(P)}
        return up(e * MU), det
    if fam in ('FA', 'FB'):                          # ADD5 sect. 1: FA's exact cp-ended rest by operators, signed, never E-R
        if 'fa_ops' not in ctx_:
            raise UhatError('C-FA-OPS: an FA end of %s:%s without its operator inputs (ADD5 sect. 1)' % (fam, key))
        eps_e, P_e, rows = end_data(fam, factors, S, EK, 2)
        Tf1, Tf1sq, tsrc = ctx_['fa_ops']['T'](fam, key)
        g, gsrc = ctx_['fa_ops']['g'](fam, key)
        form = 'FA-F4' if rows else 'FA-T'
        rest, ctag, a_, b_ = fa_rest(A, form, Tf1, Tf1sq, g, ctx_['fa_ops']['lam0'])
        term = up(eps_e * rest)
        det['ends'][2] = {'form': form, 'eps': eps_e, 'deg': poly_degree(P_e), 'truth': 'exact', 'term': term, 'rows': rows, 'rest': rest,
                          'T_src': tsrc, 'g_src': gsrc, 'c': ctag}
        det['mu_pow'] = 1
        return up(term * MU), det
    if fam in K3_FAMS:                               # ADD3 sect. 1: true rests at both ends, by operator factors
        if 'beta2' not in ctx_:
            raise UhatError('C-K3-OP: a k = 3 end of %s:%s without the operator factors (ADD3 sect. 1)' % (fam, key))
        jfac = up(mR + A + cabs)                     # route R + E-R at a bonded junction: (2A + |A - c|) + |c|
        b2, b2src = ctx_['beta2'](fam, key)
        tot, eps_of = ZERO, {}
        for e_end in FAM_ENDS[fam]:
            eps_e, P_e, rows = end_data(fam, factors, S, EK, e_end)
            eps_of[e_end] = eps_e
            jb, fl = bool(rows), bool(far_bonds(fam, factors, e_end))
            farf = ctx_['farf'](fam, key, e_end)
            if fl:                                   # ||T_{f_2^2}||^(1/2) ||G_23|| W[f_3^2]^(1/2)
                b2sq, sqsrc = ctx_['beta2sq'](fam, key, e_end)
                rest = up(b2sq * ctx_['hb'] * farf)
            else:                                    # ||T_{f_2}|| lambda_0^(1/2) W[f_3^2]^(1/2)
                sqsrc = '-'
                rest = up(b2 * ctx_['om_half'] * farf)
            term = up(eps_e * (jfac if jb else arb(1)) * rest)
            det['ends'][e_end] = {'form': 'OPS-R' if jb else 'OPS-T', 'eps': eps_e, 'deg': poly_degree(P_e), 'truth': 'true', 'term': term,
                                  'rows': rows, 'jbond': jb, 'farlink': fl, 'rest_end': 'true-V', 'b2_src': b2src, 'b2sq_src': sqsrc,
                                  'route': 'far-bonded' if fl else 'far-free', 'beta2_src': b2src, 'a4_spot': a4_spot(fam, factors, e_end)}
            tot = tot + term
        nb = k3_dd_route(fam, factors)               # the Delta-Delta term: none, one bond (route R + E-R), two bonds (and 2J at J_W)
        rf = {0: arb(1), 1: jfac, 2: up(jfac * (2 * ctx_['J_W'] + ctx_['c_far']))}[nb]
        e0, e2 = FAM_ENDS[fam]
        dd = up(eps_of[e0] * eps_of[e2] * b2 * rf)
        det['dd_bonds'], det['dd'], det['mu_pow'] = nb, dd, 2
        return up((tot + dd) * ipow(MU, 2)), det
    mu_pow, fidx = MIRROR_NORM[fam]
    Fm = fk_ball(fidx, s2)
    ends = FAM_ENDS[fam]
    tot = ZERO
    for i, e_end in enumerate(ends):
        eps_e, P_e, rows = end_data(fam, factors, S, EK, e_end)
        far = None if len(ends) == 1 else ends[1 - i]
        truth = 'model' if (i == 0 and far is not None) else 'exact'
        if far is None or truth == 'exact':
            model_P = model_K = ZERO                 # FA / FB (exact cp rest) and W2's cross term 2 (the far end is F~ exactly)
        else:
            eps_far, _, _ = end_data(fam, factors, S, EK, far)
            model_K = eps_far                        # W2: ||K^(1/2) f g|| <= eps(f) mu-hat ||psi-hat||
            model_P = up(up(mR + A).sqrt() * model_K)
        Rm = MIR(fam, key, e_end, 'K', truth)
        if rows:
            Rxi = MIR(fam, key, e_end, 'Kxi', truth)
            term = bond_term(eps_e, mR, A, cabs, Rm, Rxi, Fm, model_P, model_K)
            form = 'R2'
        else:
            term = bond_free_term(eps_e, Rm, Fm, model_K)
            form = 'T'
        det['ends'][e_end] = {'form': form, 'eps': eps_e, 'deg': poly_degree(P_e), 'truth': truth, 'term': term, 'rows': rows}
        tot = tot + term
    det['mu_pow'], det['F_index'] = mu_pow, fidx
    return up(tot * ipow(MU, mu_pow)), det


# ------------------------------------------------------------------------------------------------ 7. entry ball and the u-hat chain
def entry_ball(Rt, Fk, b0, be):
    """E = R~ (F_k + [-b_0, b_0]) + [-b_e, b_e]."""
    return Rt * (Fk + UNIT * b0) + UNIT * be


def sq(x):
    """x^2 by endpoints (a ball straddling 0 keeps its lower end 0)."""
    a, b = lo(x), up(x)
    if bool(a >= 0):
        return lo(a * a).union(up(b * b))
    if bool(b <= 0):
        return lo(b * b).union(up(a * a))
    return ZERO.union(up(amax_up(a * a, b * b)))


def chol(G, n):
    L = [[ZERO] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1):
            s = G[i][j]
            for kk in range(j):
                s = s - L[i][kk] * L[j][kk]
            if i == j:
                if not bool(s > 0):
                    return None
                L[i][i] = s.sqrt()
            else:
                L[i][j] = s / L[j][j]
    return L


class CDual:
    """value v and its derivative d in one centre variable, both arb balls: the mean-value form over a centre ball (ADD1 sect. 2: the
    entries are c-polynomials over the ball; the centred form keeps the cancellation at the mean that a plain ball product loses)."""
    __slots__ = ('v', 'd')

    def __init__(self, v, d):
        self.v, self.d = v, d

    @staticmethod
    def lift(o):
        return o if isinstance(o, CDual) else CDual(o, ZERO)

    def __add__(self, o):
        o = CDual.lift(o)
        return CDual(self.v + o.v, self.d + o.d)

    __radd__ = __add__

    def __sub__(self, o):
        o = CDual.lift(o)
        return CDual(self.v - o.v, self.d - o.d)

    def __rsub__(self, o):
        o = CDual.lift(o)
        return CDual(o.v - self.v, o.d - self.d)

    def __mul__(self, o):
        o = CDual.lift(o)
        return CDual(self.v * o.v, self.v * o.d + self.d * o.v)

    __rmul__ = __mul__

    def __neg__(self):
        return CDual(-self.v, -self.d)


def csq(x):
    """x^2 for an arb (by endpoints) or a CDual (value by endpoints, derivative 2 v d)."""
    if isinstance(x, CDual):
        return CDual(sq(x.v), 2 * x.v * x.d)
    return sq(x)


def c_centred2(fn, ce, cf):
    """the values of fn(ce, cf) (a tuple of polynomials in the two centres) over the centre balls by the two-variable mean-value form
    fn(ce_m, cf_m) + d_e fn(box) (ce - ce_m) + d_f fn(box) (cf - cf_m), ce_m and cf_m the exact midpoints."""
    cem, cfm = arb(ce.mid()), arb(cf.mid())
    v0 = fn(cem, cfm)
    de = fn(CDual(ce, arb(1)), cf)
    df = fn(ce, CDual(cf, arb(1)))
    res = []
    for a, b, c in zip(v0, de, df):
        db = b.d if isinstance(b, CDual) else ZERO
        dc = c.d if isinstance(c, CDual) else ZERO
        res.append(a + db * (ce - cem) + dc * (cf - cfm))
    return tuple(res)


def chain_uhat(E, c_e, c_f, sqf=sq, cholf=chol, span=(0, 1, 2, 3)):
    """route 0 (D3, site form) on u-hat quantities E(g, key, role), arb balls or the driver's Duals (pass Dual-aware sqf and cholf),
    with the piece's centre balls c_e, c_f (U3's G-C; ADD1 sect. 2). v and KE are linear in c; M and E[h^2] are quadratic and take the
    mean-value form Q(c_m) + Q'(c) (c - c_m). Returns G, v, KE, M, E[h^2], v^T G^-1 v, b^T M b and ||h_perp||^2; q_hat forms q."""
    n = len(span)
    cem, cfm = arb(c_e.mid()), arb(c_f.mid())
    dce, dcf = c_e - cem, c_f - cfm
    G = [[E('W2', 'G,%d,%d' % (min(a, b), max(a, b)), 'gram') for b in span] for a in span]
    v = [E('W2', 'V,%d' % a, 'entry') - c_f * E('W2', 'G,0,%d' % a, 'vcomp') for a in span]
    K1 = [E('W2', 'K1,%d' % a, 'entry') for a in span]
    KE0 = [E('W2', 'KE,%d' % a, 'entry') for a in span]
    KE = [KE0[i] - c_e * K1[i] for i in range(n)]
    KEm = [KE0[i] - cem * K1[i] for i in range(n)]
    M = [[None] * n for _ in range(n)]
    for i, a in enumerate(span):
        for j, b in enumerate(span):
            k_ = 'M,%d,%d,' % (min(a, b), max(a, b))
            ee, e12, z0 = (E('W3e', k_ + 'ee', 'entry'), E('W3e', k_ + 'e1', 'entry') + E('W3e', k_ + 'e2', 'entry'),
                           E('W3e', k_ + '00', 'entry'))
            Mm = ee - cem * e12 + cem * cem * z0 - KEm[i] * KEm[j]
            dM = (2 * c_e) * z0 - e12 + K1[i] * KE[j] + KE[i] * K1[j]
            M[i][j] = Mm + dM * dce
    FF, F12, Z3 = E('W3f', 'FF', 'entry'), E('W3f', 'F1', 'entry') + E('W3f', 'F2', 'entry'), E('W3f', 'Z', 'entry')
    Eh2 = (FF - cfm * F12 + cfm * cfm * Z3) + ((2 * c_f) * Z3 - F12) * dcf
    res = dict(G=G, v=v, KE=KE, M=M, Eh2=Eh2, pd=True, why='')
    L = cholf(G, n)
    if L is None:
        res.update(pd=False, why='a Cholesky pivot of G not positive')
        return res
    y = [None] * n
    for i in range(n):
        s = v[i]
        for kk in range(i):
            s = s - L[i][kk] * y[kk]
        y[i] = s / L[i][i]
    vGv = sqf(y[0])
    for yi in y[1:]:
        vGv = vGv + sqf(yi)
    beta = [None] * n
    for i in reversed(range(n)):
        s = y[i]
        for kk in range(i + 1, n):
            s = s - L[kk][i] * beta[kk]
        beta[i] = s / L[i][i]
    bMb = None
    for i in range(n):
        for j in range(n):
            t_ = beta[i] * M[i][j] * beta[j]
            bMb = t_ if bMb is None else bMb + t_
    res.update(vGv=vGv, bMb=bMb, hp2=Eh2 - vGv)
    return res


def q_hat(bMb, hp2, c_e, A, s2):
    """q-hat_b = (b^T M b)^(1/2) + ||P_s|| ||h_perp|| with ||P_s|| <= (A + |c_e|)/(1 - s^2) (ADD2 sect. 4), from the piece's balls;
    a negative upper end of either square stops (never clipped)."""
    Pn = up((A + up(abs(c_e))) / lo(1 - s2))
    if bool(up(hp2) < 0) or bool(up(bMb) < 0):
        return {'stop': 'the upper end of %s below 0' % ('||h_perp||^2' if bool(up(hp2) < 0) else 'b^T M b'), 'Ps': Pn}
    return {'q_hat_hi': up(up(bMb).sqrt() + Pn * up(hp2).sqrt()), 'Ps': Pn}


# ------------------------------------------------------------------------------------------------ 8. transfers
def u4_T(sp, beta, m_abs, xu, xsu):
    """U4: s' (beta + |m| + ||X u-hat|| + ||X* u-hat||) + s'^2 (beta + ||X u-hat|| + ||X* u-hat||) + beta s'^3."""
    return up(sp * (beta + m_abs + xu + xsu) + sp * sp * (beta + xu + xsu) + beta * sp * sp * sp)


def xu_bound(q_hi, m_abs, s2):
    """||X-hat u-hat|| <= (lambda_0/mu-hat)^(1/2) (q-hat_s^2 + m-hat_s^2)^(1/2) <= (1 - s^2)^(-1/2) (...)^(1/2)."""
    return up((q_hi * q_hi + m_abs * m_abs).sqrt() / lo(1 - s2).sqrt())


def route_H(q_hi, m_abs, eps_r, T, s2):
    return up(q_hi / lo(1 - s2).sqrt() + eps_r * m_abs / lo(1 - eps_r) + T)


def route_P(q_hi, Ts):
    return up(q_hi + Ts)


def beta_D3(A, c_t, c_bb, s2, p):
    """(1 - s^2)^-p (A + |c_t|)(A + |c_bb|): p = 3 at the Z position (U2), 2 at the site (route P)."""
    return up((A + up(abs(c_t))) * (A + up(abs(c_bb))) / ipow(lo(1 - s2), p))


def beta_D4(A, c_t, c_b, A2, mhat_lo, rtr, s2, eps_r):
    """(1 - s^2)^-2 (A + |c_t|) ((A2/mhat_lo + c_b^2 N*_RTR)/(1 - eps_r))^(1/2) (U2, Lemma D4 with c_b >= 0:
    Lemma D4 carries lambda_h/lambda_0 <= 1/((1 - eps_r) mhat); the A0 part is at most c_b^2 N*_RTR by RTR's CLAIM, the A2 part
    A2/mhat(t) <= A2/mhat_lo)."""
    if not bool(lo(c_b) >= 0):
        raise UhatError('beta-hat (D4): c_b must be >= 0 (Lemma D4)')
    if not bool(lo(mhat_lo) >= 1):
        raise UhatError('beta-hat (D4): mhat_lo must be >= 1 (mhat increases from 1)')
    return up((A + up(abs(c_t))) * up((A2 / lo(mhat_lo) + sq(c_b) * rtr) / lo(1 - eps_r)).sqrt() / ipow(lo(1 - s2), 2))


def mhat_lo(m1, m2, m3, J_hi):
    """mhat(1/J_hi) = 1 + m1 t + m2 t^2 + m3 t^3 at t = 1/J_hi exactly, a lower end of mhat on a piece [J_lo, J_hi] since m1..m3 > 0
    (pk08 18:28Z); 1 exactly on the last piece (J_hi = inf). m1..m3 are exact arb values of the binary64 literals."""
    if J_hi == 'inf':
        return arb(1)
    for m in (m1, m2, m3):
        if not bool(lo(m) > 0):
            raise UhatError('mhat_lo: a coefficient is not > 0')
    t = 1 / farb(Fraction(J_hi))
    return lo(1 + m1 * t + m2 * t * t + m3 * t * t * t)


def l0_d4ml0(Ev, ce, cf, sqf=sq):
    """D4ML0's Cov form with fixed centres (ce, cf): returns (||X_s psi_u||^2 sum, m-hat_s = E[S1100] - ce cf, L0 = sum - m^2)."""
    cs = [ce, cf, ce, cf]
    s = None
    for code in range(16):
        bits = [(code >> (3 - i)) & 1 for i in range(4)]
        t_ = Ev['S' + ''.join(str(x) for x in bits)]
        for i, x in enumerate(bits):
            if not x:
                t_ = t_ * (-cs[i])
        s = t_ if s is None else s + t_
    m = Ev['S1100'] - ce * cf
    return s, m, s - sqf(m)


def l0_d4l0(Ev, ce, cf, sqf=sq):
    """D4L0's Cov form with fixed centres: the 12-term sum, m-hat_s = E[E101] - ce cf, L0 = sum - m^2."""
    s = None
    for a in (0, 1):
        for b in (0, 1):
            for k in (0, 1, 2):
                t_ = (2 if k == 1 else 1) * Ev['E%d%d%d' % (a, b, k)] * (ce * ce if a + b == 0 else -ce if a + b == 1 else 1) * \
                    (cf * cf if k == 0 else -cf if k == 1 else 1)
                s = t_ if s is None else s + t_
    m = Ev['E101'] - ce * cf
    return s, m, s - sqf(m)


BPRIME_J = 4                                         # v_hat_raw.0..3: what R6.5 reads (S8's W3 chain has K = 3; INTERFACE_UHAT_R65 sect. 3)


def bprime_raw(Ev, c_t, c_b):
    """B''s raw overlaps E_j[X_c] = E(X,j) - c_b E(T,j) - c_t E(B,j) + c_t c_b E(1,j), j = 0..3 (u-hat units; basis raw)."""
    return [Ev['X,%d' % j] - c_b * Ev['T,%d' % j] - c_t * Ev['B,%d' % j] + c_t * c_b * Ev['1,%d' % j] for j in range(BPRIME_J)]


def w_factor(s2, p):
    """The factor (mu_R/lambda_0)^p in [(1 - s^2)^p, 1], the lower end rounded down."""
    return lo(ipow(lo(1 - s2), p)), arb(1)
