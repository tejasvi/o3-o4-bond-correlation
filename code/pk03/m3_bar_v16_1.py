#!/usr/bin/env python3
"""m3_bar_v16_1.py -- pk03 (code/pk03/). Lemma 19.1c bars on the M-a layer. REVISION of m3_bar_v15.py (fbf2d08a) for the review
the v1_10_4 run (2026-11-08 14:58Z), on the rules 051e1a64 and cc75cc3e (c1'); m3_bar_v16.py, an unfrozen draft of this
file, was never used:
- the big-table rule decides by declared key: Prep.declare_big, called by the job script before each entry's bound, lists every
  entry-level norm's own table (forms, D, pair cap) as bound will request it, and puts a norm in big_set when that table holds at least
  bigtab moments or its arb estimate (moments x arb_rate) passes arb_max. entry_moment consults big_set by the unit key, never the table
  that serves the norm: the layer's moments up to degree D are the same in any larger table on the same forms and caps, so the bars no
  longer depend on where a piece is cut. BIGRULE lines print the declared table beside the serving one;
- the state's 'big' entries are [unit key, inflation, e] (e = radius / |midpoint| of the moment, -1.0 when undefined);
- part_lines (051e1a64 (3)): each part's C-REP-B line, 1.15 x the product over the big-rule norms feeding it of (1 + inflation), the
  exempt keys left out (c1'); parts_of maps a unit to its parts; part_ok is C-REP-B's test; cap_over lists norms over the per-norm cap
  (051e1a64 (c)); exempt_over lists exempt norms whose e passes 1.1 x the declared e (cc75cc3e (ii)); table_moments counts a table's
  moments; budget_ok moves here from the job script;
- rule_plants adds PLANT-TABLE-COUNT, PLANT-PARTLINE, PLANT-PARTLINE-EXEMPT, PLANT-BIGCAP, PLANT-EXEMPT-E, PLANT-NORM-OK and PLANT-BUDGET;
  PLANT-BIGRULE tests the declared decision on tables of the wrong size.
Everything else is v15's; the docstrings of v15 (l.2-16), v14 (l.2-17), v13 (m3_bar_v13.py 33670f2c, l.2-102) and their predecessors
describe the rest.
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
NORM_REL = 2e-2   # m3_bar_v14: an entry-level norm takes the layer's M-a ball when its radius is at most this fraction of its midpoint


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

    def E2_ma(self, P, Q):
        """m3_bar_v13: E[P Q] from the layer with fallback=False, the M-a ball, valid however wide (bound's a_k terms). m3_bar_v14: a
        MAFallback of the layer's other kinds is recomputed in arb, as TableFB.E2 does."""
        try:
            return self.tab.E2(P, Q, fallback=False)
        except self.kern.MAFallback as err:
            A, tab = self._arb(err)
            return tab.E2(P.to_arb_dict(), Q.to_arb_dict())

    def E2_arb(self, P, Q, why):
        """m3_bar_v13: E[P Q] recomputed in arb by ARB['kern'] (its table built on first need), logged in FALLBACKS with why (an a_k total
        that fails ak_failing)."""
        A, tab = self._arb(why)
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

    def lp_ma(self, P, p):
        """m3_bar_v14: an entry-level lp moment E[P^(p/2) P^(p/2)], p even, as the layer's M-a ball: the kernel's lp_moment with
        fallback=False, its check on p kept."""
        if not (p % 2 == 0 and p >= 2):
            raise ValueError('check failed: p % 2 == 0 and p >= 2')
        Pk = P.power(p // 2)
        return self.tab.E2(Pk, Pk, fallback=False)

    def pos_ma(self, P, p):
        """m3_bar_v14: an entry-level pos moment E[P^p] as the layer's M-a ball: the kernel's pos_moment with fallback=False, its check on
        p kept."""
        if not (p >= 1):
            raise ValueError('check failed: p >= 1')
        return self.tab.E(P.power(p), fallback=False)

    def E2_ball(self, P, Q):
        """m3_bar_v14: E[P Q] as the layer's M-a ball (fallback=False) with no recompute here: entry_moment catches a MAFallback of the
        layer's other kinds (m0u, m0c)."""
        return self.tab.E2(P, Q, fallback=False)

    def moments(self):
        """m3_bar_v15: the layer table's moment count, all degrees (its code arrays)."""
        return sum(len(c) for c in self.tab.codes)


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


def relrad(a):
    """m3_bar_v13: radius / |midpoint| of an mp.iv from its ends in binary64 (inf when the midpoint is 0); a precision measure, INFO."""
    lo, hi = float(S.I(a).a), float(S.I(a).b)
    mid = (lo + hi) / 2
    return (hi - lo) / 2 / abs(mid) if mid != 0 else float('inf')


def ak_failing(sums, rel):
    """m3_bar_v13: the k whose summed a_k (mp.iv) fail the layer's test on the total: radius above rel x |midpoint|, or midpoint 0."""
    return [k for k, a in enumerate(sums) if not relrad(a) <= rel]


def norm_ok(v, rel):
    """m3_bar_v14: a norm v (mp.iv) has radius at most rel of its |midpoint| by Prep.track's measure (C-BUDGET's); a midpoint 0 fails."""
    v = S.I(v)
    mid = abs(float(v.mid))
    return mid > 0 and float((v.b - v.a).b) / 2 / mid <= rel


def infl_of(e, p):
    """m3_bar_v15: a big-rule norm's inflation (1 + e)^(1/p) - 1 for its moment's e = radius / |midpoint| (binary64, INFO); -1.0 stands for
    an undefined one (midpoint 0)."""
    return (1 + e) ** (1.0 / p) - 1 if math.isfinite(e) else -1.0


def infl_str(x):
    return 'undefined (midpoint 0)' if x < 0 else '%.3e' % x


def table_moments(nf, D, nv=None, cap=None):
    """m3_bar_v16: the moments of a layer table of degree <= D on nf forms, C(D + nf, nf); with cap, the forms are nv vertex forms and nf - nv
    pair forms whose total degree is at most cap (the kernel's MomTable codes over all levels, groups 0 and 1, caps {1: cap})."""
    if cap is None:
        return math.comb(D + nf, nf)
    npair = nf - nv
    if npair == 0:
        return math.comb(D + nv, nv)
    return sum(math.comb(a + npair - 1, npair - 1) * math.comb(D - a + nv, nv) for a in range(min(cap, D) + 1))


def parts_of(key):
    """m3_bar_v16: the bar parts a unit's norm feeds, by bound's arithmetic: m0u and the u series norms feed rem (overflow, F.R_E) and tail
    (l2); m0c, the c series norms and the bar norms feed rem (rho4, R_F); barp norms feed ann; far takes no norm."""
    if key == 'm0u':
        return ('rem', 'tail')
    if key == 'm0c':
        return ('rem',)
    _, gi, what, i, p, which = key.split('|')
    if what == 'barp':
        return ('ann',)
    if what == 'ser' and which == 'u':
        return ('rem', 'tail')
    return ('rem',)


def part_lines(big, base=1.15, exempt=()):
    """m3_bar_v16 (the review 051e1a64 (3)): each part's upper C-REP-B line, base x the product over the big-rule norms [key, inflation, e]
    feeding it of (1 + inflation); an undefined inflation (-1.0) adds no allowance, and neither does an exempt key (the c1'
    cc75cc3e: its inflation stays in the bound, not in the line), so a miss stops for a report."""
    lines = {q: base for q in ('rem', 'tail', 'ann', 'far')}
    for b in big:
        if b[1] >= 0 and b[0] not in exempt:
            for q in parts_of(b[0]):
                lines[q] *= 1 + b[1]
    return lines


def part_ok(ratio, line):
    """m3_bar_v16: C-REP-B's test of one bar part: certified/float within [1 - 1e-6, line]."""
    return 1 - 1e-6 <= ratio <= line


def cap_over(big, cap, exempt=()):
    """m3_bar_v16 (the review 051e1a64 (c)): the big-rule norms over the per-norm inflation cap, undefined inflations included, the exempt keys
    left out, as (key, inflation)."""
    return [(b[0], b[1]) for b in big if (b[1] < 0 or b[1] > cap) and b[0] not in exempt]


def exempt_over(big, declared, factor=1.1):
    """m3_bar_v16 (the review cc75cc3e (ii)): the exempt norms (declared: key -> its declared e) whose measured e passes factor x the declared e
    in binary64, an undefined e included, as (key, e, declared e)."""
    return [(b[0], b[2], declared[b[0]]) for b in big if b[0] in declared and (b[2] < 0 or b[2] > factor * declared[b[0]])]


def budget_ok(maxrel, rnd, barsum):
    """C-BUDGET's test (m3_run_v1_10_2; m3_bar_v16 holds it): the largest relative radius of a tracked norm at most NORM_REL, rnd at most 0.1
    of the bar."""
    return maxrel <= NORM_REL and rnd <= 0.1 * barsum


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
    g: m3_graph_v1.GraphIV; avec: the radii a_v (binary64, m3ref's record); ap: rho'^2 (binary64); theta0: m3ref's choice.
    m3_bar_v16: big_set and big_decl (the declared big-rule set and its tables; None = off) are set per entry by declare_big."""
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
        self.big_set, self.big_decl, self.big_hits, self.cur_unit = None, None, [], None
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
        dv = min(18, self.dmaxH)
        self.table('u', list(range(self.g.V)), dv)                # the vertex table at min(18, dmaxH) serves every stage-u norm
        self.log('TABLE-CPU u vertex forms D %d: %.2f s' % (dv, time.process_time() - t0))
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
        """C-BUDGET's measure: the largest relative radius of the norms since the last reset, each read after the root of its moment
        enclosure (m3_bar_v14: the wording, norm_ok reads the same measure)."""
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

    def big_rule(self, key):
        """m3_bar_v16: the big-table rule's test on an entry-level norm: its unit key is in the declared set (declare_big), whatever table
        serves it; None = the rule off."""
        return self.big_set is not None and key in self.big_set

    def declare_big(self, groups, scal, bigtab, arb_rate, arb_max):
        """m3_bar_v16: the entry's big-rule set, declared before its bound from each entry-level
        norm's own table as bound will request it, never from the table that serves it: m0u and m0c on the entry's forms with the pair cap
        2 qcap; the group norms 'g|gi|what|i|p|which' at bound's exponents (ser at 2G for u and c and at 4G for c, bar at G for c, barp at
        2G for p; a key bound never asks for is harmless). A norm is in the set when its table holds at least bigtab moments or its arb
        estimate (moments x arb_rate) passes arb_max (a part None is off). Sets self.big_set and self.big_decl (key -> (forms, D,
        moments)); returns the rows (key, forms, D, moments, in the set). Call it after qcap is set."""
        G_ = max(len(groups), 1)
        gds = [self.gdata(gf) for gf in groups]
        if groups:
            Fi = self.series_product([d['ser'] for d in gds], scal, 3)
        else:
            Fi = [S.spoly(self.kern, {tuple([0] * self.g.F): scal}, self.g.F)] + [self.kern.SPoly(self.g.F) for _ in range(3)]
        use = sorted(set(sum((support(P) for P in Fi + self.Ej), [])))
        nv = sum(1 for f in use if self.g.groups[f] == 0)
        d0 = max(2 * deg(Fi[0]), 1)
        rows = [(k_, len(use), d0, table_moments(len(use), d0, nv, 2 * self.qcap)) for k_ in ('m0u', 'm0c')]
        for gi, d in enumerate(gds):
            reqs = [('ser', i, 2 * G_, w) for w in ('u', 'c') for i in range(4)] + [('ser', 0, 4 * G_, 'c')]
            if self.ok:
                reqs += [('bar', j, G_, 'c') for j in range(5)] + [('barp', 0, 2 * G_, 'p')]
            for what, i, p, which in reqs:
                P = d['ser'][i] if what == 'ser' else (d['bar'][i] if what == 'bar' else d['barp'])
                if is_zero(P) or not support(P):
                    continue
                D = deg(P) * p if what == 'bar' else 2 * deg(P) * (p // 2)
                rows.append(('g|%d|%s|%d|%d|%s' % (gi, what, i, p, which), len(support(P)), D, table_moments(len(support(P)), D)))
        out = [(k_, nf, D, M, (bigtab is not None and M >= bigtab) or (arb_rate is not None and arb_max is not None and M * arb_rate > arb_max))
               for k_, nf, D, M in rows]
        self.big_set = frozenset(r[0] for r in out if r[4])
        self.big_decl = {r[0]: r[1:4] for r in out}
        return out

    def entry_moment(self, ma_fn, fb_fn, normf, tab=None, p=None):
        """m3_bar_v14: an entry-level norm's moment: the layer's M-a ball (ma_fn, fallback=False) when the norm normf makes from it passes
        norm_ok at NORM_REL, else fb_fn, v13's TableFB call (its arb recompute on the layer's MAFallback); a MAFallback of the layer's
        other kinds in ma_fn (non-finite, out of range) also takes fb_fn. Each moment sent to fb_fn is counted (NORM-RULE). m3_bar_v15:
        returns (moment, kind), kind 'ma', 'big' (the big-table rule: the M-a ball itself, a BIGRULE line, its inflation and e added to
        self.big_hits) or 'fb'. m3_bar_v16: 'big' by the declared set (big_rule of the unit key)."""
        try:
            m = S.arb_to_iv(ma_fn())
        except self.kern.MAFallback:
            m = None
        if m is not None and norm_ok(normf(m), NORM_REL):
            return m, 'ma'
        if m is not None and tab is not None and self.big_rule(self.cur_unit):
            e = relrad(m)
            x = infl_of(e, p)
            self.big_hits.append((x, e if math.isfinite(e) else -1.0))
            dec = tuple((self.big_decl or {}).get(self.cur_unit, ('-', '-', '-')))
            self.log('BIGRULE %s %s: declared forms %s D %s moments %s; served by table %s (moments %d): e %.3e, p %d, inflation %s' % (
                (self.ustate['entry'] if self.ustate else '-', self.cur_unit) + dec + (tab.label, tab.moments(), e, p, infl_str(x))))
            return m, 'big'
        self.norm_fb = getattr(self, 'norm_fb', 0) + 1
        return S.arb_to_iv(fb_fn()), 'fb'

    def lp_norm(self, P, which, p, dmax=64, prep=False):
        """riglap4.lp_norm: (E|P|^p)^(1/p), p even, on P's support; None above dmax. prep=True: no MAFallback recompute. m3_bar_v14: an
        entry-level norm (prep=False) takes its moment by entry_moment (m3_bar_v15: a big-rule norm is not tracked)."""
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
        if prep:
            mom, kind = S.arb_to_iv(tab.lp_moment_ma(Q, p)), 'ma'
        else:
            mom, kind = self.entry_moment(lambda: tab.lp_ma(Q, p), lambda: tab.lp_moment(Q, p), lambda m: S.root(m, p), tab, p)
        v = S.root(mom, p)
        if kind != 'big':
            self.track(v)
        return v

    def pos_norm(self, P, which, p):
        """riglap4.pos_norm: (E[P^p])^(1/p) for a pointwise nonnegative P. m3_bar_v14: its moment by entry_moment (m3_bar_v15: a big-rule
        norm is not tracked)."""
        if is_zero(P):
            return iv.mpf(0)
        idx = support(P)
        if not idx:
            return abs(S.isum(S.spoly_iv(P).values()))
        Q = restrict(self.kern, P, idx)
        tab = self.table(which, idx, deg(Q) * p)
        mom, kind = self.entry_moment(lambda: tab.pos_ma(Q, p), lambda: tab.pos_moment(Q, p), lambda m: S.root(m, p), tab, p)
        v = S.root(mom, p)
        if kind != 'big':
            self.track(v)
        return v

    def holder_mono(self, P, which, p):
        """riglap4.holder_mono: sum over monomials |c| prod_v ||X_v||_{p|e|}^{e_v}, X-only P, ||X_v||_q = (E X_v^q)^(1/q) by m3_scal.ex_q."""
        Gvv = {'u': self.g.Gvv, 'c': self.tilt_c and self.tilt_c['Gvv'], 'p': self.tilt_p and self.tilt_p['Gvv']}[which]
        V = self.g.V
        tot = iv.mpf(0)
        for e, c in S.spoly_iv(P).items():
            if any(x != 0 for x in e[V:]):
                raise ValueError('Hoelder fallback only for X-only polynomials')
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
        """series (order 3), majorants Fbar_0..4 at the radii a_v and Fbar_0 at rho'^2 for one factor group (riglap5c._gdata).
        m3_bar_v12 (C-GCACHE): the cache key is repr of the group's full factor tuples, never a column or group index. m3_bar_v15: 'big'
        holds (inflation, e) of its norms that took the big-table rule."""
        if not hasattr(self, 'gcache'):
            self.gcache = {}
        key = repr(gf)
        if key not in self.gcache:
            kern, g, t = self.kern, self.g, self.t
            d = {'ser': Model(kern, g, 3, gf).Fser(3).c, 'norm': {}, 'big': {}}
            if self.ok:
                mj = Majorants(kern, Model(kern, g, 4, gf), self.a_v, t)
                d['bar'] = [mj.Fbar(j) for j in range(5)]
                d['barp'] = Majorants(kern, Model(kern, g, 4, gf), [self.ap] * g.V, t).Fbar(0)
            self.gcache[key] = d
        return self.gcache[key]

    def gnorm(self, d, what, i, p, which):
        """riglap5c._gnorm: lp norms of the series terms and of Fbar_0', pos norms of the Fbar_j (cached per group). m3_bar_v12: an lp
        norm whose degree passes dmax 64 is a refusal (ValueError), never a None carried into a product."""
        key = (what, i, p, which)
        if key not in d['norm']:
            if what == 'ser':
                P = d['ser'][i]
                v = self.lp_norm(P, which, p, 64) if not is_zero(P) else iv.mpf(0)
            elif what == 'bar':
                P = d['bar'][i]
                v = self.pos_norm(P, which, p) if not is_zero(P) else iv.mpf(0)
            else:
                P = d['barp']
                v = self.lp_norm(P, which, p, 64) if not is_zero(P) else iv.mpf(0)
            if v is None:
                raise ValueError('group norm %s %d at p %d (%s): degree %d x %d passes dmax 64; refused' % (what, i, p, which, 2 * deg(P), p // 2))
            d['norm'][key] = v
        return d['norm'][key]

    def series_product(self, gser, scal, kmax):
        return series_product(self.kern, self.g.F, gser, scal, kmax)

    def _unit(self, key, fn):
        """one checkpoint unit of the entry in progress (self.ustate): its value from the restored state, or computed now when the budget
        allows (self.ubudget(), set by the job script; None = no limit), else Checkpoint with the state so far. Each unit logs its CPU.
        m3_bar_v15: a computed unit whose norm took the big-table rule enters the state's 'big' list (m3_bar_v16: [key, inflation, e])."""
        st = self.ustate
        if key in st['vals']:
            return st['vals'][key]
        if self.ubudget is not None and not self.ubudget():
            st['maxrel'] = self.maxrel
            raise Checkpoint(st)
        t0 = time.process_time()
        self.cur_unit, self.big_hits = key, []
        v = fn()
        dt = time.process_time() - t0
        st['vals'][key] = v
        if self.big_hits:
            xs, es = [h[0] for h in self.big_hits], [h[1] for h in self.big_hits]
            st['big'].append([key, -1.0 if min(xs) < 0 else max(xs), -1.0 if min(es) < 0 else max(es)])
        self.log('UNIT %s %s: %.2f s' % (st['entry'], key, dt))
        if self.unit_done is not None:
            self.unit_done(dt, True)
        return v

    def bound(self, factors, grouping='std', bars=True, entry='', state=None, ak_zero=False):
        """riglap5s.bound5s: (ak enclosures, {rem, tail, ann, far} as mp.iv with valid upper ends, info), resumable between units:
        stage a: 'ak' (the a_k table), 'm0u' and 'm0c' (nF0, nF0c); then the group norms 'g|gi|what|i|p|which' in v7's order, stage b
        (which 'u'), stage c ('c': the nFc terms, nF4c's p = 4G and EF4's bar norms) and stage d ('p': nF0p). state: a Checkpoint's
        state for this entry (its name and groups digest must match). The arithmetic and the tables are v7's. m3_bar_v12: grouping may be
        an explicit partition ('partition', scal, groups) that the job script has checked and fixed. m3_bar_v13: the 'ak' unit takes its
        terms as M-a balls and tests each summed a_k (ak_failing), recomputing in arb only a total that fails; ak_zero=True (a parity zero
        that the job script proved by C-ODD) skips that test. m3_bar_v14: m0u, m0c and the group norms take their moments by entry_moment,
        and NORM-RULE logs how many took v13's call. m3_bar_v15: the state's 'big' list (m3_bar_v16: [unit key, inflation, e]) for the
        norms that took the big-table rule (restored with the state, added from the group cache) keeps m0u and m0c out of track; info['big']
        and NORM-RULE report it."""
        g, t, J = self.g, self.t, self.J
        V, n = g.V, g.n
        if grouping == 'std':
            scal, groups = group_factors(factors)
        elif grouping == 'split':
            scal, groups = split_groups(factors)
        elif isinstance(grouping, tuple) and len(grouping) == 3 and grouping[0] == 'partition':
            scal, groups = grouping[1], [list(gf) for gf in grouping[2]]
        else:
            raise ValueError('grouping %r is neither std, split nor (partition, scal, groups)' % (grouping,))
        gid = hashlib.sha256(repr((scal, groups)).encode()).hexdigest()
        if state is not None and (state.get('entry') != entry or state.get('gid') != gid):
            raise ValueError('the restored state is for %r (groups %s), not for %r (groups %s)' % (state.get('entry'), state.get('gid'),
                                                                                                  entry, gid))
        if self.ubudget is not None and not self.ubudget():
            raise Checkpoint(state if state is not None else {'entry': entry, 'gid': gid, 'vals': {}, 'maxrel': 0.0, 'big': []})
        self.ustate = {'entry': entry, 'gid': gid, 'vals': dict(state['vals']) if state is not None else {},
                       'maxrel': state['maxrel'] if state is not None else 0.0,
                       'big': [list(b) for b in state.get('big', [])] if state is not None else []}
        self.maxrel = max(self.maxrel, self.ustate['maxrel'])
        self.norm_fb = 0
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
        for b in self.ustate['big']:                              # m3_bar_v15: and their big-rule marks
            if b[0].startswith('g|'):
                _, gi, what, i, p, which = b[0].split('|')
                gds[int(gi)]['big'].setdefault((what, int(i), int(p), which), (b[1], b[2]))
        qmax = max(qdeg(P, V) for P in Fi)
        if qmax > self.qcap:
            raise ValueError('pair degree %d above qcap %d' % (qmax, self.qcap))
        Dn = max(deg(Fi[i]) + deg(self.Ej[k - i]) for k in range(4) for i in range(k + 1) if not is_zero(Fi[i]))
        use = sorted(set(sum((support(P) for P in Fi + self.Ej), [])))
        Fi_r = [restrict(self.kern, P, use) for P in Fi]
        Ej_r = [restrict(self.kern, P, use) for P in self.Ej]

        def ak_fn():                                              # m3_bar_v13: the terms as M-a balls, the layer's test on each total
            tab = self.table('u', use, max(Dn, 1), True, {1: self.qcap})
            rel = self.kern.FALLBACK_REL
            ks = [[i for i in range(k + 1) if not is_zero(Fi[i])] for k in range(4)]
            balls = [[tab.E2_ma(Fi_r[i], Ej_r[k - i]) for i in ks[k]] for k in range(4)]
            sums = [S.isum(S.arb_to_iv(b) for b in balls[k]) for k in range(4)]
            trel = [float(b.rad()) / abs(float(b.mid())) if float(b.mid()) != 0 else float('inf') for bk in balls for b in bk]
            redo = [] if ak_zero else ak_failing(sums, rel)
            for k in redo:
                why = 'the a_%d total of %s fails FALLBACK_REL (radius / |mid| %.2e)' % (k, entry, relrad(sums[k]))
                sums[k] = S.isum(S.arb_to_iv(tab.E2_arb(Fi_r[i], Ej_r[k - i], why)) for i in ks[k])
            self.log('AK-TERMS %s: %d of %d terms over FALLBACK_REL %g (largest term radius / |mid| %.2e); totals radius / |mid| %s; %s' % (
                entry, sum(1 for r in trel if r > rel), len(trel), rel, max(trel + [0.0]), ['%.2e' % relrad(a) for a in sums],
                'parity zero: no total test (C-ODD-AK)' if ak_zero else ('recomputed in arb: a_k for k in %s' % redo if redo else 'every total passes')))
            return sums
        ak = self._unit('ak', ak_fn)
        info = {'groups': len(groups), 'Dn': Dn, 'forms': use}
        info['ak_relrad'] = max([float((S.I(a_).b - S.I(a_).a).b) / 2 / abs(float(S.I(a_).mid)) for a_ in ak if float(S.I(a_).mid) != 0] + [0.0])
        if not bars:
            return ak, None, info
        if not self.ok:
            raise ArithmeticError('a tilt is not certainly positive definite: no certified bar (riglap3 L1 would give +inf)')
        d0 = 2 * deg(Fi[0])

        def m0(which):                                            # m3_bar_v14: the M-a ball under NORM_REL, else v13's TableFB.E2
            tab = self.table(which, use, max(d0, 1), True, {1: 2 * self.qcap})
            return self.entry_moment(lambda: tab.E2_ball(Fi_r[0], Fi_r[0]), lambda: tab.E2(Fi_r[0], Fi_r[0]), S.sqrt_nn, tab, 2)[0]
        m0u = self._unit('m0u', lambda: m0('u'))
        m0c = self._unit('m0c', lambda: m0('c'))
        nF0 = S.sqrt_nn(m0u)
        nF0c = S.sqrt_nn(m0c)
        bigk = [b[0] for b in self.ustate['big']]
        for k_, v_ in (('m0u', nF0), ('m0c', nF0c)):              # m3_bar_v15: a big-rule m0 is not tracked
            if k_ not in bigk:
                self.track(v_)

        def gn(gi, what, i, p, which):
            key = 'g|%d|%s|%d|%d|%s' % (gi, what, i, p, which)
            d = gds[gi]
            nk = (what, i, p, which)
            if nk in d['norm']:
                if nk in d['big'] and key not in [b[0] for b in self.ustate['big']]:   # m3_bar_v15: a big-rule norm from the group cache
                    self.ustate['big'].append([key, d['big'][nk][0], d['big'][nk][1]])
                    self.log('BIGRULE %s %s: the group cache\'s big-rule norm, e %.3e, inflation %s' % (entry, key, d['big'][nk][1],
                                                                                                         infl_str(d['big'][nk][0])))
                return self.ustate['vals'].setdefault(key, d['norm'][nk])
            v = self._unit(key, lambda: self.gnorm(d, what, i, p, which))
            for b in self.ustate['big']:
                if b[0] == key:
                    d['big'][nk] = (b[1], b[2])
            return v

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
        big = [list(b) for b in self.ustate['big']]
        bmax = -1.0 if any(b[1] < 0 for b in big) else max([b[1] for b in big] + [0.0])
        info['norm_fb'], info['big'], info['big_max'] = self.norm_fb, big, bmax
        self.log('NORM-RULE %s: %d entry-level moments took v13\'s call (norm radius over NORM_REL %g of its midpoint, or a MAFallback of the '
                 'layer\'s other kinds; computed in this run, restored units not counted); %d norms of the entry took the big-table rule '
                 '(restored units and the group cache included; largest inflation %s)' % (entry, self.norm_fb, NORM_REL, len(big), infl_str(bmax)))
        return ak, {'rem': B_rem, 'tail': B_tail, 'ann': B_ann, 'far': B_far}, info


def rule_plants(kern):
    """m3_bar_v16: the job script's rule plants, as (name, fired, line), on stand-ins: PLANT-NORM-REL (v15's cases: [0.97, 1.03] under
    S.sqrt_nn and [0.91, 1.09] under S.root(., 6) kept, [0.85, 1.15] at p 6, [0.94, 1.06] under S.sqrt_nn and a MAFallback sent);
    PLANT-BIGRULE (the declared set decides, whatever table serves: the declared key kA on a 10-moment table stays 'ma' under NORM_REL,
    takes 'big' at [0.85, 1.15] p 6 with inflation 1.15^(1/6) - 1 and is sent on a MAFallback; the undeclared kB on a 1e7-moment table is
    sent); PLANT-TABLE-COUNT (table_moments against two small layer tables, uncapped and with the pair cap); PLANT-PARTLINE (part_lines on
    a planted list; a part at its line x (1 + 1e-6) and a part without big-rule factors at 1.16 fail part_ok); PLANT-PARTLINE-EXEMPT (an
    exempt factor stays out of the line: a part at the unwidened line x (1 + 1e-6) fails, while the widened line would pass it);
    PLANT-BIGCAP (cap_over with and without an exemption); PLANT-EXEMPT-E (exempt_over refuses e = 1.1 x declared + 1 ulp, an undefined e
    and a declared e lowered by 20%, and passes e = 1.1 x declared); PLANT-NORM-OK (norm_ok at radius 2.1e-2, midpoint 0 and 1.9e-2) and
    PLANT-BUDGET (budget_ok at 1.05 and 0.95 NORM_REL, rnd 0.11 and 0.09 of the bar)."""
    import types

    def stub(nm):
        return types.SimpleNamespace(moments=lambda: nm, label='planted table of %d moments' % nm)
    st = types.SimpleNamespace(kern=kern, norm_fb=0, big_set=None, big_decl=None, big_hits=[], cur_unit='-', ustate=None,
                               log=lambda s: None)
    st.big_rule = lambda key: Prep.big_rule(st, key)

    def mafb():
        raise kern.MAFallback('planted by PLANT-NORM-REL')

    def kind(lo, hi, normf, p, tab=None, key='-'):
        st.cur_unit = key
        ma = mafb if lo is None else (lambda: S.iv_to_arb(iv.mpf([lo, hi])))
        return Prep.entry_moment(st, ma, lambda: S.iv_to_arb(iv.mpf(['0.999999999999', '1.000000000001'])), normf, tab, p)[1]
    r6 = lambda m: S.root(m, 6)
    got1 = [kind('0.97', '1.03', S.sqrt_nn, 2), kind('0.91', '1.09', r6, 6), kind('0.85', '1.15', r6, 6), kind('0.94', '1.06', S.sqrt_nn, 2),
            kind(None, None, S.sqrt_nn, 2)]
    st.big_set, st.big_decl = frozenset(['kA']), {'kA': (6, 36, 5245786)}
    got2 = [kind('0.97', '1.03', S.sqrt_nn, 2, stub(10), 'kA'), kind('0.85', '1.15', r6, 6, stub(10), 'kA')]
    x = st.big_hits[-1][0] if st.big_hits else -1.0
    got2 += [kind(None, None, r6, 6, stub(10), 'kA'), kind('0.85', '1.15', r6, 6, stub(10 ** 7), 'kB')]
    x0 = 1.15 ** (1.0 / 6) - 1
    g3, i3 = [[2, 1, 0], [1, 3, 1], [0, 1, 2]], [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
    n1 = TableFB(kern, S.arb_mat_of(g3), 3, 4, None, None, i3, 'count test').moments()
    n2 = TableFB(kern, S.arb_mat_of(g3), 3, 4, [0, 0, 1], {1: 1}, i3, 'count test, pair cap 1').moments()
    pl = part_lines([['m0u', 0.1, 0.21], ['g|0|barp|0|6|p', 0.2, 1.99], ['g|1|ser|2|4|c', 0.05, 0.22], ['g|0|ser|3|6|u', -1.0, -1.0]])
    want = {'rem': 1.15 * 1.1 * 1.05, 'tail': 1.15 * 1.1, 'ann': 1.15 * 1.2, 'far': 1.15}
    plk = all(abs(pl[q] - want[q]) <= 1e-12 for q in want) and part_lines([]) == {q: 1.15 for q in want}
    plk = plk and not part_ok(pl['rem'] * (1 + 1e-6), pl['rem']) and part_ok(pl['rem'], pl['rem']) and not part_ok(1.16, 1.15)
    bx = [['g|0|ser|3|6|u', 0.34, 4.795], ['g|0|ser|2|6|u', 0.0666, 0.4726]]
    lx, la = part_lines(bx, 1.15, ('g|0|ser|3|6|u',))['rem'], part_lines(bx)['rem']
    ex1 = not part_ok(lx * (1 + 1e-6), lx) and part_ok(lx * (1 + 1e-6), la) and abs(lx - 1.15 * 1.0666) <= 1e-12
    big = [['k1', 0.05, 0.3], ['k2', 0.34, 4.8], ['k3', -1.0, -1.0]]
    e1 = math.nextafter(1.1 * 4.795, math.inf)
    ex2 = (exempt_over([['kE', 0.34, e1]], {'kE': 4.795}) == [('kE', e1, 4.795)] and exempt_over([['kE', 0.34, 1.1 * 4.795]], {'kE': 4.795}) == []
           and len(exempt_over([['kE', 0.34, 4.795]], {'kE': 0.8 * 4.795})) == 1 and len(exempt_over([['kE', -1.0, -1.0]], {'kE': 4.795})) == 1)
    nok = [norm_ok(iv.mpf(v), NORM_REL) for v in (['0.979', '1.021'], ['-1e-9', '1e-9'], ['0.981', '1.019'])]
    return [('PLANT-NORM-REL', got1 == ['ma', 'ma', 'fb', 'fb', 'fb'], '(entry_moment at NORM_REL %g on [0.97, 1.03] sqrt, [0.91, 1.09] p 6, '
             '[0.85, 1.15] p 6, [0.94, 1.06] sqrt and a MAFallback: %s; ma, ma, fb, fb, fb wanted)' % (NORM_REL, got1)),
            ('PLANT-BIGRULE', got2 == ['ma', 'big', 'fb', 'fb'] and abs(x - x0) <= 1e-9, '(declared set {kA}: kA on a 10-moment table with '
             '[0.97, 1.03] sqrt, [0.85, 1.15] p 6 and a MAFallback, kB on a 1e7-moment table with [0.85, 1.15] p 6: %s; ma, big, fb, fb wanted; '
             'the big one\'s inflation %.6e against 1.15^(1/6) - 1 = %.6e)' % (got2, x, x0)),
            ('PLANT-TABLE-COUNT', n1 == table_moments(3, 4) == 35 and n2 == table_moments(3, 4, 2, 1) == 25, '(layer tables on 3 forms at D 4: '
             '%d moments, and with the pair form capped at 1: %d; table_moments 35 and 25 wanted)' % (n1, n2)),
            ('PLANT-PARTLINE', plk, '(part_lines on m0u 0.1, a barp 0.2, a c series norm 0.05 and an undefined u series norm: %s, %s wanted; '
             'part_ok refuses rem at its line x (1 + 1e-6) and a part without big-rule factors at 1.16)' % (
                 {q: round(v, 9) for q, v in pl.items()}, {q: round(v, 9) for q, v in want.items()})),
            ('PLANT-PARTLINE-EXEMPT', ex1, '(an exempt factor of inflation 0.34 beside a non-exempt 0.0666: unwidened rem line %.9f, widened %.9f; '
             'a part at the unwidened line x (1 + 1e-6) must fail, the widened line would pass it)' % (lx, la)),
            ('PLANT-BIGCAP', cap_over(big, 0.10, ('k2',)) == [('k3', -1.0)] and cap_over(big, 0.10) == [('k2', 0.34), ('k3', -1.0)],
             '(cap_over at a cap of 0.10 on inflations 0.05, 0.34 and undefined, with k2 exempt and without)'),
            ('PLANT-EXEMPT-E', ex2, '(exempt_over with declared e 4.795: e = 1.1 x 4.795 + 1 ulp refused, e = 1.1 x 4.795 passed; e 4.795 against a '
             'declared e lowered by 20%, and an undefined e, refused)'),
            ('PLANT-NORM-OK', nok == [False, False, True], '(norm_ok on radius 2.1e-2, midpoint 0 and radius 1.9e-2: %s; [False, False, True] '
             'wanted)' % nok),
            ('PLANT-BUDGET', not budget_ok(1.05 * NORM_REL, 0.0, 1.0) and not budget_ok(0.0, 0.11, 1.0) and budget_ok(0.95 * NORM_REL, 0.09, 1.0),
             '(budget_ok must refuse a norm radius 1.05 NORM_REL and rnd 0.11 x bar, and pass 0.95 NORM_REL with rnd 0.09 x bar)')]


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


# ------------------------------------------------------------------ m3_bar_v11: the D16 prep in pieces (12 vertices, dmaxH 16)
import os
import json
import numpy as np


class PrepCheckpoint(Exception):
    """raised by Prep16 before a step (table start, unit or finish, an E2 or an E2 block) that the job script's budget refuses; .state is
    the prep's progress (D16Ctx.snapshot: the finished norms as exact intervals and the tables' progress), for the piece's hand-off and the
    next piece."""
    def __init__(self, state, why):
        Exception.__init__(self, 'prep checkpoint before %s' % why)
        self.state = state
        self.why = why


def mat_key(M):
    """a digest of an mp.iv matrix by its entries' exact ends."""
    return hashlib.sha256(repr([[x._mpi_ for x in row] for row in M]).encode()).hexdigest()[:32]


def file_sha(path):
    with open(path, 'rb') as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def move_aside(sdir, name, why, log, ctx=None):
    """a leftover state file of a step that a CAP-STOP cut short (it has no hand-off), renamed under a dated name in its folder, never
    deleted and never overwritten (the kernel close, 2026-11-08): the kernel refuses to write a state file whose name exists.
    Counted in ctx.moved when a D16 context is given."""
    src = os.path.join(sdir, name)
    dst = '%s.aside.%s.%d' % (src, time.strftime('%Y%m%dT%H%M%SZ', time.gmtime()), os.getpid())
    if os.path.exists(dst):
        raise ValueError('move_aside: %s exists' % os.path.basename(dst))
    os.rename(src, dst)
    if ctx is not None:
        ctx.moved += 1
    log('MOVED-ASIDE %s -> %s (%s)' % (name, os.path.basename(dst), why))


# ------------------------------------------------------------------ the kernel adapter
# The only lines that name arbeng_ma_v1_4_1's internals: SPoly's fields (l.984-1018), MomTableU's unit tuples, state file names and own
# checks (l.1363-1465, 1546-1639). Everything else uses its interface (DESIGN_ARBENG_MA_v1_4 sect. 6, DESIGN_ARBENG_MA_v1_4_ADD1):
# MomTableU(..., block).start, plan, run_unit, finish, load_view(dir, expected_sha256); E2_plan, E2_block, E2_combine(parts, plan,
# fallback=False), ma_scalar_dump, ma_scalar_load; MomTableView.E2(P, Q, fallback=False) and shadow_max; FALLBACK_REL.
def nterms(P):
    """the number of terms of a kernel polynomial."""
    return len(P.ex)


def poly_key(P):
    """a digest of a kernel polynomial by its exact M-a fields (exponents, mids, both shadows, counts), which determine every E2 on it."""
    h = hashlib.sha256(repr((P.nv,) + tuple(P.ex.shape)).encode())
    for a in (P.ex, P.v.mid, P.v.sa, P.v.sr, P.v.k):
        h.update(np.ascontiguousarray(a).tobytes())
    return h.hexdigest()[:32]


def unit_id(u):
    """a MomTableU unit (k, b0, b1, pairs) as its id: the level and the range [b0, b1) of destination blocks."""
    return 'L%d:%d-%d' % (int(u[0]), int(u[1]), int(u[2]))


def unit_pairs(u):
    """a MomTableU unit's exact candidate pair count (plan's count, before any arithmetic)."""
    return int(u[3])


def table_size(U):
    """the moments of a MomTableU table (all levels): the finish step's work."""
    return sum(len(c) for c in U.codes)


def state_block(sdir):
    """the block size a table was built with, read back from its state-0 hand-off (it also enters H_par)."""
    with open(os.path.join(sdir, 'handoff_state0.json')) as fh:
        return int(json.load(fh)['block'])


def adopt_state0(U, sdir, log, ctx=None):
    """state 0 that an earlier piece wrote but never handed off (it ended in a CAP-STOP): the sha256 of handoff_state0.json after the
    kernel's own checks (_load_Dj: H_par, the code arrays, state0.npz's size and sha256, MA.check); None when the hand-off does not exist,
    a leftover state0.npz then moved aside."""
    hp = os.path.join(sdir, 'handoff_state0.json')
    if not os.path.exists(hp):
        if os.path.exists(os.path.join(sdir, 'state0.npz')):
            move_aside(sdir, 'state0.npz', 'state 0 without its hand-off', log, ctx)
        return None
    U._load_Dj(sdir)
    return file_sha(hp)


def adopt_unit(U, sdir, u, log, ctx=None):
    """a unit that an earlier piece finished but never handed off: the report in its hand-off handoff_unit_k<k>_b<b0>_<b1>.json, after the
    kernel's own checks (_read_handoff: H_par; _read_npz: the unit file's size and sha256) and, for a level's last unit, the level's
    (_load_level; with no level hand-off, a leftover level file is moved aside and the kernel's _assemble finishes the level from its
    verified units); None when the unit's hand-off does not exist, a leftover unit file then moved aside. A hand-off that does not match
    its file or its unit raises ValueError (not a cut-short step: the job script stops)."""
    k, b0, b1 = int(u[0]), int(u[1]), int(u[2])
    tag = 'k%02d_b%05d_%05d' % (k, b0, b1)
    hp = os.path.join(sdir, 'handoff_unit_%s.json' % tag)
    if not os.path.exists(hp):
        if os.path.exists(os.path.join(sdir, 'unit_%s.npz' % tag)):
            move_aside(sdir, 'unit_%s.npz' % tag, 'unit %s without its hand-off' % tag, log, ctx)
        return None
    h = U._read_handoff(hp)
    (name, ent), = h['files'].items()
    if h.get('level') != k or list(h.get('blocks', [])) != [b0, b1] or name != 'unit_%s.npz' % tag:
        raise ValueError('C-ADOPT: %s does not describe unit %s' % (os.path.basename(hp), tag))
    U._read_npz(sdir, name, ent)
    if b1 == U.nblocks(k):
        if not os.path.exists(os.path.join(sdir, 'handoff_level_k%02d.json' % k)):
            if os.path.exists(os.path.join(sdir, 'level_k%02d.npz' % k)):
                move_aside(sdir, 'level_k%02d.npz' % k, 'level %d without its hand-off' % k, log, ctx)
            U._assemble(sdir, k)
        U._load_level(sdir, k)
    return h['report']


def adopt_table(U, sdir, log, ctx=None):
    """a finished table that an earlier piece never handed off: the sha256 of handoff_table.json (load_view then re-checks every moment
    file against it, H_par and the code arrays); None when it does not exist, leftover moment files then moved aside."""
    hp = os.path.join(sdir, 'handoff_table.json')
    if not os.path.exists(hp):
        for d in range(U.D + 1):
            if os.path.exists(os.path.join(sdir, 'mom_k%02d.npz' % d)):
                move_aside(sdir, 'mom_k%02d.npz' % d, 'moments without the table hand-off', log, ctx)
        return None
    return file_sha(hp)
# ------------------------------------------------------------------ end of the kernel adapter


class D16Ctx:
    """what a job script gives Prep16; nothing here is computed by the bar:
    kern16      arbeng_ma_v1_4_1, the layer the job script pins by full sha256 (the prep's own kernel too: Prep16's polynomials are its
                SPoly, which its tables read);
    state_root  the folder of the tables' state directories (one per table, named by its Gram digest and parameters);
    memo_path   the E2 block memo (JSONL, one line per finished block, appended before use; the job script checks the lines its previous
                piece recorded, by sha256, before it builds this context; lines after them come from a piece that ended in a CAP-STOP);
    budget      budget(est, what) -> bool: may a step of about est CPU seconds start now (the job script's piece budget);
    ns_unit     CPU seconds per planned pair of a table unit, ns_e2 per term pair of an E2, ns_fin per moment of a table's finish (the
                kernel validation's rates with the script's margin);
    block       MomTableU's destinations per block, for the whole life of every table (5000 at D16); read back from each table's state-0
                hand-off before any use (a mismatch raises ValueError);
    unit_pairs  the pair budget of a table unit (MomTableU.plan), e2_pairs of an E2 block (E2_plan), e2_min: an E2 of at most this many
                term pairs runs in one call (MomTableView.E2 with fallback=False);
    state       the previous piece's prep state ({} for the first): 'norms' (label -> interval) and 'tables' (name -> progress).
    INFO kept for the job script's lines and hand-off: adopted (state 0, units and finished tables taken from disk), moved (leftover files
    moved aside), memo_hits (E2 blocks read from the memo), steps (budget questions answered yes), e2_rel (the largest relative radius
    of a D16 E2 ball and its step), e2_trips (D16 E2s whose M-a error exceeds the kernel's FALLBACK_REL of the mid: with fallback=False
    they enter the bars as they are), shadow (each loaded table's shadow_max)."""

    def __init__(self, kern16, state_root, memo_path, budget, ns_unit, ns_e2, ns_fin, block, unit_pairs, e2_pairs, e2_min, state=None):
        self.kern16, self.state_root, self.memo_path = kern16, state_root, memo_path
        self.ns_unit, self.ns_e2, self.ns_fin, self.block = ns_unit, ns_e2, ns_fin, int(block)
        self.unit_pairs, self.e2_pairs, self.e2_min = unit_pairs, e2_pairs, e2_min
        self.adopted, self.moved, self.memo_hits, self.steps, self.e2_trips = 0, 0, 0, 0, 0
        self.e2_rel, self.shadow, self.cur = (0.0, '-'), {}, '-'
        self.budget0 = budget
        state = state or {}
        self.norms = dict(state.get('norms', {}))
        self.tables = {k: {'units': dict(v['units']), 'state0': v['state0'], 'handoff': v['handoff']} for k, v in state.get('tables', {}).items()}
        self.memo, self.memo_lines = {}, 0
        if os.path.exists(memo_path):
            with open(memo_path) as fh:
                for ln in fh:
                    d = json.loads(ln)
                    self.memo[d['k']] = d['v']
                    self.memo_lines += 1

    def budget(self, est, what):
        ok = self.budget0(est, what)
        self.steps += 1 if ok else 0
        return ok

    def memo_add(self, key, val):
        """one finished E2 block, appended to the memo file before it is used."""
        with open(self.memo_path, 'a') as fh:
            fh.write(json.dumps({'k': key, 'v': val}, sort_keys=True) + '\n')
        self.memo[key] = val
        self.memo_lines += 1

    def width(self, ball):
        """INFO on one D16 E2 ball (an arb): its relative radius, the largest so far with the step it came from, and whether its M-a error
        exceeds FALLBACK_REL of the mid (a would-be MAFallback)."""
        mid, rad = abs(float(ball.mid())), float(ball.rad())
        rel = rad / mid if mid > 0 else float('inf')
        if rel > self.e2_rel[0]:
            self.e2_rel = (rel, self.cur)
        self.e2_trips += 1 if rel > self.kern16.FALLBACK_REL else 0
        return rel

    def snapshot(self):
        return {'norms': dict(self.norms), 'memo_entries': len(self.memo), 'memo_lines': self.memo_lines,
                'tables': {k: {'units': dict(v['units']), 'state0': v['state0'], 'handoff': v['handoff']} for k, v in self.tables.items()}}


class TableU:
    """the D16 vertex table of one covariance through arbeng_ma_v1_4_1's MomTableU (DESIGN_ARBENG_MA_v1_4 sect. 1-2), with the context's
    block size, in its own state directory: started, built unit by unit in plan order, finished, then loaded read-only by load_view with
    the table hand-off's sha256 (the kernel's C-STATE re-hashes every file and checks H_par) after the block size read back from the
    state-0 hand-off equals the context's. Each step is asked of the budget first, a refusal raising PrepCheckpoint; a unit whose report
    does not read check_ok, or that ends before its last block, stops the run. A step that an earlier piece finished on disk but never
    handed off (that piece ended in a CAP-STOP) is adopted after the kernel's own checks, never recomputed; a leftover file without its
    hand-off is moved aside under a dated name and the step recomputed (adopt_state0, adopt_unit, adopt_table; the kernel never
    overwrites a state file). lp_moment_ma(Q, p) is E2(Q^(p/2), Q^(p/2)) as the M-a ball (bar v10's prep rule): in one call up to
    ctx.e2_min term pairs, else in E2_plan blocks, each memoized (ma_scalar_dump) and combined once by E2_combine with its plan and
    fallback=False."""

    def __init__(self, prep, Gam, n, D, groups, caps, Wi, label):
        ctx = prep.d16
        K16 = ctx.kern16
        self.prep, self.ctx, self.K16, self.label = prep, ctx, K16, label
        self.name = 'u16_%s_%s' % (mat_key(Gam), hashlib.sha256(repr((n, D, groups, caps, Wi)).encode()).hexdigest()[:12])   # not the block: a
        # context with another block meets this table's folder and is refused by the block gate below
        sdir = os.path.join(ctx.state_root, self.name)
        rec = ctx.tables.setdefault(self.name, {'units': {}, 'state0': None, 'handoff': None})
        U = K16.MomTableU(S.arb_mat_of(Gam), n, D, groups=groups, caps=caps, W_int=Wi, W=S.arb_mat_of(Wi), block=ctx.block)
        log = prep.log
        if rec['handoff'] is None:
            if rec['state0'] is None and os.path.isdir(sdir):
                rec['state0'] = adopt_state0(U, sdir, log, ctx)
                if rec['state0'] is not None:
                    ctx.adopted += 1
                    log('TABLE16-ADOPTED %s: state 0 (hand-off %s)' % (label, rec['state0']))
            if rec['state0'] is None:
                if not ctx.budget(60.0, 'the start of table %s' % label):
                    raise PrepCheckpoint(ctx.snapshot(), 'the start of table %s' % label)
                if not os.path.isdir(sdir):
                    os.mkdir(sdir)
                rec['state0'] = U.start(sdir)
                log('TABLE16-START %s: state %s, state0 hand-off %s' % (label, self.name, rec['state0']))
            if state_block(sdir) != ctx.block:
                raise ValueError('table %s: built with block %d, the context asks %d' % (label, state_block(sdir), ctx.block))
            for u in U.plan(sdir, ctx.unit_pairs):
                uid = unit_id(u)
                if uid in rec['units']:
                    continue
                rep = adopt_unit(U, sdir, u, log, ctx)
                if rep is not None:
                    ctx.adopted += 1
                    log('UNIT16-ADOPTED %s %s: %s' % (label, uid, json.dumps(rep, sort_keys=True)))
                else:
                    est = unit_pairs(u) * ctx.ns_unit
                    if not ctx.budget(est, 'table unit %s of %s' % (uid, label)):
                        raise PrepCheckpoint(ctx.snapshot(), 'table unit %s of %s (about %.0f s)' % (uid, label, est))
                    rep = U.run_unit(sdir, u)
                    log('UNIT16 %s %s: %s' % (label, uid, json.dumps(rep, sort_keys=True)))
                if not rep.get('check_ok') or int(rep.get('end', -1)) != int(u[2]):
                    raise ArithmeticError('table %s unit %s: the report does not read check_ok with end %d: %r' % (label, uid, int(u[2]), rep))
                rec['units'][uid] = rep
            hsha = adopt_table(U, sdir, log, ctx)
            if hsha is not None:
                ctx.adopted += 1
                log('TABLE16-ADOPTED %s: finished table (hand-off %s)' % (label, hsha))
            else:
                est = table_size(U) * ctx.ns_fin
                if not ctx.budget(est, 'the finish of table %s' % label):
                    raise PrepCheckpoint(ctx.snapshot(), 'the finish of table %s (about %.0f s)' % (label, est))
                hsha = U.finish(sdir)
            rec['handoff'] = ['handoff_table.json', hsha]
            log('TABLE16-FINISHED %s: hand-off %s %s' % (label, rec['handoff'][0], rec['handoff'][1]))
        if state_block(sdir) != ctx.block:
            raise ValueError('table %s: built with block %d, the context asks %d' % (label, state_block(sdir), ctx.block))
        t0 = time.process_time()
        self.tab = U.load_view(sdir, rec['handoff'][1])
        self.sha = rec['handoff'][1]
        ctx.shadow[label] = float(self.tab.shadow_max())
        log('TABLE16-LOADED %s: %.2f s; shadow_max %.3e' % (label, time.process_time() - t0, ctx.shadow[label]))

    def lp_moment_ma(self, Q, p):
        Pk = Q.power(p // 2)
        return self.e2(Pk, Pk)

    def e2(self, P, Q):
        """E[P Q] on the table as the M-a ball (fallback=False): in one call up to ctx.e2_min term pairs, else block by block, each block
        from the memo or computed (after the budget) and memoized, then combined once by E2_combine with its plan; the ball's relative
        radius is logged and kept (ctx.width)."""
        ctx, K16 = self.ctx, self.K16
        nq = nterms(Q)
        if nterms(P) * nq <= ctx.e2_min:
            est = nterms(P) * nq * ctx.ns_e2
            if not ctx.budget(est, 'an E2 on %s' % self.label):
                raise PrepCheckpoint(ctx.snapshot(), 'an E2 of %d term pairs on %s (about %.0f s)' % (nterms(P) * nq, self.label, est))
            ball = self.tab.E2(P, Q, fallback=False)
            self.prep.log('E2-WIDTH %s %s: %d pairs in one call, relative radius %.3e' % (self.label, ctx.cur, nterms(P) * nq, ctx.width(ball)))
            return ball
        plan = K16.E2_plan(self.tab, P, Q, ctx.e2_pairs)
        base = '%s|%s|%s|%d|%d' % (self.sha, poly_key(P), poly_key(Q), ctx.e2_pairs, len(plan['blocks']))
        parts = []
        for bi, (s, e) in enumerate(plan['blocks']):
            key = '%s|%d' % (base, bi)
            if key in ctx.memo:
                ctx.memo_hits += 1
            else:
                est = (e - s) * nq * ctx.ns_e2
                if not ctx.budget(est, 'an E2 block'):
                    raise PrepCheckpoint(ctx.snapshot(), 'E2 block %d of %d on %s (about %.0f s)' % (bi + 1, len(plan['blocks']), self.label, est))
                t0 = time.process_time()
                part = K16.E2_block(self.tab, P, Q, plan, bi)
                ctx.memo_add(key, K16.ma_scalar_dump(part))
                self.prep.log('E2BLOCK %s %d of %d: %d pairs, %.2f s' % (self.label, bi + 1, len(plan['blocks']), (e - s) * nq, time.process_time() - t0))
            parts.append(K16.ma_scalar_load(ctx.memo[key]))
        ball = K16.E2_combine(parts, plan=plan, fallback=False)
        self.prep.log('E2-WIDTH %s %s: %d pairs in %d blocks, relative radius %.3e' % (self.label, ctx.cur, plan['pairs'], len(plan['blocks']),
                                                                                      ctx.width(ball)))
        return ball


class Prep16(Prep):
    """Prep at dmaxH 16 for a 12-vertex graph, resumable across pieces (m3_bar_v11), on arbeng_ma_v1_4_1 (kern must be d16.kern16, so the
    polynomials are that kernel's SPoly, which its tables read). The always-part is Prep's. Stage u and stage c run v10's norms in v10's
    order as labelled steps: a step that d16.norms holds from an earlier piece is taken from there, and every finished step is recorded
    there at once, so a resumed piece builds neither the polynomials nor the tables of finished steps. Every prep norm on the vertex forms
    uses the covariance's D16 vertex table on all V vertex forms (TableU, built on first need; one D16 table resident at a time), never a
    smaller table on a sub-support; norms above dmaxH 16 take v10's Hoelder fallback (ex, h2 p6). A refused step raises PrepCheckpoint
    with d16.snapshot(). The arithmetic of every norm, part and scalar is v10's stage_u and stage_c."""

    def __init__(self, kern, g, J, avec, ap, theta0, qcap, d16, log=None, stages=('u', 'c'), scalars=None):
        if kern is not d16.kern16:
            raise ValueError('Prep16: the prep kernel must be the D16 context\'s kernel (its tables read only its own SPoly)')
        self.d16 = d16
        self.tables16 = {}
        self.lazy_ = {}
        Prep.__init__(self, kern, g, J, avec, ap, theta0, qcap, log=log, dmaxH=16, stages=(), scalars=scalars)
        if not self.ok:
            return
        if 'u' in stages:
            self.stage_u16()
        if 'c' in stages:
            self.stage_c16()

    def lazy(self, name, fn):
        """a polynomial built once, on first need: only pending steps ask for their majorants and products."""
        if name not in self.lazy_:
            self.lazy_[name] = fn()
        return self.lazy_[name]

    def h(self, k):
        mj = self.lazy('mj5', lambda: Majorants(self.kern, Model(self.kern, self.g, 5, []), self.a_v, self.t))
        return self.lazy('h%d' % k, lambda: mj.hbar(k))

    def hh16(self):
        return self.lazy('hh', lambda: hhat2(self.kern, self.g, self.a_v, self.t, self.h(2)))

    def h2sq(self):
        return self.lazy('h2sq', lambda: self.h(2).mul(self.h(2)))

    def table16(self, which):
        """the D16 vertex table of the covariance 'u' or 'c' (TableU); a table of the other covariance is released first."""
        key = ('d16', which)
        if key not in self.tables16:
            self.tables16.clear()
            V = self.g.V
            Gam, Wi, gr = self.g.restrict(self.cov(which), list(range(V)))
            t0 = time.process_time()
            self.tables16[key] = TableU(self, Gam, self.g.n, 16, None, None, Wi, '%s vertex forms D 16' % which)
            self.log('TABLE16 %s vertex forms D 16: %.2f s (hand-off %s)' % (which, time.process_time() - t0, self.tables16[key].sha[:8]))
        return self.tables16[key]

    def lp_norm(self, P, which, p, dmax=64, prep=False):
        """v10's lp_norm; a prep norm (prep=True) of a polynomial in the vertex forms takes the covariance's D16 vertex table on all V
        vertex forms (P restricted to them); a pair form in a prep norm is refused."""
        if not prep:
            return Prep.lp_norm(self, P, which, p, dmax, prep)
        if is_zero(P):
            return iv.mpf(0)
        idx = support(P)
        if not idx:
            return abs(S.isum(S.spoly_iv(P).values()))
        V = self.g.V
        if idx[-1] >= V:
            raise ValueError('a D16 prep norm in a pair form (support %s)' % idx)
        Q = restrict(self.kern, P, list(range(V)))
        D = 2 * deg(Q) * (p // 2)
        if D > dmax:
            return None
        mom = S.arb_to_iv(self.table16(which).lp_moment_ma(Q, p))
        v = S.root(mom, p)
        self.track(v)
        return v

    def norm16(self, label, which, p, fn):
        """one labelled prep step: from d16.norms if an earlier piece finished it, else norm_any(fn(), which, p), recorded at once."""
        key = '%s:%s' % (which, label)
        if key in self.d16.norms:
            return self.d16.norms[key]
        t0 = time.process_time()
        self.d16.cur = key
        v = self.norm_any(fn(), which, p)
        self.d16.norms[key] = v
        self.log('NORM16 %s p %d: %.2f s' % (key, p, time.process_time() - t0))
        return v

    def stage_u16(self):
        """v10's stage_u, step by step (the same norms, parts and order; the vertex table on first need)."""
        t, H = self.t, self.H
        H1, H2, H3, H4, H1sq = H[1], H[2], H[3], H[4], self.H1sq
        T = lambda k: S.ipow(t, k)
        N2 = lambda lab, fn: self.norm16(lab, 'u', 2, fn)
        ex = T(6) / 48 * N2('ex', lambda: self.h2sq().mul(self.h(2)))
        rp = {'t4|H4|': T(4) * N2('t4|H4|', lambda: H4), 't5 h5/120': T(5) / 120 * N2('t5 h5', lambda: self.h(5)),
              't4 H2^2/2': T(4) / 2 * N2('t4 H2^2', lambda: H2.mul(H2)),
              't6 h3^2/72': T(6) / 72 * N2('t6 h3^2', lambda: self.h(3).mul(self.h(3))),
              't4|H1H3|': T(4) * N2('t4|H1H3|', lambda: H1.mul(H3)),
              't5|H1H4|': T(5) * N2('t5|H1H4|', lambda: H1.mul(H4)),
              't6|H1|h5/120': T(6) / 120 * N2('t6|H1|h5', lambda: H1.mul(self.h(5))),
              't5|H2|h3/6': T(5) / 6 * N2('t5|H2|h3', lambda: H2.mul(self.h(3))),
              't4 H1^2|H2|/2': T(4) / 2 * N2('t4 H1^2|H2|', lambda: H1sq.mul(H2)),
              't5 H1^2 h3/12': T(5) / 12 * N2('t5 H1^2 h3', lambda: H1sq.mul(self.h(3))),
              't5|H1|h2^2/8': T(5) / 8 * N2('t5|H1|h2^2', lambda: H1.mul(self.h2sq()))}
        tr = T(5) / 24 * N2('tr', lambda: self.h2sq().mul(self.hh16()))
        rp['E2^3 term'] = iv.mpf([iv.mpf(0), ex.b if ex.b < tr.b else tr.b])
        self.rE_parts = rp
        self.rE = S.isum(rp.values())
        self.nE = [iv.mpf(1)] + [N2('nE%d' % j, (lambda j=j: self.Ej[j])) for j in (1, 2, 3)]
        self.nE4 = [iv.mpf(1)]
        for j in (1, 2, 3):
            if 4 * deg(self.Ej[j]) <= self.dmaxH:
                self.nE4.append(self.norm16('nE4_%d' % j, 'u', 4, (lambda j=j: self.Ej[j])))
            else:
                self.nE4.append(S.ipow(iv.mpf(3), deg(self.Ej[j])) * self.nE[j])
        self.tables16.pop(('d16', 'u'), None)

    def stage_c16(self):
        """v10's stage_c, step by step (h2 p6 above dmaxH takes the Hoelder fallback; the c vertex table on first need)."""
        g, t, T = self.g, self.t, (lambda k: S.ipow(self.t, k))
        H1 = self.H1
        nh2_6 = self.norm16('h2 p6', 'c', 6, lambda: self.h(2))
        self.nC6 = t * self.norm16('H1 p6', 'c', 6, lambda: H1) + T(2) / 2 * nh2_6
        self.nC8 = t * (self.norm16('H1 p8', 'c', 8, lambda: H1) + self.norm16('hh p8', 'c', 8, lambda: self.hh16()))
        n_ = g.n
        self.Pout = S.isum(S.chi_tail_up(self.J * S.I(a) / gv, n_) for a, gv in zip(self.a_v, g.Gvv))
        self.Pout_p = S.isum(S.chi_tail_up(self.J * S.I(a) / gv, n_) for a, gv in zip(self.a_v, self.tilt_p['Gvv']))
        self.tree = g.tree()
        self.farbase = S.far_base(self.J, S.I(self.theta0), S.I(self.ap), g.Gvv, self.tree, g.N, g.V, g.log_tau)
        self.alpha_lo = min((S.I(self.theta0) * S.I(self.ap) / (2 * gv)).a for gv in g.Gvv)
        self.tables16.pop(('d16', 'c'), None)
