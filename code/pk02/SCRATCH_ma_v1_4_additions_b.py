

# ---------------------------------------------------------------------------- arbeng_ma_v1_4 (DESIGN_ARBENG_MA_v1_4): unit-built tables, blocked E2
import hashlib, json, time


def _sha_file(path):
    with open(path, 'rb') as fh:
        return hashlib.sha256(fh.read()).hexdigest()


KERNEL_SHA = _sha_file(os.path.abspath(__file__))
BLOCK = 50000                  # destinations per block of a level (MomTableU): about 1e7 terms, 1.3 GB peak, at level 16 of D16 F12


def scalar_sum_fast(mid, sa, sr, k):
    """v1_4: seg_pairwise's single-segment case without the sort and the index bookkeeping. Level by level the pairs (2i, 2i + 1) are added
    with count max + 1 and an odd last element is carried: the same pairs in the same order as seg_pairwise with one destination, hence
    bit-identical to scalar_sum (C-FASTSUM). Returns an MA of length 1."""
    m = np.array(mid, dtype=float)
    a = np.array(sa, dtype=float)
    r = np.array(sr, dtype=float)
    kk = np.array(k, dtype=np.int64)
    if len(m) == 0:
        return MA.zeros(1)
    while len(m) > 1:
        h = len(m) // 2
        m2 = m[0:2 * h:2] + m[1:2 * h:2]
        a2 = a[0:2 * h:2] + a[1:2 * h:2]
        r2 = r[0:2 * h:2] + r[1:2 * h:2]
        k2 = np.maximum(kk[0:2 * h:2], kk[1:2 * h:2]) + 1
        if len(m) % 2:
            m2, a2, r2, k2 = np.append(m2, m[-1]), np.append(a2, a[-1]), np.append(r2, r[-1]), np.append(k2, kk[-1])
        m, a, r, kk = m2, a2, r2, k2
    return MA(m, a, r, kk)


def ma_scalar_dump(x):
    """v1_4: a length-1 MA as a lossless dict (float hex, int count), for a caller's memo."""
    return {'mid': float(x.mid[0]).hex(), 'sa': float(x.sa[0]).hex(), 'sr': float(x.sr[0]).hex(), 'k': int(x.k[0])}


def ma_scalar_load(d):
    """v1_4: the inverse of ma_scalar_dump; checks the shadow order."""
    x = MA(np.array([float.fromhex(d['mid'])]), np.array([float.fromhex(d['sa'])]), np.array([float.fromhex(d['sr'])]),
           np.array([int(d['k'])], dtype=np.int64))
    x.check('ma_scalar_load')
    return x


