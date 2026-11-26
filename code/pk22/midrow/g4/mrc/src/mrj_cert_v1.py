#!/usr/bin/env python3
"""mrj_cert_v1.py (pk22; MR_JOINT for engine v1_8_4's Proposition J, G7; the P0_LOG rows 4390, 4489-4494), made from the template
mrj_cert_v1.tmpl.py by make_mrj_v1.py, which fills the pins by tool. One CERTIFIED MR_JOINT record for both N on R4's grid (MR_SPECTRAL's keys
and jlo, jhi strings), MR_INPUT_KV_v4, FIELDS jlo jhi Cb_lo Cb_hi Cb_mid wJwx_hi wJwy_hi PewJw_hi jfw_hi A0_hi ch_lo ch_hi ct_lo ct_hi bh_hi
bt_hi Wc_hi (G6 v1_6_2 sect. 6), every term of G6 v1_1 sect. 5 (Proposition J, the exact form) as engine v1_8_4's sb_piece reads it.
Notation: Xi = M_t M_h; c_t = <u, M_t u>, c_h = <u, M_h u> (the true centres); M := M_c,t M_c,h = (M_t - c_t)(M_h - c_h), symmetric (M_t and M_h
are multipliers of the same column step and commute); Xi_c = Xi - c_t M_h - c_h M_t = M - c_t c_h; C_bulk = <u, M u>; w_J = Q0 Xi_c u = Q0 M u.
Inputs (uniform claims of every record; t a ball over the piece):
- the trial Ritz vectors u~_k = sum_b V_kb psi_b with V_kb = uhat_kb / |psi_b| (pk25's MR_LEMMAP v3 uhat, |psi_b| = G_bb^1/2 from the S9
  records' G entries), q_k and eps_jk (L3), delta_k = (2 (q_k^2 + sum_(j != k) eps_jk^2))^1/2 >= |u_k - u~_k|;
- the trial-state norms kappa_k = sum_b |V_kb| Sh_b^1/2 >= |K'^-1/2 u~_k| (pk25's DH record Sh,b; the form of pk25's MR_INSERT producer);
- the D-graph entries: JTH,b,c = <psi_b, Xi psi_c> and DHT,b,c = <psi_b, M_t psi_c> (c3j's DJ record), Gxh,b,c = <psi_b, M_h psi_c> (pk25's DH);
- the N-1 constants (pk25's certified MR_INSERT cert run, frozen output): OR_t and OR_h (the mu tool's one-row bounds on the intervals that
  contain the true centres: c_t's range from R4's certified means export, c_h's Ritz range +-0.01) and C_t = OR_t kappa_max^1/2, C_h = OR_h
  kappa_max^1/2 (MR_INSERT's t and h C_hi, which C-MU-PRINT ties to the printed lines).
Per piece:
- ct0 = <u~_0, M_t u~_0>, ch0 = <u~_0, M_h u~_0>, A~ = <u~_0, Xi u~_0>; c_t in ct0 +- dt, dt = delta_0 (C_t + OR_t kappa_0); c_h in ch0 +- dh,
  dh = delta_0 (C_h + OR_h kappa_0) (pk25's producer's forms; C-CH-HULL: c_h's interval inside the mu tool's, C-CT-RANGE: c_t's meets the
  means range);
- Wc = OR_t C_h >= OR_t OR_h kappa_max^1/2 >= C_J >= |M u| >= |w_J| (pk25's note v2_5 sect. 10; |M K'^1/2| = OR_t OR_h on K' = a (x) a (x) a);
  TRP = OR_t OR_h, so |M u~_k| <= TRP kappa_k (the trial-state route);
- C_bulk: <u~_0, M u~_0> = A~ - c_h ct0 - c_t ch0 + c_t c_h = A~ - ct0 ch0 + (c_t - ct0)(c_h - ch0) exactly (|u~_0| = 1), and
  |<u, M u> - <u~_0, M u~_0>| <= delta_0 (|M u| + |M u~_0|), so C_bulk in A~ - ct0 ch0 +- (dt dh + delta_0 (Wc + TRP kappa_0));
- w_J,a = <u_a, M u> (a = x, y; u_a is orthogonal to u): the trial value <u~_a, M u~_0> = JTH_a0 - c_h DHT_a0 - c_t Gxh_a0 (<u~_a, u~_0> = 0)
  with c_t, c_h as intervals, and the error min(delta_a Wc + TRP kappa_a delta_0, delta_0 Wc s_a^-1/2 + TRP kappa_0 delta_a) (|M u_a| <= C_J
  s_a^-1/2 by N-1 at level a; G6 4.4's trial-state route); wJw_a = s_a,hi |w_J,a|_hi;
- PewJw = tau Wc (>= |P_e S w_J|); jfw = Wc s_x^3/2 + |c_t| |c_h| s_x^2 >= |Q0 S Xi_c S Q0| on flip-even vectors (N-1 with Pi the flip-even
  u-perp projection, |S Pi| <= s_x); A0 = |C_bulk| + |c_t| |c_h| >= |<u, Xi u>|; bh = C_h s_x^3/2, bt = C_t s_x^3/2 (G6's C s_x^3/2).
Gates: C-SRC, C-MANIFEST, C-HEADERS, C-KEYS, C-MU-PRINT, C-SH-POS, C-CH-HULL, C-CT-RANGE, C-MIRROR (JTHr,1,0 against JTH,0,1), C-FINITE,
C-ROUND, C-FLOAT (joint_float_v1's J_low values inside the intervals), C-TOL (G6 v1_1 sect. 5's crude tolerances for H_J >= 10: Wc,
jfw and C_bulk's relative bar, INFO-grade but required); plants PLANT-MU-PRINT, PLANT-CH-HULL, PLANT-MIRROR, PLANT-ROUND, PLANT-FLOAT.
Output (mode 'x'): midrow/g4/mrc/out/cert/MR_JOINT_CERT_v1.kv. Usage: mrj_cert_v1.py cert"""
import hashlib
import json
import math
import os
import re
import sys
from fractions import Fraction as Fr
import flint

