# REVIEW_CODE_ARBENG_MA_V1_4: pk02's arbeng_ma_v1_4 code and its validation kt_ma_val_v1_6

Stamp: 2026-11-08T01:37:50Z

## Inputs
- pk02/arbeng_ma_v1_4.py 2c0a7338 (1679 lines), against arbeng_ma_v1_3.py 075e3586.
  - The supplied diff is DIFF_arbeng_ma_v1_3_to_v1_4.txt a9ad5b20. My own diff gives the same three hunks: the docstring (2c2,19), VERSION (67c84) and the appended section (1113a1131,1679). Every v1_3 line is otherwise byte-identical.
  - I read the appended section, l.1131-1679, in full.
- pk02/kt_ma_val_v1_6.py e182d503, with DIFF_kt_ma_val_v1_5_to_v1_6.txt d039e36e. I read piece_cmp, arb_moments, build_u, piece_v5, piece_v6 and piece_v7f.
- MANIFEST_ARBENG_MA_v1_4.sha256 8d1a2fcf: 36 of 36 OK under --strict. MANIFEST_KT_MA_VAL_v1_6_RUN.sha256 6e951721: 73 of 73 OK under --strict. The run script is run_kt_ma_val_v1_6_v2.sh 7d20997e.
- The outputs, all VERDICT VALID. The .err files are time -v reports with exit status 0.
  - v1 78a6e1a8, v2 8173c83b, v3 af14f2f1, v4 56ab092b, cmp e551791a;
  - v5 e2a582e4, v6 bb89455c;
  - v7s 11704480, v7u0 e4da33f1, v7u1 9bb02ff9, v7u2 559a41d9, v7f ddad50c8.
- My design review: REVIEW_DESIGN_ARBENG_MA_V1_4_rv01.md 53de1c0d.

## Answer first
- **CLOSE: sound and validated.** pk03 may pin it.
- Every addition of 53de1c0d is coded as asked, and there is no defect.
- There are four notes (one rule for the caller, three operational) and one tightness risk for the D16 records. None blocks.

## The kernel's new section
1. **The pull form** (MomTableU._block, l.1479-1537).
   - The coefficient coef_j(k) is the exact nonzero half-integer. D_j is scaled before the product (Q2), and each term's count is k_Dj' + k_q + 1.
   - For each subset A, the q of the block are one searchsorted range. The exponents of e_A + e_q are at most k - j + 1 <= D < B, so codes add without carry.
   - present() reads mid, sa and sr (the v1_2 fix stays), so only exact zeros are dropped.
   - The hit test removes codes in [lo, hi) that are not destinations (caps, gaps).
   - Each destination gets one seg_pairwise tree, then div_int(k), all inside np.errstate(raise), followed by MA.check.
   - minors() is v1_3's loop (l.448-474) in substance.
2. **C-PAIRS.**
   - Per block, the candidate pairs equal block_pairs' count (run_unit l.1561-1562).
   - Per destination, the terms are at most 2^|supp c| - 1, counted with np.unique (l.1527-1532).
3. **State.**
   - Files are written to a temporary name, fsynced and renamed, with the hand-off JSON last (l.1356-1376).
   - H_par covers the exact Gam, n, D, F, groups, caps, W_int, block, VERSION and KERNEL_SHA.
   - Loaders check H_par, the code hashes, the kernel sha and each file's size and sha256. They also recompute the codes and require exact equality (l.1460-1463, Q3 (a)).
   - _assemble requires the units to partition the blocks from 0, with no gap and no overlap, under one level and one kernel (l.1583-1612, Q3 (b)).
   - finish applies v1_3's factorial scaling (l.493-500), including the +1 count for factorial products above 2^53.
   - run_unit stops only between blocks and always does at least one block (l.1555-1558).
4. **Blocked E2** (l.1181-1264).
   - E2_plan's order and cuts depend only on P, Q and max_pairs. E2_check_plan requires a partition of P and is re-run in every E2_block.
   - A block's count is kP + kQ + kmom + 2, with MA.check and _scalar_ball per block.
   - E2_combine tests MAFallback once, on the total (Q4).
