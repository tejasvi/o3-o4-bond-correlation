#!/usr/bin/env python3
"""make_rcc_v1_5.py (pk22, phase (iii), NE's certified RC engine, revision v1_5): writes pk22/w1/rc_cert/kt_s8h_rcc_v1_5.py from
kt_s8h_rcc_v1_4.py (sha256 69180107...) by exact replacements with asserted counts, as a new file (mode 'x'), for the review
of v1_4:
- The fix (S8's upper-end rule): chain_h_c takes allow=None and records the place-2 allowance constants of slots 0 and 1 it used in
  ch['h']['allowH']; h_build passes the dual run's constants (upper ends over the box) to the midpoint run, and h_thin passes the run's
  constants to every thin chain (as S8's on_dual); the gate HALLOW (each piece) checks that the midpoint run used the dual run's
  constants, object for object; PLANT-HALLOW (smoke): the midpoint run rebuilt without them must fail that check.
- C-TARGET-RC, RC's radii rho and u-balls r_u of the box against rc_radii on each of the 27 thin chains (box >= target
  (1 - 1e-10)), with PLANT-TARGET-RC (the box's values x 1e-3 must fail).
- Each ROW line with a pair-form record also prints the class-level centred balls topc, +dz and -dz, so cl2 can be rebuilt from
  printed numbers (v1_4's record writer already copies output lines verbatim, so the 'n : 5' of v1_3's copy step is gone).
- The label, the usage strings and the docstring's first line change, and one docstring line is added. Nothing else changes (the diff
  shows it). Prints every sha256. Usage: make_rcc_v1_5.py."""
import ast, hashlib, os
TOP = '/mnt/g2/release/root/code/pk22/w1/rc_cert'
SRC, DST = TOP + '/kt_s8h_rcc_v1_4.py', TOP + '/kt_s8h_rcc_v1_5.py'
R = []   # (label, old, new): each old must occur exactly once
R.append(('chain_h_c def', "def chain_h_c(VV, VH, chV, mains, vac, cfix):\n",
          "def chain_h_c(VV, VH, chV, mains, vac, cfix, allow=None):\n"))
R.append(('chain_h_c docstring', "    of the run (no bar is added here); slots >= 2 and the bulk vector are set by rc_apply.\"\"\"\n",
          "    of the run (no bar is added here); slots >= 2 and the bulk vector are set by rc_apply. v1_5 (S8's upper-end rule): the\n"
          "    place-2 allowance constants s |v_u| of slots 0 and 1 are the dual run's, upper ends over the box; allow (a run's ch['h']['allowH'])\n"
          "    passes them to the midpoint run and to the thin chains, and ch['h']['allowH'] records the constants used.\"\"\"\n"))
R.append(('chain_h_c allowance',
          "    def allow(v):\n"
          "        a_ = (s * abs(v[0]).upper()).upper()\n"
          "        return (v[0], [x + CM.pm(a_) for x in v[1]])\n"
          "    L = dict(chV['L'])\n"
          "    raw = {0: allow((rhoE * fT[0] / (lam0 * e[0]), comps(fT, rhoE * sg / (lam0 * e[0])))),\n"
          "           1: allow((rhoH * hT[0] / (lam0 * lam0 * e[0]), comps(hT, rhoH * sg / (lam0 * lam0 * e[0]))))}\n",
          "    alw = {}\n"
          "\n"
          "    def allow_(i, v):\n"
          "        a_ = allow[i] if allow is not None else (s * abs(v[0]).upper()).upper()\n"
          "        alw[i] = a_\n"
          "        return (v[0], [x + CM.pm(a_) for x in v[1]])\n"
          "    L = dict(chV['L'])\n"
          "    raw = {0: allow_(0, (rhoE * fT[0] / (lam0 * e[0]), comps(fT, rhoE * sg / (lam0 * e[0])))),\n"
          "           1: allow_(1, (rhoH * hT[0] / (lam0 * lam0 * e[0]), comps(hT, rhoH * sg / (lam0 * lam0 * e[0]))))}\n"))
