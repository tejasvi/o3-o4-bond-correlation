#!/usr/bin/env python3
"""g6_engine_proto_v1_2.py (pk24; g6_engine_proto_v1_1.py with EXPECT extended by tools/count_todo_bf_v1.py's independent count, made
by tools/make_core_proto_v1_3.py; the reference of engine v1_7's C-CORE gate. g6_engine_proto_v1_1.py was g6_engine_proto_v1.py with
a band G-FLOAT, a valid crude-end norm in T2 and _v1_1 outputs, made by tools/make_proto_v1_1.py). MIDROW M1 assembly engine, FLOAT PROTOTYPE. Usage:
  g6_engine_proto_v1.py write            writes the stand-in input records into midrow/out/proto_rec_v1/ (new files) and PINS.txt;
  g6_engine_proto_v1.py run [PLANT]      runs the engine on those records; PLANT in {OPN, TAU2, SIGN, T2, PIN, COUNT} or absent.
The engine evaluates Proposition MR (MIDROW_G6_SPEC_v1 sect. 3, windowed inputs as in the M1 engine spec) on every to-do channel class of
P_3 x P_n, n = 6..14, both N, and Proposition J on the interior same-bond orbits, on two pieces: P0 (J = J_low) and P1 (t -> 0, where the
crude x amplitude is a J-free interval about 0 and the exact x of h vanishes). Arithmetic: intervals of decimal endpoints with directed
rounding (prec 50; lower ends ROUND_FLOOR, upper ends ROUND_CEILING); inputs are decimal strings read exactly. Records (MR_INPUT_KV_v1):
MR_SPECTRAL, MR_INSERT, MR_EXACT, MR_CRUDEX, MR_JOINT; their values are float stand-ins from midrow/out/g3_model_v1_N*.json and
g6_model_v1_N*.json with the bars of g6_eval_v1, certified constants where they exist (tau4, R_w, rho1, Bp_hi), and the Lemma HW bounds of
g6_hw_v1. Gates: G-PIN (record sha256 against PINS.txt), G-COUNT (to-do orbits per n against the brute-force counts of G3), G-CORNER
(corner twins give equal lower bounds), G-FLOAT (per n and N the minimum headroom against g6_eval_v1's GATE6 VPLAN lines, relative 1e-3).
Outputs: CLASS and SAMEBOND lines, SUMMARY lines, gate lines, and the output record MR_ASSEMBLY_<BASE|plant>.kv. FLOAT PROTOTYPE: the
certified engine reads certified records with per-piece uniformity; nothing here is a certificate."""
import hashlib, json, os, re, sys
from decimal import Decimal as Dm, localcontext, ROUND_FLOOR, ROUND_CEILING

W = '/mnt/g2/release/root/code/'
OUT = W + 'pk24/midrow/out/proto_rec_v1/'
M3 = {4: W + 'pk24/midrow/out/g3_model_v1_N4.json', 3: W + 'pk24/midrow/out/g3_model_v1_N3.json'}
M6 = {4: W + 'pk24/midrow/out/g6_model_v1_N4.json', 3: W + 'pk24/midrow/out/g6_model_v1_N3.json'}
G6E = W + 'pk24/midrow/out/g6_eval_v1.out'
SV = (W + 'pk07/out/export_kt_s9h_v1_2_vsweep.kv', '10f3c3d9a18b9c7a596121a8dbec7d2b82afb366704845a7c00e066c8bf6d4f6')
TAU4 = {4: '0.027702', 3: '0.026922'}
BPERP = {4: '0.032', 3: '0.025'}
HWF = {4: {'t': '1.319565', 'h': '1.726959'}, 3: {'t': '0.942249', 'h': '1.434519'}}      # g6_hw_v1: bound on |M_c S|
HWPE = {4: {'t': '1.109069', 'h': '1.452174'}, 3: {'t': '0.811120', 'h': '1.290696'}}     # g6_hw_v1: bound on |M_c S P_e|
JLOW = {4: 350.0, 3: 300.0}
JMAX = {4: (3.37e3, 5.30e5, 8.34e7, 1.31e10, 2.07e12), 3: (3.11e3, 4.89e5, 7.69e7, 1.21e10, 1.90e12)}
EXB, CB, MEB, LA = 0.01, 0.01, 0.02, 1e-3
EXPECT = {6: 25, 7: 37, 8: 52, 9: 69, 10: 89, 11: 111, 12: 136, 13: 163, 14: 193, 15: 225, 16: 260, 17: 297, 18: 337, 19: 379, 20: 424, 21: 471, 22: 521, 23: 573, 24: 628, 25: 685, 26: 745, 27: 807, 28: 872, 29: 939, 30: 1009}
PREC = 50
RX = re.compile(r'^(t|h|bb|a|b)(\d+)$')
ROW = {'t': 0, 'h': 1, 'bb': 2}


