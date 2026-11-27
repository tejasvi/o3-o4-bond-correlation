#!/usr/bin/env python3
"""cmp_certified.py: the comparison of the rerun outputs with the certified outputs, repeatable from the archive alone.

Each row of CERT_PAIRS_release_N.tsv names an output of a run of RUNS_M2_release_N.tsv (the path of Table A.1), the file the run writes
(the same path, or the code path whose copy is the record), the certified output with the neutral names of T applied (under
records/original_T), the sha256 and size of the archived original and the archived sha256 of the written file. The output is compared
line by line with its certified form (same line count required); a differing line pair passes only as:
  time      equal after masking timing and memory fields (CPU, elapsed, wall, RSS, peak memory, seconds) and UTC time stamps;
  mapped    equal outside hex tokens (8 to 64 hex digits), each differing (certified, output) token pair being a pair of the P map
            P_MAP_release_N.tsv (archived sha256 of a package file and the sha256 of the shipped file, or same-length prefixes),
            or (archived sha256 of a certified output, or sha256 of its certified form, sha256 of its output) for an output that passed in this run;
            'N bytes' passes when N is the archived size and the shipped size of a file mapped on the same line;
  recorded  a mask of CERT_MASKS_release_N.tsv (TIME and TAG fields of a family masked freely; COUNT with an exact delta; GPAIR: the
            original digest that G wrote into a changed gate, against the released 64-hex value);
  json      a line, or a whole output, that is a JSON value on both sides, compared value by value with the same rules for strings and
            the time rule for numbers under CPU or time keys;
  resorted  a line whose fields (split at ' ; ', '; ' or ', '), or a block of consecutive lines, match the certified ones one to one
            in another order, the output's order being sorted (a program that sorts by names that T renamed); also a block of lines
            NAME_NN = VALUE with the same keys on both sides whose values match one to one, sorted on the output side (a program
            that numbers its entries in that sorted order);
  self-hash a line 'END <sha256>' whose value on the output side is the sha256 of the output's own body (the second line, or every
            line before END);
  run folder a line that names the run's record folder, which the certified run wrote as pkNN/<folder> and a rerun writes as
            <folder>.rerun, equal under the rules above once the leading pkNN/ and the trailing .rerun are taken away.
The certified forms carry T and neither G nor P, and the archived originals do not ship, so two rules check one side only: for resorted
fields and blocks the order of the certified original is not checked, and for a self-hash line only the output's value is checked;
their passes are counted apart. Outputs are retried until no new pass, since an output may print the sha256 of another output.

usage: python3 -I -B cmp_certified.py [--rerun] [--images ROOT[:ROOT...]] REPORT
  without --rerun the shipped outputs are compared (each is itself the output of a rerun on a copy of the archive);
  with --rerun the files <written file>.rerun that rerun_m2.py leaves are compared;
  --images: folders searched before the package root for the certified forms; --pkg: the folder of the outputs; --tables: the folder
  of the three tables (both default to the folder of this program; the three options serve staging only).
Writes REPORT (a new file) and prints the totals; exit status 1 if any output fails."""
import sys, os, re, json, fnmatch, hashlib, collections

HEX = re.compile(r'(?<![0-9A-Za-z_])[0-9a-f]{8,64}(?![0-9A-Za-z_])')
TIME_RX = [
    (re.compile(r'\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d(?:\.\d+)?Z'), '<TS>'),
    (re.compile(r'\[cpu\s+[0-9.]+s\]'), '[cpu <T>s]'),
    (re.compile(r'(STAGE-CPU\b.*?\s)([0-9]+(?:\.[0-9]+)?)(\s*s\b)'), r'\1<T>\3'),
    (re.compile(r'(?i)\b(cpu|elapsed|wall|maxrss_kb|maxrss|rss|peak resident memory|peak|seconds|time)(\s*[=:]?\s*)([0-9]+(?:\.[0-9]+)?)'),
     r'\1\2<T>'),
    (re.compile(r'(?<![0-9A-Za-z_.])[0-9]+\.[0-9]+(\s?s\b)'), r'<T>\1'),
]
SEPS = (' ; ', '; ', ', ')
TIME_KEY = re.compile(r'(?i)(cpu|elapsed|wall|rss|time|utc|seconds)')
SIZE = re.compile(r'(?<![0-9A-Za-z_.])([0-9]+) bytes\b')
END_RX = re.compile(r'^END ([0-9a-f]{64})$')