flint.ctx.prec = 256
arb, fmpq, arb_mat = flint.arb, flint.fmpq, flint.arb_mat
if len(sys.argv) != 2 or sys.argv[1] != 'cert':
    print('usage: mrj_cert_v1.py cert')
    sys.exit(2)
W = '/mnt/g2/release/root/code'
M3O, MYO, S9H = W + '/pk03/out', W + '/pk22/m3/out', W + '/pk25'
OUTD = W + '/pk22/midrow/g4/mrc/out/cert'
MAN3 = (S9H + '/mr/MANIFEST_C6A_CERT_v3.sha256', '6c8641197635798069221101e4bec2fbc07f9462fd390b6d21a9a8b43466eb50')
MAN4 = (S9H + '/mr/MANIFEST_MR_V4_CERT_v1.sha256', '9cf8e6d238d89eb2bb67964f1ed206a4b9b1e4fd1461b69c02d568d013817615')
REC = {4: {'S9': (M3O + '/m3_s9_N4_J300_v1_8_3.json', 'bcc6434c6a03eecb232f10504b63f1ce10a94a489d5a2ba9cf3fe09c8018b831'), 'DJ': (MYO + '/m3_c3j_DJ_N4_J300_c3j.json', '290d2142a532ab23b509e6da294b864941185612f74298afc84041d98f799db3'),
           'DH': (S9H + '/m3/out/m3_s9h_DH_N4_J300_v1.json', 'e02852c2159663318d3a20a5369f5c5585b029faed3a48f4c576d47317d889f8')},
       3: {'S9': (M3O + '/m3_s9_N3_J300_v1_8_3.json', 'd287d3dcbd4bd988aa8061fbe11b3da1609e0ab4d27ae1a619eadcee963e8fa5'), 'DJ': (MYO + '/m3_c3j_DJ_N3_J300_c3j.json', 'ac33223fee938157db58c64616e475a42aad7b0b626eb244fcc3b3526e012c22'),
           'DH': (S9H + '/m3/out/m3_s9h_DH_N3_J300_v1.json', '9248b1183f8ebb5c7f8dcba4a9293e5081bf35e96c43a659b69a19f2203a0f3b')}}
JF = {4: (W + '/pk22/midrow/g4/mrx/out/joint_float_v1_n4.out', '1a8a4890597b77336e7bd7b757e5096755808459baf0aa74157f2cef326e7e88'), 3: (W + '/pk22/midrow/g4/mrx/out/joint_float_v1_n3.out', 'bdefb6c5e03d9eeee783789aa11c8ab8f5991c8e7ca90da2641a5806be74f2f4')}
LEMF, SPEF, INSF = S9H + '/mr/v3/MR_LEMMAP.kv', S9H + '/mr/v4/MR_SPECTRAL.kv', S9H + '/mr/v4/MR_INSERT.kv'
INSOUT = S9H + '/asm/out/out_kt_s9h_ins_v2_2_cert_c1.out'
LEMMAP_FIELDS = ('jlo jhi rho0_hi rhox_hi rhoy_hi mu0_lo mux_lo muy_lo tau_hi L0_hi Lx_hi Ly_hi u0p_lo u0p_hi u01_lo u01_hi u03_lo u03_hi '
                 'uxp_lo uxp_hi ux1_lo ux1_hi ux3_lo ux3_hi uyp_lo uyp_hi uy1_lo uy1_hi uy3_lo uy3_hi q0_hi qx_hi qy_hi eps_x0_hi eps_y0_hi '
                 'eps_0x_hi eps_yx_hi eps_0y_hi eps_xy_hi').split()
SPECTRAL_FIELDS = 'jlo jhi sx_lo sx_hi sy_lo sy_hi tau_hi rho1_hi Rw_hi cxm1_lo cxm1_hi cym1_lo cym1_hi'.split()
INSERT_FIELDS = ('jlo jhi vx_lo vx_hi vy_lo vy_hi Pevw_hi Pev_hi vp_hi mxx_lo mxx_hi mxy_lo mxy_hi myy_lo myy_hi PeBwux_hi PeBwuy_hi win_hi C_hi '
                 'windowed xc_lo xc_hi xf_hi').split()
OUT_FIELDS = 'jlo jhi Cb_lo Cb_hi Cb_mid wJwx_hi wJwy_hi PewJw_hi jfw_hi A0_hi ch_lo ch_hi ct_lo ct_hi bh_hi bt_hi Wc_hi'
TOL = {4: {'Wc': Fr('3.627'), 'jfw': Fr('7.446'), 'cbar': Fr('0.0921')}, 3: {'Wc': Fr('3.916'), 'jfw': Fr('7.601'), 'cbar': Fr('0.0932')}}   # G6 v1_1 sect. 5
JFJ = {4: 350, 3: 300}
LV = ('0', 'x', 'y')
BV = ('p', '1', '3')
ST = (0, 1, 3)
FAILS, NOFIRE = [], []


