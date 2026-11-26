#!/usr/bin/env python3
"""a3_bulk_checks_v1.py (pk21, step 1 component A, piece A-3): the per-piece checks of W2's bulk steps
S9(j), S9(g), S9(d'), S9(e) and S9(f) on the certified exports, in outward interval arithmetic (mpmath iv, 256 bits; every decimal
read as the tightest interval that contains it). Every row of the exports holds for every J of its piece (their J_UNIFORMITY lines).
Inputs (sha256 checked at start):
  T  = pk15/out/export_p2_t_cert_kt_p2_assembly_v1_37_1.kv     (R4's t export: At_lo, Ot_hi, Pt_hi, Xta_lo, Xtb_lo, Aa_lo, ...)
  SV = pk07/out/export_kt_s9h_v1_2_vsweep.kv                    (the S_V export: rho_hi, vp2_hi, vm2_hi, r2_hi, ro_hi, ...)
  JX = pk15/out/export_p2_14_joint_cert_kt_p2_assembly_v1_37_1.kv (R4's joint export: Cov_inf_lo per class D3, D4, D4M)
  CR = pk15/out/out_kt_p2_assembly_v1_37_1_cert.out            (R4's run output: the KT-MARGINS lines)
Checks per piece and N (lower ends must be > 0):
  S9(j): Xta_lo, Xtb_lo (X_tb = X_ta by the flip, the export's XTB_SOURCE);
  S9(g): At_lo^2 - 1.05 Ot_hi (plan row P2-4, C7) and At_lo^2 - Ot_hi; rho <= s_x,lo comes from CR's KT-MARGINS (s_x,low - tau_up,
         tau_up = S6's rho, C-TAU-READ);
  S9(d'): Xta_lo - Pt_hi pi_a, pi_a = (vp2_hi - Aa_lo^2)^(1/2) >= ||P_perp v_a+|| (plan row P2-6; Pt_hi >= ||P_perp v_t+||);
  S9(e): Xta_lo - Pt_hi pi_a r2_hi - Ot_hi^(1/2) vm2_hi^(1/2) ro_hi, the k = 1 value in units of s_x^k; r2_hi, ro_hi < 1 bound the
         even-complement and odd decay rates relative to s_x (S7's mode inputs), so the subtracted terms do not increase for k >= 1;
  S9(f), k = 0 (D5, D6) and every k >= 0 at once: Xta_lo - Pt_hi pi_a - Ot_hi^(1/2) vm2_hi^(1/2); the same with At_lo Aa_lo in place of
         Xta_lo is R5's mixed kind at e = 0 (cross-check);
  S9(f), D3, D4, D4M: Cov_inf_lo of the joint export.
Usage: a3_bulk_checks_v1.py OUTDIR
"""
import sys, os, re, hashlib
from mpmath import iv
iv.prec = 256
W = '/mnt/g2/release/root/code'
FILES = {
    'T': (W + '/pk15/out/export_p2_t_cert_kt_p2_assembly_v1_37_1.kv', 'ad7e863d'),
    'SV': (W + '/pk07/out/export_kt_s9h_v1_2_vsweep.kv', '10f3c3d9'),
    'JX': (W + '/pk15/out/export_p2_14_joint_cert_kt_p2_assembly_v1_37_1.kv', '7b8acf7c'),
    'CR': (W + '/pk15/out/out_kt_p2_assembly_v1_37_1_cert.out', 'b4a1dea6'),
}
OUT = sys.argv[1]