R.append(('chain_h_c record', "    ch['h'] = {'c': c, 'res2y0': n2y - sq(y0), 'ny0': n2y, 'Ap2y0': ap2}\n",
          "    ch['h'] = {'c': c, 'res2y0': n2y - sq(y0), 'ny0': n2y, 'Ap2y0': ap2, 'allowH': alw}\n"))
R.append(('hallow_ok', "def h_build(n, A, r, HE, q, trb, T, vac, zero_bars=False, zero_tgrad=False, fixed=None, tau_ovr=None):\n",
          "def hallow_ok(used, ref):\n"
          "    \"\"\"HALLOW (v1_5): a run used exactly the reference constants, the same keys and the same objects.\"\"\"\n"
          "    return sorted(used) == sorted(ref) and all(used[k_] is ref[k_] for k_ in ref)\n"
          "\n"
          "\n"
          "def h_build(n, A, r, HE, q, trb, T, vac, zero_bars=False, zero_tgrad=False, fixed=None, tau_ovr=None):\n"))
R.append(('h_build calls', "    chHd0 = chain_h_c(VdV, VdH, chd_V, mains, vac, cfix)\n    chHm0 = chain_h_c(VmV, VmH, chm_V, mains, vac, cfix)\n",
          "    chHd0 = chain_h_c(VdV, VdH, chd_V, mains, vac, cfix)\n"
          "    allowH = chHd0['h']['allowH']   # v1_5: the dual run's place-2 constants, upper ends over the box\n"
          "    chHm0 = chain_h_c(VmV, VmH, chm_V, mains, vac, cfix, allow=allowH)\n"
          "    hallow = hallow_ok(chHm0['h']['allowH'], allowH)\n"))
R.append(('h_build return', "    return {'keys': keys, 'rad': rad, 'chd_V': chd_V,",
          "    return {'keys': keys, 'rad': rad, 'allowH': allowH, 'hallow': hallow, 'VmV': VmV, 'VmH': VmH, 'chd_V': chd_V,"))
R.append(('eval_piece gate', "'VRERUN': not rerun_bad, 'KEYS': keys_ok(cH[3], keys) and keys_ok(cV[3], keys), 'OWN': dual_own(cH)})\n",
          "'VRERUN': not rerun_bad, 'KEYS': keys_ok(cH[3], keys) and keys_ok(cV[3], keys), 'OWN': dual_own(cH),\n"
          "                'HALLOW': hb['hallow']})\n"))
R.append(('h_thin', "    chH0 = chain_h_c(EV, EH, chV, A['mains'][n], v, hb['cfix'])\n",
          "    chH0 = chain_h_c(EV, EH, chV, A['mains'][n], v, hb['cfix'], allow=hb['allowH'])   # v1_5: the run's place-2 constants\n"))
R.append(('row_line', "            ('%.9e' % float(inf['cl2'])) if inf['cl2'] is not None else '-')\n",
          "            ('%.9e' % float(inf['cl2'])) if inf['cl2'] is not None else '-')\n"
          "        bl = lambda b: ('[%.9e, %.9e]' % (float(b.lower()), float(b.upper()))) if b is not None else '-'\n"
          "        if inf.get('topc') is not None:   # v1_5: the class-level centred balls, so cl2 can be rebuilt\n"
          "            tail += ' topc %s +dz %s -dz %s' % (bl(inf['topc']), bl(inf['cen'].get('+dz')), bl(inf['cen'].get('-dz')))\n"))
R.append(('target_h def', "def target_h(ev, mb, c1_scale=None):\n", "def target_h(ev, mb, c1_scale=None, rc_scale=None):\n"))
R.append(('target_h docstring', "    c1_scale: the box C1 multiplied by it in C-TARGET-H (PLANT-TARGET-H). Returns a dict of counts and failures.\"\"\"\n",
          "    v1_5, C-TARGET-RC: RC's radii rho[i] (i = 2..7, inf) and u-balls r_u[i] of the box >= rc_radii's values on each of\n"
          "    the 27 thin chains (same prm, tau', beta_H, w, pn_SH4 and kappa), box >= target (1 - 1e-10).\n"
          "    c1_scale: the box C1 multiplied by it in C-TARGET-H (PLANT-TARGET-H); rc_scale: the box's rho and r_u multiplied by it in\n"
          "    C-TARGET-RC (PLANT-TARGET-RC). Returns a dict of counts and failures.\"\"\"\n"))
