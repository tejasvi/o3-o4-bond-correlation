# Certified (ball arithmetic) objects for the uniform 3-row strip transfer at a given J (wave 18 pilot).
# Symmetric transfer on admissible cut states s = (t, h, bb) with labels <= L:
#   S = C^{1/2} M C^{1/2},  M = column map (squared 6j symbols, verticals a, b <= L, hub g <= 2L), C(s) = W_t W_h W_bb,
#   W_l = (l+1) k_l(J), k_l = 2 I_{l+1}(J)/J (unscaled).  M is symmetric (mirror symmetry of the column).
#   Z(P3 x Pn) = <b, S^{n-2} b>,  b(s) = C(s)^{1/2} k_t k_bb  (end column with the corner verticals; STRIPW 1.2).
#   Energies: R_tau = diag r(label_tau) for horizontals; T_X = C^{1/2} M_X C^{1/2} (vertical a weighted by r(a)),
#   T_Y the same for b.  r(l) = d/dJ log k_l = I_{l+2}/I_{l+1} + l/J.
import sys
from fractions import Fraction
sys.path.insert(0, '/mnt/g2/release/root/data/e15/dy4/scratch/code')
from su2lib import sixj_sq, adm
from flint import arb, arb_mat, fmpq


def bessel_data(J, nmax, Jrad=0.0):
    Ja = arb(fmpq(J.numerator, J.denominator)) if isinstance(J, Fraction) else J
    if Jrad:
        Ja = Ja + arb(0, Jrad)
    I = [Ja.bessel_i(l) for l in range(nmax + 3)]
    k = [2 * I[l + 1] / Ja for l in range(nmax + 1)]
    W = [(l + 1) * k[l] for l in range(nmax + 1)]
    r = [I[l + 2] / I[l + 1] + arb(l) / Ja for l in range(nmax + 1)]
    return Ja, k, W, r


def build(L, J, Jrad=0.0):
    """Returns dict with states, S, TX, TY, b, C, r-diagonals (all arb), and the Bessel data."""
    n_ = L + 1
    gcap = 2 * L
    states = [(t, h, bb) for t in range(n_) for h in range(n_) for bb in range(n_) if adm(t, h, bb)]
    sidx = {s: i for i, s in enumerate(states)}
    nS = len(states)
    Ja, k, W, r = bessel_data(J, L, Jrad)
    A1 = {s: [] for s in range(nS)}      # input state -> list of (F1 key, exact 6j^2 * (g+1), a)
    for bb in range(n_):
        for g in range(gcap + 1):
            for tp in range(n_):
                if not adm(bb, g, tp):
                    continue
                for a in range(n_):
                    for t in range(n_):
                        if not adm(a, t, tp):
                            continue
                        for h in range(n_):
                            if not (adm(bb, t, h) and adm(a, g, h)):
                                continue
                            v = sixj_sq(bb, g, tp, a, t, h)
                            if v:
                                A1[sidx[(t, h, bb)]].append(((bb, g, tp), v * (g + 1), a))
    A2 = {}                              # F1 key -> list of (output state, exact 6j^2, b)
    for tp in range(n_):
        for hp in range(n_):
            for bbp in range(n_):
                if not adm(tp, hp, bbp):
                    continue
                for b in range(n_):
                    for bb in range(n_):
                        if not adm(b, bb, bbp):
                            continue
                        for g in range(gcap + 1):
                            if not (adm(tp, bb, g) and adm(b, hp, g)):
                                continue
                            v = sixj_sq(tp, hp, bbp, b, bb, g)
                            if v:
                                A2.setdefault((bb, g, tp), []).append((sidx[(tp, hp, bbp)], v, b))
    q = lambda v: arb(fmpq(v.numerator, v.denominator))
    def colmap(wa, wb):
        Mx = arb_mat(nS, nS)
        for s in range(nS):
            acc = {}
            for (key, v1, a) in A1[s]:
                c1 = q(v1) * wa[a]
                for (sp, v2, b) in A2.get(key, ()):
                    acc[sp] = acc.get(sp, arb(0)) + c1 * q(v2) * wb[b]
            for sp, val in acc.items():
                Mx[sp, s] = val
        return Mx
    WrA = [W[a] * r[a] for a in range(n_)]
    M = colmap(W, W)
    MX = colmap(WrA, W)
    MY = colmap(W, WrA)
    MXY = colmap(WrA, WrA)
    C = [W[t] * W[h] * W[bb] for (t, h, bb) in states]
    sq = [c.sqrt() for c in C]
    def sym(Mx):
        S = arb_mat(nS, nS)
        for i in range(nS):
            for j in range(nS):
                x = Mx[i, j]
                if not x.is_zero():
                    S[i, j] = sq[i] * x * sq[j]
        return S
    S, TX, TY, TXY = sym(M), sym(MX), sym(MY), sym(MXY)
    bvec = [sq[i] * k[states[i][0]] * k[states[i][2]] for i in range(nS)]
    rdiag = {'t': [r[s[0]] for s in states], 'h': [r[s[1]] for s in states], 'bb': [r[s[2]] for s in states]}
    return dict(L=L, J=J, Ja=Ja, states=states, nS=nS, S=S, TX=TX, TY=TY, TXY=TXY, b=bvec, C=C, k=k, W=W, r=r, rdiag=rdiag)


def matvec(A, x):
    n = A.nrows()
    out = []
    for i in range(n):
        acc = arb(0)
        for j in range(A.ncols()):
            a = A[i, j]
            if not a.is_zero():
                acc += a * x[j]
        out.append(acc)
    return out


def dot(x, y):
    acc = arb(0)
    for a, b in zip(x, y):
        acc += a * b
    return acc


def norm(x):
    return dot(x, x).sqrt()