def out(line):
    print(line, flush=True)


def gate(name, ok, line):
    out('%s %s -> %s' % (name, line, 'PASS' if ok else 'FAIL'))
    if not ok:
        FAILS.append(name)


def plant(name, fired, line):
    out('%s %s -> %s' % (name, line, 'FIRES' if fired else 'DOES NOT FIRE'))
    if not fired:
        NOFIRE.append(name)


def sha(p):
    with open(p, 'rb') as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def fr_of(x):
    m, e = x.man_exp()
    m, e = int(m), int(e)
    return Fr(m) * (Fr(2) ** e) if e >= 0 else Fr(m, 2 ** (-e))


def ab(q):
    q = Fr(q)
    return arb(fmpq(q.numerator, q.denominator))


def hull(lo, hi):
    return ab(lo).union(ab(hi))


def lo_of(x):
    return fr_of(x.lower())


def hi_of(x):
    return fr_of(x.upper())


def absup(x):
    return max(abs(lo_of(x)), abs(hi_of(x)))


def dec(q, up):
    """the 17-significant-digit decimal string nearest q in the given direction (up: >= q; down: <= q), from exact integers."""
    q = Fr(q)
    if q == 0:
        return '0'
    neg = q < 0
    m = -q if neg else q
    e = len(str(m.numerator)) - len(str(m.denominator))
    while Fr(10) ** e > m:
        e -= 1
    while Fr(10) ** (e + 1) <= m:
        e += 1
    scale = Fr(10) ** (16 - e)
    v = m * scale
    away = (up and not neg) or (neg and not up)
    n = (v.numerator + v.denominator - 1) // v.denominator if away else v.numerator // v.denominator
    if n >= 10 ** 17:
        n //= 10
        e += 1
        n = n + 1 if away and Fr(n) * Fr(10) ** (e - 16) < m else n
    s = str(n)
    txt = '%s%s.%se%s%02d' % ('-' if neg else '', s[0], s[1:], '-' if e < 0 else '+', abs(e))
    assert (Fr(txt) >= q) if up else (Fr(txt) <= q), (txt, q, up)
    return txt


def read_kv(path, keyrx):
    head, rows = {}, {}
    for ln in open(path):
        ln = ln.rstrip('\n')
        if not ln or ln.startswith('#'):
            continue
        k, sep, v = ln.partition(' = ')
        assert sep, ln[:80]
        if re.fullmatch(keyrx, k):
            assert k not in rows, k
            rows[k] = v.split()
        else:
            assert k not in head, k
            head[k] = v
    return head, rows


def manifest(p):
    acc = {}
    for ln in open(p):
        if ln.strip():
            h_, p_ = ln.rstrip('\n').split('  ', 1)
            acc[p_] = h_
    return acc


# ---- pins
SRCS = {'MAN3': MAN3, 'MAN4': MAN4, 'JF4': JF[4], 'JF3': JF[3]}
for n in (4, 3):
    for k, v in REC[n].items():
        SRCS['%s%d' % (k, n)] = v
shas = dict((k, sha(p)) for k, (p, h) in SRCS.items())
gate('C-SRC', all(shas[k] == h for k, (p, h) in SRCS.items()), '(%s)' % ', '.join('%s %s' % (os.path.basename(p), shas[k][:8]) for k, (p, h) in SRCS.items()))
m3, m4 = manifest(MAN3[0]), manifest(MAN4[0])
lem_sha, spe_sha, ins_sha, iout_sha = sha(LEMF), sha(SPEF), sha(INSF), sha(INSOUT)
gate('C-MANIFEST', m3.get('mr/v3/MR_LEMMAP.kv') == lem_sha and m4.get('mr/v4/MR_SPECTRAL.kv') == spe_sha and m4.get('mr/v4/MR_INSERT.kv') == ins_sha
     and m4.get('asm/out/out_kt_s9h_ins_v2_2_cert_c1.out') == iout_sha,
     '(mr/v3 MR_LEMMAP.kv %s by MANIFEST_C6A_CERT_v3; mr/v4 MR_SPECTRAL.kv %s, MR_INSERT.kv %s and the MR_INSERT cert run output %s by '
     'MANIFEST_MR_V4_CERT_v1)' % (lem_sha[:16], spe_sha[:16], ins_sha[:16], iout_sha[:16]))
LH, LR = read_kv(LEMF, r'N[34]_P[0-9]{4}')
SH, SR = read_kv(SPEF, r'N[34]_P[0-9]{4}')
IH, IR = read_kv(INSF, r'N[34]_P[0-9]{4}_[hta]')


def certified(h, fmt, rec):
    return (h.get('FORMAT') == fmt and h.get('RECORD') == rec and h.get('PRODUCER', '').split()[:1] == ['pk25'] and h.get('EXPORT_STATUS') == 'CERTIFIED'
            and h.get('RUN_VERDICT') == 'VALID' and h.get('ORIENTATION') == 'u_x along e1, u_y along e3')


