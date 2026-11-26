# Wave 18, N = 3, version 2 = v2.1 (UNIF_NOTES 9.21): code5/o3cert.py plus the review RV21_37 MINOR-1 (closed requires
# lam2^2/(lam1 lam4) < 1), MINOR-2 (geometric remainders of the character-sum tails, Amos i_{a+1}/i_a <= J/(2a+2)),
# n3 (lam_k^S > tau_inf checked), n5 (r(l)^2 i_l decreasing above L checked); n1, v2-n1 as in code4/certint5.py.
# o3cert.py header:
# Wave 18, N = 3 (O(3) spins): code4/certint4.py (UNIF_NOTES 9.17) on the O(3) column map of code5/o3struct.py, assembled
# by code5/o3lib3.py.  Only the model-specific parts differ from certint4: the structure (signed 6j quadruples), the
# weights W_l = i_l(J) = sqrt(pi/2J) I_{l+1/2}(J) with multiplicity 2l + 1, the boundary vector
# b = sqrtC W_t W_bb g(t,h,bb), the sign of phi_0 (its |000> component is <K^{1/2} 1, psi> > 0), and the truncation
# constants of point_fast (UNIF_NOTES 9.20).  The criterion, the Taylor models and every derived bound are certint4's.
# certint4 header:
# Wave 18: certified G2 criterion on J-intervals [J0 - h, J0 + h] for all n and all pairs, version 4 (UNIF_NOTES 9.17:
# every truncation term derived: normalized perturbation |dy|, R on the label tail, full-model eigenvector Q-parts,
# vertical tails of T_X, (lam^T/lam^S)^i factors, n^2 u padding; version 3 (UNIF 9.14-9.15) below).
# Changes from certint2:
#  - point part in float mid-rad arithmetic on the interval assembly (numpy eigh, then Weyl/Ostrowski with rigorous
#    rounding bounds); no arb assembly;
#  - class vectors as order-2 vector Taylor models x(t) = c0 + c1 t + c2 t^2 + t^3 R(t), propagated through the matrix
#    Taylor models of the SCALED transfer S(J0 + t) e^{-kap t}/lam0 (every criterion quantity is invariant under a
#    common positive J-dependent factor of the class vectors or of the transfer matrices; the scaling removes the
#    lam_1^i growth that ruined the remainders of certint2);
#  - |eps|, |u~|, |Q5 u~| as norms of vector Taylor models of eps, u~ and u~ - sum_l phi_l <phi_l, u~>;
#  - deep classes (positions > I+1) from the position-(I+1) representative with Lipschitz radii (horizontal and
#    vertical classes separately);
#  - same-column pairs with normalized vector Taylor models and explicit truncation and deep fuzz.
# usage: o3cert.py TAG L I J0:h[,J0:h,...]   or   o3cert.py TAG L I adapt:JS:JE:q:qmax
import os, sys, time, math
from fractions import Fraction
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(1, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'code4'))
from flint import arb, ctx
import o3struct, o3lib3
from tm import TM
from tm2 import TM2, fdn, fup
tag, L, I = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
ADAPT = None
if sys.argv[4].startswith('adapt:'):
    ADAPT = tuple(float(x) for x in sys.argv[4].split(':')[1:])
    ivals = []
else:
    ivals = [(Fraction(x.split(':')[0]), float(x.split(':')[1])) for x in sys.argv[4].split(',')]
ctx.prec = 128
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(BASE, 'out', 'o3cert2_%s.txt' % tag)
assert '/pkg_n3/out/' in OUT and not os.path.exists(OUT)
CACHE = None                    # the home disk is above 90%: the O(3) tables are rebuilt in every job, never cached
lines = []
def say(s):
    print(s, flush=True); lines.append(s)
    open(OUT, 'w').write('\n'.join(lines) + '\n')
U64 = 2.0 ** -53
SQ2 = math.sqrt(2) * (1 + 1e-15)
INF = 1 + 1e-12                 # inflation of float-computed radii
t00 = time.time()
Q = o3struct.quad_struct(L, CACHE)
states = Q['states']; nS = len(states)
i000 = states.index((0, 0, 0))
say('o3cert %s: L=%d I=%d; %d states, %d quadruples (max merged terms %d); structure %.1fs' % (tag, L, I, nS, len(Q['c']), int(Q['cnt'].max()), time.time() - t00))

# ---------------- float mid-rad (MR) vectors and matrices, rigorous rounding margins ----------------
class MR:
    __slots__ = ('c', 'r', 'ac')
    def __init__(self, c, r):
        self.c = np.asarray(c, dtype=float); self.r = np.asarray(r, dtype=float); self.ac = None
    @staticmethod
    def iv(x, shape=None):
        c = 0.5 * (x.lo + x.hi)
        r = 0.5 * (x.hi - x.lo) * INF + 2 * U64 * (np.abs(x.lo) + np.abs(x.hi)) + 1e-300
        if shape is not None:
            c = c.reshape(shape); r = r.reshape(shape)
        return MR(c, r)
    def __add__(self, o):
        c = self.c + o.c
        return MR(c, (self.r + o.r) * INF + 4 * U64 * np.abs(c))
    def __sub__(self, o):
        c = self.c - o.c
        return MR(c, (self.r + o.r) * INF + 4 * U64 * np.abs(c))
    def scale(self, s):           # exact float s
        c = self.c * s
        return MR(c, self.r * abs(s) * INF + 4 * U64 * np.abs(c) + 1e-300)
    def absup(self):
        return (np.abs(self.c) + self.r) * INF
    def abs_c(self):
        if self.ac is None:
            self.ac = np.abs(self.c)
        return self.ac
def zero_mr(n):
    return MR(np.zeros(n), np.zeros(n))
def mv(M, x):
    """M (MR matrix) times x (MR vector)."""
    ac = M.abs_c(); ax = np.abs(x.c)
    c = M.c @ x.c
    r = ac @ x.r + M.r @ (ax + x.r) + (M.c.shape[1] + 2) * U64 * (ac @ ax)
    return MR(c, r * INF + 1e-300)
def dmul(d, x):
    c = d.c * x.c
    return MR(c, (np.abs(d.c) * x.r + d.r * (np.abs(x.c) + x.r)) * INF + 4 * U64 * np.abs(c) + 1e-300)
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
    """MR (vector or matrix) times the arb ball x"""
    c, r = cr(x)
    cc = M.c * c
    return MR(cc, (M.r * (abs(c) + r) + r * np.abs(M.c)) * INF + 4 * U64 * np.abs(cc) + 1e-300)
def tball(v, s):
    """v times an unknown t-dependent factor in [-s, s]"""
    return MR(np.zeros_like(v.c), s * v.absup() * INF)
