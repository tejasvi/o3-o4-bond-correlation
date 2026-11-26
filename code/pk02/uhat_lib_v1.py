#!/usr/bin/env python3
"""uhat_lib_v1.py -- pk02 (code/pk02/). The library of kt_uhat_asm_v1, the u-hat assembler (DESIGN_UHAT_ASM_v1_3 faa09e23 with
ADD1 03f73445 and ADD2 60de6595). No file I/O; the driver pins this file by its full sha256. Every number is an arb ball (the driver sets
ctx.prec); an upper end is taken by .upper() and a lower end by .lower(), so every bound is outward. Columns are numbered from 0, as in
the records (ADD1 sect. 5: the spec's f_j sits on record column j - 1).

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
6. Bars per (entry, role), in units of W_0 mu_R^k, by the two-term identity W - W~ = <Delta_e1, A F_e2> + <F~_e1, A Delta_e2> (ADD1
   sect. 4, decomposition (B)): cross term 1 reads the true far end (model mirror + model term), cross term 2 the model far end (exact).
   End order: the true far end goes to the end whose far junction carries no bond, when one exists. The model term of a k = 3 rest is
   second order, beta_2 eps(f_end) eps(f_far) times its bond route's factor (ADD2 sect. 2): none (at most the end's junction bond, whose
   route R form gives (m + A + |c|)), 2.3 (one bond at the interior link: R2 + E-R there, (m + A + |c|), J-uniform), 2.4 (both: the
   junction by route R and the interior bond by 0 <= xi <= 2J, (m + A + |c|)(2 J_W + |c|)). beta_2 and its source name come from the
   driver (ADD2 sect. 1); D4L0 E112 (route 2.4 with xi(4,5)^2) is refused unless its beta_2 is N*_A2/(1 - eps_r) and the rule on
   04dc9e2d sect. 2.2 is pinned (C-K3-OP). The value at J_W = 300 bounds every piece by C-K3-MONO (rate conditions with n + 1) and
   C-K3-JLAW (every near term of each law carries sig^k, k >= 1). (mu-hat/mu_R)^j <= MU^j, MU = 1/(1 - eps_r).
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
FAM_NCOL = {'W2': 2, 'W3e': 3, 'W3f': 3, 'D4L0': 3, 'D4ML0': 3, 'FA': 3, 'FB': 3}
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


def k3_src_ok(fam, key, factors, src):
    """C-K3-OP's source rule (ADD2 sect. 1): beta_2's source must match column 2's insertion degree."""
    k = int_degree(fam, factors)
    allowed = {0: ('beta(1)',), 1: ('N*_TRB', 'sup(2J)^1'), 2: ('N*_A2', 'sup(2J)^2')}[k]
    return src in allowed


LAW_NEAR_POWERS = {'LAW v1': {'NP': 2, 'R1': 1, 'D5': 5, 'R0': 5}, 'LAW-W v1': {'NPW': 2, 'R1W': 1, 'D5W': 5, 'R0W': 5}}
# near terms and their sig powers: SPEC_M2B_CERT_v1 l.70 (LAW v1); NOTE_M2B_WEIGHTED_LAWS_v1 sect. 4 l.60 (the weighted laws)


def jlaw_ok(powers):
    """C-K3-JLAW: every near term of the law carries sig^k with k >= 1, so J^(1/2) eps(J) and J eps(J) do not grow through it."""
    return bool(powers) and all(int(p) >= 1 for p in powers.values())


MIRROR_NORM = {'W2': (2, 0), 'W3e': (2, 2), 'W3f': (2, 2), 'D4L0': (2, 2), 'D4ML0': (2, 2), 'FA': (1, 2), 'FB': (1, 2)}
# (power of MU = number of modelled columns met by a cross term, index of F over the mirror's exact V columns)