okh = (certified(LH, 'MR_LEMMAP_KV_v2', 'MR_LEMMAP') and LH.get('FIELDS', '').split() == LEMMAP_FIELDS and certified(SH, 'MR_INPUT_KV_v4', 'MR_SPECTRAL')
       and SH.get('FIELDS', '').split() == SPECTRAL_FIELDS and certified(IH, 'MR_INPUT_KV_v4', 'MR_INSERT') and IH.get('FIELDS', '').split() == INSERT_FIELDS
       and SH.get('TRIAL_SET') == LH.get('TRIAL_SET') == IH.get('TRIAL_SET') and IH.get('LEMMAP_SHA256') == lem_sha)
gate('C-HEADERS', okh, '(MR_LEMMAP, MR_SPECTRAL and MR_INSERT: FORMAT, RECORD, PRODUCER pk25, EXPORT_STATUS CERTIFIED, RUN_VERDICT VALID, '
     'ORIENTATION, FIELDS; one TRIAL_SET; MR_INSERT\'s LEMMAP_SHA256 is MR_LEMMAP\'s)')
TRIAL_SET = LH.get('TRIAL_SET', '')
okk = (sorted(LR) == sorted(SR) and all(LR[k][:2] == SR[k][:2] for k in SR) and sorted(IR) == sorted(k + s for k in SR for s in ('_h', '_t', '_a'))
       and all(IR[k + '_h'][:2] == SR[k][:2] and IR[k + '_t'][:2] == SR[k][:2] for k in SR))
gate('C-KEYS', okk, '(%d keys, the same in MR_LEMMAP, MR_SPECTRAL and MR_INSERT (h, t), with the same jlo, jhi strings)' % len(SR))

# ---- the N-1 constants from pk25's certified MR_INSERT run (printed lines), tied to MR_INSERT's C_hi strings
otxt = open(INSOUT).read()
MU = {}
pr_bad = []
FL = r'([0-9]\.[0-9]{16}e[+-][0-9]{2})'
for n in (4, 3):
    mt = re.findall(r'^MU-T N=%d: c_t over the pieces in \[%s, %s\] \(exact ends\); OR_t <= %s at t <= %s \([0-9]+ boxes\); C_t = OR_t kappa_max\^1/2 <= %s$' % (
        n, FL, FL, FL, FL, FL), otxt, re.M)
    mh = re.findall(r'^MU N=%d: c~_h over the pieces in \[%s, %s\]; the interval \[%s, %s\]; OR <= %s at t <= %s \([0-9]+ boxes\); C = OR kappa_max\^1/2 <= %s$' % (
        n, FL, FL, FL, FL, FL, FL, FL), otxt, re.M)
    if len(mt) != 1 or len(mh) != 1:
        pr_bad.append('N%d: %d MU-T and %d MU lines' % (n, len(mt), len(mh)))
        continue
    ct_lo, ct_hi, ort, tmt, ctc = mt[0]
    _a, _b, ci_lo, ci_hi, orh, tmh, chc = mh[0]
    MU[n] = {'ct_range': (Fr(ct_lo), Fr(ct_hi)), 'ci': (Fr(ci_lo), Fr(ci_hi)), 'ORt': Fr(ort), 'ORh': Fr(orh), 'Ct': Fr(ctc), 'Ch': Fr(chc),
             'Ct_s': ctc, 'Ch_s': chc}
    keys_n = [k for k in SR if k.startswith('N%d_' % n)]
    cih = set(IR[k + '_h'][INSERT_FIELDS.index('C_hi')] for k in keys_n)
    cit = set(IR[k + '_t'][INSERT_FIELDS.index('C_hi')] for k in keys_n)
    if cih != {chc} or cit != {ctc}:
        pr_bad.append('N%d: MR_INSERT C_hi h %s t %s against the printed C %s, C_t %s' % (n, sorted(cih)[:2], sorted(cit)[:2], chc, ctc))


def mu_print_ok(mu_d, strs):
    return all(mu_d[n]['Ch_s'] == strs[n][0] and mu_d[n]['Ct_s'] == strs[n][1] for n in (4, 3))


STRS = dict((n, (IR[[k for k in SR if k.startswith('N%d_' % n)][0] + '_h'][INSERT_FIELDS.index('C_hi')],
                 IR[[k for k in SR if k.startswith('N%d_' % n)][0] + '_t'][INSERT_FIELDS.index('C_hi')])) for n in (4, 3))
gate('C-MU-PRINT', not pr_bad and len(MU) == 2 and mu_print_ok(MU, STRS), '(pk25\'s MR_INSERT cert run prints, per N, c_t\'s range, OR_t and C_t, and '
     'c_h\'s mu interval, OR and C; the printed C and C_t are exactly MR_INSERT\'s h and t C_hi on every piece: %s)%s' % (
         '; '.join('N%d OR_t %.6e OR_h %.6e C_t %s C_h %s' % (n, float(MU[n]['ORt']), float(MU[n]['ORh']), MU[n]['Ct_s'], MU[n]['Ch_s']) for n in MU),
         (': ' + '; '.join(pr_bad)) if pr_bad else ''))
if len(MU) == 2:
    MUP = dict((n, dict(MU[n], Ch_s=dec(MU[n]['Ch'] * 2, True))) for n in MU)
    plant('PLANT-MU-PRINT', not mu_print_ok(MUP, STRS), '(a printed C doubled must fail the tie to MR_INSERT\'s C_hi)')
