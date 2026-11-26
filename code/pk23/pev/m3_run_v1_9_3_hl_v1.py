#!/usr/bin/env python3
"""m3_run_v1_9_3_hl_v1.py -- pk23 (code/pk23/pev/): a COPY of pk22's m3_run_v1_9_3_px22_c3k_1.py (sha256 8876ba2883a37f2946ea9d40a2afda6c6ee4d1738f3c332303da69e0194d2c46)
by pk23's make_run_hl_v1.py for the option B Pev entries on S8's L graph (the P0_LOG rows 4409, 4422, 4435): the list
HL_ENTRY_LIST_v1.json (families L: TT,0,0; LH: TTh,0,0, Mh,0,0, Mhh,0,0; LT: Mt,0,0, Mtt,0,0); one prep family L (items Lp1..) read by
LH and LT (PREPOF, C-PREP-SHARE against S8_ENTRY_LIST_v2's L); the trial set z9sym (pk25's mr/v3 TRIAL_SET); references pk23's
rtwin_hl_v1 (restored prep) and twin m3ref_hl_v1 (P16L); smoke items La, LHa, LTa; RESUME_FAMS LH on Mh,0,0; PLANT-ODD on L; records
m3_hl_<G>_N<N>_J300_hl.json; PLANT-SCOPE and the reader plants on LH's record; written paths in pk23/pev/out and pk23/pev/hand.
m3_run_v1_9_3_px22_c3k_1.py -- pk22 (code/pk22/m3/). REVISION of m3_run_v1_9_3_px22_c3k.py (sha256 8ea4f3a245a672b5d8713886ca082eb0a7e1632747f69a811e8167e474db06cc) for runner
c3k_1: the list C3K_ENTRY_LIST_v1_1.json (sha256 060263495bf3fa3a3f06f3b697c67d04f3b1050d27cd9699fe6fb84381f808cd: v1 without psi_xy's plain rows G10,b and T10,b, which E1 and E2 take from S8's
items), and E4N's smoke in four parts E4Na1..E4Na4 on the entry slices [0, 2), [2, 4), [4, 5), [5, 7) (SMOKE_PARTS; C-SMOKE-PARTS):
c3k's whole E4N smoke passed the 540 s limit. Made by pk22/m3/make_c3k_1_v1.py. c3k's docstring follows.
m3_run_v1_9_3_px22_c3k.py -- pk22 (code/pk22/m3/). REVISION of m3_run_v1_9_3_px22_c3j.py (sha256 b52c454c069c24b5b50c053b94177bd29e501b2507f9b08f9b4d0572b2c6acfb) for runner c3k
(H-CONN entry E4, the P0_LOG row 4154): the families E4D and E4N of pk22's C3K_ENTRY_LIST_v1.json (sha256 73d132270f4d07da13e3d16aa50673acd21bc9753ce524f2ae80717e1f7b61de), on the
z9symxy trial set (pk22/midrow/psixy/ts_*_z9symxy_v1.json: states 0..9 z9sym's, state 10 psi_xy = e1 x e3), in split grouping:
- E4D [vac|vac] (pairs (0,1), (0,2), (1,2), (3,4), (3,5), (4,5), (1,4)): Gxh,10,b = <phi_10, K o xi_h phi_b> (b = 0, 1, 3), the control
  Gxhr,1,10 and psi_xy's Gram row G10,b (b = 0, 1, 3, 10); its own prep pieces E4Dp1..; radii from the twin piece P16E4D.<N>.p1;
- E4N [vac|int|vac] (pairs (0,1), (0,2), (1,2), (6,7), (6,8), (7,8), (1,4), (4,7)): IhL,10,b (h on (1,4) next to phi_10) and IhR,10,b
  (h on (4,7) next to phi_b), the control IhLr,1,10 and psi_xy's T row T10,b; its own prep pieces E4Np1..; radii from P16E4N.<N>.p2.
What changes against c3j: the list, FAMS and the trial set (TSF from pk22/midrow/psixy, pinned under PSX; TRIAL names it);
PREPOF (each family its own prep); FAMREF, KEYFAM, KEYREF: rtwin_c3k_v1_1's references (restored prep, split-grouping bars, TRIAL
z9symxy, which C-HASH-REF requires); PREPREF: m3ref_px22_v1_7's pieces; PLANT-ODD on E4D; RESUME_FAMS (E4N,) on IhR,10,1; records
m3_c3k_<G>_N<N>_J300_c3k.json; PLANT-SCOPE and the reader plants on E4N's record. Made by pk22/m3/make_c3k_v1.py. c3j's docstring
follows.
m3_run_v1_9_3_px22_c3j.py -- pk22 (code/pk22/m3/). REVISION of m3_run_v1_9_3_px22_c3h_1.py (sha256 3aba49d8601e747b8d54d95db24a30042d864393a6a2afe1eadd3f1aafd8f660) for runner c3j
(G7 and G4, the P0_LOG rows 4089, 4091): the families DJ and CS4TB of pk22's C3J_ENTRY_LIST_v1.json (sha256 3cc83e2a2b55ea8c000328ad9c1b83ba3941780403dd5d98d5f83b0a319dcd75):
- DJ [vac|vac] (pairs (0,1), (0,2), (1,2), (3,4), (3,5), (4,5), (0,3), (1,4), (2,5)), in split grouping: G7's rows JTH,a,b = <psi_a, M_t M_h
  psi_b> (t on (0,3), h on (1,4), the same bond) with the control JTHr,1,0, and t's trial entries for G6: DHT (M_t), DT2 (M_t^2), DTB
  (M_t M_bb, bb on (2,5)); DJ runs its own prep pieces DJp1.. (6 vertices); its radii come from the twin piece P16BD2T's PREPJSON;
- CS4TB [free|int|int|free] (pairs (0,3), (8,11)), standard grouping, sharing c1's S4 prep: xTB = <Lambda_t, Lambda_bb> (the even
  residual of t at d' = -1; the row 4089) and the controls xT (c3_1's x) and Z.
What changes against c3h_1: the list and FAMS; V3 takes each entry's grouping from the list (split or std; m3_bar_v11.split_groups for
split); PREPOF (DJ: its own prep; CS4TB: S4); KEYREF and KEYFAM: rtwin_c3j_v1's references (restored prep, with the split-grouping
bars); PREPREF: P16BD2T (DJ), m3ref_v1_14 P16S4 (CS4TB); PLANT-ODD on DJ; RESUME_FAMS (CS4TB,) on xTB; records m3_c3j_<G>_N<N>_J300_c3j.json;
PLANT-SCOPE and the reader plants on CS4TB's record. Made by pk22/m3/make_c3j_v1.py. c3h_1's docstring follows.
m3_run_v1_9_3_px22_c3h_1.py -- pk22 (code/pk22/m3/). REVISION of m3_run_v1_9_3_px22_c3h.py (sha256 4947faeef9d1758bbe338e98241dc2b15723af4d4f013ba5c8e1688c665226b7) by make_c3h_1_v1.py:
C-PREP-SHARE's line and prep_share's docstring name the list of the shared prep family's graph (C3_ENTRY_LIST_v2 for CE3, S8_ENTRY_LIST_v2
for S4 and H); text only, everything else is c3h's. c3h's docstring follows.
m3_run_v1_9_3_px22_c3h.py -- pk22 (code/pk22/m3/). REVISION of m3_run_v1_9_3_px22_c3_1.py (sha256 bbecee470d6b2a9927b4d8e51e0a1b6dc1da9a441201739b637ab1fc84b466ce) for runner c3h
(G4 certified, the P0_LOG row 4013): C3-h's exact ends, the families CE3H, CS4H and H4TH of pk22's C3H_ENTRY_LIST_v1.json
(sha256 4f56853ab2390a8e29b384921315ed9e4501a5bf97f66c82986e2283ecfb21f3), on c3_1's vertex graphs with the middle-row h insertion: CE3H [vac|int|free] holds fH,a = <s_a, S M_h w-hat> (h on (4, 7),
d = -1; a = 0, 1, 3); CS4H [free|int|int|free] the d = -1 norms Z, xH, xHr (control), xxH (h on (1, 4) and (7, 10)); H4TH
[vac|int|int|free] hH,a (h on (4, 7), d = 0), the control hH1,a (h on (7, 10)) and the plain h0,a. The machinery, gates and plants are
c3_1's. What changes:
- the list: LIST is the C3-h list (pinned); FAMS = (CE3H, CS4H, H4TH); c3's list stays pinned as LISTC3 (CE3's graph);
- items: <X>a (smoke, one item each: SMOKE_PARTS is empty), <X>k1..<X>k9, CS4Hr1, CS4Hr2 (C-RESUME on xH), asm. No family runs a
  prep: CE3H reads the CE3 prep pieces that c3_1 ran (pinned with their hand-offs), CS4H the S4 prep pieces that c1 ran, H4TH the H
  prep pieces of pk03's runner (PREPOF; item_sha gives each its producer's sha256); C-PREP-SHARE as in c3, with CE3's graph
  from LISTC3;
- float references: rtwin_c3h_v1 (m3/rtwin_c3h_v1.py): the a_k and bar parts of every C3-h key by riglap5s.bound5s on a prep restored
  from the sibling twin piece's PREPJSON (P16CE3, P16CS4, P16CH4T of m3ref_px22_v1_5) with Ej, Gc and Gp recomputed on the C3-h graph
  (its gates: C-RESTORE, bit-exact on the siblings' chain keys; C-RULE; C-PAIRFREE; C-MIRROR). KEYREF names them (pinned): the
  KEYJSON of C-SMOKE-AK, C-REP-B and C-REP-AK, and the PREPJSON that C-PREP-SHARE compares with PREPREF (P16CE3, P16S4, P16H);
- parity: no parity zero (h is flip-even and the states are 0, 1, 3); PLANT-ODD runs on [cp, 2, 0] alone on CE3H;
- RESUME_FAMS (CS4H,) on CS4H's xH; records m3_c3h_<G>_N<N>_J300_c3h.json with entry_list C3H_ENTRY_LIST_v1; PLANT-SCOPE and the
  reader plants on CS4H's record.
Made by pk22/m3/make_c3h_v1.py. c3_1's docstring follows.
m3_run_v1_9_3_px22_c3_1.py -- pk22 (code/pk22/m3/). REVISION of m3_run_v1_9_3_px22_c3.py (sha256 6df29a35c401a9fdc14a47d56a29ff77e3ec133d40196da9307c2c0fc22d0507) by make_c3_1_v1.py:
CS4's smoke in four parts CS4a1..CS4a4 on fixed slices of its entries (SMOKE_PARTS; C-SMOKE-PARTS), since the whole smoke needs
about 1000 s of CPU and an item may use 540 s; everything else is c3's. c3's docstring follows.
m3_run_v1_9_3_px22_c3.py -- pk22 (code/pk22/m3/). REVISION of m3_run_v1_9_3_px22_c1.py (sha256 af6ce85c480f50a8da5b205bc87abf088fad1ef2019add3f54225001b37ad61e) for runner
c3: the families CS4, CE3, H4T and E2T of pk22's C3_ENTRY_LIST_v2.json (sha256 e877d12f0686ff959bc34f12651f62629f0e3f43acc76b2cc363ec2524eaf1c6), one family per
vertex graph: CS4 [free|int|int|free] holds T1MN's Z, x, xr, xx and W1a's joint Gram windows at pJ = 2 (orbit A: A.JJ, A.Jx, A.Jy,
A.Jl, A.xy, A.yy, A.yl, the control A.Jxr; orbit D likewise); CE3 [vac|int|free] holds E3T's fT,a and fT2,a and the joint windows'
trial components A.J,a, A.y,a, D.J,a, D.y,a; H4T [vac|int|int|free] holds NE's hT,a and hT1,a; E2T [vac|free] the controls eT,a. A
horizontal or vertical xi is m3_entries_v3's xia factor on the triple (u, v, v). The machinery, gates and plants are c1's
(pk03's m3_run_v1_9_3). What changes:
- the list: LIST is the c3 list (pinned); FAMS = (CS4, CE3, H4T, E2T); S8_ENTRY_LIST_v2 stays pinned as LISTS8 (the S4 and H graphs);
- items: <X>a (smoke), <Y>p1..<Y>p19 (Prep16 pieces of CE3 and E2T on their own vertex graphs), <X>k1..<X>k9 (entry pieces), CS4r1,
  CS4r2 (C-RESUME), asm. CS4 and H4T have no prep pieces: CS4 reads the S4 prep pieces that c1 ran, H4T the H prep pieces that
  pk03's m3_run_v1_9_3 ran (sha256 34abe3743035bd709e202eb4de2bdc752fef8a8abc6ebd5d0e4963050caa1dbb; outputs, hand-offs and memos copied into pk22 by manifest, the tables by
  copy_h_prep_v1.sh) (PREPOF; item_sha: their outputs and hand-offs carry their producer's sha256, pinned in INPUTS with the done
  pieces and their hand-offs); C-PREP-SHARE (with PLANT-PREP-SHARE): the family's prep graph equals LISTS8's graph of its prep
  family in V, N, S_gauge, edges with tags and pairs, and the float twins (the family's own m3ref_px22_v1_5 piece and pk03's
  P16S4 or P16H, the radii the shared prep took) agree: radii, rho'^2, theta0 exactly, prep scalars to 1e-12 relative;
- float references: pk22's m3ref_px22_v1_5 (families P16CS4, P16CE3, P16CH4T, P16CE2T): KEYREF (the piece with P16-DONE,
  pinned) gives the KEYJSON of C-SMOKE-AK, C-REP-B and C-REP-AK; PREPREF the PREPJSON of the prep radii and theta0 (C-RULE,
  C-PREP-REF): the family's own twin, and for CS4 and H4T pk03's P16S4 and P16H (as the shared preps took them);
- parity: the c3 list has no parity zero (PARITY_ZERO empty; C-PARITY-SET checks that no entry passes C-ODD); PLANT-ODD runs on the
  factor set [cp, 2, 0] alone on E2T (odd state 2 on a T <-> B symmetric graph, which passes C-ODD), with S[1][2] + 1e-12; the
  reader's PLANT-PARZERO marks a free item zero (its a_k are not zero, so the reader must refuse); PLANT-SCOPE and the reader plants
  on CS4's record;
- RESUME_FAMS (CS4,) on CS4's x; records m3_c3_<G>_N<N>_J300_c3.json with entry_list C3_ENTRY_LIST_v2 and the prep's family and
  script in prep16.
Made by pk22/m3/make_c3_v1.py. c1's docstring follows.
m3_run_v1_9_3_px22_c1.py -- pk22 (code/pk22/m3/): a COPY of pk03/m3_run_v1_9_3.py (sha256 34abe3743035bd709e202eb4de2bdc752fef8a8abc6ebd5d0e4963050caa1dbb) for W1a's S4
control items (the brief to pk22, 2026-11-17). Only the written paths move to pk22/m3/: OUTD (outputs, memos, records,
out/tab16c) and HANDD (hand-offs). The hand-off module is pk22's copy m3_handoff_v3_px22.py (sha256 92bdfee1da111163c1f32e5bdc8e62f2b59cf4e377be23235964d2ff86801d58, its HAND moved to
pk22/m3/hand), pinned in OWNMOD and loaded from pk22/m3/ through MODDIR (C-HASH, the loader, C-IMPORT and C-SERIES read
it there); one assert ties HO.HAND to HANDD. The pinned inputs and float twins that sit in pk03/out (INPUTS, REFOUT) are read
there through OUTD_IN; every other module, the kernel and the inputs are read where pk03 pins them. Nothing else changes.
Made by pk22/m3/make_copy_c1_v1.py. pk03's docstring follows.
m3_run_v1_9_3.py -- pk03 (code/pk03/). REVISION of m3_run_v1_9_2.py (a87f14ee) for one plant: its smoke Ha.4 (out 53bf92a3,
the approval 2026-11-08) passed C-PREP-GRAPH, PLANT-PREP-EDGE and PLANT-PREP-TAG and stopped in PLANT-PREP-GAUGE: with S_gauge [0], vertex
0 is the ground, its G_vv is exactly 0, and the plant graph's Pout divided by it (chi_tail_up: FloatingPointError). prep_view now forms
the C-4 values in a try and records 'not formed (<error>)' for a graph whose C-4 values are not finite; C-PREP-GRAPH requires both real
views' C-4 values formed. The script's own names move to m3_run_v1_9_3 (outputs and hand-offs m3_run_v1_9_3_<ITEM>, memos
m3_run_v1_9_3_memo_<X>_N<N>.jsonl, records m3_s8v2_<X>_N<N>_J300_v1_9_3.json), since m3_run_v1_9_2's sha256 is cited. Everything else
is m3_run_v1_9_2's.
m3_run_v1_9_2's docstring follows.
m3_run_v1_9_2.py -- pk03 (code/pk03/). REVISION of m3_run_v1_9_1.py (e64e5899) for the prep's graph (the approval 2026-11-08;
the prep graph rule): m3_run_v1_9_1's S4p1.4 (out 87ed24db) stopped at arbeng_ma_v1_4_1's own _code_guard: Prep16's
'ex' term builds h2^2 x h2 (degree 9) on the family graph, whose F is 19 for S4 (12 vertices and 7 pair forms), and the kernel's exponent
packing in base 10 would overflow int64 (10^19 >= 2^63). The prep reads only the vertex forms (the rule, sect. 1), so the prep pieces
now build Prep16 on prep_graph: GraphIV(V, E, [], N, S_gauge) with the family graph's V, N, edge list (tags, in order) and S_gauge, so
F = V = 12. C-PREP-GRAPH (the rule's C-1 and C-4): pairs [] and F = V; the inputs equal the family graph's; exactly (equal _mpi_
tuples) the vertex block of Gam, G_vv, log_tau, log_det_Lr, W_int's vertex columns and, at the prep's two rate vectors, tilted()'s vertex
Gam, G_vv and N; and Pout, Pout_p, tree(), farbase and alpha_lo on both graph objects. Its plants (C-2): an edge dropped
(PLANT-PREP-EDGE), a tag changed (PLANT-PREP-TAG), S_gauge [0] (PLANT-PREP-GAUGE), one ulp in a copied vertex block (PLANT-PREP-ULP).
A prep piece reads only this script's own state and memo, so no norm comes from m3_run_v1_9_1 (C-3); the tables in out/tab16c are
adopted by name as before. The smoke piece also runs C-PREP-GRAPH with its plants, and C-PACK-PLAN with PLANT-PACK-PLAN: every moment
table the bound of its family's entries asks the kernel for (built by no smoke) has its int64 code range (D + 1)^forms below 9.0e18, the
bound of the strictest table encoder (pk03's packing table for the approval). Smoke, entry and resume items keep the family graph with
its pairs. The script's own names move to m3_run_v1_9_2 (outputs and hand-offs m3_run_v1_9_2_<ITEM>, memos
m3_run_v1_9_2_memo_<X>_N<N>.jsonl, records m3_s8v2_<X>_N<N>_J300_v1_9_2.json), since m3_run_v1_9_1's sha256 is cited. Bar, reader and
kernel are unchanged, and so is everything else.
m3_run_v1_9_1's docstring follows.
m3_run_v1_9_1.py -- pk03 (code/pk03/). REVISION of m3_run_v1_9.py (5a19caa9) for one plant: its smoke Ha.4 (out 6bc2bc73,
the approval 2026-11-08) passed every gate and stopped at PLANT-SMOKE-PATH, which took h,2, the family's first entry with a xi factor
whose c0 is 0; h,2 is a parity zero, its a_k stay 0 when that factor's c9 is scaled, so the plant could not fire. PLANT-SMOKE-PATH
now takes the family's first FREE entry with such a factor (hX,0 for H, S4,x,0,TM for S4). The script's own names move to
m3_run_v1_9_1 (outputs and hand-offs m3_run_v1_9_1_<ITEM>, memos m3_run_v1_9_1_memo_<X>_N<N>.jsonl, records
m3_s8v2_<X>_N<N>_J300_v1_9_1.json), since m3_run_v1_9's sha256 is cited. Everything else is m3_run_v1_9's.
m3_run_v1_9's docstring follows.
m3_run_v1_9.py -- pk03 (code/pk03/). The CERTIFIED D16 H and S4 entries of route (b) (the approval 2026-11-08: bar v11 /
m3_run_v1_9): the H and S4 entries of pk11's S8_ENTRY_LIST_v2 (4565c6c7), at J_REF = 300, K = 3, qcap 6, with the prep at dmaxH 16,
on pk02's arbeng_ma_v1_4_1 (4126e83e).
REVISION of m3_run_v1_8_3.py (9660d018), whose machinery is kept as written: C-HASH, C-IMPORT, C-VALIDATED with DENY, C-SERIES,
C-PREC, C-CX, C-CX2, PLANT-GUARD, C-FALLBACK-PATH, verdict-bound hand-offs, resumable entries (the stop factor, capped pieces skipped),
the smoke piece, C-REP-B and C-REP-AK, the write after every gate and plant, RECORD lines, PLANT-NOWRITE, the bound reader and
C-PREC-END. What changes:
- The layer is arbeng_ma_v1_4_1, pinned by full sha256 with its validation records (VALREC: pk02's bundle manifest 368d6f1d, the
  run manifest of kt_ma_val_v1_6 6e951721, the delta validation output af1e3f66). C-VALREC-RUN re-hashes every file
  the run manifest lists and needs VERDICT lines exactly ['VERDICT VALID'] in each of its outputs. DENY gains arbeng_ma_v1_4.py (the
  unpinned predecessor) and pk03's mock tmp/r16/mock_arbeng_v1_4.py; PLANT-MOCK: the mock, offered under the kernel's name or
  its own, must be refused the certified tag. Prep, tables and entries all run on this one kernel (Prep16's tables read only its SPoly).
- C-CALLER (the caller rules): in m3_bar_v11's source every E2_combine call passes plan= and fallback=False, every
  load_view call an expected sha256 and every MomTableU call block=; PLANT-CALLER: the source with one plan= removed must fail the scan.
- The bar is m3_bar_v11: Prep16, the prep at dmaxH 16 of a 12-vertex graph in pieces (the D16 vertex tables through MomTableU with
  block 5000, read back from each table's hand-off; the big E2s in memoized blocks combined by E2_combine with their plan; a step that a
  capped piece finished on disk adopted after the kernel's own checks, a leftover file moved aside under a dated name, never deleted);
  bound is v10's. Every D16 E2 ball's relative radius is logged (E2-WIDTH) and the largest kept with its step.
- Families (the list's graphs, edges by m3_graph_v3.strip of the list's columns, pairs from the entries' factors; C-GRAPH-LIST):
  H  [vac|int|int|free], pairs (0,1), (1,2), (0,2), (3,4): h,a and hX,a for a = 0..3 (V 12, F 16);
  S4 [free|int|int|free], pairs (0,1), (3,4), (4,5), (6,7), (7,8), (9,10), (10,11): S4,Z, S4,x,c,B and S4,xy,c1,B1,c2,B2 (V 12, F 19).
- h,2 is a parity zero (pk11: state 2 alone, odd under T <-> B; the list leaves parity_zero null): PARITY_ZERO. C-PARITY-SET: the
  entries whose factors pass C-ODD on their own graph (c_odd16: m3_graph_v3.strip's couplings, as m3_entries_v3's c_odd reads only its
  own graph names) are exactly PARITY_ZERO, with PLANT-ODD. The record writes h,2 as an exact zero with parity 'zero' (as S8's).
- Items (N = 4 or 3; X = H or S4):
  Xa.N         the smoke piece: C-PARITY-SET with PLANT-ODD; the a_k of the family's entries without bars or prep scalars against the
               float twin (C-SMOKE-AK, PLANT-SMOKE-AK) and PLANT-SMOKE-PATH, the note 3 on m3_run_v1_8_3: one entry's xi factor
               with c9 times 1 + 1e-6 must move its a_k past the threshold; no hand-off, no record;
  Xp1..Xp19.N  the prep pieces: stage u, then stage c, of Prep16 with the context D16Ctx (the tables' state directories in out/tab16c/,
               the family's E2 memo, the piece budget: a step starts only if cpu + f x estimate <= LIM - 40, f = 1.25 x 2^(capped
               pieces since the last valid one)). C-CACHE-CHAIN with PLANT-CACHE: piece K reads the last valid prep piece before it
               (capped pieces skipped; none: an empty state); the memo's first lines must have the sha256 that piece recorded, and lines
               after them (from a capped piece) are each read back by ma_scalar_load and adopted. A refused step ends the piece with
               done false and the prep state; the piece that finishes stage c has done true and the scalars of both stages, and runs
               PLANT-MONO. PREP16-REP (INFO): every finished stage's scalars against the float twin's PREPJSON (upper end / float);
  Xk1..Xk9.N   resumable entry pieces on the scalars of the family's finished prep (C-PREP-CHAIN), v10's Prep without stages;
  Xr1.N, Xr2.N C-RESUME on RESUME_KEY after the entry pieces, against the entry as the record has it (the pieces' hand-off): Xr1 the
               stage-a cut (after m0c) through a hand-off round trip, resumed with fresh caches, and PLANT-RESUME (that state with m0u
               doubled must change the bars); Xr2 the stage-b cut (before the first 'c' unit). Each item is about two entry runs, so
               neither can be cut by the piece's CPU stop the way m3_run_v1_8_3's I9k1 was (RESUME_FAMS: the families that run them);
  asm.N        the two records m3_s8v2_H_N<N>_J300_v1_9.json and m3_s8v2_S4_N<N>_J300_v1_9.json, each with exactly the list's keys of
               its graph (C-SCOPE, PLANT-SCOPE), C-RESUME-CHAIN (Xr1 and Xr2 VALID for every family in RESUME_FAMS, their C-RESUME and
               PLANT-RESUME lines quoted), C-REP-B and C-REP-AK against the float twin, C-FMT through m3_reader_v6_3, the reader and
               bound plants on the H text, PLANT-NOWRITE; each record's prep16 field names the finished D16 tables' hand-offs, the memo,
               the block and the E2 width summary, and its claim_ball field states the ball form (the crossing rule,
               point 6: the a_k balls plus the bar without rnd, the box entry_ball returns; m3_reader_v6_3 checks it exactly, with
               PLANT-CLAIM-BALL and PLANT-CLAIM-BALL-MISSING).
- The float references are m3ref_v1_14's staged probe outputs (P16H, P16S4; the piece with P16-DONE at each N): C-PREP-REF, C-RULE,
  C-SMOKE-AK, PREP16-REP, C-REP-B, C-REP-AK.
- the note 2 on m3_run_v1_8_3 (C-SRC-TRIAL) concerns copied entries; this script copies none.
- Hand-offs and outputs are named m3_run_v1_9_<ITEM>; the E2 memos m3_run_v1_9_memo_<X>_N<N>.jsonl.
m3_run_v1_8_3's docstring follows.
m3_run_v1_8_3.py -- pk03 (code/pk03/). The CERTIFIED S9 entries of pk15's item (v) (the approval 2026-11-08 00:05Z; P2-2's
SH1 entries dropped 00:08Z): S9_ENTRY_LIST_v1 (pk03/), at J_REF = 300, K = 3, qcap 6, on the closed M-a layer.
REVISION of m3_run_v1_8.py (7d72fc7f), whose machinery is kept as written: C-HASH, C-IMPORT, C-VALIDATED with DENY, C-SERIES, C-PREC,
C-CX, C-CX2, PLANT-GUARD, C-FALLBACK-PATH, verdict-bound hand-offs, resumable entries (the stop factor, capped pieces skipped), C-RESUME,
the write after every gate and plant, RECORD lines, PLANT-NOWRITE, the bound reader and C-PREC-END. What changes:
- The list is S9_ENTRY_LIST_v1 (C-HASH pins it, and S8_ENTRY_LIST_v3 for the copies' definitions). Its three new entries Iht,b are
  computed in the family I9: [vac|int|vac] with the pairs of columns 0 and 2 and the top bond (3,6). The list's [xia, [u, v, w]] is
  m3_entries_v3's 'xia' factor on the pair (u, v); EDGES maps I9 to m3_entries_v3's edges 'N', and C-GRAPH-LIST checks I9's pairs
  against the list as before.
- Items (N = 4 or 3):
  I9a.N        the smoke piece: the a_k of the three Iht entries without bars or prep scalars, against the float twin (C-SMOKE-AK with
               PLANT-SMOKE-AK); no hand-off, no record;
  I9u.N, I9c.N I9's prep stages, fresh, each with C-PREP-SAME against m3_run_v1_8's Nu.N or Nc.N hand-off: the prep reads only the
               vertex forms, and I9 has N's vertices and couplings, so every scalar must overlap N's (a cross-check; bit-identical
               scalars and the largest relative mid difference are INFO; PLANT-PREP-SAME);
  I9k1..I9k9   resumable pieces of I9 (C-RESUME in piece 1 on Iht,1, whose state 1 uses the fewest pair forms, so its own tables
               are the smallest; m3_run_v1_8 ran C-RESUME in D.N);
  asm9.N       the record.
- The float reference is m3ref_v1_15's V9I (C-PREP-REF, C-RULE, C-SMOKE-AK, C-REP-B, C-REP-AK).
- asm9.N writes m3_s9_N<N>_J300_v1_8_3.json with exactly the list's 18 keys (C-SCOPE, PLANT-SCOPE). The 15 copies are the source items
  of the S8 records m3_s8v3_D_N<N>_J300_v1_8_1.json and m3_s8v3_N_N<N>_J300_v1_8_2.json, loaded through m3_reader_v4_4.load under the
  asm outputs that name them (C-SRC), copied byte for byte with alias_of '<record> <source key> <record sha256>' (C-COPY with
  PLANT-COPY); C-COPY-DEF: each copy's graph, factors, parity and K in the S9 list equal S8_ENTRY_LIST_v3's for its source key. The three
  Iht entries come from the I9 pieces (C-PIECES). The record's families field holds the radii of D and N (m3ref_v1_10) and of I9.
- Hand-offs and outputs are named m3_run_v1_8_3_<ITEM>; m3_run_v1_8's N hand-offs are read under its sha256 (V18_SHA, pinned in OWNMOD).
- m3_run_v1_8's plant_odd and run_small stay in the file and never run here: no item calls run_small, and the list has no parity zeros.
m3_run_v1_8's docstring follows.
m3_run_v1_8: The CERTIFIED entries of S8's route without 4-column entries: pk11's S8_ENTRY_LIST_v3
(12374013; U9's g,a,b and T,a,b for all ten z9sym states and the chain-on-B entries DY, DYY, TX, e, eX, f, fX, z, wXw, wXwX), 219 per N,
at J_REF = 300, K = 3, qcap 6, on the closed M-a layer. REVISION of m3_run_v1_7.py (e55c5de1), whose safeguards are kept as written:
C-HASH, C-IMPORT, C-VALIDATED with DENY, C-SERIES, C-PREC, C-CX, C-CX2, PLANT-GUARD, C-FALLBACK-PATH, verdict-bound hand-offs, resumable
entries (m3_bar's units, C-RESUME, the stop factor, capped pieces skipped), the write after every gate and plant, RECORD lines,
PLANT-NOWRITE, the bound reader and C-PREC-END. What changes:
- Entries come from the list, read by graph: D (strip_graph(2)), N ([vac|int|vac], pairs on L, R and (3,4)), E2 ([vac|free], m3_entries'
  'mix'), E3 ([vac|int|free]) and FF ([free|free], 'free2'). A key is the list's key exactly; parity zeros (parity_zero: true) are
  computed as balls holding 0 with C-ODD and C-ODD-AK, as S7's.
- C-GRAPH-LIST: each family's graph (m3_entries_v3.build_graph: the union of its entries' pair forms) has the couplings of the list's
  column spec (m3_graph_v3.strip, as a set) and exactly the list's pairs (PLANT-GRAPH-LIST: the pairs without one must fail).
- The float references are m3ref_v1_10's (4eb5113e; z9sym): C-PREP-REF (family, N, J), C-RULE (the radii^2 equal min(80 G_vv/300, 0.6)
  on the certified G_vv mids and rho'^2 = 0.7^2, to 1e-12; PLANT-RULE), and at asm C-REP-B and C-REP-AK against their KEYJSON lines.
- Items (N = 4 or 3): D.N, E2.N, FF.N (prep and entries); E3u.N, E3c.N (E3's prep stages) and E3k1.N .. E3k9.N (resumable pieces);
  Nu.N, Nc.N and Nk1.N .. Nk19.N; asm.N. C-RESUME and PLANT-RESUME run in D.N.
- asm writes five records, m3_s8v3_<D|N|E2|E3|FF>_N<N>_J300_v1_8.json (FORMAT 'M3_RECORD_v1', m3_record_v4; read through m3_reader_v4_4,
  as the consumers' loader), each with the list's keys of its graph (C-SCOPE, PLANT-SCOPE), trial_set in full sha256 and the list's pin.
  S7's C-KR4 (pk10's J = 170 records), C-KBAR and r_main have no counterpart here and are gone.
- Modules: m3_graph_v3 (020d4b54), m3_bar_v10 (b80f4e3b; dmaxH stays 18, no graph has more than 9 vertices), m3_entries_v3 (d9791822),
  with v1_7's m3_scal_v2, m3_series_v2, m3_major_v2, m3_record_v4, m3_reader_v4_4 and m3_handoff_v3.
Arguments: ITEM LIM (5..540). Output: stdout (the run line redirects it to out/m3_run_v1_8_<ITEM>.out); hand-offs in hand/; records in out/.
Run: D=/mnt/g2/release/root/code/pk03; OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 OMP_NUM_THREADS=1 TMPDIR=$D/tmp
  timeout 580 nice -n 10 prlimit --as=8589934592 -- python3 -I -B $D/m3_run_v1_8.py ITEM LIM
  > $D/out/m3_run_v1_8_ITEM.out 2> $D/out/m3_run_v1_8_ITEM.err
m3_run_v1_7's own docstring (its history back to m3_run_v1_5) stays in that file.
"""
import resource, sys, time, math, hashlib, signal, os, json, re, traceback