5. **scalar_sum_fast** (l.1146-1165) reproduces seg_pairwise's single-segment pairing: (2i, 2i + 1) with max + 1, and the odd last term carried.

## The validation
- **C-V15SAME (cmp).** v1-v4 equal kt_ma_val_v1_5's outputs line for line. The normalization drops only the header, the kernel name and cpu/MiB, and the VERDICT lines must be equal.
- **v5.** C-V2-ARB compares 4 tables, including F = 6, D = 9 with groups and caps, against an independent arb recursion: per destination, 512 bits, exact Gam.
  - No MomTableU or MomTable ball misses. The worst |mid - arb|/rad is 0.103.
  - C-V2-OVL and C-PAIRS pass. PLANT-V2-ARB, moving each moment by 10 times the largest relative radius, fires on all of them.
- **v6.**
  - C-RESUME: block sizes 97 and 31, and 97 stopping after every block, give bit-identical moments.
  - All 7 state plants fire. PLANT-CODES, with the sha rewritten, is caught only by the codes recompute, which is the point of Q3 (a).
  - C-FASTSUM covers 36 lengths with random values, zeros, error-only and near-TINY terms.
  - C-E2B: the one-block plan equals v1_3's E2 bit for bit, and the 18-block plan contains the exact arb E2.
  - PLANT-E2PLAN fires.
- **v7.**
  - C-PLAN16: 5,304,518,790 planned pairs, equal to the exact binomial total.
  - 20 units over 3 jobs, with one stop on the CPU guard between blocks ([16, 194, 221] of the asked [16, 194, 261]).
  - C-COVER and C-PAIRS16 pass. The table has 30,421,755 moments.

## Notes (non-blocking)
- **N-1 (caller rule, then hardening).**
  - E2_combine(parts, plan=None) skips its parts-count check, and load and load_view with expected_sha256=None skip the pin.
  - In certified use the caller must always pass the plan and the table hand-off's full sha256. pk03's code review should check both.
  - A later revision can make both arguments mandatory. PLANT-E2PLAN covers only the path with a plan.
- **N-2 (state hygiene).**
  - os.rename replaces an existing target on POSIX, so the pre-check gives no-overwrite only with one writer. The run script's one-job-at-a-time rule provides that.
  - After a kill, an orphan npz without its hand-off, or a .tmp file, blocks a rerun under the same name. Move it aside; never delete it (project rule).
- **N-3 (block in H_par).** A table must be loaded with the block it was built with. A mismatch is refused (C-STATE), never silent. At D16 that block is 5000, per pk02's memory finding: peak 1.8 GB instead of 6.2 GB, with results bit-identical by C-RESUME.
- **N-4 (memory).** v1's validation run, which reran v1_5's pieces, peaked at 7.97 GB RSS under prlimit AS 12 GiB (v1.err). D16 production units should use block 5000.

## Risk for the D16 records (tightness, not soundness)
- The synthetic D16 table's worst moment has gamma_k sa/|mid| = 4.22e-3 (C-SHADOW). With k up to 173, that means sa/|mid| is about 2e11: cancellation in the recursion at level 16.
- The QC E2 (12000 x 12000 pairs) passed E2_combine, so its M-a error is at most FALLBACK_REL = 1e-3 relative. Its printed radius, 4.23e30 on 3.95e33, includes arb's print rounding.
- Whether widths like these fit the bars route (b) needs is open. The per-key multipliers (S8-2 2.17 at N4 with per-key bars; floors x11.8 for H and x9.3 for S4) come from float measurements.
- Before the certified H/S4 records are built, pk03 should report, for the first real table:
  - the M-a widths against those bars;
  - how often MAFallback fires;
  - what the fallback costs.

## Pin (for pk03)
- Pin by file and full sha256, as listed in MANIFEST_ARBENG_MA_v1_4.sha256 8d1a2fcf.
- The validation record is MANIFEST_KT_MA_VAL_v1_6_RUN.sha256 6e951721.
- Keep the deny entry for arbeng_ma_v1_1 (D-1).