if FAILS:
    out('VERDICT INVALID (fails %s); no record written' % FAILS)
    sys.exit(3)


# ---- the records
def item_of(rj, key, n):
    rec, it, hops = rj, rj['items'][key], 0
    while it.get('alias_of'):
        fn, k2, h = it['alias_of'].split()
        p = os.path.join(M3O, os.path.basename(fn))
        assert sha(p) == h, p
        rec = json.load(open(p))
        it, hops = rec['items'][k2], hops + 1
        assert hops <= 4
    assert it['kind'] == 'entry' and it['parity'] == 'free', key
    assert rec.get('J_REF') == 300 and rec.get('N') == n and rec.get('claim', '').startswith(
        'for every J >= J_REF, t = 1/J, t = 0 included: |I(J)/main(J) - sum_k ak[k] t^k| <= err'), key
    return it


class Ent:
    def __init__(self, rj, key, n, tag):
        it = item_of(rj, key, n)
        self.name = '%s:%s' % (tag, key)
        self.ak = [arb(float(c)) for c in it['ak']]
        self.err = Fr(float(it['err']))

    def ball(self, T):
        v = arb(0)
        for c in reversed(self.ak):
            v = v * T + c
        return v + arb(0, ab(self.err).upper())


def lem(key, f):
    return Fr(LR[key][LEMMAP_FIELDS.index(f)])


def spe(key, f):
    return Fr(SR[key][SPECTRAL_FIELDS.index(f)])


def piece_t(key):
    jlo, jhi = LR[key][0], LR[key][1]
    tlo = Fr(0) if jhi == 'inf' else 1 / Fr(jhi)
    return tlo, 1 / Fr(jlo), hull(tlo, 1 / Fr(jlo))


ROWS, CHK = {}, {'hull': [], 'ctr': [], 'fin': [], 'mirror': []}
REF = {}
for n in (4, 3):
    RJ = dict((k, json.load(open(p))) for k, (p, h) in REC[n].items())
    G9 = dict(((a, b), Ent(RJ['S9'], 'G,%d,%d' % (min(a, b), max(a, b)), n, 'S9')) for a in ST for b in ST)
    E = {}
    for fam, rk in (('JTH', 'DJ'), ('DHT', 'DJ'), ('Gxh', 'DH')):
        E[fam] = dict(((a, b), Ent(RJ[rk], '%s,%d,%d' % (fam, min(a, b), max(a, b)), n, rk)) for a in ST for b in ST)
    SHE = [Ent(RJ['DH'], 'Sh,%d' % b, n, 'DH') for b in ST]
    MIR = (Ent(RJ['DJ'], 'JTHr,1,0', n, 'DJ'), Ent(RJ['DJ'], 'JTH,0,1', n, 'DJ'), Ent(RJ['DJ'], 'JTH,0,3', n, 'DJ'))
    mu = MU[n]
    ORt, ORh, Ct, Ch = ab(mu['ORt']), ab(mu['ORh']), ab(mu['Ct']), ab(mu['Ch'])
    TRP = (ORt * ORh).upper()
    WC = hi_of((ORt * Ch).upper())
    keysN = sorted(k for k in SR if k.startswith('N%d_' % n))
    for key in keysN:
        tlo, thi, T = piece_t(key)
        G = [[G9[(a, b)].ball(T) for b in ST] for a in ST]
        nrm = [G[i][i].sqrt() for i in range(3)]
        U = dict((k, [hull(lem(key, 'u%s%s_lo' % (k, b)), lem(key, 'u%s%s_hi' % (k, b))) for b in BV]) for k in LV)
        V = dict((k, [U[k][i] / nrm[i] for i in range(3)]) for k in LV)
        q = dict((k, ab(lem(key, 'q%s_hi' % k))) for k in LV)
        eps = dict(((j, k), ab(lem(key, 'eps_%s%s_hi' % (j, k)))) for j in LV for k in LV if j != k)
        dl = dict((k, (2 * (q[k] ** 2 + sum((eps[(j, k)] ** 2 for j in LV if j != k), arb(0)))).sqrt().upper()) for k in LV)
        shb = [e.ball(T) for e in SHE]
        if not all(x > 0 for x in shb):
            CHK['fin'].append((key, 'Sh not positive'))
            continue
        kap = dict((k, sum((ab(absup(V[k][i])) * shb[i].sqrt().upper() for i in range(3)), arb(0)).upper()) for k in LV)
        X = dict((fam, [[E[fam][(a, b)].ball(T) for b in ST] for a in ST]) for fam in E)

        def quad(fam, k1, k2):
            return sum((V[k1][i] * V[k2][j] * X[fam][i][j] for i in range(3) for j in range(3)), arb(0))
        ct0, ch0, At = quad('DHT', '0', '0'), quad('Gxh', '0', '0'), quad('JTH', '0', '0')
        dt = (dl['0'] * (Ct + ORt * kap['0'])).upper()
        dh = (dl['0'] * (Ch + ORh * kap['0'])).upper()
        ct = ct0 + arb(0, dt)
        ch = ch0 + arb(0, dh)
        if not (mu['ci'][0] < lo_of(ch) and hi_of(ch) < mu['ci'][1]):
            CHK['hull'].append(key)
        if hi_of(ct) < mu['ct_range'][0] or lo_of(ct) > mu['ct_range'][1]:
            CHK['ctr'].append(key)
        ecb = (dt * dh + dl['0'] * (ab(WC) + TRP * kap['0'])).upper()
        cb = At - ct0 * ch0 + arb(0, ecb)
        sxl, sxh, syl, syh = ab(spe(key, 'sx_lo')), ab(spe(key, 'sx_hi')), ab(spe(key, 'sy_lo')), ab(spe(key, 'sy_hi'))
        slo, shi = {'x': sxl, 'y': syl}, {'x': sxh, 'y': syh}
        wJ, wJw = {}, {}
        for a in ('x', 'y'):
            wt = quad('JTH', a, '0') - ch * quad('DHT', a, '0') - ct * quad('Gxh', a, '0')
            e1 = (dl[a] * ab(WC) + TRP * kap[a] * dl['0']).upper()
            e2 = (dl['0'] * ab(WC) / slo[a].sqrt() + TRP * kap['0'] * dl[a]).upper()
            ea = e1 if hi_of(e1) <= hi_of(e2) else e2
            wJ[a] = wt + arb(0, ea)
            wJw[a] = hi_of((shi[a] * ab(absup(wJ[a]))).upper())
        tau = ab(spe(key, 'tau_hi'))
        pew = hi_of((tau * ab(WC)).upper())
        sx32 = (sxh * sxh.sqrt()).upper()
        jfw = hi_of((ab(WC) * sx32 + ab(absup(ct)) * ab(absup(ch)) * sxh * sxh).upper())
        a0 = hi_of((ab(absup(cb)) + ab(absup(ct)) * ab(absup(ch))).upper())
        bh, bt = hi_of((Ch * sx32).upper()), hi_of((Ct * sx32).upper())
        vals = [cb, ct, ch, wJ['x'], wJ['y']]
        if not all(x.is_finite() for x in vals):
            CHK['fin'].append((key, 'not finite'))
            continue
        mr = [m.ball(T) for m in MIR]
        if not mr[0].overlaps(mr[1]):
            CHK['mirror'].append(key)
        ROWS[key] = {'cb': cb, 'ct': ct, 'ch': ch, 'wJ': wJ, 'wJw': wJw, 'pew': pew, 'jfw': jfw, 'a0': a0, 'bh': bh, 'bt': bt, 'wc': WC,
                     'kap': kap, 'dl': dl, 'dt': dt, 'dh': dh, 'At': At, 'mirror_neg': mr[0].overlaps(mr[2])}
    # the float control on the piece that holds joint_float_v1's J
    jf = open(JF[n][0]).read()
    m = re.search(r'^JOINT-FLOAT N=%d J=%d: c_t ([0-9.]+) c_h ([0-9.]+) <u, Xi u> ([0-9.]+); C_bulk ([-+0-9.e]+); w_J x ([-+0-9.e]+) y ([-+0-9.e]+)$' % (
        n, JFJ[n]), jf, re.M)
    jkey = [k for k in keysN if Fr(LR[k][0]) <= JFJ[n] and (LR[k][1] == 'inf' or JFJ[n] <= Fr(LR[k][1]))][0]
    REF[n] = (jkey, m.groups() if m else None)

