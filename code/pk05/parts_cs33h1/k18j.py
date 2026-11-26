

def main():
    C.CAP[0] = CAP_S
    with open(__file__, 'rb') as fh:
        me = hashlib.sha256(fh.read()).hexdigest()

    def out(s):
        print(s, flush=True)
    out('SELF sha256 %s' % me)
    out('cs33h_1_rh_cert core %s engine %s probe %s item %s CAP_S %.0f NMODE %d NCERT %d K_S %d K_F %d PE %s K_EX %d NSUB %d K_MAX %d' % (
        CSHA[:8], C.ESHA[:8], PSHA[:8], ITEM, CAP_S, NMODE, NCERT, K_S, K_F, PE, K_EX, NSUB, K_MAX))
    valid, allcert, a, hi, stopped, part = run_item(ITEM, out)
    if not valid:
        verdict = 'VOID'
    elif not allcert:
        verdict = 'FAILED'
    elif ITEM == 'smoke' or ITEM.startswith('pilot'):
        verdict = 'CERTIFIED part %s' % part
    else:
        verdict = ('PARTIAL %s [%r, %s]' if stopped else 'COVERED %s [%r, %s]') % (part, a, hi.str(25, radius=False) if hi is not None else '-')
    out('VALID %s' % valid)
    out('VERDICT %s' % verdict)
    out('CPU %.1f s maxrss_kb %d' % (time.process_time() - T0, resource.getrusage(resource.RUSAGE_SELF).ru_maxrss))


if __name__ == '__main__':
    main()
