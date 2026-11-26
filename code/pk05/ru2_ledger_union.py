#!/usr/bin/env python3
# ru2_ledger_union.py (pk05, P-RH Stage B, R11; v2 of ru1_ledger_union de3c6f81): independent union check of the strip ledger. It
# reads the job outputs named in a manifest (each sha256-checked), keeps the LEDGER lines of VALID jobs only, rebuilds every interval
# [b0 - h, b0 + h] exactly from b0hex and hhex (Python Fractions; no arb, no engine code), and checks, for N = 3 and N = 4, that [a, b]
# lies in
#     U_A  n  (U_B  u  (U_Bh  n  U_Bv)),
# U_P the union of the closed intervals tagged P (a smoke's tag AB counts for A and for B).
# A job counts iff its first line is 'SELF sha256 <engine sha256>' (the engine named by line 1 of the given engine manifest), its
# output has the line 'VALID True', its VERDICT is not VOID, it has no CONFLICT line, and (v2: R9 v1_1 TR1) it has at least
# one FAMILY line with centring values and at least as many as LEDGER lines, and every centring value printed for a horizontal type
# (th, mh, bh; 9 decimals) lies in [0, 1 - 10^-9], so that the engine's alpha_e lies in [0, 1]. Every CERTIFIED interval of such a
# job counts.
# Checks per LEDGER line: the printed lo, hi (25 digits) agree with the exact endpoints to 1e-22 relative.
# Reading: COVERED N=<N> [a, b] iff the containment holds; otherwise every gap is printed exactly (as decimals to 30 digits).
# Controls (each must FIRE, else the run is VOID): P-HOLE (all intervals of U_A containing the midpoint of [a, b] removed: a gap must be
# found for each N), P-VOIDJOB (a synthetic job without 'VALID True' whose LEDGER line would close that hole must be ignored),
# P-TAG (every Bv interval dropped and every B interval retagged Bh: Bh alone must not count as B, so a gap must appear wherever the
# cover was complete), P-ALPHA (v2: a synthetic VALID job whose centring value th is 1.000000001 must be ignored, so the hole stays
# open, while the same job with th 0.999999999 counts).
# Usage: ru2_ledger_union.py <manifest of job outputs> <a> <b> <engine manifest>
import sys
import hashlib
from fractions import Fraction

ATOP = 1 - Fraction(1, 10 ** 9); import sys as _acsys, importlib.util as _acu, hashlib as _ach; _acp = '/mnt/g2/release/root/code/acc/acc2_v1.py'; _ach.sha256(open(_acp, 'rb').read()).hexdigest() == '655579ea961827c747964e9404ef8fd24d1ef6804d5bdb16595b81651bd83b1f' or _acsys.exit('acc2_v1.py does not match its pin'); ACC = _acsys.modules.get('acc2_v1'); _acs = None if ACC else _acu.spec_from_file_location('acc2_v1', _acp); ACC = ACC or _acu.module_from_spec(_acs); _acs and (_acs.loader.exec_module(ACC), _acsys.modules.setdefault('acc2_v1', ACC)); ORIG_ESHA = 'b0f40c890d4e4be4b389f4fc690916d99d57816369465503b3989a64b3657de7'  # G-ORIG: option (C), acc2 two-producer acceptance


def centring(lines):
    """(number of FAMILY lines with centring values, largest horizontal value printed, every one of them in [0, ATOP])"""
    n, vmax, ok = 0, None, True
    for x in lines:
        if not (x.startswith('FAMILY ') and ' centring ' in x):
            continue
        f = x.split(' centring ', 1)[1].split()
        kv = dict(zip(f[0::2], f[1::2]))
        n += 1
        for e in ('th', 'mh', 'bh'):
            try:
                v = Fraction(kv[e].rstrip(','))
            except (KeyError, ValueError, ZeroDivisionError):
                ok = False
                continue
            vmax = v if (vmax is None or v > vmax) else vmax
            ok = ok and (0 <= v <= ATOP)
    return n, vmax, ok


def parse_job(lines, esha=None, path=None):
    """[(part, N, lo, hi)] from one job's output lines, or [] if the job does not count"""
    if esha is not None and (not lines or not (lines[0].strip() == 'SELF sha256 %s' % esha or (path is not None and lines[0].strip() == 'SELF sha256 %s' % ORIG_ESHA and ACC.ok(path, ORIG_ESHA, esha, ORIG_ESHA)))):
        return []
    if not any(x.strip() == 'VALID True' for x in lines) or any('CONFLICT' in x for x in lines):
        return []
    if any(x.startswith('VERDICT VOID') for x in lines):
        return []
    nfam, _, aok = centring(lines)
    if not aok or nfam < max(1, sum(1 for x in lines if x.startswith('LEDGER '))):
        return []
    res = []
    for x in lines:
        if not x.startswith('LEDGER '):
            continue
        f = x.split()
        part, N = f[1], int(f[2].split('=')[1])
        kv = dict(t.split('=', 1) for t in f[3:])
        b0, h = Fraction(float.fromhex(kv['b0hex'])), Fraction(float.fromhex(kv['hhex']))
        lo, hi = b0 - h, b0 + h
        for s, v in ((kv['lo'], lo), (kv['hi'], hi)):
            if abs(Fraction(s) - v) > Fraction(1, 10 ** 22) * abs(v):
                raise SystemExit('LEDGER print mismatch: %s' % x.strip())
        res.append((part, N, lo, hi))
    return res


def merge(iv):
    """union of closed intervals as a sorted list of disjoint closed intervals"""
    out = []
    for lo, hi in sorted(iv):
        if out and lo <= out[-1][1]:
            out[-1] = (out[-1][0], max(out[-1][1], hi))
        else:
            out.append((lo, hi))
    return out