gate('C-SH-POS', not [x for x in CHK['fin'] if x[1] == 'Sh not positive'], '(the Sh,b entries certainly positive on every piece)')
gate('C-CH-HULL', not CHK['hull'], '(c_h\'s interval inside the mu tool\'s on every piece, so OR_h and C_h hold for the true c_h; failures %d, first %s)' % (
    len(CHK['hull']), CHK['hull'][:3]))
gate('C-CT-RANGE', not CHK['ctr'], '(c_t\'s interval from the DHT entries meets the range of R4\'s means export on which OR_t and C_t were formed; failures %d, '
     'first %s)' % (len(CHK['ctr']), CHK['ctr'][:3]))
gate('C-MIRROR', not CHK['mirror'], '(the control JTHr,1,0 overlaps JTH,0,1 on every piece; failures %d)' % len(CHK['mirror']))
nm_neg = sum(1 for r in ROWS.values() if r['mirror_neg'])
plant('PLANT-MIRROR', nm_neg < len(ROWS), '(JTHr,1,0 offered JTH,0,3 must miss on some piece: overlaps on %d of %d)' % (nm_neg, len(ROWS)))
gate('C-FINITE', not CHK['fin'] and len(ROWS) == len(SR), '(every row finite; %d of %d pieces; failures %s)' % (len(ROWS), len(SR), CHK['fin'][:3]))
k0 = sorted(ROWS)[0]
r0 = ROWS[k0]
shifted = r0['ch'] + ab(Fr(2, 100))
plant('PLANT-CH-HULL', not (MU[int(k0[1])]['ci'][0] < lo_of(shifted) and hi_of(shifted) < MU[int(k0[1])]['ci'][1]),
      '(%s: c_h shifted by 0.02 must leave the mu tool\'s interval)' % k0)


# ---- the rows, as written
def row_line(key, r):
    f = [LR[key][0], LR[key][1], dec(lo_of(r['cb']), False), dec(hi_of(r['cb']), True), repr(float(r['cb'].mid())), dec(r['wJw']['x'], True),
         dec(r['wJw']['y'], True), dec(r['pew'], True), dec(r['jfw'], True), dec(r['a0'], True), dec(lo_of(r['ch']), False), dec(hi_of(r['ch']), True),
         dec(lo_of(r['ct']), False), dec(hi_of(r['ct']), True), dec(r['bh'], True), dec(r['bt'], True), dec(r['wc'], True)]
    return '%s = %s' % (key, ' '.join(f))


