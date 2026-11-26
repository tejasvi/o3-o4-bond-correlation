# Wave 18, N = 3 [3, 20] cover: o3cert6 = certint6 (the matrix-free certint5, UNIF 9.25-9.29) on the O(3) column map, with
# the N = 3 model parts of o3cert2 (RV21_43; UNIF 9.20-9.21): signed factors (code8/o3mfstruct.py: the o3struct formulas,
# A1 = bottom bond q, A2 = top bond p), the weights W_l = i_l(J) (o3lib3.bessel_derivs), the multiplicities 2l+1 in the
# character-sum tails, the boundary vector b = sqrtC W_t W_bb g(t,h,bb) (signed), the sign of phi_0 from its |000> component,
# and the truncation constants of o3cert2.  New for N = 3 (UNIF 9.30, for review): (T1) vertical labels up to 2L, (T2) |Q b|
# over admissible cut states, the triangle-rule kappa_Q, the Combes-Thomas bound with RV21_44 MINOR-2 (class CT), the
# MINOR-3 scan, and the v2 error model of lam5frob for signed factors.
# certint6 header:
# Wave 18, [3, 20] label certifier, checkpoint 1 (UNIF 9.24): certint6 = matrix-free certint5 (v2.1, UNIF 9.21).
# The certificate logic (C1)-(C7), the Taylor models, the truncation terms and the adaptive cover are those of certint5;
# the dense pieces are replaced:
#  - transfer products through the exact sparse factors (code8/mfstruct.py) in MR arithmetic (code8/mfops.py, the shift
#    kap split over the five weight factors).  The vector Taylor-model product uses the point operators (orders 0-2), the
#    interval operator of order 3 on the polynomial range (integral remainder: for every y, int (t-s)^2/2 X'''(s) y ds
#    lies in t^3/6 times the convex box enclosing X'''(J) y over I) and the interval operator of order 0 on the remainder;
#  - eigenpairs at J0 by Lanczos (scipy eigsh, random start: a flip-symmetric start would miss the odd sector) on the
#    float centre operator, enclosed by rigorous residuals |S q - mu q|/|q| (S exact and symmetric);
#  - the moving frame from the Rayleigh-Schroedinger equations: explicit terms for the computed Ritz pairs plus CG on
#    their complement (any smooth frame is admissible: every residual is rigorous);
#  - row sums of |T2| + h |T3| and of |X~| over I from the operators applied to the unit box (symmetric matrices).
#  - the boundary vector shifted like the transfer, b~ = b e^{-kb (J - J0)} (class data are invariant under positive
#    J-dependent factors; |Q b~| <= e^{|kb| h} |Q b|); the interval operators use the mean-value boxes of the shifted
#    factors (mfops mvbox, UNIF 9.25).
# lambda_5 over I (argv 6): frob (default) = the Eckart-Young bound of UNIF 9.26 (code8/lam5frob.py, PENDING REVIEW);
# ph = the checkpoint-1 PLACEHOLDERS (NOT rigorous):
#  - lambda_5 at J0 = the upper end of the fifth Ritz enclosure (assumes Lanczos found the top five eigenvalues);
#  - |Qc T1 Qc| = 1.25 x a float Lanczos estimate.
# Truncation modes (argv 5): op = certint5's reviewed constants (UNIF 9.14, 9.17, 9.21); tri = the triangle rule in
# kappa_Q; vec = triangle rule + the Combes-Thomas vector bound beta(x) in the first-order uses (UNIF 9.24 (4)).
# tri and vec also keep every vertical label of a cut state (vmax = 2L: S = P T P exactly, no vertical tail eps_v, dTX,
# dTXY) and sum |Q b|, |R Q b| over admissible cut states (UNIF 9.25).
# tri and vec are PENDING REVIEW; every verdict line carries the placeholder and truncation tags.
# usage: o3cert6.py TAG L I J0:h[,J0:h,...] | adapt:JS:JE:q:qmax  [op|tri|vec] [frob|ph]
import os, sys, time, math
from fractions import Fraction
import numpy as np
import scipy.sparse.linalg as sla
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(1, os.path.join(os.path.dirname(HERE), 'code4'))
from flint import arb, ctx
import certlib3
from tm2 import TM2, fdn, fup
import o3mfstruct as mfstruct, mfops, lam5frob          # N = 3 factors (o3struct formulas, signed)
import o3mfstruct as o3mf
sys.path.insert(2, os.path.join(os.path.dirname(HERE), 'code5'))
import o3lib3
from mfops import MR, dmul, mr_from_iv, iv_from_arb
tag, L, I = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
TRUNC = sys.argv[5] if len(sys.argv) > 5 else 'op'
assert TRUNC in ('op', 'tri', 'vec')
LAM5 = sys.argv[6] if len(sys.argv) > 6 else 'frob'        # frob = UNIF 9.26 (PENDING REVIEW); ph = checkpoint-1 placeholders
assert LAM5 in ('frob', 'ph')
ADAPT = None
if sys.argv[4].startswith('adapt:'):
    ADAPT = tuple(float(x) for x in sys.argv[4].split(':')[1:])
    ivals = []
else:
    ivals = [(Fraction(x.split(':')[0]), float(x.split(':')[1])) for x in sys.argv[4].split(',')]
ctx.prec = 128
BASE = os.path.dirname(HERE)
OUT = os.path.join(BASE, 'out', 'o3cert6_%s.txt' % tag)
assert '/data/e17/unif/scratch/out/' in OUT and not os.path.exists(OUT)
lines = []
def say(s):
    print(s, flush=True); lines.append(s)
    open(OUT, 'w').write('\n'.join(lines) + '\n')
U64 = 2.0 ** -53
SQ2 = math.sqrt(2) * (1 + 1e-15)
INF = 1 + 1e-12                 # inflation of float-computed radii
KEV, NCV = 6, 24
PTAG = {'frob': 'lam5=frob[9.26,RV11_25;v2err,9.30]', 'ph': 'PLACEHOLDER(lam5,QcT1Qc)'}[LAM5]
TTAG = {'op': 'N3:trunc=op[o3cert2,RV21_43]', 'tri': 'N3:trunc=tri[9.30]', 'vec': 'N3:trunc=vec[9.24+MINOR-2,9.27,9.30]'}[TRUNC]
t00 = time.time()
st = mfstruct.build(L, verbose=False, vmax=(L if TRUNC == "op" else 2 * L))
n = L + 1; nS = st['nS']
adm = st['adm']; aidx = np.nonzero(adm)[0]; nA = len(aidx)
fl = (st['bb'] * n + st['h']) * n + st['t']          # flip (t, h, bb) -> (bb, h, t)
labs = {'t': st['t'], 'h': st['h'], 'bb': st['bb']}
say('o3cert6 %s: L=%d Lv=%d I=%d; %d states (cube %d), tuples %d + %d, CSR nnz %d + %d; structure %.1fs; %s'
    % (tag, L, st["Lv"], I, nA, nS, st['ntup'][0], st['ntup'][1], st['A1'].nnz, st['A2'].nnz, time.time() - t00, TTAG))
NPROD = [0]                     # sparse MR factor products (each = 3 CSR matvecs)
_mv = mfops.SpMR.mv
def _mv_count(self, x):
    NPROD[0] += 1
    return _mv(self, x)
mfops.SpMR.mv = _mv_count
OPS = {}

# ---------------- MR helpers (certint5) ----------------
def zero_mr(m):
    return MR(np.zeros(m), np.zeros(m))
def mdot(u, v):
    """<u, v> for MR vectors: arb ball."""
    au = np.abs(u.c)
    c = float(u.c @ v.c)
    r = float(au @ v.r + u.r @ (np.abs(v.c) + v.r)) + (len(u.c) + 2) * U64 * float(au @ np.abs(v.c))
    return arb(c, r * INF + 1e-300)
def cr(x):
    """float centre and radius of an arb ball"""
    c = float(x.mid())
    return c, fup(abs(x - c))
def bscale(M, x):
    """MR vector times the arb ball x"""
    c, r = cr(x)
    cc = M.c * c
    return MR(cc, (M.r * (abs(c) + r) + r * np.abs(M.c)) * INF + 4 * U64 * np.abs(cc) + 1e-300)
def tball(v, s):
    """v times an unknown t-dependent factor in [-s, s]"""
    return MR(np.zeros_like(v.c), s * v.absup() * INF)

# ---------------- vector Taylor models of order 2: v(t) = c0 + c1 t + c2 t^2 + t^3 R(t), R(t) in the MR box R --------
class VT:
    __slots__ = ('c0', 'c1', 'c2', 'R')
    def __init__(self, c0, c1, c2, R):
        self.c0, self.c1, self.c2, self.R = c0, c1, c2, R
    def __add__(self, o):
        return VT(self.c0 + o.c0, self.c1 + o.c1, self.c2 + o.c2, self.R + o.R)
    def __sub__(self, o):
        return VT(self.c0 - o.c0, self.c1 - o.c1, self.c2 - o.c2, self.R - o.R)
def vt_prange(v, h):
    return MR(v.c0.c, (v.c0.r + h * v.c1.absup() + h * h * v.c2.absup()) * INF)
def vt_range(v, h):
    p = vt_prange(v, h)
    return MR(p.c, (p.r + h ** 3 * v.R.absup()) * INF)
def vt_smul(s, v, h):
    """scalar TM2 s times VT v"""
    c0 = bscale(v.c0, s.a0)
    c1 = bscale(v.c1, s.a0) + bscale(v.c0, s.a1)
    c2 = bscale(v.c2, s.a0) + bscale(v.c1, s.a1) + bscale(v.c0, s.a2)
    R = bscale(v.c2, s.a1) + bscale(v.c1, s.a2) + bscale(v.c2, s.a2 * s.T) + bscale(vt_range(v, h), s.R) + bscale(v.R, s.prange())
    return VT(c0, c1, c2, R)
