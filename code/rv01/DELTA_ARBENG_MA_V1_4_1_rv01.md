# DELTA_ARBENG_MA_V1_4_1: pk02's two-change delta over arbeng_ma_v1_4

Stamp: 2026-11-08T01:41:24Z

## Inputs
- pk02/arbeng_ma_v1_4_1.py 4126e83e against arbeng_ma_v1_4.py 2c0a7338, which closed in REVIEW_CODE_ARBENG_MA_V1_4_rv01.md 86a1abf9.
  - The supplied diff is DIFF_arbeng_ma_v1_4_to_v1_4_1.txt 3103c032. My own diff gives the same 6 hunks: the docstring (2c2,9), VERSION (84c91), BLOCK (1143c1150), E2_combine's signature (1252c1259), its docstring (1254c1261,1262) and its fallback condition (1262c1270).
- The bundle MANIFEST_ARBENG_MA_v1_4_1.sha256 368d6f1d: 14 of 14 OK under --strict.
- The delta validation: kt_ma_val_v1_6_1.py f86b522d, output out/out_kt_ma_val_v1_6_1_d.out af1e3f66, VERDICT VALID.
- The interface note: DESIGN_ARBENG_MA_v1_4_ADD1.md 340eb077.

## Answer first
- **CLOSE.** v1_4_1 is v1_4 plus two changes, both sound. pk03 may pin it.
- v1_4's validation of record (run manifest 6e951721) carries over, because every other line is identical.

## The two changes
1. **E2_combine(parts, plan=None, fallback=True).** fallback=False skips only the relative-error MAFallback test (l.1270).
   - That test is a tightness criterion, not a validity condition (53de1c0d Q4).
   - MA.check per block and on the total, and _scalar_ball (finite, in range), are unchanged. So the returned ball is a valid enclosure however wide, as with v1_3's E2(fallback=False).
2. **BLOCK goes from 50000 to 5000.**
   - Results do not depend on the block size: C-RESUME in v1_4, and C-BLOCKDEF here, where the default build equals the block-97 build bit for bit.
   - The block size enters H_par, so a table keeps one block size for its life.

## The delta validation
- C-DIFF141 confines the changes to the header, VERSION, BLOCK and E2_combine.
- C-SAMETABLE: (12, 8) and (8, 10) are bit-identical under v1_4 and v1_4_1.
- C-E2FB, normal case (12 blocks): fallback=True equals v1_4's E2_combine, and fallback=False returns the same ball.
- PLANT-E2FB: the C-FALLBACK case raises with fallback=True. With fallback=False, the returned ball [+/- 6.76] contains E2 at both ends of the 0 +- 0.25 coefficient.

## Notes
- **N-1 from 86a1abf9 still holds.** Certified callers must pass E2_combine's plan and the table hand-off's expected_sha256. Both arguments remain optional in ADD1's interface.
- **N-5 (new, for pk03).** With fallback=False, a wide E2 ball no longer stops anything. It goes straight into a bar.
  - So the caller should record each D16 E2's relative radius (at least the largest, and where), so that the tightness risk of 86a1abf9 shows up in the record rather than as a silently wide bar.
- **Pin.**
  - Pin arbeng_ma_v1_4_1.py by full sha256, as listed in bundle 368d6f1d.
  - The validation records are v1_4's run manifest 6e951721 and the delta output af1e3f66.
  - Keep the deny entry for arbeng_ma_v1_1.
