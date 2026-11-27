#!/usr/bin/env python3
"""plants_midrow.py: planted-failure controls for the two middle-row runs nM1 and nM2 of RUNS_M2_release_N.tsv.

The plants are those of the assembly program code/pk24/mr_engine/kt_mr_assembly_v1_8_4.py (its fifth argument PLANT; its docstring
lists them and their gates). For each row of PLANTS_MIDROW_release_N.tsv, or for the ids given, the run's command is repeated with
three changes: the staged record folder and every output get the suffix .plant_<id>; the assembly program is called with the row's
PLANT and NMAX 10 (the size the program's plants use) in place of none; the steps after the assembly program are left out. The staging
step, the comparison of the staged records with the certified run's records and the column check run unchanged, so a plant acts on
exactly the inputs of the certified run. A plant passes when the console of the assembly program states 'PLANT <name>: FIRED'.
Run it from the root of a fresh copy of the package, where /mnt/g2/release/root is the package root (as for the runs of rerun_m2.py).

usage: python3 -I -B plants_midrow.py [ID ...]        exit status 1 if a plant did not fire or a step before the assembly failed."""
import sys, os, re, subprocess, resource


def rows(path):
    out = []
    for ln in open(path, encoding='utf-8'):
        if ln.startswith('#') or not ln.strip():
            continue
        out.append(ln.rstrip('\n').split('\t'))
    return out[0], out[1:]


def cpu():
    r = resource.getrusage(resource.RUSAGE_CHILDREN)
    return r.ru_utime + r.ru_stime


def main():
    root = os.path.dirname(os.path.abspath(__file__))
    hdr, runs = rows(os.path.join(root, 'RUNS_M2_release_N.tsv'))
    ix = dict((h, i) for i, h in enumerate(hdr))
    cmd = dict((r[ix['run']], (r[ix['folder']], r[ix['command']])) for r in runs if r[ix['run']] in ('nM1', 'nM2'))
    phdr, plants = rows(os.path.join(root, 'PLANTS_MIDROW_release_N.tsv'))
    want = set(sys.argv[1:])
    bad = 0
    for pid, run, plant, expect in plants:
        if want and pid not in want:
            continue
        folder, c = cmd[run]
        rec = re.search(r'stage_certset_v1\.py (mr_engine/\S+)\.rerun ', c).group(1)
        steps = c.split(' && ')
        k = next(i for i, s in enumerate(steps) if 'kt_mr_assembly_v1_8_4.py' in s)
        pre = [s.replace(rec + '.rerun', rec + '.plant_' + pid).replace('.rerun.console', '.plant_%s.console' % pid) for s in steps[:k]]
        asm = steps[k].replace(rec + '.rerun', rec + '.plant_' + pid)
        asm = re.sub(r'CERTIFIED (\S+) none (\d+)', 'CERTIFIED mr_engine/plants/%s.kv %s 10' % (pid, plant), asm)
        asm = re.sub(r'> (\S+\.out) 2>&1$', '> mr_engine/plants/%s.out 2>&1' % pid, asm)
        cwd = os.path.join(root, folder)
        os.makedirs(os.path.join(cwd, 'mr_engine', 'plants'), exist_ok=True)
        t0 = cpu()
        ok_pre = all(subprocess.run(['bash', '-c', s], cwd=cwd).returncode == 0 for s in pre)
        rc = subprocess.run(['bash', '-c', asm], cwd=cwd).returncode if ok_pre else None
        con = os.path.join(cwd, 'mr_engine', 'plants', pid + '.out')
        txt = open(con, encoding='utf-8', errors='replace').read() if os.path.isfile(con) else ''
        line = next((l for l in txt.split('\n') if l.startswith('PLANT %s:' % plant)), '')
        fired = ok_pre and line.startswith('PLANT %s: %s' % (plant, expect))
        bad += not fired
        print('%s %s %s %s | exit %s | cpu %.1f s | %s' % ('PASS' if fired else 'FAIL', pid, run, plant, rc, cpu() - t0,
                                                         line[:200] if line else ('steps before the assembly failed' if not ok_pre else 'no PLANT line')))
    print('PLANTS run %d, fired %d, not fired %d' % (sum(1 for p in plants if not want or p[0] in want) , sum(1 for p in plants if not want or p[0] in want) - bad, bad))
    sys.exit(1 if bad else 0)


if __name__ == '__main__':
    main()
