#!/usr/bin/env python3
"""m4h_reader_v1_1.py -- pk25 (code/pk25/m4h/). REVISION of m4h_reader_v1.py (sha256 868f6c0ab49a046ccf12004c5b0d8265c8ae5c59dfb5c7ec950c8607144d5817) with m4h_asm_v1_1 (C5's
first cert run: every gate passed, PLANT-SWAP did not fire; the asm's plant now exchanges M0): only the names move to v1_1, the
PIN_CODE names (READER_REL, ASM_REL), the binding's first-line producer m4h_asm_v1_1 and the script-mode header and usage.
m4h_reader_v1's docstring follows.
m4h_reader_v1.py -- pk25 (code/pk25/m4h/). A FORK of pk15/m4_reader_v1.py (sha256 5cef440ae313eddd2e6bcf49aac835f2595e61b6a3e59b23fca0c15671ec6bcd) for the h-row kinds h,
h1, h3 (A_h, R^xi_e1, R^xi_e3; C5 of G5_PLAN_v1 sect. 3, ADD1_1 sect. 8), the one sha-pinned reader of the record M4H_KV_v1 that
m4h_asm_v1 writes; made by pk25/m4h/make_m4h_v1.py with exact replacements of asserted counts (diff_m4_reader_v1_to_m4h_reader_v1.txt).
What changes, and nothing else:
  (1) KINDS h, h1, h3 (KK H, H1, H3; BASES (psi, e1, e3) for each, kt_cert's GK default); FORMAT and RECORD M4H_KV_v1, AUTHOR pk25,
      LAW m4h_v1, the CLAIM below; PIN_CODE names pk25/m4h/m4h_asm_v1.py and this file; the binding reads m4h_asm_v1's first line.
  (2) The law of the hook kind t for all three kinds (kt_cert's HOOK: hf = 2J; far_wpow as t; no EPSR300, D_k = sqrt(Z_min), since
      kt_cert's engine_value takes A_h and R^xi_b as the bound over Z_b^{1/2}, without lambda~_0).
  (3) C-MONO-GB: supF of h1, h3 is 2J supb (kt_cert's supF_a), of top degree 3 in J; J^d e^(-rho_G J) is nonincreasing for
      J >= d/rho_G, so the check allows top degree 3 and requires rho_G certainly above 3/300 (rho_G is 0.1113 [D]).
  (4) The script-mode plants aimed at N4 h and N4 h1 (PLANT-SWAP, PLANT-MONO) and the M4H FORMAT strings.
m4_reader_v1's docstring follows.
m4_reader_v1.py -- pk15 (code/pk15/). The one sha-pinned reader of the M4 law record M4_KV_v1 (SPEC_M4_LAW_v1_3 ff0e5e98 sect. 4
and 6), written by m4_asm_v1. m2b_reader_v1's interface pattern:
  load(path, asm_out, expected_sha256=None, reader_sha256=None) -> rec   the certified entry: the binding to m4_asm_v1's run output,
                                                                        check(), then C-PINS
  loads(record_text, record_name, asm_out_text, expected_sha256=None)    the same on texts, without C-PINS (for plants)
  check(record_text) -> rec                                              the record alone
  parse_record(record_text) -> rec                                       check() without C-MONO and C-FMT (m4_asm_v1 computes L300 on it)
  law(rec, kind, N, J) -> a decimal string at or above the upper end of L_k(J), kind in t, am, e1, e3, N in 3, 4, J >= 300 (an int, a
                          Fraction or a decimal string); anything else is refused
  law_balls(rec, kind, N, J) -> {term: arb ball}: L_k(J) and its parts (SPEC sect. 2)
Every refusal raises ValueError.
The law (SPEC sect. 2; s = 300/J, t = 1/J; arb at ctx.prec 256, each record decimal a ball containing it, used at its safe end):
  near_k = nP + nD + nR0 + tailX + tailB + ann (t, e1, e3), near_am = nP + nR, with nP = sum_{k=0..3} s^k M_k; nD = the smaller (by upper
  end) of s^4 nD and sum_{k=0..K} s^(4+k) nD_k, both valid (the review 253a52c3 l.40-43); nR0 = s^4 nR0; nR = s^4 nR;
  tailX = e^(-lam a_e (J-300)/2) TXm; tailB = e^(-lam kappa_B (J-300)/2) TBm; ann = e^(-lam a_e (J-300)/2) ann, with lam = 0.45 (kt_cert's
  LAM_T, binary64), a_e = binary64(0.6^2) (kt_cert_v1_8 l.818) and kappa_B = 2 (1 - cos 40 deg) - a^2/(4 (1 - a)), a = max(a_m, a_e)
  (kt_cert_v1_8 l.1719-1724), both recomputed here and named in the record by exact strings (A_E, KAPPA_B); the law takes a_e as the
  binary64 arb(A_E_F), never the decimal arb('0.36') (1.3e-17 higher), and C-A-E checks float(A_E) == 0.6 ** 2;
  far_k = sum over the kind's far items of weight(J) X300 (J/300)^p e^(-c (J-300)), weight hf^2 (oSS), 2 hf mbar_g (oS_g) or w_gh mbar_g
  mbar_h (oD_g_h; w_gh = 1 if g = h, else 2), hf = 2J for t and 1 for am, e1, e3, mbar_g = sum_{j=0..3} |m_gj| t^j;
  gB_k = supF_k(J) e^(-rho_G J) (sum_r ratio_main_r zR_r^up(J))^(1/2) (t, e1, e3), supF_k = sum_d coef_d J^d, zR_r^up = HI_0 +
  sum_{k=1..3} max(HI_k, 0) J^-k + err_b, rho_G = 0.95 (1 - cos 40 deg)/2 with 0.95 taken as binary64 0.95, the smaller of its two
  readings (kt_cert's gB_base uses the float th = 0.95, m2b_asm_v1 l.430 the decimal; a smaller rate only raises gB);
  D_k = sqrt(Z_min) (t, am), (1 - eps_r(300)) sqrt(Z_min) (e1, e3); L_k = (sqrt(near_k^2 + far_k) + gB_k)/D_k; L_am = sqrt(near_am^2 + far_am)/D_am.
check(): exactly the allowed keys, each once (the ND_K<k> keys contiguous from 0); FORMAT, RECORD, AUTHOR, LAW, J_REF, LAMBDA_CH, A_E,
KAPPA_B, RHO_G and VERDICT by exact equality, CLAIM equal to the text below; ASM_SHA256 a full sha256; WRITTEN_UTC a UTC stamp; PIN tokens
path:sha256 under code/; every number a finite nonnegative decimal, the m_gj exact binary64 reprs; the far items and the m_gj exactly the
kind's set (SPEC sect. 2.2); C-MONO (SPEC sect. 3) recomputed exactly: the Chernoff rates certainly > 0, (w + p)/c <= 300 per far item with
w the weight's J-power (2 for oSS at t, 1 for oS_g at t, else 0), every supF coefficient >= 0 with top degree <= 2 and rho_G certainly
above 2/300 (C-MONO-GB), Z_min > 0, eps_r(300) < 1; C-FMT: L_k(300) recomputed from the record lies at or below N<N>_<K>_L300 and within
1e-9 of it.
The binding (loads): the asm output's VERDICT lines equal exactly ['VERDICT VALID']; its first line is 'm4_asm_v1 sha256 <S> ...' with S
the record's ASM_SHA256; it holds exactly one line 'RECORD <record base name> <record sha256>' (equal to expected_sha256 when given).
C-PINS (load): every PIN token names an existing file with that sha256; PIN_CODE holds pk15/m4_asm_v1.py at ASM_SHA256 and
pk15/m4_reader_v1.py at this reader's own sha256 (the sha256 of __file__, or reader_sha256 when the reader is exec()ed).
Script mode (argv: record, asm output[, expected sha256]): load, L_k(300), L_k(600) and L_k(300)/Q300 - 1 (INFO) per N and kind, and the
plants, each refused by the named check: PLANT-SWAP (N4 t's and N4 e1's M1 exchanged: C-FMT), PLANT-MOCK (FORMAT 'M4_KV_v1 MOCK' and a
'MOCK ' claim prefix), PLANT-PRECERT (FORMAT 'M4_KV_v1_PRECERT'), PLANT-VERDICT ('VERDICT = VALID-PRECERT'), PLANT-BIND (the asm output's
RECORD sha256 changed), PLANT-MONO (N4 t's oSS rate just below its C-MONO-FAR4 threshold). VERDICT VALID only if load passes and every
plant is refused by its check.
Run (own folder): D=/mnt/g2/release/root/code/pk15; OMP_NUM_THREADS=1 timeout 580 nice -n 10 prlimit --as=8589934592 --
  python3 -I -B $D/m4_reader_v1.py <record> <asm output> > <out> 2> <err>
"""
import sys, os, re, hashlib
from fractions import Fraction
from flint import arb, ctx