def mtm_prange(M0, M1, M2, h):
    return MR(M0.c, (M0.r + h * M1.absup() + h * h * M2.absup()) * INF)
def vt_dm(Dt, v, h):
    """diagonal Taylor model Dt = (d0, d1, d2, d3, dpr) times VT v"""
    d0, d1, d2, d3, dpr = Dt
    c0 = dmul(d0, v.c0)
    c1 = dmul(d0, v.c1) + dmul(d1, v.c0)
    c2 = dmul(d0, v.c2) + dmul(d1, v.c1) + dmul(d2, v.c0)
    R = dmul(d1, v.c2) + dmul(d2, v.c1) + tball(dmul(d2, v.c2), h) + dmul(d3, vt_range(v, h)) + dmul(dpr, v.R)
    return VT(c0, c1, c2, R)
def vt_dot(u, v, h):
    a0 = mdot(u.c0, v.c0)
    a1 = mdot(u.c0, v.c1) + mdot(u.c1, v.c0)
    a2 = mdot(u.c0, v.c2) + mdot(u.c1, v.c1) + mdot(u.c2, v.c0)
    R = mdot(u.c1, v.c2) + mdot(u.c2, v.c1) + arb(0, h) * mdot(u.c2, v.c2) + mdot(u.R, vt_range(v, h)) + mdot(vt_prange(u, h), v.R)
    return TM2(a0, a1, a2, R, h)
def vt_norm(v, h):
    return math.sqrt(max(vt_dot(v, v, h).upper(), 0.0)) * INF
TMV = [0, 0.0]                  # matrix-free Taylor-model products: count (per kind), seconds
DBG = [] if os.environ.get("C6DEBUG") else None
def vt_mv(kinds, v, h):
    """matrix-free X~(t) v(t) for X in kinds (one kind: VT; a tuple: dict), X~(J0 + t) = X(J0 + t) e^{-kap t}/lam0:
    T0, T1, T2 = (point derivatives of orders 0, 1, 2 of the shifted, scaled operator) / (1, 1, 2), T3(t) y in the order-3
    interval box / 6 for y in the polynomial range, X~(t) R(t) in the mean-value order-0 box (mfops apply0); A1 products are shared"""
    t0 = time.time()
    PT, BL = OPS['PT'], OPS['BL']
    single = isinstance(kinds, str)
    kl = [kinds] if single else list(kinds)
    cs = [{}, {}, {}, {}, {}]
    pr = vt_prange(v, h)
    hasR = bool(np.any(v.R.c) or np.any(v.R.r))
    out = {}
    for kd in kl:
        a0 = PT.apply(v.c0, kd, (0, 1, 2), cs[0]); a1 = PT.apply(v.c1, kd, (0, 1, 2), cs[1]); a2 = PT.apply(v.c2, kd, (0, 1, 2), cs[2])
        for a in (a0, a1, a2):
            a[2] = a[2].scale(0.5)
        a3 = BL.apply(pr, kd, (3,), cs[4])[3].scale(1.0 / 6.0)
        R = a2[1] + a1[2] + tball(a2[2], h) + a3
        if DBG is not None:
            nn = lambda m: float(np.linalg.norm(m.absup()))
            DBG.append((kd, nn(a0[0]), nn(a2[1] + a1[2]), nn(tball(a2[2], h)), nn(a3), nn(BL.apply0(v.R, kd)) if hasR else 0.0, nn(v.R), nn(v.c1), nn(v.c2)))
        if hasR:
            R = R + BL.apply0(v.R, kd)
        out[kd] = VT(a0[0], a1[0] + a0[1], a2[0] + a1[1] + a0[2], R)
    TMV[0] += len(kl); TMV[1] += time.time() - t0
    return out[kinds] if single else out

# ---------------- truncation constants (certint5 point_fast, scalar part) and the 9.24 vector bound ----------------
def trunc_consts(J0f, h):
    """N = 3 truncation constants: o3cert2 (RV21_43) with the RV21_44 MINOR-3 scan, (T1) and (T2) for N = 3 (UNIF 9.30)"""
    Ja = arb(J0f) + arb(h)                    # exact top of the interval (the constants increase with J)
    Jl = arb(J0f) - arb(h)
    half = arb(1) / 2
    def iks(J, m0, m1):                       # i_l(J) = sqrt(pi/2J) I_{l+1/2}(J), l = m0..m1-1
        pre = (arb.pi() / (2 * J)).sqrt()
        return [pre * J.bessel_i(arb(l) + half) for l in range(m0, m1)]
    ks = iks(Ja, 0, L + 61)
    k0 = ks[0]
    # character-sum tails (o3cert2): explicit terms a = L+1..AE, AE = L+59, plus the geometric remainder; ratio bounds
    #   i_{a+1}/i_a = I_{a+3/2}/I_{a+1/2} <= J/(2a+2) <= kr (Amos, nu = a + 1/2);  (2a+3)/(2a+1) <= m2;  rq as N = 4
    AE = L + 59
    kr = Ja / (2 * AE + 2); m2 = arb(2 * AE + 3) / (2 * AE + 1); rq = (arb(AE + 1) / AE) ** 2
    def gtail(terms, q):
        if not (q.upper() < 1):
            raise ValueError('tail ratio bound >= 1')
        return sum(terms, arb(0)) + terms[-1] * q / (1 - q)
    # vertical-bond tail: e^{J s.t} - f_L(s.t) = sum_{a > L} i_a (2a + 1) P_a(s.t), |P_a| <= 1
    tail = gtail([(2 * a_ + 1) * ks[a_] for a_ in range(L + 1, AE + 1)], m2 * kr)
    eps_v = fup(abs(k0 ** 3 * tail * (2 * Ja.exp() + tail)))
    tail1 = gtail([(2 * a_ + 1) * ks[a_] * (a_ / Jl + 1) for a_ in range(L + 1, AE + 1)], m2 * kr * (AE + 1) / AE)
    eJ = Ja.exp()
    d0 = tail * (2 * eJ + tail); d1 = tail1 * (eJ + tail) + eJ * tail; d2 = tail1 * (eJ + tail1) + eJ * tail1
    dTX = fup(abs(k0 ** 3 * (d0 + d1))); dTXY = fup(abs(k0 ** 3 * (d0 + d2)))
    # boundary vector on labels > L (o3cert2): b(a,b,c)^2 = W_a^3 W_b W_c^3 (2a+1)(2b+1)(2c+1) (a b c; 000)^2 with
    # sum_b (2b+1) (a b c; 000)^2 = 1: |Q b|^2 <= W_0 (F_tot^2 - F_L^2) + W_{L+1} F_L^2, F = sum (2l+1) W_l^3
    rr = [(arb(l) / Jl + 1) ** 2 for l in range(L + 61)]
    def sums(wf, q, cut=L, ae=AE):
        lo_ = sum((wf(l) for l in range(cut + 1)), arb(0)); tl_ = gtail([wf(l) for l in range(cut + 1, ae + 1)], q)
        return lo_, tl_
    F = sums(lambda l: (2 * l + 1) * ks[l] ** 3, m2 * kr ** 3)
    Qb = fup((k0 * F[1] * (2 * F[0] + F[1]) + ks[L + 1] * F[0] * F[0]).sqrt())
    # n5 as corrected by RV21_44 MINOR-3: the ratio bound ((l+1+J)/l)^2 J/(2l+2) for r(l)^2 i_l and rr(l) i_l is applied
    # only beyond AE; below AE the maxima are explicit (m_all, m_Q here, r_Q below)
    q_r5 = ((arb(AE + 1) + Ja) / AE) ** 2 * Ja / (2 * AE + 2)
    if not (q_r5.upper() < 1):
        raise ValueError('r(l)^2 i_l not shown decreasing above AE')
    Fr = sums(lambda l: rr[l] * (2 * l + 1) * ks[l] ** 3, rq * m2 * kr ** 3)
    m_all = arb(max(fup(abs(rr[l] * ks[l])) for l in range(AE + 1)))
    m_Q = arb(max(fup(abs(rr[l] * ks[l])) for l in range(L + 1, AE + 1)))
    RQb = fup((2 * k0 * (Fr[1] * (F[0] + F[1]) + Fr[0] * F[1]) + m_all * F[1] * (2 * F[0] + F[1]) + 2 * ks[L + 1] * Fr[0] * F[0] + m_Q * F[0] * F[0]).sqrt())
    Qb_op, RQb_op = Qb, RQb
    if st['Lv'] >= 2 * L:
        # (T1) for N = 3: every vertical label of a cut state is kept (q <= c + c' <= 2L, p <= a + a' <= 2L): S = P T P
        eps_v = dTX = dTXY = 0.0
    if TRUNC != 'op':
        # (T2) for N = 3 (UNIF 9.30): |Q b|^2, |R Q b|^2 summed over ADMISSIBLE cut states with L < max <= ME (float, outward
        # per-label bounds, exact g rounded once), plus the o3cert2 bounds with the cut ME beyond
        ME = L + 30; AEx = ME + 59
        ksx = ks + iks(Ja, len(ks), AEx + 1)
        Gm = o3mf.gtable(ME + 1)
        lab = np.arange(ME + 1)
        ku = np.array([fup(ksx[l]) for l in range(ME + 1)])
        rbu = np.array([fup(arb(l) / Jl + 1) for l in range(ME + 1)])
        T_, H_, B_ = np.meshgrid(lab, lab, lab, indexing='ij')
        msk = ((T_ + H_ + B_) % 2 == 0) & (np.abs(T_ - H_) <= B_) & (B_ <= T_ + H_) & (np.maximum(np.maximum(T_, H_), B_) > L)
        b2 = (ku[T_] ** 3 * ku[H_] * ku[B_] ** 3 * Gm[T_, H_, B_] ** 2)[msk]
        rw = (rbu[T_] ** 2 + rbu[H_] ** 2 + rbu[B_] ** 2)[msk]
        nm_ = int(msk.sum())
        s0 = float(np.sum(b2)) * (1 + (nm_ + 24) * U64) * (1 + 1e-12)
        s1 = float(np.sum(rw * b2)) * (1 + (nm_ + 32) * U64) * (1 + 1e-12)
        krx = Ja / (2 * AEx + 2); m2x = arb(2 * AEx + 3) / (2 * AEx + 1); rqx = (arb(AEx + 1) / AEx) ** 2
        if not (((arb(AEx + 1) + Ja) / AEx) ** 2 * Ja / (2 * AEx + 2)).upper() < 1:
            raise ValueError('rr(l) i_l not shown decreasing above AEx')
        rrx = [(arb(l) / Jl + 1) ** 2 for l in range(AEx + 1)]
        Fx = sums(lambda l: (2 * l + 1) * ksx[l] ** 3, m2x * krx ** 3, ME, AEx)
        Frx = sums(lambda l: rrx[l] * (2 * l + 1) * ksx[l] ** 3, rqx * m2x * krx ** 3, ME, AEx)
        m_allx = arb(max(fup(abs(rrx[l] * ksx[l])) for l in range(AEx + 1)))
        m_Qx = arb(max(fup(abs(rrx[l] * ksx[l])) for l in range(ME + 1, AEx + 1)))
        Qb = fup((arb(s0) + k0 * Fx[1] * (2 * Fx[0] + Fx[1]) + ksx[ME + 1] * Fx[0] * Fx[0]).sqrt())
        RQb = fup((arb(s1) + 2 * k0 * (Frx[1] * (Fx[0] + Fx[1]) + Frx[0] * Fx[1]) + m_allx * Fx[1] * (2 * Fx[0] + Fx[1])
                   + 2 * ksx[ME + 1] * Frx[0] * Fx[0] + m_Qx * Fx[0] * Fx[0]).sqrt())
    # kappa_Q = sup over the cut states of i_t i_h i_bb: op (o3cert2) i_{L+1} i_0^2; triangle rule (9.24 (1), RV21_44 for N = 3)
    kapQ_op = ks[L + 1] * k0 ** 2
    kmax = max(fup(ks[a] * ks[L + 1 - a]) for a in range(L + 2))
    kapQ_tri = ks[L + 1] * arb(kmax)
    kapQ = kapQ_op if TRUNC == 'op' else kapQ_tri
    tau_inf = fup(abs((2 * Ja).exp() * kapQ)); cQ = fup(abs((2 * Ja).exp() * (k0 ** 3 * kapQ).sqrt()))
    cQ_op = fup(abs((2 * Ja).exp() * (k0 ** 3 * kapQ_op).sqrt())); cQ_tri = fup(abs((2 * Ja).exp() * (k0 ** 3 * kapQ_tri).sqrt()))
    Jb = arb(J0f, h)
    # r_Q (RV21_44 MINOR-3, 9.27), with the N = 3 weights
    BD = o3lib3.bessel_derivs(Jb, AE)
    rL1 = fup(BD['r'][L + 1])
    kL1lo = fdn(BD['k'][L + 1])
    rQ = max([rL1] + [fup(BD['r'][l] * (BD['k'][l] / kL1lo).sqrt()) for l in range(L + 2, AE + 1)])
    return dict(eps_v=eps_v, tau_inf=tau_inf, cQ=cQ, cQ_op=cQ_op, cQ_tri=cQ_tri, kapQ=fup(abs(kapQ)), tailexp=fup(abs(tail)), rL1=rL1, rQ=rQ,
                dTX=dTX, dTXY=dTXY, Qb=Qb, RQb=RQb, Qb_op=Qb_op, RQb_op=RQb_op, q_r5=fup(q_r5), kapQ_tri=kapQ_tri, ks=ks, Ja=Ja)