def mat_mr(iv):
    return MR.iv(iv, (nS, nS))

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
def vt_mv(Mt, v, h):
    """matrix Taylor model Mt = (M0, M1, M2, M3, Mpr) times VT v"""
    M0, M1, M2, M3, Mpr = Mt
    c0 = mv(M0, v.c0)
    c1 = mv(M0, v.c1) + mv(M1, v.c0)
    c2 = mv(M0, v.c2) + mv(M1, v.c1) + mv(M2, v.c0)
    R = mv(M1, v.c2) + mv(M2, v.c1) + tball(mv(M2, v.c2), h) + mv(M3, vt_range(v, h)) + mv(Mpr, v.R)
    return VT(c0, c1, c2, R)
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

# ---------------- point part at J0 in float mid-rad arithmetic ----------------
def point_fast(A0, J0f, h):
    S0 = mat_mr(A0['S'])
    lam, Qm = np.linalg.eigh(0.5 * (S0.c + S0.c.T))
    o = np.argsort(-lam); lam = lam[o]; Qm = Qm[:, o]
    gam = (nS + 4) * U64 / (1 - (nS + 4) * U64)
    aQ = np.abs(Qm)
    B = (Qm * lam) @ Qm.T
    absQLQ = (aQ * np.abs(lam)) @ aQ.T
    D = S0.c - B
    Er = (np.abs(D) + S0.r + (gam + 2 * U64) * absQLQ + U64 * (np.abs(S0.c) + np.abs(B))) * (1 + 1e-10)
    # float sums: n^2 squares (Frobenius) and n-term row sums, padded by 2 (count + 4) u (RV11_4 nit 5)
    eF = min(float(np.sqrt(np.sum(Er * Er))) * (1 + 2 * (Er.size + 4) * U64), math.sqrt(float(np.max(np.sum(Er, axis=1))) * float(np.max(np.sum(Er, axis=0)))) * (1 + 2 * (nS + 4) * U64)) * (1 + 1e-12)
    F = Qm.T @ Qm - np.eye(nS)
    Fr = (np.abs(F) + gam * (aQ.T @ aQ) + 2 * U64) * (1 + 1e-10)
    fF = float(np.sqrt(np.sum(Fr * Fr))) * (1 + 2 * (Fr.size + 4) * U64) * (1 + 1e-12)
    encl = [(l * (1 - fF) - eF, l * (1 + fF) + eF) if l >= 0 else (l * (1 + fF) - eF, l * (1 - fF) + eF) for l in lam]
    flip = [states.index((s[2], s[1], s[0])) for s in states]
    par = [float(Qm[flip, k] @ Qm[:, k]) for k in range(5)]
    Ja = arb(J0f) + arb(h)                    # exact top of the interval (the constants increase with J)
    # O(3) weights i_l(J_top) = sqrt(pi/2J) I_{l+1/2}(J_top), l = 0..L+60 (decreasing in l, increasing in J)
    pre = (arb.pi() / (2 * Ja)).sqrt()
    ks = [pre * Ja.bessel_i(arb(l) + arb(1) / 2) for l in range(L + 61)]
    k0 = ks[0]
    Jl = arb(J0f) - arb(h)
    # character-sum tails: explicit terms a = L+1..AE, AE = L+59, plus the geometric remainder
    # term_AE q/(1 - q), where q >= term_{a+1}/term_a for every a >= AE (all ratio bounds below decrease in a):
    #   i_{a+1}/i_a = I_{a+3/2}/I_{a+1/2} <= J/(2a+2) <= kr (Amos, nu = a + 1/2);  (2a+3)/(2a+1) <= m2;
    #   rr(a+1)/rr(a) <= ((a+1)/a)^2 = rq;  (a/J_lo + 1) ratio <= (a+1)/a
    AE = L + 59
    kr = Ja / (2 * AE + 2); m2 = arb(2 * AE + 3) / (2 * AE + 1); rq = (arb(AE + 1) / AE) ** 2
    def gtail(terms, q):
        if not (q.upper() < 1):
            raise ValueError('tail ratio bound >= 1')
        return sum(terms, arb(0)) + terms[-1] * q / (1 - q)
    # vertical-bond tail: e^{J s.t} - f_L(s.t) = sum_{a > L} i_a (2a + 1) P_a(s.t), |P_a| <= 1
    tail = gtail([(2 * a_ + 1) * ks[a_] for a_ in range(L + 1, AE + 1)], m2 * kr)
    eps_v = fup(abs(k0 ** 3 * tail * (2 * Ja.exp() + tail)))
    # r-weighted vertical tail (energy insertions on a vertical bond), r(a) <= a/J_lo + 1 on the interval
    tail1 = gtail([(2 * a_ + 1) * ks[a_] * (a_ / Jl + 1) for a_ in range(L + 1, AE + 1)], m2 * kr * (AE + 1) / AE)
    eJ = Ja.exp()
    d0 = tail * (2 * eJ + tail); d1 = tail1 * (eJ + tail) + eJ * tail; d2 = tail1 * (eJ + tail1) + eJ * tail1
    dTX = fup(abs(k0 ** 3 * (d0 + d1))); dTXY = fup(abs(k0 ** 3 * (d0 + d2)))
    # boundary vector on labels > L (full model): b(a,b,c)^2 = W_a^3 W_b W_c^3 (2a+1)(2b+1)(2c+1) (a b c; 000)^2, with
    # sum_b (2b+1) (a b c; 000)^2 = 1 for fixed a, c and W decreasing in l.  Over max(a, c) > L the b-sum is <= W_0, over
    # a, c <= L < b it is <= W_{L+1}:  |Q b|^2 <= W_0 (F_tot^2 - F_L^2) + W_{L+1} F_L^2,  F = sum (2l+1) W_l^3
    rr = [(arb(l) / Jl + 1) ** 2 for l in range(L + 61)]
    def sums(wf, q):
        lo_ = sum((wf(l) for l in range(L + 1)), arb(0)); tl_ = gtail([wf(l) for l in range(L + 1, AE + 1)], q)
        return lo_, tl_
    F = sums(lambda l: (2 * l + 1) * ks[l] ** 3, m2 * kr ** 3)
    Qb = fup((k0 * F[1] * (2 * F[0] + F[1]) + ks[L + 1] * F[0] * F[0]).sqrt())
    # r-weighted version for |R Q b| (R of any row; r(l)^2 <= rr(l) = (l/J_lo + 1)^2 on the interval): sum over Q of
    # (rr(a) + rr(b) + rr(c)) b^2; the b-sum of rr(b) W_b (2b+1)(a b c; 000)^2 is <= m = max_b rr(b) W_b (all b), resp.
    # m_Q = max_{b > L} rr(b) W_b (rr(b) W_b decreases for b > L, checked below with q_r5, so the maxima over the explicit
    # range are the maxima over all b):
    #   |R Q b|^2 <= 2 W_0 (Fr_tot F_tot - Fr_L F_L) + m (F_tot^2 - F_L^2) + 2 W_{L+1} Fr_L F_L + m_Q F_L^2
    # n5: r(l)^2 i_l and rr(l) i_l decrease for l > L: ratio <= ((l+1+J)/l)^2 J/(2l+2) at l = L+1 (decreasing in l)
    q_r5 = ((arb(L + 2) + Ja) / (L + 1)) ** 2 * Ja / (2 * L + 4)
    if not (q_r5.upper() < 1):
        raise ValueError('r(l)^2 i_l not shown decreasing above L')
    Fr = sums(lambda l: rr[l] * (2 * l + 1) * ks[l] ** 3, rq * m2 * kr ** 3)
    m_all = arb(max(fup(abs(rr[l] * ks[l])) for l in range(L + 60)))
    m_Q = arb(max(fup(abs(rr[l] * ks[l])) for l in range(L + 1, L + 60)))
    RQb = fup((2 * k0 * (Fr[1] * (F[0] + F[1]) + Fr[0] * F[1]) + m_all * F[1] * (2 * F[0] + F[1]) + 2 * ks[L + 1] * Fr[0] * F[0] + m_Q * F[0] * F[0]).sqrt())
    kapQ = ks[L + 1] * k0 ** 2
    tau_inf = fup(abs((2 * Ja).exp() * kapQ)); cQ = fup(abs((2 * Ja).exp() * (k0 ** 3 * kapQ).sqrt()))
    Jb = arb(J0f, h)
    rL1 = fup(o3lib3.bessel_derivs(Jb, L + 1)['r'][L + 1])      # r(L+1) over the interval (monotone hulls)
    return dict(lam=lam, Qm=Qm, encl=encl, par=par, eps_v=eps_v, tau_inf=tau_inf, cQ=cQ, kapQ=fup(abs(kapQ)), eF=eF, fF=fF,
                tailexp=fup(abs(tail)), rL1=rL1, lmin=lam[-1] / lam[0], dTX=dTX, dTXY=dTXY, Qb=Qb, RQb=RQb, q_r5=fup(q_r5))

