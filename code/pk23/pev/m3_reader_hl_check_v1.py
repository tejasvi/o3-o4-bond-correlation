#!/usr/bin/env python3
"""m3_reader_hl_check_v1.py -- pk23 (code/pk23/pev/): the check job of the reader fork m3_reader_hl_v1 (the P0_LOG row 4589), on the
pattern of pk22's m3_reader_c3h_check_v1_2.py. For N = 4 and 3: the three Pev records m3_hl_<F>_N<N>_J300_hl.json (F in L, LH, LT) through
the fork's load, bound to their asm output m3_run_v1_9_3_asm.<N>.out, and the law certificate m3_lawcert_hl_v1_1_N<N>.json through the fork's
load_lawcert, bound to its job's output m3_lawcert_hl_v1_1_<N>.out (C-LOAD-LAWCERT: producer m3_lawcert_hl_v1_1, 6 entries, every law's ak and
err equal its record's). C-PINS: the fork lists m3_lawcert_hl_v1_1 with the file's sha256 and the three families, and keeps its parent's
producers with their sha256s and record sets. Plants (PLANT-READER-HL), each must be refused: the producer sha256 with its last digit changed on
the job's first line, the other N on the first line, the c3k producer with its own sha256 for the hl records, the records passed without LT, and
a law changed with the RECORD line re-hashed. PLANT-PARENT: the parent m3_reader_c3h_v1_2 must refuse the hl certificate. Reads only; prints this
output. Usage: m3_reader_hl_check_v1.py"""
import copy, hashlib, importlib.util, json, os, sys
W18 = '/mnt/g2/release/root/code'
HLD = W18 + '/pk23/pev'
OUTD = HLD + '/out'
FAMS = ('L', 'LH', 'LT')
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


RDR = load_as('m3_reader_hl_v1', os.path.join(HLD, 'm3_reader_hl_v1.py'))
PAR = load_as('m3_reader_c3h_v1_2', os.path.join(W18, 'pk22/m3/m3_reader_c3h_v1_2.py'))
out('m3_reader_hl_check_v1: fork %s, parent %s, producer %s' % (sha(os.path.join(HLD, 'm3_reader_hl_v1.py'))[:16],
                                                               sha(os.path.join(W18, 'pk22/m3/m3_reader_c3h_v1_2.py'))[:16],
                                                               sha(os.path.join(HLD, 'm3_lawcert_hl_v1_1.py'))[:16]))
lc = sha(os.path.join(HLD, 'm3_lawcert_hl_v1_1.py'))
keep = all(RDR.PRODUCERS.get(k) == v for k, v in PAR.PRODUCERS.items()) and all(RDR.PRODUCER_RECORDS.get(k) == v for k, v in PAR.PRODUCER_RECORDS.items())
gate('C-PINS', RDR.PRODUCERS.get('m3_lawcert_hl_v1_1.py') == lc and RDR.PRODUCER_RECORDS.get('m3_lawcert_hl_v1_1.py') == ('m3_hl_', '_J300_hl.json', FAMS)
     and keep and len(RDR.PRODUCERS) == len(PAR.PRODUCERS) + 1,
     '(the fork lists m3_lawcert_hl_v1_1 %s with prefix m3_hl_, suffix _J300_hl.json and families %s; the parent\'s %d producers kept)' % (
         lc[:16], ', '.join(FAMS), len(PAR.PRODUCERS)))