def sha(b):
    return hashlib.sha256(b).hexdigest()


def norm(s):
    for rx, rep in TIME_RX:
        s = rx.sub(rep, s)
    return s


class Pairs:
    def __init__(self):
        self.full = collections.defaultdict(set)
        self.kind = {}
        self.pref = {}
        self.size = {}

    def add(self, a, b, kind, sizes=None):
        if a != b:
            self.full[a].add(b)
            self.kind[(a, b)] = kind
            self.pref = {}
            if sizes:
                self.size[(a, b)] = sizes

    def ok(self, a, b):
        if len(a) == 64:
            return self.kind.get((a, b)) if b in self.full.get(a, ()) else None
        k = len(a)
        if k not in self.pref:
            d = collections.defaultdict(set)
            for x, ys in self.full.items():
                for y in ys:
                    d[x[:k]].add((y[:k], self.kind[(x, y)]))
            self.pref[k] = d
        for y, kind in self.pref[k].get(a, ()):
            if y == b:
                return kind + '-prefix'
        return None


def cmp_str(a, b, pairs, masks, cnt, path):
    if a == b:
        return True
    ms = [m for m in masks if fnmatch.fnmatch(path, m[1])]
    a0, b0 = a, b
    for kind, glob, rx, delta in ms:
        if kind in ('TIME', 'TAG'):
            a, b = rx.sub('<T>', a), rx.sub('<T>', b)
    na, nb = norm(a), norm(b)
    if na == nb:
        cnt['time'] += 1
        return True
    sa, sb = SIZE.findall(na), SIZE.findall(nb)
    if len(sa) == len(sb) and sa != sb:
        na, nb = SIZE.sub('<SZ> bytes', na), SIZE.sub('<SZ> bytes', nb)
    else:
        sa = sb = []
    if HEX.split(na) == HEX.split(nb):
        ha, hb = HEX.findall(na), HEX.findall(nb)
        kinds, mapped = [], []
        for x, y in zip(ha, hb):
            if x == y:
                continue
            k = pairs.ok(x, y) if len(x) == len(y) else None
            if k is None:
                kinds = None
                break
            kinds.append(k)
            mapped.append((x, y))
        if kinds is not None and all(u == v or any(pairs.size.get(xy) == (int(u), int(v)) for xy in mapped) for u, v in zip(sa, sb)):
            for k in kinds:
                cnt['mapped ' + k] += 1
            if sa != sb:
                cnt['mapped size'] += 1
            return True
    for kind, glob, rx, delta in ms:
        if kind not in ('COUNT', 'GPAIR'):
            continue
        ma, mb = rx.match(a0), rx.match(b0)
        same = ma and mb and a0[:ma.start(1)] == b0[:mb.start(1)] and a0[ma.end(1):] == b0[mb.end(1):]
        if same and kind == 'GPAIR' and ma.group(1) == delta and re.fullmatch('[0-9a-f]{64}', mb.group(1)):
            cnt['G pair'] += 1
            return True
        if same and kind == 'COUNT' and int(mb.group(1)) - int(ma.group(1)) == int(delta):
            cnt['recorded'] += 1
            return True
    return False


def cmp_json(x, y, pairs, masks, cnt, path, key=''):
    if type(x) != type(y):
        return False
    if isinstance(x, dict):
        return set(x) == set(y) and all(cmp_json(x[k], y[k], pairs, masks, cnt, path, k) for k in x)
    if isinstance(x, list):
        return len(x) == len(y) and all(cmp_json(u, v, pairs, masks, cnt, path, key) for u, v in zip(x, y))
    if isinstance(x, str):
        return cmp_str(x, y, pairs, masks, cnt, path)
    if x == y:
        return True
    if isinstance(x, (int, float)) and TIME_KEY.search(key):
        cnt['time'] += 1
        return True
    return False


def match_perm(xs, ys, pairs, masks, path):
    used = set()
    for x in xs:
        j = next((j for j, y in enumerate(ys) if j not in used and cmp_str(x, y, pairs, masks, collections.Counter(), path)), None)
        if j is None:
            return False
        used.add(j)
    return True


