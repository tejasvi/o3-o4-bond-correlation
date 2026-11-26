#!/usr/bin/env python3
"""nerec2lean_v1_1.py (read-only; v1 with the PAIRMAP class count assert fixed): turns NE's certified RC record (NE_RC_RECORD_v1 key-value file) into Lean terms for
StripIII.NECheck: per N, the class keys of its COVER rows (each must read "pieces X of X"), the separated rows of its PAIRMAP (the record's
n = 5 pairs with their class keys, m dropped; names t_i, bb_i, a_j, b_j are 1-based: t_i = hor 0 (i-1), bb_i = hor 2 (i-1), a_j = ver 0 (j-1),
b_j = ver 1 (j-1)), and the C-COVER-LIST parameters as Lean functions. It asserts the record's gates (C-COVER-LIST and C-PAIRMAP PASS, the
counts they state), that DN, NEAR_H and NEAR_V are contiguous ranges (DN from 0, NEAR_H = 0..T_M, NEAR_V = -1..T_M - 1) and that the far
thresholds start right after them (DF = max DN + 1, DF_H = T_M + 1, DF_V = T_M), so near and far leave no gap. Usage: nerec2lean_v1_1.py RECORD"""
import ast
import hashlib
import re
import sys


def code(name):
    m = re.fullmatch(r'(t|bb|a|b)(\d+)', name)
    assert m, name
    i = int(m.group(2)) - 1
    assert i >= 0, name
    return {'t': '.hor 0 %d', 'bb': '.hor 2 %d', 'a': '.ver 0 %d', 'b': '.ver 1 %d'}[m.group(1)] % i


def ival(x):
    return '(%d)' % x if x < 0 else '%d' % x


def key(t):
    k = t[-1]
    assert k in ('flip', 'same'), t
    if t[0] == 'H2':
        assert len(t) == 4
        return '.H2 %d %d .%s' % (t[1], t[2], k)
    if t[0] in ('Hinf', 'H1'):
        assert len(t) == 4 and t[2] == {'Hinf': 'inf', 'H1': 'far'}[t[0]], t
        return '.%s %d .%s' % (t[0], t[1], k)
    if t[0] == 'M2':
        assert len(t) == 5 and t[1] == 'HV', t
        return '.M2 %d %s .%s' % (t[2], ival(t[3]), k)
    if t[0] in ('Minf', 'M1'):
        assert len(t) == 5 and t[1] in ('HV', 'VH') and t[3] == {'Minf': 'inf', 'M1': 'far'}[t[0]], t
        return '.%s%s %s .%s' % (t[0], t[1], ival(t[2]) if t[1] == 'VH' else '%d' % t[2], k)
    raise AssertionError(t)


def main():
    path = sys.argv[1]
    with open(path, 'rb') as fh:
        raw = fh.read()
    kv = {}
    for ln in raw.decode('utf-8').splitlines():
        if ln.startswith('#') or not ln.strip():
            continue
        k, v = ln.split(' = ', 1)
        assert k not in kv, k
        kv[k] = v
    assert kv['EXPORT_STATUS'] == 'CERTIFIED' and kv['RECORD'] == 'NE_RC_RECORD_v1'
    print('-- source %s sha256 %s; %s' % (path, hashlib.sha256(raw).hexdigest(), kv['CODE']))
    par = {}
    for N in (4, 3):
        cl = kv['N%d_COVERLIST_001' % N]
        m = re.fullmatch(r"C-COVER-LIST N=%d: (\d+) class keys \(DN (\{.*?\}), NEAR_H (\(.*?\)), NEAR_V (\(.*?\)), T_M (\d+), DF (\{.*?\}), "
                         r"DF_V (\d+), DF_H (\d+), MM (\d+)\), each with an m0 on every piece of \[\d+, \d+\): short none -> PASS" % N, cl)
        assert m, cl
        nk, DN, NH, NV, TM, DF, DFV, DFH = (int(m.group(1)), ast.literal_eval(m.group(2)), ast.literal_eval(m.group(3)),
                                             ast.literal_eval(m.group(4)), int(m.group(5)), ast.literal_eval(m.group(6)),
                                             int(m.group(7)), int(m.group(8)))
        for k in ('flip', 'same'):
            assert tuple(DN[k]) == tuple(range(max(DN[k]) + 1)) and DF[k] == max(DN[k]) + 1, (N, k)
        assert tuple(NH) == tuple(range(TM + 1)) and tuple(NV) == tuple(range(-1, TM)) and DFH == TM + 1 and DFV == TM, N
        par[N] = (DN, TM, DF, DFV, DFH)
        print('-- %s' % cl)
        keys = []
        i = 1
        while 'N%d_COVER_%03d' % (N, i) in kv:
            f = kv['N%d_COVER_%03d' % (N, i)].split(' | ')
            assert f[0] == 'COVER N=%d' % N, f
            mm = re.fullmatch(r'pieces (\d+) of (\d+)', f[2])
            assert mm and mm.group(1) == mm.group(2), f
            keys.append(key(ast.literal_eval(f[1])))
            i += 1
        assert len(keys) == nk and len(set(keys)) == nk, (N, len(keys))
        print('def recKeys%d : List NEKey := [' % N)
        print(',\n'.join('  ' + x for x in keys))
        print(']')
        g = kv['N%d_PAIRMAPGATE_001' % N]
        mg = re.fullmatch(r'C-PAIRMAP N=%d: (\d+) pairs, (\d+) separated with an n = 5 class \(each class with a row\), (\d+) joint; '
                          r'pairs without an image or a row none -> PASS' % N, g)
        assert mg, g
        rows = []
        njoint = 0
        i = 1
        while 'N%d_PAIRMAP_%03d' % (N, i) in kv:
            f = kv['N%d_PAIRMAP_%03d' % (N, i)].split(' | ')
            assert f[0] == 'PAIRMAP N=%d' % N, f
            if f[-1] == 'joint (no chain class)':
                njoint += 1
            else:
                cls = re.findall(r'(H2|M2) (\([^)]*\)) [\d.]+ at piece \d+', f[-1])
                assert cls and len(cls) == len(f[-1].split('; ')), f
                ks = []
                for name, tup in cls:
                    t = ast.literal_eval(tup)
                    ks.append(key((name,) + tuple(t[:-1])))
                e, ff = f[1].split(',')
                rows.append('(%s, %s, [%s])' % (code(e), code(ff), ', '.join(ks)))
            i += 1
        assert len(rows) == int(mg.group(2)) and njoint == int(mg.group(3)) and len(rows) + njoint == int(mg.group(1)), N
        print('-- %s' % g)
        print('def pairMap%d : List (ECode × ECode × List NEKey) := [' % N)
        print(',\n'.join('  ' + x for x in rows))
        print(']')
    DN, TM4, DF, DFV4, DFH4 = par[4]
    DN3, TM3, DF3, DFV3, DFH3 = par[3]
    assert DN == DN3 and DF == DF3
    print('/-- the record\'s C-COVER-LIST parameters: max DN per kind (DN = 0..max), T_M (NEAR_H = 0..T_M, NEAR_V = -1..T_M - 1), DF = max DN + 1, '
          'DF_H = T_M + 1, DF_V = T_M -/')
    print('def recDNmax : RK → Nat\n  | .flip => %d\n  | .same => %d' % (max(DN['flip']), max(DN['same'])))
    print('def recTM (N : Nat) : Nat := if N == 4 then %d else %d' % (TM4, TM3))


if __name__ == '__main__':
    main()
