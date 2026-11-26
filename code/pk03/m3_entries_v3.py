#!/usr/bin/env python3
"""m3_entries_v3.py -- pk03 (code/pk03/). Entry specs made concrete. REVISION of m3_entries_v2.py (833e0cda) for M2's vacuum entries
(PLAN_M3_CODE_v1_2_ADD6 sect. 2): graph_edges takes 'G4-r0', 'G4-r1' and 'G4-r2', G4 = strip(vac, int, int, vac) without the horizontal bond (r, 3 + r)
(m3_graph's minus; vacmono l.144-146, M3_ENTRY_LIST_v1_2's graph G4-r). Everything else is v2's.
m3_entries_v2: Entry specs of M3_ENTRY_LIST_v1_1.json (and S8_ENTRY_LIST_v1_1.json) made concrete:
REVISION of m3_entries_v1.py (abcfa5d8): imports the generic module names (m3_scal, m3_graph, m3_series, m3_major), which the job scripts load from sha-pinned files;
no other change.
riglap factor tuples from the run's trial set, the graph of each family with the union of the pair forms its entries use, and the exact
symmetry checks behind parity zeros (C-ODD) and mirror aliases (C-MIRROR). No compute of its own.
Factor encodings (list conventions): [pv, col], [cp, a, col], [delta, col], [xia, col], [xip, col], [wt, col]; col is a column name of the
graph (L, M, R) or an explicit triple; S8's list: [cp, a, c] and [xi, TM|MB, c] with a column index c.
"""
import json
import m3_graph as G
from m3_series import BASIS9

COLS = {'D': {'L': (0, 1, 2), 'R': (3, 4, 5)}, 'N': {'L': (0, 1, 2), 'M': (3, 4, 5), 'R': (6, 7, 8)},
        'E3': {'L': (0, 1, 2), 'M': (3, 4, 5), 'R': (6, 7, 8)}, 'mix': {'L': (0, 1, 2), 'R': (3, 4, 5)},
        'free2': {'L': (0, 1, 2), 'R': (3, 4, 5)}}
PERM9 = [1, 0, 2, 4, 3, 5, 6, 8, 7]      # BASIS9 under xi_0 <-> xi_1 (T <-> B in a column): (0,)<->(1,), (0,0)<->(1,1), (1,2)<->(0,2)


class TrialSet:
    """S (10 x 10, columns = states), q1, q2, q3 of vacres, kbar (exact binary64)."""
    def __init__(self, S, q, kbar):
        self.S, self.q, self.kbar = S, q, kbar

    def pv(self, col):
        return ('p', tuple(col), list(self.q[0]), list(self.q[1]), list(self.q[2]))

    def cp(self, a, col):
        if a == 0:
            return self.pv(col)
        return ('xi', tuple(col), float(self.S[0][a]), [float(self.S[r][a]) for r in range(1, 10)])


def load_trial(ts_path, vac_path, kbar):
    with open(ts_path) as fh:
        S = json.load(fh)['S']
    with open(vac_path) as fh:
        V = json.load(fh)
    return TrialSet(S, (V['q1'], V['q2'], V['q3']), float(kbar))


def col_of(graph, c):
    if isinstance(c, str):
        return COLS[graph][c]
    if isinstance(c, int):
        return (3 * c, 3 * c + 1, 3 * c + 2)
    return tuple(c)


def factor(ts, graph, enc):
    """one riglap factor tuple from a list encoding."""
    k = enc[0]
    if k == 'pv':
        return ts.pv(col_of(graph, enc[1]))
    if k == 'cp':
        return ts.cp(enc[1], col_of(graph, enc[2]))
    if k == 'xi' and enc[1] in ('TM', 'MB'):
        c9 = [1.0 if (enc[1] == 'TM' and i == 0) or (enc[1] == 'MB' and i == 1) else 0.0 for i in range(9)]
        return ('xi', col_of(graph, enc[2]), 0.0, c9)
    col = col_of(graph, enc[1])
    if k == 'delta':
        return ('xi', col, 0.0, [0.5, -0.5] + [0.0] * 7)
    if k == 'xia':
        return ('xi', col, 0.0, [1.0] + [0.0] * 8)
    if k == 'xip':
        return ('xi', col, 0.0, [0.5, 0.5] + [0.0] * 7)
    if k == 'wt':
        return ('xi', col, -ts.kbar, [0.5, 0.5] + [0.0] * 7)
    raise ValueError('factor encoding %r' % (enc,))


