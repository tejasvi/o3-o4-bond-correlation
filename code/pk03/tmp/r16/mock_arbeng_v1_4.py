#!/usr/bin/env python3
"""mock_arbeng_v1_4.py -- pk03 (code/pk03/tmp/r16/). A HAND MOCK of arbeng_ma_v1_4's additions (DESIGN_ARBENG_MA_v1_4 f01a6429
sect. 2-3) for m3_desk_bar_v11's tests of m3_bar_v11's control flow only. It certifies nothing and no certified run imports it.
- MomTableU: start writes the table's parameters (the Gram matrix's exact arb ends, n, D, groups, caps, W_int) to state_dir/params.json;
  plan lists one unit per level 1..D with a deterministic pair count (the level's binomial count times the subsets); run_unit writes the
  unit's marker file; finish writes handoff.json over the markers and returns (name, sha256); load re-hashes handoff.json and builds the
  real table with arbeng_ma_v1_3.allmom2 from params.json, so every moment and E2 is v1_3's.
- E2_plan splits P's terms (sorted by degree, then exponents) into blocks of at most max_pairs term pairs; E2_block returns the block's
  E2 (v1_3's, fallback=False) as its exact arb ends in JSON-able form; E2_combine adds the blocks' balls exactly in block order.
"""
import hashlib
import json
import math
import os
import sys

sys.path.append('/mnt/g2/release/root/code/pk02')
import arbeng_ma_v1_3 as K13
from flint import arb, arb_mat

VERSION = 'mock_arbeng_v1_4'
PREC = K13.PREC
MAFallback = K13.MAFallback


def _end(e):
    m, x = e.man_exp() if e != 0 else (0, 0)
    return [str(int(m)), int(x)]


def _arb_json(x):
    """a ball as the exact (mantissa, exponent) pairs of its lower and upper ends (as m3_scal.arb_to_iv reads them)."""
    return _end(x.lower()) + _end(x.upper())


def _arb_from(j):
    """the ball holding both exact ends (their union, as m3_scal.iv_to_arb builds it)."""
    lo = arb(int(j[0])) * arb(2) ** int(j[1])
    hi = arb(int(j[2])) * arb(2) ** int(j[3])
    return lo.union(hi)


def _sha_file(p):
    with open(p, 'rb') as fh:
        return hashlib.sha256(fh.read()).hexdigest()


class MomTableU:
    @staticmethod
    def start(Gam, n, D, groups, caps, W_int, W, state_dir):
        os.mkdir(state_dir)
        F = Gam.nrows()
        par = {'Gam': [[_arb_json(Gam[i, j]) for j in range(F)] for i in range(F)], 'n': n, 'D': D, 'groups': groups,
               'caps': sorted((int(k), int(v)) for k, v in caps.items()) if caps else None, 'W_int': W_int}
        with open(os.path.join(state_dir, 'params.json'), 'x') as fh:
            json.dump(par, fh, sort_keys=True)

    @staticmethod
    def plan(F, D, groups, caps, unit_pairs):
        return [{'level': k, 'b0': 0, 'b1': 1, 'pairs': math.comb(F + k - 1, k) * (2 ** min(F, k) - 1)} for k in range(1, D + 1)]

    @staticmethod
    def run_unit(state_dir, unit):
        p = os.path.join(state_dir, 'unit_L%d.json' % unit['level'])
        with open(p, 'x') as fh:
            json.dump(unit, fh, sort_keys=True)
        return {'check_ok': True, 'pairs': unit['pairs'], 'k_max': 0, 'shadow_max': 0.0, 'tiny': 0, 'mock': True}

    @staticmethod
    def finish(state_dir):
        names = sorted(f for f in os.listdir(state_dir) if f.startswith('unit_L'))
        ho = {'units': {f: _sha_file(os.path.join(state_dir, f)) for f in names}, 'params': _sha_file(os.path.join(state_dir, 'params.json'))}
        p = os.path.join(state_dir, 'handoff.json')
        with open(p, 'x') as fh:
            json.dump(ho, fh, sort_keys=True)
        return 'handoff.json', _sha_file(p)

    @staticmethod
    def load(path, expected_sha256):
        if _sha_file(path) != expected_sha256:
            raise ValueError('mock MomTableU.load: the hand-off sha256 does not match')
        sd = os.path.dirname(path)
        with open(path) as fh:
            ho = json.load(fh)
        if _sha_file(os.path.join(sd, 'params.json')) != ho['params'] or any(_sha_file(os.path.join(sd, f)) != h for f, h in ho['units'].items()):
            raise ValueError('mock MomTableU.load: a state file does not match the hand-off')
        with open(os.path.join(sd, 'params.json')) as fh:
            par = json.load(fh)
        F = len(par['Gam'])
        G = arb_mat(F, F)
        for i in range(F):
            for j in range(F):
                G[i, j] = _arb_from(par['Gam'][i][j])
        Wi = par['W_int']
        Wa = arb_mat(len(Wi), len(Wi[0]))
        for i in range(len(Wi)):
            for j in range(len(Wi[0])):
                Wa[i, j] = arb(Wi[i][j])
        caps = dict(par['caps']) if par['caps'] else None
        return K13.allmom2(G, par['n'], par['D'], groups=par['groups'], caps=caps, W_int=Wi, W=Wa)


def E2_plan(tab, P, Q, max_pairs):
    terms = sorted(P.to_arb_dict().items(), key=lambda kv: (sum(kv[0]), kv[0]))
    nq = max(1, len(Q.to_arb_dict()))
    per = max(1, int(max_pairs // nq))
    return [{'lo': i, 'hi': min(i + per, len(terms)), 'pairs': (min(i + per, len(terms)) - i) * nq} for i in range(0, len(terms), per)]


def E2_block(tab, P, Q, block):
    terms = sorted(P.to_arb_dict().items(), key=lambda kv: (sum(kv[0]), kv[0]))
    Pb = K13.SPoly.from_dict(dict(terms[block['lo']:block['hi']]), P.nv)
    return {'ball': _arb_json(tab.E2(Pb, Q, fallback=False))}


def E2_combine(parts, fallback=True):
    tot = arb(0)
    for p in parts:
        tot = tot + _arb_from(p['ball'])
    return tot