ctx.prec = 256
W18 = '/mnt/g2/release/root/code'
READER_REL, ASM_REL = 'pk25/m4h/m4h_reader_v1_1.py', 'pk25/m4h/m4h_asm_v1_1.py'   # m4h_reader_v1: the PIN_CODE names (paths under code/)
CLAIM = ('for N in {3, 4}, k in {h, h1, h3} and every J >= 300 (t = 1/J in (0, 1/300], t -> 0 included), the amplitude Q_k(J) that '
         'kt_cert bounds (A_h: the engine bound over sqrt(Z_psi); R^xi_e1, R^xi_e3: the engine bound over sqrt(Z_e1), sqrt(Z_e3), the hook '
         'kinds having no lambda~_0), with kt_cert\'s decomposition constants (Lambda, the radii, lambda = 0.45, the 40 deg cones), which do not '
         'depend on J, satisfies Q_k(J) <= L_k(J), and L_k is nonincreasing in J (SPEC_M4_LAW_v1_1 sect. 2, the h-row kinds as the hook kind t: '
         'hf = 2J, D_k = sqrt(Z_min), supF of top degree at most 3).')
RHO_M, RHO_E = 0.55, 0.6                       # kt_cert_v1_8 l.341 (exact binary64)
A_M_F, A_E_F = RHO_M ** 2, RHO_E ** 2           # kt_cert_v1_8 l.818: a_m, a_e in binary64, as kt_cert sets them
LAM_CH = arb(0.45)                              # kt_cert_v1_8 l.1621 LAM_T (exact binary64)
COS40 = (arb.pi() * 40 / 180).cos()             # kt_cert_v1_8 l.342 DELTA
RHO_G = arb(0.95) * (1 - COS40) / 2             # 0.95 as binary64: below the decimal, so the smaller rate
KINDS = ('h', 'h1', 'h3')                       # m4h_reader_v1: A_h, R^xi_e1, R^xi_e3
KK = {'h': 'H', 'h1': 'H1', 'h3': 'H3'}
BASES = {'h': ('psi', 'e1', 'e3'), 'h1': ('psi', 'e1', 'e3'), 'h3': ('psi', 'e1', 'e3')}   # m4h_reader_v1: kt_cert's GK default
FIXED = {'FORMAT': 'M4H_KV_v1', 'RECORD': 'M4H_KV_v1', 'AUTHOR': 'pk25', 'LAW': 'm4h_v1', 'J_REF': '300', 'LAMBDA_CH': '0.45',
         'A_E': repr(A_E_F), 'KAPPA_B': '2 (1 - cos 40 deg) - a^2/(4 (1 - a)), a = max(binary64(0.55^2), A_E)',
         'RHO_G': '0.95 (1 - cos 40 deg)/2', 'VERDICT': 'VALID'}
