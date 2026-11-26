#!/usr/bin/env python3
"""m3_bar_v8.py -- pk03 (code/pk03/). Lemma 19.1c bars on the M-a layer. REVISION of m3_bar_v7.py (4101de17)
after batch 1 (entry I_N of N = 4 needs more than one 540-s piece by itself): Prep.bound is resumable between units, so a piece can stop
inside an entry and the next piece resume it.
- Units: stage a 'ak' (the a_k table), 'm0u', 'm0c' (nF0, nF0c); then every group norm 'g|gi|what|i|p|which' in v7's order: stage b
  (covariance 'u'), stage c ('c': the nFc terms, nF4c's p = 4G and EF4's bar norms), stage d ('p': nF0p).
- Before each unit not yet in the entry's state, the job script's budget (Prep.ubudget; None = no limit) is asked; a 'no' raises
  Checkpoint(state), the state holding the entry name, a sha256 digest of its factor groups, the values computed so far (exact mp.iv
  intervals) and C-BUDGET's maxrel. bound(..., entry, state) resumes from such a state (name and digest must match): restored units are
  not recomputed, and restored group norms enter the group cache. The budget is also asked before the per-entry series and majorants.
- The arithmetic, its order and the tables are v7's; a unit computed in a fresh process builds the same tables, so a straight and a
  resumed entry give the same intervals when the cut falls at a stage boundary (the job script's C-RESUME).
- CPU lines: TABLE-CPU per moment table, UNIT per unit, GDATA-CPU per entry (group series, majorants, F_i).
m3_bar_v7: Lemma 19.1c bars on the M-a layer (PLAN_M3_CODE_v1, v1_1, v1_2): riglap5s's Prep5s
REVISION of m3_bar_v6.py (f43e8c83): 'ex' is kept, so the E2^3 part is [0, min(ex, tr)] as in riglap5s. m3_probe_u_v2_1 (9606d4a8) put
stage u at 200.7 s with the cut and stage c at 171.3 s on the closed layer, while the cut cost 1.3% of N's rE (5.521e-7 against the
float 5.450e-7). Restoring ex adds the D-18 table and one self-product, about 110 s, so stage u stays near 310 s, inside one piece.
Prep-stage norms keep fallback=False (the M-a ball), C-BUDGET measures norms after the root, and the NORM lines stay.
m3_bar_v6: Lemma 19.1c bars on the M-a layer (PLAN_M3_CODE_v1, v1_1, v1_2): riglap5s's Prep5s
REVISION of m3_bar_v5.py (16de56e1), for PLAN_M3_CODE_v1_2_ADD5 sect. 7 (the N prep on the layer):
- stage u drops 'ex' from the E2^3 part: the part becomes [0, tr], which contains [0, min(ex, tr)], so the bound stays valid; it builds
  its D-16 vertex table first, which then serves every stage-u norm (no norm there needs more once 'ex' is gone);
- prep-stage norms (norm_any in stages u and c) take E2 with fallback=False: the layer's M-a ball is a valid enclosure (API sect. 1),
  and an arb recompute of a table that size is impractical; entry-level norms keep the MAFallback recompute through TableFB;
- C-BUDGET's maxrel measures every norm after its root (the quantity that enters the bars), not the moment under it;
- every prep-stage norm logs its CPU (NORM lines) for the piece plan.
Every other inequality term as v5.
REVISION of m3_bar_v4.py (0c46482f), for PLAN_M3_CODE_v1_2_ADD5 sect. 2-3: the a_k no longer enter C-BUDGET's maxrel (an a_k may be near
zero by cancellation; its only route into err is rnd); info gains ak_relrad (their largest relative radius, INFO) and, for m3_diag_v1,
every rem sub-term (nF, nFc, nFle3, nFle3c, nF4c, EF4, m0u, m0c, rho4 in its C8 and C6 forms). Every inequality term as v4.
REVISION of m3_bar_v3.py (9ddc5b93) for the frozen layer API (pk02's SPEC_MA_LAYER_v1_3_API.md, 541ccda8):
- every moment table is built with the forms W = W_int as an exact integer arb_mat, which the API requires with W_int;
- tables are TableFB objects: the layer's MAFallback, and only it, is caught at E2, lp_moment and pos_moment (API sect. 1: the one
  exception a caller may catch, meaning recompute in arb); the value is then recomputed from the same arguments by ARB['kern'] (set by
  the job script: arbeng_ma_stub_v1_1, every value in arb through arbeng_c2b_v2), and each recompute is logged in FALLBACKS.
  Every other exception stops the run. Every inequality term as v3.
REVISION of m3_bar_v2.py (f3056cd6): imports the generic module names (m3_scal, m3_graph, m3_series, m3_major), which the job scripts load from sha-pinned files;
kernel polynomials take arb coefficients only (m3_scal.spoly/ka) and mp.iv views come through m3_scal.arb_to_iv, since arbeng_ma_stub_v1's mpi_to_arb drops the sign of negative ends (m3_smoke_v2 d4).
REVISION of m3_bar_v1.py (096fca32): Prep in stages (always / u / c) with hand-off restore and largest-degree-first norms;
every inequality term as v1.
(Prep5 + 5r + 5s) and bound5s, term for term, with
- every Gaussian moment from the kernel's moment table (allmom2) on the forms in use (riglap4._restrict), as an mp.iv enclosure;
- every polynomial product on the kernel's SPoly; every scalar in mp.iv (m3_scal);
- the tilt rates c_v t_REF rounded UP to binary64 (C-TILT a) and certain positive definiteness of each tilt (C-TILT b);
- the far term at the theta0 that m3ref_v1 recorded (any theta is valid);
- Lemma U (PLAN_M3_CODE_v1 sect. 5, v1_2 sect. C): radii and tilt rates fixed at J_REF, so each bar holds for every J >= J_REF.
Upper ends only enter the bars: a min of two bounds is the min of their upper ends; a quantity >= 0 by construction has its lower end
clipped at 0 (m3_scal_v1.nonneg). Groupings: 'std' (riglap4.group_factors) or 'split' (one group per factor, kt_s9b_v3_2 l.219).
No compute of its own.
"""
import hashlib
import math
import time
from fractions import Fraction
from mpmath import iv
import m3_scal as S
from m3_series import Model, BASIS9
from m3_major import Majorants, hhat2


