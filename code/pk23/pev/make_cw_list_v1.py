#!/usr/bin/env python3
"""make_cw_list_v1.py (pk23, C_w variant B; the P0_LOG row 4589, pk25's D2_DESIGN_v1_3): writes pk23/pev/HL_CW_ENTRY_LIST_v1.json, the
entry list of the (1,1) block of |S M_c u~_x|^2 on the 4-column graph LC = S8's L [vac|int|int|vac] with the pairs (0,2), (9,11) (state 1's xi_TB
on each vac column) and the outer middle-row bonds (1,4), (7,10). Keys (b = b' = 1, e1 on both vac columns):
  Cxx,1,1 = <M_h psi_1, S^2 M_h psi_1>   (xi on (1,4) and on (7,10))
  Cx1,1,1 = <M_h psi_1, S^2 psi_1>       (xi on (1,4) only)
  C1x,1,1 = <psi_1, S^2 M_h psi_1>       (xi on (7,10) only; the mirror of Cx1,1,1, a control)
  C11,1,1 = <psi_1, S^2 psi_1>           (no insertion)
so that |S M_c psi_1|^2 = Cxx - c_h (Cx1 + C1x) + c_h^2 C11 with M_c = M_h - c_h. Graph L itself (S8's, the prep family) is listed for the prep and
C-RESTORE only; it has no entry here. The counts are computed from the entries. Usage: make_cw_list_v1.py (writes the list, mode x; prints its sha256)."""
import hashlib, json, os
HLD = '/mnt/g2/release/root/code/pk23/pev'
DST = os.path.join(HLD, 'HL_CW_ENTRY_LIST_v1.json')
assert os.path.dirname(os.path.abspath(DST)) == HLD and not os.path.exists(DST), DST
cols = ['vac', 'int', 'int', 'vac']
graphs = {
    'L': {'columns': cols, 'pairs': [[0, 1], [1, 2], [0, 2], [9, 10], [10, 11], [9, 11]], 'shape_V_edges_F': [12, 19, 18]},
    'LC': {'columns': cols, 'pairs': [[0, 2], [9, 11], [1, 4], [7, 10]], 'shape_V_edges_F': [12, 19, 16]},
}
X1, X2 = ['xia', [1, 4, 4]], ['xia', [7, 10, 10]]
P1L, P1R = ['cp', 1, 0], ['cp', 1, 3]
entries = []
for key, facs, role, note in (
        ('Cxx,1,1', [P1L, X1, X2, P1R], 'chain', '<M_h psi_1, S^2 M_h psi_1>: xi on the outer bonds (1,4) and (7,10)'),
        ('Cx1,1,1', [P1L, X1, P1R], 'chain', '<M_h psi_1, S^2 psi_1>: xi on (1,4), next to the left psi_1'),
        ('C1x,1,1', [P1L, X2, P1R], 'control', '<psi_1, S^2 M_h psi_1>: xi on (7,10); equal to Cx1,1,1 by the left-right reflection of LC'),
        ('C11,1,1', [P1L, P1R], 'chain', '<psi_1, S^2 psi_1>: no insertion (TT on states 1)')):
    entries.append({'key': key, 'graph': 'LC', 'factors': facs, 'grouping': 'split', 'parity_zero': False, 'K': 3, 'role': role, 'note': note})
counts = {}
for e in entries:
    counts[e['graph']] = counts.get(e['graph'], 0) + 1
doc = {'author': 'pk23',
       'conventions': {
           'task': "the P0_LOG row 4589 (C_w variant B, pk25's D2_DESIGN_v1_3): the new 4-column norms of |Q S M_c u~_x|^2, the (1,1) block only",
           'template': 'pk23/pev/HL_ENTRY_LIST_v1.json (0c4c72c2), the Pev list on the same L graph and prep',
           'cp': '[cp, a, col]: trial state a on the vac column col (a = 1: e1 = s1 = S01 + S31 xi_TB, pure mode 1 at t^0)',
           'xia': "[xia, [u, v, v]]: m3_entries_v3's xia factor, xi_uv = J(1 - sigma_u . sigma_v) on the pair (u, v)",
           'grouping': 'split (one group per factor, m3_bar_v11.split_groups), as the Pev list',
           'graph_L': "S8's L (pk11/out/S8_ENTRY_LIST_v2.json, graph L): the prep family (its certified D16 prep pieces Lp1.. of m3_run_v1_9_3_hl_v1); no entry here",
           'graph_LC': 'L with only the pairs its entries use: (0,2) and (9,11) (e1 uses xi_TB alone) and the outer middle-row bonds (1,4), (7,10); reads L\'s prep',
           'trial_set': "z9sym: pk11/out/ts_N4_J170_D_S_z9sym_v1.json (ea9d6c1b) and ts_N3_S_z9sym_v1.json (a298db65), pk25's mr/v3 TRIAL_SET",
           'vertex': '3*col + row (row 0 T, 1 M, 2 B); columns 0-indexed',
           'parity': 'state 1 is even (z9sym); the middle-row bonds map to themselves under T <-> B, so no entry is a parity zero'},
       'counts': counts, 'graphs': graphs, 'entries': entries}
text = json.dumps(doc, indent=1) + '\n'
with open(DST, 'x') as fh:
    fh.write(text)
print('LIST %s %s (%d entries)' % (hashlib.sha256(text.encode('utf-8')).hexdigest(), DST, len(entries)))