def resorted_line(x, y, pairs, masks, path):
    hx, hy = x.find(' = '), y.find(' = ')
    if hx >= 0 and hy >= 0 and x[:hx] == y[:hy]:
        x, y = x[hx + 3:], y[hy + 3:]
    for sep in SEPS:
        fx, fy = x.split(sep), y.split(sep)
        if len(fx) > 1 and len(fx) == len(fy) and fy == sorted(fy) and fx != fy and match_perm(fx, fy, pairs, masks, path):
            return True
    return False


def json_line(x, y, pairs, masks, cnt, path):
    try:
        jx, jy = json.loads(x), json.loads(y)
    except ValueError:
        return False
    if not isinstance(jx, (dict, list)):
        return False
    c2 = collections.Counter()
    if cmp_json(jx, jy, pairs, masks, c2, path):
        cnt.update(c2)
        return True
    return False


def self_hash(a, b, i):
    ma, mb = END_RX.match(a[i]), END_RX.match(b[i])
    if not (ma and mb):
        return False
    for body in ((b[1] if len(b) > 1 else None), '\n'.join(b[:i]) + '\n'):
        if body is not None and sha(body.encode('latin-1')) == mb.group(1):
            return True
    return False


FOLDER_RX = [(re.compile(r'(?<![A-Za-z0-9_./])pk[0-9]{2}/(?=[A-Za-z0-9_]+/)'), ''), (re.compile(r'\.rerun(?![A-Za-z0-9_])'), '')]


def run_folder(x, y, pairs, masks, cnt, path):
    """a line that names the run's record folder: the certified run wrote it as pkNN/<folder>, the rerun writes <folder>.rerun under
    the package's code folder; equal under the other rules once the leading pkNN/ and the trailing .rerun are taken away."""
    x2, y2 = x, y
    for rx, rep in FOLDER_RX:
        x2, y2 = rx.sub(rep, x2), rx.sub(rep, y2)
    if (x2, y2) == (x, y):
        return False
    c2 = collections.Counter()
    if cmp_str(x2, y2, pairs, masks, c2, path):
        cnt.update(c2)
        return True
    return False


KEYED = re.compile(r'^([A-Za-z][A-Za-z0-9]*_)([0-9]+)( = )(.*)$')


def renumbered(xs, ys, pairs, masks, path):
    """a block of lines NAME_NN = VALUE whose keys run the same on both sides and whose values, sorted on the output side, match the
    certified values one to one (a program that numbers its entries in the sorted order of names that T renamed)."""
    mx, my = [KEYED.match(x) for x in xs], [KEYED.match(y) for y in ys]
    if not all(mx) or not all(my):
        return False
    if [(m.group(1), m.group(2)) for m in mx] != [(m.group(1), m.group(2)) for m in my]:
        return False
    vy = [m.group(4) for m in my]
    return vy == sorted(vy) and match_perm([m.group(4) for m in mx], vy, pairs, masks, path)


def compare(old, new, pairs, masks, path):
    cnt = collections.Counter()
    if old == new:
        cnt['identical file'] = 1
        return True, cnt, []
    a, b = old.decode('latin-1').split('\n'), new.decode('latin-1').split('\n')
    fails = []
    if len(a) == len(b):
        bad = []
        for i, (x, y) in enumerate(zip(a, b)):
            if not cmp_str(x, y, pairs, masks, cnt, path):
                if run_folder(x, y, pairs, masks, cnt, path):
                    cnt['run folder'] += 1
                elif resorted_line(x, y, pairs, masks, path):
                    cnt['resorted fields (output order checked)'] += 1
                elif json_line(x, y, pairs, masks, cnt, path):
                    cnt['json line'] += 1
                elif self_hash(a, b, i):
                    cnt['self-hash (output side checked)'] += 1
                else:
                    bad.append(i)
        k = 0
        while k < len(bad):
            e = k
            while e + 1 < len(bad) and bad[e + 1] == bad[e] + 1:
                e += 1
            i0, i1 = bad[k], bad[e] + 1
            if i1 - i0 > 1 and b[i0:i1] == sorted(b[i0:i1]) and match_perm(a[i0:i1], b[i0:i1], pairs, masks, path):
                cnt['resorted lines (output order checked)'] += i1 - i0
            elif i1 - i0 > 1 and renumbered(a[i0:i1], b[i0:i1], pairs, masks, path):
                cnt['resorted lines with renumbered keys (output order checked)'] += i1 - i0
            else:
                fails += [(i + 1, a[i], b[i]) for i in range(i0, i1)]
            k = e + 1
        if not fails:
            return True, cnt, []
    else:
        fails.append((0, 'line count %d' % len(a), 'line count %d' % len(b)))
    try:
        jo, jn = json.loads(old), json.loads(new)
    except ValueError:
        return False, cnt, fails
    c2 = collections.Counter()
    if cmp_json(jo, jn, pairs, masks, c2, path):
        c2['json'] = 1
        return True, c2, []
    return False, cnt, fails


