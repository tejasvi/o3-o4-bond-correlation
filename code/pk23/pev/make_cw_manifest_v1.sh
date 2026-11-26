#!/bin/bash
# make_cw_manifest_v1.sh (pk23, C_w variant B; the P0_LOG rows 4589, 4598, 4610): the release manifest of the certified C_w records, on
# the pattern of make_pev_manifest_v1_1.sh. Run it, and freeze_cw_v1.sh after it, with guard logs named outside the listed globs
# (pk23/guard/PK23_GUARD_manifest_cw1.log, PK23_GUARD_freeze_cw1.log), so no listed file changes after hashing.
# Writes pk23/pev/MANIFEST_CW_LC_RECORDS_v1.sha256 (noclobber), the sha256sum list (paths relative to pk23/pev, guard logs of
# pk23/guard by the absolute path; check with: env -C pk23/pev sha256sum -c MANIFEST_CW_LC_RECORDS_v1.sha256) of
#   FROZEN (a-w after this script, by freeze_cw_v1.sh): the two LC records, the summary CW_LC_RECORDS_v1.md and its maker and output, the
#   runner m3_run_v1_9_3_cw_v1 and the list with their makers and outputs, the float twin rtwin_cw_v1 with its maker, run script and
#   outputs, the chain script, every runner item output, the LC hand-offs, the run manifest MANIFEST_CW_RUN_ABS_v1, the law certificates
#   (m3_lawcert_cw_v1 and the Pev records' m3_lawcert_hl_v1_1, with makers, certificates, job outputs and the Pev run manifest
#   MANIFEST_PEV_RUN_ABS_v1), the reader forks m3_reader_hl_v1 and m3_reader_cw_v1 with makers, diffs, check jobs and outputs, and this
#   script and the freeze script;
#   PINNED (listed, already frozen by the Pev release): MANIFEST_PEV_L_RECORDS_v1_1.sha256, which lists L's prep hand-offs and table states
#   that the LC runs read by C-PREP-SHARE;
#   WRITABLE (listed only): the chain and rtwin logs, the C_w guard logs (pk23/pev and pk23/guard), the syntax check and run-manifest
#   check outputs, and the superseded first hl law-certificate tools (make_m3_lawcert_hl_v1.py and its output; the SCRATCH gap-plant copies).
# Prints the manifest's sha256 and row counts. Usage: bash make_cw_manifest_v1.sh
set -u
B=/mnt/g2/release/root/code/pk23/pev
H=/mnt/g2/release/root/code/pk23
M=$B/MANIFEST_CW_LC_RECORDS_v1.sha256
F=$B/out/MANIFEST_CW_LC_RECORDS_v1.frozen.txt
set -o noclobber
cd $B || exit 2
if [ -e $M ] || [ -e $F ]; then echo "exists: $M or $F"; exit 3; fi
for n in 4 3; do [ -e out/m3_cw_LC_N${n}_J300_cw.json ] || { echo "missing record out/m3_cw_LC_N${n}_J300_cw.json"; exit 4; }; done
[ -e CW_LC_RECORDS_v1.md ] || { echo "missing CW_LC_RECORDS_v1.md"; exit 4; }
frozen=( out/m3_cw_LC_N4_J300_cw.json out/m3_cw_LC_N3_J300_cw.json CW_LC_RECORDS_v1.md make_cw_summary_v1.py out/make_cw_summary_v1.out
  HL_CW_ENTRY_LIST_v1.json make_cw_list_v1.py out/make_cw_list_v1.out m3_run_v1_9_3_cw_v1.py make_run_cw_v1.py out/make_run_cw_v1.out
  rtwin_cw_v1.py make_rtwin_cw_v1.py out/make_rtwin_cw_v1.out run_rtwin_cw_v1.sh out/rtwin_cw_v1_LC.4_z9sym.out out/rtwin_cw_v1_LC.3_z9sym.out
  out/rtwin_cw_v1_LC.4.log out/rtwin_cw_v1_LC.3.log chain_cw_v1.sh
  out/m3_run_v1_9_3_LCa.*.out out/m3_run_v1_9_3_LCa.*.err out/m3_run_v1_9_3_LCk*.out out/m3_run_v1_9_3_LCk*.err
  out/m3_run_v1_9_3_LCr*.out out/m3_run_v1_9_3_LCr*.err out/m3_run_v1_9_3_asmc.*.out out/m3_run_v1_9_3_asmc.*.err
  hand/m3_run_v1_9_3_LCk*.json hand/m3_run_v1_9_3_LCr*.json MANIFEST_CW_RUN_ABS_v1.sha256
  m3_lawcert_cw_v1.py make_m3_lawcert_cw_v1.py out/make_m3_lawcert_cw_v1.out out/m3_lawcert_cw_v1_N4.json out/m3_lawcert_cw_v1_N3.json
  out/m3_lawcert_cw_v1_static.out out/m3_lawcert_cw_v1_4.out out/m3_lawcert_cw_v1_3.out
  m3_lawcert_hl_v1_1.py make_m3_lawcert_hl_v1_1.py out/make_m3_lawcert_hl_v1_1.out out/m3_lawcert_hl_v1_1_N4.json out/m3_lawcert_hl_v1_1_N3.json
  out/m3_lawcert_hl_v1_1_static.out out/m3_lawcert_hl_v1_1_4.out out/m3_lawcert_hl_v1_1_3.out MANIFEST_PEV_RUN_ABS_v1.sha256
  m3_reader_hl_v1.py make_m3_reader_hl_v1.py diff_m3_reader_c3h_v1_2_to_hl_v1.txt m3_reader_hl_check_v1.py out/make_m3_reader_hl_v1.out
  out/m3_reader_hl_check_v1.out m3_reader_cw_v1.py make_m3_reader_cw_v1.py diff_m3_reader_hl_v1_to_cw_v1.txt m3_reader_cw_check_v1.py
  m3_reader_cw_check_v1_1.py diff_m3_reader_cw_check_v1_to_v1_1.txt out/make_m3_reader_cw_v1.out out/m3_reader_cw_check_v1.out
  out/m3_reader_cw_check_v1_1.out make_cw_manifest_v1.sh freeze_cw_v1.sh )
