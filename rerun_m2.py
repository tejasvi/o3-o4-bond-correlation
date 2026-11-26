#!/usr/bin/env python3
"""rerun_m2.py: the reruns of this package, in level order, each output compared with the copy this package ships.

Run it from the package root, mounted at /mnt/g2/release/root, on a writable copy or overlay of the package, with a python3 that has
the packages the programs import. For each selected run of the run table RUNS_M2_release_<issue>.tsv at the root, in level order:
1. each output of the run that the package holds (the shipped rerun output at its code path; records/ holds byte copies) is moved
   to <path>.shipped, since the programs create their outputs with mode 'x';
2. the command runs in its folder (sh -c, one thread);
3. each new output is compared line by line with the shipped copy. Masked: timing fields (CPU, elapsed and wall times, memory peaks,
   time stamps, decimal seconds, and in JSON lines the numbers under timing keys); and, in named files only, two fields: the per-row
   timings t_in=, t_k=, t_p= and t= (seconds) of the four hub cover outputs code/pk05/out/hubcert_v1e_cover<N>_<range>.out (N 3 or 4,
   range 20_50 or 50_100), and the stray tag on the IMPORT line of code/pk12/out/p212_v1_3_6_2/out_kt_p212_cert_v1_3_6_2_cert_final.out
   (the program takes the first free tag of r50..r99, so on a copy where p212pre has run it takes the next one). Accepted: a line
   'END <sha256>' when each side's
   value is the sha256 of its own body; a checksum (or its leading hex digits) of a file written by the same run, when it maps the
   shipped file's checksum to the new file's;
4. the new output is kept as <path>.rerun and the shipped copy is moved back, so later runs read the bytes their checksum pins name.
It prints PASS or FAIL for each output, with the first differing lines, and the totals; the exit status is 1 if any output fails.
usage: python3 -I -B rerun_m2.py [--runs ID,ID,...] [--levels FIRST-LAST]"""
import sys, os, re, json, hashlib, subprocess

ROOT = '/mnt/g2/release/root'
TABLE = os.path.join(ROOT, next(n for n in sorted(os.listdir(ROOT)) if n.startswith('RUNS_M2_release_') and n.endswith('.tsv')))
TIME_RX = [
    (re.compile(r'\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d(?:\.\d+)?Z'), '<TS>'),
    (re.compile(r'\[cpu\s+[0-9.]+s\]'), '[cpu <T>s]'),
    (re.compile(r'(STAGE-CPU\b.*?\s)([0-9]+(?:\.[0-9]+)?)(\s*s\b)'), r'\1<T>\3'),
    (re.compile(r'(?i)\b(cpu|elapsed|wall|maxrss_kb|maxrss|rss|peak resident memory|peak|seconds|time)(\s*[=:]?\s*)([0-9]+(?:\.[0-9]+)?)'),
     r'\1\2<T>'),
    (re.compile(r'(?<![0-9A-Za-z_.])[0-9]+\.[0-9]+(\s?s\b)'), r'<T>\1'),
]
TIME_KEY = re.compile(r'(?i)^(cpu|elapsed|wall|rss|time|seconds)$')
END_RX = re.compile(r'^END ([0-9a-f]{64})$')
HEX_RX = re.compile(r'(?<![0-9a-f])[0-9a-f]{8,64}(?![0-9a-f])')
HUB_T = [(re.compile(r'(?<![0-9A-Za-z_.])(t_in|t_k|t_p|t)=[0-9]+(?:\.[0-9]+)?(?![0-9A-Za-z_.])'), r'\1=<T>')]
IMPORT_TAG = [(re.compile(r'^(IMPORT: kt_s8_cert_v1_14_3 in its cert namespace, chunk c[0-9]+_[0-9]+_[0-9]+ with tag )r[0-9]+'
                          r'( \(the first free of r50\.\.r99; a stray, not counted)'), r'\1r<N>\2')]
FILE_RX = {
    'code/pk05/out/hubcert_v1e_cover3_20_50.out': HUB_T,
    'code/pk05/out/hubcert_v1e_cover3_50_100.out': HUB_T,
    'code/pk05/out/hubcert_v1e_cover4_20_50.out': HUB_T,
    'code/pk05/out/hubcert_v1e_cover4_50_100.out': HUB_T,
    'code/pk12/out/p212_v1_3_6_2/out_kt_p212_cert_v1_3_6_2_cert_final.out': IMPORT_TAG,
}


def sha(b):
    return hashlib.sha256(b).hexdigest()


