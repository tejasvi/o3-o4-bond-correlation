# Wave 18 pilot, step 2: certified G2 criterion for ALL pairs on uniform 3 x n grids (all n) at one J, ball arithmetic.
# Model: labels <= L (truncation effects bounded separately in step 1: eigenvectors 1e-5, eigenvalues 1e-11 at L=12, J=1).
# Notation (STRIPW 1.3, 4.4): left data (L^1, L^E) of an edge at distance i from the left end, right data mirror-wise;
#   Cov N^2 = sum_{l>=2} (lam_l/lam_1)^m a_l b_l + R_CE(m),  a_l = <phi_l, u~>, u~ = (L^E - c_e L^1)/u^1_1.
# Criterion: (C1) block ordering + lam_5 bound [step 1]; (C2) lam_2 + lam_4 >= 2 lam_3; (C3) mode signs for every class;
#   (C4) opposite-side pairs: p_2 >= p_4 >= 0 and F(0) = p_2 + p_4 - d > 0;  (C5) dominance for m >= m0:
#   S_cl >= (lam_4/lam_1)^m (p_2+p_4) [same side, h] or (lam_3/lam_1)^m F(0) [opposite] beats
#   |S_inf| <= (lam_5/lam_1)^m |Q5 u~||Q5 v~| and |R_CE| <= (lam_2/lam_1)^{2m} |u~||eps_L||v~||eps_R|;
#   (C6) m < m0: direct certified evaluation of the normalized 2x2 minor for every class pair; same-column (a,b) pairs.
# Classes: horizontals t, h, bb at cut i = 0..I and 'deep' (i > I, enclosed with a radius from (lam_2/lam_1)^{I+1});
#   verticals a, b in column j = 1..I and deep.  Right classes equal left classes (mirror symmetry at uniform J).
# usage: cert2.py TAG L J PREC I
import os, sys, time, math
from fractions import Fraction
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from flint import arb, arb_mat, ctx
import certlib
tag, L, prec, I = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
Jlist = [Fraction(x) for x in sys.argv[5].split(',')]
Jrad = 0.0; force_m0 = 0
ctx.prec = prec
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'out', 'certgrid_%s.txt' % tag)
assert '/pkg_v2/out/' in OUT and not os.path.exists(OUT)
lines = []
def say(s):
    print(s, flush=True); lines.append(s)
    open(OUT, 'w').write('\n'.join(lines) + '\n')
