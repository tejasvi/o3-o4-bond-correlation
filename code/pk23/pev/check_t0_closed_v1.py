#!/usr/bin/env python3
"""check_t0_closed_v1.py (pk23, Pev entries): a float check of the closed forms behind rtwin_hl_v1's C-T0, before that control is used.
At order 0 the field is the Gaussian free field of the infinite 3-row strip with N - 1 components. The transverse modes of P_3 have
mu = 0, 1, 3 (vectors (1,1,1)/sqrt3, (1,0,-1)/sqrt2, (1,-2,1)/sqrt6); mode m is a 1D chain with mass^2 mu, so a horizontal step has
variance g(mu) = 1 - sqrt(mu/(mu+4)) and adjacent steps have covariance -(1-lam)^2/sqrt(mu^2+4mu), lam = (mu+2-sqrt(mu^2+4mu))/2.
Checks: (N - 1) G_h / 2 against KC4's c_h0; E5's certified-twin HH,0,0 a_0 (h on (1,4) and (4,7)) against c_h0^2 + (N - 1) C_h^2 / 2 and
HH,1,1 against lam_1^2 times that; s_x0 = lam_1^2 and s_y0 = lam_3^2 against KC4. Prints the C-T0 predictions for the L-graph keys.
Usage: check_t0_closed_v1.py (reads pk22's KC4 and rtwin_e5_v1 outputs, read-only)."""
import json, math, re
W18 = '/mnt/g2/release/root/code'
KC4 = W18 + '/pk22/midrow/out/out_kt_kc4_v1_2_n%d.out'
E5 = W18 + '/pk22/m3/out/rtwin_e5_v1_E5N.%d_z9symxy.out'
V = {0: (1 / 3, 1 / 3, 1 / 3), 1: (1 / 2, 0.0, 1 / 2), 3: (1 / 6, 4 / 6, 1 / 6)}   # v_m(r)^2 for rows T, M, B


def g(mu):
    return 1.0 if mu == 0 else 1 - math.sqrt(mu / (mu + 4.0))


def lam(mu):
    return (mu + 2 - math.sqrt(mu * mu + 4 * mu)) / 2


def cadj(mu):
    return 0.0 if mu == 0 else -(1 - lam(mu)) ** 2 / math.sqrt(mu * mu + 4 * mu)


GH = sum(V[m][1] * g(m) for m in V)
GT = sum(V[m][0] * g(m) for m in V)
CH = sum(V[m][1] * cadj(m) for m in V)
print('G_h %.15f (closed 1 - (2/3) sqrt(3/7) = %.15f); G_t %.15f (closed 1 - sqrt(1/5)/2 - sqrt(3/7)/6 = %.15f); C_h %.15f' % (
    GH, 1 - 2 * math.sqrt(3 / 7) / 3, GT, 1 - math.sqrt(0.2) / 2 - math.sqrt(3 / 7) / 6, CH))
worst = 0.0
for N in (4, 3):
    kt = open(KC4 % N).read()
    m1 = re.search(r'^V1 IDENT N=%d: .*?eta = v_h ([-+0-9.eE]+) ([-+0-9.eE]+) ([-+0-9.eE]+) ' % N, kt, re.M)
    m2 = re.search(r'^KC4 V1 RITZ N=%d: s_x ([0-9.]+) \+ t [-0-9.]+; mu_y ([0-9.]+) \+ t' % N, kt, re.M)
    ch0, hy0, sx0, sy0 = float(m1.group(1)), float(m1.group(3)), float(m2.group(1)), float(m2.group(2))
    ch = (N - 1) * GH / 2
    ak = {}
    for ln in open(E5 % N):
        if ln.startswith('KEYJSON '):
            d = json.loads(ln[8:])
            ak[d['key']] = d['ak'][0]
    p00 = ch * ch + (N - 1) * CH * CH / 2
    p11 = lam(1) ** 2 * p00
    r = [abs(ch / ch0 - 1), abs(lam(1) ** 2 / sx0 - 1), abs(lam(3) ** 2 / sy0 - 1), abs(ak['HH,0,0'] / p00 - 1), abs(ak['HH,1,1'] / p11 - 1),
         abs((N - 1) * CH * CH / 2 / (hy0 * hy0 / sy0) - 1)]
    worst = max(worst, r[3], r[4])
    print('N=%d: (N-1) G_h/2 %.12f vs KC4 c_h0 %.7f (rel %.2e); lam_1^2 %.12f vs s_x0 %.12f (rel %.2e); lam_3^2 %.12f vs s_y0 %.12f (rel %.2e)' % (
        N, ch, ch0, r[0], lam(1) ** 2, sx0, r[1], lam(3) ** 2, sy0, r[2]))
    print('N=%d: E5 HH,0,0 a_0 %.13f vs c_h^2 + (N-1) C_h^2/2 = %.13f (rel %.2e); HH,1,1 a_0 %.13f vs lam_1^2 times that %.13f (rel %.2e); '
          '(N-1) C_h^2/2 vs KC4 m_y^2 s_y0 (rel %.2e)' % (N, ak['HH,0,0'], p00, r[3], ak['HH,1,1'], p11, r[4], r[5]))
    ct = (N - 1) * GT / 2
    print('N=%d PRED: TT,0,0 1; Mh,0,0 %.13f; Mhh,0,0 %.13f; Mt,0,0 = Mb,0,0 %.13f; Mtt,0,0 %.13f' % (
        N, ch, ch * ch * (N + 1) / (N - 1), ct, ct * ct * (N + 1) / (N - 1)))
print('E5 worst relative difference %.2e -> %s' % (worst, 'PASS' if worst <= 1e-9 else 'FAIL'))
