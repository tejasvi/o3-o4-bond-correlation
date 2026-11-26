#!/usr/bin/env python3
"""acc2_v1.py -- two-producer acceptance for the option (C) re-verification package.

A reader accepts an item if the item names the cleaned producer's own sha256 (an item regenerated with the cleaned code), or if it
names the original producer's sha256 and the item file's bytes equal its row in the item manifest ITEM_MANIFEST_v1.tsv (an item
carried over from the original runs, with only the T renaming and the listed pins applied). The manifest is pinned by its sha256
below; each row gives the package path, the original sha256, the cleaned sha256, the T and P versions and the original producer.
Every decision is logged; at exit the log goes to the file named by the environment variable ACC2_LOG (if set), one row per decision:
decision (cleaned, original, refused), package path, named sha256."""
import atexit
import hashlib
import os
import sys

ROOT = '/mnt/g2/release/root'
MANIFEST = ROOT + '/code/acc/ITEM_MANIFEST_v1.tsv'
MANIFEST_SHA = '9a142db7bd88a221cfe171bc52111eb21e061b0d8b4b3fb92ebd0378e9612619'
LOG = []
_rows = []
_accepted = set()


def _load():
    if not _rows:
        raw = open(MANIFEST, 'rb').read()
        if hashlib.sha256(raw).hexdigest() != MANIFEST_SHA:
            raise SystemExit('acc2: the item manifest does not match its pin')
        rows = {}
        for ln in raw.decode('utf-8').split('\n')[1:]:
            if ln:
                f = ln.split('\t')
                rows[f[0]] = {'orig_sha': f[1], 'cleaned_sha': f[2], 't': f[3], 'p': f[4], 'producer': f[5]}
        _rows.append(rows)
    return _rows[0]


def _rel(path):
    return os.path.relpath(os.path.abspath(path), ROOT)


def _carried(path, original):
    """True iff path is a carried-over item of the original producer whose bytes equal its manifest row."""
    if path is None or original is None:
        return False
    row = _load().get(_rel(path))
    if row is None or row['producer'] != original:
        return False
    try:
        data = open(path, 'rb').read()
    except OSError:
        return False
    return hashlib.sha256(data).hexdigest() == row['cleaned_sha']


def ok(path, named, cleaned, original):
    """True iff the item at path names the cleaned producer, or names the original producer and is a carried-over item."""
    if named == cleaned:
        LOG.append(('cleaned', _rel(path) if path else '-', named))
        return True
    if named == original and _carried(path, original):
        LOG.append(('original', _rel(path), named))
        _accepted.add((cleaned, original))
        return True
    LOG.append(('refused', _rel(path) if path else '-', str(named)))
    return False


def expect(path, cleaned, original):
    """the producer sha256 a reader should require of the item at path: the original one for a carried-over item, else the cleaned one."""
    if _carried(path, original):
        LOG.append(('original', _rel(path), original))
        _accepted.add((cleaned, original))
        return original
    LOG.append(('cleaned', _rel(path), cleaned))
    return cleaned


def out(path, cleaned, original):
    """a producer record (its first line names 'script sha256 <sha>'): returns path if ok(), else raises ValueError."""
    first = open(path).readline()
    named = first.split('script sha256 ', 1)[1][:64] if 'script sha256 ' in first else None
    if not ok(path, named, cleaned, original):
        raise ValueError('producer record %s: its script sha256 is neither the cleaned producer nor a carried-over item of the original' % path)
    return path


def pair(cleaned, original):
    """the producer values a header may name in this run: the cleaned one, and the original one once a carried-over item of it was
    accepted."""
    return {cleaned, original} if (cleaned, original) in _accepted else {cleaned}


def carried(path):
    """True iff path is a carried-over item (any original producer) whose bytes equal its manifest row; for provenance fields (a
    kernel, a validation list) that a reader checks in a carried-over record."""
    row = _load().get(_rel(path)) if path else None
    try:
        ok_ = row is not None and hashlib.sha256(open(path, 'rb').read()).hexdigest() == row['cleaned_sha']
    except OSError:
        ok_ = False
    LOG.append(('carried' if ok_ else 'not-carried', _rel(path) if path else '-', row['producer'] if row else '-'))
    return ok_


def fail_unless(cond, exc):
    """raise exc unless cond (the patched form of a reader's 'raise' on a provenance mismatch)."""
    if not cond:
        raise exc


def pair_if(key, cleaned, original):
    """the values a provenance field (a kernel name and sha8, say) may hold: the cleaned one, and the original one once a carried-over
    item of the producer pair key (cleaned, original) was accepted."""
    return {cleaned, original} if key in _accepted else {cleaned}


def caller_p(depth=2):
    """the local variable p (the item path) of the frame depth levels up, for readers whose call site cannot pass it."""
    return sys._getframe(depth).f_locals.get('p')


def _write_log():
    dest = os.environ.get('ACC2_LOG')
    if dest and LOG:
        with open(dest, 'x') as fh:
            fh.write('decision\tpath\tnamed_sha256\n')
            for d, p, n in LOG:
                fh.write('%s\t%s\t%s\n' % (d, p, n))


atexit.register(_write_log)