KEYS_CONST = ('FORMAT', 'RECORD', 'AUTHOR', 'WRITTEN_UTC', 'CLAIM', 'LAW', 'J_REF', 'ASM_SHA256', 'LAMBDA_CH', 'A_E', 'KAPPA_B', 'RHO_G',
              'VERDICT')
KEYS_PIN = ('PIN_KTCERT', 'PIN_X', 'PIN_M2B', 'PIN_M3_S9', 'PIN_M3_VAC', 'PIN_TRIAL', 'PIN_FAR', 'PIN_CODE')
DEC = re.compile(r'[0-9]+(\.[0-9]+)?(e[-+]?[0-9]+)?')
REPR = re.compile(r'-?([0-9]+(\.[0-9]*)?|\.[0-9]+)(e[-+]?[0-9]+)?')
HEX64 = re.compile(r'[0-9a-f]{64}')
INT = re.compile(r'0|[1-9][0-9]*')


def far_names(kind):
    """the kind's far items in kt_cert's FLOAT-IN order (SPEC sect. 2.2; logR left out, R = 1)."""
    g = BASES[kind]
    return ['oSS'] + ['oS_%s' % a for a in g] + ['oD_%s_%s' % (g[i], g[j]) for i in range(len(g)) for j in range(i, len(g))]


def far_wpow(kind, name):
    """the J-power of the item's weight: 2 for hf^2 X_SS and 1 for 2 hf X_S_g at t (hf = 2J); 0 elsewhere (hf = 1; mbar nonincreasing)."""
    if kind not in ('h', 'h1', 'h3'):                 # m4h_reader_v1: every kind here is a hook kind (hf = 2J), as t
        return 0
    return 2 if name == 'oSS' else (1 if name.startswith('oS_') else 0)