def pairs_of(f):
    """the pair forms a factor uses (riglap3: 'p' all three of its triple; 'xi' those with a nonzero c9 coefficient)."""
    T, M, B = f[1]
    prs = [(T, M), (M, B), (T, B)]
    if f[0] == 'p':
        return set(prs)
    if f[0] == 'xi':
        return {prs[p_] for cb, mono in zip(f[3], BASIS9) if cb != 0.0 for p_ in mono}
    return set()


def graph_edges(graph, N):
    if graph == 'D':
        return G.strip(['vac', 'vac'])
    if graph == 'N':
        return G.strip(['vac', 'int', 'vac'])
    if graph == 'E3':
        return G.strip(['vac', 'int', 'free'])
    if graph == 'mix':
        return G.endw_mix()
    if graph == 'free2':
        return G.endw_free()
    if graph == 'G4':
        return G.strip(['vac', 'int', 'int', 'vac'])
    if graph in ('G4-r0', 'G4-r1', 'G4-r2'):
        r = int(graph[-1])
        V, E = G.strip(['vac', 'int', 'int', 'vac'])
        return G.minus(V, E, (r, 3 + r))
    raise ValueError('graph %r' % graph)


def build_graph(graph, N, factor_lists):
    """GraphIV of a family with the union (sorted) of the pair forms of the given factor lists."""
    V, E = graph_edges(graph, N)
    prs = set()
    for fl in factor_lists:
        for f in fl:
            prs |= {tuple(sorted(p)) for p in pairs_of(f)}
    return G.GraphIV(V, E, sorted(prs), N)


# ------------------------------------------------------------------ exact symmetry checks
def sigma(v):
    """T <-> B in every column: 3c + r -> 3c + (2 - r)."""
    return 3 * (v // 3) + (2 - v % 3)


def mirror(v, ncols):
    """left-right reflection: column c -> ncols - 1 - c, rows kept."""
    return 3 * (ncols - 1 - v // 3) + v % 3


def edges_map_onto(E, fmap):
    """True if the vertex map sends the edge list onto itself with identical coupling tags."""
    d = {frozenset(e): t for e, t in E}
    return all(d.get(frozenset((fmap(u), fmap(v)))) == t for (u, v), t in E) and len(d) == len(E)


def parity_class(f):
    """'even', 'odd' or None for a factor on a column triple under T <-> B (exact comparisons of binary64 coefficients)."""
    T, M, B = f[1]
    if not (M == T + 1 and B == T + 2 and T % 3 == 0):
        return None
    if f[0] == 'p':
        ok = all(q[PERM9[i]] == q[i] for q in f[2:5] for i in range(9))
        return 'even' if ok else None
    if f[0] == 'xi':
        c0, c9 = f[2], f[3]
        if all(c9[PERM9[i]] == c9[i] for i in range(9)):
            return 'even'
        if c0 == 0.0 and all(c9[PERM9[i]] == -c9[i] for i in range(9)):
            return 'odd'
    return None


def c_odd(graph, N, factors):
    """C-ODD (PLAN_M3_CODE_v1 sect. 3): (i) sigma is an automorphism of the coupling list; (ii) every factor is exactly even or odd and
    exactly one is odd. Returns (ok, reason)."""
    V, E = graph_edges(graph, N)
    if not edges_map_onto(E, sigma):
        return False, 'T <-> B is not an automorphism of the couplings'
    cls = [parity_class(f) for f in factors]
    if any(c is None for c in cls):
        return False, 'a factor is neither exactly even nor exactly odd: %s' % cls
    if cls.count('odd') != 1:
        return False, '%d odd factors' % cls.count('odd')
    return True, 'one exactly odd factor, the rest exactly even, T <-> B an automorphism'


def map_factor(f, fmap):
    return (f[0], tuple(fmap(v) for v in f[1])) + tuple(f[2:])


def c_mirror(graph, N, factors_alias, factors_target):
    """C-MIRROR: the mirror is an automorphism of the couplings and maps the alias's factor list onto the target's (as multisets)."""
    V, E = graph_edges(graph, N)
    nc = V // 3
    fm = lambda v: mirror(v, nc)
    if not edges_map_onto(E, fm):
        return False, 'the mirror is not an automorphism of the couplings'
    img = sorted(repr(map_factor(f, fm)) for f in factors_alias)
    tgt = sorted(repr(f) for f in factors_target)
    return (img == tgt), ('factor lists map exactly' if img == tgt else 'factor lists differ under the mirror')
