#!/usr/bin/env python3
"""m3_reader_cw_check_v1_1.py -- pk23 (code/pk23/pev/): the check job of the reader fork m3_reader_cw_v1 (the P0_LOG rows 4589 and 4610),
on the pattern of pk23's m3_reader_hl_check_v1.py. For N = 4 and 3: the C_w record m3_cw_LC_N<N>_J300_cw.json through the fork's load, bound
to its asm output m3_run_v1_9_3_asmc.<N>.out, and the law certificate m3_lawcert_cw_v1_N<N>.json through the fork's load_lawcert, bound to its
job's output m3_lawcert_cw_v1_<N>.out (C-LOAD-LAWCERT: producer m3_lawcert_cw_v1, 4 entries, every law's ak, ak_rad, err and parts equal its
record's). C-PINS: the fork lists m3_lawcert_cw_v1 with the file's sha256 and the family LC, and keeps its parent's producers with their sha256s
and record sets. The Pev records still load through the fork (C-PARENT-RECORDS: the hl certificate of both N). Plants (PLANT-READER-CW), each
must be refused: the producer sha256 with its last digit changed on the job's first line, the other N on the first line, the hl producer with
its own sha256 for the cw record, the record passed as family L, and a law changed with the RECORD line re-hashed. PLANT-PARENT: the parent
m3_reader_hl_v1 must refuse the cw certificate. Reads only; prints this output. Usage: m3_reader_cw_check_v1_1.py
v1_1: m3_reader_cw_check_v1.py with the LAW lines printed in exponent form (v1 cut the strings and dropped the exponents); nothing else changes."""
import copy, hashlib, importlib.util, json, os, sys
W18 = '/mnt/g2/release/root/code'
HLD = W18 + '/pk23/pev'
OUTD = HLD + '/out'
FAMS = ('LC',)
KEYS = ('C11,1,1', 'C1x,1,1', 'Cx1,1,1', 'Cxx,1,1')
J_REF = 300
FAILS, NOFIRE = [], []


def out(line):
    print(line, flush=True)


def gate(name, ok, line):
    out('%s %s -> %s' % (name, line, 'PASS' if ok else 'FAIL'))
    if not ok:
        FAILS.append(name)


def plant(name, fired, line):
    out('%s %s -> %s' % (name, line, 'FIRES' if fired else 'DOES NOT FIRE'))
    if not fired:
        NOFIRE.append(name)


def sha(path):
    with open(path, 'rb') as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def tsha(text):
    return hashlib.sha256(text.encode()).hexdigest()


def flip(h):
    return h[:-1] + ('0' if h[-1] != '0' else '1')