ITEM_RE = r'((L|LH|LT)a|Lp([1-9]|1[0-9])|(L|LH|LT)k[1-9]|LHr[12]|asm)\.(4|3)'   # pk23 hl_v1: L's prep pieces, one smoke item per family
if len(sys.argv) != 3 or not re.fullmatch(ITEM_RE, sys.argv[1]):
    print('usage: m3_run_v1_9_3_hl_v1.py ITEM LIM   (ITEM = La|LHa|LTa|Lp1..Lp19|<X>k1..<X>k9|LHr1|LHr2|asm . 4|3, X = L|LH|LT; LIM = RLIMIT_CPU soft limit in s, 5..540)')
    sys.exit(2)
ITEM = sys.argv[1]
FAM, NN = ITEM.split('.')[0], int(ITEM.split('.')[1])
LIM = int(sys.argv[2]) if re.fullmatch(r'[0-9]{1,3}', sys.argv[2]) else -1
if not (5 <= LIM <= 540):
    print('bad LIM %r' % sys.argv[2])
    sys.exit(2)
resource.setrlimit(resource.RLIMIT_CPU, (LIM, LIM + 5))
STAGE = ['start']


def cpu():
    return time.process_time()


def out(line):
    print(line, flush=True)


def _on_xcpu(signum, frame):
    out('CAP-STOP SIGXCPU at cpu %.1f s in stage %s' % (cpu(), STAGE[0]))
    out('VERDICT INCOMPLETE (CAP-STOP)')
    os._exit(3)