class Iv:
    __slots__ = ('lo', 'hi')

    def __init__(s, lo, hi=None):
        s.lo, s.hi = lo, (lo if hi is None else hi)
        assert s.lo <= s.hi, (s.lo, s.hi)

    def _r(self, fn, mode):
        with localcontext() as c:
            c.prec, c.rounding = PREC, mode
            return fn()

    def __add__(s, o):
        o = cv(o)
        return Iv(s._r(lambda: s.lo + o.lo, ROUND_FLOOR), s._r(lambda: s.hi + o.hi, ROUND_CEILING))

    def __sub__(s, o):
        o = cv(o)
        return Iv(s._r(lambda: s.lo - o.hi, ROUND_FLOOR), s._r(lambda: s.hi - o.lo, ROUND_CEILING))

    def __mul__(s, o):
        o = cv(o)
        ends = [(a, b) for a in (s.lo, s.hi) for b in (o.lo, o.hi)]
        return Iv(min(s._r(lambda a=a, b=b: a * b, ROUND_FLOOR) for a, b in ends),
                  max(s._r(lambda a=a, b=b: a * b, ROUND_CEILING) for a, b in ends))

    def inv(s):
        assert s.lo > 0
        return Iv(s._r(lambda: 1 / s.hi, ROUND_FLOOR), s._r(lambda: 1 / s.lo, ROUND_CEILING))

    def __truediv__(s, o):
        return s * cv(o).inv()

    def __pow__(s, k):
        r = Iv(Dm(1))
        for _ in range(k):
            r = r * s
        return r

    def amax(s):
        return max(abs(s.lo), abs(s.hi))

    def sqrt(s):
        assert s.lo >= 0
        return Iv(s._r(lambda: s.lo.sqrt(), ROUND_FLOOR), s._r(lambda: s.hi.sqrt(), ROUND_CEILING))


def cv(x):
    return x if isinstance(x, Iv) else Iv(Dm(str(x)))


def iv2(lo, hi):
    return Iv(Dm(str(lo)), Dm(str(hi)))


def up(x):
    """an upper-bound interval [0, x] style scalar as a point interval"""
    return Iv(Dm(str(x)))