LINES = [row_line(k, ROWS[k]) for k in sorted(ROWS, key=lambda k: (-int(k[1]), k))]
bad_round = 0
for ln in LINES:
    k, f = ln.split(' = ')[0], ln.split(' = ')[1].split()
    r = ROWS[k]
    ok_r = (Fr(f[2]) <= lo_of(r['cb']) and Fr(f[3]) >= hi_of(r['cb']) and Fr(f[5]) >= r['wJw']['x'] and Fr(f[6]) >= r['wJw']['y'] and Fr(f[7]) >= r['pew']
            and Fr(f[8]) >= r['jfw'] and Fr(f[9]) >= r['a0'] and Fr(f[10]) <= lo_of(r['ch']) and Fr(f[11]) >= hi_of(r['ch'])
            and Fr(f[12]) <= lo_of(r['ct']) and Fr(f[13]) >= hi_of(r['ct']) and Fr(f[14]) >= r['bh'] and Fr(f[15]) >= r['bt'] and Fr(f[16]) >= r['wc']
            and all(Fr(f[i]) >= 0 for i in (5, 6, 7, 8, 9, 14, 15, 16)) and Fr(f[2]) <= Fr(f[3]) and Fr(f[10]) <= Fr(f[11]) and Fr(f[12]) <= Fr(f[13]))
    bad_round += 0 if ok_r else 1
gate('C-ROUND', bad_round == 0, '(every written lo <= the exact lower end, every hi >= the upper end, single upper bounds >= 0; failures %d)' % bad_round)
q_lo = lo_of(r0['cb'])
wrong = Fr(dec(q_lo, False)) + abs(q_lo) * Fr(1, 10 ** 15)
plant('PLANT-ROUND', not (wrong <= q_lo), '(Cb_lo of %s written one part in 1e15 above its rounded-down value)' % k0)

# ---- the float control and the tolerances
fl_ok, fl_lines, fl_plant = True, [], True
for n in (4, 3):
    jkey, g = REF[n]
    if g is None or jkey not in ROWS:
        fl_ok = False
        fl_lines.append('N%d: no JOINT-FLOAT line or no row' % n)
        continue
    r = ROWS[jkey]
    ctf, chf, a0f, cbf, wxf, wyf = (float(x) for x in g)
    inside = lambda x, b: float(lo_of(b)) <= x <= float(hi_of(b))
    oks = [inside(ctf, r['ct']), inside(chf, r['ch']), inside(cbf, r['cb']), inside(wxf, r['wJ']['x']), inside(wyf, r['wJ']['y'])]
    fl_ok = fl_ok and all(oks)
    hw = float(r['cb'].rad())
    fl_plant = fl_plant and not inside(cbf + 10 * hw, r['cb'])
    fl_lines.append('N%d %s: c_t %.9f in [%.9f, %.9f] %s; c_h %.9f in [%.9f, %.9f] %s; C_bulk %.9e in [%.9e, %.9e] %s; w_J,x %.4e in [%.4e, %.4e] %s; '
                    'w_J,y %.5f in [%.5f, %.5f] %s' % (n, jkey, ctf, float(lo_of(r['ct'])), float(hi_of(r['ct'])), oks[0], chf, float(lo_of(r['ch'])),
                                                       float(hi_of(r['ch'])), oks[1], cbf, float(lo_of(r['cb'])), float(hi_of(r['cb'])), oks[2], wxf,
                                                       float(lo_of(r['wJ']['x'])), float(hi_of(r['wJ']['x'])), oks[3], wyf, float(lo_of(r['wJ']['y'])),
                                                       float(hi_of(r['wJ']['y'])), oks[4]))
gate('C-FLOAT', fl_ok, '(joint_float_v1\'s Ritz-level values at J = 350 (N4) and 300 (N3) inside the certified intervals: %s)' % '; '.join(fl_lines))
plant('PLANT-FLOAT', fl_plant, '(C_bulk\'s float moved by ten half-widths must leave the interval)')
tol_bad, tol_lines = [], []
for n in (4, 3):
    ks = [k for k in ROWS if k.startswith('N%d_' % n)]
    wc = max(ROWS[k]['wc'] for k in ks)
    jf_ = max(ROWS[k]['jfw'] for k in ks)
    cbar = max(Fr(float(ROWS[k]['cb'].rad())) / abs(Fr(float(ROWS[k]['cb'].mid()))) for k in ks)
    cbmin = min(lo_of(ROWS[k]['cb']) for k in ks)
    ok_ = wc <= TOL[n]['Wc'] and jf_ <= TOL[n]['jfw'] and cbar <= TOL[n]['cbar'] and cbmin > 0
    if not ok_:
        tol_bad.append(n)
    tol_lines.append('N%d: Wc %.4f (tol %s), jfw max %.4e (tol %s), C_bulk relative half-width max %.3e (tol %s), C_bulk lo min %.6e' % (
        n, float(wc), TOL[n]['Wc'], float(jf_), TOL[n]['jfw'], float(cbar), TOL[n]['cbar'], float(cbmin)))