def sha(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()


def read_kv(path):
    fields, rows = None, {}
    for line in open(path):
        if line.startswith('FIELDS'):
            fields = line.split('=', 1)[1].split()
        m = re.match(r'(N[34]_(?:[A-Z0-9]+_)?P\d{4}) = (.*)$', line.rstrip('\n'))
        if m:
            rows[m.group(1)] = m.group(2).split('|', 1)[0].split()
    return fields, rows


def I(s):
    return iv.mpf(s)


def lo(x):
    return float(x.a)


def main():
    print('a3_bulk_checks_v1 sha256 %s' % sha(os.path.abspath(__file__)))
    for k, (p, s8) in FILES.items():
        h = sha(p)
        print('INPUT %s %s sha256 %s -> %s' % (k, p.replace(W + '/', ''), h, 'PIN OK' if h.startswith(s8) else 'PIN MISMATCH'))
        if not h.startswith(s8):
            raise SystemExit('pin mismatch')
    ft, T = read_kv(FILES['T'][0])
    fs, SV = read_kv(FILES['SV'][0])
    fj, JX = read_kv(FILES['JX'][0])
    cr = open(FILES['CR'][0]).read()
    for N in (4, 3):
        m = re.search(r'INFO KT-MARGINS N=%d: .*?s_x,low - tau_up ([0-9.eE+-]+), g_below ([0-9.eE+-]+)' % N, cr)
        print('CR KT-MARGINS N=%d: smallest s_x,low - tau_up %s, g_below %s (lower ends over the 904 port rows)' % (N, m.group(1), m.group(2)))
    ti = {f: i for i, f in enumerate(ft)}
    si = {f: i for i, f in enumerate(fs)}
    ji = {f: i for i, f in enumerate(fj)}
    bad = 0
    for N in (4, 3):
        keys = sorted(k for k in T if k.startswith('N%d_P' % N))
        mins = {}
        tsv = open(os.path.join(OUT, 'a3_rows_N%d_v1.tsv' % N), 'x')
        tsv.write('piece\tjlo\tjhi\tXta_lo\tg_ratio\td1\te1\tf0\tf0R\tr2_hi\tro_hi\n')
        for k in keys:
            t, s = T[k], SV[k]
            if t[0] != s[0] or t[1] != s[1]:
                raise SystemExit('grid mismatch at %s: %s %s vs %s %s' % (k, t[0], t[1], s[0], s[1]))
            At, Ot, Pt = I(t[ti['At_lo']]), I(t[ti['Ot_hi']]), I(t[ti['Pt_hi']])
            Xa, Xb, Aa = I(t[ti['Xta_lo']]), I(t[ti['Xtb_lo']]), I(t[ti['Aa_lo']])
            vp2, vm2 = I(s[si['vp2_hi']]), I(s[si['vm2_hi']])
            r2, ro = I(s[si['r2_hi']]), I(s[si['ro_hi']])
            arg = vp2 - Aa * Aa
            pia = iv.sqrt(iv.mpf([0, arg.b])) if (arg.b > 0) else iv.mpf(0)
            pia = iv.mpf([pia.b, pia.b])                       # an upper bound used as a point
            so = iv.sqrt(Ot)
            vm = iv.sqrt(vm2)
            vals = {
                'j_a': Xa, 'j_b': Xb,
                'g_ratio': (At * At) / (iv.mpf('1.05') * Ot), 'g_105': At * At - iv.mpf('1.05') * Ot, 'g_flip': At * At - Ot,
                'd1': Xa - Pt * pia,
                'e1': Xa - Pt * pia * r2 - so * vm * ro,
                'f0': Xa - Pt * pia - so * vm,
                'f0R': At * Aa - Pt * pia - so * vm,
                'one_minus_r2': 1 - r2, 'one_minus_ro': 1 - ro,
            }
            for name, v in vals.items():
                if name not in mins or v.a < mins[name][0].a:
                    mins[name] = (v, k, t[0], t[1])
            for name in ('j_a', 'j_b', 'g_105', 'g_flip', 'd1', 'e1', 'f0', 'f0R', 'one_minus_r2', 'one_minus_ro'):
                if not (vals[name].a > 0):
                    bad += 1
                    print('NONPOSITIVE %s %s lower end %.8e' % (name, k, float(vals[name].a)))
            tsv.write('%s\t%s\t%s\t%.8e\t%.6f\t%.8e\t%.8e\t%.8e\t%.8e\t%.6f\t%.6f\n' % (
                k, t[0], t[1], lo(Xa), lo(vals['g_ratio']), lo(vals['d1']), lo(vals['e1']), lo(vals['f0']), lo(vals['f0R']),
                float(r2.b), float(ro.b)))
        tsv.close()
        print('N=%d: %d pieces (t and S_V grids identical)' % (N, len(keys)))
        for name in ('j_a', 'j_b', 'g_ratio', 'g_flip', 'd1', 'e1', 'f0', 'f0R', 'one_minus_r2', 'one_minus_ro'):
            v, k, a, b = mins[name]
            print('  min %-13s lower end %.10e at %s [%s, %s]' % (name, float(v.a), k, a, b))
        for cl in ('D3', 'D4', 'D4M'):
            ks = sorted(x for x in JX if x.startswith('N%d_%s_P' % (N, cl)))
            mn = min(ks, key=lambda x: float(I(JX[x][ji['Cov_inf_lo']]).a))
            nonpos = sum(1 for x in ks if not (I(JX[x][ji['Cov_inf_lo']]).a > 0))
            bad += nonpos
            print('  joint %-3s %d pieces: min Cov_inf_lo %s at %s; nonpositive %d' % (cl, len(ks), JX[mn][ji['Cov_inf_lo']], mn, nonpos))
    print('NONPOSITIVE COUNT %d' % bad)
    print('VERDICT %s' % ('ALL POSITIVE' if bad == 0 else 'SOME NONPOSITIVE'))


if __name__ == '__main__':
    main()