signal.signal(signal.SIGXCPU, _on_xcpu)
W18 = '/mnt/g2/release/root/code'
OWN = W18 + '/pk03'
C2B = W18 + '/pk02'
INP = W18 + '/pk10/scratch'
W4 = W18 + '/pk11/out'
MYD = W18 + '/pk22/m3'   # pk22 copy: the folder of every written path
HLD = W18 + '/pk23/pev'   # pk23 hl_v1: the list, the hand-off module copy, the references
OUTD = HLD + '/out'   # pk23 hl_v1: written outputs, memos, records and out/tab16c here (MYD: pk22's pinned inputs, read-only)
OUTD_IN = OWN + '/out'   # pk22 copy: the pinned inputs and float twins that sit in pk03/out
HANDD = HLD + '/hand'   # pk23 hl_v1: hand-offs here
PSX = W18 + '/pk22/midrow/psixy'   # c3k: the z9symxy trial files
MODDIR = {'m3_handoff_v3_hl.py': HLD}   # pk23 hl_v1: the one module read from pk23/pev/
KERNEL = 'arbeng_ma_v1_4_1'   # m3_run_v1_9: the layer of every table, prep and entry here
ARBK = 'arbeng_ma_stub_v1_1'
ARBB = 'arbeng_c2b_v2'   # the arb base under ARBK (pinned in KFILES)
KFILES = {
    'arbeng_ma_v1_4_1.py': '1f58ad80ceb1c0992f08f894c0f6af26ef18d397627020a5a5fe7130818375d9',
    'arbeng_ma_stub_v1_1.py': '794fabc7111555db2f6390a144d3f5af6deeb358d02da8b5705cf3ceaefd0af1',
    'arbeng_c2b_v2.py': '12c839a6dcde8028d61e88dad31ad3dc3bf0faae850e8f9065407e3ace092cb0',
}
VALREC = [   # m3_run_v1_9: arbeng_ma_v1_4_1's validation records and the two closes, in order
    (C2B, 'MANIFEST_ARBENG_MA_v1_4_1.sha256', 'c172e15f42cad0278bdea3343ddea084327dbf89a4eef2561df7e5d23140f5fc'),
    (C2B, 'MANIFEST_KT_MA_VAL_v1_6_RUN.sha256', '7ec00dc5d98d64c06e345d80b4a0959e7ec6805239a4d03ba7be006882186314'),
    (C2B + '/out', 'out_kt_ma_val_v1_6_1_d.out', 'af1e3f66a88c27b0593b31e23f936986ecd04c813854ed4001cc601f7a6bef12'),
    (W18 + '/rv01', 'REVIEW_CODE_ARBENG_MA_V1_4_rv01.md', '8afbb958904ab2067d75b6876b2b6496dda7286ba99d4d00428e3cd7a4485335'),
    (W18 + '/rv01', 'DELTA_ARBENG_MA_V1_4_1_rv01.md', '3fd1bfa7dc00d4600aa3ff1d413807cb75e9ab9d910600d580ab48bd6b36fc4f'),
]
VALIDATED = {('arbeng_ma_v1_4_1.py', '1f58ad80ceb1c0992f08f894c0f6af26ef18d397627020a5a5fe7130818375d9', tuple(v[2] for v in VALREC))}
DENY = {('arbeng_ma_v1_1.py', '81f7fb89f863343149b1558bfc3c8ba3e09b3e6c36ec00db4c12197b11158e7f'),
        ('arbeng_ma_v1_2.py', '935f2ca77dbcb7de0670d43505044f9c12c086f69de2a30f7b8133522ffcec80'),
        ('arbeng_ma_v1_4.py', '9870e7f8d5dc33f0edca029f9945de4774a1eb572114aa385dd7b75d7506e017'),   # m3_run_v1_9: the unpinned predecessor
        ('mock_arbeng_v1_4.py', '324ae7e77e67c7f8fc84e7f3819f17de59d46bfcc88f7d14294bab5cf8e4b02e')}   # pk03's mock (tmp/r16)


def tag_for(kfile, ksha, vshas, validated=None):
    """'' (certified) only for a (file, full sha256, validation sha256s) in VALIDATED and never for a denied (file, sha256)."""
    if (kfile, ksha) in DENY:
        return '_PRECERT'
    return '' if (kfile, ksha, tuple(vshas)) in (VALIDATED if validated is None else validated) else (
        '_STUB' if 'stub' in kfile else '_PRECERT')


TAG = None   # set by C-VALIDATED after the imports
OWNMOD = {
    'm3_scal_v2.py': 'd22d3ad696074d4235f0fd31b026477e87f96f5d4b5331e29ab8d399e1e8f054',
    'm3_graph_v3.py': '46fd3c668e0121d58e6992636aec96f0d27c72176c70a69aa6a367f81c12da6a',
    'm3_series_v2.py': '08b1acf127062612d2dd3dd583e555f5ad3097b1b657cba89424019c4d958923',
    'm3_major_v2.py': '89dd5a2184a511d4dea39fb3c558501e9738af118be9d41f2ac4b2d4b8d7b016',
    'm3_bar_v11.py': 'a11438d0b7d555e3f53aae65e57588df0a2a8a88a79fd0dc47300feeed4f59e3',
    'm3_entries_v3.py': '7bf360cbc739cad1397aa5f23ba2ab3e838dec5d65c686880b664fe3318ce9a9',
    'm3_record_v4.py': '2c8a53efb5170d6c6e320bd814c824e69d2ccdd73c57cf87a9130b796109e30f',
    'm3_reader_v6_3.py': '539b613f6a9c07a9bef3d0cbb408c1d41de276a6a59aede8b03149204ce28661',
    'm3_handoff_v3_hl.py': 'bb07cd3e28c1d3e1b114086a69038b8d01fe4484136e3c2923e28c4f641f17f3',   # pk23 hl_v1: pk22's copy with HAND moved to pk23/pev/hand
}
INPUTS = {
    (W4, 'S8_ENTRY_LIST_v2.json'): 'c3830f588dbaa2ef4de558659ab742caa7b231e91810dfd2ec036d66d9cdce5e',   # m3_run_v1_9
    (W4, 'ts_N4_J170_D_S_z9sym_v1.json'): 'ea9d6c1bc72cdac5b6d55091766a908937c7ce2bf60257636824388ffe5b7b5d',
    (W4, 'ts_N3_S_z9sym_v1.json'): 'a298db655d832c0685a9aba093dd123d372698fa2fb7905a15f442bb0e35f8e6',
    (W4, 'vacres_K3_N4_sym_v1.json'): 'b40859de2607f64cd127cb1834a04e9f33b3c2cbe4af9fe4f2bb80badaacd43e',
    (W4, 'vacres_K3_N3_sym_v1.json'): 'e5a9b49fde1896ff1d87de1d4a44571376eeeeb31b0ce4205faecdd2463115c0',
    (INP, 'm2_N4_J170.json.b'): '7c0d4316e5162300becf5b541ebb4d2e68c83115ee2f35f30c4f2b22ffc95a19',
    (INP, 'm2_N3_J170.json.b'): '55da99fdd7bf1719685203a10b2c76e0fafc1dbb62fe859f36fc3b04f9cd2af0',
    (OUTD_IN, 'm3ref_v1_14_P16H.4.p6_z9sym.out'): 'df052bb8e868d03c6ca08cbd5cd4da288e5ab2e82e92e6eee805429b3200703a',
    (OUTD_IN, 'm3ref_v1_14_P16S4.4.p6_z9sym.out'): 'c6aa2973996139496fcf370d7289ca84b10365be2b736da7afe23f2775794437',
    (OUTD_IN, 'm3ref_v1_14_P16H.3.p6_z9sym.out'): '5029d364ccc4786b5e973cf216ca11677b71169c9cf1da3289fab7bf9d945781',
    (OUTD_IN, 'm3ref_v1_14_P16S4.3.p6_z9sym.out'): 'dd394db3466596f191b34a1a648dff26016fda74b1cf53e360b44e8e06e03d7b',
    (OWN + '/tmp/r16', 'mock_arbeng_v1_4.py'): '324ae7e77e67c7f8fc84e7f3819f17de59d46bfcc88f7d14294bab5cf8e4b02e',   # PLANT-MOCK's file
    (MYD, 'C3_ENTRY_LIST_v2.json'): 'e877d12f0686ff959bc34f12651f62629f0e3f43acc76b2cc363ec2524eaf1c6',   # c3: the c3 list
    (MYD, 'm3_run_v1_9_3_px22_c1.py'): 'af6ce85c480f50a8da5b205bc87abf088fad1ef2019add3f54225001b37ad61e',   # c3: c1, the producer of the S4 prep pieces CS4 reads
    (OWN, 'm3_run_v1_9_3.py'): '34abe3743035bd709e202eb4de2bdc752fef8a8abc6ebd5d0e4963050caa1dbb',   # c3: pk03's runner, the producer of the H prep pieces H4T reads
    (MYD, 'C3H_ENTRY_LIST_v1.json'): '4f56853ab2390a8e29b384921315ed9e4501a5bf97f66c82986e2283ecfb21f3',   # c3h: the C3-h list
    (MYD, 'm3_run_v1_9_3_px22_c3_1.py'): 'bbecee470d6b2a9927b4d8e51e0a1b6dc1da9a441201739b637ab1fc84b466ce',   # c3h: c3_1, the producer of the CE3 prep pieces CE3H reads
    (MYD, 'rtwin_c3h_v1.py'): 'cf775f629f4a51ec94a6fa0c8cb7456d0fb7115c03670ff86740f13bd39dae81',   # c3h: the producer of the float references (restored prep)
    (MYD, 'C3J_ENTRY_LIST_v1.json'): '3cc83e2a2b55ea8c000328ad9c1b83ba3941780403dd5d98d5f83b0a319dcd75',   # c3j: the c3j list
    (MYD, 'rtwin_c3j_v1.py'): '8e723da06cc9505be81266f6845ba3ef41e1c13cd46f614af5ec9600614722ff',   # c3j: the producer of the float references (restored prep)
    (MYD, 'C3K_ENTRY_LIST_v1.json'): '73d132270f4d07da13e3d16aa50673acd21bc9753ce524f2ae80717e1f7b61de',   # c3k: the c3k list
    (MYD, 'C3K_ENTRY_LIST_v1_1.json'): '060263495bf3fa3a3f06f3b697c67d04f3b1050d27cd9699fe6fb84381f808cd',   # c3k_1: the c3k_1 list
    (MYD, 'rtwin_c3k_v1_1.py'): '49308d692626aed52c32be71091024e2d00dbd5bf4b48df2b85b995d732b2eb8',   # c3k: the producer of the float references (restored prep)
    (HLD, 'HL_ENTRY_LIST_v1.json'): '2d115b6de96e5d8da01bb20ca11ccda6c7d650eb74faed1262f24be619e3ed42',   # pk23 hl_v1
    (HLD, 'rtwin_hl_v1.py'): '16d60bcf688effb26812881b3cac6d6bbfe07b3c921a2f85c179dc86b222f373',   # pk23 hl_v1
    (HLD, 'm3ref_hl_v1.py'): 'd3572ec715f3b1be159939258bfa0c86f12f975390f3f925f7aef2de47620bee',   # pk23 hl_v1
    (OUTD, 'm3ref_hl_v1_P16L.4.p5_z9sym.out'): '19ddb6ec632f6e5611141cc2daeb902b6ecde22bb055314d9c174a3983c994de',   # pk23 hl_v1
    (OUTD, 'm3ref_hl_v1_P16L.3.p5_z9sym.out'): 'fe622646f061c745870bd459d9423f870c70fb9ee8c5c7250f9372f4a9969668',   # pk23 hl_v1
    (OUTD, 'rtwin_hl_v1_L.4_z9sym.out'): 'a741208b76de52a6b66e46af4f43f33ffc0014eafe054c7ed9ebe8a158ea8fc8',   # pk23 hl_v1
    (OUTD, 'rtwin_hl_v1_LH.4_z9sym.out'): '9b447ca42a0bdfd83aaba67e1799b7fcc60a079176cae1d2d6bb44479465aaba',   # pk23 hl_v1
    (OUTD, 'rtwin_hl_v1_LT.4_z9sym.out'): '420cea82880ea912c8a7dbfec39c226e99844c410c2bfa30d13649904971a95b',   # pk23 hl_v1
    (OUTD, 'rtwin_hl_v1_L.3_z9sym.out'): 'ab93f3d760ba85746841b5bad9709e5d4fd8478e18824bb3447d93c506ac1510',   # pk23 hl_v1
    (OUTD, 'rtwin_hl_v1_LH.3_z9sym.out'): 'b3a2a24a50fda54cbaa5cd86a6eace84852dea6007a6e05e6bf4810c122179f0',   # pk23 hl_v1
    (OUTD, 'rtwin_hl_v1_LT.3_z9sym.out'): '838d442af63ed6857361347c190271ef5a7a52fb5994029ce6bed1f961e9d70f',   # pk23 hl_v1
}
# c3: REFP16, REFPIECE and REFOUT give way to KEYREF and PREPREF (the configuration below)

FAILS, NOFIRE = [], []


def gate(name, ok, line):
    out('%s %s -> %s' % (name, line, 'PASS' if ok else 'FAIL'))
    if not ok:
        FAILS.append(name)


def plant(name, fired, line):
    out('%s %s -> %s' % (name, line, 'FIRES' if fired else 'DOES NOT FIRE'))
    if not fired:
        NOFIRE.append(name)


def valid_verdict():
    """the exact verdict line of a valid run of this script (certified TAG '' is required, so 'VERDICT VALID')."""
    return 'VERDICT VALID'


def finish():
    if 'S' in globals():
        out('PRECISION end: %s' % S.precision_line())
    if 'K' in globals() and 'flint' in globals():
        gate('C-PREC-END', K.PREC == 512 and flint.ctx.prec == 512, '(flint ctx.prec %d at the end of the item; C-PREC checked the start)' % flint.ctx.prec)
    out('STAGE-CPU total %.2f s' % cpu())
    if FAILS or NOFIRE:
        out('VERDICT INVALID (%s)' % ', '.join(FAILS + ['%s did not fire' % p for p in NOFIRE]))
    elif TAG != '':
        out('VERDICT INVALID (C-VALIDATED: TAG %r; this script writes certified records only)' % (TAG,))
    else:
        out(valid_verdict())


def sha(path):
    with open(path, 'rb') as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def tsha(text):
    """the sha256 of a text as written (json.dumps texts are ASCII)."""
    return hashlib.sha256(text.encode()).hexdigest()


def flip(h):
    """h with its last hex digit changed (plants)."""
    return h[:-1] + ('0' if h[-1] != '0' else '1')


def stage(name):
    STAGE[0] = name
    out('STAGE-CPU %s start %.2f s' % (name, cpu()))


SELF_SHA = sha(os.path.abspath(__file__))
out('m3_run_v1_9_3 item %s LIM %d; script sha256 %s; python %s' % (ITEM, LIM, SELF_SHA, sys.version.split()[0]))
stage('C-HASH')
bad = [f for f, h in OWNMOD.items() if sha(os.path.join(MODDIR.get(f, OWN), f)) != h]
bad += [f for f, h in KFILES.items() if sha(os.path.join(C2B, f)) != h]
bad += [f for (d, f), h in INPUTS.items() if os.path.exists(os.path.join(d, f)) and sha(os.path.join(d, f)) != h]
missing = [f for (d, f), h in INPUTS.items() if not os.path.exists(os.path.join(d, f))]
gate('C-HASH', not bad and not missing, '(%d modules, the kernel files, %d inputs)%s%s' % (len(OWNMOD), len(INPUTS),
     (': changed ' + ', '.join(bad)) if bad else '', (': missing ' + ', '.join(missing)) if missing else ''))
plant('PLANT-HASH', sha(os.path.join(OWN, 'm3_scal_v2.py')) != OWNMOD['m3_scal_v2.py'][:-1] + ('0' if OWNMOD['m3_scal_v2.py'][-1] != '0' else '1'),
      '(m3_scal_v2 against a sha with its last digit changed)')
if FAILS:
    finish()
    sys.exit(1)
from fractions import Fraction
from decimal import Decimal
import importlib.util
GENERIC = [('m3_scal', 'm3_scal_v2.py'), ('m3_graph', 'm3_graph_v3.py'), ('m3_series', 'm3_series_v2.py'), ('m3_major', 'm3_major_v2.py'),
           ('m3_bar', 'm3_bar_v11.py'), ('m3_entries', 'm3_entries_v3.py'), ('m3_record', 'm3_record_v4.py'), ('m3_reader', 'm3_reader_v6_3.py'),
           ('m3_handoff', 'm3_handoff_v3_hl.py')]


def load_as(name, fname):
    """a pinned file of pk03/ loaded under its generic module name (dependencies first)."""
    spec = importlib.util.spec_from_file_location(name, os.path.join(MODDIR.get(fname, OWN), fname))
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


MODS = {name: load_as(name, fname) for name, fname in GENERIC}
S, GR, SER, BAR, ENT, REC, RDR, HO = (MODS[k] for k in ('m3_scal', 'm3_graph', 'm3_series', 'm3_bar', 'm3_entries', 'm3_record', 'm3_reader',
                                                         'm3_handoff'))
sys.path.append(C2B)
import arbeng_ma_v1_4_1 as K
import arbeng_ma_stub_v1_1 as A
_to_arb0 = {'layer': K.to_arb, 'arb': A.to_arb}


def _guard(which):
    def conv(v):
        """the kernel's own converter, refusing mp.iv values: M3 passes arb balls only (a checked fact since m3_run_v1_3)."""
        if hasattr(v, '_mpi_'):
            raise TypeError('an mp.iv value reached the %s kernel converter; M3 passes arb only' % which)
        return _to_arb0[which](v)
    return conv


K.to_arb = _guard('layer')
A.to_arb = _guard('arb')
BAR.ARB['kern'] = A
assert HO.HAND == HANDD, (HO.HAND, HANDD)   # pk22 copy: the hand-off module writes where item_state looks
import flint
from mpmath import iv
badw = [n for n, m in MODS.items() if os.path.abspath(m.__file__) != os.path.join(MODDIR.get(dict(GENERIC)[n], OWN), dict(GENERIC)[n])]
badw += [] if os.path.dirname(os.path.abspath(K.__file__)) == C2B else ['kernel']
badw += [] if os.path.dirname(os.path.abspath(A.__file__)) == C2B else ['arb kernel']
gate('C-IMPORT', not badw and K.VERSION == KERNEL and A.VERSION == ARBK, '(generic names from their pinned files in %s; kernel %s and arb kernel %s from %s)%s' % (
    OWN, K.VERSION, A.VERSION, C2B, (': ' + ', '.join(badw)) if badw else ''))
stage('C-VALIDATED')
vbad = []
if os.path.abspath(K.__file__) != os.path.join(C2B, KERNEL + '.py') or sha(os.path.abspath(K.__file__)) != KFILES[KERNEL + '.py']:
    vbad.append('the imported layer is not pk02/%s.py with the pinned sha256' % KERNEL)