def sha(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()


# ---------------------------------------------------------------- classes (as midrow/g6_eval_v1.py)
def span(name):
    m = RX.match(name)
    ty, i = m.group(1), int(m.group(2))
    return (i, i + 1) if ty in ROW else (i, i)


def image(name, n, flip, refl):
    m = RX.match(name)
    ty, i = m.group(1), int(m.group(2))
    if flip:
        ty = {'t': 'bb', 'bb': 't', 'a': 'b', 'b': 'a'}.get(ty, ty)
    if refl:
        i = (n - i) if ty in ROW else (n + 1 - i)
    return '%s%d' % (ty, i)


def canon(e, f, n):
    return min(tuple(sorted((image(e, n, fl, rf), image(f, n, fl, rf)))) for fl in (0, 1) for rf in (0, 1))


def position(e, f, n):
    for rf in (0, 1):
        a, b = image(e, n, 0, rf), image(f, n, 0, rf)
        for x, y in ((a, b), (b, a)):
            if RX.match(x).group(1) != 'h':
                continue
            sx, sy = span(x), span(y)
            if sy[0] < sx[0] or (sy[0] == sx[0] and RX.match(y).group(1) == 'h' and int(RX.match(y).group(2)) < int(RX.match(x).group(2))):
                continue
            ty = {'bb': 't', 'b': 'a'}.get(RX.match(y).group(1), RX.match(y).group(1))
            i, j = int(RX.match(x).group(2)), int(RX.match(y).group(2))
            return ty, i - 2, sy[0] - sx[1] - 1, (n - j - 2) if RX.match(y).group(1) in ROW else (n - j - 1), (x, y)
    return None


def edges(n):
    E = {}
    for r, nm in ((0, 't'), (1, 'h'), (2, 'bb')):
        for i in range(1, n):
            E['%s%d' % (nm, i)] = ((r, i), (r, i + 1))
    for nm, r in (('a', 0), ('b', 1)):
        for j in range(1, n + 1):
            E['%s%d' % (nm, j)] = ((r, j), (r + 1, j))
    return E


def todo(n):
    E = edges(n)
    names = sorted(E)
    out = set()
    for ia in range(len(names)):
        for ib in range(ia + 1, len(names)):
            e, f = names[ia], names[ib]
            if 'h' not in (RX.match(e).group(1), RX.match(f).group(1)):
                continue
            if set(E[e]) & set(E[f]) or image(e, n, 0, 1) == f:
                continue
            out.add(canon(e, f, n))
    return sorted(out)


def corner_twin(e, f, n):
    tw = {'t1': 'a1', 'a1': 't1', 't%d' % (n - 1): 'a%d' % n, 'a%d' % n: 't%d' % (n - 1),
          'bb1': 'b1', 'b1': 'bb1', 'bb%d' % (n - 1): 'b%d' % n, 'b%d' % n: 'bb%d' % (n - 1)}
    E = edges(n)
    out = []
    for x, y in ((e, f), (f, e)):
        if y in tw and x != y and not (set(E[y]) & set(E[tw[y]]) & set(E[x])):
            out.append(canon(x, tw[y], n))
    return out


# ---------------------------------------------------------------- writer
def kv_write(path, record, fields, rows, source):
    lines = ['# %s: stand-in input record of the M1 engine prototype (float values; not certified)' % record,
             'FORMAT = MR_INPUT_KV_v1', 'RECORD = %s' % record, 'PRODUCER = pk24 g6_engine_proto_v1 write', 'STATUS = FLOAT-STANDIN',
             'SOURCE = %s' % source,
             'J_UNIFORMITY = PROTOTYPE: piece P0 is J = J_low; piece P1 is t -> 0 with J-free stand-ins (a certified record states per-piece uniformity)',
             'FIELDS = %s' % ' '.join(fields)]
    for k, vals in rows:
        lines.append('%s = %s' % (k, ' '.join(repr(float(v)) if not isinstance(v, str) else v for v in vals)))
    with open(path, 'x') as fh:
        fh.write('\n'.join(lines) + '\n')


def write():
    os.makedirs(OUT, exist_ok=False)
    assert sha(SV[0]) == SV[1]
    RW, RHO1, BP = {}, {}, {}
    fields = None
    for ln in open(SV[0]):
        if ln.startswith('FIELDS'):
            fields = ln.split('=', 1)[1].split()
        mm = re.match(r'^N(\d)_P\d+ = (.*?) \|', ln)
        if mm and fields:
            v = dict(zip(fields, [float(x) for x in mm.group(2).split()]))
            N = int(mm.group(1))
            RW[N] = max(RW.get(N, 0.0), v['Rw_hi'])
            RHO1[N] = max(RHO1.get(N, 0.0), v['rho1_hi'])
            BP[N] = max(BP.get(N, 0.0), v['Bp_hi'])
    src = ' '.join('%s:%s' % (os.path.basename(p), sha(p)[:8]) for p in [M3[4], M3[3], M6[4], M6[3], SV[0]])
    spec, ins, exa, crx, jnt = [], [], [], [], []
    for N in (4, 3):
        m3, m6 = json.load(open(M3[N])), json.load(open(M6[N]))
        sx, sy, tau = m3['sx'], m3['sy'], float(TAU4[N])
        cxm, cym = m6['eps']['-1']['cx'], m6['eps']['-1']['cy']
        for P in ('P0', 'P1'):
            jl, jh = (JLOW[N], JLOW[N]) if P == 'P0' else ('inf', 'inf')
            spec.append(('N%d_%s' % (N, P), [str(jl), str(jh), sx, sx, sy, sy, tau, RHO1[N], RW[N],
                                             cxm * (1 - CB), cxm * (1 + CB), cym * (1 - CB), cym * (1 + CB)]))
            for X in ('h', 't', 'a'):
                b, me = m6['bulk'][X], m6['me'][X]
                if X == 'a':
                    W_ = [me['xx'], me['xy'], me['yy']]
                    peb = [me['Pe_x'] * (1 + MEB), me['Pe_y'] * (1 + MEB)]
                    pevw, win, hwf, hwpe, wf = tau * b['Pe_v'], BP[N], BP[N], BP[N], 0
                else:
                    W_ = [sx * sx * me['xx'], sx * sy * me['xy'], sy * sy * me['yy']]
                    peb = [tau * sx * me['Pe_x'] * (1 + MEB), tau * sy * me['Pe_y'] * (1 + MEB)]
                    pevw, win, hwf, hwpe, wf = tau * b['Pe_v'], float(BPERP[N]), float(HWF[N][X]), float(HWPE[N][X]), 1
                row = [b['vx'] - LA * abs(b['vx']), b['vx'] + LA * abs(b['vx']), b['vy'] - LA * abs(b['vy']), b['vy'] + LA * abs(b['vy']),
                       pevw, b['Pe_v'], b['v_even'] * (1 + LA)]
                for wv in W_:
                    row += [wv - MEB * abs(wv), wv + MEB * abs(wv)]
                row += peb + [win, hwf, hwpe, str(wf)]
                ins.append(('N%d_%s_%s' % (N, P, X), row))
            for X, d in (('h', -1), ('h', 0), ('t', -1)):
                v = m3['vec']['%s%d' % (X, d)]
                ax_lo, ax_hi = (v['Ax'] * (1 - EXB), v['Ax'] * (1 + EXB))
                if P == 'P1' and X == 'h':
                    ax_lo, ax_hi = 0.0, v['Ax']          # O(t): vanishes at t -> 0 with its certified sign
                evn = (v['Ax'] ** 2 + v['Ay'] ** 2 + v['Re'] ** 2) ** 0.5
                exa.append(('N%d_%s_%s%d' % (N, P, X, d), [abs(v['Ay']) * (1 - EXB), abs(v['Ay']) * (1 + EXB), ax_lo, ax_hi,
                                                          v['Re'] * (1 + EXB), v['V'] * 1.01, evn * 1.01, abs(v['Ay'])]))
            for d in range(1, 13):
                ax = m3['vec']['h%d' % min(d, m3['DMAX'])]['Ax']
                jm = JMAX[N][d] if d < 5 else JMAX[N][-1] * 157.0 ** (d - 4)
                rel = JLOW[N] / jm
                if P == 'P0':
                    crx.append(('N%d_P0_h%d' % (N, d), [ax * (1 - rel), ax * (1 + rel)]))
                else:
                    crx.append(('N%d_P1_h%d' % (N, d), [-abs(ax) * rel, abs(ax) * rel]))
            jt = m6['joint']
            cb = jt['C_bulk']
            xi0 = cb + m6['c']['h'] * m6['c']['t']
            jnt.append(('N%d_%s' % (N, P), [cb * (1 - EXB), cb * (1 + EXB), sx * abs(jt['wJ_x']) * (1 + MEB), sy * abs(jt['wJ_y']) * (1 + MEB),
                                            tau * jt['Pe_wJ'] * (1 + MEB), jt['full_window_Xic'] * 1.1, m6['bulk']['h']['v_even'] * 1.01,
                                            m6['bulk']['t']['v_even'] * 1.01, abs(xi0) * 1.01, abs(m6['c']['h'] * m6['c']['t']) * 1.01, cb]))
    kv_write(OUT + 'MR_SPECTRAL.kv', 'MR_SPECTRAL', 'jlo jhi sx_lo sx_hi sy_lo sy_hi tau_hi rho1_hi Rw_hi cxm1_lo cxm1_hi cym1_lo cym1_hi'.split(),
             spec, src)
    kv_write(OUT + 'MR_INSERT.kv', 'MR_INSERT', ('vx_lo vx_hi vy_lo vy_hi Pevw_hi Pev_hi vp_hi Wxx_lo Wxx_hi Wxy_lo Wxy_hi Wyy_lo Wyy_hi '
                                                 'PeBwux_hi PeBwuy_hi win_hi muHWf_hi muHWpe_hi windowed').split(), ins, src)
    kv_write(OUT + 'MR_EXACT.kv', 'MR_EXACT', 'Ay_lo Ay_hi Ax_lo Ax_hi Pe_hi norm_hi evnorm_hi Ay_mid'.split(), exa, src)
    kv_write(OUT + 'MR_CRUDEX.kv', 'MR_CRUDEX', 'ax_lo ax_hi'.split(), crx, src)
    kv_write(OUT + 'MR_JOINT.kv', 'MR_JOINT', ('Cb_lo Cb_hi wJwx_hi wJwy_hi PewJw_hi jfw_hi vh_hi vtp_hi xi0_hi chct_hi Cb_mid').split(), jnt, src)
    pins = ['%s  %s' % (sha(OUT + f), f) for f in ('MR_SPECTRAL.kv', 'MR_INSERT.kv', 'MR_EXACT.kv', 'MR_CRUDEX.kv', 'MR_JOINT.kv')]
    with open(OUT + 'PINS.txt', 'x') as fh:
        fh.write('\n'.join(pins) + '\n')
    for p in pins:
        print('WROTE %s' % p)


# ---------------------------------------------------------------- engine
def kv_read(path, corrupt=False):
    raw = open(path, 'rb').read()
    if corrupt:
        raw = raw.replace(b'MR_', b'MX_', 1)
    txt = raw.decode()
    fields, rows, head = None, {}, {}
    for ln in txt.splitlines():
        if ln.startswith('#') or not ln.strip():
            continue
        k, v = [x.strip() for x in ln.split('=', 1)]
        if k == 'FIELDS':
            fields = v.split()
        elif fields is None:
            head[k] = v
        else:
            rows[k] = dict(zip(fields, v.split()))
    return hashlib.sha256(raw).hexdigest(), head, rows


def run(plant):
    print('g6_engine_proto_v1_1 run: PLANT %s' % (plant or 'none'))
    pins = dict((l.split()[1], l.split()[0]) for l in open(OUT + 'PINS.txt').read().splitlines())
    recs, bad = {}, []
    for f in ('MR_SPECTRAL.kv', 'MR_INSERT.kv', 'MR_EXACT.kv', 'MR_CRUDEX.kv', 'MR_JOINT.kv'):
        h, head, rows = kv_read(OUT + f, corrupt=(plant == 'PIN' and f == 'MR_INSERT.kv'))
        recs[f.split('.')[0]] = rows
        ok = h == pins[f]
        print('G-PIN %s %s %s' % (f, h[:8], 'OK' if ok else 'MISMATCH against %s' % pins[f][:8]))
        if not ok:
            bad.append(f)
    if bad:
        print('G-PIN FIRED: %s; the engine stops' % bad)
        print('PLANT %s: %s' % (plant, 'FIRED' if plant == 'PIN' else 'UNEXPECTED STOP'))
        return 0 if plant == 'PIN' else 8
    g6 = {}
    for ln in open(G6E):
        mm = re.match(r'^GATE6 VPLAN N=(\d) n=(\d+): .*min H_low (\S+) at .*min H_inf (\S+) at', ln)
        if mm:
            g6[(int(mm.group(1)), int(mm.group(2)))] = (float(mm.group(3)), float(mm.group(4)))
    out_rows, nfail, gate_fail = [], 0, []
    nmax = 14 if plant is None else 10           # plants run on n = 6..10, where each of them must fire
    for N in (4, 3):
        for n in range(6, nmax + 1):
            classes = todo(n)
            if plant == 'COUNT' and n == 10:
                classes = classes[:-1]
            cnt_ok = len(classes) == EXPECT[n]
            if not cnt_ok:
                gate_fail.append('G-COUNT N%d n%d: %d against %d' % (N, n, len(classes), EXPECT[n]))
            res_n = {}
            minH = {'P0': 1e99, 'P1': 1e99}
            for P in ('P0', 'P1'):
                sp_ = recs['MR_SPECTRAL']['N%d_%s' % (N, P)]
                sx, sy = iv2(sp_['sx_lo'], sp_['sx_hi']), iv2(sp_['sy_lo'], sp_['sy_hi'])
                tau = up(sp_['tau_hi'])
                if plant == 'TAU2':
                    tau = tau * 10
                rho1, Rw = up(sp_['rho1_hi']), up(sp_['Rw_hi'])
                cxm, cym = iv2(sp_['cxm1_lo'], sp_['cxm1_hi']), iv2(sp_['cym1_lo'], sp_['cym1_hi'])
                cmin = lambda z: min(abs(z.lo), abs(z.hi)) if z.lo * z.hi > 0 else Dm(0)
                pem1 = (Rw * Rw - Iv(cmin(cxm)) * Iv(cmin(cxm)) - Iv(cmin(cym)) * Iv(cmin(cym))).sqrt()

                def e_(d):
                    return Rw * (rho1 ** (d + 1))

                def pen(d):
                    return (tau ** (d + 1)) * pem1

                def cx(d):
                    return (sx ** (d + 1)) * cxm

                def cy(d):
                    return (sy ** (d + 1)) * cym

                def end(X, d):
                    """(Ay iv, Ax iv, N' hi (iv), Pe hi (iv), norm hi (iv), Ay central)"""
                    if (X == 'h' and d <= 0) or (X in ('t', 'a') and d <= -1):
                        key = 'N%d_%s_%s%d' % (N, P, 't' if X == 'a' else X, d)
                        r = recs['MR_EXACT'][key]
                        pe = up(r['Pe_hi'])
                        return (iv2(r['Ay_lo'], r['Ay_hi']), iv2(r['Ax_lo'], r['Ax_hi']), tau * pe, pe, up(r['norm_hi'] if X == 'h' else r['evnorm_hi']),
                                float(r['Ay_mid']))
                    r = recs['MR_INSERT']['N%d_%s_%s' % (N, P, X)]
                    Wxx, Wxy, Wyy = iv2(r['Wxx_lo'], r['Wxx_hi']), iv2(r['Wxy_lo'], r['Wxy_hi']), iv2(r['Wyy_lo'], r['Wyy_hi'])
                    vx, vy = iv2(r['vx_lo'], r['vx_hi']), iv2(r['vy_lo'], r['vy_hi'])
                    vp, win = up(r['vp_hi']), up(r['win_hi'])
                    if r['windowed'] == '1':
                        mxx, mxy, myy = Wxx / (sx * sx), Wxy / (sx * sy), Wyy / (sy * sy)
                        pbx, pby = up(r['PeBwux_hi']) / sx, up(r['PeBwuy_hi']) / sy      # |P_e B^w u_a| / s_a
                        dB, dP = d, d
                        rem_y = pby * pen(dB - 1) + vp * e_(dB) * Iv(cy(dP).amax())
                        rem_x = pbx * pen(dB - 1) + vp * e_(dB) * Iv(cx(dP).amax())
                        npr = up(r['Pevw_hi']) + Iv(cx(dB).amax()) * pbx + Iv(cy(dB).amax()) * pby + win * pen(dB - 1) + vp * e_(dB) * tau * pen(dP)
                        hwf, hwpe = up(r['muHWf_hi']), up(r['muHWpe_hi'])
                        pe = (up(r['Pev_hi']) + Iv(cx(dB).amax()) * hwf / sx + Iv(cy(dB).amax()) * hwf / sy + hwpe * pen(dB - 1) +
                              vp * e_(dB) * pen(dP))
                    else:
                        mxx, mxy, myy = Wxx, Wxy, Wyy                                    # the vertical B_a is bounded: no window
                        pbx, pby = up(r['PeBwux_hi']), up(r['PeBwuy_hi'])
                        dB, dP = d - 1, d
                        rem_y = pby * pen(dB) + vp * e_(dB) * Iv(cy(dP).amax())
                        rem_x = pbx * pen(dB) + vp * e_(dB) * Iv(cx(dP).amax())
                        core = up(r['Pev_hi']) + Iv(cx(dB).amax()) * pbx + Iv(cy(dB).amax()) * pby + vp * e_(dB) * pen(dP)
                        npr = tau * (core + win * pen(dB))
                        pe = core + win * pen(dB)
                    lead_y = cx(dB) * mxy + cy(dB) * myy
                    lead_x = cx(dB) * mxx + cy(dB) * mxy
                    if plant == 'OPN':
                        bar = (win * e_(dB - 1)) / sy if r['windowed'] == '1' else win * e_(dB)
                        Ay = vy + Iv(-bar.hi, bar.hi)
                    else:
                        Ay = vy + lead_y + Iv(-rem_y.hi, rem_y.hi)
                    Ax = vx + lead_x + Iv(-rem_x.hi, rem_x.hi)
                    if r['windowed'] == '1':
                        nrm = vp + hwf * e_(dB - 1) + vp * e_(dB) * e_(dP)
                    else:
                        nrm = vp + win * e_(dB) + vp * e_(dB) * e_(dP)
                    ayc = float((vy.lo + vy.hi) / 2 + (lead_y.lo + lead_y.hi) / 2)
                    return Ay, Ax, npr, pe, nrm, ayc

                cache = {}

                def endc(X, d):
                    if (X, d) not in cache:
                        cache[(X, d)] = end(X, d)
                    return cache[(X, d)]

                for c in classes:
                    ty, d, kr, dp, ori = position(c[0], c[1], n)
                    m = kr + 2 if ty in ('t', 'h') else kr + 1
                    if m == 0:
                        continue
                    lab = '%s-%s' % ori
                    AyL, AxL, nL, peL, nrL, aycL = endc('h', d)
                    AyR, AxR, nR, peR, nrR, aycR = endc(ty, dp)
                    if d >= 1:
                        r = recs['MR_CRUDEX']['N%d_%s_h%d' % (N, P, min(d, 12))]
                        AxL = iv2(r['ax_lo'], r['ax_hi'])
                        if plant == 'SIGN':
                            AxL = Iv(-AxL.amax(), AxL.amax())
                    if ty == 'h' and dp >= 1:
                        r = recs['MR_CRUDEX']['N%d_%s_h%d' % (N, P, min(dp, 12))]
                        AxR = iv2(r['ax_lo'], r['ax_hi'])
                        if plant == 'SIGN':
                            AxR = Iv(-AxR.amax(), AxR.amax())
                    route = 'chan-crude' if (d >= 1 or (ty == 'h' and dp >= 1)) else 'chan-exact'
                    fail_reason = ''
                    if AyL.lo <= 0 or AyR.lo <= 0:
                        Ylo = Iv(Dm(0))
                        fail_reason = 'y lower end <= 0'
                    else:
                        Ylo = (Iv(sy.lo) ** m) * Iv(AyL.lo) * Iv(AyR.lo)
                    x = (sx ** m) * AxL * AxR
                    Xb = Iv(-x.lo) if x.lo < 0 else Iv(Dm(0))
                    if m >= 2:
                        R = (tau ** (m - 2)) * nL * nR
                    else:
                        R = Iv(min((peL * nR).hi, (nL * peR).hi))
                    eL, eR = e_(d), e_(dp)
                    dz = (Iv(sx.hi) ** m) * eL * eR
                    T2 = (Iv(sx.hi) ** (2 * m)) * nrL * nrR * eL * eR / (Iv(Dm(1)) - dz)
                    if plant == 'T2':
                        T2 = T2 * 1000
                    marg = Ylo - Xb - R - T2
                    Llo = (marg / (Iv(Dm(1)) + dz)).lo if marg.lo > 0 else marg.lo
                    yc = float(sy.lo) ** m * aycL * aycR
                    den = yc - float(Ylo.lo) + float(Xb.hi) + float(R.hi) + float(T2.hi)
                    H = yc / den if den > 0 else float('inf')
                    verdict = 'PASS' if marg.lo > 0 else 'FAIL'
                    if verdict == 'FAIL':
                        nfail += 1
                    res_n.setdefault(c, {})[P] = (float(Llo), H, verdict, route, d, kr, dp, m, lab, fail_reason)
                    minH[P] = min(minH[P], H)
            # same-bond orbits (Proposition J)
            sbl = []
            for i in range(2, n // 2 + 1):
                for P in ('P0', 'P1'):
                    sp_ = recs['MR_SPECTRAL']['N%d_%s' % (N, P)]
                    sx, sy = iv2(sp_['sx_lo'], sp_['sx_hi']), iv2(sp_['sy_lo'], sp_['sy_hi'])
                    tau, rho1, Rw = up(sp_['tau_hi']), up(sp_['rho1_hi']), up(sp_['Rw_hi'])
                    cxm, cym = iv2(sp_['cxm1_lo'], sp_['cxm1_hi']), iv2(sp_['cym1_lo'], sp_['cym1_hi'])
                    pem1 = (Rw * Rw - Iv(min(abs(cxm.lo), abs(cxm.hi))) ** 2 - Iv(min(abs(cym.lo), abs(cym.hi))) ** 2).sqrt()
                    j = recs['MR_JOINT']['N%d_%s' % (N, P)]
                    dL, dR = i - 2, n - i - 2
                    fo = Iv(Dm(0))
                    for dd in (dL, dR):
                        fo = fo + Iv(((sx ** dd) * cxm).amax()) * up(j['wJwx_hi']) + Iv(((sy ** dd) * cym).amax()) * up(j['wJwy_hi']) + \
                            (tau ** dd) * pem1 * up(j['PewJw_hi'])
                    eL, eR = Rw * (rho1 ** (dL + 1)), Rw * (rho1 ** (dR + 1))
                    epL, epR = Rw * (rho1 ** dL), Rw * (rho1 ** dR)
                    r2 = up(j['jfw_hi']) * epL * epR + up(j['vh_hi']) * up(j['vtp_hi']) * (eL + eR) ** 2 + \
                        (up(j['xi0_hi']) + up(j['chct_hi']) * 3) * eL * eR
                    LJ = iv2(j['Cb_lo'], j['Cb_hi']).lo - (fo + r2).hi
                    cbm = float(j['Cb_mid'])
                    HJ = cbm / (cbm - float(LJ)) if cbm > float(LJ) else float('inf')
                    sbl.append((i, P, float(LJ), HJ, 'PASS' if LJ > 0 else 'FAIL'))
                    if LJ <= 0:
                        nfail += 1
            # corner twins
            for c in classes:
                for tw in corner_twin(c[0], c[1], n):
                    if tw in res_n and c in res_n and tw != c and c < tw:
                        for P in ('P0', 'P1'):
                            a_, b_ = res_n[c][P][0], res_n[tw][P][0]
                            if abs(a_ - b_) > 1e-12 * max(abs(a_), abs(b_), 1e-300):
                                gate_fail.append('G-CORNER N%d n%d %s/%s %s: %.6e vs %.6e' % (N, n, res_n[c][P][8], res_n[tw][P][8], P, a_, b_))
            ref = g6.get((N, n))
            fl0 = abs(minH['P0'] / ref[0] - 1) if ref else float('nan')
            fl1 = abs(minH['P1'] / ref[1] - 1) if ref else float('nan')
            band_ok = (minH['P0'] <= ref[0] * (1 + 1e-3) and minH['P1'] <= ref[1] * (1 + 1e-3) and minH['P0'] >= 2 and minH['P1'] >= 2)
            if plant is None and not band_ok:
                gate_fail.append('G-FLOAT N%d n%d: min H %.4f / %.4f against g6_eval %.4f / %.4f (band: not above it by more than 0.1%%, '
                                 'and >= 2)' % (N, n, minH['P0'], minH['P1'], ref[0], ref[1]))
            nchan = len(res_n)
            npass = sum(1 for c in res_n if all(res_n[c][P][2] == 'PASS' for P in ('P0', 'P1')))
            print('SUMMARY N=%d n=%d: to-do orbits %d (expected %d, %s); channel classes %d, PASS on both pieces %d; min H P0 %.3f P1 %.3f '
                  '(g6_eval %s); same-bond interior orbits %d, min H_J %.2f; G-FLOAT rel %.1e / %.1e' % (
                      N, n, len(classes), EXPECT[n], 'ok' if cnt_ok else 'MISMATCH', nchan, npass, minH['P0'], minH['P1'],
                      ('%.3f / %.3f' % ref) if ref else '-', len(set(i for i, P, *_ in sbl)), min([s[3] for s in sbl] or [float('inf')]), fl0, fl1))
            for c in sorted(res_n, key=lambda c: res_n[c]['P0'][8]):
                r0, r1 = res_n[c]['P0'], res_n[c]['P1']
                out_rows.append(('N%d_n%02d_%s' % (N, n, r0[8]), [r0[3], r0[4], r0[5], r0[6], r0[7], r0[0], r1[0], min(r0[1], r1[1]),
                                                                    'PASS' if r0[2] == r1[2] == 'PASS' else 'FAIL']))
                if n in (6, 7) or r0[2] != 'PASS' or r1[2] != 'PASS':
                    print('CLASS N=%d n=%d %-8s route=%s d=%d k=%d dp=%d m=%d P0: L %.4e H %.2f %s; P1: L %.4e H %.2f %s %s' % (
                        N, n, r0[8], r0[3], r0[4], r0[5], r0[6], r0[7], r0[0], r0[1], r0[2], r1[0], r1[1], r1[2], r0[9] or r1[9]))
            for i, P, LJ, HJ, vd in sbl:
                out_rows.append(('N%d_n%02d_h%d-t%d_%s' % (N, n, i, i, P), ['same-bond', i - 2, -2, n - i - 2, 0, LJ, LJ, HJ, vd]))
    for g in gate_fail[:20]:
        print(g)
    print('GATES: %d gate lines fired' % len(gate_fail))
    tag = plant or 'BASE'
    path = OUT + 'MR_ASSEMBLY_%s_v1_1.kv' % tag
    lines = ['# MR_ASSEMBLY: prototype output (float stand-ins; not a certificate)', 'FORMAT = MR_ASSEMBLY_KV_v1',
             'RECORD = MR_ASSEMBLY_%s_v1_1' % tag, 'PRODUCER = pk24 g6_engine_proto_v1_1 run', 'INPUT_PINS = %s' % ' '.join(
                 '%s:%s' % (k, v[:8]) for k, v in sorted(pins.items())), 'RUN_VERDICT = %s' % ('VALID' if (nfail == 0 and not gate_fail) else 'INVALID'),
             'FIELDS = route d k dp m Lmin_P0 Lmin_P1 Hmin verdict']
    lines += ['%s = %s' % (k, ' '.join(str(x) for x in v)) for k, v in out_rows]
    with open(path, 'x') as fh:
        fh.write('\n'.join(lines) + '\n')
    print('WROTE %s %s (%d rows); FAIL rows %d' % (sha(path)[:8], path, len(out_rows), nfail))
    if plant is None:
        print('RUN_VERDICT %s' % ('VALID' if (nfail == 0 and not gate_fail) else 'INVALID'))
        return 0 if (nfail == 0 and not gate_fail) else 9
    fired = nfail > 0 or len(gate_fail) > 0
    print('PLANT %s: %s (FAIL rows %d, gate lines %d)' % (plant, 'FIRED' if fired else 'NOT FIRED', nfail, len(gate_fail)))
    return 0 if fired else 9


if __name__ == '__main__':
    if sys.argv[1] == 'write':
        write()
    else:
        sys.exit(run(sys.argv[2] if len(sys.argv) > 2 else None))
