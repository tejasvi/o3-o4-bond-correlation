#!/usr/bin/env python3
"""SCRATCH (pk02, hand): fills every '@@SHA:<path>@@' token of a draft (path relative to the own folder) with the file's sha256 (never
typed) and writes the frozen candidate; refuses any other '@@...@@' left. argv: draft path, output path (a new file in the own folder)."""
import sys, os, hashlib, re

CODEDIR = '/mnt/g2/release/root/code'
OWN = os.path.join(CODEDIR, 'pk02')
if len(sys.argv) != 3:
    raise SystemExit('usage: draft out')
draft, outp = sys.argv[1], sys.argv[2]
if not (os.path.dirname(os.path.realpath(outp)) == os.path.realpath(OWN) and not os.path.exists(outp) and
        os.path.realpath(outp) != os.path.realpath(draft)):
    raise SystemExit('out must be a new file in the own folder, not the draft')


def sha(path):
    with open(path, 'rb') as fh:
        return hashlib.sha256(fh.read()).hexdigest()


src = open(draft).read()
subs = {}
for tok in sorted(set(re.findall(r'@@SHA:([^@]+)@@', src))):
    p = os.path.normpath(os.path.join(OWN, tok))
    if not (p.startswith(CODEDIR + os.sep) and os.path.isfile(p)):
        raise SystemExit('pin %s: no such file under code' % tok)
    subs['@@SHA:%s@@' % tok] = sha(p)
text = src
for k, v in subs.items():
    text = text.replace(k, v)
left = sorted(set(re.findall(r'@@[^@]*@@', text)))
if left:
    raise SystemExit('placeholders left: %s' % left)
with open(outp, 'x') as fh:
    fh.write(text)
for k in sorted(subs):
    print('PIN %s %s' % (k[6:-2], subs[k][:8]))
print('wrote %s: %d sha pins, sha256 %s' % (os.path.basename(outp), len(subs), hashlib.sha256(text.encode()).hexdigest()))