for d_, f_, h_ in VALREC:
    p_ = os.path.join(d_, f_)
    if not os.path.exists(p_) or sha(p_) != h_:
        vbad.append('%s missing or changed' % f_)
    elif f_.startswith('out_kt_ma_val'):
        with open(p_) as fh:
            vl = [ln.rstrip('\n') for ln in fh if ln.startswith('VERDICT')]
        if vl != ['VERDICT VALID']:
            vbad.append('%s: VERDICT lines %r' % (f_, vl))
TAG = tag_for(KERNEL + '.py', KFILES[KERNEL + '.py'], [v[2] for v in VALREC])
gate('C-VALIDATED', not vbad and TAG == '', '(layer %s:%s; %d validation records with exactly ["VERDICT VALID"] and the close by sha256; TAG %r)%s' % (
    KERNEL, KFILES[KERNEL + '.py'][:8], len(VALREC), TAG, (': ' + '; '.join(vbad)) if vbad else ''))
d11 = [k for k in DENY if k[0] == 'arbeng_ma_v1_1.py'][0]
plant('PLANT-DENY', tag_for(d11[0], d11[1], [v[2] for v in VALREC], set(VALIDATED) | {(d11[0], d11[1], tuple(v[2] for v in VALREC))}) != '',
      '(arbeng_ma_v1_1 placed in a copy of VALIDATED must still be refused the certified tag)')
# m3_run_v1_9: C-VALREC-RUN, PLANT-MOCK, C-CALLER and PLANT-CALLER
RUNMAN = [v for v in VALREC if v[1] == 'MANIFEST_KT_MA_VAL_v1_6_RUN.sha256'][0]
rbad, nrun, nvo = [], 0, 0
with open(os.path.join(RUNMAN[0], RUNMAN[1])) as fh:
    for ln in fh:
        h_, p_ = ln.split()
        nrun += 1
        if not os.path.exists(p_) or sha(p_) != h_:
            rbad.append('%s missing or changed' % os.path.basename(p_))
        elif os.path.basename(p_).startswith('out_kt_ma_val') and p_.endswith('.out'):
            nvo += 1
            with open(p_) as fo:
                vl = [x.rstrip('\n') for x in fo if x.startswith('VERDICT')]
            if vl != ['VERDICT VALID']:
                rbad.append('%s: VERDICT lines %r' % (os.path.basename(p_), vl))
gate('C-VALREC-RUN', not rbad and nrun > 0 and nvo > 0, '(%s: %d files re-hashed against it, %d validation outputs with exactly ["VERDICT '
     'VALID"])%s' % (RUNMAN[1], nrun, nvo, (': ' + '; '.join(rbad)) if rbad else ''))
MOCK = os.path.join(OWN, 'tmp', 'r16', 'mock_arbeng_v1_4.py')
msha = sha(MOCK)
plant('PLANT-MOCK', tag_for(KERNEL + '.py', msha, [v[2] for v in VALREC]) != '' and tag_for('mock_arbeng_v1_4.py', msha, [v[2] for v in VALREC]) != '',
      '(pk03\'s mock tmp/r16/mock_arbeng_v1_4.py, sha256 %s, offered as %s.py and under its own name, must be refused the certified '
      'tag)' % (msha[:8], KERNEL))


def caller_scan(text):
    """C-CALLER's scan of a source text: the offending call lines (E2_combine without plan= or fallback=False, load_view without a second
    argument, MomTableU without block=), comments aside."""
    bad = []
    for i, ln in enumerate(text.split('\n')):
        code = ln.split('#')[0]
        if re.search(r'\.E2_combine\(', code) and not ('plan=' in code and 'fallback=False' in code):
            bad.append('l.%d E2_combine' % (i + 1))
        if re.search(r'\.load_view\(', code) and not re.search(r'\.load_view\([^,()]+,\s*[^)\s]', code):
            bad.append('l.%d load_view' % (i + 1))
        if re.search(r'\.MomTableU\(', code) and 'block=' not in code:
            bad.append('l.%d MomTableU' % (i + 1))
    return bad


with open(os.path.join(OWN, 'm3_bar_v11.py')) as fh:
    BARSRC = fh.read()
ncall = len(re.findall(r'\.E2_combine\(|\.load_view\(|\.MomTableU\(', '\n'.join(ln.split('#')[0] for ln in BARSRC.split('\n'))))
cbad = caller_scan(BARSRC)
gate('C-CALLER', ncall >= 3 and not cbad, '(m3_bar_v11: %d kernel calls; every E2_combine passes plan= and fallback=False, every load_view an '
     'expected sha256, every MomTableU block=)%s' % (ncall, (': ' + ', '.join(cbad)) if cbad else ''))
cmut = BARSRC.replace('E2_combine(parts, plan=plan, fallback=False)', 'E2_combine(parts, fallback=False)', 1)
plant('PLANT-CALLER', cmut != BARSRC and bool(caller_scan(cmut)), '(m3_bar_v11 with one E2_combine call\'s plan= removed)')
SER_RE = re.compile(r'[A-Za-z0-9]' + '_series' + r'\s*\(')
ser_hits = []
for p_ in [os.path.join(MODDIR.get(f, OWN), f) for f in OWNMOD] + [os.path.join(C2B, f) for f in KFILES] + [os.path.abspath(__file__)]:
    with open(p_) as fh:
        ser_hits += ['%s:%d' % (os.path.basename(p_), i + 1) for i, ln in enumerate(fh) if SER_RE.search(ln)]
gate('C-SERIES', not ser_hits, '(no *_series( call in %d modules, the kernel files and this script)%s' % (len(OWNMOD), (': ' + ', '.join(ser_hits)) if ser_hits else ''))
plant('PLANT-SERIES', bool(SER_RE.search('x = acb' + '_series(1)')), '(a planted *_series( call must be flagged)')
S.setup()
flint.ctx.prec = K.PREC
gate('C-PREC', K.PREC == 512 and flint.ctx.prec == 512, '(flint ctx.prec %d = the layer\'s PREC %d)' % (flint.ctx.prec, K.PREC))
out('PRECISION start: %s; env %s' % (S.precision_line(), K.env_probes()))
cx_ok, cx_fired = S.crossings_test()
gate('C-CX', cx_ok, '(M3\'s own mp.iv <-> arb crossings: round trips contain their sources)')
plant('PLANT-CX', cx_fired, '(the unsigned to_man_exp form must lose -1/3)')


def _ef(raw):
    """an mp.iv end as an exact rational from its raw (sign, man, exp, bc); special values raise."""
    sign, man, exp, bc = raw
    if man == 0 and exp != 0:
        raise ValueError('special interval end %r' % (raw,))
    v = Fraction(man) * Fraction(2) ** exp
    return -v if sign else v


cx2 = []
for lo_, hi_ in (('-0.25', '0.75'), ('-0.75', '0.25'), ('-0.5', '0')):
    x_ = iv.mpf([lo_, hi_])
    a_ = S.iv_to_arb(x_)
    b_ = [_ef(r) for r in S.arb_to_iv(a_)._mpi_]
    cx2.append(a_.contains(flint.arb(lo_)) and a_.contains(flint.arb(hi_)) and b_[0] <= Fraction(lo_) and Fraction(hi_) <= b_[1])
gate('C-CX2', all(cx2), '(asymmetric straddling and zero-end intervals [-0.25, 0.75], [-0.75, 0.25], [-0.5, 0]: iv -> arb holds both ends, '
     'arb -> iv holds the source)')
from mpmath import libmp
x_ = iv.mpf(['-0.25', '0.75'])
um = [libmp.to_man_exp(r) for r in x_._mpi_]
uarb = (flint.arb(int(um[0][0])) * flint.arb(2) ** int(um[0][1])).union(flint.arb(int(um[1][0])) * flint.arb(2) ** int(um[1][1]))
plant('PLANT-CX2', not uarb.contains(flint.arb('-0.25')), '(the unsigned to_man_exp form of [-0.25, 0.75] must lose -0.25)')
gfired = []
for mod in (K, A):
    try:
        mod.to_arb(iv.mpf(1) / 3)
        gfired.append(False)
    except TypeError:
        gfired.append(True)
plant('PLANT-GUARD', all(gfired), '(an mp.iv value handed to either kernel converter must raise)')


def fallback_tests():
    """C-FALLBACK-PATH: a MAFallback forced at a 2-form table (Gam = [[2, 1], [1, 3]], W_int = I) is recomputed by the arb kernel, whose
    ball must overlap the layer's own for the same E2; PLANT-FALLBACK-ONLY: a ValueError in the layer's E2 must reach the caller."""
    tb = BAR.TableFB(K, S.arb_mat_of([[2, 1], [1, 3]]), NN - 1, 4, None, None, [[1, 0], [0, 1]], 'fallback test')
    P = S.spoly(K, {(1, 0): 1, (0, 1): -1}, 2)
    Q = S.spoly(K, {(1, 1): 1}, 2)
    v_ma = tb.E2(P, Q)
    real = tb.tab

    class Raise:
        def __init__(self, exc):
            self.exc = exc

        def E2(self, P_, Q_, fallback=True):
            raise self.exc

    n0 = len(BAR.FALLBACKS)
    tb.tab = Raise(K.MAFallback('forced by C-FALLBACK-PATH'))
    v_arb = tb.E2(P, Q)
    gate('C-FALLBACK-PATH', len(BAR.FALLBACKS) == n0 + 1 and v_ma.overlaps(v_arb),
         '(a forced MAFallback: the arb kernel\'s E2 %s overlaps the layer\'s %s)' % (v_arb.str(12), v_ma.str(12)))
    tb.tab = Raise(ValueError('planted'))
    try:
        tb.E2(P, Q)
        fired = False
    except ValueError:
        fired = True
    plant('PLANT-FALLBACK-ONLY', fired, '(a ValueError in the layer\'s E2 must reach the caller)')
    tb.tab = real
    del BAR.FALLBACKS[:]


def fb_info():
    """the item's MAFallback recomputes (INFO), printed and kept in its hand-off."""
    out('FALLBACKS %d (MAFallback recomputes in arb, INFO)%s' % (len(BAR.FALLBACKS), (': ' + '; '.join(BAR.FALLBACKS[:20])) if BAR.FALLBACKS else ''))
    return list(BAR.FALLBACKS)


fallback_tests()
T_REF = Fraction(1, 300)


def read_lines(path, tag):
    with open(path) as fh:
        return [json.loads(ln[len(tag) + 1:]) for ln in fh if ln.startswith(tag + ' ')]


LISTF = 'HL_ENTRY_LIST_v1.json'   # pk23 hl_v1: pk23's L list (pinned in INPUTS under HLD)
with open(os.path.join(HLD, LISTF)) as fh:   # pk23 hl_v1
    LIST = json.load(fh)
with open(os.path.join(MYD, 'C3_ENTRY_LIST_v2.json')) as fh:   # c3h: c3's list, for CE3's graph (C-PREP-SHARE; unused by c3k's families)
    LISTC3 = json.load(fh)
with open(os.path.join(W4, 'S8_ENTRY_LIST_v2.json')) as fh:   # c3: S8's list v2, for the S4 and H graphs of the shared preps (C-PREP-SHARE)
    LISTS8 = json.load(fh)
with open(os.path.join(INP, 'm2_N%d_J170.json.b' % NN)) as fh:
    KBAR = json.load(fh)['kbar']
TSF = {4: 'ts_N4_J170_D_S_z9sym_v1.json', 3: 'ts_N3_S_z9sym_v1.json'}[NN]   # pk23 hl_v1: z9sym, pk25's mr/v3 TRIAL_SET (the row 4435)
TS = ENT.load_trial(os.path.join(W4, TSF), os.path.join(W4, 'vacres_K3_N%d_sym_v1.json' % NN), KBAR)   # pk23 hl_v1
TRIAL = {'ts': '%s:%s' % (TSF, INPUTS[(W4, TSF)]), 'vacres': 'vacres_K3_N%d_sym_v1.json:%s' % (NN, INPUTS[(W4, 'vacres_K3_N%d_sym_v1.json' % NN)])}   # pk23 hl_v1
FAMS = ('L', 'LH', 'LT')   # pk23 hl_v1: the L list's graphs computed here (LB is a float control only)
EDGES = {g: 'N' for g in FAMS}   # only for m3_entries_v3.factor's column lookup: every factor here names its column by index or triple
PARITY_ZERO = set()   # c3k: no parity zero in the c3k list (C-PARITY-SET checks that no entry passes C-ODD)
V3 = [{'id': '%s:%s' % (e['graph'], e['key']), 'key': e['key'], 'graph': e['graph'], 'factors': e['factors'],
       'parity': 'zero' if (e.get('parity_zero') or '%s:%s' % (e['graph'], e['key']) in PARITY_ZERO) else 'free', 'grouping': e.get('grouping', 'std')}
      for e in LIST['entries'] if e['graph'] in FAMS]   # c3j: each entry's grouping from the list
assert all(e['grouping'] in ('std', 'split') for e in V3)
PREPOF = {'L': 'L', 'LH': 'L', 'LT': 'L'}   # pk23 hl_v1: one prep family L (12 vertices) read by LH and LT
FAMREF = {'L': 'P16L', 'LH': 'P16L', 'LT': 'P16L'}   # pk23 hl_v1: the twin m3ref_hl_v1's P16L PREPJSON
KEYFAM = {'L': 'P16L', 'LH': 'P16LH', 'LT': 'P16LT'}   # pk23 hl_v1: the family names of rtwin_hl_v1's KEYJSON
KEYREF = dict((g, 'rtwin_hl_v1_%s.%d_z9sym.out' % (g, NN)) for g in FAMS)   # pk23 hl_v1: rtwin_hl_v1's references (restored prep; pinned)
PREPREF = dict((g, os.path.join(OUTD, {4: 'm3ref_hl_v1_P16L.4.p5_z9sym.out', 3: 'm3ref_hl_v1_P16L.3.p5_z9sym.out'}[NN])) for g in FAMS)   # pk23 hl_v1: the twin's P16L pieces with P16-DONE (pinned)
RULE = (80.0, 0.6, 0.7)   # the float references' radii sqrt(min(80 G_vv/J, 0.6)) and rho' (m3ref_v1_14's default for every P16 family)
PFX = {'L': 'L', 'LH': 'LH', 'LT': 'LT', 'CE3': 'CE3', 'S4': 'S4', 'H': 'H'}   # item prefixes (pk23 hl_v1: L, LH, LT)
MAXP = {g: 9 for g in FAMS}   # entry pieces
MAXPP = 19   # prep pieces
RESUME_FAMS = ('LH',)   # pk23 hl_v1: the family with the items Xr1, Xr2
RESUME_KEY = {'LH': 'Mh,0,0'}   # C-RESUME's entry (pk23 hl_v1)
C1_SHA = INPUTS[(MYD, 'm3_run_v1_9_3_px22_c1.py')]   # c3: the producer of the S4 prep pieces (unused by c3k's families)
H_SHA = INPUTS[(OWN, 'm3_run_v1_9_3.py')]   # c3: pk03's runner (its H prep pieces; unused by c3k's families)
C31_SHA = INPUTS[(MYD, 'm3_run_v1_9_3_px22_c3_1.py')]   # c3h: c3_1 (its CE3 prep pieces; unused by c3k's families)


def item_sha(item):
    """c3h: the script sha256 an item's output and hand-off carry: c1's for the S4 prep pieces, pk03's runner's for the H prep
    pieces, c3_1's for the CE3 prep pieces, this script's for every other item (c3k: E4D's and E4N's prep pieces are this script's)."""
    if re.fullmatch(r'S4p[0-9]+\.[34]', item):
        return C1_SHA
    if re.fullmatch(r'Hp[0-9]+\.[34]', item):
        return H_SHA
    if re.fullmatch(r'CE3p[0-9]+\.[34]', item):
        return C31_SHA
    return SELF_SHA
TAB16 = os.path.join(OUTD, 'tab16c')   # the D16 tables' state directories (MomTableU), kept
NS_UNIT, NS_E2, NS_FIN = 2.5e-7, 1.2e-7, 4.0e-6   # CPU s per planned pair of a table unit, per E2 term pair, per moment of a finish
BLOCK16 = 5000   # MomTableU's destinations per block, for every table's life (v1_4_1's default)
UNIT_PAIRS, E2_PAIRS, E2_MIN = 1.0e9, 1.5e9, 2.0e8   # the pair budgets of a table unit and of an E2 block; E2s up to E2_MIN pairs in one call
CLAIM_BALL = ('for every J >= J_REF, t = 1/J, t = 0 included: I(J)/main(J) lies in sum_k [ak_k - ak_rad_k, ak_k + ak_rad_k] t^k + '
              '[-sum Bp, sum Bp] (Lemma U: PLAN_M3_CODE_v1 l.125, v1_2 U4)')   # 


def name_of(e):
    return e['key']


def qcap_of(e):
    """qcap 6 for every entry of the list (S8's convention; m3ref_v1_10 ran the same)."""
    return 6


def entries_of(graph, names=None):
    out_ = [e for e in V3 if e['graph'] == graph and (names is None or name_of(e) in names)]
    if names is not None:
        assert sorted(name_of(e) for e in out_) == sorted(names), (names, [name_of(e) for e in out_])
    return out_


def family_graph(graph):
    """the family's GraphIV: the edges of the list's columns (m3_graph_v3.strip) and the union of its entries' pair forms (values do not
    depend on unused pairs). C-GRAPH-LIST: the pairs equal the list's and (V, edges, F) its shape_V_edges_F (PLANT-GRAPH-LIST)."""
    spec = LIST['graphs'][graph]
    V, E = GR.strip(spec['columns'])
    prs = set()
    for e in V3:
        if e['graph'] == graph:
            for enc in e['factors']:
                prs |= {tuple(sorted(p)) for p in ENT.pairs_of(ENT.factor(TS, EDGES[graph], enc))}
    g = GR.GraphIV(V, E, sorted(prs), NN)
    want = sorted(tuple(sorted(p)) for p in spec['pairs'])
    got = sorted(tuple(sorted(p)) for p in g.pairs)
    shape = tuple(spec['shape_V_edges_F'])
    gate('C-GRAPH-LIST', got == want and (g.V, len(g.edges), g.F) == shape, '(%s: the columns %s give V %d, %d edges and F %d (the list: '
         '%s); pairs %s equal the list\'s)' % (graph, spec['columns'], g.V, len(g.edges), g.F, list(shape), got))
    plant('PLANT-GRAPH-LIST', got[1:] != want, '(%s: the pair list without its first pair)' % graph)
    return g


