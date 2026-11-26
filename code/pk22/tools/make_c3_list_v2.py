#!/usr/bin/env python3
"""make_c3_list_v2.py (pk22, phase (iii)): writes pk22/m3/C3_ENTRY_LIST_v2.json, the M3 entry list of
runner c3 and of the float twin m3ref_px22_v1_4, with one family per vertex graph, so that each graph's prep (certified, and the twin's
float probe) runs once. REVISION of make_c3_list_v1.py (pk22/tools, its list C3_ENTRY_LIST_v1.json never used): the same 56
entries and factors, regrouped, with keys unique across the list.
- CS4 on S4's vertex graph [free, int, int, free] (pairs (0,3), (1,2), (4,5), (6,9), (7,8), (10,11)):
  T1MN's Z, x, xr, xx (copied from pk22/m3/B_ENTRY_LIST_v1.json, read only, sha256 643e00ad...), and W1a's joint Gram windows at
  pJ = 2 (W1_DESIGN_v3 sect. 7): orbit A (representative (b2, t1)) as A.JJ, A.Jx, A.Jy, A.Jl, A.xy, A.yy, A.yl and the control A.Jxr;
  orbit D ((b1, t1)) as D.*. In the doubled window the left half is the vector at half-bond 2 and the right half its mirror: t1 is xi
  on (0,3), mirrored (6,9); b2 is xi on (4,5), mirrored (7,8); b1 is xi on (1,2), mirrored (10,11). J_A = (t1, b2), J_D = (b1, t1),
  x = the t1 vector, y_A = the b2 vector, y_D = the b1 vector, l = the plain state; <x, x>, <x, l>, <l, l> are xx, x, Z.
- CE3 on E3T's vertex graph [vac, int, free] (pairs (0,1), (0,2), (1,2), (0,3), (3,6), (4,5), (7,8)): E3T's fT,a and fT2,a
  (copied), and the trial components at half-bond 2: A.J,a = <s_a, J_A>, A.y,a = <s_a, y_A>, D.J,a, D.y,a (a = 0..3); the free
  column is the strip's column 1 and the int column its column 2, so t1 is xi on (3,6), b2 xi on (4,5), b1 xi on (7,8).
- H4T and E2T: copied from the B list (NE's hT,a, hT1,a and the controls eT,a).
Every xi factor is m3_entries_v3's xia on the triple (u, v, v); every cp factor is [cp, a, 0] on the vac column 0. No entry is a parity
zero (no factor set is T <-> B symmetric). shape_V_edges_F follows m3_graph_v3.strip with F = V + pairs; check_c3_list_v1.py verifies
shapes and pairs with the pinned modules. Asserts: each xia pair lies in its graph's pairs and vertex range; each cp column is vac;
keys unique; the counts. Writes one new file (mode 'x'). Usage: make_c3_list_v2.py."""
import hashlib, json, os
CODEDIR = '/mnt/g2/release/root/code'
SRC = CODEDIR + '/pk22/m3/B_ENTRY_LIST_v1.json'
DST = CODEDIR + '/pk22/m3/C3_ENTRY_LIST_v2.json'
assert os.path.dirname(DST) == CODEDIR + '/pk22/m3' and not os.path.exists(DST), DST
with open(SRC, 'rb') as fh:
    raw = fh.read()
ssha = hashlib.sha256(raw).hexdigest()
assert ssha.startswith('efc0b7cb'), ssha
with open(__file__, 'rb') as fh:
    msha = hashlib.sha256(fh.read()).hexdigest()
blist = json.loads(raw)


def edges_of(cols):
    ne = 0
    for j, ty in enumerate(cols):
        ne += 3 if ty == 'vac' else 2
        if j < len(cols) - 1:
            ne += 3
    return ne


VAC = [[0, 1], [0, 2], [1, 2]]
graphs = {'CS4': {'columns': ['free', 'int', 'int', 'free'], 'pairs': [[0, 3], [1, 2], [4, 5], [6, 9], [7, 8], [10, 11]]},
          'CE3': {'columns': ['vac', 'int', 'free'], 'pairs': VAC + [[0, 3], [3, 6], [4, 5], [7, 8]]},
          'H4T': {'columns': list(blist['graphs']['H4T']['columns']), 'pairs': [list(p) for p in blist['graphs']['H4T']['pairs']]},
          'E2T': {'columns': list(blist['graphs']['E2T']['columns']), 'pairs': [list(p) for p in blist['graphs']['E2T']['pairs']]}}
for g, spec in graphs.items():
    V = 3 * len(spec['columns'])
    spec['shape_V_edges_F'] = [V, edges_of(spec['columns']), V + len(spec['pairs'])]


def xa(u, v):
    return ['xia', [u, v, v]]


MOVE = {'T1MN': 'CS4', 'E3T': 'CE3', 'H4T': 'H4T', 'E2T': 'E2T'}
entries = []
for e in blist['entries']:
    if e['graph'] in MOVE:
        d = dict(e)
        d['graph'] = MOVE[e['graph']]
        d['b_list_graph'] = e['graph']
        entries.append(d)