pinned=( MANIFEST_PEV_L_RECORDS_v1_1.sha256 )
writable=( chain_cw_v1.log rtwin_cw_v1.log PK23_GUARD_cw_* out/cw_ast9.out out/cw_bashn1.out out/cw_bashn2.out out/cw_absman.out
  make_m3_lawcert_hl_v1.py out/make_m3_lawcert_hl_v1.out SCRATCH_m3_lawcert_hl_v1_gapplant.py out/SCRATCH_m3_lawcert_hl_v1_static_gapplant.out
  out/SCRATCH_m3_lawcert_hl_v1_4_gapplant.out out/SCRATCH_m3_lawcert_hl_v1_3_gapplant.out )
mapfile -t gl < <(find $H/guard -maxdepth 1 -type f -name 'PK23_GUARD_cw_*' | sort)
for p in "${frozen[@]}" "${pinned[@]}" "${writable[@]}" "${gl[@]}"; do [ -f "$p" ] || { echo "not a file: $p"; exit 5; }; done
n_rec=$(printf '%s\n' "${frozen[@]}" | awk '/^out\/m3_cw_LC_N[43]_J300_cw\.json$/' | awk 'END{print NR}')
[ "$n_rec" = 2 ] || { echo "records listed $n_rec, expected 2"; exit 6; }
printf '%s\n' "${frozen[@]}" > $F
sha256sum "${frozen[@]}" "${pinned[@]}" "${writable[@]}" "${gl[@]}" > $M
echo "MANIFEST $(sha256sum $M | cut -d' ' -f1) $M rows $(awk 'END{print NR}' $M) (frozen $(awk 'END{print NR}' $F), pinned ${#pinned[@]}, writable $(( ${#writable[@]} + ${#gl[@]} )))"
echo "CHECK $(sha256sum -c $M 2>&1 | awk '/: OK$/ {o++} !/: OK$/ {b++} END {print o+0 " OK, " b+0 " not OK"}')"