class CT:
    """N = 3 Combes-Thomas vector bound (UNIF 9.24 (2) with RV21_44 MINOR-2, UNIF 9.30): for x on the labels <= L and d >= 0,
    |Q T x| <= G_Q(d) M(d) |e^{d Psi} K^{1/2} x|, Psi = t + h + bb, K = i_t i_h i_bb, G_Q(d) = e^{-2 d (L+1)} kappa_Q^tri^{1/2},
    M(0) = e^{2J} (|V| <= e^{2J}) and, for d > 0, M(d) = Lambda0(d)^2/(1 - e^{-2d}) with Lambda0(d) = sum_p (2p+1) i_p e^{2dp}:
    V = sum_{p,q} i_p i_q (2p+1)(2q+1) V_pq with |V_pq| <= 1 (|P_p| <= 1), the label change |Delta Psi| <= 2(p+q) is even
    in the parity-even sector, and a band component has norm <= the norm of the operator, so
    |e^{d Psi} V_pq e^{-d Psi}| <= sum_{even |d'| <= 2(p+q)} e^{d d'} <= e^{2d(p+q)}/(1 - e^{-2d}).  All i at the top of the
    interval; d chosen per vector by a float grid search, evaluated rigorously only at the chosen value."""
    def __init__(self, TC, J0f):
        self.ks, self.Ja = TC['ks'], TC['Ja']
        self.PE = len(self.ks) - 1
        self.kapt = TC['kapQ_tri']
        self.kf = np.array([float(x.mid()) for x in self.ks])
        self.lab = np.arange(L + 1)
        PE = self.PE; Jt = float(self.Ja.upper())
        dtail = 0.5 * math.log(0.9 * (2 * PE + 2) / Jt * (2 * PE + 1) / (2 * PE + 3))
        self.grid = np.linspace(0.0, max(0.01, min(2.5 * (L + 1) / (5.25 * J0f), dtail)), 41)
        p = np.arange(self.PE + 1)
        self.logM = np.array([2 * Jt if d == 0.0 else 2 * math.log(float(np.sum((2 * p + 1) * self.kf * np.exp(2 * d * p)))) - math.log(-math.expm1(-2 * d)) for d in self.grid])
        self.sqk = np.sqrt(self.kf[:L + 1])
    def wnorm_f(self, xabs, d):
        g = self.sqk * np.exp(d * self.lab)
        v = g[st['t']] * g[st['h']] * g[st['bb']] * xabs
        return float(np.sqrt(np.sum(v * v)))
    def wnorm_up(self, xabs, d):
        g = np.array([fup(self.ks[l].sqrt() * (arb(d) * l).exp()) for l in range(L + 1)])
        v = g[st['t']] * g[st['h']] * g[st['bb']] * (1 + 4 * U64) * xabs * (1 + 2 * U64)
        return float(np.sqrt(np.sum(v * v))) * (1 + (len(v) + 8) * U64) * INF
    def M(self, d):
        if d == 0.0:
            return (2 * self.Ja).exp()
        e2 = (2 * arb(d)).exp()
        terms = [(2 * p + 1) * self.ks[p] * e2 ** p for p in range(self.PE + 1)]
        q = arb(2 * self.PE + 3) / (2 * self.PE + 1) * self.Ja / (2 * self.PE + 2) * e2
        if not (q.upper() < 1):
            raise ValueError('CT tail ratio >= 1')
        lam0 = sum(terms, arb(0)) + terms[-1] * q / (1 - q)
        return lam0 * lam0 / (1 - (-2 * arb(d)).exp())
    def beta(self, xabs):
        vals = [-2 * d * (L + 1) + lM + math.log(max(self.wnorm_f(xabs, d), 1e-300)) for d, lM in zip(self.grid, self.logM)]
        i = int(np.argmin(vals)); d = float(self.grid[i])
        con = fup((-2 * arb(d) * (L + 1)).exp() * self.kapt.sqrt() * self.M(d))
        return con * self.wnorm_up(xabs, d) * INF, d

# ---------------- point part at J0: Lanczos + rigorous residual enclosures ----------------
def point_mf(J0f):
    OP = mfops.OpSet(st, arb(J0f), 1, fams=('p',))
    cnt = [0]
    def Sa(xa):
        cnt[0] += 1
        x = np.zeros(nS); x[aidx] = xa
        return OP.apply_c(x, 'S', (0,))[0][aidx]
    lin = sla.LinearOperator((nA, nA), matvec=Sa, dtype=float)
    v0 = np.random.default_rng(12345).standard_normal(nA)
    lam, Qa = sla.eigsh(lin, k=KEV, which='LA', tol=1e-13, v0=v0, ncv=min(NCV, nA - 1))
    o = np.argsort(-lam); lam = lam[o]; Qa = Qa[:, o]
    QA = np.zeros((nS, KEV)); QA[aidx] = Qa
    encl, resn = [], []
    for k in range(KEV):
        q = QA[:, k]
        r = OP.apply(MR(q), 'S', (0,))[0] - MR(q).scale(float(lam[k]))
        rn = float(np.linalg.norm(r.absup())) * (1 + (nS + 4) * U64) * INF
        qn = float(np.linalg.norm(q)) * (1 - (nS + 4) * U64)
        e = rn / qn * INF
        encl.append((float(lam[k]) - e, float(lam[k]) + e)); resn.append(e / float(lam[0]))
    par = [float(QA[fl, k] @ QA[:, k]) for k in range(5)]
    return dict(lam=lam, QA=QA, encl=encl, resn=resn, par=par, OP=OP, nmv=cnt[0])

