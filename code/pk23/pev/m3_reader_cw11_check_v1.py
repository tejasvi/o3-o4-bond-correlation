#!/usr/bin/env python3
"""m3_reader_cw11_check_v1.py -- pk23 (code/pk23/pev/): the check job of the reader fork m3_reader_cw_v1_1 (pk22's producer
m3_lawcert_c3k_v2 for the c3kp records), on the pattern of m3_reader_cw_check_v1_1.py. For N = 4 and 3: the two c3kp records
m3_c3kp_<F>_N<N>_J300_c3kp.json (F in E4D, E4N) through the fork's load, bound to their asm output m3_run_v1_9_3_asm.<N>_c3k2.out, and the law
certificate m3_lawcert_c3k_v2_N<N>.json through the fork's load_lawcert, bound to its job's output m3_lawcert_c3k_v2_<N>.out (C-LOAD-LAWCERT:
producer m3_lawcert_c3k_v2, every entry of both records, each with its record's ak, ak_rad, err, parts and laws; the IhR,10,b entries free).
C-PINS: the fork lists m3_lawcert_c3k_v2 with the file's sha256 and the families E4D, E4N, and keeps its parent's producers with their sha256s
and record sets. C-PARENT-RECORDS: pk23's cw certificate still loads through the fork. Plants (PLANT-READER-CW11), each must be refused: the
producer sha256 with its last digit changed on the job's first line, the other N on the first line, the cw producer with its own sha256 for the
c3kp records, the records passed without E4D, and a law changed with the RECORD line re-hashed. PLANT-PARENT: the parent m3_reader_cw_v1 must
refuse the c3kp certificate. Reads only; prints this output. Usage: m3_reader_cw11_check_v1.py"""
import hashlib, importlib.util, json, os, sys
W18 = '/mnt/g2/release/root/code'
HLD = W18 + '/pk23/pev'
S3, S3O = W18 + '/pk22/m3', W18 + '/pk22/m3/out'
FAMS = ('E4D', 'E4N')
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


def refused(fn):
    try:
        fn()
        return False
    except Exception:
        return True


RDR = load_as('m3_reader_cw_v1_1', os.path.join(HLD, 'm3_reader_cw_v1_1.py'))
PAR = load_as('m3_reader_cw_v1', os.path.join(HLD, 'm3_reader_cw_v1.py'))
lc = sha(os.path.join(S3, 'm3_lawcert_c3k_v2.py'))
out('m3_reader_cw11_check_v1: fork %s, parent %s, producer %s' % (sha(os.path.join(HLD, 'm3_reader_cw_v1_1.py'))[:16],
                                                                 sha(os.path.join(HLD, 'm3_reader_cw_v1.py'))[:16], lc[:16]))
keep = all(RDR.PRODUCERS.get(k) == v for k, v in PAR.PRODUCERS.items()) and all(RDR.PRODUCER_RECORDS.get(k) == v for k, v in PAR.PRODUCER_RECORDS.items())
gate('C-PINS', RDR.PRODUCERS.get('m3_lawcert_c3k_v2.py') == lc and RDR.PRODUCER_RECORDS.get('m3_lawcert_c3k_v2.py') == ('m3_c3kp_', '_J300_c3kp.json', FAMS)
     and keep and len(RDR.PRODUCERS) == len(PAR.PRODUCERS) + 1 and len(RDR.PRODUCER_RECORDS) == len(PAR.PRODUCER_RECORDS) + 1,
     '(the fork lists m3_lawcert_c3k_v2 %s with prefix m3_c3kp_, suffix _J300_c3kp.json and families %s; the parent\'s %d producers kept)' % (
         lc[:16], ', '.join(FAMS), len(PAR.PRODUCERS)))