R.append(('target_h res',
          "    res = {'classes': 0, 'active': 0, 'points': 0, 'fail': [], 'tchecks': 0, 'tfail': [], 'tworst': 0.0, 'vchecks': 0, 'vfail': []}\n",
          "    res = {'classes': 0, 'active': 0, 'points': 0, 'fail': [], 'tchecks': 0, 'tfail': [], 'tworst': 0.0, 'vchecks': 0, 'vfail': [],\n"
          "           'rchecks': 0, 'rfail': [], 'rworst': 0.0}\n"))
R.append(('target_h rc', "    RkT = {}\n",
          "    for it, mode, chHt, chVt in mb['thin']:   # v1_5: C-TARGET-RC\n"
          "        rho_t, ru_t = rc_radii(chHt, ev['prmV'], hb['tau'], hb['bH'], ev['vac'], hb['w_b'], hb['pn'], hb['kap'])\n"
          "        for k_ in list(range(2, 8)) + ['inf']:\n"
          "            pairs = [('rho', hb['rho'][k_], rho_t[k_])] + ([('r_u', hb['r_u'][k_], ru_t[k_])] if k_ != 'inf' else [])\n"
          "            for nm, bx, tg in pairs:\n"
          "                res['rchecks'] += 1\n"
          "                b_ = float((bx * arb(rc_scale)).upper()) if rc_scale is not None else float(bx.upper())\n"
          "                g_ = float(tg.upper())\n"
          "                res['rworst'] = max(res['rworst'], g_ / b_ if b_ > 0 else (0.0 if g_ <= 0 else float('inf')))\n"
          "                if not (g_ * (1 - 1e-10) <= b_):\n"
          "                    res['rfail'].append('%s %s' % (nm, k_))\n"
          "    RkT = {}\n"))
R.append(('checks_h rc line', "            gate('C-TARGET-H', not d['tfail'] and not d['vfail'])))\n    return mb\n",
          "            gate('C-TARGET-H', not d['tfail'] and not d['vfail'])))\n"
          "    out('C-TARGET-RC N=%d piece %d%s (RC\\'s radii rho and u-balls r_u of the box against rc_radii on the 27 thin chains, box >= target '\n"
          "        '(1 - 1e-10)): %d checks, largest target/box %.4f, failing %d%s -> %s' % (\n"
          "            n, i, tag, d['rchecks'], d['rworst'], len(d['rfail']), (' (%s)' % ', '.join(sorted(set(d['rfail']))[:3])) if d['rfail'] else '',\n"
          "            gate('C-TARGET-RC', not d['rfail'])))\n"
          "    return mb\n"))
R.append(('smoke plants',
          "    plant('PLANT-TARGET-H', len(dtp['tfail']) > 0, '(piece %d with the box C1 x 1e-3: C-TARGET-H fails %d of %d checks)' % (\n"
          "        i0, len(dtp['tfail']), dtp['tchecks']))\n",
          "    plant('PLANT-TARGET-H', len(dtp['tfail']) > 0, '(piece %d with the box C1 x 1e-3: C-TARGET-H fails %d of %d checks)' % (\n"
          "        i0, len(dtp['tfail']), dtp['tchecks']))\n"
          "    dtr = target_h(ev, mb, rc_scale=1e-3)   # v1_5 (N-3)\n"
          "    plant('PLANT-TARGET-RC', len(dtr['rfail']) > 0, '(piece %d with the box\\'s rho and r_u x 1e-3: C-TARGET-RC fails %d of %d '\n"
          "          'checks)' % (i0, len(dtr['rfail']), dtr['rchecks']))\n"
          "    hb0 = ev['hb']   # v1_5: the midpoint run rebuilt without the dual run's constants must fail HALLOW\n"
          "    chx = chain_h_c(hb0['VmV'], hb0['VmH'], hb0['chm_V'], A['mains'][n], ev['vac'], hb0['cfix'])\n"
          "    out('C-HALLOW N=%d piece %d: the midpoint run used the dual run\\'s place-2 constants (slots 0 and 1: %s) -> %s' % (\n"
          "        n, i0, ', '.join('%.6e' % float(hb0['allowH'][k_]) for k_ in sorted(hb0['allowH'])), gate('C-HALLOW', hb0['hallow'])))\n"
          "    plant('PLANT-HALLOW', not hallow_ok(chx['h']['allowH'], hb0['allowH']), '(the midpoint run rebuilt without them: its own constants '\n"
          "          '%s)' % ', '.join('%.6e' % float(chx['h']['allowH'][k_]) for k_ in sorted(chx['h']['allowH'])))\n"))