def inter(u, v):
    """intersection of two merged lists"""
    i, j, out = 0, 0, []
    while i < len(u) and j < len(v):
        lo, hi = max(u[i][0], v[j][0]), min(u[i][1], v[j][1])
        if lo <= hi:
            out.append((lo, hi))
        if u[i][1] < v[j][1]:
            i += 1
        else:
            j += 1
    return merge(out)


def certified(recs, N):
    """U_A n (U_B u (U_Bh n U_Bv)) for one N"""
    U = {p: merge([(lo, hi) for (q, n, lo, hi) in recs if n == N and (q == p or (q == 'AB' and p in 'AB'))]) for p in ('A', 'B', 'Bh', 'Bv')}
    return inter(U['A'], merge(U['B'] + inter(U['Bh'], U['Bv']))), {p: len(u) for p, u in U.items()}


def gaps(cert, a, b):
    """the parts of [a, b] outside the merged list cert (closed intervals; a gap may be a single point)"""
    out, x = [], a
    for lo, hi in cert:
        if hi < x:
            continue
        if lo > b:
            break
        if lo > x:
            out.append((x, lo))
        x = max(x, hi)
        if x >= b:
            break
    if x < b:
        out.append((x, b))
    return out


def dec(v):
    """v >= 0 as a decimal with 30 digits after the point (truncated)"""
    q = v.numerator // v.denominator
    return '%d.%030d' % (q, (v - q) * 10 ** 30 // 1)


def main():
    with open(__file__, 'rb') as fh:
        print('SELF sha256 %s' % hashlib.sha256(fh.read()).hexdigest(), flush=True)
    man, a, b = sys.argv[1], Fraction(sys.argv[2]), Fraction(sys.argv[3])
    with open(sys.argv[4]) as fh:
        esha = fh.readline().split()[0]
    print('ENGINE sha256 %s (line 1 of %s)' % (esha, sys.argv[4]), flush=True)
    recs, njob, nok = [], 0, 0
    with open(man) as fh:
        entries = [x.split() for x in fh if x.strip()]
    for sha, path in entries:
        with open(path, 'rb') as fh:
            data = fh.read()
        if hashlib.sha256(data).hexdigest() != sha:
            raise SystemExit('SHA MISMATCH %s' % path)
        njob += 1
        lines = data.decode().splitlines()
        r = parse_job(lines, esha, path)
        nf, vm, aok = centring(lines)
        nok += 1 if r else 0
        recs += r
        print('JOB %s sha8 %s: %d ledger intervals counted; FAMILY centring lines %d, largest horizontal centring %s (%s)' % (
            path, sha[:8], len(r), nf, '-' if vm is None else '%.9f' % float(vm), 'in range' if aok else 'OUT OF RANGE'), flush=True)
    covered, fired = {}, {}
    mid = (a + b) / 2
    for N in (3, 4):
        cert, cnt = certified(recs, N)
        g = gaps(cert, a, b)
        covered[N] = not g
        print('UNION N=%d: merged components per tag %s; certified components %d; gaps %d %s' % (
            N, cnt, len(cert), len(g), ' '.join('[%s, %s]' % (dec(lo), dec(hi)) for lo, hi in g[:5])), flush=True)
        hole = [r for r in recs if not (r[1] == N and r[0] in ('A', 'AB') and r[2] <= mid <= r[3])]
        fired['P-HOLE N=%d' % N] = bool(gaps(certified(hole, N)[0], a, b))
        fake = parse_job(['SELF sha256 %s' % esha, 'LEDGER A N=%d lo=%s hi=%s b0hex=%s hhex=%s' % (N, '0', '0', float(mid).hex(), (1.0).hex())],
                         esha)
        fired['P-VOIDJOB N=%d' % N] = (fake == []) and bool(gaps(certified(hole + fake, N)[0], a, b))
        m0 = Fraction(float(mid))

        def fakej(th):
            return ['SELF sha256 %s' % esha, 'FAMILY base: centring th %s mh 0.5 bh 0.5 tv 0.5 bv 0.5, |J_p| 1' % th, 'VALID True',
                    'LEDGER A N=%d lo=%s hi=%s b0hex=%s hhex=%s' % (N, m0 - 1, m0 + 1, float(mid).hex(), (1.0).hex())]
        bad, good = parse_job(fakej('1.000000001'), esha), parse_job(fakej('0.999999999'), esha)
        fired['P-ALPHA N=%d' % N] = (bad == []) and len(good) == 1 and bool(gaps(certified(hole + bad, N)[0], a, b))
        tagged = []
        for r in recs:
            if r[1] != N or r[0] == 'Bv':
                continue
            if r[0] == 'AB':
                tagged += [('A',) + r[1:], ('Bh',) + r[1:]]
            else:
                tagged.append(('Bh',) + r[1:] if r[0] == 'B' else r)
        fired['P-TAG N=%d' % N] = (not covered[N]) or bool(gaps(certified(tagged, N)[0], a, b))
    print('CONTROLS %s' % ' '.join('%s:%s' % (k, 'FIRED' if v else 'DID-NOT-FIRE') for k, v in fired.items()), flush=True)
    valid = all(fired.values())
    print('JOBS %d, counted %d' % (njob, nok), flush=True)
    print('VALID %s' % valid, flush=True)
    for N in (3, 4):
        print('VERDICT N=%d [%s, %s]: %s' % (N, sys.argv[2], sys.argv[3], ('COVERED' if covered[N] else 'NOT COVERED') if valid else 'VOID'))


if __name__ == '__main__':
    main()
