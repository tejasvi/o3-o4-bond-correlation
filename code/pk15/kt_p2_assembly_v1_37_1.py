#!/usr/bin/env python3
"""kt_p2_assembly_v1_37_1.py -- pk15 (code/pk15/). REVISION of kt_p2_assembly_v1_37.py (9c9797ea; freeze manifest d8d4d113; R4 cert run
e353d42b VALID; the review freeze check 844b56e2), 2026-11-08, on the approval for one print line (pk11's R6.5 needs the certified Phi_eps per N).
Changes:
  (1) PHI-EPS: right after LG[N] in the Lemma G loop, one out() line in every mode prints, per N, S_eps (upper end), G_00 (lower end),
      Phi_eps and Phi_eps,theta (upper ends; dec_hi, dec_lo) of Lemma T-prime at Lemma G's eps. v1_37 computed and used the same values
      (Lemma E-prime, the gg tail of c_t, Gbad-prime, R8) but printed them only outside cert mode (INFO LEMMA-G, INFO LEMMA-E). Nothing
      else changes; the exports equal v1_37's row for row.
kt_p2_assembly_v1_37's docstring follows; its run line and file names change to v1_37_1.
kt_p2_assembly_v1_37.py -- pk15 (code/pk15/). REVISION of kt_p2_assembly_v1_36.py (a3db4f0a; mock run 37443d59 and certdry run 97df17fb
VALID; the review d1d86a4f complete, nothing blocking R4), 2026-11-08, on the requests of 10:00:03Z and after: three
fixes that ride with the R4 version pinning the v1_10 records. Changes:
  (1) A staged, all-or-none cert write (the choice (a); the review note 2, the review N-1 checks). Nothing can be deleted here, so a refused
      write must leave nothing that a retry under the same label would trip on. cert_stage runs cert_checks and C-CERT-EXISTS on the final
      name and on this run's temporary name (check_cert_free; cert_tmp gives <name>.<RUN_TAG>.part, RUN_TAG the run's UTC start stamp and PID,
      so a .part that an earlier run left is harmless), writes cert_text through the store fs and syncs it, then runs C-READBACK and the
      record's reader as CERTIFIED on the bytes read back; it touches no final name. cert_commit runs once all three exports are staged: it
      checks the three final names and the staged bytes again, then renames each and requires the renamed file to hold its bytes
      (C-CERT-RENAME). A refusal anywhere leaves only this run's .part files. The store is DISK in a cert run; the pre-write plants use NOWRITE
      (names tested on disk, a write or a rename raises) and the new tests MemFS (in memory). PLANT-CERT-PART: this run's temporary name
      taken gives a named refusal, not FileExistsError. PLANT-CERT-STAGE2: the joint export stages and passes, the t export is refused, and
      C-CERT-ALLORNONE finds no final name in the store, only the two .part files, and nothing on disk. C-CERT-DRY (control): the success path
      in a memory store, all three staged, checked and renamed, the store then holding exactly the three final names with their bytes
      (the review N-2's dry control without a disk write). INFO C-CERT-EXISTS/PART prints RUN_TAG and lists the .part files that earlier
      refused writes left in pk15/out.
  (2) C-COV-PROD names a failing row: the row prints its own FAIL line and the run stops before routes_piece, whose
      cov_from would refuse the same balls; the gate line over every row stays.
  (3) Wording: the C-S9H-READ line no longer says "which joint_read does not bind".
  (4) SETAC_RECORDS names m3_run_v1_10_4's records and asm outputs (pk03 sends the sha256s after production; earlier v1_10 runs write no
      records): pk03/out/m3_p2_<X>_N<N>_J300_v1_10_4.json and pk03/out/m3_run_v1_10_4_asm.<N>.out. Reader, run list, record fields
      and kernel layer (arbeng_ma_v1_4_1 4126e83e) unchanged.
  (5) The D4 and D4M normX_HS rows (the approval for draft A3; SPEC_HS_INV_NORMX_v1_2_ADD1 f2ad58c9). HS_RECORD is
      pk08's combined record HS_INV_NORMX_v1_d3d4b.kv (f8e3d5e0, run b8b7f8b7; D3B rows for R6), and hs_rows reads the D3, D4 and D4M rows: C-HS-OP
      (OPERATOR_D4 and OPERATOR_D4M exactly ADD1's; C-HS-OP-SPEC holds this file's strings against the pinned ADD1), C-HS-LAMBDA (p = 2 for D3,
      1 for D4 and D4M), C-HS-MIRROR (MIRROR_D4M = ADJOINT_OF_D4, the D4M row keys token for token the D4 ones), C-HS-J; C-HS-D3-SAME (every
      key of the D3 record 6b82dc63 but CODE and END unchanged). hs_piece takes the class's power; C-HS-CBOX, C-HS-COV and C-HS-SPOT (from the
      N*_<class>_SPOT lines) run for every class. normX_hi = min(Lemma S', normX_HS) for every class, the minimum of two valid upper bounds; the
      route TSV names each row's normX source and value and NORMX_HS_USED counts per class (the joint rows keep their seven columns, the
      consumer's layout). Plants PLANT-HS-D3-SAME, -OP-SPEC, -OP-D4, -LAMBDA-D4, -MIRROR (a D4M row changed), -SPOT-D4.
  (6) Cov_inf_hi (the rule, choice (a); the review 2a1da1e1 confirmed the per-route upper end): every admissible route's upper end
      Cov_hi = E11_hi - c_e,lo c_f,lo (mean_ends' upper end of E11; the product rule's other end under C-COV-PROD's positivity), and
      Cov_inf_hi = the smallest over the routes that give Cov_inf_lo. The means export carries Cov_inf_lo and Cov_inf_hi as its last two
      columns; the joint export keeps its seven (kt_s9h's layout). px_from's placeholder end |Cov_lo| + 1 reaches no export. C-COV-ORDER
      (lo <= hi, both finite) and C-COV-SAME (the means Cov_inf_lo equals the joint one string for string), with PLANT-COV-ORDER and
      PLANT-COV-SAME. The means header states the centring, COV_CENTRING (X_c centred at the exact bulk means, so Cov_inf = E_u[X_c] =
      E11 - c_e c_f; pk11 for R6.5), and means_check requires it on a CERTIFIED record and Cov_inf_lo > 0 on every
      row (the joint export's C-COV-POS decimals, equal by C-COV-SAME). mean_ends refuses a relative correction e_1 > 0 on a ratio ball
      that is not certainly positive, since mb (1 +- e_1) scales an end correctly only when it is >= 0 (C-MEAN-SIGN;
      PLANT-MEAN-SIGN).
  (7) PLANT-MOCK-B called load_setac(M_M3, 4, 'CERTIFIED'), and the certified path never reads that path: it loads the pinned records, so
      once R4 pins them the plant is accepted in every mode (the pins-only scratch draft A10p read VERDICT INVALID on that plant alone).
      PLANT-A-BIND-PIN (the NTB N4 record's pin replaced by 64 zeros) and PLANT-A-BIND-ASM-PIN (its asm output's pin replaced) take its
      place; C-A-BIND's pin test refuses both before any read, with or without the R4 pins. The INFO line after C-A-PERREC says so.
kt_p2_assembly_v1_36's docstring follows; its run line and file names change to v1_37.
kt_p2_assembly_v1_36.py -- pk15 (code/pk15/). REVISION of kt_p2_assembly_v1_35.py (ad587153; mock run 54ba2c64 and certdry run 706c2b5c
VALID), 2026-11-08, R3 on the approval of 09:24Z after the code the review and
the review of pk07's readers module. Changes:
  (1) Read-back by the consumer's readers. RDR_PATH, pk07/kt_s9h_v1_3_readers.py (610af315, SOUND), is read
      once as bytes, checked against its full sha256 pin and run from those bytes in a fresh module (s9h_load; C-S9H-LOAD: rlimits, the SIGXCPU
      handler, argv, cwd and the flint and mpmath precisions unchanged; PLANT-S9H-PIN); C-S9H-GRID: its joint_grid is this run's grid. One
      reader per RECORD (s9h_readers): the joint export through joint_read plus the record's identity (s9h_ident), the t export through t_read
      (aa empty, so a missing Aa_lo is refused, not replaced), the means export through means_check (kt_s9h does not read it); any exception
      from a reader is a refusal, as is a non-empty problems list. The cert writer is split: cert_checks holds every refusal that comes before
      a file operation (C-CERT-HEADER also requires FLOAT_IN none, OPEN_CONDITIONS none and J_UNIF_PP, C-CERT-READER: the dict has
      a reader for the record); kv_write_cert writes cert_text to the temporary file through an opener (the plants pass nowrite, so no plant
      can write), fsyncs it, runs C-READBACK and then the record's reader on the bytes read back, checks the final name again, renames,
      and requires the renamed file to hold those bytes (C-CERT-RENAME); a refused file never takes the final name. New plants
      PLANT-CERT-HEADER, -JUNIF and -RECORD; C-CERT-NOFILE. Three read-back tests: C-S9H-READ, each written export through its record's
      reader (as MOCK in the MOCK items, as CERTIFIED in cert); C-S9H-CERTCOPY, each export with its certified header built in memory
      (certify_header) through cert_checks, C-READBACK and then its reader as CERTIFIED, with PLANT-S9H-CENTRING and PLANT-S9H-JOINT-T (the joint
      reader refuses the t export); C-S9H-BIND, rule V2's bound_ok on a synthetic run output in this run's EXPORT line form
      (PLANT-S9H-BIND-SHA). Binding an export to this run's own VERDICT line stays the consumer's step: the line does not exist during the run.
      joint_read checks content only and binds no FORMAT, RECORD, END or EXPORT_STATUS (pk07 77dbcf77), so every
      reader runs after the header test and C-READBACK, and s9h_ident compares those keys, TAG and RUN_VERDICT for the mode itself.
  (2) J_UNIFORMITY as written: each export's J_UNIFORMITY carries MSFX in a MOCK export, so the per-piece string never stands
      beside EXPORT_STATUS MOCK (pk07's readers check J_UNIFORMITY on CERTIFIED records only). C-JUNIF-STATUS now runs after the writes, on
      the three pairs as written and on status_junif's triples for the joint and means exports and for the t export; PLANT-JUNIF-MOCKPAIR is
      the pair v1_35 wrote.
  (3) Plants for the refusals that had none: a C-COV-PROD gate line over every row (check_cov_prod, cov_from's own test)
      and PLANT-COV-PROD (c_e,lo = 0); PLANT-ROUTE-LARGER for C-ROUTE's maximum test; reader (b2)'s per-record tests as functions
      (check_setac_layer, check_setac_list, check_trial_full, check_setac_count), planted on S7's record through v6_3 (PLANT-A-LAYER, layer
      arbeng_ma_v1_3), an S8 record (PLANT-A-LIST-S8: S8's entry list) and the NTB key set offered as a DT record (PLANT-A-COUNT-FAM), with
      controls (C-A-PERREC); one INFO line per certified record (family, record sha8, layer, claim_ball); check_e2t with
      PLANT-D4S-E2 (E2_t below the trial ratio).
  (4) Output by mode: the EXPORT line takes rule V2's form 'EXPORT <name> sha256 <hex>' (EXPORT_FMT), with rows, FORMAT, EXPORT_STATUS and
      J_UNIFORMITY on an INFO line; C-SELF, PLANT-MOCK-D and C-NOCERT run in the MOCK items only (v1_35's loop would have failed a cert run).
      C-COV-POS (Cov_inf_lo > 0 on every joint row) and C-T-POS (At_lo, Aa_lo and Xta_lo > 0 on every t row), exact on the printed decimals,
      with plants. JT_FIELDS, TP_FIELDS and MN_FIELDS hold the FIELDS strings; CLAIM_CERT names no version; the first output line drops
      "MOCK run".
kt_p2_assembly_v1_35's docstring follows; its run line and file names change to v1_36.
kt_p2_assembly_v1_35.py -- pk15 (code/pk15/). REVISION of kt_p2_assembly_v1_34.py (72e9abb1; mock run 2ee01065 VALID
and the review cc6aabe1 OK), 2026-11-08, R3 on the approval: the A/C version, DESIGN_KT_P2_ASSEMBLY_v1_35 (3fe43b47) with its ADD1 (1acf7680). Changes:
  (1) Reader (b2) of Sets A, C and W (pk03/P2_RUN_LIST_v1_10.json, 23 entries per N; load_setac) with the fixed key map KEYMAP: M3_ij = SM3,i,j
      except M3_11 = X3; M4_ij = SM4,i,j except M4_10 = Gxt,0,0 and M4_11 = Y4; M4M := M4 (the mirror identity); W1, W2 (route D); IhZ, IhZb,
      IhZh (row 2). CERTIFIED: the seven family records per N (SETAC_FAMS) through m3_reader_v6_3 under m3_run_v1_10's asm output (C-A-BIND, with
      the layer arbeng_ma_v1_4_1), C-A-LIST (entry_list), C-A-TRIAL (trial_set), C-A-COUNT per record; refused until R4 pins the files. C-A-MAP
     : every slot of the key map against the pinned run list's graph and factor counts. C-A-MIRROR; INFO A-PARTITION; C-A-V63 (S7's
      g,0,0 through v6_3 equals v4_4's, the certified path's control).
  (2) Row 2 (P2-3) by the odd Ritz route: t^_z = mhat G_22^(-1/2) IhZ/(G_00^(1/2) lambda~_0,low^2) with S8's certified g,2,2 (C-C-TRIAL on the S8
      records), Delta_z = NH s' + s'|t_00| + GP (sigma_z = 0) with NH, GP, s' and |t_00| from the piece's lemma_a_amp dict at one Lam (nh_gp,
      C-Z-LEVEL), tz_hi = |t^_z| + Delta_z; C-ZFLIP (IhZb = -IhZ), C-ZPAR (IhZh = 0), C-G22-POS. tz leaves OWN_FLOAT_TP and TZ_P2_3 reads CERTIFIED.
      mu_z = T,2,2/g,2,2 is INFO. The port's Hbad' is tail_h(N, 1, LAM_T, 0) kappa^2 at the code level (HBP), no longer I[N]'s.
  (3) The means by the double eigen trick (STB_P2_PREP_v1_2 8c92ed24 l.100-104; ADD1 sect. 2), one ball per (N, piece) for every
      class, in the norm form (entries over their family's main term, Ritz values in main_N/main_D units): c_t = [mhat (Iht,0 + IhTt,0) - mhat^2
      Gxt,0,0]/(G_00 lambda~_0^2) with (a) gg <= Lam_t eps_r^2 (mhat/lt0)^2 (box) + tail_h(N, 1, Lam_t, 0) (kappa + mhat/lt0)^2 Phi_eps (tail,
      the fix), (b) the s-part (2 s' + s'^2) normS' of the w = 2 horizontal window (D4 (1,0)) and (c) G_00 lambda~_0^2 as the normalization
      (no D); c_b = Tb/(G_00 lambda~_0) (w = 1) with the D4 (0,1) s-part (kappa^2 >= kappa: C-KAPPA-GE1); c_bb = c_t. The s-part levels are the
      minimizers over the fixed grid 2, 2.5, ..., 40 (best_slev; any level is valid). C-MEAN-PARTS; C-MEAN-DT (sanity) against each class's
      single-trick means. lambda~_0's ball is [max(mu_0, lt0), mu_0/m0lo]. IhTt,0 := S9 Iht,0 by C-ALIAS-MIRROR and Tb := S7 A,0 by C-ALIAS-FLIP
     , with pk03's m3_entries_v3 and its modules pinned.
  (4) the joint-path items: check_sigma fails closed on NaN; rho_terms gates q_Q > 0; C-MHAT (mhat > 0 where lt0 is formed). C-TAU-TRIAL gets
      its own flag (C-TAU-N keeps load_tau's: its only N step is the label check). Label fixes: GBAD_SOURCE, INFO LEMMA-E, E2_CONSTANTS name
      Lemma T-prime with S7's G_00 record; the kt_rb-ratio Phi and C-ZR0 are comparison only. C-FLOATIN-OWN now expects the empty own list.
  (5) Row 5 (ADD1 sect. 3): Cov_inf_lo per piece is the maximum over the admissible routes (ROUTE_OK: D3 SINGLE, CS; D4 and D4M SINGLE,
      DOUBLE; ties to SINGLE), each E11_lo - c_e,hi c_f,hi with the double-trick means (cov_from, C-COV-PROD). SINGLE: Lemma E' on M_11/M_00
      (g-part and s-part minimized over ROUTE_GRID). DOUBLE: [mhat (W1 + W2) - mhat^2 Y4]/(G_00 lambda~_0^2) with gg = Lemma E''s e_11 less its
      first-order box (the eta box and every tail kept), the s-part the smaller of Lemma E''s and C-D4S's sigma_D4 (ADD1_1 30950bd4
      cdd70f5f: 2 L_b s' sqrt(E2_t) + s'^2 ||A^_f||_S' + (2 s' + s'^2) b-tail at L_b). CS: Lemma E-CS (NOTE_LEMMA_E_CS_v1 d57590da sect. 2,
      the review e6ea2e4c SOUND), each term the smaller of E' and E-CS, with rho_(phi,ij) by the Q-form bound rho^2 <= 1 + 8 kappa row_h(N, 2, 0)
      sigma_R sqrt(Phi_W,R Phi_eps) G_00,hi/M_ij,lo (ecs_rho; C-ECS-PHI, C-M-POS) and (1 - s'^2) in the denominators. Gates C-ROUTE (ROUTE_OK and
      the maximum), C-ECS-LEVEL (both level pairs), C-ECS-E2 and C-D4S-LEVEL (sanity), C-RHO-F1. The joint rows gain a 7th column ROUTE
      (NOTE_KT_P2_V1_35_JOINT_HEADER_v1 32d3e069), and the per-piece route values go to a side TSV.
      Lemma R's sigma and Phi_W enter R8 at Lemma R's own eps_R = RHO_EPS_R = 0.85 (pk02, Phi_eps keeps Lemma G's eps 1/4):
      C-RHO-R (eps_R in (0, 1), r* >= r0, the sigma grid check at eps_R, one eps for the sigma and Phi_W pair: r8_pair) with
      PLANT-RHO-SIGMA-R and PLANT-RHO-PAIR. The K-form rho_phi of Lemma E' keeps eps 1/4.
  (6) The normX_HS slot (SPEC_HS_INV_NORMX_v1_2 84f6a3e0): D3 rows by Lemma D3 of pk08/HS_NORMX_LEMMA_NOTE_v1.md (1340a52c),
      HS2_hi = COEF (1/lambda~_0,lo)^2 per piece and normX_hi = min(Lemma S', sqrt(HS2_hi)); gates C-HS-SRC, C-HS-NOTE, C-HS-OP, C-HS-J,
      C-HS-LAMBDA, C-HS-CBOX (with c_lo >= 0), C-HS-MIRROR (no D4 rows while held), C-HS-COV; C-HS-SPOT (a control) against kt_s8rf_v1's
      spot values (the record's N*_D3_SPOT, sources pinned). pk08's certified record pk08/out/HS_INV_NORMX_v1.kv (6b82dc63, run output
      aedbf7c3) is read in both modes; the MOCK record serves no gate. NORMX_BOUND reads
      MIN_OPERATOR_BOX_PLUS_SCHUR_TAIL_HS_INV.
  (7) Cert mode (ADD1 sect. 6): items mock, certdry and cert. CERT_MODE (certdry, cert) never loads I[N] (load_inputs
      refuses: C-CERT-NOI) and skips every comparison with the MOCK inputs (reader (a)'s mocks, reader (d), C-TP-DOM, the Lemma G and Lemma E
      kt_rb comparisons, the mock-input t row and its gates, C-KAPPA, P2-8's stand-in with C-COVX, C-REPF and the DH preview); cert reads Sets A,
      C and W through the certified path (C-A-BIND refuses until R4), certdry reads the MOCK records and writes MOCK exports (the rehearsal of
      the cert path, its exports equal to the mock run's). The cert writer kv_write_cert (pk15/out/ only, a certified header, no MOCK token,
      a temporary file in 'x' mode, the final name checked before the write and before os.rename, then the consumer reader's read-back) refuses
      while S9H_READER (kt_s9h_v1_3's joint reader) is not pinned. status_junif gives each export's status, FLOAT_IN and J_UNIFORMITY in one
      code path (J_UNIF_PP only with CERTIFIED); C-JUNIF-STATUS. C-READBACK reads every written export back key for key. Plants
      PLANT-CERT-NOI, -PATH, -MOCKTOKEN, -READER, -EXISTS, -REWRITE and PLANT-JUNIF-STATUS (none writes a file).
kt_p2_assembly_v1_34's docstring follows; its run line and file names change to v1_35.
kt_p2_assembly_v1_34.py -- pk15 (code/pk15/). REVISION of kt_p2_assembly_v1_33.py (427b0882; its mock run out_kt_p2_assembly_v1_33_mock.out
27617090 was VALID; the review found v1_33 OK), 2026-11-08, on the GOs of 04:18Z and 04:23Z after the review of pk02's
NOTE_TAU_CRUDE_v1 (pk02/NOTE_TAU_CRUDE_v1.md f2285009, with its ADD1 pk02/NOTE_TAU_CRUDE_v1_ADD1.md f72962da; reviewed with its ADD1; SOUND):
  (a) eps_y's gap is s_x,low - mu_y,high again (v1_32's form). By the note's L10 (H5) tau enters only the Weyl level ylev = max(mu_y,high, tau),
      s_y,high = ylev + c-bar, the gap tests and q = c-bar/(s_x,low - tau); eps_y needs only s_x - mu_y^S >= s_x,low - mu_y,high, which
      g_below > 0 implies. v1_33's ylev in eps_y cost a factor of about 1.66 at J = 300.
  C-KT0, a hard gate (R6a (C7), the note's H6): kt0 = 1 - c-bar - (s_x,high + c-bar), the denominator ball that m0lo divides by and the
      same arb expression, must be certainly positive before m0lo is formed. PLANT-KT0 (s_x,high replaced by 1 - 1.5 c-bar in that expression)
      must be refused by C-KT0.
  (Point 2) C-TAU-TRIAL, H2 as a machine gate inside load_tau. The sweep's run output names its script on line 1 by full sha256; that script
      (pk07/kt_s9h_v1_2.py, pinned here) holds TRIAL_SET with the four full sha256s, which must equal this file's pinned ts and vacres files
      (basename and full sha256, per N). The output's C-TRIAL line must name the same four files with the same sha8 prefixes and read PASS, and
      its C-TRIAL chain line must read PASS. The output prints sha8 prefixes only, hence the step through the pinned script. PLANT-TAU-TRIAL
      (the N4 ts pin changed) must be refused by C-TAU-TRIAL.
      The label side of H2 is pk03's cp rule (m3_run_v1_7 builds labels 0, 1, 3 by S8_ENTRY_LIST_v3's cp rule), cited in pk02's
      pk02/NOTE_TAU_CRUDE_v1_ADD1.md f72962da (M3_ENTRY_LIST_v1_2 l.19-20 = S8_ENTRY_LIST_v3 l.13; S9_ENTRY_LIST_v1 l.10).
  (C-TAU-N) the ADD1: the tau rows must be the export's rows of the assembly's N. load_tau reads the export's own N<N>_P<idx> labels
      beside the reader and refuses unless every row's rho_hi equals, as an exact decimal, the token on the line of its own N and index. N3's
      and N4's rho_hi differ by only about 3e-3 relative and the two grids are equal, so no number test would see a swap. PLANT-TAU-N (the
      reader's N4 and N3 rows swapped) must be refused by C-TAU-N.
  (INFO) KT-MARGINS per N: the smallest s_x,low - tau_up, g_below and 1 - 2 c-bar - s_x,high over the port rows (lower ends).
  (grep) Hypotheses used but not gated on the t path, found by a grep of v1_33 for divisions, roots, inverses and float conversions:
      C-DK0 (lemma_a_amp: sigma_0's Davis-Kahan denominator mhat - mu_x,high certainly positive; PLANT-DK0); C-SP (tprov: 1 - s'^2 certainly
      positive, the denominator of ||v_t||'s bound; m2b_eps gates s in (0, 1) only; PLANT-SP); C-GRAM (tprov: the Ritz-vector Gram G certainly
      positive definite by Gershgorin before G^-1, where python-flint's inv raised an exception rather than a refusal and positivity was not
      checked; PLANT-GRAM). Each plant counts only a refusal that names its gate. Non-outward conversions: tprov's t0p radius, ent_ad's bar and
      the two mean-value widths took float() of an arb end (round to nearest, at most 1 ulp short); each is now arb(0, 1) times the end.
      The full list, with what stays open on the MOCK joint path, is in NOTE_KT_P2_ASSEMBLY_v1_34_FREEZE.
  (doc) tau = rho_hi (tau_abs), the absolute S-scale reading of pk07's rho_hi, on the port's rows (the review sect. 4 (c)).
kt_p2_assembly_v1_33's docstring follows; its run line and file names change to v1_34.
kt_p2_assembly_v1_33.py -- pk15 (code/pk15/). REVISION of kt_p2_assembly_v1_32.py (4bf4d624; its mock run out_kt_p2_assembly_v1_32_mock.out
62bceea1 was VALID; the review found v1_32 OK), 2026-11-08, on the approval for (1)-(3):
  (1) One grid reading for every consumer (made a rule). An end string stands for both its decimal and its binary64 value
      (kt_s9h's reading; kt_s67_export_reader_v2_1's V1 note): grid_j(s, low) is the smaller (low) or larger of Fraction(s) and Fraction(float(s)).
      t_ends gives t's upper end from the smaller reading of jlo and t's lower end from the larger reading of jhi; tball's ball is their hull,
      so the piece's t range holds both readings of both ends by construction; the M2(b) and M4 laws are taken at the smaller reading of jlo
      (they are nonincreasing in J). C-GRID-HULL checks the raw ends on every piece by point comparison (t_hi at or above 1/J and t_lo at or
      below 1/J for both readings), and PLANT-GRID-DEC (v1_32's decimal-only ends) is refused. A containment test on the ball alone cannot
      tell the readings apart: arb stores the union's radius to about 30 bits, about 1e-14 of slack on a piece, far above the 1e-19 gap
      between the two readings, so v1_32's balls already held both readings (diagnostics out_diag_arbstr_v1.out 70f989ed and out_diag_gridhull_v1.out e6d34271).
  (2) the optional N-2 ([0, upper] from m4_law) is not adopted: lemma_a_cbar forms c-bar = sqrt(rho^2 sum) with R_e1, R_e3 inside rho,
      and a ball reaching below 0 gives nan there (the draft's dry run refused every piece, C-KT); m4_law keeps the ball around the upper end,
      which enters only increasing positions.
  (3) TAU_R certified by the crude bound (the FB-1, pk02's form; NOTE_TAU_CRUDE_v1 (pk02's note, named here; its sha8 goes into NOTE_KT_P2_ASSEMBLY_v1_33_FREEZE when pk02 freezes it; the review reviews it, and no certified export run of this path happens before the OK, main)): tau = rho_hi = L_1^odd/lambda_0,lo
      (S units, rounded up), per piece, from pk07's certified vertical sweep export_kt_s9h_v1_2_vsweep.kv (761084be) through its sha-pinned
      reader kt_s67_export_reader_v2_1 (b0a23237; load binds the export to its VALID run output out_kt_s9h_v1_2_vsweep.out f18072f4 by rule
      V2 and requires EXPORT_STATUS CERTIFIED), on the same grid (index for index, the same doubles). In lemma_a_cbar tau = rho_hi, the Weyl
      level below s_x is max(mu_y,high, tau) + c-bar (kt_rb's r_tau < 1 is not assumed), and eps_y's gap is s_x,low - max(mu_y,high, tau);
      q = c-bar/(s_x,low - tau). The FB-1 float scan (SCRATCH_kt_p2_fb1_v1.py, output 77ebce0c, t export b974089b) kept every port gate:
      corner ratio N4 1.014948 against 1.027, N3 1.006499 against 1.008; pk07's kt_s9h read of that export: pk07's mock sweep kt_s9h_m38.py 058536f7, out_kt_s9h_m38_sweep.out c73830f5: every C2-a kind and joint class holds at its plan threshold at both N (N4 same at d = 1 and N3 mixed at d = 2 rest on slack > 0 alone, as before FB-1; C-VERT-MODES is INVALID only because M2(b) is mocked there).
      OWN_FLOAT_TP is then tz alone, and M4SRC marks TAU_R CERTIFIED (the t export keeps the ASSUMED J_UNIFORMITY string while TZ_P2_3 is
      FLOAT). C-TAU-READ; INFO TAU; PLANT-TAU-PIN, PLANT-TAU-READER-PIN, PLANT-TAU-GRID. C-LA300 keeps kt_rb's FLOAT TAU_R for its comparison.
kt_p2_assembly_v1_32's docstring follows; its run line and file names change to v1_33.
kt_p2_assembly_v1_32.py -- pk15 (code/pk15/). REVISION of kt_p2_assembly_v1_31.py (f9935a6a; its mock run out_kt_p2_assembly_v1_31_mock.out
de65bd62 was VALID; the review found v1_31 OK), 2026-11-08, the decision (ii): the M4 wiring, the exports still MOCK overall:
  (1) A_t, A_am, R_e1 and R_e3 come from the certified M4 law record M4_KV_v1 (e209c53f, its asm output d3ed95bb) through its one sha-pinned
      reader m4_reader_v1 (d3f82819; load binds the record to its run output and runs the record checks and C-PINS). For each piece the law
      at the piece's left end, law(rec, kind, N, jlo), a decimal at or above L_k(jlo), bounds the quantity on the whole piece [jlo, jhi], as
      L_k is nonincreasing in J (SPEC_M4_LAW_v1_3 sect. 0). They replace reader (a)'s J = 300 A_t, A_am (kt_cert_v1_7's g records; reader (a)
      stays for its comparisons) and kt_rb_v1_5's FLOAT R_e1, R_e3 in the port's rows: lemma_a_cbar's residual ratios, lemma_a_amp's A_a,
      tprov's A_t. The t export's own FLOAT inputs are then tau_r and tz (OWN_FLOAT_TP), FINM holds the M4 record's empty FLOAT-IN list, and
      M4SRC marks LAW_A_T_A_AM and R_E1_R_E3 CERTIFIED; TAU_R and TZ_P2_3 stay FLOAT, so the t export keeps the ASSUMED J_UNIFORMITY string.
      C-M4-READ; INFO M4-AT-300; PLANT-M4-PIN and PLANT-M4-READER-PIN (a pin changed: refused).
  (2) C-GRID-EXACT (the grid condition, NOTE_STB_EXPORT_DEPS_v1 f030a7f5): the first jlo is exactly 300, each jhi string equals the next
      jlo, each finite end is a binary64 repr (repr(float(s)) == s), jlo < jhi, and the last jhi is 'inf' (t -> 0); PLANT-GRID-GAP (one jhi
      moved by a relative 1e-12: refused).
kt_p2_assembly_v1_31's docstring follows; its run line and file names change to v1_32.
kt_p2_assembly_v1_31.py -- pk15 (code/pk15/). REVISION of kt_p2_assembly_v1_30.py (9ec74758; its mock run out_kt_p2_assembly_v1_30_mock.out
4d15cc5f stopped at C-RITZ300 N=4 alone, VERDICT INVALID), 2026-11-08, on the approval (02:18Z) and its check:
  (1) C-RITZ300 compares the port's first piece with kt_rb's CERT300 lines. On the mock entries (from kt_s9b_v2, as kt_rb's) the comparison
      is within one set of entries and keeps v1_27's containment form, hard: each enclosure of lambda_0, s_x, mu_y holds kt_rb's midpoint,
      and each |a^_k| ball holds kt_rb's bar. On pk03's S9 records every leg compares two enclosures built from different entries (S9
      against kt_s9b_v2), which must meet but need not contain each other's midpoints or bars. There the hard form is overlap: each enclosure
      meets kt_rb's [lo, hi], and each |a^_k| ball's lower end is at most kt_rb's bar (an upper bound of |a_k|); midpoint containment and the
      upper leg (kt_rb's bar at most the ball's upper end) are INFO. On the S9 bars the Davis-Kahan ball of |a^_1| at N4 ends below kt_rb's bar
      (diagnostic copy, output 09e327c4): a tighter enclosure, not a defect. The gate line names the form; INFO RITZ300 gives the reason,
      the midpoints, the containment results and kt_rb's bar minus each upper end; PLANT-RITZ300-SWAP and the note swap run in the gate's
      form, and INFO RITZ300-SWAP-GAP prints how far the swapped lambda_0 ball lies from kt_rb's interval.
kt_p2_assembly_v1_30's docstring follows; its run line and file names change to v1_31.
kt_p2_assembly_v1_30.py -- pk15 (code/pk15/). REVISION of kt_p2_assembly_v1_29.py (b8e98eeb; its mock run out_kt_p2_assembly_v1_29_mock.out
ad36b195 was VALID; the review found v1_26 -> v1_29 OK: ebe44b68), 2026-11-08, the version that pins pk03's S9 records:
  (1) S9_RECORDS pins pk03's Ritz record and asm output per N by full sha256 (N4 m3_s9_N4_J300_v1_8_3.json c14756e9 + asm9.4 53aa28da, N3 m3_s9_N3_J300_v1_8_3.json 4f05913c + asm9.3 31cbb115; run manifest e67720cc); the port runs on them (RITZ_STATUS CERTIFIED for
      the entries; every other t-path input is as in v1_29, so the exports stay MOCK). load_ritz now also refuses keys beyond the 18
      (the review 4). PLANT-RITZ-NOS9 becomes PLANT-RITZ-S9-PIN (an S9 file failing its pin). C-WIDTH-PORT and C-RITZ300 are read on S9's bars.
  (2) dtx takes kt_rb's eps_0 h0t with h0t = d0 NH (key t0t from lemma_a_amp; the mock-input row keeps t0, a
      conservative departure); ritz_piece's res_k squares the upper end of |r_ki|; C-LA300's tolerance is 1e-2.
  (3) the per-direction conditions: the rows take the componentwise intersection of the PD and DK vectors (pd_dk_meet; both hold v_k with
      u_k . v_k > 0, and an empty intersection is refused); C-PD-CONTROL on the ball diag(1, 0.5, 0.2) +- 1e-6 (both bounds contain e_k, and the
      PD bar is at most the DK bar); PLANT-PD-ZEROGAP (diag(1, 0.5, 0.5): no gap, refused).
kt_p2_assembly_v1_29's docstring follows; its run line and file names change to v1_30.
kt_p2_assembly_v1_29.py -- pk15 (code/pk15/). REVISION of kt_p2_assembly_v1_28.py (cfc36f7b), 2026-11-08. v1_28's mock run
(out_kt_p2_assembly_v1_28_mock.out 58ce3f9f) stopped in stage item (v) with VERDICT INVALID (ERROR): pd_vectors squared each residual ball
r_ji as a product of the ball with itself, whose lower end goes below 0 when the ball straddles 0, so the square root was nan and every
piece was refused (q_k not positive). The only change: R_j is now the square root of the sum of the squared upper ends of |r_ji|, which
still bounds ||r_j(A)|| for every A in the ball (NOTE_P2_17_RITZ_PD_v1 sect. 3).
kt_p2_assembly_v1_28's docstring follows; its run line and file names change to v1_29.
kt_p2_assembly_v1_28.py -- pk15 (code/pk15/). REVISION of kt_p2_assembly_v1_27.py (628118e4; its mock run out_kt_p2_assembly_v1_27_mock.out
96597c51 was VALID), 2026-11-08, on the approval for the per-direction eigenvector bound:
  (1) NOTE_P2_17_RITZ_PD_v1 (a753c254): ritz_piece's Ritz vectors now come from pd_vectors. For every symmetric A in the ball C,
      (lambda_k - lam~_j) u_j . v_k = r_j . v_k with r_j = A u_j - lam~_j u_j, so |u_j . v_k| <= R_j/g_kj, with R_j the arb bound of ||r_j|| over
      the ball and g_kj = |lam~_k - lam~_j| - res_k - rF (Weyl plus the disjoint residual intervals); u_k . v_k follows from ||v_k|| = 1 with the
      sign u_k . v_k > 0. kt_rb's uniform Davis-Kahan bar (vecmode 'DK') stays for the comparisons: C-RITZ300 and C-LA300 run on DK, the rows
      on PD. New: C-PD-DK (the PD and DK vectors overlap on every piece; PLANT-PD-DK), PLANT-PD-GAP (gaps understated by a factor 10^-6 make
      the bound fail), C-WIDTH-PORT (the port rows' corner ratio within the budget at d^h + 1 at both N; PLANT-WIDTH-DK: the DK rows are refused
      at N4), and INFO PD-BARS (both bars and both corner ratios per N). The widths use the mock entry bars; C-WIDTH-PORT is read again once the
      S9 records are pinned.
kt_p2_assembly_v1_27's docstring follows; its run line and file names change to v1_28.
kt_p2_assembly_v1_27.py -- pk15 (code/pk15/). REVISION of kt_p2_assembly_v1_26.py (3b5b20f6; its mock run out_kt_p2_assembly_v1_26_mock.out
e1725a56 was VALID; the review found v1_24 -> v1_26 OK: f48fe024), 2026-11-08, on the approval for item (v) against mocks:
  (1) Item (v) of P2-17 (NOTE_P2_17_RITZ_PIECES_v1 d3cbeb18): the per-piece Ritz and Lemma A data. On every piece of the grid the 18 S9
      entries (G,b,c T,b,c Iht,b Dx,b, the keys agreed with pk03) are balls over the piece's t-ball in the direct form. ritz_piece is
      kt_rb_v1_5's ritz_cert in arb (interval Cholesky, Weyl with rF, disjoint enclosures, Davis-Kahan vector bars, amplitude balls) with Iht
      in place of Ih. lemma_a_cbar and lemma_a_amp are its assembly_cert Lemma A part, with eps_r and s from law_v1 at the piece's jlo, mhat
      over the piece from the M2(b) record's m1..m3, Lemma B's NA-prime (NOTE_P2_17_BETA_v1 aa37c76e, SOUND) in place of BETA_R
      mhat/lambda~0, Lemma G's Hbad-prime, Gbad-prime and Abad-prime at the levels (40, 20) with u from the M2(b) eps_r, and the Ritz Gram of
      the c_k. tprov then gives each piece's t export row, and the export takes these rows; the J = 300 mock-input row stays as the reference
      of C-QV4, C-PT and C-WIDTH. Still FLOAT: R_e1 and R_e3 (kt_rb's C-IN values), TAU_R, tz and dtz (the mock inputs; P2-3), and A_t, A_am
      at J = 300 (reader (a), until pk02's LAW). So OWN_FLOAT_TP is tau_r R_e1 R_e3 tz, and the t export keeps J_UNIFORMITY ASSUMED.
      Entries: MOCK mode reads MOCK_RITZ_ENTRIES_v1 (mocks/mock_ritz_entries_v1.kv d28e28e2, built by SCRATCH_mk_mock_ritz_entries_v1.awk
      065a147c from kt_s9b_v2's ENTRY lines and kt_sh1_v1's Iht lines). CERTIFIED mode reads pk03's S9 record per N through
      m3_reader_v4_4, pinned by full sha256 with its asm output, with its trial_set equal to the pinned ts and vacres files (basename:sha256).
      No S9 record is pinned yet, so CERTIFIED refuses; a KV MOCK copy is refused in CERTIFIED mode at its FORMAT/TAG (PLANT-RITZ-MOCK-CERT).
      Gates: C-RITZ-READ; C-RITZ300 (the first piece holds kt_rb's CERT300 lambda_0, s_x and mu_y midpoints and its |a^_k| bars); C-GAP (every
      piece: Cholesky, disjoint enclosures, Davis-Kahan gaps, Kato-Temple, C-SX, C-SIGN0); C-LA300 (Lemma A on the first piece with kt_rb's
      FLOAT inputs reproduces its CBAR line within 5e-2); C-NA (NA-prime's L >= 1 and NA-prime >= every piece's |a^_00|); C-PT-PORT (C-PT's
      identity and A_t > 0 on every piece). Plants: PLANT-RITZ-MOCK-CERT, PLANT-RITZ-NOS9, PLANT-RITZ-MISSING, PLANT-S9-TRIAL,
      PLANT-RITZ300-SWAP (G,0,0 and G,1,1 exchanged, which moves lambda_0 by about 5e-3; INFO RITZ300-NOTE-SWAP reports whether the note's
      G,0,1/G,1,3 swap is refused at these bars), PLANT-RITZ-BAR (G,1,1's bar raised to 1: the note's x10^2 does not reach these gaps, so
      the plant uses a bar that must break the Cholesky step), PLANT-NA (an NA from the FLOAT literal carries beta_r and cannot be tagged
      CERTIFIED).
  (2) the four points on v1_26 (f48fe024), each with plants: C-TP-DOM (mock eps_r and s-prime at or above the M2(b) ends, mock
      lt0 at or below (1 - eps_r) mhat_lo, mhat_lo from the M2(b) record's own m1..m3 and checked against its MHAT_UP; PLANT-TP-DOM-EPS, -SP,
      -LT0, -MOCKMHAT, PLANT-TP-MHAT-SRC; the bound holds at J = 300 only), C-M2B-TRIAL (PLANT-M2B-TRIAL), C-GRID's first jlo >= 300
      (PLANT-GRID-START), and every reader call at ctx.prec 256 (m2b_call; C-M2B-PREC, PLANT-M2B-PREC).
  (3) J_UNIFORMITY, with the string pk07 pinned: the joint and means exports carry J_UNIF_PP; the t export carries it only when every M4
      input of the t path is certified (t_uniformity), so today the ASSUMED string. C-JUNIF, PLANT-JUNIF-T.
kt_p2_assembly_v1_26's docstring follows; its run line and file names change to v1_27.
kt_p2_assembly_v1_26.py -- pk15 (code/pk15/). REVISION of kt_p2_assembly_v1_25.py (dc4209b7), 2026-11-07. v1_25's mock run
(out_kt_p2_assembly_v1_25_mock.out 27d2e685) stopped in the exports stage with VERDICT INVALID (ERROR): kv_write refuses the word CERTIFIED in
any value of a MOCK export, and v1_25's new KAPPA_SOURCE value named the certified eps_r. Every gate before the exports passed and every plant
fired. The only change: KAPPA_SOURCE now reads (eps_r of M2B_KV_v1 at J = 300).
kt_p2_assembly_v1_25's docstring follows; its run line and file names change to v1_26.
kt_p2_assembly_v1_25.py -- pk15 (code/pk15/). REVISION of kt_p2_assembly_v1_24.py (ded07b5e; its mock run out_kt_p2_assembly_v1_24_mock.out
0196fe45 was VALID; the review found v1_18 -> v1_21 and v1_21 -> v1_24 OK: 8f7fd44f, ba6ad9e5), 2026-11-07:
  (1) The M2(b) reader (the order; pk02's message of 2026-11-07): pk02's certified vacuum record M2B_KV_v1.txt (13cc0d9a, VERDICT
      VALID; the CHECK_M2B_ASM_v1 8d465b64 OK TO RUN, the approval) through its one sha-pinned reader m2b_reader_v1.py (3580bce7): load(record,
      asm output, expected_sha256, reader_sha256) binds the record to out_m2b_asm_v1.out (518f7a4c) and runs the record checks and C-PINS;
      law_v1(rec, N, 300) gives eps_r and s as decimal strings at or above their upper ends. LAW v1 is nonincreasing in J on [300, oo) (the
      record's C-MONO), so the J = 300 values bound every piece. The joint path takes them (CE's eps and s-prime = s (1 + s), the kt_rb form
      that the mock key sp holds; kappa_bound), so the joint export's own FLOAT list OWN_FLOAT_JT is empty. The t path keeps the mock inputs'
      FLOAT eps_r and s-prime until item (v) brings its certified per-piece inputs (C-QV4's float reading is built on them), so OWN_FLOAT_TP is
      unchanged. C-M2B: law_v1 at J = 300 equals the record's N*_EPS_R_300 and N*_S_300 within 1e-9, decreases from J = 300 to 600, 3000 and
      10^6, and the record's ASM_SHA256 is the pinned m2b_asm_v1.py. C-FLOATIN-JT: with the four record lists empty the joint export would read
      CERTIFIED; C-FLOATIN-OWN and PLANT-FLOATIN-OWN move to OWN_FLOAT_TP. Plants: PLANT-M2B-PIN, PLANT-M2B-ASM-PIN and PLANT-M2B-READER-PIN (a
      file failing its pin), PLANT-M2B-MOCKFORMAT (the reader's check refuses FORMAT M2B_KV_v1 MOCK), PLANT-M2B-BIND (the reader's binding
      refuses a changed record) and PLANT-M2B-INF (s = inf is refused).
  (2) C-C1 live: load_m2b runs check_c1 on the pinned record's lines, so C1 is cleared and every export carries OPEN_CONDITIONS none. v1_14's
      unit test stays inside C-C1. PLANT-C1-LIVE-NOSPACE: the record with the no-space wording is refused.
  (3) The addition on the note 1 (8f7fd44f): g00_s7 refuses unless the S7 record's trial_set names VACRES[N], the vacres file the
      assembly pins for S_eps, with its pinned sha prefix (check_trial_set). C-G00-TRIAL; PLANT-G00-TRIAL puts N3's vacres in the N4 record.
  (4) one plant per condition. PLANT-G00-A0EXACT (a0_exact alone), PLANT-G00-A0BALL (the a_0 ball alone) and PLANT-G00-PIN-ASM
      (the asm output pin alone) join PLANT-G00-NORM and PLANT-G00-PIN.
  (5) the note on v1_24 (ba6ad9e5): INFO CE-CLASS prints each class's c_t ball per N (the first piece's mid and width, then the mid range
      and the largest width over the pieces), so that a class enclosing a different quantity would show.
  (6) F-2 refresh: E2B_FLOAT and E2_GLEV come from e2_bound_v4.awk (1d08e3d4; out/e2_bound_v4.txt 1217347a), which is e2_bound_v3 with the
      certified eps_r and s; C-E2-FLOAT compares with it.
kt_p2_assembly_v1_24's docstring follows; its run line and file names change to v1_25.
kt_p2_assembly_v1_24.py -- pk15 (code/pk15/). REVISION of kt_p2_assembly_v1_23.py (31c7c359; its mock run out_kt_p2_assembly_v1_23_mock.out
46521385 was VALID), 2026-11-07:
  (1) pk07's ask under the route B for SH4's c_e(J): EXPORT_P2_T_v1 gains FIELDS ce_lo ce_hi, per piece the intersection over D3, D4 and
      D4M of the joint path's Lemma E-prime balls of c_t = E xi_t (ce_lo rounded down, ce_hi up; MOCK SM entries here). C-CE-T: the
      intersection is non-empty on every piece. INFO CE-T prints min ce_lo and max ce_hi per N against the P-3 gate (RULING_P3_BETAH_TRBH
      19f74c2b: max ce_hi <= (N - 1)/2 - c_N/300, c_N = 2 + (N - 1)(N - 3)/8) and pk07's binding lower ends (CE_LO_NEED). The per-class
      means export stays as a diagnostic.
  (2) The C1 pin fix: the C1 string's origin is pk02's SPEC_M2B_CERT_v1_ADD3.md (cb472451, frozen), now pinned with pk07's frozen
      kt_s9h_m21.py (472bc24c) for the no-space wording; C-C1-SOURCE checks that the SPEC holds C1_CLAIM exactly once and kt_s9h_m21.py
      C1_NOSPACE exactly once. The v1_14 citation now names the SPEC; kt_s9h_v1.py, rewritten in place after v1_14 copied the string, is
      frozen at 0cc5b670.
  (3) the check of v1_18 (ac408d1e), minor (1): C-TRACE-REC tests lambda_0 of the L = 600 chain that trace_T uses.
kt_p2_assembly_v1_23's docstring follows; its run line and file names change to v1_24.
kt_p2_assembly_v1_23.py -- pk15 (code/pk15/). REVISION of kt_p2_assembly_v1_22.py (bccd66d1; its mock run out_kt_p2_assembly_v1_22_mock.out
69eb76e0 was INVALID on C-MEANS alone: its rule asked every mean ball to sit within 1% of the J = 300 FLOAT mean, but the mock entries' bars make
the balls up to 10.4% wide at N4 (D4) and 3.9% at N3, while every one of the 5424 balls contains the FLOAT mean). One change: C-MEANS asks every
ball to be ordered and positive, and the first piece (J in [300, 300.75]) of every class to contain the J = 300 FLOAT mean for both factors;
INFO MEANS also prints the largest relative width of c_t per N. Every other line is v1_22's.
kt_p2_assembly_v1_22's docstring follows; its run line and file names change to v1_23.
kt_p2_assembly_v1_22.py -- pk15 (code/pk15/). REVISION of kt_p2_assembly_v1_21.py (bcca4a72; its mock run out_kt_p2_assembly_v1_21_mock.out
af72e907 was VALID). The approval of 2026-11-07 on route B for SH4's c_e(J) (pk07's beta_H provider): a third export, EXPORT_P2_14_MEANS_v1,
carries per piece and class the joint path's Lemma E-prime mean balls (m = 1 on the SM window entries): ce for the top-row horizontal edge t
(c_t = E xi_t) and cf for the second factor (D3: bb, c_bb = c_t by the flip; D4 and D4M: the vertical b). FIELDS jlo jhi ce_lo ce_hi cf_lo
cf_hi, ends rounded outward; FLOAT_IN and OPEN_CONDITIONS as the joint export's. It goes certified when M3's certified window entries and the
fixed eps_r and s exist. C-MEANS: 5424 rows, every ball ordered and within 1% of its FLOAT mean (MEAN_FLOAT, MEANV_FLOAT); INFO MEANS prints
c_t's range per N and (N - 1)/2 - c_t,hi for SH4's condition. C-SELF, PLANT-MOCK-D and C-NOCERT cover the new export.
kt_p2_assembly_v1_21's docstring follows; its run line and file names change to v1_22.
kt_p2_assembly_v1_21.py -- pk15 (code/pk15/). REVISION of kt_p2_assembly_v1_20.py (2a13e310; its mock run out_kt_p2_assembly_v1_20_mock.out
005eb83c was VALID). Labels only: two printed lines still called G_00 a MOCK after v1_20 switched it to S7's certified lower end (INFO LEMMA-G
and C-G00-FLOAT); they now say so. No value changes.
kt_p2_assembly_v1_20's docstring follows; its run line and file names change to v1_21.
kt_p2_assembly_v1_20.py -- pk15 (code/pk15/). REVISION of kt_p2_assembly_v1_19.py (55f06527; its mock run out_kt_p2_assembly_v1_19_mock.out
11655278 was VALID). The decision of 2026-11-07: Phi's G_00 comes from S7's certified g,0,0 now.
  (1) load_g00('CERTIFIED') returns, per N, the lower end over every J >= 300 of S7's certified g,0,0 (g00_s7: the record and its asm output must
      match their pins, the entry must pass check_g00_entry, then g00_lower): 0.99999126 at N4 and 0.99999560 at N3. It refuses only if a record
      or its asm output fails its pin (PLANT-G00-PIN, in place of v1_19's PLANT-G00-CERT) or the entry fails the normalization pin
      (PLANT-G00-NORM and PLANT-G00-CLAIM stay). C-G00-S7 also checks that the run's G_00 is that lower end.
  (2) Identity: pk03 confirmed that S7's certified g,0,0 is the same object as S9's G,0,0 (stated next to G00_NORM). M3's records are not
      affected by.
  (3) G00 leaves FLOAT_IN in both exports; G00_MOCK stays for tests only.
kt_p2_assembly_v1_19's docstring follows; its run line and file names change to v1_20.
kt_p2_assembly_v1_19.py -- pk15 (code/pk15/). REVISION of kt_p2_assembly_v1_18.py (5e052976; its mock run out_kt_p2_assembly_v1_18_mock.out
1c49542c was VALID). The rule on the triangle note and pk03's confirmation of G,0,0, 2026-11-07:
  (1) G00_NORM states pk03's confirmed normalization: G,0,0 = I_D(J)/main_D(J) = <phi_0, K phi_0>/main_D over strip_graph(2, (A, B)), V = 6,
      main_D = exp of riglap2's logmain at J, a0_exact 1. check_g00_entry pins it on a record: the claim starts with G00_CLAIM (copied by tool
      from pk03's S7 record m3_b5_N4_J300_v1_7.json 3e4502dd; N3 the same), a0_exact is '1' and the a_0 ball is exactly 1 (a wrong main term or
      area factor moves the t = 0 value). PLANT-G00-NORM (a main term off by a factor 2, so a_0 = 2) and PLANT-G00-CLAIM (main_T in the claim)
      are refused.
  (2) A reader test on the real certified entry: S7's g,0,0 (m3_b5_N<N>_J300_v1_7.json with its asm output, pinned; pk03: the same object
      as S9's G,0,0) through m3_reader_v4_4 passes check_g00_entry, and g00_lower gives its lower end over every J >= 300 (the cubic as a ball
      over t in [0, 1/300], minus err), which is 1 - err. C-G00-S7. Phi keeps the MOCK G_00 = 1 and FLOAT_IN keeps G00 until main confirms
      the source.
kt_p2_assembly_v1_18's docstring follows; its run line and file names change to v1_19.
kt_p2_assembly_v1_18.py -- pk15 (code/pk15/). REVISION of kt_p2_assembly_v1_17.py (c2a99b41; its mock run out_kt_p2_assembly_v1_17_mock.out
32988a5b was INVALID: the new C-TRACE-REC block named its k1 reference 'ref', which shadowed the joint loop's dict of FLOAT reference rows, so
ref.get raised in stage Lemma E). One change: that variable is k1ref. Every other line is v1_17's; v1_17's printed Lemma T values stand (exact
Z_T at J = 300: N4 0.99918, 0.99856, 0.99862; N3 1.00015, 1.00073, 1.00032 for W^(1-eps), W_theta, W_theta^(b)).
kt_p2_assembly_v1_17's docstring follows; its run line and file names change to v1_18.
kt_p2_assembly_v1_17.py -- pk15 (code/pk15/). REVISION of kt_p2_assembly_v1_16.py (21ed85dc; its mock run out_kt_p2_assembly_v1_16_mock.out
f6fc1b1d was VALID; the review found Lemma R and v1_16 SOUND). Item 2 of the slice-47 list, the certified triangle norms (NOTE_P2_17_TRIANGLE_v1
e76ec496):
  (1) Lemma T-prime: every Phi (Phi_eps, Phi_eps,theta, Phi_eps,theta,b) is S^2 (tau_D/(w_1 w_2))^(n/2)/G_00 (phi_T; TB in the trace), with no
      remainder ratio and no power of J. G_00 is its only J-dependent input: load_g00 (CERTIFIED refuses until M3's S9 record is pinned, which
      must declare G00_NORM; MOCK G00_MOCK = 1), check_g00 refuses a lower end that is not certainly positive (PLANT-G00-NONPOS), and
      C-G00-FLOAT asks it to lie within 5% of 1. C-PHIT-FORM checks the closed form against its k1_lim form at J = 300 and 3000.
  (2) Lemma T at J = 300 as a check (C-TRACE): the exact trace (lambda_list from series starts and the downward recurrence; trace_T with the
      geometric tail, PLANT-TRACE-L for a too-short sum) lies below the Lemma T-prime bound for the three triangles; INFO TRACE prints Z_T and
      the factor. C-TRACE-REC: the recurrence's lambda_0 agrees with k1.
  (3) The remainder ratios retire (remainder_ratios and need_ratios stay uncalled; PLANT-ZR-MISSING is gone). The own FLOAT_IN tokens Z_eps and
      Z_eps_theta_b give way to G00. E2_GLEV, E2B_FLOAT and RHO_FLOAT take e2_bound_v3's values (cd2c38b3).
kt_p2_assembly_v1_16's docstring follows; its run line and file names change to v1_17.
kt_p2_assembly_v1_16.py -- pk15 (code/pk15/). REVISION of kt_p2_assembly_v1_15.py (a2f53bdf; its mock run out_kt_p2_assembly_v1_15_mock.out
ece74936 was VALID; the review found Lemma E-prime and v1_15 SOUND). One change, the condition 3 (F1 with the factor 2): rho_phi is bounded by
Lemma R (NOTE_P2_14_RHO_v1 32222a69): rho_phi <= 1 + 2 sigma_eps sqrt(Phi_W), Phi_W = Phi_eps/S_eps^2 (the same triangle and remainder ratio),
sigma_eps = h(max(r*, r0)) with h(r) = e^(-eps B r)(q_Q r^2 + q_L r - 1) (rho_terms, rho_h; the z9sym q at t = 1/300). The bound is the CE
constant 'rho' that e1_bound and lemma_e read; the joint FLOAT_IN drops rho_phi (its FLOAT part is Z_eps, already listed). C-RHO: 1 <= rho_phi
<= 1.1 and within 1e-4 of rho_float_v1 (4f74b8fa); C-RHO-GRID: check_sigma finds no grid value of h on [r0, 50 r0] above sigma_eps;
PLANT-RHO-SIGMA: check_sigma refuses h(r0 + 1) as sigma. E2B_FLOAT takes rho_float_v1's Delta_E2 (box times rho_phi).
kt_p2_assembly_v1_15's docstring follows; its run line and file names change to v1_16.
kt_p2_assembly_v1_15.py -- pk15 (code/pk15/). REVISION of kt_p2_assembly_v1_14.py (39e6e050; its mock run out_kt_p2_assembly_v1_14_mock.out
13531d5a was VALID). The rules on NOTE_P2_14_E2_v1_2 and the pre-read of its sect. 2a, 2026-11-07:
  (1) One theta for Abad' and Lemma E-prime: theta = 0.7 (THETA_G). Why 0.7: at N4 the D4 and D4M b-tail decays like e^(-A_theta L_b),
      and theta = 0.5 fails the d = 3 tolerance there (e2_bound_v2: ratio 1.03), while 0.7 gives 0.571; 0.9 would give 0.390 with weaker
      Laplace conditioning (). With the remainder ratio doubled, 0.7 still gives 0.510 (D3) and 0.656 (D4, D4M; e2_bound_v2_sens2).
      Lemma E-prime reads its theta separately (the_s); C-THETA requires both to be THETA_G = 0.7; PLANT-THETA.
  (2) Phi_eps, Phi_eps,theta and Phi_eps,theta,b each take their own remainder ratio Z_T(w)/Z_psi (remainder_ratios: 'eps',
      'theta', 'theta_b'; W_theta^(b) is the same for D4 and D4M by the flip T <-> B). CERTIFIED refuses until a certified source is pinned;
      MOCK uses kt_rb's ratio times a separate MOCK factor per set (ZR_MOCK), and need_ratios refuses a missing one (PLANT-ZR-MISSING). The own
      FLOAT_IN tokens split Z_tri into Z_eps (both exports) and Z_eps_theta_b (joint).
  (3) v1_14's vertical level check (L_b >= c+ + m/A_theta from the exact header constants; at m = 1 the general c+ + 2
      check already implies it, since A_theta > 1/2) gets an edge test: C-E2-VLEVEL-EDGE passes a level 2^-20 above c+ + 2/A_theta, and
      PLANT-E2-VLEVEL-EDGE refuses one 2^-20 below.
  (4) The per-class C-E2-FLOAT lines name e2_bound_v2 (v1_14 printed v1 there).
kt_p2_assembly_v1_14's docstring follows; its run line and file names change to v1_15.
kt_p2_assembly_v1_14.py -- pk15 (code/pk15/). REVISION of kt_p2_assembly_v1_13.py (65f5cb54; its mock run out_kt_p2_assembly_v1_13_mock.out
800ee721 was VALID). On the mocks, 2026-11-07:
  (1) Lemma E-prime (NOTE_P2_14_E2_v1_2 b741c439 sect. 2a, the Lemma G cut; not yet reviewed). lemma_e takes Phi_eps for Phi, S' =
      sqrt(Phi_eps Phi_eps,theta,b) for S (C['S']; Phi_eps,theta,b on lg_weights_b, bond b's weight cut to (1 - theta)(1 - eps)A), and
      A_theta = theta (1 - eps) A for the A-weighted vertical sups, with the vertical level check L_b >= c+ + m/A_theta. One theta (0.7) serves
      Abad' and Lemma E-prime. The g-levels drop to e2_bound_v2's optimum (N4: D3 25.5/25.5, D4 and D4M 19.5/26; N3: 20/20, 15/24.5), and
      C-E2-FLOAT compares with e2_bound_v2 (e9ac1e69). The joint export's own FLOAT_IN list becomes eps_r s Z_tri rho_phi. The DH preview names
      d^h = 3 at N4 where the FLOAT slack at d = 3 is positive; the rule holds N4 at 4 until kt_s9h's certified DH.
  (2) C-C1 (the decision of 2026-11-07). check_c1 clears C1 only if exactly one line of the M2B record starts with 'CLAIM = ' and holds
      C1_CLAIM exactly once: the 41-byte string of pk07's kt_s9h_v1.py (09344ac4, M2B_CLAIM_G), copied by tool; its origin, pinned from v1_24, is pk02's SPEC_M2B_CERT_v1_ADD3.md cb472451. open_conditions() keeps C1
      open until a pinned M2B record passes. The M2B record is not pinned yet, so both exports keep C1 open. C-C1 (unit test),
      PLANT-C1-NOSPACE (the wording of kt_s9h_m21.py 472bc24c), PLANT-C1-TWICE.
kt_p2_assembly_v1_13's docstring follows; its run line and file names change to v1_14.
kt_p2_assembly_v1_13.py -- pk15 (code/pk15/). REVISION of kt_p2_assembly_v1_12.py (9e9fa12b; its mock run out_kt_p2_assembly_v1_12_mock.out
61f7e34f was INVALID on C-JPOW alone). One change, to C-JPOW. phi_main's ratio between J = 3000 and J = 300 is exactly 1 at every point of its
balls, but the trial weights A and B enter as hulls about 1e-16 wide (kt_rb v1_2's convention), and ball arithmetic does not see that both J
values carry the same A and B: the ratio's ball is about 1e-15 wide, so v1_12's 1e-40 test could not pass. v1_13 splits off the J-dependent
factor jfac(N, J) = k1_lim(J)^3 (2 pi/J)^(-3n/2), whose ratio C-JPOW now tests against 1e-40 (exact constants only), and tests phi_main's ratio
against 1e-12, still far below the effect of any wrong power of J (a factor 10^(1/2) or more between the two J). Every other line is v1_12's.
kt_p2_assembly_v1_12's docstring follows; its run line and file names change to v1_13.
kt_p2_assembly_v1_12.py -- pk15 (code/pk15/). REVISION of kt_p2_assembly_v1_11.py (f5352655; its mock run out_kt_p2_assembly_v1_11_mock.out
e649d67b was VALID). Lemma G (NOTE_P2_17_GBAD_ABAD_v1 f44b1962), coded on the mocks, 2026-11-07:
  (1) Reader (f): the z9sym trial coefficients q1, q2, q3 (pk11/out/vacres_K3_N<N>_sym_v1.json, pinned), taken exactly. S_eps by (G3) at
      t = 1/300 (s_eps) and kt_rb's supp0 on the same q (supp0_kt). C-SEPS: S_eps below supp0 and within 2e-6 of seps_v1's FLOAT values.
  (2) Phi in certified form (phi_lg): c_K S^2 ||W'||^2/||psi-hat||^2 <= S^2 k1_lim^3 (main_T(w)/main_D) Z_T(w)/Z_psi at J = 300, with riglap2's
      logmain in arb (triangle tau = a1 a2 + (a1 + a2) b; main_D on lapl2.strip_graph(2), tau_strip). c_K takes the limit bounds
      k1_lim = 1/(2J) (N = 3) and sqrt(2/pi) J^(-3/2) (N = 4), so the J-powers cancel exactly. C-JPOW checks the cancellation (J = 3000 against
      300). C-K1-LIM checks k1 < k1_lim at N = 4, J = 300 and 3000 (k1 from the I_1 series; N = 3 is exact), and (k1_lim/k1)^3 is printed.
      the remainder ratio Z_T(w)/Z_psi is an input from the certified run. MOCK here: kt_rb's ratio backed out of its Gbad/Hbad
      (zr0, which carries (1 + 1/kappa)^2; C-ZR0 asks 0.5..2) times Z_T(w)/Z_T(w0) = 1 (ZRATIO_MOCK). eps = 1/4; theta = 0.7, so the TM and MB
      weights of W_theta are 2(1 - theta)(1 - eps)A = 0.57 (171 at J = 300: a smaller theta than 0.9 costs little).
  (3) Gbad' = tau~0(Lam) kappa (kappa + u) sqrt(Phi_eps) (G1) replaces kt_rb's Gbad in ||Q_4 v_t||. Abad'(Lam_a) (G2) is computed and printed
      for item (v)'s a-chain; the t export still takes the a-side from the mock inputs. C-QV4 now checks the formula with kt_rb's Gbad against
      the float reading, and the Gbad' value is an INFO line. C-GBADP: Gbad' < Gbad and Abad' < Abad. PLANT-GBADP-LEVEL, PLANT-ABADP-LEVEL,
      PLANT-SEPS-EPS. The t export's FLOAT_IN gains Z_tri and its header GBAD_SOURCE.
  (4) The C1 rule: both exports carry OPEN_CONDITIONS (C1, the |g| form of M2(b)'s bound (b), which R6a l.44 and Lemma E's step (E4) use).
      export_status and certified_tag read open conditions: with every FLOAT-IN list empty and C1 open the status is
      CERTIFIED_GIVEN_OPEN_CONDITIONS. C-OPEN; PLANT-OPEN-C1.
kt_p2_assembly_v1_11's docstring follows; its run line and file names change to v1_12.
kt_p2_assembly_v1_11.py -- pk15 (code/pk15/). REVISION of kt_p2_assembly_v1_10.py (beb84cfd; its mock run out_kt_p2_assembly_v1_10_mock.out
91cb72bb was VALID). Code items of the Lemma E review (SOUND; the note is now NOTE_P2_14_E2_v1_1
6b8f85a9), 2026-11-07:
  (1) F2. e_1 = (2 eps_r rho_phi + eps_r^2) u^2/(1 - s'^2) (e1_bound) takes rho_phi from the constants, as lemma_e's e_f does; s' >= s keeps
      the denominator on the safe side. C-E1-RHO: e_1 at rho_phi = 1.5 exceeds e_1 at the run's rho_phi (1, MOCK).
  (2) m1. norm_win refuses a horizontal m = 2 level below c+ (D3 both slots, D4 the t slot), as normx_sprime does. PLANT-NORMX-HLEVEL D3, D4.
  (3) m2. Lemma E's ends are [min(x, (1 - s'^2) x) - s-part, max(y, 0) + s-part], x and y the ends of R_f (e_lower, e_upper, mean_ends;
      check_e_lower asserts the lower end on every piece); E2_hi takes max(R, 0). C-E-LOWER: unit control (R = -1, 1 for the lower end; -1, 2
      for the upper). PLANT-E-LOWER: (1 - s'^2) x on x < 0 is refused. The FLOAT numbers do not move (the means' lower ends are positive).
  (4) The assembly's own FLOAT inputs join FLOAT_IN under the record name kt_p2_assembly, as told to pk07: the joint export
      eps_r s Phi Psi supp0 rho_phi (Lemma E; normX's kappa_max through eps_r), the t export eps_r s Phi Psi supp0 tau_r beta_r R_e1 R_e3 (the
      kt_rb chain behind the mock inputs t~, a~, q, eps_0, eps_y). C-FLOATIN-OWN: with the four record lists empty the own list still gives
      CERTIFIED_GIVEN_FLOAT_IN; PLANT-FLOATIN-OWN: certified_tag refuses it. load_p2_8's certified branch, once a producer is pinned, must
      return that record's FLOAT_IN for the joint export (it refuses until then).
kt_p2_assembly_v1_10's docstring follows; its run line and file names change to v1_11.
kt_p2_assembly_v1_10.py -- pk15 (code/pk15/). REVISION of kt_p2_assembly_v1_9.py (ea7c7b44; its mock run out_kt_p2_assembly_v1_9_mock.out
7065555e was VALID). One change, the correction of 2026-11-07 to C-WIDTH: above the corner budget at the current mixed d^h the remedy
is a higher mixed DH (kt_s9h decides the certified DH from certified slack; P2-12 covers the step below), not a dead export. So C-WIDTH prints
the corner line with L against the budgets at d^h and d^h + 1 and an INFO line naming the d^h that L supports, and it is a hard gate only
when L exceeds the d^h + 1 budget (1.033 at N4, 1.030 at N3), which is past P2-12's one-step allowance: stop and ask. PLANT-WIDTH-CORNER
now lowers At_lo by 4% at N4 (L = 1.042 > 1.033); 3% gives L = 1.031, below the d^h + 1 budget, and is printed as INFO (d^h = 4 supported).
kt_p2_assembly_v1_9's docstring follows; its run line and file names change to v1_10.
kt_p2_assembly_v1_9.py -- pk15 (code/pk15/). REVISION of kt_p2_assembly_v1_8.py (b579b91f; its mock run out_kt_p2_assembly_v1_8_mock.out
3a5d57de was VALID). P2-17 (M4) items (i) and (ii), the decision of 2026-11-07 (claims 1 and 2 correct):
  (1) kappa bounded. kappa_max = k1_hi(300)^3/((1 - eps_r,max) lambda_h(300)) bounds kappa(J) = k1^3/lambda_0 for every J >= 300. Here
      lambda_h(J) J^(3(N-1)/2) and k1_hi(J) J^((N-1)/2) are constant, mhat >= 1, and lambda_0 >= (1 - eps_r) mhat lambda_h (S3 (c)).
      lambda_h = exp(logmain_N - logmain_D) uses riglap2's logmain (l.52-56) with det(L_sub)/V = tau(G), the weighted spanning-tree count by
      Kirchhoff's theorem, computed as a cofactor in arb on lapl2.strip_graph(3) and (2): end triangles (A, A, B) with A and B the hulls of
      the algebraic values and their binary64 roundings (kt_rb v1_2's convention), interior verticals 1 and horizontals 1. The MOCK eps_r,max
      is the mock inputs' eps_r; certified, it is M2(b)'s LAW bound over J >= 300. normX (Lemma S') and Lemma E use kappa_max. C-KAPPA checks it
      against the kappa backed out of kt_rb's printed Hbad (2 digits, mock x1.03), relative 5e-2.
  (2) Hbad' = tau~0(Lam) kappa_max^2 (Schur's test on the tail row; NOTE_M4_SCOPE_v1 sect. 3), J-uniform, replaces kt_rb's Hbad in the
      ||Q_4 v_t|| formula. NH' = Lam + Hbad' is printed (INFO). Gbad stays kt_rb's until NOTE_P2_17_GBAD_ABAD_v1 (f44b1962) is SOUND. Lemma E's
      Phi keeps kt_rb's Hbad, through Gbad/Hbad.
kt_p2_assembly_v1_8's docstring follows; its run line and file names change to v1_9.
kt_p2_assembly_v1_8.py -- pk15 (code/pk15/). REVISION of kt_p2_assembly_v1_7.py (712b7fc7; its mock run out_kt_p2_assembly_v1_7_mock.out
f28683a8 was VALID). Changes, 2026-11-07:
  (1) The FLOAT-IN rule for the certified path. A certified-path export may read CERTIFIED only if every input's FLOAT-IN list is empty.
      Otherwise its status is CERTIFIED_GIVEN_FLOAT_IN, with the token lists named (export_status), and pk07's reader refuses that as
      certified. certified_tag refuses CERTIFIED while any list is non-empty. kt_cert_v1_7's g records carry "far logR gBb eps_r Z" (t) and
      "far eps_r Z" (am). C-FLOATIN: on the four real records the status is CERTIFIED_GIVEN_FLOAT_IN; C-FLOATIN-EMPTY: empty lists give
      CERTIFIED; PLANT-FLOATIN-CERT: tagging an export built from them CERTIFIED is refused. Reader (a) re-pins to kt_cert_v1_8 (empty lists)
      when it exists. The MOCK exports name the mock records' tokens in a FLOAT_IN header line.
  (2) pX_hi is printed by px_print from the printed E2_hi and Cov_inf_lo, in exact rationals: the smallest '%.16e' decimal whose square is
      >= E2_hi - max(Cov_inf_lo, 0)^2. pk07's exact C-SRC-J (pX_hi^2 >= E2_hi - Cov_inf_lo^2 on the printed decimals) failed on 1467 of
      v1_3's 5424 rows by 1e-18 to 1e-16 relative: directed roundings of E2_hi up and Cov down outran the arb sqrt. C-SRCJ checks the
      re-read joint export exactly on every row; PLANT-SRCJ: a row with pX_hi lowered by 1e-13 relative must fail.
  (3) C-WIDTH gates the joint corner (after pk07's m5 scan, out_kt_s9h_m5_scan.out 6b643742): L = max(A_t,ref/At_lo, A_a,ref/Aa_lo)
      must stay within the corner budget at which the mixed kind's slack flips when A_t and A_a are lowered together and pi_t, pi_a are
      recomputed: L_CORNER N4 1.027 at the mixed d^h = 3 (1.033 at d = 4), N3 1.008 at d^h = 2 (1.030 at d = 3). A_REF is the v1_5 MOCK t
      export (the scan's base). On certified inputs the references are the FLOAT values and the budget is read from kt_s9h's certified corner
      line, which every certified run prints. PLANT-WIDTH-CORNER: At_lo lowered by 3% must fail at N4. v1_5-v1_7's INFO product form is gone.
  (4) C-GAMMA extended (the note (a)): Gamma(5/2, L) and Gamma(7/2, L) at every level in use, and gamma(3/2, 300), against flint's
      gamma_upper / gamma_lower.
  (5) Notes: k1 <= sqrt(2/pi) J^(-3/2) at N = 4 for every J > 0, since k1 = (2/pi) J^(-3/2) int_0^(2J) (xi (2 - xi/J))^(1/2) e^-xi dxi
      <= (2/pi) J^(-3/2) sqrt(2) Gamma(3/2); k1 <= 1/(2J) at N = 3. E_k < 3/2 at N = 4 also follows from Amos (1974), nu = 0: I_1/I_0 <
      x/(1/2 + (x^2 + 1/4)^(1/2)), so J(I_0/I_1 - 1) > 1/2. The tail chain: tau~_hi divides by k1_lo = (2/pi) J^(-3/2) gamma(3/2, J) (N4; the
      closed form at N3), and kappa_hi = k1_hi^3/lambda_0,lo; tau~_hi falls in J, so its value at a piece's jlo bounds the piece, and only
      kappa_hi carries M4.
kt_p2_assembly_v1_7's docstring follows; its run line and file names change to v1_8.
kt_p2_assembly_v1_7.py -- pk15 (code/pk15/). REVISION of kt_p2_assembly_v1_6.py (922eccf0; its mock run out_kt_p2_assembly_v1_6_mock.out
7a08e7df was VALID). The decision of 2026-11-07 on item 2, route (A), by NOTE_P2_14_E2_v1 (8da98d2e) Lemma E:
  (1) The means c_e, c_f per piece: Lemma E with f = xi_e, xi_f (single uncentred factors) on the AD route's M_10/M_00, M_01/M_00 over the
      piece: [(1 - s'^2)(R (1 - e_1) - e_f) - s-part, R (1 + e_1) + e_f + s-part], s-part = (2s' + s'^2) ||A_f|| by Lemma S' (norm_win).
  (2) E2_hi = E2_c (1 + e_1) + e_{X_c^2} + (2s' + s'^2) ||A_{X_c^2}||, with E2_c the mean-value form in t at the centring held fixed over the
      balls of (1) (joint_ad_c; The uniform centring). Lemma E's g-part levels E2_GLEV and s-part levels E2_SLEV are exact constants
      (e2_bound_v1's minimizers): N4 D3 (34.5, 34.5) / (11.5, 11.5), D4 and D4M (33, 28.5) / (6, 6.5); N3 D3 (29, 29) / (6, 6), D4 and D4M
      (27.5, 26.5) / (3, 3). pX_hi = (E2_hi - Cov_inf_lo^2)^(1/2) with P2-8's Cov; normX_hi (Lemma S') takes the balls of (1).
  (3) MOCK constants of Lemma E: Phi = (Gbad/Hbad)^2 (>= c_K ||phi_0||^2/||psi-hat||^2), sqrt(Psi) = Abad/(2J supp0 kappa_lo e^-40) (kt_rb's
      Abad at level 20), supp0 = kt_rb's QVA value (SUPP0_MOCK), rho_phi = 1; eps_r and s' from the mock inputs; s' stands for s in 1 - s^2.
      Certified: Phi and Psi from kt_rb's phi ratio and k1(2BJ) form (FLOAT until M4's weighted sup), rho_phi from a bound on phi_0's negative
      part.
  (4) Checks: C-E2 (E2_hi >= the uncorrected value on every row); C-E2-FLOAT (Delta_E2 on the first piece within 30% of e2_bound_v1, which uses
      the slightly smaller Phi = (Gbad/Hbad/(1 + 1/kappa))^2); PLANT-E2-LEVEL (a Lemma E level below c+ + 2 is refused). C-REPF compares the
      uncorrected (SM) pX_hi and E2_hi with the FLOAT export. INFO DH-PREVIEW per class: min J0/Cov at d = 3, 4 with the corrected pX_hi, the
      Lemma S' normX_hi and the FLOAT grid's e; N4 takes d^h = 4, N3 keeps 3 only with positive slack on every row. The
      certified decision is kt_s9h's DH_N<N>_<class> from the certified inputs. Header: VACUUM_CORRECTION, CENTRING, E2_GLEVELS, E2_SLEVELS,
      E2_CONSTANTS.
kt_p2_assembly_v1_6's docstring follows; its run line and file names change to v1_7.
kt_p2_assembly_v1_6.py -- pk15 (code/pk15/). REVISION of kt_p2_assembly_v1_5.py (171906d8; its mock run out_kt_p2_assembly_v1_5_mock.out
fa86abbf was VALID). The GOs of 2026-11-07: the normX code after the review found NOTE_P2_14_SCHUR_v1 SOUND (eada4486), and item 2's rule that
Cov_inf_lo comes from P2-8's C4.1 record.
  (1) normX_hi by Lemma S': NOTE_P2_14_SCHUR_v1's Lemma S with the J-uniform horizontal tail slots (Schur's test on the tail kernel
      itself). normX = Lbar_e Lbar_f + T_e + T_f, with
        D4, D4M: T_t = tau~(L_t) gamma_b kappa^2 and T_b = tau_b rho_t kappa^2;
        D3:      T_t + T_bb = (tau~(L_t) rho_bb + tau~(L_bb) rho_t) kappa^3.
      Here Lbar = max(c+, L - c-), tau_b = (L_b - c-) e^-L_b, gamma = max(c+, e^(-1 - c-)) and rho = (N - 1)/2 + c+. E_k <= (N - 1)/2 at
      every J: for N = 4 by Chebyshev's inequality with the decreasing factor (2 - xi/J)^(1/2), plus truncation at 2J; for N = 3 by truncation.
      tau~ = int_{xi > L} (xi - c-) e^-xi dmu / k1, evaluated at J = 300, bounds every J >= 300:
        N = 3: (L - c- + 1) e^-L/(1 - e^-600);
        N = 4: sqrt(2) [Gamma(5/2, L) - c- Gamma(3/2, L)]/gamma(3/2, 300), with Gamma(3/2, L) = sqrt(L) e^-L + (sqrt(pi)/2) erfc(sqrt(L)),
               Gamma(5/2, L) = L^(3/2) e^-L + (3/2) Gamma(3/2, L) and gamma(3/2, J) = (sqrt(pi)/2) erf(sqrt(J)) - sqrt(J) e^-J.
      kappa = k1^3/lambda_0. Certified: k1_hi^3/lambda_0,lo, the shared M4 item. MOCK: kappa^2 = Hbad e^40 k1_hi/(2J) from the mock inputs'
      Hbad, with k1_hi = 1/(2J) (N = 3) and sqrt(2/pi) J^(-3/2) (N = 4). The box holds by positivity: K^(1/2) has a nonnegative kernel (Kent 1977).
      Levels NORMX_LEVELS are exact constants that minimize normX at the FLOAT J = 300 data (float_check_schur_v2): N4 D3 (14, 14), D4 and D4M
      (9, 8.5); N3 D3 (8, 8), D4 and D4M (4, 6). The means' balls per piece are the AD route's enclosures of M_10/M_00 and M_01/M_00 over the
      piece, widened by 1e-3 relative (MEANS_WIDEN, a MOCK stand-in for S3's correction of the first moments, item 2).
      Checks: C-GAMMA (the closed-form Gamma(3/2, 5) against flint's gamma_upper, in whichever argument order matches); C-NORMX-FLOAT (first
      piece against float_check_schur_v2's normX, relative 2e-2); C-NORMX-BOX (levels + 20: tails <= 1e-9 of the box); PLANT-NORMX-LEVEL (a
      level below c+ + 1 is refused). C-REPF drops normX_hi, whose FLOAT reference carries the old product form.
  (2) Cov_inf_lo from P2-8's C4.1 record, reader (e). CERTIFIED path: no certified P2-8 producer is pinned yet, so it refuses after the format
      check. MOCK: mocks/mock_p2_8_c4_v1.kv (5e4c58f7; dc790d56's Cov_inf_lo strings). The joint export copies Cov_inf_lo string for string
      (COV_SOURCE = P2_8_C4_1 (MOCK record)); pX_hi takes cmin = Cov_inf_lo if positive, else 0. C-COVX: the SM route's Cov lower end against
      the record, relative 1e-4 (a cross-check only). PLANT-MOCK-E: the CERTIFIED reader refuses the mock record.
kt_p2_assembly_v1_5's docstring follows; its run line and file names change to v1_6.
kt_p2_assembly_v1_5.py -- pk15 (code/pk15/). REVISION of kt_p2_assembly_v1_4.py (1cf33da9; its mock run out_kt_p2_assembly_v1_4_mock.out
636b66da was VALID). Changes, 2026-11-07:
  (1) The t export takes pk07's certified layout: RECORD = EXPORT_P2_T_v1, FIELDS = jlo jhi At_lo Vt_hi Ot_hi Pt_hi Xta_lo Xtb_lo Aa_lo
      dtx_hi Qvt_hi tz_hi, file export_p2_t_mock_<this file>.kv. Aa_lo = |a~_x| - da_x is new: S9(b)'s amplitude lower end, the one X_ta uses,
      so the mixed kind reads A_a from one pinned record. The header keeps VT_FORM, PT_FORM and XTB_SOURCE.
  (2) pX_hi goes through px_from(E2_hi, Cov_lo, Cov_hi): the smallest |Cov| over the ball, with a refusal (ValueError) if E2_hi - cmin^2 < 0
      before the square root. C-PX3 is a three-case unit control (Cov ball positive, negative, straddling) against
      the direct formulas; PLANT-PX-NEG: E2_hi below cmin^2 must raise.
  (3) C-WIDTH is an INFO line, no longer a gate, and PLANT-WIDTH is gone. pk07 showed that the product form (1 - eps_t)(1 - eps_a) >=
      1/1.085 is optimistic, because both widths also enter the subtracted side of the mixed kind. The budget is pk07's slack M at the
      corner (At_lo and Aa_lo lowered, pi_a recomputed, Pt_hi at the matching dt_x), computed in kt_s9h.
  (4) Notes, no code change. K^(1/2) has a nonnegative kernel (Kent 1977: the von Mises-Fisher kernel is infinitely divisible), so the box
      part of NORMX_BOUND holds by positivity as stated, and v1_3's remark that the pointwise form needs a positive window kernel is
      withdrawn: the pointwise and the integrated Cauchy-Schwarz forms are both valid. Erratum to NOTE_P2_14_HOME_v1_1 sect. 1: p
      does not depend on the centring; p_X does, and its bound inherits the centring through E_bulk[X_c^2].
kt_p2_assembly_v1_4's docstring follows; its run line and file names change to v1_5.
kt_p2_assembly_v1_4.py -- pk15 (code/pk15/). REVISION of kt_p2_assembly_v1_3.py (f710d6e7; its mock run out_kt_p2_assembly_v1_3_mock.out
7a63295c was VALID). The route-independent part of the item 2 and the gate from plan v1_4, 2026-11-07:
  (1) Reader (a)'s CERTIFIED path on pk02's certified kt_cert_v1_7 g records (tn3, tn4, amn3, amn4; full sha256 pinned): each must be
      accepted (READER-A CERTIFIED); its A hi must agree with the mock's within 1e-5 relative (C-READ-CERT; the mocks carry kt_c_t_v1_1's
      floats times 1 + 1e-6); the MOCK reader must refuse each (PLANT-A-REAL-AS-MOCK). INFO: ||Q_4 v_t|| from the certified A_t with the MOCK
      inputs. Outputs stay MOCK: the exports still use the mock A_t.
  (2) The joint export's header names Cov_inf_lo's source: COV_SOURCE = SM_MOMENTS (MOCK). The certified joint input takes P2-8's certified
      C4.1 lower end (NOTE_P2_14_S3_v1 73119816 sect. 1), COV_SOURCE = P2_8_C4_1.
  (3) C-WIDTH (plan v1_4 51de5d61; pk07's width budget): per N, eps_t = 1 - A_t,lo/|t_x| and eps_a = da_x/|a_x| against the split
      eps_t <= 0.03, eps_a <= 0.045 and (1 - eps_t)(1 - eps_a) >= 1/1.085. On certified inputs the reference values are the FLOAT A_t and A_a.
      PLANT-WIDTH: da_x times 2000 must fail it.
kt_p2_assembly_v1_3's docstring follows; its run line and file names change to v1_4.
kt_p2_assembly_v1_3.py -- pk15 (code/pk15/). REVISION of kt_p2_assembly_v1_2.py (11981a60; its mock run out_kt_p2_assembly_v1_2_mock.out
a8894d14 was VALID). Changes, from pk07's export requests and the review of pk07's note v1_1 (fb3b9648), 2026-11-07:
  (1) EXPORT_P2_TPROV_v1 gains the field Xtb_lo : X_tb_lo = t~_x b~_x - R_c^tb, R_c^tb = dt_x |b~_x| + |t~_x| db_x + dt_x db_x
      (b's Ritz x amplitude and its Lemma A error; a signed product like X_ta; not the flip pair). By the flip F, v_b = F v_a and e_x is
      F-even, so b~_x = a~_x and X_tb = X_ta exactly. b's amplitudes are not computed separately here, so Xtb_lo := Xta_lo (the same ball,
      the same decimal) and the header says XTB_SOURCE = FLIP_OF_XTA. FIELDS = jlo jhi At_lo Vt_hi Ot_hi Xta_lo Xtb_lo Pt_hi dtx_hi Qvt_hi tz_hi.
  (2) R_c^ta = dt_x |a~_x| + |t~_x| da_x + dt_x da_x is computed from this script's dt_x and the inputs a_x, da_x (v1_2 read R_c^ta as an
      input); the input value is printed beside it as INFO.
  (3) C-FLIP on the TPROV export as re-read from its file: XTB_SOURCE = FLIP_OF_XTA and Xtb_lo equal to Xta_lo string for string on every
      row (a declaration check, not a computation check). Any other XTB_SOURCE is refused until b's amplitudes have a producer; the gate
      then becomes agreement within the stated bars. Plants: PLANT-FLIP-ROW (one Xtb_lo moved by one unit in its 17th digit),
      PLANT-FLIP-DECL (no XTB_SOURCE line), PLANT-FLIP-SRC (XTB_SOURCE = COMPUTED).
  (4) pX_hi = sqrt(E2_hi - c^2) with c the smallest |Cov| over the Cov ball. v1_2 used Cov_lo^2, which is too large when the ball is
      negative (an unsafe pX_hi for a negative Cov); the two agree when Cov_lo > 0.
  (5) Certified-path notes (no code change). <u, B'u> = 0 and <u, X_c u> = Cov_inf need c = the exact bulk means, so E2_hi, normX_hi
      and the members' B (beta_H, nB_p) must be certified at that centring, e.g. uniformly over the means' certified intervals
      (CENTRING = CERTIFIED_BALLS); the harmonic centring is for estimates only. joint_ad centres at M_10/M_00 and M_01/M_00 of the same
      entries, so with certified (S3-corrected) entries it centres at the exact bulk means, and its ball evaluation covers every centring
      in those balls; this MOCK run's header still says ROUTE_MEANS (MOCK). PX_hi rests on p_X^2 <= E[X_c^2] - Cov^2 by the
      integrated Cauchy-Schwarz form (the pointwise form needs a positive window kernel, and T = K^(1/2) V K^(1/2) has K^(1/2) ends):
      w = K^(1/2) u > 0, g = M_f w, ||X u||^2 = <g, K g> <= <|g|, K |g|> with |g| <= (alpha beta)^(1/2), alpha = M_(f^2) w, beta = M_1 w,
      and Cauchy-Schwarz on K gives <= <alpha, K beta> = <alpha, w> = E[X_c^2]. The mean-value form with constant bars: the true entry is
      p(t) + e(t) with |e(t)| <= ERR and e not differentiable; for each fixed e in the bar box G(., e) is differentiable, so
      F(t) = G(t, e(t)) lies in G(t_m, box) + d_t G([t], box) [-r, r], and ent_ad puts the bars into both evaluations.
kt_p2_assembly_v1_2's docstring follows; its run line and file names change to v1_3.
kt_p2_assembly_v1_2.py -- pk15 (code/pk15/). REVISION of kt_p2_assembly_v1_1.py (b5a72a29). Its mock run passed every check and plant but
C-REPF, whose normX_hi tolerance (1e-6) was set below the FLOAT export's own margin: export_p2_14_joint_float_v1_2 carries normX x(1 + 1e-4).
The one change: C-REPF's normX_hi tolerance is 2e-4 (Cov_inf_lo, pX_hi and E2_hi stay at 1e-4; v1_1's run read 2.4e-6, 4.4e-7, 8.8e-7).
kt_p2_assembly_v1_1's docstring follows; its run line and file names change to v1_2.
kt_p2_assembly_v1_1.py -- pk15 (code/pk15/). REVISION of kt_p2_assembly_v1.py (c335dec4; its mock run out_kt_p2_assembly_v1_mock.out:
all plants fired, C-QV4 passed, C-REPF failed by 2e-2 on Cov_inf_lo because t entered every entry as a ball over the piece). Changes:
  (1) P2-14 per piece by the mean-value form: f([t]) is inside f(t_m) + f'([t]) [-r, r], with f' from forward differentiation in arb, for
      f = E2 and Cov; the entries' constant bars enter f(t_m) as balls;
  (2) entries as m3_reader_v4_4 gives them: coefficient balls a_0..a_K and a constant bar ERR over t in [0, 1/300] (entry_ball's err_b);
  (3) the strict KV key pattern is [A-Z][A-Z0-9_]* (pk07's S4U_KV_v1 rule): mocks v1_1 (uppercase keys, the class M4M), exports with
      the class D4M, PLANT-KEYCASE (a lowercase key must be refused);
  (4) reader (b)'s CERTIFIED path is pk03's bound loader m3_reader_v4_4.load(path, asm_out, expected_J_REF, expected_N) (a5ba5c80,
      pinned by full sha256 and imported from its file); PLANT-MOCK-B now runs it on the mock;
  (5) the exports carry pk07's header keys (VACUUM_CORRECTION, CENTRING, NORMX_BOUND; VT_FORM, PT_FORM) with the values this MOCK run
      used; the certified values (S3, CERTIFIED_BALLS, OPERATOR_BOX_PLUS_SCHUR_TAIL) are required once TAG reads CERTIFIED;
  (6) C-REPF compares with export_p2_14_joint_float_v1_2.kv (dc790d56, D4M keys).
kt_p2_assembly_v1's docstring follows; its run line and file names change to v1_1.
kt_p2_assembly_v1.py -- pk15 (code/pk15/). The SKELETON of S_TB' Phase 2's assembly (STB_P2_PREP_v1_3 1e533bba, sect. 3), on MOCK
records only (the rules of 2026-11-07): every mock carries FORMAT ...MOCK and a claim prefix MOCK and lives in pk15/mocks/; each real
reader refuses a mock (PLANT-MOCK per reader); no output of this script carries a certified FORMAT. Outputs go to pk15/mocks/out/ with FORMAT
"S4U_KV_v1 MOCK" and TAG "MOCK ..." (C-NOCERT checks them; PLANT-CERTOUT: the writer raises on a certified FORMAT before opening a file). The goal
is that the readers, formulas and exports are built and tested before the certified inputs land. One item: mock. No run without the approval
(or the standing approval for small mock tests) naming this file's sha8.
Readers (sect. 3.1; mode CERTIFIED or MOCK; the CERTIFIED path of every reader is the one the certified assembly will use):
  (a) kt_cert_v1_7 g records (A_t, A_am; P2-1c): header with v1_7's full sha256 and ITEM=g.<tn3|tn4|amn3|amn4>, exactly one FORMAT
      "KT_CERT_RECORD_v1_7 CERTIFIED" (MOCK: "... MOCK" and the MOCK claim prefix on header, VALUE and RESULT lines), exactly one KERNEL line
      equal to the pin, VERDICT lines exactly ['VERDICT VALID'], exactly one RESULT line ([lo, hi] read as exact decimals, lo <= hi, FLOAT-IN
      tokens exactly "far logR gBb eps_r Z" or "far eps_r Z"), VALUE >= RESULT hi; PRECERT/STUB refused.
  (b) M3 entry records: CERTIFIED only through pk03's m3_reader_v4_3.load(path, asm_out, expected_J_REF, expected_N), not pinned yet, so
      the CERTIFIED path refuses after its format check; MOCK: the KV record MOCK_M3_ENTRIES_v1 (K, a_0..a_K, R with |M - sum a_k t^k| <= R t^(K+1)).
  (c) the other certified inputs (S9(b), SH1, P2-3, P2-5 quantities): no certified producer pinned yet (the CERTIFIED path refuses after its
      format check); MOCK: MOCK_S9B_INPUTS_v1.
  (d) strict S4U_KV_v1: every non-comment, non-blank line is KEY = value with unique keys; FORMAT, RECORD, TAG, EXPORT_STATUS, CLAIM, KERNEL,
      RUN_VERDICT (= VALID by equality) and END (= RECORD) checked per mode; PRECERT/STUB in FORMAT, RECORD, TAG or EXPORT_STATUS refused. The
      GRID mode reads pk07's export 2520bfb9 (FLOAT) for its piece grid only (jlo, jhi copied string for string).
Formulas (sect. 3.2; arb, ctx.prec 256): ||Q_4 v_t|| = (mhat/lt0^2) A_t + Lam (mhat/lt0) eps_r + (Lam + t_0 + Hbad) s' + Gbad (kt_rb_v1_5's form;
  the g-part's power for w = 2 stays a check item for the N-5); delta t_x = q ||Q_4 v_t|| + eps_0 t_0 + eps_y |t_y| + (q^2 + eps_0^2 + eps_y^2)|t_x|;
  A_t = |t_x| - delta t_x; V_t = c^T G^-1 c + ||Q_4 v_t||^2 with c = (t~_0, t_x, t_y), |t~_0| <= s' ||v_t|| (projected) and the Gram G;
  Pt^2 <= t~_0^2 + t_y^2 + 2|t_x| delta t_x + ||Q_4 v_t||^2 + |c^T (G^-1 - I) c| (joint, Gram-corrected; pk07); O_t <= (|t_z| + delta t_z)^2 +
  ||Q_4 v_t||^2; X_ta = t_x a_x - R_c^ta. P2-14: E2 = sum_ij C(2,i)C(2,j)(-m_e)^(2-i)(-m_f)^(2-j) M_ij/M_00, Cov = M_11/M_00 - m_e m_f per piece
  with t as a ball over the piece; pX = sqrt(E2_hi - Cov_lo^2); normX = Lam_e Lam_f + Lam_f Hbad_e + Lam_e Bad_f + Hbad_e Bad_f.
Exports (sect. 3.3; MOCK): EXPORT_P2_TPROV_v1 (At_lo Vt_hi Ot_hi Xta_lo Pt_hi dtx_hi Qvt_hi tz_hi; the J = 300 inputs on every piece, flagged
  UNIFORM-J ASSUMED (M4)) and EXPORT_P2_14_JOINT_v1 (jlo jhi Cov_inf_lo pX_hi normX_hi E2_hi), strict KV on 2520bfb9's grid, directed decimals.
Checks (gates) and plants (must fire):
  C-HASH (pins); C-GRID (904 pieces per N, contiguous, last jhi 'inf'); reader (a) on the four mocks; PLANT-MOCK-A (CERTIFIED refuses each mock),
  PLANT-A-PRECERT, PLANT-A-KERNEL, PLANT-A-VERDICT2, PLANT-A-HILO, PLANT-A-TOKENS, PLANT-A-VALUE (in-memory variants of a mock, each refused);
  reader (d) on the mock KV inputs; PLANT-MOCK-D, PLANT-D-PRECERT, PLANT-D-DUPKEY, PLANT-D-BARE (a bare 'VERDICT VALID' line), PLANT-D-END,
  PLANT-D-KERNEL; PLANT-MOCK-B and PLANT-MOCK-C (the CERTIFIED paths of (b) and (c) refuse the mocks at the format check);
  C-QV4: ||Q_4 v_t|| against NOTE_P2_14_FLOAT_v1's float reading (3.8822e-4 N = 3, 1.5913e-3 N = 4), relative 5e-4 (mock bars);
  C-PT: the joint Pt^2 is not above the difference route V_t - A_t^2; INFO: C7's margin A_t^2/O_t against 1.05;
  C-REPF: P2-14's rows against export_p2_14_joint_float_v1_1.kv (820d0745), relative 1e-4 (Cov_inf_lo, pX_hi, E2_hi) and 1e-6 (normX_hi);
  PLANT-CERTOUT; C-NOCERT (every output FORMAT is "S4U_KV_v1 MOCK", no CERTIFIED in FORMAT, TAG or EXPORT_STATUS); C-SELF (each export
  re-read by (d): MOCK accepts, CERTIFIED refuses).
Writes only pk15/mocks/out/out_<this file>_mock.out and the two exports export_p2_tprov_mock_<this file>.kv and
export_p2_14_joint_mock_<this file>.kv. Price [E]: a few seconds (LIM 60, cap 65 s = 0.018 core-h). Run:
  D=/mnt/g2/release/root/code/pk15; OMP_NUM_THREADS=1 timeout 580 nice -n 10 prlimit --as=8589934592 --
  python3 -I -B $D/kt_p2_assembly_v1_37.py mock 60 > $D/mocks/out/kt_p2_assembly_v1_37_mock.log 2>&1
"""
import os
for _v in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS'):
    os.environ[_v] = '1'
import resource, sys, time, math, hashlib, signal, traceback, re, json
ITEMS = ('mock', 'certdry', 'cert')   # v1_35 (7)
if len(sys.argv) < 3 or sys.argv[1] not in ITEMS:
    print('usage: kt_p2_assembly_v1_37.py mock|certdry|cert LIM   (LIM = RLIMIT_CPU soft limit in s, 10..120; hard LIM + 5)')
    sys.exit(2)
MODE = sys.argv[1]
CERT_MODE = MODE in ('certdry', 'cert')   # v1_35 (7): no I[N] and no MOCK comparison inputs
MOCK_SETAC = MODE != 'cert'   # v1_35 (7): certdry rehearses the cert path on the MOCK Set A/C/W records
LIM = int(sys.argv[2]) if re.fullmatch(r'[0-9]{1,3}', sys.argv[2]) else -1
if not (10 <= LIM <= 120):
    print('bad LIM %r (need 10 <= LIM <= 120)' % sys.argv[2])
    sys.exit(2)
resource.setrlimit(resource.RLIMIT_CPU, (LIM, LIM + 5))
resource.setrlimit(resource.RLIMIT_FSIZE, (4 * 2 ** 20, 4 * 2 ** 20))
STAGE = ['start']

CODEDIR = '/mnt/g2/release/root/code'
OWN = CODEDIR + '/pk15'
MOCKS = OWN + '/mocks'
MOUT = MOCKS + '/out'
COUT = OWN + '/out'   # v1_35 (7): the cert run's outputs
LABEL = os.path.splitext(os.path.basename(os.path.abspath(__file__)))[0]
XOUT = COUT if MODE == 'cert' else MOUT   # v1_35 (7)
OUT_PATH = os.path.join(XOUT, 'out_%s_%s.out' % (LABEL, MODE))
MSFX = '' if MODE == 'cert' else ' (MOCK)'   # v1_35 (7): the MOCK suffix of the header strings (NOTE_KT_P2_V1_35_JOINT_HEADER_v1)
RDR_PATH = CODEDIR + '/pk07/kt_s9h_v1_3_readers.py'   # v1_36 (1): pk07's side-effect-free readers of kt_s9h_v1_3, pinned; replaces v1_35's S9H_READER
S9H_NAMES = ('s4u_read_port', 'joint_grid', 'joint_read', 't_read', 'bound_ok')   # v1_36 (1): the readers' entry points this file calls
S9H_RDNAME = {'EXPORT_P2_14_JOINT_v1': 'kt_s9h_v1_3 joint_read', 'EXPORT_P2_T_v1': 'kt_s9h_v1_3 t_read', 'EXPORT_P2_14_MEANS_v1': 'means_check'}   # v1_36 (1)
CLAIM_CERT = ('kt_p2_assembly rows from pinned certified records; every row holds for every J in [jlo, jhi] of its piece, as J_UNIFORMITY '
              'states, with the sources the *_SOURCE keys name')   # v1_35 (7)
EXPORT_FMT = 'EXPORT %s sha256 %s'   # v1_36 (4): the run output's EXPORT line in rule V2's form (base name, sha256 of the bytes)
JT_FIELDS = 'jlo jhi Cov_inf_lo pX_hi normX_hi E2_hi ROUTE'   # v1_36 (4): FIELDS of the joint export (NOTE_KT_P2_V1_35_JOINT_HEADER_v1)
TP_FIELDS = 'jlo jhi At_lo Vt_hi Ot_hi Pt_hi Xta_lo Xtb_lo Aa_lo dtx_hi Qvt_hi tz_hi ce_lo ce_hi'   # v1_36 (4): FIELDS of the t export
MN_FIELDS = 'jlo jhi ce_lo ce_hi cf_lo cf_hi Cov_inf_lo Cov_inf_hi'   # v1_36 (4), v1_37 (6): FIELDS of the means export
COV_CENTRING = ('TRUE_BULK_MEANS: Cov_inf = E_u[X_c] = E11 - c_e c_f, X_c centred at the exact bulk means c_e = E xi_e and c_f = E xi_f, '
                'which the ce and cf balls of this export enclose')   # v1_37 (6): the means export's COV_CENTRING (pk11, R6.5)
DEC_RE = r'-?[0-9]+(\.[0-9]+)?(e[+-]?[0-9]+)?'   # v1_36 (4): an S4U_KV_v1 decimal (the readers' dec_frac form)
RUN_TAG = '%s_%d' % (time.strftime('%Y%m%dT%H%M%SZ', time.gmtime()), os.getpid())   # v1_37 (1): the run's UTC start stamp and PID, in this run's temporary names (cert_tmp)
EXP_TP = os.path.join(XOUT, 'export_p2_t_%s_%s.kv' % (MODE, LABEL))   # EXPORT_P2_T_v1 (v1_5 (1))
EXP_JT = os.path.join(XOUT, 'export_p2_14_joint_%s_%s.kv' % (MODE, LABEL))
EXP_MN = os.path.join(XOUT, 'export_p2_14_means_%s_%s.kv' % (MODE, LABEL))   # EXPORT_P2_14_MEANS_v1 (v1_22): c_e per piece and class for pk07
MEAN_FLOAT = {4: '1.00102816', 3: '0.66748795'}   # v1_22: FLOAT means of a horizontal bond energy (e2_bound_v1's mh), for C-MEANS
MEANV_FLOAT = {4: '0.82681845', 3: '0.55121210'}   # v1_22: FLOAT means of a vertical bond energy (e2_bound_v1's mv), for C-MEANS
GRID = CODEDIR + '/pk07/out/export_kt_s67_cert_v2_2_sweep.kv'
JOINTF = OWN + '/out/export_p2_14_joint_float_v1_2.kv'
M_CT = dict(((k, n), os.path.join(MOCKS, 'mock_kt_cert_v1_7_g.%sn%d.out' % (k, n))) for k in ('t', 'am') for n in (3, 4))
REAL_CT = dict(((k, n), CODEDIR + '/pk02/out_kt_cert_v1_7_g.%sn%d.out' % (k, n)) for k in ('t', 'am') for n in (3, 4))   # certified (v1_4 (1))
M_M3 = os.path.join(MOCKS, 'mock_m3_entries_v2.kv')   # v1_35 (1): the run list's 23 keys per N (MOCK_M3_ENTRIES_v2)
M_IN = os.path.join(MOCKS, 'mock_s9b_inputs_v1_1.kv')
M_P28 = os.path.join(MOCKS, 'mock_p2_8_c4_v1.kv')   # reader (e), v1_6 (2)
NORMX_LEVELS = {(4, 'D3'): ('14', '14'), (4, 'D4'): ('9', '8.5'), (4, 'D4M'): ('9', '8.5'), (3, 'D3'): ('8', '8'), (3, 'D4'): ('4', '6'),
                (3, 'D4M'): ('4', '6')}   # v1_6 (1): exact levels (float_check_schur_v2)
NX_FLOAT = {(4, 'D3'): 201.2190, (4, 'D4'): 78.4732, (3, 'D3'): 73.1116, (3, 'D4'): 28.9355}   # float_check_schur_v2 first-piece normX
MEANS_WIDEN = '1e-3'   # v1_6 (1): MOCK stand-in for S3's correction of the means (a decimal string; arb is imported below)
SUPP0_MOCK = {4: '169.3', 3: '168.8'}   # v1_7 (3): kt_rb_v1_5's QVA lines (FLOAT), a MOCK input of Lemma E
OWN_FLOAT_JT = []   # v1_11 (4), v1_14 (1), v1_15 (2), v1_25 (1): the joint export's own FLOAT inputs; eps_r and s come from the certified M2B record
OWN_FLOAT_TP = []   # v1_35 (2): tz and dtz from Set C's IhZ (the odd Ritz route); before v1_35   # v1_11 (4), v1_27 (1), v1_32 (1), v1_33 (3): the t export own FLOAT inputs: the mock tz and dtz (P2-3); R_e1, R_e3 from M4_KV_v1, tau from the S67 sweep
EPS_G, THETA_G = '0.25', '0.7'   # v1_12 (2), v1_15 (1): Lemma G's eps and the one theta of Abad' and Lemma E-prime
ZR_MOCK = {'eps': '1', 'theta': '1', 'theta_b': '1'}   # v1_15 (2): MOCK Z_T(w)/Z_T(w0), one per weight set; certified: one remainder per triangle
G00_NORM = ('G,0,0 = I_D(J)/main_D(J) = <phi_0, K phi_0>/main_D (pk03): I_D the integral of cp(0,L) cp(0,R) over strip_graph(2, (A, B)), V = 6, '
            'end triangles T-M A, M-B A, T-B B, horizontals 1, pairs on both columns; main_D = exp of riglap2 logmain at J; a0_exact 1')   # v1_17 (1), v1_19 (1)
# v1_20 (2), the identity behind S7's use: pk03's message to pk15 of 2026-11-07 ("S9 G,0,0 normalization: I_D/main_D, a0 = 1 exactly,
# uniform err") says: "G,0,0 will be the same object as S7's certified g,0,0, under the key as you write it." So S7's certified g,0,0 serves as
# G_00 until the S9 record exists (the decision of 2026-11-07); M3's records are not affected by F-2.
G00_MOCK = '1'   # v1_17 (1): MOCK lower end of G_00; certified: M3's G,0,0 per piece, the last piece containing t = 0
G00_CLAIM = 'for every J >= J_REF, t = 1/J, t = 0 included: |I(J)/main(J) - sum_k ak[k] t^k| <= err (Lemma U'   # v1_19 (1): the M3 record claim's prefix, copied by tool
S7G00 = dict((N, (CODEDIR + '/pk03/out/m3_b5_N%d_J300_v1_7.json' % N, CODEDIR + '/pk03/out/m3_run_v1_7_asm.%d.out' % N)) for N in (4, 3))   # v1_19 (2), pinned
SEPS_FLOAT = {4: '1.023598', 3: '1.020529'}   # v1_12 (1): seps_v1.awk's S_eps at eps = 1/4 (out/seps_v1.txt, FLOAT), for C-SEPS
VACRES = dict((N, CODEDIR + '/pk11/out/vacres_K3_N%d_sym_v1.json' % N) for N in (4, 3))   # v1_12 (1): reader (f), pinned
OPEN_CONDITIONS = {'C1': "M2(b)'s bound (b) in the |g| form, ||K^{1/2}|g||| <= eps_r mu-hat ||psi-hat|| (R6a l.44, Lemma E (E4); pk02 to confirm)"}
C1_CLAIM = '||K^{1/2} |g| || <= eps_r mhat ||psihat||'   # v1_14 (2), v1_24 (2): the C1 string, 41 bytes; origin pk02's SPEC_M2B_CERT_v1_ADD3.md cb472451 (frozen, pinned)
C1_NOSPACE = '||K^{1/2}|g||| <= eps_r mhat ||psihat||'   # v1_14 (2), v1_24 (2): the earlier no-space wording (pk07's kt_s9h_m21.py 472bc24c, frozen, pinned), for PLANT-C1-NOSPACE
C1_SOURCE = (CODEDIR + '/pk02/SPEC_M2B_CERT_v1_ADD3.md', CODEDIR + '/pk07/kt_s9h_m21.py')   # v1_24 (2): C-C1-SOURCE, both pinned
CE_LO_NEED = {4: '0.9724', 3: '0.6444'}   # v1_24 (1): pk07's binding lower ends for c_t (beta_H provider), INFO only
M2B = (CODEDIR + '/pk02/M2B_KV_v1.txt', CODEDIR + '/pk02/out/out_m2b_asm_v1.out')   # v1_25 (1): pk02's certified M2(b) record and its asm output, pinned
M2B_READER_PATH = CODEDIR + '/pk02/m2b_reader_v1.py'   # v1_25 (1): the one sha-pinned reader of M2B_KV_v1 (load, law_v1), pinned
M2B_ASM_PATH = CODEDIR + '/pk02/m2b_asm_v1.py'   # v1_25 (1): the asm script named by the record's ASM_SHA256, pinned
M2B_PREC = 256   # (4) the review note 3 on v1_26, the fixed flint precision of every call into m2b_reader_v1
M4 = (CODEDIR + '/pk15/M4_KV_v1.txt', CODEDIR + '/pk15/out/out_m4_asm_v1.out')   # v1_32 (1): the certified M4 law record and its asm output, pinned
M4_READER_PATH = CODEDIR + '/pk15/m4_reader_v1.py'   # v1_32 (1): the one sha-pinned reader of M4_KV_v1 (load, law), pinned
M4_PREC = 256   # v1_32 (1): the flint precision of every call into m4_reader_v1 (the reader's own)
S67 = (CODEDIR + '/pk07/out/export_kt_s9h_v1_2_vsweep.kv', CODEDIR + '/pk07/out/out_kt_s9h_v1_2_vsweep.out')   # v1_33 (3): pk07's certified vertical sweep and its run output, pinned
S67_READER_PATH = CODEDIR + '/pk07/kt_s67_export_reader_v2_1.py'   # v1_33 (3): its one sha-pinned reader (load), pinned
S67_SCRIPT = CODEDIR + '/pk07/kt_s9h_v1_2.py'   # v1_34 (Point 2): the sweep's producer script, pinned; its TRIAL_SET holds the four full sha256s
J_UNIF_PP = 'UNIFORM-J PER-PIECE (M4): every row holds for every J in [jlo, jhi] of its piece; the last piece runs to J = inf (t = 0)'   # (5) pinned by pk07 as J_UNIF_CERT
J_UNIF_PP_LEN, J_UNIF_PP_SHA16 = 120, '7aba90d5c6b9411b'   # (5) measured by tool (length, sha256 prefix of the bare string)
J_UNIF_T_ASSUMED = 'UNIFORM-J ASSUMED (M4): the J = 300 inputs on every piece'   # (5) the t export until every M4 input of the t path is a pinned certified record
REVEN, RPE = (0, 1, 3), ((0, 0), (0, 1), (0, 3), (1, 1), (1, 3), (3, 3))   # v1_27 (1): the even block and its pairs (NOTE_P2_17_RITZ_PIECES_v1 sect. 2)
RITZ_KEYS = tuple(['G,%d,%d' % p for p in RPE] + ['T,%d,%d' % p for p in RPE] + ['Iht,%d' % b for b in REVEN] + ['Dx,%d' % b for b in REVEN])   # the 18 S9 keys (pk03)
M_RITZ = os.path.join(MOCKS, 'mock_ritz_entries_v1.kv')   # v1_27 (1): MOCK_RITZ_ENTRIES_v1, pinned
S9_RECORDS = {4: (CODEDIR + '/pk03/out/m3_s9_N4_J300_v1_8_3.json', CODEDIR + '/pk03/out/m3_run_v1_8_3_asm9.4.out'), 3: (CODEDIR + '/pk03/out/m3_s9_N3_J300_v1_8_3.json', CODEDIR + '/pk03/out/m3_run_v1_8_3_asm9.3.out')}   # v1_27 (1): pk03's S9 records {N: (record json, asm output)}, each pinned by full sha256 once it exists; empty until then
TS_FILES = {4: CODEDIR + '/pk11/out/ts_N4_J170_D_S_z9sym_v1.json', 3: CODEDIR + '/pk11/out/ts_N3_S_z9sym_v1.json'}   # v1_27 (1): S9's trial ts files, pinned
RBOUT = dict((N, CODEDIR + '/pk01/out_kt_rb_v1_5_r%d.out' % N) for N in (4, 3))   # v1_27 (1): kt_rb_v1_5's CERT300 and C-IN lines, pinned
TAU_R_FLOAT = {4: '0.983', 3: '0.769'}   # v1_27 (1): kt_rb_v1_5 l.200 (FLOAT; P2-9 certifies tau): token tau_r
BETA_R_FLOAT = {4: '0.912', 3: '0.645'}   # v1_27 (1): kt_rb_v1_5 l.201, for PLANT-NA only (Lemma B replaces it)
LAM_T, LAM_A = '40', '20'   # v1_27 (1): the Lemma A split levels (kt_rb's at J = 300); any level gives a valid bound
E2_GLEV = {(4, 'D3'): ('26.5', '26.5'), (4, 'D4'): ('20.5', '27.5'), (4, 'D4M'): ('20.5', '27.5'), (3, 'D3'): ('20', '20'),
           (3, 'D4'): ('15', '25'), (3, 'D4M'): ('15', '25')}   # v1_7 (2), v1_14 (1), v1_17 (3), v1_25 (6): Lemma E-prime g-part levels (e2_bound_v4, theta 0.7, certified eps_r and s)
E2_SLEV = {(4, 'D3'): ('11.5', '11.5'), (4, 'D4'): ('6', '6.5'), (4, 'D4M'): ('6', '6.5'), (3, 'D3'): ('6', '6'),
           (3, 'D4'): ('3', '3'), (3, 'D4M'): ('3', '3')}   # v1_7 (2): Lemma S' levels for the s-parts (e2_bound_v1)
E2B_FLOAT = {(4, 'D3'): 5.4667, (4, 'D4'): 3.5477, (3, 'D3'): 0.6716, (3, 'D4'): 0.6110}   # v1_16, v1_17 (3), v1_25 (6): e2_bound_v4's Delta_E2 at theta 0.7 (Lemma T-prime, rho_phi with it, certified eps_r and s)
RHO_FLOAT = {4: '1.023447', 3: '1.011781'}   # v1_16, v1_17 (3): e2_bound_v3's rho_phi bounds (FLOAT, Lemma T-prime), for C-RHO
A_REF = {(4, 't'): '3.9959529081931337e-02', (4, 'a'): '1.0478453304134999e-01', (3, 't'): '3.2650335288598495e-02',
         (3, 'a'): '8.5529211732059990e-02'}   # v1_8 (3): At_lo, Aa_lo of the v1_5 MOCK t export e9d8bce9, the base of pk07's m5 corner scan
L_CORNER = {(4, 3): '1.027', (4, 4): '1.033', (3, 2): '1.008', (3, 3): '1.030'}   # v1_8 (3): pk07 m5 6b643742, joint corner L at d
D_MIXED = {4: 3, 3: 2}   # v1_8 (3): the mixed kind's FLOAT d^h (pk07 m5)
M3_READER_PATH = CODEDIR + '/pk03/m3_reader_v4_4.py'
RUN_LIST = CODEDIR + '/pk03/P2_RUN_LIST_v1_10.json'   # v1_35 (1): pk03's run list of Sets A, C and W, pinned
RUN_KEYS = ('SM3,0,0', 'SM3,1,0', 'SM3,0,1', 'SM3,2,0', 'SM3,0,2', 'SM3,2,1', 'SM3,1,2', 'SM3,2,2', 'X3', 'SM4,0,0', 'SM4,0,1', 'SM4,2,0', 'SM4,0,2',
            'SM4,2,1', 'SM4,1,2', 'SM4,2,2', 'Gxt,0,0', 'Y4', 'IhZ', 'IhZb', 'IhZh', 'W1', 'W2')
KEYMAP = {'SM3,0,0': 'M3_00', 'SM3,1,0': 'M3_10', 'SM3,0,1': 'M3_01', 'SM3,2,0': 'M3_20', 'SM3,0,2': 'M3_02', 'X3': 'M3_11', 'SM3,2,1': 'M3_21',
          'SM3,1,2': 'M3_12', 'SM3,2,2': 'M3_22', 'SM4,0,0': 'M4_00', 'Gxt,0,0': 'M4_10', 'SM4,0,1': 'M4_01', 'SM4,2,0': 'M4_20', 'SM4,0,2': 'M4_02',
          'Y4': 'M4_11', 'SM4,2,1': 'M4_21', 'SM4,1,2': 'M4_12', 'SM4,2,2': 'M4_22', 'W1': 'W1', 'W2': 'W2', 'IhZ': 'IHZ', 'IhZb': 'IHZB', 'IhZh': 'IHZH'}
SETAC_FAMS = ('NTB', 'DT', 'NIT', 'NIB', 'NIH', 'NBT', 'NTT')   # v1_35 (1): m3_run_v1_10's family graphs (pk03, 07:21Z)
SETAC_RECORDS = dict((N, [(X, CODEDIR + '/pk03/out/m3_p2_%s_N%d_J300_v1_10_4.json' % (X, N), CODEDIR + '/pk03/out/m3_run_v1_10_4_asm.%d.out' % N)
                          for X in SETAC_FAMS]) for N in (4, 3))   # v1_35 (1), v1_37 (4): m3_run_v1_10_4's names, pinned at R4; C-A-BIND refuses an unpinned file
SETAC_TOPS = {}   # v1_35 (1): (N, family) -> the record's top fields, for INFO A-PARTITION
M3R6_PATH = CODEDIR + '/pk03/m3_reader_v6_3.py'   # v1_35 (1): pk03's reader of arbeng_ma_v1_4_1 records (claim_ball), pinned
M3R6_LAYER = ('arbeng_ma_v1_4_1.py', '1f58ad80')   # v1_35 (1): the layer C-A-BIND requires of the v1_10 records
AMAP_A = {'M3': ('NTB', ['cp', 0, 0], ['cp', 0, 2], ['xh', 'T', 0, 1], ['xh', 'B', 1, 7]),
          'M4': ('DT', ['cp', 0, 0], ['cp', 0, 1], ['xh', 'T', 0, 1], ['xi', 'MB', 0])}   # v1_35 (1), C-A-MAP: graph, end factors, i-factor, j-factor
AMAP_CW = {'IhZ': ('NIT', [['cp', 2, 0], ['xh', 'T', 1, 7], ['cp', 0, 2]]), 'IhZb': ('NIB', [['cp', 2, 0], ['xh', 'B', 1, 7], ['cp', 0, 2]]),
           'IhZh': ('NIH', [['cp', 2, 0], ['xh', 'M', 1, 8], ['cp', 0, 2]]),
           'W1': ('NBT', [['cp', 0, 0], ['xi', 'MB', 1], ['xh', 'T', 1, 7], ['cp', 0, 2]]),
           'W2': ('NTT', [['cp', 0, 0], ['xi', 'MB', 0], ['xh', 'T', 0, 1], ['cp', 0, 2]])}   # v1_35 (1), C-A-MAP: Sets C and W, fixed
S8D = dict((N, (CODEDIR + '/pk03/out/m3_s8v3_D_N%d_J300_v1_8_1.json' % N, CODEDIR + '/pk03/out/m3_run_v1_8_1_asmP.%d.out' % N)) for N in (4, 3))   # v1_35 (2): g,2,2
S8N = dict((N, (CODEDIR + '/pk03/out/m3_s8v3_N_N%d_J300_v1_8_2.json' % N, CODEDIR + '/pk03/out/m3_run_v1_8_2_asmN.%d.out' % N)) for N in (4, 3))   # v1_35 (2): T,2,2
M3E_MODS = [('m3_scal', CODEDIR + '/pk03/m3_scal_v2.py'), ('m3_graph', CODEDIR + '/pk03/m3_graph_v3.py'),
            ('m3_series', CODEDIR + '/pk03/m3_series_v2.py'), ('m3_entries_v3', CODEDIR + '/pk03/m3_entries_v3.py')]   # v1_35 (3): the alias checks, pinned
ALIAS_LISTS = {'S9': CODEDIR + '/pk03/S9_ENTRY_LIST_v1.json', 'M3': CODEDIR + '/pk03/M3_ENTRY_LIST_v1_2.json', 'P2': OWN + '/P2_ENTRY_LIST_v1_3.json'}   # pinned
ROUTE_OK = {'D3': ('SINGLE', 'CS'), 'D4': ('SINGLE', 'DOUBLE'), 'D4M': ('SINGLE', 'DOUBLE')}   # v1_35 (5): the first one wins ties
ROUTE_GRID = tuple('%d' % L for L in range(4, 41))   # v1_35 (5): the fixed level grid of the route terms (every level gives a valid bound)
M_HS = os.path.join(MOCKS, 'mock_hs_inv_normx_v1.kv')   # v1_35 (6): the MOCK HS record (SPEC_HS_INV_NORMX_v1_2 sect. 6 keys)
HS_NOTE = CODEDIR + '/pk08/HS_NORMX_LEMMA_NOTE_v1.md'   # v1_35 (6): Lemma D3's note, pinned (L-1)
HS_RECORD = (CODEDIR + '/pk08/out/HS_INV_NORMX_v1_d3d4b.kv', CODEDIR + '/pk08/out/px08_hsd3b_export_v1_1_run.out')   # v1_37 (5): pk08's combined record v2 (D3, D4, D4M and R6's D3B rows), pinned
HS_RECORD_D3 = CODEDIR + '/pk08/out/HS_INV_NORMX_v1.kv'   # v1_35 (6), v1_37 (5): the D3 record, pinned; C-HS-D3-SAME's reference
HS_ADD1 = OWN + '/SPEC_HS_INV_NORMX_v1_2_ADD1.md'   # v1_37 (5): the D4/D4M interface, pinned; C-HS-OP-SPEC
HS_OP_D3 = ('Z = K^(1/2) V^(1/2); G_t = V^(1/2) (K_t - c_t K) V^(1/2); G_bb = V^(1/2) (K_bb - c_bb K) V^(1/2); lambda_0^3 X_c = Z G_t G_bb Z*; '
            'w = 3; t = gap-0 top horizontal, bb = gap-1 bottom horizontal; HS2 = tr_H(X_c* X_c) <= COEF (lambda_h/lambda_0)^2, lambda_0 by its '
            'certified lower end')   # v1_35 (6): SPEC_HS_INV_NORMX_v1_2 sect. 6, exactly (L-2)
HS_OP_D4 = ('Z = K^(1/2) V^(1/2); M = (xi_b - c_b) on column 0, xi_b = J(1 - s_M.s_B); G_t = V^(1/2) (K_t - c_t K) V^(1/2); lambda_0^2 X_c = Z M G_t Z*; '
            'w = 2; t = gap-0 top horizontal, b = column-0 MB vertical; HS2 = tr_H(X_c* X_c) <= COEF (lambda_h/lambda_0)^1, lambda_0 by its certified '
            'lower end')   # v1_37 (5): SPEC_HS_INV_NORMX_v1_2_ADD1 sect. 1, exactly (C-HS-OP-SPEC checks it against the pinned file)
HS_OP_D4M = ('Z = K^(1/2) V^(1/2); M = (xi_b - c_b) on column 1, xi_b = J(1 - s_M.s_B); G_t = V^(1/2) (K_t - c_t K) V^(1/2); lambda_0^2 X_c = Z G_t M Z*, '
             'the adjoint of D4\'s; w = 2; t = gap-0 top horizontal, b = column-1 MB vertical; HS2 = tr_H(X_c* X_c) <= COEF (lambda_h/lambda_0)^1, '
             'lambda_0 by its certified lower end')   # v1_37 (5): ADD1 sect. 1, exactly
HS_P = {'D3': 2, 'D4': 1, 'D4M': 1}   # v1_37 (5): LAMBDA_POWER per class (v1_2 L-3, ADD1)
HS_NORM = 'HS2_TR_XC_STAR_XC'   # v1_35 (6): one normalization (v1_2 sect. 0)
HS_JCLAIM = 'UNIFORM-J PER-ROW: every row holds for every J in [jlo, jhi]; jhi = inf includes t = 0'
HS_METHODS = ('LEMMA', 'T_SERIES_REMAINDER', 'J_BALL', 'MONOTONE_IN_J')   # v1_35 (6): C-HS-J (the review d0cc9120 adds LEMMA)
HS_SPOT_SRC = dict((N, CODEDIR + '/pk11/out/s8hf_v1/out_kt_s8rf_v1_n%d.out' % N) for N in (4, 3))   # v1_35 (6): C-HS-SPOT's sources, pinned
RHO_EPS_R = '0.85'   # v1_35 (5): Lemma R's own eps for rho_(phi,ij) (pk02 08:36Z); Phi_eps keeps EPS_G


def _under(path, top):
    return os.path.realpath(os.path.dirname(path)) == os.path.realpath(top) and os.path.realpath(top).startswith(os.path.realpath(MOCKS) + os.sep)

def _in_dir(path, top):
    """v1_35 (7): path lies directly in top, and top is the mock outputs folder or the cert outputs folder (pk15/out); _under keeps the
    MOCK writer inside mocks/."""
    t = os.path.realpath(top)
    return os.path.realpath(os.path.dirname(path)) == t and t in (os.path.realpath(MOUT), os.path.realpath(COUT))



if not (os.path.isdir(XOUT) and all(_in_dir(p, XOUT) for p in (OUT_PATH, EXP_TP, EXP_JT, EXP_MN))):   # v1_35 (7): the mode's own folder
    print('output directory check failed')
    sys.exit(2)
FH = open(OUT_PATH, 'x')


def cpu():
    return time.process_time()


def out(line):
    FH.write(line + '\n')
    FH.flush()


def _on_xcpu(signum, frame):
    out('CAP-STOP SIGXCPU at cpu %.1f s in stage %s' % (cpu(), STAGE[0]))
    out('VERDICT INCOMPLETE (CAP-STOP)')
    os._exit(3)


signal.signal(signal.SIGXCPU, _on_xcpu)

PINS = {
    '/mnt/g2/release/root/code/pk15/mocks/mock_kt_cert_v1_7_g.tn3.out': 'c89fb8be0993060c68e65733624a024b957c190e1ce72b062c6841e7f4792bfa',
    '/mnt/g2/release/root/code/pk15/mocks/mock_kt_cert_v1_7_g.tn4.out': '0390df6dfeab74bc83a2cee81dbe03ecb6ef8176eafa1b612744f8b7e8472ac1',
    '/mnt/g2/release/root/code/pk15/mocks/mock_kt_cert_v1_7_g.amn3.out': '24ae78ce1d4c5076a82cc77717a1b77f59624b28c6c397c6a45c1f1eb1c405b7',
    '/mnt/g2/release/root/code/pk15/mocks/mock_kt_cert_v1_7_g.amn4.out': '291b1e6ee5f794b175df38024650c3eb6f20b55db04ae781a1c63b25d91c29a1',
    '/mnt/g2/release/root/code/pk15/mocks/mock_m3_entries_v1_1.kv': '17f7ab022f3177c4b914c237c5ff42e52f3e7b7eb36f293db19f527d6679e75e',
    '/mnt/g2/release/root/code/pk15/mocks/mock_s9b_inputs_v1_1.kv': '8f9ba499aa9fafbf824c1f150276e8b89a507eb1f4ce56639cfac651fbbc1dc2',
    '/mnt/g2/release/root/code/pk07/out/export_kt_s67_cert_v2_2_sweep.kv': '6fe9ab65f5207dc3658c98ff4f3696bd2db6aa784b0dec84b33881b2da579c34',
    '/mnt/g2/release/root/code/pk15/out/export_p2_14_joint_float_v1_2.kv': '39d08be920a031ac33aeab936f63aa743611578e94e342e83b72a030abcbfc3e',
    '/mnt/g2/release/root/code/pk03/m3_reader_v4_4.py': 'b5b2c953b67c3e848b7561b7b059efb05f7788debd3cde18fefc39c100d929a0',
    '/mnt/g2/release/root/code/pk02/out_kt_cert_v1_7_g.tn3.out': '3fdb90f757e44acb0fd9331ef67721753a7a3000e8a6106ec520b9b8741ba21e',
    '/mnt/g2/release/root/code/pk02/out_kt_cert_v1_7_g.tn4.out': '438ed87cb606ccd6e17aabf273a2f6c1229903d27aa0f0ec7673e49fb9c31cc5',
    '/mnt/g2/release/root/code/pk02/out_kt_cert_v1_7_g.amn3.out': 'b9c30e6d4680a06b2ec9772ea4dd63b9eb78c761daf73233383f8b980f370ce3',
    '/mnt/g2/release/root/code/pk02/out_kt_cert_v1_7_g.amn4.out': '132e3a27b1f16877c5afbe179f351e2070d7d147541cfcca0f79a278b2220592',
    '/mnt/g2/release/root/code/pk15/mocks/mock_p2_8_c4_v1.kv': 'ad783d685b5b5e5d4ba753e3b4d5212b1915b1be53317eab2875b67ead0b21f6',
    '/mnt/g2/release/root/code/pk11/out/vacres_K3_N4_sym_v1.json': 'b40859de2607f64cd127cb1834a04e9f33b3c2cbe4af9fe4f2bb80badaacd43e',
    '/mnt/g2/release/root/code/pk11/out/vacres_K3_N3_sym_v1.json': 'e5a9b49fde1896ff1d87de1d4a44571376eeeeb31b0ce4205faecdd2463115c0',
    '/mnt/g2/release/root/code/pk03/out/m3_b5_N4_J300_v1_7.json': '77f83bc79060bae4c34de47884f00d48e6403fee995e3e54dab6781e4c527b3a',
    '/mnt/g2/release/root/code/pk03/out/m3_b5_N3_J300_v1_7.json': '411913043ce7c90970f8fc35918e6c221af2eb025b728dde6f55b755646ab8d3',
    '/mnt/g2/release/root/code/pk03/out/m3_run_v1_7_asm.4.out': 'a5b294f364f9399b9d12f89af6ce1a1e598b8b424bc6e60d35e122ebd1391b97',
    '/mnt/g2/release/root/code/pk03/out/m3_run_v1_7_asm.3.out': '18964e97c320395f44b5923d132b1ac65c95b935cc8708a50e197076cc24e0dc',
    '/mnt/g2/release/root/code/pk02/SPEC_M2B_CERT_v1_ADD3.md': '6dbc8ea49fb6038ab7dd99aebeb48f9daba46b669700d92c2749b543b231058e',
    '/mnt/g2/release/root/code/pk07/kt_s9h_m21.py': 'e80f4ab999653c4c30ae62d3b7a7020596f7765dbadfa6bb78c924059dffc35e',
    '/mnt/g2/release/root/code/pk02/M2B_KV_v1.txt': '01ffc2aacb0bf6b4f33c55602c9419964481ce0f0a6c1fbdc6520a91aab0b72d',
    '/mnt/g2/release/root/code/pk02/out/out_m2b_asm_v1.out': 'cf5ed7d4e73188870cd2bff8fc91f6ed0c5919b1e9a105d44a361dfe53658391',
    '/mnt/g2/release/root/code/pk02/m2b_reader_v1.py': 'a9f15db48e9fa51629448181d8a83679c1b93cd2b5696c8ed1e6b41d60df8b02',
    '/mnt/g2/release/root/code/pk02/m2b_asm_v1.py': '27560e5669498c6090d9f583b5dceaac03a572ad912c27a13395ee1ee43317e6',
    '/mnt/g2/release/root/code/pk15/mocks/mock_ritz_entries_v1.kv': '568e62829e1fa07f774b48f23e11d0f677be6841be81e2b84c2382d630a8f15a',
    '/mnt/g2/release/root/code/pk11/out/ts_N4_J170_D_S_z9sym_v1.json': 'ea9d6c1bc72cdac5b6d55091766a908937c7ce2bf60257636824388ffe5b7b5d',
    '/mnt/g2/release/root/code/pk11/out/ts_N3_S_z9sym_v1.json': 'a298db655d832c0685a9aba093dd123d372698fa2fb7905a15f442bb0e35f8e6',
    '/mnt/g2/release/root/code/pk01/out_kt_rb_v1_5_r4.out': '842edc202150668838ce24b1fc54f0adbebadc8f0df984480a44c84fed6ecf5a',
    '/mnt/g2/release/root/code/pk01/out_kt_rb_v1_5_r3.out': '3e79a6c072ad730235944064b5f1980252d28336e35b1af1a1ad4e0cc35e54cc',
    '/mnt/g2/release/root/code/pk03/out/m3_s9_N4_J300_v1_8_3.json': 'bcc6434c6a03eecb232f10504b63f1ce10a94a489d5a2ba9cf3fe09c8018b831',
    '/mnt/g2/release/root/code/pk03/out/m3_run_v1_8_3_asm9.4.out': 'a41763a35f405668c748cdd1aaccfff681aacf5fb096342a791659ccb49c07a7',
    '/mnt/g2/release/root/code/pk03/out/m3_s9_N3_J300_v1_8_3.json': 'd287d3dcbd4bd988aa8061fbe11b3da1609e0ab4d27ae1a619eadcee963e8fa5',
    '/mnt/g2/release/root/code/pk03/out/m3_run_v1_8_3_asm9.3.out': 'e7f09f7381919a8aef322adfae9ada7506bda4db527faba01b8deacdf6542655',
    '/mnt/g2/release/root/code/pk15/M4_KV_v1.txt': '4bafdcc1c41cf44f6b618644d7b0fdd404422aa5ffeadcfaadae02183e9eee51',
    '/mnt/g2/release/root/code/pk15/out/out_m4_asm_v1.out': '616dd9e1919695ed9dc953c55e8c46d66dabd9700d2913722d11f94502dc858e',
    '/mnt/g2/release/root/code/pk15/m4_reader_v1.py': '5cef440ae313eddd2e6bcf49aac835f2595e61b6a3e59b23fca0c15671ec6bcd',
    '/mnt/g2/release/root/code/pk07/out/export_kt_s9h_v1_2_vsweep.kv': '10f3c3d9a18b9c7a596121a8dbec7d2b82afb366704845a7c00e066c8bf6d4f6',
    '/mnt/g2/release/root/code/pk07/out/out_kt_s9h_v1_2_vsweep.out': '58814f7f59dd0d8e9d16b73084b3cc5072f94fb1138300a112e0e49ff017835f',
    '/mnt/g2/release/root/code/pk07/kt_s67_export_reader_v2_1.py': '4c6949462ca8c5dda337027b7dc5bada51102a063dc5ff6f8a1c2def01eaf49d',
    '/mnt/g2/release/root/code/pk07/kt_s9h_v1_2.py': '1b68e47141dfc5e873e2660711f6430a0badc9cc948ada32eb11641fabde4ff4',
    '/mnt/g2/release/root/code/pk03/P2_RUN_LIST_v1_10.json': '31b96a5376c3f074858c91784ebe719bdf732a0461f427fe075503e8a555e522',
    '/mnt/g2/release/root/code/pk03/m3_reader_v6_3.py': '539b613f6a9c07a9bef3d0cbb408c1d41de276a6a59aede8b03149204ce28661',
    '/mnt/g2/release/root/code/pk03/out/m3_s8v3_D_N4_J300_v1_8_1.json': '389be198d9fe919e1a097865759691847a9e4dc7553275c083d91bd753819b00',
    '/mnt/g2/release/root/code/pk03/out/m3_run_v1_8_1_asmP.4.out': '08c8fab3f4b9080424a40c8cb61b7932f557852520e8d49c5915092a8963a127',
    '/mnt/g2/release/root/code/pk03/out/m3_s8v3_D_N3_J300_v1_8_1.json': '8707107b0ebc3dea6989d22b6284f9df368c954837c883dc36824edda63c4926',
    '/mnt/g2/release/root/code/pk03/out/m3_run_v1_8_1_asmP.3.out': 'b6e9c2dd6a6308f6dc8d72124ba37326156983ec3444625d152ab46f28e927ed',
    '/mnt/g2/release/root/code/pk03/out/m3_s8v3_N_N4_J300_v1_8_2.json': '4afe8f5ba75d29cbf89f0c0940c9d7790b9a215cbf1faba6f4759d1fdd7b28d6',
    '/mnt/g2/release/root/code/pk03/out/m3_run_v1_8_2_asmN.4.out': '66a663de3924e2d8f8af1cdd65bfd88c0edc77cca9313f4dd2ef8cfb09eac3d9',
    '/mnt/g2/release/root/code/pk03/out/m3_s8v3_N_N3_J300_v1_8_2.json': '87f09d3ee43e44d7572e49b40f7103d2e1ef2b7409a1cb24b67d117b4145315a',
    '/mnt/g2/release/root/code/pk03/out/m3_run_v1_8_2_asmN.3.out': 'c1544e32848907c28ea30bf9e6e404fa836176947ce2f6f23e22ae4895c4697e',
    '/mnt/g2/release/root/code/pk03/m3_scal_v2.py': 'd22d3ad696074d4235f0fd31b026477e87f96f5d4b5331e29ab8d399e1e8f054',
    '/mnt/g2/release/root/code/pk03/m3_graph_v3.py': '46fd3c668e0121d58e6992636aec96f0d27c72176c70a69aa6a367f81c12da6a',
    '/mnt/g2/release/root/code/pk03/m3_series_v2.py': '08b1acf127062612d2dd3dd583e555f5ad3097b1b657cba89424019c4d958923',
    '/mnt/g2/release/root/code/pk03/m3_entries_v3.py': '7bf360cbc739cad1397aa5f23ba2ab3e838dec5d65c686880b664fe3318ce9a9',
    '/mnt/g2/release/root/code/pk03/S9_ENTRY_LIST_v1.json': '50beb53e74fe42aab6d5c889734fd91a04570ea69b2188fdd8ddf2379107de4e',
    '/mnt/g2/release/root/code/pk03/M3_ENTRY_LIST_v1_2.json': 'f6e844fb55249177e3cbeda4c2b974db78ea913b9dbef6f1f6880a622d9eac13',
    '/mnt/g2/release/root/code/pk15/P2_ENTRY_LIST_v1_3.json': 'c5741affabf029d35486b2c10a73aa23da5b804921d7256a386ea84df6bf3579',
    '/mnt/g2/release/root/code/pk15/mocks/mock_m3_entries_v2.kv': 'b7da93a3b5f4ce14204731e7c416fa205b6c2f2b7035e848d3dcc1bae5eb9f17',
    '/mnt/g2/release/root/code/pk08/HS_NORMX_LEMMA_NOTE_v1.md': 'ffd98fc1946714e36e86359c338c38a6b89af31eb7f707306a0a59f3f281493b',
    '/mnt/g2/release/root/code/pk15/mocks/mock_hs_inv_normx_v1.kv': '2231495b23a89e8228f902eb4a4f5d7137df07be535b7cca985b838ef48e0608',
    '/mnt/g2/release/root/code/pk08/out/HS_INV_NORMX_v1.kv': '90bbc6f2eaa35cee6b01a77c77995d35659028c9806d5e21278f1899a6c2e67e',
    '/mnt/g2/release/root/code/pk08/out/px08_hsd3_export_v1_run.out': 'e12440402124d07d7e5795d431b0e1d19073a7e6ae844e4235c650f4e452dea8',
    '/mnt/g2/release/root/code/pk11/out/s8hf_v1/out_kt_s8rf_v1_n4.out': 'a8644832e801ba75e25222df9070c3a494a7e16bd64b0832071564e14b95394f',
    '/mnt/g2/release/root/code/pk11/out/s8hf_v1/out_kt_s8rf_v1_n3.out': 'cc9cd98cfa466749593ff2de1e2e8deae4a435d15eacb6845d48e6a9e000caea',
    '/mnt/g2/release/root/code/pk07/kt_s9h_v1_3_readers.py': '631441d5360a31908e3709fb769950205fd9487be0ec336a6b41f624f3de1e09',
    '/mnt/g2/release/root/code/pk08/out/HS_INV_NORMX_v1_d3d4.kv': '45a2ab00dcbe47cf6873e5b12db69a1ff8ae3171c84abbc57c5ee43f8a39b343',
    '/mnt/g2/release/root/code/pk08/out/px08_hsd4_export_v1_run.out': '02122c7f140129bd2bf98e3f6330641eac840519c778f806af07764b3e071ada',
    '/mnt/g2/release/root/code/pk15/SPEC_HS_INV_NORMX_v1_2_ADD1.md': 'b289d61e4df0b7345db63843d3ac15d414723810982702bb3316d07e318a797c',
    '/mnt/g2/release/root/code/pk08/out/HS_INV_NORMX_v1_d3d4b.kv': 'b80760c5b79f121a0c39d3302308816064a482fb47c90341938d52f9420772a3',
    '/mnt/g2/release/root/code/pk08/out/px08_hsd3b_export_v1_1_run.out': '2fc5ab7f1701d98349920d28fd345e16c653e0872ecb2c0071cad09a558f2d38',
    '/mnt/g2/release/root/code/pk03/out/m3_p2_NTB_N4_J300_v1_10_4.json': 'd4db816d688fcaa6d24664e8df394f68bdee791720e93a37312ce403213833af',
    '/mnt/g2/release/root/code/pk03/out/m3_p2_DT_N4_J300_v1_10_4.json': '780a7adb4f508e0d847463684b8c547004453e0ce649af4a75bb12d8e1bae3e7',
    '/mnt/g2/release/root/code/pk03/out/m3_p2_NIT_N4_J300_v1_10_4.json': 'e0f1f01d52729b871da92c61997d7e66ff379016b10f311222ba859d6fedd209',
    '/mnt/g2/release/root/code/pk03/out/m3_p2_NIB_N4_J300_v1_10_4.json': 'b1ecd3dca3177c4fe41679141c07c7e3176ed6a0576ac5ad592b71e14b944fdf',
    '/mnt/g2/release/root/code/pk03/out/m3_p2_NIH_N4_J300_v1_10_4.json': 'f1c54f2f05d0937c96daa6e576093a58842f5c7e2fcf48c0262c56b3326dc66c',
    '/mnt/g2/release/root/code/pk03/out/m3_p2_NBT_N4_J300_v1_10_4.json': '7c44cdf920cc993496f9368144e754e9f92b334a4bd699c90381331aa3bab2d6',
    '/mnt/g2/release/root/code/pk03/out/m3_p2_NTT_N4_J300_v1_10_4.json': 'fd196bdb7e6a8ba1bc672a11505a4cae12d50f08e1ba4546d156c39ff400b1d8',
    '/mnt/g2/release/root/code/pk03/out/m3_run_v1_10_4_asm.4.out': 'ba673c06772faf6d110aa0d4bfdc733be0800a62b5b2f088e778f912210263af',
    '/mnt/g2/release/root/code/pk03/out/m3_p2_NTB_N3_J300_v1_10_4.json': '6e08eb659915dfff3cba6ad2a1ce8416fd76a1a89946a16e8058636ac468cd5e',
    '/mnt/g2/release/root/code/pk03/out/m3_p2_DT_N3_J300_v1_10_4.json': 'f06ae251666aff46b4fab26893831e5660cb508b1437ca63e877c8ddb728bf97',
    '/mnt/g2/release/root/code/pk03/out/m3_p2_NIT_N3_J300_v1_10_4.json': 'f732294cb89f9ffebe9cb9c0bc01254457133ff8a2d83388e659d0965efa68dc',
    '/mnt/g2/release/root/code/pk03/out/m3_p2_NIB_N3_J300_v1_10_4.json': '625c376d7def66f8307b238dfb0b4f4d120c4cb8fd3bbfdc1c2026b5090b88b8',
    '/mnt/g2/release/root/code/pk03/out/m3_p2_NIH_N3_J300_v1_10_4.json': '32b5f4648feedb76a700e6384cd9a0cba43d8a37944df03722b9dc9343d947ae',
    '/mnt/g2/release/root/code/pk03/out/m3_p2_NBT_N3_J300_v1_10_4.json': 'fa8d944489c4a221af5e8fb9cdd09d4b8d0ccafc4bc15b3ca6ab9a50e8afc1f4',
    '/mnt/g2/release/root/code/pk03/out/m3_p2_NTT_N3_J300_v1_10_4.json': 'fe26efa98164896e619396f3b65bb432dc081ac136efbf5375e3ca8c95b0b0f8',
    '/mnt/g2/release/root/code/pk03/out/m3_run_v1_10_4_asm.3.out': '822761d5ebc1b0dc4726a320742a89317a4a8476670ec27216a0a89b9e35a4b9',
    '/mnt/g2/release/root/code/pk03/BIGRULE_EXEMPT_v1_10_4_N4.json': '1e12ea4fec58c15ce44891ffac87cb512a90bad67dda10545efc8bfb13c7a917',
    '/mnt/g2/release/root/code/pk03/BIGRULE_EXEMPT_v1_10_4_N3.json': 'dc8fa8e7dad2a6c59e06ba6fb5a6aa59f1df17feb61083f6d6e960d5e1a5b8a2',
}


def sha_file(path):
    try:
        with open(path, 'rb') as fh:
            return hashlib.sha256(fh.read()).hexdigest()
    except OSError:
        return 'MISSING'


out('%s sha256 %s ITEM=%s LIM=%d (RLIMIT_CPU soft %d, hard %d)' % (LABEL, sha_file(os.path.abspath(__file__)), MODE, LIM, LIM, LIM + 5))
_bad = ['%s %s' % (os.path.basename(_p), sha_file(_p)) for _p in sorted(PINS) if sha_file(_p) != PINS[_p]]
out('C-HASH %s (%d pinned files)%s' % ('PASS' if not _bad else 'FAIL', len(PINS), (': ' + '; '.join(_bad)) if _bad else ''))
if _bad:
    out('VERDICT INVALID (C-HASH)')
    sys.exit(2)
from flint import arb, arb_mat, ctx
from fractions import Fraction   # v1_33 (1)
ctx.prec = 256

KTCERT_SHA = '765ed898af05c3a59c6f5bc87f5fd92cbbfaf05dc0dd54c545b5bf7f032ba95a'   # kt_cert_v1_7.py (pk02), the reader's pin
KERNEL_SHA = '12c839a6dcde8028d61e88dad31ad3dc3bf0faae850e8f9065407e3ace092cb0'   # arbeng_c2b_v2.py, from kt_cert_v1_7's OWNFILES
KERNEL_LINE = 'arbeng_c2b_v2.py %s ctx.prec 512' % KERNEL_SHA
M3_READER_SHA = 'b5b2c953b67c3e848b7561b7b059efb05f7788debd3cde18fefc39c100d929a0'   # pk03's m3_reader_v4_4.py, the bound loader; also in PINS
TOKENS = {'t': 'far logR gBb eps_r Z', 'am': 'far eps_r Z'}
NAMES = {'t': 'A_t', 'am': 'A_am'}
BADWORDS = ('PRECERT', 'STUB')
FLOATQ = {3: '3.8822e-04', 4: '1.5913e-03'}   # NOTE_P2_14_FLOAT_v1's float reading of ||Q_4 v_t||


class Refused(Exception):
    pass


class CapStop(Exception):
    pass


def need(what):
    if cpu() > LIM - 5:
        raise CapStop(what)


def lines_of(path):
    with open(path) as fh:
        return fh.read().split('\n')


def gate(fails, name, ok):
    if not ok:
        fails.append(name)
    return 'PASS' if ok else 'FAIL'


def dec_hi(x):
    """a decimal string (17 significant digits) whose value is >= every point of the ball x."""
    u = x.upper()
    f = float(u)
    for _ in range(8):
        s = '%.16e' % f
        if arb(s).lower() >= u:
            return s
        f = math.nextafter(f, math.inf)
    raise ValueError('dec_hi')


def dec_lo(x):
    """a decimal string (17 significant digits) whose value is <= every point of the ball x."""
    lo = x.lower()
    f = float(lo)
    for _ in range(8):
        s = '%.16e' % f
        if arb(s).upper() <= lo:
            return s
        f = math.nextafter(f, -math.inf)
    raise ValueError('dec_lo')


# ---- reader (a): kt_cert_v1_7 g records
def read_kt_cert_g(L, kind, N, mode):
    """returns the record's A ball [lo, hi] as exact decimals (hi is what the assembly uses), the VALUE upper end and the FLOAT-IN tokens."""
    if mode not in ('CERTIFIED', 'MOCK'):
        raise ValueError(mode)
    pre = '' if mode == 'CERTIFIED' else 'MOCK '
    L = [x for x in L if x != '']
    if not L or not L[0].startswith('%skt_cert_v1_7 sha256 %s ITEM=g.%sn%d ' % (pre, KTCERT_SHA, kind, N)):
        raise Refused('header')
    fmt = [x for x in L if x.startswith('FORMAT')]
    if any(w in x for x in fmt for w in BADWORDS):
        raise Refused('PRECERT/STUB format')
    if fmt != ['FORMAT KT_CERT_RECORD_v1_7 %s' % ('CERTIFIED' if mode == 'CERTIFIED' else 'MOCK')]:
        raise Refused('FORMAT %r' % fmt)
    if [x for x in L if x.startswith('KERNEL')] != ['KERNEL ' + KERNEL_LINE]:
        raise Refused('KERNEL')
    if [x for x in L if x.startswith('VERDICT')] != ['VERDICT VALID']:
        raise Refused('VERDICT')
    res = [x for x in L if x.startswith(pre + 'RESULT ')]
    if len(res) != 1 or len([x for x in L if 'RESULT ' in x]) != 1:
        raise Refused('RESULT count')
    m = re.match(r'^%sRESULT N=%d J=300 %s: %s \[(\S+), (\S+)\] bound \[(\S+), (\S+)\] FLOAT-IN (.+)$' % (re.escape(pre), N, kind, NAMES[kind]), res[0])
    if m is None:
        raise Refused('RESULT layout')
    lo, hi = arb(m.group(1)), arb(m.group(2))
    if not (lo.lower() <= hi.upper()) or not (arb(m.group(3)).lower() <= arb(m.group(4)).upper()):
        raise Refused('interval with hi < lo')
    if m.group(5) != TOKENS[kind]:
        raise Refused('FLOAT-IN tokens %r' % m.group(5))
    val = [x for x in L if x.startswith(pre + 'VALUE ')]
    mv = re.match(r'^%sVALUE N=%d J=300 %s: %s <= (\S+)( |$)' % (re.escape(pre), N, kind, NAMES[kind]), val[0]) if len(val) == 1 else None
    if mv is None or not (arb(mv.group(1)).lower() >= hi.upper()):
        raise Refused('VALUE line missing or below RESULT hi')
    return {'lo': lo.lower(), 'hi': hi.upper(), 'value_hi': arb(mv.group(1)).upper(), 'float_in': m.group(5)}


# ---- reader (d): strict S4U_KV_v1
def kv_parse(L):
    d, order = {}, []
    for x in L:
        if x == '' or x.startswith('#'):
            continue
        m = re.match(r'^([A-Z][A-Z0-9_]*) = (.*)$', x)
        if m is None:
            raise Refused('non-KV line %r' % x[:40])
        if m.group(1) in d:
            raise Refused('duplicate key %s' % m.group(1))
        d[m.group(1)] = m.group(2)
        order.append(m.group(1))
    return d, order


def read_kv(L, mode, record):
    """strict KV reader; mode CERTIFIED, MOCK or GRID (pk07's FLOAT grid export, for jlo and jhi only)."""
    d, order = kv_parse(L)
    for k in ('FORMAT', 'RECORD', 'TAG', 'EXPORT_STATUS'):
        if any(w in d.get(k, '') for w in BADWORDS):
            raise Refused('PRECERT/STUB in %s' % k)
    _mode_checks(d, mode, record)
    if d.get('RUN_VERDICT') != 'VALID':
        raise Refused('RUN_VERDICT %r' % d.get('RUN_VERDICT'))
    if not order or order[-1] != 'END' or d['END'] != record or d.get('RECORD') != record:
        raise Refused('RECORD/END')
    return d


def _mode_checks(d, mode, record):
    """the FORMAT, TAG, CLAIM and KERNEL checks of read_kv (v1_1: before RECORD/END, so that a mock is refused at its FORMAT)."""
    if mode == 'GRID':
        if d.get('FORMAT') != 'S4U_KV_v1' or record != 'EXPORT_KT_S67_v1':
            raise Refused('grid FORMAT/RECORD')
    elif mode == 'CERTIFIED':
        if d.get('FORMAT') != 'S4U_KV_v1' or not d.get('TAG', '').startswith('CERTIFIED ') or 'MOCK' in d.get('TAG', '') + d.get('EXPORT_STATUS', ''):
            raise Refused('certified FORMAT/TAG')
        if d.get('KERNEL') != KERNEL_LINE:
            raise Refused('KERNEL')
    elif mode == 'MOCK':
        if d.get('FORMAT') != 'S4U_KV_v1 MOCK' or not d.get('TAG', '').startswith('MOCK') or d.get('EXPORT_STATUS') != 'MOCK':
            raise Refused('mock FORMAT/TAG')
        if not d.get('CLAIM', '').startswith('MOCK'):
            raise Refused('claim prefix')
        if 'KERNEL' in d and d['KERNEL'] != KERNEL_LINE:
            raise Refused('KERNEL')
    else:
        raise ValueError(mode)
    return d


# ---- reader (b): M3 entries; reader (c): the other certified inputs
def _frac_ball(lo, hi):
    """the arb ball containing the exact rationals lo <= hi (fractions.Fraction)."""
    a = arb(lo.numerator) / arb(lo.denominator)
    b = arb(hi.numerator) / arb(hi.denominator)
    return a.lower().union(b.upper())


def load_m3(path, N, mode, J_REF=300, asm_out=None):
    """reader (b). Entries come back as (coefficient balls a_0..a_K, a constant bar ERR over t in [0, 1/J_REF]), as entry_ball gives them."""
    if mode == 'CERTIFIED':
        if sha_file(M3_READER_PATH) != M3_READER_SHA:
            raise Refused('m3_reader_v4_4 does not match its pin')
        import importlib.util
        spec = importlib.util.spec_from_file_location('m3_reader_v4_4', M3_READER_PATH)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        try:
            rec = mod.load(path, asm_out, int(J_REF), int(N))
        except Exception as e:
            raise Refused('m3_reader_v4_4.load: %s' % e)
        E = {}
        for key in rec['balls']:
            LO, HI, err = mod.entry_ball(rec, key)
            E[key] = ([_frac_ball(a, b) for a, b in zip(LO, HI)], (arb(err.numerator) / arb(err.denominator)).upper())
        return E
    d = read_kv(lines_of(path), 'MOCK', 'MOCK_M3_ENTRIES_v1')
    E = {}
    for k, v in d.items():
        m = re.match(r'^N%d_(M(3|4|4M)_[0-2][0-2])$' % N, k)
        if m:
            f = v.split()
            K = int(f[0])
            if len(f) != K + 3:
                raise Refused('entry %s layout' % k)
            E[m.group(1)] = ([arb(x) for x in f[1:K + 2]], arb(f[K + 2]).upper())
    if len(E) != 27 or d.get('N%d_ENTRIES' % N) != '27':
        raise Refused('entry count N=%d' % N)
    return E

def kv_key(k):
    """v1_35 (1): a run-list key in S4U_KV_v1 form ('SM3,0,0' -> 'SM3_0_0', 'Gxt,0,0' -> 'GXT_0_0', 'IhZb' -> 'IHZB')."""
    return k.replace(',', '_').upper()


def run_list(pins=None):
    """v1_35 (1): the pinned run list's entries by key (C-A-LIST's reference and C-A-MAP's table)."""
    pins = PINS if pins is None else pins
    if pins.get(RUN_LIST) is None or sha_file(RUN_LIST) != pins[RUN_LIST]:
        raise Refused('C-A-LIST: P2_RUN_LIST_v1_10 does not match its pin')
    with open(RUN_LIST) as fh:
        d = json.load(fh)
    ents = dict((e['key'], e) for e in d['entries'])
    if d.get('list') != 'P2_RUN_LIST_v1_10' or len(d['entries']) != len(RUN_KEYS) or sorted(ents) != sorted(RUN_KEYS):
        raise Refused('C-A-LIST: the run list does not hold exactly the 23 keys')
    return ents


def check_amap(ents, keymap):
    """v1_35 (1), C-A-MAP: every Set A key's slot in keymap against the run list: the slot's graph and two end factors, exactly i
    factors of the slot's i-kind and j of its j-kind and nothing else, each slot once; Sets C and W by graph and factor list (AMAP_CW)."""
    seen = {}
    for k in RUN_KEYS:
        e, s = ents[k], keymap.get(k)
        if k in AMAP_CW:
            if s != KEYMAP[k] or (e['graph'], e['factors']) != AMAP_CW[k]:
                raise Refused('C-A-MAP: %s is not %s on %s' % (k, AMAP_CW[k][1], AMAP_CW[k][0]))
            continue
        if not (isinstance(s, str) and len(s) == 5 and s[:2] in AMAP_A and s[2] == '_' and s[3] in '012' and s[4] in '012'):
            raise Refused('C-A-MAP: %s has no window slot' % k)
        g, cl, cr, fi, fj = AMAP_A[s[:2]]
        i, j = int(s[3]), int(s[4])
        f = e['factors']
        mid = f[1:-1]
        if e['graph'] != g or f[0] != cl or f[-1] != cr or len(mid) != i + j or mid.count(fi) != i or mid.count(fj) != j:
            raise Refused('C-A-MAP: %s (%s) does not fit slot %s' % (k, e['graph'], s))
        if s in seen:
            raise Refused('C-A-MAP: slot %s holds %s and %s' % (s, seen[s], k))
        seen[s] = k
    if len(seen) != 18:
        raise Refused('C-A-MAP: %d window slots filled, not 18' % len(seen))
    return True


def check_setac_list(top, pins=None):
    """v1_35 (1), C-A-LIST: a family record names the pinned run list as pk03's records do, entry_list = '<basename>:<sha256>'."""
    pins = PINS if pins is None else pins
    want = '%s:%s' % (os.path.basename(RUN_LIST), pins.get(RUN_LIST))
    if pins.get(RUN_LIST) is None or top.get('entry_list') != want:
        raise Refused('C-A-LIST: entry_list %r is not the pinned run list' % (top.get('entry_list'),))
    return True


def check_trial_full(top, N, pins=None, tag='C-A-TRIAL'):
    """v1_35 (1), (2): a record's trial_set names the pinned ts and vacres files as '<basename>:<sha256>' (C-A-TRIAL; C-C-TRIAL for S8)."""
    pins = PINS if pins is None else pins
    ts = top.get('trial_set') if isinstance(top, dict) else None
    for fld, p in (('ts', TS_FILES[N]), ('vacres', VACRES[N])):
        if not isinstance(ts, dict) or pins.get(p) is None or ts.get(fld) != '%s:%s' % (os.path.basename(p), pins[p]):
            raise Refused('%s: trial_set %s is not the pinned %s' % (tag, fld, os.path.basename(p)))
    return True


def m3r6_mod(pins=None):
    """v1_35 (1): pk03's m3_reader_v6_3, sha-pinned and imported from its file."""
    pins = PINS if pins is None else pins
    if pins.get(M3R6_PATH) is None or sha_file(M3R6_PATH) != pins[M3R6_PATH]:
        raise Refused('C-A-BIND: m3_reader_v6_3 does not match its pin')
    import importlib.util
    spec = importlib.util.spec_from_file_location('m3_reader_v6_3', M3R6_PATH)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def m3r6_entries(mod, rec):
    """v1_35 (1): a v6_3 record's entries as (coefficient balls, constant bar), built from entry_ball as load_m3 builds them from v4_4."""
    E = {}
    for key in rec['balls']:
        LO, HI, err = mod.entry_ball(rec, key)
        E[key] = ([_frac_ball(a, b) for a, b in zip(LO, HI)], (arb(err.numerator) / arb(err.denominator)).upper())
    return E


def m3r6_control(N, pins=None):
    """v1_35 (1), C-A-V63: S7's certified g,0,0 through m3_reader_v6_3 equals m3_reader_v4_4's, ball for ball (the certified path's control)."""
    pins = PINS if pins is None else pins
    rp, ap = S7G00[N]
    mod = m3r6_mod(pins)
    try:
        rec = mod.load(rp, ap, 300, int(N))
    except Exception as e:
        raise Refused('C-A-V63: m3_reader_v6_3.load %s: %s' % (os.path.basename(rp), e))
    a = m3r6_entries(mod, rec)['g,0,0']
    b = load_m3(rp, N, 'CERTIFIED', 300, ap)['g,0,0']
    if len(a[0]) != len(b[0]) or not all(x.mid() == y.mid() and x.rad() == y.rad() for x, y in zip(a[0], b[0])) or not (a[1] == b[1]):
        raise Refused('C-A-V63: v6_3 and v4_4 disagree on %s g,0,0' % os.path.basename(rp))
    return True


def m3r6_bind_text(N, verdict, pins=None):
    """v1_35 (1), PLANT-A-BIND-PRECERT: S7's record under its asm output with each VERDICT line replaced by verdict, through v6_3.loads."""
    pins = PINS if pins is None else pins
    rp, ap = S7G00[N]
    mod = m3r6_mod(pins)
    with open(rp) as fh:
        txt = fh.read()
    with open(ap) as fh:
        out2 = '\n'.join(verdict if x.startswith('VERDICT') else x for x in fh.read().split('\n'))
    try:
        mod.loads(txt, out2, 300, int(N), os.path.basename(rp))
    except Exception as e:
        raise Refused('C-A-BIND: %s' % e)
    return True


def load_setac(path, N, mode, pins=None, lines=None):
    """v1_35 (1), reader (b2): the 23 run-list entries (Sets A, C, W) at N as (coefficient balls, constant bar). MOCK: MOCK_M3_ENTRIES_v2 with
    kv_key keys (lines: plants only). CERTIFIED: the seven family records of SETAC_RECORDS through m3_reader_v6_3 under m3_run_v1_10_4's asm output
    (C-A-BIND: every file pinned, VERDICT VALID, the record's sha256 on its RECORD line, the arbeng_ma_v1_4_1 layer), each naming the pinned run
    list (C-A-LIST) and trial set (C-A-TRIAL) and carrying exactly the run-list keys of its graph (C-A-COUNT). C-A-MIRROR here."""
    pins = PINS if pins is None else pins
    EA = {}
    if mode == 'CERTIFIED':
        recs = SETAC_RECORDS.get(N) or []
        if [x[0] for x in recs] != list(SETAC_FAMS):
            raise Refused('C-A-BIND: the seven family records are not named at N=%d' % N)
        for X, rp, ap in recs:
            for p in (rp, ap):
                if pins.get(p) is None or sha_file(p) != pins[p]:
                    raise Refused('C-A-BIND: %s is not pinned (R4) or does not match its pin' % os.path.basename(p))
        mod, ents = m3r6_mod(pins), run_list(pins)
        for X, rp, ap in recs:
            try:
                rec = mod.load(rp, ap, 300, int(N))
            except Exception as e:
                raise Refused('C-A-BIND: m3_reader_v6_3.load %s: %s' % (os.path.basename(rp), e))
            top = rec['top']
            out('INFO C-A-BIND N=%d %s: record %s, kernel_file %s, kernel sha256 %s, claim_ball %s' % (N, X, pins[rp][:8], top.get('kernel_file'),   # v1_36 (3)
                str(top.get('kernel_sha256', ''))[:8], 'present' if 'claim_ball' in top else 'absent'))
            check_setac_layer(top, os.path.basename(rp))   # v1_36 (3): the per-record tests as functions, each planted
            check_setac_list(top, pins)
            check_trial_full(top, N, pins)
            check_setac_count(rec['balls'], X, ents, os.path.basename(rp))
            for k, v in m3r6_entries(mod, rec).items():
                if k in EA:
                    raise Refused('C-A-COUNT: key %s in two records' % k)
                EA[k] = v
            SETAC_TOPS[(N, X)] = top
    else:
        d = read_kv(lines if lines is not None else lines_of(path), 'MOCK', 'MOCK_M3_ENTRIES_v2')
        want = set(kv_key(k) for k in RUN_KEYS)
        for k in RUN_KEYS:
            v = d.get('N%d_%s' % (N, kv_key(k)))
            if v is None:
                raise Refused('C-A-COUNT: entry %s missing at N=%d' % (k, N))
            f = v.split()
            K = int(f[0])
            if len(f) != K + 3:
                raise Refused('entry %s layout' % k)
            EA[k] = ([arb(x) for x in f[1:K + 2]], arb(f[K + 2]).upper())
        pre = 'N%d_' % N
        extra = [x for x in d if x.startswith(pre) and x != pre + 'ENTRIES' and x[len(pre):] not in want]
        if extra or d.get(pre + 'ENTRIES') != str(len(RUN_KEYS)):
            raise Refused('C-A-COUNT: extra keys %s or entry count at N=%d' % (extra[:3], N))
    if sorted(EA) != sorted(RUN_KEYS):
        raise Refused('C-A-COUNT: the keys are not exactly the run list at N=%d' % N)
    if any(k.upper().startswith(('M4M', 'SM4M')) for k in EA):
        raise Refused('C-A-MIRROR: a record carries an M4M key')
    return EA


def moments_of(EA):
    """v1_35 (1): the fixed key map KEYMAP to the assembly's window moments, M4M := M4 (the mirror identity). Returns (E, EX): E the 27
    window moments M3_ij, M4_ij, M4M_ij; EX the route D and Set C entries W1, W2, IHZ, IHZB, IHZH."""
    E, EX = {}, {}
    for k, v in EA.items():
        a = KEYMAP[k]
        (E if a.startswith('M') else EX)[a] = v
    for ij in ('00', '10', '01', '20', '02', '11', '21', '12', '22'):
        E['M4M_' + ij] = E['M4_' + ij]
    if len(E) != 27 or sorted(EX) != ['IHZ', 'IHZB', 'IHZH', 'W1', 'W2']:
        raise Refused('key map: %d moments, extras %s' % (len(E), sorted(EX)))
    return E, EX



INKEYS = ('mhat', 'lt0', 'eps_r', 'sp', 'Lam', 'Hbad', 'Gbad', 'Lam_a', 'Abad', 'q', 'eps0', 'epsy', 't0', 'tx', 'ty', 'tz', 'dtz', 'ax', 'dax', 'Rcta')


def load_inputs(path, N, mode, cert=None):
    if (CERT_MODE if cert is None else cert):   # v1_35 (7): I[N] is never loaded in cert mode
        raise Refused('C-CERT-NOI: MOCK_S9B_INPUTS (I[N]) is not loaded in cert mode')
    L = lines_of(path)
    if mode == 'CERTIFIED':
        read_kv(L, 'CERTIFIED', 'S9B_INPUTS')
        raise Refused('no certified producer pinned for these inputs yet')
    d = read_kv(L, 'MOCK', 'MOCK_S9B_INPUTS_v1')
    I = dict((k, arb(d['N%d_%s' % (N, k.upper())])) for k in INKEYS)
    g = [arb(x) for x in d['N%d_G' % N].split()]
    r = float(d['N%d_G_RAD' % N])
    I['G'] = arb_mat(3, 3, [x + arb(0, r) for x in g])
    return I


def read_grid():
    d = read_kv(lines_of(GRID), 'GRID', 'EXPORT_KT_S67_v1')
    P = {}
    for N in (4, 3):
        rows = []
        for i in range(10000):
            v = d.get('N%d_P%04d' % (N, i))
            if v is None:
                break
            f = v.split('|')[0].split()
            rows.append(('%04d' % i, f[0], f[1]))
        P[N] = rows
    return P, d


# ---- writer (MOCK only)
def kv_write(path, record, header, rows):
    """writes a strict KV export; refuses (before opening) anything but a MOCK header and any value containing CERTIFIED."""
    if not _under(path, MOUT):
        raise ValueError('output path outside mocks/out')
    if header.get('FORMAT') != 'S4U_KV_v1 MOCK' or not header.get('TAG', '').startswith('MOCK') or header.get('EXPORT_STATUS') != 'MOCK' \
            or not header.get('CLAIM', '').startswith('MOCK') or header.get('RECORD') != record:
        raise ValueError('not a MOCK header')
    for k, v in list(header.items()) + list(rows):
        if 'CERTIFIED' in str(v).upper():
            raise ValueError('CERTIFIED in an output value (%s)' % k)
    with open(path, 'x') as fh:
        fh.write('# %s (MOCK): written by %s from MOCK records only; never a certified record, never a C-REP reference.\n' % (record, LABEL))
        for k, v in header.items():
            fh.write('%s = %s\n' % (k, v))
        for k, v in rows:
            fh.write('%s = %s\n' % (k, v))
        fh.write('END = %s\n' % record)
    return sha_file(path)


# ---- formulas
def qv4(A_hi, I):
    """||Q_4 v_t|| (kt_rb_v1_5's form with A_t, t_0 in place of A_h, h_0)."""
    mh, lt0 = I['mhat'], I['lt0']
    hb = I.get('HbadP', I['Hbad'])   # v1_9 (2): Hbad' = tau~0(Lam) kappa^2 when computed
    return (mh / (lt0 * lt0)) * A_hi + I['Lam'] * (mh / lt0) * I['eps_r'] + (I['Lam'] + I['t0'] + hb) * I['sp'] + I.get('GbadP', I['Gbad'])   # v1_12 (3): Gbad' (Lemma G) when computed


def tprov(A_hi, I):
    """the t provider's fields at J = 300 from reader (a)'s A_t and reader (c)'s inputs."""
    Q = qv4(A_hi, I)
    tx, ty, q, e0, ey = abs(I['tx']), abs(I['ty']), I['q'], I['eps0'], I['epsy']
    dtx = q * Q + e0 * I.get('t0t', I['t0']) + ey * ty + (q * q + e0 * e0 + ey * ey) * tx   # v1_30 (2): kt_rb's eps_0 h0t, h0t = d0 NH (t0t) on the port rows; the mock-input row keeps t0
    At = tx - dtx
    if not ((1 - I['sp'] * I['sp']) > 0):   # v1_34 (grep): C-SP, the denominator below
        raise Refused("C-SP: 1 - s'^2 is not certainly positive")
    vb = ((tx * tx + ty * ty + I['tz'] * I['tz'] + Q * Q) / (1 - I['sp'] * I['sp'])).sqrt()
    t0p = arb(0, 1) * (I['sp'] * vb).upper()   # v1_34 (grep): outward; v1_33 took float() of the upper end
    c = arb_mat(3, 1, [t0p, I['tx'], I['ty']])
    for i in range(3):   # v1_34 (grep): C-GRAM, G certainly positive definite (Gershgorin) before G^-1
        off = sum((abs(I['G'][i, j]) for j in range(3) if j != i), arb(0))
        if not ((I['G'][i, i] - off) > 0):
            raise Refused('C-GRAM: the Ritz-vector Gram G is not certainly positive definite (Gershgorin row %d)' % i)
    Gi = I['G'].inv()
    cGc = (c.transpose() * Gi * c)[0, 0]
    corr = (c.transpose() * (Gi - arb_mat(3, 3, [1, 0, 0, 0, 1, 0, 0, 0, 1])) * c)[0, 0]
    Vt = cGc + Q * Q
    Pt2 = t0p * t0p + ty * ty + 2 * tx * dtx + Q * Q + abs(corr)
    tz = abs(I['tz']) + I['dtz']
    Ot = tz * tz + Q * Q
    Rcta = dtx * abs(I['ax']) + tx * I['dax'] + dtx * I['dax']
    Xta = I['tx'] * I['ax'] - Rcta
    # Xtb by the flip (b~_x = a~_x, db_x = da_x): the same ball, so the same decimal; the export declares XTB_SOURCE = FLIP_OF_XTA
    Aa = abs(I['ax']) - I['dax']   # S9(b)'s A_a, the lower end X_ta uses (v1_5 (1))
    return {'Q': Q, 'dtx': dtx, 'At': At, 'Vt': Vt, 'Pt2': Pt2, 'Ot': Ot, 'tz': tz, 'Rcta': Rcta, 'Xta': Xta, 'Xtb': Xta, 'Aa': Aa}


def px_from(e2hi, clo, chi):
    """pX_hi = (E2_hi - c^2)^(1/2) with c the smallest |Cov| over [clo, chi] (exact arb ends); refuses a negative radicand (v1_5 (2))."""
    cmin = clo if clo > 0 else (-chi if chi < 0 else arb(0))
    rad = e2hi - cmin * cmin
    if not (rad.lower() >= 0):
        raise Refused('E2_hi - cmin^2 is not >= 0')
    return (rad.upper()).sqrt(), cmin


def px_print(e2_str, cov_str):
    """v1_8 (2): the printed pX_hi from the printed E2_hi and Cov_inf_lo decimals, in exact rationals: the smallest '%.16e' decimal whose square
    is >= E2_hi - max(Cov_inf_lo, 0)^2 (so pk07's exact C-SRC-J, pX_hi^2 >= E2_hi - Cov_inf_lo^2, holds on the printed values)."""
    from fractions import Fraction
    c = Fraction(cov_str)
    rad = Fraction(e2_str) - (c * c if c > 0 else 0)
    if rad < 0:
        raise Refused('E2_hi - Cov_inf_lo^2 < 0')
    x = math.sqrt(float(rad))
    for _ in range(64):
        s = '%.16e' % x
        if Fraction(s) * Fraction(s) >= rad:
            return s
        x = math.nextafter(x, math.inf)
    raise ValueError('px_print')


def check_srcj(L):
    """v1_8 (2): pk07's C-SRC-J on a joint export's text, exactly: pX_hi^2 >= E2_hi - Cov_inf_lo^2 on every row (FIELDS by name)."""
    from fractions import Fraction
    d, order = kv_parse(L)
    fl = d.get('FIELDS', '').split()
    if not all(x in fl for x in ('Cov_inf_lo', 'pX_hi', 'E2_hi')):
        raise Refused('FIELDS %r' % d.get('FIELDS'))
    ic, ip, ie = fl.index('Cov_inf_lo'), fl.index('pX_hi'), fl.index('E2_hi')
    n = 0
    for k in order:
        if re.fullmatch(r'N[34]_D(?:3|4|4M)_P[0-9]{4}', k):
            f = d[k].split()
            p, e, c = Fraction(f[ip]), Fraction(f[ie]), Fraction(f[ic])
            if p * p < e - c * c:
                raise Refused('row %s: pX_hi^2 < E2_hi - Cov_inf_lo^2' % k)
            n += 1
    return n


def export_status(float_in_lists, open_conds=None):
    """v1_8 (1), the FLOAT-IN rule: a certified-path export may read CERTIFIED only if every input's FLOAT-IN list is empty; otherwise its
    status is CERTIFIED_GIVEN_FLOAT_IN with the token lists named (pk07's reader refuses it as certified). Returns (status, FLOAT_IN value)."""
    named = ['%s: %s' % (k, ' '.join(v)) for k, v in sorted(float_in_lists.items()) if v]
    if named:
        return 'CERTIFIED_GIVEN_FLOAT_IN', '; '.join(named)
    if open_conds:
        return 'CERTIFIED_GIVEN_OPEN_CONDITIONS', 'none'   # v1_12 (4): the C1 rule
    return 'CERTIFIED', 'none'


def certified_tag(float_in_lists, open_conds=None):
    """the certified writer's guard (v1_8 (1)): refuses to tag an export CERTIFIED while any input carries FLOAT-IN tokens."""
    st, named = export_status(float_in_lists, open_conds)
    if st != 'CERTIFIED':
        raise Refused('FLOAT-IN inputs (%s), open conditions (%s): the export cannot be tagged CERTIFIED' % (named, ' '.join(sorted(open_conds or {})) or 'none'))
    return st


def width_corner(At_lo, Aa_lo, N, d_mixed):
    """v1_8 (3), C-WIDTH at the joint corner (pk07's m5 scan 6b643742): L = max(A_t,ref/At_lo, A_a,ref/Aa_lo) against the corner budget
    L_corner(N, d) at which the mixed kind's slack flips with A_t and A_a lowered together and pi_t, pi_a recomputed. v1_10: above the
    budget at the mixed d^h the remedy is the next d (kt_s9h decides the certified DH; P2-12 takes the step below), so it refuses only L above
    the budget at d^h + 1 (past P2-12's one-step allowance: stop and ask); returns (L, budget at d^h, at d^h + 1, the d^h that L supports)."""
    L = up(arb(A_REF[(N, 't')]) / At_lo, arb(A_REF[(N, 'a')]) / Aa_lo)
    b0, b1 = arb(L_CORNER[(N, d_mixed)]), arb(L_CORNER[(N, d_mixed + 1)])
    if not (L <= b1.lower()):
        raise Refused('corner ratio %s above even the budget %s at d^h + 1 = %d: stop and ask' % (dec_hi(L), L_CORNER[(N, d_mixed + 1)], d_mixed + 1))
    return L, b0, b1, (d_mixed if L <= b0.lower() else d_mixed + 1)


def check_flip(L):
    """C-FLIP  on the t export's text: XTB_SOURCE = FLIP_OF_XTA and Xtb_lo equal to Xta_lo string for string on every
    row. Any other source is refused: b's amplitudes have no producer yet (then the check becomes agreement within the stated bars)."""
    d, order = kv_parse(L)
    if d.get('XTB_SOURCE') != 'FLIP_OF_XTA':
        raise Refused('XTB_SOURCE %r' % d.get('XTB_SOURCE'))
    fl = d.get('FIELDS', '').split()
    if fl.count('Xta_lo') != 1 or fl.count('Xtb_lo') != 1:
        raise Refused('FIELDS %r' % d.get('FIELDS'))
    ia, ib = fl.index('Xta_lo'), fl.index('Xtb_lo')
    pieces = [d.get('N%d_PIECES' % N, '') for N in (4, 3)]
    if not all(re.fullmatch(r'[1-9][0-9]*', p) for p in pieces):
        raise Refused('PIECES %r' % pieces)
    n = 0
    for k in order:
        if re.fullmatch(r'N[34]_P[0-9]{4}', k):
            f = d[k].split()
            if len(f) != len(fl):
                raise Refused('row %s layout' % k)
            if f[ia] != f[ib]:
                raise Refused('row %s: Xtb_lo %s, Xta_lo %s' % (k, f[ib], f[ia]))
            n += 1
    if n != sum(int(p) for p in pieces):
        raise Refused('row count %d' % n)
    return n


def width_check(I, X):
    """INFO since v1_5 (3): the product form below is optimistic; the budget is pk07's corner slack. Kept to print eps_t and eps_a.
    C-WIDTH (plan v1_4): the relative losses eps_t = 1 - A_t,lo/|t_x| and eps_a = da_x/|a_x| against the split (0.03, 0.045) and the joint
    budget (1 - eps_t)(1 - eps_a) >= 1/1.085 (pk07: A_a's FLOAT distance to failure at d = 3, N = 4). Returns (eps_t, eps_a) upper ends."""
    et = (1 - X['At'] / abs(I['tx'])).upper()
    ea = (I['dax'] / abs(I['ax'])).upper()
    if not (et <= arb('0.03') and ea <= arb('0.045')):
        raise Refused('split: eps_t %s, eps_a %s' % (dec_hi(arb(et)), dec_hi(arb(ea))))
    if not ((1 - arb(et)) * (1 - arb(ea)) * arb('1.085')).lower() >= 1:
        raise Refused('joint budget: (1 - eps_t)(1 - eps_a) below 1/1.085')
    return et, ea


MOM = ((0, 0), (1, 0), (0, 1), (2, 0), (0, 2), (1, 1), (2, 1), (1, 2), (2, 2))
CLS = {'D3': ('M3', 3, 'h'), 'D4': ('M4', 2, 'v'), 'D4M': ('M4M', 2, 'v')}


class AD:
    """forward differentiation in arb: a value ball and a derivative ball."""
    __slots__ = ('v', 'd')

    def __init__(self, v, d):
        self.v, self.d = v, d

    def __add__(self, o):
        o = _ad(o)
        return AD(self.v + o.v, self.d + o.d)

    __radd__ = __add__

    def __sub__(self, o):
        o = _ad(o)
        return AD(self.v - o.v, self.d - o.d)

    def __rsub__(self, o):
        o = _ad(o)
        return AD(o.v - self.v, o.d - self.d)

    def __mul__(self, o):
        o = _ad(o)
        return AD(self.v * o.v, self.d * o.v + self.v * o.d)

    __rmul__ = __mul__

    def __truediv__(self, o):
        o = _ad(o)
        q = self.v / o.v
        return AD(q, (self.d - q * o.d) / o.v)

    def __neg__(self):
        return AD(-self.v, -self.d)


def _ad(x):
    return x if isinstance(x, AD) else AD(arb(x), arb(0))


def tball(jlo, jhi):
    """the piece's t range [1/jhi, 1/jlo] as a ball, its midpoint (exact) and radius (an upper bound)."""
    tl, th = t_ends(jlo, jhi)   # v1_33 (1): the hull of both readings of each end
    # v1_33 (1): t_ends takes t's upper end from the smaller J reading of jlo and t's lower end from the larger reading of jhi
    tb = tl.union(th)
    return tb, arb(tb.mid()), arb(tb.rad())


def grid_j(s, low):
    """v1_33 (1), the rule: a grid end string stands for its decimal and for its binary64 value (kt_s9h's reading); the
    smaller (low) or larger of Fraction(s) and Fraction(float(s)), exactly."""
    a, b = Fraction(s), Fraction(float(s))
    return min(a, b) if low else max(a, b)


def q2arb(f):
    """an exact Fraction as an arb ball (exact when the denominator is a power of 2, else a containing ball)."""
    return arb(f.numerator) / arb(f.denominator)


def t_ends(jlo, jhi):
    """v1_33 (1): the piece's t ends as points: t_lo from the larger reading of jhi (0 for 'inf'), t_hi from the smaller reading of jlo."""
    th = (arb(1) / q2arb(grid_j(jlo, True))).upper()
    tl = arb(0) if jhi == 'inf' else (arb(1) / q2arb(grid_j(jhi, False))).lower()
    return tl, th


def t_ends_dec(jlo, jhi):
    """v1_33 (1), for PLANT-GRID-DEC only: v1_32's ends, which read each end as its decimal alone."""
    th = (arb(1) / arb(jlo)).upper()
    tl = arb(0) if jhi == 'inf' else (arb(1) / arb(jhi)).lower()
    return tl, th


def ent_ad(e, t, with_d):
    """an entry at t (a point or a ball): value sum_k a_k t^k plus the constant bar, and its t-derivative sum_k k a_k t^(k-1) if with_d."""
    ak, err = e
    v, d, tk, tk1 = arb(0), arb(0), arb(1), arb(0)
    for k, a in enumerate(ak):
        v += a * tk
        if k:
            d += k * a * tk1
        tk1 = tk
        tk = tk * t
    return AD(v + err * arb(0, 1), d if with_d else arb(0))   # v1_34 (grep): outward, as entry_piece


def joint_ad(M):
    """E2 and Cov of one class from its nine window moments M[(i, j)] (AD numbers): the ratios M_ij/M_00 remove the normalization."""
    R = dict((k, M[k] / M[(0, 0)]) for k in M)
    me, mf = R[(1, 0)], R[(0, 1)]
    ex2 = _ad(0)
    for i, j in MOM:
        a, b = _ad(1), _ad(1)
        for _ in range(2 - i):
            a = a * (-me)
        for _ in range(2 - j):
            b = b * (-mf)
        ex2 = ex2 + math.comb(2, i) * math.comb(2, j) * a * b * R[(i, j)]
    return ex2, R[(1, 1)] - me * mf, me, mf


def joint_enclosure(E, pre, jlo, jhi):
    """E2, Cov and the two means over the piece by the mean-value form: f(t_m) with the entries' bars, plus f'([t]) [-r, r] (v1_1 change 1;
    v1_6 adds the means)."""
    tb, tm, r = tball(jlo, jhi)
    keys = ['%s_%d%d' % (pre, i, j) for i, j in MOM]
    mid = joint_ad(dict((ij, ent_ad(E[k], tm, False)) for ij, k in zip(MOM, keys)))
    der = joint_ad(dict((ij, ent_ad(E[k], tb, True)) for ij, k in zip(MOM, keys)))
    w = arb(0, 1) * r.upper()   # v1_34 (grep): outward
    return tuple(mid[i].v + der[i].d * w for i in range(4))


def norm_x(I, kf):
    le = I['Lam']
    lf, bf = (I['Lam'], I['Hbad']) if kf == 'h' else (I['Lam_a'], I['Abad'])
    return le * lf + lf * I['Hbad'] + le * bf + I['Hbad'] * bf


# ---- normX by Lemma S' (v1_6 (1))
def tau_tilde(N, L, cl):
    """the J-uniform horizontal tail slot: int_{xi > L} (xi - cl) e^-xi dmu / k1, bounded at J = 300, hence for every J >= 300."""
    if N == 3:
        return (L - cl + 1) * (-L).exp() / (1 - arb(-600).exp())
    sq, sp = L.sqrt(), arb.const_sqrt_pi()
    g32 = sq * (-L).exp() + sp / 2 * sq.erfc()
    g52 = L * sq * (-L).exp() + arb(3) / 2 * g32
    j0 = arb(300)
    low = sp / 2 * j0.sqrt().erf() - j0.sqrt() * (-j0).exp()
    return arb(2).sqrt() * (g52 - cl * g32) / low


def up(*xs):
    """an exact upper bound of the largest of the balls xs."""
    u = xs[0].upper()
    for x in xs[1:]:
        if x.upper() > u:
            u = x.upper()
    return u


def normx_sprime(N, cls, levels, ce, cf, kap):
    """Lemma S'. levels: two decimal strings (L_e, L_f); ce, cf: (lo, hi) exact ends of the means' balls of e and f; kap: kappa's ball.
    Returns (normX, box) as balls; refuses a level below c+ + 1."""
    Le, Lf = arb(levels[0]), arb(levels[1])
    (cel, ceh), (cfl, cfh) = ce, cf
    if not (Le >= ceh + 1 and Lf >= cfh + 1):
        raise Refused('a level below c+ + 1')
    box = up(Le - cel, ceh) * up(Lf - cfl, cfh)
    k2 = kap * kap
    if cls == 'D3':
        tails = (tau_tilde(N, Le, cel) * (arb(N - 1) / 2 + cfh) + tau_tilde(N, Lf, cfl) * (arb(N - 1) / 2 + ceh)) * k2 * kap
    else:
        g = up(cfh, (-1 - cfl).exp())
        tails = (tau_tilde(N, Le, cel) * g + (Lf - cfl) * (-Lf).exp() * (arb(N - 1) / 2 + ceh)) * k2
    return box + tails, box


def lam_h(N, J):
    """lambda_h(J) = exp(logmain_N - logmain_D) by riglap2's logmain (pk10/scripts/riglap2.py l.52-56), with det(L_sub)/V = tau(G), the weighted
    spanning-tree count (Kirchhoff), on lapl2.strip_graph(3) and (2): end triangles (A, A, B), interior verticals 1, horizontals 1 (v1_9 (1))."""
    A = ((arb(3) + arb(21).sqrt()) / 6).union(arb((3 + 21 ** 0.5) / 6))
    B = ((3 * arb(5).sqrt() - arb(21).sqrt()) / 12).union(arb((3 * 5 ** 0.5 - 21 ** 0.5) / 12))

    def tau(ncols):
        V = 3 * ncols
        L = arb_mat(V, V)
        E = []
        for j in range(ncols):
            T, M, Bv = 3 * j, 3 * j + 1, 3 * j + 2
            if j == 0 or j == ncols - 1:
                E += [(T, M, A), (M, Bv, A), (T, Bv, B)]
            else:
                E += [(T, M, arb(1)), (M, Bv, arb(1))]
            if j < ncols - 1:
                E += [(3 * j + r, 3 * (j + 1) + r, arb(1)) for r in range(3)]
        for u, v, c in E:
            L[u, u] += c
            L[v, v] += c
            L[u, v] -= c
            L[v, u] -= c
        Lr = arb_mat(V - 1, V - 1, [L[i, k] for i in range(1, V) for k in range(1, V)])
        return Lr.det()
    n = N - 1
    area = 2 * arb.pi() * arb.pi() if N == 4 else 4 * arb.pi()
    logl = -3 * area.log() + arb(3 * n) / 2 * (2 * arb.pi() / J).log() - arb(n) / 2 * (tau(3) / tau(2)).log()
    return logl.exp()


def kappa_bound(N, eps_r_max):
    """kappa_max = k1_hi(300)^3/((1 - eps_r_max) lambda_h(300)), valid for every J >= 300: lambda_h(J) J^(3(N-1)/2) and k1_hi(J) J^((N-1)/2) are
    constant, mhat >= 1 and lambda_0 >= (1 - eps_r) mhat lambda_h (NOTE_M4_SCOPE_v1 sect. 2; the review 606b1fe4 claim 1). v1_25 (1): eps_r_max is the certified eps_r of M2B_KV_v1 at J = 300 (LAW v1 is nonincreasing in J)."""
    j0 = arb(300)
    k1h = 1 / (2 * j0) if N == 3 else (2 / arb.pi()).sqrt() / (j0 * j0 * j0).sqrt()
    return k1h * k1h * k1h / ((1 - eps_r_max) * lam_h(N, j0))


def kappa_mock(I, N):
    """MOCK kappa: kappa^2 = Hbad e^40 k1_hi/(2J) at J = 300 from the mock inputs' Hbad (kt_rb_v1_5's level 40); k1_hi = 1/(2J) (N = 3),
    sqrt(2/pi) J^(-3/2) (N = 4). Certified: k1_hi^3/lambda_0,lo (M4)."""
    j0 = arb(300)
    k1h = 1 / (2 * j0) if N == 3 else (2 / arb.pi()).sqrt() / (j0 * j0 * j0).sqrt()
    return (I['Hbad'] * arb(40).exp() * k1h / (2 * j0)).sqrt()


# ---- Lemma G (NOTE_P2_17_GBAD_ABAD_v1) (v1_12)
BASIS = [(0,), (1,), (2,), (0, 0), (1, 1), (2, 2), (0, 1), (1, 2), (0, 2)]   # kt_rb_v1_5 l.198: monomials in (xi_TM, xi_MB, xi_TB)


def trial_ab():
    """the trial weights A = (3 + sqrt 21)/6 and B = (3 sqrt 5 - sqrt 21)/12 as hulls of the algebraic values and their binary64 roundings
    (kt_rb v1_2's convention, as in lam_h)."""
    A = ((arb(3) + arb(21).sqrt()) / 6).union(arb((3 + 21 ** 0.5) / 6))
    B = ((3 * arb(5).sqrt() - arb(21).sqrt()) / 12).union(arb((3 * 5 ** 0.5 - 21 ** 0.5) / 12))
    return A, B


def load_trial_q(path, N):
    """reader (f): the z9sym trial coefficients q1, q2, q3 (9 each, on BASIS) of pk11's vacres json (pinned), taken exactly: they define p0."""
    with open(path) as fh:
        d = json.load(fh)
    q = []
    for key in ('q1', 'q2', 'q3'):
        v = d.get(key)
        if not isinstance(v, list) or len(v) != 9 or not all(isinstance(x, (int, float)) and not isinstance(x, bool) for x in v):
            raise Refused('vacres %s: %s is not 9 numbers' % (os.path.basename(path), key))
        q.append([arb(x) for x in v])
    return q


def s_eps(q, eps, t):
    """(G3): S_eps = sup |p0| W^eps <= 1 + sum_i t^i sum_m |q_i[m]| prod_j (d_j/(eps w_j e))^d_j, w = (A, A, B): each monomial's sup over
    xi >= 0 against e^(-eps w . xi). Nonincreasing in J, so t = 1/300 bounds every J >= 300. Refuses eps outside (0, 1)."""
    if not (eps > 0 and eps < 1):
        raise Refused('Lemma G eps outside (0, 1)')
    A, B = trial_ab()
    w, e = (A, A, B), arb(1).exp()
    S, ti = arb(1), arb(1)
    for i in range(3):
        ti = ti * t
        for c, mono in zip(q[i], BASIS):
            f = arb(1)
            for j in range(3):
                d = mono.count(j)
                for _ in range(d):
                    f = f * d / (eps * w[j] * e)
            S = S + ti * abs(c) * f
    return S


def supp0_kt(q, J):
    """kt_rb's supp0 = 1 + sum_i t^i sum_m |q_i[m]| (2J)^deg on the same q (the sup over xi <= 2J; R6a), for C-SEPS."""
    S, ti = arb(1), arb(1)
    for i in range(3):
        ti = ti / J
        for c, mono in zip(q[i], BASIS):
            p = arb(1)
            for _ in mono:
                p = p * 2 * J
            S = S + ti * abs(c) * p
    return S


def k1_lim(N, J):
    """k1 <= 1/(2J) (N = 3) and k1 <= sqrt(2/pi) J^(-3/2) (N = 4, through I_1 <= I_1/2), for every J."""
    return 1 / (2 * J) if N == 3 else (2 / arb.pi()).sqrt() / (J * J * J).sqrt()


def bessel_i1(x):
    """I_1(x) for x > 0 by its power series. Once the term ratio r = (x/2)^2/((k + 1)(k + 2)) is below 1/2 and the last term below 2^-280 of
    the sum, the rest is at most term r/(1 - r), since the ratios decrease. For C-K1-LIM only."""
    h2 = (x / 2) * (x / 2)
    term, s, k = x / 2, x / 2, 0
    while True:
        term = term * h2 / ((k + 1) * (k + 2))
        s = s + term
        k += 1
        r = h2 / ((k + 1) * (k + 2))
        if r.upper() < 0.5 and (term / s).upper() < arb(2) ** -280:
            return s + arb(0, (term * r / (1 - r)).upper())


def k1_exact(N, J):
    """k1 = int e^-xi dmu: (1 - e^-2J)/(2J) at N = 3 and 2 e^-J I_1(J)/J at N = 4 (C-K1-LIM)."""
    if N == 3:
        return (1 - (-2 * J).exp()) / (2 * J)
    return 2 * (-J).exp() * bessel_i1(J) / J


def tau_tri(a1, a2, b):
    """the weighted spanning-tree count of the triangle (TM, MB, TB) with edge weights (a1, a2, b): a1 a2 + (a1 + a2) b, so a^2 + 2ab."""
    return a1 * a2 + (a1 + a2) * b


def tau_strip(ncols):
    """tau of lapl2.strip_graph(ncols), end triangles (A, A, B), interior verticals 1, horizontals 1: lam_h's graph, here for main_D (ncols 2)."""
    A, B = trial_ab()
    V = 3 * ncols
    L = arb_mat(V, V)
    E = []
    for j in range(ncols):
        T, M, Bv = 3 * j, 3 * j + 1, 3 * j + 2
        if j == 0 or j == ncols - 1:
            E += [(T, M, A), (M, Bv, A), (T, Bv, B)]
        else:
            E += [(T, M, arb(1)), (M, Bv, arb(1))]
        if j < ncols - 1:
            E += [(3 * j + r, 3 * (j + 1) + r, arb(1)) for r in range(3)]
    for a, b, c in E:
        L[a, a] += c
        L[b, b] += c
        L[a, b] -= c
        L[b, a] -= c
    return arb_mat(V - 1, V - 1, [L[i, k] for i in range(1, V) for k in range(1, V)]).det()


def jfac(N, J):
    """v1_13: the J-dependent factor of phi_main, k1_lim(J)^3 (2 pi/J)^(-3n/2); exactly constant in J (C-JPOW tests it alone)."""
    k = k1_lim(N, J)
    return k * k * k * (-arb(3 * (N - 1)) / 2 * (2 * arb.pi() / J).log()).exp()


def phi_main(N, wT, J):
    """k1_lim(J)^3 main_T(wT)/main_D by riglap2's logmain (pk10/scripts/riglap2.py l.52-56), main_G = area^-(V-1) (2 pi/J)^(n (V-1)/2)
    tau(G)^(-n/2) with V_T = 3 and V_D = 6: the J-powers cancel (C-JPOW)."""
    n = N - 1
    area = 2 * arb.pi() * arb.pi() if N == 4 else 4 * arb.pi()
    lg = 3 * area.log() - arb(n) / 2 * (tau_tri(*wT) / tau_strip(2)).log()
    # v1_13: the J-dependent factor is jfac (C-JPOW tests it alone)
    return jfac(N, J) * lg.exp()


def lg_weights(eps, theta):
    """(G4): the triangle edge weights (TM, MB, TB) of ||W||^2 (kt_rb's phi ratio), ||W^(1-eps)||^2 and ||W_theta||^2."""
    A, B = trial_ab()
    w0 = (2 * A, 2 * A, 2 * B)
    we = (2 * (1 - eps) * A, 2 * (1 - eps) * A, 2 * (1 - eps) * B)
    wt = (2 * (1 - theta) * (1 - eps) * A, 2 * (1 - theta) * (1 - eps) * A, 2 * (1 - eps) * B)
    return w0, we, wt


def phi_lg(N, S, wT, zr):
    """Lemma G's Phi in certified form: c_K S^2 ||W'||_2^2/||psi-hat||^2 <= S^2 phi_main(N, wT, 300) zr, with zr = Z_T(wT)/Z_psi, riglap2.bound's
    remainder at the weights over G_00's (from the certified run, ; MOCK in this skeleton)."""
    return S * S * phi_main(N, wT, arb(300)) * zr


def gbad_p(N, Lam, kap, u, phi_e):
    """(G1): Gbad'(Lam) = tau~0(Lam) kappa (kappa + u) sqrt(Phi_eps), for Lam >= 1."""
    if not (Lam >= 1):
        raise Refused('Lemma G level Lam below 1')
    return tail_h(N, 1, Lam, arb(0)) * kap * (kap + u) * phi_e.sqrt()


def abad_p(Lam_a, kap, u, phi_e, phi_t, eps, theta):
    """(G2): Abad'(Lam_a) = Lam_a e^(-2 Lam_a) kappa sqrt(Phi_eps) + u Lam_a e^(-2 theta (1 - eps) A Lam_a) sqrt(Phi_eps,theta), for theta in
    (0, 1), Lam_a >= 1/2 and Lam_a >= 1/(2 theta (1 - eps) A)."""
    A, _b = trial_ab()
    c = 2 * theta * (1 - eps) * A
    if not (theta > 0 and theta < 1 and Lam_a >= arb(1) / 2 and Lam_a * c >= 1):
        raise Refused('Lemma G level Lam_a below max(1/2, 1/(2 theta (1 - eps) A)), or theta outside (0, 1)')
    return Lam_a * (-2 * Lam_a).exp() * kap * phi_e.sqrt() + u * Lam_a * (-c * Lam_a).exp() * phi_t.sqrt()


def lg_weights_b(eps, theta):
    """v1_14 (1), Lemma E-prime: the triangle weights of ||W_theta^(b)||^2: bond b's weight cut to (1 - theta)(1 - eps)A, the other vertical
    bond at (1 - eps)A and TB at (1 - eps)B, each doubled for the square."""
    A, B = trial_ab()
    return (2 * (1 - theta) * (1 - eps) * A, 2 * (1 - eps) * A, 2 * (1 - eps) * B)


def remainder_ratios(zr0, mode):
    """v1_15 (2): one remainder ratio Z_T(w)/Z_psi per triangle weight set: W^(1-eps) ('eps'), Lemma G's W_theta ('theta')
    and Lemma E-prime's W_theta^(b) ('theta_b', the same for D4 and D4M by the flip T <-> B). CERTIFIED: no certified source (riglap2.bound at
    these weights, ) is pinned yet, so it refuses. MOCK: kt_rb's ratio zr0 times a separate MOCK factor per set (ZR_MOCK)."""
    if mode == 'CERTIFIED':
        raise Refused('no certified remainder source (riglap2.bound at the Lemma G weights) pinned yet')
    return dict((k, zr0 * arb(ZR_MOCK[k])) for k in ('eps', 'theta', 'theta_b'))


def need_ratios(zr):
    """v1_15 (2): the three remainder ratios are separate inputs; a missing one is refused, never copied from another."""
    for k in ('eps', 'theta', 'theta_b'):
        if k not in zr:
            raise Refused('remainder ratio %s missing' % k)
    return zr


def check_theta(theta_g, theta_e):
    """v1_15 (1), the rule: Lemma G's Abad' and Lemma E-prime use one theta, THETA_G (compared as the defining strings)."""
    if not (theta_g == theta_e == THETA_G):
        raise Refused('Abad-prime and Lemma E-prime use different theta (%s, %s)' % (theta_g, theta_e))
    return True


def rho_h(r, qL, qQ, c):
    """v1_16, Lemma R: h(r) = e^(-c r)(q_Q r^2 + q_L r - 1)."""
    return (-c * r).exp() * (qQ * r * r + qL * r - 1)


def rho_terms(q, eps, t):
    """v1_16, Lemma R (NOTE_P2_14_RHO_v1): (q_L, q_Q, r0, c, sigma_eps). Q_m = sum_i t^i |q_i[m]|; q_L and q_Q are upper bounds of the largest
    linear and quadratic Q_m; r0 is the positive root of q_Q r^2 + q_L r = 1; c = eps B; sigma_eps = sup over r >= r0 of rho_h, which is h(r*)
    at the positive root r* of c q_Q r^2 + (c q_L - 2 q_Q) r - (c + q_L) = 0 when r* >= r0 (h rises before r* and falls after), else 0."""
    if not (eps > 0 and eps < 1):
        raise Refused('Lemma R eps outside (0, 1)')
    _a, B = trial_ab()
    ti = [t, t * t, t * t * t]
    Qm = [ti[0] * abs(q[0][m]) + ti[1] * abs(q[1][m]) + ti[2] * abs(q[2][m]) for m in range(9)]
    qL, qQ = up(*Qm[:3]), up(*Qm[3:])
    c = eps * B
    if not (qQ > 0):   # v1_35 (4), the division below
        raise Refused('Lemma R: q_Q is not certainly positive')
    r0 = (-qL + (qL * qL + 4 * qQ).sqrt()) / (2 * qQ)
    a2, a1, a0 = c * qQ, c * qL - 2 * qQ, -(c + qL)
    rs = (-a1 + (a1 * a1 - 4 * a2 * a0).sqrt()) / (2 * a2)
    sig = arb(0) if rs < r0 else up(rho_h(rs, qL, qQ, c), arb(0))
    return qL, qQ, r0, c, sig, rs


def check_sigma(sig, qL, qQ, c, r0, n=2000):
    """v1_16, C-RHO-GRID: refuses sig if rho_h is definitely above it at a grid point of [r0, 50 r0]."""
    for k in range(n + 1):
        r = r0 + r0 * 49 * k / n
        if not (rho_h(r, qL, qQ, c).lower() <= sig.upper()):   # v1_35 (4): fails closed on NaN
            raise Refused('sigma_eps below rho_h at r = %s' % r.str(6, radius=False))
    return True


def load_g00(mode, pins=None):
    """v1_17 (1), v1_20 (1): G_00's lower end per N over every J >= 300, Lemma T-prime's only J-dependent input. CERTIFIED: S7's certified g,0,0
    (g00_s7; refused only on a pin failure of a record or its asm output, or on the normalization pin). MOCK: G00_MOCK, for tests only."""
    if mode == 'CERTIFIED':
        return dict((N, g00_s7(N, pins)[0]) for N in (4, 3))
    return dict((N, arb(G00_MOCK)) for N in (4, 3))


def g00_s7(N, pins=None):
    """v1_20 (1): S7's certified g,0,0 at N (pk03: the same object as S9's G,0,0). The record and its asm output must match their pins (PINS,
    or pins for a plant), the entry must pass check_g00_entry, and its lower end over every J >= 300 is g00_lower's. Returns (lower end, value
    at J = 300, err, record)."""
    pins = PINS if pins is None else pins
    rp, ap = S7G00[N]
    for p in (rp, ap):
        if pins.get(p) is None or sha_file(p) != pins[p]:
            raise Refused('S7 g,0,0 file %s does not match its pin' % os.path.basename(p))
    cf7, er7 = load_m3(rp, N, 'CERTIFIED', 300, ap)['g,0,0']
    with open(rp) as fh:
        r7 = json.load(fh)
    check_g00_entry(r7['claim'], r7['items']['g,0,0']['a0_exact'], cf7[0].lower(), cf7[0].upper())
    check_trial_set(r7, N, pins)   # v1_25 (3): main, on the note 1
    t300 = 1 / arb(300)
    v300 = arb(0)
    for a in reversed(cf7):
        v300 = v300 * t300 + a
    return check_g00(g00_lower(cf7, er7, t300)), v300, er7, r7


def check_g00(g):
    """v1_17 (1), a piece whose G_00 lower end is not certainly positive is refused."""
    if not (g > 0):
        raise Refused('G_00 lower end not certainly positive')
    return g


def check_g00_entry(claim, a0_exact, lo0, hi0):
    """v1_19 (1), the pin: an M3 G,0,0 entry (S7's g,0,0) stands for <phi_0, K phi_0>/main_D only if its record's claim starts with G00_CLAIM,
    its a0_exact is '1' and its a_0 ball is exactly 1 (the t = 0 value; a wrong main term or area factor would move it)."""
    if not (isinstance(claim, str) and claim.startswith(G00_CLAIM) and a0_exact == '1' and lo0 == 1 and hi0 == 1):
        raise Refused('G,0,0 normalization does not match the pin (claim, a0_exact or a_0)')
    return True


def g00_lower(coef, err, t_hi):
    """v1_19 (2): the lower end of sum_k a_k t^k - err over t in [0, t_hi], the cubic as a ball over the t-interval (pk03's rule)."""
    t = arb(0).union(t_hi)
    s = arb(0)
    for a in reversed(coef):
        s = s * t + a
    return (s - err).lower()


def phi_T(N, S, wT, g00):
    """v1_17 (1), Lemma T-prime (NOTE_P2_17_TRIANGLE_v1): c_K S^2 ||W'||^2/||psi-hat||^2 <= S^2 (tau_D/(w_1 w_2))^(n/2)/G_00,
    with the TB edge (the smallest weight) in the trace and (w_1, w_2) the TM and MB weights; every power of J, area and 2 pi cancels."""
    r = tau_strip(2) / (wT[0] * wT[1])
    f = r * r.sqrt() if N == 4 else r
    return S * S * f / check_g00(g00)


def phi_T_k1(N, S, wT, g00, J):
    """v1_17 (1), C-PHIT-FORM: the same bound in its k1_lim form at J, S^2 k1_lim(J)^3 k1_lim(J w_1) k1_lim(J w_2)/(main_D(J) G_00)."""
    n = N - 1
    area = 2 * arb.pi() * arb.pi() if N == 4 else 4 * arb.pi()
    lmd = -5 * area.log() + arb(5 * n) / 2 * (2 * arb.pi() / J).log() - arb(n) / 2 * tau_strip(2).log()
    k = k1_lim(N, J)
    return S * S * k * k * k * k1_lim(N, J * wT[0]) * k1_lim(N, J * wT[1]) / (lmd.exp() * g00)


def main_T_val(N, wT, J):
    """v1_17 (2): the triangle's Laplace main term, area^-2 (2 pi/J)^n tau(w)^(-n/2) (riglap2's logmain, V_T = 3), for C-TRACE's Z_T."""
    n = N - 1
    area = 2 * arb.pi() * arb.pi() if N == 4 else 4 * arb.pi()
    return (-2 * area.log() + arb(n) * (2 * arb.pi() / J).log() - arb(n) / 2 * tau_tri(*wT).log()).exp()


def bessel_in_series(nu, x):
    """v1_17 (2): I_nu(x) for integer nu >= 0 and x > 0 by its power series; once the term ratio is below 1/2 and the last term below 2^-280 of
    the sum, the rest is at most term r/(1 - r), since the ratios decrease."""
    term = arb(1)
    for j in range(1, nu + 1):
        term = term * (x / 2) / j
    h2 = (x / 2) * (x / 2)
    s, k = term, 0
    while True:
        term = term * h2 / ((k + 1) * (k + 1 + nu))
        s = s + term
        k += 1
        r = h2 / ((k + 1) * (k + 1 + nu))
        if r.upper() < 0.5 and (term / s).upper() < arb(2) ** -280:
            return s + arb(0, (term * r / (1 - r)).upper())


def sph_i_series(l, x):
    """v1_17 (2): the modified spherical Bessel i_l(x) = sum_k x^(l + 2k)/(2^k k! (2l + 2k + 1)!!) for x > 0, with bessel_in_series's tail rule."""
    term = arb(1)
    for j in range(1, l + 1):
        term = term * x / (2 * j + 1)
    s, k = term, 0
    while True:
        term = term * x * x / (2 * (k + 1) * (2 * l + 2 * k + 3))
        s = s + term
        k += 1
        r = x * x / (2 * (k + 1) * (2 * l + 2 * k + 3))
        if r.upper() < 0.5 and (term / s).upper() < arb(2) ** -280:
            return s + arb(0, (term * r / (1 - r)).upper())


def lambda_list(N, c, L):
    """v1_17 (2), Lemma T: the Funk-Hecke eigenvalues lambda_0..lambda_L of e^(-c(1 - x.y)), 2 e^-c I_(l+1)(c)/c (N = 4) or e^-c i_l(c) (N = 3),
    from series at the two top orders and the downward recurrence (all terms positive, so it is stable)."""
    if N == 4:
        I = [None] * (L + 3)
        I[L + 2], I[L + 1] = bessel_in_series(L + 2, c), bessel_in_series(L + 1, c)
        for nu in range(L + 1, 1, -1):
            I[nu - 1] = I[nu + 1] + 2 * nu / c * I[nu]
        return [2 * (-c).exp() * I[l + 1] / c for l in range(L + 1)]
    i = [None] * (L + 2)
    i[L + 1], i[L] = sph_i_series(L + 1, c), sph_i_series(L, c)
    for l in range(L, 0, -1):
        i[l - 1] = i[l + 1] + (2 * l + 1) / c * i[l]
    return [(-c).exp() * i[l] for l in range(L + 1)]


def trace_T(N, wT, J, L=600):
    """v1_17 (2), Lemma T: ||W'||^2 = sum_l dim_l prod_e lambda_l(J w_e), with the geometric tail T_L R_L/(1 - R_L),
    R_L = (dim_(L+1)/dim_L) prod_e c_e/(2(nu_L + 1)), nu_L = L + 1 (N = 4) or L + 1/2 (N = 3); refused unless R_L < 1/2."""
    cs = [J * w for w in wT]
    lams = [lambda_list(N, c, L) for c in cs]

    def dim(l):
        return (l + 1) * (l + 1) if N == 4 else 2 * l + 1
    s = arb(0)
    for l in range(L + 1):
        s = s + dim(l) * lams[0][l] * lams[1][l] * lams[2][l]
    nuL = arb(L + 1) if N == 4 else arb(2 * L + 1) / 2
    RL = arb(dim(L + 1)) / dim(L)
    for c in cs:
        RL = RL * c / (2 * (nuL + 1))
    if not (RL < arb('0.5')):
        raise Refused('Lemma T tail ratio R_L not below 1/2 (L = %d)' % L)
    TL = dim(L) * lams[0][L] * lams[1][L] * lams[2][L]
    return s + arb(0, (TL * RL / (1 - RL)).upper())


def check_c1(lines):
    """v1_14 (2), C-C1: the M2B record clears C1 only if exactly one of its lines starts with 'CLAIM = ' and holds C1_CLAIM, the agreed 41-byte
    string, exactly once (the same string and length check as pk07's)."""
    if len(C1_CLAIM.encode('utf-8')) != 41:
        raise Refused('C1_CLAIM is not the agreed 41-byte string')
    cl = [ln for ln in lines if ln.startswith('CLAIM = ')]
    if len(cl) != 1 or cl[0].count(C1_CLAIM) != 1:
        raise Refused('the M2B record CLAIM does not state the |g| form exactly once (C1)')
    return True


def open_conditions(m2b_lines=None):
    """v1_14 (2): C1 stays open until a pinned M2B record's lines pass check_c1 (a pinned record that fails is refused)."""
    if m2b_lines is not None and check_c1(m2b_lines):
        return {}
    return dict(OPEN_CONDITIONS)


def check_trial_set(r7, N, pins=None):
    """v1_25 (3), the addition on the note 1: S7's g,0,0 serves as G_00 only if its record's trial_set names the vacres file the
    assembly pins for S_eps, VACRES[N], with its pinned sha prefix (the record writes basename:sha8). a_0 = 1 does not depend on the trial, so
    check_g00_entry cannot see a mismatch."""
    pins = PINS if pins is None else pins
    want = '%s:%s' % (os.path.basename(VACRES[N]), (pins.get(VACRES[N]) or '')[:8])
    ts = r7.get('trial_set') if isinstance(r7, dict) else None
    got = ts.get('vacres') if isinstance(ts, dict) else None
    if pins.get(VACRES[N]) is None or got != want:
        raise Refused('S7 record trial_set vacres %r is not the pinned %s' % (got, want))
    return True


def load_m2b(pins=None):
    """v1_25 (1), (2), the M2(b) reader: pk02's certified vacuum record M2B_KV_v1 through its one sha-pinned reader m2b_reader_v1.load, which
    binds the record to m2b_asm_v1's run output (VERDICT lines exactly [VERDICT VALID], the RECORD line naming the record's sha256), runs the
    record's own checks (allow-listed keys, FORMAT, LAW, VERDICT, CLAIM, C-MONO, C-FMT) and C-PINS with this reader's pinned sha256. The record,
    its asm output and the reader must match their pins first, the flint precision is restored after the reader's import, and check_c1 must pass
    on the record's lines (C-C1, live). Returns (rec, reader module, record lines)."""
    pins = PINS if pins is None else pins
    for p in (M2B[0], M2B[1], M2B_READER_PATH):
        if pins.get(p) is None or sha_file(p) != pins[p]:
            raise Refused('M2(b) file %s does not match its pin' % os.path.basename(p))
    import importlib.util
    spec = importlib.util.spec_from_file_location('m2b_reader_v1', M2B_READER_PATH)
    mod = importlib.util.module_from_spec(spec)
    p0 = ctx.prec
    spec.loader.exec_module(mod)
    ctx.prec = p0
    try:
        rec = m2b_call(mod.load, M2B[0], M2B[1], expected_sha256=pins[M2B[0]], reader_sha256=pins[M2B_READER_PATH])
    except Exception as e:
        raise Refused('m2b_reader_v1.load: %s' % e)
    L = lines_of(M2B[0])
    check_c1(L)
    return rec, mod, L


def m2b_eps(vals):
    """v1_25 (1): (eps_r, s, s-prime = s (1 + s)) as arb balls from law_v1's decimal strings, each at or above its upper end; s-prime is the
    kt_rb form that the mock key sp holds. s = inf (2 - Rtr - eps_r not certainly positive) is refused."""
    if not isinstance(vals, dict) or vals.get('eps_r') in (None, 'inf') or vals.get('s') in (None, 'inf'):
        raise Refused('M2(b) law_v1 gave no finite eps_r and s')
    er, s = arb(vals['eps_r']), arb(vals['s'])
    if not ((er > 0) and (s > 0) and (er < 1) and (s < 1)):
        raise Refused('M2(b) eps_r and s are not inside (0, 1)')
    return er, s, s * (1 + s)


def m2b_reader_plant(fn, *args):
    """v1_25 (1): a reader call made for a plant; any refusal of the reader (a ValueError) becomes Refused."""
    try:
        return m2b_call(fn, *args)
    except Exception as e:
        raise Refused('m2b_reader_v1: %s' % e)


def m2b_call(fn, *args, **kw):
    """(4), the note 3 on v1_26: every call into m2b_reader_v1 runs at ctx.prec = M2B_PREC, restored afterwards, so the reader's
    balls do not depend on the assembly's precision; a call that leaves ctx.prec changed is refused."""
    p0 = ctx.prec
    ctx.prec = M2B_PREC
    try:
        r = fn(*args, **kw)
        if ctx.prec != M2B_PREC:
            raise Refused('a reader call changed ctx.prec to %d' % ctx.prec)
        return r
    finally:
        ctx.prec = p0


def load_m4(pins=None):
    """v1_32 (1): the certified M4 law record M4_KV_v1 through its one sha-pinned reader m4_reader_v1.load, which binds the record to
    m4_asm_v1's run output (VERDICT lines exactly [VERDICT VALID], one RECORD line naming the record's sha256), runs the record's own checks
    (allow-list, exact fields, forms, C-MONO, C-FMT) and C-PINS with this reader's pinned sha256. The record, its run output and the reader must
    match their pins first; flint's precision is restored after the reader's import. Returns (rec, reader module)."""
    pins = PINS if pins is None else pins
    for p in (M4[0], M4[1], M4_READER_PATH):
        if pins.get(p) is None or sha_file(p) != pins[p]:
            raise Refused('M4 file %s does not match its pin' % os.path.basename(p))
    import importlib.util
    spec = importlib.util.spec_from_file_location('m4_reader_v1', M4_READER_PATH)
    mod = importlib.util.module_from_spec(spec)
    p0 = ctx.prec
    spec.loader.exec_module(mod)
    ctx.prec = p0
    try:
        rec = m4_call(mod.load, M4[0], M4[1], pins[M4[0]], pins[M4_READER_PATH])
    except Exception as e:
        raise Refused('m4_reader_v1.load: %s' % e)
    return rec, mod


def m4_call(fn, *args):
    """v1_32 (1): every call into m4_reader_v1 runs at ctx.prec = M4_PREC, restored afterwards; a call that leaves it changed is refused."""
    p0 = ctx.prec
    ctx.prec = M4_PREC
    try:
        r = fn(*args)
        if ctx.prec != M4_PREC:
            raise Refused('an M4 reader call changed ctx.prec to %d' % ctx.prec)
        return r
    finally:
        ctx.prec = p0


def m4_law(rec, mod, kind, N, jlo):
    """v1_32 (1): L_k at the piece's left end as an arb ball around m4_reader_v1.law's decimal (at or above L_k(jlo)); L_k is nonincreasing in
    J, so the ball bounds the quantity on the whole piece."""
    try:
        s = m4_call(mod.law, rec, kind, N, jlo)
    except Exception as e:
        raise Refused('m4_reader_v1.law %s N=%d at %s: %s' % (kind, N, jlo, e))
    x = arb(s)
    if not (x > 0):
        raise Refused('the M4 law %s N=%d at %s is not positive' % (kind, N, jlo))
    return x


def m2b_mhat_coeffs(asm_lines, N):
    """(1), main and the review on the lt0 clause: the trial m1, m2, m3 at N as the M2(b) record's asm output lists them in its passing C-MHAT
    line (the output that m2b_reader_v1 binds to the record), parsed exactly (a Python float repr round-trips)."""
    pre = 'C-MHAT N=%d: m1..m3 = [' % N
    L = [x for x in asm_lines if x.startswith(pre)]
    if len(L) != 1 or not L[0].rstrip().endswith('-> PASS'):
        raise Refused('the M2B asm output has no single passing C-MHAT line for N=%d' % N)
    try:
        m = [float(x) for x in L[0][len(pre):].split(']', 1)[0].split(', ')]
    except ValueError:
        raise Refused('the M2B asm output C-MHAT line for N=%d does not parse' % N)
    if len(m) != 3 or not all(x >= 0 for x in m):
        raise Refused('the M2B asm output C-MHAT line for N=%d does not hold three nonnegative m' % N)
    return m


def vacres_m(path):
    """(1): m1, m2, m3 of a pinned vacres json, exactly as binary64."""
    with open(path) as fh:
        d = json.load(fh)
    m = [d.get(k) for k in ('m1', 'm2', 'm3')]
    if not all(isinstance(x, (int, float)) and not isinstance(x, bool) for x in m):
        raise Refused('vacres %s: m1, m2, m3 are not numbers' % os.path.basename(path))
    return [float(x) for x in m]


def mhat_lower(m, t):
    """(1): the lower end in arb of mhat(t) = 1 + m1 t + m2 t^2 + m3 t^3 from exact binary64 m (exact in arb). mhat is nondecreasing in t
    (the record's C-MHAT), so at t = 1/300 this is the lower end at J = 300."""
    a = [arb(x) for x in m]
    return (1 + a[0] * t + a[1] * t * t + a[2] * t * t * t).lower()


def check_tp_dom(I, EPSC, MH, MHUP):
    """(1), the review on v1_26 and on the lt0 clause (required before any certified t export): the t path may combine the certified kappa
    with the mock eps_r and s-prime only while (a) the mock eps_r and s-prime lie at or above the M2B ends at both N, and (b) the mock lt0 lies
    at or below (1 - eps_r) mhat_lo. mhat_lo (MH) is the arb lower end of mhat(1/300) from the M2(b) record's own coefficients; it must agree
    with the record's MHAT_UP (MHUP: MH <= MHUP and MHUP - MH <= 1e-12), so the mock mhat key cannot stand in for it. qv4 and tprov are
    monotone in each, so upper ends taken from different eps_r values stay upper ends. Caveat: the bound in (b) holds at
    J = 300 only, where tprov states its fields. If the t values are ever used for every piece, the clause becomes lt0 <= (1 - eps_r)
    (mhat >= 1), or per-piece values, which item (v) brings."""
    for N in (4, 3):
        if not ((MH[N] <= MHUP[N]) and (MHUP[N] - MH[N] <= arb('1e-12'))):
            raise Refused('C-TP-DOM: the mhat used at N=%d is not the M2B record value (MHAT_UP)' % N)
        In, er, sp = I[N], EPSC[N][0], EPSC[N][2]
        if not ((In['eps_r'] >= er) and (In['sp'] >= sp) and (In['lt0'] <= (1 - er) * MH[N])):
            raise Refused('C-TP-DOM: the mock eps_r, s-prime or lt0 at N=%d is not on the safe side of the M2B values' % N)
    return True


def check_m2b_trial(lines, pins=None):
    """(2), the note 2 on v1_26: the M2B record's PIN_TRIAL must name the vacres files the assembly pins, VACRES[N], with their full
    pinned sha256, as code-relative path:sha256 tokens, each exactly once."""
    pins = PINS if pins is None else pins
    pt = [x for x in lines if x.startswith('PIN_TRIAL = ')]
    if len(pt) != 1:
        raise Refused('the M2B record has no single PIN_TRIAL line')
    toks = pt[0][len('PIN_TRIAL = '):].split(' ; ')
    for N in (4, 3):
        want = '%s:%s' % (os.path.relpath(VACRES[N], CODEDIR), pins.get(VACRES[N]) or '')
        if pins.get(VACRES[N]) is None or toks.count(want) != 1:
            raise Refused('the M2B record PIN_TRIAL does not name %s with its pinned sha256' % os.path.basename(VACRES[N]))
    return True


def check_grid_start(P):
    """(3), the note 1 on v1_26: law_v1(300) bounds the pieces only from J = 300, so the first piece of each N must start at
    jlo >= J_MIN = 300."""
    for N in (4, 3):
        if not (float(P[N][0][1]) >= 300):
            raise Refused('the first piece at N=%d starts below J = 300 (jlo %s)' % (N, P[N][0][1]))
    return True


def check_grid_exact(P):
    """v1_32 (2), the grid condition: the pieces tile [300, inf) exactly with binary64 ends: the first jlo is exactly 300, each jhi string
    equals the next jlo, each finite end is a binary64 repr (repr(float(s)) == s), jlo < jhi, and the last jhi is 'inf' (t -> 0)."""
    for N in (4, 3):
        rows = P[N]
        if not rows or rows[0][1] != repr(300.0):
            raise Refused('C-GRID-EXACT N=%d: the first jlo is not exactly 300' % N)
        for i, (_idx, jlo, jhi) in enumerate(rows):
            if repr(float(jlo)) != jlo or (jhi != 'inf' and repr(float(jhi)) != jhi):
                raise Refused('C-GRID-EXACT N=%d piece %d: an end is not a binary64 repr' % (N, i))
            if not (float(jlo) < (float('inf') if jhi == 'inf' else float(jhi))):
                raise Refused('C-GRID-EXACT N=%d piece %d: jlo is not below jhi' % (N, i))
            if i + 1 < len(rows) and jhi != rows[i + 1][1]:
                raise Refused('C-GRID-EXACT N=%d piece %d: jhi %s is not the next jlo %s' % (N, i, jhi, rows[i + 1][1]))
        if rows[-1][2] != 'inf':
            raise Refused('C-GRID-EXACT N=%d: the last jhi is not inf' % N)
    return True


def check_grid_hull(P, tef):
    """v1_33 (1), C-GRID-HULL: on every piece the raw ends of tef hold both readings (decimal and binary64) of both piece ends, by point
    comparison: t_hi at or above the upper end of 1/J for each reading of jlo, t_lo at or below the lower end of 1/J for each reading of
    jhi (t_lo = 0 for 'inf'); refused otherwise."""
    for N in (4, 3):
        for idx, jlo, jhi in P[N]:
            tl, th = tef(jlo, jhi)
            if not all(bool(th >= (arb(1) / q2arb(J)).upper()) for J in (Fraction(jlo), Fraction(float(jlo)))):
                raise Refused('C-GRID-HULL N=%d piece %s: t_hi misses a reading of jlo %s' % (N, idx, jlo))
            if jhi == 'inf':
                if not bool(tl == 0):
                    raise Refused('C-GRID-HULL N=%d piece %s: the last piece does not run to t = 0' % (N, idx))
            elif not all(bool(tl <= (arb(1) / q2arb(J)).lower()) for J in (Fraction(jhi), Fraction(float(jhi)))):
                raise Refused('C-GRID-HULL N=%d piece %s: t_lo misses a reading of jhi %s' % (N, idx, jhi))
    return True


def check_tau_trial(pins):
    """v1_34 (Point 2): H2 as a machine gate (the review 5c8dd2f3 Point 2). The sweep's run output (S67[1]) names its script on line 1 by full sha256;
    that script (S67_SCRIPT, pinned) holds TRIAL_SET with the four full sha256s, which must equal this file's pinned ts and vacres files
    (basename and full sha256, per N). The output's C-TRIAL line must name the same files with the same sha8 prefixes and read PASS, and its
    C-TRIAL chain line must read PASS. Returns True or raises Refused('C-TAU-TRIAL: ...')."""
    if pins.get(S67_SCRIPT) is None or sha_file(S67_SCRIPT) != pins[S67_SCRIPT]:
        raise Refused('C-TAU-TRIAL: the S67 producer script does not match its pin')
    L = lines_of(S67[1])
    m = re.match(r'kt_s9h_v1_2 sha256 ([0-9a-f]{64}) ', L[0]) if L else None
    if m is None or m.group(1) != pins[S67_SCRIPT]:
        raise Refused('C-TAU-TRIAL: the run output line 1 does not name the pinned script by its full sha256')
    src = lines_of(S67_SCRIPT)
    k = [i for i, x in enumerate(src) if x.startswith('TRIAL_SET = {')]
    if len(k) != 1:
        raise Refused('C-TAU-TRIAL: TRIAL_SET is not defined exactly once in the producer script')
    block = ' '.join(src[k[0]:k[0] + 4])
    got = re.findall(r"(\d): dict\(ts=\('pk11/out/([^']+)', '([0-9a-f]{64})'\),\s*vacres=\('pk11/out/([^']+)', '([0-9a-f]{64})'\)\)", block)
    want = dict((N, (os.path.basename(TS_FILES[N]), pins.get(TS_FILES[N]), os.path.basename(VACRES[N]), pins.get(VACRES[N]))) for N in (4, 3))
    if sorted(int(g[0]) for g in got) != [3, 4] or any(tuple(g[1:]) != want[int(g[0])] for g in got):
        raise Refused('C-TAU-TRIAL: kt_s9h TRIAL_SET differs from the pinned ts and vacres files')
    ct = [x for x in L if x.startswith('C-TRIAL: ')]
    toks = re.findall(r'(ts_N\d\S*?\.json|vacres_K3_N\d_sym_v1\.json):([0-9a-f]{8})', ct[0]) if len(ct) == 1 else []
    exp = [(want[4][0], (want[4][1] or '')[:8]), (want[4][2], (want[4][3] or '')[:8]), (want[3][0], (want[3][1] or '')[:8]), (want[3][2], (want[3][3] or '')[:8])]
    if len(ct) != 1 or toks != exp or ' -> PASS;' not in ct[0]:
        raise Refused('C-TAU-TRIAL: the run output C-TRIAL line does not name the pinned trial set with PASS')
    ch = [x for x in L if x.startswith('C-TRIAL chain ')]
    if len(ch) != 1 or "the script's INPUTS pin the four TRIAL_SET files by the same full sha256 -> PASS" not in ch[0]:
        raise Refused('C-TAU-TRIAL: the run output C-TRIAL chain line is missing or not PASS')
    return True


def load_tau(P, pins=None, plant=None):
    """v1_33 (3): the crude tau per piece, rho_hi = L_1^odd/lambda_0,lo (S units, rounded up), from pk07's certified vertical sweep
    EXPORT_KT_S67_v1 through its sha-pinned reader kt_s67_export_reader_v2_1.load (rule V2 binding to the sweep's VALID run output; EXPORT_STATUS
    CERTIFIED, RUN_VERDICT VALID). The pieces must be this grid's, index for index, with the same doubles. Returns {N: {idx: Fraction}}."""
    pins = PINS if pins is None else pins
    for p in (S67[0], S67[1], S67_READER_PATH):
        if pins.get(p) is None or sha_file(p) != pins[p]:
            raise Refused('S67 file %s does not match its pin' % os.path.basename(p))
    check_tau_trial(pins)   # v1_34 (Point 2)
    import importlib.util
    spec = importlib.util.spec_from_file_location('kt_s67_export_reader_v2_1', S67_READER_PATH)
    mod = importlib.util.module_from_spec(spec)
    p0 = ctx.prec
    spec.loader.exec_module(mod)
    ctx.prec = p0
    try:
        ex = mod.load(S67[0], S67[1])
    except Exception as e:
        raise Refused('kt_s67_export_reader_v2_1.load: %s' % e)
    if 'rho_hi' not in ex['fields']:
        raise Refused('the S67 export carries no rho_hi field')
    if plant == 'SWAPN':   # v1_34 (C-TAU-N): PLANT-TAU-N's hook, the reader's N4 and N3 rows swapped
        ex['pieces'] = {4: ex['pieces'].get(3, {}), 3: ex['pieces'].get(4, {})}
    fi = ex['fields'].index('rho_hi')
    lab = {}   # v1_34 (C-TAU-N): the export's own N<N>_P<idx> labels, read here beside the reader
    for x in lines_of(S67[0]):
        mm = re.match(r'N([34])_P([0-9]{4}) = (.*)$', x)
        if mm:
            lab[(int(mm.group(1)), int(mm.group(2)))] = mm.group(3).partition(' | ')[0].split(' ')
    out_t = {}
    for N in (4, 3):
        pcs = ex['pieces'].get(N, {})
        if len(pcs) != len(P[N]):
            raise Refused('the S67 export has %d pieces at N=%d, the grid %d' % (len(pcs), N, len(P[N])))
        out_t[N] = {}
        for i, (idx, jlo, jhi) in enumerate(P[N]):
            e = pcs[i]
            if e['jlo'] != float(jlo) or e['jhi'] != (math.inf if jhi == 'inf' else float(jhi)):
                raise Refused('the S67 export grid differs at N=%d piece %s' % (N, idx))
            r = Fraction(e['rho_hi'])
            tk = lab.get((N, i))
            if tk is None or len(tk) <= fi or Fraction(tk[fi]) != r:
                raise Refused('C-TAU-N: the tau row for N=%d piece %s is not the export line N%d_P%04d' % (N, idx, N, i))
            if not (r > 0):
                raise Refused('the S67 rho_hi at N=%d piece %s is not positive' % (N, idx))
            out_t[N][idx] = r
    return out_t


def t_uniformity(sources):
    """(5): the t export carries J_UNIF_PP only when every M4 input of the t path (sources: input name -> status) is a pinned certified record,
    else J_UNIF_T_ASSUMED."""
    return J_UNIF_PP if (sources and all(v == 'CERTIFIED' for v in sources.values())) else J_UNIF_T_ASSUMED


def check_t_uniformity(value, sources):
    """(5): refuses J_UNIF_PP on a t export while any M4 input of the t path is not certified."""
    if value == J_UNIF_PP and not (sources and all(v == 'CERTIFIED' for v in sources.values())):
        raise Refused('J_UNIFORMITY PER-PIECE on a t export whose M4 inputs are not all certified')
    return True


# ---- item (v): the per-piece Ritz and Lemma A data (v1_27 (1), NOTE_P2_17_RITZ_PIECES_v1)
def load_ritz_mock(L, N):
    """v1_27 (1): MOCK_RITZ_ENTRIES_v1 lines L at N as {key: (coefficient balls, bar)}; strict KV with the MOCK FORMAT, TAG and CLAIM; exactly
    the 18 S9 keys."""
    d = read_kv(L, 'MOCK', 'MOCK_RITZ_ENTRIES_v1')
    E = {}
    for k, v in d.items():
        m = re.match(r'^N%d_(G|T)_([013])_([013])$' % N, k)
        n = re.match(r'^N%d_(IHT|DX)_([013])$' % N, k)
        if m:
            name = '%s,%s,%s' % m.groups()
        elif n:
            name = '%s,%s' % ({'IHT': 'Iht', 'DX': 'Dx'}[n.group(1)], n.group(2))
        else:
            continue
        f = v.split()
        K = int(f[0])
        if K < 3 or len(f) != K + 3:
            raise Refused('mock Ritz entry %s layout' % k)
        E[name] = ([arb(x) for x in f[1:K + 2]], arb(f[K + 2]).upper())
    if d.get('N%d_ENTRIES' % N) != '18' or sorted(E) != sorted(RITZ_KEYS):
        raise Refused('mock Ritz entries at N=%d are not the 18 S9 keys' % N)
    return E


def check_s9_trial(r9, N, pins=None):
    """v1_27 (1): an S9 record's trial_set must name the pinned ts and vacres files in pk03's form basename:<full sha256>."""
    pins = PINS if pins is None else pins
    ts = r9.get('trial_set') if isinstance(r9, dict) else None
    for k, p in (('ts', TS_FILES[N]), ('vacres', VACRES[N])):
        want = '%s:%s' % (os.path.basename(p), pins.get(p) or '')
        if pins.get(p) is None or not isinstance(ts, dict) or ts.get(k) != want:
            raise Refused('S9 record trial_set %s is not the pinned %s' % (k, os.path.basename(p)))
    return True


def load_ritz(N, mode, path=None, asm_out=None, pins=None):
    """v1_27 (1): the 18 S9 entries of N as {key: (coefficient balls a_0..a_K, bar)} over t in [0, 1/300] (J_REF 300). CERTIFIED: pk03's
    S9 record and its asm output, both pinned by full sha256 (S9_RECORDS), through m3_reader_v4_4 (load_m3), then check_s9_trial; a KV file
    (a MOCK copy) is refused at read_kv's CERTIFIED FORMAT/TAG check before any value is read; refused while no S9 record is pinned.
    MOCK: MOCK_RITZ_ENTRIES_v1."""
    pins = PINS if pins is None else pins
    if mode == 'CERTIFIED':
        if path is None:
            if N not in S9_RECORDS:
                raise Refused('no S9 record pinned for N=%d yet' % N)
            path, asm_out = S9_RECORDS[N]
        for p in (path, asm_out):
            if p is None or pins.get(p) is None or sha_file(p) != pins[p]:
                raise Refused('S9 file %s does not match its pin' % os.path.basename(str(p)))
        if not path.endswith('.json'):
            read_kv(lines_of(path), 'CERTIFIED', 'S9_RECORD')
            raise Refused('an S9 record is an M3 json record')
        E = load_m3(path, N, 'CERTIFIED', 300, asm_out)
        with open(path) as fh:
            check_s9_trial(json.load(fh), N, pins)
    elif mode == 'MOCK':
        E = load_ritz_mock(lines_of(M_RITZ if path is None else path), N)
    else:
        raise ValueError(mode)
    miss = [k for k in RITZ_KEYS if k not in E]
    if miss:
        raise Refused('S9 entries missing at N=%d: %s' % (N, ' '.join(miss)))
    extra = sorted(k for k in E if k not in RITZ_KEYS)   # v1_30 (1), the review 4: the S9 record holds exactly the 18 keys
    if extra:
        raise Refused('S9 entries beyond the 18 keys at N=%d: %s' % (N, ' '.join(extra)))
    return dict((k, E[k]) for k in RITZ_KEYS)


def entry_piece(e, tb):
    """v1_27 (1): an entry over the piece: sum_k a_k t^k on the piece's t-ball tb plus the constant bar (the direct form, NOTE sect. 4)."""
    ak, err = e
    s = arb(0)
    for a in reversed(ak):
        s = s * tb + a
    return s + err * arb(0, 1)


def mhat_ball(m, tb):
    """v1_27 (1): mhat(t) = 1 + m1 t + m2 t^2 + m3 t^3 on the piece's t-ball tb, from exact binary64 m (the M2(b) record's m1..m3)."""
    a = [arb(x) for x in m]
    return 1 + a[0] * tb + a[1] * tb * tb + a[2] * tb * tb * tb


def _min_pt(a, b):
    return a if a < b else b


def _jacobi3(A):
    """v1_27 (1): float Jacobi on a symmetric 3 x 3 list matrix: eigenvalue and eigenvector guesses only (kt_rb_v1_5's jacobi in binary64)."""
    n = 3
    A = [row[:] for row in A]
    V = [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]
    for _ in range(100):
        if sum(A[i][j] ** 2 for i in range(n) for j in range(n) if i != j) < 1e-30:
            break
        for p in range(n - 1):
            for q in range(p + 1, n):
                if A[p][q] == 0:
                    continue
                th = (A[q][q] - A[p][p]) / (2 * A[p][q])
                tt = (1 if th >= 0 else -1) / (abs(th) + math.sqrt(th * th + 1))
                c = 1 / math.sqrt(tt * tt + 1)
                s = tt * c
                for k in range(n):
                    x, y = A[k][p], A[k][q]
                    A[k][p], A[k][q] = c * x - s * y, s * x + c * y
                for k in range(n):
                    x, y = A[p][k], A[q][k]
                    A[p][k], A[q][k] = c * x - s * y, s * x + c * y
                for k in range(n):
                    x, y = V[k][p], V[k][q]
                    V[k][p], V[k][q] = c * x - s * y, s * x + c * y
    return [A[i][i] for i in range(n)], V


def ritz_piece(B, mh, vecmode='PD'):
    """v1_27 (1): kt_rb_v1_5's ritz_cert (l.567-675) in arb on one piece's entry balls B (NOTE_P2_17_RITZ_PIECES_v1 sect. 4): interval Cholesky
    of the 3 x 3 Gram block (refused unless certainly positive definite), X = L^-1, C = X T X^T symmetrized by averaging (both enclose the true
    value), float Jacobi guesses on C's midpoint, residuals in arb, Weyl with rF = ||C - mid C||_F, disjoint enclosures, Davis-Kahan vector
    bars (the angle at most pi/2 times its sine), c_k = X^T v_k with c_k[k] > 0, and the amplitude balls t^_k = mhat (c_k . Iht)/(G00^(1/2)
    lambda_0^2) and a^_k = mhat (c_k . Dx)/(G00^(1/2) lambda_0) (Iht, the top-row bond, in place of kt_rb's Ih). C-GAP refusals: overlapping
    enclosures, no gap, an undetermined vector sign."""
    n = 3
    G = [[B['G,%d,%d' % (min(b, c), max(b, c))] for c in REVEN] for b in REVEN]
    T = [[B['T,%d,%d' % (min(b, c), max(b, c))] for c in REVEN] for b in REVEN]
    Iht = [B['Iht,%d' % b] for b in REVEN]
    Dx = [B['Dx,%d' % b] for b in REVEN]
    L = [[arb(0) for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(i + 1):
            s = G[i][j]
            for k in range(j):
                s = s - L[i][k] * L[j][k]
            if i == j:
                if not (s > 0):
                    raise Refused('interval Gram block not positive definite')
                L[i][i] = s.sqrt()
            else:
                L[i][j] = s / L[j][j]
    X = [[arb(0) for _ in range(n)] for _ in range(n)]
    for i in range(n):
        X[i][i] = 1 / L[i][i]
        for j in range(i):
            s = arb(0)
            for k in range(j, i):
                s = s + L[i][k] * X[k][j]
            X[i][j] = -s / L[i][i]
    XT = [[sum((X[i][k] * T[k][j] for k in range(n)), arb(0)) for j in range(n)] for i in range(n)]
    C = [[sum((XT[i][k] * X[j][k] for k in range(n)), arb(0)) for j in range(n)] for i in range(n)]
    for i in range(n):
        for j in range(i):
            C[i][j] = C[j][i] = (C[i][j] + C[j][i]) / 2
    Cm = [[float(C[i][j].mid()) for j in range(n)] for i in range(n)]
    rf2 = arb(0)
    for i in range(n):
        for j in range(n):
            d = abs(C[i][j] - arb(Cm[i][j])).upper()
            rf2 = rf2 + d * d
    rF = rf2.sqrt().upper()
    lam, Q = _jacobi3(Cm)
    order = sorted(range(n), key=lambda k: -lam[k])
    lamo, res, vec = [], [], []
    for k in order:
        v = [Q[i][k] for i in range(n)]
        r2, nv2 = arb(0), arb(0)
        for i in range(n):
            ri = sum((arb(Cm[i][j]) * arb(v[j]) for j in range(n)), arb(0)) - arb(lam[k]) * arb(v[i])
            r2 = r2 + abs(ri).upper() * abs(ri).upper()   # v1_30 (2): the upper end of |r_ki| squared
            nv2 = nv2 + arb(v[i]) * arb(v[i])
        lamo.append(lam[k])
        res.append((r2.sqrt() / nv2.sqrt()).upper())
        vec.append(v)
    one = arb(0, 1)
    encl = [arb(lamo[k]) + one * (res[k] + rF) for k in range(n)]
    cme = [arb(lamo[k]) + one * res[k] for k in range(n)]
    for k in range(n - 1):
        if not ((cme[k].lower() > cme[k + 1].upper()) and (encl[k].lower() > encl[k + 1].upper())):
            raise Refused('eigenvalue enclosures overlap (C-GAP)')
    vecs, dmin = [], None
    for k in range(n):
        g = None
        for j in range(n):
            if j != k:
                x = (abs(arb(lamo[k]) - arb(lamo[j])) - res[k] - res[j]).lower()
                g = x if g is None else _min_pt(g, x)
        d = (g - rF).lower()
        dmin = d if dmin is None else _min_pt(dmin, d)
        if not ((g > 0) and (d > 0)):
            raise Refused('no eigenvalue gap (C-GAP)')
        eps = (arb.pi() / 2 * (res[k] / g + rF / d)).upper()
        vecs.append([arb(x) + one * eps for x in vec[k]])
    if vecmode == 'PD':   # v1_28 (1): the per-direction bound (NOTE_P2_17_RITZ_PD_v1) in place of the uniform bar above
        vecs = pd_dk_meet(pd_vectors(C, vec, lamo, res, rF), vecs)   # v1_30 (3): the smaller of PD and DK per component
    elif vecmode != 'DK':
        raise ValueError(vecmode)
    cvecs = []
    for rank in range(n):
        vk = vecs[rank]
        c = [sum((X[j][i] * vk[j] for j in range(n)), arb(0)) for i in range(n)]
        if c[rank].upper() < 0:
            c = [-x for x in c]
        elif not (c[rank].lower() > 0):
            raise Refused('sign of a Ritz vector not determined (C-GAP)')
        cvecs.append(c)
    l0 = encl[0]
    sg0 = G[0][0].sqrt()

    def amp(c, w, p):
        s = sum((c[i] * w[i] for i in range(n)), arb(0))
        den = sg0
        for _ in range(p):
            den = den * l0
        return mh * s / den
    return dict(vals=encl, vecs=cvecs, C=C, vec=vec, lamo=lamo, t=[amp(cvecs[k], Iht, 2) for k in range(n)], a=[amp(cvecs[k], Dx, 1) for k in range(n)],
                rF=rF, res=res, dmin=dmin, G=G, Iht0=Iht[0], Dx0=Dx[0])


def lemma_a_cbar(RC, eps_r, Rb12, tau_r, tau_abs=None, plant=None):
    """v1_27 (1): kt_rb_v1_5's assembly_cert l.711-746 in arb on one piece: c-bar from the residual ratios Rb = (eps_r/(1 - eps_r), R_e1, R_e3),
    Weyl on the block form of S and Kato-Temple at the top (refused unless both denominators are positive: C-KT; and C-SX), then
    q = c-bar/(s_x,low - tau), eps_0 and eps_y. tau = TAU_R mu_y,high when tau_abs is None (kt_rb's form, C-LA300 only), else tau = tau_abs =
    rho_hi (the port's rows, v1_33 (3)). v1_34: eps_y = rho_y q/(s_x,low - mu_y,high) ((a)); C-KT0 gates m0lo's denominator (); plant='KT0'
    is PLANT-KT0's hook (s_x,high replaced by 1 - 1.5 c-bar in that denominator only)."""
    vals, G, V = RC['vals'], RC['G'], RC['vecs']
    s_x, mu_y = vals[1] / vals[0], vals[2] / vals[0]
    tau = arb(tau_r) * mu_y.upper() if tau_abs is None else tau_abs   # v1_33 (3): the crude certified tau (rho_hi) on the port's rows
    Rb = [eps_r / (1 - eps_r), Rb12[0], Rb12[1]]
    rho = []
    for k in range(3):
        acc = arb(0)
        for b in range(3):
            acc = acc + abs(V[k][b]).upper() * G[b][b].sqrt().upper() * Rb[b]
        rho.append(acc)
    cbar = (rho[0] * rho[0] + rho[1] * rho[1] + rho[2] * rho[2]).sqrt()
    ylev = mu_y.upper() if (tau_abs is None or mu_y.upper() > tau.upper()) else tau.upper()   # v1_33 (3): max(mu_y, tau), no r_tau < 1
    syhi = ylev + cbar
    gap_x = _min_pt((1 - s_x.upper()).lower(), (s_x.lower() - syhi).lower())
    if not (gap_x > 0):
        raise Refused('C-KT: no gap around s_x')
    s_xlo = (s_x.lower() - cbar * cbar / gap_x).lower()
    kt0 = 1 - cbar - ((s_x.upper() if plant != 'KT0' else 1 - 3 * cbar / 2) + cbar)   # v1_34: m0lo's denominator, the same arb expression
    if not (kt0 > 0):
        raise Refused('C-KT0: 1 - 2 c-bar - s_x,high (the m0lo denominator) is not certainly positive')
    m0lo = 1 - rho[0] * rho[0] / kt0
    sx_mm = s_x.lower() * m0lo
    g_below = s_xlo - syhi
    if not (g_below > 0):
        raise Refused('C-KT: s_x,low - s_y,high not positive')
    sxhi = s_x.upper() + cbar * cbar / g_below
    den0 = m0lo - sxhi
    if not (den0 > 0):
        raise Refused('C-KT: Kato-Temple denominator not positive')
    if not (s_xlo.upper() <= sx_mm.lower()):
        raise Refused('C-SX: s_x,low above the min-max bound')
    q = cbar / (s_xlo - tau)
    return dict(s_x=s_x, mu_y=mu_y, tau=tau, rho=rho, cbar=cbar, s_xlo=s_xlo, syhi=syhi, sxhi=sxhi, den0=den0, kt0=kt0, m0lo=m0lo, g_below=g_below, q=q, eps0=rho[0] * q / den0,
                epsy=rho[2] * q / (s_xlo - mu_y.upper()))   # v1_34 (a): eps_y's gap s_x,low - mu_y,high (NOTE_TAU_CRUDE_v1 L10, H5)


def lemma_a_amp(RC, LA, eps_r, s, mh, NAp, HbP, GbP, AbP, Aa_hi):
    """v1_27 (1): kt_rb_v1_5's assembly_cert l.747-792 in arb on one piece, at the levels (LAM_T, LAM_A), with Iht in place of Ih (the t side),
    Lemma B's NA-prime in place of BETA_R mhat/lambda~0, and Lemma G's Hbad-prime, Gbad-prime, Abad-prime: sigma_k (C-SIGN0), the vacuum
    values |t_00| and |a_00|, the corrections Delta, the amplitude balls t~_x = t^_x + [-Delta_x, Delta_x], t~_y, a~_x, and da_x (with A_am at
    J = 300). dt_x is tprov's (it needs A_t). Returns tprov's inputs for the piece plus av0 (the vacuum bar |a^_00|) for C-NA."""
    vals, G, V = RC['vals'], RC['G'], RC['vecs']
    if not (mh > 0):   # v1_35 (4): C-MHAT, where lt0 is formed
        raise Refused('C-MHAT: mhat is not certainly positive')
    lt0 = (1 - eps_r) * mh
    sp = s * (1 + s)
    if not ((mh - vals[1].upper()) > 0):   # v1_34 (grep): C-DK0, sigma_0's Davis-Kahan denominator
        raise Refused('C-DK0: mhat - mu_x,high is not certainly positive')
    sig0 = eps_r * mh / (mh - vals[1].upper())
    ip = []
    for k in range(3):
        acc = arb(0)
        for b in range(3):
            acc = acc + G[0][b] * V[k][b]
        ip.append(acc / G[0][0].sqrt())
    if not (ip[0] > 0):
        raise Refused('C-SIGN0: <u~_0, u-hat> not certainly positive')
    s0 = sig0.upper()
    sgk = [None, _min_pt(s0, abs(ip[1]).upper()), _min_pt(s0, abs(ip[2]).upper())]
    d0 = sig0 * (1 + sig0) + sp
    tv0 = abs(mh * RC['Iht0'] / (G[0][0] * vals[0] * vals[0])).upper()
    av0 = abs(mh * RC['Dx0'] / (G[0][0] * vals[0])).upper()
    axb, ayb = abs(RC['a'][1]).upper(), abs(RC['a'][2]).upper()
    Lam, Lam_a = arb(LAM_T), arb(LAM_A)
    NH = Lam + HbP
    GP = Lam * (mh / lt0) * eps_r + GbP
    GA = Lam_a * (mh / lt0) * eps_r + AbP
    t00 = tv0 + 2 * NH * sp + GP
    dlx = NH * sp + (sp + sgk[1]) * t00 + GP
    dly = NH * sp + (sp + sgk[2]) * t00 + GP
    a00 = av0 + 2 * NAp * sp + GA
    dlax = NAp * sp + (sp + sgk[1]) * a00 + GA
    dlay = NAp * sp + (sp + sgk[2]) * a00 + GA
    q, eps0, epsy = LA['q'], LA['eps0'], LA['epsy']
    Qva = (mh / lt0) * Aa_hi + Lam_a * (mh / lt0) * eps_r + (NAp + a00) * sp + AbP
    dax = q * Qva + eps0 * (d0 * NAp) + epsy * (ayb + dlay) + (q * q + eps0 * eps0 + epsy * epsy) * (axb + dlax)
    one = arb(0, 1)
    Gr = arb_mat(3, 3, [sum((V[k][i] * G[i][j] * V[l][j] for i in range(3) for j in range(3)), arb(0)) for k in range(3) for l in range(3)])
    return dict(mhat=mh, lt0=lt0, eps_r=eps_r, sp=sp, Lam=Lam, Hbad=HbP, HbadP=HbP, Gbad=GbP, GbadP=GbP, Lam_a=Lam_a, Abad=AbP, AbadP=AbP, q=q,
                eps0=eps0, epsy=epsy,
                t0=t00, t0t=d0 * NH, tx=RC['t'][1] + one * dlx.upper(), ty=RC['t'][2] + one * dly.upper(), ax=RC['a'][1] + one * dlax.upper(), dax=dax, G=Gr,
                av0=av0, a00=a00)


def na_prime(kap):
    """v1_27 (1), Lemma B (a) (NOTE_P2_17_BETA_v1): ||T_xi_TM||/lambda_0 <= L + L e^(-L) kappa for every L >= 1, so
    NA-prime is the minimum over the grid L = 1, 9/8, ..., 20 at kappa = kappa_max, J-uniform for J >= 300 (any L >= 1 is valid, so the grid
    needs no certification). Returns (NA-prime as an upper end, its L)."""
    best = None
    for k in range(8, 161):
        L = arb(k) / 8
        v = (L + L * (-L).exp() * kap).upper()
        if best is None or v < best[0]:
            best = (v, L)
    return best


def na_value(kind, N, kap=None, mh=None, lt0=None):
    """v1_27 (1): NA for Lemma A with its FLOAT_IN tokens. LEMMA_B: (NA-prime, []). FLOAT_LITERAL: kt_rb's BETA_R mhat/lambda~0 with the token
    beta_r, which certified_tag refuses (PLANT-NA)."""
    if kind == 'LEMMA_B':
        return na_prime(kap)[0], []
    if kind == 'FLOAT_LITERAL':
        return arb(BETA_R_FLOAT[N]) * mh / lt0, ['beta_r']
    raise ValueError(kind)


_NUM = r'([-+0-9.eE]+)'
_PT = r'\[' + _NUM + r', [-+0-9.eE]+\]'


def rb_ref(N, pins=None):
    """v1_27 (1): kt_rb_v1_5's CERT300 lines at N (pinned RBOUT[N], old trial set): the Ritz enclosures (lambda_0, s_x, mu_y), the bars |a^_k|
    and the CBAR constants (rho, c-bar, q, eps_0, eps_y) for C-RITZ300 and C-LA300, and its FLOAT inputs: eps_r and s (QV line) and R_e1, R_e3
    (C-IN lines, rounded up 1e-6 by kt_rb). Values are the printed strings."""
    pins = PINS if pins is None else pins
    p = RBOUT[N]
    if pins.get(p) is None or sha_file(p) != pins[p]:
        raise Refused('kt_rb output %s does not match its pin' % os.path.basename(p))
    L = lines_of(p)

    def one(pre):
        x = [ln for ln in L if ln.startswith(pre)]
        if len(x) != 1:
            raise Refused('kt_rb line %r is not there exactly once' % pre)
        return x[0]
    r = {}
    ritz = one('CERT300 RITZ N=%d J=300: ' % N)
    for nm in ('lambda_0', 's_x', 'mu_y'):
        m = re.search(re.escape(nm) + r' in \[' + _PT + r', ' + _PT + r'\]', ritz)
        if m is None:
            raise Refused('kt_rb RITZ line: no %s' % nm)
        r[nm] = (m.group(1), m.group(2))
    amp = one('CERT300 AMP N=%d J=300: ' % N).split('|a^| <= ', 1)
    ab = re.findall(_PT, amp[1]) if len(amp) == 2 else []
    if len(ab) < 3:
        raise Refused('kt_rb AMP line: no |a^| bars')
    r['abar'] = ab[:3]
    m = re.search(r'rho ' + _PT + ' ' + _PT + ' ' + _PT + r'; c-bar <= ' + _PT + r'; q <= ' + _PT + r'; eps_0 <= ' + _PT + r', eps_y <= ' + _PT,
                  one('CERT300 CBAR N=%d J=300: ' % N))
    if m is None:
        raise Refused('kt_rb CBAR line does not parse')
    r['rho'] = [m.group(1), m.group(2), m.group(3)]
    r['cbar'], r['q'], r['eps0'], r['epsy'] = m.group(4), m.group(5), m.group(6), m.group(7)
    m = re.search(r'FLOAT inputs eps_r ' + _NUM + ', s ' + _NUM + r'\s*$', one('CERT300 QV N=%d J=300: ' % N))
    if m is None:
        raise Refused('kt_rb QV line: no FLOAT inputs')
    r['eps_r'], r['s'] = m.group(1), m.group(2)
    for k in ('e1', 'e3'):
        m = re.search(r'\(used ' + _NUM + r'\)\s*$', one('C-IN N=%d %s: ' % (N, k)))
        if m is None:
            raise Refused('kt_rb C-IN %s: no used value' % k)
        r[k] = m.group(1)
    return r


def check_ritz300(RC, rf, s9=False):
    """v1_27 (1), C-RITZ300: on the first piece the eigenvalue enclosures hold kt_rb's CERT300 midpoints of lambda_0, s_x and mu_y, and each
    |a^_k| ball holds kt_rb's bar (both from kt_s9b_v2's entries; mock run). v1_31 (1), s9=True (the S9 records): every leg compares
    two enclosures built from different entries, which must meet: each enclosure meets kt_rb's [lo, hi], and each |a^_k| ball's lower end is
    at most kt_rb's bar; containment and the upper leg are INFO (ritz300_info)."""
    l0 = RC['vals'][0]
    for nm, x in (('lambda_0', l0), ('s_x', RC['vals'][1] / l0), ('mu_y', RC['vals'][2] / l0)):
        lo, hi = rf[nm]
        if not (x.overlaps(arb(lo).union(arb(hi))) if s9 else x.contains((arb(lo) + arb(hi)) / 2)):
            raise Refused('C-RITZ300: %s does not %s' % (nm, 'meet the kt_rb CERT300 interval' if s9 else 'hold the kt_rb CERT300 midpoint'))
    for k in range(3):
        aa, r = abs(RC['a'][k]), arb(rf['abar'][k])
        if not ((aa.lower() <= r) and (s9 or (r <= aa.upper() + arb('1e-9')))):   # v1_31 (1): the lower leg alone on the S9 records
            raise Refused('C-RITZ300: |a^_%d| does not hold the kt_rb bar%s' % (k, ' (lower leg)' if s9 else ''))
    return True


def ritz300_info(RC, rf):
    """v1_31 (1): the INFO parts of C-RITZ300: whether each enclosure holds kt_rb's midpoint, and kt_rb's bar minus each |a^_k| upper end."""
    l0 = RC['vals'][0]
    cont = ' '.join('%s %s' % (nm, 'holds' if x.contains((arb(rf[nm][0]) + arb(rf[nm][1])) / 2) else 'misses')
                    for nm, x in (('lambda_0', l0), ('s_x', RC['vals'][1] / l0), ('mu_y', RC['vals'][2] / l0)))
    up = ' '.join((arb(rf['abar'][k]) - abs(RC['a'][k]).upper()).str(3) for k in range(3))
    return 'the kt_rb midpoint: %s; kt_rb bar minus the |a^_k| upper end: %s' % (cont, up)


def tp_vals(X):
    """v1_27 (1): the ten t export fields of one row from tprov's dict, as directed decimals."""
    return (dec_lo(X['At']), dec_hi(X['Vt']), dec_hi(X['Ot']), dec_hi(X['Pt2'].upper().sqrt()), dec_lo(X['Xta']), dec_lo(X['Xtb']),
            dec_lo(X['Aa']), dec_hi(X['dtx']), dec_hi(X['Q']), dec_hi(X['tz']))


def lo_min(xs):
    """v1_27 (1): the smallest lower end of the balls xs, as a point ball."""
    m = None
    for x in xs:
        m = x.lower() if m is None else _min_pt(m, x.lower())
    return m


def hi_max(xs):
    """v1_27 (1): the largest upper end of the balls xs, as a point ball."""
    m = None
    for x in xs:
        v = x.upper()
        m = v if (m is None or v > m) else m
    return m


def pd_vectors(C, vec, lamo, res, rF, gap_scale=1):
    """v1_28 (1), NOTE_P2_17_RITZ_PD_v1: the per-direction Ritz vectors. For every symmetric A in the ball C and its unit eigenvectors v_k (sign
    u_k . v_k > 0): (lambda_k - lam~_j) u_j . v_k = r_j . v_k with r_j = A u_j - lam~_j u_j, so |u_j . v_k| <= R_j/g_kj for j != k, where R_j is
    the arb upper end of ||C u_j - lam~_j u_j|| (it bounds ||r_j(A)|| over the ball) and g_kj = |lam~_k - lam~_j| - res_k - rF bounds
    |lambda_k(A) - lam~_j| from below (Weyl plus the disjoint residual intervals; refused unless positive). With M = U^T U, beta = U^T v_k,
    beta^T M^-1 beta = 1 gives u_k . v_k. Returns the v_k as arb vectors in C's basis, in the order of lamo. gap_scale (PLANT-PD-GAP only)
    multiplies the gap bounds."""
    n = 3
    one = arb(0, 1)
    U = [[arb(x) for x in vec[j]] for j in range(n)]
    R = []
    for j in range(n):
        rr = arb(0)
        for i in range(n):
            ri = abs(sum((C[i][l] * U[j][l] for l in range(n)), arb(0)) - arb(lamo[j]) * U[j][i]).upper()   # v1_29: the upper end of |r_ji|
            rr = rr + ri * ri
        R.append(rr.sqrt().upper())
    Mi = arb_mat(n, n, [sum((U[i][l] * U[j][l] for l in range(n)), arb(0)) for i in range(n) for j in range(n)]).inv()
    vk_all = []
    for k in range(n):
        beta = [None] * n
        for j in range(n):
            if j != k:
                g = ((abs(arb(lamo[k]) - arb(lamo[j])) - res[k] - rF) * gap_scale).lower()
                if not (g > 0):
                    raise Refused('per-direction bound: no gap between lambda_%d and lam~_%d' % (k, j))
                beta[j] = one * (R[j] / g).upper()
        bk = one * sum((U[k][l] * U[k][l] for l in range(n)), arb(0)).sqrt().upper()
        cross = arb(0)
        for i in range(n):
            for j in range(n):
                if (i, j) != (k, k):
                    cross = cross + (bk if i == k else beta[i]) * Mi[i, j] * (bk if j == k else beta[j])
        qk = (1 - cross) / Mi[k, k]
        if not (qk > 0):
            raise Refused('per-direction bound: the u_%d component is not certainly positive' % k)
        beta[k] = qk.sqrt()
        alpha = [sum((Mi[i, j] * beta[j] for j in range(n)), arb(0)) for i in range(n)]
        vk_all.append([sum((alpha[j] * U[j][i] for j in range(n)), arb(0)) for i in range(n)])
    return vk_all


def check_pd_dk(RCp, RCd):
    """v1_28 (1), C-PD-DK: the per-direction and the uniform Davis-Kahan Ritz coefficient vectors c_k of one piece overlap componentwise (both
    hold the exact c_k with the sign c_k[k] > 0)."""
    for k in range(3):
        for i in range(3):
            a, b = RCp['vecs'][k][i], RCd['vecs'][k][i]
            if not ((a.lower() <= b.upper()) and (b.lower() <= a.upper())):
                raise Refused('C-PD-DK: c_%d[%d] of the two bounds do not overlap' % (k, i))
    return True


def pd_dk_meet(pd, dk):
    """v1_30 (3), the per-direction condition 3: the componentwise intersection of the per-direction and the uniform Davis-Kahan Ritz
    vectors, both of which hold v_k with u_k . v_k > 0; an empty intersection is refused."""
    out_v = []
    for k in range(3):
        row = []
        for i in range(3):
            a, b = pd[k][i], dk[k][i]
            lo = a.lower() if a.lower() > b.lower() else b.lower()
            hi = a.upper() if a.upper() < b.upper() else b.upper()
            if not (lo <= hi):
                raise Refused('the PD and DK bounds of v_%d[%d] do not meet' % (k, i))
            row.append(lo.union(hi))
        out_v.append(row)
    return out_v


def pd_control(diag, rad):
    """v1_30 (3), the control: the PD and DK vectors of the ball diag(d_0, d_1, d_2) +- rad on every entry (symmetric). Its midpoint's
    eigenpairs are exact (res = 0, e_k), so C-PD-CONTROL checks that both bounds contain e_k and that the PD bar is at most the DK bar; a repeated
    d gives no gap and is refused (PLANT-PD-ZEROGAP). Returns (PD vectors, DK vectors)."""
    n = 3
    one = arb(0, 1)
    C = [[arb(diag[i] if i == j else 0) + one * arb(rad) for j in range(n)] for i in range(n)]
    Cm = [[float(diag[i]) if i == j else 0.0 for j in range(n)] for i in range(n)]
    rf2 = arb(0)
    for i in range(n):
        for j in range(n):
            d = abs(C[i][j] - arb(Cm[i][j])).upper()
            rf2 = rf2 + d * d
    rF = rf2.sqrt().upper()
    lam, Q = _jacobi3(Cm)
    order = sorted(range(n), key=lambda k: -lam[k])
    lamo = [lam[k] for k in order]
    vec = [[Q[i][k] for i in range(n)] for k in order]
    res = [arb(0) for _ in range(n)]
    for k in range(n - 1):
        if not ((arb(lamo[k]) - res[k] - rF) > (arb(lamo[k + 1]) + res[k + 1] + rF)):
            raise Refused('control: eigenvalue enclosures overlap (no gap)')
    dk = []
    for k in range(n):
        g = None
        for j in range(n):
            if j != k:
                x = (abs(arb(lamo[k]) - arb(lamo[j])) - res[k] - res[j]).lower()
                g = x if g is None else _min_pt(g, x)
        d = (g - rF).lower()
        if not ((g > 0) and (d > 0)):
            raise Refused('control: no eigenvalue gap')
        eps = (arb.pi() / 2 * (res[k] / g + rF / d)).upper()
        dk.append([arb(x) + one * eps for x in vec[k]])
    return pd_vectors(C, vec, lamo, res, rF), dk


# ---- reader (e): P2-8's C4.1 record (v1_6 (2))
def load_p2_8(path, mode):
    """Cov_inf_lo per class, N and piece. CERTIFIED: no certified P2-8 producer pinned yet (refuses after the format check; once one is pinned, its FLOAT_IN list must join the joint export's FLOAT_IN under its record name, the FLOAT-IN rule); MOCK:
    MOCK_P2_8_C4_v1. Returns {(N<N>_<cls>, idx): [jlo, jhi, Cov_inf_lo]} with the strings as written."""
    L = lines_of(path)
    if mode == 'CERTIFIED':
        read_kv(L, 'CERTIFIED', 'EXPORT_P2_8_C4_v1')
        raise Refused('no certified P2-8 producer pinned yet')
    d = read_kv(L, 'MOCK', 'MOCK_P2_8_C4_v1')
    if d.get('FIELDS') != 'jlo jhi Cov_inf_lo' or d.get('CLASSES') != 'D3 D4 D4M':
        raise Refused('P2-8 record layout')
    C = {}
    for k, v in d.items():
        m = re.fullmatch(r'(N[34]_D(?:3|4|4M))_P([0-9]{4})', k)
        if m:
            f = v.split()
            if len(f) != 3:
                raise Refused('P2-8 row %s' % k)
            C[(m.group(1), m.group(2))] = f
    for N in (4, 3):
        for cls in ('D3', 'D4', 'D4M'):
            nm = 'N%d_%s' % (N, cls)
            if d.get(nm + '_PIECES') != '904' or sum(1 for (a, _) in C if a == nm) != 904:
                raise Refused('P2-8 pieces %s' % nm)
    return C


# ---- Lemma E (NOTE_P2_14_E2_v1): S3's g-part and s-part for single-trick window moments (v1_7)
def _gam_up(N, s2, L):
    """Gamma(s2/2, L) for s2 in {3, 5, 7}, closed forms through erfc (C-GAMMA checks Gamma(3/2, 5) against flint)."""
    sq = L.sqrt()
    g = sq * (-L).exp() + arb.const_sqrt_pi() / 2 * sq.erfc()
    if s2 >= 5:
        g = L * sq * (-L).exp() + arb(3) / 2 * g
    if s2 >= 7:
        g = L * L * sq * (-L).exp() + arb(5) / 2 * g
    return g


def tail_h(N, m, L, cl):
    """the horizontal Schur slot int_{xi > L} (xi - cl)^m e^-xi dmu / k1 (m = 1 with cl = 0, or m = 2), at J = 300, hence for every J >= 300."""
    if N == 3:
        x = L - cl
        poly = (x + 1) if m == 1 else (x * x + 2 * x + 2)
        return poly * (-L).exp() / (1 - arb(-600).exp())
    j0 = arb(300)
    low = arb.const_sqrt_pi() / 2 * j0.sqrt().erf() - j0.sqrt() * (-j0).exp()
    if m == 1:
        num = _gam_up(N, 5, L) - cl * _gam_up(N, 3, L)
    else:
        num = _gam_up(N, 7, L) - 2 * cl * _gam_up(N, 5, L) + cl * cl * _gam_up(N, 3, L)
    return arb(2).sqrt() * num / low


def row_h(N, m, ch):
    """an unrestricted horizontal row's norm over k1: int |xi - c|^m e^-xi dmu / k1 <= 1, (N - 1)/2, or E_k[xi^2] + ch^2 (m = 0, 1, 2)."""
    if m == 0:
        return arb(1)
    if m == 1:
        return arb(N - 1) / 2
    return (arb(2) if N == 3 else arb(15) / 4) + ch * ch


def vert_w(m, cl, ch, A):
    """the vertical end factor's unrestricted sup with the V weight (A = 1) or phi_0's weight e^-(A xi): sup_xi |xi - c|^m e^-(A xi)."""
    if m == 0:
        return arb(1)
    if m == 1:
        return 1 / (A * arb(1).exp())
    return up(ch * ch, (2 / A) * (2 / A) * (-A * cl - 2).exp())


def vert_tail(m, L, cl, A):
    """sup over xi > L of |xi - c|^m e^-(A xi) (L >= c+ + 2): (L - cl)^m e^-(A L)."""
    x = L - cl
    return ((x if m == 1 else x * x) if m else arb(1)) * (-A * L).exp()


def lemma_e(N, cls, mt, mf, levels, ce, cf, C):
    """(e_f, F_box) for the window function with powers (mt, mf) on the class's two factors (m = 2 centred at (ce, cf); m = 1 the uncentred
    bond variable; m = 0 absent). C: eps, sp (s' >= s), kap, Phi, rho, A, and S or (Psi, supp0) (balls). Refuses a level below c+ + 2 and,
    for A < 1, a vertical level below c+ + m/A (v1_14 (1)). Lemma E-prime (v1_14): Phi = Phi_eps, S = sqrt(Phi_eps Phi_eps,theta,b), A = A_theta."""
    Le, Lf = arb(levels[0]), arb(levels[1])
    (cel, ceh), (cfl, cfh) = ce, cf
    if not (Le >= ceh + 2 and Lf >= cfh + 2):
        raise Refused('a Lemma E level below c+ + 2')
    u = 1 / (1 - C['eps'])
    den = 1 - C['sp'] * C['sp']
    k, P = C['kap'], C['Phi']

    def boxf(m, L, cl, ch):
        return arb(1) if m == 0 else (L if m == 1 else up(L - cl, ch) * up(L - cl, ch))
    zero = arb(0)
    cel1, ceh1 = (cel, ceh) if mt == 2 else (zero, zero)
    cfl1, cfh1 = (cfl, cfh) if mf == 2 else (zero, zero)
    F = boxf(mt, Le, cel1, ceh1) * boxf(mf, Lf, cfl1, cfh1)
    e = (2 * C['eps'] * C['rho'] + C['eps'] * C['eps']) * u * u * F / den
    sharp = P * (2 * u * (k + u) + (k + u) * (k + u))
    if cls == 'D3' or mf == 0:
        kw = k if cls == 'D3' else arb(1)
        if mt:
            e += tail_h(N, mt, Le, cel1) * row_h(N, mf, cfh1) * kw * sharp / den
        if mf and cls == 'D3':
            e += tail_h(N, mf, Lf, cfl1) * row_h(N, mt, ceh1) * kw * sharp / den
        return e, F
    S = C['S'] if 'S' in C else C['supp0'] * (C['Psi'] * P).sqrt()   # v1_14 (1): Lemma E-prime's S'
    A = C['A']
    if not (Lf >= cfh1 + mf / (A if A < 1 else arb(1))):
        raise Refused('a vertical Lemma E level below c+ + m/A (v1_14 (1))')

    def vterm(op, wv, wa):
        return op * (u * k * P * wv + u * u * S * wa + 2 * u * (k + u) * S * wa + k * (k + u) * P * wv) / den
    if mt:
        e += vterm(tail_h(N, mt, Le, cel1), vert_w(mf, cfl1, cfh1, arb(1)), vert_w(mf, cfl1, cfh1, A))
    e += vterm(row_h(N, mt, ceh1), vert_tail(mf, Lf, cfl1, arb(1)), vert_tail(mf, Lf, cfl1, A))
    return e, F


def e1_bound(C):
    """v1_11 (1): e_1 = (2 eps_r rho_phi + eps_r^2) u^2/(1 - s'^2), u = 1/(1 - eps_r); s' >= s is on the safe side."""
    u = 1 / (1 - C['eps'])
    return (2 * C['eps'] * C['rho'] + C['eps'] * C['eps']) * u * u / (1 - C['sp'] * C['sp'])


def e_lower(x, ss):
    """v1_11 (3): the lower end of E_f from R_f's lower end x is min(x, (1 - s'^2) x), right also for x < 0."""
    a, b = x.lower(), (ss * x).lower()
    return a if a < b else b


def e_upper(y):
    """v1_11 (3): the upper end of E_f from R_f's upper end y is max(y, 0)."""
    z = y.upper()
    return z if z > 0 else arb(0)


def check_e_lower(lo, x, ss):
    """v1_11 (3): the assert behind e_lower: lo may not exceed min(x, (1 - s'^2) x)."""
    if not (lo <= x.lower() and lo <= (ss * x).lower()):
        raise Refused('a Lemma E lower end above min(R, (1 - sp^2) R)')
    return lo


def mean_ends(mb, e1, em, spart, ss):
    """v1_11 (3): Lemma E's ends for a mean, [min(x, (1 - s'^2) x) - s-part, max(y, 0) + s-part], with x, y the ends of R_f."""
    if not (e1 == 0) and not (mb.lower() > 0):   # v1_37 (6) 2a1da1e1: mb (1 +- e_1) scales an end correctly only when it is >= 0
        raise Refused('C-MEAN-SIGN: a relative correction e_1 > 0 on a ratio ball that is not certainly positive')
    x = mb.lower() * (1 - e1) - em
    lo = check_e_lower(e_lower(x, ss), x, ss)
    return ((lo - spart).lower(), (e_upper(mb.upper() * (1 + e1) + em) + spart).upper())



def tz_odd(mh, RC, ihz, g22, NH, GP, sp, t00, lt_lo):
    """v1_35 (2), row 2 by the odd Ritz route: t^_z = mhat G_22^(-1/2) IhZ/(G_00^(1/2) lt_lo^2), lt_lo = lambda~_0's certified lower end
    max(mu_0, lt0), and Delta_z = NH s' + s'|t_00| + GP (R6a's Delta_k with sigma_z = 0: psi_2 is odd, u-hat even), NH and GP at
    one Lam (nh_gp). C-G22-POS: G_22, G_00 and lt_lo certainly > 0."""
    G = RC['G']
    if not (g22 > 0 and G[0][0] > 0 and lt_lo > 0):
        raise Refused('C-G22-POS: g,2,2, G_00 or lambda~_0,low is not certainly positive')
    return mh * ihz / (g22.sqrt() * G[0][0].sqrt() * lt_lo * lt_lo), NH * sp + sp * t00 + GP


def nh_gp(IP, hb_lev, gb_lev):
    """v1_35 (2), C-Z-LEVEL: NH = Lam + Hbad'(Lam) and GP = Lam (mhat/lt0) eps_r + Gbad'(Lam) from the piece's lemma_a_amp dict,
    refused unless Hbad' and Gbad' were built at the dict's own Lam, the code level LAM_T."""
    if not (hb_lev == gb_lev == LAM_T and IP['Lam'] == arb(LAM_T)):
        raise Refused('C-Z-LEVEL: NH and GP are not at one Lam (Hbad-prime at %s, Gbad-prime at %s, the dict at %s)' % (
            hb_lev, gb_lev, IP['Lam'].str(4, radius=False)))
    return IP['Lam'] + IP['HbadP'], IP['Lam'] * (IP['mhat'] / IP['lt0']) * IP['eps_r'] + IP['GbadP']


def lt_ball(RC, LA, lt0):
    """v1_35 (3): lambda~_0's certified ball on the piece, [max(mu_0, (1 - eps_r) mhat), mu_0/mu_0^S,low] (Rayleigh, Lemma 19.2 (c), Kato-Temple's m0lo)."""
    mu0 = RC['vals'][0]
    lo = mu0.lower() if mu0.lower() > lt0.lower() else lt0.lower()
    if not (LA['m0lo'] > 0):
        raise Refused('lambda~_0 ball: m0lo is not certainly positive')
    hi = (mu0 / LA['m0lo']).upper()
    if not (lo <= hi):
        raise Refused('lambda~_0 ball: empty')
    return arb(lo).union(arb(hi))


def best_slev(N, mt, mf, kap):
    """v1_35 (3): the w = 2 window's Lemma S' value (D4 geometry, powers (mt, mf), uncentred) minimized over the fixed level grid 2, 2.5, ...,
    40. Every level gives a valid bound, so the minimum over this finite grid is one. Returns (value, level)."""
    z2 = (arb(0), arb(0))
    best = None
    for k in range(4, 81):
        L = '%g' % (k / 2)
        v = norm_win(N, 'D4', mt, mf, (L, L), z2, z2, kap)
        if best is None or v.upper() < best[0].upper():
            best = (v, L)
    return best


def mean_t_dt(mh, iht0, ihtt0, gxt00, G00, Lt, lam, eps_r, lt0, gtc, kap):
    """v1_35 (3), STB_P2_PREP_v1_2 l.100 in the norm form (ADD1 sect. 2): E_psi of the w = 2 window, [mhat (Iht,0 + IhTt,0) - mhat^2 Gxt,0,0]/
    (G_00 lambda~_0^2), and (a) the product term |<g, K_t g>|/(||psi-hat||^2 lambda_0^2) split at Lam_t: the box
    Lam_t eps_r^2 (mhat/lt0)^2 (C1: ||K^(1/2)|g||| <= eps_r mhat ||psi-hat||) and the tail k1^3 tail_h ||g||^2/(||psi-hat||^2 lambda_0^2) <=
    tail_h(N, 1, Lam_t, 0) (kappa + mhat/lt0)^2 Phi_eps (R6a's ||g|| <= (k1^3 + mu-hat) ||phi_0||; k1^3/lambda_0 <= kappa; k1^3 ||phi_0||^2/
    ||psi-hat||^2 <= c_K S^2 ||W'||^2/||psi-hat||^2 <= Phi_eps by Lemma T', c_K = k1_lim^3), with gtc = tail_h(N, 1, Lam_t, 0) Phi_eps.
    Returns (gg box, gg tail)."""
    main = (mh * (iht0 + ihtt0) - mh * mh * gxt00) / (G00 * Lt * Lt)
    u = mh / lt0
    return main, (lam * eps_r * eps_r * u * u).upper(), (gtc * (kap + u) * (kap + u)).upper()


def mean_b_nt(tb, G00, Lt):
    """v1_35 (3): E_psi of the w = 1 window of xi_b without a trick, Tb/(G_00 lambda~_0); the s-part is its only error."""
    return tb / (G00 * Lt)


def check_mean_parts(c, main, gg, sp, tag='C-MEAN-PARTS'):
    """v1_35 (3), C-MEAN-PARTS: a mean's ball (lo, hi) reaches main -+ (gg + s-part): lo <= main_lo - gg - sp and hi >= main_hi +
    gg + sp, each compared with the other side's rounding, so that only a missing part fails it (soundness is mean_ends's construction)."""
    if not (c[0] <= (main.lower() - gg - sp).upper() and c[1] >= (main.upper() + gg + sp).lower()):
        raise Refused('%s: a mean ball without its gg part or its s-part' % tag)
    return True


def means_dt(P_, gxt, tbv, spt, spb, ss, lam, gtc, kap):
    """v1_35 (3): one piece's double-trick means ((c_t lo, hi), (c_b lo, hi), parts) by mean_ends with e_1 = 0 (ADD1 sect. 2). P_ = the port's
    (mhat, lt0, lambda~_0 ball, G_00, eps_r, Iht,0, t-ball); gxt Gxt,0,0 and tbv Tb (S7 A,0) as entries; spt, spb the s-parts; ss = 1 - s'^2;
    lam = Lam_t, gtc and kap for the gg tail. parts = (gg box, gg tail, s-part c_t, s-part c_b, c_t main, c_b main, the relative width of
    G_00 lambda~_0^2)."""
    mh, lt0, Lt, G00, er, iht, tb = P_
    mt, ggb, ggt = mean_t_dt(mh, iht, iht, entry_piece(gxt, tb), G00, Lt, lam, er, lt0, gtc, kap)   # IhTt,0 := Iht,0 (C-ALIAS-MIRROR)
    gg = (ggb + ggt).upper()
    mb = mean_b_nt(entry_piece(tbv, tb), G00, Lt)
    ct, cb = mean_ends(mt, 0, gg, spt, ss), mean_ends(mb, 0, arb(0), spb, ss)
    check_mean_parts(ct, mt, gg, spt)
    check_mean_parts(cb, mb, arb(0), spb)
    nz = G00 * Lt * Lt
    return ct, cb, (ggb, ggt, spt, spb, mt, mb, (nz.rad() / nz.mid()).upper())


def load_m3e(pins=None):
    """v1_35 (3): pk03's m3_entries_v3 with its generic modules, each sha-pinned and loaded under the generic name as pk03's job scripts
    do (m3_run_v1_9_2 GENERIC); ctx.prec is restored after."""
    import importlib.util
    pins = PINS if pins is None else pins
    p0 = ctx.prec
    mods = {}
    for name, path in M3E_MODS:
        if pins.get(path) is None or sha_file(path) != pins[path]:
            raise Refused('alias module %s does not match its pin' % os.path.basename(path))
        spec = importlib.util.spec_from_file_location(name, path)
        mod = importlib.util.module_from_spec(spec)
        sys.modules[name] = mod
        spec.loader.exec_module(mod)
        mods[name] = mod
    ctx.prec = p0
    return mods['m3_entries_v3']


def alias_encs(pins=None):
    """v1_35 (3): the factor encodings from the pinned lists: S9's Iht,0 (S9_ENTRY_LIST_v1), S7's A,0 (M3_ENTRY_LIST_v1_2 'N:A,0'), Tb
    (P2_ENTRY_LIST_v1_3)."""
    pins = PINS if pins is None else pins
    for p in ALIAS_LISTS.values():
        if pins.get(p) is None or sha_file(p) != pins[p]:
            raise Refused('alias list %s does not match its pin' % os.path.basename(p))
    with open(ALIAS_LISTS['S9']) as fh:
        s9 = json.load(fh)
    with open(ALIAS_LISTS['M3']) as fh:
        m3 = json.load(fh)
    with open(ALIAS_LISTS['P2']) as fh:
        p2 = json.load(fh)
    iht = [e for e in s9['entries'] if e.get('key') == 'Iht,0']
    a0 = [e for e in m3['entries'] if e.get('id') == 'N:A,0']
    tb = [e for e in p2['entries'] if e.get('key') == 'Tb']
    if len(iht) != 1 or len(a0) != 1 or len(tb) != 1:
        raise Refused('alias encodings not found exactly once')
    return iht[0]['factors'], a0[0]['factors'], tb[0]['factors']


def c_alias_mirror(M3E, N, encs, alias=None):
    """v1_35 (3), C-ALIAS-MIRROR: IhTt,0 encoded as the exact mirror image [cp0 col 0, xia [3,0,1], cp0 col 2]; require
    c_mirror('N', N, IhTt,0, Iht,0) against S9's Iht,0 encoding. alias (plants only) replaces the encoding. True or Refused."""
    ts = M3E.load_trial(TS_FILES[N], VACRES[N], 0.0)
    enc = alias if alias is not None else [['cp', 0, 0], ['xia', [3, 0, 1]], ['cp', 0, 2]]
    ok, why = M3E.c_mirror('N', N, [M3E.factor(ts, 'N', e) for e in enc], [M3E.factor(ts, 'N', e) for e in encs[0]])
    if not ok:
        raise Refused('C-ALIAS-MIRROR: %s' % why)
    return True


def c_alias_flip(M3E, N, encs, tb_mid=None, q_shift=None):
    """v1_35 (3), C-ALIAS-FLIP: Tb = S7 A,0. (i) T <-> B (sigma) is an automorphism of N's couplings; (ii) every end factor
    exactly even (parity_class); (iii) Tb's middle c9 equals A,0's after PERM9 on the same triple (never repr: sigma reverses the triple);
    (iv) both are N-family entries (main_N). tb_mid and q_shift are for the plants only. True or Refused."""
    ts = M3E.load_trial(TS_FILES[N], VACRES[N], 0.0)
    if q_shift is not None:
        q = [list(x) for x in ts.q]
        q[0][0] = q[0][0] + q_shift
        ts = M3E.TrialSet(ts.S, (q[0], q[1], q[2]), ts.kbar)
    tb = [M3E.factor(ts, 'N', e) for e in encs[2]]
    a0 = [M3E.factor(ts, 'N', e) for e in encs[1]]
    if tb_mid is not None:
        tb[1] = tb_mid
    V, E = M3E.graph_edges('N', N)
    if not M3E.edges_map_onto(E, M3E.sigma):
        raise Refused('C-ALIAS-FLIP (i): T <-> B is not an automorphism of the couplings')
    if any(M3E.parity_class(f) != 'even' for f in (tb[0], tb[2], a0[0], a0[2])):
        raise Refused('C-ALIAS-FLIP (ii): an end factor is not exactly even')
    mt, ma = tb[1], a0[1]
    if not (mt[0] == 'xi' and ma[0] == 'xi' and tuple(mt[1]) == tuple(ma[1]) and mt[2] == ma[2]
            and all(mt[3][M3E.PERM9[i]] == ma[3][i] for i in range(9))):
        raise Refused('C-ALIAS-FLIP (iii): the middle factors differ under PERM9')
    return True

def norm_win(N, cls, mt, mf, levels, ce, cf, kap):
    """Lemma S' for the window function with powers (mt, mf) (squared or single factors): ||A_f||/lambda_0^w <= box + tails."""
    Le, Lf = arb(levels[0]), arb(levels[1])
    (cel, ceh), (cfl, cfh) = ce, cf
    zero = arb(0)
    cel1, ceh1 = (cel, ceh) if mt == 2 else (zero, zero)
    cfl1, cfh1 = (cfl, cfh) if mf == 2 else (zero, zero)
    if cls != 'D3' and mf and not (Lf >= cfh1 + mf):
        raise Refused('a vertical Lemma S-prime level below c+ + m')
    if (mt == 2 and not (Le >= ceh1)) or (cls == 'D3' and mf == 2 and not (Lf >= cfh1)):
        raise Refused('a horizontal Lemma S-prime level below c+ (v1_11 (2))')

    def boxf(m, L, cl, ch):
        return arb(1) if m == 0 else (L if m == 1 else up(L - cl, ch) * up(L - cl, ch))
    F = boxf(mt, Le, cel1, ceh1) * boxf(mf, Lf, cfl1, cfh1)
    if cls == 'D3':
        t = zero
        if mt:
            t += tail_h(N, mt, Le, cel1) * row_h(N, mf, cfh1)
        if mf:
            t += tail_h(N, mf, Lf, cfl1) * row_h(N, mt, ceh1)
        return F + t * kap * kap * kap
    t = zero
    if mt:
        t += tail_h(N, mt, Le, cel1) * vert_w(mf, cfl1, cfh1, arb(1))
    if mf:
        t += vert_tail(mf, Lf, cfl1, arb(1)) * row_h(N, mt, ceh1)
    return F + t * kap * kap


def joint_ad_c(M, ce, cf):
    """E2 of one class with the centring held at the balls ce, cf (constants in t): sum C(2,i)C(2,j)(-ce)^(2-i)(-cf)^(2-j) M_ij/M_00."""
    R = dict((k, M[k] / M[(0, 0)]) for k in M)
    me, mf = _ad(ce), _ad(cf)
    ex2 = _ad(0)
    for i, j in MOM:
        a, b = _ad(1), _ad(1)
        for _ in range(2 - i):
            a = a * (-me)
        for _ in range(2 - j):
            b = b * (-mf)
        ex2 = ex2 + math.comb(2, i) * math.comb(2, j) * a * b * R[(i, j)]
    return ex2


def e2_enclosure_c(E, pre, jlo, jhi, ce, cf):
    """E2 over the piece by the mean-value form with the centring fixed at the balls ce, cf."""
    tb, tm, r = tball(jlo, jhi)
    keys = ['%s_%d%d' % (pre, i, j) for i, j in MOM]
    mid = joint_ad_c(dict((ij, ent_ad(E[k], tm, False)) for ij, k in zip(MOM, keys)), ce, cf)
    der = joint_ad_c(dict((ij, ent_ad(E[k], tb, True)) for ij, k in zip(MOM, keys)), ce, cf)
    w = arb(0, 1) * r.upper()   # v1_34 (grep): outward
    return mid.v + der.d * w


def mij_enclosure(E, pre, ij, jlo, jhi):
    """v1_35 (5) (covtest3's): M_ij/M_00 over the piece by joint_enclosure's mean-value form (ij a string such as '11', '20', '02')."""
    tb, tm, r = tball(jlo, jhi)
    kij, k00 = '%s_%s' % (pre, ij), '%s_00' % pre
    mid = ent_ad(E[kij], tm, False) / ent_ad(E[k00], tm, False)
    der = ent_ad(E[kij], tb, True) / ent_ad(E[k00], tb, True)
    return mid.v + der.d * (arb(0, 1) * r.upper())


def cov_from(e11lo, ce, cf):
    """v1_35 (5), ADD1 sect. 3: the one product rule of every route, Cov_lo = E11_lo - c_e,hi c_f,hi, with c_e,lo > 0 and c_f,lo > 0
    certainly (C-COV-PROD)."""
    if not (ce[0] > 0 and cf[0] > 0):
        raise Refused('C-COV-PROD: a mean ball whose lower end is not certainly positive')
    return (e11lo - ce[1] * cf[1]).lower()


def cov_hi_from(e11hi, ce, cf):
    """v1_37 (6), the rule: the product rule's other end, Cov_hi = E11_hi - c_e,lo c_f,lo, under C-COV-PROD's positivity (for positive mean
    balls c_e c_f >= c_e,lo c_f,lo)."""
    if not (ce[0] > 0 and cf[0] > 0):
        raise Refused('C-COV-PROD: a mean ball whose lower end is not certainly positive')
    return (e11hi - ce[0] * cf[0]).upper()


def cov_inf_hi(covh, cls):
    """v1_37 (6): Cov_inf_hi, the smallest upper end over the admissible routes computed for the piece (ROUTE_OK, the route set of Cov_inf_lo)."""
    vals = [covh[r] for r in ROUTE_OK[cls] if r in covh]
    if not vals:
        raise Refused('C-COV-ORDER: no route upper end for %s' % cls)
    best = vals[0]
    for v in vals[1:]:
        if v < best:
            best = v
    return best


def check_cov_order(lo_s, hi_s):
    """v1_37 (6), C-COV-ORDER: a row's printed Cov_inf_lo and Cov_inf_hi are finite decimals with Cov_inf_lo <= Cov_inf_hi (exact)."""
    if not (re.fullmatch(DEC_RE, lo_s) and re.fullmatch(DEC_RE, hi_s)) or not (Fraction(lo_s) <= Fraction(hi_s)):
        raise Refused('C-COV-ORDER: Cov_inf_lo %s, Cov_inf_hi %s' % (lo_s, hi_s))
    return True


def check_cov_same(Lm, Lj):
    """v1_37 (6), C-COV-SAME: on every row key the means export's Cov_inf_lo equals the joint export's Cov_inf_lo string for string. Returns the
    number of rows compared."""
    dm, om = kv_parse(Lm)
    dj, oj = kv_parse(Lj)
    if 'Cov_inf_lo' not in dm.get('FIELDS', '').split() or 'Cov_inf_lo' not in dj.get('FIELDS', '').split():
        raise Refused('C-COV-SAME: a FIELDS without Cov_inf_lo')
    im, ij = dm['FIELDS'].split().index('Cov_inf_lo'), dj['FIELDS'].split().index('Cov_inf_lo')
    rows = [k for k in oj if re.fullmatch(r'N[34]_D(?:3|4|4M)_P[0-9]{4}', k)]
    if sorted(rows) != sorted(k for k in om if re.fullmatch(r'N[34]_D(?:3|4|4M)_P[0-9]{4}', k)):
        raise Refused('C-COV-SAME: the two exports hold different row keys')
    for k in rows:
        a, b = dm[k].split(), dj[k].split()
        if len(a) <= im or len(b) <= ij or a[im] != b[ij]:
            raise Refused('C-COV-SAME: row %s differs between the means and the joint export' % k)
    return len(rows)


def route_consts(N, cls, C, kap):
    """v1_35 (5): one class's J-uniform route terms at N for f = xi_e xi_f (powers 1, 1, uncentred), minimized over ROUTE_GRID: SINGLE's Lemma E'
    g-part e_11 and Lemma S' s-part (2 s' + s'^2) nw; DOUBLE's gg = e_11 less its first-order box 2 eps rho u^2 F/(1 - s'^2) (the eta box and every
    tail stay); per level, CS's Sigma_tails (e_11 less its box) and the S' tail rows (nw less its box F = L^2)."""
    z2 = (arb(0), arb(0))
    eps, rho, sp = C['eps'], C['rho'], C['sp']
    u = 1 / (1 - eps)
    den = 1 - sp * sp
    sq = 2 * sp + sp * sp
    best, tails, srows = {}, {}, {}
    for L in ROUTE_GRID:
        try:
            e, F = lemma_e(N, cls, 1, 1, (L, L), z2, z2, C)
            nw = norm_win(N, cls, 1, 1, (L, L), z2, z2, kap)
        except Refused:
            continue
        g1 = 2 * eps * rho * u * u * F / den
        box = (2 * eps * rho + eps * eps) * u * u * F / den
        for k, v in (('e11', e), ('nw', nw), ('ggd', e - g1)):
            if k not in best or v.upper() < best[k][0].upper():
                best[k] = (v, L)
        tails[L], srows[L] = e - box, nw - F
    if not best:
        raise Refused('route terms: no admissible level at N=%d %s' % (N, cls))
    return {'e11': best['e11'], 'nw': best['nw'], 's11': (sq * best['nw'][0], best['nw'][1]), 'ggd': best['ggd'], 'tails': tails, 'srows': srows,
            'u': u, 'den': den, 'sq': sq}


def e2t_piece(N, cls, E, pre, jlo, jhi, C, kap, e1, ss, glev, slev):
    """v1_35 (5): E2_t, Lemma E''s upper end of the bulk mean of xi_t^2 (m = 2, uncentred) from the class's own window ratio M_20/M_00, and that
    ratio's lower end (C-ECS-E2, C-D4S-LEVEL: E2_t at least the trial ratio, a sanity check)."""
    z2 = (arb(0), arb(0))
    R = mij_enclosure(E, pre, '20', jlo, jhi)
    e2, _F = lemma_e(N, cls, 2, 0, glev, z2, z2, C)
    s2 = (2 * C['sp'] + C['sp'] * C['sp']) * norm_win(N, cls, 2, 0, slev, z2, z2, kap)
    return (e_upper(R.upper() * (1 + e1) + e2) + s2).upper(), R.lower()


def sigma_d4(N, sp, e2t, kap, Lb, nwf, Lt=None):
    """v1_35 (5), C-D4S (ADD1_1 30950bd4, the review cdd70f5f's norm route): sigma_D4 = 2 L_b s' sqrt(E2_t) + s'^2 ||A^_f||_S' + (2 s' + s'^2) times the
    (1,1) window's b-tail row at the same level L_b (vert_tail(1, L_b) row_h(N, 1) kappa^2, t unrestricted). C-D4S-LEVEL: Lt, when given, is the
    b-tail's level and must equal L_b."""
    if Lt is not None and Lt != Lb:
        raise Refused('C-D4S-LEVEL: the split level %s is not the b-tail level %s' % (Lb, Lt))
    La = arb(Lb)
    btail = vert_tail(1, La, arb(0), arb(1)) * row_h(N, 1, arb(0)) * kap * kap
    return 2 * La * sp * e2t.sqrt() + sp * sp * nwf + (2 * sp + sp * sp) * btail


def ecs_rho(R8, g00hi, mlo):
    """v1_35 (5), C-ECS-PHI with C-M-POS: rho_(phi,ij)^2 <= 1 + 8 ||Q_ij||_Schur ||phi_0|| ||phi_0^-||/(main_N M_ij,lo) (the review e6ea2e4c The
    plain L^2 norms in which M_ij is defined; |phi_0| = phi_0 + 2 phi_0^-), in units: R8 = 8 kappa row_h(N, 2, 0) sigma_R sqrt(Phi_W,R Phi_eps)
    bounds 8 ||Q_ij|| ||phi_0|| ||phi_0^-||/(lambda_h ||psi-hat||^2) (||Q_ij|| <= k1^6 row_h(N, 2, 0); c_K ||phi_0||^2/||psi-hat||^2 <= Phi_eps;
    |phi_0^-| <= sigma_R W^(1-eps_R) (Lemma R at RHO_EPS_R), so c_K ||phi_0^-||^2/||psi-hat||^2 <= sigma_R^2 Phi_W,R (Lemma T' at eps_R); k1^3/lambda_h <= kappa; c_K = k1_lim^3 >=
    k1^3), and main_N M_ij/(lambda_h ||psi-hat||^2) = M_ij/G_00. Returns the bound on rho^2."""
    if not (mlo > 0):
        raise Refused('C-M-POS: M_ij lower end not certainly positive')
    return 1 + R8 * g00hi / mlo


def ecs_level(Lbox, Ltail):
    """v1_35 (5), C-ECS-LEVEL (): a CS box term and the tail term it is added to come from one level."""
    if Lbox != Ltail:
        raise Refused('C-ECS-LEVEL: box level %s with tail level %s' % (Lbox, Ltail))
    return True


def routes_piece(N, cls, K_, E, EX, pre, jlo, jhi, ce, cf, C, e1, ss, kap, port, R8, glev, slev):
    """v1_35 (5): the admissible routes' Cov lower ends ({route: Cov_lo}), upper ends ({route: Cov_hi}, v1_37 (6)) and info (E2_t, its trial ratio, rho_02^2, rho_20^2 or
    None). K_ = route_consts(N, cls); port = (mhat, lt0, lambda~_0 ball, G_00, eps_r, Iht,0, t-ball) of the piece."""
    eps, sp = C['eps'], C['sp']
    u, den, sq = K_['u'], K_['den'], K_['sq']
    R11 = mij_enclosure(E, pre, '11', jlo, jhi)
    e2t, r20 = e2t_piece(N, cls, E, pre, jlo, jhi, C, kap, e1, ss, glev, slev)
    s_e = K_['s11'][0]
    covs, covh, info = {}, {}, [e2t, r20, None, None]
    if cls != 'D3':
        sd4 = min((sigma_d4(N, sp, e2t, kap, L, K_['nw'][0], L) for L in ROUTE_GRID), key=lambda v: float(v.upper()))
        s_e = s_e if s_e.upper() < sd4.upper() else sd4
    lo, hi = mean_ends(R11, e1, K_['e11'][0], s_e, ss)
    covs['SINGLE'], covh['SINGLE'] = cov_from(lo, ce, cf), cov_hi_from(hi, ce, cf)
    mh, lt0, Lt, G00, er, iht, tb = port
    if cls == 'D3':
        m02, m20 = entry_piece(E['M3_02'], tb), entry_piece(E['M3_20'], tb)
        r02, r2_ = ecs_rho(R8, G00.upper(), m02.lower()), ecs_rho(R8, G00.upper(), m20.lower())
        info[2], info[3] = r02, r2_
        nz = Lt.lower() * G00.lower()
        q02, q20 = (r02 * m02.upper() / nz).sqrt(), (r2_ * m20.upper() / nz).sqrt()
        ef, sg = K_['e11'][0], K_['s11'][0]
        for L in ROUTE_GRID:
            if L not in K_['tails']:
                continue
            ecs_level(L, L)
            La = arb(L)
            g = u * u * (eps * (La * q02 + La * q20) + eps * eps * La * La) / den + K_['tails'][L]
            s = sp * 2 * La * e2t.sqrt() + sp * sp * La * La + sq * K_['srows'][L]
            ef = ef if ef.upper() < g.upper() else g
            sg = sg if sg.upper() < s.upper() else s
        lo, hi = mean_ends(R11, e1, ef, sg, ss)
        covs['CS'], covh['CS'] = cov_from(lo, ce, cf), cov_hi_from(hi, ce, cf)
    else:
        md = (mh * (entry_piece(EX['W1'], tb) + entry_piece(EX['W2'], tb)) - mh * mh * entry_piece(E['M4_11'], tb)) / (G00 * Lt * Lt)
        lo, hi = mean_ends(md, 0, K_['ggd'][0], s_e, ss)
        covs['DOUBLE'], covh['DOUBLE'] = cov_from(lo, ce, cf), cov_hi_from(hi, ce, cf)
    return covs, info, covh


def pick_route(cls, covs):
    """v1_35 (5): the exported (route, Cov_inf_lo): the largest admissible route value; ties go to the first route of ROUTE_OK[cls]."""
    best = None
    for r in ROUTE_OK[cls]:
        if r in covs and (best is None or covs[r] > best[1]):
            best = (r, covs[r])
    if best is None:
        raise Refused('C-ROUTE: no admissible route computed for %s' % cls)
    return best


def check_route(cls, route, cov, covs):
    """v1_35 (5), C-ROUTE: the exported route is admissible for the class (ROUTE_OK), its value is that route's own computation, and
    no admissible route computed is larger."""
    if route not in ROUTE_OK[cls]:
        raise Refused('C-ROUTE: route %s is not admissible for %s' % (route, cls))
    if route not in covs or not (cov == covs[route]):
        raise Refused('C-ROUTE: the exported Cov_inf_lo is not route %s value' % route)
    if any(covs[r] > cov for r in ROUTE_OK[cls] if r in covs):
        raise Refused('C-ROUTE: an admissible route is larger than the exported one')
    return True


def rho_f1_check(src):
    """v1_35 (5), C-RHO-F1 (ADD5): rho_phi = 1 + 2 sigma_eps sqrt(Phi_W) from Lemma R and Lemma T' needs G_00 from S7's certified g,0,0."""
    if src != 'S7_CERTIFIED_G00':
        raise Refused('C-RHO-F1: rho_phi with G_00 from %s' % src)
    return True


def load_hs(path, mode, pins=None, lines=None):
    """v1_35 (6), the normX_HS slot's reader (SPEC_HS_INV_NORMX_v1_2 sect. 5): MOCK through read_kv; CERTIFIED by rule V2 (C-HS-SRC): the record and
    its run output pinned, the run output's VERDICT lines exactly ['VERDICT VALID'] and one 'RECORD <file> <sha256>' line, EXPORT_STATUS
    CERTIFIED, FORMAT S4U_KV_v1, no MOCK token; refused until HS_RECORD is pinned. Returns the KV dict."""
    pins = PINS if pins is None else pins
    if mode == 'CERTIFIED':
        if HS_RECORD is None:
            raise Refused('C-HS-SRC: no certified HS record pinned yet')
        rp, ap = HS_RECORD
        for p in (rp, ap):
            if pins.get(p) is None or sha_file(p) != pins[p]:
                raise Refused('C-HS-SRC: %s does not match its pin' % os.path.basename(p))
        La = lines_of(ap)
        if [x for x in La if x.startswith('VERDICT')] != ['VERDICT VALID'] or \
                [x.split() for x in La if x.startswith('RECORD ')] != [['RECORD', os.path.basename(rp), pins[rp]]]:
            raise Refused('C-HS-SRC: the run output does not bind %s' % os.path.basename(rp))
        d, order = kv_parse(lines_of(rp))
        if d.get('FORMAT') != 'S4U_KV_v1' or d.get('EXPORT_STATUS') != 'CERTIFIED' or 'MOCK' in ' '.join(d.values()).upper():
            raise Refused('C-HS-SRC: not a certified S4U_KV_v1 record')
        if d.get('RECORD') != 'HS_INV_NORMX_v1' or not order or order[-1] != 'END' or d['END'] != 'HS_INV_NORMX_v1':
            raise Refused('C-HS-SRC: RECORD/END')
        return d
    return read_kv(lines if lines is not None else lines_of(path), 'MOCK', 'HS_INV_NORMX_v1')


def hs_rows(d, pins=None):
    """v1_35 (6), v1_37 (5): the record-level gates of SPEC_HS_INV_NORMX_v1_2 sect. 5 and its ADD1 on the D3, D4 and D4M rows, each refusal naming
    its gate (C-HS-NOTE, C-HS-OP, C-HS-INV, C-HS-LAMBDA, C-HS-J, C-HS-MIRROR; C-HS-D3-SAME is hs_d3_same). Returns {(N, class): (jlo, jhi or None,
    (ce_lo, ce_hi), (cf_lo, cf_hi), COEF)} in exact Fractions."""
    pins = PINS if pins is None else pins
    want = '%s:%s' % (HS_NOTE[len(CODEDIR) + 1:], pins.get(HS_NOTE))
    if pins.get(HS_NOTE) is None or sha_file(HS_NOTE) != pins[HS_NOTE] or d.get('LEMMA_NOTE') != want:
        raise Refused('C-HS-NOTE: LEMMA_NOTE %r is not the pinned %s' % (d.get('LEMMA_NOTE'), os.path.basename(HS_NOTE)))
    for cls, op in (('D3', HS_OP_D3), ('D4', HS_OP_D4), ('D4M', HS_OP_D4M)):
        if d.get('OPERATOR_%s' % cls) != op:
            raise Refused('C-HS-OP: OPERATOR_%s is not the exact string of the spec (v1_2 sect. 6, ADD1 sect. 1)' % cls)
    if d.get('NORMALIZATION') != HS_NORM:
        raise Refused('C-HS-OP: NORMALIZATION %r is not %s' % (d.get('NORMALIZATION'), HS_NORM))
    if d.get('TRACE') != 'HAAR_TWISTED_ON_H' or d.get('INTERFACE') != 'CENTRED_HS2_BOX':
        raise Refused('C-HS-INV: TRACE or INTERFACE')
    for cls, p in sorted(HS_P.items()):
        if d.get('LAMBDA_POWER_%s' % cls) != str(p):
            raise Refused('C-HS-LAMBDA: LAMBDA_POWER_%s %r is not %d' % (cls, d.get('LAMBDA_POWER_%s' % cls), p))
    if d.get('J_CLAIM') != HS_JCLAIM or d.get('FIELDS') != 'jlo jhi ce_lo ce_hi cf_lo cf_hi COEF':
        raise Refused('C-HS-J: J_CLAIM or FIELDS')
    if d.get('MIRROR_D4M') != 'ADJOINT_OF_D4' or \
            any(d.get('N%d_D4M_%s' % (N, k)) != d.get('N%d_D4_%s' % (N, k)) for N in (4, 3) for k in ('ROWS', 'R000', 'METHOD')):
        raise Refused('C-HS-MIRROR: MIRROR_D4M or a D4M row key differs from its D4 key')
    rows = {}
    for N in (4, 3):
        for cls in ('D3', 'D4', 'D4M'):
            if d.get('N%d_%s_METHOD' % (N, cls)) not in HS_METHODS:
                raise Refused('C-HS-J: N%d_%s_METHOD %r' % (N, cls, d.get('N%d_%s_METHOD' % (N, cls))))
            f = d.get('N%d_%s_R000' % (N, cls), '').split()
            if d.get('N%d_%s_ROWS' % (N, cls)) != '1' or len(f) != 7:
                raise Refused('C-HS-J: N%d_%s rows' % (N, cls))
            jl, jh = Fraction(f[0]), (None if f[1] == 'inf' else Fraction(f[1]))
            if jh is not None and not (jh > jl):
                raise Refused('C-HS-J: the N%d_%s row is a point value' % (N, cls))
            rows[(N, cls)] = (jl, jh, (Fraction(f[2]), Fraction(f[3])), (Fraction(f[4]), Fraction(f[5])), Fraction(f[6]))
    return rows


def hs_d3_same(d, pins=None):
    """v1_37 (5), C-HS-D3-SAME (ADD1 sect. 2): every key of the pinned D3 record HS_RECORD_D3 (6b82dc63) except CODE and END has the same value in
    the combined record, so its D3 rows cannot move unnoticed."""
    pins = PINS if pins is None else pins
    if pins.get(HS_RECORD_D3) is None or sha_file(HS_RECORD_D3) != pins[HS_RECORD_D3]:
        raise Refused('C-HS-D3-SAME: %s does not match its pin' % os.path.basename(HS_RECORD_D3))
    old, _order = kv_parse(lines_of(HS_RECORD_D3))
    bad = [k for k, v in old.items() if k not in ('CODE', 'END') and d.get(k) != v]
    if bad:
        raise Refused('C-HS-D3-SAME: %d keys of the D3 record differ (first %s)' % (len(bad), bad[0]))
    return True


def hs_op_spec(pins=None, ops=None):
    """v1_37 (5), C-HS-OP-SPEC: this file's HS_OP_D4 and HS_OP_D4M (ops: a plant's stand-ins) are, line for line, the OPERATOR_D4 and OPERATOR_D4M
    strings of the pinned SPEC_HS_INV_NORMX_v1_2_ADD1 (the first line with each key, sect. 1)."""
    pins = PINS if pins is None else pins
    ops = (HS_OP_D4, HS_OP_D4M) if ops is None else ops
    if pins.get(HS_ADD1) is None or sha_file(HS_ADD1) != pins[HS_ADD1]:
        raise Refused('C-HS-OP-SPEC: %s does not match its pin' % os.path.basename(HS_ADD1))
    L = lines_of(HS_ADD1)
    for k, op in zip(('OPERATOR_D4', 'OPERATOR_D4M'), ops):
        if [x for x in L if x.startswith(k + ' = ')][:1] != [k + ' = ' + op]:
            raise Refused('C-HS-OP-SPEC: %s differs from ADD1 sect. 1' % k)
    return True


def hs_piece(row, jlo, jhi, ce, cf, lt_lo, p=2):
    """v1_35 (6), v1_37 (5): one piece's normX_HS = (COEF/lambda~_0,lo^p)^(1/2) (HS2_hi = COEF (lambda_h/lambda_0,lo)^p, C-HS-LAMBDA: p = 2 for D3,
    1 for D4 and D4M), after C-HS-J (the piece inside the row's J range under grid_j's readings) and C-HS-CBOX (the certified mean balls inside
    the row's box, lower ends >= 0)."""
    jl, jh, bxe, bxf, coef = row
    if not (grid_j(jlo, True) >= jl) or (jh is not None and (jhi == 'inf' or grid_j(jhi, False) > jh)):
        raise Refused('C-HS-J: piece [%s, %s] outside the row' % (jlo, jhi))
    for c, bx in ((ce, bxe), (cf, bxf)):
        if not (c[0] >= 0 and c[0] >= _frac_ball(bx[0], bx[0]).upper() and c[1] <= _frac_ball(bx[1], bx[1]).lower()):
            raise Refused('C-HS-CBOX: a mean ball outside the row box')
    if not (lt_lo > 0):
        raise Refused('C-HS-LAMBDA: lambda~_0,lo not certainly positive')
    if p not in (1, 2):
        raise Refused('C-HS-LAMBDA: power %r' % (p,))
    return (_frac_ball(coef, coef).upper() / (lt_lo if p == 1 else lt_lo * lt_lo)).sqrt().upper()


def hs_spot(d, N, pins=None, cls='D3'):
    """v1_35 (6), v1_37 (5), C-HS-SPOT (a control, not soundness): the record's N<N>_<class>_SPOT second token, the float value of
    2 Cov(X_c, theta X_c) + Cov^2 at the half-step plane from pk11's kt_s8rf_v1, whose source the record names by path and full sha256; it
    must be the pinned output."""
    pins = PINS if pins is None else pins
    v = d.get('N%d_%s_SPOT' % (N, cls), '')
    f = v.split()
    src = v.split('source ')[-1].strip() if 'source ' in v else ''
    p = HS_SPOT_SRC[N]
    if len(f) < 2 or pins.get(p) is None or sha_file(p) != pins[p] or src != '%s:%s' % (p[len(CODEDIR) + 1:], pins[p]):
        raise Refused('C-HS-SPOT: N%d_%s_SPOT does not name the pinned kt_s8rf_v1 output' % (N, cls))
    return Fraction(f[1])


def r8_pair(N, kap, sig, sig_eps, pw, pw_eps, pe):
    """v1_35 (5), C-RHO-R: ecs_rho's constant R8 = 8 kappa row_h(N, 2, 0) sigma sqrt(Phi_W Phi_eps) from one Lemma R pair: sigma
    and Phi_W must come from the same eps (a sigma at 0.85 with a Phi_W at 1/4 is unsound, since W^0.75 < W^0.15)."""
    if sig_eps != pw_eps:
        raise Refused('C-RHO-R: sigma at eps %s with Phi_W at eps %s' % (sig_eps, pw_eps))
    return 8 * kap * row_h(N, 2, arb(0)) * sig * (pw * pe).sqrt()


def status_junif(float_in_lists, open_conds, m4src=None):
    """v1_35 (7): one code path for an export's (status, FLOAT_IN, J_UNIFORMITY): the per-piece string J_UNIF_PP only with the status
    CERTIFIED (and, for the t export, every M4 input of the t path certified: t_uniformity), else J_UNIF_T_ASSUMED."""
    st, named = export_status(float_in_lists, open_conds)
    ju = J_UNIF_PP if (st == 'CERTIFIED' and (m4src is None or t_uniformity(m4src) == J_UNIF_PP)) else J_UNIF_T_ASSUMED
    return st, named, ju


def check_status_junif(st, named, ju):
    """v1_35 (7), C-JUNIF-STATUS: the per-piece J_UNIFORMITY string only beside the status CERTIFIED and an empty FLOAT_IN."""
    if ju == J_UNIF_PP and (st != 'CERTIFIED' or named != 'none'):
        raise Refused('C-JUNIF-STATUS: the per-piece J_UNIFORMITY with status %s and FLOAT_IN %s' % (st, named))
    return True


def readback_lines(L, record, header, rows):
    """v1_35 (7), C-READBACK: an export's lines hold exactly the header and rows meant to be written, key for key and string for string,
    and END (PLANT-CERT-REWRITE: a row changed after writing is refused)."""
    d, order = kv_parse(L)
    want = dict(list(header.items()) + list(rows))
    if order[-1:] != ['END'] or d.get('END') != record or len(d) != len(want) + 1 or any(d.get(k) != v for k, v in want.items()):
        raise Refused('C-READBACK: the %s lines do not read back as written' % record)
    return True


def cert_checks(path, record, header, rows, readers=None):
    """v1_36 (1): the cert writer's refusals, each before any file operation (v1_35 (7)). C-CERT-PATH: pk15/out/ only.
    C-CERT-HEADER: FORMAT S4U_KV_v1, TAG CERTIFIED ..., EXPORT_STATUS CERTIFIED and RECORD the record; since v1_36 also FLOAT_IN none,
    OPEN_CONDITIONS none and J_UNIFORMITY J_UNIF_PP. C-CERT-MOCKTOKEN: no MOCK token in any value. C-CERT-READER: readers,
    the dict of one reader per RECORD, has a reader for the record. The in-memory certified copy runs these checks too
    (cert_copy_check)."""
    if not _in_dir(path, COUT):
        raise Refused('C-CERT-PATH: a certified export outside pk15/out')
    if header.get('FORMAT') != 'S4U_KV_v1' or header.get('EXPORT_STATUS') != 'CERTIFIED' or not header.get('TAG', '').startswith('CERTIFIED ') \
            or header.get('RECORD') != record:
        raise Refused('C-CERT-HEADER: not a certified header')
    if header.get('FLOAT_IN') != 'none' or header.get('OPEN_CONDITIONS') != 'none' or header.get('J_UNIFORMITY') != J_UNIF_PP:
        raise Refused('C-CERT-HEADER: FLOAT_IN, OPEN_CONDITIONS or J_UNIFORMITY is not the certified value (none, none, J_UNIF_PP)')
    for k, v in list(header.items()) + list(rows):
        if 'MOCK' in str(v).upper():
            raise Refused('C-CERT-MOCKTOKEN: MOCK in %s' % k)
    if not isinstance(readers, dict) or not callable(readers.get(record)):
        raise Refused('C-CERT-READER: no reader for %s in the readers dict; no certified export is written' % record)
    return True


class DiskFS(object):
    """v1_37 (1): the cert writer's store on disk, the one a cert run uses."""
    def exists(self, p):
        return os.path.exists(p)

    def open_x(self, p):
        return open(p, 'x', encoding='utf-8')

    def sync(self, fh):
        fh.flush()
        os.fsync(fh.fileno())

    def read(self, p):
        with open(p, 'rb') as fh:
            return fh.read()

    def rename(self, a, b):
        os.rename(a, b)


class NoWriteFS(DiskFS):
    """v1_37 (1): the pre-write plants' store: names are tested on disk, and a write or a rename raises, so a plant that gets
    past the check under test stops before it writes (v1_36's nowrite opener)."""
    def open_x(self, p):
        raise RuntimeError('PLANT-NOWRITE: a cert plant reached the file write')

    def rename(self, a, b):
        raise RuntimeError('PLANT-NOWRITE: a cert plant reached a rename')


class MemFS(object):
    """v1_37 (1): an in-memory store with DiskFS's operations, for PLANT-CERT-PART, PLANT-CERT-STAGE2 and C-CERT-DRY; nothing touches the disk.
    existing: names that already exist (as empty files)."""
    def __init__(self, existing=()):
        self.files = dict((p, b'') for p in existing)

    def exists(self, p):
        return p in self.files

    def open_x(self, p):
        if p in self.files:
            raise FileExistsError(p)
        return MemFile(self, p)

    def sync(self, fh):
        pass

    def read(self, p):
        return self.files[p]

    def rename(self, a, b):
        self.files[b] = self.files.pop(a)


class MemFile(object):
    """v1_37 (1): a MemFS file open for writing; its text is stored, UTF-8 encoded, when the with block closes it."""
    def __init__(self, fs, p):
        self.fs, self.p, self.parts = fs, p, []

    def write(self, s):
        self.parts.append(s)

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        self.fs.files[self.p] = ''.join(self.parts).encode('utf-8')
        return False


DISK = DiskFS()


def cert_tmp(path):
    """v1_37 (1): this run's temporary name for the final name path, <path>.<RUN_TAG>.part. It is unique per run, so a .part that a refused
    write left behind, which nothing here can delete, never blocks a retry."""
    return '%s.%s.part' % (path, RUN_TAG)


def check_cert_free(path, tmp, fs):
    """v1_37 (1), C-CERT-EXISTS before a write: neither the final name nor this run's temporary name exists in the store, each a named
    refusal (PLANT-CERT-EXISTS: the final name on disk; PLANT-CERT-PART: the temporary name in a MemFS)."""
    if fs.exists(path):
        raise Refused('C-CERT-EXISTS: %s exists' % os.path.basename(path))
    if fs.exists(tmp):
        raise Refused('C-CERT-EXISTS: the temporary file %s exists' % os.path.basename(tmp))
    return True


def cert_stage(path, record, header, rows, readers=None, fs=None):
    """v1_37 (1), the cert writer's first phase (v1_35 (7)): cert_checks; check_cert_free; the text
    (cert_text) written to this run's temporary file through fs (DISK by default) and synced; the bytes read back through C-READBACK and then
    the record's reader as CERTIFIED. No final name is touched. Returns (final name, temporary name, sha256 of the bytes) for cert_commit."""
    fs = DISK if fs is None else fs
    cert_checks(path, record, header, rows, readers)
    tmp = cert_tmp(path)
    check_cert_free(path, tmp, fs)
    try:
        fh = fs.open_x(tmp)
    except FileExistsError:
        raise Refused('C-CERT-EXISTS: the temporary file %s appeared before the write' % os.path.basename(tmp))
    with fh:
        fh.write(cert_text(record, header, rows))
        fs.sync(fh)
    raw = fs.read(tmp)
    L = raw.decode('utf-8').split('\n')
    readback_lines(L, record, header, rows)   # C-READBACK binds the header strings and END before the reader runs
    readers[record](L, True)
    return (path, tmp, hashlib.sha256(raw).hexdigest())


def cert_commit(staged, fs=None):
    """v1_37 (1), the cert writer's second phase, after every export is staged: the final names distinct and still free (C-CERT-EXISTS) and
    every temporary file still holding its checked bytes (C-CERT-COMMIT), all before the first rename; then each rename, the renamed file
    holding its bytes (C-CERT-RENAME). Returns the sha256s in order."""
    fs = DISK if fs is None else fs
    if len(set(p for p, t, s in staged)) != len(staged):
        raise Refused('C-CERT-COMMIT: a final name is staged twice')
    for p, t, s in staged:
        if fs.exists(p):
            raise Refused('C-CERT-EXISTS: %s appeared after staging' % os.path.basename(p))
        if hashlib.sha256(fs.read(t)).hexdigest() != s:
            raise Refused('C-CERT-COMMIT: %s changed after its checks' % os.path.basename(t))
    for p, t, s in staged:
        fs.rename(t, p)
        if hashlib.sha256(fs.read(p)).hexdigest() != s:
            raise Refused('C-CERT-RENAME: %s does not hold the bytes read back' % os.path.basename(p))
    return [s for p, t, s in staged]


def cert_write_all(items, readers, fs=None):
    """v1_37 (1), the choice (a): the staged cert write, all or none: every item (final name, record, header, rows) is staged before any is
    committed, so a refusal anywhere leaves only this run's temporary files and no final name."""
    staged = [cert_stage(p, r, h, w, readers, fs) for p, r, h, w in items]
    return cert_commit(staged, fs)


def kv_write_cert(path, record, header, rows, readers=None, fs=None):
    """v1_37 (1): one export through the staged writer (the cert plants' entry point); returns its sha256."""
    return cert_write_all([(path, record, header, rows)], readers, fs)[0]


def check_setac_layer(top, name):
    """v1_36 (3): reader (b2)'s layer test of one record, part of C-A-BIND: the record's kernel is M3R6_LAYER (arbeng_ma_v1_4_1 by
    sha8; m3_reader_v6_3 has checked the full sha256 against its validated layers). PLANT-A-LAYER: S7's record through v6_3 (arbeng_ma_v1_3)."""
    if (top.get('kernel_file'), str(top.get('kernel_sha256', ''))[:8]) != M3R6_LAYER:
        raise Refused('C-A-BIND: %s carries the layer %r, not %s' % (name, top.get('kernel_file'), M3R6_LAYER[0]))
    return True


def check_setac_count(keys, X, ents, name):
    """v1_36 (3): C-A-COUNT for one record: its keys are exactly the run-list keys of its family graph X. PLANT-A-COUNT-FAM: the NTB
    key set offered as a DT record."""
    if sorted(keys) != sorted(k for k in RUN_KEYS if ents[k]['graph'] == X):
        raise Refused('C-A-COUNT: %s does not carry exactly the run-list keys of %s' % (name, X))
    return True


def check_cov_prod(ce, cf):
    """v1_36 (3): C-COV-PROD on one row, by cov_from's own test (both mean balls certainly positive at their lower ends)."""
    cov_from(arb(0), ce, cf)
    return True


def check_e2t(e2t, r20):
    """v1_36 (3): C-ECS-E2 on one piece (a sanity check): E2_t is at least the lower end of the trial ratio M_20/M_00. PLANT-D4S-E2."""
    if not (e2t >= r20):
        raise Refused('C-ECS-E2: E2_t below the trial ratio M_20/M_00')
    return True


def check_pos(rows, fields, names, tag):
    """v1_36 (4): C-COV-POS and C-T-POS: on every row each named field, an exact decimal as printed, is > 0 (Fraction). The consumer's C-SRC-J
    needs Cov_inf_lo > 0 and its SIGN test A_t, A_a, X_ta > 0."""
    fl = fields.split()
    ix = [fl.index(n) for n in names]
    for k, v in rows:
        f = v.split()
        if len(f) != len(fl) or not all(re.fullmatch(DEC_RE, f[i]) and Fraction(f[i]) > 0 for i in ix):
            raise Refused('%s: row %s has a field of %s that is not a decimal > 0' % (tag, k, ', '.join(names)))
    return True


def s9h_load(pins=None):
    """v1_36 (1): pk07's readers module read once as bytes, checked against the full sha256 of its pin
    and run from those same bytes in a fresh module (no import by path, no second read); the entry points S9H_NAMES must be there."""
    pins = PINS if pins is None else pins
    with open(RDR_PATH, 'rb') as fh:
        raw = fh.read()
    if pins.get(RDR_PATH) is None or hashlib.sha256(raw).hexdigest() != pins[RDR_PATH]:
        raise Refused('C-S9H-LOAD: %s does not match its pin' % os.path.basename(RDR_PATH))
    import types
    rd = types.ModuleType('kt_s9h_v1_3_readers')
    rd.__file__ = RDR_PATH
    exec(compile(raw.decode('utf-8'), RDR_PATH, 'exec'), rd.__dict__)
    miss = [n for n in S9H_NAMES if not callable(getattr(rd, n, None))]
    if miss:
        raise Refused('C-S9H-LOAD: the readers module lacks %s' % ', '.join(miss))
    return rd


def s9h_grid(rd):
    """v1_36 (1): the readers' piece grid, [(jlo, jhi)] as strings (joint_grid reads v2_2's pinned export, the file GRID names); any exception is
    a refusal ()."""
    try:
        return [tuple(x) for x in rd.joint_grid()]
    except Exception as e:
        raise Refused('C-S9H-GRID: joint_grid raised %r' % (e,))


def s9h_ident(d, record, certified, tag):
    """v1_36 (1): a record's identity and mode, which joint_read leaves to its caller: RECORD and END the record, FORMAT and EXPORT_STATUS the
    mode's (S4U_KV_v1 and CERTIFIED, or S4U_KV_v1 MOCK and MOCK), TAG starting with CERTIFIED or MOCK, and RUN_VERDICT VALID."""
    want = {'RECORD': record, 'END': record, 'FORMAT': 'S4U_KV_v1' if certified else 'S4U_KV_v1 MOCK',
            'EXPORT_STATUS': 'CERTIFIED' if certified else 'MOCK', 'RUN_VERDICT': 'VALID'}
    bad = [k for k, v in want.items() if d.get(k) != v] + ([] if d.get('TAG', '').startswith('CERTIFIED ' if certified else 'MOCK') else ['TAG'])
    if bad:
        raise Refused('%s: %s not as a %s %s record' % (tag, ', '.join(bad), 'CERTIFIED' if certified else 'MOCK', record))
    return True


def s9h_joint_check(rd, grid, L, certified):
    """v1_36 (1): the joint export's reader: kt_s9h_v1_3's s4u_read_port and joint_read, which must find no problems, then
    s9h_ident. Any exception from the readers is a refusal."""
    try:
        rec = rd.s4u_read_port('\n'.join(L))
        J, probs = rd.joint_read(rec, grid)
    except Exception as e:
        raise Refused('C-S9H-JOINT: the reader raised %r' % (e,))
    if probs:
        raise Refused('C-S9H-JOINT: joint_read finds %d problems (first: %s)' % (len(probs), '; '.join(probs[:3])))
    return s9h_ident(rec, 'EXPORT_P2_14_JOINT_v1', certified, 'C-S9H-JOINT')


def s9h_t_check(rd, grid, L, certified):
    """v1_36 (1): the t export's reader: kt_s9h_v1_3's s4u_read_port and t_read with the mode's R, which must find no problems,
    then s9h_ident. aa is empty: the export names Aa_lo in FIELDS, and a record without it is refused (KeyError) instead of taking t_read's
    stand-in. Any exception is a refusal ()."""
    R = dict(record='EXPORT_P2_T_v1', fmt='S4U_KV_v1' if certified else 'S4U_KV_v1 MOCK', status='CERTIFIED' if certified else 'MOCK')
    try:
        rec = rd.s4u_read_port('\n'.join(L))
        T, probs = rd.t_read(rec, grid, R, {})
    except Exception as e:
        raise Refused('C-S9H-T: the reader raised %r' % (e,))
    if probs:
        raise Refused('C-S9H-T: t_read finds %d problems (first: %s)' % (len(probs), '; '.join(probs[:3])))
    return s9h_ident(rec, 'EXPORT_P2_T_v1', certified, 'C-S9H-T')


def means_check(grid, L, certified):
    """v1_36 (1): the means export's own reader (kt_s9h does not read it): s9h_ident; FIELDS MN_FIELDS, CLASSES D3 D4 D4M and each
    class's piece count at both N; every row on the grid string for string, its six numbers exact decimals with 0 < ce_lo <= ce_hi,
    0 < cf_lo <= cf_hi and 0 < Cov_inf_lo <= Cov_inf_hi (v1_37 (6)), and no other row; PRECERT or STUB refused; a CERTIFIED record also
    FLOAT_IN none, OPEN_CONDITIONS none, J_UNIFORMITY J_UNIF_PP, COV_CENTRING exactly (v1_37 (6)) and no MOCK token. Any exception is a refusal."""
    try:
        d, order = kv_parse(L)
        s9h_ident(d, 'EXPORT_P2_14_MEANS_v1', certified, 'C-MEANS-READ')
        want = dict(FIELDS=MN_FIELDS, CLASSES='D3 D4 D4M')
        if certified:
            want.update(FLOAT_IN='none', OPEN_CONDITIONS='none', J_UNIFORMITY=J_UNIF_PP, COV_CENTRING=COV_CENTRING)
        bad = ['header %s' % k for k, v in want.items() if d.get(k) != v]
        if any(w in d.get(k, '').upper() for k in ('FORMAT', 'RECORD', 'END', 'TAG', 'CLAIM') for w in BADWORDS):
            bad.append('marked PRECERT or STUB')
        if certified and any('MOCK' in v.upper() for v in d.values()):
            bad.append('a MOCK token')
        for N in (4, 3):
            for cls in ('D3', 'D4', 'D4M'):
                if d.get('N%d_%s_PIECES' % (N, cls)) != str(len(grid)):
                    bad.append('N%d_%s_PIECES' % (N, cls))
                for i, (jlo, jhi) in enumerate(grid):
                    v = d.get('N%d_%s_P%04d' % (N, cls, i), '').split(' ')
                    if len(v) != 8 or v[0] != jlo or v[1] != jhi or not all(re.fullmatch(DEC_RE, x) for x in v[2:]):
                        bad.append('row N%d_%s_P%04d' % (N, cls, i))
                    elif not (0 < Fraction(v[2]) <= Fraction(v[3]) and 0 < Fraction(v[4]) <= Fraction(v[5]) and 0 < Fraction(v[6]) <= Fraction(v[7])):
                        bad.append('balls N%d_%s_P%04d' % (N, cls, i))
        nrow = len([k for k in order if re.fullmatch(r'N[0-9]+_[A-Z0-9]+_P[0-9]+', k)])
        if nrow != 6 * len(grid):
            bad.append('%d rows, not %d' % (nrow, 6 * len(grid)))
    except Refused as e:
        raise Refused(str(e) if str(e).startswith('C-MEANS-READ') else 'C-MEANS-READ: %s' % e)
    except Exception as e:
        raise Refused('C-MEANS-READ: raised %r' % (e,))
    if bad:
        raise Refused('C-MEANS-READ: %d problems (first: %s)' % (len(bad), '; '.join(bad[:3])))
    return True


def s9h_readers(rd, grid):
    """v1_36 (1): one reader per RECORD, each a function of (lines, certified) that returns True or raises Refused; the cert writer
    and the read-back use this dict, and a record without an entry has no reader (C-CERT-READER)."""
    return {'EXPORT_P2_14_JOINT_v1': lambda L, c: s9h_joint_check(rd, grid, L, c),
            'EXPORT_P2_T_v1': lambda L, c: s9h_t_check(rd, grid, L, c),
            'EXPORT_P2_14_MEANS_v1': lambda L, c: means_check(grid, L, c)}


def bind_check(rd, name, sha, otext):
    """v1_36 (1), C-S9H-BIND: rule V2's binding of a run output to an export (kt_s9h_v1_3's bound_ok): VERDICT lines exactly ['VERDICT VALID']
    and exactly one EXPORT line naming the base name with its sha256. Here a test on a synthetic text: this run's own VERDICT line does not
    exist while it runs, so the real binding is the consumer's. Any exception is a refusal."""
    try:
        ok = rd.bound_ok(name, sha, otext)
    except Exception as e:
        raise Refused('C-S9H-BIND: bound_ok raised %r' % (e,))
    if ok is not True:
        raise Refused('C-S9H-BIND: bound_ok refuses %s with sha256 %s...' % (name, sha[:8]))
    return True


def cert_text(record, header, rows):
    """v1_36 (1): the cert writer's text: one comment line, the header, the rows and END (also the in-memory certified copy's)."""
    return ''.join(['# %s: written by %s from pinned certified records.\n' % (record, LABEL)] +
                   ['%s = %s\n' % kv for kv in list(header.items()) + list(rows)] + ['END = %s\n' % record])


def certify_header(h, sha):
    """v1_36 (1), C-S9H-CERTCOPY: a MOCK export's header as a cert run writes it, in memory only: the suffixes ' (MOCK)' (MSFX) and
    ' (MOCK constants)' taken off every value; FORMAT S4U_KV_v1, TAG CERTIFIED <label> <sha8>, EXPORT_STATUS CERTIFIED, CLAIM CLAIM_CERT and
    J_UNIFORMITY J_UNIF_PP; the key order kept."""
    c = {}
    for k, v in h.items():
        for sfx in (' (MOCK constants)', ' (MOCK)'):
            if v.endswith(sfx):
                v = v[:-len(sfx)]
        c[k] = v
    c.update(FORMAT='S4U_KV_v1', TAG='CERTIFIED %s %s' % (LABEL, sha[:8]), EXPORT_STATUS='CERTIFIED', CLAIM=CLAIM_CERT, J_UNIFORMITY=J_UNIF_PP)
    return c


def cert_copy_check(record, header, rows, readers):
    """v1_36 (1), C-S9H-CERTCOPY: one export with its certified header, in memory: the cert writer's refusals before any file operation
    (cert_checks, at a name in pk15/out), then C-READBACK and the record's reader as CERTIFIED on the text the cert writer writes
    (cert_text). Nothing is written."""
    cert_checks(os.path.join(COUT, 'export_certcopy_%s.kv' % LABEL), record, header, rows, readers)
    L = cert_text(record, header, rows).split('\n')
    readback_lines(L, record, header, rows)
    return readers[record](L, True)


# ---- tests
def plant(nofire, name, fn):
    """a must-fire plant: fn must raise Refused (a refusal by the reader under test)."""
    try:
        fn()
    except Refused as e:
        out('%s: refused (%s) -> FIRES' % (name, e))
        return
    except Exception as e:
        out('%s: raised %r instead of a refusal -> DOES NOT FIRE' % (name, e))
        nofire.append(name)
        return
    out('%s: accepted -> DOES NOT FIRE' % name)
    nofire.append(name)


def flag(fn):
    """v1_35: True if fn() returns True, False on a refusal (for a gate with its own flag)."""
    try:
        return fn() is True
    except Refused:
        return False


def ovl(a, b):
    """v1_35: two (lo, hi) balls meet (each lower end at most the other upper end)."""
    return (a[0] <= b[1]) and (b[0] <= a[1])


def ecs_rho_used(rho2, R8, g00hi, mlo):
    """v1_35 (5), C-ECS-PHI: a rho_(phi,ij)^2 used by the CS route is at least the Q-form bound (PLANT-ECS-PHI: rho^2 = 1, phi_0 >= 0 assumed, must fail)."""
    if not (rho2 >= ecs_rho(R8, g00hi, mlo)):
        raise Refused('C-ECS-PHI: rho_(phi,ij) below its Q-form bound')
    return True


def hs_cov_check(nxh, cvl):
    """v1_35 (6), C-HS-COV (SPEC_HS_INV_NORMX_v1_2 sect. 5): normX_HS >= max(Cov_inf_lo, 0), since ||X|| >= |<Omega_0, X Omega_0>|."""
    if not (nxh >= (cvl if cvl > 0 else arb(0))):
        raise Refused('C-HS-COV: normX_HS below the Cov_inf_lo lower end')
    return True


def only(tag, fn):
    """v1_34: a plant body that counts only a refusal naming tag; another gate's refusal becomes an error, so the plant does not fire."""
    def g():
        try:
            fn()
        except Refused as e:
            if tag in str(e):
                raise
            raise RuntimeError('refused by another gate: %s' % e)
    return g


NOWRITE = NoWriteFS()   # v1_37 (1): the pre-write cert plants' store, replacing v1_36's nowrite opener


def flag_why(fn):
    """v1_36: (True, '') if fn() returns True, (False, the refusal's text) on a refusal."""
    try:
        return fn() is True, ''
    except Refused as e:
        return False, str(e)


def zero_field(row, fields, name):
    """v1_36 (4): the row (key, value) with its field name set to 0 (PLANT-COV-POS, PLANT-T-POS)."""
    f = row[1].split()
    f[fields.split().index(name)] = '0.0000000000000000e+00'
    return (row[0], ' '.join(f))


def dry_commit(items, readers):
    """v1_37 (1), C-CERT-DRY: the staged writer's success path in a memory store (the review N-2's dry control, no disk write): every export
    staged, checked and renamed; the store then holds exactly the final names, each with the bytes of its cert_text."""
    fs = MemFS()
    shas = cert_write_all(items, readers, fs)
    want = dict((p, cert_text(r, h, w).encode('utf-8')) for p, r, h, w in items)
    if sorted(fs.files) != sorted(want) or any(fs.files[p] != b for p, b in want.items()) or \
            shas != [hashlib.sha256(want[p]).hexdigest() for p, r, h, w in items]:
        raise Refused('C-CERT-DRY: the memory store does not hold exactly the final names with their bytes')
    return True


def cov_lo_bump(L):
    """v1_37 (6): L with the first means row's Cov_inf_lo moved by bump_last_digit (PLANT-COV-SAME)."""
    d, order = kv_parse(L)
    i = d['FIELDS'].split().index('Cov_inf_lo')
    k = [x for x in order if re.fullmatch(r'N[34]_D(?:3|4|4M)_P[0-9]{4}', x)][0]
    f = d[k].split()
    f[i] = bump_last_digit(f[i])
    return [('%s = %s' % (k, ' '.join(f))) if x.startswith(k + ' = ') else x for x in L]


def swap_hilo(x):
    m = re.match(r'^(MOCK RESULT .*?: A_\w+ \[)(\S+), (\S+)(\].*)$', x)
    return '%s%s, %s%s' % (m.group(1), m.group(3), m.group(2), m.group(4)) if m else x


def lower_value(x):
    m = re.match(r'^(MOCK VALUE .*?<= )(\S+)(.*)$', x)
    return '%s%.9e%s' % (m.group(1), float(m.group(2)) / 2, m.group(3)) if m else x


def bump_last_digit(s):
    """the decimal s moved by one unit in its last mantissa digit (the 17th digit of a '%.16e' string)."""
    i = s.find('e')
    j = (i if i >= 0 else len(s)) - 1
    return s[:j] + str((int(s[j]) + 1) % 10) + s[j + 1:]


def flip_row_plant(L):
    """L with the first row's Xtb_lo moved by bump_last_digit."""
    d, order = kv_parse(L)
    ib = d['FIELDS'].split().index('Xtb_lo')
    k = [x for x in order if re.fullmatch(r'N[34]_P[0-9]{4}', x)][0]
    f = d[k].split()
    f[ib] = bump_last_digit(f[ib])
    return [('%s = %s' % (k, ' '.join(f))) if x.startswith(k + ' = ') else x for x in L]


def srcj_down(L):
    """L with the first joint row's pX_hi lowered by 1e-13 relative (PLANT-SRCJ, v1_8 (2))."""
    d, order = kv_parse(L)
    ip = d['FIELDS'].split().index('pX_hi')
    k = [x for x in order if re.fullmatch(r'N[34]_D(?:3|4|4M)_P[0-9]{4}', x)][0]
    f = d[k].split()
    f[ip] = '%.16e' % (float(f[ip]) * (1 - 1e-13))
    return [('%s = %s' % (k, ' '.join(f))) if x.startswith(k + ' = ') else x for x in L]


def run(fails, nofire):
    SELF = sha_file(os.path.abspath(__file__))
    STAGE[0] = 'grid'
    P, gd = read_grid()
    ok = all(len(P[N]) == 904 and P[N][-1][2] == 'inf' and gd.get('N%d_PIECES' % N) == '904' for N in (4, 3)) and \
        all(float(P[N][i][2]) == float(P[N][i + 1][1]) for N in (4, 3) for i in range(903)) and P[4] == P[3] and check_grid_start(P)
    out('C-GRID: %d + %d pieces from %s (FLOAT grid: jlo, jhi only, copied string for string; first jlo >= J_MIN 300), first [%s, %s], last jhi %s -> %s' % (
        len(P[4]), len(P[3]), os.path.basename(GRID), P[4][0][1], P[4][0][2], P[4][-1][2], gate(fails, 'C-GRID', ok)))
    try:
        gex = check_grid_exact(P)   # v1_32 (2)
    except Refused as e:
        gex = str(e)
    out('C-GRID-EXACT: the pieces tile [300, inf) exactly at N = 4 and 3 (first jlo exactly 300, each jhi string the next jlo, binary64 repr ends, last jhi inf): %s -> %s' % (
        'exact' if gex is True else gex, gate(fails, 'C-GRID-EXACT', gex is True)))
    plant(nofire, 'PLANT-GRID-GAP', lambda: check_grid_exact({4: [r if i != 5 else (r[0], r[1], repr(float(r[2]) * (1 + 1e-12))) for i, r in enumerate(P[4])], 3: P[3]}))
    try:
        ghl = check_grid_hull(P, t_ends)   # v1_33 (1)
    except Refused as e:
        ghl = str(e)
    out('C-GRID-HULL: on every piece at N = 4 and 3 the raw t ends hold 1/J for both readings (decimal and binary64) of both ends: %s -> %s' % (
        'yes' if ghl is True else ghl, gate(fails, 'C-GRID-HULL', ghl is True)))
    plant(nofire, 'PLANT-GRID-DEC', lambda: check_grid_hull(P, t_ends_dec))   # v1_33 (1): v1_32's decimal-only ends are refused
    plant(nofire, 'PLANT-GRID-START', lambda: check_grid_start({**P, 4: [(P[4][0][0], '299.0', P[4][0][2])] + P[4][1:]}))   # (3)

    STAGE[0] = 'reader (a)'
    A = {}
    for (k, n) in (() if CERT_MODE else sorted(M_CT)):   # v1_35 (7): reader (a)'s MOCK records, the mock run only
        path = M_CT[(k, n)]
        L = lines_of(path)
        A[(k, n)] = read_kt_cert_g(L, k, n, 'MOCK')
        out('READER-A MOCK %s: %s <= %s (VALUE %s; FLOAT-IN %s) -> read' % (
            os.path.basename(path), NAMES[k], dec_hi(A[(k, n)]['hi']), dec_hi(A[(k, n)]['value_hi']), A[(k, n)]['float_in']))
        plant(nofire, 'PLANT-MOCK-A %s' % os.path.basename(path), lambda L=L, k=k, n=n: read_kt_cert_g(L, k, n, 'CERTIFIED'))
    L = [] if CERT_MODE else lines_of(M_CT[('t', 4)])
    bad_sha = KERNEL_SHA[:-1] + ('0' if KERNEL_SHA[-1] != '0' else '1')
    variants = (
        ('PLANT-A-PRECERT', [x.replace('FORMAT KT_CERT_RECORD_v1_7 MOCK', 'FORMAT KT_CERT_RECORD_v1_7 PRECERT') for x in L]),
        ('PLANT-A-KERNEL', [x.replace(KERNEL_SHA, bad_sha) for x in L]),
        ('PLANT-A-VERDICT2', L + ['VERDICT VALID']),
        ('PLANT-A-HILO', [swap_hilo(x) for x in L]),
        ('PLANT-A-TOKENS', [x.replace('FLOAT-IN far logR gBb eps_r Z', 'FLOAT-IN far logR eps_r Z') for x in L]),
        ('PLANT-A-VALUE', [lower_value(x) for x in L]),
    )
    for nm, V in (() if CERT_MODE else variants):
        if V == L:
            out('%s: the variant equals the record -> DOES NOT FIRE' % nm)
            nofire.append(nm)
            continue
        plant(nofire, nm, lambda V=V: read_kt_cert_g(V, 't', 4, 'MOCK'))

    STAGE[0] = 'reader (a) CERTIFIED'
    AC = {}
    for (k, n) in sorted(REAL_CT):
        path = REAL_CT[(k, n)]
        Lr = lines_of(path)
        try:
            AC[(k, n)] = read_kt_cert_g(Lr, k, n, 'CERTIFIED')
        except Refused as e:
            out('READER-A CERTIFIED %s: refused (%s) -> %s' % (os.path.basename(path), e, gate(fails, 'READER-A CERTIFIED %s%d' % (k, n), False)))
        if (k, n) in AC and (k, n) in A:
            rel = float(abs(AC[(k, n)]['hi'] / A[(k, n)]['hi'] - 1).upper())
            out('READER-A CERTIFIED %s: %s <= %s (VALUE %s; FLOAT-IN %s); the mock hi %s, relative %.2e -> %s' % (
                os.path.basename(path), NAMES[k], dec_hi(AC[(k, n)]['hi']), dec_hi(AC[(k, n)]['value_hi']), AC[(k, n)]['float_in'],
                dec_hi(A[(k, n)]['hi']), rel, gate(fails, 'C-READ-CERT %s%d' % (k, n), rel <= 1e-5)))
        plant(nofire, 'PLANT-A-REAL-AS-MOCK %s' % os.path.basename(path), lambda Lr=Lr, k=k, n=n: read_kt_cert_g(Lr, k, n, 'MOCK'))
    fin = dict(('g.%sn%d' % (k, n), AC[(k, n)]['float_in'].split()) for (k, n) in AC)
    st, named = export_status(dict(fin, kt_p2_assembly=OWN_FLOAT_JT))
    out('C-FLOATIN: the four kt_cert_v1_7 records and the assembly own list give the certified-path status %s with FLOAT-IN %s -> %s' % (
        st, named, gate(fails, 'C-FLOATIN', len(fin) == 4 and st == 'CERTIFIED_GIVEN_FLOAT_IN')))
    st0, named0 = export_status(dict((x, []) for x in fin))
    out('C-FLOATIN-EMPTY: empty FLOAT-IN lists give %s (FLOAT_IN %s) -> %s' % (st0, named0, gate(fails, 'C-FLOATIN-EMPTY', st0 == 'CERTIFIED')))
    sto, namedo = export_status(dict([(x, []) for x in fin] + [('kt_p2_assembly', OWN_FLOAT_TP)]))
    out('C-FLOATIN-OWN: with the four record lists empty, the t export own FLOAT list is empty from v1_35 (tz by the odd Ritz route), so it reads %s (FLOAT_IN %s) -> %s' % (
        sto, namedo, gate(fails, 'C-FLOATIN-OWN', OWN_FLOAT_TP == [] and sto == 'CERTIFIED')))
    plant(nofire, 'PLANT-FLOATIN-OWN', lambda: certified_tag(dict([(x, []) for x in fin] + [('kt_p2_assembly', ['tz'])])))   # v1_35 (2): the pre-v1_35 own list, still refused
    stj, _nj = export_status(dict([(x, []) for x in fin] + [('kt_p2_assembly', OWN_FLOAT_JT)]))   # v1_25 (1)
    out('C-FLOATIN-JT: the joint export own FLOAT list is empty (eps_r and s come from the certified M2B record), so with the four record lists empty it reads %s -> %s' % (
        stj, gate(fails, 'C-FLOATIN-JT', OWN_FLOAT_JT == [] and stj == 'CERTIFIED')))
    sto2, _n2 = export_status(dict((x, []) for x in fin), OPEN_CONDITIONS)
    out('C-OPEN: with every FLOAT-IN list empty, the open condition C1 still gives %s -> %s' % (
        sto2, gate(fails, 'C-OPEN', sto2 == 'CERTIFIED_GIVEN_OPEN_CONDITIONS')))
    plant(nofire, 'PLANT-OPEN-C1', lambda: certified_tag(dict((x, []) for x in fin), OPEN_CONDITIONS))
    c1ok = check_c1(['FORMAT = M2B_KV_v1', 'CLAIM = MOCK certified eps_r bound: ' + C1_CLAIM + ' (unit test)'])
    M2R, M2MOD, M2BL = load_m2b()   # v1_25 (1), (2): the M2(b) reader; check_c1 runs inside it on the pinned record lines
    c1live = open_conditions(M2BL) == {}
    out('C-C1: a CLAIM line holding the agreed %d-byte |g| string exactly once clears C1 (unit test), and the pinned M2B record %s (%s) has one CLAIM line holding it exactly once, so C1 is cleared and the exports carry OPEN_CONDITIONS none (live) -> %s' % (
        len(C1_CLAIM.encode('utf-8')), os.path.basename(M2B[0]), PINS[M2B[0]][:8], gate(fails, 'C-C1', c1ok is True and open_conditions(['CLAIM = x ' + C1_CLAIM]) == {} and 'C1' in open_conditions() and c1live)))
    plant(nofire, 'PLANT-C1-NOSPACE', lambda: check_c1(['CLAIM = MOCK ' + C1_NOSPACE]))
    plant(nofire, 'PLANT-C1-TWICE', lambda: check_c1(['CLAIM = ' + C1_CLAIM + ' and ' + C1_CLAIM]))
    plant(nofire, 'PLANT-C1-LIVE-NOSPACE', lambda: check_c1([x.replace(C1_CLAIM, C1_NOSPACE) for x in M2BL]))   # v1_25 (2)
    plant(nofire, 'PLANT-M2B-PIN', lambda: load_m2b(dict(PINS, **{M2B[0]: '0' * 64})))   # v1_25 (1): a file failing its pin is refused
    plant(nofire, 'PLANT-M2B-ASM-PIN', lambda: load_m2b(dict(PINS, **{M2B[1]: '0' * 64})))
    plant(nofire, 'PLANT-M2B-READER-PIN', lambda: load_m2b(dict(PINS, **{M2B_READER_PATH: '0' * 64})))
    M2TXT, M2ATX = '\n'.join(M2BL), '\n'.join(lines_of(M2B[1]))
    plant(nofire, 'PLANT-M2B-MOCKFORMAT', lambda: m2b_reader_plant(M2MOD.check, M2TXT.replace('FORMAT = M2B_KV_v1', 'FORMAT = M2B_KV_v1 MOCK')))
    plant(nofire, 'PLANT-M2B-BIND', lambda: m2b_reader_plant(M2MOD.loads, M2TXT.replace('AUTHOR = pk02', 'AUTHOR = pk01_x'), os.path.basename(M2B[0]), M2ATX))
    plant(nofire, 'PLANT-M2B-INF', lambda: m2b_eps({'eps_r': '1e-6', 's': 'inf'}))
    plant(nofire, 'PLANT-FLOATIN-CERT', lambda: certified_tag(fin))
    FINM = {'M4_KV_v1': []}   # v1_32 (1): A_t and A_am come from the M4 record (FLOAT-IN none); reader (a)'s lists stay in C-FLOATIN's unit checks
    FIN_JT = export_status(dict(FINM, kt_p2_assembly=OWN_FLOAT_JT))[1]
    FIN_TP = export_status(dict(FINM, kt_p2_assembly=OWN_FLOAT_TP))[1]

    STAGE[0] = 'reader (d)'
    Lk = [] if CERT_MODE else lines_of(M_IN)   # v1_35 (7): reader (d), the mock run only
    if not CERT_MODE: read_kv(Lk, 'MOCK', 'MOCK_S9B_INPUTS_v1')
    if not CERT_MODE: out('READER-D MOCK %s: accepted' % os.path.basename(M_IN))
    if not CERT_MODE: plant(nofire, 'PLANT-MOCK-D %s' % os.path.basename(M_IN), lambda: read_kv(Lk, 'CERTIFIED', 'MOCK_S9B_INPUTS_v1'))
    variants = (
        ('PLANT-D-PRECERT', [x.replace('TAG = MOCK', 'TAG = MOCK PRECERT') for x in Lk]),
        ('PLANT-D-DUPKEY', Lk + ['RUN_VERDICT = VALID']),
        ('PLANT-D-BARE', Lk[:-2] + ['VERDICT VALID'] + Lk[-2:]),
        ('PLANT-D-END', [x.replace('END = MOCK_S9B_INPUTS_v1', 'END = MOCK_OTHER') for x in Lk]),
        ('PLANT-D-KERNEL', [x.replace(KERNEL_SHA, bad_sha) for x in Lk]),
        ('PLANT-KEYCASE', [x.replace('N4_MHAT = ', 'N4_mhat = ') for x in Lk]),
    )
    for nm, V in (() if CERT_MODE else variants):
        if V == Lk:
            out('%s: the variant equals the record -> DOES NOT FIRE' % nm)
            nofire.append(nm)
            continue
        plant(nofire, nm, lambda V=V: read_kv(V, 'MOCK', 'MOCK_S9B_INPUTS_v1'))

    STAGE[0] = 'readers (b), (c)'
    EA = dict((N, load_setac(M_M3, N, 'MOCK' if MOCK_SETAC else 'CERTIFIED')) for N in (4, 3))   # v1_35 (1): Sets A, C and W
    E = dict((N, moments_of(EA[N])[0]) for N in (4, 3))   # v1_35 (1): the 27 window moments by KEYMAP, M4M := M4
    EX = dict((N, moments_of(EA[N])[1]) for N in (4, 3))   # v1_35 (1): W1, W2, IHZ, IHZB, IHZH
    SETAC_STATUS = 'MOCK' if MOCK_SETAC else 'CERTIFIED'   # v1_35 (2): the status of Sets A, C and W for M4SRC (CERTIFIED once the certified path reads them, R4)
    I = None if CERT_MODE else dict((N, load_inputs(M_IN, N, 'MOCK')) for N in (4, 3))   # v1_35 (7): no I[N] in cert mode
    EPSV = dict((N, m2b_call(M2MOD.law_v1, M2R, N, 300)) for N in (4, 3))   # v1_25 (1): LAW v1 at J = 300 (upper ends; nonincreasing in J on [300, oo))
    EPSC = dict((N, m2b_eps(EPSV[N])) for N in (4, 3))   # (eps_r, s, s-prime = s (1 + s)) as arb balls
    rk = dict(x.split(' = ', 1) for x in M2BL if (' = ' in x) and not x.startswith('#'))
    m2mono = all(float(m2b_call(M2MOD.law_v1, M2R, N, J2)[k]) <= float(m2b_call(M2MOD.law_v1, M2R, N, J1)[k]) for N in (4, 3) for (J1, J2) in ((300, 600), (600, 3000), (3000, 10 ** 6)) for k in ('eps_r', 's'))
    m2ok = m2mono and (rk.get('ASM_SHA256') == PINS[M2B_ASM_PATH]) and all(
        abs(float(EPSV[N][k]) / float(rk['N%d_%s_300' % (N, kk)]) - 1) <= 1e-9 for N in (4, 3) for (k, kk) in (('eps_r', 'EPS_R'), ('s', 'S')))
    out('C-M2B: %s (%s) through m2b_reader_v1 (%s; binding to %s, record checks, C-PINS): law_v1 at J = 300 equals N*_EPS_R_300 and N*_S_300 within 1e-9, decreases from J = 300 to 600, 3000 and 10^6, and ASM_SHA256 is the pinned m2b_asm_v1.py -> %s' % (
        os.path.basename(M2B[0]), PINS[M2B[0]][:8], PINS[M2B_READER_PATH][:8], os.path.basename(M2B[1]), gate(fails, 'C-M2B', m2ok)))
    out('C-M2B-TRIAL: the record PIN_TRIAL names the vacres files the assembly pins for S_eps with their full sha256 (%s, %s) -> %s' % (
        PINS[VACRES[4]][:8], PINS[VACRES[3]][:8], gate(fails, 'C-M2B-TRIAL', check_m2b_trial(M2BL) is True)))   # (2)
    plant(nofire, 'PLANT-M2B-TRIAL', lambda: check_m2b_trial([x.replace(PINS[VACRES[4]], PINS[VACRES[3]]) if x.startswith('PIN_TRIAL = ') else x for x in M2BL]))
    p0_ = ctx.prec
    ctx.prec = 64
    try:
        e64 = dict((N, m2b_call(M2MOD.law_v1, M2R, N, 300)) for N in (4, 3))   # (4)
    finally:
        ctx.prec = p0_
    out('C-M2B-PREC: reader calls run at ctx.prec %d whatever the caller sets: law_v1 at J = 300 called from ctx.prec 64 equals the run value at both N, and the caller precision is restored -> %s' % (
        M2B_PREC, gate(fails, 'C-M2B-PREC', all(e64[N] == EPSV[N] for N in (4, 3)) and ctx.prec == p0_)))
    plant(nofire, 'PLANT-M2B-PREC', lambda: m2b_call(setattr, ctx, 'prec', 64))   # a reader call that changes the precision is refused
    for N in (() if CERT_MODE else (4, 3)):
        out('INFO M2B N=%d: certified eps_r <= %s and s <= %s at J = 300 (s-prime <= %s), used by the joint path; the t path keeps the mock kt_rb floats eps_r %s and s-prime %s' % (
            N, EPSV[N]['eps_r'], EPSV[N]['s'], dec_hi(EPSC[N][2]), dec_hi(I[N]['eps_r']), dec_hi(I[N]['sp'])))
    MC = dict((N, m2b_mhat_coeffs(lines_of(M2B[1]), N)) for N in (4, 3))   # (1): the M2(b) record's own m1..m3 (its asm output's C-MHAT)
    MH = dict((N, mhat_lower(MC[N], 1 / arb(300))) for N in (4, 3))   # the arb lower end of mhat at J = 300
    MHUP = dict((N, arb(rk['N%d_MHAT_UP' % N])) for N in (4, 3))   # the record's MHAT_UP
    mcv = all(MC[N] == vacres_m(VACRES[N]) for N in (4, 3))   # the same m as the pinned vacres files of S_eps
    if not CERT_MODE: out('C-TP-DOM: the t path keeps the mock eps_r and s-prime beside the M2B kappa only while they lie at or above the M2B ends, and the mock lt0 at or below (1 - eps_r) mhat_lo at J = 300 (m1..m3 from the M2B asm C-MHAT, equal to the pinned vacres m: %s; mhat_lo N4 %s, N3 %s against MHAT_UP N4 %s, N3 %s; the bound N4 %s, N3 %s; mock lt0 N4 %s, N3 %s) -> %s' % (
        mcv, dec_lo(MH[4]), dec_lo(MH[3]), dec_hi(MHUP[4]), dec_hi(MHUP[3]), dec_lo((1 - EPSC[4][0]) * MH[4]), dec_lo((1 - EPSC[3][0]) * MH[3]),
        dec_hi(I[4]['lt0']), dec_hi(I[3]['lt0']), gate(fails, 'C-TP-DOM', mcv and check_tp_dom(I, EPSC, MH, MHUP) is True)))   # (1)
    if not CERT_MODE: plant(nofire, 'PLANT-TP-DOM-EPS', lambda: check_tp_dom({N: dict(I[N], eps_r=EPSC[N][0] / 2) for N in (4, 3)}, EPSC, MH, MHUP))   # one plant per condition
    if not CERT_MODE: plant(nofire, 'PLANT-TP-DOM-SP', lambda: check_tp_dom({N: dict(I[N], sp=EPSC[N][2] / 2) for N in (4, 3)}, EPSC, MH, MHUP))
    if not CERT_MODE: plant(nofire, 'PLANT-TP-DOM-LT0', lambda: check_tp_dom({N: dict(I[N], lt0=MH[N]) for N in (4, 3)}, EPSC, MH, MHUP))
    if not CERT_MODE: plant(nofire, 'PLANT-TP-DOM-MOCKMHAT', lambda: check_tp_dom(I, EPSC, dict((N, I[N]['mhat']) for N in (4, 3)), MHUP))   # the mock mhat key must fail
    plant(nofire, 'PLANT-TP-MHAT-SRC', lambda: m2b_mhat_coeffs([x for x in lines_of(M2B[1]) if not x.startswith('C-MHAT N=4')], 4))
    KAPB = dict((N, kappa_bound(N, EPSC[N][0])) for N in (4, 3))   # v1_9 (1), v1_25 (1): the certified eps_r
    for N in (() if CERT_MODE else (4, 3)):
        I[N]['HbadP'] = tail_h(N, 1, I[N]['Lam'], arb(0)) * KAPB[N] * KAPB[N]   # v1_9 (2): Hbad' = tau~0(Lam) kappa^2
        out('INFO HBAD\' N=%d: Hbad\' = tau~0(%s) kappa_max^2 <= %s (kt_rb\'s Hbad, mock x1.03: %s); NH\' = Lam + Hbad\' <= %s; J-uniform given kappa' % (
            N, I[N]['Lam'].str(3, radius=False), dec_hi(I[N]['HbadP']), dec_hi(I[N]['Hbad']), dec_hi(I[N]['Lam'] + I[N]['HbadP'])))
    if not CERT_MODE: out('READER-B MOCK %s: %d + %d entries; READER-C MOCK %s: %d keys per N -> read' % (
        os.path.basename(M_M3), len(E[4]), len(E[3]), os.path.basename(M_IN), len(INKEYS)))
    plant(nofire, 'PLANT-A-BIND-PIN', only('C-A-BIND', lambda: load_setac(M_M3, 4, 'CERTIFIED', pins=dict(PINS, **{SETAC_RECORDS[4][0][1]: '0' * 64}))))   # v1_37 (7): replaces PLANT-MOCK-B, which the R4 pins turned into an accepted call; refused before any read
    plant(nofire, 'PLANT-A-BIND-ASM-PIN', only('C-A-BIND', lambda: load_setac(M_M3, 4, 'CERTIFIED', pins=dict(PINS, **{SETAC_RECORDS[4][0][2]: '0' * 64}))))   # v1_37 (7): the asm output pin
    plant(nofire, 'PLANT-MOCK-C %s' % os.path.basename(M_IN), lambda: load_inputs(M_IN, 4, 'CERTIFIED'))
    plant(nofire, 'PLANT-CERT-NOI', only('C-CERT-NOI', lambda: load_inputs(M_IN, 4, 'MOCK', cert=True)))   # v1_35 (7)
    LM3 = lines_of(M_M3)   # v1_35 (1): reader (b2)'s gates and their plants
    RL = run_list()
    out('C-A-LIST: P2_RUN_LIST_v1_10 (%s) holds exactly the 23 keys; MOCK_M3_ENTRIES_v2 is built on it; each certified record must name it in entry_list (C-A-BIND path) -> %s' % (
        PINS[RUN_LIST][:8], gate(fails, 'C-A-LIST', len(RL) == len(RUN_KEYS))))
    out('C-A-COUNT: %s carries exactly the %d run-list keys at both N (no other N_ key) -> %s' % (
        os.path.basename(M_M3), len(RUN_KEYS), gate(fails, 'C-A-COUNT', all(sorted(EA[N]) == sorted(RUN_KEYS) for N in (4, 3)))))
    plant(nofire, 'PLANT-A-DROP', only('C-A-COUNT', lambda: load_setac(M_M3, 4, 'MOCK', lines=[x for x in LM3 if not x.startswith('N4_Y4 = ')])))
    plant(nofire, 'PLANT-A-EXTRA', only('C-A-COUNT', lambda: load_setac(M_M3, 4, 'MOCK', lines=[y for x in LM3 for y in (['N4_UL3 = 2 1 0 0 0', x] if x.startswith('END = ') else [x])])))
    out('C-A-MAP: every slot of the key map against the pinned run list (graph, end factors, i T-factors, j B- or MB-factors, nothing else; each slot once; Sets C and W by graph and factor list) -> %s' % gate(
        fails, 'C-A-MAP', flag(lambda: check_amap(RL, KEYMAP))))
    plant(nofire, 'PLANT-A-MAP-SWAP', only('C-A-MAP', lambda: check_amap(RL, dict(KEYMAP, **{'SM4,2,0': 'M4_02', 'SM4,0,2': 'M4_20'}))))
    out('C-A-MIRROR: M4M_ij is M4_ij (the same object) for every ij at both N, and no record key carries M4M -> %s' % gate(
        fails, 'C-A-MIRROR', all(E[N]['M4M_' + ij] is E[N]['M4_' + ij] for N in (4, 3) for ij in ('00', '10', '01', '20', '02', '11', '21', '12', '22'))))
    out('C-A-V63: S7 g,0,0 through m3_reader_v6_3 (%s) equals m3_reader_v4_4 ball for ball at both N (the certified path control) -> %s' % (
        PINS[M3R6_PATH][:8], gate(fails, 'C-A-V63', all(flag(lambda N=N: m3r6_control(N)) for N in (4, 3)))))
    plant(nofire, 'PLANT-A-BIND-PRECERT', only('C-A-BIND', lambda: m3r6_bind_text(3, 'VERDICT VALID-PRECERT')))
    plant(nofire, 'PLANT-A-LAYER', only('carries the layer', lambda: check_setac_layer(m3r6_mod().load(S7G00[3][0], S7G00[3][1], 300, 3)['top'],
                                                                                         os.path.basename(S7G00[3][0]))))   # v1_36 (3): S7's record through v6_3 (layer arbeng_ma_v1_3)
    plant(nofire, 'PLANT-A-COUNT-FAM', only('C-A-COUNT', lambda: check_setac_count([k for k in RUN_KEYS if RL[k]['graph'] == 'NTB'], 'DT', RL, 'the NTB key set')))   # v1_36 (3)
    FAM = dict((X, [k for k in RUN_KEYS if RL[k]['graph'] == X]) for X in SETAC_FAMS)
    out('C-A-PERREC (controls): each family\'s own run-list key set passes check_setac_count, the seven sets cover the %d keys once, and a top naming the pinned run list passes check_setac_list -> %s' % (
        len(RUN_KEYS), gate(fails, 'C-A-PERREC', all(flag(lambda X=X: check_setac_count(FAM[X], X, RL, X)) for X in SETAC_FAMS)
                            and sorted(k for X in SETAC_FAMS for k in FAM[X]) == sorted(RUN_KEYS)
                            and flag(lambda: check_setac_list({'entry_list': '%s:%s' % (os.path.basename(RUN_LIST), PINS[RUN_LIST])})))))
    out('INFO C-A-BIND/C-A-TRIAL/A-PARTITION: the certified path of reader (b2) (seven records per N through m3_reader_v6_3, layer %s %s) reads only the v1_10_4 files pinned at R4 and refuses one that fails its pin (PLANT-A-BIND-PIN, PLANT-A-BIND-ASM-PIN); the MOCK records carry no partition field' % M3R6_LAYER)

    STAGE[0] = 'Lemma G'
    QT = dict((N, load_trial_q(VACRES[N], N)) for N in (4, 3))   # v1_12 (1): reader (f)
    G00 = load_g00('CERTIFIED')   # v1_17 (1), v1_20 (1): S7's certified g,0,0, Lemma T-prime's only J-dependent input
    STAGE[0] = 'S8 and the aliases (v1_35)'
    G22E = dict((N, load_m3(S8D[N][0], N, 'CERTIFIED', 300, S8D[N][1])['g,2,2']) for N in (4, 3))   # v1_35 (2): S8's certified g,2,2
    T22E = dict((N, load_m3(S8N[N][0], N, 'CERTIFIED', 300, S8N[N][1])['T,2,2']) for N in (4, 3))   # v1_35 (2): T,2,2 (INFO mu_z)
    TBE = dict((N, load_m3(S7G00[N][0], N, 'CERTIFIED', 300, S7G00[N][1])['A,0']) for N in (4, 3))   # v1_35 (3): Tb := S7 A,0
    S8T = {}
    for N in (4, 3):
        for p in (S8D[N][0], S8N[N][0]):
            with open(p) as fh:
                S8T[(N, p)] = json.load(fh)
    out('C-C-TRIAL: the four S8 records (D: %s %s; N: %s %s) name the pinned ts and vacres files with their full sha256 -> %s' % (
        PINS[S8D[4][0]][:8], PINS[S8D[3][0]][:8], PINS[S8N[4][0]][:8], PINS[S8N[3][0]][:8], gate(
            fails, 'C-C-TRIAL', all(flag(lambda r=r, N=k[0]: check_trial_full(r, N, tag='C-C-TRIAL')) for k, r in S8T.items()))))
    plant(nofire, 'PLANT-C-TRIAL', only('C-C-TRIAL', lambda: check_trial_full(S8T[(3, S8D[3][0])], 4, tag='C-C-TRIAL')))
    plant(nofire, 'PLANT-A-LIST-S8', only('C-A-LIST', lambda: check_setac_list(S8T[(4, S8D[4][0])])))   # v1_36 (3): an S8 record names S8's entry list
    t300 = 1 / arb(300)
    for N in (4, 3):
        g22, t22 = entry_piece(G22E[N], t300), entry_piece(T22E[N], t300)
        out('INFO ROW2 N=%d: S8 g,2,2 %s, T,2,2 %s at J = 300; mu_z = T,2,2/g,2,2 %s (m3_s8v3 D %s, N %s)' % (
            N, g22.str(8, radius=False), t22.str(8, radius=False), (t22 / g22).str(6, radius=False), PINS[S8D[N][0]][:8], PINS[S8N[N][0]][:8]))
    zf = all(all((a + b).lower() <= 0 and (a + b).upper() >= 0 for a, b in zip(EX[N]['IHZB'][0], EX[N]['IHZ'][0])) for N in (4, 3))
    out('C-ZFLIP: IhZb = -IhZ (each coefficient ball of IhZb + IhZ contains 0) at both N -> %s' % gate(fails, 'C-ZFLIP', zf))
    zp = all(all(a == 0 for a in EX[N]['IHZH'][0]) and EX[N]['IHZH'][1] == 0 for N in (4, 3))
    out('C-ZPAR: IhZh is an exact parity zero (every coefficient and the bar exactly 0) at both N -> %s' % gate(fails, 'C-ZPAR', zp))
    out('C-G22-POS: g,2,2 certainly > 0 at J = 300, both N (and per piece in tz_odd) -> %s' % gate(
        fails, 'C-G22-POS', all(entry_piece(G22E[N], t300) > 0 for N in (4, 3))))
    plant(nofire, 'PLANT-G22-POS', only('C-G22-POS', lambda: tz_odd(arb(1), {'G': [[arb(1)]], 'vals': [arb(1)]}, arb(1), arb(0, 1) * arb('1e-3'), arb(0), arb(0), arb(0), arb(0), arb(1))))
    M3E = load_m3e()   # v1_35 (3): the alias checks
    ENCS = alias_encs()
    for N in (4, 3):
        out('C-ALIAS-MIRROR N=%d: IhTt,0 = [cp0 col 0, xia [3,0,1], cp0 col 2] is the exact mirror image of S9 Iht,0 %s (c_mirror on N) -> %s' % (
            N, ENCS[0], gate(fails, 'C-ALIAS-MIRROR N=%d' % N, flag(lambda: c_alias_mirror(M3E, N, ENCS)))))
        out('C-ALIAS-FLIP N=%d: Tb %s = S7 A,0 %s under T <-> B ((i) automorphism, (ii) even ends, (iii) PERM9 on the middle c9, (iv) main_N) -> %s' % (
            N, ENCS[2], ENCS[1], gate(fails, 'C-ALIAS-FLIP N=%d' % N, flag(lambda: c_alias_flip(M3E, N, ENCS)))))
    plant(nofire, 'PLANT-ALIAS-MIDROW', only('C-ALIAS-MIRROR', lambda: c_alias_mirror(M3E, 4, ENCS, alias=[['cp', 0, 0], ['xia', [4, 1, 2]], ['cp', 0, 2]])))
    plant(nofire, 'PLANT-ALIAS-CP1', only('C-ALIAS-MIRROR', lambda: c_alias_mirror(M3E, 4, ENCS, alias=[['cp', 1, 0], ['xia', [3, 0, 1]], ['cp', 0, 2]])))
    plant(nofire, 'PLANT-ALIAS-QSHIFT', only('C-ALIAS-FLIP (ii)', lambda: c_alias_flip(M3E, 4, ENCS, q_shift=1e-12)))
    plant(nofire, 'PLANT-ALIAS-TB', only('C-ALIAS-FLIP (iii)', lambda: c_alias_flip(M3E, 4, ENCS, tb_mid=('xi', (3, 4, 5), 0.0, [0.0, 0.0, 1.0] + [0.0] * 6))))
    STAGE[0] = 'Lemma G'
    g7ok, G7 = True, {}   # v1_19 (2): the S7 certified g,0,0 (pk03: the same object as S9's G,0,0), read through m3_reader_v4_4
    for N in (4, 3):
        rp, ap = S7G00[N]
        cf7, er7 = load_m3(rp, N, 'CERTIFIED', 300, ap)['g,0,0']
        with open(rp) as fh:
            r7 = json.load(fh)
        check_g00_entry(r7['claim'], r7['items']['g,0,0']['a0_exact'], cf7[0].lower(), cf7[0].upper())
        gm = check_g00(g00_lower(cf7, er7, 1 / arb(300)))
        v300 = arb(0)
        for a in reversed(cf7):
            v300 = v300 * (1 / arb(300)) + a
        G7[N] = (gm, v300, er7, r7)
        g7ok = g7ok and (gm > arb('0.95')) and (gm < arb('1.05'))
        g7ok = g7ok and (gm == G00[N])   # v1_20 (1): the lower end Phi uses
        out('INFO G00-S7 N=%d: %s g,0,0 through m3_reader_v4_4: a0_exact %s, err %s; lower end over every J >= 300 (t in [0, 1/300]) %s; at J = 300 %s (value_ref %s)' % (
            N, os.path.basename(rp), r7['items']['g,0,0']['a0_exact'], dec_hi(er7), dec_lo(gm), v300.str(12, radius=False), r7['items']['g,0,0']['value_ref']))
    out('C-G00-S7: the S7 certified g,0,0 matches the normalization pin, and its lower end over every J >= 300 lies within 5%% of 1 at both N (Phi takes this lower end) -> %s' % gate(
        fails, 'C-G00-S7', g7ok))
    tsok = all(check_trial_set(G7[N][3], N) is True for N in (4, 3))   # v1_25 (3)
    out('C-G00-TRIAL: each S7 record trial_set names the vacres file the assembly pins for S_eps (%s; %s); g00_s7 checks it too -> %s' % (
        G7[4][3]['trial_set']['vacres'], G7[3][3]['trial_set']['vacres'], gate(fails, 'C-G00-TRIAL', tsok)))
    plant(nofire, 'PLANT-G00-TRIAL', lambda: check_trial_set(dict(G7[4][3], trial_set=dict(G7[4][3]['trial_set'], vacres=G7[3][3]['trial_set']['vacres'])), 4))
    plant(nofire, 'PLANT-G00-A0EXACT', lambda: check_g00_entry(G7[4][3]['claim'], '2', arb(1), arb(1)))   # v1_25 (4): one plant per condition
    plant(nofire, 'PLANT-G00-A0BALL', lambda: check_g00_entry(G7[4][3]['claim'], '1', arb(2), arb(2)))
    plant(nofire, 'PLANT-G00-NORM', lambda: check_g00_entry(G7[4][3]['claim'], '2', arb(2), arb(2)))
    plant(nofire, 'PLANT-G00-CLAIM', lambda: check_g00_entry(G7[4][3]['claim'].replace('I(J)/main(J)', 'I(J)/main_T(J)'), '1', arb(1), arb(1)))
    epsg, thg = arb(EPS_G), arb(THETA_G)
    w0, we, wt = lg_weights(epsg, thg)
    LG = {}
    sok, jok, kok, zok, gok = True, True, True, True, True
    for N in (4, 3):
        In = None if CERT_MODE else I[N]
        S = s_eps(QT[N], epsg, 1 / arb(300))
        sk = supp0_kt(QT[N], arb(300))
        sok = sok and (S < sk) and (abs(S - arb(SEPS_FLOAT[N])) < arb('2e-6'))
        for w in (w0, we, wt):
            jok = jok and (abs(phi_main(N, w, arb(3000)) / phi_main(N, w, arb(300)) - 1) < arb('1e-12'))   # v1_13: the A, B hulls (about 1e-16) enter both J
        jok = jok and (abs(jfac(N, arb(3000)) / jfac(N, arb(300)) - 1) < arb('1e-40'))   # v1_13: the J-dependent factor alone
        kr = k1_lim(N, arb(300)) / k1_exact(N, arb(300))
        if N == 4:
            kok = kok and all(k1_exact(N, arb(J)) < k1_lim(N, arb(J)) for J in (300, 3000))
        gr = None if CERT_MODE else In['Gbad'] / In['Hbad']
        zr0 = None if CERT_MODE else gr * gr / (arb(SUPP0_MOCK[N]) * arb(SUPP0_MOCK[N]) * phi_main(N, w0, arb(300)))
        zok = zok and (CERT_MODE or ((zr0 > arb('0.5')) and (zr0 < 2)))
        g00 = check_g00(G00[N])   # v1_17 (1): Lemma T-prime replaces the remainder ratios
        u = None if CERT_MODE else 1 / (1 - In['eps_r'])
        pe, pt = phi_T(N, S, we, g00), phi_T(N, S, wt, g00)
        if not CERT_MODE: In['GbadP'] = gbad_p(N, In['Lam'], KAPB[N], u, pe)
        if not CERT_MODE: In['AbadP'] = abad_p(In['Lam_a'], KAPB[N], u, pe, pt, epsg, thg)
        LG[N] = {'S': S, 'g00': g00, 'pe': pe, 'theta': THETA_G}   # v1_14 (1), v1_15 (1): for Lemma E-prime, and the theta Abad-prime used
        out('PHI-EPS N=%d (Lemma T-prime, eps %s, S7 certified G_00): S_eps <= %s, G_00 >= %s, Phi_eps <= %s, Phi_eps,theta <= %s' % (N, EPS_G, dec_hi(S), dec_lo(g00), dec_hi(pe), dec_hi(pt)))   # v1_37_1 (1): every mode (pk11 R6.5)
        gok = gok and (CERT_MODE or ((In['GbadP'] < In['Gbad']) and (In['AbadP'] < In['Abad'])))
        if not CERT_MODE: out('INFO LEMMA-G N=%d (eps %s, theta %s): S_eps <= %s (supp0 on the same q %s); kt_rb ratio (comparison only, not an input) %s, G_00 %s (S7 certified lower end; Lemma T-prime); Phi_eps <= %s, Phi_eps,theta <= %s; '
            'Gbad-prime(%s) <= %s (kt_rb Gbad %s); Abad-prime(%s) <= %s (kt_rb Abad %s); (k1_lim/k1)^3 at J = 300: %s' % (
                N, EPS_G, THETA_G, dec_hi(S), dec_hi(sk), dec_hi(zr0), dec_hi(g00), dec_hi(pe), dec_hi(pt), In['Lam'].str(3, radius=False), dec_hi(In['GbadP']),
                dec_hi(In['Gbad']), In['Lam_a'].str(3, radius=False), dec_hi(In['AbadP']), dec_hi(In['Abad']), dec_hi(kr * kr * kr)))
    out('C-SEPS: S_eps (G3, z9sym q, t = 1/300) below supp0 on the same q and within 2e-6 of seps_v1 FLOAT, both N -> %s' % gate(fails, 'C-SEPS', sok))
    out('C-JPOW: jfac = k1_lim^3 (2 pi/J)^(-3n/2) at J = 3000 against J = 300 below 1e-40, and k1_lim^3 main_T/main_D for the three weight sets below 1e-12 (A, B hulls), both N (the J-powers cancel) -> %s' % gate(
        fails, 'C-JPOW', jok))
    out('C-K1-LIM: k1 < k1_lim at N = 4, J = 300 and 3000 (I_1 series; N = 3 exact) -> %s' % gate(fails, 'C-K1-LIM', kok))
    if not CERT_MODE: out('C-ZR0 (comparison only, not an input): MOCK Z_T/Z_psi backed out of kt_rb Gbad/Hbad lies in 0.5..2 at both N (the main terms against kt_rb phi ratio) -> %s' % gate(
        fails, 'C-ZR0', zok))
    if not CERT_MODE: out('C-GBADP: Gbad-prime < kt_rb Gbad and Abad-prime < kt_rb Abad at both N -> %s' % gate(fails, 'C-GBADP', gok))
    plant(nofire, 'PLANT-GBADP-LEVEL', lambda: gbad_p(4, arb('0.5'), KAPB[4], arb(1), arb(1)))
    plant(nofire, 'PLANT-ABADP-LEVEL', lambda: abad_p(arb('0.5'), KAPB[4], arb(1), arb(1), arb(1), epsg, thg))
    plant(nofire, 'PLANT-SEPS-EPS', lambda: s_eps(QT[4], arb(1), 1 / arb(300)))

    STAGE[0] = 'formulas'
    need('formulas')
    T = {}
    for N in (() if CERT_MODE else (4, 3)):   # v1_35 (7): the mock-input J = 300 row, the mock run only
        T[N] = tprov(A[('t', N)]['hi'], I[N])
        Q = qv4(A[('t', N)]['hi'], dict((k, v) for k, v in I[N].items() if k != 'GbadP'))   # v1_12 (3): C-QV4 on kt_rb's Gbad
        dq = abs(Q / arb(FLOATQ[N]) - 1).upper()
        out('C-QV4 N=%d: ||Q_4 v_t|| <= %s against the float reading %s: relative %.2e -> %s' % (
            N, dec_hi(Q), FLOATQ[N], float(dq), gate(fails, 'C-QV4 N=%d' % N, dq <= 5e-4)))
        out('INFO QV4-GBADP N=%d: ||Q_4 v_t|| with Gbad-prime (Lemma G) <= %s; with kt_rb Gbad %s' % (N, dec_hi(T[N]['Q']), dec_hi(Q)))
        if ('t', N) in AC:
            out('INFO QV4-CERT-A N=%d: ||Q_4 v_t|| with the certified A_t and the MOCK inputs <= %s (with the mock A_t: %s); a MOCK reading' % (
                N, dec_hi(qv4(AC[('t', N)]['hi'], I[N])), dec_hi(T[N]['Q'])))
        at, dtx = T[N]['At'].lower(), T[N]['dtx'].upper()
        diff = T[N]['Vt'].upper() - at * at
        corr = abs(T[N]['Vt'] - T[N]['Q'] * T[N]['Q'] - (I[N]['tx'] * I[N]['tx'] + I[N]['ty'] * I[N]['ty'])).upper()
        ok = T[N]['Pt2'].upper() <= diff + dtx * dtx + 2 * corr + arb('1e-30') and at > 0
        out('C-PT N=%d: joint Pt^2 <= %s, difference route V_t - A_t^2 <= %s (identity: they differ by dtx^2 and the Gram terms) -> %s' % (
            N, dec_hi(T[N]['Pt2']), dec_hi(diff), gate(fails, 'C-PT N=%d' % N, ok)))
        out('INFO C7 N=%d: A_t >= %s, O_t <= %s, A_t^2/O_t >= %.4f (claim 1.05); X_ta >= %s' % (
            N, dec_lo(T[N]['At']), dec_hi(T[N]['Ot']), float((at * at / T[N]['Ot'].upper()).lower()), dec_lo(T[N]['Xta'])))
        out('INFO R_c^ta N=%d: computed %s (this run\'s delta t_x), input %s (kt_sh1_v1\'s line); X_tb := X_ta (XTB_SOURCE = FLIP_OF_XTA)' % (
            N, dec_hi(T[N]['Rcta']), dec_hi(I[N]['Rcta'])))
        try:
            Lc, b0, b1, dsup = width_corner(T[N]['At'].lower(), T[N]['Aa'].lower(), N, D_MIXED[N])
            out('C-WIDTH N=%d (corner line): L = max(A_t,ref/At_lo, A_a,ref/Aa_lo) = %s against pk07\'s joint-corner budgets %s at the mixed '
                'd^h = %d and %s at d^h + 1 (planning budgets, MOCK references; the hard gate is the d^h + 1 budget) -> %s' % (
                    N, dec_hi(Lc), L_CORNER[(N, D_MIXED[N])], D_MIXED[N], L_CORNER[(N, D_MIXED[N] + 1)], gate(fails, 'C-WIDTH N=%d' % N, True)))
            out('INFO C-WIDTH N=%d: L supports the mixed d^h = %d%s' % (N, dsup, '' if dsup == D_MIXED[N] else
                                                                       ' (one above the planning d^h; P2-12 takes mixed d = %d)' % D_MIXED[N]))
        except Refused as e:
            out('C-WIDTH N=%d (corner line): refused (%s) -> %s' % (N, e, gate(fails, 'C-WIDTH N=%d' % N, False)))
    if not CERT_MODE: L3, _b0, _b1, d3 = width_corner(T[4]['At'].lower() * arb('0.97'), T[4]['Aa'].lower(), 4, D_MIXED[4])
    if not CERT_MODE: out('INFO C-WIDTH N=4 at At_lo - 3%%: L = %s supports the mixed d^h = %d (below the d^h + 1 budget %s, so no stop)' % (
        dec_hi(L3), d3, L_CORNER[(4, D_MIXED[4] + 1)]))
    if not CERT_MODE: plant(nofire, 'PLANT-WIDTH-CORNER', lambda: width_corner(T[4]['At'].lower() * arb('0.96'), T[4]['Aa'].lower(), 4, D_MIXED[4]))

    STAGE[0] = 'item (v)'   # v1_27 (1): the per-piece Ritz and Lemma A data (NOTE_P2_17_RITZ_PIECES_v1)
    need('item (v)')
    RE_M = {} if CERT_MODE else dict((N, load_ritz(N, 'MOCK')) for N in (4, 3))   # v1_30 (1): the mock, for the plants
    RE = dict((N, load_ritz(N, 'CERTIFIED') if N in S9_RECORDS else RE_M[N]) for N in (4, 3))   # v1_30 (1): the S9 records when pinned
    RITZ_STATUS = 'CERTIFIED' if all(N in S9_RECORDS for N in (4, 3)) else 'MOCK'
    try:
        M4REC, M4MOD = load_m4()   # v1_32 (1)
        m4ok = True
    except Refused as e:
        M4REC = M4MOD = None
        m4ok = str(e)
    out('C-M4-READ: %s (%s) with %s (%s) through m4_reader_v1 (%s): the binding, the record checks and C-PINS -> %s' % (
        os.path.basename(M4[0]), PINS[M4[0]][:8], os.path.basename(M4[1]), PINS[M4[1]][:8], PINS[M4_READER_PATH][:8], gate(fails, 'C-M4-READ', m4ok is True)))
    if m4ok is not True:
        raise Refused('item (v): the M4 record does not read: %s' % m4ok)
    for N in (() if CERT_MODE else (4, 3)):
        out('INFO M4-AT-300 N=%d: L_t %s, L_am %s, L_e1 %s, L_e3 %s at J = 300 (m4_reader_v1.law); reader (a) A_t %s, A_am %s (the mock records in a mock run)' % (
            N, m4_call(M4MOD.law, M4REC, 't', N, 300), m4_call(M4MOD.law, M4REC, 'am', N, 300), m4_call(M4MOD.law, M4REC, 'e1', N, 300),
            m4_call(M4MOD.law, M4REC, 'e3', N, 300), dec_hi(A[('t', N)]['hi']), dec_hi(A[('am', N)]['hi'])))
    plant(nofire, 'PLANT-M4-PIN', lambda: load_m4(dict(PINS, **{M4[0]: '0' * 64})))
    plant(nofire, 'PLANT-M4-READER-PIN', lambda: load_m4(dict(PINS, **{M4_READER_PATH: '0' * 64})))
    try:
        TAU = load_tau(P)   # v1_33 (3)
        tok = True
    except Refused as e:
        TAU = None
        tok = str(e)
    out('C-TAU-READ: %s (%s) with %s (%s) through kt_s67_export_reader_v2_1 (%s): rule V2, EXPORT_STATUS CERTIFIED, the same grid -> %s' % (
        os.path.basename(S67[0]), PINS[S67[0]][:8], os.path.basename(S67[1]), PINS[S67[1]][:8], PINS[S67_READER_PATH][:8], gate(fails, 'C-TAU-READ', tok is True)))
    if tok is not True:
        raise Refused('item (v): the crude tau does not read: %s' % tok)
    for N in (4, 3):
        tv = sorted(TAU[N].values())
        out('INFO TAU N=%d: rho_hi %s .. %s (S units) over %d pieces; kt_rb FLOAT TAU_R %s (for C-LA300 only)' % (N, dec_hi(q2arb(tv[0])), dec_hi(q2arb(tv[-1])), len(tv), TAU_R_FLOAT[N]))
    plant(nofire, 'PLANT-TAU-PIN', lambda: load_tau(P, dict(PINS, **{S67[0]: '0' * 64})))
    plant(nofire, 'PLANT-TAU-READER-PIN', lambda: load_tau(P, dict(PINS, **{S67_READER_PATH: '0' * 64})))
    plant(nofire, 'PLANT-TAU-GRID', lambda: load_tau({4: [r if i != 7 else (r[0], repr(float(r[1]) * (1 + 1e-12)), r[2]) for i, r in enumerate(P[4])], 3: P[3]}))
    out('C-TAU-TRIAL: %s line 1 names kt_s9h_v1_2 by full sha256 = the pinned %s (%s); its TRIAL_SET equals the pinned ts and vacres files (N4 %s %s, N3 %s %s); the C-TRIAL and C-TRIAL chain lines read PASS (checked inside load_tau) -> %s' % (
        os.path.basename(S67[1]), os.path.basename(S67_SCRIPT), PINS[S67_SCRIPT][:8], PINS[TS_FILES[4]][:8], PINS[VACRES[4]][:8], PINS[TS_FILES[3]][:8], PINS[VACRES[3]][:8],
        gate(fails, 'C-TAU-TRIAL', flag(lambda: check_tau_trial(PINS)))))   # v1_35 (4): its own flag   # v1_34 (Point 2)
    plant(nofire, 'PLANT-TAU-TRIAL', only('C-TAU-TRIAL', lambda: load_tau(P, dict(PINS, **{TS_FILES[4]: '0' * 64}))))   # v1_34 (Point 2)
    out('C-TAU-N: every tau row is the export line of its own N (the N4_P and N3_P labels read beside the reader; rho_hi equal as exact decimals on every row) -> %s' % gate(fails, 'C-TAU-N', tok is True))   # v1_34 (C-TAU-N)
    plant(nofire, 'PLANT-TAU-N', only('C-TAU-N', lambda: load_tau(P, plant='SWAPN')))   # v1_34 (C-TAU-N)
    out('C-RITZ-READ: %s (%s) and the pinned S9 records give the 18 S9 keys at both N; the port runs on the S9 entries -> %s' % (
        os.path.basename(M_RITZ), PINS[M_RITZ][:8], gate(fails, 'C-RITZ-READ', all(sorted(RE[N]) == sorted(RITZ_KEYS) and (CERT_MODE or sorted(RE_M[N]) == sorted(RITZ_KEYS)) for N in (4, 3)) and RITZ_STATUS == 'CERTIFIED')))
    Lr = lines_of(M_RITZ)
    plant(nofire, 'PLANT-RITZ-MOCK-CERT', lambda: load_ritz(4, 'CERTIFIED', path=M_RITZ, asm_out=M_RITZ, pins={M_RITZ: PINS[M_RITZ]}))   # a MOCK copy with the real keys
    plant(nofire, 'PLANT-RITZ-S9-PIN', lambda: load_ritz(4, 'CERTIFIED', pins=dict(PINS, **{S9_RECORDS[4][0]: '0' * 64})))   # v1_30 (1)
    plant(nofire, 'PLANT-RITZ-MISSING', lambda: load_ritz_mock([x for x in Lr if not x.startswith('N4_DX_3 = ')], 4))
    plant(nofire, 'PLANT-S9-TRIAL', lambda: check_s9_trial({'trial_set': {'ts': '%s:%s' % (os.path.basename(TS_FILES[4]), PINS[TS_FILES[3]]),
                                                                          'vacres': '%s:%s' % (os.path.basename(VACRES[4]), PINS[VACRES[4]])}}, 4))
    RF = dict((N, rb_ref(N)) for N in (4, 3))
    NAP = dict((N, na_prime(KAPB[N])) for N in (4, 3))
    LGP = {}
    for N in (4, 3):
        uC = 1 / (1 - EPSC[N][0])
        ptN = phi_T(N, LG[N]['S'], wt, LG[N]['g00'])
        LGP[N] = (gbad_p(N, arb(LAM_T), KAPB[N], uC, LG[N]['pe']), abad_p(arb(LAM_A), KAPB[N], uC, LG[N]['pe'], ptN, epsg, thg))
    HBP = dict((N, tail_h(N, 1, arb(LAM_T), arb(0)) * KAPB[N] * KAPB[N]) for N in (4, 3))   # v1_35 (2): Hbad' at the code level LAM_T (ADD1 sect. 4)
    HBL, GBL = LAM_T, LAM_T   # v1_35 (2): the levels of HBP and of LGP's Gbad' (C-Z-LEVEL)
    TP, PF, FIRST, AVM, ptok, TPD, pdok = {}, {}, {}, {}, {4: 0, 3: 0}, {}, {4: 0, 3: 0}
    MG = {}   # v1_34 (INFO): per N the (s_x,low - tau_up, g_below, kt0) balls of the good port rows
    PORT = {}   # v1_35 (3): the port's per-piece inputs of the double-trick means
    for N in (4, 3):
        In = None   # v1_35 (7): I[N] no longer enters the port (Hbad' = HBP, tz by tz_odd)
        RbF = (arb(RF[N]['e1']), arb(RF[N]['e3']))   # v1_32 (1): kt_rb's FLOAT R_e1, R_e3, kept for C-LA300's comparison only
        GbP, AbP = LGP[N]
        for idx, jlo, jhi in P[N]:
            tb, _tm, _r = tball(jlo, jhi)
            try:
                JL = grid_j(jlo, True)   # v1_33 (1): the laws at the smaller J reading of jlo
                At_hi, Aa_hi = m4_law(M4REC, M4MOD, 't', N, JL), m4_law(M4REC, M4MOD, 'am', N, JL)   # v1_32 (1): L_k(jlo) bounds the piece
                Rb12 = (m4_law(M4REC, M4MOD, 'e1', N, JL), m4_law(M4REC, M4MOD, 'e3', N, JL))
                Bp = dict((k, entry_piece(RE[N][k], tb)) for k in RITZ_KEYS)
                mh = mhat_ball(MC[N], tb)
                er, s_, _sp = m2b_eps(m2b_call(M2MOD.law_v1, M2R, N, JL))
                RC = ritz_piece(Bp, mh)
                LA = lemma_a_cbar(RC, er, Rb12, TAU_R_FLOAT[N], q2arb(TAU[N][idx]))   # v1_33 (3)
                IP = lemma_a_amp(RC, LA, er, s_, mh, NAP[N][0], HBP[N], GbP, AbP, Aa_hi)
                RCd = ritz_piece(Bp, mh, 'DK')   # v1_28 (1): kt_rb's uniform Davis-Kahan bar, for the comparisons
                LAd = lemma_a_cbar(RCd, er, Rb12, TAU_R_FLOAT[N], q2arb(TAU[N][idx]))   # v1_33 (3)
                IPd = lemma_a_amp(RCd, LAd, er, s_, mh, NAP[N][0], HBP[N], GbP, AbP, Aa_hi)
            except Refused as e:
                PF.setdefault(N, []).append((idx, str(e)))
                continue
            MG.setdefault(N, []).append((LA['s_xlo'] - LA['tau'].upper(), LA['g_below'], LA['kt0']))   # v1_34 (INFO)
            try:   # v1_35 (2), (3): row 2 by the odd Ritz route and the double-trick inputs, NH and GP at one Lam (C-Z-LEVEL)
                NHp, GPp = nh_gp(IP, HBL, GBL)
                Ltp = lt_ball(RC, LA, IP['lt0'])
                IP['tz'], IP['dtz'] = tz_odd(mh, RC, entry_piece(EX[N]['IHZ'], tb), entry_piece(G22E[N], tb), NHp, GPp, IP['sp'], IP['t0'], Ltp.lower())
                PORT[(N, idx)] = (mh, IP['lt0'], Ltp, RC['G'][0][0], er, RC['Iht0'], tb)
            except Refused as e:
                PF.setdefault(N, []).append((idx, str(e)))
                continue
            X = tprov(At_hi, IP)
            TP[(N, idx)] = X
            IPd['tz'], IPd['dtz'] = IP['tz'], IP['dtz']   # v1_35 (2): the odd route's tz on the DK rows too
            TPD[(N, idx)] = tprov(At_hi, IPd)
            try:
                pdok[N] += 1 if check_pd_dk(RC, RCd) else 0
            except Refused:
                pass
            AVM[N] = IP['av0'] if (N not in AVM or IP['av0'] > AVM[N]) else AVM[N]
            at = X['At'].lower()
            corr = abs(X['Vt'] - X['Q'] * X['Q'] - (IP['tx'] * IP['tx'] + IP['ty'] * IP['ty'])).upper()
            if (X['Pt2'].upper() <= X['Vt'].upper() - at * at + X['dtx'].upper() * X['dtx'].upper() + 2 * corr + arb('1e-30')) and (at > 0):
                ptok[N] += 1
            if idx == '0000':
                FIRST[N] = (RC, LA, IP, Bp, mh, RCd, er, s_, Rb12, q2arb(TAU[N][idx]))   # v1_34: the first piece's inputs for the plants
    ngood = dict((N, sum(1 for (n, _i) in TP if n == N)) for N in (4, 3))
    out('C-GAP: the Ritz problem and Lemma A on every piece (interval Cholesky, disjoint enclosures, Davis-Kahan gaps, Kato-Temple, C-SX, C-SIGN0): N4 %d of 904, N3 %d of 904 pieces -> %s' % (
        ngood[4], ngood[3], gate(fails, 'C-GAP', ngood[4] == 904 and ngood[3] == 904)))
    for N in (4, 3):
        if PF.get(N):
            out('INFO C-GAP N=%d: first refusals %s' % (N, '; '.join('%s %s' % x for x in PF[N][:3])))
    for N in (4, 3):   # v1_34 (INFO)
        if MG.get(N):
            mv = [min((x[k] for x in MG[N]), key=lambda a: float(a.lower())) for k in range(3)]
            out('INFO KT-MARGINS N=%d: over the %d good port rows the smallest s_x,low - tau_up %s, g_below %s, 1 - 2 c-bar - s_x,high %s (lower ends)' % (
                N, len(MG[N]), dec_lo(mv[0]), dec_lo(mv[1]), dec_lo(mv[2])))
    if not all(N in FIRST for N in (4, 3)):
        raise Refused('item (v): a first piece was refused')
    F2 = FIRST[4][2]   # v1_35 (2): C-Z-LEVEL on the first N4 piece's dict
    out('C-Z-LEVEL: NH = Lam + Hbad-prime(Lam) and GP = Lam (mhat/lt0) eps_r + Gbad-prime(Lam) at one Lam = LAM_T = %s on every port piece (nh_gp; Hbad-prime %s at N4) -> %s' % (
        LAM_T, dec_hi(HBP[4]), gate(fails, 'C-Z-LEVEL', flag(lambda: nh_gp(F2, HBL, GBL) is not None))))
    plant(nofire, 'PLANT-Z-LEVEL', only('C-Z-LEVEL', lambda: nh_gp(F2, HBL, LAM_A)))
    for N in (4, 3):
        RC1 = FIRST[N][5]   # v1_28 (1): kt_rb's method (DK) against its CERT300 lines
        try:
            r3 = check_ritz300(RC1, RF[N], RITZ_STATUS == 'CERTIFIED')   # v1_31 (1): the S9 records take the overlap form
        except Refused as e:
            r3 = str(e)
        out('C-RITZ300 N=%d: form %s: the first piece lambda_0 %s, s_x %s, mu_y %s against the kt_rb CERT300 lines, and |a^_k| %s against its bars %s -> %s' % (
            N, 'S9 records, overlap and the lower leg' if RITZ_STATUS == 'CERTIFIED' else 'mock, containment and both legs', RC1['vals'][0].str(10, radius=False), (RC1['vals'][1] / RC1['vals'][0]).str(8, radius=False), (RC1['vals'][2] / RC1['vals'][0]).str(8, radius=False),
            ' '.join(abs(x).str(6, radius=False) for x in RC1['a']), ' '.join(x[:10] for x in RF[N]['abar']), gate(fails, 'C-RITZ300 N=%d' % N, r3 is True)))
        out('INFO RITZ300 N=%d: %s; midpoints lambda_0 %s, s_x %s, mu_y %s; %s' % (
            N, 'every hard leg holds' if r3 is True else r3, RC1['vals'][0].mid().str(15), (RC1['vals'][1] / RC1['vals'][0]).mid().str(15),
            (RC1['vals'][2] / RC1['vals'][0]).mid().str(15), ritz300_info(RC1, RF[N])))   # v1_31 (1)
    B1, mh1 = FIRST[4][3], FIRST[4][4]
    plant(nofire, 'PLANT-RITZ300-SWAP', lambda: check_ritz300(ritz_piece({**B1, 'G,0,0': B1['G,1,1'], 'G,1,1': B1['G,0,0']}, mh1, 'DK'), RF[4], RITZ_STATUS == 'CERTIFIED'))   # moves lambda_0 by about 5e-3; v1_31 (1): in the gate's form
    try:
        RCs = ritz_piece({**B1, 'G,0,0': B1['G,1,1'], 'G,1,1': B1['G,0,0']}, mh1, 'DK')
        a_, b_ = arb(RF[4]['lambda_0'][0]) - RCs['vals'][0].upper(), RCs['vals'][0].lower() - arb(RF[4]['lambda_0'][1])
        gsw = (a_ if a_ > b_ else b_).str(3)
    except Refused as e:
        gsw = 'not computed (ritz_piece refuses the swap: %s)' % e
    out('INFO RITZ300-SWAP-GAP: the swapped lambda_0 ball lies %s from the kt_rb CERT300 interval (positive: they do not meet)' % gsw)   # v1_31 (1)
    try:
        check_ritz300(ritz_piece({**B1, 'G,0,1': B1['G,1,3'], 'G,1,3': B1['G,0,1']}, mh1, 'DK'), RF[4], RITZ_STATUS == 'CERTIFIED')
        nsw = 'accepted: the swap stays inside the enclosures and bars'
    except Refused as e:
        nsw = 'refused (%s)' % e
    out('INFO RITZ300-NOTE-SWAP: the note G,0,1/G,1,3 swap at N4 is %s' % nsw)
    plant(nofire, 'PLANT-RITZ-BAR', lambda: ritz_piece({**B1, 'G,1,1': B1['G,1,1'] + arb(0, 1)}, mh1))
    F4 = FIRST[4]   # v1_34: the new gates' plants on the first N4 piece
    plant(nofire, 'PLANT-KT0', only('C-KT0', lambda: lemma_a_cbar(F4[0], F4[6], F4[8], TAU_R_FLOAT[4], F4[9], plant='KT0')))
    plant(nofire, 'PLANT-DK0', only('C-DK0', lambda: lemma_a_amp(dict(F4[0], vals=[F4[0]['vals'][0], arb(2), F4[0]['vals'][2]]), F4[1], F4[6], F4[7], F4[4],
                                                                  NAP[4][0], HBP[4], LGP[4][0], LGP[4][1], arb(0))))
    plant(nofire, 'PLANT-SP', only('C-SP', lambda: tprov(arb(0), dict(F4[2], sp=arb(1)))))
    plant(nofire, 'PLANT-GRAM', only('C-GRAM', lambda: tprov(arb(0), dict(F4[2], G=arb_mat(3, 3, [1, 2, 0, 2, 1, 0, 0, 0, 1])))))
    for N in (4, 3):
        LA0 = lemma_a_cbar(FIRST[N][5], arb(RF[N]['eps_r']), (arb(RF[N]['e1']), arb(RF[N]['e3'])), TAU_R_FLOAT[N])
        mine = LA0['rho'] + [LA0['cbar'], LA0['q'], LA0['eps0'], LA0['epsy']]
        ref = RF[N]['rho'] + [RF[N]['cbar'], RF[N]['q'], RF[N]['eps0'], RF[N]['epsy']]
        rel = max(float(abs(x.upper() / arb(r) - 1).upper()) for x, r in zip(mine, ref))
        out('C-LA300 N=%d: Lemma A on the first piece with the kt_rb FLOAT eps_r %s, R_e1 %s, R_e3 %s and TAU_R %s gives rho, c-bar, q, eps_0 and eps_y within %.2e of its CBAR line (1e-2: the piece widening) -> %s' % (
            N, RF[N]['eps_r'], RF[N]['e1'], RF[N]['e3'], TAU_R_FLOAT[N], rel, gate(fails, 'C-LA300 N=%d' % N, rel <= 1e-2)))
    for N in (4, 3):
        nap, Lb = NAP[N]
        out('C-NA N=%d: NA-prime (Lemma B) = %s at L = %s with kappa_max %s; L >= 1 and NA-prime >= the largest |a^_00| over the pieces %s -> %s' % (
            N, dec_hi(nap), Lb.str(5, radius=False), dec_hi(KAPB[N]), dec_hi(AVM[N]), gate(fails, 'C-NA N=%d' % N, (Lb >= 1) and (nap >= AVM[N]))))
    plant(nofire, 'PLANT-NA', lambda: certified_tag(dict([(x, []) for x in fin] + [('kt_p2_assembly', na_value('FLOAT_LITERAL', 4, mh=FIRST[4][2]['mhat'], lt0=FIRST[4][2]['lt0'])[1])])))
    out('C-PT-PORT: the C-PT identity (Pt^2 <= V_t - A_t^2 + dtx^2 + Gram terms) and A_t > 0 on every port row: N4 %d, N3 %d of 904 -> %s' % (
        ptok[4], ptok[3], gate(fails, 'C-PT-PORT', ptok[4] == 904 and ptok[3] == 904)))
    out('C-PD-DK: on every piece the per-direction and the uniform Davis-Kahan Ritz vectors overlap componentwise (both hold c_k): N4 %d, N3 %d of 904 -> %s' % (
        pdok[4], pdok[3], gate(fails, 'C-PD-DK', pdok[4] == 904 and pdok[3] == 904)))   # v1_28 (1)
    RCf = FIRST[4][0]
    plant(nofire, 'PLANT-PD-DK', lambda: check_pd_dk(dict(RCf, vecs=[[x + 1 for x in RCf['vecs'][0]]] + RCf['vecs'][1:]), FIRST[4][5]))
    plant(nofire, 'PLANT-PD-GAP', lambda: pd_vectors(RCf['C'], RCf['vec'], RCf['lamo'], RCf['res'], RCf['rF'], gap_scale=arb('1e-6')))   # an understated gap makes the bound fail
    pdc, dkc = pd_control(('1', '0.5', '0.2'), '1e-6')   # v1_30 (3): the control
    ctl = all(pdc[k][i].contains(arb(1 if i == k else 0)) and dkc[k][i].contains(arb(1 if i == k else 0)) for k in range(3) for i in range(3))
    ctl = ctl and all(arb(pdc[k][i].rad()) <= arb(dkc[k][i].rad()) for k in range(3) for i in range(3))
    out('C-PD-CONTROL: on the ball diag(1, 0.5, 0.2) +- 1e-6 the per-direction and the Davis-Kahan vectors contain e_k, and every per-direction bar is at most the Davis-Kahan bar (largest %s against %s) -> %s' % (
        dec_hi(hi_max([arb(pdc[k][i].rad()) for k in range(3) for i in range(3)])), dec_hi(hi_max([arb(dkc[k][i].rad()) for k in range(3) for i in range(3)])),
        gate(fails, 'C-PD-CONTROL', ctl)))
    plant(nofire, 'PLANT-PD-ZEROGAP', lambda: pd_control(('1', '0.5', '0.5'), '1e-6'))   # a zero gap must be refused
    LW = {}
    for N in (4, 3):
        rp = [TP[(N, i)] for (i, _jl, _jh) in P[N] if (N, i) in TP]
        rd = [TPD[(N, i)] for (i, _jl, _jh) in P[N] if (N, i) in TPD]
        LW[N] = (lo_min([x['At'] for x in rp]), lo_min([x['Aa'] for x in rp]), lo_min([x['At'] for x in rd]), lo_min([x['Aa'] for x in rd]))
        Lp = up(arb(A_REF[(N, 't')]) / LW[N][0], arb(A_REF[(N, 'a')]) / LW[N][1])
        Ld = up(arb(A_REF[(N, 't')]) / LW[N][2], arb(A_REF[(N, 'a')]) / LW[N][3])
        Rp, Rd = FIRST[N][0], FIRST[N][5]
        out('INFO PD-BARS N=%d: the first piece t^_x radius %s per-direction against %s Davis-Kahan, a^_x radius %s against %s; the corner L of the port rows %s per-direction against %s Davis-Kahan; budgets %s at d^h = %d, %s at d^h + 1' % (
            N, dec_hi(arb(Rp['t'][1].rad())), dec_hi(arb(Rd['t'][1].rad())), dec_hi(arb(Rp['a'][1].rad())), dec_hi(arb(Rd['a'][1].rad())), dec_hi(Lp), dec_hi(Ld),
            L_CORNER[(N, D_MIXED[N])], D_MIXED[N], L_CORNER[(N, D_MIXED[N] + 1)]))
    for N in (4, 3):
        try:
            Lc, _b0, _b1, dsup = width_corner(LW[N][0], LW[N][1], N, D_MIXED[N])
            wv, wok = 'L %s supports the mixed d^h = %d' % (dec_hi(Lc), dsup), True
        except Refused as e:
            wv, wok = 'refused (%s)' % e, False
        out('C-WIDTH-PORT N=%d: the corner ratio of the port rows (smallest At_lo and Aa_lo over the pieces) within the budget at d^h + 1: %s -> %s' % (
            N, wv, gate(fails, 'C-WIDTH-PORT N=%d' % N, wok)))
    plant(nofire, 'PLANT-WIDTH-DK', lambda: width_corner(LW[4][2], LW[4][3], 4, D_MIXED[4]))   # the Davis-Kahan rows at N4 must be refused
    for N in (4, 3):
        X1, XN = TP[(N, '0000')], T.get(N)
        if XN is not None: out('INFO PORT300 N=%d: the first port row At_lo %s, Aa_lo %s, Xta_lo %s, dtx_hi %s, Qvt_hi %s; the mock-input J = 300 row %s, %s, %s, %s, %s' % (
            N, dec_lo(X1['At']), dec_lo(X1['Aa']), dec_lo(X1['Xta']), dec_hi(X1['dtx']), dec_hi(X1['Q']), dec_lo(XN['At']), dec_lo(XN['Aa']), dec_lo(XN['Xta']),
            dec_hi(XN['dtx']), dec_hi(XN['Q'])))
        rows = [TP[(N, i)] for (i, _jl, _jh) in P[N] if (N, i) in TP]
        out('INFO PORT-RANGE N=%d: over the %d port rows min At_lo %s, min Aa_lo %s, min Xta_lo %s, max dtx_hi %s, max Qvt_hi %s' % (
            N, len(rows), dec_lo(lo_min([x['At'] for x in rows])), dec_lo(lo_min([x['Aa'] for x in rows])), dec_lo(lo_min([x['Xta'] for x in rows])),
            dec_hi(hi_max([x['dtx'] for x in rows])), dec_hi(hi_max([x['Q'] for x in rows]))))
    RITZ_SRC = ('pk03 S9 records %s (N4), %s (N3) through m3_reader_v4_4: per piece, the direct form over the t-ball' % (PINS[S9_RECORDS[4][0]][:8], PINS[S9_RECORDS[3][0]][:8])) if RITZ_STATUS == 'CERTIFIED' else ('MOCK_RITZ_ENTRIES_v1 %s (MOCK): per piece, the direct form over the t-ball' % PINS[M_RITZ][:8])
    NA_SRC = 'LEMMA_B: NA-prime = min over L >= 1 of L + L exp(-L) kappa_max (N4 %s, N3 %s)' % (dec_hi(NAP[4][0]), dec_hi(NAP[3][0]))
    EPS_SRC = 'law_v1 of M2B_KV_v1 %s at each piece jlo' % PINS[M2B[0]][:8]

    STAGE[0] = 'P2-14'
    need('P2-14')
    q1, q2, e2u = arb(1) / arb(256), arb(1) / arb(128), arb(1) / arb(2)
    cases = (('positive', q1, q2, q1), ('negative', -q2, -q1, q1), ('straddling', -q1, q2, arb(0)))
    ok = True
    for nm, lo, hi, want in cases:
        pxu, cu = px_from(e2u, lo, hi)
        ok = ok and (cu == want) and (pxu - (e2u - want * want).sqrt()).contains(0)
    out('C-PX3: px_from on a positive, a negative and a straddling Cov ball gives cmin = 1/256, 1/256, 0 and pX = (E2 - cmin^2)^(1/2) -> %s' % (
        gate(fails, 'C-PX3', ok)))
    plant(nofire, 'PLANT-PX-NEG', lambda: px_from(arb(1) / arb(2 ** 20), q1, q2))
    ref = {}
    for x in lines_of(JOINTF):
        m = re.match(r'^(N[34]_D[34]M?_P[0-9]{4}) = (.*)$', x)
        if m:
            ref[m.group(1)] = m.group(2).split()
    STAGE[0] = 'reader (e)'
    C28 = {} if CERT_MODE else load_p2_8(M_P28, 'MOCK')   # v1_35 (7): P2-8's MOCK stand-in, for the mock run's comparisons only
    if not CERT_MODE: out('READER-E MOCK %s: %d rows (a MOCK stand-in for P2-8\'s C4.1 record) -> read' % (os.path.basename(M_P28), len(C28)))
    plant(nofire, 'PLANT-MOCK-E %s' % os.path.basename(M_P28), lambda: load_p2_8(M_P28, 'CERTIFIED'))

    STAGE[0] = 'normX'
    x5 = arb(5)
    g_closed = x5.sqrt() * (-x5).exp() + arb.const_sqrt_pi() / 2 * x5.sqrt().erfc()
    orders = []
    for nm, fn in (('gamma_upper as arb(5).gamma_upper(3/2)', lambda: x5.gamma_upper(arb(3) / 2)),
                   ('gamma_upper as arb(3/2).gamma_upper(5)', lambda: (arb(3) / 2).gamma_upper(x5))):
        try:
            val = fn()
        except Exception as e:
            out('INFO C-GAMMA: %s raised %r' % (nm, e))
            continue
        if val.is_finite() and val.overlaps(g_closed):
            orders.append(nm)
    out('C-GAMMA: the closed form Gamma(3/2, 5) = %s agrees with flint\'s %s -> %s' % (
        g_closed.str(12, radius=False), ' and '.join(orders) if orders else 'gamma_upper in neither order', gate(fails, 'C-GAMMA', len(orders) == 1)))
    levs = sorted(set(x for tab in (NORMX_LEVELS, E2_GLEV, E2_SLEV) for v in tab.values() for x in v), key=float)
    bad = []
    for x in levs:
        Lx = arb(x)
        for s2 in (5, 7):
            if not _gam_up(4, s2, Lx).overlaps(Lx.gamma_upper(arb(s2) / 2)):
                bad.append('Gamma(%d/2, %s)' % (s2, x))
    j0 = arb(300)
    low = arb.const_sqrt_pi() / 2 * j0.sqrt().erf() - j0.sqrt() * (-j0).exp()
    if not low.overlaps(j0.gamma_lower(arb(3) / 2)):
        bad.append('gamma(3/2, 300)')
    out('C-GAMMA2: the closed forms of Gamma(5/2, L) and Gamma(7/2, L) at the %d levels in use (%s) and gamma(3/2, 300) = %s against flint\'s '
        'gamma_upper and gamma_lower: %s -> %s' % (len(levs), ' '.join(levs), low.str(12, radius=False), ', '.join(bad) if bad else 'all agree',
                                                   gate(fails, 'C-GAMMA2', not bad)))
    KAPM = None if CERT_MODE else dict((N, kappa_mock(I[N], N)) for N in (4, 3))
    KAP = KAPB
    relk = 0.0 if CERT_MODE else max(abs(float((KAPB[N] / KAPM[N]).mid()) - 1) for N in (4, 3))
    if not CERT_MODE: out('C-KAPPA: kappa_max = k1_hi^3/((1 - eps_r) lambda_h(300)), lambda_h by the matrix-tree theorem: N4 %s, N3 %s; against the kappa backed out of '
        'kt_rb\'s Hbad (2 digits, mock x1.03): N4 %s, N3 %s; worst relative %.2e (5e-2) -> %s' % (dec_hi(KAPB[4]), dec_hi(KAPB[3]), dec_hi(KAPM[4]),
                                                                           dec_hi(KAPM[3]), relk, gate(fails, 'C-KAPPA', relk <= 5e-2)))
    STAGE[0] = 'Lemma E'
    the_s = THETA_G   # v1_15 (1): Lemma E-prime's own reading of theta; C-THETA checks it against Abad-prime's
    the = arb(the_s)
    A_TH = the * (1 - epsg) * trial_ab()[0]   # v1_14 (1): Lemma E-prime's A_theta
    CE, E1, E1R, RHO = {}, {}, {}, {}   # v1_16: RHO for Lemma R
    for N in (4, 3):
        In, kap = (None if CERT_MODE else I[N]), KAP[N]
        rat = None if CERT_MODE else In['Gbad'] / In['Hbad']
        sup0 = arb(SUPP0_MOCK[N])
        sps = None if CERT_MODE else In['Abad'] / (600 * sup0 * kap.lower() * arb(-40).exp())
        ptb = phi_T(N, LG[N]['S'], lg_weights_b(epsg, the), LG[N]['g00'])   # v1_14 (1), v1_15 (2): Phi_eps,theta,b, its own remainder ratio
        rterms = rho_terms(QT[N], epsg, 1 / arb(300))   # v1_16, Lemma R
        pw = LG[N]['pe'] / (LG[N]['S'] * LG[N]['S'])
        RHO[N] = (rterms, 1 + 2 * rterms[4] * pw.sqrt(), pw)
        CE[N] = {'eps': EPSC[N][0], 'sp': EPSC[N][2], 'kap': kap, 'Phi': LG[N]['pe'], 'S': (LG[N]['pe'] * ptb).sqrt(), 'rho': RHO[N][1], 'A': A_TH, 'theta': the_s}   # v1_16: rho_phi by Lemma R; v1_25 (1): the certified eps_r and s-prime
        E1[N] = e1_bound(CE[N])   # v1_11 (1): rho_phi enters e_1
        E1R[N] = e1_bound(dict(CE[N], rho=arb('1.5')))
        if not CERT_MODE: out('INFO LEMMA-E N=%d (Lemma E-prime; Lemma T-prime with the S7 certified G_00): Phi_eps <= %s, Phi_eps,theta,b <= %s, S-prime <= %s, A_theta %s; Lemma E (MOCK) had Phi <= %s, S <= %s; rho_phi <= %s (Lemma R), e_1 <= %s' % (
            N, dec_hi(CE[N]['Phi']), dec_hi(ptb), dec_hi(CE[N]['S']), A_TH.str(6, radius=False), dec_hi(rat * rat), dec_hi(sup0 * (sps * sps * rat * rat).sqrt()), dec_hi(RHO[N][1]), dec_hi(E1[N])))
    out('C-E1-RHO: e_1 with rho_phi = 1.5 exceeds e_1 with the run rho_phi at both N -> %s' % gate(
        fails, 'C-E1-RHO', all(E1R[N] > E1[N] for N in (4, 3))))
    plant(nofire, 'PLANT-E2-LEVEL', lambda: lemma_e(4, 'D3', 2, 2, ('2.5', '34.5'), (arb(1), arb(1)), (arb(1), arb(1)), CE[4]))
    plant(nofire, 'PLANT-E2-VLEVEL', lambda: lemma_e(4, 'D4', 2, 2, ('25.5', '3.5'), (arb(1), arb(1)), (arb('0.8'), arb('0.9')), CE[4]))   # v1_14 (1)
    out('C-THETA: Abad-prime and Lemma E-prime use one theta = %s at both N -> %s' % (THETA_G, gate(
        fails, 'C-THETA', all(check_theta(LG[N]['theta'], CE[N]['theta']) for N in (4, 3)) and THETA_G == '0.7')))
    plant(nofire, 'PLANT-THETA', lambda: check_theta('0.7', '0.9'))
    pok, tok, rok2 = True, True, True   # v1_17 (1), (2): Lemma T-prime's form, Lemma T's trace, the recurrence
    for N in (4, 3):
        Sn, gn = LG[N]['S'], LG[N]['g00']
        for nm, w in (('eps', we), ('theta', wt), ('theta_b', lg_weights_b(epsg, the))):
            pc = phi_T(N, Sn, w, gn)
            pok = pok and all(abs(phi_T_k1(N, Sn, w, gn, arb(J)) / pc - 1) < arb('1e-12') for J in (300, 3000))
            it = trace_T(N, w, arb(300))
            bnd = k1_lim(N, 300 * w[0]) * k1_lim(N, 300 * w[1])
            mt = main_T_val(N, w, arb(300))
            tok = tok and (it < bnd)
            out('INFO TRACE N=%d %s: Lemma T exact ||W||^2 at J = 300 %s, Z_T %s; Lemma T-prime bound %s, factor %s over main_T' % (
                N, nm, dec_hi(it), dec_hi(it / mt), dec_hi(bnd), dec_hi(bnd / mt)))
        c0 = 300 * we[0]
        k1ref = 2 * (-c0).exp() * bessel_i1(c0) / c0 if N == 4 else (1 - (-2 * c0).exp()) / (2 * c0)
        rok2 = rok2 and lambda_list(N, c0, 600)[0].overlaps(k1ref)
    out('C-PHIT-FORM: Lemma T-prime closed form against its k1_lim form at J = 300 and 3000, three triangles, both N, relative below 1e-12 -> %s' % gate(
        fails, 'C-PHIT-FORM', pok))
    out('C-TRACE: the exact Lemma T trace lies below the Lemma T-prime bound for the three triangles at J = 300, both N -> %s' % gate(fails, 'C-TRACE', tok))
    out('C-TRACE-REC: the recurrence lambda_0 of the L = 600 chain agrees with k1 (I_1 series at N = 4, closed form at N = 3) -> %s' % gate(fails, 'C-TRACE-REC', rok2))
    out('C-G00-FLOAT: the G_00 lower end lies within 5%% of 1 at both N (S7 certified lower end) -> %s' % (gate(
        fails, 'C-G00-FLOAT', all(abs(G00[N] - 1) < arb('0.05') for N in (4, 3)))))
    plant(nofire, 'PLANT-G00-NONPOS', lambda: check_g00(arb(0)))
    plant(nofire, 'PLANT-G00-PIN', lambda: g00_s7(4, dict(PINS, **{S7G00[4][0]: '0' * 64})))   # v1_20 (1): a record failing its pin is refused
    plant(nofire, 'PLANT-G00-PIN-ASM', lambda: g00_s7(4, dict(PINS, **{S7G00[4][1]: '0' * 64})))   # v1_25 (4): the asm output pin alone
    plant(nofire, 'PLANT-TRACE-L', lambda: trace_T(4, we, arb(300), 10))
    thr = arb('0.9') + 2 / A_TH
    out('C-E2-VLEVEL-EDGE: the vertical level bound c+ + 2/A_theta = %s (c+ 0.9): a level 2^-20 above it passes -> %s' % (dec_hi(thr), gate(
        fails, 'C-E2-VLEVEL-EDGE', lemma_e(4, 'D4', 2, 2, ('25.5', dec_hi(thr + arb(2) ** -20)), (arb(1), arb(1)), (arb('0.8'), arb('0.9')), CE[4])[1] > 0)))
    plant(nofire, 'PLANT-E2-VLEVEL-EDGE', lambda: lemma_e(4, 'D4', 2, 2, ('25.5', dec_lo(thr - arb(2) ** -20)), (arb(1), arb(1)), (arb('0.8'), arb('0.9')), CE[4]))
    rok, gok2 = True, True
    for N in (4, 3):
        rt, rho, pw = RHO[N]
        rok = rok and (rho >= 1) and (rho < arb('1.1')) and (abs(rho - arb(RHO_FLOAT[N])) < arb('1e-4'))
        gok2 = gok2 and check_sigma(rt[4], rt[0], rt[1], rt[3], rt[2])
        out('INFO RHO N=%d (Lemma R, eps %s): q_L %s, q_Q %s, r0 %s, r* %s, sigma_eps %s, Phi_W %s; rho_phi <= %s' % (
            N, EPS_G, dec_hi(rt[0]), dec_hi(rt[1]), rt[2].str(8, radius=False), rt[5].str(8, radius=False), dec_hi(rt[4]), dec_hi(pw), dec_hi(rho)))
    out('C-RHO: 1 <= rho_phi <= 1.1 and within 1e-4 of rho_float_v1 at both N -> %s' % gate(fails, 'C-RHO', rok))
    out('C-RHO-GRID: no grid value of h on [r0, 50 r0] (2001 points) above sigma_eps at both N -> %s' % gate(fails, 'C-RHO-GRID', gok2))
    plant(nofire, 'PLANT-RHO-SIGMA', lambda: check_sigma(rho_h(RHO[4][0][2] + 1, RHO[4][0][0], RHO[4][0][1], RHO[4][0][3]), RHO[4][0][0], RHO[4][0][1], RHO[4][0][3], RHO[4][0][2]))
    ssu = arb('0.5')
    elo = (e_lower(arb(-1), ssu) == arb(-1)) and (e_lower(arb(1), ssu) == arb('0.5')) and (e_upper(arb(-1)) == 0) and (e_upper(arb(2)) == 2)
    out('C-E-LOWER: Lemma E ends min(R, (1 - sp^2) R) on R = -1, 1 and max(R, 0) on R = -1, 2 with 1 - sp^2 = 0.5 -> %s' % gate(
        fails, 'C-E-LOWER', elo))
    plant(nofire, 'PLANT-E-LOWER', lambda: check_e_lower((ssu * arb(-1)).lower(), arb(-1), ssu))
    rows_jt, audit, worst = [], [], {'Cov_inf_lo': 0.0, 'pX_hi': 0.0, 'E2_hi': 0.0}
    rows_mn, mn_ok, mn_ext, mn_w, CE_T, CEC = [], True, {}, {}, {}, {}   # v1_22: route B, the means export for pk07
    covx, first, e2up, dhp = 0.0, {}, True, {}
    MEANS, mpf = {}, []   # v1_35 (3): the double-trick means per (N, piece), ADD1 sect. 2
    SLT = dict((N, best_slev(N, 1, 0, KAP[N])) for N in (4, 3))   # the w = 2 horizontal window: (value, level)
    SLB = dict((N, best_slev(N, 0, 1, KAP[N])) for N in (4, 3))   # the vertical one at w = 2, which dominates w = 1 (C-KAPPA-GE1)
    SPT = dict((N, (2 * CE[N]['sp'] + CE[N]['sp'] * CE[N]['sp']) * SLT[N][0]) for N in (4, 3))
    SPB = dict((N, (2 * CE[N]['sp'] + CE[N]['sp'] * CE[N]['sp']) * SLB[N][0]) for N in (4, 3))
    GTC = dict((N, tail_h(N, 1, arb(LAM_T), arb(0)) * LG[N]['pe']) for N in (4, 3))   # the gg tail's constant at Lam_t
    for N in (4, 3):
        ss_ = 1 - CE[N]['sp'] * CE[N]['sp']
        for idx, jlo, jhi in P[N]:
            if (N, idx) not in PORT:
                mpf.append((N, idx, 'no port inputs'))
                continue
            try:
                MEANS[(N, idx)] = means_dt(PORT[(N, idx)], E[N]['M4_10'], TBE[N], SPT[N], SPB[N], ss_, arb(LAM_T), GTC[N], KAP[N])
            except Refused as e:
                mpf.append((N, idx, str(e)))
    out('C-KAPPA-GE1: kappa >= 1 certainly at both N (N4 %s, N3 %s): the w = 2 s-part of c_b dominates Lemma S at w = 1 (ADD1 sect. 2) -> %s' % (
        dec_lo(KAP[4]), dec_lo(KAP[3]), gate(fails, 'C-KAPPA-GE1', all(KAP[N] >= 1 for N in (4, 3)))))
    out('C-MEAN-PARTS: on every piece the c_t (w = 2, double trick) and c_b (w = 1, Tb) balls hold main -+ (gg box + gg tail + s-part) over G_00 lambda~_0^w: %d failures%s -> %s' % (
        len(mpf), (' (first %s)' % (mpf[0],)) if mpf else '', gate(fails, 'C-MEAN-PARTS', (not mpf) and len(MEANS) == len(P[4]) + len(P[3]))))
    for N in (4, 3):
        prt = [MEANS[(N, x[0])][2] for x in P[N] if (N, x[0]) in MEANS]
        if prt:
            out('INFO MEAN-PARTS N=%d: first piece gg box %s, gg tail %s, s-part c_t %s (level %s), s-part c_b %s (level %s), normalization relative width %s; c_t main %s, c_b main %s; largest gg box %s' % (
                N, dec_hi(prt[0][0]), dec_hi(prt[0][1]), dec_hi(prt[0][2]), SLT[N][1], dec_hi(prt[0][3]), SLB[N][1], dec_hi(prt[0][6]),
                prt[0][4].str(10, radius=False), prt[0][5].str(10, radius=False), dec_hi(max((p[0] for p in prt), key=float))))
    P0 = PORT.get((4, P[4][0][0]))
    if P0 is not None:
        mt0, gb0, gt0 = mean_t_dt(P0[0], P0[5], P0[5], entry_piece(E[4]['M4_10'], P0[6]), P0[3], P0[2], arb(LAM_T), P0[4], P0[1], GTC[4], KAP[4])
        gg0 = (gb0 + gt0).upper()
        plant(nofire, 'PLANT-MEAN-NOSPART', only('C-MEAN-PARTS', lambda: check_mean_parts(mean_ends(mt0, 0, gg0, arb(0), 1 - CE[4]['sp'] * CE[4]['sp']), mt0, gg0, SPT[4])))
    plant(nofire, 'PLANT-MEAN-SIGN', only('C-MEAN-SIGN', lambda: mean_ends(arb(0.5, 1), arb(0.001), arb(0), arb(0), arb(1))))   # v1_37 (6) N-1: a ratio ball reaching below 0 with e_1 > 0
    mdt_ok = True   # v1_35 (3): C-MEAN-DT
    STAGE[0] = 'routes and the normX_HS slot (v1_35)'
    HSD = load_hs(None, 'CERTIFIED')   # v1_35 (6): the normX_HS slot (SPEC_HS_INV_NORMX_v1_2), pk08's certified D3 record
    out('C-HS-SRC: %s (%s) under its run output %s (%s), rule V2: both pinned, VERDICT lines exactly [VERDICT VALID], one RECORD line with the record sha256, EXPORT_STATUS and FORMAT certified, no MOCK token -> %s' % (
        os.path.basename(HS_RECORD[0]), PINS[HS_RECORD[0]][:8], os.path.basename(HS_RECORD[1]), PINS[HS_RECORD[1]][:8], gate(fails, 'C-HS-SRC', HSD.get('RECORD') == 'HS_INV_NORMX_v1')))
    plant(nofire, 'PLANT-HS-SRC', only('C-HS-SRC', lambda: load_hs(None, 'CERTIFIED', pins=dict(PINS, **{HS_RECORD[0]: '0' * 64}))))
    plant(nofire, 'PLANT-HS-SRC-RUN', only('C-HS-SRC', lambda: load_hs(None, 'CERTIFIED', pins=dict(PINS, **{HS_RECORD[1]: '0' * 64}))))
    try:
        HSR, hsw = hs_rows(HSD), 'COEF ' + ', '.join('N%d_%s %s' % (N, c, HSD['N%d_%s_R000' % (N, c)].split()[-1]) for N in (4, 3) for c in ('D3', 'D4', 'D4M'))
    except Refused as e:
        HSR, hsw = None, 'refused: %s' % e
    out('C-HS-RECORD: C-HS-NOTE (LEMMA_NOTE = the pinned HS_NORMX_LEMMA_NOTE_v1 %s), C-HS-OP (OPERATOR_D3, OPERATOR_D4, OPERATOR_D4M exact; NORMALIZATION %s), C-HS-INV, C-HS-LAMBDA (p = 2 for D3, 1 for D4 and D4M), C-HS-J (METHOD in %s, ranges), C-HS-MIRROR (MIRROR_D4M = ADJOINT_OF_D4, the D4M row keys = the D4 ones): %s -> %s' % (
        PINS[HS_NOTE][:8], HS_NORM, '/'.join(HS_METHODS), hsw, gate(fails, 'C-HS-RECORD', HSR is not None)))
    out('C-HS-D3-SAME: every key of the D3 record %s (%s) but CODE and END is unchanged in the combined record (ADD1 sect. 2) -> %s' % (
        os.path.basename(HS_RECORD_D3), PINS[HS_RECORD_D3][:8], gate(fails, 'C-HS-D3-SAME', flag(lambda: hs_d3_same(HSD)))))
    plant(nofire, 'PLANT-HS-D3-SAME', only('C-HS-D3-SAME', lambda: hs_d3_same(dict(HSD, N4_D3_R000=HSD['N4_D3_R000'] + '1'))))   # v1_37 (5): one D3 row changed
    out('C-HS-OP-SPEC: HS_OP_D4 and HS_OP_D4M equal OPERATOR_D4 and OPERATOR_D4M of %s (%s) line for line -> %s' % (
        os.path.basename(HS_ADD1), PINS[HS_ADD1][:8], gate(fails, 'C-HS-OP-SPEC', flag(lambda: hs_op_spec()))))
    plant(nofire, 'PLANT-HS-OP-SPEC', only('C-HS-OP-SPEC', lambda: hs_op_spec(ops=(HS_OP_D4.replace('w = 2', 'w = 3'), HS_OP_D4M))))   # v1_37 (5)
    for nm, tag, dd in (('PLANT-HS-NOTE', 'C-HS-NOTE', dict(HSD, LEMMA_NOTE=HSD['LEMMA_NOTE'][:-8] + '00000000')),
                        ('PLANT-HS-OP-W2', 'C-HS-OP', dict(HSD, OPERATOR_D3=HS_OP_D3.replace('w = 3', 'w = 2'))),
                        ('PLANT-HS-OP-D4', 'C-HS-OP', dict(HSD, OPERATOR_D4=HS_OP_D4.replace('w = 2', 'w = 3'))),   # v1_37 (5)
                        ('PLANT-HS-OP-NORM2', 'C-HS-OP', dict(HSD, NORMALIZATION='HS2_TR_XC_STAR_XC_OVER_LAMBDA0_2W')),
                        ('PLANT-HS-LAMBDA', 'C-HS-LAMBDA', dict(HSD, LAMBDA_POWER_D3='1')),
                        ('PLANT-HS-LAMBDA-D4', 'C-HS-LAMBDA', dict(HSD, LAMBDA_POWER_D4='2')),   # v1_37 (5)
                        ('PLANT-HS-J-POINT', 'C-HS-J', dict(HSD, N4_D3_METHOD='POINT')),
                        ('PLANT-HS-J-JLOJHI', 'C-HS-J', dict(HSD, N4_D3_R000='300 300 0.94 1.06 0.94 1.06 44.4')),
                        ('PLANT-HS-MIRROR', 'C-HS-MIRROR', dict(HSD, N4_D4M_R000=HSD['N4_D4M_R000'] + '1'))):   # v1_37 (5): one D4M row changed
        plant(nofire, nm, only(tag, lambda dd=dd: hs_rows(dd)))
    if HSR is not None:
        plant(nofire, 'PLANT-HS-CBOX', only('C-HS-CBOX', lambda: hs_piece((HSR[(4, 'D3')][0], HSR[(4, 'D3')][1], (Fraction('1.07'), Fraction('1.2')), HSR[(4, 'D3')][3], HSR[(4, 'D3')][4]),
                                                                          P[4][0][1], P[4][0][2], MEANS[(4, P[4][0][0])][0], MEANS[(4, P[4][0][0])][0], arb(1))))
    plant(nofire, 'PLANT-HS-COV', only('C-HS-COV', lambda: hs_cov_check(arb('0.001'), arb('0.01'))))
    SPOT, hs_first, spw = {}, {}, ''   # v1_35 (6): C-HS-SPOT (a control): the record spot values and the first piece's normX_HS, per (N, class) since v1_37 (5)
    try:
        SPOT = dict(((N, c), hs_spot(HSD, N, cls=c)) for N in (4, 3) for c in ('D3', 'D4', 'D4M'))
    except Refused as e:
        spw = str(e)
    RTC = dict(((N, cls), route_consts(N, cls, CE[N], KAP[N])) for N in (4, 3) for cls in ('D3', 'D4', 'D4M'))   # v1_35 (5)
    RHOR = {}   # v1_35 (5): Lemma R at its own eps_R (pk02 08:36Z): (rho_terms at eps_R, Phi_W at eps_R by Lemma T-prime)
    for N in (4, 3):
        RHOR[N] = (rho_terms(QT[N], arb(RHO_EPS_R), 1 / arb(300)), phi_T(N, arb(1), lg_weights(arb(RHO_EPS_R), thg)[1], LG[N]['g00']))
    rrok = all((RHOR[N][0][5] >= RHOR[N][0][2]) and flag(lambda N=N: check_sigma(RHOR[N][0][4], RHOR[N][0][0], RHOR[N][0][1], RHOR[N][0][3], RHOR[N][0][2]))
               for N in (4, 3))
    out('C-RHO-R: Lemma R at eps_R = %s in (0, 1) (Lemma G keeps eps %s): r* >= r0 (the closed form branch) and no grid value of h on [r0, 50 r0] above sigma_R, both N; sigma_R N4 %s, N3 %s; Phi_W,R N4 %s, N3 %s -> %s' % (
        RHO_EPS_R, EPS_G, dec_hi(RHOR[4][0][4]), dec_hi(RHOR[3][0][4]), dec_hi(RHOR[4][1]), dec_hi(RHOR[3][1]), gate(fails, 'C-RHO-R', rrok)))
    plant(nofire, 'PLANT-RHO-SIGMA-R', lambda: check_sigma(RHOR[4][0][4] / 2, RHOR[4][0][0], RHOR[4][0][1], RHOR[4][0][3], RHOR[4][0][2]))
    for N in (4, 3):
        out('INFO RHO-R N=%d: eps_R %s: sigma_R %s, r0 %s, r* %s, Phi_W,R %s (Lemma G eps %s: sigma %s, Phi_W %s)' % (
            N, RHO_EPS_R, dec_hi(RHOR[N][0][4]), RHOR[N][0][2].str(8, radius=False), RHOR[N][0][5].str(8, radius=False), dec_hi(RHOR[N][1]),
            EPS_G, dec_hi(RHO[N][0][4]), dec_hi(RHO[N][2])))
    plant(nofire, 'PLANT-RHO-PAIR', only('C-RHO-R', lambda: r8_pair(4, KAP[4], RHOR[4][0][4], RHO_EPS_R, RHO[4][2], EPS_G, LG[4]['pe'])))
    R8 = dict((N, r8_pair(N, KAP[N], RHOR[N][0][4], RHO_EPS_R, RHOR[N][1], RHO_EPS_R, LG[N]['pe'])) for N in (4, 3))   # v1_35 (5): ecs_rho's constant, Lemma R at eps_R
    for (N, cls) in sorted(RTC):
        k_ = RTC[(N, cls)]
        out('INFO ROUTE-TERMS N=%d %s: e_11 %s (level %s), s-part %s (level %s), DOUBLE gg %s (level %s)%s' % (
            N, cls, dec_hi(k_['e11'][0]), k_['e11'][1], dec_hi(k_['s11'][0]), k_['s11'][1], dec_hi(k_['ggd'][0]), k_['ggd'][1],
            '' if cls != 'D3' else '; ecs_rho constant R8 %s' % dec_hi(R8[N])))
    rt_ok, e2_ok, cp_ok, cord_ok, rt_cnt, rho_rng, cov_min, rrows = True, True, True, True, {}, {}, {}, []
    hs_used, hs_fail, hs_cov = {}, [], []
    for N in (4, 3):
        sq = 2 * CE[N]['sp'] + CE[N]['sp'] * CE[N]['sp']
        for cls in ('D3', 'D4', 'D4M'):
            pre, wX, kf = CLS[cls]
            lev, glev, slev = NORMX_LEVELS[(N, cls)], E2_GLEV[(N, cls)], E2_SLEV[(N, cls)]
            audit.append(('N%d_%s_PIECES' % (N, cls), '904'))
            for idx, jlo, jhi in P[N]:
                ex2, cov, me, mf = joint_enclosure(E[N], pre, jlo, jhi)
                key = 'N%d_%s_P%s' % (N, cls, idx)
                rec = None if CERT_MODE else C28.get(('N%d_%s' % (N, cls), idx))
                if (not CERT_MODE) and (rec is None or rec[0] != jlo or rec[1] != jhi):
                    raise Refused('P2-8 record row %s missing or off the grid' % key)
                c28 = None if CERT_MODE else arb(rec[2]).lower()
                covx = covx if CERT_MODE else max(covx, abs(float(cov.lower()) / float(rec[2]) - 1))
                e2sm = ex2.upper()
                pxsm, _c = (None, None) if CERT_MODE else px_from(e2sm, c28, abs(c28) + 1)
                cer, cfr = (me.lower(), me.upper()), (mf.lower(), mf.upper())
                eme, _f = lemma_e(N, cls, 1, 0, glev, cer, cfr, CE[N])
                emf, _f = lemma_e(N, cls, 0, 1, glev, cer, cfr, CE[N])
                spe = sq * norm_win(N, cls, 1, 0, slev, cer, cfr, KAP[N])
                spf = sq * norm_win(N, cls, 0, 1, slev, cer, cfr, KAP[N])
                ss = 1 - CE[N]['sp'] * CE[N]['sp']
                ce_s = mean_ends(me, E1[N], eme, spe, ss)   # v1_11 (3), since v1_35 the single-trick reference of C-MEAN-DT
                if (N, idx) not in MEANS:
                    raise Refused('C-MEAN-PARTS: no double-trick means at %s' % key)
                ce = MEANS[(N, idx)][0]   # v1_35 (3): c_t by the double trick, one ball per (N, piece)
                mdt_ok = mdt_ok and ovl(ce, ce_s)
                cm_, cw_ = float(((ce[0] + ce[1]) / 2).mid()), float((ce[1] - ce[0]).upper())   # v1_25 (5): each class c_t ball
                q_ = CEC.setdefault((N, cls), [0.0, 0.0, 1e300, -1e300, 0.0])
                if idx == '0000':
                    q_[0], q_[1] = cm_, cw_
                q_[2], q_[3], q_[4] = min(q_[2], cm_), max(q_[3], cm_), max(q_[4], cw_)
                cf_s = mean_ends(mf, E1[N], emf, spf, ss)   # v1_35 (3): the single-trick reference
                cf = ce if cls == 'D3' else MEANS[(N, idx)][1]   # v1_35 (3): c_bb = c_t (the flip); c_b = Tb (S7 A,0), w = 1
                mdt_ok = mdt_ok and ovl(cf, cf_s)
                rows_mn.append((key, ' '.join((jlo, jhi, dec_lo(ce[0]), dec_hi(ce[1]), dec_lo(cf[0]), dec_hi(cf[1])))))   # v1_22
                lo_c, hi_c = CE_T.get((N, idx), (ce[0], ce[1]))
                CE_T[(N, idx)] = (ce[0] if ce[0] > lo_c else lo_c, ce[1] if ce[1] < hi_c else hi_c)   # v1_24 (1): the intersection over the classes
                mt_, mf_ = arb(MEAN_FLOAT[N]), arb(MEAN_FLOAT[N] if cls == 'D3' else MEANV_FLOAT[N])
                mn_ok = mn_ok and (ce[0] <= ce[1]) and (cf[0] <= cf[1]) and (ce[0] > 0) and (cf[0] > 0) and \
                    ((idx != '0000') or ((ce[0] <= mt_) and (mt_ <= ce[1]) and (cf[0] <= mf_) and (mf_ <= cf[1])))   # v1_23
                lo_, hi_ = mn_ext.get(N, (ce[0], ce[1]))
                mn_ext[N] = (ce[0] if ce[0] < lo_ else lo_, ce[1] if ce[1] > hi_ else hi_)
                mn_w[N] = max(mn_w.get(N, 0.0), float(((ce[1] - ce[0]) / mt_).upper()))   # v1_23
                e2c = e2_enclosure_c(E[N], pre, jlo, jhi, ce[0].union(ce[1]), cf[0].union(cf[1]))
                ef, F = lemma_e(N, cls, 2, 2, glev, ce, cf, CE[N])
                s2 = sq * norm_win(N, cls, 2, 2, slev, ce, cf, KAP[N])
                e2hi = (e_upper(e2c.upper() * (1 + E1[N]) + ef) + s2).upper()   # v1_11 (3): max(R, 0)
                e2up = e2up and (e2hi >= e2sm)
                cp_row = flag(lambda: check_cov_prod(ce, cf))   # v1_37 (2): C-COV-PROD per row, a failing row named before the run stops
                cp_ok = cp_ok and cp_row
                if not cp_row:
                    out('C-COV-PROD %s: a mean ball whose lower end is not certainly positive; the routes multiply both, so the run stops at this row -> %s' % (key, gate(fails, 'C-COV-PROD', False)))
                    raise Refused('C-COV-PROD: row %s (named on the line above)' % key)
                covs, rinfo, covh = routes_piece(N, cls, RTC[(N, cls)], E[N], EX[N], pre, jlo, jhi, ce, cf, CE[N], E1[N], 1 - CE[N]['sp'] * CE[N]['sp'], KAP[N], PORT[(N, idx)], R8[N], glev, slev)   # v1_35 (5)
                rt, cvl = pick_route(cls, covs)
                rt_ok = rt_ok and flag(lambda: check_route(cls, rt, cvl, covs))
                rt_cnt[(N, cls, rt)] = rt_cnt.get((N, cls, rt), 0) + 1
                e2_ok = e2_ok and flag(lambda: check_e2t(rinfo[0], rinfo[1]))   # v1_36 (3): the test as a function (PLANT-D4S-E2)
                if rinfo[2] is not None:
                    rr = rho_rng.get(N, (1e300, 0.0))
                    rho_rng[N] = (min(rr[0], float(rinfo[2].lower()), float(rinfo[3].lower())), max(rr[1], float(rinfo[2].upper()), float(rinfo[3].upper())))
                cvs = dec_lo(cvl)
                cvh = dec_hi(cov_inf_hi(covh, cls))   # v1_37 (6): Cov_inf_hi = min over the admissible routes of E11_hi - c_e,lo c_f,lo
                cord_ok = cord_ok and flag(lambda: check_cov_order(cvs, cvh))
                rows_mn[-1] = (rows_mn[-1][0], rows_mn[-1][1] + ' ' + cvs + ' ' + cvh)   # v1_37 (6): the means row carries Cov_inf_lo and Cov_inf_hi
                px, cmin = px_from(e2hi, arb(cvs), abs(arb(cvs)) + 1)   # v1_35 (5): the route maximum replaces P2-8's record value
                rrows.append('\t'.join((str(N), cls, idx, jlo, dec_lo(covs['SINGLE']), dec_lo(covs['CS'] if cls == 'D3' else covs['DOUBLE']), rt)))
                if (N, cls) not in cov_min or float(cvl) < cov_min[(N, cls)][0]:
                    cov_min[(N, cls)] = (float(cvl), idx)
                nx, box = normx_sprime(N, cls, lev, ce, cf, KAP[N])
                nx_s = nx   # v1_35: Lemma S' itself, for C-NORMX-FLOAT and the AUDIT lines; the rows carry the HS min
                nsrc = 'LEMMA_S_PRIME'   # v1_37 (5): the row's normX source, for the route TSV
                if HSR is not None:   # v1_35 (6), v1_37 (5): the normX_HS slot for every class, normX_hi = min(Lemma S', HS)
                    try:
                        nxh = hs_piece(HSR[(N, cls)], jlo, jhi, ce, cf, PORT[(N, idx)][2].lower(), HS_P[cls])
                        if idx == '0000':
                            hs_first[(N, cls)] = nxh
                    except Refused as e:
                        hs_fail.append((N, cls, idx, str(e)))
                        nxh = None
                    if nxh is not None and not flag(lambda: hs_cov_check(nxh, cvl)):
                        hs_cov.append((N, cls, idx))
                    elif nxh is not None and nxh < nx:
                        nx, nsrc = nxh, 'HS_INV'
                        hs_used[(N, cls)] = hs_used.get((N, cls), 0) + 1
                rrows[-1] += '\t%s\t%s' % (nsrc, dec_hi(nx))
                if idx == '0000':
                    first[(N, cls)] = (nx_s, ce, cf, e2hi - e2sm, ef, s2)
                e2s = dec_hi(e2hi)
                vals = (cvs, px_print(e2s, cvs), dec_hi(nx), e2s, rt)   # v1_35 (5): the 7th column ROUTE
                rows_jt.append((key, ' '.join((jlo, jhi) + vals)))
                gf = gd['N%d_P%s' % (N, idx)].split('|')[0].split()
                for d in (() if CERT_MODE else (3, 4)):
                    e = arb(gf[16])
                    for _ in range(d):
                        e = e * arb(gf[7])
                    j0 = float(((arb(rec[2]) - 2 * e * px - e * e * nx) / arb(rec[2])).lower())
                    dhp[(N, cls, d)] = min(dhp.get((N, cls, d), j0), j0)
                r = None if CERT_MODE else ref.get(key)
                if r is None or r[0] != jlo or r[1] != jhi:
                    worst['Cov_inf_lo'] = float('inf')
                    continue
                for j, val in ((0, rec[2]), (1, dec_hi(pxsm)), (3, dec_hi(e2sm))):
                    fld = ('Cov_inf_lo', 'pX_hi', 'normX_hi', 'E2_hi')[j]
                    worst[fld] = max(worst[fld], abs(float(val) / float(r[2 + j]) - 1))
            audit.append(('AUDIT_N%d_%s' % (N, cls), 'normX levels %s %s, kappa <= %s, normX_hi %s; E2 g-levels %s %s, s-levels %s %s, Delta_E2 %s on the '
                          'first piece%s' % (lev[0], lev[1], dec_hi(KAP[N]), dec_hi(first[(N, cls)][0]), glev[0], glev[1], slev[0], slev[1],
                                                            dec_hi(first[(N, cls)][3]), ' (MOCK constants)' if MODE != 'cert' else '')))
    out('C-MEAN-DT: on every row the double-trick means (c_t; c_bb = c_t; c_b = Tb) meet the single-trick Lemma E-prime balls (a sanity check) -> %s' % gate(
        fails, 'C-MEAN-DT', mdt_ok))
    out('C-E2: E2_hi (Lemma E) >= the uncorrected SM value on every row -> %s' % gate(fails, 'C-E2', e2up))
    out('C-ROUTE: on every row the exported route is admissible for its class (ROUTE_OK) and Cov_inf_lo is the largest admissible route value -> %s' % gate(
        fails, 'C-ROUTE', rt_ok))
    plant(nofire, 'PLANT-ROUTE-D3-DOUBLE', only('C-ROUTE', lambda: check_route('D3', 'DOUBLE', arb(1), {'DOUBLE': arb(1), 'SINGLE': arb(0)})))
    plant(nofire, 'PLANT-ROUTE-ABOVE', only('C-ROUTE', lambda: check_route('D4', 'DOUBLE', arb(2), {'DOUBLE': arb(1), 'SINGLE': arb(0)})))
    out('C-COV-PROD: on every row both mean balls the routes multiply (c_e, c_f) are certainly positive at their lower ends (cov_from\'s test) -> %s' % gate(
        fails, 'C-COV-PROD', cp_ok))
    plant(nofire, 'PLANT-COV-PROD', only('C-COV-PROD', lambda: cov_from(arb(1), (arb(0), arb(1)), (arb(1), arb(1)))))   # v1_36 (3): c_e,lo = 0
    plant(nofire, 'PLANT-ROUTE-LARGER', only('larger', lambda: check_route('D4', 'SINGLE', arb(0), {'DOUBLE': arb(1), 'SINGLE': arb(0)})))   # v1_36 (3)
    out('C-COV-ORDER: on every row Cov_inf_lo <= Cov_inf_hi, both finite decimals (Cov_inf_hi = min over the admissible routes of E11_hi - c_e,lo c_f,lo; the means export carries both) -> %s' % gate(
        fails, 'C-COV-ORDER', cord_ok))
    plant(nofire, 'PLANT-COV-ORDER', only('C-COV-ORDER', lambda: check_cov_order(rows_mn[0][1].split()[7], rows_mn[0][1].split()[6])))   # v1_37 (6): the first row's pair swapped
    for N in (4, 3):
        for cls in ('D3', 'D4', 'D4M'):
            out('INFO ROUTES N=%d %s: %s; smallest Cov_inf_lo %.6e at piece %s' % (N, cls, ', '.join('%s %d' % (r, rt_cnt.get((N, cls, r), 0)) for r in ROUTE_OK[cls]),
                                                                              cov_min[(N, cls)][0], cov_min[(N, cls)][1]))
    out('C-ECS-PHI: the CS route uses rho_(phi,ij)^2 by its Q-form bound 1 + R8 G_00,hi/M_ij,lo (R8 N4 %s, N3 %s): rho^2 in [%.4g, %.4g] (N4), [%.4g, %.4g] (N3) -> %s' % (
        dec_hi(R8[4]), dec_hi(R8[3]), rho_rng[4][0], rho_rng[4][1], rho_rng[3][0], rho_rng[3][1], gate(fails, 'C-ECS-PHI', rho_rng[4][0] >= 1 and rho_rng[3][0] >= 1)))
    plant(nofire, 'PLANT-ECS-PHI', only('C-ECS-PHI', lambda: ecs_rho_used(arb(1), R8[4], PORT[(4, P[4][0][0])][3].upper(),
                                                                         entry_piece(E[4]['M3_02'], PORT[(4, P[4][0][0])][6]).lower())))
    plant(nofire, 'PLANT-M-POS', only('C-M-POS', lambda: ecs_rho(R8[4], arb(1), arb(0))))
    out('C-ECS-LEVEL: each CS box term and the tail term it joins come from one level, in the g-part (Sigma_tails) and in the s-part (the S-prime tail rows) -> %s' % gate(
        fails, 'C-ECS-LEVEL', flag(lambda: ecs_level('10', '10'))))
    plant(nofire, 'PLANT-ECS-LEVEL', only('C-ECS-LEVEL', lambda: ecs_level('10', '12')))
    out('C-ECS-E2/C-D4S-LEVEL (sanity): E2_t (Lemma E-prime, m = 2) is at least the trial ratio M_20/M_00 on every piece (E2_bb = E2_t by the flip); sigma_D4 takes the b-tail at its own split level -> %s' % gate(
        fails, 'C-ECS-E2', e2_ok))
    plant(nofire, 'PLANT-D4S-LEVEL', only('C-D4S-LEVEL', lambda: sigma_d4(4, CE[4]['sp'], arb(2), KAP[4], '10', arb(1), '12')))
    plant(nofire, 'PLANT-D4S-E2', only('C-ECS-E2', lambda: check_e2t(arb(1), arb(2))))   # v1_36 (3): E2_t below the trial ratio
    out('C-RHO-F1: rho_phi = 1 + 2 sigma_eps sqrt(Phi_W) from Lemma R with Lemma T-prime and the S7 certified G_00 lower end: N4 %s, N3 %s -> %s' % (
        dec_hi(RHO[4][1]), dec_hi(RHO[3][1]), gate(fails, 'C-RHO-F1', flag(lambda: rho_f1_check('S7_CERTIFIED_G00')))))
    plant(nofire, 'PLANT-RHO-F1', only('C-RHO-F1', lambda: rho_f1_check('G00_MOCK')))
    out('C-HS-CBOX/C-HS-J (per piece): every piece of D3, D4 and D4M inside its HS row J range and its mean balls inside the row box: %d refusals%s -> %s' % (
        len(hs_fail), (' (first %s)' % (hs_fail[0],)) if hs_fail else '', gate(fails, 'C-HS-CBOX', HSR is not None and not hs_fail)))
    out('C-HS-COV: normX_HS >= max(Cov_inf_lo, 0) on every piece served (D3, D4, D4M): %d failures -> %s' % (len(hs_cov), gate(fails, 'C-HS-COV', not hs_cov)))
    out('INFO C-HS-MIN: normX_hi = min(Lemma S-prime, normX_HS) per piece and class (both valid upper bounds); HS smaller on %s of 904 pieces each' % (
        ', '.join('N%d_%s %d' % (N, c, hs_used.get((N, c), 0)) for N in (4, 3) for c in ('D3', 'D4', 'D4M'))))
    spok = bool(SPOT) and all(k in hs_first and (hs_first[k] * hs_first[k]) >= _frac_ball(SPOT[k], SPOT[k]).upper() for k in SPOT)   # v1_37 (5): every class
    out('C-HS-SPOT (a control): HS2_hi on the first piece of each class is at least the float spot value 2 Cov(X_c, theta X_c) + Cov^2 at the half-step plane from kt_s8rf_v1 (outputs %s %s): %s%s -> %s' % (
        PINS[HS_SPOT_SRC[4]][:8], PINS[HS_SPOT_SRC[3]][:8], '; '.join('N%d_%s %s vs %.6e' % (k[0], k[1], dec_hi(hs_first[k] * hs_first[k]) if k in hs_first else '-', SPOT[k]) for k in sorted(SPOT)),
        (' (%s)' % spw) if spw else '', gate(fails, 'C-HS-SPOT', spok)))
    plant(nofire, 'PLANT-HS-SPOT', only('C-HS-SPOT', lambda: hs_spot(dict(HSD, N4_D3_SPOT=HSD['N4_D3_SPOT'].replace(PINS[HS_SPOT_SRC[4]], '0' * 64)), 4)))
    plant(nofire, 'PLANT-HS-SPOT-D4', only('C-HS-SPOT', lambda: hs_spot(dict(HSD, N4_D4_SPOT=HSD['N4_D4_SPOT'].replace(PINS[HS_SPOT_SRC[4]], '0' * 64)), 4, cls='D4')))   # v1_37 (5)
    RTSV = os.path.join(XOUT, 'routes_%s_%s.tsv' % (LABEL, MODE))
    if not _in_dir(RTSV, XOUT):
        raise ValueError('route TSV outside mocks/out')
    with open(RTSV, 'x') as fh:
        fh.write('# routes of %s (%s run): per piece the SINGLE and the DOUBLE (D4, D4M) or CS (D3) Cov lower ends, the route taken, and the normX_hi source (LEMMA_S_PRIME or HS_INV) with its value\n' % (LABEL, MODE))
        fh.write('N\tclass\tpiece\tJ_lo\tCov_SINGLE_lo\tCov_ROUTE2_lo\troute\tnormX_src\tnormX_hi\n')
        fh.write('\n'.join(rrows) + '\n')
    out('ROUTE-TSV %s sha256 %s rows %d' % (os.path.basename(RTSV), sha_file(RTSV), len(rrows)))
    for (N, cls) in sorted(first):
        if cls == 'D4M':
            continue
        dE = float(first[(N, cls)][3].upper())
        rel = abs(dE / E2B_FLOAT[(N, cls)] - 1)
        out('E2 N=%d %s: Delta_E2 %.4f on the first piece (e_f %s, s-part %s) against e2_bound_v4\'s %.4f: relative %.2e' % (
            N, cls, dE, dec_hi(first[(N, cls)][4]), dec_hi(first[(N, cls)][5]), E2B_FLOAT[(N, cls)], rel))
        gate(fails, 'C-E2-FLOAT N=%d %s' % (N, cls), rel <= 0.3)
    out('C-E2-FLOAT: Delta_E2 against e2_bound_v4 (theta 0.7, Lemma T-prime, rho_phi with it, certified eps_r and s) within 30%% (Lemma E-prime: the same Phi_eps, S-prime, A_theta and levels; the means +-1%% there) -> %s' % (
        'PASS' if not [x for x in fails if x.startswith('C-E2-FLOAT')] else 'FAIL'))
    for N in (() if CERT_MODE else (4, 3)):
        for cls in ('D3', 'D4', 'D4M'):
            d3, d4 = dhp[(N, cls, 3)], dhp[(N, cls, 4)]
            if N == 4:
                verdict = ('d^h = 3 if certified (FLOAT slack positive on every row); the rule holds N4 at 4 until kt_s9h\'s certified DH' if d3 > 0 else 'd^h = 4 (the rule for N4; FLOAT slack at d = 3 not positive)')
            else:
                verdict = 'd^h = 3 if certified (FLOAT slack positive on every row)' if d3 > 0 else 'd^h = 4 (FLOAT slack at d = 3 not positive)'
            out('INFO DH-PREVIEW N=%d %s: min J0/Cov d=3 %.4f, d=4 %.4f (corrected pX, Lemma S\' normX, FLOAT grid e) -> %s; the certified '
                'decision is kt_s9h\'s DH_N%d_%s' % (N, cls, d3, d4, verdict, N, cls))
    for N in (4, 3):
        lo_, hi_ = mn_ext[N]
        out('INFO MEANS N=%d: c_t over every piece and class in [%s, %s] (the double-trick means); for SH4 (N - 1)/2 - c_t,hi = %s; largest relative width of c_t %.4f' % (
            N, dec_lo(lo_), dec_hi(hi_), dec_lo(arb(N - 1) / 2 - hi_), mn_w[N]))
    out('C-MEANS: %d rows; every mean ball ordered and positive, and every first piece contains the J = 300 FLOAT mean (t and bb %s, b %s at N4) -> %s' % (
        len(rows_mn), MEAN_FLOAT[4], MEANV_FLOAT[4], gate(fails, 'C-MEANS', mn_ok and len(rows_mn) == 5424)))
    cok = True   # v1_24 (1)
    for N in (4, 3):
        mlo, mhi = None, None
        for idx, _jl, _jh in P[N]:
            lo_c, hi_c = CE_T[(N, idx)]
            cok = cok and (lo_c <= hi_c)
            mlo = lo_c if (mlo is None or lo_c < mlo) else mlo
            mhi = hi_c if (mhi is None or hi_c > mhi) else mhi
        cN = 2 + arb((N - 1) * (N - 3)) / 8
        out('INFO CE-T N=%d: c_t per piece (intersection over the classes): min ce_lo %s, max ce_hi %s; SH4 gate (N - 1)/2 - c_N/300 = %s; pk07 binding ce_lo >= %s' % (
            N, dec_lo(mlo), dec_hi(mhi), dec_lo(arb(N - 1) / 2 - cN / 300), CE_LO_NEED[N]))
    out('C-CE-T: the intersection of the three classes c_t balls is non-empty on every piece, both N -> %s' % gate(fails, 'C-CE-T', cok))
    for N in (4, 3):   # v1_25 (5): the note on v1_24
        out('INFO CE-CLASS N=%d: c_t ball per class, first piece mid (width), then the mid range and the largest width over the pieces: %s' % (
            N, '; '.join('%s %.6f (%.2e), [%.6f, %.6f], %.2e' % ((cls,) + tuple(CEC[(N, cls)])) for cls in ('D3', 'D4', 'D4M'))))
    c1s = open(C1_SOURCE[0]).read().count(C1_CLAIM) == 1 and open(C1_SOURCE[1]).read().count(C1_NOSPACE) == 1
    out('C-C1-SOURCE: the pinned SPEC_M2B_CERT_v1_ADD3.md holds C1_CLAIM once and kt_s9h_m21.py holds C1_NOSPACE once -> %s' % gate(fails, 'C-C1-SOURCE', c1s))
    ok = len(rows_jt) == 5424 and worst['Cov_inf_lo'] <= 1e-4 and worst['pX_hi'] <= 1e-4 and worst['E2_hi'] <= 1e-4
    if not CERT_MODE: out('C-REPF: %d rows against %s: worst relative Cov_inf_lo %.2e, pX_hi %.2e, E2_hi %.2e (pX_hi and E2_hi uncorrected, the SM route; normX_hi left out: its FLOAT reference carries the old '
        'product form) -> %s' % (len(rows_jt), os.path.basename(JOINTF), worst['Cov_inf_lo'], worst['pX_hi'], worst['E2_hi'], gate(fails, 'C-REPF', ok)))
    if not CERT_MODE: out('C-COVX: the SM route\'s Cov lower end against P2-8\'s record (MOCK): worst relative %.2e (a cross-check, 1e-4) -> %s' % (
        covx, gate(fails, 'C-COVX', covx <= 1e-4)))
    worstnx = 0.0
    for (N, cls) in sorted(first):
        nx0 = first[(N, cls)][0]
        refnx = NX_FLOAT[(N, 'D3' if cls == 'D3' else 'D4')]
        rel = abs(float(nx0.upper()) / refnx - 1)
        worstnx = max(worstnx, rel)
        out('NORMX N=%d %s: normX_hi %s at levels %s (Lemma S\') against float_check_schur_v2\'s %.4f: relative %.2e' % (
            N, cls, dec_hi(nx0), ' '.join(NORMX_LEVELS[(N, cls)]), refnx, rel))
    out('C-NORMX-FLOAT: worst relative %.2e (2e-2) -> %s' % (worstnx, gate(fails, 'C-NORMX-FLOAT', worstnx <= 2e-2)))
    nx0, ce0, cf0 = first[(4, 'D4')][:3]
    big = tuple(str(float(x) + 20) for x in NORMX_LEVELS[(4, 'D4')])
    nxb, boxb = normx_sprime(4, 'D4', big, ce0, cf0, KAP[4])
    tailb = float((nxb - boxb).upper())
    out('C-NORMX-BOX: at levels %s the tails are %.3e of the box (at most 1e-9) -> %s' % (
        ' '.join(big), tailb / float(boxb.lower()), gate(fails, 'C-NORMX-BOX', tailb <= 1e-9 * float(boxb.lower()))))
    plant(nofire, 'PLANT-NORMX-LEVEL', lambda: normx_sprime(4, 'D4', (str(float(ce0[1]) + 0.5), NORMX_LEVELS[(4, 'D4')][1]), ce0, cf0, KAP[4]))
    plant(nofire, 'PLANT-NORMX-HLEVEL D3', lambda: norm_win(4, 'D3', 2, 2, ('1', '14'), (arb(1), arb(2)), (arb(1), arb(2)), KAP[4]))
    plant(nofire, 'PLANT-NORMX-HLEVEL D4', lambda: norm_win(4, 'D4', 2, 2, ('1', '9'), (arb(1), arb(2)), (arb(1), arb(2)), KAP[4]))

    STAGE[0] = 'exports'
    need('exports')
    import mpmath   # v1_36 (1): C-S9H-LOAD compares mpmath's global precisions too
    s9b = (resource.getrlimit(resource.RLIMIT_CPU), resource.getrlimit(resource.RLIMIT_FSIZE), resource.getrlimit(resource.RLIMIT_AS),
           signal.getsignal(signal.SIGXCPU), list(sys.argv), os.getcwd(), ctx.prec, mpmath.mp.prec, mpmath.iv.prec)
    RD = s9h_load()   # v1_36 (1), the review K-1, the review The readers from their checked bytes
    s9a = (resource.getrlimit(resource.RLIMIT_CPU), resource.getrlimit(resource.RLIMIT_FSIZE), resource.getrlimit(resource.RLIMIT_AS),
           signal.getsignal(signal.SIGXCPU), list(sys.argv), os.getcwd(), ctx.prec, mpmath.mp.prec, mpmath.iv.prec)
    out('C-S9H-LOAD: %s (%s) read once, checked against its full sha256 pin and run from those bytes; rlimits, the SIGXCPU handler, argv, cwd and the flint and mpmath precisions unchanged -> %s' % (
        os.path.basename(RDR_PATH), PINS[RDR_PATH][:8], gate(fails, 'C-S9H-LOAD', s9a == s9b and s9a[3] is _on_xcpu)))
    plant(nofire, 'PLANT-S9H-PIN', only('C-S9H-LOAD', lambda: s9h_load(dict(PINS, **{RDR_PATH: '0' * 64}))))
    GRD = s9h_grid(RD)
    out('C-S9H-GRID: the readers\' joint_grid (v2_2\'s pinned export) equals this run\'s grid string for string (%d pieces) -> %s' % (
        len(GRD), gate(fails, 'C-S9H-GRID', GRD == [(jlo, jhi) for _i, jlo, jhi in P[4]])))
    READERS = s9h_readers(RD, GRD)   # v1_36 (1): one reader per RECORD, for the cert writer and the read-back
    PARTS = sorted(f for f in os.listdir(COUT) if f.endswith('.part'))   # v1_37 (1)
    out('INFO C-CERT-EXISTS/PART: this run\'s temporary names end in .%s.part; .part files that earlier refused cert writes left in pk15/out (harmless; nothing here deletes, move them aside by hand): %s' % (
        RUN_TAG, ', '.join(PARTS) if PARTS else 'none'))
    out('C-COV-POS: Cov_inf_lo > 0 exactly on every joint row as printed (the consumer\'s C-SRC-J needs it) -> %s' % gate(
        fails, 'C-COV-POS', flag(lambda: check_pos(rows_jt, JT_FIELDS, ('Cov_inf_lo',), 'C-COV-POS'))))
    plant(nofire, 'PLANT-COV-POS', only('C-COV-POS', lambda: check_pos([zero_field(rows_jt[0], JT_FIELDS, 'Cov_inf_lo')], JT_FIELDS, ('Cov_inf_lo',), 'C-COV-POS')))
    STJ, NMJ, JUJ = status_junif(dict(FINM, kt_p2_assembly=OWN_FLOAT_JT), open_conditions(M2BL))   # v1_35 (7): the joint and means exports
    out('INFO JUNIF: the joint and means exports\' certified-path triple from status_junif: status %s, FLOAT_IN %s, J_UNIFORMITY %s; C-JUNIF-STATUS after the writes tests it, the t triple and the pairs as written' % (
        STJ, NMJ, 'J_UNIF_PP' if JUJ == J_UNIF_PP else 'the ASSUMED string'))
    plant(nofire, 'PLANT-JUNIF-STATUS', only('C-JUNIF-STATUS', lambda: check_status_junif('CERTIFIED_GIVEN_FLOAT_IN', 'x: y', J_UNIF_PP)))
    common = (('FORMAT', 'S4U_KV_v1' if MODE == 'cert' else 'S4U_KV_v1 MOCK'), ('AUTHOR', 'pk15'), ('PRODUCER', 'pk15'), ('CODE', 'pk15/%s.py:%s' % (LABEL, SELF[:8])),
              ('J_MIN', '300'), ('TAG', '%s %s %s' % ('CERTIFIED' if MODE == 'cert' else 'MOCK', LABEL, SELF[:8])), ('EXPORT_STATUS', 'MOCK'),
              ('CLAIM', CLAIM_CERT if MODE == 'cert' else 'MOCK skeleton output from mock inputs; reader and layout tests only'), ('RUN_VERDICT', 'VALID'), ('OPEN_CONDITIONS', '; '.join('%s: %s' % kv for kv in sorted(open_conditions(M2BL).items())) or 'none'))
    hj = dict((('RECORD', 'EXPORT_P2_14_JOINT_v1'),) + common + (('CLASSES', 'D3 D4 D4M'), ('WX_D3', '3'), ('WX_D4', '2'), ('WX_D4M', '2'),
                                                              ('J_UNIFORMITY', JUJ + MSFX), ('VACUUM_CORRECTION', 'S3_LEMMA_E' + MSFX),
                                                              ('CENTRING', 'DOUBLE_TRICK_MEAN_BALLS' + MSFX),
                                                              ('E2_GLEVELS', ' '.join('N%d_%s %s %s' % (N, c, E2_GLEV[(N, c)][0], E2_GLEV[(N, c)][1])
                                                                                      for N in (4, 3) for c in ('D3', 'D4', 'D4M'))),
                                                              ('E2_SLEVELS', ' '.join('N%d_%s %s %s' % (N, c, E2_SLEV[(N, c)][0], E2_SLEV[(N, c)][1])
                                                                                      for N in (4, 3) for c in ('D3', 'D4', 'D4M'))),
                                                              ('E2_CONSTANTS', 'LEMMA_E_PRIME (Lemma G cut): Phi_eps, S = sqrt(Phi_eps Phi_eps,theta,b), A_theta = theta (1 - eps) A, eps 1/4, theta 0.7; Lemma T-prime with the S7 G_00 record; rho_phi by Lemma R'),
                                                              ('NORMX_BOUND', 'MIN_OPERATOR_BOX_PLUS_SCHUR_TAIL_HS_INV' + MSFX),
                                                              ('NORMX_FORM', 'LEMMA_S_PRIME: box by positivity (Kent 1977), J-uniform Schur tails; kappa M4'),
                                                              ('NORMX_LEVELS', ' '.join('N%d_%s %s %s' % (N, c, NORMX_LEVELS[(N, c)][0], NORMX_LEVELS[(N, c)][1])
                                                                                        for N in (4, 3) for c in ('D3', 'D4', 'D4M'))),
                                                              ('KAPPA_SOURCE', 'KAPPA_MAX: k1_hi^3/((1 - eps_r) lambda_h(300)), lambda_h by the matrix-tree theorem (eps_r of M2B_KV_v1 at J = 300)'),
                                                              ('COV_SOURCE', 'ROUTE_MAX' + MSFX),
                                                              ('FLOAT_IN', FIN_JT), ('NORMX_HS_RECORD', '%s:%s' % (os.path.basename(HS_RECORD[0]), PINS[HS_RECORD[0]])), ('NORMX_HS_USED', ' '.join('N%d_%s %d' % (N, c, hs_used.get((N, c), 0)) for N in (4, 3) for c in ('D3', 'D4', 'D4M'))), ('ROUTE_ADMISSIBLE', 'SINGLE:D3,D4,D4M DOUBLE:D4,D4M CS:D3'), ('RHO_SOURCE', 'LEMMA_R_LEMMA_T_PRIME_S7_G00'), ('CE_SOURCE', 'DOUBLE_TRICK'),
                                                              ('FIELDS', JT_FIELDS)) + tuple(audit))
    hj['EXPORT_STATUS'] = STJ if MODE == 'cert' else 'MOCK'   # v1_35 (7)
    sj = cert_stage(EXP_JT, 'EXPORT_P2_14_JOINT_v1', hj, rows_jt, READERS) if MODE == 'cert' else kv_write(EXP_JT, 'EXPORT_P2_14_JOINT_v1', hj, rows_jt)
    rows_tp = []
    for N in (4, 3):
        X = T.get(N)   # v1_27 (1): the mock-input J = 300 row, now the reference only; the rows take the port values below
        vals = None if X is None else (dec_lo(X['At']), dec_hi(X['Vt']), dec_hi(X['Ot']), dec_hi(X['Pt2'].upper().sqrt()), dec_lo(X['Xta']), dec_lo(X['Xtb']),
                dec_lo(X['Aa']), dec_hi(X['dtx']), dec_hi(X['Q']), dec_hi(X['tz']))
        for idx, jlo, jhi in P[N]:
            rows_tp.append(('N%d_P%s' % (N, idx), ' '.join((jlo, jhi) + tp_vals(TP[(N, idx)]) + (dec_lo(CE_T[(N, idx)][0]), dec_hi(CE_T[(N, idx)][1])))))   # v1_24 (1)
    out('C-T-POS: At_lo, Aa_lo and Xta_lo > 0 exactly on every t row as printed (the consumer\'s SIGN test) -> %s' % gate(
        fails, 'C-T-POS', flag(lambda: check_pos(rows_tp, TP_FIELDS, ('At_lo', 'Aa_lo', 'Xta_lo'), 'C-T-POS'))))
    plant(nofire, 'PLANT-T-POS', only('C-T-POS', lambda: check_pos([zero_field(rows_tp[0], TP_FIELDS, 'Aa_lo')], TP_FIELDS, ('At_lo', 'Aa_lo', 'Xta_lo'), 'C-T-POS')))
    M4SRC = {'S9_RITZ_PIECES': RITZ_STATUS, 'NA_LEMMA_B': 'CERTIFIED', 'EPS_M2B': 'CERTIFIED', 'LAW_A_T_A_AM': 'CERTIFIED', 'R_E1_R_E3': 'CERTIFIED', 'TAU_R': 'CERTIFIED', 'TZ_P2_3': SETAC_STATUS}   # v1_35 (2): tz by the odd Ritz route on Set C   # (5) the t path M4 inputs and their status (item (v))
    JUT = t_uniformity(M4SRC)
    out('C-JUNIF: J_UNIF_PP is the string pinned with pk07 (%d chars, sha256 %s...); the joint and means exports carry it, the t export carries %s while its M4 inputs are %s (each with MSFX in a MOCK export) -> %s' % (
        len(J_UNIF_PP), J_UNIF_PP_SHA16, 'J_UNIF_PP' if JUT == J_UNIF_PP else 'the ASSUMED string', ', '.join('%s %s' % kv for kv in sorted(M4SRC.items())), gate(
            fails, 'C-JUNIF', len(J_UNIF_PP) == J_UNIF_PP_LEN and hashlib.sha256(J_UNIF_PP.encode()).hexdigest()[:16] == J_UNIF_PP_SHA16 and check_t_uniformity(JUT, M4SRC) is True)))
    plant(nofire, 'PLANT-JUNIF-T', lambda: check_t_uniformity(J_UNIF_PP, dict(M4SRC, TZ_P2_3='MOCK')))   # v1_35 (2): one input not certified, in either mode   # (5)
    STT, NMT, JUT2 = status_junif(dict(FINM, kt_p2_assembly=OWN_FLOAT_TP), open_conditions(M2BL), M4SRC)   # v1_35 (7): the t export
    ht = dict((('RECORD', 'EXPORT_P2_T_v1'),) + common + (('J_UNIFORMITY', JUT2 + MSFX),
                                                           ('VT_FORM', 'GRAM_PLUS_Q4'), ('PT_FORM', 'JOINT_GRAM'), ('XTB_SOURCE', 'FLIP_OF_XTA'), ('GBAD_SOURCE', 'LEMMA_G: tau~0(Lam) kappa (kappa + u) sqrt(Phi_eps), eps 1/4; Lemma T-prime with the S7 G_00 record'),
                                                           ('RITZ_SOURCE', RITZ_SRC), ('NA_SOURCE', NA_SRC), ('EPS_SOURCE', EPS_SRC), ('FLOAT_IN', FIN_TP),
                                                           ('CE_SOURCE', 'DOUBLE_TRICK: c_t by the double eigen trick per piece in the norm form (gg, s-part, G_00 lambda~_0^2), one ball for every class' + MSFX), ('FIELDS', TP_FIELDS),
                                                           ('N4_PIECES', '904'), ('N3_PIECES', '904')))
    ht['EXPORT_STATUS'] = STT if MODE == 'cert' else 'MOCK'   # v1_35 (7)
    st = cert_stage(EXP_TP, 'EXPORT_P2_T_v1', ht, rows_tp, READERS) if MODE == 'cert' else kv_write(EXP_TP, 'EXPORT_P2_T_v1', ht, rows_tp)
    hm = dict((('RECORD', 'EXPORT_P2_14_MEANS_v1'),) + common + (('CLASSES', 'D3 D4 D4M'),
                                                               ('MEAN_SOURCE', 'DOUBLE_TRICK: c_t by the double eigen trick (w = 2) and c_b = Tb/(G_00 lambda~_0) (w = 1, S7 A,0), each with its gg part and s-part (ADD1 sect. 2); c_bb = c_t'),
                                                               ('CE_EDGE', 't, the top-row horizontal edge: c_t = E xi_t'),
                                                               ('CF_EDGE', 'D3: bb, the bottom-row horizontal edge (c_bb = c_t by the flip); D4 and D4M: b, the vertical edge'),
                                                               ('COV_SOURCE', 'ROUTE_MAX_LO_ROUTE_MIN_HI: Cov_inf_lo as in the joint export (max over the admissible routes of E11_lo - c_e,hi c_f,hi); Cov_inf_hi = min over the same routes of E11_hi - c_e,lo c_f,lo' + MSFX),   # v1_37 (6)
                                                               ('COV_CENTRING', COV_CENTRING + MSFX),   # v1_37 (6): pk11 for R6.5
                                                               ('J_UNIFORMITY', JUJ + MSFX),
                                                               ('FLOAT_IN', FIN_JT),
                                                               ('FIELDS', MN_FIELDS)) +
              tuple(('N%d_%s_PIECES' % (N, c), '904') for N in (4, 3) for c in ('D3', 'D4', 'D4M')))
    hm['EXPORT_STATUS'] = STJ if MODE == 'cert' else 'MOCK'   # v1_35 (7)
    sm = cert_stage(EXP_MN, 'EXPORT_P2_14_MEANS_v1', hm, rows_mn, READERS) if MODE == 'cert' else kv_write(EXP_MN, 'EXPORT_P2_14_MEANS_v1', hm, rows_mn)   # v1_22
    if MODE == 'cert': sj, st, sm = cert_commit([sj, st, sm])   # v1_37 (1), the choice (a): all three staged and checked before the first rename
    rbk = all(flag(lambda p=p, r=r, h=h, w=w: readback_lines(lines_of(p), r, h, w)) for p, r, h, w in (
        (EXP_JT, 'EXPORT_P2_14_JOINT_v1', hj, rows_jt), (EXP_TP, 'EXPORT_P2_T_v1', ht, rows_tp), (EXP_MN, 'EXPORT_P2_14_MEANS_v1', hm, rows_mn)))
    out('C-READBACK: each written export reads back key for key and string for string (header, rows, END) -> %s' % gate(fails, 'C-READBACK', rbk))
    JW = dict((r, kv_parse(lines_of(p))[0]) for r, p in (('EXPORT_P2_14_JOINT_v1', EXP_JT), ('EXPORT_P2_T_v1', EXP_TP), ('EXPORT_P2_14_MEANS_v1', EXP_MN)))   # v1_36 (2)
    jsok = all(flag(lambda d=d: check_status_junif(d.get('EXPORT_STATUS'), d.get('FLOAT_IN'), d.get('J_UNIFORMITY'))) for d in JW.values()) and \
        flag(lambda: check_status_junif(STJ, NMJ, JUJ)) and flag(lambda: check_status_junif(STT, NMT, JUT2))
    out('C-JUNIF-STATUS: the per-piece J_UNIFORMITY only beside EXPORT_STATUS CERTIFIED and FLOAT_IN none, in the three exports as written (EXPORT_STATUS %s, %s, %s) and in status_junif\'s triples (joint and means %s with %s, t %s with %s) -> %s' % (
        JW['EXPORT_P2_14_JOINT_v1'].get('EXPORT_STATUS'), JW['EXPORT_P2_T_v1'].get('EXPORT_STATUS'), JW['EXPORT_P2_14_MEANS_v1'].get('EXPORT_STATUS'),
        STJ, 'J_UNIF_PP' if JUJ == J_UNIF_PP else 'the ASSUMED string', STT, 'J_UNIF_PP' if JUT2 == J_UNIF_PP else 'the ASSUMED string', gate(fails, 'C-JUNIF-STATUS', jsok)))
    plant(nofire, 'PLANT-JUNIF-MOCKPAIR', only('C-JUNIF-STATUS', lambda: check_status_junif('MOCK', 'none', J_UNIF_PP)))   # v1_36 (2): the pair v1_35 wrote
    try:   # v1_37 (6): C-COV-SAME on the written exports
        why, ok = '%d rows' % check_cov_same(lines_of(EXP_MN), lines_of(EXP_JT)), True
    except Refused as e:
        why, ok = 'refused: %s' % e, False
    out('C-COV-SAME: the means export Cov_inf_lo equals the joint export Cov_inf_lo string for string on every row (%s) -> %s' % (why, gate(fails, 'C-COV-SAME', ok)))
    plant(nofire, 'PLANT-COV-SAME', only('C-COV-SAME', lambda: check_cov_same(cov_lo_bump(lines_of(EXP_MN)), lines_of(EXP_JT))))   # v1_37 (6): one Cov_inf_lo moved in its last digit
    LJ0 = lines_of(EXP_JT)
    plant(nofire, 'PLANT-CERT-REWRITE', only('C-READBACK', lambda: readback_lines([x.replace('= 300.0 300.75', '= 300.0 300.76') if x.startswith('N4_D3_P0000 = ') else x
                                                                                    for x in LJ0], 'EXPORT_P2_14_JOINT_v1', hj, rows_jt)))
    hcert = {'RECORD': 'EXPORT_P2_14_JOINT_v1', 'FORMAT': 'S4U_KV_v1', 'TAG': 'CERTIFIED plant', 'EXPORT_STATUS': 'CERTIFIED', 'FLOAT_IN': 'none', 'OPEN_CONDITIONS': 'none', 'J_UNIFORMITY': J_UNIF_PP}   # v1_36 (1): passes C-CERT-HEADER
    RACC = {'EXPORT_P2_14_JOINT_v1': lambda L, c: True}   # v1_36 (1): an accepting reader for the plants; with NOWRITE as the store no plant can write
    plant(nofire, 'PLANT-CERT-PATH', only('C-CERT-PATH', lambda: kv_write_cert(os.path.join(MOUT, 'plant_cert_path_%s.kv' % LABEL), 'EXPORT_P2_14_JOINT_v1', hcert, [], RACC, NOWRITE)))
    plant(nofire, 'PLANT-CERT-MOCKTOKEN', only('C-CERT-MOCKTOKEN', lambda: kv_write_cert(os.path.join(COUT, 'plant_cert_mock_%s.kv' % LABEL), 'EXPORT_P2_14_JOINT_v1', dict(hcert, CLAIM='MOCK'), [], RACC, NOWRITE)))
    plant(nofire, 'PLANT-CERT-READER', only('C-CERT-READER', lambda: kv_write_cert(os.path.join(COUT, 'plant_cert_reader_%s.kv' % LABEL), 'EXPORT_P2_14_JOINT_v1', hcert, [], None, NOWRITE)))
    plant(nofire, 'PLANT-CERT-EXISTS', only('C-CERT-EXISTS', lambda: kv_write_cert(JOINTF, 'EXPORT_P2_14_JOINT_v1', hcert, [], RACC, NOWRITE)))
    plant(nofire, 'PLANT-CERT-HEADER', only('not a certified header', lambda: kv_write_cert(os.path.join(COUT, 'plant_cert_header_%s.kv' % LABEL), 'EXPORT_P2_14_JOINT_v1', dict(hcert, EXPORT_STATUS='CERTIFIED_GIVEN_FLOAT_IN'), [], RACC, NOWRITE)))   # v1_36 (1)
    plant(nofire, 'PLANT-CERT-JUNIF', only('not the certified value', lambda: kv_write_cert(os.path.join(COUT, 'plant_cert_junif_%s.kv' % LABEL), 'EXPORT_P2_14_JOINT_v1', dict(hcert, J_UNIFORMITY=J_UNIF_T_ASSUMED), [], RACC, NOWRITE)))   # v1_36 (1)
    plant(nofire, 'PLANT-CERT-RECORD', only('C-CERT-READER', lambda: kv_write_cert(os.path.join(COUT, 'plant_cert_record_%s.kv' % LABEL), 'EXPORT_P2_T_v1', dict(hcert, RECORD='EXPORT_P2_T_v1'), [], RACC, NOWRITE)))   # v1_36 (1): no reader for the record
    plant(nofire, 'PLANT-CERT-PART', only('temporary file', lambda: kv_write_cert(os.path.join(COUT, 'plant_cert_part_%s.kv' % LABEL), 'EXPORT_P2_14_JOINT_v1', hcert, [], RACC, MemFS([cert_tmp(os.path.join(COUT, 'plant_cert_part_%s.kv' % LABEL))]))))   # v1_37 (1): this run's temporary name taken
    PFS = [os.path.join(COUT, 'plant_cert_%s_%s.kv' % (x, LABEL)) for x in ('mock', 'reader', 'header', 'junif', 'record', 'part')] + [os.path.join(MOUT, 'plant_cert_path_%s.kv' % LABEL)]
    out('C-CERT-NOFILE: no cert plant left a file or a temporary file (%d names checked) -> %s' % (len(PFS), gate(fails, 'C-CERT-NOFILE', not any(os.path.exists(q) or os.path.exists(q + '.part') or os.path.exists(cert_tmp(q)) for q in PFS))))
    for path, rec, sh, nrow in ((EXP_JT, 'EXPORT_P2_14_JOINT_v1', sj, len(rows_jt)), (EXP_TP, 'EXPORT_P2_T_v1', st, len(rows_tp)), (EXP_MN, 'EXPORT_P2_14_MEANS_v1', sm, len(rows_mn))):
        out(EXPORT_FMT % (os.path.basename(path), sh))   # v1_36 (4): rule V2's form; rows, format and status on the INFO line
        Lx = lines_of(path)
        dx = kv_parse(Lx)[0]
        out('INFO EXPORT %s: %d rows, FORMAT %s, EXPORT_STATUS %s, J_UNIFORMITY %s' % (os.path.basename(path), nrow, dx.get('FORMAT'), dx.get('EXPORT_STATUS'), {
            J_UNIF_PP: 'J_UNIF_PP', J_UNIF_PP + ' (MOCK)': 'J_UNIF_PP (MOCK)', J_UNIF_T_ASSUMED: 'ASSUMED', J_UNIF_T_ASSUMED + ' (MOCK)': 'ASSUMED (MOCK)'}.get(dx.get('J_UNIFORMITY'), repr(dx.get('J_UNIFORMITY')))))
        ok, why = flag_why(lambda: READERS[rec](Lx, MODE == 'cert'))   # v1_36 (1): the record's own reader (test 1: the MOCK exports in the MOCK items)
        out('C-S9H-READ %s: after C-READBACK, %s reads it as %s and s9h_ident compares FORMAT, RECORD, END, EXPORT_STATUS, TAG and RUN_VERDICT (%s) -> %s' % (os.path.basename(path), S9H_RDNAME[rec], 'CERTIFIED' if MODE == 'cert' else 'MOCK', why or 'no problems', gate(fails, 'C-S9H-READ %s' % rec, ok)))
        ok = True
        try:
            None if MODE == 'cert' else read_kv(Lx, 'MOCK', rec)   # v1_36 (4): C-SELF, PLANT-MOCK-D and C-NOCERT are the MOCK items' tests
        except Refused as e:
            ok = False
            out('C-SELF %s: MOCK reader refused (%s)' % (os.path.basename(path), e))
        if MODE != 'cert': out('C-SELF %s: the MOCK reader accepts it -> %s' % (os.path.basename(path), gate(fails, 'C-SELF %s' % rec, ok)))
        if MODE != 'cert': plant(nofire, 'PLANT-MOCK-D %s' % os.path.basename(path), lambda Lx=Lx, rec=rec: read_kv(Lx, 'CERTIFIED', rec))
        bad = [] if MODE == 'cert' else [x for x in Lx if not x.startswith('#') and (('CERTIFIED' in x.upper() and re.match(r'^(FORMAT|TAG|EXPORT_STATUS) = ', x))
                                                          or (x.startswith('FORMAT') and x != 'FORMAT = S4U_KV_v1 MOCK')
                                                          or (x.startswith('TAG = ') and not x.startswith('TAG = MOCK'))
                                                          or (x.startswith('EXPORT_STATUS = ') and x != 'EXPORT_STATUS = MOCK'))]
        if MODE != 'cert': out('C-NOCERT %s: %d offending lines -> %s' % (os.path.basename(path), len(bad), gate(fails, 'C-NOCERT %s' % rec, not bad)))
    CC = dict((r, certify_header(h, SELF)) for r, h in (('EXPORT_P2_14_JOINT_v1', hj), ('EXPORT_P2_T_v1', ht), ('EXPORT_P2_14_MEANS_v1', hm)))   # v1_36 (1), test 2
    RW = {'EXPORT_P2_14_JOINT_v1': rows_jt, 'EXPORT_P2_T_v1': rows_tp, 'EXPORT_P2_14_MEANS_v1': rows_mn}
    for r in ('EXPORT_P2_14_JOINT_v1', 'EXPORT_P2_T_v1', 'EXPORT_P2_14_MEANS_v1'):
        ok, why = flag_why(lambda r=r: cert_copy_check(r, CC[r], RW[r], READERS))
        out('C-S9H-CERTCOPY %s: in memory, with the certified header (certify_header), it passes the cert writer\'s refusals before any file operation, C-READBACK, then %s as CERTIFIED with s9h_ident (%s) -> %s' % (
            r, S9H_RDNAME[r], why or 'no problems', gate(fails, 'C-S9H-CERTCOPY %s' % r, ok)))
    plant(nofire, 'PLANT-S9H-CENTRING', only('CENTRING', lambda: cert_copy_check('EXPORT_P2_14_JOINT_v1', dict(CC['EXPORT_P2_14_JOINT_v1'], CENTRING='SINGLE_TRICK_MEAN_BALLS'), rows_jt, READERS)))
    plant(nofire, 'PLANT-S9H-JOINT-T', only('joint_read finds', lambda: READERS['EXPORT_P2_14_JOINT_v1'](lines_of(EXP_TP), MODE == 'cert')))   # the joint reader refuses the t export
    NMJ_ = os.path.basename(EXP_JT)
    SYN = EXPORT_FMT % (NMJ_, sj) + '\nVERDICT VALID\n'   # v1_36 (1), test 3: a run output in this run's EXPORT line form with the final VERDICT
    ok, why = flag_why(lambda: bind_check(RD, NMJ_, sj, SYN))
    out('C-S9H-BIND (a test): rule V2\'s bound_ok accepts a synthetic run output in this run\'s EXPORT line form with VERDICT VALID for %s (%s); the binding to this run\'s own VERDICT is the consumer\'s -> %s' % (
        NMJ_, why or 'accepted', gate(fails, 'C-S9H-BIND', ok)))
    plant(nofire, 'PLANT-S9H-BIND-SHA', only('C-S9H-BIND', lambda: bind_check(RD, NMJ_, sj[:-1] + ('1' if sj[-1] == '0' else '0'), SYN)))
    PD = dict((r, os.path.join(COUT, 'export_drycert_%s_%s.kv' % (r, LABEL))) for r in RW)   # v1_37 (1): final names for the memory stores only
    MF2 = MemFS()
    plant(nofire, 'PLANT-CERT-STAGE2', only('C-S9H-T', lambda: cert_write_all([(PD['EXPORT_P2_14_JOINT_v1'], 'EXPORT_P2_14_JOINT_v1', CC['EXPORT_P2_14_JOINT_v1'], rows_jt),
                                                                              (PD['EXPORT_P2_T_v1'], 'EXPORT_P2_T_v1', dict(CC['EXPORT_P2_T_v1'], XTB_SOURCE='COMPUTED'), rows_tp)], READERS, MF2)))   # v1_37 (1), main (a): the second export refused after the first passed
    out('C-CERT-ALLORNONE: after PLANT-CERT-STAGE2 the store holds no final name, only the two staged temporary files, and nothing of it is on disk -> %s' % gate(
        fails, 'C-CERT-ALLORNONE', not any(MF2.exists(p) for p in PD.values()) and sorted(MF2.files) == sorted(cert_tmp(PD[r]) for r in ('EXPORT_P2_14_JOINT_v1', 'EXPORT_P2_T_v1'))
        and not any(os.path.exists(p) or os.path.exists(cert_tmp(p)) for p in PD.values())))
    ok, why = flag_why(lambda: dry_commit([(PD[r], r, CC[r], RW[r]) for r in ('EXPORT_P2_14_JOINT_v1', 'EXPORT_P2_T_v1', 'EXPORT_P2_14_MEANS_v1')], READERS))
    out('C-CERT-DRY (control): in a memory store the three exports with their certified headers are staged, checked and renamed, and the store then holds exactly the three final names with their bytes (%s) -> %s' % (
        why or 'as expected', gate(fails, 'C-CERT-DRY', ok)))
    Lj = lines_of(EXP_JT)
    try:
        why, ok = '%d rows' % check_srcj(Lj), True
    except Refused as e:
        why, ok = 'refused: %s' % e, False
    out('C-SRCJ %s: pk07\'s C-SRC-J, pX_hi^2 >= E2_hi - Cov_inf_lo^2 exactly on the printed decimals (%s) -> %s' % (
        os.path.basename(EXP_JT), why, gate(fails, 'C-SRCJ', ok)))
    plant(nofire, 'PLANT-SRCJ', lambda: check_srcj(srcj_down(Lj)))
    Lt = lines_of(EXP_TP)
    try:
        why, ok = '%d rows' % check_flip(Lt), True
    except Refused as e:
        why, ok = 'refused: %s' % e, False
    out('C-FLIP %s: XTB_SOURCE = FLIP_OF_XTA and Xtb_lo equal to Xta_lo string for string (%s) -> %s' % (
        os.path.basename(EXP_TP), why, gate(fails, 'C-FLIP', ok)))
    plant(nofire, 'PLANT-FLIP-ROW', lambda: check_flip(flip_row_plant(Lt)))
    plant(nofire, 'PLANT-FLIP-DECL', lambda: check_flip([x for x in Lt if not x.startswith('XTB_SOURCE = ')]))
    plant(nofire, 'PLANT-FLIP-SRC', lambda: check_flip([('XTB_SOURCE = COMPUTED' if x.startswith('XTB_SOURCE = ') else x) for x in Lt]))
    pc = os.path.join(MOUT, 'plant_certout_%s.kv' % LABEL)
    try:
        kv_write(pc, 'EXPORT_P2_14_JOINT_v1', {'FORMAT': 'S4U_KV_v1', 'RECORD': 'EXPORT_P2_14_JOINT_v1', 'TAG': 'CERTIFIED %s' % LABEL,
                                                'EXPORT_STATUS': 'CERTIFIED', 'CLAIM': 'certified'}, [])
        fired = False
    except ValueError:
        fired = True
    fired = fired and not os.path.exists(pc)
    out('PLANT-CERTOUT: the writer with a certified FORMAT %s -> %s' % ('raised before opening a file' if fired else 'wrote or did not raise',
                                                                         'FIRES' if fired else 'DOES NOT FIRE'))
    if not fired:
        nofire.append('PLANT-CERTOUT')


def main():
    fails, nofire = [], []
    complete = False
    try:
        run(fails, nofire)
        complete = True
    except CapStop as e:
        out('CAP-STOP before %s at cpu %.1f s (LIM %d)' % (e, cpu(), LIM))
    except Exception as e:
        out(traceback.format_exc().rstrip())
        out('ERROR in stage %s at cpu %.1f s: %r' % (STAGE[0], cpu(), e))
        out('VERDICT INVALID (ERROR)')
        return 1
    why = fails + ['%s did not fire' % x for x in nofire] + ([] if complete else ['INCOMPLETE'])
    out('ITEM %s cpu %.1f s, peak resident memory %d MiB' % (MODE, cpu(), resource.getrusage(resource.RUSAGE_SELF).ru_maxrss // 1024))
    out('VERDICT %s%s' % ('VALID' if not why else 'INVALID', '' if not why else ' (%s)' % ', '.join(why)))
    return 0


if __name__ == '__main__':
    sys.exit(main())
