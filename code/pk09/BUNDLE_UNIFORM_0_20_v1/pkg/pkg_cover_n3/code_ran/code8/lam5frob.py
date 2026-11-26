# Wave 18, checkpoint 2 (UNIF 9.26, RV11_25; v2 error model for signed factors, UNIF 9.30): lambda_5 bound over I = [J0 - h, J0 + h] from the deflated Taylor
# model of the scaled transfer S~(t) = S(J0 + t) e^{-kap t}/lam0 (Weyl, lambda_5 <= sigma_5, Eckart-Young-Mirsky):
#   lambda_5(S~(t)) <= sum_{n<=2} h^n |T_n - F_n|_F + sum_{n=3}^{6} h^n |F_n|_F + h^3 sup_t |R(t)|_2,
# F(t) = sum_k c_k(t) v_k(t) v_k(t)^T (rank <= 4, moving frame).  |T_n - F_n|_F from dense column blocks of the float
# centre T~_n (blocked sparse-sparse products A2^(j) A1^(k)[:, block], j + k <= 2), plus the entrywise error bound
# |T_n - T~_n| <= E_n entrywise (telescoped factor radii, v2), |E_n|_F <= sqrt(nA) max rowsum; |R(t)|_2 <= max_i
# r_i/(6 u_i) (Collatz-Wielandt), r = radius of the tight order-3 interval operator applied to the box [-u, u].
import math
import numpy as np
from mfops import MR

U = 2.0 ** -53
INF = 1 + 1e-12


def lam5_frob(st, PT, BL, frames, cks, h, block=600):
    """frames: 4 tuples (p, w, w2) of float cube vectors (v_k(t) = p + t w + t^2 w2); cks: 4 tuples (c0, c1, c2) of
    floats (c_k(t)); PT: shifted point OpSet (order >= 2, fac = 1/lam0); BL: tight interval OpSet (order >= 3)"""
    aidx = np.nonzero(st['adm'])[0]; nA = len(aidx)
    A1 = {k: PT.A1[('p', k)].Mc.tocsc()[:, aidx] for k in range(3)}
    A2 = {j: PT.A2[('p', j)].Mc.tocsr()[aidx, :] for j in range(3)}
    Dr = {l: PT.Dc[l][aidx] for l in range(3)}
    Dl = {i: PT.Dlc[i][aidx] for i in range(3)}
    V = [[np.asarray(v)[aidx] for v in fr] for fr in frames]
    C = [list(c) for c in cks]
    fact = math.factorial
    terms = {n: [(i, j, k, n - i - j - k, 1.0 / (fact(i) * fact(j) * fact(k) * fact(n - i - j - k)))
                 for i in range(n + 1) for j in range(n + 1 - i) for k in range(n + 1 - i - j)] for n in range(3)}
    acc = [0.0, 0.0, 0.0]
    for b0 in range(0, nA, block):
        B = slice(b0, min(b0 + block, nA))
        Z = {(j, k): (A2[j] @ A1[k][:, B]).toarray() for j in range(3) for k in range(3) if j + k <= 2}
        for n in range(3):
            T = np.zeros((nA, B.stop - B.start))
            for (i, j, k, l, cf) in terms[n]:
                T += cf * (Dl[i][:, None] * Z[(j, k)] * Dr[l][None, B])
            for kk in range(4):
                for a in range(3):
                    for b in range(3):
                        c = n - a - b
                        if 0 <= c <= 2:
                            T -= C[kk][a] * np.outer(V[kk][b], V[kk][c][B])
            acc[n] += float(np.sum(T * T))
    fro = [math.sqrt(x * (1 + (nA * nA + 8) * U)) * INF for x in acc]
    # entrywise error of T~_n (v2, valid for signed factors): for each term X Y Z W = Dl^(i) A2^(j) A1^(k) D^(l), telescoping
    # |X Y Z W - X' Y' Z' W'| <= |dX| |Y| |Z| |W| + |X'| |dY| |Z| |W| + |X'| |Y'| |dZ| |W| + |X'| |Y'| |Z'| |dW| with
    # |A| <= Mabs, |dA| <= Mrg (SpMR), |D| <= |Dc| + D.r, |dD| <= D.r, plus the product rounding (gamma_K + 8 u) |X'||Y'||Z'||W'|;
    # the row sums E_n 1 come from sparse products with these nonnegative matrices; |E_n|_F <= sqrt(nA) max_i (E_n 1)_i
    K = max(PT.A2[('p', k)].rowcount for k in range(3))
    gK = K * U / (1 - K * U)
    Du = {l: np.abs(PT.D[l].c) + PT.D[l].r for l in range(3)}; Dr = {l: PT.D[l].r for l in range(3)}
    Dlu = {i: np.abs(PT.Dl[i].c) + PT.Dl[i].r for i in range(3)}; Dlr = {i: PT.Dl[i].r for i in range(3)}
    M1 = {k: PT.A1[('p', k)].Mabs for k in range(3)}; R1 = {k: PT.A1[('p', k)].Mrg for k in range(3)}
    M2 = {j: PT.A2[('p', j)].Mabs for j in range(3)}; R2 = {j: PT.A2[('p', j)].Mrg for j in range(3)}
    err = []
    for n in range(3):
        e = np.zeros(st['nS'])
        for (i, j, k, l, cf) in terms[n]:
            v = M1[k] @ Du[l]
            mv = M2[j] @ v
            e += cf * (Dlr[i] * mv + Dlu[i] * (R2[j] @ v + M2[j] @ (R1[k] @ Du[l]) + M2[j] @ (M1[k] @ Dr[l]) + (gK + 8 * U) * mv))
        err.append(math.sqrt(nA) * float(np.max(e[aidx])) * (1 + 64 * U) * INF)
    eps = gK
    # F_n for n = 3..6 (rank-one terms)
    nv = [[float(np.linalg.norm(v)) * (1 + (nA + 4) * U) for v in Vk] for Vk in V]
    Fh = {}
    for n in range(7):
        s = 0.0
        for kk in range(4):
            for a in range(3):
                for b in range(3):
                    c = n - a - b
                    if 0 <= c <= 2:
                        s += abs(C[kk][a]) * nv[kk][b] * nv[kk][c]
        Fh[n] = s * INF
    # remainder: |R(t)|_2 <= max_i r_i/(6 u_i), u = |p_1| + floor on the cut states
    p1 = np.abs(np.asarray(frames[0][0]))
    u = np.where(st['adm'], p1 + 1e-3 * float(np.max(p1)), 1.0)
    r = BL.apply(MR(np.zeros(st['nS']), u), 'S', (3,))[3].absup()
    Rn = float(np.max(r / (6 * u))) * INF
    err = [err[n] + 8 * U * Fh[n] for n in range(3)]           # float rounding of the explicit F_n columns and of T - F
    bound = sum(h ** n * (fro[n] + err[n]) for n in range(3)) + sum(h ** n * Fh[n] for n in range(3, 7)) + h ** 3 * Rn
    return dict(bound=bound * INF, fro=fro, err=err, Fh=Fh, Rn=Rn, eps=eps)