up = lambda x: float(abs(x).upper())
lo = lambda x: float(x.lower())
hi = lambda x: float(x.upper())
import certlib2
t00 = time.time()
ST = certlib2.build_struct(L)
say('certgrid %s: L=%d prec=%d I=%d; exact 6j structure built in %.1fs' % (tag, L, prec, I, time.time() - t00))
summary = []
def certify(J):
    t0 = time.time()
    D = certlib2.assemble(ST, J, Jrad)
    nS, states = D['nS'], D['states']
    def symm(A):
        B = arb_mat(nS, nS)
        for i in range(nS):
            for j in range(nS):
                B[i, j] = (A[i, j] + A[j, i]) / 2
        return B
    S, TX, TY, TXY = symm(D['S']), symm(D['TX']), symm(D['TY']), symm(D['TXY'])
    say('cert2 %s: J=%s +/- %g L=%d prec=%d I=%d; %d states; build %.1fs' % (tag, J, Jrad, L, prec, I, nS, time.time() - t0))
    # ---- spectral verification (as cert1) ----
    Smid = np.array([[float(S[i, j].mid()) for j in range(nS)] for i in range(nS)])
    lam, Q = np.linalg.eigh(Smid)
    order = np.argsort(-lam); lam = lam[order]; Q = Q[:, order]
    Qa = arb_mat(Q.tolist())
    QL = arb_mat(nS, nS)
    for i in range(nS):
        for j in range(nS):
            QL[i, j] = Qa[i, j] * arb(float(lam[j]))
    E = S - QL * Qa.transpose()
    F = Qa.transpose() * Qa
    Eu = [[up(E[i, j]) for j in range(nS)] for i in range(nS)]
    eF = min(math.sqrt(sum(x * x for row in Eu for x in row)), math.sqrt(max(sum(row) for row in Eu) * max(sum(Eu[i][j] for i in range(nS)) for j in range(nS)))) * (1 + 1e-12)
    fF = math.sqrt(sum(up(F[i, j] - (1 if i == j else 0)) ** 2 for i in range(nS) for j in range(nS))) * (1 + 1e-12)
    encl = [(l * (1 - fF) - eF, l * (1 + fF) + eF) if l >= 0 else (l * (1 + fF) - eF, l * (1 - fF) + eF) for l in lam]
    qv = [[Qa[i, k] for i in range(nS)] for k in range(6)]
    # refine the top-4 eigenvectors by two steps of shifted inverse iteration in arb (float64 eigh is not accurate
    # enough at weak coupling, where the block splittings are ~J^3); enclose each eigenvalue by Rayleigh quotient +/- residual
    dlt = []
    Iden = arb_mat(nS, nS)
    for i in range(nS):
        Iden[i, i] = arb(1)
    for k in range(4):
        x = arb_mat(nS, 1)
        for i in range(nS):
            x[i, 0] = qv[k][i]
        sig = arb(float(lam[k]))
        A = S - Iden * sig
        for it in range(2):
            y = A.solve(x)
            ny = sum((y[i, 0] ** 2 for i in range(nS)), arb(0)).sqrt()
            for i in range(nS):
                x[i, 0] = y[i, 0] / ny
        Sx = S * x
        nx2 = sum((x[i, 0] ** 2 for i in range(nS)), arb(0))
        rho = sum((x[i, 0] * Sx[i, 0] for i in range(nS)), arb(0)) / nx2
        rk = math.sqrt(sum(up(Sx[i, 0] - rho * x[i, 0]) ** 2 for i in range(nS)) / lo(nx2)) * (1 + 1e-12)
        lo_r, hi_r = lo(rho) - rk, hi(rho) + rk
        encl[k] = (max(encl[k][0], lo_r), min(encl[k][1], hi_r))
        gap = min(min(abs(float(rho.mid()) - encl[j][0]), abs(float(rho.mid()) - encl[j][1])) for j in range(nS) if j != k)
        dlt.append(math.sqrt(2) * rk / gap)
        say('      refine k=%d: rho %s rk %.2e gap %.3e encl [%.15e, %.15e]' % (k, rho.str(15, radius=False), rk, gap, encl[k][0], encl[k][1]))
        nx = nx2.sqrt()
        qv[k] = [x[i, 0] / nx for i in range(nS)]
    # ---- label truncation (labels > L in the cut states, verticals > L), as in cert1: widen eigen-data to the full T ----
    Ja = D['Ja']
    tail = arb(0)
    for a_ in range(L + 1, L + 60):
        tail += (a_ + 1) ** 2 * 2 * Ja.bessel_i(a_ + 1) / Ja
    tail = tail * (1 + arb(1e-10))
    k0 = 2 * Ja.bessel_i(1) / Ja
    eps_v = up(k0 ** 3 * tail * (2 * Ja.exp() + tail))
    kapQ = 2 * Ja.bessel_i(L + 2) / Ja * k0 ** 2
    tau_inf = up((2 * Ja).exp() * kapQ); cQ = up((2 * Ja).exp() * (k0 ** 3 * kapQ).sqrt())
    encl_full = []
    for k in range(5):
        lo_k = encl[k][0] - eps_v
        encl_full.append((lo_k, encl[k][1] + eps_v + cQ ** 2 / max(lo_k - tau_inf, 1e-300)))
    encl_full[4] = (encl_full[4][0], max(encl_full[4][1], tau_inf))
    for k in range(4):
        gap_k = min(abs(lam[k] - encl[j][0]) for j in range(nS) if j != k)
        chi = cQ / max(encl_full[k][0] - tau_inf, 1e-300)
        g_k = cQ ** 2 / max(encl_full[k][0] - tau_inf, 1e-300)
        dlt[k] += math.sqrt(2) * (eps_v / max(gap_k - 2 * eps_v, 1e-300) + g_k / max(gap_k - (encl_full[k][1] - encl_full[k][0]), 1e-300)) + chi
    say('   truncation: eps_v <= %.2e, tau_inf <= %.2e, c <= %.2e -> full-T eigenvector errors %s' % (eps_v, tau_inf, cQ, ' '.join('%.1e' % d for d in dlt)))
    encl = encl_full + encl[5:]
    lamA = [arb((encl[k][0] + encl[k][1]) / 2, (encl[k][1] - encl[k][0]) / 2) for k in range(5)]
    r21, r31, r41, r51 = [lamA[k] / lamA[0] for k in (1, 2, 3, 4)]
    say('   eigenvalues / lam_1: %s ; eigenvector errors (truncated model) %s' % (' '.join(x.str(10, radius=False) for x in (r21, r31, r41, r51)), ' '.join('%.1e' % d for d in dlt)))
    conv = lamA[1] + lamA[3] - 2 * lamA[2]
    say('   (C1) ordering: %s; (C2) (lam_2 + lam_4 - 2 lam_3)/lam_1 = %s (lower bound %.6e)'
        % (lo(lamA[0]) > hi(lamA[1]) and lo(lamA[1]) > hi(lamA[2]) and lo(lamA[2]) > hi(lamA[3]) and lo(lamA[3]) > hi(lamA[4]),
           (conv / lamA[0]).str(8, radius=False), lo(conv / lamA[0])))
    # ---- vector helpers ----
    def mv(A, v):
        c = arb_mat(nS, 1)
        for i in range(nS):
            c[i, 0] = v[i]
        w = A * c
        return [w[i, 0] for i in range(nS)]
    def dot(x, y):
        return sum((a * b for a, b in zip(x, y)), arb(0))
    def nrm(x):
        return dot(x, x).sqrt()
    def fuzz(x, e):
        return x + arb(0, e)
    rd = D['rdiag']
    b = D['b']
    # powers S^i b
    Sb = [b]
    for i in range(I + 1):
        Sb.append(mv(S, Sb[-1]))
    q1 = qv[0]
    classes = []                 # (name, type, pos, L1, LE)
    for tau in ('t', 'h', 'bb'):
        for i in range(I + 1):
            classes.append(('%s@%d' % (tau, i), tau, i, Sb[i], [rd[tau][s] * Sb[i][s] for s in range(nS)]))
        classes.append(('%s@deep' % tau, tau, 'deep', q1, [rd[tau][s] * q1[s] for s in range(nS)]))
    for vt, TV in (('a', TX), ('b', TY)):
        for j in range(1, I + 1):
            classes.append(('%s@%d' % (vt, j), vt, j, Sb[j], mv(TV, Sb[j - 1])))
        classes.append(('%s@deep' % vt, vt, 'deep', mv(S, q1), mv(TV, q1)))
    # deep enclosure radius: eps(i) <= (lam2/lam1)^i eps(0); u~ moves by <= 3 |R| |eps|
    rmax = max(up(x) for x in D['r'])
    TXn = math.sqrt(max(sum(up(TX[i, j]) for j in range(nS)) for i in range(nS)) ** 2)    # row-sum norm (TX symmetric)
    side = {'t': 1, 'a': 1, 'bb': -1, 'b': -1, 'h': 0}
    data = {}
    for (name, typ, pos, L1, LE) in classes:
        u1 = fuzz(dot(q1, L1), dlt[0] * up(nrm(L1)))
        uE = fuzz(dot(q1, LE), dlt[0] * up(nrm(LE)))
        ce = uE / u1
        ut = [(LE[s] - ce * L1[s]) / u1 for s in range(nS)]
        nut = up(nrm(ut))
        al = [fuzz(dot(qv[l], ut), dlt[l] * nut) for l in (1, 2, 3)]
        eps = [L1[s] / u1 - q1[s] for s in range(nS)]
        neps = up(nrm(eps)) + dlt[0]
        proj = [ut[s] - sum((dot(qv[l], ut) * qv[l][s] for l in range(4)), arb(0)) for s in range(nS)]
        q5 = up(nrm(proj)) + 2 * sum(dlt) * nut
        data[name] = dict(typ=typ, pos=pos, a2=al[0], a3=al[1], a4=al[2], nut=nut, neps=neps, q5=q5, L1=[x / u1 for x in L1], LE=[x / u1 for x in LE])
    eps0 = max(data[c[0]]['neps'] for c in classes if c[2] == 0 or (c[2] == 1 and c[1] in ('a', 'b')))
    eta = 3 * max(rmax, TXn / lo(lamA[0])) * hi(r21) ** (I + 1) * eps0 * 1.01
    # truncation of the class vectors: |T^i b - S^i b| <= i lam1^{i-1} (eps_v + c)|b| + lam1^i |Q b|; relative to the normalized
    # vectors this is <= trel; the normalized data (u~, a_l) move by <= 4 (rmax + TXn/lam1) trel (crude)
    Rq = max(max(up(nrm([rd[tau][s] * qv[l][s] for s in range(nS)])) for tau in ('t', 'h', 'bb')) for l in range(4))
    Tq = max(up(nrm(mv(TX, qv[l]))) for l in range(4)) / lo(lamA[0])
    mult = 2 * (max(Rq, Tq) + 1.0)          # |<R phi_l, dL>| <= (|R q_l| + |R| dlt_l) |dL|, dlt_l tiny; +1 covers c_e and the tails
    trel = (I + 2) * (eps_v + cQ) / lo(lamA[0]) + (L + 1) * math.sqrt(up(kapQ)) * 4
    tfz = 2 * mult * trel
    for name in data:
        dd = data[name]
        dd['a2'], dd['a3'], dd['a4'] = fuzz(dd['a2'], tfz), fuzz(dd['a3'], tfz), fuzz(dd['a4'], tfz)
        dd['nut'] += tfz; dd['q5'] += tfz; dd['neps'] += trel
    say('   class-vector truncation: relative <= %.2e, mode data fuzz %.2e (added to every class)' % (trel, tfz))
    for name in data:
        if data[name]['pos'] == 'deep':
            dd = data[name]
            dd['a2'], dd['a3'], dd['a4'] = fuzz(dd['a2'], eta), fuzz(dd['a3'], eta), fuzz(dd['a4'], eta)
            dd['nut'] += eta; dd['q5'] += eta; dd['neps'] = hi(r21) ** (I + 1) * eps0
    say('   deep classes enclose all positions > %d with radius %.2e (eps(0) <= %.3f, r_max %.2f)' % (I, eta, eps0, rmax))
    # ---- (C3) mode signs ----
    s2 = [np.sign(float(d['a2'].mid())) for d in data.values()]; s4 = [np.sign(float(d['a4'].mid())) for d in data.values()]
    ok2 = all(lo(d['a2'] * s2[0]) > 0 for d in data.values()); ok4 = all(lo(d['a4'] * s4[0]) > 0 for d in data.values())
    s3ref = np.sign(float(data['t@deep']['a3'].mid()))
    ok3 = all((lo(d['a3'] * s3ref * side[d['typ']]) > 0) if side[d['typ']] != 0 else True for d in data.values())
    h3 = max(up(d['a3']) for d in data.values() if d['typ'] == 'h')
    say('   (C3) mode signs: a_2 one-signed over all %d classes: %s; a_4 one-signed: %s; a_3 = +/- by side (top +, bottom -): %s; |a_3| on h classes <= %.1e (0 by symmetry)'
        % (len(data), ok2, ok4, ok3, h3))
    for nm in ('t@0', 't@1', 't@deep', 'h@0', 'h@deep', 'bb@deep', 'a@1', 'a@deep', 'b@deep'):
        d = data[nm]
        say('      %-8s a2 %s a3 %s a4 %s |u~| %.3e |eps| %.3e |Q5 u~| %.3e'
            % (nm, d['a2'].str(6, radius=False), d['a3'].str(6, radius=False), d['a4'].str(6, radius=False), d['nut'], d['neps'], d['q5']))
    # ---- (C4), (C5) ----
    names = list(data)
    worst_F0 = None; worst_pp = None; worst_same = None; worst_sf = None
    m0 = 0
    x5_4 = hi(r51 / r41); x5_3 = hi(r51 / r31); x22_4 = hi(r21 * r21 / r41); x22_3 = hi(r21 * r21 / r31)
    for X in names:
        for Y in names:
            dX, dY = data[X], data[Y]
            p2, p3, p4 = dX['a2'] * dY['a2'], dX['a3'] * dY['a3'], dX['a4'] * dY['a4']
            if dX['typ'] == 'h' or dY['typ'] == 'h':
                p3 = arb(0)      # exact: phi_3 is flip-odd (simple eigenvalue), R_h and the boundary vectors are flip-even
            opp = side[dX['typ']] * side[dY['typ']] < 0
            q55 = dX['q5'] * dY['q5']; AA = dX['nut'] * dX['neps'] * dY['nut'] * dY['neps']
            if opp:
                F0 = p2 + p4 + p3
                pp = p2 - p4
                if worst_F0 is None or lo(F0) < worst_F0[0]:
                    worst_F0 = (lo(F0), X, Y)
                if worst_pp is None or lo(pp) < worst_pp[0]:
                    worst_pp = (lo(pp), X, Y)
                base, ra, rb = lo(F0), x5_3, x22_3
            else:
                base = lo(p2 + p4) + (min(lo(p3), 0.0))
                if worst_same is None or base < worst_same[0]:
                    worst_same = (base, X, Y)
                ra, rb = x5_4, x22_4
            m = 0
            while base <= 0 or q55 * ra ** m + AA * rb ** m >= base:
                m += 1
                if m > 60:
                    break
            m0 = max(m0, m)
            sf = base / max(q55 + AA, 1e-300)
            if worst_sf is None or sf < worst_sf[0]:
                worst_sf = (sf, X, Y)
    say('   (C4) opposite-side pairs: min (p_2 - p_4) = %.4e at (%s, %s); min F(0) = %.4e at (%s, %s)' % (worst_pp + worst_F0))
    say('        same-side and h pairs: min (p_2 + p_4 + min(p_3,0)) = %.4e at (%s, %s)' % worst_same)
    say('   (C5) dominance holds for every class pair from m0 = %d on (ratios: lam5/lam4 <= %.4f, lam5/lam3 <= %.4f, lam2^2/(lam1 lam4) <= %.4f)'
        % (m0, x5_4, x5_3, x22_4))
    say('        safety factor at m = 0 (block term / remainder bound), minimum over all class pairs: %.3e at (%s, %s)' % worst_sf)
    # ---- (C6) direct evaluation for m < m0 ----
    m0_run = max(m0, force_m0)
    Sh = [[x / lamA[0] for x in row] for row in []]
    neg = 0; worst = None; nev = 0
    Rvec = {nm: (data[nm]['L1'], data[nm]['LE']) for nm in names}
    for m in range(m0_run):
        Rm = {}
        for nm in names:
            r1, rE = Rvec[nm]
            for _ in range(m):
                r1 = [x / lamA[0] for x in mv(S, r1)]
                rE = [x / lamA[0] for x in mv(S, rE)]
            Rm[nm] = (r1, rE)
        for X in names:
            l1, lE = data[X]['L1'], data[X]['LE']
            for Y in names:
                if m == 0 and data[X]['typ'] == data[Y]['typ'] and data[X]['typ'] in ('t', 'h', 'bb'):
                    continue          # same horizontal edge
                r1, rE = Rm[Y]
                A_ = dot(lE, rE); B_ = dot(lE, r1); C_ = dot(l1, rE); D_ = dot(l1, r1)
                if data[X]['pos'] == 'deep' or data[Y]['pos'] == 'deep':
                    e_ = eta * (up(nrm(lE)) + up(nrm(rE)) + up(nrm(l1)) + up(nrm(r1)) + 2 * eta)
                    A_, B_, C_, D_ = fuzz(A_, e_), fuzz(B_, e_), fuzz(C_, e_), fuzz(D_, e_)
                mnr = A_ * D_ - B_ * C_
                nev += 1
                if not (lo(mnr) > 0):
                    neg += 1
                if worst is None or lo(mnr) < worst[0]:
                    worst = (lo(mnr), X, Y, m)
    if worst is not None:
        say('   (C6) direct evaluation, m < %d: %d class-pair evaluations; not certified > 0: %d; smallest lower bound %.4e at (%s, %s, m=%d)'
            % ((m0_run, nev, neg) + worst))
    # same-column (a, b) pairs: Cov Z^2 = <L0,TXY R0><L0,S R0> - <L0,TX R0><L0,TY R0>, L0 = S^i b, R0 = S^i' b
    negc = 0; worstc = None
    pos_list = list(range(I + 1)) + ['deep']
    vecs0 = {i: [x / fuzz(dot(q1, Sb[i]), dlt[0] * up(nrm(Sb[i]))) for x in Sb[i]] for i in range(I + 1)}
    vecs0['deep'] = q1
    for iL in pos_list:
        for iR in pos_list:
            l0, r0 = vecs0[iL], vecs0[iR]
            a_ = dot(l0, mv(TXY, r0)); s_ = dot(l0, mv(S, r0)); x_ = dot(l0, mv(TX, r0)); y_ = dot(l0, mv(TY, r0))
            e_t = 2 * mult * trel * 4 * max(up(nrm(l0)), up(nrm(r0))) * (TXn / lo(lamA[0]) + 1) * max(up(nrm(l0)), up(nrm(r0)))
            a_, s_, x_, y_ = fuzz(a_, e_t), fuzz(s_, e_t), fuzz(x_, e_t), fuzz(y_, e_t)
            if iL == 'deep' or iR == 'deep':
                e_ = eta * 4 * max(up(nrm(l0)), up(nrm(r0))) * (TXn + 1)
                a_, s_, x_, y_ = fuzz(a_, e_), fuzz(s_, e_), fuzz(x_, e_), fuzz(y_, e_)
            c_ = a_ * s_ - x_ * y_
            if not (lo(c_) > 0):
                negc += 1
            if worstc is None or lo(c_) < worstc[0]:
                worstc = (lo(c_), iL, iR)
    say('   same-column (a,b): %d position pairs; not certified > 0: %d; smallest lower bound %.4e at (%s, %s)' % ((len(pos_list) ** 2, negc) + worstc))
    say('   J=%s done %.1fs' % (J, time.time() - t0))
    summary.append((J, lo(conv / lamA[0]), worst_pp[0], worst_F0[0], worst_same[0], m0, worst_sf[0], worstc[0], time.time() - t0))
for J in Jlist:
    certify(J)
say('SUMMARY: J  conv/lam1  min(p2-p4)  min F(0)  min same-side  m0  safety  min same-column  seconds')
for row in summary:
    say('   %s  %.5f  %.3e  %.3e  %.3e  %d  %.2f  %.3e  %.0f' % row)
say('total %.1fs' % (time.time() - t00))
