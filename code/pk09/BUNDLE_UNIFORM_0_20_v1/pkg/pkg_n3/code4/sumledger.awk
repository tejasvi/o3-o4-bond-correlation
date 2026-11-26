# Summary of a cover3 ledger: certified/failed trials, covered range, smallest margins of the certified intervals.
# usage: awk -f sumledger.awk out/cover3_R1.ledger
$5 == "CERT" {
    c++; lo = $1 - $2; hi = $1 + $2
    if (c == 1 || lo < jmin) jmin = lo
    if (c == 1 || hi > jmax) jmax = hi
    for (i = 6; i <= NF; i++) { split($i, kv, "="); v[kv[1]] = kv[2] + 0 }
    if (c == 1 || v["sf"] < sfmin) { sfmin = v["sf"]; jsf = $1 }
    if (c == 1 || v["F0"] < f0min) { f0min = v["F0"]; jf0 = $1 }
    if (c == 1 || v["c7"] < c7min) { c7min = v["c7"]; jc7 = $1 }
    if (c == 1 || v["pp"] < ppmin) { ppmin = v["pp"]; jpp = $1 }
    if (v["m0"] > 0) c6++
    q = $2 / $1; if (c == 1 || q < qmin) qmin = q; if (c == 1 || q > qmax) qmax = q
    L = $3; I = $4
}
$5 == "FAIL" { f++ }
END {
    printf "%s: L=%s I=%s; %d certified, %d failed trials; J in [%.6g, %.6g]; h/J %.4f..%.4f; min safety %.3g (J=%.4g); min F(0) %.3e (J=%.4g); min p2-p4 %.3e (J=%.4g); min C7 %.3e (J=%.4g); certified with direct evaluation (m0 > 0): %d\n",
        FILENAME, L, I, c, f, jmin, jmax, qmin, qmax, sfmin, jsf, f0min, jf0, ppmin, jpp, c7min, jc7, c6 + 0
}