ARB = {'kern': None}
FALLBACKS = []


class Checkpoint(Exception):
    """raised by Prep.bound when the job script's budget stops an entry between two units; .state is the entry's state so far
    (entry name, groups digest, the computed units' values, C-BUDGET's maxrel), for the piece's hand-off and the next piece's resume."""
    def __init__(self, state):
        Exception.__init__(self, 'checkpoint in entry %s after %d units' % (state.get('entry'), len(state.get('vals', {}))))
        self.state = state


class TableFB:
    """one moment table of the layer with the API's recompute (SPEC_MA_LAYER_v1_3_API sect. 1): only the layer's MAFallback is caught;
    the value is then recomputed in arb by ARB['kern'] from the same arguments (its table built on first need). W_int goes with the forms
    W = W_int, exact integers (API sect. 3)."""
    def __init__(self, kern, Gam, n, D, groups, caps, Wi, label):
        self.kern, self.Gam, self.n, self.D, self.label = kern, Gam, n, D, label
        self.kw = {'groups': groups, 'caps': caps, 'W_int': Wi, 'W': S.arb_mat_of(Wi)}
        self.tab = kern.allmom2(Gam, n, D, **self.kw)
        self.zeroed = getattr(self.tab, 'zeroed', -1)
        self.arbtab = None

    def _arb(self, err):
        A = ARB['kern']
        if A is None:
            raise RuntimeError('MAFallback (%s) on table %s, and no arb kernel is set' % (err, self.label))
        FALLBACKS.append('%s: %s' % (self.label, err))
        if self.arbtab is None:
            self.arbtab = A.allmom2(self.Gam, self.n, self.D, **self.kw)
        return A, self.arbtab

    def E2(self, P, Q):
        try:
            return self.tab.E2(P, Q)
        except self.kern.MAFallback as err:
            A, tab = self._arb(err)
            return tab.E2(P.to_arb_dict(), Q.to_arb_dict())

    def lp_moment(self, P, p):
        try:
            return self.kern.lp_moment(self.tab, P, p)
        except self.kern.MAFallback as err:
            A, tab = self._arb(err)
            return A.lp_moment(tab, A.SPoly.from_dict(P.to_arb_dict(), P.nv), p)

    def pos_moment(self, P, p):
        try:
            return self.kern.pos_moment(self.tab, P, p)
        except self.kern.MAFallback as err:
            A, tab = self._arb(err)
            return A.pos_moment(tab, A.SPoly.from_dict(P.to_arb_dict(), P.nv), p)

    def lp_moment_ma(self, P, p):
        """E[P^(p/2) P^(p/2)] from the layer with fallback=False: the M-a ball, valid however wide (prep-stage norms only)."""
        Pk = P.power(p // 2)
        return self.tab.E2(Pk, Pk, fallback=False)


def support(P):
    s = set()
    for e in P.to_arb_dict():
        for i, x in enumerate(e):
            if x:
                s.add(i)
    return sorted(s)


def deg(P):
    return max([sum(e) for e in P.to_arb_dict()] + [0])


def qdeg(P, V):
    return max([sum(e[V:]) for e in P.to_arb_dict()] + [0])


def is_zero(P):
    return not P.to_arb_dict()


def restrict(kern, P, idx):
    """P in the variables idx only (riglap4._restrict); the kernel's enclosures become the new coefficients' radii."""
    out = {}
    for e, c in S.spoly_iv(P).items():
        k = tuple(e[i] for i in idx)
        out[k] = out[k] + c if k in out else c
    return S.spoly(kern, out, len(idx))


def group_factors(factors):
    """riglap4.group_factors: groups of factors with overlapping vertex sets, consts folded into a scalar."""
    scal = 1
    groups = []
    for f in factors:
        if f[0] == 'const':
            scal *= f[1]
            continue
        vs = set(f[1])
        hit = [gi for gi, (gv, gf) in enumerate(groups) if gv & vs]
        if not hit:
            groups.append((vs, [f]))
        else:
            gv, gf = groups[hit[0]]
            gv |= vs
            gf.append(f)
            for gi in sorted(hit[1:], reverse=True):
                gv |= groups[gi][0]
                gf.extend(groups[gi][1])
                groups.pop(gi)
    return scal, [gf for gv, gf in groups]


def split_groups(factors):
    """kt_s9b_v3_2.split_groups: one group per factor, consts folded into the scalar."""
    scal = 1
    groups = []
    for f in factors:
        if f[0] == 'const':
            scal *= f[1]
        else:
            groups.append([f])
    return scal, groups


def comps(i, ng):
    """compositions of i into ng parts, in riglap5b's order."""
    out = [()]
    for _ in range(ng):
        out = [c + (x,) for c in out for x in range(i + 1)]
    return [c for c in out if sum(c) == i]


def sup_F(factors, J):
    """riglap2.sup_F and riglap3.sup_F3 with every coefficient in absolute value; also the J-degree m_F of Lemma U."""
    J, t = S.I(J), 1 / S.I(J)
    s, mF = iv.mpf(1), 0
    for f in factors:
        if f[0] == 'const':
            s = s * abs(S.I(f[1]))
        elif f[0] == 'p':
            _, col, q1, q2, q3 = f
            val, mx = iv.mpf(1), 0
            for i, coef in ((1, q1), (2, q2), (3, q3)):
                for cb, mono in zip(coef, BASIS9):
                    val = val + S.ipow(t, i) * S.I(abs(cb)) * S.ipow(2 * J, len(mono))
                    if cb != 0.0:
                        mx = max(mx, len(mono) - i)
            s, mF = s * val, mF + mx
        elif f[0] == 'xi':
            _, col, c0, c9 = f
            val, mx = S.I(abs(c0)), 0
            for cb, mono in zip(c9, BASIS9):
                val = val + S.I(abs(cb)) * S.ipow(2 * J, len(mono))
                if cb != 0.0:
                    mx = max(mx, len(mono))
            s, mF = s * val, mF + mx
        else:
            raise ValueError('factor kind %r is not supported' % (f[0],))
    return S.finite(s), mF


class Prep:
    """riglap5s.Prep5s for one graph at J_REF, in stages for checkpointed pieces (PLAN_M3_CODE_v1 sect. 7):
    always (cheap, deterministic): the tilt rates rounded up (C-TILT a), the two tilts with a certain positive-definiteness test
    (C-TILT b), the series H(4) and E_0..E_3;
    stage 'u': Prep5r/5s's untilted norms: nE, nE4 (the 3^deg fallback above dmaxH), the 12 rE parts with min(ex, tr);
    stage 'c': the tilted norms nC8, nC6, P_out, P'_out, the far base at m3ref's theta0 and Lemma U's alpha_lo;
    scalars: the stage results restored from hand-offs instead of computed.
    Within each stage the largest-degree norm is computed first, so one moment table per covariance serves the rest.
    g: m3_graph_v1.GraphIV; avec: the radii a_v (binary64, m3ref's record); ap: rho'^2 (binary64); theta0: m3ref's choice."""
    UK = ('nE', 'nE4', 'rE_parts', 'rE')
    CK = ('nC8', 'nC6', 'Pout', 'Pout_p', 'farbase', 'alpha_lo')

    def __init__(self, kern, g, J, avec, ap, theta0, qcap, log=None, dmaxH=18, stages=('u', 'c'), scalars=None):
        self.kern, self.g, self.J, self.qcap, self.dmaxH = kern, g, S.I(J), qcap, dmaxH
        self.t = 1 / S.I(J)
        self.log = log if log is not None else (lambda s: None)
        V = g.V
        self.a_v, self.ap, self.theta0 = list(avec), ap, theta0
        self.tables = {}
        self.maxrel = 0.0
        self.ubudget, self.unit_done, self.ustate = None, None, None
        t = self.t
        self.rates = [S.up(-iv.log(1 - S.I(a)) / (2 * S.I(a)) * t) for a in self.a_v]
        self.ratesp = [S.up(-iv.log(1 - S.I(ap)) / (2 * S.I(ap)) * t)] * V
        self.tilt_c = g.tilted(self.rates)
        self.tilt_p = g.tilted(self.ratesp)
        self.ok = self.tilt_c is not None and self.tilt_p is not None
        self.log('PREP tilts: c %s, p %s' % ('certainly positive definite' if self.tilt_c else 'NOT certain',
                                              'certainly positive definite' if self.tilt_p else 'NOT certain'))
        self.m4 = Model(kern, g, 4, [])
        Hs = self.m4.H(4)
        self.H = Hs.c
        H1, H2, H3 = Hs.c[1], Hs.c[2], Hs.c[3]
        H1sq = H1.mul(H1)
        self.H1, self.H1sq = H1, H1sq
        self.Ej = [self.m4.const(1), H1, H2.add(H1sq.scale(S.ka(Fraction(1, 2)))), H3.add(H1.mul(H2)).add(H1sq.mul(H1).scale(S.ka(Fraction(1, 6))))]
        if scalars:
            for k, v in scalars.items():
                setattr(self, k, v)
        if not self.ok:
            return
        if 'u' in stages or 'c' in stages:
            mj = Majorants(kern, Model(kern, g, 5, []), self.a_v, t)
            self.h2 = mj.hbar(2)
            self.hh = hhat2(kern, g, self.a_v, t, self.h2)
        if 'u' in stages:
            self.stage_u(mj)
        if 'c' in stages:
            self.stage_c()

    def stage_u(self, mj):
        t, H = self.t, self.H
        H1, H2, H3, H4, H1sq = H[1], H[2], H[3], H[4], self.H1sq
        h2, hh = self.h2, self.hh
        h3, h5 = mj.hbar(3), mj.hbar(5)
        N2 = lambda P, lab: self.norm_any(P, 'u', 2, lab)
        T = lambda k: S.ipow(t, k)
        h2sq = h2.mul(h2)
        t0 = time.process_time()
        self.table('u', list(range(self.g.V)), 18)                # the D-18 vertex table serves every stage-u norm
        self.log('TABLE-CPU u vertex forms D 18: %.2f s' % (time.process_time() - t0))
        ex = T(6) / 48 * N2(h2sq.mul(h2), 'ex')
        rp = {'t4|H4|': T(4) * N2(H4, 't4|H4|'), 't5 h5/120': T(5) / 120 * N2(h5, 't5 h5'), 't4 H2^2/2': T(4) / 2 * N2(H2.mul(H2), 't4 H2^2'),
              't6 h3^2/72': T(6) / 72 * N2(h3.mul(h3), 't6 h3^2'), 't4|H1H3|': T(4) * N2(H1.mul(H3), 't4|H1H3|'),
              't5|H1H4|': T(5) * N2(H1.mul(H4), 't5|H1H4|'), 't6|H1|h5/120': T(6) / 120 * N2(H1.mul(h5), 't6|H1|h5'),
              't5|H2|h3/6': T(5) / 6 * N2(H2.mul(h3), 't5|H2|h3'), 't4 H1^2|H2|/2': T(4) / 2 * N2(H1sq.mul(H2), 't4 H1^2|H2|'),
              't5 H1^2 h3/12': T(5) / 12 * N2(H1sq.mul(h3), 't5 H1^2 h3'), 't5|H1|h2^2/8': T(5) / 8 * N2(H1.mul(h2sq), 't5|H1|h2^2')}
        tr = T(5) / 24 * N2(h2sq.mul(hh), 'tr')
        rp['E2^3 term'] = iv.mpf([iv.mpf(0), ex.b if ex.b < tr.b else tr.b])
        self.rE_parts = rp
        self.rE = S.isum(rp.values())
        self.nE = [iv.mpf(1)] + [N2(self.Ej[j], 'nE%d' % j) for j in (1, 2, 3)]
        self.nE4 = [iv.mpf(1)]
        for j in (1, 2, 3):
            if 4 * deg(self.Ej[j]) <= self.dmaxH:
                self.nE4.append(self.norm_any(self.Ej[j], 'u', 4, 'nE4_%d' % j))
            else:
                self.nE4.append(S.ipow(iv.mpf(3), deg(self.Ej[j])) * self.nE[j])

    def stage_c(self):
        g, t, T = self.g, self.t, (lambda k: S.ipow(self.t, k))
        H1, h2, hh = self.H1, self.h2, self.hh
        nh2_6 = self.norm_any(h2, 'c', 6, 'h2 p6')                # degree 18 first
        self.nC6 = t * self.norm_any(H1, 'c', 6, 'H1 p6') + T(2) / 2 * nh2_6
        self.nC8 = t * (self.norm_any(H1, 'c', 8, 'H1 p8') + self.norm_any(hh, 'c', 8, 'hh p8'))
        n_ = g.n
        self.Pout = S.isum(S.chi_tail_up(self.J * S.I(a) / gv, n_) for a, gv in zip(self.a_v, g.Gvv))
        self.Pout_p = S.isum(S.chi_tail_up(self.J * S.I(a) / gv, n_) for a, gv in zip(self.a_v, self.tilt_p['Gvv']))
        self.tree = g.tree()
        self.farbase = S.far_base(self.J, S.I(self.theta0), S.I(self.ap), g.Gvv, self.tree, g.N, g.V, g.log_tau)
        self.alpha_lo = min((S.I(self.theta0) * S.I(self.ap) / (2 * gv)).a for gv in g.Gvv)

    def track(self, x):
        """C-BUDGET's measure: the largest relative radius of the kernel's moment enclosures since the last reset."""
        m = abs(float(S.I(x).mid))
        if m > 0:
            self.maxrel = max(self.maxrel, float((S.I(x).b - S.I(x).a).b) / 2 / m)

    def scalars_out(self, stage):
        return {k: getattr(self, k) for k in (self.UK if stage == 'u' else self.CK)}

    def cov(self, which):
        return {'u': self.g.Gam, 'c': self.tilt_c and self.tilt_c['Gam'], 'p': self.tilt_p and self.tilt_p['Gam']}[which]

    def table(self, which, idx, D, groups=False, caps=None):
        """the kernel's moment table (a TableFB) on the forms idx under the covariance 'u', 'c' or 'p', degree >= D (cached; a larger
        table serves)."""
        key = (which, tuple(idx), bool(groups), tuple(sorted(caps.items())) if caps else ())
        hit = self.tables.get(key)
        if hit is not None and hit[0] >= D:
            return hit[1]
        Gam, Wi, gr = self.g.restrict(self.cov(which), idx)
        label = '%s forms %s D %d caps %s' % (which, list(idx), D, caps)
        t0 = time.process_time()
        tab = TableFB(self.kern, S.arb_mat_of(Gam), self.g.n, D, gr if groups else None, caps, Wi, label)
        self.tables[key] = (D, tab)
        self.log('TABLE %s: %d exact zeros' % (label, tab.zeroed))
        self.log('TABLE-CPU %s: %.2f s' % (label, time.process_time() - t0))
        return tab

    def lp_norm(self, P, which, p, dmax=64, prep=False):
        """riglap4.lp_norm: (E|P|^p)^(1/p), p even, on P's support; None above dmax. prep=True: no MAFallback recompute."""
        if is_zero(P):
            return iv.mpf(0)
        idx = support(P)
        if not idx:
            return abs(S.isum(S.spoly_iv(P).values()))
        Q = restrict(self.kern, P, idx)
        D = 2 * deg(Q) * (p // 2)
        if D > dmax:
            return None
        tab = self.table(which, idx, D)
        mom = S.arb_to_iv(tab.lp_moment_ma(Q, p) if prep else tab.lp_moment(Q, p))
        v = S.root(mom, p)
        self.track(v)
        return v

    def pos_norm(self, P, which, p):
        """riglap4.pos_norm: (E[P^p])^(1/p) for a pointwise nonnegative P."""
        if is_zero(P):
            return iv.mpf(0)
        idx = support(P)
        if not idx:
            return abs(S.isum(S.spoly_iv(P).values()))
        Q = restrict(self.kern, P, idx)
        tab = self.table(which, idx, deg(Q) * p)
        mom = S.arb_to_iv(tab.pos_moment(Q, p))
        v = S.root(mom, p)
        self.track(v)
        return v

    def holder_mono(self, P, which, p):
        """riglap4.holder_mono: sum over monomials |c| prod_v ||X_v||_{p|e|}^{e_v}, X-only P, ||X_v||_q = (E X_v^q)^(1/q) by m3_scal.ex_q."""
        Gvv = {'u': self.g.Gvv, 'c': self.tilt_c and self.tilt_c['Gvv'], 'p': self.tilt_p and self.tilt_p['Gvv']}[which]
        V = self.g.V
        tot = iv.mpf(0)
        for e, c in S.spoly_iv(P).items():
            assert all(x == 0 for x in e[V:]), 'Hoelder fallback only for X-only polynomials'
            k = sum(e)
            if k == 0:
                tot = tot + abs(c)
                continue
            q = p * k
            val = abs(c)
            for v in range(V):
                if e[v]:
                    val = val * S.ipow(S.root(S.ex_q(Gvv[v], q, self.g.n), q), e[v])
            tot = tot + val
        return tot

    def norm_any(self, P, which, p, label=None):
        t0 = time.process_time()
        v = self.lp_norm(P, which, p, self.dmaxH, prep=True)
        v = v if v is not None else self.holder_mono(P, which, p)
        if label:
            self.log('NORM %s %s p %d: %.2f s' % (which, label, p, time.process_time() - t0))
        return v

    # ------------------------------------------------------------------ per-entry part (riglap5s.bound5s with riglap5c's group cache)
    def gdata(self, gf):
        """series (order 3), majorants Fbar_0..4 at the radii a_v and Fbar_0 at rho'^2 for one factor group (riglap5c._gdata)."""
        if not hasattr(self, 'gcache'):
            self.gcache = {}
        key = repr(gf)
        if key not in self.gcache:
            kern, g, t = self.kern, self.g, self.t
            d = {'ser': Model(kern, g, 3, gf).Fser(3).c, 'norm': {}}
            if self.ok:
                mj = Majorants(kern, Model(kern, g, 4, gf), self.a_v, t)
                d['bar'] = [mj.Fbar(j) for j in range(5)]
                d['barp'] = Majorants(kern, Model(kern, g, 4, gf), [self.ap] * g.V, t).Fbar(0)
            self.gcache[key] = d
        return self.gcache[key]

    def gnorm(self, d, what, i, p, which):
        """riglap5c._gnorm: lp norms of the series terms and of Fbar_0', pos norms of the Fbar_j (cached per group)."""
        key = (what, i, p, which)
        if key not in d['norm']:
            if what == 'ser':
                P = d['ser'][i]
                d['norm'][key] = self.lp_norm(P, which, p, 64) if not is_zero(P) else iv.mpf(0)
            elif what == 'bar':
                P = d['bar'][i]
                d['norm'][key] = self.pos_norm(P, which, p) if not is_zero(P) else iv.mpf(0)
            else:
                P = d['barp']
                d['norm'][key] = self.lp_norm(P, which, p, 64) if not is_zero(P) else iv.mpf(0)
        return d['norm'][key]

    def series_product(self, gser, scal, kmax):
        return series_product(self.kern, self.g.F, gser, scal, kmax)

    def _unit(self, key, fn):
        """one checkpoint unit of the entry in progress (self.ustate): its value from the restored state, or computed now when the budget
        allows (self.ubudget(), set by the job script; None = no limit), else Checkpoint with the state so far. Each unit logs its CPU."""
        st = self.ustate
        if key in st['vals']:
            return st['vals'][key]
        if self.ubudget is not None and not self.ubudget():
            st['maxrel'] = self.maxrel
            raise Checkpoint(st)
        t0 = time.process_time()
        v = fn()
        dt = time.process_time() - t0
        st['vals'][key] = v
        self.log('UNIT %s %s: %.2f s' % (st['entry'], key, dt))
        if self.unit_done is not None:
            self.unit_done(dt, True)
        return v

    def bound(self, factors, grouping='std', bars=True, entry='', state=None):
        """riglap5s.bound5s: (ak enclosures, {rem, tail, ann, far} as mp.iv with valid upper ends, info), resumable between units:
        stage a: 'ak' (the a_k table), 'm0u' and 'm0c' (nF0, nF0c); then the group norms 'g|gi|what|i|p|which' in v7's order, stage b
        (which 'u'), stage c ('c': the nFc terms, nF4c's p = 4G and EF4's bar norms) and stage d ('p': nF0p). state: a Checkpoint's
        state for this entry (its name and groups digest must match). The arithmetic and the tables are v7's."""
        g, t, J = self.g, self.t, self.J
        V, n = g.V, g.n
        scal, groups = group_factors(factors) if grouping == 'std' else split_groups(factors)
        gid = hashlib.sha256(repr((scal, groups)).encode()).hexdigest()
        if state is not None and (state.get('entry') != entry or state.get('gid') != gid):
            raise ValueError('the restored state is for %r (groups %s), not for %r (groups %s)' % (state.get('entry'), state.get('gid'),
                                                                                                  entry, gid))
        if self.ubudget is not None and not self.ubudget():
            raise Checkpoint(state if state is not None else {'entry': entry, 'gid': gid, 'vals': {}, 'maxrel': 0.0})
        self.ustate = {'entry': entry, 'gid': gid, 'vals': dict(state['vals']) if state is not None else {},
                       'maxrel': state['maxrel'] if state is not None else 0.0}
        self.maxrel = max(self.maxrel, self.ustate['maxrel'])
        G_ = max(len(groups), 1)
        t0 = time.process_time()
        gds = [self.gdata(gf) for gf in groups]
        if groups:
            Fi = self.series_product([d['ser'] for d in gds], scal, 3)
        else:
            Fi = [S.spoly(self.kern, {tuple([0] * g.F): scal}, g.F)] + [self.kern.SPoly(g.F) for _ in range(3)]
        dtg = time.process_time() - t0
        self.log('GDATA-CPU %s: %.2f s (group series, majorants and F_i)' % (entry, dtg))
        if self.unit_done is not None:
            self.unit_done(dtg, False)
        for k, v in self.ustate['vals'].items():                  # restore the group norms of a resumed entry
            if k.startswith('g|'):
                _, gi, what, i, p, which = k.split('|')
                gds[int(gi)]['norm'].setdefault((what, int(i), int(p), which), v)
        qmax = max(qdeg(P, V) for P in Fi)
        assert qmax <= self.qcap, (qmax, self.qcap)
        Dn = max(deg(Fi[i]) + deg(self.Ej[k - i]) for k in range(4) for i in range(k + 1) if not is_zero(Fi[i]))
        use = sorted(set(sum((support(P) for P in Fi + self.Ej), [])))
        Fi_r = [restrict(self.kern, P, use) for P in Fi]
        Ej_r = [restrict(self.kern, P, use) for P in self.Ej]

        def ak_fn():
            tab = self.table('u', use, max(Dn, 1), True, {1: self.qcap})
            return [S.isum(S.arb_to_iv(tab.E2(Fi_r[i], Ej_r[k - i])) for i in range(k + 1) if not is_zero(Fi[i])) for k in range(4)]
        ak = self._unit('ak', ak_fn)
        info = {'groups': len(groups), 'Dn': Dn, 'forms': use}
        info['ak_relrad'] = max([float((S.I(a_).b - S.I(a_).a).b) / 2 / abs(float(S.I(a_).mid)) for a_ in ak if float(S.I(a_).mid) != 0] + [0.0])
        if not bars:
            return ak, None, info
        if not self.ok:
            raise ArithmeticError('a tilt is not certainly positive definite: no certified bar (riglap3 L1 would give +inf)')
        d0 = 2 * deg(Fi[0])
        m0u = self._unit('m0u', lambda: S.arb_to_iv(self.table('u', use, max(d0, 1), True, {1: 2 * self.qcap}).E2(Fi_r[0], Fi_r[0])))
        m0c = self._unit('m0c', lambda: S.arb_to_iv(self.table('c', use, max(d0, 1), True, {1: 2 * self.qcap}).E2(Fi_r[0], Fi_r[0])))
        nF0 = S.sqrt_nn(m0u)
        nF0c = S.sqrt_nn(m0c)
        self.track(nF0)
        self.track(nF0c)

        def gn(gi, what, i, p, which):
            key = 'g|%d|%s|%d|%d|%s' % (gi, what, i, p, which)
            d = gds[gi]
            if (what, i, p, which) in d['norm']:
                return self.ustate['vals'].setdefault(key, d['norm'][(what, i, p, which)])
            return self._unit(key, lambda: self.gnorm(d, what, i, p, which))

        def fnorm(i, which, p=2):
            return abs(S.I(scal)) * S.isum(math.prod((gn(gi, 'ser', ig, p * G_, which) for gi, ig in enumerate(c)),
                                                     start=iv.mpf(1)) for c in comps(i, len(groups)))
        T = lambda k: S.ipow(t, k)
        nF = [nF0] + [fnorm(i, 'u') for i in (1, 2, 3)]
        nFc = [nF0c] + [fnorm(i, 'c') for i in (1, 2, 3)]
        nFle3 = S.isum(T(i) * nF[i] for i in range(4))
        nFle3c = S.isum(T(i) * nFc[i] for i in range(4))
        three = iv.mpf(3)
        nF4c = fnorm(0, 'c', 4) + S.isum(T(i) * S.ipow(three, deg(Fi[i])) * nFc[i] for i in (1, 2, 3) if not is_zero(Fi[i]))
        EF4 = iv.mpf(0)
        for c in comps(4, len(groups)):
            EF4 = EF4 + S.I(Fraction(24, math.prod(math.factorial(x) for x in c))) * math.prod(
                (gn(gi, 'bar', jg, G_, 'c') for gi, jg in enumerate(c)), start=iv.mpf(1))
        EF4 = abs(S.I(scal)) * EF4
        overflow = S.isum(T(i + j) * nF[i] * self.nE[j] for i in range(4) for j in range(4) if i + j >= 4)
        Nc = self.tilt_c['N']
        f8 = nFle3c * S.ipow(self.nC8, 4)
        f6 = nF4c * S.ipow(self.nC6, 4)
        rho4 = Nc / 24 * iv.mpf([iv.mpf(0), f8.b if f8.b < f6.b else f6.b])
        B_rem = overflow + nFle3 * self.rE + rho4 + T(4) / 24 * Nc * EF4
        hc = lambda i: S.ipow(three, deg(Fi[i])) * nF[i] if not is_zero(Fi[i]) else iv.mpf(0)
        l2 = nF0 + S.isum(T(k) * S.isum((hc(i) if i > 0 else S.ipow(three, deg(Fi[0])) * nF0) * self.nE4[k - i] for i in range(k + 1))
                          for k in range(1, 4))
        B_tail = l2 * S.sqrt_nn(self.Pout)
        nF0p = abs(S.I(scal)) * math.prod((gn(gi, 'barp', 0, 2 * G_, 'p') for gi in range(len(gds))), start=iv.mpf(1))
        B_ann = self.tilt_p['N'] * nF0p * S.sqrt_nn(self.Pout_p)
        supF, mF = sup_F(factors, J)
        B_far = supF * self.farbase
        info.update({'mF': mF, 'overflow': overflow, 'F.R_E': nFle3 * self.rE, 'rho4': rho4, 'R_F': T(4) / 24 * Nc * EF4})
        info.update({'nF': nF, 'nFc': nFc, 'nFle3': nFle3, 'nFle3c': nFle3c, 'nF4c': nF4c, 'EF4': EF4, 'm0u': m0u, 'm0c': m0c,
                     'rho4_C8': Nc / 24 * f8, 'rho4_C6': Nc / 24 * f6})
        return ak, {'rem': B_rem, 'tail': B_tail, 'ann': B_ann, 'far': B_far}, info


def series_product(kern, nv, gser, scal, kmax):
    """riglap5b.series_product: F_i = scal sum over compositions prod_g F^(g)_{i_g}, i <= kmax (SPoly products)."""
    out = []
    for i in range(kmax + 1):
        acc = [kern.SPoly(nv)]

        def rec(gi, rem, cur):
            if gi == len(gser):
                if rem == 0:
                    acc[0] = acc[0].add(cur)
                return
            for ig in range(rem + 1):
                if not is_zero(gser[gi][ig]):
                    rec(gi + 1, rem - ig, cur.mul(gser[gi][ig]))
        rec(0, i, S.spoly(kern, {tuple([0] * nv): scal}, nv))
        out.append(acc[0])
    return out
