# High-precision check of Lemma 5.3 claims: centred insertion vectors (4-state model), deep and boundary-dressed,
# components in units: (0) and (011) in J^3, (110) in J/8, (101) in J^2/32; overlaps in J/16; f(0) in J^4/1024.
import mpmath as mp
mp.mp.dps = 50
def cat(p): return mp.binomial(2*p, p) / (p + 1)
def mom(J, q, P=30):
    s = mp.mpf(0)
    for n in range(0, 2*P):
        e = q + n
        if e % 2: continue
        s += J**n * cat(e//2) / mp.mpf(4)**(e//2) / mp.factorial(n)
    return s
def mats(J):
    k0, k1, m2, m3 = [mom(J, q) for q in range(4)]
    A = (k0-m2)/3; B = (4*m2-k0)/3; Ap = (k1-m3)/3; Bp = (4*m3-k1)/3
    V = [[k0**2, 2*k0*k1, 2*k1**2, 2*k0*k1], [2*k0*k1, 4*k0*m2, 4*k1*m2, 4*k1**2],
         [2*k1**2, 4*k1*m2, 4*(4*A*A+2*A*B+B*B), 4*k1*m2], [2*k0*k1, 4*k1**2, 4*k1*m2, 4*k0*m2]]
    XV = [[k1*k0, 2*m2*k0, 2*m2*k1, 2*k1*k1], [2*m2*k0, 4*m3*k0, 4*m3*k1, 4*m2*k1],
          [2*m2*k1, 4*m3*k1, 4*(4*Ap*A+Ap*B+Bp*A+Bp*B), 4*m2*m2], [2*k1*k1, 4*m2*k1, 4*m2*m2, 4*k1*m2]]
    ks = [k0**3, k1*k1*k0, k1*k1*k0, k1*k1*k0]
    T = mp.matrix(4, 4); TX = mp.matrix(4, 4)
    for i in range(4):
        for j in range(4):
            T[i, j] = mp.sqrt(ks[i]*ks[j])*V[i][j]; TX[i, j] = mp.sqrt(ks[i]*ks[j])*XV[i][j]
    perm = [0, 3, 2, 1]
    TY = mp.matrix(4, 4)
    for i in range(4):
        for j in range(4):
            TY[i, j] = TX[perm[i], perm[j]]
    b = mp.matrix([mp.sqrt(ks[i])*V[i][0] for i in range(4)])
    return T, TX, TY, b
def r(J, l):
    I = lambda nu: mp.besseli(nu, J)
    return (I(l)+I(l+2))/(2*I(l+1)) - 1/J
for J in [mp.mpf('0.01'), mp.mpf('0.001')]:
    T, TX, TY, b = mats(J)
    E, Q = mp.eigsy(T)
    order = sorted(range(4), key=lambda i: -E[i]); mu = [E[i] for i in order]
    P = [mp.matrix([Q[j, i] for j in range(4)]) for i in order]
    if P[0][0] < 0: P[0] = -P[0]
    for k in (1, 2, 3):
        if P[k][1] < 0: P[k] = -P[k]
    phi = P[0]
    r0, r1 = r(J, 0), r(J, 1)
    Rt = mp.diag([r0, r1, r1, r0]); Rbb = mp.diag([r0, r0, r1, r1])
    dot = lambda x, y: sum(x[i]*y[i] for i in range(4))
    def cent(L1, LE):
        u1 = dot(phi, L1); c = dot(phi, LE)/u1
        return (LE - c*L1)/u1
    vec = {
        't deep': cent(phi, Rt*phi), 'bb deep': cent(phi, Rbb*phi),
        'a deep': cent(T*phi, TX*phi), 'b deep': cent(T*phi, TY*phi),
        't cut0': cent(b, Rt*b), 'bb cut0': cent(b, Rbb*b),
        'a col1': cent(T*b, TX*b), 'b col1': cent(T*b, TY*b),
    }
    print('J =', mp.nstr(J, 3))
    for name, u in vec.items():
        ov = [dot(P[k], u)/(J/16) for k in (1, 2, 3)]
        print('   %-8s comps: (0)/J^3=%s (110)/(J/8)=%s (101)/(J^2/32)=%s (011)/J^3=%s | overlaps/(J/16): %s' % (
            name, mp.nstr(u[0]/J**3, 5), mp.nstr(u[1]/(J/8), 8), mp.nstr(u[2]/(J**2/32), 8), mp.nstr(u[3]/J**3, 5),
            [mp.nstr(x, 7) for x in ov]))
    for L in ('t deep', 'a deep', 't cut0', 'a col1'):
        for R in ('bb deep', 'b deep', 'bb cut0', 'b col1'):
            u, v = vec[L], vec[R]
            f0 = dot(u, v)
            pk = [dot(P[k], u)*dot(P[k], v) for k in (1, 2, 3)]
            print('   %-8s x %-8s : f(0)/(J^4/1024)=%s  (101-product)/(J^4/1024)=%s  (p2-p4)/(3J^3/(512 sqrt2))=%s  signs p2,p3,p4: %s' % (
                L, R, mp.nstr(f0/(J**4/1024), 8), mp.nstr(u[2]*v[2]/(J**4/1024), 8),
                mp.nstr((pk[0]-pk[2])/(3*J**3/(512*mp.sqrt(2))), 6), [int(mp.sign(x)) for x in pk]))