def ref_files(graph):
    """c3: the family's float twin output with its KEYJSON lines (pk22's m3ref_px22_v1_5, the piece with P16-DONE)."""
    return [os.path.join(OUTD, KEYREF[graph])]


def ref_prep(graph):
    """c3: the PREPJSON whose radii and theta0 the family's prep takes: its own twin's; CS4 and H4T pk03's P16S4 and P16H."""
    return read_lines(PREPREF[graph], 'PREPJSON')[0]


def make_prep(graph, g, scalars=None, d16=None):
    """C-RULE (PLANT-RULE), the family's prep without stages, C-TILT and C-PREP-REF. With a D16 context (the prep pieces): m3_bar_v11's
    Prep16, whose stages the piece then runs; without (smoke, entry and resume items): v10's Prep at dmaxH 16 on the restored scalars,
    whose bound the item runs. Both on the one kernel K."""
    rp = ref_prep(graph)
    mid = [(S.up(gv) + S.down(gv)) / 2 for gv in g.Gvv]
    want = [min(RULE[0] * m / 300, RULE[1]) for m in mid]
    drule = max([abs(a - w) / w for a, w in zip(rp['a_v'], want)] + [abs(rp['ap'] - RULE[2] ** 2) / RULE[2] ** 2])
    gate('C-RULE', len(want) == len(rp['a_v']) and drule <= 1e-12, '(%s: the reference radii^2 = min(%g G_vv/300, %g) and rho\'^2 = %g^2, '
         'G_vv the certified mids: max relative difference %.1e (tol 1e-12))' % (graph, RULE[0], RULE[1], RULE[2], drule))
    bad = [min(1.01 * RULE[0] * m / 300, 1.01 * RULE[1]) for m in mid]
    plant('PLANT-RULE', not (max(abs(a - w) / w for a, w in zip(rp['a_v'], bad)) <= 1e-12), '(%s: 80 and 0.6 times 1.01)' % graph)
    if d16 is not None:
        pr = BAR.Prep16(K, g, 300, rp['a_v'], rp['ap'], rp['theta0'], 6, d16, log=out, stages=(), scalars=scalars)
    else:
        pr = BAR.Prep(K, g, 300, rp['a_v'], rp['ap'], rp['theta0'], 6, log=out, dmaxH=16, stages=(), scalars=scalars)
    encl = [-iv.log(1 - S.I(a)) / (2 * S.I(a)) * (1 / S.I(300)) for a in rp['a_v']]
    gate('C-TILT', pr.ok and all(S.I(r) >= x.b for r, x in zip(pr.rates, encl)),
         '(a) %d tilt rates rounded up from their mp.iv enclosures; (b) both tilts certainly positive definite (lowest pivots %s, %s)' % (
             len(pr.rates), None if not pr.tilt_c else S.down(pr.tilt_c['low']), None if not pr.tilt_p else S.down(pr.tilt_p['low'])))
    gate('C-PREP-REF', rp['family'] == FAMREF[graph] and rp['N'] == NN and rp['J'] == 300, '(%s: %s PREPJSON of family %s, N %r, J %r)' % (
        graph, os.path.basename(PREPREF[graph]), rp['family'], rp['N'], rp['J']))
    return pr, rp


def c_odd16(graph, facs):
    """C-ODD on the family's own graph: T <-> B (m3_entries_v3.sigma) is an automorphism of the couplings of m3_graph_v3.strip(the
    list's columns), every factor is exactly even or odd (m3_entries_v3.parity_class) and exactly one is odd. m3_entries_v3.c_odd reads
    its edges from its own graph names, which have no H or S4. Returns (ok, reason)."""
    V, E = GR.strip(LIST['graphs'][graph]['columns'])
    if not ENT.edges_map_onto(E, ENT.sigma):
        return False, 'T <-> B is not an automorphism of the couplings of %s' % graph
    cls = [ENT.parity_class(f) for f in facs]
    if any(c is None for c in cls):
        return False, 'a factor is neither exactly even nor exactly odd: %s' % cls
    if cls.count('odd') != 1:
        return False, '%d odd factors' % cls.count('odd')
    return True, 'one exactly odd factor, the rest exactly even, T <-> B an automorphism of %s' % graph


def parity_set():
    """c3, C-PARITY-SET by entry id (family:key): the entries whose factors pass c_odd16 are exactly PARITY_ZERO (empty in the c3
    list), and V3 marks exactly those 'zero'. PLANT-ODD: the factor set [cp, 2, 0] alone on E4D (the odd trial state on a T <-> B
    symmetric graph) passes c_odd16, and from a copy of the trial set with S[1][2] + 1e-12 it must fail."""
    import copy
    passing = sorted(e['id'] for e in V3 if c_odd16(e['graph'], [ENT.factor(TS, EDGES[e['graph']], enc) for enc in e['factors']])[0])
    marked = sorted(e['id'] for e in V3 if e['parity'] == 'zero')
    gate('C-PARITY-SET', passing == sorted(PARITY_ZERO) and marked == sorted(PARITY_ZERO), '(the entries whose factors pass C-ODD on their own '
         'graph: %s; marked zero: %s; PARITY_ZERO %s)' % (passing, marked, sorted(PARITY_ZERO)))
    ok0, why0 = c_odd16('L', [ENT.factor(TS, EDGES['L'], ['cp', 2, 0])])   # pk23 hl_v1: on L
    gate('C-ODD-PLANT-BASE', ok0, '(hl_v1: [cp, 2, 0] alone on L passes C-ODD: %s)' % why0)
    ts2 = copy.deepcopy(TS)
    ts2.S[1][2] = ts2.S[1][2] + 1e-12
    ok, why = c_odd16('L', [ENT.factor(ts2, EDGES['L'], ['cp', 2, 0])])   # pk23 hl_v1
    plant('PLANT-ODD', not ok, '([cp, 2, 0] on L with S[1][2] + 1e-12: %s)' % why)


def laws_of(pr, mF):
    """U3's laws (PLAN_M3_CODE_v1_2 sect. C) and Lemma U's far rate (lower end) for an entry with J-degree m_F."""
    g = pr.g
    cF = mF + Fraction(g.n * (g.V - 1), 2)
    rate = pr.alpha_lo - S.I(cF) / 300
    return {'rem_tpow': 4, 'tail': {'n': g.n, 'J_REF': 300, 'a_G': [[a, S.up(gv)] for a, gv in zip(pr.a_v, g.Gvv)]},
            'ann': {'n': g.n, 'J_REF': 300, 'a_G': [[a, S.up(gv)] for a, gv in zip(pr.a_v, pr.tilt_p['Gvv'])]},
            'far_rate': S.down(rate), 'far_cF': str(cF)}, rate


def compute_entry(pr, e, state=None):
    """one entry: (result dict for the hand-off). Parity zeros: C-ODD and a_k balls containing 0, no bars."""
    name = name_of(e)
    facs = [ENT.factor(TS, EDGES[e['graph']], enc) for enc in e['factors']]
    pr.qcap = qcap_of(e)
    pr.maxrel = 0.0
    t0 = cpu()
    STAGE[0] = 'entry %s' % name
    if e['parity'] == 'zero':
        ok, why = c_odd16(e['graph'], facs)   # m3_run_v1_9: C-ODD on the family's own graph
        gate('C-ODD', ok, '%s: %s' % (name, why))
        ak, _, info = pr.bound(facs, e.get('grouping', 'std'), bars=False, entry=name, state=state)
        has0 = all(a.a <= 0 <= a.b for a in ak)
        gate('C-ODD-AK', has0, '%s: every a_k ball contains 0 (widest %.1e)' % (name, max(float((a.b - a.a).b) for a in ak)))
        out('STAGE-CPU entry %s %.2f s (parity zero)%s' % (name, cpu() - t0, resumed(state)))
        return {'name': name, 'parity': 'zero', 'ak': ak, 'qcap': pr.qcap, 'cpu': cpu() - t0}
    ak, bars, info = pr.bound(facs, e.get('grouping', 'std'), entry=name, state=state)
    laws, rate = laws_of(pr, info['mF'])
    gate('C-MONO-FAR', rate.a > 0, '%s: far rate alpha_min - (m_F + n(V-1)/2)/J_REF = %.4e > 0 (m_F %d)' % (name, S.down(rate), info['mF']))
    a0 = 1 if all(f[0] == 'p' for f in facs) else None
    rec = REC.entry_record(ak, bars, T_REF, 'free', a0_exact=a0, laws=laws)
    barsum = rec['Bp']['rem'] + rec['Bp']['tail'] + rec['Bp']['ann'] + rec['Bp']['far']
    okb = pr.maxrel <= 1e-3 and rec['B']['rnd'] <= 0.1 * barsum
    gate('C-BUDGET', okb, '%s: largest relative radius of a norm %.1e (<= 1e-3), rnd %.2e <= 0.1 x bar %.3e' % (name, pr.maxrel, rec['B']['rnd'], barsum))
    out('AKRAD-INFO %s: largest relative radius of an a_k %.2e' % (name, info.get('ak_relrad', 0.0)))
    out('ENTRY %s ak %s err %.9e parts rem %.9e tail %.9e ann %.9e far %.9e rnd %.3e groups %d Dn %d forms %d' % (
        name, ['%.12g' % x for x in rec['ak']], rec['err'], rec['B']['rem'], rec['B']['tail'], rec['B']['ann'], rec['B']['far'], rec['B']['rnd'],
        info['groups'], info['Dn'], len(info['forms'])))
    out('STAGE-CPU entry %s %.2f s%s' % (name, cpu() - t0, resumed(state)))
    return {'name': name, 'parity': 'free', 'ak': ak, 'bars': bars, 'a0_exact': a0, 'laws': laws, 'qcap': pr.qcap,
            'maxrel': pr.maxrel, 'cpu': cpu() - t0}


def plant_mono(pr):
    """PLANT-MONO: with theta0 = 1e-3 the far rate must not be certainly positive."""
    g = pr.g
    alpha = min((S.I(1e-3) * S.I(pr.ap) / (2 * gv)).a for gv in g.Gvv)
    rate = alpha - S.I(Fraction(g.n * (g.V - 1), 2)) / 300
    plant('PLANT-MONO', not (rate.a > 0), '(theta0 = 1e-3: far rate %.3e)' % S.down(rate))


def header(fam):
    return {'script': SELF_SHA, 'item': ITEM, 'family': fam, 'N': NN, 'kernel': '%s:%s' % (KERNEL, KFILES[KERNEL + '.py'][:8]),
            'arb_kernel': '%s:%s' % (ARBK, KFILES[ARBK + '.py'][:8]), 'trial': TRIAL, 'format': 'm3_run_v1_9_3 hand-off'}


def same(x, y):
    """exact equality of hand-off values: intervals by their raw ends, containers recursively."""
    if hasattr(x, '_mpi_') or hasattr(y, '_mpi_'):
        return hasattr(x, '_mpi_') and hasattr(y, '_mpi_') and x._mpi_ == y._mpi_
    if isinstance(x, dict) and isinstance(y, dict):
        return set(map(str, x)) == set(map(str, y)) and all(same(x[k], y[str(k)] if str(k) in y else y[k]) for k in x)
    if isinstance(x, (list, tuple)) and isinstance(y, (list, tuple)):
        return len(x) == len(y) and all(same(a, b) for a, b in zip(x, y))
    return x == y


def write_handoff(fam, body):
    name = 'm3_run_v1_9_3_%s.json' % ITEM
    path, hsha = HO.write(name, header(fam), body)
    out('HANDOFF %s %s' % (name, hsha))
    with open(path) as fh:
        text = fh.read()
    hdr_rt, body_rt = HO.read_text(text, {'script': SELF_SHA, 'item': ITEM, 'N': NN})
    gate('C-HANDOFF-RT', same(body, body_rt), '(the hand-off decodes to exactly the values written)')
    for lab, refused in HO.plant_handoff(text, {'script': SELF_SHA, 'item': ITEM, 'N': NN}):
        plant('PLANT-HANDOFF', refused, '(%s tampered in memory)' % lab)
    plant('PLANT-VERDICT', HO.plant_verdict(valid_verdict()), '(a producer record whose VERDICT line extends %r must be refused)' % valid_verdict())


def read_handoff(item, fam):
    name = 'm3_run_v1_9_3_%s.json' % item
    hdr, body = HO.read(name, os.path.join(OUTD, 'm3_run_v1_9_3_%s.out' % item), {'script': item_sha(item), 'item': item, 'N': NN, 'family': fam},
                        valid_verdict())
    gate('C-HANDOFF', True, '(%s: producer record VERDICT lines exactly [%r], file sha256, END checksum, header)' % (name, valid_verdict()))
    return body


def memo_path(graph):
    """the family's E2 block memo at this N (JSONL, appended by Prep16's TableU before use)."""
    return os.path.join(OUTD, 'm3_run_v1_9_3_memo_%s_N%d.jsonl' % (graph, NN))


def item_state(item):
    """an item's state, as piece_state for the entry pieces: 'valid' (its hand-off exists; read_handoff checks it), 'capped' (no
    hand-off; the output's first line names this script and item, and its VERDICT lines are exactly [CAPPED]) or 'missing' (no output);
    anything else raises ValueError."""
    po = os.path.join(OUTD, 'm3_run_v1_9_3_%s.out' % item)
    ho = os.path.join(HANDD, 'm3_run_v1_9_3_%s.json' % item)
    if not os.path.exists(po):
        if os.path.exists(ho):
            raise ValueError('%s: a hand-off without its producer output' % item)
        return 'missing'
    if os.path.exists(ho):
        return 'valid'
    with open(po) as fh:
        lines = fh.read().split('\n')
    m = re.fullmatch(r'm3_run_v1_9_3 item (\S+) LIM ([0-9]+); script sha256 ([0-9a-f]{64}); python (\S+)', lines[0])
    if m and m.group(1) == item and m.group(3) == item_sha(item) and HO.verdict_ok(lines, CAPPED):   # c3: item_sha
        return 'capped'
    raise ValueError('%s: an output without a hand-off that is not a clean CAP-STOP of this script' % item)


def memo_head(mp, nlines):
    """(the sha256 of the memo's first nlines lines as bytes, its lines after them); the file must hold at least nlines lines."""
    with open(mp, 'rb') as fh:
        lines = fh.read().split(b'\n')
    if lines and lines[-1] == b'':
        lines = lines[:-1]
    if len(lines) < nlines:
        raise ValueError('%s holds %d lines, fewer than the %d recorded' % (os.path.basename(mp), len(lines), nlines))
    return hashlib.sha256(b''.join(x + b'\n' for x in lines[:nlines])).hexdigest(), lines[nlines:]


def prep_state(graph, piece):
    """C-CACHE-CHAIN with PLANT-CACHE: piece K reads the last valid prep piece j < K (capped pieces skipped; j = 0, none: an empty state and
    no memo lines recorded). Piece j's hand-off has done false, and the memo's first memo_lines lines have the sha256 it recorded; lines
    after them are allowed only when a capped piece came after j, each read back by ma_scalar_load (adopted, INFO). Returns (piece j's
    prep state, the budget factor 1.25 x 2^(capped pieces after j), the adopted memo lines)."""
    mp = memo_path(graph)
    caps, j = 0, 0
    for jj in range(piece - 1, 0, -1):
        st = item_state('%sp%d.%d' % (PFX[graph], jj, NN))
        if st == 'capped':
            caps += 1
            continue
        if st != 'valid':
            raise ValueError('%sp%d.%d is %s, so prep piece %d cannot start' % (PFX[graph], jj, NN, st, piece))
        j = jj
        break
    if j:
        body = read_handoff('%sp%d.%d' % (PFX[graph], j, NN), graph)
        state, nrec, hrec, done = body['state'], body['memo_lines'], body['memo_head_sha'], body['done']
    else:
        state, nrec, hrec, done = {}, 0, hashlib.sha256(b'').hexdigest(), False
    if os.path.exists(mp):
        h, extra = memo_head(mp, nrec)
    else:
        h, extra = (hashlib.sha256(b'').hexdigest(), []) if nrec == 0 else ('missing', [])
    for x in extra:
        d = json.loads(x.decode())
        K.ma_scalar_load(d['v'])
    gate('C-CACHE-CHAIN', done is False and h == hrec and (not extra or caps > 0), '(%s prep piece %d: %s; memo %s: its first %d lines have '
         'sha256 %s (recorded %s), %d lines after them from %d capped piece(s), each read back by ma_scalar_load)' % (
             graph, piece, ('piece %d\'s hand-off, done %r' % (j, done)) if j else 'no valid prep piece before it', os.path.basename(mp), nrec,
             h[:8], hrec[:8], len(extra), caps))
    plant('PLANT-CACHE', h != flip(hrec), '(the memo head against its recorded sha256 with the last digit changed)')
    return state, 1.25 * 2 ** caps, len(extra)


def prep_final(graph):
    """C-PREP-CHAIN: the family's valid prep pieces, capped ones skipped, have done false up to the last, which has done true (each
    hand-off bound to its producer output); returns that hand-off (the scalars of both stages)."""
    seen = []
    for k in range(1, MAXPP + 1):
        st = item_state('%sp%d.%d' % (PFX[PREPOF[graph]], k, NN))
        if st == 'capped':
            continue
        if st == 'missing':
            break
        body = read_handoff('%sp%d.%d' % (PFX[PREPOF[graph]], k, NN), PREPOF[graph])   # c3: PREPOF
        if body['piece'] != k:
            break
        if body['done']:
            gate('C-PREP-CHAIN', True, '(%s: prep pieces %s with done false, piece %d done)' % (graph, seen or 'none', k))
            return body
        seen.append(k)
    gate('C-PREP-CHAIN', False, '(%s: no finished prep piece in order; valid pieces %s)' % (graph, seen))
    raise ValueError('%s: no finished prep piece in order' % graph)


def resumed(state):
    return (' (this piece; %d units of the entry restored)' % len(state['vals'])) if state else ''