def interval(J0, h):
    t0 = time.time()
    J0f = float(J0)
    Jlo, Jhi = J0f - h, J0f + h
    A0 = o3lib3.assemble_derivs(Q, states, arb(J0f), 2)
    P = point_fast(A0, J0f, h)
    S1 = mat_mr(A0['S1'])
    lamf = P['lam']; Qf = P['Qm']
    phic = [Qf[:, k].copy() for k in range(4)]
    if phic[0][i000] < 0:          # the |000> component of the Perron vector is positive (signed basis: not the sum)
        phic[0] = -phic[0]
    # ---- scaled matrix Taylor models: X(J0 + t) e^{-kap t} linv (eigenvalue ratios, signs and all class data are
    #      invariant under this positive J-dependent factor) ----
    linv = 1.0 / float(lamf[0])
    kap = float(phic[0] @ (S1.c @ phic[0])) * linv
    Kb = arb(kap)
    Ee = (-(Kb * arb(0, h))).exp()
    eEup = fup(Ee)
    sc = linv * eEup * INF                       # >= the scale factor linv e^{-kap t} over I
    # third derivatives over I of the scaled matrices, assembled with the log-derivative shifted by kap
    AI = o3lib3.assemble_derivs(Q, states, arb(J0f, h), 3, kshift=kap, fac=Ee * arb(linv))
    tasm = time.time() - t0
    # mean-value sharpening of the energies r: X2(I) in X2(J0) +/- h|X3(I)|, X1(I) in X1(J0) +/- h|X2(I)|, X(I) in X(J0) +/- h|X1(I)|
    def shp3(x0, x1, x2, x3):
        c2 = 0.5 * (x2.lo + x2.hi); r2 = 0.5 * (x2.hi - x2.lo) + h * x3.absmax() + 2 * U64 * (np.abs(x2.lo) + np.abs(x2.hi))
        c1 = 0.5 * (x1.lo + x1.hi); r1 = 0.5 * (x1.hi - x1.lo) + h * (np.abs(c2) + r2) + 2 * U64 * (np.abs(x1.lo) + np.abs(x1.hi))
        c0 = 0.5 * (x0.lo + x0.hi); r0 = 0.5 * (x0.hi - x0.lo) + h * (np.abs(c1) + r1) + 2 * U64 * (np.abs(x0.lo) + np.abs(x0.hi))
        return MR(c0, r0 * INF), MR(c1, r1 * INF), MR(c2, r2 * INF)
    SHr = {tau: shp3(A0['r'][tau], A0['r1'][tau], A0['r2'][tau], AI['r3'][tau]) for tau in ('t', 'h', 'bb')}
    def mtm(nm):
        M0, M1_, M2 = mat_mr(A0[nm]), mat_mr(A0[nm + '1']), mat_mr(A0[nm + '2'])
        T0 = M0.scale(linv)
        T1 = (M1_ - M0.scale(kap)).scale(linv)
        T2 = (M2.scale(0.5) - M1_.scale(kap) + bscale(M0, Kb * Kb / 2)).scale(linv)
        T3 = mat_mr(AI[nm + '3']).scale(1.0 / 6.0)
        return (T0, T1, T2, T3, mtm_prange(T0, T1, T2, h))
    St, TXt, TYt, TXYt = mtm('S'), mtm('TX'), mtm('TY'), mtm('TXY')
    T0m, T1m, T2m, T3m = St[:4]
    def mtm_norm(Mt):
        """row-sum bound of |X~(J)| over I (symmetric matrices: >= the operator norm)"""
        return float(np.max(np.sum(Mt[4].absup() + h ** 3 * Mt[3].absup(), axis=1))) * INF
    # ---- eigen-data over I: second-order moving frame v_k(t) = p_k + t w_k + t^2 w2_k (Rayleigh-Schroedinger
    #      coefficients of S~(t) = T0 + t T1 + t^2 T2 + ..., computed in float; any smooth frame is admissible) ----
    lt = lamf * linv
    zv = np.zeros(nS); z = zero_mr(nS)
    VF, ws, rhos, rk_h, r0s, dens, rco = [], [], [], [], [], [], []
    nr = lambda x: float(np.linalg.norm(x.absup())) * INF
    for k in range(4):
        p = phic[k]
        dl = lt[k] - lt; dl[k] = 1.0
        g1 = T1m.c @ p
        l1 = float(p @ g1)
        cf = (Qf.T @ g1) / dl; cf[k] = 0.0
        w = Qf @ cf; w = w - (p @ w) * p
        g2 = T1m.c @ w - l1 * w + T2m.c @ p
        cf = (Qf.T @ g2) / dl; cf[k] = 0.0
        w2 = Qf @ cf; w2 = w2 - (p @ w2) * p
        v = VT(MR(p, zv), MR(w, zv), MR(w2, zv), z)
        Sv = vt_mv(St, v, h)
        num = vt_dot(v, Sv, h); den = vt_dot(v, v, h)
        rho = num * den.inv()
        # residual of mu(t) = c0 + c1 t + c2 t^2 + c3 t^3 (float midpoints of the Rayleigh TM2); |S v - rho v| <= |S v - mu v|
        mu = TM2(float(rho.a0.mid()), float(rho.a1.mid()), float(rho.a2.mid()), float(rho.R.mid()), h)
        r = Sv - vt_smul(mu, v, h)
        r0s.append(nr(r.c0))
        rco.append((nr(r.c0), nr(r.c1), nr(r.c2), nr(r.R)))
        rk_h.append((nr(r.c0) + h * nr(r.c1) + h * h * nr(r.c2) + h ** 3 * nr(r.R)) * INF)
        VF.append(v); ws.append(w); rhos.append(rho); dens.append(den)
    # lam_5 over I: min-max on the complement of p_1..p_4.  For unit x orthogonal to the p_k:
    #   x^T T0 x <= lam~_5 + lam~_1 sum_k sin^2(p_k, phi_k),  x^T T1 x = x^T Qc T1 Qc x (Qc = I - Phi Phi^T),
    #   |x^T (T2 + t T3(t)) x| <= rowsum(|T2| + h |T3|).
    Phi = np.array(phic).T
    Qc = np.eye(nS) - Phi @ Phi.T
    aQc = np.abs(Qc)
    M1 = Qc @ T1m.c @ Qc
    gam = (nS + 4) * U64 / (1 - (nS + 4) * U64)
    M1abs = (np.abs(M1) + aQc @ T1m.r @ aQc + 3 * gam * (aQc @ np.abs(T1m.c) @ aQc)) * (1 + 1e-10)
    q1norm = float(np.max(np.sum(M1abs, axis=1))) * (1 + 1e-9)
    t2norm = float(np.max(np.sum(T2m.absup() + h * T3m.absup(), axis=1))) * INF
    enc = [(e[0] * linv - abs(e[0] * linv) * 1e-15, e[1] * linv + abs(e[1] * linv) * 1e-15) for e in P['encl']]   # scaled point enclosures at J0 (outward)
    th0 = []
    dist = lambda x, e: max(e[0] - x, x - e[1], 0.0)
    for k in range(4):
        r0c = float(rhos[k].a0.mid())
        dk = min(dist(r0c, enc[j]) for j in range(nS) if j != k) - fup(abs(rhos[k].a0 - r0c))
        th0.append(r0s[k] / max(dk, 1e-300) * (1 + 1e-12))
    lam5_hi = enc[4][1] + enc[0][1] * sum(x * x for x in th0) * INF + h * q1norm + h * h * t2norm
    S0c = mat_mr(A0['S']).c; S0c = 0.5 * (S0c + S0c.T); opchk = []
    for nm in ('TX', 'TXY'):            # numerical check of -S <= T_X, T_XY <= S (not used in the bounds)
        Mc = mat_mr(A0[nm]).c; Mc = 0.5 * (Mc + Mc.T)
        opchk.append(min(np.linalg.eigvalsh(S0c - Mc)[0], np.linalg.eigvalsh(S0c + Mc)[0]) / float(lamf[0]))
    say('   residual coefficients (r0, r1, r2, r3) per mode: %s; |Qc T1 Qc| <= %.3e; |T2 + t T3| <= %.3e; eF %.1e fF %.1e; lam_min/lam_1 = %.2e; min eig (S -+ T_X, S -+ T_XY)/lam_1 = %.2e %.2e'
        % (' ; '.join('%.1e %.1e %.1e %.1e' % c for c in rco), q1norm, t2norm, P['eF'], P['fF'], P['lmin'], opchk[0], opchk[1]))
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
    eps_vs, cQs, taus = P['eps_v'] * sc, P['cQ'] * sc, P['tau_inf'] * sc      # truncation constants, scaled
    # n3: the Schur-complement bounds below need lam_k^S > tau_inf (k = 1..4) and lam_5^S (upper bound) > tau_inf
    if not (min(rhos[k].lower() for k in range(4)) > taus and lam5_hi > taus):
        say('   lam^S not above tau_inf: Schur bounds unavailable'); return None
    # T >= 0 (S1 for the full model) gives |PTQ| <= sqrt(|PTP| |QTQ|) <= sqrt((lam_1^S + eps_v) tau_inf): sharper than the
    # Schur constant when lam_1 < e^{2J} k_0^3
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
    # ordering pointwise in J: differences of the eigenvalue Taylor models
    order_ok = (lamT[0] - lamT[1]).lower() > 0 and (lamT[1] - lamT[2]).lower() > 0 and (lamT[2] - lamT[3]).lower() > 0 and l_lo[3] > lam5_full
    # rotation bounds: frame vs eigenvectors of the truncated S (Davis-Kahan), plus label truncation (Q-component
    # cQ/(lam - tau) and P-part rotation by the Schur perturbation eps_v + cQ^2/(lam - tau))
    th_tr = [(cQs / max(l_lo[k] - taus, 1e-300) + (eps_vs + cQs ** 2 / max(l_lo[k] - taus, 1e-300)) / gaps[k]) * INF for k in range(4)]
    theta = [(rk_h[k] / (gaps[k] * math.sqrt(max(dens[k].lower(), 1e-300))) + th_tr[k]) * INF for k in range(4)]
    # block of modes 2-4: subspace angle by Davis-Kahan sin(Theta) <= |S V - V M|_F / delta_B (V the orthonormalized frame)
    resB = math.sqrt(sum((rk_h[k] / math.sqrt(max(dens[k].lower(), 1e-300))) ** 2 for k in (1, 2, 3))) * INF
    deltaB = min((lamT[0] - lamT[1]).lower(), l_lo[3] - lam5_full) - 2 * resB
    if deltaB <= 0:
        say('   block separation not certified'); return None
    thB_tr = (cQs / max(l_lo[3] - taus, 1e-300) + (eps_vs + cQs ** 2 / max(l_lo[3] - taus, 1e-300)) / deltaB) * INF
    r21 = l_hi[1] / l_lo[0]; r51_4 = lam5_full / l_lo[3]; r51_3 = lam5_full / l_lo[2]
    x22_4 = l_hi[1] ** 2 / (l_lo[0] * l_lo[3]); x22_3 = l_hi[1] ** 2 / (l_lo[0] * l_lo[2])
    say('J in [%.6f, %.6f] (J0=%s, h=%g): assembly %.1fs; parities %s; |w_k| %s; gaps over I %s; rotation theta %s'
        % (Jlo, Jhi, J0, h, tasm, ' '.join('%+.0f' % p for p in P['par'][:4]), ' '.join('%.2f' % float(np.linalg.norm(w)) for w in ws), ' '.join('%.3e' % g for g in gaps), ' '.join('%.2e' % x for x in theta)))
    say('   (C1) ordering over I: %s; (C2) min over I of (lam2+lam4-2lam3)/lam1 >= %.5f (scaled lam1 in [%.5f, %.5f]); lam5/lam1 <= %.4e; lam2/lam1 <= %.4f'
        % (order_ok, conv_lo / l_hi[0], l_lo[0], l_hi[0], lam5_full / l_lo[0], r21))
    def dtm(x0, x1, x2, x3):
        d0, d1, d2, d3 = MR.iv(x0), MR.iv(x1), MR.iv(x2).scale(0.5), MR.iv(x3).scale(1.0 / 6.0)
        return (d0, d1, d2, d3, mtm_prange(d0, d1, d2, h))
    rt = {tau: dtm(A0['r'][tau], A0['r1'][tau], A0['r2'][tau], AI['r3'][tau]) for tau in ('t', 'h', 'bb')}
    bvt = VT(MR.iv(A0['b']), MR.iv(A0['b1']), MR.iv(A0['b2']).scale(0.5), MR.iv(AI['b3']).scale(1.0 / 6.0))
    # normalizations of the frame vectors v_l(t) (exact polynomials)
    den2 = dens
    nrm2 = [den2[l].invsqrt() for l in range(4)]
    sq0 = den2[0].sqrt()
    phi0 = vt_smul(nrm2[0], VF[0], h)                # unit frame vector phi_0(t)
    # class vectors rescaled at every step by an EXACT positive polynomial q(t) ~ 1/<phi_0, y(t)> (float coefficients, no
    # remainder): all class data are invariant under positive factors; the rescaling keeps the Taylor coefficients bounded
    # in i, and (unlike a Taylor-model division) it feeds no remainder back
    def qpoly(nn):
        iv = nn.inv()
        q = TM2(float(iv.a0.mid()), float(iv.a1.mid()), float(iv.a2.mid()), 0, h)
        if not (q.lower() > 0):
            raise ValueError('rescaling polynomial not positive')
        return q
    xs = [vt_smul(qpoly(vt_dot(phi0, bvt, h)), bvt, h)]
    qst = [None]; nst = [None]                        # q_j and a_j = <phi_0, S x_{j-1}>/<phi_0, x_{j-1}>
    for i in range(I + 1):
        y = vt_mv(St, xs[-1], h)
        qj = qpoly(vt_dot(phi0, y, h))
        qst.append(qj)
        nst.append(vt_dot(phi0, y, h) * vt_dot(phi0, xs[-1], h).inv())
        xs.append(vt_smul(qj, y, h))
    cxs = [max(abs(vt_dot(phi0, x, h).lower()), abs(vt_dot(phi0, x, h).upper())) for x in xs]   # <phi_0, x_i> <= cxs[i]
    classes = []
    for tau in ('t', 'h', 'bb'):
        for i in range(I + 2):
            classes.append(('%s@%d' % (tau, i), tau, i, xs[i], vt_dm(rt[tau], xs[i], h)))
    for vt, Tt in (('a', TXt), ('b', TYt)):
        for j in range(1, I + 2):
            classes.append(('%s@%d' % (vt, j), vt, j, xs[j], vt_smul(qst[j], vt_mv(Tt, xs[j - 1], h), h)))
    ef2 = 0.0
    for k in range(4):
        for l in range(4):
            gkl = vt_dot(VF[k], VF[l], h) * nrm2[k] * nrm2[l] - (1 if k == l else 0)
            ef2 += max(abs(gkl.lower()), abs(gkl.upper())) ** 2
    ef = math.sqrt(ef2) * INF
    thq = math.sqrt(sum(x * x for x in theta)) / math.sqrt(1 - ef) * INF
    thB = (resB / math.sqrt(1 - ef) / deltaB + thB_tr) * INF            # block (modes 2-4) subspace angle
    efB = ef * (1 + ef) / (1 - ef) * INF                                 # |Phi Phi^T - P_frame| for the block
    data = {}
    side = {'t': 1, 'a': 1, 'bb': -1, 'b': -1, 'h': 0}
    rmax = max(float(np.max(SHr[tau][0].absup())) for tau in ('t', 'h', 'bb'))
    # |T_X|, |T_XY| <= |S| + (vertical-tail terms): -V <= V_X, V_XY <= V pointwise in spin space (|s.s'| <= 1), so
    # -S <= T_X <= S up to the truncation of the character sums; the row sums are a second, cruder bound
    Tn = min(max(mtm_norm(TXt), mtm_norm(TYt)), l_hi[0] + P['dTX'] * sc)
    TXYn = min(mtm_norm(TXYt), l_hi[0] + P['dTXY'] * sc)
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
                          a_rep=None, alf=alf, nutf=nut_f, du=du, u0lo=uUn, L1v=L1, LEv=LE)
        if typ in ('a', 'b') and pos == I + 1:
            # a = <phi_0, S y>, y = x_{j-1}/<phi_0, x_{j-1}> (for the vertical Lipschitz radius)
            # a = <phi_0, S y> with y = x_{j-1} normalized (<phi_0, y> = 1): the step normalization n_j
            data[name]['a_rep'] = nst[pos].lower()
    # ---- eps(0), geometric decay, deep classes, truncation fuzz ----
    # eps0 bounds |eps(0)| w.r.t. any unit vector within angle theta_0 of the frame, in particular phi_0 of the
    # truncated S; there |eps^S(i)| <= r21^i eps0.  Against phi_0 of the full model (angle <= th_tr[0] from phi_0^S):
    #   |eps(i)| <= 2 (1 + e) |eps^S(i)| / (1 - theta_0 - e)^2 + tan(th_tr[0]),  e = max |eps^S|.
    eps0 = max(dd['neps'] for dd in data.values() if dd['pos'] == 0)
    # ---- label truncation of the class vectors (full model T against truncated S), every term derived (UNIF 9.17) ----
    # X_i - x_i = sum_j T^{i-1-j}(T - S)x_j + T^i Q b with (T - S)x = (PTP - S)x + QTPx, |PTP - S| <= eps_v,
    # |QTP| <= c (T >= 0: c <= ((lam_1^S + eps_v) tau_inf)^{1/2}), |x_j| = u_j |y_j|, u_j = (lam^S)^j u0(b), |y_j| <= 1 + eps0;
    # relative to u_i = (lam^S)^i u0(b), with rho >= lam^T/lam^S:  trel <= i rho^{i-1}(eps_v + c)(1+eps0)/lam + rho^i |Qb|/u0(b).
    # v2-n1: u0(b) = <phi_0^S, b> uses the eigenvector of S; the frame value is lowered by |phi_0^S - phi_0^frame| |b|,
    # with |phi_0^S - phi_0^frame| <= sqrt2 theta_0 (theta_0 bounds the frame angle to the eigenvector)
    u0b = vt_dot(phi0, bvt, h).lower() - SQ2 * theta[0] * vt_norm(bvt, h)
    if not (u0b > 0):
        say('   u0(b) not certified positive'); return None
    rho = (1 + (eps_vs + cQs ** 2 / max(l_lo[0] - taus, 1e-300)) / l_lo[0]) * INF
    ii = I + 2
    trelA = ii * rho ** (ii - 1) * (eps_vs + cQs) / l_lo[0] * (1 + eps0) * INF
    trelB = rho ** ii * P['Qb'] / u0b * INF
    trel = (trelA + trelB) * INF
    # normalized vectors y = x/<phi, x> with phi = phi_0 of the full model: <phi, x> >= u^S kap0 (angle th_tr[0] to phi_0^S)
    kap0 = 1 - th_tr[0] * (1 + eps0)
    yv0 = (1 + eps0) / kap0 * INF                            # |y|
    if not (kap0 - trel > 0.5):
        say('   truncation too large (%.3e)' % trel); return None
    dy = trel * (1 + yv0) / (kap0 - trel) * INF              # |Y - y|
    # R on the perturbation: |R T| <= r_max lam^T + r_Q (c + tau_inf) (T >= 0, r(l)^2 k_l decreasing above L), so transfer
    # steps carry rTf = max(r_max, r(L+1))(1 + (c + tau)/lam); the boundary term carries |R Q b| (i = 0) or rTf |Q b| (i >= 1)
    assert math.isfinite(P['rL1'])
    rQm = max(rmax, P['rL1'])
    rTf = rQm * (1 + (cQs + taus) / l_lo[0]) * INF
    RdLraw = (rTf * rho * trelA + max(P['RQb'], rTf * rho ** ii * P['Qb']) / u0b) * INF
    RdY = (RdLraw + rmax * yv0 * trel) / (kap0 - trel) * INF  # |R (Y - y)|
    # eps(0) of the FULL model (deep positions are bounded inside the full model): |eps^full(0)| <= eps0 + dy
    eps0f = (eps0 + dy) * INF
    den_e = (1 - theta[0] - eps0f) ** 2
    if den_e <= 0.5:
        say('   eps(0) too large for the geometric bound (%.3e)' % eps0f); return None
    geo = lambda i: (2 * (1 + eps0f) * r21 ** i * eps0f / den_e + th_tr[0] / (1 - th_tr[0])) * INF
    for dd in data.values():
        dd['neps'] = min(dd['neps'], geo(dd['pos']))
    # |R phi_l|, |T phi_l| for the full-model eigenvectors: frame value, rotation (theta includes the truncation angle),
    # and the Q-part of phi_l^full = T phi_l/lam_l:  |R_Q phi_l| <= r_Q (c + tau_inf)/lam_l
    Rq = 0.0; Tqa = 0.0
    for l in range(4):
        vl = vt_smul(nrm2[l], VF[l], h)
        for tau in ('t', 'h', 'bb'):
            Rq = max(Rq, (vt_norm(vt_dm(rt[tau], vl, h), h) + rmax * SQ2 * theta[l] + rQm * (cQs + taus) / l_lo[l]) * INF)
        for Tt in (TXt, TYt):
            Tqa = max(Tqa, (vt_norm(vt_mv(Tt, vl, h), h) + l_hi[0] * SQ2 * theta[l] + 2 * cQs + P['dTX'] * sc) * INF)
    Tq = Tqa / l_lo[0]
    # horizontal classes, u~ = R y - <phi, R y> y:  |du~| <= |R dy|(1 + |Y|) + |<R phi, y>| |dy|,
    #   |da_l| <= |dy| |R phi| (1 + |eps| + |dy|) + |<R phi, y>| |dy|  with |<R phi, y>| <= |R phi| |y|
    nfz_h = (RdY * (1 + yv0 + dy) + Rq * yv0 * dy) * INF
    tfz_h = min(nfz_h, dy * Rq * (1 + geo(0) + dy + yv0) * INF)
    # vertical classes, (L1, LE) = (S y', T_X y') with deviations d1 = lam dy + (eps_v + c)|y'|, dE = lam dy + (dTX + 2c)|y'|
    # (|QT_X P| <= 2c from -T <= T_X <= T); u~ = LE/a - e L1/a^2, a = <phi, L1>, e = <phi, LE>, a >= a_lo
    yvf = 1 + geo(0) + SQ2 * theta[0]                        # |y'| for frame-normalized y'
    a_fr = min(nst[j].lower() for j in range(1, I + 2))
    a_lo = (a_fr - SQ2 * theta[0] * l_hi[0] * yvf) / (1 + SQ2 * theta[0] * yvf)
    d1 = (l_hi[0] * dy + (eps_vs + cQs) * yv0) * INF
    dE = (l_hi[0] * dy + (P['dTX'] * sc + 2 * cQs) * yv0) * INF
    a_m = a_lo - d1
    if not (a_m > 0):
        say('   vertical normalization not certified'); return None
    L1n = (l_hi[0] + eps_vs) * yv0; LEn = (l_hi[0] + P['dTX'] * sc) * yv0; e_abs = Tqa * yv0
    nfz_v = (dE / a_m + LEn * d1 / (a_lo * a_m) + dE * (L1n + d1) / a_m ** 2 + e_abs * d1 / a_m ** 2
             + e_abs * L1n * d1 * (2 * a_lo + d1) / (a_lo ** 2 * a_m ** 2)) * INF
    tfz_v = nfz_v
    # raw normalized class vectors (for C6): horizontal (y, R y), vertical (S y'/a, T_X y'/a)
    dv_raw = {'h': (dy, RdY), 'v': ((d1 + L1n * d1 / a_lo) / a_m * INF, (dE + LEn * d1 / a_lo) / a_m * INF)}
    # deep positions i >= I+2, bounded in the full model: y_i = x_i/<phi, x_i> for a unit phi within angle theta_0 of phi_0,
    #   |y_i - y_j| <= 2 (1 + e)(|eps(i)| + |eps(j)|)/(1 - theta_0 - e)^2, |eps(i)| <= (lam2/lam1)^i eps0f.
    e_d = 2 * (1 + eps0f) * (r21 ** (I + 1) + r21 ** (I + 2)) * eps0f / den_e * INF       # y = x_i, i >= I+1
    e_dv = 2 * (1 + eps0f) * (r21 ** I + r21 ** (I + 1)) * eps0f / den_e * INF            # y = x_{j-1}, j >= I+1
    yh = 1 + geo(I + 1) + SQ2 * theta[0]; yv = 1 + geo(I) + SQ2 * theta[0]          # |y| bounds
    Sn = l_hi[0]                                # |S| over I (scaled), full model included
    Tnf = l_hi[0]                               # |T_X|, |T_Y| <= lam_1 in the full model (S2 with no truncation term)
    rT = rTf                                    # |R T| / lam_1 in the full model
    eta_v = 0.0; a_v = float('inf'); am_v = float('inf')
    for dd in data.values():
        if dd['a_rep'] is not None:
            # a = <phi, S y> for the full-model phi: a >= (a_frame - sqrt2 theta_0 |S| |y|)/(1 + sqrt2 theta_0 |y|), minus the
            # truncation change of the representative (|S| dy)
            a = (dd['a_rep'] - SQ2 * theta[0] * Sn * yv) / (1 + SQ2 * theta[0] * yv) - Sn * dy
            am = a - Sn * e_dv
            if am <= 0:
                say('   deep vertical radius: a_min <= 0'); return None
            br = 1 + yv * Sn / am + Sn * (yv + e_dv) / am + yv * Sn / am + yv * yv * Sn * Sn * (2 * a + Sn * e_dv) / (a * a * am)
            eta_v = max(eta_v, Tnf * e_dv / am * br * INF)
            a_v = min(a_v, a); am_v = min(am_v, am)
    # horizontal: u~ = R y - <phi, R y> y with R y = R T y'/a (y' = y_{i-1}), so |R (y_i - y_rep)| <= (|RT|/a_m)(1 + |S||y'|/a)|y'_i - y'_rep|
    dRy = rT * Sn / am_v * (1 + Sn * yv / a_v) * e_dv
    eta_h = (dRy * (1 + yh + e_d) + rT * Sn * yv / a_v * e_d) * INF
    neps_deep = geo(I + 1)
    for name, dd in data.items():
        vert = dd['typ'] in ('a', 'b')
        etad = (eta_v if vert else eta_h) if dd['pos'] == I + 1 else 0.0
        tfz_c, nfz_c = (tfz_v, nfz_v) if vert else (tfz_h, nfz_h)
        dd['al'] = [a.addball(tfz_c + etad) for a in dd['al']]
        dd['nut'] += nfz_c + etad; dd['q5'] += nfz_c + etad
        dd['dB'] = (dd['du'] + nfz_c + etad) * INF          # |u~(true, full model, any deep position) - u~(frame)|
        dd['neps'] = (neps_deep if dd['pos'] == I + 1 else dd['neps']) + dy
    tfz, nfz = max(tfz_h, tfz_v), max(nfz_h, nfz_v)
    say('   classes: eps(0) <= %.4e; deep radii: horizontal %.2e, vertical %.2e; truncation: trel %.2e, |dy| %.2e; mode fuzz h %.2e v %.2e, norm fuzz h %.2e v %.2e (Rq %.2f, Tq %.2f); frame Gram dev %.1e; block angle %.2e; r^2 k ratio above L <= %.3f'
        % (eps0, eta_h, eta_v, trel, dy, tfz_h, tfz_v, nfz_h, nfz_v, Rq, Tq, ef, thB, P['q_r5']))
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
                # F(0) = <P_B u~_X, P_B u~_Y> is invariant under rotations inside the block of modes 2-4: frame values plus
                # the block subspace angle, independent of the (small at weak J) gaps inside the block
                aX, aY = dX['alf'], dY['alf']
                FB = (aX[0] * aY[0] + aX[1] * aY[1] + aX[2] * aY[2]).lower()
                nX, nY = dX['nutf'], dY['nutf']
                FB -= ((efB + thB) * nX * nY + dX['dB'] * (nY + dY['dB']) + dY['dB'] * nX) * INF
                F0 = max(F0, FB)
                if wF0 is None or F0 < wF0[0]:
                    wF0 = (F0, X, Y)
                if wpp is None or pp < wpp[0]:
                    wpp = (pp, X, Y)
                base, ra, rb = F0, r51_3, x22_3
            else:
                base = (p2 + p4).lower()
                if wsame is None or base < wsame[0]:
                    wsame = (base, X, Y)
                ra, rb = r51_4, x22_4
            m = 0
            while base <= 0 or q55 * ra ** m + AA * rb ** m >= base:
                m += 1
                if m > 60:
                    break
            m0 = max(m0, m)
            if m > 0:
                need[(X, Y)] = m if base > 0 else 99
            sf = base / max(q55 + AA, 1e-300)
            if wsf is None or sf < wsf[0]:
                wsf = (sf, X, Y)
    # ---- (C6): direct evaluation of Cov Z^2 = A D - B C for the pairs (and distances m) below their dominance threshold ----
    # A = <LE_X, S^m RE_Y>, B = <LE_X, S^m R1_Y>, C = <L1_X, S^m RE_Y>, D = <L1_X, S^m R1_Y> (right classes = mirrored left ones);
    # the right vectors are propagated with a common positive normalization per step, which keeps the sign of A D - B C.
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
                        a1 += e_d; aE += dRy                 # R smoothed by one transfer step (full model)
                cmx = nl1[nm]                        # scale of the stored vectors: <phi, L1> <= |L1|
                return a1 * cmx * INF, aE * cmx * INF
            prop = {}
            def right(nm, m):       # (r1, rE, |r1|, |rE|, d1, dE) after m normalized steps
                if (nm, m) in prop:
                    return prop[(nm, m)]
                if m == 0:
                    d1, dE = dev(nm)
                    out = (data[nm]['L1v'], data[nm]['LEv'], nl1[nm], nlE[nm], d1, dE)
                else:
                    r1, rE, n1, nE, d1, dE = right(nm, m - 1)
                    y1, yE = vt_mv(St, r1, h), vt_mv(St, rE, h)
                    ni = qpoly(vt_dot(phi0, y1, h)); qup = ni.upper()     # exact positive polynomial rescaling
                    g = Sn * qup; tr = (eps_vs + cQs) * qup
                    r1n, rEn = vt_smul(ni, y1, h), vt_smul(ni, yE, h)
                    out = (r1n, rEn, vt_norm(r1n, h), vt_norm(rEn, h), (g * d1 + tr * n1) * INF, (g * dE + tr * nE) * INF)
                prop[(nm, m)] = out
                return out
            for (X, Y), mXY in need.items():
                lX1, lXE = data[X]['L1v'], data[X]['LEv']; dX1, dXE = dev(X)
                for m in range(mXY):
                    if m == 0 and data[X]['typ'] == data[Y]['typ'] and data[X]['typ'] in ('t', 'h', 'bb'):
                        continue                # the same horizontal edge
                    r1, rE, n1, nE, d1, dE = right(Y, m)
                    A = vt_dot(lXE, rE, h).addball(dXE * nE + nlE[X] * dE + dXE * dE)
                    B = vt_dot(lXE, r1, h).addball(dXE * n1 + nlE[X] * d1 + dXE * d1)
                    C = vt_dot(lX1, rE, h).addball(dX1 * nE + nl1[X] * dE + dX1 * dE)
                    D = vt_dot(lX1, r1, h).addball(dX1 * n1 + nl1[X] * d1 + dX1 * d1)
                    mn = (A * D - B * C).lower(); nD = (D * D).lower()
                    n6 += 1
                    if not (mn > 0):
                        neg6 += 1
                    if w6 is None or mn / max(nD, 1e-300) < w6[0]:
                        w6 = (mn / max(nD, 1e-300), X, Y, m)
            c6ok = neg6 == 0
    # ---- same-column (a, b) pairs: Cov Z^2 = <l, TXY r><l, S r> - <l, TX r><l, TY r> with normalized l, r ----
    lv = {}
    for i in range(I + 2):
        lv[i] = xs[i]                                # already normalized, <phi_0, x_i> = 1
    nl = {i: vt_norm(lv[i], h) for i in lv}
    Mts = {'TXY': TXYt, 'S': St, 'TX': TXt, 'TY': TYt}
    Mn = {'S': Sn, 'TX': Tn, 'TY': Tn, 'TXY': TXYn}
    Mr = {(k, i): vt_mv(Mts[k], lv[i], h) for k in Mts for i in lv}
    # truncation fuzz of a normalized bilinear form: vertical tails (r-weighted) plus class-vector truncation
    rv = P['rL1'] + 1.0
    # perturbation of <l, M r>: the P-block change of M by the vertical tail (<= eps_v rv^2 for all four M) plus the
    # class-vector truncation against the FULL-model operator, whose norm is <= lam_1 for S, T_X, T_Y, T_XY (S1, S2)
    Mfull = l_hi[0] * INF
    vtail = {'S': eps_vs, 'TX': P['dTX'] * sc, 'TY': P['dTX'] * sc, 'TXY': P['dTXY'] * sc}   # |M^full_PP - M| (vertical tails)
    eM = {k: vtail[k] * INF for k in Mts}
    negc = 0; wc = None; DBG7 = []
    for iL in range(I + 2):
        for iR in range(I + 2):
            vals = {}
            for k in Mts:
                v = vt_dot(lv[iL], Mr[(k, iR)], h)
                e = eM[k] * nl[iL] * nl[iR]
                dL = (dy + (e_d if iL == I + 1 else 0.0)) * nl[iL]      # truncation (|dy|) plus deep deviation, at the stored scale
                dR = (dy + (e_d if iR == I + 1 else 0.0)) * nl[iR]
                e += Mfull * (dL * (nl[iR] + dR) + nl[iL] * dR) * INF
                vals[k] = v.addball(e)
            cv = vals['TXY'] * vals['S'] - vals['TX'] * vals['TY']
            if not math.isfinite(cv.lower()) and not DBG7:
                DBG7.append(1)
                say('      [C7 debug] (%d,%d): nl %.3e %.3e; eM %s; Mn %s; vals %s' % (iL, iR, nl[iL], nl[iR], {k: '%.2e' % eM[k] for k in eM}, {k: '%.2e' % Mn[k] for k in Mn}, {k: (vals[k].a0.str(3), vals[k].a1.str(3), vals[k].a2.str(3), vals[k].R.str(3)) for k in vals}))
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
    # MINOR-1: (C5) carries the dominance from m0 to every m >= m0 only if both ratios are < 1 (lam5/lam4 < 1 is in
    # order_ok; lam2^2/(lam1 lam3) <= lam2^2/(lam1 lam4))
    x22_ok = x22_4 * INF < 1
    closed = order_ok and conv_lo > 0 and ok2 and ok3 and ok4 and wpp[0] > 0 and wF0[0] > 0 and wsame[0] > 0 and (m0 == 0 or c6ok) and negc == 0 and x22_ok
    say('   ==> interval [%.6f, %.6f]: %s (%.1fs)' % (Jlo, Jhi, 'CERTIFIED' if closed else 'NOT certified', time.time() - t0))
    return dict(closed=closed, F0=wF0[0], pp=wpp[0], sf=wsf[0], c7=wc[0], conv=conv_lo / l_hi[0], m0=m0)

