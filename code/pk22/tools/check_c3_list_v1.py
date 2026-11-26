#!/usr/bin/env python3
"""check_c3_list_v1.py (pk22): check_w1a_list_v1.py (pk22/tools, sha256 below in the job log) with the list path as its argument
(default pk22/m3/C3_ENTRY_LIST_v1.json). Reads the list and, with pk03's pinned m3_graph_v3 (loaded by file path, read
only), prints for each graph V, the edge count and F = V + pairs of GR.strip(columns), against the list's shape_V_edges_F, and the
pair forms that m3_entries_v3 gives the entries' factors (union per graph) against the list's pairs. Writes nothing."""
import hashlib, importlib.util, json, sys
CODEDIR = '/mnt/g2/release/root/code'
OWN = CODEDIR + '/pk03'
LF = sys.argv[1] if len(sys.argv) > 1 else CODEDIR + '/pk22/m3/C3_ENTRY_LIST_v1.json'


def load_as(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


for nm, fn in (('m3_scal', 'm3_scal_v2.py'), ('m3_graph', 'm3_graph_v3.py'), ('m3_series', 'm3_series_v2.py'), ('m3_entries', 'm3_entries_v3.py')):
    with open(OWN + '/' + fn, 'rb') as fh:
        print('MODULE %s %s' % (fn, hashlib.sha256(fh.read()).hexdigest()))
GR = sys.modules['m3_graph'] if 'm3_graph' in sys.modules else None
import importlib
MODS = {}
for nm, fn in (('m3_scal', 'm3_scal_v2.py'), ('m3_graph', 'm3_graph_v3.py'), ('m3_series', 'm3_series_v2.py'), ('m3_entries', 'm3_entries_v3.py')):
    MODS[nm] = load_as(nm, OWN + '/' + fn)
GR, ENT = MODS['m3_graph'], MODS['m3_entries']
with open(LF, 'rb') as fh:
    b = fh.read()
print('LIST %s %s' % (hashlib.sha256(b).hexdigest(), LF))
L = json.loads(b)


class TS0:
    """a stand-in trial set for pairs_of only: cp a >= 1 gets a c9 with every BASIS9 coefficient nonzero, as the real states have."""
    S = [[1.0] * 10 for _ in range(10)]
    q = ([1.0] * 9, [1.0] * 9, [1.0] * 9)
    kbar = 0.0

    def pv(self, col):
        return ('p', tuple(col), list(self.q[0]), list(self.q[1]), list(self.q[2]))

    def cp(self, a, col):
        return self.pv(col) if a == 0 else ('xi', tuple(col), 1.0, [1.0] * 9)


ts = TS0()
bad = 0
for g, spec in L['graphs'].items():
    V, E = GR.strip(spec['columns'])
    want = sorted(tuple(sorted(p)) for p in spec['pairs'])
    used = set()
    for e in L['entries']:
        if e['graph'] == g:
            for enc in e['factors']:
                used |= {tuple(sorted(p)) for p in ENT.pairs_of(ENT.factor(ts, 'N', enc))}
    got = (V, len(E), V + len(want))
    ok = list(got) == spec['shape_V_edges_F'] and sorted(used) == want
    bad += 0 if ok else 1
    print('GRAPH %s columns %s: V %d, edges %d, F %d (list %s); entry pairs %s, list pairs %s -> %s' % (
        g, spec['columns'], V, len(E), V + len(want), spec['shape_V_edges_F'], sorted(used), want, 'OK' if ok else 'MISMATCH'))
print('CHECK %s' % ('ALL OK' if not bad else '%d MISMATCH' % bad))