def load_as(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


RDR = load_as('m3_reader_cw_v1', os.path.join(HLD, 'm3_reader_cw_v1.py'))
PAR = load_as('m3_reader_hl_v1', os.path.join(HLD, 'm3_reader_hl_v1.py'))
out('m3_reader_cw_check_v1_1: fork %s, parent %s, producer %s' % (sha(os.path.join(HLD, 'm3_reader_cw_v1.py'))[:16],
                                                               sha(os.path.join(HLD, 'm3_reader_hl_v1.py'))[:16],
                                                               sha(os.path.join(HLD, 'm3_lawcert_cw_v1.py'))[:16]))
lc = sha(os.path.join(HLD, 'm3_lawcert_cw_v1.py'))
keep = all(RDR.PRODUCERS.get(k) == v for k, v in PAR.PRODUCERS.items()) and all(RDR.PRODUCER_RECORDS.get(k) == v for k, v in PAR.PRODUCER_RECORDS.items())
gate('C-PINS', RDR.PRODUCERS.get('m3_lawcert_cw_v1.py') == lc and RDR.PRODUCER_RECORDS.get('m3_lawcert_cw_v1.py') == ('m3_cw_', '_J300_cw.json', FAMS)
     and keep and len(RDR.PRODUCERS) == len(PAR.PRODUCERS) + 1 and len(RDR.PRODUCER_RECORDS) == len(PAR.PRODUCER_RECORDS) + 1,
     '(the fork lists m3_lawcert_cw_v1 %s with prefix m3_cw_, suffix _J300_cw.json and family %s; the parent\'s %d producers kept)' % (
         lc[:16], ', '.join(FAMS), len(PAR.PRODUCERS)))


def refused(fn):
    try:
        fn()
        return False
    except Exception:
        return True


for N in (4, 3):
    asm = os.path.join(OUTD, 'm3_run_v1_9_3_asmc.%d.out' % N)
    rpath = os.path.join(OUTD, 'm3_cw_LC_N%d_J300_cw.json' % N)
    recs = {'LC': RDR.load(rpath, asm, J_REF, N)}
    cpath, opath = os.path.join(OUTD, 'm3_lawcert_cw_v1_N%d.json' % N), os.path.join(OUTD, 'm3_lawcert_cw_v1_%d.out' % N)
    cert = RDR.load_lawcert(cpath, opath, J_REF, N, recs)
    ents = cert['entries']
    same = sorted(ents) == ['LC:%s' % k for k in KEYS]
    for k in KEYS:
        law, rl = RDR.entry_law(cert, 'LC', k), recs['LC']['laws'][k]
        same = same and law is not None and law['parity'] == 'free' and law['laws'] is not None and all(law[x] == rl[x] for x in ('ak', 'ak_rad', 'err', 'parts', 'laws'))
    gate('C-LOAD-LAWCERT', cert['producer'] == 'm3_lawcert_cw_v1.py' and len(ents) == 4 and same,
         '(N=%d: %s through load_lawcert bound to %s: producer %s, %d entries %s, each free with its record\'s ak, ak_rad, err, parts and laws)' % (
             N, os.path.basename(cpath), os.path.basename(opath), cert['producer'], len(ents), ', '.join(sorted(ents))))
    for k in KEYS:
        e = ents['LC:' + k]
        out('LAW N=%d LC:%s: ak %s ak_rad %s parts %s far_rate %s' % (N, k, ['%.12e' % float(x) for x in e['ak']], ['%.3e' % float(x) for x in e['ak_rad']],
                                                                    dict((p, '%.3e' % float(v)) for p, v in e['parts'].items()), '%.8f' % float(e['laws']['far_rate'])))
    hasm = os.path.join(OUTD, 'm3_run_v1_9_3_asm.%d.out' % N)
    hrecs = dict((f, RDR.load(os.path.join(OUTD, 'm3_hl_%s_N%d_J300_hl.json' % (f, N)), hasm, J_REF, N)) for f in ('L', 'LH', 'LT'))
    hcert = RDR.load_lawcert(os.path.join(OUTD, 'm3_lawcert_hl_v1_1_N%d.json' % N), os.path.join(OUTD, 'm3_lawcert_hl_v1_1_%d.out' % N), J_REF, N, hrecs)
    gate('C-PARENT-RECORDS', hcert['producer'] == 'm3_lawcert_hl_v1_1.py' and len(hcert['entries']) == 6,
         '(N=%d: the hl certificate still loads through the fork: producer %s, %d entries)' % (N, hcert['producer'], len(hcert['entries'])))
    text = open(cpath).read()
    otext = open(opath).read()
    first, rest = otext.split('\n', 1)
    plant('PLANT-READER-CW', refused(lambda: RDR.loads_lawcert(text, first.replace(lc, flip(lc)) + '\n' + rest, J_REF, N, recs, os.path.basename(cpath))),
          '(N=%d: the producer sha256 with its last digit changed must be refused)' % N)
    plant('PLANT-READER-CW', refused(lambda: RDR.loads_lawcert(text, first.replace(' N %d ' % N, ' N %d ' % (7 - N), 1) + '\n' + rest, J_REF, N, recs,
                                                               os.path.basename(cpath))), '(N=%d: the other N on the first line must be refused)' % N)
    hl = RDR.PRODUCERS['m3_lawcert_hl_v1_1.py']
    plant('PLANT-READER-CW', refused(lambda: RDR.loads_lawcert(text, first.replace('m3_lawcert_cw_v1 ', 'm3_lawcert_hl_v1_1 ', 1).replace(lc, hl) + '\n' + rest,
                                                               J_REF, N, recs, os.path.basename(cpath))),
          '(N=%d: the hl producer with its own sha256 for the cw record must be refused)' % N)
    plant('PLANT-READER-CW', refused(lambda: RDR.loads_lawcert(text, otext, J_REF, N, {'L': recs['LC']}, os.path.basename(cpath))),
          '(N=%d: the record passed as family L must be refused)' % N)
    c2 = json.loads(text)
    k0 = sorted(c2['entries'])[0]
    c2['entries'][k0]['laws']['rem_tpow'] = 5 if c2['entries'][k0]['laws'].get('rem_tpow') != 5 else 6
    t2 = json.dumps(c2, sort_keys=True)
    o2 = otext.replace(tsha(text), tsha(t2))
    plant('PLANT-READER-CW', refused(lambda: RDR.loads_lawcert(t2, o2, J_REF, N, recs, os.path.basename(cpath))),
          '(N=%d: a law changed with the RECORD line re-hashed must be refused)' % N)
    c3 = json.loads(text)
    c3['entries'][k0]['laws']['far_rate'] = str(2 * RDR.Fraction(c3['entries'][k0]['laws']['far_rate']))
    t3 = json.dumps(c3, sort_keys=True)
    o3 = otext.replace(tsha(text), tsha(t3))
    plant('PLANT-READER-CW', refused(lambda: RDR.loads_lawcert(t3, o3, J_REF, N, recs, os.path.basename(cpath))),
          '(N=%d: a doubled far rate with the RECORD line re-hashed must be refused)' % N)
    plant('PLANT-PARENT', refused(lambda: PAR.load_lawcert(cpath, opath, J_REF, N, {'LC': PAR.load(rpath, asm, J_REF, N)})),
          '(N=%d: the parent m3_reader_hl_v1 must refuse the cw certificate)' % N)
out('VERDICT %s' % ('VALID' if not FAILS and not NOFIRE else 'INVALID (%s)' % ', '.join(FAILS + ['%s did not fire' % p for p in NOFIRE])))