NOTE = {'A': {'JJ': 'the moved joint norm <J_A, J_A>, J_A = (t1, b2) at half-bond 2: [free -xi_t- int(X_b) -K- int(X_b) -xi_t- free]',
              'Jx': '<J_A, x>, x = the t1 vector', 'Jy': '<J_A, y_A>, y_A = the b2 vector', 'Jl': '<J_A, l>, l the plain state',
              'xy': '<x, y_A>', 'yy': '<y_A, y_A> (S8 list: S4,xy,1,MB,2,MB)', 'yl': '<y_A, l> (S8 list: S4,x,1,MB)',
              'Jxr': 'the mirror of A.Jx (control: equal to A.Jx by the window\'s reflection)'},
        'D': {'JJ': 'the moved joint norm <J_D, J_D>, J_D = (b1, t1) at half-bond 2: [free(X_b) -xi_t- int -K- int -xi_t- free(X_b)]',
              'Jx': '<J_D, x>, x = the t1 vector', 'Jy': '<J_D, y_D>, y_D = the b1 vector', 'Jl': '<J_D, l>, l the plain state',
              'xy': '<x, y_D>', 'yy': '<y_D, y_D> (S8 list: S4,xy,0,MB,3,MB)', 'yl': '<y_D, l> (S8 list: S4,x,0,MB)',
              'Jxr': 'the mirror of D.Jx (control: equal to D.Jx by the window\'s reflection)'}}
t1, t1m = xa(0, 3), xa(6, 9)
for o, b, bm in (('A', xa(4, 5), xa(7, 8)), ('D', xa(1, 2), xa(10, 11))):
    fac = {'JJ': [b, t1, t1m, bm], 'Jx': [b, t1, t1m], 'Jy': [b, t1, bm], 'Jl': [b, t1], 'xy': [t1, bm], 'yy': [b, bm], 'yl': [b],
           'Jxr': [t1, bm, t1m]}
    for key in ('JJ', 'Jx', 'Jy', 'Jl', 'xy', 'yy', 'yl', 'Jxr'):
        entries.append({'key': '%s.%s' % (o, key), 'graph': 'CS4', 'factors': fac[key], 'parity_zero': False,
                        'role': 'control' if key == 'Jxr' else 'chain', 'note': NOTE[o][key]})
for o, bv, lab in (('A', xa(4, 5), 'b2'), ('D', xa(7, 8), 'b1')):
    for a in range(4):
        entries.append({'key': '%s.J,%d' % (o, a), 'graph': 'CE3', 'factors': [['cp', a, 0], xa(3, 6), bv], 'parity_zero': False,
                        'role': 'chain', 'K': 3, 'note': '<s_%d, J_%s> at half-bond 2, J_%s = (t1, %s)' % (a, o, o, lab)})
        entries.append({'key': '%s.y,%d' % (o, a), 'graph': 'CE3', 'factors': [['cp', a, 0], bv], 'parity_zero': False, 'role': 'chain',
                        'K': 3, 'note': '<s_%d, y_%s> at half-bond 2, y_%s = the %s vector' % (a, o, o, lab)})
# checks
for e in entries:
    gs = graphs[e['graph']]
    nv = 3 * len(gs['columns'])
    prs = {tuple(sorted(p)) for p in gs['pairs']}
    for f in e['factors']:
        if f[0] == 'xia':
            u, v, w = f[1]
            assert v == w and 0 <= u < nv and 0 <= v < nv and tuple(sorted((u, v))) in prs, (e['graph'], e['key'], f)
        else:
            assert f[0] == 'cp' and gs['columns'][f[2]] == 'vac', (e['graph'], e['key'], f)
keys = [e['key'] for e in entries]
assert len(keys) == len(set(keys)), 'duplicate keys'
cnt = {}
for e in entries:
    cnt[e['graph']] = cnt.get(e['graph'], 0) + 1
assert cnt == {'CS4': 20, 'CE3': 24, 'H4T': 8, 'E2T': 4}, cnt
out = {'list': 'C3_ENTRY_LIST_v2', 'author': 'pk22', 'source': {'B_ENTRY_LIST_v1.json': ssha, 'make_c3_list_v2.py': msha},
       'purpose': "runner c3's and twin m3ref_px22_v1_4's M3 entries, one family per vertex graph: CS4 (T1MN and W1a's "
                  "joint Gram windows JA, JD at pJ = 2), CE3 (E3T's fT entries and the joint windows' trial components), H4T and E2T "
                  "(NE's one-vac chain entries and controls); no L, N2T, D2T",
       'conventions': dict(blist['conventions'], joint='CS4: the left half of the doubled window is the vector at half-bond 2, the right half '
                           'its mirror; CE3: E3T\'s columns, the free column is the strip\'s column 1; keys unique across the list'),
       'counts': cnt, 'graphs': graphs, 'entries': entries}
b = (json.dumps(out, indent=1, sort_keys=True) + '\n').encode('utf-8')
with open(DST, 'xb') as fh:
    fh.write(b)
print('SOURCE %s %s' % (ssha, SRC))
print('MAKER %s' % msha)
print('LIST %s %s: %d entries %s; shapes %s' % (hashlib.sha256(b).hexdigest(), DST, len(entries), cnt,
                                                {g: s['shape_V_edges_F'] for g, s in sorted(graphs.items())}))