def E2_plan(table, P, Q, max_pairs):
    """v1_4: blocks of P's terms for E2_block. The order is v1_3's E2 order (by degree, then the term's own index within P), cut into
    contiguous blocks whose pair counts (each P term against every Q term) stay at or below max_pairs; a single term is never split.
    Returns {'blocks': [(start, end), ...], 'order': index array, 'pairs': total}."""
    dP, cP, aP = table._arr(P)
    dQ, cQ, aQ = table._arr(Q)
    order = np.concatenate([np.flatnonzero(dP == d1) for d1 in np.unique(dP)]) if len(dP) else np.zeros(0, dtype=np.int64)
    per = len(cQ)
    if per == 0 or len(order) == 0:
        return {'blocks': [], 'order': order, 'pairs': 0}
    rows = max(1, int(max_pairs) // per)
    blocks = [(s, min(s + rows, len(order))) for s in range(0, len(order), rows)]
    E2_check_plan(table, P, Q, {'blocks': blocks, 'order': order})
    return {'blocks': blocks, 'order': order, 'pairs': per * len(order)}


def E2_check_plan(table, P, Q, plan):
    """v1_4: the blocks' P ranges partition P (contiguous, no gap, no overlap, every term once) and the order is the
    deterministic one E2_plan builds; ValueError otherwise."""
    dP, cP, aP = table._arr(P)
    want = np.concatenate([np.flatnonzero(dP == d1) for d1 in np.unique(dP)]) if len(dP) else np.zeros(0, dtype=np.int64)
    if not np.array_equal(np.asarray(plan['order']), want):
        raise ValueError('E2 plan: the order is not E2_plan\'s')
    pos = 0
    for s, e in plan['blocks']:
        if s != pos or not (e > s):
            raise ValueError('E2 plan: the blocks do not partition P')
        pos = e
    if pos != len(want):
        raise ValueError('E2 plan: the blocks do not cover P')


def E2_block(table, P, Q, plan, b):
    """v1_4: v1_3's E2 loop (MomTable.E2) restricted to the P terms of block b of plan; returns the block's sum as an MA of length 1, before
    any ball or fallback test (E2_combine does both once). A one-block plan reproduces v1_3's E2 sum exactly (same parts, same trees;
    scalar_sum_fast is bit-identical to scalar_sum)."""
    E2_check_plan(table, P, Q, plan)
    dP, cP, aP = table._arr(P)
    dQ, cQ, aQ = table._arr(Q)
    s0, s1_ = plan['blocks'][b]
    inblock = np.zeros(len(dP), dtype=bool)
    inblock[plan['order'][s0:s1_]] = True
    parts = []
    with np.errstate(over='raise', invalid='raise', divide='raise'):
        for d1 in np.unique(dP):
            s1 = np.flatnonzero((dP == d1) & inblock)
            if len(s1) == 0:
                continue
            for d2 in np.unique(dQ):
                s2 = np.flatnonzero(dQ == d2)
                kd = int(d1 + d2)
                if not (kd <= table.D):
                    raise ValueError('check failed: kd <= table.D')
                mom = table.mom[kd]
                rows = max(1, table.chunk // len(s2))
                for st in range(0, len(s1), rows):
                    pi = s1[st:st + rows]
                    idx = table.index(kd, (cP[pi][:, None] + cQ[s2][None, :]).ravel())
                    pp = np.repeat(pi, len(s2))
                    qq = np.tile(s2, len(pi))
                    tm, ta, tr = _prod((aP.mid[pp], aP.sa[pp], aP.sr[pp]), (aQ.mid[qq], aQ.sa[qq], aQ.sr[qq]),
                                       (mom.mid[idx], mom.sa[idx], mom.sr[idx]))
                    parts.append(scalar_sum_fast(tm, ta, tr, aP.k[pp] + aQ.k[qq] + mom.k[idx] + 2))
    one = tree_sum(parts)
    if one is None:
        return MA.zeros(1)
    one.check('E2_block')
    _scalar_ball(one)                   # the block's validity (finite, in binary64's range); no relative-error test here
    return one


def E2_combine(parts, plan=None):
    """v1_4: the blocks' sums (MA scalars, in block order; with plan, one per block of it) by tree_sum with tracked counts, then MA.check,
    the ball and the MAFallback test once, on the total (a single block may cancel). Returns the arb ball, as v1_3's E2."""
    if plan is not None and len(parts) != len(plan['blocks']):
        raise ValueError('E2_combine: %d parts for %d blocks' % (len(parts), len(plan['blocks'])))
    if not parts:
        return arb(0)
    one = tree_sum(list(parts))
    one.check('E2')
    ball, err = _scalar_ball(one)
    if float(one.mid[0]) != 0 and err > FALLBACK_REL * abs(float(one.mid[0])):
        raise MAFallback('E2: M-a error %.2e of %.2e' % (err, abs(float(one.mid[0]))))
    return ball


def _arb_exact_str(x):
    """the exact (mid, rad) of an arb ball as integer mantissa/exponent pairs (for the parameter hash)."""
    m, e = x.mid().man_exp()
    rm, re_ = x.rad().man_exp()
    return '%d,%d,%d,%d' % (int(m), int(e), int(rm), int(re_))


class MomTableView(MomTable):
    """v1_4: a read-only MomTable built from MomTableU's verified files (MomTableU.load); E, E2, index, _arr and shadow_max are MomTable's."""
    def __init__(self, F, D, n, groups, caps, B, pw, codes, mom, chunk=4000000):
        self.F, self.D, self.n, self.chunk = F, D, n, chunk
        self.groups, self.caps, self.B, self.pw = groups, caps, B, pw
        self.codes, self.mom = codes, mom
        self.zeroed, self.max_zero_rad, self.dropped = None, None, None


class MomTableU(MomTable):
    """v1_4 (DESIGN_ARBENG_MA_v1_4 sect. 1-2): MomTable's recursion in destination code blocks, built in resumable units with verified state.
    Only ok, decode and index are used from MomTable (its __init__ is not called). Usage: U = MomTableU(Gam, n, D, ...); U.start(dir);
    for unit in U.plan(dir, unit_pairs): U.run_unit(dir, unit); U.finish(dir); then MomTableU.load(dir, Gam, n, D, ...) or U.load_view(dir)."""
    def __init__(self, Gam, n, D, groups=None, caps=None, W_int=None, W=None, block=BLOCK, chunk=4000000):
        _check_prec()
        if W_int is not None:
            _check_W(W, W_int)
            if W.ncols() != Gam.nrows():
                raise ValueError('W has %d forms, Gam %d' % (W.ncols(), Gam.nrows()))
        if not (float(n) == n):
            raise ValueError('check failed: float(n) == n')
        F = Gam.nrows()
        self.F, self.D, self.n, self.chunk, self.block = F, D, n, chunk, int(block)
        self.groups = np.zeros(F, dtype=np.int64) if groups is None else np.asarray(groups, dtype=np.int64)
        self.caps = {} if caps is None else dict(caps)
        self.Gam, self.W_int, self.W = Gam, W_int, W
        B = D + 1
        _code_guard(B, F, 'MomTableU')
        self.B = B
        self.pw = np.array([B ** f for f in range(F)], dtype=np.int64)
        codes = [np.zeros(1, dtype=np.int64)]
        for d in range(1, D + 1):
            c = np.unique((codes[-1][:, None] + self.pw[None, :]).ravel())
            codes.append(c[self.ok(c)])
        self.codes = codes
        self.codes_sha = [hashlib.sha256(c.tobytes()).hexdigest() for c in codes]
        self.hpar = self._hpar()

    def _hpar(self):
        """H_par: sha256 over the exact Gam entries, n, D, F, groups, caps, W_int, the block size, VERSION and the kernel's sha256."""
        F = self.F
        parts = ['arbeng_ma_v1_4 MomTableU', 'VERSION=%s' % VERSION, 'KERNEL=%s' % KERNEL_SHA, 'F=%d' % F, 'D=%d' % self.D,
                 'n=%s' % Fraction(self.n), 'groups=%s' % ','.join(str(int(g)) for g in self.groups),
                 'caps=%s' % ';'.join('%d:%d' % (int(g), int(c)) for g, c in sorted(self.caps.items())), 'block=%d' % self.block,
                 'Gam=' + ';'.join(_arb_exact_str(self.Gam[i, j]) for i in range(F) for j in range(F))]
        if self.W_int is not None:
            parts.append('W_int=' + ';'.join(','.join(str(int(x)) for x in row) for row in np.asarray(self.W_int)))
        return hashlib.sha256('|'.join(parts).encode()).hexdigest()

    # ----- the minors (v1_3's MomTable loop, l.431-457, unchanged in substance)
    def minors(self):
        F, D = self.F, self.D
        zeroed, max_zero_rad, dropped = 0, 0.0, []
        Dj = [None] * (min(F, D) + 1)
        for j in range(1, min(F, D) + 1):
            cs, mids, rads = [], [], []
            sign = arb(-2) ** j
            for A in itertools.combinations(range(F), j):
                c = int(sum(int(self.pw[f]) for f in A))
                if not self.ok(np.array([c], dtype=np.int64))[0]:
                    continue
                sub = arb_mat(j, j)
                for a_, fa in enumerate(A):
                    for b_, fb in enumerate(A):
                        sub[a_, b_] = self.Gam[fa, fb]
                d = sub.det()
                if self.W_int is not None and int_rank(self.W_int, A) < j:
                    if not d.contains(0):
                        raise ValueError('det of the singular subset %s excludes 0' % (A,))
                    zeroed += 1
                    max_zero_rad = max(max_zero_rad, float(d.rad()))
                    dropped.append(A)
                    continue
                m, r = ball_to_in(sign * d)
                cs.append(c)
                mids.append(m)
                rads.append(r)
            Dj[j] = (np.array(cs, dtype=np.int64), MA.inputs(mids, rads))
        return Dj, zeroed, max_zero_rad, dropped

    # ----- files and hand-offs (atomic writes, a temporary name then a rename, the hand-off JSON last)
    @staticmethod
    def _atomic(path, write):
        if os.path.exists(path):
            raise ValueError('C-STATE: %s exists; a state file is never overwritten' % os.path.basename(path))
        tmp = '%s.tmp.%d.%d' % (path, os.getpid(), time.time_ns())
        with open(tmp, 'xb') as fh:
            write(fh)
            fh.flush()
            os.fsync(fh.fileno())
        if os.path.exists(path):
            raise ValueError('C-STATE: %s appeared during the write' % os.path.basename(path))
        os.rename(tmp, path)

    @staticmethod
    def _write_npz(path, arrays):
        MomTableU._atomic(path, lambda fh: np.savez(fh, **arrays))
        return {'size': os.path.getsize(path), 'sha256': _sha_file(path)}

    @staticmethod
    def _write_json(path, obj):
        MomTableU._atomic(path, lambda fh: fh.write(json.dumps(obj, sort_keys=True, indent=1).encode()))
        return _sha_file(path)

    def _read_handoff(self, path):
        with open(path) as fh:
            h = json.load(fh)
        if h.get('hpar') != self.hpar:
            raise ValueError('C-STATE: %s carries another parameter hash' % os.path.basename(path))
        return h

    @staticmethod
    def _read_npz(state_dir, name, entry):
        path = os.path.join(state_dir, name)
        if not (os.path.getsize(path) == entry['size'] and _sha_file(path) == entry['sha256']):
            raise ValueError('C-STATE: %s differs from its hand-off (size or sha256)' % name)
        with np.load(path, allow_pickle=False) as z:
            return dict((k, z[k]) for k in z.files)

    @staticmethod
    def _ma(arrs, prefix=''):
        x = MA(arrs[prefix + 'mid'].astype(float), arrs[prefix + 'sa'].astype(float), arrs[prefix + 'sr'].astype(float),
               arrs[prefix + 'k'].astype(np.int64))
        x.check('MomTableU file')
        return x

    def nblocks(self, k):
        return -(-len(self.codes[k]) // self.block)

    def start(self, state_dir):
        """state 0: the minors D_j (raw MA fields per j) and the hand-off with H_par and the code hashes."""
        Dj, zeroed, mzr, dropped = self.minors()
        arrays = {}
        for j in range(1, len(Dj)):
            cj, vj = Dj[j]
            arrays.update({'c%d' % j: cj, 'mid%d' % j: vj.mid, 'sa%d' % j: vj.sa, 'sr%d' % j: vj.sr, 'k%d' % j: vj.k})
        ent = self._write_npz(os.path.join(state_dir, 'state0.npz'), arrays)
        h = {'kind': 'MomTableU state0', 'hpar': self.hpar, 'kernel_sha': KERNEL_SHA, 'F': self.F, 'D': self.D, 'block': self.block,
             'codes_sha': self.codes_sha, 'files': {'state0.npz': ent}, 'zeroed': zeroed, 'max_zero_rad': mzr,
             'dropped': [list(A) for A in dropped]}
        return self._write_json(os.path.join(state_dir, 'handoff_state0.json'), h)

    def _load_Dj(self, state_dir):
        h = self._read_handoff(os.path.join(state_dir, 'handoff_state0.json'))
        if h.get('codes_sha') != self.codes_sha:
            raise ValueError('C-STATE: state0 was built on other code arrays')
        z = self._read_npz(state_dir, 'state0.npz', h['files']['state0.npz'])
        Dj = [None] * (min(self.F, self.D) + 1)
        for j in range(1, len(Dj)):
            v = MA(z['mid%d' % j].astype(float), z['sa%d' % j].astype(float), z['sr%d' % j].astype(float), z['k%d' % j].astype(np.int64))
            v.check('MomTableU D_j')
            Dj[j] = (z['c%d' % j].astype(np.int64), v)
        return Dj

    def block_pairs(self, k, b, Dj):
        """the exact candidate pair count of block b of level k (two searchsorted per (j, A)), before any arithmetic."""
        ck = self.codes[k]
        i0, i1 = b * self.block, min((b + 1) * self.block, len(ck))
        lo, hi = int(ck[i0]), int(ck[i1 - 1]) + 1
        tot = 0
        for j in range(1, min(k, self.F) + 1):
            cj = Dj[j][0]
            if len(cj) == 0:
                continue
            cq = self.codes[k - j]
            tot += int((np.searchsorted(cq, hi - cj, 'left') - np.searchsorted(cq, lo - cj, 'left')).sum())
        return tot

    def plan(self, state_dir, unit_pairs):
        """the units (k, b0, b1, pairs) in build order: per level, consecutive blocks packed up to unit_pairs (at least one block each)."""
        Dj = self._load_Dj(state_dir)
        units = []
        for k in range(1, self.D + 1):
            cur, acc = None, 0
            for b in range(self.nblocks(k)):
                p = self.block_pairs(k, b, Dj)
                if cur is not None and acc + p > unit_pairs:
                    units.append((k, cur, b, acc))
                    cur, acc = None, 0
                if cur is None:
                    cur = b
                acc += p
            if cur is not None:
                units.append((k, cur, self.nblocks(k), acc))
        return units

    def _codes_equal(self, z, k, name):
        """the review 53de1c0d Q3 (a): the stored codes must equal the codes recomputed from (F, D, groups, caps), exactly."""
        if 'codes' not in z or not np.array_equal(z['codes'].astype(np.int64), self.codes[k]):
            raise ValueError('C-STATE: %s does not carry this table\'s codes of level %d' % (name, k))

    def _load_level(self, state_dir, k):
        if k == 0:
            return MA.exact([1.0])
        h = self._read_handoff(os.path.join(state_dir, 'handoff_level_k%02d.json' % k))
        if h.get('level') != k or h.get('codes_sha') != self.codes_sha[k] or h.get('kernel_sha') != KERNEL_SHA:
            raise ValueError('C-STATE: level %d hand-off does not match' % k)
        name = 'level_k%02d.npz' % k
        z = self._read_npz(state_dir, name, h['files'][name])
        self._codes_equal(z, k, name)
        x = self._ma(z)
        if len(x.mid) != len(self.codes[k]):
            raise ValueError('C-STATE: level %d has %d entries, %d codes' % (k, len(x.mid), len(self.codes[k])))
        return x

    def _block(self, k, b, Dj, M):
        """block b of level k in the pull form (DESIGN sect. 1): all terms of its destinations, one seg_pairwise tree per destination,
        then div_int(k). Returns (MA, terms, candidate pairs, the largest terms / (2^|supp c| - 1) over the block's destinations)."""
        ck = self.codes[k]
        i0, i1 = b * self.block, min((b + 1) * self.block, len(ck))
        lo, hi = int(ck[i0]), int(ck[i1 - 1]) + 1
        dsts, mids, sas, srs, ks = [], [], [], [], []
        cand = 0
        with np.errstate(over='raise', invalid='raise', divide='raise'):
            for j in range(1, min(k, self.F) + 1):
                cj, vj = Dj[j]
                if len(cj) == 0:
                    continue
                coef = float(Fraction(2 - self.n, 2) * j - k)
                vs = vj.scale(coef)
                cq = self.codes[k - j]
                Mq = M[k - j]
                left = np.searchsorted(cq, lo - cj, 'left')
                right = np.searchsorted(cq, hi - cj, 'left')
                cnt = right - left
                sel = np.flatnonzero(cnt > 0)
                if len(sel) == 0:
                    continue
                cs = cnt[sel]
                tot = int(cs.sum())
                cand += tot
                A = np.repeat(sel, cs)
                q = np.repeat(left[sel], cs) + (np.arange(tot, dtype=np.int64) - np.repeat(np.cumsum(cs) - cs, cs))
                keep = Mq.present()[q]
                A, q = A[keep], q[keep]
                dest = cj[A] + cq[q]
                idx = np.searchsorted(ck, dest)
                idx[idx >= len(ck)] = 0
                hit = ck[idx] == dest
                A, q, idx = A[hit], q[hit], idx[hit]
                if len(A) == 0:
                    continue
                mid, sa, sr = _prod((vs.mid[A], vs.sa[A], vs.sr[A]), (Mq.mid[q], Mq.sa[q], Mq.sr[q]))
                dsts.append(idx - i0)
                mids.append(mid)
                sas.append(sa)
                srs.append(sr)
                ks.append(vs.k[A] + Mq.k[q] + 1)
            nb = i1 - i0
            ratio = 0.0
            if dsts:
                dall = np.concatenate(dsts)
                acc = seg_pairwise(dall, np.concatenate(mids), np.concatenate(sas), np.concatenate(srs), np.concatenate(ks), nb)
                u, cnts = np.unique(dall, return_counts=True)          # C-PAIRS: terms per destination <= 2^|supp c| - 1
                supp = (self.decode(ck[i0:i1][u]) > 0).sum(axis=1)
                bound = np.left_shift(np.ones(len(u), dtype=np.int64), supp) - 1
                if np.any(cnts > bound):
                    raise ValueError('C-PAIRS: a destination of level %d block %d has more terms than 2^|supp c| - 1' % (k, b))
                ratio = float(np.max(cnts / bound))
            else:
                acc = MA.zeros(nb)
            res = acc.div_int(k)
        res.check('MomTableU level %d block %d' % (k, b))
        return res, int(sum(len(x) for x in dsts)), cand, ratio

    def run_unit(self, state_dir, unit, cpu_budget=None):
        """one unit (k, b0, b1[, pairs]): loads the levels it needs (verified), computes its blocks, writes them and a hand-off, and
        assembles and saves the level when the unit ends it. With cpu_budget (s), it stops between blocks, never inside one, before a block
        whose expected CPU (the previous block's CPU per pair times this block's pairs) would cross the budget; the report's 'end' is then
        the first block not done, which the caller's next unit starts from. C-PAIRS: the candidate pairs generated equal plan()'s exact
        count block by block, and no destination has more than 2^|supp c| - 1 terms. Returns the report dict."""
        t0 = time.process_time()
        tiny0 = TINY_COUNT[0]
        k, b0, b1 = int(unit[0]), int(unit[1]), int(unit[2])
        if not (1 <= k <= self.D and 0 <= b0 < b1 <= self.nblocks(k)):
            raise ValueError('a unit outside the table: %s' % (unit,))
        Dj = self._load_Dj(state_dir)
        M = [None] * (self.D + 1)
        for kk in range(max(0, k - min(k, self.F)), k):
            M[kk] = self._load_level(state_dir, kk)
        outs, terms, cands, planned, ratio, rate, end = [], 0, 0, 0, 0.0, None, b0
        for b in range(b0, b1):
            p = self.block_pairs(k, b, Dj)
            if cpu_budget is not None and outs and rate is not None and (time.process_time() - t0) + rate * p > cpu_budget:
                break
            tb = time.process_time()
            r, nt, cand, rt = self._block(k, b, Dj, M)
            if cand != p:
                raise ValueError('C-PAIRS: level %d block %d generated %d candidate pairs, plan() counted %d' % (k, b, cand, p))
            rate = (time.process_time() - tb) / max(p, 1)
            outs.append(r)
            terms, cands, planned, ratio, end = terms + nt, cands + cand, planned + p, max(ratio, rt), b + 1
        cat = MA(np.concatenate([o.mid for o in outs]), np.concatenate([o.sa for o in outs]), np.concatenate([o.sr for o in outs]),
                 np.concatenate([o.k for o in outs]))
        i0, i1 = b0 * self.block, min(end * self.block, len(self.codes[k]))
        name = 'unit_k%02d_b%05d_%05d.npz' % (k, b0, end)
        ent = self._write_npz(os.path.join(state_dir, name), {'codes': self.codes[k][i0:i1], 'mid': cat.mid, 'sa': cat.sa, 'sr': cat.sr,
                                                              'k': cat.k})
        rep = {'unit': [k, b0, end], 'asked': [k, b0, b1], 'pairs': planned, 'cand': cands, 'terms': terms, 'blocks': end - b0,
               'max_terms_ratio': ratio, 'check_ok': True, 'k_max': int(cat.k.max()) if len(cat.k) else 0,
               'shadow_max': float(cat.shadow_max()), 'tiny': TINY_COUNT[0] - tiny0, 'cpu': round(time.process_time() - t0, 3),
               'end': end, 'level_done': end == self.nblocks(k)}
        h = {'kind': 'MomTableU unit', 'hpar': self.hpar, 'kernel_sha': KERNEL_SHA, 'level': k, 'blocks': [b0, end], 'files': {name: ent},
             'report': rep}
        self._write_json(os.path.join(state_dir, 'handoff_unit_k%02d_b%05d_%05d.json' % (k, b0, end)), h)
        if end == self.nblocks(k):
            self._assemble(state_dir, k)
        return rep

    def _assemble(self, state_dir, k):
        """level k from its units: every unit hand-off of the level, contiguous from block 0, files verified, concatenated in order."""
        hs = []
        for fn in sorted(os.listdir(state_dir)):
            if fn.startswith('handoff_unit_k%02d_' % k) and fn.endswith('.json'):
                hs.append(self._read_handoff(os.path.join(state_dir, fn)))
        hs.sort(key=lambda h: h['blocks'][0])
        pos, parts = 0, []
        for h in hs:                                  # The review 53de1c0d Q3 (b): the unit ranges partition the destinations in code order
            if h.get('level') != k or h.get('kernel_sha') != KERNEL_SHA or h['blocks'][0] != pos or not (h['blocks'][1] > pos):
                raise ValueError('C-STATE: the units of level %d do not partition its blocks (gap, overlap, level or kernel)' % k)
            (name, ent), = h['files'].items()
            z = self._read_npz(state_dir, name, ent)
            j0, j1 = h['blocks'][0] * self.block, min(h['blocks'][1] * self.block, len(self.codes[k]))
            if not np.array_equal(z['codes'].astype(np.int64), self.codes[k][j0:j1]):
                raise ValueError('C-STATE: unit %s does not carry the codes of its blocks' % name)
            parts.append(self._ma(z))
            pos = h['blocks'][1]
        if pos != self.nblocks(k):
            raise ValueError('C-STATE: level %d is incomplete' % k)
        x = MA(np.concatenate([p.mid for p in parts]), np.concatenate([p.sa for p in parts]), np.concatenate([p.sr for p in parts]),
               np.concatenate([p.k for p in parts]))
        if len(x.mid) != len(self.codes[k]):
            raise ValueError('C-STATE: level %d assembled %d entries for %d codes' % (k, len(x.mid), len(self.codes[k])))
        x.check('MomTableU level %d' % k)
        name = 'level_k%02d.npz' % k
        ent = self._write_npz(os.path.join(state_dir, name), {'codes': self.codes[k], 'mid': x.mid, 'sa': x.sa, 'sr': x.sr, 'k': x.k})
        h = {'kind': 'MomTableU level', 'hpar': self.hpar, 'kernel_sha': KERNEL_SHA, 'level': k, 'codes_sha': self.codes_sha[k],
             'files': {name: ent}, 'units': [h_['blocks'] for h_ in hs]}
        return self._write_json(os.path.join(state_dir, 'handoff_level_k%02d.json' % k), h)

    def finish(self, state_dir):
        """the moments: each level times its rows' exponent factorials (v1_3's MomTable l.475-483), saved per level, and the table hand-off."""
        files = {}
        smax = 0.0
        for d in range(self.D + 1):
            Md = self._load_level(state_dir, d)
            ex = self.decode(self.codes[d])
            f = [math.prod(math.factorial(int(x)) for x in row) for row in ex]
            fl = np.array([float(x) for x in f])
            kf = np.array([1 if x > 2 ** 53 else 0 for x in f], dtype=np.int64)
            mm = MA(Md.mid * fl, Md.sa * fl, Md.sr * fl, Md.k + kf + 1)
            mm.check('MomTableU moments %d' % d)
            smax = max(smax, mm.shadow_max())
            name = 'mom_k%02d.npz' % d
            files[name] = self._write_npz(os.path.join(state_dir, name), {'codes': self.codes[d], 'mid': mm.mid, 'sa': mm.sa, 'sr': mm.sr,
                                                                          'k': mm.k})
        h = {'kind': 'MomTableU table', 'hpar': self.hpar, 'kernel_sha': KERNEL_SHA, 'F': self.F, 'D': self.D, 'codes_sha': self.codes_sha,
             'files': files, 'shadow_max': smax}
        return self._write_json(os.path.join(state_dir, 'handoff_table.json'), h)

    def load_view(self, state_dir, expected_sha256=None):
        """the finished table as a MomTableView, after verifying the table hand-off (its sha256 when given), H_par, the code hashes and
        every moment file."""
        path = os.path.join(state_dir, 'handoff_table.json')
        if expected_sha256 is not None and _sha_file(path) != expected_sha256:
            raise ValueError('C-STATE: the table hand-off is not the expected one')
        h = self._read_handoff(path)
        if h.get('codes_sha') != self.codes_sha or h.get('kernel_sha') != KERNEL_SHA:
            raise ValueError('C-STATE: the table was built on other code arrays or by another kernel')
        mom = []
        for d in range(self.D + 1):
            name = 'mom_k%02d.npz' % d
            z = self._read_npz(state_dir, name, h['files'][name])
            self._codes_equal(z, d, name)
            x = self._ma(z)
            if len(x.mid) != len(self.codes[d]):
                raise ValueError('C-STATE: moments of level %d have %d entries' % (d, len(x.mid)))
            mom.append(x)
        return MomTableView(self.F, self.D, self.n, self.groups, self.caps, self.B, self.pw, self.codes, mom, self.chunk)

    @staticmethod
    def load(state_dir, Gam, n, D, groups=None, caps=None, W_int=None, W=None, block=BLOCK, expected_sha256=None):
        """the consumer's entry: H_par recomputed from the caller's inputs, then load_view."""
        return MomTableU(Gam, n, D, groups=groups, caps=caps, W_int=W_int, W=W, block=block).load_view(state_dir, expected_sha256)


def compare_float(table, npz_path, code_key='codes', value_key='moments'):
    """v1_4 INFO: a float moment table (codes and values, the codes in base B = D + 1 with pw = B^f) against the certified one: the largest
    |mid - float| / rad over the codes both hold, and the coverage (float values inside the balls). Returns a dict; never a gate."""
    with np.load(npz_path, allow_pickle=False) as z:
        cf, vf = z[code_key].astype(np.int64), z[value_key].astype(float)
    allc = np.concatenate(table.codes)                  # distinct across levels: a code fixes the exponents, hence the degree
    allm = np.concatenate([m.mid for m in table.mom])
    allr = np.concatenate([m.radius() for m in table.mom])
    order = np.argsort(allc, kind='stable')
    sc = allc[order]
    pos = np.searchsorted(sc, cf)
    pos[pos >= len(sc)] = 0
    hit = np.flatnonzero(sc[pos] == cf)
    g = order[pos[hit]]
    diff = np.abs(allm[g] - vf[hit])
    rad = allr[g]
    with np.errstate(divide='ignore', invalid='ignore'):
        q = np.where(rad > 0, diff / np.where(rad > 0, rad, 1.0), np.where(diff == 0, 0.0, np.inf))
    return {'compared': int(len(hit)), 'float_codes': int(len(cf)), 'inside': int(np.count_nonzero(diff <= rad)),
            'worst_diff_over_rad': float(q.max()) if len(q) else 0.0}