def rows(path):
    out = []
    for ln in open(path, encoding='utf-8'):
        if ln.startswith('#') or not ln.strip():
            continue
        out.append(ln.rstrip('\n').split('\t'))
    return out[1:]


def main():
    args = sys.argv[1:]
    rerun = '--rerun' in args
    args = [x for x in args if x != '--rerun']
    opt = {}
    for name in ('--images', '--pkg', '--tables'):
        if name in args:
            i = args.index(name)
            opt[name] = args[i + 1]
            args = args[:i] + args[i + 2:]
    if len(args) != 1:
        sys.exit(__doc__)
    report = os.path.abspath(args[0])
    if os.path.exists(report):
        sys.exit('REPORT must be a new file')
    here = os.path.dirname(os.path.abspath(__file__))
    pkg = opt.get('--pkg', here)
    tab = opt.get('--tables', here)
    roots = [x for x in opt.get('--images', '').split(':') if x]
    pairs = Pairs()
    for r in rows(os.path.join(tab, 'P_MAP_release_N.tsv')):
        osha, obytes, rsha, rbytes = r[0], r[1], r[3], r[4]
        pairs.add(osha, rsha, 'P', (int(obytes), int(rbytes)) if obytes.isdigit() and rbytes.isdigit() else None)
    masks = [(r[0], r[1], re.compile(r[2]), r[3]) for r in rows(os.path.join(tab, 'CERT_MASKS_release_N.tsv'))]
    todo = []
    for r in rows(os.path.join(tab, 'CERT_PAIRS_release_N.tsv')):
        out, prod, cert, osha, obytes, psha = r[0], r[1], r[2], r[3], r[4], r[5]
        src = os.path.join(pkg, prod + '.rerun') if rerun else os.path.join(pkg, out)
        img = next((os.path.join(x, cert) for x in roots + [pkg] if os.path.isfile(os.path.join(x, cert))), None)
        todo.append((out, cert, src, img, osha, int(obytes) if obytes.isdigit() else None, psha))
    results = {}
    changed = True
    while changed:
        changed = False
        for out, cert, src, img, osha, obytes, psha in todo:
            if results.get(out, (False,))[0]:
                continue
            if img is None or not os.path.isfile(src):
                results[out] = (False, collections.Counter(), [(0, 'certified form missing' if img is None else 'output missing', '')])
                continue
            new = open(src, 'rb').read()
            cert = open(img, 'rb').read()
            ok, cnt, fails = compare(cert, new, pairs, masks, out)
            results[out] = (ok, cnt, fails)
            if ok:
                for h in {osha, psha} - {'-'}:
                    pairs.add(h, sha(new), 'rerun', (obytes, len(new)) if obytes is not None else None)
                if sha(cert) not in (osha, psha):
                    pairs.add(sha(cert), sha(new), 'rerun', (len(cert), len(new)))
                changed = True
    lines, nbad, tot = [], 0, collections.Counter()
    for out, cert, src, img, osha, obytes, psha in todo:
        ok, cnt, fails = results[out]
        nbad += not ok
        tot.update(cnt)
        lines.append('%s %s <- %s | %s' % ('PASS' if ok else 'FAIL', out, cert, ' '.join('%s=%d' % kv for kv in sorted(cnt.items()))))
        for i, x, y in fails[:6]:
            lines.append('    l.%d certified: %s' % (i, x[:300]))
            lines.append('    l.%d output:    %s' % (i, y[:300]))
    lines.append('TOTAL outputs %d, pass %d, fail %d; %s' % (len(todo), len(todo) - nbad, nbad, ' '.join('%s=%d' % kv for kv in sorted(tot.items()))))
    with open(report, 'x') as f:
        f.write('\n'.join(lines) + '\n')
    print(lines[-1])
    sys.exit(1 if nbad else 0)


if __name__ == '__main__':
    main()
