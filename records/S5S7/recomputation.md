# CHECK_SV_SPOTCHECK_V3_1_rv03: v3 on DEFS_S67_PIN_v1_2, all 17 scalars fully pinned (v3_1)

Written 2026-11-08T02:27:39Z (cap 0.01 core-h).
It follows CHECK_SV_SPOTCHECK_V3_rv03.md 48c7a594. The definitions are pk07's DEFS_S67_PIN_v1_2 da67c29f, the pin of record
(hand check 1ca428a9). Run: t111_sv_B_v3_1.py 81400659, out 480f802e (err 0a1bf938), 2.14 s of CPU.

## Result

**NO MISMATCH, VERDICT VALID. All 17 scalars agree at all 8 pieces and 3 points, now with every definition pinned, and both claimed
pairs hold.**

Of v3's three readings:
- (a), mu_x on rows {i0, ix} of the U-basis A', was right and stays.
- (b) and (c) now follow the pin. q_x is the lower end of (L^-1 T L^-T)[1][1] in the raw Cholesky basis, and q_x' is the lower end of
  q_x - (1 + eps_r) mhat_hi sp^2, with mhat_hi = mhat(1/J_lo). a_x is |w_1|/(mhat sqrt g00) in the raw basis.

Nothing else changed from v3. C-RIY still matches R_IY_HI to within 0.02%, and the rooms and VEX are unchanged (0/16 disagreements). All
9 plants fire, PLANT-RAWBASIS included.

**Slack of the basis-dependent fields** (minimum over the 3 points; the other ten fields and the overlap rows are as in 48c7a594):

| scalar | N4 P0120 | N4 P0000 | N4 P0903 | N4 P0400 | N3 P0120 | N3 P0116 | N3 P0903 | N3 P0400 |
|---|---|---|---|---|---|---|---|---|
| rho_hi | +1.1e-05 | +8.5e-06 | +4.2e-07 | +6.4e-07 | +9.1e-06 | +9.6e-06 | +3.7e-07 | +5.5e-07 |
| rho1_hi | +2.4e-05 | +1.3e-05 | +9.5e-07 | +1.4e-06 | +1.8e-05 | +1.8e-05 | +7.2e-07 | +1.1e-06 |
| r2_hi | +6.3e-05 | +5.0e-05 | +4.4e-05 | +4.5e-05 | +3.9e-05 | +4.0e-05 | +2.2e-05 | +2.2e-05 |
| ro_hi | +1.9e-05 | +7.3e-06 | +7.6e-07 | +1.2e-06 | +1.8e-05 | +1.8e-05 | +7.2e-07 | +1.1e-06 |
| rp_lo | +1.6e-04 | +5.5e-05 | +6.8e-06 | +9.9e-06 | +1.2e-04 | +1.2e-04 | +5.0e-06 | +7.3e-06 |
| cx_lo | +2.5e-04 | +9.3e-05 | +1.2e-05 | +1.7e-05 | +1.6e-04 | +1.7e-04 | +7.5e-06 | +1.1e-05 |
| vSv_m_hi | +3.8e-05 | +1.3e-05 | +1.6e-06 | +2.3e-06 | +2.8e-05 | +2.9e-05 | +1.2e-06 | +1.7e-06 |

cx_lo's slack is smaller than under v3's U-basis reading (+7.6e-6 to +6.3e-4 there) but positive everywhere. The tightest margins are
unchanged: rho_hi +3.7e-7, and rho1_hi and ro_hi +7.2e-7, all at N3 P0903.

## Notes

- **g00:** the export takes b5's g,0,0 in every Ritz matrix and m2's g00 in the H_T / D_n / R_w group (DEFS v1_2). My single g00
  comes from the m2 and b5 intersection, so it lies inside both boxes, and every corner is an admissible input of the export's
  function.
- **The spot check is closed on my side.** The same-function fields are confirmed by admissible corners and ADM points, the overlap
  rows all pass, and the claimed pairs pass both on my BOX bounds and on the export's own bounds.

| file | sha256 (8) |
|---|---|
| rv03/t111_sv_B_v3_1.py | 81400659 |
| rv03/out_t111_sv_B_v3_1.out | 480f802e |
| rv03/out_t111_sv_B_v3_1.err | 0a1bf938 |
| pk07/DEFS_S67_PIN_v1_2.md | da67c29f |
| pk07/out/precond_u_kt_s9h_v1_2_v1.kv | f40b6096 |