def run_resume(graph, part):
    """Xr1 (part 1) and Xr2 (part 2): C-RESUME on RESUME_KEY[graph] after the entry pieces, against the entry as the record will have it
    (the pieces' hand-offs through walk_pieces, as asm reads them), on v10's Prep with the finished prep's scalars. m3_run_v1_8_3's
    check_resume (m3_bar_v8's C-RESUME), split so that each item is about two entry runs:
      part 1: the checkpoint after stage a (the units 'ak', 'm0u', 'm0c') through a hand-off encode/decode round trip, resumed with fresh
              table and group caches, must give the record's a_k and bars exactly (C-RESUME); PLANT-RESUME: that state with m0u doubled
              must change the bars;
      part 2: a straight run (C-RESUME-SAME: exactly the record's a_k and bars, which also gives the unit order), then the checkpoint
              before the first stage-c unit, through the round trip and resumed the same way (C-RESUME).
    The hand-off holds the outcome for asm's C-RESUME-CHAIN."""
    stage('%s resume part %d' % (graph, part))
    if graph not in RESUME_FAMS:
        raise ValueError('%s is not in RESUME_FAMS %s' % (graph, RESUME_FAMS))
    res = {}
    walk_pieces(graph, res)
    fin = prep_final(graph)
    g = family_graph(graph)
    pr, rp = make_prep(graph, g, scalars=dict(fin['scal_u'], **fin['scal_c']))
    prep_share(graph)   # c3
    e = entries_of(graph, [RESUME_KEY[graph]])[0]
    name = name_of(e)
    src = res[(graph, name)]
    facs = [ENT.factor(TS, EDGES[graph], enc) for enc in e['factors']]
    gr = e.get('grouping', 'std')
    pr.qcap = qcap_of(e)

    def run(state=None, cut=None):
        pr.tables, pr.gcache, pr.maxrel = {}, {}, 0.0
        cnt = [0]
        if cut is not None:
            pr.unit_done = lambda dt, prog: cnt.__setitem__(0, cnt[0] + (1 if prog else 0))
            pr.ubudget = lambda: cnt[0] < cut
        try:
            return pr.bound(facs, gr, entry=name, state=state), None
        except BAR.Checkpoint as cp:
            return None, HO.dec(json.loads(json.dumps(HO.enc(cp.state))))
        finally:
            pr.ubudget = pr.unit_done = None
    body = {'family': graph, 'part': part, 'entry': name}
    if part == 1:
        t0 = cpu()
        _, st = run(cut=3)
        keys = list(st['vals']) if st else []
        r1, _ = run(state=st) if st else (None, None)
        ok = keys == ['ak', 'm0u', 'm0c'] and r1 is not None and same(src['ak'], r1[0]) and same(src['bars'], r1[1])
        gate('C-RESUME', ok, '(%s part 1: cut after stage a, units %s, resumed with fresh caches: a_k and bars %s the record\'s; %.2f s)' % (
            name, keys, 'identical to' if ok else 'NOT identical to', cpu() - t0))
        r2 = None
        if st:
            bad = dict(st, vals=dict(st['vals']))
            bad['vals']['m0u'] = 2 * bad['vals']['m0u']
            r2, _ = run(state=bad)
        fired = r2 is not None and not same(src['bars'], r2[1])
        plant('PLANT-RESUME', fired, '(%s: the stage-a state with m0u doubled must change the bars; rem %s -> %s)' % (
            name, '%.9e' % S.up(src['bars']['rem']), ('%.9e' % S.up(r2[1]['rem'])) if r2 else 'no result'))
        body.update({'cut': keys, 'resume_ok': ok, 'plant_fired': fired})
    else:
        t0 = cpu()
        (ak0, b0, _), _ = run()
        seq = list(pr.ustate['vals'])
        oks = same(src['ak'], ak0) and same(src['bars'], b0)
        gate('C-RESUME-SAME', oks, '(%s straight, %d units, %.2f s: a_k and bars %s the record\'s)' % (
            name, len(seq), cpu() - t0, 'identical to' if oks else 'NOT identical to'))
        cutb = next(i for i, k in enumerate(seq) if k.endswith('|c'))
        t0 = cpu()
        _, st = run(cut=cutb)
        r3, _ = run(state=st) if st else (None, None)
        ok = st is not None and len(st['vals']) == cutb and r3 is not None and same(src['ak'], r3[0]) and same(src['bars'], r3[1])
        gate('C-RESUME', ok, '(%s part 2: cut after %d of %d units, before the first stage-c unit, resumed with fresh caches: a_k and bars %s '
             'the record\'s; %.2f s)' % (name, cutb, len(seq), 'identical to' if ok else 'NOT identical to', cpu() - t0))
        body.update({'cut': cutb, 'units': len(seq), 'resume_ok': ok and oks})
    pr.tables, pr.gcache, pr.maxrel = {}, {}, 0.0
    body['fallbacks'] = fb_info()
    write_handoff(graph, body)


def prep16_rep(graph, pr, rp, stg):
    """PREP16-REP (INFO, the measurement step's numbers): a finished stage's scalars against the float twin's PREPJSON, upper end / float."""
    keys = {'u': ('rE', 'rE_parts', 'nE', 'nE4'), 'c': ('nC8', 'nC6', 'Pout', 'Pout_p', 'farbase')}[stg]
    rows = []
    for k in keys:
        for lab, x in iv_leaves(getattr(pr, k)):
            f = rp[k]
            for part in [p for p in re.findall(r'\[([^\]]*)\]', lab)]:
                f = f[int(part)] if isinstance(f, list) else f[part]
            if isinstance(f, (int, float)) and f > 0:
                rows.append((S.up(x) / f, k + lab))
    rows.sort()
    if not rows:
        out('PREP16-REP %s stage %s: no scalar with a positive float value' % (graph, stg))
        return
    out('PREP16-REP %s stage %s: %d scalars, certified upper end / float in [%.6f (%s), %.6f (%s)]; %s' % (
        graph, stg, len(rows), rows[0][0], rows[0][1], rows[-1][0], rows[-1][1], '; '.join('%s %.6f' % (lab, r) for r, lab in rows)))


def iv_leaves(v, lab=''):
    """the (label, interval) leaves of a scalar container: dicts by sorted key, lists by index."""
    if isinstance(v, dict):
        return sum((iv_leaves(v[k], '%s[%s]' % (lab, k)) for k in sorted(v, key=str)), [])
    if isinstance(v, (list, tuple)):
        return sum((iv_leaves(x, '%s[%d]' % (lab, i)) for i, x in enumerate(v)), [])
    return [(lab, v)]


def prep_graph(g):
    """m3_run_v1_9_2: the graph the prep pieces build Prep16 on: GraphIV(V, E, [], N, S_gauge)
    with the family graph g's V, N, edge list (pairs and tags, in order) and S_gauge, so F = V and the prep's polynomials pack in int64
    codes (m3_run_v1_9_1's S4p1.4 stopped at the kernel's _code_guard, 10^19 >= 2^63 at F 19). prep_same checks it (C-PREP-GRAPH)."""
    return GR.GraphIV(g.V, list(g.edges), [], g.N, list(g.S_gauge))


def prep_view(G, pr):
    """what the prep reads of a graph object, for C-PREP-GRAPH: (the inputs V, N, S_gauge and the edge list with tags in order; C-1's
    values: the V x V vertex block of Gam, G_vv, log_tau, log_det_Lr, W_int's vertex columns, and at the prep's rate vectors pr.rates and
    pr.ratesp the vertex block of tilted()'s 'Gam', its 'Gvv' and its 'N'; C-4's values: Pout, Pout_p, tree(), farbase and alpha_lo,
    formed as Prep.stage_c and Prep16.stage_c16 form them from pr's J, radii, theta0 and rho'^2). m3_run_v1_9_3: a graph whose C-4 values
    are not finite (a plant's: S_gauge [0] makes vertex 0's G_vv exactly 0) gets the text 'not formed (<error>)' in their place."""
    V = G.V
    vb = lambda M: [list(r[:V]) for r in M[:V]]
    tl = lambda T: None if T is None else {'Gam': vb(T['Gam']), 'Gvv': list(T['Gvv']), 'N': T['N']}
    tc, tp = G.tilted(pr.rates), G.tilted(pr.ratesp)
    ins = {'V': G.V, 'N': G.N, 'S_gauge': list(G.S_gauge), 'edges': [(tuple(e), c) for e, c in G.edges]}
    c1 = {'Gam': vb(G.Gam), 'Gvv': list(G.Gvv), 'log_tau': G.log_tau, 'log_det_Lr': G.log_det_Lr, 'W_int': [list(r[:V]) for r in G.W_int],
          'tilt_c': tl(tc), 'tilt_p': tl(tp)}
    c4 = None
    if tp is not None:
        th, ap = S.I(pr.theta0), S.I(pr.ap)
        try:   # m3_run_v1_9_3
            tree = G.tree()
            c4 = {'Pout': S.isum(S.chi_tail_up(pr.J * S.I(a) / gv, G.n) for a, gv in zip(pr.a_v, G.Gvv)),
                  'Pout_p': S.isum(S.chi_tail_up(pr.J * S.I(a) / gv, G.n) for a, gv in zip(pr.a_v, tp['Gvv'])),
                  'tree': tree, 'farbase': S.far_base(pr.J, th, ap, G.Gvv, tree, G.N, G.V, G.log_tau),
                  'alpha_lo': min((th * ap / (2 * gv)).a for gv in G.Gvv)}
        except (ArithmeticError, ValueError) as ex:
            c4 = 'not formed (%s)' % type(ex).__name__
    return ins, c1, c4


VIEW_PARTS = ('inputs', 'C-1 values', 'C-4 values')


def view_diff(a, b):
    """the parts of two prep_views that differ: the inputs by ==, the values by their raw interval ends (same(): equal _mpi_ tuples)."""
    return [n_ for n_, x, y in zip(VIEW_PARTS, a, b) if not same(x, y)]


def prep_same(graph, g, gp, pr):
    """C-PREP-GRAPH: the prep graph gp has no pair forms (pairs [] and F = V), and its
    prep_view equals the family graph g's exactly, at the rate vectors of the prep pr, with both views' C-4 values formed (m3_run_v1_9_3).
    The plants (C-2), each must make that comparison fail: the graph with its first edge dropped (PLANT-PREP-EDGE), with its first edge's
    tag changed ('A' to 'B', else to 'A'; PLANT-PREP-TAG), with S_gauge [0] (PLANT-PREP-GAUGE), and a copy of gp's view whose
    vertex-block entry [0][1] has each raw end moved up by one unit of its last bit (PLANT-PREP-ULP: the moved entry still overlaps the
    original, so only an endpoint-exact test refuses it)."""
    import types
    vg, vp = prep_view(g, pr), prep_view(gp, pr)
    d0 = view_diff(vg, vp)
    formed = isinstance(vg[2], dict) and isinstance(vp[2], dict)
    ok = gp.pairs == [] and gp.F == gp.V and formed and not d0
    gate('C-PREP-GRAPH', ok, '(%s: the prep graph has V %d, F %d and pairs %r (the family graph: F %d); against the family graph, V, N, '
         'S_gauge and the %d edges with tags in order equal, and exactly (equal _mpi_ tuples) the %d x %d vertex block of Gam, %d G_vv, '
         'log_tau, log_det_Lr, W_int\'s vertex columns and tilted()\'s vertex Gam, G_vv and N at both rate vectors (C-1), and Pout, Pout_p, '
         'tree(), farbase and alpha_lo (C-4)%s%s)' % (graph, gp.V, gp.F, gp.pairs, g.F, len(g.edges), g.V, g.V, len(g.Gvv),
                                                      ('; differ: ' + ', '.join(d0)) if d0 else '',
                                                      '' if formed else '; C-4 values of the family and prep graphs: %r, %r' % (
                                                          vg[2] if not isinstance(vg[2], dict) else 'formed',
                                                          vp[2] if not isinstance(vp[2], dict) else 'formed')))
    E, S0 = list(g.edges), list(g.S_gauge)
    t1 = 'B' if E[0][1] == 'A' else 'A'
    for lab, what, gx in (('PLANT-PREP-EDGE', 'its first edge %r dropped' % (E[0],), GR.GraphIV(g.V, E[1:], [], g.N, S0)),
                          ('PLANT-PREP-TAG', 'its first edge\'s tag %r changed to %r' % (E[0][1], t1),
                           GR.GraphIV(g.V, [(E[0][0], t1)] + E[1:], [], g.N, S0)),
                          ('PLANT-PREP-GAUGE', 'S_gauge [0]', GR.GraphIV(g.V, E, [], g.N, [0]))):
        dx = view_diff(vg, prep_view(gx, pr))
        plant(lab, bool(dx), '(%s: the prep graph with %s, against the family graph: differs in %s)' % (graph, what, ', '.join(dx) or 'nothing'))
    x = vp[1]['Gam'][0][1]
    mv = types.SimpleNamespace(_mpi_=tuple(libmp.mpf_add(r, libmp.from_man_exp(1, r[2]), 0) for r in x._mpi_))
    (a0, b0), (a1, b1) = [_ef(r) for r in x._mpi_], [_ef(r) for r in mv._mpi_]
    c1m = dict(vp[1], Gam=[list(r) for r in vp[1]['Gam']])
    c1m['Gam'][0][1] = mv
    dx = view_diff(vg, (vp[0], c1m, vp[2]))
    lap = a1 <= b0 and a0 <= b1
    plant('PLANT-PREP-ULP', bool(dx) and lap, '(%s: a copy of the prep graph\'s view with its vertex-block entry [0][1] moved up by one unit '
          'of each end\'s last bit (overlapping the original: %s), against the family graph: differs in %s)' % (graph, lap, ', '.join(dx) or 'nothing'))


def prep_share(graph):
    """c3, C-PREP-SHARE: a family whose prep is another family's (PREPOF; CS4 reads c1's S4 prep, H4T pk03's H prep) has that
    family's prep graph: the vertex-only graphs (prep_graph) of its own graph and of LISTS8's graph of that family (LISTC3's for CE3;
    c3h_1) agree in V, N,
    S_gauge, the edges with their tags in order and the (empty) pairs; and the float twins' PREPJSON lines, the family's own (ref_files)
    and the one the shared prep took (ref_prep), agree: radii, rho'^2 and theta0 exactly, rE, nC8, nC6, Pout, Pout_p and farbase to
    1e-12 relative. PLANT-PREP-SHARE: the family's prep graph with its first edge dropped must differ. A family with its own prep:
    nothing."""
    pf = PREPOF[graph]
    if pf == graph:
        return
    spec = (LISTC3 if pf == 'CE3' else LISTS8)['graphs'][pf]   # c3h: CE3's graph is in c3's list
    V0, E0 = GR.strip(spec['columns'])
    p0 = prep_graph(GR.GraphIV(V0, E0, sorted(tuple(sorted(p)) for p in spec['pairs']), NN))
    p1 = prep_graph(family_graph(graph))
    ins = lambda G: (G.V, G.N, list(G.S_gauge), [(tuple(e), c) for e, c in G.edges], list(G.pairs))
    okg = ins(p0) == ins(p1)
    a = read_lines(ref_files(graph)[0], 'PREPJSON')[0]
    b = ref_prep(graph)
    ex = all(a[k] == b[k] for k in ('a_v', 'ap', 'theta0'))
    rel = max(abs(a[k] - b[k]) / abs(b[k]) for k in ('rE', 'nC8', 'nC6', 'Pout', 'Pout_p', 'farbase'))
    gate('C-PREP-SHARE', okg and ex and rel <= 1e-12, '(%s reads %s\'s prep (pinned): the prep graphs of %s and of %s\'s %s '
         'agree in V, N, S_gauge, edges with tags and pairs: %s; float twins %s and %s: radii, rho\'^2 and theta0 equal: %s, prep scalars '
         'within %.1e relative)' % (graph, pf, graph, 'C3_ENTRY_LIST_v2' if pf == 'CE3' else 'S8_ENTRY_LIST_v2', pf, okg,   # c3h_1
                                    os.path.basename(ref_files(graph)[0]), os.path.basename(PREPREF[graph]), ex, rel))
    pb = GR.GraphIV(p1.V, list(p1.edges)[1:], [], p1.N, list(p1.S_gauge))
    plant('PLANT-PREP-SHARE', ins(pb) != ins(p0), '(%s\'s prep graph with its first edge dropped, against %s\'s)' % (graph, pf))


PACK_LIM = 9 * 10 ** 18   # the strictest table encoder: arbeng_c2b_v2's AllMom2A asserts float(D + 1)^F < 9.0e18 (the layer's _code_guard: 2^63)


def pack_ok(forms, D, lp):
    """C-PACK-PLAN's test of one table request: the code range (D + 1)^forms below PACK_LIM in exact integers (so below the layer's
    _code_guard bound 2^63 and the arb fallback's 9.0e18), and D <= 64 for an lp norm (Prep.lp_norm returns None above its dmax 64)."""
    return (D + 1) ** forms < PACK_LIM and (not lp or D <= 64)