for N in (4, 3):
    asm = os.path.join(S3O, 'm3_run_v1_9_3_asm.%d_c3k2.out' % N)
    recs = dict((f, RDR.load(os.path.join(S3O, 'm3_c3kp_%s_N%d_J300_c3kp.json' % (f, N)), asm, J_REF, N)) for f in FAMS)
    cpath, opath = os.path.join(S3O, 'm3_lawcert_c3k_v2_N%d.json' % N), os.path.join(S3O, 'm3_lawcert_c3k_v2_%d.out' % N)
    cert = RDR.load_lawcert(cpath, opath, J_REF, N, recs)
    ents = cert['entries']
    want = sorted('%s:%s' % (f, k) for f in FAMS for k in recs[f]['laws'])
    same = sorted(ents) == want
    for eid in want:
        f, k = eid.split(':', 1)
        law, rl = RDR.entry_law(cert, f, k), recs[f]['laws'][k]
        same = same and all(law[x] == rl[x] for x in ('ak', 'ak_rad', 'err', 'parts', 'laws', 'parity'))
    free = all(RDR.entry_law(cert, 'E4N', 'IhR,10,%d' % b)['parity'] == 'free' for b in (0, 1, 3))
    gate('C-LOAD-LAWCERT', cert['producer'] == 'm3_lawcert_c3k_v2.py' and same and free,
         '(N=%d: %s through load_lawcert bound to %s: producer %s, %d entries, each with its record\'s ak, ak_rad, err, parts and laws; IhR,10,b free)' % (
             N, os.path.basename(cpath), os.path.basename(opath), cert['producer'], len(ents)))
    for b in (0, 1, 3):
        e = ents['E4N:IhR,10,%d' % b]
        out('LAW N=%d E4N:IhR,10,%d: ak %s ak_rad %s parts %s' % (N, b, ['%.12e' % float(x) for x in e['ak']], ['%.3e' % float(x) for x in e['ak_rad']],
                                                                   dict((p, '%.3e' % float(v)) for p, v in e['parts'].items())))
    hasm = os.path.join(HLD, 'out', 'm3_run_v1_9_3_asmc.%d.out' % N)
    hrecs = {'LC': RDR.load(os.path.join(HLD, 'out', 'm3_cw_LC_N%d_J300_cw.json' % N), hasm, J_REF, N)}
    hcert = RDR.load_lawcert(os.path.join(HLD, 'out', 'm3_lawcert_cw_v1_N%d.json' % N), os.path.join(HLD, 'out', 'm3_lawcert_cw_v1_%d.out' % N), J_REF, N, hrecs)
    gate('C-PARENT-RECORDS', hcert['producer'] == 'm3_lawcert_cw_v1.py' and len(hcert['entries']) == 4,
         '(N=%d: the cw certificate still loads through the fork: producer %s, %d entries)' % (N, hcert['producer'], len(hcert['entries'])))
    text = open(cpath).read()
    otext = open(opath).read()
    first, rest = otext.split('\n', 1)
    plant('PLANT-READER-CW11', refused(lambda: RDR.loads_lawcert(text, first.replace(lc, flip(lc)) + '\n' + rest, J_REF, N, recs, os.path.basename(cpath))),
          '(N=%d: the producer sha256 with its last digit changed must be refused)' % N)
    plant('PLANT-READER-CW11', refused(lambda: RDR.loads_lawcert(text, first.replace(' N %d ' % N, ' N %d ' % (7 - N), 1) + '\n' + rest, J_REF, N, recs,
                                                                 os.path.basename(cpath))), '(N=%d: the other N on the first line must be refused)' % N)
    cw = RDR.PRODUCERS['m3_lawcert_cw_v1.py']
    plant('PLANT-READER-CW11', refused(lambda: RDR.loads_lawcert(text, first.replace('m3_lawcert_c3k_v2 ', 'm3_lawcert_cw_v1 ', 1).replace(lc, cw) + '\n' + rest,
                                                                 J_REF, N, recs, os.path.basename(cpath))),
          '(N=%d: the cw producer with its own sha256 for the c3kp records must be refused)' % N)
    plant('PLANT-READER-CW11', refused(lambda: RDR.loads_lawcert(text, otext, J_REF, N, {'E4N': recs['E4N']}, os.path.basename(cpath))),
          '(N=%d: the records passed without E4D must be refused)' % N)
    c2 = json.loads(text)
    k0 = sorted(k for k in c2['entries'] if c2['entries'][k]['laws'] is not None)[0]
    c2['entries'][k0]['laws']['rem_tpow'] = 5 if c2['entries'][k0]['laws'].get('rem_tpow') != 5 else 6
    t2 = json.dumps(c2, sort_keys=True)
    o2 = otext.replace(tsha(text), tsha(t2))
    plant('PLANT-READER-CW11', refused(lambda: RDR.loads_lawcert(t2, o2, J_REF, N, recs, os.path.basename(cpath))),
          '(N=%d: a law changed with the RECORD line re-hashed must be refused)' % N)
    plant('PLANT-PARENT', refused(lambda: PAR.load_lawcert(cpath, opath, J_REF, N, dict((f, PAR.load(os.path.join(S3O, 'm3_c3kp_%s_N%d_J300_c3kp.json' % (f, N)),
                                                                                                    asm, J_REF, N)) for f in FAMS))),
          '(N=%d: the parent m3_reader_cw_v1 must refuse the c3kp certificate)' % N)
out('VERDICT %s' % ('VALID' if not FAILS and not NOFIRE else 'INVALID (%s)' % ', '.join(FAILS + ['%s did not fire' % p for p in NOFIRE])))