def kind_keys(kind):
    """the per-kind key stems of N<N>_<K>_..., without the ND_K<k> keys."""
    if kind == 'am':
        return ('M0', 'M1', 'M2', 'M3', 'NR', 'MG', 'FAR', 'ZMIN', 'L300', 'Q300')
    return (('M0', 'M1', 'M2', 'M3', 'ND', 'NR0', 'TXM', 'TBM', 'ANN', 'MG', 'FAR', 'SUPF', 'ZMIN', 'L300', 'Q300')
            + (('EPSR300',) if kind not in ('h', 'h1', 'h3') else ()))   # m4h_reader_v1: no lambda~_0 for the hook kinds


def farb(f):
    """an exact Fraction as an arb ball (exact when the denominator is a power of 2, else a containing ball)."""
    f = Fraction(f)
    return arb(f.numerator) / f.denominator


def ipow(x, k):
    """x^k for an integer k by repeated multiplication (arb ** int takes the general real power)."""
    if k < 0:
        return 1 / ipow(x, -k)
    r = arb(1)
    for _ in range(k):
        r = r * x
    return r


def frac_upper(x):
    """the exact upper end of a finite ball as a Fraction (python-flint's man_exp is signed)."""
    if not x.is_finite():
        raise ValueError('a law ball is not finite')
    m, e = x.upper().man_exp()
    return Fraction(int(m)) * Fraction(2) ** int(e)


