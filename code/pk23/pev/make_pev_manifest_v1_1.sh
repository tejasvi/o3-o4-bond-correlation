#!/bin/bash
# make_pev_manifest_v1_1.sh (pk23, option B Pev entries): make_pev_manifest_v1.sh with one fix. v1 listed its own job's guard log
# (PK23_GUARD_pev_manifest.log) among the writable rows and hashed it while that job ran, so that row stopped matching when the guard
# closed its log (the v1 manifest and freeze list are kept as SCRATCH_MANIFEST_PEV_L_RECORDS_v1_stale_guardlog.sha256 and
# out/SCRATCH_MANIFEST_PEV_L_RECORDS_v1.frozen.txt). v1_1 is run, and freeze_pev_v1_1.sh after it, with guard logs named outside the
# listed globs (pk23/guard/PK23_GUARD_manifest_pev11.log, PK23_GUARD_freeze_pev11.log), so no listed file changes after hashing.
# Writes pk23/pev/MANIFEST_PEV_L_RECORDS_v1_1.sha256 (noclobber), the sha256sum list (paths relative to pk23/pev; check with:
# cd pk23/pev && sha256sum -c MANIFEST_PEV_L_RECORDS_v1_1.sha256) of
#   FROZEN (a-w after this script, by freeze_pev_v1_1.sh): the six records, the summary, the runner and its hand-off copy, the list, the
#   twin and rtwin scripts with their makers and checks, every twin, rtwin and runner item output, the hand-offs, the memos, the certified
#   D16 table states (out/tab16c), the plan, and this script and the freeze script;
#   WRITABLE (listed only): the chain and rtwin logs, the guard logs (pk23/pev and pk23/guard, by the absolute path), the syntax
#   check outputs, chain_hl_v1's empty control files PAUSE_chain_hl and STOP_chain_hl (the switch to chain_hl_v1_1 after Lp6), the unused
#   scratch copy chain_hl_v1_1.draft, and the superseded v1 tools and v1 manifest files.
# The twin's float table cache out/tab16 is not listed (no record reads it). Prints the manifest's sha256 and row counts.
# Usage: bash make_pev_manifest_v1_1.sh
set -u
B=/mnt/g2/release/root/code/pk23/pev
H=/mnt/g2/release/root/code/pk23
M=$B/MANIFEST_PEV_L_RECORDS_v1_1.sha256
F=$B/out/MANIFEST_PEV_L_RECORDS_v1_1.frozen.txt
set -o noclobber
cd $B || exit 2
if [ -e $M ] || [ -e $F ]; then echo "exists: $M or $F"; exit 3; fi
for n in 4 3; do for g in L LH LT; do [ -e out/m3_hl_${g}_N${n}_J300_hl.json ] || { echo "missing record out/m3_hl_${g}_N${n}_J300_hl.json"; exit 4; }; done; done
[ -e PEV_L_RECORDS_v1.md ] || { echo "missing PEV_L_RECORDS_v1.md"; exit 4; }
frozen=( out/m3_hl_*_J300_hl.json PEV_L_RECORDS_v1.md PEV_L_PLAN_v1.md HL_ENTRY_LIST_v1.json m3_run_v1_9_3_hl_v1.py m3_handoff_v3_hl.py
  m3ref_hl_v1.py rtwin_hl_v1.py make_m3ref_hl_v1.py make_rtwin_hl_v1.py make_run_hl_v1.py make_pev_summary_v1.py make_pev_manifest_v1_1.sh
  check_t0_closed_v1.py test_rtwin_maker_ast_v1.py chain_twin_hl_v1.sh chain_hl_v1.sh chain_hl_v1_1.sh run_rtwin_hl_v1.sh freeze_pev_v1_1.sh
  out/m3ref_hl_v1_P16L.*_z9sym.out out/m3ref_hl_v1_P16L.*_z9sym.err out/s16memo_P16L_N*.jsonl
  out/rtwin_hl_v1_*_z9sym.out out/rtwin_hl_v1_*.log out/m3_run_v1_9_3_*.out out/m3_run_v1_9_3_*.err out/m3_run_v1_9_3_memo_L_N*.jsonl
  out/check_t0_closed_v1.out out/make_rtwin_hl_v1.out out/make_run_hl_v1.out out/make_pev_summary_v1.out )
mapfile -t hands < <(find hand -type f | sort)
mapfile -t tabs < <(find out/tab16c -type f | sort)
writable=( chain_hl_v1.log chain_hl_v1_1.log chain_twin_hl_v1_N4.log chain_twin_hl_v1_N3.log rtwin_hl_v1.log PK23_GUARD_pev_*.log out/ast*.out
  chain_hl_v1_1.draft PAUSE_chain_hl STOP_chain_hl make_pev_manifest_v1.sh freeze_pev_v1.sh SCRATCH_MANIFEST_PEV_L_RECORDS_v1_stale_guardlog.sha256
  out/SCRATCH_MANIFEST_PEV_L_RECORDS_v1.frozen.txt out/make_pev_manifest_v1.out out/mancheck1.out )
mapfile -t gl < <(find $H/guard -maxdepth 1 -type f -name 'PK23_GUARD_pev_*.log' | sort)
for p in "${frozen[@]}" "${hands[@]}" "${tabs[@]}"; do [ -f "$p" ] || { echo "not a file: $p"; exit 5; }; done
printf '%s\n' "${frozen[@]}" "${hands[@]}" "${tabs[@]}" > $F
sha256sum "${frozen[@]}" "${hands[@]}" "${tabs[@]}" "${writable[@]}" "${gl[@]}" > $M
echo "MANIFEST $(sha256sum $M | cut -d' ' -f1) $M rows $(awk 'END{print NR}' $M) (frozen $(awk 'END{print NR}' $F): ${#frozen[@]} named, ${#hands[@]} hand-offs, ${#tabs[@]} table-state files; writable $(( ${#writable[@]} + ${#gl[@]} )))"
echo "CHECK $(sha256sum -c $M 2>&1 | awk '/: OK$/ {o++} !/: OK$/ {b++} END {print o+0 " OK, " b+0 " not OK"}')"
