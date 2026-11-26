#!/usr/bin/env python3
"""stage_certset_v1.py (pk24; M1's certified run, the rows 4446, 4505, 4520): copies the five certified MR_INPUT records byte for byte
into a new record directory under pk24 as MR_SPECTRAL.kv, MR_INSERT.kv, MR_EXACT.kv, MR_CRUDEX.kv and MR_JOINT.kv, checks every copy's
sha256 against its source (and against an expected sha8 when one is given as PATH:SHA8), writes PINS.txt in the engine's form and prints each
record's sha256, its header's PRODUCER, EXPORT_STATUS and RUN_VERDICT, and PINS.txt's sha256. Nothing is changed in any record.
Usage: stage_certset_v1.py OUTDIR SPECTRAL INSERT EXACT CRUDEX JOINT (each a code-relative path, optionally :SHA8)"""
import hashlib, os, sys

W = '/mnt/g2/release/root/code/'
RECS = ('MR_SPECTRAL', 'MR_INSERT', 'MR_EXACT', 'MR_CRUDEX', 'MR_JOINT')


def sha_b(b):
    return hashlib.sha256(b).hexdigest()


def head(b):
    h = {}
    for ln in b.decode().splitlines():
        if ln.startswith('FIELDS = '):
            break
        if ' = ' in ln and not ln.startswith('#'):
            k, v = ln.split(' = ', 1)
            h[k.strip()] = v.strip()
    return h


def main():
    out = sys.argv[1]
    args = sys.argv[2:7]
    assert len(args) == 5, 'five record paths'
    assert os.path.realpath(out).startswith(W + 'pk24/') and not os.path.exists(out), out
    os.mkdir(out)
    pins = []
    for rec, a in zip(RECS, args):
        path, s8 = (a.split(':', 1) + [None])[:2]
        b = open(W + path, 'rb').read()
        s = sha_b(b)
        assert s8 is None or s.startswith(s8), (rec, path, s[:8], s8)
        dst = os.path.join(out, rec + '.kv')
        with open(dst, 'xb') as fh:
            fh.write(b)
        assert sha_b(open(dst, 'rb').read()) == s, (rec, 'copy differs')
        h = head(b)
        assert h.get('RECORD') == rec, (rec, h.get('RECORD'))
        print('STAGE %s %s from %s | PRODUCER %s | %s/%s | %s' % (rec, s, path, h.get('PRODUCER'), h.get('EXPORT_STATUS'), h.get('RUN_VERDICT'),
                                                              h.get('FORMAT')))
        pins.append('%s  %s.kv\n' % (s, rec))
    with open(os.path.join(out, 'PINS.txt'), 'x') as fh:
        fh.write(''.join(pins))
    print('PINS %s %s' % (sha_b(open(os.path.join(out, 'PINS.txt'), 'rb').read()), os.path.join(out, 'PINS.txt').replace(W, '')))
    return 0


if __name__ == '__main__':
    sys.exit(main())