def pack_plan(pr, facs, grouping, info, bars):
    """m3_run_v1_9_2, C-PACK-PLAN's requests for one entry: every moment table Prep.bound asks the kernel for at this entry, as (what,
    forms, D, lp), distinct, from the polynomials the smoke built (pr's group cache); no table is built here. A table packs its monomials
    in int64 codes of base D + 1 over its forms (the layer's MomTable and the arb fallback's AllMom2A), and the powers and products inside
    its moments stay within that base. The requests: the a_k table (D = max(Dn, 1) over the entry's forms; the smoke built it); for a free
    entry also m0u and m0c (D = max(2 deg F_0, 1) over the same forms) and every group norm of the bars, each on its polynomial's support:
    'ser' i_g at p = 2G for the compositions of i = 1, 2, 3 and at p = 4G for nF4c's i = 0 (lp_norm: D = 2 deg x (p // 2)), 'bar' j_g at
    p = G for the compositions of 4 (pos_norm: D = deg x p) and 'barp' at p = 2G (lp_norm), G = max(groups, 1). A polynomial's support
    size and deg are read from its exponent rows P.ex (the keys of P.to_arb_dict(), which m3_bar_v11's support and deg read), once per
    polynomial; restricted to its own support it keeps its deg."""
    import numpy as np
    use = info['forms']
    reqs = [('a_k', len(use), max(info['Dn'], 1), False)]
    if not bars:
        return reqs
    scal, groups = BAR.group_factors(facs) if grouping == 'std' else BAR.split_groups(facs)
    G_ = max(len(groups), 1)
    gds = [pr.gdata(gf) for gf in groups]
    d0 = 2 * BAR.deg(pr.series_product([d['ser'] for d in gds], scal, 0)[0]) if groups else 0
    reqs.append(('m0u m0c', len(use), max(d0, 1), False))
    shape = {}

    def req(lab, P, p, pos):
        if id(P) not in shape:
            shape[id(P)] = (int(np.count_nonzero(P.ex.any(axis=0))), int(P.ex.sum(axis=1).max())) if len(P.ex) else (0, 0)
        nf, dq = shape[id(P)]
        r = (lab, nf, dq * p if pos else 2 * dq * (p // 2), not pos)
        if nf and r not in reqs:
            reqs.append(r)
    for i in (1, 2, 3):
        for c in BAR.comps(i, len(groups)):
            for gi, ig in enumerate(c):
                req('group %d ser %d p %d' % (gi, ig, 2 * G_), gds[gi]['ser'][ig], 2 * G_, False)
    for c in BAR.comps(0, len(groups)):
        for gi, ig in enumerate(c):
            req('group %d ser %d p %d' % (gi, ig, 4 * G_), gds[gi]['ser'][ig], 4 * G_, False)
    for c in BAR.comps(4, len(groups)):
        for gi, jg in enumerate(c):
            req('group %d bar %d p %d' % (gi, jg, G_), gds[gi]['bar'][jg], G_, True)
    for gi in range(len(gds)):
        req('group %d barp p %d' % (gi, 2 * G_), gds[gi]['barp'], 2 * G_, False)
    return reqs


def pack_gate(graph, plans):
    """C-PACK-PLAN over all of a family's entries (plans: [(entry, (what, forms, D, lp))]) with PLANT-PACK-PLAN (a request of D 16 over
    16 forms must be refused, and the control D 14 over 16 forms accepted)."""
    bad = [(nm, r) for nm, r in plans if not pack_ok(r[1], r[2], r[3])]
    nm, r = max(plans, key=lambda x: x[1][1] * math.log(x[1][2] + 1))
    lpm = max([x[1][2] for x in plans if x[1][3]] + [0])
    gate('C-PACK-PLAN', bool(plans) and not bad, '(%s: the bound of all %d entries asks the kernel for %d table requests, distinct within each '
         'entry; the largest code range (D + 1)^forms is %d^%d = %.3e (%s, %s), below %.1e; the largest lp-norm D is %d (<= 64))%s' % (
             graph, len(set(x[0] for x in plans)), len(plans), r[2] + 1, r[1], float(r[2] + 1) ** r[1], nm, r[0], PACK_LIM, lpm,
             (': refused ' + '; '.join('%s %s D %d over %d forms' % (x[0], x[1][0], x[1][2], x[1][1]) for x in bad[:10])) if bad else ''))
    plant('PLANT-PACK-PLAN', not pack_ok(16, 16, False) and pack_ok(16, 14, False), '(a request of D 16 over 16 forms, 17^16 = %.3e, must '
          'be refused, and the control D 14 over 16 forms, 15^16 = %.3e, accepted)' % (17.0 ** 16, 15.0 ** 16))


def run_prep16(graph, piece):
    """one prep piece: C-CACHE-CHAIN, the family graph (C-GRAPH-LIST), the prep graph without pair forms (prep_graph) and Prep16 on it
    with the last valid piece's state (C-PREP-GRAPH and its plants, prep_same, before any step), then stage u and stage c until both
    are done or the budget refuses a step (PrepCheckpoint). The hand-off holds the prep state, the memo's line count and head sha256, the
    piece's INFO (adopted and moved steps, E2 widths, tables' shadow_max) and, when done, both stages' scalars (PLANT-MONO then)."""
    stage('%s prep piece %d' % (graph, piece))
    state, factor, adopted_lines = prep_state(graph, piece)
    if FAILS:
        return
    g = family_graph(graph)
    gp = prep_graph(g)   # m3_run_v1_9_2: the prep on the vertex-only graph
    mp = memo_path(graph)
    if not os.path.isdir(TAB16):
        os.mkdir(TAB16)   # the tables' state directories go inside it (out/tab16c), kept

    def budget16(est, what):
        """a step of about est CPU seconds starts only if cpu + factor x est ends 40 s before LIM (the hand-off and the plants)."""
        return cpu() + factor * est <= LIM - 40
    ctx = BAR.D16Ctx(K, TAB16, mp, budget16, NS_UNIT, NS_E2, NS_FIN, BLOCK16, UNIT_PAIRS, E2_PAIRS, E2_MIN, state)
    pr, rp = make_prep(graph, gp, d16=ctx)
    prep_same(graph, g, gp, pr)   # m3_run_v1_9_2: C-PREP-GRAPH and its plants
    if FAILS:
        return
    out('PREP16-START %s piece %d: %d norms finished before, %d memo lines (%d adopted from capped pieces), budget factor %.2f' % (
        graph, piece, len(ctx.norms), ctx.memo_lines, adopted_lines, factor))
    done, why = False, ''
    try:
        pr.stage_u16()
        prep16_rep(graph, pr, rp, 'u')   # in every piece that gets past stage u (from the norm memo after the first): INFO only
        pr.stage_c16()
        done = True
        prep16_rep(graph, pr, rp, 'c')
    except BAR.PrepCheckpoint as cp:
        why = cp.why
    st = ctx.snapshot()
    nl = ctx.memo_lines
    hh = memo_head(mp, nl)[0] if os.path.exists(mp) else hashlib.sha256(b'').hexdigest()
    info = {'adopted': ctx.adopted, 'moved': ctx.moved, 'memo_hits': ctx.memo_hits, 'steps': ctx.steps, 'adopted_memo_lines': adopted_lines,
            'e2_rel': [ctx.e2_rel[0], ctx.e2_rel[1]], 'e2_trips': ctx.e2_trips, 'shadow': ctx.shadow, 'factor': factor}
    body = {'family': graph, 'piece': piece, 'done': done, 'why': why, 'state': st, 'memo_lines': nl, 'memo_head_sha': hh, 'info': info,
            'fallbacks': fb_info()}
    if done:
        body['scal_u'] = pr.scalars_out('u')
        body['scal_c'] = pr.scalars_out('c')
        plant_mono(pr)
        out('PREP %s N=%d: V %d, F %d, radii from %s, theta0 %r; rE %.6e nC8 %.6e nC6 %.6e farbase %.6e' % (
            graph, NN, gp.V, gp.F, os.path.basename(PREPREF[graph]), rp['theta0'], float(pr.rE.mid), float(pr.nC8.mid), float(pr.nC6.mid), float(pr.farbase.b)))
    tabs = ', '.join('%s %s' % (k[:20], ('finished %s' % v['handoff'][1][:8]) if v['handoff'] else '%d units' % len(v['units']))
                     for k, v in sorted(st['tables'].items()))
    out('PREP16 %s piece %d: %s; %d norms finished, memo %d lines (head sha256 %s); tables: %s; adopted %d, moved aside %d, memo hits %d; '
        'largest E2 relative radius %.3e at %s, %d over FALLBACK_REL; shadow_max %s' % (
            graph, piece, 'DONE' if done else 'PARTIAL before %s' % why, len(st['norms']), nl, hh[:8], tabs or 'none', ctx.adopted, ctx.moved,
            ctx.memo_hits, ctx.e2_rel[0], ctx.e2_rel[1], ctx.e2_trips, ', '.join('%s %.3e' % kv for kv in sorted(ctx.shadow.items())) or '-'))
    write_handoff(graph, body)


def order_of(graph):
    """a piece family's entries in the list's order (the resumable pieces walk it)."""
    return [name_of(e) for e in entries_of(graph)]


CAPPED = 'VERDICT INCOMPLETE (CAP-STOP)'


def piece_state(graph, piece):
    """'valid' (its hand-off exists; read_handoff checks it), 'capped' (no hand-off; the output's first line names this script and
    item, and its VERDICT lines are exactly [CAPPED]) or 'missing' (no output); anything else raises ValueError."""
    item = '%sk%d.%d' % (PFX[graph], piece, NN)
    po = os.path.join(OUTD, 'm3_run_v1_9_3_%s.out' % item)
    ho = os.path.join(HANDD, 'm3_run_v1_9_3_%s.json' % item)
    if not os.path.exists(po):
        if os.path.exists(ho):
            raise ValueError('%s: a hand-off without its producer output' % item)
        return 'missing'
    if os.path.exists(ho):
        return 'valid'
    with open(po) as fh:
        lines = fh.read().split('\n')
    m = re.fullmatch(r'm3_run_v1_9_3 item (\S+) LIM ([0-9]+); script sha256 ([0-9a-f]{64}); python (\S+)', lines[0])
    if m and m.group(1) == item and m.group(3) == SELF_SHA and HO.verdict_ok(lines, CAPPED):
        return 'capped'
    raise ValueError('%s: an output without a hand-off that is not a clean CAP-STOP of this script' % item)


def run_nk(graph, piece):
    stage('%s keys piece %d' % (graph, piece))
    order = order_of(graph)
    g = family_graph(graph)
    fin = prep_final(graph)   # m3_run_v1_9: the scalars of the family's finished prep (C-PREP-CHAIN)
    su, sc = fin['scal_u'], fin['scal_c']
    start, caps, partial = 0, 0, None
    for j in range(piece - 1, 0, -1):
        st = piece_state(graph, j)
        if st == 'capped':
            caps += 1
            continue
        if st != 'valid':
            raise ValueError('%sk%d.%d is %s, so piece %d cannot start' % (PFX[graph], j, NN, st, piece))
        prev = read_handoff('%sk%d.%d' % (PFX[graph], j, NN), graph)
        start, partial = prev['next'], prev['partial']
        break
    factor = 1.5 * 2 ** caps
    nin = len(partial['vals']) if partial else 0
    out('PIECE-START %s piece %d resumes at entry %d%s after %d capped piece(s); stop factor %.1f' % (
        graph, piece, start, (' with %d units of %s restored' % (nin, partial['entry'])) if partial else '', caps, factor))
    pr, rp = make_prep(graph, g, scalars=dict(su, **sc))   # m3_run_v1_9: v10's Prep on the restored scalars
    prep_share(graph)   # c3
    slow, units = [60.0], [0]

    def budget():
        return units[0] == 0 or cpu() + factor * slow[0] <= LIM - 20

    def done(dt, progress):
        slow[0] = max(slow[0], dt)
        if progress:
            units[0] += 1
    pr.ubudget, pr.unit_done = budget, done
    res, i, part = [], start, None
    while i < len(order):
        try:
            res.append(compute_entry(pr, entries_of(graph, [order[i]])[0], state=partial))
        except BAR.Checkpoint as cp:
            part = cp.state
            break
        partial = None
        i += 1
    pr.ubudget = pr.unit_done = None
    nout = len(part['vals']) if part else 0
    prog = i > start or (part is not None and nout > nin)
    gate('C-PIECE', prog, '(%s piece %d: entries %d..%d of %d done, next %d; %d units computed%s)' % (
        graph, piece, start, i - 1, len(order), i, units[0], (', %d units of %s carried' % (nout, part['entry'])) if part else ''))
    write_handoff(graph, {'family': graph, 'piece': piece, 'start': start, 'next': i, 'partial': part, 'stop_factor': factor,
                          'entries': res, 'fallbacks': fb_info()})


def write_records(texts, paths, fails, nofire, tag, opener=open):
    """for asm's records (texts and paths keyed alike): writes the record texts (open 'x', inside out/, no file
    there yet) only when no gate has failed, every plant so far has fired and the TAG is certified; returns [(key, path)] written, or []
    when it refuses."""
    if fails or nofire or tag != '':
        return []
    for f in paths:
        if os.path.dirname(os.path.abspath(paths[f])) != OUTD or os.path.exists(paths[f]):
            raise ValueError('record path %s: outside out/ or already there' % paths[f])
    done = []
    for f in sorted(paths):
        with opener(paths[f], 'x') as fh:
            fh.write(texts[f])
        done.append((f, paths[f]))
    return done


def walk_pieces(graph, res):
    """C-PIECES: the pieces of a family cover its entries in order, each advancing, none left in progress; their entries go into res."""
    order, nxt, piece, nin = order_of(graph), 0, 1, 0
    while nxt < len(order) and piece <= MAXP[graph]:
        st = piece_state(graph, piece)
        if st == 'missing':
            break
        if st == 'capped':
            out('PIECE-CAPPED %sk%d.%d: a clean CAP-STOP of this script, no hand-off; skipped and kept' % (PFX[graph], piece, NN))
            piece += 1
            continue
        body = read_handoff('%sk%d.%d' % (PFX[graph], piece, NN), graph)
        pt = body['partial']
        nout = len(pt['vals']) if pt else 0
        okp = body['start'] == nxt and (body['next'] > nxt or nout > nin) and (pt is None or (body['next'] < len(order) and pt['entry'] == order[body['next']]))
        gate('C-PIECES', okp, '(%sk%d.%d: entries %d..%d complete%s)' % (PFX[graph], piece, NN, body['start'], body['next'] - 1,
                                                                          (', %d units of %s carried' % (nout, pt['entry'])) if pt else ''))
        for r in body['entries']:
            res[(graph, r['name'])] = r
        nxt, piece, nin = body['next'], piece + 1, nout
    gate('C-PIECES', nxt == len(order) and nin == 0, '(the %s pieces cover all %d %s entries, in order, none left in progress)' % (
        graph, len(order), graph))


SMOKE_PARTS = {}   # pk23 hl_v1: every family's smoke is one item


def run_smoke(graph, part=None):
    """Xa, the smoke piece: C-PARITY-SET with PLANT-ODD; the family graph (C-GRAPH-LIST), its tilts and C-RULE against the float twin;
    m3_run_v1_9_2: C-PREP-GRAPH with its plants on the family's prep graph (prep_same); then the a_k of the family's entries without bars
    or prep scalars, each against the float twin's KEYJSON (C-SMOKE-AK, 1e-9 of max(1, |float|) as C-REP-AK), with PLANT-SMOKE-AK (the
    threshold) and PLANT-SMOKE-PATH (the family's first free entry with a xi factor whose c0 is 0, recomputed with that
    factor's c9 times 1 + 1e-6, must move its a_k past the threshold); m3_run_v1_9_2: C-PACK-PLAN with PLANT-PACK-PLAN, every moment table
    the bound of the family's entries asks the kernel for (pack_plan, from the polynomials built here; no such table is built) within the
    int64 code range of its encoder. No hand-off, no record."""
    stage('smoke %s' % graph)
    parity_set()
    g = family_graph(graph)
    pr, rp = make_prep(graph, g)
    prep_same(graph, g, prep_graph(g), pr)   # m3_run_v1_9_2
    prep_share(graph)   # c3
    refs = {d['key']: d for d in read_lines(ref_files(graph)[0], 'KEYJSON')}
    worst, n, path, plans = (0.0, '-', 0), 0, None, []
    sl = entries_of(graph)   # c3_1: the part's slice (C-SMOKE-PARTS: the parts cover the family's entries once, in order)
    if graph in SMOKE_PARTS or part is not None:
        cuts = sorted(SMOKE_PARTS.get(graph, {}).values())
        okp = (part in SMOKE_PARTS.get(graph, {}) and cuts[0][0] == 0 and cuts[-1][1] == len(sl) and
               all(cuts[j][1] == cuts[j + 1][0] for j in range(len(cuts) - 1)) and all(a_ < b_ for a_, b_ in cuts))
        gate('C-SMOKE-PARTS', okp, '(%s smoke part %s of %s on entries [%s): the slices cover the %d entries once, in order)' % (
            graph, part, sorted(SMOKE_PARTS.get(graph, {})), ', '.join('%d, %d' % c_ for c_ in cuts), len(sl)))
        if not okp:
            raise ValueError('%s smoke part %r is not a part of SMOKE_PARTS' % (graph, part))
        a_, b_ = SMOKE_PARTS[graph][part]
        sl = sl[a_:b_]
    for e in sl:
        name = name_of(e)
        facs = [ENT.factor(TS, EDGES[graph], enc) for enc in e['factors']]
        pr.qcap = qcap_of(e)
        t0 = cpu()
        STAGE[0] = 'smoke a_k %s' % name
        ak, _, info = pr.bound(facs, e['grouping'], bars=False, entry=name)
        for k, (a, fa) in enumerate(zip(ak, refs[name]['ak'])):
            worst = max(worst, (abs(float(a.mid) - fa) / max(1.0, abs(fa)), name, k))
        n += 1
        out('SMOKE %s ak %s Dn %d forms %d: %.2f s' % (name, ['%.12g' % float(a.mid) for a in ak], info['Dn'], len(info['forms']), cpu() - t0))
        if path is None and e['parity'] == 'free' and any(f[0] == 'xi' and f[2] == 0.0 for f in facs):   # m3_run_v1_9_1: a free entry
            path = (name, facs)
        STAGE[0] = 'smoke pack plan %s' % name
        pl = pack_plan(pr, facs, e['grouping'], info, e['parity'] == 'free')   # m3_run_v1_9_2
        top = max(pl, key=lambda r: r[1] * math.log(r[2] + 1))
        out('PACK-PLAN %s: %d table requests; largest code range %d^%d (%s)' % (name, len(pl), top[2] + 1, top[1], top[0]))
        plans += [(name, r) for r in pl]
    gate('C-SMOKE-AK', n == len(sl) and n > 0 and worst[0] <= 1e-9, '(the a_k of %d %s entries against rtwin_hl_v1 %s (restored prep): largest '
         '|certified mid - float| / max(1, |float|) %.2e at %s a_%d)' % (n, graph, KEYFAM[graph], worst[0], worst[1], worst[2]))
    plant('PLANT-SMOKE-AK', not (worst[0] + 1e-6 <= 1e-9), '(the largest difference plus 1e-6)')
    name, facs = path
    i0 = next(i for i, f in enumerate(facs) if f[0] == 'xi' and f[2] == 0.0)
    f0 = facs[i0]
    facs2 = list(facs)
    facs2[i0] = (f0[0], f0[1], f0[2], [c * (1 + 1e-6) for c in f0[3]])
    STAGE[0] = 'smoke plant %s' % name
    ak2, _, _ = pr.bound(facs2, 'std', bars=False, entry=name + ' (planted)')
    w2 = max(abs(float(a.mid) - fa) / max(1.0, abs(fa)) for a, fa in zip(ak2, refs[name]['ak']))
    plant('PLANT-SMOKE-PATH', not (w2 <= 1e-9), '(%s with its xi factor\'s c9 times 1 + 1e-6: largest difference %.2e)' % (name, w2))
    pack_gate(graph, plans)   # m3_run_v1_9_2
    fb_info()


def rep_checks(news, res, refs):
    """C-REP-B and C-REP-AK with their plants on the computed free entries news [(graph, key, record item)] against the float twins."""
    rep, rak = [], []
    for graph, key, it in news:
        r, d = res[(graph, key)], refs[graph][key]
        for p in ('rem', 'tail', 'ann', 'far'):
            if d['B'][p] > 0:
                rep.append((it['B'][p] / d['B'][p], key, p))
        for k, (a, fa) in enumerate(zip(r['ak'], d['ak'])):
            rak.append((abs(float(a.mid) - fa) / max(1.0, abs(fa)), key, k))
    lo_, hi_ = min(rep), max(rep)
    gate('C-REP-B', 1 - 1e-6 <= lo_[0] and hi_[0] <= 1.15, '(%d bar parts against rtwin_hl_v1 (restored prep) z9sym: certified/float in [%.9f (%s %s), '
         '%.6f (%s %s)])' % (len(rep), lo_[0], lo_[1], lo_[2], hi_[0], hi_[1], hi_[2]))
    plant('PLANT-REPB', not (1 - 1e-6 <= lo_[0] * 0.5), '(the smallest ratio times 0.5)')
    wr = max(rak)
    gate('C-REP-AK', wr[0] <= 1e-9, '(%d a_k against rtwin_hl_v1 (restored prep) z9sym: largest |certified mid - float| / max(1, |float|) %.2e at %s a_%d)' % (
        len(rak), wr[0], wr[1], wr[2]))
    plant('PLANT-REPAK', not (wr[0] + 1e-6 <= 1e-9), '(the largest difference plus 1e-6)')


def reader_plants(text, name):
    """m3_run_v1_8_3's reader plants on the H record's text, through m3_reader_v6_3 (_check_text: the writer's parse; loads: the bound
    entry point), with the layer plants of the v1_4_1 pin: the denied layers, a record naming arbeng_ma_v1_3 with this layer's validation
    list, one validation sha256 changed, and the mock; then C-BOUND-RT with the bound-load plants."""
    dd = json.loads(text)
    k0 = sorted(k for k in dd['items'] if dd['items'][k]['parity'] == 'free')[0]
    dd['items'][k0]['B'].pop('rnd')
    try:
        RDR._check_text(json.dumps(dd), 300, NN)
        plant('PLANT-FMT', False, '(H copy without one rnd)')
    except ValueError:
        plant('PLANT-FMT', True, '(H copy without one rnd)')
    dd2 = json.loads(text)
    kr = max((k for k in dd2['items'] if dd2['items'][k]['parity'] == 'free'), key=lambda k: sum(dd2['items'][k]['ak_rad']))
    dd2['items'][kr]['B']['rnd'] = 0.0
    try:
        RDR._check_text(json.dumps(dd2), 300, NN)
        plant('PLANT-RND', False, '(H copy with %s rnd = 0)' % kr)
    except ValueError:
        plant('PLANT-RND', sum(dd2['items'][kr]['ak_rad']) > 0, '(H copy with %s rnd = 0; its ak_rad sum %.1e)' % (kr, sum(dd2['items'][kr]['ak_rad'])))
    deny = dict(DENY)
    nx = 3 if NN == 4 else 4
    for lab, mut, jref, nexp in (('PLANT-READER-PRECERT', 'precert', 300, NN), ('PLANT-READER-KERNEL', 'kernel', 300, NN),
                                 ('PLANT-READER-PREC', 'prec', 300, NN), ('PLANT-LAYER-V1_1', 'arbeng_ma_v1_1.py', 300, NN),
                                 ('PLANT-LAYER-V1_2', 'arbeng_ma_v1_2.py', 300, NN), ('PLANT-LAYER-V1_4', 'arbeng_ma_v1_4.py', 300, NN),
                                 ('PLANT-READER-MOCK', 'mock_arbeng_v1_4.py', 300, NN), ('PLANT-LAYER-MIX', 'mix', 300, NN),
                                 ('PLANT-VALREC', 'valrec', 300, NN), ('PLANT-CLAIM', 'claim', 300, NN), ('PLANT-ARBK', 'arbk', 300, NN),
                                 ('PLANT-ARBB', 'arbb', 300, NN), ('PLANT-JREF', None, 150, NN), ('PLANT-N', None, 300, nx),
                                 ('PLANT-KIND', 'kind', 300, NN), ('PLANT-PARZERO', 'parzero', 300, NN),
                                 ('PLANT-CLAIM-BALL', 'claimball', 300, NN), ('PLANT-CLAIM-BALL-MISSING', 'noclaimball', 300, NN)):
        dd3 = json.loads(text)
        if mut == 'precert':
            dd3['format'] = 'M3_RECORD_v1_PRECERT'
            dd3['claim'] = 'NOT CERTIFIED (PRECERT): ' + dd3['claim']
        elif mut == 'kernel':
            dd3['kernel_sha256'] = flip(dd3['kernel_sha256'])
        elif mut == 'prec':
            dd3['kernel_prec'] = 256
        elif mut in deny:
            dd3['kernel_file'], dd3['kernel_sha256'] = mut, deny[mut]
        elif mut == 'mix':
            dd3['kernel_file'], dd3['kernel_sha256'] = 'arbeng_ma_v1_3.py', '9530f2c324bccc06bb29a043329a2b772a3ee60c241828f26f9ef8feace594be'
        elif mut == 'valrec':
            dd3['validation'] = dd3['validation'][:-1] + [flip(dd3['validation'][-1])]
        elif mut == 'claim':
            dd3['claim'] = dd3['claim'] + ' '
        elif mut == 'arbk':
            dd3['arb_kernel_sha256'] = flip(dd3['arb_kernel_sha256'])
        elif mut == 'arbb':
            dd3['arb_base_sha256'] = flip(dd3['arb_base_sha256'])
        elif mut == 'kind':
            dd3['items'][sorted(dd3['items'])[0]].pop('kind')
        elif mut == 'parzero':
            k0_ = sorted(k for k in dd3['items'] if dd3['items'][k]['parity'] == 'free')[0]   # c3: no parity zero in the c3 records
            dd3['items'][k0_]['parity'] = 'zero'   # c3: a free item marked zero (its a_k are not zero)
        elif mut == 'claimball':
            dd3['claim_ball'] = dd3['claim_ball'] + ' '
        elif mut == 'noclaimball':
            dd3.pop('claim_ball')
        what = mut or ('expected J_REF %d' % jref if jref != 300 else 'expected N %d' % nexp)
        try:
            RDR._check_text(json.dumps(dd3), jref, nexp)
            plant(lab, False, '(m3_reader_v6_3 must refuse the mutated H copy: %s)' % what)
        except ValueError:
            plant(lab, True, '(m3_reader_v6_3 refuses the mutated H copy: %s)' % what)
    dh = tsha(text)
    try:
        RDR.loads(text, 'RECORD %s %s\nVERDICT VALID\n' % (name, dh), 300, NN, name)
        gate('C-BOUND-RT', True, '(m3_reader_v6_3.loads accepts the H text under an output that names it and ends VALID)')
    except ValueError as ex:
        gate('C-BOUND-RT', False, '(refused: %s)' % ex)
    for lab, otext in (('PLANT-BOUND-VERDICT', 'RECORD %s %s\nVERDICT VALID-PRECERT\n' % (name, dh)),
                       ('PLANT-BOUND-INVALID', 'RECORD %s %s\nVERDICT INVALID (C-REP-B)\n' % (name, dh)),
                       ('PLANT-BOUND-TWO', 'RECORD %s %s\nVERDICT VALID\nVERDICT VALID\n' % (name, dh)),
                       ('PLANT-BOUND-SHA', 'RECORD %s %s\nVERDICT VALID\n' % (name, flip(dh))),
                       ('PLANT-BOUND-NONE', 'VERDICT VALID\n')):
        try:
            RDR.loads(text, otext, 300, NN, name)
            plant(lab, False, '(m3_reader_v6_3.loads must refuse this asm output)')
        except ValueError:
            plant(lab, True, '(m3_reader_v6_3.loads refuses this asm output)')


def resume_chain():
    """C-RESUME-CHAIN: Xr1 and Xr2 of every family in RESUME_FAMS are valid (hand-offs bound to their producer outputs), each with
    resume_ok, and Xr1 with plant_fired; the outcome per family is printed (PLANT-RESUME's status, as it was asked for S9)."""
    ok, why = True, []
    for graph in RESUME_FAMS:
        b1 = read_handoff('%sr1.%d' % (PFX[graph], NN), graph)
        b2 = read_handoff('%sr2.%d' % (PFX[graph], NN), graph)
        ok = ok and b1['resume_ok'] is True and b1['plant_fired'] is True and b2['resume_ok'] is True and b1['entry'] == b2['entry'] == RESUME_KEY[graph]
        why.append('%s on %s: part 1 cut %s resumed %s, PLANT-RESUME %s; part 2 cut after %d of %d units resumed %s' % (
            graph, b1['entry'], b1['cut'], 'identical' if b1['resume_ok'] else 'DIFFERENT', 'FIRES' if b1['plant_fired'] else 'DOES NOT FIRE',
            b2['cut'], b2['units'], 'identical' if b2['resume_ok'] else 'DIFFERENT'))
    gate('C-RESUME-CHAIN', ok, '(%s)' % '; '.join(why))


def prep_info(graph):
    """the INFO of a family's valid prep pieces for the record: the largest D16 E2 relative radius with its step, the would-be MAFallback
    count, each table's shadow_max, the adopted and moved-aside steps, the pieces."""
    rel, trips, shadow, adopted, moved, pieces = (0.0, '-'), 0, {}, 0, 0, []
    for k in range(1, MAXPP + 1):
        st = item_state('%sp%d.%d' % (PFX[PREPOF[graph]], k, NN))
        if st == 'missing':
            break
        if st == 'capped':
            pieces.append('%d capped' % k)
            continue
        info = read_handoff('%sp%d.%d' % (PFX[PREPOF[graph]], k, NN), PREPOF[graph])['info']   # c3: PREPOF
        rel = max(rel, (info['e2_rel'][0], info['e2_rel'][1]))
        trips, adopted, moved = trips + info['e2_trips'], adopted + info['adopted'], moved + info['moved']
        shadow.update(info['shadow'])
        pieces.append(str(k))
    return {'e2_rel_max': rel[0], 'e2_rel_where': rel[1], 'e2_over_fallback_rel': trips, 'shadow_max': shadow, 'adopted': adopted,
            'moved_aside': moved, 'pieces': pieces}


def run_asm():
    stage('asm')
    parity_set()
    res = {}
    for graph in FAMS:
        walk_pieces(graph, res)
    resume_chain()
    refs, fins = {}, {}
    for graph in FAMS:
        fins[graph] = prep_final(graph)
        prep_share(graph)   # c3
        refs[graph] = {}
        for p in ref_files(graph):
            with open(p) as fh:
                lines = fh.read().split('\n')
            okv = HO.verdict_ok(lines, 'VERDICT VALID') and [ln for ln in lines if ln.startswith('TRIAL')] == ['TRIAL z9sym']
            gate('C-HASH-REF', okv, '(%s, sha256 %s: VERDICT lines exactly [VERDICT VALID], TRIAL lines exactly [TRIAL z9sym])' % (
                os.path.basename(p), sha(p)))
            for d in read_lines(p, 'KEYJSON'):
                refs[graph][d['key']] = d
    files, news, pz = {g: {} for g in FAMS}, [], []
    for e in V3:
        r = res[(e['graph'], name_of(e))]
        if e['parity'] == 'zero':
            if r['parity'] != 'zero':
                raise ValueError('%s: marked zero, computed %s' % (name_of(e), r['parity']))
            files[e['graph']][name_of(e)] = REC.entry_record(None, None, T_REF, 'zero')
            pz.append(name_of(e))
            continue
        it = REC.entry_record(r['ak'], r['bars'], T_REF, 'free', a0_exact=r['a0_exact'], laws=r['laws'])
        files[e['graph']][name_of(e)] = it
        news.append((e['graph'], name_of(e), it))
    out('PARITY-ZERO %s: written as exact zeros with parity zero (C-ODD and C-ODD-AK in their pieces)' % pz)
    want = {g: set(e['key'] for e in LIST['entries'] if e['graph'] == g) for g in FAMS}
    gate('C-SCOPE', all(set(files[g]) == want[g] for g in FAMS), '(the hl records hold exactly the list\'s keys of their graphs: %s)' % (
        ', '.join('%s %d' % (g, len(files[g])) for g in FAMS)))
    plant('PLANT-SCOPE', not (set(list(files['LH'])[1:]) == want['LH']), '(LH without one key)')   # pk23 hl_v1
    rep_checks(news, res, refs)
    # the texts, C-FMT, the plants, and only then the write
    tag = TAG
    eng = {'m3_run_v1_9_3': SELF_SHA, 'modules': dict(OWNMOD)}
    kern = {'kernel_file': KERNEL + '.py', 'kernel_sha256': KFILES[KERNEL + '.py'], 'kernel_prec': int(flint.ctx.prec),
            'validation': [v[2] for v in VALREC], 'arb_kernel_file': ARBK + '.py', 'arb_kernel_sha256': KFILES[ARBK + '.py'],
            'arb_base_file': ARBB + '.py', 'arb_base_sha256': KFILES[ARBB + '.py']}
    radii = lambda d: {k: d[k] for k in ('a_v', 'ap', 'theta0')}
    texts, paths = {}, {}
    for g in FAMS:
        tabs = {k: v['handoff'] for k, v in sorted(fins[g]['state']['tables'].items())}
        pinfo = prep_info(g)
        extra = {'entry_list': '%s:%s' % (LISTF, INPUTS[(HLD, LISTF)]), 'graph': g, 'dmaxH': 16, 'claim_ball': CLAIM_BALL,   # c3
                 'prep16': dict({'tables': tabs, 'block': BLOCK16, 'memo': os.path.basename(memo_path(PREPOF[g])), 'memo_lines': fins[g]['memo_lines'],
                                 'memo_head_sha256': fins[g]['memo_head_sha'], 'prep_piece': fins[g]['piece'], 'prep_family': PREPOF[g],
                                 'prep_script': item_sha('%sp1.%d' % (PFX[PREPOF[g]], NN))}, **pinfo)}
        out('PREP16-INFO %s: largest D16 E2 relative radius %.3e at %s, %d over FALLBACK_REL; shadow_max %s; adopted %d, moved aside %d; '
            'pieces %s' % (g, pinfo['e2_rel_max'], pinfo['e2_rel_where'], pinfo['e2_over_fallback_rel'],
                           ', '.join('%s %.3e' % kv for kv in sorted(pinfo['shadow_max'].items())), pinfo['adopted'], pinfo['moved_aside'],
                           ', '.join(pinfo['pieces'])))
        top = REC.top_level(NN, 300, {g: radii(ref_prep(g))}, TRIAL, eng, tag, kern, extra=extra)
        texts[g] = json.dumps(dict(top, items=files[g]))
        paths[g] = os.path.join(OUTD, 'm3_hl_%s_N%d_J300%s_hl.json' % (g, NN, tag))   # pk23 hl_v1
        rd = RDR._check_text(texts[g], 300, NN, name=os.path.basename(paths[g]))
        okf = all(rd['entries'][k] == (files[g][k]['ak'], files[g][k]['err']) for k in files[g]) and set(rd['entries']) == set(files[g])
        gate('C-FMT', okf, '(%s: %d keys read back exactly from the text by m3_reader_v6_3; %d bytes; sha256 %s)' % (
            os.path.basename(paths[g]), len(files[g]), len(texts[g]), tsha(texts[g])))
    reader_plants(texts['LH'], os.path.basename(paths['LH']))   # pk23 hl_v1
    gate('C-PREC-ASM', K.PREC == 512 and flint.ctx.prec == 512, '(flint ctx.prec %d before the write)' % flint.ctx.prec)
    opened = []

    def no_open(p, mode):
        opened.append(p)
        raise OSError('PLANT-NOWRITE: the writer opened %s' % p)
    refused = 0
    for fl, nf, tg in ((FAILS + ['PLANT-FORCED'], NOFIRE, tag), (FAILS, NOFIRE + ['PLANT-FORCED'], tag), (FAILS, NOFIRE, '_PRECERT')):
        try:
            if write_records(texts, paths, fl, nf, tg, opener=no_open) == []:
                refused += 1
        except OSError:
            pass
    plant('PLANT-NOWRITE', refused == 3 and not opened, '(write_records under a failed gate, an unfired plant and a PRECERT tag: %d of 3 refused, %d files opened)' % (
        refused, len(opened)))
    written = write_records(texts, paths, FAILS, NOFIRE, tag)
    if not written:
        out('RECORDS NOT WRITTEN (%s)' % ', '.join(FAILS + ['%s did not fire' % p for p in NOFIRE] + ([] if tag == '' else ['TAG %r' % (tag,)])))
    for b, path in written:
        gate('C-WRITE', sha(path) == tsha(texts[b]), '(%s holds exactly its C-FMT text)' % os.path.basename(path))
        out('RECORD %s %s' % (os.path.basename(path), sha(path)))


try:
    m_ = re.fullmatch(r'(L|LH|LT)(a|p|k|r)([0-9]*)', FAM)   # pk23 hl_v1
    if FAM == 'asm':
        run_asm()
    elif m_.group(2) == 'a':
        run_smoke(m_.group(1), int(m_.group(3)) if m_.group(3) else None)   # c3_1
    elif m_.group(2) == 'p':
        run_prep16(m_.group(1), int(m_.group(3)))
    elif m_.group(2) == 'r':
        run_resume(m_.group(1), int(m_.group(3)))
    else:
        run_nk(m_.group(1), int(m_.group(3)))
    finish()
except SystemExit:
    raise
except BaseException:
    out('EXCEPTION in stage %s:' % STAGE[0])
    for ln in traceback.format_exc().rstrip().split('\n'):
        out('  ' + ln)
    out('VERDICT INVALID (EXCEPTION)')
    sys.exit(1)