if not ADAPT:
    for (J0, h) in ivals:
        interval(J0, h)
else:
    # adaptive cover of [JS, JE]: intervals [J0 - h, J0 + h] with J0 - h = a - ovl h below the current lower end a,
    # h = q J0; q grows by 1.25 after a success (<= qmax) and halves after a failure; ledger lines are appended.
    JS, JE, q, qmax = ADAPT
    LEDGER = os.path.join(BASE, 'out', 'o3cover2_%s.ledger' % tag.split('_')[0])
    assert '/pkg_n3/out/' in LEDGER
    a = JS; ovl = 0.02; budget = 500.0
    while a < JE and time.time() - t00 < budget:
        h = q * a / (1 - q * (1 - ovl))
        J0f = a + (1 - ovl) * h
        try:
            res = interval(Fraction(J0f), h)
        except (ZeroDivisionError, ValueError) as ex:
            say('   interval J0=%r h=%r: exception %s' % (J0f, h, ex)); res = None
        ok = bool(res and res['closed'])
        with open(LEDGER, 'a') as f:
            if res:
                f.write('%r %r %d %d %s F0=%.4e pp=%.4e sf=%.3e c7=%.4e conv=%.5f m0=%d job=%s\n' % (J0f, h, L, I, 'CERT' if ok else 'FAIL', res['F0'], res['pp'], res['sf'], res['c7'], res['conv'], res['m0'], tag))
            else:
                f.write('%r %r %d %d FAIL early job=%s\n' % (J0f, h, L, I, tag))
        if ok:
            a = J0f + h
            q = min(q * 1.15, qmax)
        else:
            q = q / 1.6
            if q < 1e-4:
                say('adaptive cover stopped: q too small at a = %r' % a); break
    say('adaptive cover: reached a = %r (target %r), last q = %.4g' % (a, JE, q))
say('total %.1fs' % (time.time() - t00))
