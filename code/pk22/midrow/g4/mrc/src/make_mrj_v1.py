#!/usr/bin/env python3
"""make_mrj_v1.py (pk22; MR_JOINT, the rows 4489-4494): writes (mode 'x') midrow/g4/mrc/src/mrj_cert_v1.py from the template
mrj_cert_v1.tmpl.py by filling its pin tokens @@...@@ with full sha256s computed here from the files, each checked against the sha8 the producer's
tool outputs gave and, where a producer's manifest lists the file, against that manifest's line. No hash is typed in the template or here."""
import hashlib, os

W = '/mnt/g2/release/root/code'
D = W + '/pk22/midrow/g4/mrc/src'
TPL, DST = D + '/mrj_cert_v1.tmpl.py', D + '/mrj_cert_v1.py'
M3O, MYO, S9H = W + '/pk03/out', W + '/pk22/m3/out', W + '/pk25'
PINS = {   # token: (file, sha8 from the producer's tool outputs, (manifest, its listing key) or None)
    'MAN3': (S9H + '/mr/MANIFEST_C6A_CERT_v3.sha256', '6c864119', None),
    'MAN4': (S9H + '/mr/MANIFEST_MR_V4_CERT_v1.sha256', '9cf8e6d2', None),
    'S9_4': (M3O + '/m3_s9_N4_J300_v1_8_3.json', 'bcc6434c', None),
    'S9_3': (M3O + '/m3_s9_N3_J300_v1_8_3.json', 'd287d3dc', None),
    'DJ_4': (MYO + '/m3_c3j_DJ_N4_J300_c3j.json', '290d2142', (W + '/pk22/midrow/g4/MANIFEST_G7_C3J_v1.sha256', MYO + '/m3_c3j_DJ_N4_J300_c3j.json')),
    'DJ_3': (MYO + '/m3_c3j_DJ_N3_J300_c3j.json', 'ac33223f', (W + '/pk22/midrow/g4/MANIFEST_G7_C3J_v1.sha256', MYO + '/m3_c3j_DJ_N3_J300_c3j.json')),
    'DH_4': (S9H + '/m3/out/m3_s9h_DH_N4_J300_v1.json', 'e02852c2', (S9H + '/MANIFEST_S9H_PROD_v1.sha256', 'm3/out/m3_s9h_DH_N4_J300_v1.json')),
    'DH_3': (S9H + '/m3/out/m3_s9h_DH_N3_J300_v1.json', '9248b118', (S9H + '/MANIFEST_S9H_PROD_v1.sha256', 'm3/out/m3_s9h_DH_N3_J300_v1.json')),
    'JF_4': (W + '/pk22/midrow/g4/mrx/out/joint_float_v1_n4.out', '1a8a4890', None),
    'JF_3': (W + '/pk22/midrow/g4/mrx/out/joint_float_v1_n3.out', 'bdefb6c5', None),
}


def sha(p):
    with open(p, 'rb') as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def manifest(p):
    acc = {}
    for ln in open(p):
        if ln.strip():
            h_, p_ = ln.rstrip('\n').split('  ', 1)
            acc[p_] = h_
    return acc


assert os.path.dirname(DST) == os.path.dirname(os.path.abspath(__file__)) and not os.path.exists(DST), DST
st = sha(TPL)
print('TEMPLATE %s %s' % (st, TPL))
with open(TPL) as fh:
    T = fh.read()
for tok, (p, s8, man) in PINS.items():
    h = sha(p)
    assert h.startswith(s8), (tok, h)
    if man is not None:
        assert manifest(man[0]).get(man[1]) == h, (tok, 'manifest')
    n = T.count('@@%s@@' % tok)
    assert n == 1, (tok, n)
    T = T.replace('@@%s@@' % tok, h)
    print('PIN %s %s %s%s' % (tok, h, p, (' (listed so in %s)' % os.path.basename(man[0])) if man else ''))
assert '@@' not in T
with open(DST, 'x') as fh:
    fh.write(T)
print('WROTE %s %s' % (hashlib.sha256(T.encode('utf-8')).hexdigest(), DST))