def interval(J0, h):
    t0 = time.time()
    J0f = float(J0)
    Jlo, Jhi = J0f - h, J0f + h
    NPROD[0] = 0; TMV[0] = 0; TMV[1] = 0.0
    P = point_mf(J0f)
    TC = trunc_consts(J0f, h)
    CTo = CT(TC, J0f)
    teig = time.time() - t0
    lamf = P['lam']; QA = P['QA']
    phic = [QA[:, k].copy() for k in range(4)]
    if phic[0][0] < 0:              # N = 3: the |000> component of the Perron vector is positive (signed basis)
        phic[0] = -phic[0]
    # ---- scaled Taylor models: X(J0 + t) e^{-kap t}/lam0 (eigenvalue ratios, signs and all class data are invariant) ----
    linv = 1.0 / float(lamf[0])
    kap = float(phic[0] @ P['OP'].apply_c(phic[0], 'S', (1,))[1]) * linv
    del P['OP']
    Kb = arb(kap)
    Ee = (-(Kb * arb(0, h))).exp()
    eEup = fup(Ee)
    sc = linv * eEup * INF                       # >= the scale factor linv e^{-kap t} over I
    PT = mfops.OpSet(st, arb(J0f), 2, kap=kap, fac=arb(linv))
    BL = mfops.OpSet(st, arb(J0f, h), 3, kap=kap, mvbox=(J0f, h, arb(linv)))     # tight interval operators (mean-value boxes)
    OPS['PT'], OPS['BL'] = PT, BL
    tasm = time.time() - t0 - teig
    # per-state r data: r, r1, r2 at J0, r3 over I (labels of the rows t, h, bb)
    rl0 = {nm: iv_from_arb(PT.B[nm]) for nm in ('r', 'r1', 'r2')}
    r3I = iv_from_arb(BL.B['r3'])
    def shp3(tau):
        """mean-value sharpening over I: X2(I) in X2(J0) +/- h|X3(I)|, X1(I) in X1(J0) +/- h|X2(I)|, X(I) in X(J0) +/- h|X1(I)|"""
        lb = labs[tau]
        (x0l, x0h), (x1l, x1h), (x2l, x2h) = [(rl0[nm][0][lb], rl0[nm][1][lb]) for nm in ('r', 'r1', 'r2')]
        x3a = np.maximum(np.abs(r3I[0][lb]), np.abs(r3I[1][lb]))
        c2 = 0.5 * (x2l + x2h); r2 = 0.5 * (x2h - x2l) + h * x3a + 2 * U64 * (np.abs(x2l) + np.abs(x2h))
        c1 = 0.5 * (x1l + x1h); r1 = 0.5 * (x1h - x1l) + h * (np.abs(c2) + r2) + 2 * U64 * (np.abs(x1l) + np.abs(x1h))
        c0 = 0.5 * (x0l + x0h); r0 = 0.5 * (x0h - x0l) + h * (np.abs(c1) + r1) + 2 * U64 * (np.abs(x0l) + np.abs(x0h))
        return MR(c0, r0 * INF), MR(c1, r1 * INF), MR(c2, r2 * INF)
    SHr = {tau: shp3(tau) for tau in ('t', 'h', 'bb')}
    # ---- eigen-data over I: second-order moving frame v_k(t) = p_k + t w_k + t^2 w2_k ----
    lt = lamf * linv
    zv = np.zeros(nS); z = zero_mr(nS)
    Qa = QA[aidx, :]
    ncg = [0]
    def T0a(xa):
        x = np.zeros(nS); x[aidx] = xa
        return PT.apply_c(x, 'S', (0,))[0][aidx]
    def rs_solve(k, g):
        """sum_{j != k} phi_j <phi_j, g>/(lt_k - lt_j): computed Ritz pairs explicitly, CG on their complement"""
        ga = g[aidx]
        cf = Qa.T @ ga
        w = np.zeros(nA)
        for j in range(KEV):
            if j != k:
                w += Qa[:, j] * (cf[j] / (lt[k] - lt[j]))
        rhs = ga - Qa @ cf
        def A(xa):
            ncg[0] += 1
            xp = xa - Qa @ (Qa.T @ xa)
            y = lt[k] * xp - T0a(xp)
            return y - Qa @ (Qa.T @ y)
        op = sla.LinearOperator((nA, nA), matvec=A, dtype=float)
        sol, info = sla.cg(op, rhs, rtol=1e-12, atol=0.0, maxiter=3000)
        sol = sol - Qa @ (Qa.T @ sol)
        out = np.zeros(nS); out[aidx] = w + sol
        return out
    VF, ws, rhos, rk_h, r0s, dens, rco = [], [], [], [], [], [], []
    nr = lambda x: float(np.linalg.norm(x.absup())) * INF
    for k in range(4):
        p = phic[k]
        g1 = PT.apply_c(p, 'S', (1,))[1]
        l1 = float(p @ g1)
        w = rs_solve(k, g1); w = w - (p @ w) * p
        g2 = PT.apply_c(w, 'S', (1,))[1] - l1 * w + 0.5 * PT.apply_c(p, 'S', (2,))[2]
        w2 = rs_solve(k, g2); w2 = w2 - (p @ w2) * p
        v = VT(MR(p, zv), MR(w, zv), MR(w2, zv), z)
        Sv = vt_mv('S', v, h)
        num = vt_dot(v, Sv, h); den = vt_dot(v, v, h)
        rho = num * den.inv()
        # residual of mu(t) = c0 + c1 t + c2 t^2 + c3 t^3 (float midpoints of the Rayleigh TM2); |S v - rho v| <= |S v - mu v|
        mu = TM2(float(rho.a0.mid()), float(rho.a1.mid()), float(rho.a2.mid()), float(rho.R.mid()), h)
        r = Sv - vt_smul(mu, v, h)
        r0s.append(nr(r.c0))
        rco.append((nr(r.c0), nr(r.c1), nr(r.c2), nr(r.R)))
        rk_h.append((nr(r.c0) + h * nr(r.c1) + h * h * nr(r.c2) + h ** 3 * nr(r.R)) * INF)
        VF.append(v); ws.append(w); rhos.append(rho); dens.append(den)
    tframe = time.time() - t0 - teig - tasm
    box = MR(np.zeros(nS), adm.astype(float))
    Mrow = {kd: float(np.max(BL.apply0(box, kd).absup())) * INF for kd in ('S', 'TX', 'TY', 'TXY')}   # |X~(J)| over I
    q1norm = q1est = T1row = t2norm = lam5pt = lam5_hi = float('nan')
    if LAM5 == 'ph':
        # checkpoint-1 PLACEHOLDERS (NOT rigorous; comparison runs only).  lam_5 over I by min-max on the complement of
        # p_1..p_4: x^T T0 x <= lam~_5 + lam~_1 sum_k sin^2(p_k, phi_k), x^T T1 x = x^T Qc T1 Qc x, |x^T (T2 + t T3) x| <= rowsum
        Phi = np.array(phic).T
        def QT1Q(xa):
            x = np.zeros(nS); x[aidx] = xa
            x = x - Phi @ (Phi.T @ x)
            y = PT.apply_c(x, 'S', (1,))[1]
            y = y - Phi @ (Phi.T @ y)
            return y[aidx]
        q1est = float(abs(sla.eigsh(sla.LinearOperator((nA, nA), matvec=QT1Q, dtype=float), k=1, which='LM', tol=1e-6,
                                    v0=np.random.default_rng(7).standard_normal(nA), ncv=min(20, nA - 1))[0][0]))
        q1norm = 1.25 * q1est
        T1row = float(np.max(PT.apply(box, 'S', (1,))[1].absup())) * INF
        T2b = PT.apply(box, 'S', (2,))[2].scale(0.5); T3b = BL.apply(box, 'S', (3,))[3].scale(1.0 / 6.0)
        t2norm = float(np.max(T2b.absup() + h * T3b.absup())) * INF
        enc = [(e[0] * linv - abs(e[0] * linv) * 1e-15, e[1] * linv + abs(e[1] * linv) * 1e-15) for e in P['encl']]
        lam5pt = enc[4][1]
        th0 = []
        dist = lambda x, e: max(e[0] - x, x - e[1], 0.0)
        for k in range(4):
            r0c = float(rhos[k].a0.mid())
            dk = min(min(dist(r0c, enc[j]) for j in range(4) if j != k), r0c - lam5pt) - fup(abs(rhos[k].a0 - r0c))
            th0.append(r0s[k] / max(dk, 1e-300) * (1 + 1e-12))
        lam5_hi = lam5pt + enc[0][1] * sum(x * x for x in th0) * INF + h * q1norm + h * h * t2norm
    t5 = time.time()
    cks = []
    for k in range(4):
        ck = rhos[k] * dens[k].inv()
        cks.append((float(ck.a0.mid()), float(ck.a1.mid()), float(ck.a2.mid())))
    L5 = lam5frob.lam5_frob(st, PT, BL, [(VF[k].c0.c, VF[k].c1.c, VF[k].c2.c) for k in range(4)], cks, h)
    t5 = time.time() - t5
    lam5_ph = lam5_hi
    if LAM5 == 'frob':
        lam5_hi = L5['bound']
    say('   lam5 over I (9.26): %.4e = |T_n - F_n|_F %s + err %s + h^n |F_n| (n>=3) %.1e + h^3 |R| (|R| <= %.3e); placeholder %.4e; used %s (%.1fs)'
        % (L5['bound'], ' '.join('%.3e' % x for x in L5['fro']), ' '.join('%.1e' % x for x in L5['err']), sum(h ** n * L5['Fh'][n] for n in range(3, 7)), L5['Rn'], lam5_ph, LAM5, t5))
    say('   residual coefficients (r0, r1, r2, r3) per mode: %s; |Qc T1 Qc| <= %.3e [PLACEHOLDER 1.25 x float %.3e; rigorous unprojected rowsum %.3e]; |T2 + t T3| <= %.3e; Ritz residuals/lam1 %s; lam5/lam1 %.4e [PLACEHOLDER]; eigsh %d matvecs, CG %d'
        % (' ; '.join('%.1e %.1e %.1e %.1e' % c for c in rco), q1norm, q1est, T1row, t2norm, ' '.join('%.1e' % x for x in P['resn']), lam5pt, P['nmv'], ncg[0]))
    gaps = []
    for k in range(4):
        g = float('inf')
        for j in range(4):
            if j != k:
                dlt_kj = rhos[k] - rhos[j]
                sep = min(abs(dlt_kj.lower()), abs(dlt_kj.upper())) if dlt_kj.lower() * dlt_kj.upper() > 0 else 0.0
                g = min(g, sep - rk_h[j] / math.sqrt(max(dens[j].lower(), 1e-300)))
        g = min(g, rhos[k].lower() - rk_h[k] - lam5_hi)
        gaps.append(g)
    disjoint = True
    for k in range(4):
        for j in range(k + 1, 4):
            dlt_kj = rhos[k] - rhos[j]
            sep = min(abs(dlt_kj.lower()), abs(dlt_kj.upper())) if dlt_kj.lower() * dlt_kj.upper() > 0 else 0.0
            disjoint = disjoint and sep > rk_h[k] / math.sqrt(max(dens[k].lower(), 1e-300)) + rk_h[j] / math.sqrt(max(dens[j].lower(), 1e-300))
    if min(gaps) <= 0 or not disjoint:
        say('J0=%s h=%g: gaps not certified (%s; residual intervals disjoint: %s)' % (J0, h, ' '.join('%.3e' % g for g in gaps), disjoint))
        return None
    eps_vs, cQs, taus = TC['eps_v'] * sc, TC['cQ'] * sc, TC['tau_inf'] * sc      # truncation constants, scaled
    # n3: the Schur-complement bounds below need lam_k^S > tau_inf (k = 1..4) and lam_5^S (upper bound) > tau_inf
    if not (min(rhos[k].lower() for k in range(4)) > taus and lam5_hi > taus):
        say('   lam^S not above tau_inf: Schur bounds unavailable'); return None
    lam1S_up = rhos[0].upper() + rk_h[0] ** 2 / (gaps[0] * max(dens[0].lower(), 1e-300))
    cQs = min(cQs, math.sqrt((lam1S_up + eps_vs) * taus) * INF)
    lamT = []
    for k in range(4):
        kt = rk_h[k] ** 2 / (gaps[k] * max(dens[k].lower(), 1e-300))
        trunc = eps_vs + cQs ** 2 / max(rhos[k].lower() - taus, 1e-300)
        lamT.append(rhos[k].addball((kt + trunc) * INF))
    lam5_full = max(lam5_hi + eps_vs + cQs ** 2 / max(lam5_hi - taus, 1e-300), taus)
    conv = lamT[1] + lamT[3] - lamT[2] * 2
    conv_lo = conv.lower()
    l_lo = [lamT[k].lower() for k in range(4)]; l_hi = [lamT[k].upper() for k in range(4)]
    order_ok = (lamT[0] - lamT[1]).lower() > 0 and (lamT[1] - lamT[2]).lower() > 0 and (lamT[2] - lamT[3]).lower() > 0 and l_lo[3] > lam5_full
    # normalizations of the frame vectors v_l(t) (exact polynomials) and the frame Gram deviation
    nrm2 = [dens[l].invsqrt() for l in range(4)]
    ef2 = 0.0
    for k in range(4):
        for l in range(4):
            gkl = vt_dot(VF[k], VF[l], h) * nrm2[k] * nrm2[l] - (1 if k == l else 0)
            ef2 += max(abs(gkl.lower()), abs(gkl.upper())) ** 2
    ef = math.sqrt(ef2) * INF
    vln = [vt_smul(nrm2[l], VF[l], h) for l in range(4)]           # unit frame vectors
    bv = [CTo.beta(vt_range(vln[l], h).absup())[0] * sc for l in range(4)]   # 9.24 Q-leak of the frame vectors (scaled)
    # rotation bounds: frame vs eigenvectors of the truncated S (Davis-Kahan), plus label truncation: Q-component
    # |Q T phi_P|/(lam - tau) and P-part rotation by the Schur perturbation eps_v + c^2/(lam - tau).  vec: |Q T phi_P| <=
    # |<v_k, phi_P>| beta(v_k) + c |w| with w the part of phi_P orthogonal to v_k, |w| <= sin angle(phi_P, v_k) <= theta_DK + schur
    # (RV21_44 MINOR-1: the full P-angle); the block uses the root-sum-square of beta over modes 2-4 and the block angle
    thDK = [rk_h[k] / (gaps[k] * math.sqrt(max(dens[k].lower(), 1e-300))) for k in range(4)]
    schur = [(eps_vs + cQs ** 2 / max(l_lo[k] - taus, 1e-300)) / gaps[k] for k in range(4)]
    if TRUNC == 'vec':
        th_tr = [((bv[k] + cQs * (thDK[k] + schur[k])) / max(l_lo[k] - taus, 1e-300) + schur[k]) * INF for k in range(4)]
    else:
        th_tr = [(cQs / max(l_lo[k] - taus, 1e-300) + schur[k]) * INF for k in range(4)]
    theta = [(thDK[k] + th_tr[k]) * INF for k in range(4)]
    # block of modes 2-4: subspace angle by Davis-Kahan sin(Theta) <= |S V - V M|_F / delta_B (V the orthonormalized frame)
    resB = math.sqrt(sum((rk_h[k] / math.sqrt(max(dens[k].lower(), 1e-300))) ** 2 for k in (1, 2, 3))) * INF
    deltaB = min((lamT[0] - lamT[1]).lower(), l_lo[3] - lam5_full) - 2 * resB
    if deltaB <= 0:
        say('   block separation not certified'); return None
    if not (ef < 0.5):
        say('   frame Gram deviation too large'); return None
    thB_DK = resB / math.sqrt(1 - ef) / deltaB
    schurB = (eps_vs + cQs ** 2 / max(l_lo[3] - taus, 1e-300)) / deltaB
    if TRUNC == 'vec':
        bB = math.sqrt(sum(bv[k] ** 2 for k in (1, 2, 3))) / math.sqrt(1 - ef) * INF
        thB_tr = ((bB + cQs * (thB_DK + schurB)) / max(l_lo[3] - taus, 1e-300) + schurB) * INF
    else:
        thB_tr = (cQs / max(l_lo[3] - taus, 1e-300) + schurB) * INF
    r21 = l_hi[1] / l_lo[0]; r51_4 = lam5_full / l_lo[3]; r51_3 = lam5_full / l_lo[2]
    x22_4 = l_hi[1] ** 2 / (l_lo[0] * l_lo[3]); x22_3 = l_hi[1] ** 2 / (l_lo[0] * l_lo[2])
    say('J in [%.6f, %.6f] (J0=%s, h=%g): eigen %.1fs, operators %.1fs, frame %.1fs; parities %s; |w_k| %s; gaps over I %s; rotation theta %s'
        % (Jlo, Jhi, J0, h, teig, tasm, tframe, ' '.join('%+.0f' % p for p in P['par'][:4]), ' '.join('%.2f' % float(np.linalg.norm(w)) for w in ws), ' '.join('%.3e' % g for g in gaps), ' '.join('%.2e' % x for x in theta)))
    say('   (C1) ordering over I: %s; (C2) min over I of (lam2+lam4-2lam3)/lam1 >= %.5f (scaled lam1 in [%.5f, %.5f]); lam5/lam1 <= %.4e; lam2/lam1 <= %.4f'
        % (order_ok, conv_lo / l_hi[0], l_lo[0], l_hi[0], lam5_full / l_lo[0], r21))
    def dtm(tau):
        lb = labs[tau]
        d0 = mr_from_iv(rl0['r'][0][lb], rl0['r'][1][lb]); d1 = mr_from_iv(rl0['r1'][0][lb], rl0['r1'][1][lb])
        d2 = mr_from_iv(rl0['r2'][0][lb], rl0['r2'][1][lb]).scale(0.5); d3 = mr_from_iv(r3I[0][lb], r3I[1][lb]).scale(1.0 / 6.0)
        return (d0, d1, d2, d3, mtm_prange(d0, d1, d2, h))
    rt = {tau: dtm(tau) for tau in ('t', 'h', 'bb')}
    # boundary vector (N = 3, o3lib3): b(t, h, bb) = sqrt(W_t W_h W_bb) W_t W_bb g(t, h, bb), g signed (exact, rounded once),
    # log-derivative rb = R/2 + r_t + r_bb, SHIFTED like the transfer: b~ = b e^{-kb (J - J0)} with kb = <p_0, b'>/<p_0, b>
    # (class data are invariant under positive J-dependent factors); over I, b~ lies in b(J0) exp([-h, h] sup_I |rb - kb|)
    gst = np.where(adm, st['G'][st['t'], st['h'], st['bb']], 0.0)
    def bvec(B):
        sw = iv_from_arb([B['W'][i].sqrt() for i in range(L + 1)]); kk = iv_from_arb(B['k'])
        t_, h_, bb_ = st['t'], st['h'], st['bb']
        plo = sw[0][t_] * sw[0][h_] * sw[0][bb_] * kk[0][t_] * kk[0][bb_] * (1 - 16 * U64)
        phi = sw[1][t_] * sw[1][h_] * sw[1][bb_] * kk[1][t_] * kk[1][bb_] * (1 + 16 * U64)
        pc = 0.5 * (plo + phi); pr = 0.5 * (phi - plo) * INF + 2 * U64 * (np.abs(plo) + np.abs(phi))
        c = pc * gst
        r = (pr * np.abs(gst) + (np.abs(pc) + pr) * np.abs(gst) * 2 * U64) * INF + 4 * U64 * np.abs(c) + 1e-300
        b0 = MR(np.where(adm, c, 0.0), np.where(adm, r, 0.0))
        def rbm(nm):
            lo, hi = iv_from_arb(B[nm])
            m = [mr_from_iv(lo[lb], hi[lb]) for lb in (t_, h_, bb_)]
            return m[0].scale(1.5) + m[1].scale(0.5) + m[2].scale(1.5)
        return b0, rbm('r'), rbm('r1'), rbm('r2')
    b0, rb, rb1, _ = bvec(PT.B)
    _, rbI, rb1I, rb2I = bvec(BL.B)
    kb = float(phic[0] @ (b0.c * rb.c)) / float(phic[0] @ b0.c)
    def shift(v, s):                                  # MR v - s (s exact float)
        c = v.c - s
        return MR(c, v.r * INF + 4 * U64 * np.abs(c) + 1e-300)
    rr0 = shift(rb, kb); rrI = shift(rbI, kb)
    mI = rrI.absup() * INF
    bIt = MR(b0.c, (b0.r + (np.abs(b0.c) + b0.r) * np.expm1(h * mI) * (1 + 1e-12)) * INF + 1e-300)    # b(J0) exp([-h, h] mI), b >= 0
    b3 = dmul(bIt, dmul(dmul(rrI, rrI), rrI) + dmul(rrI, rb1I).scale(3.0) + rb2I)
    bvt = VT(b0, dmul(b0, rr0), dmul(b0, dmul(rr0, rr0) + rb1).scale(0.5), b3.scale(1.0 / 6.0))
    sq0 = dens[0].sqrt()
    phi0 = vt_smul(nrm2[0], VF[0], h)                # unit frame vector phi_0(t)
    # class vectors rescaled at every step by an EXACT positive polynomial q(t) ~ 1/<phi_0, y(t)>
    def qpoly(nn):
        iv = nn.inv()
        q = TM2(float(iv.a0.mid()), float(iv.a1.mid()), float(iv.a2.mid()), 0, h)
        if not (q.lower() > 0):
            raise ValueError('rescaling polynomial not positive')
        return q
    xs = [vt_smul(qpoly(vt_dot(phi0, bvt, h)), bvt, h)]
    qst = [None]; nst = [None]                        # q_j and a_j = <phi_0, S x_{j-1}>/<phi_0, x_{j-1}>
    MV = {}                                           # X~ x_i for X in S, TX, TY, TXY (shared with the vertical classes and C7)
    for i in range(I + 1):
        res = vt_mv(('S', 'TX', 'TY', 'TXY'), xs[-1], h)
        for kd in res:
            MV[(kd, i)] = res[kd]
        y = res['S']
        qj = qpoly(vt_dot(phi0, y, h))
        qst.append(qj)
        nst.append(vt_dot(phi0, y, h) * vt_dot(phi0, xs[-1], h).inv())
        xs.append(vt_smul(qj, y, h))
    if DBG is not None:
        for e in DBG:
            if e[0] == "S":
                say("   [debug] vt_mv S: |c0| %.3e; R parts: T1c2+T2c1 %.3e, h|T2c2| %.3e, T3 prange %.3e, X~R %.3e; input |R| %.3e |c1| %.3e |c2| %.3e" % e[1:])
        DBG.clear()
    res = vt_mv(('S', 'TX', 'TY', 'TXY'), xs[I + 1], h)
    for kd in res:
        MV[(kd, I + 1)] = res[kd]
    classes = []
    for tau in ('t', 'h', 'bb'):
        for i in range(I + 2):
            classes.append(('%s@%d' % (tau, i), tau, i, xs[i], vt_dm(rt[tau], xs[i], h)))
    for vt, kd in (('a', 'TX'), ('b', 'TY')):
        for j in range(1, I + 2):
            classes.append(('%s@%d' % (vt, j), vt, j, xs[j], vt_smul(qst[j], MV[(kd, j - 1)], h)))
    thq = math.sqrt(sum(x * x for x in theta)) / math.sqrt(1 - ef) * INF
    thB = (thB_DK + thB_tr) * INF                                        # block (modes 2-4) subspace angle
    efB = ef * (1 + ef) / (1 - ef) * INF                                 # |Phi Phi^T - P_frame| for the block
    data = {}
    side = {'t': 1, 'a': 1, 'bb': -1, 'b': -1, 'h': 0}
    rmax = max(float(np.max(SHr[tau][0].absup())) for tau in ('t', 'h', 'bb'))
    Tn = min(max(Mrow['TX'], Mrow['TY']), l_hi[0] + TC['dTX'] * sc)
    TXYn = min(Mrow['TXY'], l_hi[0] + TC['dTXY'] * sc)
    for (name, typ, pos, L1, LE) in classes:
        U = vt_dot(VF[0], L1, h)
        Ui = U.inv()
        E1 = vt_dot(VF[0], LE, h)
        ce = E1 * Ui
        iu0 = sq0 * Ui                                   # 1 / <phi_0, L1>
        ut = vt_smul(iu0, LE - vt_smul(ce, L1, h), h)    # u~ with the frame phi_0
        cl = [vt_dot(VF[l], ut, h) * nrm2[l] for l in range(4)]
        alf = cl[1:]
        eps = vt_smul(iu0, L1, h) - vt_smul(nrm2[0], VF[0], h)
        proj = ut
        for l in range(4):
            proj = proj - vt_smul(cl[l] * nrm2[l], VF[l], h)
        nut_f, neps_f, q5_f = vt_norm(ut, h), vt_norm(eps, h), vt_norm(proj, h)
        nL1, nLE = vt_norm(L1, h), vt_norm(LE, h)
        Un = U * nrm2[0]
        uUn = Un.lower()
        eU = max(abs((E1 * nrm2[0]).lower()), abs((E1 * nrm2[0]).upper()))
        dU = SQ2 * theta[0] * nL1; dE = SQ2 * theta[0] * nLE
        if not (uUn > dU > -1):
            say('   class %s: vacuum rotation too large' % name); return None
        dinv = dU / (uUn * (uUn - dU)) * INF
        dq = (dE / (uUn - dU) ** 2 + eU * dU * (2 * uUn + dU) / (uUn ** 2 * (uUn - dU) ** 2)) * INF
        du = (nLE * dinv + nL1 * dq) * INF
        rot = [(SQ2 * theta[l + 1] * (nut_f + du) + du) * INF for l in range(3)]
        al = [alf[l].addball(rot[l]) for l in range(3)]
        neps = (neps_f + nL1 * dinv + SQ2 * theta[0]) * INF
        data[name] = dict(typ=typ, pos=pos, al=al, nut=(nut_f + du) * INF, neps=neps, q5=(q5_f + thq * nut_f + du) * INF,
                          a_rep=None, alf=alf, nutf=nut_f, du=du, u0lo=uUn, L1v=L1, LEv=LE, rot=rot)
        if typ in ('a', 'b') and pos == I + 1:
            data[name]['a_rep'] = nst[pos].lower()
    # ---- eps(0), geometric decay, deep classes, truncation fuzz ----
    eps0 = max(dd['neps'] for dd in data.values() if dd['pos'] == 0)
    # ---- label truncation of the class vectors (full model T against truncated S), every term derived (UNIF 9.17) ----
    # X_i - x_i = sum_j T^{i-1-j}(T - S)x_j + T^i Q b, |(T - S) x| <= eps_v |x| + |Q T x|; op/tri: |Q T x| <= c |x|;
    # vec (9.24): |Q T x_j| <= beta(x_j); relative to u_i = (lam^S)^i u0(b):
    #   trelA = sum_j rho^{i-1-j} (eps_v |y_j| + beta(y_j))/lam,  y_j = x_j/<phi_0^S, x_j>,  |y_j| <= 1 + eps0
    u0b = vt_dot(phi0, bvt, h).lower() - SQ2 * theta[0] * vt_norm(bvt, h)
    if not (u0b > 0):
        say('   u0(b) not certified positive'); return None
    rho = (1 + (eps_vs + cQs ** 2 / max(l_lo[0] - taus, 1e-300)) / l_lo[0]) * INF
    ii = I + 2
    bx = []
    for j in range(ii):
        cxl = vt_dot(phi0, xs[j], h).lower() - SQ2 * theta[0] * vt_norm(xs[j], h)
        bx.append(CTo.beta(vt_range(xs[j], h).absup())[0] * sc / cxl if cxl > 0 else float('inf'))
    trelA_op = ii * rho ** (ii - 1) * (eps_vs + cQs) / l_lo[0] * (1 + eps0) * INF
    trelA_vec = sum(rho ** (ii - 1 - j) * (eps_vs * (1 + eps0) + bx[j]) for j in range(ii)) / l_lo[0] * INF
    trelA = trelA_vec if TRUNC == 'vec' else trelA_op
    ebs = math.exp(abs(kb) * h) * (1 + 1e-12)        # |Q b~| = e^{-kb t} |Q b| <= ebs |Q b| (b~ = shifted boundary vector)
    trelB = rho ** ii * TC['Qb'] * ebs / u0b * INF
    trel = (trelA + trelB) * INF
    kap0 = 1 - th_tr[0] * (1 + eps0)
    yv0 = (1 + eps0) / kap0 * INF                            # |y|
    if not (kap0 - trel > 0.5):
        say('   truncation too large (%.3e)' % trel); return None
    dy = trel * (1 + yv0) / (kap0 - trel) * INF              # |Y - y|
    assert math.isfinite(TC['rQ'])
    rQm = max(rmax, TC['rQ'])
    rTf = rQm * (1 + (cQs + taus) / l_lo[0]) * INF
    RdLraw = (rTf * rho * trelA + max(TC['RQb'], rTf * rho ** ii * TC['Qb']) * ebs / u0b) * INF
    RdY = (RdLraw + rmax * yv0 * trel) / (kap0 - trel) * INF  # |R (Y - y)|
    eps0f = (eps0 + dy) * INF
    den_e = (1 - theta[0] - eps0f) ** 2
    if den_e <= 0.5:
        say('   eps(0) too large for the geometric bound (%.3e)' % eps0f); return None
    geo = lambda i: (2 * (1 + eps0f) * r21 ** i * eps0f / den_e + th_tr[0] / (1 - th_tr[0])) * INF
    for dd in data.values():
        dd['neps'] = min(dd['neps'], geo(dd['pos']))
    Rq = 0.0; Tqa = 0.0
    for l in range(4):
        vl = vln[l]
        for tau in ('t', 'h', 'bb'):
            Rq = max(Rq, (vt_norm(vt_dm(rt[tau], vl, h), h) + rmax * SQ2 * theta[l] + rQm * (cQs + taus) / l_lo[l]) * INF)
        res = vt_mv(('TX', 'TY'), vl, h)
        for kd in ('TX', 'TY'):
            Tqa = max(Tqa, (vt_norm(res[kd], h) + l_hi[0] * SQ2 * theta[l] + 2 * cQs + TC['dTX'] * sc) * INF)
    Tq = Tqa / l_lo[0]
    nfz_h = (RdY * (1 + yv0 + dy) + Rq * yv0 * dy) * INF
    tfz_h = min(nfz_h, dy * Rq * (1 + geo(0) + dy + yv0) * INF)
    yvf = 1 + geo(0) + SQ2 * theta[0]                        # |y'| for frame-normalized y'
    a_fr = min(nst[j].lower() for j in range(1, I + 2))
    a_lo = (a_fr - SQ2 * theta[0] * l_hi[0] * yvf) / (1 + SQ2 * theta[0] * yvf)
    if TRUNC == 'vec':
        d1 = (l_hi[0] * dy + eps_vs * yv0 + max(bx[:I + 1]) / kap0) * INF
    else:
        d1 = (l_hi[0] * dy + (eps_vs + cQs) * yv0) * INF
    dE = (l_hi[0] * dy + (TC['dTX'] * sc + 2 * cQs) * yv0) * INF
    a_m = a_lo - d1
    if not (a_m > 0):
        say('   vertical normalization not certified'); return None
    L1n = (l_hi[0] + eps_vs) * yv0; LEn = (l_hi[0] + TC['dTX'] * sc) * yv0; e_abs = Tqa * yv0
    nfz_v = (dE / a_m + LEn * d1 / (a_lo * a_m) + dE * (L1n + d1) / a_m ** 2 + e_abs * d1 / a_m ** 2
             + e_abs * L1n * d1 * (2 * a_lo + d1) / (a_lo ** 2 * a_m ** 2)) * INF
    tfz_v = nfz_v
    dv_raw = {'h': (dy, RdY), 'v': ((d1 + L1n * d1 / a_lo) / a_m * INF, (dE + LEn * d1 / a_lo) / a_m * INF)}
    e_d = 2 * (1 + eps0f) * (r21 ** (I + 1) + r21 ** (I + 2)) * eps0f / den_e * INF       # y = x_i, i >= I+1
    e_dv = 2 * (1 + eps0f) * (r21 ** I + r21 ** (I + 1)) * eps0f / den_e * INF            # y = x_{j-1}, j >= I+1
    yh = 1 + geo(I + 1) + SQ2 * theta[0]; yv = 1 + geo(I) + SQ2 * theta[0]          # |y| bounds
    Sn = l_hi[0]
    Tnf = l_hi[0]
    rT = rTf
    eta_v = 0.0; a_v = float('inf'); am_v = float('inf')
    for dd in data.values():
        if dd['a_rep'] is not None:
            a = (dd['a_rep'] - SQ2 * theta[0] * Sn * yv) / (1 + SQ2 * theta[0] * yv) - Sn * dy
            am = a - Sn * e_dv
            if am <= 0:
                say('   deep vertical radius: a_min <= 0'); return None
            br = 1 + yv * Sn / am + Sn * (yv + e_dv) / am + yv * Sn / am + yv * yv * Sn * Sn * (2 * a + Sn * e_dv) / (a * a * am)
            eta_v = max(eta_v, Tnf * e_dv / am * br * INF)
            a_v = min(a_v, a); am_v = min(am_v, am)
    dRy = rT * Sn / am_v * (1 + Sn * yv / a_v) * e_dv
    eta_h = (dRy * (1 + yh + e_d) + rT * Sn * yv / a_v * e_d) * INF
    neps_deep = geo(I + 1)
    for name, dd in data.items():
        vert = dd['typ'] in ('a', 'b')
        etad = (eta_v if vert else eta_h) if dd['pos'] == I + 1 else 0.0
        tfz_c, nfz_c = (tfz_v, nfz_v) if vert else (tfz_h, nfz_h)
        dd['al'] = [a.addball(tfz_c + etad) for a in dd['al']]
        dd['nut'] += nfz_c + etad; dd['q5'] += nfz_c + etad
        dd['dB'] = (dd['du'] + nfz_c + etad) * INF
        dd['neps'] = (neps_deep if dd['pos'] == I + 1 else dd['neps']) + dy
    say('   classes: eps(0) <= %.4e; deep radii: horizontal %.2e, vertical %.2e; truncation: trel %.2e, |dy| %.2e; mode fuzz h %.2e v %.2e, norm fuzz h %.2e v %.2e (Rq %.2f, Tq %.2f); frame Gram dev %.1e; block angle %.2e; r_Q %.3f (r_{L+1} %.3f), tail ratio above AE <= %.3f'
        % (eps0, eta_h, eta_v, trel, dy, tfz_h, tfz_v, nfz_h, nfz_v, Rq, Tq, ef, thB, TC['rQ'], TC['rL1'], TC['q_r5']))
    say('   truncation comparison (scaled, /lam1): c op %.2e, c tri %.2e (used %.2e); beta(y_j) %s; beta(v_k) %s; trelA op %.2e vec %.2e; trelB %.2e (op %.2e); eps_v/lam1 %.1e; th_tr %s'
        % (TC['cQ_op'] * sc / l_lo[0], TC['cQ_tri'] * sc / l_lo[0], cQs / l_lo[0], ' '.join('%.1e' % (x / l_lo[0]) for x in bx), ' '.join('%.1e' % (x / l_lo[0]) for x in bv),
           trelA_op, trelA_vec, trelB, rho ** ii * TC["Qb_op"] * ebs / u0b * INF, eps_vs / l_lo[0], ' '.join('%.1e' % x for x in th_tr)))
    for nm in ('t@0', 'bb@0', 'h@0', 'a@1', 't@%d' % (I + 1), 'a@%d' % (I + 1)):
        d = data[nm]
        say('      %-6s a2 %s a3 %s a4 %s |u~| %.3e |eps| %.3e |Q5 u~| %.3e' % (nm, ' '.join('%.4e' % x for x in (d['al'][0].lower(), d['al'][0].upper())),
            ' '.join('%.4e' % x for x in (d['al'][1].lower(), d['al'][1].upper())), ' '.join('%.4e' % x for x in (d['al'][2].lower(), d['al'][2].upper())), d['nut'], d['neps'], d['q5']))
    # ---- criterion over I ----
    s2 = np.sign(float(data['t@0']['al'][0].a0.mid())); s4 = np.sign(float(data['t@0']['al'][2].a0.mid()))
    s3 = np.sign(float(data['t@%d' % (I + 1)]['al'][1].a0.mid()))
    ok2 = all((dd['al'][0] * float(s2)).lower() > 0 for dd in data.values())
    ok4 = all((dd['al'][2] * float(s4)).lower() > 0 for dd in data.values())
    ok3 = all(((dd['al'][1] * float(s3 * side[dd['typ']])).lower() > 0) if side[dd['typ']] != 0 else True for dd in data.values())
    names = list(data)
    wF0 = None; wpp = None; wsame = None; wsf = None; m0 = 0; need = {}
    zero = TM2(0, 0, 0, 0, h)
    for X in names:
        for Y in names:
            dX, dY = data[X], data[Y]
            p2 = dX['al'][0] * dY['al'][0]; p4 = dX['al'][2] * dY['al'][2]
            hp = dX['typ'] == 'h' or dY['typ'] == 'h'
            p3 = zero if hp else dX['al'][1] * dY['al'][1]
            opp = side[dX['typ']] * side[dY['typ']] < 0
            q55 = dX['q5'] * dY['q5'] * INF; AA = dX['nut'] * dX['neps'] * dY['nut'] * dY['neps'] * INF
            if opp:
                F0 = (p2 + p4 + p3).lower(); pp = (p2 - p4).lower()
                aX, aY = dX['alf'], dY['alf']
                FB = (aX[0] * aY[0] + aX[1] * aY[1] + aX[2] * aY[2]).lower()
                nX, nY = dX['nutf'], dY['nutf']
                FB -= ((efB + thB) * nX * nY + dX['dB'] * (nY + dY['dB']) + dY['dB'] * nX) * INF
                F0 = max(F0, FB)
                if wF0 is None or F0 < wF0[0]:
                    wF0 = (F0, X, Y)
                if wpp is None or pp < wpp[0]:
                    wpp = (pp, X, Y)
                base, ra, rb_ = F0, r51_3, x22_3
            else:
                base = (p2 + p4).lower()
                if wsame is None or base < wsame[0]:
                    wsame = (base, X, Y)
                ra, rb_ = r51_4, x22_4
            m = 0
            while base <= 0 or q55 * ra ** m + AA * rb_ ** m >= base:
                m += 1
                if m > 60:
                    break
            m0 = max(m0, m)
            if m > 0:
                need[(X, Y)] = m if base > 0 else 99
            sf = base / max(q55 + AA, 1e-300)
            if wsf is None or sf < wsf[0]:
                wsf = (sf, X, Y)
    if os.environ.get("C6DEBUG") and wF0 is not None:
        X, Y = wF0[1], wF0[2]; dX, dY = data[X], data[Y]
        Fv = dX["al"][0] * dY["al"][0] + dX["al"][2] * dY["al"][2] + dX["al"][1] * dY["al"][1]
        tm = lambda s: "a0 %s a1 %s a2 %s R %s" % (s.a0.str(4), s.a1.str(4), s.a2.str(4), s.R.str(4))
        say("   [debug] F0 pair %s %s: F %s" % (X, Y, tm(Fv)))
        say("   [debug] rot %s / %s; du %.3e %.3e; tfz_v %.3e eta_v %.3e tfz_h %.3e eta_h %.3e; theta %s" % (dX["rot"], dY["rot"], dX["du"], dY["du"], tfz_v, eta_v, tfz_h, eta_h, theta))
        for nm in (X, Y):
            for l in range(3):
                say("   [debug]   %s alpha%d frame %s | with fuzz %s" % (nm, l + 2, tm(data[nm]["alf"][l]), tm(data[nm]["al"][l])))
    # ---- (C6): direct evaluation of Cov Z^2 = A D - B C for the pairs (and distances m) below their dominance threshold ----
    M6MAX = 4
    n6 = 0; neg6 = 0; w6 = None; c6ok = True
    if need:
        if max(need.values()) > M6MAX:
            c6ok = False
        else:
            nl1 = {nm: vt_norm(data[nm]['L1v'], h) for nm in data}; nlE = {nm: vt_norm(data[nm]['LEv'], h) for nm in data}
            def dev(nm):            # perturbation bounds of the normalized (L1, LE) of class nm: truncation plus deep positions
                d = data[nm]; a1, aE = dv_raw['v' if d['typ'] in ('a', 'b') else 'h']
                if d['pos'] == I + 1:
                    if d['typ'] in ('a', 'b'):
                        fac = (1 + Sn * yv / a_v) / am_v * e_dv
                        a1 += Sn * fac; aE += Tnf * fac
                    else:
                        a1 += e_d; aE += dRy
                cmx = nl1[nm]
                return a1 * cmx * INF, aE * cmx * INF
            prop = {}
            def right(nm, m):       # (r1, rE, |r1|, |rE|, d1, dE) after m normalized steps
                if (nm, m) in prop:
                    return prop[(nm, m)]
                if m == 0:
                    d1_, dE_ = dev(nm)
                    out = (data[nm]['L1v'], data[nm]['LEv'], nl1[nm], nlE[nm], d1_, dE_)
                else:
                    r1, rE, n1, nE, d1_, dE_ = right(nm, m - 1)
                    y1, yE = vt_mv('S', r1, h), vt_mv('S', rE, h)
                    ni = qpoly(vt_dot(phi0, y1, h)); qup = ni.upper()
                    g = Sn * qup
                    r1n, rEn = vt_smul(ni, y1, h), vt_smul(ni, yE, h)
                    if TRUNC == 'vec':
                        b1_ = CTo.beta(vt_range(r1, h).absup())[0] * sc; bE_ = CTo.beta(vt_range(rE, h).absup())[0] * sc
                        out = (r1n, rEn, vt_norm(r1n, h), vt_norm(rEn, h), (g * d1_ + qup * (eps_vs * n1 + b1_)) * INF, (g * dE_ + qup * (eps_vs * nE + bE_)) * INF)
                    else:
                        tr = (eps_vs + cQs) * qup
                        out = (r1n, rEn, vt_norm(r1n, h), vt_norm(rEn, h), (g * d1_ + tr * n1) * INF, (g * dE_ + tr * nE) * INF)
                prop[(nm, m)] = out
                return out
            for (X, Y), mXY in need.items():
                lX1, lXE = data[X]['L1v'], data[X]['LEv']; dX1, dXE = dev(X)
                for m in range(mXY):
                    if m == 0 and data[X]['typ'] == data[Y]['typ'] and data[X]['typ'] in ('t', 'h', 'bb'):
                        continue
                    r1, rE, n1, nE, d1_, dE_ = right(Y, m)
                    A = vt_dot(lXE, rE, h).addball(dXE * nE + nlE[X] * dE_ + dXE * dE_)
                    B = vt_dot(lXE, r1, h).addball(dXE * n1 + nlE[X] * d1_ + dXE * d1_)
                    C = vt_dot(lX1, rE, h).addball(dX1 * nE + nl1[X] * dE_ + dX1 * dE_)
                    D = vt_dot(lX1, r1, h).addball(dX1 * n1 + nl1[X] * d1_ + dX1 * d1_)
                    mn = (A * D - B * C).lower(); nD = (D * D).lower()
                    n6 += 1
                    if not (mn > 0):
                        neg6 += 1
                    if w6 is None or mn / max(nD, 1e-300) < w6[0]:
                        w6 = (mn / max(nD, 1e-300), X, Y, m)
            c6ok = neg6 == 0
    # ---- same-column (a, b) pairs: Cov Z^2 = <l, TXY r><l, S r> - <l, TX r><l, TY r> with normalized l, r ----
    lv = {i: xs[i] for i in range(I + 2)}
    nl = {i: vt_norm(lv[i], h) for i in lv}
    Mts = ('TXY', 'S', 'TX', 'TY')
    Mr = {(k, i): MV[(k, i)] for k in Mts for i in lv}
    Mfull = l_hi[0] * INF
    vtail = {'S': eps_vs, 'TX': TC['dTX'] * sc, 'TY': TC['dTX'] * sc, 'TXY': TC['dTXY'] * sc}
    eM = {k: vtail[k] * INF for k in Mts}
    negc = 0; wc = None
    for iL in range(I + 2):
        for iR in range(I + 2):
            vals = {}
            for k in Mts:
                v = vt_dot(lv[iL], Mr[(k, iR)], h)
                e = eM[k] * nl[iL] * nl[iR]
                dL = (dy + (e_d if iL == I + 1 else 0.0)) * nl[iL]
                dR = (dy + (e_d if iR == I + 1 else 0.0)) * nl[iR]
                e += Mfull * (dL * (nl[iR] + dR) + nl[iL] * dR) * INF
                vals[k] = v.addball(e)
            cv = vals['TXY'] * vals['S'] - vals['TX'] * vals['TY']
            norm = (vals['S'] * vals['S']).lower()
            low = cv.lower()
            if not (low > 0):
                negc += 1
            if wc is None or low / max(norm, 1e-300) < wc[0]:
                wc = (low / max(norm, 1e-300), iL, iR)
    say('   (C3) signs over I: a2 one-signed %s, a4 one-signed %s, a3 by side %s' % (ok2, ok4, ok3))
    say('   (C4) over I: min (p2 - p4) = %.4e at (%s, %s); min F(0) = %.4e at (%s, %s); same-side min %.4e at (%s, %s)' % (wpp + wF0 + wsame))
    say('   (C5) over I: m0 = %d, safety factor >= %.3e at (%s, %s) (ratios lam5/lam4 <= %.4f, lam5/lam3 <= %.4f, lam2^2/(lam1 lam4) <= %.4f)'
        % ((m0,) + wsf + (r51_4, r51_3, x22_4)))
    say('   (C7) same-column over I: %d position pairs, not certified > 0: %d; min (Cov Z^2 / <S>^2) lower bound %.4e at %s' % ((I + 2) ** 2, negc, wc[0], wc[1:]))
    if need:
        say('   (C6) direct evaluation below the dominance threshold: %d pairs, max m = %d; %d evaluations, not certified > 0: %d; min (A D - B C)/D^2 lower bound %s'
            % (len(need), max(need.values()), n6, neg6, ('%.4e at (%s, %s, m=%d)' % w6) if w6 else '-'))
    x22_ok = x22_4 * INF < 1
    closed = order_ok and conv_lo > 0 and ok2 and ok3 and ok4 and wpp[0] > 0 and wF0[0] > 0 and wsame[0] > 0 and (m0 == 0 or c6ok) and negc == 0 and x22_ok
    tt = time.time() - t0
    say('   ==> interval [%.6f, %.6f]: %s [%s; %s] (%.1fs: eigen %.1f, operators %.1f, frame %.1f, %d Taylor-model products in %.1fs, %d MR factor products)'
        % (Jlo, Jhi, 'CERTIFIED' if closed else 'NOT certified', PTAG, TTAG, tt, teig, tasm, tframe, TMV[0], TMV[1], NPROD[0]))
    return dict(closed=closed, F0=wF0[0], pp=wpp[0], sf=wsf[0], c7=wc[0], conv=conv_lo / l_hi[0], m0=m0, trel=trel, secs=tt)