def norm(s):
    for rx, rep in TIME_RX:
        s = rx.sub(rep, s)
    return s


def fnorm(s, rel):
    s = norm(s)
    for rx, rep in FILE_RX.get(rel, ()):
        s = rx.sub(rep, s)
    return s


def jnorm(x):
    if isinstance(x, dict):
        return {k: ('<T>' if TIME_KEY.match(k) and isinstance(v, (int, float)) else jnorm(v)) for k, v in x.items()}
    if isinstance(x, list):
        return [jnorm(v) for v in x]
    return norm(x) if isinstance(x, str) else x


def self_hash(L, i):
    m = END_RX.match(L[i])
    if not m:
        return False
    bodies = ['\n'.join(L[:i]) + '\n', '\n'.join(L[:i])]
    return any(sha(b.encode('latin-1')) == m.group(1) for b in bodies)


def compare(new, old, pairs, rel):
    a, b = new.decode('latin-1').split('\n'), old.decode('latin-1').split('\n')
    if len(a) != len(b):
        return ['line count %d, shipped %d' % (len(a), len(b))]
    bad = []
    for i, (x, y) in enumerate(zip(a, b)):
        if x == y or fnorm(x, rel) == fnorm(y, rel):
            continue
        if END_RX.match(x) and END_RX.match(y) and self_hash(a, i) and self_hash(b, i):
            continue
        y2 = HEX_RX.sub(lambda m: next((n[:len(m.group(0))] for o, n in pairs if o.startswith(m.group(0))), m.group(0)), y)
        if x == y2 or fnorm(x, rel) == fnorm(y2, rel):
            continue
        try:
            jx, jy = json.loads(x), json.loads(y2)
            if isinstance(jx, (dict, list)) and jnorm(jx) == jnorm(jy):
                continue
        except ValueError:
            pass
        bad.append('line %d: new %r / shipped %r' % (i + 1, x[:160], y[:160]))
    return bad


def main():
    args = sys.argv[1:]
    runs = levels = None
    while args:
        k = args.pop(0)
        if k == '--runs':
            runs = set(args.pop(0).split(','))
        elif k == '--levels':
            lo, hi = args.pop(0).split('-')
            levels = (int(lo), int(hi))
        else:
            sys.exit(__doc__)
    rows = []
    for ln in open(TABLE):
        if ln.startswith('#') or ln.startswith('run\t') or not ln.strip():
            continue
        rid, lv, fam, folder, outs, after, cmd = ln.rstrip('\n').split('\t')
        if (runs is None or rid in runs) and (levels is None or levels[0] <= int(lv) <= levels[1]):
            rows.append((int(lv), rid, folder, [o.split('=', 1)[0] for o in outs.split(';')], cmd))
    env = dict(os.environ, OMP_NUM_THREADS='1', OPENBLAS_NUM_THREADS='1', MKL_NUM_THREADS='1')
    npass = nfail = 0
    for lv, rid, folder, outs, cmd in sorted(rows):
        moved = []
        try:
            for p in outs:
                q = os.path.join(ROOT, p)
                if os.path.exists(q):
                    os.rename(q, q + '.shipped')
                    moved.append(q)
                else:
                    print('  FAIL %s: the package holds no copy of this output' % p)
                    nfail += 1
            r = subprocess.run(['sh', '-c', cmd], cwd=os.path.join(ROOT, folder), env=env, stdout=subprocess.PIPE,
                               stderr=subprocess.STDOUT)
            print('run %s (level %d) exit %d' % (rid, lv, r.returncode), flush=True)
            new = {q: open(q, 'rb').read() for q in moved if os.path.exists(q)}
            old = {q: open(q + '.shipped', 'rb').read() for q in moved}
            pairs = [(sha(old[q]), sha(new[q])) for q in moved if q in new]
            for q in moved:
                bad = ['no new output'] if q not in new else compare(new[q], old[q], pairs, os.path.relpath(q, ROOT))
                print('  %s %s%s' % ('PASS' if not bad else 'FAIL', os.path.relpath(q, ROOT), ''.join('\n    ' + x for x in bad[:3])))
                npass, nfail = npass + (not bad), nfail + bool(bad)
        finally:
            for q in moved:
                if os.path.exists(q):
                    os.rename(q, q + '.rerun')
                os.rename(q + '.shipped', q)
    print('TOTAL outputs %d, pass %d, fail %d' % (npass + nfail, npass, nfail))
    sys.exit(1 if nfail else 0)


if __name__ == '__main__':
    main()