def entry_bars(fam, key, role, factors, S, EK, MIR, ctx_):
    """(b_e, detail) for one (entry, role) in units of W_0 mu_R^k. MIR(fam, key, end, kind, truth) returns the engine's mirror ratio ball
    over its own empty mirror (kind 'K' or 'Kxi'; truth 'model' for cross term 1's true far end, 'exact' otherwise). ctx_ holds
    columns, A, MU, s2, eps_r, J_W (= 300; C-K3-MONO), c_R (route R's centre ball), c_far (an upper bound on |c| for a far-junction bond) and
    beta_int(fam, key) ((I6) / (I6')). b_0 of a family is b_e of its empty key in the same role (the driver forms it)."""
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
    mu_pow, fidx = MIRROR_NORM[fam]
    Fm = fk_ball(fidx, s2)
    ends = FAM_ENDS[fam]
    if len(ends) == 2 and fam != 'W2' and len(far_bonds(fam, factors, ends[0])) > len(far_bonds(fam, factors, ends[1])):
        ends = (ends[1], ends[0])                    # the model term goes on the end whose far junction carries no bond
    det['order'] = ends
    tot = ZERO
    for i, e_end in enumerate(ends):
        eps_e, P_e, rows = end_data(fam, factors, S, EK, e_end)
        far = None if len(ends) == 1 else ends[1 - i]
        truth = 'model' if (i == 0 and far is not None) else 'exact'
        route, src = '-', '-'
        if far is None or truth == 'exact':
            model_P = model_K = ZERO                 # FA / FB (exact cp rest) and cross term 2 (the far end is F~ exactly)
        else:
            eps_far, _, _ = end_data(fam, factors, S, EK, far)
            if fam == 'W2':
                model_K = eps_far                    # ||K^(1/2) f g|| <= eps(f) mu-hat ||psi-hat||
            else:                                    # k = 3: second order through column 2 (ADD1 sect. 4, ADD2 sect. 1-3)
                if 'beta2' not in ctx_:
                    raise UhatError('C-K3-OP: a k = 3 end of %s:%s without the column-2 bound beta_2 (ADD2 sect. 1)' % (fam, key))
                frows = far_bonds(fam, factors, e_end)
                route = 'none' if not frows else ('2.4' if rows else '2.3')
                b2, src = ctx_['beta2'](fam, key)
                if route == '2.4' and int_degree(fam, factors) == 2 and not (src == 'N*_A2' and ctx_.get('ruling_22')):
                    raise UhatError('C-K3-OP: %s:%s (route 2.4 with a degree-2 column-2 insertion) needs beta_2 = N*_A2/(1 - eps_r) and '
                                    'the pinned rule on 04dc9e2d sect. 2.2; it has %s%s' % (
                                        fam, key, src, '' if ctx_.get('ruling_22') else ' and no pinned rule'))
                if route == '2.3':
                    bf = up(mR + A + cabs)           # R2 + E-R at the interior link (04dc9e2d sect. 2.3), J-uniform
                elif route == '2.4':
                    bf = up(2 * ctx_['J_W'] + ctx_['c_far'])      # 0 <= xi <= 2J at the interior link, at J_W (C-K3-MONO, C-K3-JLAW)
                else:
                    bf = arb(1)
                model_K = up(bf * b2 * eps_far)
            model_P = up(up(mR + A).sqrt() * model_K)
        Rm = MIR(fam, key, e_end, 'K', truth)
        if rows:
            Rxi = MIR(fam, key, e_end, 'Kxi', truth)
            term = bond_term(eps_e, mR, A, cabs, Rm, Rxi, Fm, model_P, model_K)
            form = 'R2'
        else:
            term = bond_free_term(eps_e, Rm, Fm, model_K)
            form = 'T'
        det['ends'][e_end] = {'form': form, 'eps': eps_e, 'deg': poly_degree(P_e), 'truth': truth, 'term': term, 'rows': rows,
                              'route': route, 'beta2_src': src}
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


def beta_D4(A, c_t, c_b, A2, mhat_lo, rtr, s2):
    """(1 - s^2)^-2 (A + |c_t|) (A2/mhat_lo + c_b^2 N*_RTR)^(1/2) (U2, Lemma D4 with c_b >= 0; ADD1 sect. 3: the A0 part of
    (A2 + c_b^2 A0) lambda_h/mu-hat is at most c_b^2 N*_RTR by RTR's CLAIM, the A2 part is A2/mhat(t) <= A2/mhat_lo)."""
    if not bool(lo(c_b) >= 0):
        raise UhatError('beta-hat (D4): c_b must be >= 0 (Lemma D4)')
    if not bool(lo(mhat_lo) >= 1):
        raise UhatError('beta-hat (D4): mhat_lo must be >= 1 (mhat increases from 1)')
    return up((A + up(abs(c_t))) * up(A2 / lo(mhat_lo) + sq(c_b) * rtr).sqrt() / ipow(lo(1 - s2), 2))


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


def bprime_raw(Ev, c_t, c_b):
    """B''s raw overlaps E_j[X_c] = E(X,j) - c_b E(T,j) - c_t E(B,j) + c_t c_b E(1,j), j = 0..9 (u-hat units; basis raw)."""
    return [Ev['X,%d' % j] - c_b * Ev['T,%d' % j] - c_t * Ev['B,%d' % j] + c_t * c_b * Ev['1,%d' % j] for j in range(10)]


def w_factor(s2, p):
    """The factor (mu_R/lambda_0)^p in [(1 - s^2)^p, 1], the lower end rounded down."""
    return lo(ipow(lo(1 - s2), p)), arb(1)