gate('C-TOL', not tol_bad, '(G6 v1_1 sect. 5\'s crude tolerances, each alone, for H_J >= 10, and C_bulk certainly positive: %s)' % '; '.join(tol_lines))

# ---- summaries
for n in (4, 3):
    jkey = REF[n][0]
    r = ROWS.get(jkey)
    if r is None:
        continue
    out('JLOW N=%d %s: Cb [%.9e, %.9e] (A~ %.9f, ct0 ch0 %.9f, error %.3e); c_t [%.9f, %.9f] (dt %.2e); c_h [%.9f, %.9f] (dh %.2e); w_J,x [%+.4e, %+.4e], '
        'w_J,y [%+.5f, %+.5f]; wJw x %.3e y %.3e; Wc %.4f; jfw %.4e; A0 %.4f; bh %.4e bt %.4e; PewJw %.4e; kappa %s; delta %s' % (
            n, jkey, float(lo_of(r['cb'])), float(hi_of(r['cb'])), float(r['At'].mid()), float(r['At'].mid()) - float(r['cb'].mid()),
            float(r['cb'].rad()), float(lo_of(r['ct'])), float(hi_of(r['ct'])), float(r['dt']), float(lo_of(r['ch'])), float(hi_of(r['ch'])),
            float(r['dh']), float(lo_of(r['wJ']['x'])), float(hi_of(r['wJ']['x'])), float(lo_of(r['wJ']['y'])), float(hi_of(r['wJ']['y'])),
            float(r['wJw']['x']), float(r['wJw']['y']), float(r['wc']), float(r['jfw']), float(r['a0']), float(r['bh']), float(r['bt']), float(r['pew']),
            ' '.join('%.3e' % float(r['kap'][k]) for k in LV), ' '.join('%.3e' % float(r['dl'][k]) for k in LV)))
    ks = [k for k in ROWS if k.startswith('N%d_' % n)]
    last = sorted(ks)[-1]
    rl = ROWS[last]
    out('LAST N=%d %s: Cb [%.9e, %.9e]; w_J,x [%+.4e, %+.4e], w_J,y [%+.5f, %+.5f]' % (n, last, float(lo_of(rl['cb'])), float(hi_of(rl['cb'])),
                                                                                    float(lo_of(rl['wJ']['x'])), float(hi_of(rl['wJ']['x'])),
                                                                                    float(lo_of(rl['wJ']['y'])), float(hi_of(rl['wJ']['y']))))

# ---- the record
if FAILS or NOFIRE:
    out('VERDICT INVALID (fails %s, plants not firing %s); no record written' % (FAILS, NOFIRE))
    sys.exit(3)
os.makedirs(OUTD, exist_ok=True)
code_sha = sha(os.path.abspath(__file__))
path = os.path.join(OUTD, 'MR_JOINT_CERT_v1.kv')
assert os.path.dirname(path) == OUTD
head = ['# MR_JOINT: CERTIFIED record of pk22 (mrj_cert_v1, both N) for engine v1_8_4\'s Proposition J (G6 v1_1 sect. 5, G6 v1_6_2 sect. 6); '
        'entries by their uniform claims',
        'FORMAT = MR_INPUT_KV_v4', 'RECORD = MR_JOINT', 'PRODUCER = pk22 mrj_cert_v1 CERT',
        'CODE = pk22/midrow/g4/mrc/src/mrj_cert_v1.py:%s' % code_sha[:8], 'STATUS = CERTIFIED', 'EXPORT_STATUS = CERTIFIED', 'RUN_VERDICT = VALID',
        'SOURCE = %s' % ' '.join('%s:%s' % (os.path.basename(p), shas[k][:8]) for k, (p, h) in SRCS.items()) + ' MR_LEMMAP.kv:%s MR_SPECTRAL.kv:%s '
        'MR_INSERT.kv:%s out_kt_s9h_ins_v2_2_cert_c1.out:%s' % (lem_sha[:8], spe_sha[:8], ins_sha[:8], iout_sha[:8]),
        'J_UNIFORMITY = PER-PIECE: every row holds for every J in [jlo, jhi] of its piece; the last piece runs to J = inf (t = 0)',
        'ORIENTATION = u_x along e1, u_y along e3', 'TRIAL_SET = %s' % TRIAL_SET, 'LEMMAP_SHA256 = %s' % lem_sha,
        'WC_FORM = Wc = OR_t C_h >= OR_t OR_h kappa_max^1/2 >= C_J >= |w_J| (pk25 note v2_5 sect. 10); PewJw = tau Wc; jfw = Wc s_x^3/2 + |c_t| |c_h| '
        's_x^2; bh = C_h s_x^3/2, bt = C_t s_x^3/2',
        'CB_FORM = C_bulk in A~ - ct0 ch0 +- (dt dh + delta_0 (Wc + OR_t OR_h kappa_0)); c_t, c_h by the trial-state route of pk25\'s MR_INSERT producer; '
        'w_J,a by the trial-state route with min(delta_a Wc + OR_t OR_h kappa_a delta_0, delta_0 Wc s_a^-1/2 + OR_t OR_h kappa_0 delta_a)',
        'FIELDS = %s' % OUT_FIELDS]
with open(path, 'x') as fh:
    fh.write('\n'.join(head + LINES) + '\n')
out('RECORD %s sha256 %s rows %d' % (path, sha(path), len(LINES)))
out('VERDICT VALID')
