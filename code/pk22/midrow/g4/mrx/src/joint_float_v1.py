#!/usr/bin/env python3
"""joint_float_v1.py (pk22, G7, FLOAT CONTROL; nothing here is certified): C_bulk = <u, M_t M_h u> - c_h c_t and w_J's x, y components
<u_a, Xi u> - c_t <u_a, M_h u> - c_h <u_a, M_t u> (Proposition J; Ritz vectors in place of the true ones) from the c3j records' central a_k
(JTH, DHT on the D graph) and the reduced-prep riglap a_k of <psi_a, M_h psi_b> (h on (1, 4); pk25's Gxh family certifies these), at
J = 350 (N = 4) and 300 (N = 3), the tables' beta of pk24's model; against pk24's g6_model_v1 JOINT line. Orientation: u_x along e1,
u_y along e3 (the row 4089). Usage: joint_float_v1.py N"""
import sys, json, math, re
sys.path.insert(0, '/mnt/g2/release/root/code/pk10/scripts')
import numpy as np
import riglap5b, riglap5s
import riglap3 as _r3
from riglap2 import Graph
from pseries import padd, pscale, pmul
N = int(sys.argv[1])
J = {4: 350.0, 3: 300.0}[N]
t = 1.0 / J
W = '/mnt/g2/release/root/code'
S9 = json.load(open(W + '/pk03/out/m3_s9_N%d_J300_v1_8_3.json' % N))
DJ = json.load(open(W + '/pk22/m3/out/m3_c3j_DJ_N%d_J300_c3j.json' % N))
TSF = {4: 'ts_N4_J170_D_S_z9sym_v1.json', 3: 'ts_N3_S_z9sym_v1.json'}[N]
S = np.array(json.load(open(W + '/pk11/out/' + TSF))['S'])
R3 = json.load(open(W + '/pk11/out/vacres_K3_N%d_sym_v1.json' % N))
MOD = open(W + '/pk24/midrow/out/g6_model_v1_N%d.out' % N).read()
A_F, B_F = (3 + math.sqrt(21)) / 6, (3 * math.sqrt(5) - math.sqrt(21)) / 12
ST = (0, 1, 3)
XREC = {}


def item(rec, key):
    it = rec['items'][key]
    while it.get('alias_of'):
        fn, k2, sh = it['alias_of'].split()
        p = W + '/pk03/out/' + fn.split('/')[-1]
        if p not in XREC:
            XREC[p] = json.load(open(p))
        it = XREC[p]['items'][k2]
    return it


val = lambda rec, key: sum(a * t ** k for k, a in enumerate(item(rec, key)['ak']))
sym = lambda rec, pre: np.array([[val(rec, '%s,%d,%d' % (pre, min(a, b), max(a, b))) for b in ST] for a in ST])
Gm, Tm = sym(S9, 'G'), sym(S9, 'T')
JTH, DHT = sym(DJ, 'JTH'), sym(DJ, 'DHT')


class Lite:
    def __init__(self, g):
        self.g, self.J, self.t, self.key, self.qcap, self.am0, self.ok = g, 300.0, 1.0 / 300.0, 'jl', 6, None, False
        Hs = _r3.Model3(g, 3, []).H(3)
        H1, H2, H3 = Hs.c[1], Hs.c[2], Hs.c[3]
        H1sq = pmul(H1, H1)
        self.Ej = [{tuple([0] * g.F): 1.0}, H1, padd(H2, pscale(H1sq, 0.5)), padd(H3, pmul(H1, H2), pscale(pmul(H1sq, H1), 1.0 / 6))]
    engine = riglap5b.Prep5.engine


E = {(0, 1): A_F, (1, 2): A_F, (0, 2): B_F, (3, 4): A_F, (4, 5): A_F, (3, 5): B_F, (0, 3): 1.0, (1, 4): 1.0, (2, 5): 1.0}
g = Graph(6, E, [(0, 1), (1, 2), (0, 2), (3, 4), (4, 5), (3, 5), (1, 4)], N=N)
pr = Lite(g)
cp = lambda a, col: ('p', col, R3['q1'], R3['q2'], R3['q3']) if a == 0 else ('xi', col, float(S[0, a]), [float(x) for x in S[1:, a]])
xia = ('xi', (1, 4, 4), 0.0, [1.0] + [0.0] * 8)
DHh = np.zeros((3, 3))
for i, a in enumerate(ST):
    for j, b in enumerate(ST):
        if j < i:
            DHh[i, j] = DHh[j, i]
            continue
        ak, _ = riglap5s.bound5s(pr, [cp(a, (0, 1, 2)), xia, cp(b, (3, 4, 5))])
        DHh[i, j] = sum(x * t ** k for k, x in enumerate(ak))
ev, Vr = np.linalg.eig(np.linalg.solve(Gm, Tm))
order = np.argsort(-ev.real)
C = []
n1, n3 = S[3, 1], S[1, 3] / 2.0
for i, k in enumerate(order):
    c = Vr[:, k].real
    c = c / math.sqrt(float(c @ Gm @ c))
    ref = [c[0], c[1] * math.copysign(1.0, n1), c[2] * math.copysign(1.0, n3)][i]
    if ref < 0:
        c = -c
    C.append(c)
c0, cx, cy = C
ct, ch = float(c0 @ DHT @ c0), float(c0 @ DHh @ c0)
Xuu = float(c0 @ JTH @ c0)
Cb = Xuu - ch * ct
wx = float(cx @ JTH @ c0) - ct * float(cx @ DHh @ c0) - ch * float(cx @ DHT @ c0)
wy = float(cy @ JTH @ c0) - ct * float(cy @ DHh @ c0) - ch * float(cy @ DHT @ c0)
m = re.search(r'JOINT: C_bulk ([0-9.e+-]+); \|w_J\| ([0-9.e+-]+) \(even ([0-9.e+-]+); x ([0-9.e+-]+), y ([0-9.e+-]+)', MOD)
print('JOINT-FLOAT N=%d J=%g: c_t %.9f c_h %.9f <u, Xi u> %.9f; C_bulk %.9e; w_J x %+.4e y %+.4e' % (N, J, ct, ch, Xuu, Cb, wx, wy))
print('MODEL N=%d (pk24 g6_model_v1 JOINT): C_bulk %s; w_J x %s y %s; relative C_bulk difference %.2e' % (
    N, m.group(1), m.group(4), m.group(5), abs(Cb / float(m.group(1)) - 1)))
