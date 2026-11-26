#!/usr/bin/env python3
"""SCRATCH (pk02, hand): kit c for the trade-fix asm (draft f). Fills every '@@SHA:<path>@@' token (path relative to the own folder) with
the file's sha256, the '#@PIECEPINS@' line with the 20 piece records and 20 hand-offs of the PRODUCER map (m2b_cert_v1_4 for d5, dwt,
dwl, r0, tA; m2b_cert_v1_1 otherwise), and '@@RHOPPHEX@@' with the one rho_pp_hex of the 20 hand-off HEADs (field 19); never typed.
argv: draft path, output path (a new file in the own folder). Prints the sha8 of the pk03 pins for the comparison with its message."""
import sys, os, hashlib, re

CODEDIR = '/mnt/g2/release/root/code'
OWN = os.path.join(CODEDIR, 'pk02')
draft, outp = sys.argv[1], sys.argv[2]
if not (len(sys.argv) == 3 and os.path.dirname(os.path.realpath(outp)) == os.path.realpath(OWN) and not os.path.exists(outp) and
        os.path.realpath(outp) != os.path.realpath(draft)):
    raise SystemExit('usage: draft out (a new file in the own folder, not the draft)')


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
pieces = ('x', 'd5', 'dwt', 'dwl', 'r0', 'tX0', 'tX1', 'tX2', 'tB', 'tA')
lines, hexes = [], set()
for n in (4, 3):
    for pc in pieces:
        prod = 'm2b_cert_v1_4' if pc in ('d5', 'dwt', 'dwl', 'r0', 'tA') else 'm2b_cert_v1_1'
        for nm in ('out_%s_%s.n%d.out' % (prod, pc, n), 'hand_%s_%s.n%d.txt' % (prod, pc, n)):
            lines.append("    'pk02/%s': '%s'," % (nm, sha(os.path.join(OWN, nm))))
        head = open(os.path.join(OWN, 'hand_%s_%s.n%d.txt' % (prod, pc, n))).readline().split()
        if not (len(head) == 19 and head[1] == prod and head[17] == 'rho_pp_hex'):
            raise SystemExit('hand-off %s %s n%d: HEAD' % (prod, pc, n))
        hexes.add(head[18])
if len(hexes) != 1:
    raise SystemExit('the hand-offs carry %d rho_pp_hex values' % len(hexes))
subs['@@RHOPPHEX@@'] = hexes.pop()
out = []
for ln in src.split('\n'):
    if ln == '#@PIECEPINS@':
        out.extend(lines)
        continue
    for k, v in subs.items():
        ln = ln.replace(k, v)
    out.append(ln)
text = '\n'.join(out)
left = sorted(set(re.findall(r'@@[^@]*@@', text)))
if left or '#@PIECEPINS@' in text:
    raise SystemExit('placeholders left: %s' % left)
with open(outp, 'x') as fh:
    fh.write(text)
for k in sorted(subs):
    if 'pk03' in k:
        print('M3PIN %s %s' % (k[6:-2], subs[k][:8]))
print('wrote %s: %d sha pins, %d piece files, rho_pp_hex %s, sha256 %s' % (os.path.basename(outp), len(subs) - 1, len(lines),
                                                                          subs['@@RHOPPHEX@@'], hashlib.sha256(text.encode()).hexdigest()))
