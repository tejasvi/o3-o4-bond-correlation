#!/usr/bin/env python3
"""make_rcc_v1_3.py (pk22, phase (iii), NE's certified RC engine, the pins-only revision): writes pk22/w1/rc_cert/kt_s8h_rcc_v1_3.py
from kt_s8h_rcc_v1_2.py (sha256 1a04598f...) by exact replacements with asserted counts, as a new file (mode 'x'). It fills CERT_PINS
with runner c3_1's records m3_c3_<CS4|CE3|H4T>_N<4|3>_J300_c3.json and their asm outputs m3_run_v1_9_3_asm.<4|3>.out (pk22/m3/out), by
full sha256, after checking each record against its asm output: VERDICT lines exactly [VERDICT VALID] and exactly one RECORD line naming
the record with its sha256 (the bound reader's rule). It also changes the label, the usage strings and the docstring's first line, and
adds one docstring line naming this revision; nothing else changes (the diff shows it). Prints every sha256. Usage: make_rcc_v1_3.py."""
import hashlib, os
B = '/mnt/g2/release/root/code/pk22'
TOP = B + '/w1/rc_cert'
SRC, DST = TOP + '/kt_s8h_rcc_v1_2.py', TOP + '/kt_s8h_rcc_v1_3.py'
M3O = B + '/m3/out'
C3G = ('CS4', 'CE3', 'H4T')


def sha(b):
    return hashlib.sha256(b).hexdigest()


def fsha(p):
    with open(p, 'rb') as fh:
        return sha(fh.read())


def rep(t, old, new, count, label):
    n = t.count(old)
    assert n == count, 'replacement %s: %d occurrences, expected %d' % (label, n, count)
    print('REPLACE %s: %d occurrence(s)' % (label, n))
    return t.replace(old, new)


assert os.path.dirname(os.path.abspath(DST)) == TOP and not os.path.exists(DST), DST
ssha = fsha(SRC)
print('SOURCE %s %s' % (ssha, SRC))
assert ssha.startswith('0a01aacb'), ssha
pins = []
for n in (4, 3):
    asm = os.path.join(M3O, 'm3_run_v1_9_3_asm.%d.out' % n)
    with open(asm) as fh:
        ls = fh.read().split('\n')
    assert [x for x in ls if x.startswith('VERDICT')] == ['VERDICT VALID'], (asm, 'VERDICT')
    ah = fsha(asm)
    for g in C3G:
        name = 'm3_c3_%s_N%d_J300_c3.json' % (g, n)
        rh = fsha(os.path.join(M3O, name))
        hit = [x.split() for x in ls if x.startswith('RECORD ') and len(x.split()) == 3 and x.split()[1] == name]
        assert hit == [['RECORD', name, rh]], (name, hit)
        print('PIN %s %s (bound: asm.%d RECORD line)' % (name, rh, n))
        pins.append("C3REC[%d]['%s']: '%s'" % (n, g, rh))
    print('PIN %s %s' % (os.path.basename(asm), ah))
    pins.append("C3ASM[%d]: '%s'" % (n, ah))
with open(SRC, 'rb') as fh:
    t = fh.read().decode('utf-8')
t = rep(t, '"""kt_s8h_rcc_v1_2.py -- pk22', '"""kt_s8h_rcc_v1_3.py -- pk22', 1, 'docstring name')
t = rep(t, 'v1_2 (this revision of v1_1, 26e64080:',
        'v1_3 (the pins-only revision of v1_2, 1a04598f, by make_rcc_v1_3.py): CERT_PINS holds runner c3_1\'s records and asm outputs of\n'
        'both N by full sha256; nothing else changes. v1_2 (the revision of v1_1, 26e64080:', 1, 'docstring v1_3 line')
t = rep(t, 'Usage: kt_s8h_rcc_v1_2.py cert|dev', 'Usage: kt_s8h_rcc_v1_3.py cert|dev', 1, 'docstring usage')
t = rep(t, "USAGE = 'usage: kt_s8h_rcc_v1_2.py", "USAGE = 'usage: kt_s8h_rcc_v1_3.py", 1, 'USAGE')
t = rep(t, "LABEL = 'kt_s8h_rcc_v1_2'", "LABEL = 'kt_s8h_rcc_v1_3'", 1, 'LABEL')
t = rep(t, "CERT_PINS = {}   # runner c3's records and asm outputs by full sha256: a pins-only revision after c3's production fills these",
        "CERT_PINS = {%s}   # runner c3_1's records and asm outputs by full sha256 (make_rcc_v1_3.py)" % ', '.join(pins), 1, 'CERT_PINS')
nb = t.encode('utf-8')
with open(DST, 'xb') as fh:
    fh.write(nb)
print('ENGINE %s %s' % (sha(nb), DST))
