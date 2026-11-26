# J-independent structure (exact 6j^2 values as arb balls) and per-J assembly of the certified 3-row transfer.
# Same conventions as certlib.py; build_struct does the expensive exact 6j part once, assemble(struct, J) is cheap.
import sys
from fractions import Fraction
sys.path.insert(0, '/mnt/g2/release/root/data/e15/dy4/scratch/code')
from su2lib import sixj_sq, adm
from flint import arb, arb_mat, fmpq
from certlib import bessel_data


def build_struct(L):
    n_ = L + 1
    gcap = 2 * L
    states = [(t, h, bb) for t in range(n_) for h in range(n_) for bb in range(n_) if adm(t, h, bb)]
    sidx = {s: i for i, s in enumerate(states)}
    q = lambda v: arb(fmpq(v.numerator, v.denominator))
    A1 = {s: [] for s in range(len(states))}
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
                                A1[sidx[(t, h, bb)]].append(((bb, g, tp), q(v * (g + 1)), a))
    A2 = {}
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
                                A2.setdefault((bb, g, tp), []).append((sidx[(tp, hp, bbp)], q(v), b))
    return dict(L=L, states=states, sidx=sidx, A1=A1, A2=A2)


def assemble(st, J, Jrad=0.0):
    L, states = st['L'], st['states']
    nS = len(states)
    n_ = L + 1
    Ja, k, W, r = bessel_data(J, L, Jrad)
    M = arb_mat(nS, nS); MX = arb_mat(nS, nS); MY = arb_mat(nS, nS); MXY = arb_mat(nS, nS)
    for s in range(nS):
        acc = {}
        for (key, v1, a) in st['A1'][s]:
            c1 = v1 * W[a]
            for (sp, v2, b) in st['A2'].get(key, ()):
                w = c1 * v2 * W[b]
                e = acc.get(sp)
                if e is None:
                    acc[sp] = [w, w * r[a], w * r[b], w * r[a] * r[b]]
                else:
                    e[0] += w; e[1] += w * r[a]; e[2] += w * r[b]; e[3] += w * r[a] * r[b]
        for sp, e in acc.items():
            M[sp, s] = e[0]; MX[sp, s] = e[1]; MY[sp, s] = e[2]; MXY[sp, s] = e[3]
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