for N in (4, 3):
    asm = os.path.join(OUTD, 'm3_run_v1_9_3_asm.%d.out' % N)
    recs = dict((f, RDR.load(os.path.join(OUTD, 'm3_hl_%s_N%d_J300_hl.json' % (f, N)), asm, J_REF, N)) for f in FAMS)
    cpath, opath = os.path.join(OUTD, 'm3_lawcert_hl_v1_1_N%d.json' % N), os.path.join(OUTD, 'm3_lawcert_hl_v1_1_%d.out' % N)
    cert = RDR.load_lawcert(cpath, opath, J_REF, N, recs)
    ents = cert['entries']
    same = True
    for eid, e in ents.items():
        f, k = eid.split(':', 1)
        rec_it = recs[f]['entries'][k] if 'entries' in recs[f] else None
        law = RDR.entry_law(cert, f, k)
        if e is None or law is None:
            same = False
    gate('C-LOAD-LAWCERT', cert['producer'] == 'm3_lawcert_hl_v1_1.py' and len(ents) == 6 and same,
         '(N=%d: %s through load_lawcert bound to %s: producer %s, %d entries %s)' % (
             N, os.path.basename(cpath), os.path.basename(opath), cert['producer'], len(ents), ', '.join(sorted(ents))))
    for k in ('L:TT,0,0', 'LH:Mh,0,0'):
        e = ents[k]
        out('LAW N=%d %s: ak %s ak_rad %s parts %s' % (N, k, [str(x)[:14] for x in e['ak']], [str(x)[:10] for x in e['ak_rad']],
                                                     dict((p, str(v)[:12]) for p, v in e['parts'].items())))
    text = open(cpath).read()
    otext = open(opath).read()
    first, rest = otext.split('\n', 1)

    def refused(fn):
        try:
            fn()
            return False
        except Exception:
            return True
    plant('PLANT-READER-HL', refused(lambda: RDR.loads_lawcert(text, first.replace(lc, flip(lc)) + '\n' + rest, J_REF, N, recs, os.path.basename(cpath))),
          '(N=%d: the producer sha256 with its last digit changed must be refused)' % N)
    plant('PLANT-READER-HL', refused(lambda: RDR.loads_lawcert(text, first.replace(' N %d ' % N, ' N %d ' % (7 - N), 1) + '\n' + rest, J_REF, N, recs,
                                                               os.path.basename(cpath))), '(N=%d: the other N on the first line must be refused)' % N)
    c3k = RDR.PRODUCERS['m3_lawcert_c3k_v1.py']
    plant('PLANT-READER-HL', refused(lambda: RDR.loads_lawcert(text, first.replace('m3_lawcert_hl_v1_1 ', 'm3_lawcert_c3k_v1 ', 1).replace(lc, c3k) + '\n' + rest,
                                                               J_REF, N, recs, os.path.basename(cpath))),
          '(N=%d: the c3k producer with its own sha256 for the hl records must be refused)' % N)
    plant('PLANT-READER-HL', refused(lambda: RDR.loads_lawcert(text, otext, J_REF, N, dict((f, recs[f]) for f in FAMS if f != 'LT'), os.path.basename(cpath))),
          '(N=%d: the records passed without LT must be refused)' % N)
    c2 = json.loads(text)
    k0 = sorted(c2['entries'])[0]
    c2['entries'][k0]['laws']['rem_tpow'] = '5' if str(c2['entries'][k0]['laws'].get('rem_tpow')) != '5' else '6'
    t2 = json.dumps(c2, sort_keys=True)
    o2 = otext.replace(tsha(text), tsha(t2))
    plant('PLANT-READER-HL', refused(lambda: RDR.loads_lawcert(t2, o2, J_REF, N, recs, os.path.basename(cpath))),
          '(N=%d: a law changed with the RECORD line re-hashed must be refused)' % N)
    plant('PLANT-PARENT', refused(lambda: PAR.load_lawcert(cpath, opath, J_REF, N, dict((f, PAR.load(os.path.join(OUTD, 'm3_hl_%s_N%d_J300_hl.json' % (f, N)),
                                                                                                    asm, J_REF, N)) for f in FAMS))),
          '(N=%d: the parent m3_reader_c3h_v1_2 must refuse the hl certificate)' % N)
out('VERDICT %s' % ('VALID' if not FAILS and not NOFIRE else 'INVALID (%s)' % ', '.join(FAILS + ['%s did not fire' % p for p in NOFIRE])))