def dec_up(f, digits=17):
    """a decimal string at or above the Fraction f >= 0 (rounded up exactly to the given significant digits)."""
    if f < 0:
        raise ValueError('dec_up: negative value %r' % f)
    if f == 0:
        return '0'
    e = len(str(f.numerator)) - len(str(f.denominator))
    while Fraction(10) ** e > f:
        e -= 1
    while Fraction(10) ** (e + 1) <= f:
        e += 1
    sc = f * Fraction(10) ** (digits - 1 - e)
    n = -((-sc.numerator) // sc.denominator)
    if n == 10 ** digits:
        n, e = 10 ** (digits - 1), e + 1
    s = str(n)
    return '%s.%se%+03d' % (s[0], s[1:], e)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def parse(text):
    kv = {}
    for ln in text.splitlines():
        if not ln.strip() or ln.startswith('#'):
            continue
        mt = re.fullmatch(r'([A-Z][A-Z0-9_]*) = (.*)', ln)
        if mt is None:
            raise ValueError('not a KEY = value line: %r' % ln[:60])
        if mt.group(1) in kv:
            raise ValueError('key %s twice' % mt.group(1))
        kv[mt.group(1)] = mt.group(2)
    return kv


def dec(s, what):
    if not DEC.fullmatch(s):
        raise ValueError('%s: not a nonnegative finite decimal: %r' % (what, s[:40]))
    return Fraction(s)


def binrepr(s, what):
    """an exact binary64 repr (the shortest round-trip form) as its exact Fraction."""
    if not REPR.fullmatch(s) or repr(float(s)) != s:
        raise ValueError('%s: not an exact binary64 repr: %r' % (what, s[:40]))
    return Fraction(float(s))


def jfrac(J):
    if isinstance(J, bool) or not isinstance(J, (int, Fraction, str)):
        raise ValueError('law: J must be an int, a Fraction or a decimal string')
    if isinstance(J, str) and not DEC.fullmatch(J):
        raise ValueError('law: J = %r is not a decimal string' % J[:40])
    if Fraction(J) < 300:
        raise ValueError('law: J = %s is below J_REF 300' % J)
    return Fraction(J)


def kappa_b():
    """kt_cert_v1_8 l.1719-1724: 2 (1 - cos delta) - a^2/(4 (1 - a)), a = max(a_m, a_e) (binary64 values, exact in arb)."""
    a = arb(max(A_M_F, A_E_F))
    return 2 * (1 - COS40) - a * a / (4 * (1 - a))


def parse_kind(kv, n, kind, ndkeys):
    """the kind's values at N = n as exact Fractions, with their form checks."""
    pre = 'N%d_%s_' % (n, KK[kind])
    p = {}
    for k in kind_keys(kind):
        if k not in ('MG', 'FAR', 'SUPF'):
            p[k] = dec(kv[pre + k], pre + k)
    if kind != 'am':
        p['NDK'] = [dec(kv[k], k) for k in ndkeys]
        sup = {}
        for tok in kv[pre + 'SUPF'].split(' ; '):
            parts = tok.split(':')
            if len(parts) != 2 or not re.fullmatch(r'-?(0|[1-9][0-9]*)', parts[0]) or parts[0] == '-0' or int(parts[0]) in sup:
                raise ValueError('%sSUPF: bad token %r' % (pre, tok[:40]))
            sup[int(parts[0])] = dec(parts[1], pre + 'SUPF')
        p['SUPF'] = sup
    mg = {}
    for tok in kv[pre + 'MG'].split(' ; '):
        parts = tok.split(':')
        if len(parts) != 3 or parts[0] not in BASES[kind] or parts[1] not in ('0', '1', '2', '3') or (parts[0], int(parts[1])) in mg:
            raise ValueError('%sMG: bad token %r' % (pre, tok[:40]))
        mg[(parts[0], int(parts[1]))] = binrepr(parts[2], pre + 'MG')
    if len(mg) != 4 * len(BASES[kind]):
        raise ValueError('%sMG: %d tokens, not 4 per basis vector' % (pre, len(mg)))
    p['MG'] = mg
    far = {}
    for tok in kv[pre + 'FAR'].split(' ; '):
        parts = tok.split(':')
        if len(parts) != 4 or parts[0] not in far_names(kind) or parts[0] in far or not INT.fullmatch(parts[2]):
            raise ValueError('%sFAR: bad token %r' % (pre, tok[:60]))
        far[parts[0]] = (dec(parts[1], pre + 'FAR X300'), int(parts[2]), dec(parts[3], pre + 'FAR c'))
    if len(far) != len(far_names(kind)):
        raise ValueError('%sFAR: %d items, not the kind set of %d' % (pre, len(far), len(far_names(kind))))
    p['FAR'] = far
    return p


def c_mono(rec):
    """C-MONO (SPEC sect. 3), exactly, from the record's own values and the reader's constants."""
    if not (A_E_F > 0 and bool(kappa_b() > 0)):
        raise ValueError('C-MONO: a Chernoff rate is not certainly > 0')
    if not bool(RHO_G > arb(3) / 300):                # m4h_reader_v1: supF of h1, h3 has top degree 3 (2J supb)
        raise ValueError('C-MONO-GB: rho_G is not certainly above 3/300')
    for n in (4, 3):
        for kind in KINDS:
            p = rec['N%d' % n][kind]
            for name in far_names(kind):
                x300, pw, c = p['FAR'][name]
                if not (c > 0 and Fraction(far_wpow(kind, name) + pw) / c <= 300):
                    raise ValueError('C-MONO-FAR4 N%d %s %s: (w + p)/c is above 300' % (n, kind, name))
            if kind != 'am':
                top = max([d for d, v in p['SUPF'].items() if v > 0], default=0)
                if top > 3:
                    raise ValueError('C-MONO-GB N%d %s: supF top degree %d is above 3' % (n, kind, top))
            if not p['ZMIN'] > 0:
                raise ValueError('N%d %s: Z_min is not > 0' % (n, kind))
            if kind in ('e1', 'e3') and not p['EPSR300'] < 1:
                raise ValueError('N%d %s: eps_r(300) is not below 1' % (n, kind))
    return True


def law_balls(rec, kind, N, J):
    """L_k(J) and its parts as arb balls (SPEC sect. 2), from the record alone."""
    if kind not in KINDS or isinstance(N, bool) or N not in (3, 4):
        raise ValueError('law: kind %r or N %r is not covered' % (kind, N))
    Ja = farb(jfrac(J))
    s, t = 300 / Ja, 1 / Ja
    q = rec['N%d' % N]
    p = q[kind]
    out = {'nP': sum((ipow(s, k) * farb(p['M%d' % k]) for k in range(4)), arb(0))}
    if kind == 'am':
        out['nR'] = ipow(s, 4) * farb(p['NR'])
        near = out['nP'] + out['nR']
    else:
        nd1 = ipow(s, 4) * farb(p['ND'])
        nd2 = sum((ipow(s, 4 + k) * farb(v) for k, v in enumerate(p['NDK'])), arb(0))
        out['nD'] = nd1 if frac_upper(nd1) <= frac_upper(nd2) else nd2
        out['nR0'] = ipow(s, 4) * farb(p['NR0'])
        da = (-LAM_CH * arb(A_E_F) * (Ja - 300) / 2).exp()
        db = (-LAM_CH * kappa_b() * (Ja - 300) / 2).exp()
        out['tailX'], out['tailB'], out['ann'] = da * farb(p['TXM']), db * farb(p['TBM']), da * farb(p['ANN'])
        near = out['nP'] + out['nD'] + out['nR0'] + out['tailX'] + out['tailB'] + out['ann']
    out['near'] = near
    hf = 2 * Ja if kind in ('h', 'h1', 'h3') else arb(1)   # m4h_reader_v1: kt_cert's HOOK kinds
    mbar = dict((g, sum((abs(farb(p['MG'][(g, j)])) * ipow(t, j) for j in range(4)), arb(0))) for g in BASES[kind])
    far = arb(0)
    for name in far_names(kind):
        x300, pw, c = p['FAR'][name]
        xj = farb(x300) * ipow(Ja / 300, pw) * (-farb(c) * (Ja - 300)).exp()
        if name == 'oSS':
            w = hf * hf
        elif name.startswith('oS_'):
            w = 2 * hf * mbar[name[3:]]
        else:
            g, h = name[3:].split('_')
            w = (1 if g == h else 2) * mbar[g] * mbar[h]
        far = far + w * xj
    out['far'] = far
    z = farb(p['ZMIN']).sqrt()
    if kind == 'am':
        out['gB'], out['D'] = arb(0), z
        out['L'] = (near * near + far).sqrt() / z
        return out
    supf = sum((farb(v) * ipow(Ja, d) for d, v in sorted(p['SUPF'].items())), arb(0))
    gs = arb(0)
    for r in range(3):
        hi = q['ZR'][r]
        zr = farb(hi[0]) + sum((farb(max(hi[k], 0)) * ipow(Ja, -k) for k in (1, 2, 3)), arb(0)) + farb(hi[4])
        gs = gs + farb(q['RM'][r]) * zr
    out['gB'] = supf * (-RHO_G * Ja).exp() * gs.sqrt()
    out['D'] = z * (1 - farb(p['EPSR300'])) if kind in ('e1', 'e3') else z
    out['L'] = ((near * near + far).sqrt() + out['gB']) / out['D']
    return out


def law(rec, kind, N, J):
    """L_k(J) as a decimal string at or above its ball's upper end."""
    return dec_up(frac_upper(law_balls(rec, kind, N, J)['L']))


def parse_record(text):
    """check() without C-MONO and C-FMT: the allow-list, the exact fields, the forms; returns rec (m4_asm_v1 computes L300 on it)."""
    kv = parse(text)
    want = set(KEYS_CONST) | set(KEYS_PIN)
    ndk = {}
    for n in (4, 3):
        want |= {'N%d_RATIO_MAIN_%d' % (n, r) for r in range(3)} | {'N%d_ZR_%d' % (n, r) for r in range(3)}
        for kind in KINDS:
            want |= {'N%d_%s_%s' % (n, KK[kind], k) for k in kind_keys(kind)}
            if kind != 'am':
                pre = 'N%d_%s_ND_K' % (n, KK[kind])
                ks = sorted(int(k[len(pre):]) for k in kv if k.startswith(pre) and INT.fullmatch(k[len(pre):]))
                if not ks or ks != list(range(len(ks))):
                    raise ValueError('%s<k> keys are not contiguous from 0' % pre)
                ndk[(n, kind)] = ['%s%d' % (pre, i) for i in ks]
                want |= set(ndk[(n, kind)])
    if set(kv) != want:
        raise ValueError('keys: missing %s; not allowed %s' % (sorted(want - set(kv))[:6], sorted(set(kv) - want)[:6]))
    for k, v in FIXED.items():
        if kv[k] != v:
            raise ValueError('%s = %r (must be %r)' % (k, kv[k][:60], v))
    if kv['CLAIM'] != CLAIM:
        raise ValueError('CLAIM differs from the certified text')
    if not (float(kv['A_E']) == A_E_F == 0.6 ** 2):
        raise ValueError('C-A-E: A_E is not the binary64 0.6 ** 2 that kt_cert_v1_8 l.818 computes')   # the law uses arb(A_E_F)
    if not HEX64.fullmatch(kv['ASM_SHA256']):
        raise ValueError('ASM_SHA256 is not a full sha256')
    if not re.fullmatch(r'20[0-9]{2}-[01][0-9]-[0-3][0-9]T[0-2][0-9]:[0-5][0-9]:[0-5][0-9]Z', kv['WRITTEN_UTC']):
        raise ValueError('WRITTEN_UTC is not a UTC stamp')
    for k in KEYS_PIN:
        for tok in kv[k].split(' ; '):
            p_, _, h = tok.rpartition(':')
            if not (re.fullmatch(r'[A-Za-z0-9_][A-Za-z0-9_./-]*', p_) and HEX64.fullmatch(h) and '..' not in p_.split('/')):
                raise ValueError('%s: bad token %r' % (k, tok[:60]))
    rec = {'kv': kv}
    for n in (4, 3):
        rn = {'RM': [dec(kv['N%d_RATIO_MAIN_%d' % (n, r)], 'N%d_RATIO_MAIN_%d' % (n, r)) for r in range(3)], 'ZR': []}
        for r in range(3):
            parts = kv['N%d_ZR_%d' % (n, r)].split(' ; ')
            if len(parts) != 5:
                raise ValueError('N%d_ZR_%d: %d entries, not 5' % (n, r, len(parts)))
            rn['ZR'].append([dec(x, 'N%d_ZR_%d' % (n, r)) for x in parts])
        for kind in KINDS:
            rn[kind] = parse_kind(kv, n, kind, ndk.get((n, kind)))
        rec['N%d' % n] = rn
    return rec


def check(text):
    """the record's own checks (see the docstring); returns rec, without 'record' and 'sha256'."""
    rec = parse_record(text)
    kv = rec['kv']
    c_mono(rec)
    for n in (4, 3):
        for kind in KINDS:
            u = frac_upper(law_balls(rec, kind, n, 300)['L'])
            v = rec['N%d' % n][kind]['L300']
            if not (u <= v <= u * (1 + Fraction(1, 10 ** 9))):
                raise ValueError('C-FMT N%d %s: L300 %s, the law upper end %s' % (n, kind, kv['N%d_%s_L300' % (n, KK[kind])], dec_up(u)))
    return rec


def loads(record_text, record_name, asm_out_text, expected_sha256=None):
    """the binding to m4_asm_v1's run output, then check() (no C-PINS)."""
    h = sha(record_text.encode())
    if expected_sha256 is not None and h != expected_sha256:
        raise ValueError('record sha256 %s differs from the pin' % h)
    lines = asm_out_text.splitlines()
    if [ln for ln in lines if ln.startswith('VERDICT')] != ['VERDICT VALID']:
        raise ValueError('asm output: VERDICT lines are not exactly [VERDICT VALID]')
    mt = re.match(r'm4h_asm_v1_1 sha256 ([0-9a-f]{64}) ', lines[0] if lines else '')   # m4h_reader_v1
    if mt is None or mt.group(1) != parse(record_text).get('ASM_SHA256'):
        raise ValueError('asm output: the first line does not name the record ASM_SHA256')
    rl = [ln for ln in lines if ln.startswith('RECORD ')]
    if rl != ['RECORD %s %s' % (record_name, h)]:
        raise ValueError('asm output: RECORD lines %r do not bind %s %s' % ([x[:90] for x in rl][:3], record_name, h[:8]))
    rec = check(record_text)
    rec.update(record=record_name, sha256=h)
    return rec


def load(path, asm_out, expected_sha256=None, reader_sha256=None):
    """the certified entry: loads() on the files, then C-PINS. C-PINS needs this reader's own sha256: reader_sha256 (the sha256 of the
    bytes a consumer checked and exec()ed) or, when the reader runs as a file, the sha256 of __file__."""
    with open(path, 'rb') as fh:
        data = fh.read()
    with open(asm_out) as fh:
        atext = fh.read()
    rec = loads(data.decode(), os.path.basename(path), atext, expected_sha256)
    if reader_sha256 is not None:
        if not HEX64.fullmatch(str(reader_sha256)):
            raise ValueError('C-PINS: reader_sha256 is not a full sha256')
        own = reader_sha256
    elif '__file__' in globals():
        with open(os.path.abspath(globals()['__file__']), 'rb') as fh:
            own = sha(fh.read())
    else:
        raise ValueError('C-PINS: this reader runs without __file__ (exec); pass reader_sha256, the sha256 of the bytes you executed')
    for k in KEYS_PIN:
        for tok in rec['kv'][k].split(' ; '):
            p_, _, h = tok.rpartition(':')
            try:
                with open(os.path.join(W18, p_), 'rb') as fh:
                    got = sha(fh.read())
            except OSError:
                got = 'MISSING'
            if got != h:
                raise ValueError('C-PINS: %s %s (pinned %s)' % (p_, got[:8], h[:8]))
    code = dict(tok.rpartition(':')[::2] for tok in rec['kv']['PIN_CODE'].split(' ; '))
    if code.get(READER_REL) != own:
        raise ValueError('C-PINS: PIN_CODE does not name this reader sha256')
    if code.get(ASM_REL) != rec['kv']['ASM_SHA256']:
        raise ValueError('C-PINS: PIN_CODE does not name m4h_asm_v1_1.py at ASM_SHA256')
    return rec


def _refused(fn):
    try:
        fn()
        return False, ''
    except ValueError as e:
        return True, str(e)


def _sub(text, key, new):
    return '\n'.join(('%s = %s' % (key, new)) if ln.startswith(key + ' = ') else ln for ln in text.splitlines()) + '\n'


def _plant_far_c(text, kv):
    """N4 t's oSS rate set just below its C-MONO-FAR4 threshold (2 + p)/300: c = (2 + p)/301, rounded up to 17 digits."""
    out = []
    for tok in kv['N4_H_FAR'].split(' ; '):   # m4h_reader_v1: N4 h
        nm, x, pw, c = tok.split(':')
        out.append(':'.join((nm, x, pw, dec_up(Fraction(2 + int(pw), 301)))) if nm == 'oSS' else tok)
    return _sub(text, 'N4_H_FAR', ' ; '.join(out))


def plants(text, atext, name):
    """the script-mode plants as (name, the refusing check's message prefix, call)."""
    kv = parse(text)
    return [('PLANT-SWAP', 'C-FMT N4 h:', lambda: check(_sub(_sub(text, 'N4_H_M1', kv['N4_H1_M1']), 'N4_H1_M1', kv['N4_H_M1']))),
            ('PLANT-MOCK', 'FORMAT = ', lambda: check(_sub(_sub(text, 'FORMAT', 'M4H_KV_v1 MOCK'), 'CLAIM', 'MOCK ' + kv['CLAIM']))),
            ('PLANT-PRECERT', 'FORMAT = ', lambda: check(_sub(text, 'FORMAT', 'M4H_KV_v1_PRECERT'))),
            ('PLANT-VERDICT', 'VERDICT = ', lambda: check(_sub(text, 'VERDICT', 'VALID-PRECERT'))),
            ('PLANT-BIND', 'asm output: RECORD lines ',
             lambda: loads(text, name, re.sub(r'^(RECORD \S+ )[0-9a-f]{64}$', r'\g<1>' + '0' * 64, atext, flags=re.M))),
            ('PLANT-MONO', 'C-MONO-FAR4 N4 h oSS:', lambda: check(_plant_far_c(text, kv)))]


def run_plants(pl):
    """each plant must be refused, by the named check; returns the failures."""
    fails = []
    for nm, want, fn in pl:
        ok, why = _refused(fn)
        hit = ok and why.startswith(want)
        print('%s -> %s (%s)' % (nm, 'REFUSED by %s' % want.strip() if hit else 'NOT REFUSED AS PLANNED', why[:110]))
        if not hit:
            fails.append('%s not refused by %s' % (nm, want.strip()))
    return fails


def script(path, aout, pin=None, reader_sha256=None):
    """script mode: load, the law at J = 300 and 600 per N and kind, the plants and the VERDICT line."""
    fails = []
    try:
        rec = load(path, aout, pin, reader_sha256)
        print('READ: the binding, the record checks (allow-list, exact fields, forms, C-MONO, C-FMT) and C-PINS PASS')
        for n in (4, 3):
            for k in KINDS:
                l300, q = law(rec, k, n, 300), rec['N%d' % n][k]['Q300']
                print('LAW N=%d %s: L(300) %s; L(600) %s; INFO L(300)/Q300 - 1 = %s' % (n, k, l300, law(rec, k, n, 600),
                                                                                       '%.4e' % (Fraction(l300) / q - 1) if q > 0 else 'n/a'))
    except ValueError as e:
        print('READ: refused: %s' % e)
        fails.append('READ')
    with open(path) as fh:
        text = fh.read()
    with open(aout) as fh:
        atext = fh.read()
    fails += run_plants(plants(text, atext, os.path.basename(path)))
    print('VERDICT %s' % ('VALID' if not fails else 'INVALID (%s)' % ', '.join(fails)))
    return not fails


if __name__ == '__main__':
    if len(sys.argv) not in (3, 4):
        print('usage: m4h_reader_v1_1.py <record> <asm output> [expected sha256]')
        sys.exit(2)
    with open(os.path.abspath(__file__), 'rb') as fh:
        print('m4h_reader_v1_1 sha256 %s; record %s; asm output %s' % (sha(fh.read()), os.path.basename(sys.argv[1]),
                                                                  os.path.basename(sys.argv[2])))
    script(sys.argv[1], sys.argv[2], sys.argv[3] if len(sys.argv) == 4 else None)
