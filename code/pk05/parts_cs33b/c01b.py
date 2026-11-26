#!/usr/bin/env python3
# cs33b_rh_core.py (pk05, P-RH Stage B, v1_1 of cs33_rh_core cfa3c2da): shared arithmetic and operators of route H on the uniform 3 x n strip,
# N = 3, 4. v1_1 changes: tm_sqrt and the insertion multiplier g use the series enclosure per entry wherever it beats the crude one (c02b, c05b).
# Math: LEMMA_STRIP_RH_v1 (05964cd1) R1-R6; Lambda^2 identity, objects, near/far regimes and Taylor-model propagation in the header of
# cs33b_rh_cert.py. Route H's MR/TM arithmetic, corner_tm, kernel_tm, tm_lin_rows come from hubcert_v1e.py (c08d33c1), loaded read-only after
# its sha256 check. Imported by cs33b_rh_cert.py (sha-checked); never run alone.
import sys
import time
import math
import hashlib
import importlib.util
import numpy as np
from scipy.linalg import eigh_tridiagonal
from scipy.sparse.linalg import LinearOperator, eigsh

DIR = '/mnt/g2/release/root/code/pk05/'
ENGINE, ESHA = DIR + 'hubcert_v1e.py', 'fbed2d93a84a738207d59b3bd451e6c7572a293c2d356167c0a57a2ddac1ad30'
CAP = [1e9]


def guard(tag):
    if time.process_time() > CAP[0] - 5.0:
        print('CAP-STOP at %.1f s (%s)' % (time.process_time(), tag), flush=True)
        sys.exit(3)


def load(path, sha, name):
    with open(path, 'rb') as fh:
        got = hashlib.sha256(fh.read()).hexdigest()
    if got != sha:
        print('SHA MISMATCH %s %s' % (path, got), flush=True)
        sys.exit(2)
    spec_ = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec_)
    spec_.loader.exec_module(mod)
    return mod


E = load(ENGINE, ESHA, 'hubcert_v1e_mod')
MR, TM, arb, U, ETA, up, gam = E.MR, E.TM, E.arb, E.U, E.ETA, E.up, E.gam
SQ2 = arb(2).sqrt()


def dn(x):
    return np.nextafter(x, -np.inf)


def amin(a, b):
    return a if a < b else b


def amax(a, b):
    return a if a > b else b


def tm_bounds(A):
    """entrywise floats lo <= A(t) <= hi for every |t| <= h"""
    rest, hp = np.zeros_like(A.R), 1.0
    for d in range(1, A.k + 1):
        hp = up(hp * A.h)
        rest = up(rest + A.c[d].absu() * hp)
    rest = up((rest + A.R + A.c[0].r) * (1.0 + 4 * (A.k + 3) * U))
    m = A.c[0].m
    return dn(m - rest), up(m + rest)


def tm_const(v, like, h, k):
    """degree-k TM of an exact float (array or scalar) broadcast to the shape of like"""
    z = np.zeros_like(np.asarray(like, dtype=np.float64))
    return TM([MR(np.asarray(v, dtype=np.float64) + z)] + [MR(z.copy()) for _ in range(k)], z.copy(), h, k)


def tm_trunc(A, k):
    """the same function as a degree-k TM (k <= A.k): coefficients above k move to the remainder"""
    if k >= A.k:
        return A
    extra, hp = np.zeros_like(A.R), _hp(A.h, k + 1)
    for d in range(k + 1, A.k + 1):
        extra = up(extra + A.c[d].absu() * hp)
        hp = up(hp * A.h)
    return TM([A.c[d] for d in range(k + 1)], up((A.R + extra) * (1.0 + 4 * U)), A.h, k)


def _hp(h, d):
    v = 1.0
    for _ in range(d):
        v = up(v * h)
    return v


def poly(A, t):
    """float value of A's polynomial part at t (Horner); remainders ignored (float operator only)"""
    v = A.c[A.k].m.copy()
    for d in range(A.k - 1, -1, -1):
        v = v * t + A.c[d].m
    return v
