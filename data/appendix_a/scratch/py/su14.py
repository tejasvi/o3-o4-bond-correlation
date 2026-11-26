# High-precision check of the 4-state model expansion coefficients (mpmath, 60 digits).
# Moments via Catalan series: E[X^{2p}] = C_p / 4^p for the S^3 coordinate (semicircle on [-1,1]).
import mpmath as mp
mp.mp.dps = 60
def cat(p): return mp.binomial(2*p, p) / (p + 1)
def mom(J, q, P=40):   # E[X^q e^{JX}] = sum_n J^n E[X^{q+n}]/n!
    s = mp.mpf(0)
    for n in range(0, 2*P):
        e = q + n
        if e % 2: continue
        s += J**n * cat(e//2) / mp.mpf(4)**(e//2) / mp.factorial(n)
    return s
def model(J):
    k0, k1, m2, m3 = mom(J, 0), mom(J, 1), mom(J, 2), mom(J, 3)
    A = (k0 - m2)/3; B = (4*m2 - k0)/3
    V = mp.matrix([[k0**2, 2*k0*k1, 2*k1**2, 2*k0*k1], [2*k0*k1, 4*k0*m2, 4*k1*m2, 4*k1**2],
                   [2*k1**2, 4*k1*m2, 4*(4*A*A + 2*A*B + B*B), 4*k1*m2], [2*k0*k1, 4*k1**2, 4*k1*m2, 4*k0*m2]])
    ks = [k0**3, k1*k1*k0, k1*k1*k0, k1*k1*k0]
    T = mp.matrix(4, 4)
    for i in range(4):
        for j in range(4):
            T[i, j] = mp.sqrt(ks[i]*ks[j]) * V[i, j]
    return T, k0, k1
def r(J, l):
    I = lambda nu: mp.besseli(nu, J)
    return (I(l) + I(l + 2)) / (2*I(l + 1)) - 1/J
for J in [mp.mpf('0.001'), mp.mpf('0.0005')]:
    T, k0, k1 = model(J)
    E, Q = mp.eigsy(T)
    order = sorted(range(4), key=lambda i: -E[i])
    mu = [E[i] for i in order]; P = [[Q[j, i] for j in range(4)] for i in order]
    if P[0][0] < 0: P[0] = [-x for x in P[0]]
    for k in (1, 2, 3):
        if P[k][1] < 0: P[k] = [-x for x in P[k]]
    kap1 = k1*k1*k0
    muh = [m/kap1 for m in mu]
    beta = P[0][1]/P[0][0]; gamma = P[0][2]/P[0][0]
    # rotation angle of even cluster eigenvectors: psi2 = cos(th) e+ + sin(th) e101
    th = mp.atan2(P[1][2], (P[1][1] + P[1][3])/mp.sqrt(2))
    rho = r(J, 1) - r(J, 0)
    phi = P[0]
    nrm = phi[0]
    def ab(states, k): return rho * sum(P[k][s]*phi[s] for s in states)
    a = {k: ab([1, 2], k) for k in (1, 2, 3)}; bb = {k: ab([2, 3], k) for k in (1, 2, 3)}
    f0 = sum(a[k]*bb[k] for k in (1, 2, 3))
    p2 = a[1]*bb[1]; p4 = a[3]*bb[3]
    print('J =', mp.nstr(J, 4))
    print('  (mu2h - 1 - sqrt2 J/4)/J^2 =', mp.nstr((muh[1] - 1 - mp.sqrt(2)*J/4)/J**2, 12), ' [pred 3/16 = 0.1875]')
    print('  (mu3h - 1)/J^2 =', mp.nstr((muh[2] - 1)/J**2, 12), ' [pred 1/8]')
    print('  (mu4h - 1 + sqrt2 J/4)/J^2 =', mp.nstr((muh[3] - 1 + mp.sqrt(2)*J/4)/J**2, 12), ' [pred 3/16]')
    print('  (mu2+mu4-2mu3)/(kap1 J^2) =', mp.nstr((mu[1] + mu[3] - 2*mu[2])/(kap1*J**2), 12), ' [pred 1/8]')
    print('  beta/(J^2/8) =', mp.nstr(beta/(J**2/8), 12), '  gamma/(J^3/32) =', mp.nstr(gamma/(J**3/32), 12))
    print('  (theta - pi/4)/(J/(8 sqrt2)) =', mp.nstr((th - mp.pi/4)/(J/(8*mp.sqrt(2))), 12))
    print('  deep t-bb f(0)/(J^4/1024) =', mp.nstr(f0/(J**4/1024), 12), '  check rho^2[g^2-(b^2+g^2)^2]/(J^4/1024) =',
          mp.nstr(rho**2*(gamma**2 - (beta**2 + gamma**2)**2)*nrm**4/(J**4/1024), 12))
    print('  deep t-bb (p2 - p4)/(3 J^3/(512 sqrt2)) =', mp.nstr((p2 - p4)/(3*J**3/(512*mp.sqrt(2))), 12))
    print('  a_k^(t)/(J/16):', [mp.nstr(a[k]/(J/16), 10) for k in (1, 2, 3)])