R.append(('docstring name', '"""kt_s8h_rcc_v1_4.py -- pk22', '"""kt_s8h_rcc_v1_5.py -- pk22'))
R.append(('docstring v1_5 line', 'v1_4 (this revision of v1_3, 5aad7ad7, by make_rcc_v1_4.py):',
          'v1_5 (this revision of v1_4, 69180107, by make_rcc_v1_5.py): the horizontal place-2 allowance constants of\n'
          'slots 0 and 1 from the dual run passed to the midpoint run and the thin chains (S8\'s upper-end rule), gate HALLOW with PLANT-HALLOW;\n'
          'C-TARGET-RC with PLANT-TARGET-RC; the class-level centred balls on the ROW lines. v1_4 (the revision of v1_3, 5aad7ad7, by\n'
          'make_rcc_v1_4.py):'))
R.append(('docstring usage', 'Usage: kt_s8h_rcc_v1_4.py cert|dev', 'Usage: kt_s8h_rcc_v1_5.py cert|dev'))
R.append(('USAGE', "USAGE = 'usage: kt_s8h_rcc_v1_4.py", "USAGE = 'usage: kt_s8h_rcc_v1_5.py"))
R.append(('LABEL', "LABEL = 'kt_s8h_rcc_v1_4'", "LABEL = 'kt_s8h_rcc_v1_5'"))


def sha(b):
    return hashlib.sha256(b).hexdigest()


assert os.path.dirname(os.path.abspath(DST)) == TOP and not os.path.exists(DST), DST
with open(SRC, 'rb') as fh:
    sb = fh.read()
print('SOURCE %s %s' % (sha(sb), SRC))
assert sha(sb).startswith('0dd303c6'), sha(sb)
t = sb.decode('utf-8')
# the chain_h_c replacements apply inside chain_h_c's own source segment: the ported float chain_h (rcm6) holds the same allowance
# lines word for word, and must not change
seg = [ast.get_source_segment(t, nd) for nd in ast.parse(t).body if isinstance(nd, ast.FunctionDef) and nd.name == 'chain_h_c']
assert len(seg) == 1 and t.count(seg[0]) == 1, 'chain_h_c segment'
fseg = seg[0] + '\n'
for lab, old, new in [x for x in R if x[0].startswith('chain_h_c ')]:
    n = fseg.count(old)
    assert n == 1, 'replacement %s (in chain_h_c): %d occurrences, expected 1' % (lab, n)
    fseg = fseg.replace(old, new)
    print('REPLACE %s: 1 occurrence in chain_h_c' % lab)
t = t.replace(seg[0] + '\n', fseg)
for lab, old, new in [x for x in R if not x[0].startswith('chain_h_c ')]:
    n = t.count(old)
    assert n == 1, 'replacement %s: %d occurrences, expected 1' % (lab, n)
    t = t.replace(old, new)
    print('REPLACE %s: 1 occurrence' % lab)
ast.parse(t)
nb = t.encode('utf-8')
with open(DST, 'xb') as fh:
    fh.write(nb)
print('ENGINE %s %s' % (sha(nb), DST))