if not ADAPT:
    for (J0, h) in ivals:
        interval(J0, h)
else:
    # adaptive cover of [JS, JE] (certint5)
    JS, JE, q, qmax = ADAPT
    LEDGER = os.path.join(BASE, 'out', 'o3cover6_%s.ledger' % tag.split('_')[0])
    assert '/data/e17/unif/scratch/out/' in LEDGER
    a = JS; ovl = 0.02; budget = 520.0; last = 0.0         # stop before an interval would end past the budget (jobs < 580 s)
    while a < JE and time.time() - t00 + 1.3 * last < budget:
        h = q * a / (1 - q * (1 - ovl))
        J0f = a + (1 - ovl) * h
        try:
            ti = time.time()
            res = interval(Fraction(J0f), h)
            last = time.time() - ti
        except (ZeroDivisionError, ValueError, sla.ArpackNoConvergence) as ex:
            say('   interval J0=%r h=%r: exception %s' % (J0f, h, ex)); res = None
        ok = bool(res and res['closed'])
        with open(LEDGER, 'a') as f:
            if res:
                f.write('%r %r %d %d %s F0=%.4e pp=%.4e sf=%.3e c7=%.4e conv=%.5f m0=%d trel=%.2e secs=%.1f %s %s job=%s\n' % (J0f, h, L, I, 'CERT' if ok else 'FAIL', res['F0'], res['pp'], res['sf'], res['c7'], res['conv'], res['m0'], res['trel'], res['secs'], PTAG, TTAG.replace(' ', '_'), tag))
            else:
                f.write('%r %r %d %d FAIL early %s %s job=%s\n' % (J0f, h, L, I, PTAG, TTAG.replace(' ', '_'), tag))
        if ok:
            a = J0f + h
            q = min(q * 1.15, qmax)
        else:
            q = q / 1.6
            if q < 1e-4:
                say('adaptive cover stopped: q too small at a = %r' % a); break
    say('adaptive cover: reached a = %r (target %r), last q = %.4g' % (a, JE, q))
say('total %.1fs' % (time.time() - t00))
