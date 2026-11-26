# Record: S4(c), tight half (pk21, W1 component S)

Status: the record run of piece S, promoted after the review, with the bytes unchanged. Paths are relative to
/mnt/g2/release/root/code/; the manifest's paths are relative to pk21/.

Version v1_1 replaces pk21/p2/s4c/S4C_TIGHT_RECORD_v1.md (3b7334fa, kept frozen) after the records check (Review below). It
corrects three statements: the input tags number four, not eight; the engine diff has six hunks, two of them read-only hooks in
item_sweep; and the manifest's paths are relative to pk21/. No claim value or pin changes. This version's manifest is
pk21/p2/s4c/MANIFEST_S4C_TIGHT_RECORD_v1_1.sha256: the same 16 files, with this record in place of v1.

## Claim

For N in {3, 4} and every J >= 300,

  ||Q_4 S Q_4|| <= tau_4(N),   tau_4(4) = 0.027702,   tau_4(3) = 0.026922,

with S = T/lambda_0, P_4 = span{psi-hat, e_1, e_2, e_3} the paper's explicit trial space (e_2 flip-odd), and Q_4 = 1 - P_4 its trial
complement. This is the form that Lemma A uses. By Courant-Fischer the same tau_4 bounds the fifth eigenvalue of S in modulus.
tau_4(N) is the largest per-piece bound, rounded up at the sixth decimal: 0.027701428 (N = 4) and 0.026921234 (N = 3), both on the
first piece [300, 300.75]. Per-piece values: the TSVs below.

## Argument

pk21/p2/s4c/S4C_TIGHT_METHOD_v1.md (57e50736), section 2: ||Q_4 T Q_4||_HS^2 <= tr T^2 - tr((Pi_4 T Pi_4)^2), the parity split
of the Ritz matrix, S4(a)'s trace bound, and S6's certified per-piece quantities, which give tau_4 = sqrt(rho2 - mu_z^2)/lambda_0,lo.

## Uniformity in J

The bound holds for every J of each piece through S6's per-piece forms: the interval values on the piece and the mean-value forms,
checked by C-MV. The run's C-MV lines equal the original certified run's, and so do its S5, S6, S7, INFO-HARM and VERDICT lines
(control below). The last piece runs to J = inf.

## Run and files

- Engine: pk21/p2/s4c/kt_s9h_tau4_pk21_v1.py (cc6f0a5f), a copy of pk07/kt_s9h_v1_2.py (848d7376); diff
  pk21/p2/s4c/diff_vs_kt_s9h_v1_2_v1.txt (0d48880e), six hunks. Four lie outside the verdict-path functions: OWN (l.273), the CODE
  line of the two header writers (l.2989, l.3198) and the added tau4_row / tau4_summary block (copy l.5244-5283). The other two are
  one-line hooks inside item_sweep (copy l.5298 and l.5472) that only read Q and write the tau4 rows. The run's verdict-path output
  lines equal the original certified run's (Uniformity in J), which shows that the hooks change nothing.
- Run: vsweep mode, LIM 300, pk21/p2/job22_tau4.sh (8c0c836b); guard log pk21/guard/S1_GUARD_job22_tau4.log (0.030 core-h).
- Output: pk21/p2/s4c/out/out_kt_s9h_tau4_pk21_v1_vsweep.out (1f3693f0). VERDICT VALID; all four input tags certified (M3
  entries, M2 vacuum, S4 U and S4 TRB; output l.148); the output's first line names the engine by its full sha256.
- TSVs: pk21/p2/s4c/out/tau4_kt_s9h_tau4_pk21_v1_N4.tsv (b6e65884) and ..._N3.tsv (51deea98), 904 rows each.
- The copy's S_V export: pk21/p2/s4c/out/export_kt_s9h_tau4_pk21_v1_vsweep.kv (26d83883).
- Control: pk21/p2/s4c/out/cmp_vs_original_v1.txt (acc002c4), from pk21/p2/job26_s4c_cmp.sh. The 1808 piece rows of the copy's
  export equal those of pk07's certified export (761084be); the headers differ only in the comment line and the CODE line.
- The engine's own comment calls the run "a reading, not a certified record"; it was written before the review. The review
  promoted this run to the record run, and no byte changed.

## Review

The review: SOUND.
- The HS argument and the parity split are right.
- rho2, mu_z and lambda_0,lo are S6's certified quantities. The TSVs' rho_hi equals the certified export's on all 904 + 904 pieces.
- The diff is clean, and tau4_row is outward interval arithmetic.
- The run stands as the record run once these files are frozen with a manifest: pk21/p2/s4c/MANIFEST_S4C_TIGHT_RECORD_v1.sha256.

The records check: CLEARED. Every number and pin checks, including the outward
recomputation of tau_4 from the TSV rows and the 1808 identical export rows. This version makes the check's one fix and two wording
points.

## Uses

- W1's connected engine: the condition 2 asks for a certified tau below about 0.059 on every piece.
- The middle-row programme: the sketch needs tau below s_y (about 0.0436).
- The supplement's S4(c), tau < s_x - c-bar, follows; the crude half already held on disk.
