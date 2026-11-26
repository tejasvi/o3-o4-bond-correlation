#!/usr/bin/env python3
"""m3ref_hl_v1.py -- pk23 (code/pk23/pev/). FLOAT twin for the option B Pev entries on S8's L graph. Nothing here is certified.
A COPY of pk22's m3ref_px22_v1_7.py (sha256 a7e471f233d4eded3d4c585ab8fc6459a7fc05678b30761312f9759470f6fe70) by pk23's make_m3ref_hl_v1.py: one P16 family P16L (graph L of
pk23/pev/HL_ENTRY_LIST_v1.json, sha256 2d115b6de96e5d8da01bb20ca11ccda6c7d650eb74faed1262f24be619e3ed42, pinned in INPUTS_HL, list version hl; key TT,0,0; dmaxH 16, qcap 6, npoly base 11);
every written path in pk23/pev/out (the P16 cache out/tab16, the E2 memos, the earlier pieces); piece outputs m3ref_hl_v1_*.
m3ref_px22_v1_7's docstring follows.
m3ref_px22_v1_7.py -- pk22 (code/pk22/m3/). FLOAT reference for B's and W1a's M3 windows. Nothing here is certified.
A REVISION of m3ref_px22_v1_6.py (sha256 88019593e181ce5df920efd127da9c36d2e6ad96273253d786456b6d09b63cb7) by make_m3ref_px22_v1_7.py: a trial set z9symxy (TRIAL argument;
pk22/midrow/psixy/ts_N4_J170_D_S_z9symxy_v1.json 909b20bf and ts_N3_S_z9symxy_v1.json d6b2ab93, pinned in INPUTS_PSX; states 0..9 are z9sym's, state 10 is psi_xy), and two
families that read pk22's C3K_ENTRY_LIST_v1.json (sha256 73d132270f4d07da13e3d16aa50673acd21bc9753ce524f2ae80717e1f7b61de, pinned in INPUTS_W1A, list version c3k): P16E4D, P16E4N, at dmaxH 16 and
qcap 6; npoly bases E4D 28, E4N 13; a family's later pieces read its earlier pieces of the same TRIAL; piece outputs m3ref_px22_v1_7_*.
v1_6's docstring follows.
m3ref_px22_v1_6.py -- pk22 (code/pk22/m3/). FLOAT reference for B's and W1a's M3 windows. Nothing here is certified.
A REVISION of m3ref_px22_v1_5.py (sha256 99b5c798220ffbe78b4fe8a103128078fab003a1ca013a4c5eb74ca8d669d165) by make_m3ref_px22_v1_6.py: three families read pk22's
C3H_ENTRY_LIST_v1.json (sha256 4f56853ab2390a8e29b384921315ed9e4501a5bf97f66c82986e2283ecfb21f3, pinned in INPUTS_W1A, list version c3h): P16CE3H, P16CS4H, P16CH4TH, at dmaxH 16 and qcap 6;
npoly bases CE3H 28, CS4H 22, H4TH 13 (the largest B with B**F < 2**63); piece outputs m3ref_px22_v1_6_*. v1_5's docstring follows.
m3ref_px22_v1_5.py -- pk22 (code/pk22/m3/). FLOAT reference for B's and W1a's M3 windows. Nothing here is certified.
A REVISION of m3ref_px22_v1_4.py (sha256 e78b0b678e74ddbad90e2fdf3fe16b522c9c7baaa327dc49e0b3296997110a2a) by make_m3ref_px22_v1_5.py: a new table's CPU estimate is 5 s + 9e-6 s per
moment, C(D + F, F) moments (v1_4 estimated by D alone, 900 s from D 17 on, which stopped every piece of P16CE3 at N = 4 before a
D-18 table on 2 forms); piece outputs m3ref_px22_v1_5_*. v1_4's docstring follows.
m3ref_px22_v1_4.py -- pk22 (code/pk22/m3/). FLOAT reference for B's and W1a's M3 windows. Nothing here is certified.
A REVISION of m3ref_px22_v1_3.py (sha256 6ee3148d14bdd80ae262ecf82f0c1e7a4e79c79d23fcbc786f36c8c351f4fed8) by make_m3ref_px22_v1_4.py: four families read pk22's
C3_ENTRY_LIST_v2.json (sha256 e877d12f0686ff959bc34f12651f62629f0e3f43acc76b2cc363ec2524eaf1c6, pinned in INPUTS_W1A, list version c): P16CS4, P16CE3, P16CH4T, P16CE2T, at dmaxH 16 and qcap 6;
npoly bases CS4 11, CE3 15, H4T 13, E2T 16 (the largest B with B**F < 2**63); piece outputs m3ref_px22_v1_4_*. v1_3's docstring follows.
m3ref_px22_v1_3.py -- pk22 (code/pk22/m3/). FLOAT reference for B's and W1a's M3 windows. Nothing here is certified.
A REVISION of m3ref_px22_v1_2.py (sha256 f0b36284ec6e2d55db9a39fa14800b1f1e9a8e65da0810ca0504f3cb10897a0a) by make_m3ref_px22_v1_3.py: the P16 disk cache adopts an existing table file under
its own key (TABLE-ADOPTED, sha256 and size recorded in the memo chain); piece outputs m3ref_px22_v1_3_*. v1_2's docstring follows.
m3ref_px22_v1_2.py -- pk22 (code/pk22/m3/). FLOAT reference for B's and W1a's M3 windows. Nothing here is certified.
A REVISION of m3ref_px22_v1_1.py (sha256 a7ba24e911ed96185d864751b6bd4328e27679277902fa924205fc21c1c6e951), made by pk22/m3/make_m3ref_px22_v1_2.py: seven families read pk22's
B_ENTRY_LIST_v1.json (sha256 efc0b7cbb0df35a982367597e780024363a91192575bdb792dc8fb7df2546846, pinned in INPUTS_W1A, list version b): P16BD2T, P16BE2T, P16BE3T, P16BH4T, P16BL, P16BN2T, P16BT1MN, at dmaxH 16 and qcap 6, as
m3ref_v1_14's staged P16 probe; piece outputs m3ref_px22_v1_2_<family>.<N>.p<k>_z9sym.out. v1_1's docstring follows.
m3ref_px22_v1_1.py -- pk22 (code/pk22/m3/). FLOAT reference for W1a's M3 windows. Nothing here is certified.
A COPY of pk03/m3ref_v1_15.py (sha256 12a445c894b9c99410e29729046171fe041b99d14654807642a4055081fc4356), made by pk22/m3/make_m3ref_px22_v1_1.py, with four families added:
  P16T1, P16T1N, P16T2, P16T2N  the graphs T1 [vac|free], T1n [free|free], T2 [vac|int|free] and T2n [free|int|int|free] of
  pk22's W1A_ENTRY_LIST_v2.json (sha256 224ecce138214bfbf710b29585e796b676282a5ff9d7fe2a2e881780b4c6553d, pinned in INPUTS_W1A and read as list version w1a), every key of each graph,
  as m3ref_v1_14's staged P16 probe at dmaxH 16 (qcap 6, npoly base 16; [xia, [u, v, v]] is m3ref_v1_15's xia factor);
the P16 disk cache (out/tab16), the E2 memos (out/s16memo_<family>_N<N>.jsonl) and the chain of piece outputs
(out/m3ref_px22_v1_1_<family>.<N>.p<k>_z9sym.out) are in pk22/m3/out; p16_done prints P16-PART none for a family without a
dmaxH-12 base record. Every other input is read where m3ref_v1_15 reads it. pk03's docstring follows.
m3ref_v1_15.py -- pk03 (code/pk03/). FLOAT reference for M3. Nothing here is certified.
REVISION of m3ref_v1_14.py (40c11a82) for the S9 entries (the approval 2026-11-08 00:05Z; pk15's item (v)): the float twin of
the new entries of S9_ENTRY_LIST_v1 (pk03/), family
  V9I  I9 [vac|int|vac] with the pairs of columns 0 and 2 and the top bond (3,6): Iht,0, Iht,1 and Iht,3 (F = 16, npoly base 15),
read from the list as S8's V3 families are; [xia, [u, v, w]] is riglap3's xi factor on the pair (u, v) with c9 = e_1, as
kt_sh1_v1's XI(u, v, w).
- C-HASH also pins the S9 list and the two m3ref_v1_10 V3N records (REF9).
- C-PREP9 (C-PREP9-REF and PLANT-PREP9): the prep reads only the vertex forms, so the radii, rho'^2, theta0 and every prep scalar
  of V9I must agree with V3N's record at the same N to 1e-12 relative; V9-INFO prints the CPU per key.
The PREPJSON and KEYJSON lines are the references of the certified run (C-PREP-REF, C-RULE, C-REP-B, C-REP-AK). Everything else
is m3ref_v1_14's. Its docstring follows.
m3ref_v1_14: FLOAT reference for M3. Nothing here is certified.
REVISION of m3ref_v1_13.py (2e5626a2) for option 1 (the staged probe): families P16H and P16S4, the graphs of S8H and
S8S4 (list v2) at dmaxH 16 at N4, run as pieces P16H.4.p1, .p2, ... of at most 540 s each, until one ends P16-DONE:
- a disk cache for moment tables of degree >= 13 (riglap4._engine wrapped): a new table is built after a budget check and saved in
  out/tab16/<id>.npz (TABLE-SAVED: bytes and sha256), a recorded one is loaded after its size and sha256 are checked (TABLE-LOADED);
- E2 of big inputs (more than 2e8 term pairs; AllMom2.E2 wrapped) as a sum over chunks of P's sorted terms, each chunk's value kept
  in the memo out/s16memo_<family>_N<N>.jsonl and reused by later pieces (E2-CHUNK lines); a budget check before every new chunk
  or table raises StopPiece, and the piece ends PREP-PARTIAL with its CACHE-STATE (memo and table sha256s) and VERDICT VALID;
- C-CACHE-CHAIN: piece 1 starts with no memo; piece K reads piece K-1's output (VERDICT lines exactly ['VERDICT VALID'], one
  CACHE-STATE line, no P16-DONE) and requires the memo and every recorded table to have its sha256s (PLANT-CACHE);
- a piece that finishes the prep runs every key, ANALOG-INFO/ANALOG-MAX and DMAX16-INFO/DMAX16-MAX against m3ref_v1_8's dmaxH-12
  record as S8H16/S8S416 would, then P16-PART (every rE part, nE, nE4, nC8 and nC6 at dmaxH 16 against dmaxH 12) and P16-DONE.
- v1_12's dmaxH-12 record map REF12 is renamed REF16BASE (and REF12_SHA REF16BASE_SHA): the earlier name shadowed the m3ref_v1_2
  map that C-HASH reads first, harmless there but confusing.
Everything else is m3ref_v1_13's. Its docstring follows.
m3ref_v1_13: FLOAT reference for M3. Nothing here is certified.
REVISION of m3ref_v1_12.py (a485bde0) for option 2, after S8L16.4 capped in its dmaxH-16 prep (D-16 table
263.6 s): three items U16L, U16H and U16S4 (N4) that compute only the rE parts at dmaxH 16 on the graphs of m3ref_v1_8's S8L, S8H
and S8S4 (list v2), with no tilted norm, no other prep quantity and no key:
- the twelve parts of riglap5r.Prep5r l.33-39 and riglap5s.Prep5s l.29's E2^3 form (h2 from Model(g, 3) majorants, as there), each
  scale times norm_any(P, G, n, W, 2, key, 16), largest dmaxH-12 part first, each printed as it ends (U16-PART: degree, exact at
  dmaxH 12 and 16 by lp_norm's rule 2 deg P <= dmaxH, the value against m3ref_v1_8's dmaxH-12 PREPJSON part, CPU), so a capped
  item still reports the parts it finished;
- C-REF12 (the dmaxH-12 record's sha256 and VERDICT lines) with PLANT-REF12; C-U16-SETUP (radii and family equal that record's);
  C-U16-SAME (every part whose exactness is the same at dmaxH 12 and 16 equals its dmaxH-12 value to 1e-12 relative, at least
  three such parts, which checks the shared polynomials; PLANT-U16-SAME);
- U16-RE: rE at dmaxH 16 (the eleven parts plus min(ex, tr)) against the record's rE; U16-EXTRAP per key: err12 + F.R_E12
  (rE16/rE12 - 1), F.R_E being nFle3 rE in bound5s, over the key's analog (C-ANALOG-REF as before), beside the dmaxH-12 ratio and
  the ratio without F.R_E; U16-MAX: the largest. overflow, rho4, R_F, tail and ann stay as computed at dmaxH 12.
Everything else is m3ref_v1_12's. Its docstring follows.
m3ref_v1_12: FLOAT reference for M3. Nothing here is certified.
REVISION of m3ref_v1_11.py (3e833645) for route decision B (the W3 hybrid):
the float dmaxH-16 probe of S8's 4-column graphs. Three new families, copies of m3ref_v1_8's S8L, S8H and S8S4 (same list v2
graphs, keys, npoly bases, qcap 6, analogs) with the prep's degree cap dmaxH = 16 instead of 12 (Prep5sH: the vertex table at
D 16 on V = 12, so every norm up to degree 16 is exact and only norms above 16 take riglap4's Hoelder fallback):
  S8L16 (TT on L), S8H16 (h, hX on H), S8S416 (S4 keys on S4).
- ANALOG-INFO and ANALOG-MAX as m3ref_v1_8 (err / analog against pk11's analogs, C-ANALOG-REF with its plant).
- DMAX16-INFO per key: this run's err, rem, tail and ann against m3ref_v1_8's dmaxH-12 record of the same key (C-REF12: the
  record's sha256 pinned and VERDICT lines exactly [VERDICT VALID]; PLANT-REF12), and DMAX16-MAX: the smallest and largest err
  ratio 16/12 with the rem ratio beside it.
- TABLE-START and TABLE-BUILD lines around every moment table of degree >= 13 (degree, forms, moments, CPU), printed as they
  happen, so a capped prep still shows when its D-16 table began.
Everything else is m3ref_v1_11's. Its docstring follows.
m3ref_v1_11: FLOAT reference for M3. Nothing here is certified.
REVISION of m3ref_v1_10.py (4eb5113e): float a_k and bars of the 59 K-form entries that pk11's S8_ENTRY_LIST_v4 adds to v3 (the review's
K-factor rule), J_REF 300, K 3, qcap 6, z9sym, exact D-18 preps. Three families read the v4 list:
  V4NK   N [vac|int|vac] (pairs on L, R and (3,4)): TXX,a,b = [cp a 0, xi TM 1, xi TM 1, cp b 2], 0 <= a <= b <= 9 (55 keys; xi_TM^2 on
         column 1 as two factors);
  V4E3K  E3 [vac|int|free]: fXX,0 = [cp 0 0, xi TM 1, xi TM 1];
  V4F3   F3 [free|int|free] with the pair (3,4), a new graph built by the same checked column builder: wTw, wTXw and wTXXw.
npoly bases: V4NK 15 (F = 16); V4E3K and V4F3 16. The K-form keys have no earlier float record, so v3's C-REPOLD does not apply; C-PARZERO
would apply to any key the list marks parity_zero (none here). REL-INFO per key: err / |value at J = 300| (value by Horner, as v1_9)
against the list's rel_bar_max (1e-6); REL-MAX per item; V3-INFO's CPU per key. Everything else is v1_10's.
m3ref_v1_10: FLOAT reference for M3. Nothing here is certified.
REVISION of m3ref_v1_9.py (76310eac): float a_k and bars of pk11's S8_ENTRY_LIST_v3 (S8 with no 4-column entry: U9's g,a,b and
T,a,b for all ten z9sym states, and the chain-on-B entries DY, TX, e, eX, f, fX, z, wXw, wXwX), J_REF 300, K 3, z9sym, with the S8
3-column conventions (radii sqrt(min(80 G_vv/J, 0.6)), rho' 0.7, qcap 6, exact D-18 preps: no graph has more than 9 vertices).
The families read the list by graph, so a graph added to a later list needs only an S8FAM line:
  V3D   D [vac|vac]: g,a,b (0 <= a <= b <= 9), DY,a and DYY (66 keys);
  V3N   N [vac|int|vac] with pairs on L, R and (3,4): T,a,b and TX,a,b (110 keys);
  V3E2  E2 [vac|free]: e,a and eX,a (20);  V3E3  E3 [vac|int|free]: f,a and fX,a (20);  V3FF  FF [free|free]: z, wXw, wXwX (3).
npoly bases (NPB4): V3N 15 (F = 16) and V3E3 16 (F = 13); the others keep 16. C-NPB and riglap5b's carry guard as in v1_8.
New checks:
  C-REPOLD   every key the list marks old (new: false; parity zeros excepted) reproduces its earlier float record (OLDSRC: m3ref_v1_2
             D and N0T, m3ref_v1_3 S8D, S8N, S8E2, S8E3, S8FF; the same N, z9sym) to 1e-10 of max|a_k|. T,a,b: N0T ran qcap 4
             against 6 here (measured 4.5e-12 of max|a_k|), and graph N here has the pair (3,4) more than N0T, which no T factor
             reads. C-REPOLD-REF: those records have their sha256 (REF_OLD) and VERDICT lines exactly ['VERDICT VALID'].
             PLANT-REPOLD: one reference coefficient times 1 + 1e-6 must fail;
  C-PARZERO  every key the list marks parity_zero has max|a_k| <= 1e-10 of the largest nonzero key's in this run (PLANT-PARZERO:
             that largest key read as a parity zero must fail).
V3-INFO per item: keys done (old, new, parity zeros) and the CPU per key, for the certified price. Everything else is v1_9's.
m3ref_v1_9: FLOAT reference for M3. Nothing here is certified.
REVISION of m3ref_v1_8.py (350ab86e): a float probe of pk11's centered entries (NOTE_S8_LEAKAGE_ROUTES_v1 74f65c9f sect. 3.2-3.3),
each one integrand on one graph with exact binary64 centring constants, beside its uncentered siblings in the same run, at J_REF 300
with S8's 3-column conventions (prep dmaxH 12 on the 12-vertex graphs H and S4, D-18 exact elsewhere), z9sym. Five new families:
  S8Hc   H [vac|int|int|free]: h,a, hX,a and hXc,a = E_H[cp(a,0) (xi_TM(col 1) - k1)], a = 0..3;
  S8E3c  E3 [vac|int|free]: f,a, fX,a and fXc,a = E_E3[cp(a,0) (xi_TM(col 1) - k0)];
  S8E2c  E2 [vac|free]: e,a, eX,a and eXc,a = E_E2[cp(a,0) (xi_TM(col 1) - km)];
  S8FFc  FF [free|free]: z, wXw, wXwX and wXcwXc = E_FF[(xi_TM(col 0) - km)(xi_TM(col 1) - km)];
  S8S4c  S4 [free|int|int|free]: its 18 keys, XXc = E_S4[(xi_TM(col 1) - k0)(xi_TM(col 2) - k0)] and the strip covariances
         Covc,cx,bx,cy,by = E_S4[(xi_x - m_x)(xi_y - m_y)] for the 10 n = 4 pairs (N4PAIRS of kt_s8_cert_v1_11 afd8f0ca l.495-499).
The constants are binary64 ratios at J = 300 of pinned float records, each value a_0 + a_1 t + a_2 t^2 + a_3 t^3 by Horner with
t = 1.0/300: k0 = fX,0/f,0 (m3ref_v1_3 S8E3), km = eX,0/e,0 (m3ref_v1_3 S8E2), k1 = hX,0/h,0 (m3ref_v1_8 S8H), m_x = S4,x/S4,Z
(m3ref_v1_8 S8S4). A centered factor is the 'xi' factor of its bond with constant -const (encoding ['xic', TM|MB, name, col]).
C-CENTER-REF: the four records of this N have their pinned sha256 and VERDICT lines exactly ['VERDICT VALID']; C-KAPPA-REF: k0 and km
equal pk11's kappa0 (kt_s8f3g_v1_1 80c401df, float.hex) exactly (PLANT-KAPPA-REF: a hex with one mantissa digit changed must
fail); CONSTJSON prints every constant's float.hex. C-CENTER-AK: each centered key's a_k equal the linear combination of its
uncentered siblings in this run (hX,a - k1 h,a; fX,a - k0 f,a; eX,a - km e,a; wXwX - 2 km wXw + km^2 z by FF's mirror symmetry;
X1X2 - k0 (S4,x,1,TM + S4,x,2,TM) + k0^2 S4,Z; S4,xy - m_y S4,x - m_x S4,y + m_x m_y S4,Z) to 1e-10 of max|a_k| (PLANT-CENTER-AK: the
first constant times 1 + 1e-6 must fail). CENTER-INFO per centered key: err and value against its uncentered sibling's; CENTERJSON.
Everything else is v1_8's.
m3ref_v1_8: FLOAT reference for M3. Nothing here is certified.
REVISION of m3ref_v1_7.py (7ccbc320), whose S8L.4 item stopped at npoly's constructor (OverflowError: NPOLY_B 16 with F = 18 forms
puts 16**17 outside int64). npoly codes monomials in base B in one int64, so B**F must stay below 2**63; riglap5b already asserts at
every NPoly product that no exponent reaches B ("set to 8 for graphs with many forms", its l.16). The new families get the largest
base that fits (NPB4): S8L 11 (F = 18), S8H 15 (F = 16), S8S4 9 (F = 19); the older families keep theirs. C-NPB: B**F < 2**63 in exact
integers and B = NPB4's; PLANT-NPGUARD: riglap5b's guarded product is the one installed, and it fails on x^3 times x^2 in base 4.
Everything else is v1_7's.
m3ref_v1_7: FLOAT reference for M3. Nothing here is certified.
REVISION of m3ref_v1_6.py (476cf155): a float probe of S8's 4-column entries (S8_ENTRY_LIST_v2) at prep dmaxH 12 (Prep5sH: V = 12,
so the D-18 vertex table does not fit), J_REF 300, with the conventions of S8's 3-column families (radii sqrt(min(80 G_vv/J, 0.6)),
rho' 0.7, qcap 6, NPOLY_B 16) on the z9sym set. Three new families:
  S8L   graph L [vac|int|int|vac] with its 6 pairs: TT,a,b (10 keys);
  S8H   graph H [vac|int|int|free]: h,a and hX,a (8 keys);
  S8S4  graph S4 [free|int|int|free]: its 18 keys (S4,Z; S4,x,<col>,TM|MB; S4,xy,...).
New checks: C-GRAPH also requires L's column spec (v2) to give strip_graph(4) exactly (PLANT-GRAPH as before); C-ANALOG-REF: the
3-column record an analog reads (m3ref_v1_2 N0T, m3ref_v1_3 S8E3 or S8FF, z9sym, the same N) has its pinned sha256 (REF_ANALOG) and
VERDICT lines exactly ['VERDICT VALID'] (PLANT-ANALOG-REF: a sha with its last digit changed must fail).
ANALOG-INFO per key: err / analog with pk11's analogs (kt_s8f3g_v1_1 80c401df): TT,a,b -> 2 T,a,b; h,a -> 2 f,a; hX,a -> 2 fX,a;
S4,Z -> 2 z; S4,x,* -> 6 z; S4,xy,* -> 18 z (pk11 names Z4 = S4,Z, X1 = S4,x,1,TM and X1X2 = S4,xy,1,TM,2,TM); a key whose parent has
no record (zero by parity) prints n/a. ANALOG-MAX per family: the largest ratio and its key, beside pk11's requirement (the analog
set may grow together by x1.9 at N 4 and x4.4 at N 3). Everything else is v1_6's.
m3ref_v1_6: FLOAT reference for M3. Nothing here is certified.
REVISION of m3ref_v1_5.py (307cbed7) for the C-3 (suggested in review, INFO), one new family:
  vDcal  the vD graph and key D_Z2 at J_REF 150 with vD's conventions (radii sqrt(min(80 G_vv/J, 0.6)), rho' 0.7), where the D-18
         table fits (V = 6): preps riglap5s.Prep5s (vD's own path) and Prep5sH at dmaxH 18, 14 and 12, each followed by bound5s.
         The values compared are the prep quantities (rE and its parts, nC8, nC6, nE[1..3], nE4[1..3], Nc, Np, Pout, Pout_p,
         farbase) and the bar parts (rem, tail, ann, far, err).
         C-VD14  the Prep5s bar parts, err and a_k equal m3ref_v1_4's vD record of the same N (TRIAL z9sym; sha pinned in REFV14) to
                 1e-13 relative and 1e-12 of max|a_k| (PLANT-VD14: the record's err times 1 + 1e-9 must fail);
         C-H18   Prep5sH at dmaxH 18 equals Prep5s: every value to 1e-13 relative, a_k to 1e-12 of max|a_k| (PLANT-H18: the Prep5s
                 values times 1 + 1e-9 must fail);
         C-CAL   at dmaxH 12 and at 14, every value divided by its dmaxH-18 value is >= 1 - 1e-12 (a Hoelder or 3^deg value is never
                 below the exact norm: a direct test on the real polynomials), and the a_k agree to 1e-12 of max|a_k| (they do not
                 depend on dmaxH) (PLANT-CAL: the dmaxH-12 ratios inverted must fail; PLANT-CAL-AK: the largest dmaxH-12 coefficient
                 times 1 + 1e-6 must fail).
         CAL-INFO lists the ratios that differ from 1 by more than 1e-12, and the unchanged ones; CALJSON has every value, ratio and
         a_k, and riglap5s's printed rem split (2-3 digits, INFO only). Items vDcal.<N>.all with TRIAL z9sym. Everything else is v1_5's.
m3ref_v1_5: FLOAT reference for M3. Nothing here is certified.
REVISION of m3ref_v1_4.py (6b6e4db5) after its G4R results (G4R_0 = G4R_2 err 89.1, far 84.5 and rem 4.67; G4R_1 err 1.13): six
families test G4R with vacrig11w's own conventions for these graphs, radii sqrt(min(60 G_vv/J, 0.5)) and rho' = 0.9 (vacrig11w l.407,
riglap2.bound(gR, [], 1, J, rho_v, 0.9)), at dmaxH 12 (vG4ra0..2) and dmaxH 14 (vG4rb0..2), J_REF 150. Everything else is v1_4's.
m3ref_v1_4: FLOAT reference for M3. Nothing here is certified.
REVISION of m3ref_v1_3.py (4c291c67) for M2's vacuum records (PLAN_M3_CODE_v1_2_ADD4; ADD6), on the same pinned engines and trial sets,
with J_REF = 150 for the new families (300 for every older one):
  vD     graph D [vac|vac], pairs on L and R: D_Z2 = [pv(L), pv(R)] (bound5s, K 3);
  vG4r0, vG4r1, vG4r2  graph G4 (strip_graph(4)) without the horizontal bond (r, 3 + r), no factors: G4R_r. V = 12, so a D-18 vertex
         table does not fit (C(30, 12) = 8.6e7 moments): the prep is Prep5sH, riglap5s.Prep5s with its degree cap as a parameter (its
         l.22-34 with the literal 18 replaced by dmaxH; C-SRC-H checks the text), at dmaxH = 12; norms above it take riglap4's Hoelder
         fallback, as riglap5b.Prep5 already does above its own cap;
  OF4, OF3, OFD  the float outer_far of vacrig11f for E4 (S = 3..8, pcols (0,1,2), (9,10,11)), E3 (S = 3..8, pcols (0,1,2), (6,7,8))
         and ED (S = 0..5, pcols (0,1,2), (3,4,5)) at J = 150 (vacrig11f l.389-390): its lap, gauge_basis, tilted_cov, outer_far and
         edge lists E4, E3, ED_ are copied verbatim, with vacmod2's PAIRS and BASIS (C-SRC against their source lines), and its
         constants a_m = 0.55**2, A_P = 0.9**2, C_P = -log(1 - A_P)/(2 A_P). outer_far_parts repeats outer_far with its parts kept
         (chart per lam, lam*, the far base farp at its theta*, supp, value, the S-gauge variances, and the far law's rate
         r = min_v theta* A_P/(2 GS_vv) - n(V - 1)/(2 J)): C-OF-SAME (its value equals outer_far's exactly), C-OF-LAM (some lam
         tilt certainly positive definite), OFJSON, C-OF-LAW-INFO;
  OFC    C-REP-VAC: far_out = o4 + 2 mhat o3 + mhat^2 oD from this script's OF4, OF3 and OFD outputs of the same N and TRIAL; at
         N = 4 with TRIAL ts0 (vacrig11's own inputs) it must print as vacrig11_N4.txt's '7.2e-11' (PLANT-REP-VAC: times 1.02 must not).
The vacuum keys have no pk10 J = 170 record, so they have no C-REP170.
m3ref_v1_3: FLOAT reference for M3 (PLAN_M3_CODE_v1 ffdf8446, sect. 7). Nothing here is certified.
REVISION of m3ref_v1_2.py (8b0335c4): float bars for S8's entries on 3 columns or fewer (pk11's request), on the same
pinned engines and trial sets, with each key's rem split. New families, read at run time from pk11's sha-pinned entry lists:
  S8D   graph D [vac|vac]: DY,0..3 and DYY (S8_ENTRY_LIST_v2);
  S8N   graph N [vac|int|vac] with all 8 of its pairs: TX,a,b (11 keys, TX,1,0 included) and TY,a,b (10) (S8_ENTRY_LIST_v1_1);
  S8E2  graph E2 [vac|free]: e,0..3 and eX,0..3;  S8E3  graph E3 [vac|int|free]: f,0..3 and fX,0..3;  S8FF  graph FF [free|free]: z, wXw, wXwX.
  Factors: [cp, a, col] = vacres p (a = 0) or cluster state a (riglap3 xi factor, S's column a); [xi, TM|MB, col] = xi on that bond
  (c9 = e_TM or e_MB). qcap 6 for every new family.
New checks, each with a plant that must fire:
  C-GRAPH  graphs built from the lists' column specs equal strip_graph(2), strip_graph(3), Emix and Efree for D, N, E2 and FF exactly
           (so E3 comes from the same checked builder) (PLANT-GRAPH: one coupling changed must mismatch);
  C-ALIAS  e,0 = I_mix and z = I_free (m3ref_v1_2's z9sym mix/free records), TX,a,0 = A,a and TX,0,a = A,a by the left-right mirror (its
           N1 records): max_k |diff| <= 1e-10 max_k |a_k| (PLANT-ALIAS: one reference coefficient times 1 + 1e-6 must fail); the bar parts'
           relative differences print as C-ALIAS-B-INFO;
  C-TY     TY,a,b = pi_a pi_b TX,a,b (T <-> B automorphism of N; pi = +1, +1, -1, +1 for states 0..3) and TX,1,0 = TX,0,1 (mirror), a_k
           to 1e-10 max|a_k| (PLANT-TY: the sign of pi_2 flipped must fail on a pair with state 2); bars as C-TY-B-INFO;
  PAR-INFO e,2 and f,2 (one odd state on a T <-> B symmetric graph): max |a_k|.
Each KEYJSON gains rem_split = {overflow, F.R_E, rho4, rho4_C8, rho4_C6, R_F}, read from riglap5s.bound5s's own verbose line.
Also fixes m3ref_v1_2's print slips (ERRATUM_m3ref_v1_2_z9sym_v1): the banner names this file, the inputs line names the TRIAL's files,
and C-HASH counts every pinned input.
REVISION of m3ref_v1_1.py (c264a7f3): a third argument TRIAL selects the trial set: ts0 = pk10's ts_* and vacres_K3_N* (as v1_1),
z9sym = pk11's ts_*_z9sym_v1 and vacres_K3_N*_sym_v1 (the certified runs' set). Under z9sym, C-REP170 gates only the keys without
cluster states, to 1e-10 of max|a_k| (the vacres pairs were averaged, by up to 3.7e-13); cluster-state keys print C-REP170-INFO.
REVISION of m3ref_v1.py (d50c5e7e), on its N0.4.all record (VERDICT INVALID by C-REP170 only: T,2,2's a_3 differed from cluster_T's
by 4.55e-13 = 4.5e-12 of max|a_k| under qcap 6 against cluster_T's qcap 4). Single change: family N0 is split into N0T (cluster_T's 7
keys, qcap 4, as cluster_T) and N0m (pairs_m2's I3p, I3m, I3c, qcap 6, as pairs_m2); every other family keeps qcap 6 as its producers.
Re-runs pk10's Lemma 19.1c producers (pairs_m2 c9c18669, pairs_m2b ad303222, binding5 f09c0427, cluster_T 112622a4, binding4 3309733d,
endw bcddbe81) at J_REF = 300 with radii from J_REF, on read-only sha-pinned copies of the riglap stack in pk03/pin/. It gives C-REP's
references (a_k, bar parts, prep quantities, radii, theta0) and STAGE-CPU / PROFILE lines for the price of the certified pieces.
Families (graph, factor lists, NPOLY_B and qcap as the producers):
  D    [vac|vac], pairs on L and R: g,a,b (0 <= a <= b <= 3), Ndel, Na (binding5 D); kn, Nw (pairs_m2 D). Aliases m2 g00 = g,0,0, Nd = Ndel.
  N0T  [vac|int|vac], pairs on L and R, qcap 4: T,a,b (cluster_T's 7 pairs). Alias m2 T00 = T,0,0.
  N0m  the same graph, qcap 6: I3p, I3m, I3c (pairs_m2 N).
  N1   N0T's graph plus the pair (3,4): A,0..A,3, Ia (binding5 Na).
  N2   N0T's graph plus the pairs (3,4), (4,5): I_N (binding4), Ip3, A0w (pairs_m2b).
  mix  [vac|free], pairs on L: I_mix (endw); free [free|free], no pairs: I_free (endw). Both items also give endw's r_main (J-independent:
       its three graphs have V = 6, so the J-terms of logmain cancel in 2 logmain(mix) - logmain(free) - logmain(D)).
Items <family>.<N>.<range>: range 'all', or i-j (0-based key indices, inclusive) to resume after a CAP-STOP; D.<N>.mono is C-MONO-INFO.
Arguments: ITEM LIM TRIAL; LIM = RLIMIT_CPU soft limit in s (5..540), hard LIM + 5; SIGXCPU prints CAP-STOP and VERDICT INCOMPLETE (CAP-STOP).
Checks of v1_2 kept: C-COPY, C-SRC, C-HASH, C-REP170 (families with pk10 records), C-RMAIN, C-THETA, with their plants.
Prints PREPJSON, one KEYJSON per key, STAGE-CPU and PROFILE lines, then VERDICT VALID, VERDICT INCOMPLETE (CAP-STOP) or VERDICT INVALID.
It writes no file; the run line redirects stdout and stderr into pk03/out/.
Run: D=/mnt/g2/release/root/code/pk03; OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 OMP_NUM_THREADS=1 TMPDIR=$D/tmp
  timeout 580 nice -n 10 prlimit --as=8589934592 -- python3 -I -B $D/m3ref_v1_3.py ITEM LIM TRIAL
  > $D/out/m3ref_v1_3_ITEM_TRIAL.out 2> $D/out/m3ref_v1_3_ITEM_TRIAL.err
"""
import resource, sys, time, math, hashlib, signal, os, json, re, inspect, traceback, io, contextlib

ITEM_RE = r'(D|N0T|N0m|N1|N2|mix|free|S8D|S8N|S8E2|S8E3|S8FF|vD|vG4r0|vG4r1|vG4r2|OF4|OF3|OFD|OFC|vG4ra0|vG4ra1|vG4ra2|vG4rb0|vG4rb1|vG4rb2|vDcal|S8L|S8H|S8S4|S8L16|S8H16|S8S416|U16L|U16H|U16S4|P16H|P16S4|S8Hc|S8E3c|S8E2c|S8FFc|S8S4c|V3D|V3N|V3E2|V3E3|V3FF|V4NK|V4E3K|V4F3|V9I|P16T1|P16T1N|P16T2|P16T2N|P16BD2T|P16BE2T|P16BE3T|P16BH4T|P16BL|P16BN2T|P16BT1MN|P16CS4|P16CE3|P16CH4T|P16CE2T|P16CE3H|P16CS4H|P16CH4TH|P16E4D|P16E4N|P16L)\.(4|3)\.(all|[0-9]{1,2}-[0-9]{1,2}|mono|p[1-9])'
if len(sys.argv) != 4 or sys.argv[3] not in ('ts0', 'z9sym', 'z9symxy') or not re.fullmatch(ITEM_RE, sys.argv[1]) or (sys.argv[1].endswith('.mono') and not sys.argv[1].startswith('D.')):
    print('usage: m3ref_v1_11.py ITEM LIM TRIAL (ITEM = <family>.<N>.<range>, family D, N0T, N0m, N1, N2, mix, free, S8D, S8N, S8E2, S8E3, '
          'S8FF, vD, vG4r0, vG4r1, vG4r2, OF4, OF3, OFD, OFC, vG4ra0-2, vG4rb0-2, vDcal, S8L, S8H, S8S4, S8L16, S8H16, S8S416, U16L, U16H, U16S4, P16H (range p1-p9), P16S4 (range p1-p9), S8Hc, S8E3c, S8E2c, S8FFc, S8S4c, V3D, V3N, V3E2, V3E3, V3FF, V4NK, V4E3K, V4F3 or V9I, N 4 or 3, range all, i-j or mono (D only); LIM = RLIMIT_CPU soft limit in s, 5..540; TRIAL ts0 | z9sym)')
    sys.exit(2)
FAM, NN_S, RNG = sys.argv[1].split('.')
TRIAL = sys.argv[3]
NN = int(NN_S)
LIM = int(sys.argv[2]) if re.fullmatch(r'[0-9]{1,3}', sys.argv[2]) else -1
if not (5 <= LIM <= 540):
    print('bad LIM %r (need 5 <= LIM <= 540)' % sys.argv[2])
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

SCR = '/mnt/g2/release/root/code/pk10/scripts'
INP = '/mnt/g2/release/root/code/pk10/scratch'
OWN = '/mnt/g2/release/root/code/pk03'
MYD = '/mnt/g2/release/root/code/pk22/m3'   # pk22 copy: its list and the P16 cache and outputs
HLD = '/mnt/g2/release/root/code/pk23/pev'   # pk23 hl_v1: the L list, the P16 cache, the memos, the pieces
PIN = os.path.join(OWN, 'pin')
PINNED = {
    'riglap2.py': 'dbc052f8d3519ab9045752ea41ab6d3a02ee452a9a14a40c46485a9f72bb1aac',
    'riglap3.py': 'e394f81567e62222240050c7cbc70c480b0804d929a8713a7b30e70ebbf1ea69',
    'riglap4.py': 'ed8eecd6c6ed529b9471097e205b63a9c0f1435973c498d9f1920850ec3d29d7',
    'riglap5.py': 'bbfbea1f5b2680eec71eee647b2c608e08f8feacf8c21fbd67f4d0ff76f037a3',
    'riglap5b.py': '0f9dc107d8709a78e4793db0fce23d8559fa93346d593304433162c72b5b0b93',
    'riglap5c.py': 'efb2f505a2d169874e2beb358ed5179901fbd6bde0791ccd578309a2a57a054e',
    'riglap5e.py': 'cafd025a5bb46c8b4a742ca3358d299bdea8e1b382893a9c8127ec4a1da821d9',
    'riglap5r.py': '7feb47f7ce840837cf04b3156e4ed94c22ec2cb3543276c0d3892c4d6a6fe749',
    'riglap5s.py': '44bdafd38b6a77af38af0e77ea17833fa08cdde734ecce3951795984b957e839',
    'pseries.py': '20936f6e02cb71a02436316b688072762b041c4e78736f3ff58ac38160f81d0e',
    'npoly.py': '5112976c24f0cb02bc82e215462d9fc78b75456b7634542a5074f2d0fce3e9de',
    'amom2b.py': '940aa05202561e01589623f7f57e89369357a4f3861eea7c8d221155cd968bfc',
}
SRCFILES = {
    'lapl2.py': 'b28ffbdb86fab237564f2db9ea8b3e904481fba31ad79e39421de7b8a9dfe116',
    'vacmod2.py': '533546b173af147a56e9531e26afa64cb3dbaccefd5fb7b1283f03baff06a000',
    'endw.py': '1c4efd9409470625309a8100bcb207165ee2732031c145f340068d79003af073',
    'vacrig11f.py': 'c2d6c059adaee674e5bc9cdc2fe96f97a73ac9042eda620c1e259f734e870eff',
}
INPUTS = {
    'vacres_K3_N4.json': '516b2501c37a65b21b617fba3cb1d7b02adf9966f409bc5105418822dfa0e765',
    'vacres_K3_N3.json': 'ebcbd08ca532642188071c964039808a318038020bb1a788a7fa3a49cb357426',
    'ts_N4_J170_D_S.json': 'd6d104ea1f2f64a82f051ce2872f1fbbd0628c9875b0743e4815bf74643fea8c',
    'ts_N3_S.json': '26e20e76fbce80c205703f5ba27395ebddaeaa2713bb129b0b4e5902a2061955',
    'm2_N4_J170.json.b': '7c0d4316e5162300becf5b541ebb4d2e68c83115ee2f35f30c4f2b22ffc95a19',
    'm2_N3_J170.json.b': '55da99fdd7bf1719685203a10b2c76e0fafc1dbb62fe859f36fc3b04f9cd2af0',
    'b5_N4_J170.json': 'f19d1e085ca8bc89b5d1c65a18589ebe61507886c891f5dcb924569f0f931928',
    'b5_N3_J170.json': '567f5543f49b4c4b379ed8724503cce3401646687ad113414617601786ee2db2',
    'clT_N4_J170.json': 'cfd2ab7c1be04487f8ec1b012eda42cbced4bb38310d00fcd2ac5e765b312669',
    'clT_N3_J170.json': '7d62c3030480a4ffb41befe931614bd790d06cf975e07963814dcac9269dc998',
    'binding4_N4_J170.json': '46a47036b45a90e5b0729901c764fd029cf87a92cece7597171e706b876415e4',
    'binding4_N3_J170.json': 'f5e90b08d606c2cec7e33635ebf6f45eee99925c125e82beaa3f162c91d46f6e',
    'endw_N4_J170.json': 'e8b1fe300f1de5ac1a1909c101afb6e00c5008b96de1747007accf5a6946f9c4',
    'endw_N3_J170.json': '0db59cc3459200ec06c5583b988291f7ab28eff9beeee8609ac93cdb4cf49d67',
    'vacrig11_N4.txt': '3c9d992f65202def7e0b8e793e4677ceef9f0dbaff7dd3c18e812a05f41bfdfb',
}
INPUTS_W4 = {
    'ts_N4_J170_D_S_z9sym_v1.json': 'ea9d6c1bc72cdac5b6d55091766a908937c7ce2bf60257636824388ffe5b7b5d',
    'ts_N3_S_z9sym_v1.json': 'a298db655d832c0685a9aba093dd123d372698fa2fb7905a15f442bb0e35f8e6',
    'vacres_K3_N4_sym_v1.json': 'b40859de2607f64cd127cb1834a04e9f33b3c2cbe4af9fe4f2bb80badaacd43e',
    'vacres_K3_N3_sym_v1.json': 'e5a9b49fde1896ff1d87de1d4a44571376eeeeb31b0ce4205faecdd2463115c0',
}
INPUTS_PSX = {   # pk22 v1_7: the z9symxy trial files (pk22/midrow/psixy/)
    'ts_N4_J170_D_S_z9symxy_v1.json': '909b20bfa30a4b95c2a78194e032508cde161da4f66de147fc40167b6c4ee560',
    'ts_N3_S_z9symxy_v1.json': 'd6b2ab93d086831e2423eed52ece6bc11abc0eeb92c31f8b8fa9368afd5f5a91',
}
INPUTS_HL = {   # pk23 hl_v1: the L list (pk23/pev/)
    'HL_ENTRY_LIST_v1.json': '2d115b6de96e5d8da01bb20ca11ccda6c7d650eb74faed1262f24be619e3ed42',
}
INPUTS_S8 = {
    'S8_ENTRY_LIST_v1_1.json': '8b4066f53a36ba8de1f50f2678fa13ee802e7f7dccecee6c611f2fee81e1cf84',
    'S8_ENTRY_LIST_v2.json': 'c3830f588dbaa2ef4de558659ab742caa7b231e91810dfd2ec036d66d9cdce5e',
    'S8_ENTRY_LIST_v3.json': 'aa7cc0c938c23fcf4ba3510fdc0333055d3059b71a4147cc8f0de49c2b04cf00',
    'S8_ENTRY_LIST_v4.json': '6294d0aca8846f8bc1f0d1c31ba680b21722f7f64f1d481f217f6871a73d95ad',
}
INPUTS_S9 = {   # m3ref_v1_15: the S9 list (pk03/)
    'S9_ENTRY_LIST_v1.json': '50beb53e74fe42aab6d5c889734fd91a04570ea69b2188fdd8ddf2379107de4e',
}
INPUTS_W1A = {   # pk22 copy: the W1a list (pk22/m3/); v1_2: and B's list; v1_4: and c3's list
    'C3_ENTRY_LIST_v2.json': 'e877d12f0686ff959bc34f12651f62629f0e3f43acc76b2cc363ec2524eaf1c6',
    'C3H_ENTRY_LIST_v1.json': '4f56853ab2390a8e29b384921315ed9e4501a5bf97f66c82986e2283ecfb21f3',   # pk22 v1_6: c3h's list
    'C3K_ENTRY_LIST_v1.json': '73d132270f4d07da13e3d16aa50673acd21bc9753ce524f2ae80717e1f7b61de',   # pk22 v1_7: c3k's list
    'B_ENTRY_LIST_v1.json': 'efc0b7cbb0df35a982367597e780024363a91192575bdb792dc8fb7df2546846',
    'W1A_ENTRY_LIST_v2.json': '224ecce138214bfbf710b29585e796b676282a5ff9d7fe2a2e881780b4c6553d',
}
REF9 = {   # m3ref_v1_15: the base family's records that C-PREP9 compares with (m3ref_v1_10, z9sym; m3_run_v1_8's pins)
    'm3ref_v1_10_V3N.4.all_z9sym.out': '65a8145b6f2ce35aa3692ab3f89447aa52c4420220408f3c028ee67bf7fdf0c2',
    'm3ref_v1_10_V3N.3.all_z9sym.out': 'd12836039cc0390feed5435486459530a781cc75865f1ecf8b95f497a0421945',
}
REF12 = {   # m3ref_v1_2's z9sym records read by C-ALIAS (MANIFEST_m3ref_v1_2_z9sym_v1 2b968a47)
    'm3ref_v1_2_mix.4.all_z9sym.out': '94a36828d07ae51af934d3a0e9e284a28df657d979bef1c2954749fe15914814',
    'm3ref_v1_2_free.4.all_z9sym.out': '9527a96047a95aeccaea52c8d2cca62d4a35d2f0d8129aed201c0ce08051d4bc',
    'm3ref_v1_2_N1.4.all_z9sym.out': '9af0ce8ef35c24d60a09e6237a5333ff513fa336d78b497da3ef193309028ee8',
    'm3ref_v1_2_mix.3.all_z9sym.out': 'ff8ce1302c4af1ae0044edf48086dec5e66f830dfb6b1d096088461b2ef67c05',
    'm3ref_v1_2_free.3.all_z9sym.out': '0d8da9258c06611ee248362d1959b917f3dd1f5ff671522ac9324441f95df2b2',
    'm3ref_v1_2_N1.3.all_z9sym.out': '1dfc0231da346454e2ac38e8e4a0c95b2fee27329544d5a4f084a518f04d4557',
}
W4 = '/mnt/g2/release/root/code/pk11/out'
VACFAM = ('vD', 'vG4r0', 'vG4r1', 'vG4r2', 'OF4', 'OF3', 'OFD', 'OFC', 'vG4ra0', 'vG4ra1', 'vG4ra2', 'vG4rb0', 'vG4rb1', 'vG4rb2', 'vDcal')
RULE = {f: (60.0, 0.5, 0.9) for f in ('vG4ra0', 'vG4ra1', 'vG4ra2', 'vG4rb0', 'vG4rb1', 'vG4rb2')}   # vacrig11w l.407: radius factor, cap, rho'
J_REF = 150.0 if FAM in VACFAM else 300.0
S_RAD, RCAP, RHO_P = RULE.get(FAM, (80.0, 0.6, 0.7))
QCAP = {'D': 6, 'N0T': 4, 'N0m': 6, 'N1': 6, 'N2': 6, 'mix': 6, 'free': 6, 'S8D': 6, 'S8N': 6, 'S8E2': 6, 'S8E3': 6,
        'S8FF': 6, 'vD': 6, 'vG4r0': 6, 'vG4r1': 6, 'vG4r2': 6, 'vG4ra0': 6, 'vG4ra1': 6, 'vG4ra2': 6, 'vG4rb0': 6, 'vG4rb1': 6, 'vG4rb2': 6, 'vDcal': 6, 'S8L': 6, 'S8H': 6, 'S8S4': 6, 'S8L16': 6, 'S8H16': 6, 'S8S416': 6, 'U16L': 6, 'U16H': 6, 'U16S4': 6, 'P16H': 6, 'P16S4': 6,
        'S8Hc': 6, 'S8E3c': 6, 'S8E2c': 6, 'S8FFc': 6, 'S8S4c': 6,
        'V3D': 6, 'V3N': 6, 'V3E2': 6, 'V3E3': 6, 'V3FF': 6,
        'V4NK': 6, 'V4E3K': 6, 'V4F3': 6, 'V9I': 6, 'P16T1': 6, 'P16T1N': 6, 'P16T2': 6, 'P16T2N': 6, 'P16BD2T': 6, 'P16BE2T': 6, 'P16BE3T': 6, 'P16BH4T': 6, 'P16BL': 6, 'P16BN2T': 6, 'P16BT1MN': 6, 'P16CS4': 6, 'P16CE3': 6, 'P16CH4T': 6, 'P16CE2T': 6, 'P16CE3H': 6, 'P16CS4H': 6, 'P16CH4TH': 6, 'P16E4D': 6, 'P16E4N': 6, 'P16L': 6}


def strip_graph(ncols, end_ab, mid_c=1.0):
    """3-row strip with ncols columns; end columns are triangles with couplings (a, a, b) (T-M, M-B, T-B); interior columns verticals mid_c;
    horizontals 1.  Vertex id = 3*col + row (row 0 = T, 1 = M, 2 = B)."""
    a, b = end_ab
    E = {}
    for j in range(ncols):
        T, Mv, B = 3 * j, 3 * j + 1, 3 * j + 2
        if j == 0 or j == ncols - 1:
            E[(T, Mv)] = a; E[(Mv, B)] = a
            if b > 0:
                E[(T, B)] = b
        else:
            E[(T, Mv)] = mid_c; E[(Mv, B)] = mid_c
        if j < ncols - 1:
            for r in range(3):
                E[(3 * j + r, 3 * (j + 1) + r)] = 1.0
    return 3 * ncols, E


A_EX = (3 + math.sqrt(21)) / 6
B_EX = (3 * math.sqrt(5) - math.sqrt(21)) / 12
a, b = A_EX, B_EX
H = {(0, 3): 1.0, (1, 4): 1.0, (2, 5): 1.0}
Emix = dict(H); Emix.update({(0, 1): a, (1, 2): a, (0, 2): b, (3, 4): 1.0, (4, 5): 1.0})
Efree = dict(H); Efree.update({(0, 1): 1.0, (1, 2): 1.0, (3, 4): 1.0, (4, 5): 1.0})


def read_bytes(path):
    with open(path, 'rb') as fh:
        return fh.read()


def sha(bts):
    return hashlib.sha256(bts).hexdigest()


def src_lines(path, lo, hi):
    """lines lo..hi (1-based, inclusive) of a text file, as one string with newlines."""
    lines = read_bytes(path).decode('utf-8').split('\n')
    return '\n'.join(lines[lo - 1:hi]) + '\n'


def own_lines(first, count):
    """the count lines of this file that start at the first line equal to `first` ('' if absent)."""
    lines = read_bytes(os.path.abspath(__file__)).decode('utf-8').split('\n')
    for i, ln in enumerate(lines):
        if ln == first:
            return '\n'.join(lines[i:i + count]) + '\n'
    return ''


FAILS, NOFIRE = [], []


def gate(name, ok, line):
    out('%s %s -> %s' % (name, line, 'PASS' if ok else 'FAIL'))
    if not ok:
        FAILS.append(name)


def plant(name, fired, line):
    out('%s %s -> %s' % (name, line, 'FIRES' if fired else 'DOES NOT FIRE'))
    if not fired:
        NOFIRE.append(name)


def finish(extra=''):
    out('STAGE-CPU total %.2f s' % cpu())
    if FAILS or NOFIRE:
        out('VERDICT INVALID (%s)' % ', '.join(FAILS + ['%s did not fire' % p for p in NOFIRE]) + extra)
    else:
        out('VERDICT VALID' + extra)


out('m3ref_v1_15 item %s LIM %d; python %s' % (sys.argv[1], LIM, sys.version.split()[0]))
STAGE[0] = 'C-COPY'
bad = [f for f, h in PINNED.items() if sha(read_bytes(os.path.join(PIN, f))) != h]
gate('C-COPY', not bad, '(%d pinned copies in %s)%s' % (len(PINNED), PIN, (': ' + ', '.join(bad)) if bad else ''))
plant('PLANT-COPY', sha(read_bytes(os.path.join(PIN, 'riglap2.py')) + b'#') != PINNED['riglap2.py'], '(riglap2 bytes plus one byte)')
STAGE[0] = 'C-SRC'
bad = [f for f, h in SRCFILES.items() if sha(read_bytes(os.path.join(SCR, f))) != h]
pairs_src = [('strip_graph', src_lines(os.path.join(SCR, 'lapl2.py'), 63, 79), inspect.getsource(strip_graph)),
             ('A_EX, B_EX', src_lines(os.path.join(SCR, 'vacmod2.py'), 8, 9), own_lines('A_EX = (3 + math.sqrt(21)) / 6', 2)),
             ('endw couplings', src_lines(os.path.join(SCR, 'endw.py'), 16, 19), own_lines('a, b = A_EX, B_EX', 4))]
VSRC = os.path.join(SCR, 'vacrig11f.py')
pairs_src += [('vacrig11f lap', src_lines(VSRC, 166, 170), own_lines('def lap(edges, V):', 5)),
              ('vacrig11f gauge_basis', src_lines(VSRC, 173, 175), own_lines('def gauge_basis(V, S):', 3)),
              ('vacrig11f tilted_cov', src_lines(VSRC, 178, 186), own_lines('def tilted_cov(L, Bm, rates, extra=None):', 9)),
              ('vacrig11f ED_', src_lines(VSRC, 196, 197), own_lines("ED_ = [((r, s), [a, a, b][p_]) for p_, (r, s) in enumerate(PAIRS)] + "
                                                                     "[((3 + r, 3 + s), [a, a, b][p_]) for p_, (r, s) in enumerate(PAIRS)] + \\", 2)),
              ('vacrig11f E4, E3', src_lines(VSRC, 240, 244), own_lines("E4 = [((r, s), [a, a, b][p_]) for p_, (r, s) in enumerate(PAIRS)] + "
                                                                       "[((9 + r, 9 + s), [a, a, b][p_]) for p_, (r, s) in enumerate(PAIRS)] + \\", 5)),
              ('vacrig11f C_P', src_lines(VSRC, 247, 247), own_lines('C_P = -math.log(1 - A_P) / (2 * A_P)', 1)),
              ('vacrig11f outer_far', src_lines(VSRC, 250, 287), own_lines('def outer_far(edges, V, S, pcols, J):', 38)),
              ('vacmod2 PAIRS, BASIS', src_lines(os.path.join(SCR, 'vacmod2.py'), 12, 13), own_lines('PAIRS = [(0, 1), (1, 2), (0, 2)]', 2)),
              ('riglap5s Prep5s l.22-34 with dmaxH', src_lines(os.path.join(PIN, 'riglap5s.py'), 22, 34).replace(', 18)', ', dmaxH)'),
               own_lines('        if not self.ok:', 13))]
diff = [lab for lab, ref, mine in pairs_src if ref != mine]
gate('C-SRC', not bad and not diff, '(lapl2 l.63-79, vacmod2 l.8-9 and l.12-13, endw l.16-19, vacrig11f l.166-170, 173-175, 178-186, 196-197, 240-244, 247, 250-287, riglap5s l.22-34 (C-SRC-H) against this file; source shas)%s' % (
    (': ' + ', '.join(bad + diff)) if (bad or diff) else ''))
ref0 = pairs_src[0][1]
k0 = ref0.index('ncols')
plant('PLANT-SRC', (ref0[:k0] + 'Ncols' + ref0[k0 + 5:]) != pairs_src[0][2], '(strip_graph text with one character changed)')
STAGE[0] = 'C-HASH'
bad = [f for f, h in INPUTS.items() if sha(read_bytes(os.path.join(INP, f))) != h]
bad += [f for f, h in INPUTS_W4.items() if sha(read_bytes(os.path.join(W4, f))) != h]
bad += [f for f, h in INPUTS_S8.items() if sha(read_bytes(os.path.join(W4, f))) != h]
bad += [f for f, h in INPUTS_S9.items() if sha(read_bytes(os.path.join(OWN, f))) != h]
bad += [f for f, h in INPUTS_W1A.items() if sha(read_bytes(os.path.join(MYD, f))) != h]   # pk22 copy
bad += [f for f, h in INPUTS_PSX.items() if sha(read_bytes(os.path.join(os.path.dirname(MYD), 'midrow', 'psixy', f))) != h]   # pk22 v1_7
bad += [f for f, h in INPUTS_HL.items() if sha(read_bytes(os.path.join(HLD, f))) != h]   # pk23 hl_v1
bad += [f for f, h in REF9.items() if sha(read_bytes(os.path.join(OWN, 'out', f))) != h]
bad += [f for f, h in REF12.items() if sha(read_bytes(os.path.join(OWN, 'out', f))) != h]
gate('C-HASH', not bad, '(%d pk10 inputs and J = 170 records, %d trial files and %d S8 lists in pk11/out, %d m3ref_v1_2 records, '
     'the S9 list and %d m3ref_v1_10 base records)%s' % (
    len(INPUTS), len(INPUTS_W4), len(INPUTS_S8), len(REF12), len(REF9), (': ' + ', '.join(bad)) if bad else ''))
h0 = INPUTS['vacres_K3_N4.json']
plant('PLANT-HASH', sha(read_bytes(os.path.join(INP, 'vacres_K3_N4.json'))) != h0[:-1] + ('0' if h0[-1] != '0' else '1'),
      '(vacres_K3_N4 against a sha with its last digit changed)')
if FAILS or NOFIRE:
    finish(' before the engines were imported')
    sys.exit(1)

sys.path.insert(0, PIN)
import numpy as np
import scipy
from scipy.special import ive
import amom2b, npoly, pseries
import riglap2, riglap4, riglap5, riglap5b, riglap5r, riglap5s
from riglap2 import Graph
out('versions: numpy %s, scipy %s; engines from %s' % (np.__version__, scipy.__version__, os.path.dirname(riglap5s.__file__)))
if os.path.dirname(os.path.abspath(riglap5s.__file__)) != PIN or os.path.dirname(os.path.abspath(amom2b.__file__)) != PIN:
    gate('C-COPY import path', False, '(the engines did not load from the pinned folder)')
    finish()
    sys.exit(1)


def npguard_fires():
    """riglap5b's NPoly carry guard on a product that would carry (x^3 times x^2 in base 4)."""
    try:
        npoly.NPoly.from_dict({(3, 0): 1.0}, 2, 4).mul(npoly.NPoly.from_dict({(2, 0): 1.0}, 2, 4))
        return False
    except AssertionError:
        return True


plant('PLANT-NPGUARD', npoly.NPoly.mul is riglap5b._guarded_mul and npguard_fires(), '(riglap5b\'s guarded NPoly product is installed and '
      'refuses x^3 times x^2 in base 4)')

# PROFILE: cumulative CPU and calls of the moment tables, expectations and polynomial products (numerics untouched)
PROF = {}


def timed(label, fn):
    def wrapper(*args, **kw):
        t = cpu()
        try:
            return fn(*args, **kw)
        finally:
            c, s = PROF.get(label, (0, 0.0))
            PROF[label] = (c + 1, s + cpu() - t)
    return wrapper


amom2b.AllMom2.__init__ = timed('AllMom2.init', amom2b.AllMom2.__init__)
amom2b.AllMom2.E = timed('AllMom2.E', amom2b.AllMom2.E)
amom2b.AllMom2.E2 = timed('AllMom2.E2', amom2b.AllMom2.E2)
_init_timed = amom2b.AllMom2.__init__


def _init_logged(self, *a, **k):
    """m3ref_v1_12: a TABLE-START line before and a TABLE-BUILD line after every moment table of degree >= 13 (the D-16 probe's
    measured build times), printed at once."""
    dg = a[2] if len(a) > 2 else k.get('D', 0)
    t0 = cpu()
    if dg >= 13:
        out('TABLE-START D %d (cpu so far %.1f s)' % (dg, t0))
    _init_timed(self, *a, **k)
    if dg >= 13:
        out('TABLE-BUILD D %d F %d moments %d: %.2f s (cpu so far %.1f s)' % (dg, self.F, sum(len(c) for c in self.codes), cpu() - t0, cpu()))


amom2b.AllMom2.__init__ = _init_logged
npoly.NPoly.mul = timed('NPoly.mul', npoly.NPoly.mul)
_tp = timed('pmul', pseries.pmul)
for _m in (pseries, riglap2, riglap4, riglap5, riglap5b, riglap5r, riglap5s):
    if hasattr(_m, 'pmul'):
        _m.pmul = _tp


def prof_line(tag):
    out('PROFILE %s %s' % (tag, json.dumps({k: [v[0], round(v[1], 2)] for k, v in sorted(PROF.items())})))


def wload(name):
    with open(os.path.join(W4, name)) as fh:
        return json.load(fh)


def pload(name):   # pk22 v1_7: the z9symxy trial files
    with open(os.path.join(os.path.dirname(MYD), 'midrow', 'psixy', name)) as fh:
        return json.load(fh)


def cluster_key(name):
    parts = name.split(',')
    return name[0] in 'gTA' and len(parts) > 1 and any(int(x) >= 1 for x in parts[1:])


def jload(name):
    with open(os.path.join(INP, name)) as fh:
        return json.load(fh)


R3 = jload('vacres_K3_N%d.json' % NN) if TRIAL == 'ts0' else wload('vacres_K3_N%d_sym_v1.json' % NN)
S = np.array((jload({4: 'ts_N4_J170_D_S.json', 3: 'ts_N3_S.json'}[NN]) if TRIAL == 'ts0' else
              (pload({4: 'ts_N4_J170_D_S_z9symxy_v1.json', 3: 'ts_N3_S_z9symxy_v1.json'}[NN]) if TRIAL == 'z9symxy' else
               wload({4: 'ts_N4_J170_D_S_z9sym_v1.json', 3: 'ts_N3_S_z9sym_v1.json'}[NN])))['S'])   # pk22 v1_7: z9symxy
M2B = jload('m2_N%d_J170.json.b' % NN)
KBAR = M2B['kbar']
REC = {'m2': M2B['items'], 'b5': jload('b5_N%d_J170.json' % NN)['items'], 'clT': jload('clT_N%d_J170.json' % NN)['items'],
       'binding4': {'I_N': jload('binding4_N%d_J170.json' % NN)['I_N']}, 'endw': jload('endw_N%d_J170.json' % NN)['items']}
ENDW_RMAIN = jload('endw_N%d_J170.json' % NN)['r_main']
out('TRIAL %s' % TRIAL)
out('inputs: N = %d, kbar %r (m2_N%d_J170.json.b), trial set %s, %s' % (
    NN, KBAR, NN, ({4: 'ts_N4_J170_D_S.json', 3: 'ts_N3_S.json'}[NN] if TRIAL == 'ts0' else {4: 'ts_N4_J170_D_S_z9symxy_v1.json', 3: 'ts_N3_S_z9symxy_v1.json'}[NN] if TRIAL == 'z9symxy' else {4: 'ts_N4_J170_D_S_z9sym_v1.json', 3: 'ts_N3_S_z9sym_v1.json'}[NN]),
    ('vacres_K3_N%d.json' % NN) if TRIAL == 'ts0' else ('vacres_K3_N%d_sym_v1.json' % NN)))


_r = riglap2
from riglap4 import norm_any
from pseries import pmul
DMAXH = {'vG4r0': 12, 'vG4r1': 12, 'vG4r2': 12, 'vG4ra0': 12, 'vG4ra1': 12, 'vG4ra2': 12, 'vG4rb0': 14, 'vG4rb1': 14, 'vG4rb2': 14,
         'S8L': 12, 'S8H': 12, 'S8S4': 12, 'S8L16': 16, 'S8H16': 16, 'S8S416': 16, 'P16H': 16, 'P16S4': 16, 'S8Hc': 12, 'S8S4c': 12, 'P16T1': 16, 'P16T1N': 16, 'P16T2': 16, 'P16T2N': 16, 'P16BD2T': 16, 'P16BE2T': 16, 'P16BE3T': 16, 'P16BH4T': 16, 'P16BL': 16, 'P16BN2T': 16, 'P16BT1MN': 16, 'P16CS4': 16, 'P16CE3': 16, 'P16CH4T': 16, 'P16CE2T': 16, 'P16CE3H': 16, 'P16CS4H': 16, 'P16CH4TH': 16, 'P16E4D': 16, 'P16E4N': 16, 'P16L': 16}


class Prep5sH(riglap5s.Prep5s):
    """riglap5s.Prep5s with its degree cap as the parameter dmaxH: its l.22-34 with the literal 18 replaced by dmaxH (C-SRC-H); norms above
    dmaxH take riglap4's Hoelder fallback, as riglap5b.Prep5 already does for its own norms."""
    def __init__(self, g, J, rho, rho_p, key="g", qcap=4, dmaxH=18):
        riglap5r.Prep5r.__init__(self, g, J, rho, rho_p, key=key, dmaxH=dmaxH, qcap=qcap)
        if not self.ok:
            return
        t, n, W = self.t, g.n, g.W
        mjH = _r.Majorants(_r.Model(g, 3, []), self.a_v, t, B=riglap5b.NPOLY_B)
        h2 = mjH.hbar(2).to_dict()
        H1 = self.Ej[1]
        kH, kc = key + "|H", key + "|c%.10g" % t
        ex = t ** 6 / 48 * norm_any(pmul(h2, pmul(h2, h2)), g.G, n, W, 2, kH, dmaxH)
        tr = self.rE_parts["t5 h2^2 hhat/24"]
        self.rE_parts["E2^3 term"] = min(ex, tr)
        del self.rE_parts["t5 h2^2 hhat/24"]
        self.rE = sum(self.rE_parts.values())
        self.nC6 = t * norm_any(H1, self.Gc, n, W, 6, kc, dmaxH) + t * t / 2 * norm_any(h2, self.Gc, n, W, 6, kc, dmaxH)


# ------------------------------------------------------------------ outer_far float reference (m3ref_v1_4): vacrig11f's pieces, verbatim
from amom2b import AllMom2
nn = NN - 1
q = [None, R3["q1"], R3["q2"], R3["q3"]]
a_m = 0.55 ** 2                                            # vacrig11f: a_m = rho_m ** 2, rho_m 0.55 (vacrig11_N4.txt's banner)
A_P = 0.9 ** 2                                             # vacrig11f l.245-246: RHO_P = 0.9, A_P = RHO_P ** 2
C_P = -math.log(1 - A_P) / (2 * A_P)
PAIRS = [(0, 1), (1, 2), (0, 2)]
BASIS = [(0,), (1,), (2,), (0, 0), (1, 1), (2, 2), (0, 1), (1, 2), (0, 2)]


def lap(edges, V):
    L = np.zeros((V, V))
    for (u, v), c in edges:
        L[u, u] += c; L[v, v] += c; L[u, v] -= c; L[v, u] -= c
    return L


def gauge_basis(V, S):
    u = np.zeros(V); u[list(S)] = 1.0
    return np.linalg.svd(np.eye(V) - np.outer(u, u) / u.dot(u))[0][:, :V - 1]


def tilted_cov(L, Bm, rates, extra=None):
    Lr = Bm.T @ L @ Bm
    Lx = L - 2 * np.diag(rates)
    if extra is not None:
        Lx = Lx - 2 * extra
    Lt = Bm.T @ Lx @ Bm
    if np.linalg.eigvalsh(Lt).min() <= 0:
        return None, float("inf")
    return Bm @ np.linalg.inv(Lt) @ Bm.T, (np.linalg.det(Lr) / np.linalg.det(Lt)) ** (0.5 * nn)


ED_ = [((r, s), [a, a, b][p_]) for p_, (r, s) in enumerate(PAIRS)] + [((3 + r, 3 + s), [a, a, b][p_]) for p_, (r, s) in enumerate(PAIRS)] + \
      [((r, 3 + r), 1.0) for r in range(3)]
E4 = [((r, s), [a, a, b][p_]) for p_, (r, s) in enumerate(PAIRS)] + [((9 + r, 9 + s), [a, a, b][p_]) for p_, (r, s) in enumerate(PAIRS)] + \
     [((r, 3 + r), 1.0) for r in range(3)] + [((3 + r, 6 + r), 1.0) for r in range(3)] + [((6 + r, 9 + r), 1.0) for r in range(3)] + \
     [((3, 4), 1.0), ((4, 5), 1.0), ((6, 7), 1.0), ((7, 8), 1.0)]
E3 = [((r, s), [a, a, b][p_]) for p_, (r, s) in enumerate(PAIRS)] + [((6 + r, 6 + s), [a, a, b][p_]) for p_, (r, s) in enumerate(PAIRS)] + \
     [((r, 3 + r), 1.0) for r in range(3)] + [((3 + r, 6 + r), 1.0) for r in range(3)] + [((3, 4), 1.0), ((4, 5), 1.0)]


def outer_far(edges, V, S, pcols, J):
    """bound, relative to the graph's main term, of the integral with |p| on pcols over {some v in S with |pi_v| > rho_m (S-gauge pole)}:
    chart part (all |pi| <= rho'): E_{S-gauge}[e^{c' t sum X} pbar pbar' e^{lam (X_v - J a_m)}] summed over v in S (Chernoff);
    truly far part (some |pi_v| > rho' or lower hemisphere): sup|p|^2 x per-vertex energy (S-gauge variances), theta-split, tree bound."""
    t = 1.0 / J
    L = lap(edges, V)
    Bm_ = gauge_basis(V, S)
    pairs = []
    for c_ in pcols:
        pairs += [(c_[0], c_[1]), (c_[1], c_[2]), (c_[0], c_[2])]
    g_ = riglap2.Graph(V, dict(edges), pairs, N=NN)
    m_ = riglap2.Model(g_, 3, [('p', c_, q[1], q[2], q[3]) for c_ in pcols])
    mj_ = riglap2.Majorants(m_, [A_P] * V, t, B=10)
    P0 = mj_.Fbar(0)
    degP = int(P0.degrees().max())
    qP = int(np.stack([(P0.codes // P0.pw[i]) % P0.B for i in range(P0.nv)], axis=1)[:, V:].sum(axis=1).max())
    best = float("inf")
    for lam in (0.5, 1.0, 1.5):
        acc = 0.0; ok = True
        for v in S:
            rates = np.full(V, C_P * t); rates[v] += lam
            G_, N_ = tilted_cov(L, Bm_, rates)
            if G_ is None:
                ok = False; break
            am_ = AllMom2(G_, nn, max(degP, 1), W=g_.W, groups=g_.groups, caps={1: max(qP, 1)})
            acc += math.exp(-lam * J * a_m) * N_ * riglap2.expect_np(am_, P0)
        if ok:
            best = min(best, acc)
    GS = Bm_ @ np.linalg.inv(Bm_.T @ L @ Bm_) @ Bm_.T
    tree = riglap2.tree_couplings(g_)
    if NN == 4:
        lt = lambda Jp: sum(math.log(2.0 * ive(1, Jp * c) / (Jp * c)) for c in tree)
    else:
        lt = lambda Jp: sum(math.log(-math.expm1(-2 * Jp * c) / (2 * Jp * c)) for c in tree)
    farp = math.exp(min(math.log(sum(math.exp(-th * J * A_P / (2 * GS[v, v])) for v in range(V))) + lt((1 - th) * J) - g_.logmain(J)
                        for th in np.linspace(0.01, 0.99, 197)))
    supp_ = 1.0 + sum(t ** i * abs(cb) * (2.0 * J) ** len(mono_) for i, coef in ((1, q[1]), (2, q[2]), (3, q[3])) for cb, mono_ in zip(coef, BASIS))
    return best + supp_ ** len(pcols) * farp


OFSPEC = {'OF4': ('E4', 12, list(range(3, 9)), [(0, 1, 2), (9, 10, 11)]), 'OF3': ('E3', 9, list(range(3, 9)), [(0, 1, 2), (6, 7, 8)]),
          'OFD': ('ED_', 6, list(range(6)), [(0, 1, 2), (3, 4, 5)])}       # vacrig11f l.389-390


def outer_far_parts(edges, V, S, pcols, J):
    """vacrig11f.outer_far with its parts kept: the same arithmetic in the same order (C-OF-SAME), plus lam*, theta*, the S-gauge
    variances and the far law's rate r = min_v theta* A_P/(2 GS_vv) - n(V - 1)/(2 J) (PLAN_M3_CODE_v1_2_ADD4 sect. 4)."""
    t = 1.0 / J
    L = lap(edges, V)
    Bm_ = gauge_basis(V, S)
    pairs = []
    for c_ in pcols:
        pairs += [(c_[0], c_[1]), (c_[1], c_[2]), (c_[0], c_[2])]
    g_ = riglap2.Graph(V, dict(edges), pairs, N=NN)
    m_ = riglap2.Model(g_, 3, [('p', c_, q[1], q[2], q[3]) for c_ in pcols])
    mj_ = riglap2.Majorants(m_, [A_P] * V, t, B=10)
    P0 = mj_.Fbar(0)
    degP = int(P0.degrees().max())
    qP = int(np.stack([(P0.codes // P0.pw[i]) % P0.B for i in range(P0.nv)], axis=1)[:, V:].sum(axis=1).max())
    best = float("inf")
    accs, lam_star = {}, None
    for lam in (0.5, 1.0, 1.5):
        acc = 0.0; ok = True
        for v in S:
            rates = np.full(V, C_P * t); rates[v] += lam
            G_, N_ = tilted_cov(L, Bm_, rates)
            if G_ is None:
                ok = False; break
            am_ = AllMom2(G_, nn, max(degP, 1), W=g_.W, groups=g_.groups, caps={1: max(qP, 1)})
            acc += math.exp(-lam * J * a_m) * N_ * riglap2.expect_np(am_, P0)
        accs[str(lam)] = acc if ok else None
        if ok:
            if acc < best:
                lam_star = lam
            best = min(best, acc)
    GS = Bm_ @ np.linalg.inv(Bm_.T @ L @ Bm_) @ Bm_.T
    tree = riglap2.tree_couplings(g_)
    if NN == 4:
        lt = lambda Jp: sum(math.log(2.0 * ive(1, Jp * c) / (Jp * c)) for c in tree)
    else:
        lt = lambda Jp: sum(math.log(-math.expm1(-2 * Jp * c) / (2 * Jp * c)) for c in tree)
    ths = np.linspace(0.01, 0.99, 197)
    vals = [math.log(sum(math.exp(-th * J * A_P / (2 * GS[v, v])) for v in range(V))) + lt((1 - th) * J) - g_.logmain(J) for th in ths]
    farp = math.exp(min(vals))
    th_star = float(ths[int(np.argmin(vals))])
    supp_ = 1.0 + sum(t ** i * abs(cb) * (2.0 * J) ** len(mono_) for i, coef in ((1, q[1]), (2, q[2]), (3, q[3])) for cb, mono_ in zip(coef, BASIS))
    value = best + supp_ ** len(pcols) * farp
    r = min(th_star * A_P / (2 * GS[v, v]) for v in range(V)) - nn * (V - 1) / 2 / J
    return {'V': V, 'S': list(S), 'pcols': [list(c_) for c_ in pcols], 'edges': [[list(e), c] for e, c in edges], 'degP': degP, 'qP': qP,
            'chart_per_lam': accs, 'lam_star': lam_star, 'chart': best, 'farp': farp, 'theta_star': th_star, 'supp': supp_,
            'far': supp_ ** len(pcols) * farp, 'value': value, 'GS_diag': [float(GS[v, v]) for v in range(V)], 'r': r, 'tree': list(tree),
            'J': J, 'a_m': a_m, 'A_P': A_P, 'C_P': C_P}


def run_of(fam):
    """one graph's float outer_far at J_REF = 150: OFJSON, C-OF-SAME (the parts' value equals vacrig11f's outer_far exactly), C-OF-LAM
    (some lam tilt certainly positive definite), C-OF-LAW-INFO (lam* >= 0.5 and r >= 0.5 a_m in floating point; the certified run gates
    them)."""
    name, V, Sg, pcols = OFSPEC[fam]
    edges = {'E4': E4, 'E3': E3, 'ED_': ED_}[name]
    STAGE[0] = 'outer_far parts %s' % name
    t1 = cpu()
    d = outer_far_parts(edges, V, Sg, pcols, J_REF)
    dt1 = cpu() - t1
    STAGE[0] = 'outer_far %s (vacrig11f text)' % name
    t2 = cpu()
    ref = outer_far(edges, V, Sg, pcols, J_REF)
    dt2 = cpu() - t2
    d.update({'graph': name, 'N': NN, 'trial': TRIAL, 'cpu_parts': round(dt1, 2), 'cpu_ref': round(dt2, 2)})
    out('OFJSON ' + json.dumps(d))
    gate('C-OF-SAME', d['value'] == ref, '(%s: outer_far_parts value %r, vacrig11f.outer_far %r)' % (name, d['value'], ref))
    plant('PLANT-OF-SAME', not (d['value'] * (1 + 1e-12) == ref), '(the parts value times 1 + 1e-12)')
    gate('C-OF-LAM', d['lam_star'] is not None, '(%s: lam* %r; chart per lam %s)' % (name, d['lam_star'], json.dumps(d['chart_per_lam'])))
    out('C-OF-LAW-INFO %s: lam* %r (>= 0.5), r %.6e against 0.5 a_m %.6e; chart %.6e, far %.6e (theta* %r, supp %.6f), value %.6e' % (
        name, d['lam_star'], d['r'], 0.5 * a_m, d['chart'], d['far'], d['theta_star'], d['supp'], d['value']))


def run_ofc():
    """C-REP-VAC: far_out = o4 + 2 mhat o3 + mhat^2 oD at J 150 (vacrig11f l.389-390) from this script's OF4, OF3 and OFD outputs of the
    same N and TRIAL (each VERDICT lines exactly ['VERDICT VALID']); N = 4 with TRIAL ts0 (vacrig11's own inputs) must round to
    vacrig11_N4.txt's two-digit 7.2e-11: 7.15e-11 <= far_out < 7.25e-11 (PLANT-REP-VAC: far_out times 1.02 must leave it)."""
    vals = {}
    for fam in ('OF4', 'OF3', 'OFD'):
        p = os.path.join(OWN, 'out', 'm3ref_v1_11_%s.%d.all_%s.out' % (fam, NN, TRIAL))
        lines = read_bytes(p).decode('utf-8').split('\n')
        okv = [ln for ln in lines if ln.startswith('VERDICT')] == ['VERDICT VALID']
        js = [json.loads(ln[len('OFJSON '):]) for ln in lines if ln.startswith('OFJSON ')]
        gate('C-OFC-IN', okv and len(js) == 1, '(%s, sha256 %s: VERDICT lines exactly [VERDICT VALID], one OFJSON)' % (os.path.basename(p), sha(read_bytes(p))))
        vals[fam] = js[0]['value'] if js else float('nan')
    t = 1.0 / J_REF
    mser = [1.0, R3["m1"], R3["m2"], R3["m3"]]
    mhat = 1.0 + mser[1] * t + mser[2] * t ** 2 + mser[3] * t ** 3
    far_out = vals['OF4'] + 2 * mhat * vals['OF3'] + mhat ** 2 * vals['OFD']
    win = lambda x: 7.15e-11 <= x < 7.25e-11
    if NN == 4 and TRIAL == 'ts0':
        txt = read_bytes(os.path.join(INP, 'vacrig11_N4.txt')).decode('utf-8')
        m = re.search(r'J =\s+150\.0: .* far_out (\S+) ', txt)
        gate('C-REP-VAC', m is not None and m.group(1) == '7.2e-11' and win(far_out) and ('%.1e' % far_out) == m.group(1),
             '(far_out %.6e = o4 %.4e + 2 mhat o3 %.4e + mhat^2 oD %.4e, mhat %.9f; vacrig11_N4.txt far_out %s)' % (
                 far_out, vals['OF4'], 2 * mhat * vals['OF3'], mhat ** 2 * vals['OFD'], mhat, m.group(1) if m else None))
        plant('PLANT-REP-VAC', not win(far_out * 1.02), '(far_out times 1.02)')
    else:
        out('C-REP-VAC-INFO N=%d TRIAL %s: far_out %.6e = o4 %.4e + 2 mhat o3 %.4e + mhat^2 oD %.4e (mhat %.9f)' % (
            NN, TRIAL, far_out, vals['OF4'], 2 * mhat * vals['OF3'], mhat ** 2 * vals['OFD'], mhat))
    out('OFCJSON ' + json.dumps({'N': NN, 'trial': TRIAL, 'mhat': mhat, 'o4': vals['OF4'], 'o3': vals['OF3'], 'oD': vals['OFD'], 'far_out': far_out}))


def pv(col):
    return ('p', col, R3["q1"], R3["q2"], R3["q3"])


def cpoly(al, col):
    return pv(col) if al == 0 else ('xi', col, float(S[0, al]), [float(x) for x in S[1:, al]])


def delta(col):
    return ('xi', col, 0.0, [0.5, -0.5] + [0.0] * 7)


def xia(col):
    return ('xi', col, 0.0, [1.0] + [0.0] * 8)


def xip(col, c0=0.0):
    return ('xi', col, c0, [0.5, 0.5] + [0.0] * 7)


# ------------------------------------------------------------------ S8 families (m3ref_v1_3)
S8LIST = {}
S8FAM = {'S8D': ('v2', 'D', r'DY'), 'S8N': ('v1_1', 'N', r'T[XY],'), 'S8E2': ('v1_1', 'E2', r'eX?,'), 'S8E3': ('v1_1', 'E3', r'fX?,'),
         'S8FF': ('v1_1', 'FF', r'(z|wXw|wXwX)$'),
         'S8L': ('v2', 'L', r'TT,'), 'S8H': ('v2', 'H', r'hX?,'), 'S8S4': ('v2', 'S4', r'S4,'),
         'S8L16': ('v2', 'L', r'TT,'), 'S8H16': ('v2', 'H', r'hX?,'), 'S8S416': ('v2', 'S4', r'S4,'),
         'P16H': ('v2', 'H', r'hX?,'), 'P16S4': ('v2', 'S4', r'S4,'),
         'S8Hc': ('v2', 'H', r'hX?,'), 'S8E3c': ('v1_1', 'E3', r'fX?,'), 'S8E2c': ('v1_1', 'E2', r'eX?,'),
         'S8FFc': ('v1_1', 'FF', r'(z|wXw|wXwX)$'), 'S8S4c': ('v2', 'S4', r'S4,'),
         'V3D': ('v3', 'D', r''), 'V3N': ('v3', 'N', r''), 'V3E2': ('v3', 'E2', r''), 'V3E3': ('v3', 'E3', r''), 'V3FF': ('v3', 'FF', r''),
         'V4NK': ('v4', 'N', r'TXX,'), 'V4E3K': ('v4', 'E3', r'fXX,'), 'V4F3': ('v4', 'F3', r''),
         'V9I': ('s9', 'I9', r''),
         'P16T1': ('w1a', 'T1', r''), 'P16T1N': ('w1a', 'T1n', r''), 'P16T2': ('w1a', 'T2', r''), 'P16T2N': ('w1a', 'T2n', r''),   # pk22
         'P16BD2T': ('b', 'D2T', r''), 'P16BE2T': ('b', 'E2T', r''), 'P16BE3T': ('b', 'E3T', r''), 'P16BH4T': ('b', 'H4T', r''), 'P16BL': ('b', 'L', r''), 'P16BN2T': ('b', 'N2T', r''), 'P16BT1MN': ('b', 'T1MN', r''),   # pk22 v1_2: B
         'P16CS4': ('c', 'CS4', r''), 'P16CE3': ('c', 'CE3', r''), 'P16CH4T': ('c', 'H4T', r''), 'P16CE2T': ('c', 'E2T', r''),   # pk22 v1_4: c3
         'P16CE3H': ('c3h', 'CE3H', r''), 'P16CS4H': ('c3h', 'CS4H', r''), 'P16CH4TH': ('c3h', 'H4TH', r''),   # pk22 v1_6: c3h
         'P16E4D': ('c3k', 'E4D', r''), 'P16E4N': ('c3k', 'E4N', r''),   # pk22 v1_7: c3k
         'P16L': ('hl', 'L', r'')}   # pk23 hl_v1: S8's L graph from pk23's list
NPB4 = {'S8L': 11, 'S8H': 15, 'S8S4': 9, 'S8L16': 11, 'S8H16': 15, 'S8S416': 9, 'P16H': 15, 'P16S4': 9, 'S8Hc': 15, 'S8S4c': 9, 'V3N': 15, 'V3E3': 16, 'V4NK': 15, 'V4E3K': 16, 'V4F3': 16, 'V9I': 15, 'P16T1': 16, 'P16T1N': 16, 'P16T2': 16, 'P16T2N': 16, 'P16BD2T': 16, 'P16BE2T': 16, 'P16BE3T': 16, 'P16BH4T': 15, 'P16BL': 11, 'P16BN2T': 12, 'P16BT1MN': 16, 'P16CS4': 11, 'P16CE3': 15, 'P16CH4T': 13, 'P16CE2T': 16, 'P16CE3H': 28, 'P16CS4H': 22, 'P16CH4TH': 13, 'P16E4D': 28, 'P16E4N': 13, 'P16L': 11}   # npoly bases for F = 18, 16, 19 forms: the largest B with B**F < 2**63 (m3ref_v1_8)
COLTYPES = {'vac': (A_EX, A_EX, B_EX), 'int': (1.0, 1.0, 0.0), 'free': (1.0, 1.0, 0.0)}
PI = {0: 1, 1: 1, 2: -1, 3: 1}
RES = {}
KEYCPU = {}


def s8_lists():
    if not S8LIST:
        for ver, fn in (('v1_1', 'S8_ENTRY_LIST_v1_1.json'), ('v2', 'S8_ENTRY_LIST_v2.json'), ('v3', 'S8_ENTRY_LIST_v3.json'), ('v4', 'S8_ENTRY_LIST_v4.json')):
            with open(os.path.join(W4, fn)) as fh:
                S8LIST[ver] = json.load(fh)
        with open(os.path.join(OWN, 'S9_ENTRY_LIST_v1.json')) as fh:   # m3ref_v1_15
            S8LIST['s9'] = json.load(fh)
        with open(os.path.join(MYD, 'W1A_ENTRY_LIST_v2.json')) as fh:   # pk22 copy
            S8LIST['w1a'] = json.load(fh)
        with open(os.path.join(MYD, 'B_ENTRY_LIST_v1.json')) as fh:   # pk22 v1_2: B's list
            S8LIST['b'] = json.load(fh)
        with open(os.path.join(MYD, 'C3_ENTRY_LIST_v2.json')) as fh:   # pk22 v1_4: c3's list
            S8LIST['c'] = json.load(fh)
        with open(os.path.join(MYD, 'C3H_ENTRY_LIST_v1.json')) as fh:   # pk22 v1_6: c3h's list
            S8LIST['c3h'] = json.load(fh)
        with open(os.path.join(MYD, 'C3K_ENTRY_LIST_v1.json')) as fh:   # pk22 v1_7: c3k's list
            S8LIST['c3k'] = json.load(fh)
        with open(os.path.join(HLD, 'HL_ENTRY_LIST_v1.json')) as fh:   # pk23 hl_v1: the L list
            S8LIST['hl'] = json.load(fh)
    return S8LIST


def graph_of(columns):
    """edges of a 3-row strip from a column-type list (pk11's conventions): vac T-M A_EX, M-B A_EX, T-B B_EX; int and free T-M 1,
    M-B 1, no T-B; horizontals 1.0 between adjacent columns. Vertex id = 3*col + row."""
    E = {}
    for j, ty in enumerate(columns):
        T, Mv, B = 3 * j, 3 * j + 1, 3 * j + 2
        tm, mb, tb = COLTYPES[ty]
        E[(T, Mv)] = tm; E[(Mv, B)] = mb
        if tb > 0:
            E[(T, B)] = tb
        if j < len(columns) - 1:
            for r in range(3):
                E[(3 * j + r, 3 * (j + 1) + r)] = 1.0
    return 3 * len(columns), E


def s8_factor(enc):
    """[cp, a, col] or [xi, TM|MB, col] as a riglap factor tuple; m3ref_v1_15: [xia, [u, v, w]], riglap3's xi factor on (u, v)."""
    if enc[0] == 'xia' and len(enc) == 2 and len(enc[1]) == 3:
        return ('xi', tuple(int(v) for v in enc[1]), 0.0, [1.0] + [0.0] * 8)
    c3 = (3 * enc[-1], 3 * enc[-1] + 1, 3 * enc[-1] + 2)
    if enc[0] == 'cp' and len(enc) == 3:
        return cpoly(enc[1], c3)
    if enc[0] == 'xi' and len(enc) == 3 and enc[1] in ('TM', 'MB'):
        c9 = [0.0] * 9
        c9[0 if enc[1] == 'TM' else 1] = 1.0
        return ('xi', c3, 0.0, c9)
    if enc[0] == 'xic' and len(enc) == 4 and enc[1] in ('TM', 'MB'):
        c9 = [0.0] * 9
        c9[0 if enc[1] == 'TM' else 1] = 1.0
        return ('xi', c3, -CONST[enc[2]], c9)
    raise ValueError('S8 factor encoding %r' % (enc,))


def s8_family(fam):
    ver, gname, pat = S8FAM[fam]
    L = s8_lists()
    spec = L[ver]['graphs'][gname]
    V, E = graph_of(spec['columns'])
    g = Graph(V, E, [tuple(p) for p in spec['pairs']], N=NN)
    keys = [(e['key'], [s8_factor(enc) for enc in e['factors']], []) for e in L[ver]['entries'] if e['graph'] == gname and re.match(pat, e['key'])]
    keys += [(k, [s8_factor(enc) for enc in encs], []) for k, encs in center_keys(fam)]
    if fam in V4FAM:
        V4REL.update({e['key']: e.get('rel_bar_max') for e in L[ver]['entries'] if e['graph'] == gname and re.match(pat, e['key'])})
    if fam in V3FAM + V4FAM:
        V3META.update({e['key']: (bool(e.get('new')), bool(e.get('parity_zero'))) for e in L[ver]['entries'] if e['graph'] == gname})
    return g, NPB4.get(fam, 12 if V == 9 else 16), keys


def rem_split(text):
    """riglap5s.bound5s's verbose line (l.80-82) as numbers."""
    m = re.search(r'overflow (\S+) F\.R_E (\S+) rho4 (\S+) \(C8 form (\S+), C6 form (\S+)\) R_F (\S+)', text)
    return None if not m else dict(zip(('overflow', 'F.R_E', 'rho4', 'rho4_C8', 'rho4_C6', 'R_F'), (float(x) for x in m.groups())))


def family(fam):
    """(graph, NPOLY_B, keys [(name, factors, [(record, key) refs])]) as the pk10 producers set them up."""
    if fam in S8FAM:
        return s8_family(fam)
    L, M, R = (0, 1, 2), (3, 4, 5), (6, 7, 8)
    if fam == 'D':
        VD, ED = strip_graph(2, (A_EX, B_EX))
        g = Graph(VD, ED, [(0, 1), (1, 2), (0, 2), (3, 4), (4, 5), (3, 5)], N=NN)
        R = (3, 4, 5)
        keys = [('g,%d,%d' % (al, be), [cpoly(al, L), cpoly(be, R)], [('b5', 'g,%d,%d' % (al, be))] + ([('m2', 'g00')] if al == be == 0 else []))
                for al in range(4) for be in range(al, 4)]
        keys += [('Ndel', [delta(L), pv(L), delta(R), pv(R)], [('b5', 'Ndel'), ('m2', 'Nd')]),
                 ('Na', [xia(L), pv(L), xia(R), pv(R)], [('b5', 'Na')]),
                 ('kn', [xip(L), pv(L), pv(R)], [('m2', 'kn')]),
                 ('Nw', [xip(L, -KBAR), pv(L), xip(R, -KBAR), pv(R)], [('m2', 'Nw')])]
        return g, 16, keys
    if fam in ('N0T', 'N0m', 'N1', 'N2'):
        VN, EN = strip_graph(3, (A_EX, B_EX))
        mid = {'N0T': [], 'N0m': [], 'N1': [(3, 4)], 'N2': [(3, 4), (4, 5)]}[fam]
        g = Graph(VN, EN, [(0, 1), (1, 2), (0, 2)] + mid + [(6, 7), (7, 8), (6, 8)], N=NN)
        if fam == 'N0T':
            keys = [('T,%d,%d' % ab, [cpoly(ab[0], L), cpoly(ab[1], R)], [('clT', 'T,%d,%d' % ab)] + ([('m2', 'T00')] if ab == (0, 0) else []))
                    for ab in ((0, 0), (0, 1), (0, 3), (1, 1), (1, 3), (3, 3), (2, 2))]
        elif fam == 'N0m':
            keys = [('I3p', [xip(L, -KBAR), pv(L), xip(R, -KBAR), pv(R)], [('m2', 'I3p')]),
                     ('I3m', [delta(L), pv(L), delta(R), pv(R)], [('m2', 'I3m')]),
                     ('I3c', [pv(L), xip(R, -KBAR), pv(R)], [('m2', 'I3c')])]
        elif fam == 'N1':
            keys = [('A,%d' % al, [cpoly(al, L), xia(M), pv(R)], [('b5', 'A,%d' % al)]) for al in range(4)]
            keys += [('Ia', [xia(L), pv(L), xia(M), pv(R)], [('b5', 'Ia')])]
        else:
            keys = [('I_N', [delta(L), pv(L), delta(M), pv(R)], [('binding4', 'I_N')]),
                    ('Ip3', [xip(L, -KBAR), pv(L), xip(M, -KBAR), pv(R)], [('m2', 'Ip3')]),
                    ('A0w', [pv(L), xip(M, -KBAR), pv(R)], [('m2', 'A0w')])]
        return g, 12, keys
    if fam == 'vD':
        VD, ED = strip_graph(2, (A_EX, B_EX))
        g = Graph(VD, ED, [(0, 1), (1, 2), (0, 2), (3, 4), (4, 5), (3, 5)], N=NN)
        return g, 16, [('D_Z2', [pv(L), pv((3, 4, 5))], [])]
    if fam[:4] == 'vG4r':
        r = int(fam[-1])
        V4, E4s = strip_graph(4, (A_EX, B_EX))
        E4r = {e: c for e, c in E4s.items() if e != (r, 3 + r)}
        assert len(E4r) == len(E4s) - 1
        return Graph(V4, E4r, [], N=NN), 16, [('G4R_%d' % r, [], [])]
    if fam == 'mix':
        return Graph(6, Emix, [(0, 1), (1, 2), (0, 2)], N=NN), 16, [('I_mix', [pv((0, 1, 2))], [('endw', 'I_mix')])]
    return Graph(6, Efree, [], N=NN), 16, [('I_free', [], [('endw', 'I_free')])]


def err_of(d):
    return d['err'] if 'err' in d else sum(d['B'].values())


def theta0(g, J, ap):
    """the grid argmin of Prep5b's far exponent (riglap5b l.67-73) and exp of its minimum."""
    Lp = np.diag(g.G)
    tree = riglap2.tree_couplings(g)
    if g.N == 4:
        logtree = lambda Jp: sum(math.log(2.0 * ive(1, Jp * c) / (Jp * c)) for c in tree)
    else:
        logtree = lambda Jp: sum(math.log(-math.expm1(-2 * Jp * c) / (2 * Jp * c)) for c in tree)
    ths = np.linspace(0.01, 0.99, 197)
    vals = [math.log(sum(math.exp(-th * J * ap / (2 * Lp[v])) for v in range(g.V))) + logtree((1 - th) * J) - g.logmain(J) for th in ths]
    i0 = int(np.argmin(vals))
    return float(ths[i0]), math.exp(vals[i0]), tree


def prep(g, J, rr, tag):
    t1 = cpu()
    STAGE[0] = 'prep J=%g' % J
    pr = (Prep5sH(g, J, rr, RHO_P, key=tag, qcap=QCAP[FAM], dmaxH=DMAXH[FAM]) if FAM in DMAXH else
          riglap5s.Prep5s(g, J, rr, RHO_P, key=tag, qcap=QCAP[FAM]))
    dt = cpu() - t1
    out('STAGE-CPU prep J=%g %.2f s (ok %s)' % (J, dt, pr.ok))
    prof_line('prep J=%g' % J)
    return pr, dt


def run_keys(g, pr, keys, J, rr, lo, hi, first_plant):
    """bound5s for keys[lo..hi]; KEYJSON lines; C-REP170 (and its plant on the first key that has a reference)."""
    done = 0
    for idx in range(lo, hi + 1):
        name, facs, refs = keys[idx]
        STAGE[0] = 'key %s J=%g' % (name, J)
        t1 = cpu()
        buf = io.StringIO()
        pr.verbose = True
        with contextlib.redirect_stdout(buf):
            ak, B = riglap5s.bound5s(pr, facs)
        pr.verbose = False
        split = rem_split(buf.getvalue())
        RES[name] = (ak, B)
        dt = cpu() - t1
        KEYCPU[name] = dt
        err = sum(B.values())
        rep = []
        for rec, rk in refs:
            d = REC[rec][rk]
            ref = d['ak']
            scale = max(abs(x) for x in ref) or 1.0
            dmax = max(abs(x - y) for x, y in zip(ak, ref)) if len(ref) == len(ak) else float('inf')
            rep.append({'record': rec, 'key': rk, 'dmax_rel': dmax / scale, 'err170': err_of(d), 'kr4_ratio': err / err_of(d)})
            if J == J_REF:
                tol = 1e-12 if TRIAL == 'ts0' else (None if cluster_key(name) else 1e-10)
                if tol is None:
                    out('C-REP170-INFO %s vs %s_N%d_J170 %s (cluster state, trial set z9sym): max|diff| %.2e, max|a_k ref| %.3e' % (
                        name, rec, NN, rk, dmax, scale))
                else:
                    gate('C-REP170', dmax <= tol * scale, '%s vs %s_N%d_J170 %s (tol %.0e): max|diff| %.2e, max|a_k ref| %.3e' % (
                        name, rec, NN, rk, tol, dmax, scale))
                if first_plant[0] and tol is not None:
                    first_plant[0] = False
                    bad = list(ref)
                    im = max(range(len(bad)), key=lambda i: abs(bad[i]))
                    bad[im] = bad[im] * (1 + 1e-6)
                    dp = max(abs(x - y) for x, y in zip(ak, bad))
                    plant('PLANT-REP170', not (dp <= tol * scale), '(%s: the largest reference coefficient times 1 + 1e-6)' % name)
        out('KEYJSON ' + json.dumps({'family': FAM, 'N': NN, 'J': J, 'key': name, 'index': idx, 'ak': ak, 'B': B, 'err': err, 'cpu': round(dt, 2),
                                     'refs': rep, 'rem_split': split}))
        out('STAGE-CPU key %s J=%g %.2f s' % (name, J, dt))
        prof_line('after %s J=%g' % (name, J))
        done += 1
    return done


def ref12(fn, key):
    """(ak, B) of one key in an m3ref_v1_2 record (pinned in REF12)."""
    for ln in read_bytes(os.path.join(OWN, 'out', fn)).decode('utf-8').split('\n'):
        if ln.startswith('KEYJSON '):
            d = json.loads(ln[8:])
            if d['key'] == key:
                return d['ak'], d['B']
    raise KeyError((fn, key))


def cmp_ak(ak, ref, sign=1.0):
    scale = max(abs(x) for x in ref) or 1.0
    return max(abs(x - sign * y) for x, y in zip(ak, ref)) / scale


def b_rel(B1, B2):
    return max((abs(B1[p] - B2[p]) / B2[p]) if B2[p] > 0 else 0.0 for p in ('rem', 'tail', 'ann', 'far'))


def s8_graph_check():
    """C-GRAPH: the column-spec builder against strip_graph and endw's graphs; PLANT-GRAPH."""
    L = s8_lists()
    ref = {'D': strip_graph(2, (A_EX, B_EX)), 'N': strip_graph(3, (A_EX, B_EX)), 'E2': (6, Emix), 'FF': (6, Efree)}
    oks = [graph_of(L['v1_1']['graphs'][gn]['columns']) == r for gn, r in ref.items()]
    oks += [graph_of(L['v2']['graphs']['D']['columns']) == ref['D']]
    oks += [graph_of(L['v2']['graphs']['L']['columns']) == strip_graph(4, (A_EX, B_EX))]
    gate('C-GRAPH', all(oks), '(the column specs of D (v1_1, v2), N, E2, FF and L (v2) give strip_graph(2), strip_graph(3), Emix, Efree and strip_graph(4) exactly)')
    Vb, Eb = graph_of(L['v1_1']['graphs']['D']['columns'])
    Eb[(0, 2)] = Eb[(0, 2)] * (1 + 1e-12)
    plant('PLANT-GRAPH', (Vb, Eb) != ref['D'], '(D with its T-B coupling times 1 + 1e-12)')


def s8_checks():
    """C-ALIAS, C-TY and PAR-INFO on the keys of this run (RES)."""
    pairs = []
    if FAM == 'S8E2' and 'e,0' in RES:
        pairs.append(('e,0 = I_mix',) + RES['e,0'] + ref12('m3ref_v1_2_mix.%d.all_z9sym.out' % NN, 'I_mix'))
    if FAM == 'S8FF' and 'z' in RES:
        pairs.append(('z = I_free',) + RES['z'] + ref12('m3ref_v1_2_free.%d.all_z9sym.out' % NN, 'I_free'))
    if FAM == 'S8N':
        for a in range(4):
            for k in ('TX,%d,0' % a, 'TX,0,%d' % a):
                if k in RES:
                    pairs.append(('%s = A,%d' % (k, a),) + RES[k] + ref12('m3ref_v1_2_N1.%d.all_z9sym.out' % NN, 'A,%d' % a))
    for lab, ak, B, rak, rB in pairs:
        d = cmp_ak(ak, rak)
        gate('C-ALIAS', d <= 1e-10, '%s: max|diff| / max|a_k| %.2e' % (lab, d))
        out('C-ALIAS-B-INFO %s: largest relative bar-part difference %.2e' % (lab, b_rel(B, rB)))
    if pairs:
        lab, ak, B, rak, rB = pairs[0]
        bad = list(rak)
        im = max(range(len(bad)), key=lambda i: abs(bad[i]))
        bad[im] = bad[im] * (1 + 1e-6)
        plant('PLANT-ALIAS', not (cmp_ak(ak, bad) <= 1e-10), '(%s: the largest reference coefficient times 1 + 1e-6)' % lab)
    if FAM == 'S8N':
        w = None
        for a in range(4):
            for b in range(a, 4):
                kx, ky = 'TX,%d,%d' % (a, b), 'TY,%d,%d' % (a, b)
                if kx in RES and ky in RES:
                    s = PI[a] * PI[b]
                    d = cmp_ak(RES[ky][0], RES[kx][0], s)
                    gate('C-TY', d <= 1e-10, '%s = %+d x %s: max|diff| / max|a_k| %.2e' % (ky, s, kx, d))
                    out('C-TY-B-INFO %s vs %s: largest relative bar-part difference %.2e' % (ky, kx, b_rel(RES[ky][1], RES[kx][1])))
                    if w is None and (a == 2) != (b == 2):
                        w = (kx, ky, s)
        if 'TX,1,0' in RES and 'TX,0,1' in RES:
            d = cmp_ak(RES['TX,1,0'][0], RES['TX,0,1'][0])
            gate('C-TY', d <= 1e-10, 'TX,1,0 = TX,0,1 (mirror): max|diff| / max|a_k| %.2e' % d)
            out('C-TY-B-INFO TX,1,0 vs TX,0,1: largest relative bar-part difference %.2e' % b_rel(RES['TX,1,0'][1], RES['TX,0,1'][1]))
        if w is not None:
            kx, ky, s = w
            plant('PLANT-TY', not (cmp_ak(RES[ky][0], RES[kx][0], -s) <= 1e-10), '(%s against %s with pi_2 = +1)' % (ky, kx))
    for k in ('e,2', 'f,2'):
        if k in RES:
            out('PAR-INFO %s: max |a_k| %.2e (one odd state on a T <-> B symmetric graph)' % (k, max(abs(x) for x in RES[k][0])))


# ------------------------------------------------------------------ S8 entry list v3 (m3ref_v1_10)
V3FAM = ('V3D', 'V3N', 'V3E2', 'V3E3', 'V3FF')
REF_OLD = {   # the earlier float records the list's old keys must reproduce (z9sym), with their sha256
    'm3ref_v1_2_D.4.all_z9sym.out': '14b5f1910b5777b89f939127b107e1884a2cb7dbaca4d8a961b55f5b1868446f',
    'm3ref_v1_2_D.3.all_z9sym.out': 'c34f79f76ea42e87d959109559502dff28a432e56b0158ff2a0d93508e79c7ce',
    'm3ref_v1_3_S8D.4.all_z9sym.out': 'e93c69a86c1aca57d97741969fbdbc370f125ed119f1d3f7d6768b5745f33023',
    'm3ref_v1_3_S8D.3.all_z9sym.out': '95173d25b7dddb7849e210130b149fe78ee37ef15df00a41dbd38ed2c01512f9',
    'm3ref_v1_2_N0T.4.all_z9sym.out': 'c4700f0c1d8164735f83315bfe0c07fc97cad5c28294e9235b90e196921b1327',
    'm3ref_v1_2_N0T.3.all_z9sym.out': '750039535e6adc2dc8042e53607f83805677fa124a43e4d149bb762479b81259',
    'm3ref_v1_3_S8N.4.all_z9sym.out': 'd5f736d9db0f920a4d3b13ee3112b41f02ee88f1d0e0acc38c3976b95ef332a6',
    'm3ref_v1_3_S8N.3.all_z9sym.out': 'dc8f2b6dfb3fc337e09b16fa2df1e39417a988c8e159f7564a892534f272f3fb',
    'm3ref_v1_3_S8E2.4.all_z9sym.out': '3f2659310bee438c0abd6b77f52e0b71ad2143810e618c4f621bab46a4bbcc43',
    'm3ref_v1_3_S8E2.3.all_z9sym.out': 'f497d719ce330c70399f85d85c5654743e29d89ea658917574491e60916530a4',
    'm3ref_v1_3_S8E3.4.all_z9sym.out': 'dec1127c55e8c9cbc4a4fc95affe2201a51a753d0037d01cc420a0de8ab7e67c',
    'm3ref_v1_3_S8E3.3.all_z9sym.out': '0c19570ce59ae37d497e948ce33ea73aa80f9c50da96bf86c45195deac74e9a7',
    'm3ref_v1_3_S8FF.4.all_z9sym.out': 'a78b2543b44ca193cca1a5ead1b72c3ee4aad1df37412f0ce8a8e85f823c24e9',
    'm3ref_v1_3_S8FF.3.all_z9sym.out': '924f92a582bffb242fc29fd028a3d039d633e1149f0b883e85631a097dac726d',
}
OLDSRC = {'V3D': ('m3ref_v1_2_D', 'm3ref_v1_3_S8D'), 'V3N': ('m3ref_v1_2_N0T', 'm3ref_v1_3_S8N'), 'V3E2': ('m3ref_v1_3_S8E2',),
          'V3E3': ('m3ref_v1_3_S8E3',), 'V3FF': ('m3ref_v1_3_S8FF',)}
V3META = {}   # key -> (new, parity_zero), from the list


def v3_checks():
    """C-REPOLD-REF, C-REPOLD and C-PARZERO with their plants, and V3-INFO, on the keys of this run (RES)."""
    STAGE[0] = 'v3 checks'
    bad, old = [], {}
    for stem in OLDSRC[FAM]:
        fn = '%s.%d.all_z9sym.out' % (stem, NN)
        text = read_bytes(os.path.join(OWN, 'out', fn))
        vl = [ln for ln in text.decode('utf-8').split('\n') if ln.startswith('VERDICT')]
        if sha(text) != REF_OLD[fn] or vl != ['VERDICT VALID']:
            bad.append(fn)
            continue
        for k, a in rec_ak(fn).items():
            old.setdefault(k, a)
    gate('C-REPOLD-REF', TRIAL == 'z9sym' and not bad, '(%s at N = %d: sha256 pinned, VERDICT lines exactly [VERDICT VALID]; TRIAL '
         '%s)%s' % (', '.join(OLDSRC[FAM]), NN, TRIAL, (': ' + ', '.join(bad)) if bad else ''))
    done = [k for k in V3META if k in RES]
    olds = [k for k in done if not V3META[k][0] and not V3META[k][1]]
    miss = [k for k in olds if k not in old or len(old[k]) != len(RES[k][0])]
    cmp_ = [(cmp_ak(RES[k][0], old[k]), k) for k in olds if k not in miss]
    if olds:
        worst = max(cmp_) if cmp_ else (math.inf, '-')
        gate('C-REPOLD', not bad and not miss and worst[0] <= 1e-10, '(%d old keys of this range against %s: largest max|diff| / '
             'max|a_k| %.2e at %s%s)' % (len(olds), ', '.join(OLDSRC[FAM]), worst[0], worst[1],
                                         ('; no earlier record for ' + ', '.join(miss)) if miss else ''))
        if cmp_:
            k0 = cmp_[0][1]
            ref = list(old[k0])
            im = max(range(len(ref)), key=lambda i: abs(ref[i]))
            ref[im] = ref[im] * (1 + 1e-6)
            plant('PLANT-REPOLD', not (cmp_ak(RES[k0][0], ref) <= 1e-10), '(%s: the largest reference coefficient times 1 + 1e-6)' % k0)
    pz = [k for k in done if V3META[k][1]]
    nz = [k for k in done if not V3META[k][1]]
    mx = lambda k: max(abs(x) for x in RES[k][0])
    big = max((mx(k) for k in nz), default=0.0)
    if pz:
        wpz = max((mx(k), k) for k in pz)
        gate('C-PARZERO', big > 0 and wpz[0] <= 1e-10 * big, '(%d parity-zero keys of this range: largest max|a_k| %.2e at %s, against '
             '1e-10 of the largest nonzero key\'s %.3e)' % (len(pz), wpz[0], wpz[1], big))
        if nz:
            kb = max(nz, key=mx)
            plant('PLANT-PARZERO', not (mx(kb) <= 1e-10 * big), '(%s, the largest nonzero key, read as a parity zero)' % kb)
    news = [k for k in done if V3META[k][0]]
    cpus = sorted(((KEYCPU.get(k, 0.0), k) for k in done), reverse=True)
    out('V3-INFO %s N=%d: %d keys done (%d old, %d new, %d parity zeros); CPU per key: max %.2f s at %s, mean %.2f s, total %.1f s' % (
        FAM, NN, len(done), len(olds), len(news), len(pz), cpus[0][0] if cpus else 0.0, cpus[0][1] if cpus else '-',
        sum(c for c, _ in cpus) / len(cpus) if cpus else 0.0, sum(c for c, _ in cpus)))


# ------------------------------------------------------------------ S8 entry list v4, K-form keys (m3ref_v1_11)
V4FAM = ('V4NK', 'V4E3K', 'V4F3')
V4REL = {}   # key -> the list's rel_bar_max


def v4_checks():
    """C-PARZERO (keys the list marks parity_zero; none expected), REL-INFO and REL-MAX against the list's rel_bar_max, and V3-INFO."""
    STAGE[0] = 'v4 checks'
    done = [k for k in V3META if k in RES]
    pz = [k for k in done if V3META[k][1]]
    nz = [k for k in done if not V3META[k][1]]
    mx = lambda k: max(abs(x) for x in RES[k][0])
    if pz:
        big = max((mx(k) for k in nz), default=0.0)
        wpz = max((mx(k), k) for k in pz)
        gate('C-PARZERO', big > 0 and wpz[0] <= 1e-10 * big, '(%d parity-zero keys: largest max|a_k| %.2e at %s, against 1e-10 of %.3e)' % (
            len(pz), wpz[0], wpz[1], big))
    worst = None
    for k in nz:
        err, val = sum(RES[k][1].values()), hval(RES[k][0])
        rel = err / abs(val) if val else float('inf')
        lim = V4REL.get(k)
        out('REL-INFO %s: err %.6e, value %.6e, err/|value| %.3e against rel_bar_max %s%s' % (k, err, val, rel, lim,
                                                                                       '' if lim is None or rel <= lim else ' (above)'))
        if worst is None or rel > worst[0]:
            worst = (rel, k)
    if worst is not None:
        nabove = sum(1 for k in nz if V4REL.get(k) is not None and sum(RES[k][1].values()) > V4REL[k] * abs(hval(RES[k][0])))
        out('REL-MAX %s N=%d: largest err/|value| %.3e at %s; %d of %d keys above their rel_bar_max' % (FAM, NN, worst[0], worst[1], nabove, len(nz)))
    cpus = sorted(((KEYCPU.get(k, 0.0), k) for k in done), reverse=True)
    out('V3-INFO %s N=%d: %d keys done (%d parity zeros); CPU per key: max %.2f s at %s, mean %.2f s, total %.1f s' % (
        FAM, NN, len(done), len(pz), cpus[0][0] if cpus else 0.0, cpus[0][1] if cpus else '-',
        sum(c for c, _ in cpus) / len(cpus) if cpus else 0.0, sum(c for c, _ in cpus)))


# ------------------------------------------------------------------ S8 centered entries (m3ref_v1_9)
CFAM = ('S8Hc', 'S8E3c', 'S8E2c', 'S8FFc', 'S8S4c')
REF_CENTER = {   # the float records the centring constants are read from (z9sym), with their sha256
    'm3ref_v1_3_S8E3.4.all_z9sym.out': 'dec1127c55e8c9cbc4a4fc95affe2201a51a753d0037d01cc420a0de8ab7e67c',
    'm3ref_v1_3_S8E3.3.all_z9sym.out': '0c19570ce59ae37d497e948ce33ea73aa80f9c50da96bf86c45195deac74e9a7',
    'm3ref_v1_3_S8E2.4.all_z9sym.out': '3f2659310bee438c0abd6b77f52e0b71ad2143810e618c4f621bab46a4bbcc43',
    'm3ref_v1_3_S8E2.3.all_z9sym.out': 'f497d719ce330c70399f85d85c5654743e29d89ea658917574491e60916530a4',
    'm3ref_v1_8_S8H.4.all_z9sym.out': 'cd053938c104ebe08f823a49bce54a9f44e2a228b66c771699d689e26736ef95',
    'm3ref_v1_8_S8H.3.all_z9sym.out': 'fefe2fd600076ab179f8f724d9154456421ed4afcab894c9c09223c4a3794b61',
    'm3ref_v1_8_S8S4.4.all_z9sym.out': '5f3517ef2b751ab93a5cd31e78101b02dc70f58b15424f8e89a52a3d5490d534',
    'm3ref_v1_8_S8S4.3.all_z9sym.out': '36c122028670d44bab7b75ad8c7ece0987f58a1c134a9668d318b208da1aa04d',
}
KAPPA_W4 = {('k0', 4): '0x1.b3304ab7231d0p-1', ('km', 4): '0x1.0e966a08fdb45p+0', ('k0', 3): '0x1.222158b1721aep-1',
            ('km', 3): '0x1.68e2bed9b7c07p-1'}   # pk11's kappa0 (kt_s8f3g_v1_1 80c401df): d = 0 fX,0/f,0, d = -1 eX,0/e,0
S4BONDS = [(0, 'TM'), (1, 'TM'), (1, 'MB'), (2, 'TM'), (2, 'MB'), (3, 'TM'), (3, 'MB')]   # kt_s8_cert_v1_11 afd8f0ca l.494
N4PAIRS = [((0, 'TM'), (1, 'TM')), ((0, 'TM'), (1, 'MB')), ((1, 'TM'), (2, 'TM')), ((1, 'TM'), (2, 'MB')), ((0, 'TM'), (2, 'TM')),
           ((0, 'TM'), (2, 'MB')), ((0, 'TM'), (3, 'TM')), ((0, 'TM'), (3, 'MB')), ((2, 'TM'), (3, 'TM')), ((2, 'TM'), (3, 'MB'))]   # l.495-499
CONST = {}
T300 = 1.0 / 300.0


def hval(ak):
    """an entry's value at J = 300 from its a_k by Horner (a_0 + a_1 t + a_2 t^2 + a_3 t^3, t = 1.0/300)."""
    v = 0.0
    for a in reversed(ak):
        v = v * T300 + a
    return v


def rec_ak(fn):
    """{key: a_k} from a float record's KEYJSON lines."""
    res = {}
    for ln in read_bytes(os.path.join(OWN, 'out', fn)).decode('utf-8').split('\n'):
        if ln.startswith('KEYJSON '):
            d = json.loads(ln[8:])
            res[d['key']] = d['ak']
    return res


def center_setup():
    """C-CENTER-REF, the constants (CONST), C-KAPPA-REF with its plant, CONSTJSON; False if a source record fails."""
    STAGE[0] = 'centring constants'
    bad = []
    for stem in ('m3ref_v1_3_S8E3', 'm3ref_v1_3_S8E2', 'm3ref_v1_8_S8H', 'm3ref_v1_8_S8S4'):
        fn = '%s.%d.all_z9sym.out' % (stem, NN)
        text = read_bytes(os.path.join(OWN, 'out', fn))
        vl = [ln for ln in text.decode('utf-8').split('\n') if ln.startswith('VERDICT')]
        if sha(text) != REF_CENTER[fn] or vl != ['VERDICT VALID']:
            bad.append(fn)
    gate('C-CENTER-REF', TRIAL == 'z9sym' and not bad, '(m3ref_v1_3 S8E3, S8E2 and m3ref_v1_8 S8H, S8S4 at N = %d: sha256 pinned, VERDICT '
         'lines exactly [VERDICT VALID]; TRIAL %s)%s' % (NN, TRIAL, (': ' + ', '.join(bad)) if bad else ''))
    if bad or TRIAL != 'z9sym':
        return False
    e3, e2 = rec_ak('m3ref_v1_3_S8E3.%d.all_z9sym.out' % NN), rec_ak('m3ref_v1_3_S8E2.%d.all_z9sym.out' % NN)
    hh, s4 = rec_ak('m3ref_v1_8_S8H.%d.all_z9sym.out' % NN), rec_ak('m3ref_v1_8_S8S4.%d.all_z9sym.out' % NN)
    CONST['k0'] = hval(e3['fX,0']) / hval(e3['f,0'])
    CONST['km'] = hval(e2['eX,0']) / hval(e2['e,0'])
    CONST['k1'] = hval(hh['hX,0']) / hval(hh['h,0'])
    for c_, b_ in S4BONDS:
        CONST['m,%d,%s' % (c_, b_)] = hval(s4['S4,x,%d,%s' % (c_, b_)]) / hval(s4['S4,Z'])
    okk = all(CONST[k] == float.fromhex(KAPPA_W4[(k, NN)]) for k in ('k0', 'km'))
    gate('C-KAPPA-REF', okk, '(k0 = fX,0/f,0 and km = eX,0/e,0 by Horner at J = 300 against pk11\'s kappa0: %s)' % ', '.join(
        '%s %s vs %s' % (k, CONST[k].hex(), KAPPA_W4[(k, NN)]) for k in ('k0', 'km')))
    h0 = KAPPA_W4[('k0', NN)]
    hb = h0[:-4] + ('1' if h0[-4] != '1' else '2') + h0[-3:]
    plant('PLANT-KAPPA-REF', CONST['k0'] != float.fromhex(hb), '(k0 against pk11\'s hex with its last mantissa digit changed: %s)' % hb)
    out('CONSTJSON ' + json.dumps({'N': NN, 'J': 300, 'horner_t': '1.0/300', 'const': {k: v.hex() for k, v in CONST.items()},
                                   'repr': {k: repr(v) for k, v in CONST.items()}}))
    return True


def center_keys(fam):
    """a family's centered keys as (key, factor encodings)."""
    if fam == 'S8Hc':
        return [('hXc,%d' % a, [['cp', a, 0], ['xic', 'TM', 'k1', 1]]) for a in range(4)]
    if fam == 'S8E3c':
        return [('fXc,%d' % a, [['cp', a, 0], ['xic', 'TM', 'k0', 1]]) for a in range(4)]
    if fam == 'S8E2c':
        return [('eXc,%d' % a, [['cp', a, 0], ['xic', 'TM', 'km', 1]]) for a in range(4)]
    if fam == 'S8FFc':
        return [('wXcwXc', [['xic', 'TM', 'km', 0], ['xic', 'TM', 'km', 1]])]
    if fam == 'S8S4c':
        ks = [('XXc', [['xic', 'TM', 'k0', 1], ['xic', 'TM', 'k0', 2]])]
        for (cx, bx), (cy, by) in N4PAIRS:
            ks.append(('Covc,%d,%s,%d,%s' % (cx, bx, cy, by), [['xic', bx, 'm,%d,%s' % (cx, bx), cx], ['xic', by, 'm,%d,%s' % (cy, by), cy]]))
        return ks
    return []


def center_combo(name):
    """[(coefficient, sibling key)] whose combination of a_k equals the centered key's (C-CENTER-AK)."""
    if name[:4] in ('hXc,', 'fXc,', 'eXc,'):
        k = CONST[{'h': 'k1', 'f': 'k0', 'e': 'km'}[name[0]]]
        return [(1.0, name[0] + 'X,' + name[4:]), (-k, name[0] + ',' + name[4:])]
    if name == 'wXcwXc':
        k = CONST['km']
        return [(1.0, 'wXwX'), (-2 * k, 'wXw'), (k * k, 'z')]
    if name == 'XXc':
        k = CONST['k0']
        return [(1.0, 'S4,xy,1,TM,2,TM'), (-k, 'S4,x,1,TM'), (-k, 'S4,x,2,TM'), (k * k, 'S4,Z')]
    _, cx, bx, cy, by = name.split(',')
    mx, my = CONST['m,%s,%s' % (cx, bx)], CONST['m,%s,%s' % (cy, by)]
    return [(1.0, 'S4,xy,%s,%s,%s,%s' % (cx, bx, cy, by)), (-my, 'S4,x,%s,%s' % (cx, bx)), (-mx, 'S4,x,%s,%s' % (cy, by)), (mx * my, 'S4,Z')]


def s8_center():
    """C-CENTER-AK with its plant, CENTER-INFO per centered key and CENTERJSON."""
    first = True
    info = {}
    for name, _ in center_keys(FAM):
        if name not in RES:
            continue
        combo = center_combo(name)
        if not all(k in RES for _, k in combo):
            gate('C-CENTER-AK', False, '%s: a sibling key is missing from this run' % name)
            continue
        ak = RES[name][0]
        ref = [sum(c * RES[k][0][i] for c, k in combo) for i in range(len(ak))]
        scale = max(abs(x) for x in list(ak) + ref) or 1.0
        d = max(abs(x - y) for x, y in zip(ak, ref)) / scale
        gate('C-CENTER-AK', d <= 1e-10, '%s = %s: max|diff| / max|a_k| %.2e' % (name, ' + '.join('%.9g %s' % ck for ck in combo), d))
        if first:
            first = False
            bad = [sum((c * (1 + 1e-6) if j == 1 else c) * RES[k][0][i] for j, (c, k) in enumerate(combo)) for i in range(len(ak))]
            plant('PLANT-CENTER-AK', not (max(abs(x - y) for x, y in zip(ak, bad)) / scale <= 1e-10), '(%s with its first constant times '
                  '1 + 1e-6)' % name)
        sib = combo[0][1]
        ec, es = sum(RES[name][1].values()), sum(RES[sib][1].values())
        vc, vs = hval(ak), hval(RES[sib][0])
        info[name] = {'err': ec, 'value': vc, 'sibling': sib, 'sib_err': es, 'sib_value': vs}
        out('CENTER-INFO %s: err %.6e, value %.6e; %s: err %.6e, value %.6e; err ratio %.4g' % (name, ec, vc, sib, es, vs,
                                                                                          ec / es if es else float('nan')))
    out('CENTERJSON ' + json.dumps({'family': FAM, 'N': NN, 'const': {k: v.hex() for k, v in CONST.items()}, 'keys': info}))


# ------------------------------------------------------------------ S8 4-column analogs (m3ref_v1_7)
REF_ANALOG = {   # the 3-column records the analogs read (z9sym), with their sha256
    'm3ref_v1_2_N0T.4.all_z9sym.out': 'c4700f0c1d8164735f83315bfe0c07fc97cad5c28294e9235b90e196921b1327',
    'm3ref_v1_2_N0T.3.all_z9sym.out': '750039535e6adc2dc8042e53607f83805677fa124a43e4d149bb762479b81259',
    'm3ref_v1_3_S8E3.4.all_z9sym.out': 'dec1127c55e8c9cbc4a4fc95affe2201a51a753d0037d01cc420a0de8ab7e67c',
    'm3ref_v1_3_S8E3.3.all_z9sym.out': '0c19570ce59ae37d497e948ce33ea73aa80f9c50da96bf86c45195deac74e9a7',
    'm3ref_v1_3_S8FF.4.all_z9sym.out': 'a78b2543b44ca193cca1a5ead1b72c3ee4aad1df37412f0ce8a8e85f823c24e9',
    'm3ref_v1_3_S8FF.3.all_z9sym.out': '924f92a582bffb242fc29fd028a3d039d633e1149f0b883e85631a097dac726d',
}
ANALOG_SRC = {'S8L': 'm3ref_v1_2_N0T', 'S8H': 'm3ref_v1_3_S8E3', 'S8S4': 'm3ref_v1_3_S8FF',
              'S8L16': 'm3ref_v1_2_N0T', 'S8H16': 'm3ref_v1_3_S8E3', 'S8S416': 'm3ref_v1_3_S8FF', 'P16H': 'm3ref_v1_3_S8E3', 'P16S4': 'm3ref_v1_3_S8FF'}
REF16BASE = {'S8L16': 'm3ref_v1_8_S8L', 'S8H16': 'm3ref_v1_8_S8H', 'S8S416': 'm3ref_v1_8_S8S4',   # the dmaxH-12 records (m3ref_v1_8 350ab86e)
             'P16H': 'm3ref_v1_8_S8H', 'P16S4': 'm3ref_v1_8_S8S4'}
REF16BASE_SHA = {
    'm3ref_v1_8_S8L.4.all_z9sym.out': '8b97a22bdaf3bf1429de6771868494b6695ad8fe7c604131c3319259fa30d271',
    'm3ref_v1_8_S8H.4.all_z9sym.out': 'cd053938c104ebe08f823a49bce54a9f44e2a228b66c771699d689e26736ef95',
    'm3ref_v1_8_S8S4.4.all_z9sym.out': '5f3517ef2b751ab93a5cd31e78101b02dc70f58b15424f8e89a52a3d5490d534',
    'm3ref_v1_8_S8L.3.all_z9sym.out': '8476e7b113a0f67ef0f984549c199b1726e0bb04feb5751c5a7d32d20eb6ec1f',
    'm3ref_v1_8_S8H.3.all_z9sym.out': 'fefe2fd600076ab179f8f724d9154456421ed4afcab894c9c09223c4a3794b61',
    'm3ref_v1_8_S8S4.3.all_z9sym.out': '36c122028670d44bab7b75ad8c7ece0987f58a1c134a9668d318b208da1aa04d',
}


def s8_dmax16_info():
    """C-REF12 with its plant, then DMAX16-INFO per key of this run (RES) against m3ref_v1_8's dmaxH-12 record, and DMAX16-MAX."""
    fn = '%s.%d.all_z9sym.out' % (REF16BASE[FAM], NN)
    text = read_bytes(os.path.join(OWN, 'out', fn))
    vl = [ln for ln in text.decode('utf-8').split('\n') if ln.startswith('VERDICT')]
    good = sha(text) == REF16BASE_SHA[fn] and vl == ['VERDICT VALID']
    gate('C-REF12', good, '(%s: sha256 pinned, VERDICT lines %r)' % (fn, vl))
    h0 = REF16BASE_SHA[fn]
    plant('PLANT-REF12', sha(text) != h0[:-1] + ('0' if h0[-1] != '0' else '1'), '(%s against a sha with its last digit changed)' % fn)
    if not good:
        return
    r12 = {}
    for ln in text.decode('utf-8').split('\n'):
        if ln.startswith('KEYJSON '):
            d = json.loads(ln[8:])
            r12[d['key']] = d
    rats = []
    for name in RES:
        B = RES[name][1]
        e16 = sum(B.values())
        if name not in r12 or not r12[name]['err'] > 0:
            out('DMAX16-INFO %s: err %.6e; no dmaxH-12 err to compare' % (name, e16))
            continue
        d = r12[name]
        q = lambda p: (B[p] / d['B'][p]) if d['B'][p] > 0 else float('nan')
        rats.append((e16 / d['err'], name, q('rem')))
        out('DMAX16-INFO %s: err %.6e (dmaxH 12: %.6e), ratio 16/12 %.4g; rem %.4g, tail %.4g, ann %.4g' % (
            name, e16, d['err'], e16 / d['err'], q('rem'), q('tail'), q('ann')))
    if rats:
        lo, hi = min(rats), max(rats)
        out('DMAX16-MAX %s N=%d: err ratio 16/12 from %.4g (%s, rem %.4g) to %.4g (%s, rem %.4g) over %d keys' % (
            FAM, NN, lo[0], lo[1], lo[2], hi[0], hi[1], hi[2], len(rats)))
NAMED = {'S4,Z': 'Z4', 'S4,x,1,TM': 'X1', 'S4,xy,1,TM,2,TM': 'X1X2'}
NEED = {4: 1.9, 3: 4.4}   # pk11's requirement: the analog 4-column set may grow together by this factor


def analog_of(key):
    """(factor, parent key) of pk11's analog for a 4-column key (kt_s8f3g_v1_1)."""
    if key.startswith('TT,'):
        return 2, 'T,' + key[3:]
    if key.startswith('hX,'):
        return 2, 'fX,' + key[3:]
    if key.startswith('h,'):
        return 2, 'f,' + key[2:]
    if key == 'S4,Z':
        return 2, 'z'
    if key.startswith('S4,xy,'):
        return 18, 'z'
    if key.startswith('S4,x,'):
        return 6, 'z'
    raise KeyError(key)


def s8_analog():
    """C-ANALOG-REF with its plant, ANALOG-INFO per key of this run (RES) and ANALOG-MAX."""
    fn = '%s.%d.all_z9sym.out' % (ANALOG_SRC[FAM], NN)
    text = read_bytes(os.path.join(OWN, 'out', fn))
    vl = [ln for ln in text.decode('utf-8').split('\n') if ln.startswith('VERDICT')]
    good = TRIAL == 'z9sym' and sha(text) == REF_ANALOG[fn] and vl == ['VERDICT VALID']
    gate('C-ANALOG-REF', good, '(%s: sha256 pinned, VERDICT lines %r; TRIAL %s)' % (fn, vl, TRIAL))
    h0 = REF_ANALOG[fn]
    plant('PLANT-ANALOG-REF', sha(text) != h0[:-1] + ('0' if h0[-1] != '0' else '1'), '(%s against a sha with its last digit changed)' % fn)
    if not good:
        return
    perr = {}
    for ln in text.decode('utf-8').split('\n'):
        if ln.startswith('KEYJSON '):
            d = json.loads(ln[8:])
            perr[d['key']] = d['err']
    worst = None
    for name in RES:
        fac, pk = analog_of(name)
        err = sum(RES[name][1].values())
        tag = (' (%s)' % NAMED[name]) if name in NAMED else ''
        if perr.get(pk, 0) > 0:
            r = err / (fac * perr[pk])
            out('ANALOG-INFO %s%s: err %.6e, analog %d x %s = %.6e, ratio %.4g' % (name, tag, err, fac, pk, fac * perr[pk], r))
            if worst is None or r > worst[0]:
                worst = (r, name)
        else:
            out('ANALOG-INFO %s%s: err %.6e, analog %d x %s n/a (no record of %s in %s)' % (name, tag, err, fac, pk, pk, fn))
    if worst is not None:
        out('ANALOG-MAX %s N=%d: largest err / analog %.4g at %s (pk11 allows x%g at this N)' % (FAM, NN, worst[0], worst[1], NEED[NN]))


U16FAM = {'U16L': 'S8L', 'U16H': 'S8H', 'U16S4': 'S8S4'}   # m3ref_v1_13: the stage-u rE probe at dmaxH 16 on the base family's graph
U16REF = {'U16L': 'm3ref_v1_8_S8L', 'U16H': 'm3ref_v1_8_S8H', 'U16S4': 'm3ref_v1_8_S8S4'}   # the dmaxH-12 records (REF16BASE_SHA)


def _deg(P):
    return max([sum(e) for e in P] + [0])


def run_u16():
    """m3ref_v1_13: rE's parts at dmaxH 16 against m3ref_v1_8's dmaxH-12 record of the same graph, and the re-extrapolated analog
    ratios (docstring at the top)."""
    import riglap3
    base = U16FAM[FAM]
    fn = '%s.%d.all_z9sym.out' % (U16REF[FAM], NN)
    text = read_bytes(os.path.join(OWN, 'out', fn))
    lines = text.decode('utf-8').split('\n')
    vl = [ln for ln in lines if ln.startswith('VERDICT')]
    good = sha(text) == REF16BASE_SHA[fn] and vl == ['VERDICT VALID']
    gate('C-REF12', good, '(%s: sha256 pinned, VERDICT lines %r)' % (fn, vl))
    h0 = REF16BASE_SHA[fn]
    plant('PLANT-REF12', sha(text) != h0[:-1] + ('0' if h0[-1] != '0' else '1'), '(%s against a sha with its last digit changed)' % fn)
    if not good:
        return
    p12 = [json.loads(ln[9:]) for ln in lines if ln.startswith('PREPJSON ')][0]
    k12 = {d['key']: d for d in (json.loads(ln[8:]) for ln in lines if ln.startswith('KEYJSON '))}
    g, npb, keys = s8_family(base)
    riglap5b.NPOLY_B = npb
    rr = [math.sqrt(min(S_RAD * g.G[v, v] / J_REF, RCAP)) for v in range(g.V)]
    a_v = [r * r for r in rr]
    t, n, W = 1.0 / J_REF, g.n, g.W
    gate('C-U16-SETUP', p12['family'] == base and p12['N'] == NN and p12['a_v'] == a_v and p12['J'] == J_REF,
         '(%s: family %s, N %d, J %g and the radii equal the dmaxH-12 record\'s)' % (FAM, base, NN, J_REF))
    out('family %s N=%d: the graph of %s (V %d, F %d), NPOLY_B %d; rE parts at dmaxH 16 against %s' % (FAM, NN, base, g.V, g.F, npb, fn))
    # riglap5r.Prep5r l.25-28 and l.31-39 (the twelve parts) and riglap5s.Prep5s l.25-26 and l.29 (ex), term by term
    Hs = riglap3.Model3(g, 4, []).H(4)
    H1, H2, H3, H4 = Hs.c[1], Hs.c[2], Hs.c[3], Hs.c[4]
    mjH = riglap2.Majorants(riglap2.Model(g, 5, []), a_v, t, B=riglap5b.NPOLY_B)
    h2 = mjH.hbar(2).to_dict(); h3 = mjH.hbar(3).to_dict(); h5 = mjH.hbar(5).to_dict()
    H1sq = pmul(H1, H1)
    mjS = riglap2.Majorants(riglap2.Model(g, 3, []), a_v, t, B=riglap5b.NPOLY_B)
    h2s = mjS.hbar(2).to_dict()
    parts = [('t4|H4|', t ** 4, H4), ('t5 h5/120', t ** 5 / 120, h5), ('t4 H2^2/2', 0.5 * t ** 4, pmul(H2, H2)),
             ('t6 h3^2/72', t ** 6 / 72, pmul(h3, h3)), ('t4|H1H3|', t ** 4, pmul(H1, H3)), ('t5|H1H4|', t ** 5, pmul(H1, H4)),
             ('t6|H1|h5/120', t ** 6 / 120, pmul(H1, h5)), ('t5|H2|h3/6', t ** 5 / 6, pmul(H2, h3)),
             ('t4 H1^2|H2|/2', 0.5 * t ** 4, pmul(H1sq, H2)), ('t5 H1^2 h3/12', t ** 5 / 12, pmul(H1sq, h3)),
             ('t5|H1|h2^2/8', t ** 5 / 8, pmul(H1, pmul(h2, h2))),
             ('tr: t5 h2^2 hhat/24', t ** 5 / 24, pmul(pmul(h2, h2), riglap5.hhat2(g, a_v, t, h2))),
             ('ex: t6 h2^3/48', t ** 6 / 48, pmul(h2s, pmul(h2s, h2s)))]
    v12 = dict(p12['rE_parts'])
    order = sorted([p for p in parts if p[0] in v12], key=lambda p: -v12[p[0]]) + [p for p in parts if p[0] not in v12]
    v16 = {}
    for lab, sc, P in order:
        STAGE[0] = 'U16 part %s' % lab
        d = _deg(P)
        t1 = cpu()
        val = sc * norm_any(P, g.G, n, W, 2, FAM + '|H', 16)
        v16[lab] = val
        ref = v12.get(lab)
        out('U16-PART %s: deg %d (exact at dmaxH 12 %s, at 16 %s), %d terms; dmaxH 16 %.6e, dmaxH 12 %s, ratio 16/12 %s; cpu %.1f s (so far %.1f s)' % (
            lab, d, 2 * d <= 12, 2 * d <= 16, len(P), val, ('%.6e' % ref) if ref is not None else 'n/a',
            ('%.4g' % (val / ref)) if ref else 'n/a', cpu() - t1, cpu()))
    STAGE[0] = 'U16 checks'
    same = [(lab, v16[lab], v12[lab]) for lab, sc, P in parts if lab in v12 and (2 * _deg(P) <= 12 or 2 * _deg(P) > 16)]
    bad = [lab for lab, a, b in same if not abs(a - b) <= 1e-12 * abs(b)]
    gate('C-U16-SAME', len(same) >= 3 and not bad, '(%d parts with the same exactness at dmaxH 12 and 16 equal their dmaxH-12 values to 1e-12: %s)%s' % (
        len(same), ', '.join(lab for lab, a, b in same), (': differ ' + ', '.join(bad)) if bad else ''))
    if same:
        lab, a, b = same[0]
        plant('PLANT-U16-SAME', not abs(a * (1 + 1e-9) - b) <= 1e-12 * abs(b), '(%s times 1 + 1e-9 must differ)' % lab)
    e23 = min(v16['ex: t6 h2^3/48'], v16['tr: t5 h2^2 hhat/24'])
    rE16 = sum(v16[lab] for lab, sc, P in parts if lab in v12) + e23
    rE12 = p12['rE']
    out('U16-RE %s N=%d: rE dmaxH 16 %.6e, dmaxH 12 %.6e, ratio %.4g; E2^3 term min(ex %.3e, tr %.3e) = %.3e (dmaxH 12: %.3e)' % (
        FAM, NN, rE16, rE12, rE16 / rE12, v16['ex: t6 h2^3/48'], v16['tr: t5 h2^2 hhat/24'], e23, v12.get('E2^3 term', float('nan'))))
    afn = '%s.%d.all_z9sym.out' % (ANALOG_SRC[base], NN)
    atext = read_bytes(os.path.join(OWN, 'out', afn))
    avl = [ln for ln in atext.decode('utf-8').split('\n') if ln.startswith('VERDICT')]
    agood = TRIAL == 'z9sym' and sha(atext) == REF_ANALOG[afn] and avl == ['VERDICT VALID']
    gate('C-ANALOG-REF', agood, '(%s: sha256 pinned, VERDICT lines %r; TRIAL %s)' % (afn, avl, TRIAL))
    if not agood:
        return
    perr = {}
    for ln in atext.decode('utf-8').split('\n'):
        if ln.startswith('KEYJSON '):
            dd = json.loads(ln[8:])
            perr[dd['key']] = dd['err']
    worst = None
    for name, facs, refs in keys:
        dd = k12.get(name)
        if dd is None or not dd.get('rem_split') or not dd['err'] > 0:
            continue
        fre = dd['rem_split']['F.R_E']
        e16 = dd['err'] + fre * (rE16 / rE12 - 1)
        fac, pk = analog_of(name)
        if perr.get(pk, 0) > 0:
            an = fac * perr[pk]
            out('U16-EXTRAP %s: err dmaxH 12 %.6e (ratio %.4g); with the dmaxH-16 rE %.6e (ratio %.4g); without F.R_E ratio %.4g' % (
                name, dd['err'], dd['err'] / an, e16, e16 / an, (dd['err'] - fre) / an))
            if worst is None or e16 / an > worst[0]:
                worst = (e16 / an, name, dd['err'] / an)
    if worst is not None:
        out('U16-MAX %s N=%d: largest err / analog with the dmaxH-16 rE %.4g at %s (dmaxH 12: %.4g)' % (FAM, NN, worst[0], worst[1], worst[2]))


# ------------------------------------------------------------------ m3ref_v1_15: the S9 family V9I of S9_ENTRY_LIST_v1
V9FAM = ('V9I',)
V9BASE = {'V9I': 'V3N'}   # the S8 family with the same vertices and couplings (only the pair forms differ)


def v9_base_file():
    """the m3ref_v1_10 record of the base family at this N (pinned in REF9)."""
    return 'm3ref_v1_10_%s.%d.all_z9sym.out' % (V9BASE[FAM], NN)


def v9_flat(d):
    """a PREPJSON dict as a list of (label, value): the radii, rho'^2, theta0 and, for a prep that is ok, every scalar."""
    v = [('ap', d['ap']), ('theta0', d['theta0'])] + [('a_v[%d]' % i, x) for i, x in enumerate(d['a_v'])]
    if d.get('ok'):
        v += [(k, d[k]) for k in ('rE', 'nC8', 'nC6', 'Pout', 'Pout_p', 'farbase')]
        v += [('rE_parts[%s]' % k, x) for k, x in sorted(d['rE_parts'].items())]
        v += [('nE[%d]' % j, x) for j, x in enumerate(d['nE'])] + [('nE4[%d]' % j, x) for j, x in enumerate(d['nE4'])]
    return v


def v9_worst(a, b):
    """the largest relative difference between two flat lists with the same labels, and its label."""
    return max(((abs(x - y) / max(abs(y), 1e-300), k) for (k, x), (_, y) in zip(a, b)), default=(0.0, '-'))


def v9_checks(pj):
    """C-PREP9-REF and C-PREP9 with PLANT-PREP9: this run's prep against the base family's record (m3ref_v1_10, pinned in REF9). The
    prep reads only the vertex forms, so the radii, rho'^2, theta0 and every prep scalar must agree to 1e-12 relative. Then V9-INFO."""
    STAGE[0] = 'v9 checks'
    fn = v9_base_file()
    text = read_bytes(os.path.join(OWN, 'out', fn))
    lines = text.decode('utf-8').split('\n')
    vl = [ln for ln in lines if ln.startswith('VERDICT')]
    good = sha(text) == REF9[fn] and vl == ['VERDICT VALID']
    gate('C-PREP9-REF', good, '(%s: sha256 pinned, VERDICT lines %r)' % (fn, vl))
    ref = [json.loads(ln[len('PREPJSON '):]) for ln in lines if ln.startswith('PREPJSON ')][0]
    a, b = v9_flat(pj), v9_flat(ref)
    same_labels = [k for k, _ in a] == [k for k, _ in b]
    worst = v9_worst(a, b) if same_labels else (math.inf, 'the labels differ')
    gate('C-PREP9', good and same_labels and worst[0] <= 1e-12, '(%s against %s at N = %d: %d prep values, largest relative difference %.1e at %s)' % (
        FAM, V9BASE[FAM], NN, len(a), worst[0], worst[1]))
    b2 = [(k, y * (1 + 1e-9) if k == 'rE' else y) for k, y in b]
    plant('PLANT-PREP9', not (v9_worst(a, b2)[0] <= 1e-12), '(the base family\'s rE times 1 + 1e-9)')
    cpus = sorted(((KEYCPU.get(k, 0.0), k) for k in RES), reverse=True)
    out('V9-INFO %s N=%d: %d keys; CPU per key: max %.2f s at %s, total %.1f s' % (
        FAM, NN, len(RES), cpus[0][0] if cpus else 0.0, cpus[0][1] if cpus else '-', sum(c for c, _ in cpus)))


# ------------------------------------------------------------------ m3ref_v1_14: the staged dmaxH-16 probe (P16H, P16S4)
P16FAM = {'P16H': 'S8H', 'P16S4': 'S8S4', 'P16T1': 'T1', 'P16T1N': 'T1n', 'P16T2': 'T2', 'P16T2N': 'T2n',   # pk22: + W1a
          'P16BD2T': 'BD2T', 'P16BE2T': 'BE2T', 'P16BE3T': 'BE3T', 'P16BH4T': 'BH4T', 'P16BL': 'BL', 'P16BN2T': 'BN2T', 'P16BT1MN': 'BT1MN',   # pk22 v1_2: B
          'P16CS4': 'C3CS4', 'P16CE3': 'C3CE3', 'P16CH4T': 'C3H4T', 'P16CE2T': 'C3E2T',   # pk22 v1_4: c3
          'P16CE3H': 'C3HCE3H', 'P16CS4H': 'C3HCS4H', 'P16CH4TH': 'C3HH4TH',   # pk22 v1_6: c3h
          'P16E4D': 'C3KE4D', 'P16E4N': 'C3KE4N',   # pk22 v1_7: c3k
          'P16L': 'HLL'}   # pk23 hl_v1
TABD = os.path.join(HLD, 'out', 'tab16')   # pk23 hl_v1
P16 = {'piece': 0, 'memo': {}, 'memo_path': None, 'tables': {}}


class StopPiece(Exception):
    """raised before a table build or an E2 chunk that would not fit in this piece: the piece ends PREP-PARTIAL."""


def _file_sha(path):
    h = hashlib.sha256()
    with open(path, 'rb') as fh:
        for blk in iter(lambda: fh.read(1 << 24), b''):
            h.update(blk)
    return h.hexdigest()


def _tab_id(G, n, W, D, groups, caps):
    """the identity of a moment table: its covariance (or Gram) and form matrices, n, D, groups and caps."""
    h = hashlib.sha256()
    for a in (np.ascontiguousarray(G, dtype=float), np.ascontiguousarray(W, dtype=float)):
        h.update(repr(a.shape).encode())
        h.update(a.tobytes())
    h.update(repr((int(n), int(D), None if groups is None else [int(x) for x in groups],
                   sorted((int(k), int(v)) for k, v in (caps or {}).items()))).encode())
    return h.hexdigest()[:32]


def _budget(est, what):
    """StopPiece unless about est more CPU seconds fit in this piece (25 s kept for CACHE-STATE and the verdict)."""
    if cpu() + est > LIM - 25:
        raise StopPiece('%s needs about %.0f s and %.0f s are left' % (what, est, LIM - 25 - cpu()))


def _save_table(am, tid):
    path = os.path.join(TABD, tid + '.npz')
    arrs = {'pw': am.pw, 'Gam': am.Gam, 'groups': am.groups}
    for d in range(am.D + 1):
        arrs['codes_%d' % d] = am.codes[d]
        arrs['mom_%d' % d] = am.mom[d]
    meta = json.dumps({'V': int(am.V), 'F': int(am.F), 'D': int(am.D), 'n': am.n, 'chunk': int(am.chunk), 'B': int(am.B),
                       'caps': sorted((int(k), int(v)) for k, v in am.caps.items())})
    with open(path, 'xb') as fh:
        np.savez(fh, meta=np.array(meta), **arrs)
    s = _file_sha(path)
    P16['tables'][tid] = [os.path.basename(path), s, os.path.getsize(path)]
    out('TABLE-SAVED %s: D %d F %d moments %d, %d bytes, sha256 %s (cpu so far %.1f s)' % (
        os.path.basename(path), am.D, am.F, sum(len(c) for c in am.codes), os.path.getsize(path), s, cpu()))


def _load_table(tid):
    fname, s, size = P16['tables'][tid]
    path = os.path.join(TABD, fname)
    if os.path.getsize(path) != size or _file_sha(path) != s:
        raise ValueError('the cached table %s does not have its recorded size and sha256' % fname)
    z = np.load(path, allow_pickle=False)
    meta = json.loads(str(z['meta']))
    am = amom2b.AllMom2.__new__(amom2b.AllMom2)
    am.V, am.F, am.D, am.n, am.chunk, am.B = meta['V'], meta['F'], meta['D'], meta['n'], meta['chunk'], meta['B']
    am.caps = dict((k, v) for k, v in meta['caps'])
    am.groups, am.pw, am.Gam = z['groups'], z['pw'], z['Gam']
    am.codes = [z['codes_%d' % d] for d in range(am.D + 1)]
    am.mom = [z['mom_%d' % d] for d in range(am.D + 1)]
    am._p16id = tid
    out('TABLE-LOADED %s: D %d F %d moments %d (cpu so far %.1f s)' % (fname, am.D, am.F, sum(len(c) for c in am.codes), cpu()))
    return am


_engine0 = riglap4._engine


def _engine_p16(G, n, W, idx, D, key):
    """riglap4._engine with a disk cache for tables of degree >= 13: a recorded table is loaded, a new one is built after a budget
    check and saved; the in-process cache (_ENG) works as before."""
    k = (key, tuple(idx), D)
    if k in riglap4._ENG:
        return riglap4._ENG[k]
    if D < 13:
        return _engine0(G, n, W, idx, D, key)
    Wi = W[:, list(idx)]
    tid = _tab_id(G, n, Wi, D, None, None)
    pth_ = os.path.join(TABD, tid + '.npz')
    if tid not in P16['tables'] and os.path.exists(pth_):   # v1_3: adopt the file built under the same key (another family, or a copy)
        P16['tables'][tid] = [os.path.basename(pth_), _file_sha(pth_), os.path.getsize(pth_)]
        out('TABLE-ADOPTED %s: sha256 %s, %d bytes (the same key; built by another family or copied)' % (
            os.path.basename(pth_), P16['tables'][tid][1], P16['tables'][tid][2]))
    if tid in P16['tables']:
        am = _load_table(tid)
    else:
        _budget(5.0 + 9e-6 * math.comb(D + len(idx), len(idx)), 'the D-%d table on %d forms' % (D, len(idx)))   # pk22 v1_5: by moments
        t1 = cpu()
        am = amom2b.AllMom2(G, n, D, W=Wi)
        am._p16id = tid
        out('TABLE-BUILT D %d F %d: %.2f s' % (D, am.F, cpu() - t1))
        _save_table(am, tid)
    riglap4._ENG[k] = am
    return am


def _poly_hash(P):
    return hashlib.sha256(repr(sorted(P.items())).encode()).hexdigest()[:32]


def _am_id(am):
    tid = getattr(am, '_p16id', None)
    if tid is None:
        tid = _tab_id(am.Gam, am.n, np.eye(1), am.D, am.groups, am.caps)
        am._p16id = tid
    return tid


_E2_0 = amom2b.AllMom2.E2


def _E2_p16(self, P, Q):
    """AllMom2.E2 for big inputs (more than 2e8 term pairs) as a sum over chunks of P's terms (sorted), each chunk's value memoized on
    disk (s16memo) and taken from there when a later piece meets the same E2 again; a budget check before each new chunk."""
    if len(P) * len(Q) <= 2e8:
        return _E2_0(self, P, Q)
    base = '%s|%s|%s' % (_am_id(self), _poly_hash(P), _poly_hash(Q))
    items = sorted(P.items())
    csz = max(1, int(2e9 // max(1, len(Q))))
    tot = 0.0
    for ci, s in enumerate(range(0, len(items), csz)):
        key = '%s|%d|%d' % (base, csz, ci)
        if key in P16['memo']:
            tot += P16['memo'][key]
            continue
        chunk = dict(items[s:s + csz])
        _budget(len(chunk) * len(Q) * 4.5e-8 + 5, 'an E2 chunk of %d x %d terms' % (len(chunk), len(Q)))
        t1 = cpu()
        v = _E2_0(self, chunk, Q)
        P16['memo'][key] = v
        with open(P16['memo_path'], 'a') as fh:
            fh.write(json.dumps({'k': key, 'v': repr(v)}) + '\n')
        out('E2-CHUNK %d of %d (%d x %d terms): %.1f s (cpu so far %.1f s)' % (ci + 1, (len(items) + csz - 1) // csz, len(chunk), len(Q), cpu() - t1, cpu()))
        tot += v
    return tot


def p16_state():
    st = {'memo': os.path.basename(P16['memo_path']), 'memo_sha': _file_sha(P16['memo_path']), 'memo_entries': len(P16['memo']),
          'tables': P16['tables']}
    out('CACHE-STATE ' + json.dumps(st, sort_keys=True))


def p16_setup():
    """the piece number from the range pK; C-CACHE-CHAIN: piece 1 starts with no memo, piece K > 1 needs piece K-1's output with VERDICT
    lines exactly ['VERDICT VALID'] and one CACHE-STATE line whose memo and table sha256s the files on disk still have (PLANT-CACHE);
    then the disk cache and the chunked E2 are installed."""
    global RNG
    if not re.fullmatch(r'p[1-9]', RNG):
        out('a P16 item needs the range p1 .. p9, not %r' % RNG)
        out('VERDICT INVALID (range)')
        sys.exit(2)
    P16['piece'] = int(RNG[1:])
    RNG = 'all'
    if not os.path.isdir(TABD):
        os.mkdir(TABD)
    P16['memo_path'] = os.path.join(HLD, 'out', 's16memo_%s_N%d.jsonl' % (FAM, NN))   # pk23 hl_v1
    k = P16['piece']
    if k == 1:
        ok = not os.path.exists(P16['memo_path'])
        gate('C-CACHE-CHAIN', ok, '(piece 1: no memo %s yet; no recorded table)' % os.path.basename(P16['memo_path']))
        if ok:
            open(P16['memo_path'], 'x').close()
    else:
        prev = 'm3ref_hl_v1_%s.%d.p%d_%s.out' % (FAM, NN, k - 1, TRIAL)   # pk23 hl_v1: its own piece outputs, same TRIAL
        lines = read_bytes(os.path.join(HLD, 'out', prev)).decode('utf-8').split('\n')   # pk23 hl_v1
        vl = [ln for ln in lines if ln.startswith('VERDICT')]
        sts = [json.loads(ln[len('CACHE-STATE '):]) for ln in lines if ln.startswith('CACHE-STATE ')]
        done = any(ln.startswith('P16-DONE') for ln in lines)
        ok = vl == ['VERDICT VALID'] and len(sts) == 1 and not done
        st = sts[0] if len(sts) == 1 else {}
        bad = []
        if ok:
            if _file_sha(P16['memo_path']) != st['memo_sha']:
                bad.append(st['memo'])
            for tid, (fname, s, size) in st['tables'].items():
                p_ = os.path.join(TABD, fname)
                if not os.path.exists(p_) or os.path.getsize(p_) != size or _file_sha(p_) != s:
                    bad.append(fname)
        gate('C-CACHE-CHAIN', ok and not bad, '(piece %d: %s has VERDICT lines %r, one CACHE-STATE line and no P16-DONE; the memo (%d entries) '
             'and %d tables have its sha256s)%s' % (k, prev, vl, st.get('memo_entries', -1), len(st.get('tables', {})),
                                                   (': differ ' + ', '.join(bad)) if bad else ''))
        if ok and not bad:
            P16['tables'] = {tid: list(v) for tid, v in st['tables'].items()}
            with open(P16['memo_path']) as fh:
                for ln in fh:
                    d = json.loads(ln)
                    P16['memo'][d['k']] = float(d['v'])
            h0 = st['memo_sha']
            plant('PLANT-CACHE', _file_sha(P16['memo_path']) != h0[:-1] + ('0' if h0[-1] != '0' else '1'),
                  '(the memo against its recorded sha256 with the last digit changed)')
    if FAILS:
        finish()
        sys.exit(1)
    riglap4._engine = _engine_p16
    amom2b.AllMom2.E2 = _E2_p16
    out('P16 piece %d of %s N=%d: disk table cache %s, E2 memo %s (%d entries)' % (k, FAM, NN, TABD, os.path.basename(P16['memo_path']), len(P16['memo'])))


def p16_partial(why):
    out('PREP-PARTIAL piece %d: %s' % (P16['piece'], why))
    p16_state()


def p16_done(pr):
    """the finished prep against m3ref_v1_8's dmaxH-12 record of the base family: every rE part, nE, nE4, nC8 and nC6 (P16-PART)."""
    fn = ('%s.%d.all_z9sym.out' % (REF16BASE[FAM], NN)) if FAM in REF16BASE else None   # pk22 copy
    text = read_bytes(os.path.join(OWN, 'out', fn)) if fn else b''
    if fn is None:
        out('P16-PART none (%s has no dmaxH-12 base record)' % FAM)
    elif sha(text) == REF16BASE_SHA[fn]:
        p12 = [json.loads(ln[9:]) for ln in text.decode('utf-8').split('\n') if ln.startswith('PREPJSON ')][0]
        q = lambda a, b: ('%.4g' % (a / b)) if b else 'n/a'
        for lab, v in pr.rE_parts.items():
            out('P16-PART %s: dmaxH 16 %.6e, dmaxH 12 %.6e, ratio 16/12 %s' % (lab, v, p12['rE_parts'].get(lab, float('nan')), q(v, p12['rE_parts'].get(lab, 0.0))))
        out('P16-PART rE: dmaxH 16 %.6e, dmaxH 12 %.6e, ratio %s' % (pr.rE, p12['rE'], q(pr.rE, p12['rE'])))
        for lab in ('nC8', 'nC6'):
            out('P16-PART %s: dmaxH 16 %.6e, dmaxH 12 %.6e, ratio %s' % (lab, getattr(pr, lab), p12[lab], q(getattr(pr, lab), p12[lab])))
        for j in (1, 2, 3):
            out('P16-PART nE[%d] %.6e (12: %.6e), nE4[%d] %.6e (12: %.6e)' % (j, pr.nE[j], p12['nE'][j], j, pr.nE4[j], p12['nE4'][j]))
    out('P16-DONE piece %d of %s N=%d' % (P16['piece'], FAM, NN))
    p16_state()


# ------------------------------------------------------------------ C-3 calibration of the dmaxH fallback on vD (m3ref_v1_6)
REFV14 = {   # m3ref_v1_4's vD records (z9sym), read by C-VD14
    'm3ref_v1_4_vD.4.all_z9sym.out': 'e08acdb1017b62fec802c9d913e63638425fa99cafa6315a8fd66f5093dd08ac',
    'm3ref_v1_4_vD.3.all_z9sym.out': 'abd71c3b94a71b7841b008f33cf6a1deaff13d81a615b3850bd3e3eecff47f91',
}


def rel_diff(a, b):
    return abs(a - b) / abs(b) if b else abs(a)


def cal_vals(pr, B):
    """one calibration prep's prep norms and bar parts, flat."""
    v = {'rE ' + k: x for k, x in pr.rE_parts.items()}
    v['rE'] = pr.rE
    v['nC8'], v['nC6'] = pr.nC8, pr.nC6
    for j in range(1, len(pr.nE)):
        v['nE[%d]' % j] = pr.nE[j]
        v['nE4[%d]' % j] = pr.nE4[j]
    for k in ('Nc', 'Np', 'Pout', 'Pout_p', 'farbase'):
        v[k] = getattr(pr, k)
    for k, x in B.items():
        v['B ' + k] = x
    v['err'] = sum(B.values())
    return v


def cal_ratio(v, w):
    """v[k] / w[k] for the keys of w that v has (None where both are 0, +-inf where only w[k] is 0)."""
    return {k: (v[k] / w[k] if w[k] else (None if v[k] == 0 else math.copysign(math.inf, v[k]))) for k in w if k in v}


def run_dcal():
    """the C-3 (041e0a1d, suggested, INFO): vD's prep at dmaxH 18 (riglap5s.Prep5s, and Prep5sH at 18), 14 and 12, each with
    bound5s on D_Z2; C-VD14, C-H18 and C-CAL with their plants, CAL-INFO and CALJSON (the module docstring has the rules)."""
    g, NPB, keys = family('vD')
    riglap5b.NPOLY_B = NPB
    rr = [math.sqrt(min(S_RAD * g.G[v, v] / J_REF, RCAP)) for v in range(g.V)]
    name, facs, refs = keys[0]
    out('family vDcal N=%d: the vD graph (V %d, F %d), NPOLY_B %d, qcap %d, key %s, J_REF %g, rule (%g, %g, %g), TRIAL %s' % (
        NN, g.V, g.F, NPB, QCAP['vD'], name, J_REF, S_RAD, RCAP, RHO_P, TRIAL))
    V, AK, SPLIT, OK = {}, {}, {}, {}
    for tag in ('s18', 'h18', 'h14', 'h12'):
        STAGE[0] = 'calibration %s' % tag
        t1 = cpu()
        if tag == 's18':
            pr = riglap5s.Prep5s(g, J_REF, rr, RHO_P, key='cal' + tag, qcap=QCAP['vD'])
        else:
            pr = Prep5sH(g, J_REF, rr, RHO_P, key='cal' + tag, qcap=QCAP['vD'], dmaxH=int(tag[1:]))
        OK[tag] = pr.ok
        if not pr.ok:
            out('CAL prep %s: ok False' % tag)
            continue
        buf = io.StringIO()
        pr.verbose = True
        with contextlib.redirect_stdout(buf):
            ak, B = riglap5s.bound5s(pr, facs)
        pr.verbose = False
        AK[tag], V[tag], SPLIT[tag] = ak, cal_vals(pr, B), rem_split(buf.getvalue())
        out('STAGE-CPU calibration %s (%s) %.2f s: err %.6e' % (tag, 'riglap5s.Prep5s' if tag == 's18' else 'Prep5sH dmaxH %s' % tag[1:],
                                                                cpu() - t1, V[tag]['err']))
    if not all(OK.values()):
        gate('C-CAL', False, '(calibration preps not ok: %s)' % ', '.join(t for t, o in OK.items() if not o))
        return
    STAGE[0] = 'C-VD14'
    fn = 'm3ref_v1_4_vD.%d.all_z9sym.out' % NN
    good = TRIAL == 'z9sym' and sha(read_bytes(os.path.join(OWN, 'out', fn))) == REFV14[fn]
    rak, rB = ref12(fn, name) if good else ([], {})
    rerr = sum(rB.values())
    dB = max([rel_diff(V['s18']['B ' + k], x) for k, x in rB.items()] + [rel_diff(V['s18']['err'], rerr)]) if good else math.inf
    dA = cmp_ak(AK['s18'], rak) if good and len(rak) == len(AK['s18']) else math.inf
    gate('C-VD14', dB <= 1e-13 and dA <= 1e-12, '(riglap5s.Prep5s here against %s, TRIAL %s, sha pinned: bar parts and err max relative '
         'difference %.2e (tol 1e-13), a_k %.2e of max|a_k| (tol 1e-12))' % (fn, TRIAL, dB, dA))
    plant('PLANT-VD14', not (rel_diff(V['s18']['err'], rerr * (1 + 1e-9)) <= 1e-13), '(the record\'s err times 1 + 1e-9)')
    STAGE[0] = 'C-H18'
    same = set(V['h18']) == set(V['s18']) and len(AK['h18']) == len(AK['s18'])
    d18 = max(rel_diff(V['h18'].get(k, math.inf), x) for k, x in V['s18'].items())
    a18 = cmp_ak(AK['h18'], AK['s18'])
    gate('C-H18', same and d18 <= 1e-13 and a18 <= 1e-12, '(Prep5sH at dmaxH 18 against riglap5s.Prep5s, %d prep norms and bar parts: '
         'max relative difference %.2e (tol 1e-13), a_k %.2e of max|a_k| (tol 1e-12))' % (len(V['s18']), d18, a18))
    dp = max(rel_diff(V['h18'].get(k, math.inf), x * (1 + 1e-9)) for k, x in V['s18'].items())
    plant('PLANT-H18', not (dp <= 1e-13), '(the Prep5s values times 1 + 1e-9)')
    STAGE[0] = 'C-CAL'
    RAT = {}
    for tag in ('h12', 'h14'):
        RAT[tag] = cal_ratio(V[tag], V['h18'])
        low = sorted(k for k, r in RAT[tag].items() if r is not None and not (r >= 1 - 1e-12))
        same = set(V[tag]) == set(V['h18']) and len(AK[tag]) == len(AK['h18'])
        da = cmp_ak(AK[tag], AK['h18'])
        gate('C-CAL', same and not low and da <= 1e-12, '(dmaxH %s against 18: each of %d prep norms and bar parts divided by its dmaxH-18 '
             'value >= 1 - 1e-12; a_k %.2e of max|a_k| (tol 1e-12))%s' % (tag[1:], len(RAT[tag]), da, (': below at ' + ', '.join(low)) if low else ''))
        chg = sorted((k, r) for k, r in RAT[tag].items() if r is not None and abs(r - 1) > 1e-12)
        out('CAL-INFO dmaxH %s / 18, changed (|ratio - 1| > 1e-12): %s' % (tag[1:], ', '.join('%s %.6g' % kr for kr in chg) if chg else 'none'))
        out('CAL-INFO dmaxH %s / 18, unchanged: %s' % (tag[1:], ', '.join(k for k, r in sorted(RAT[tag].items(), key=lambda kv: kv[0])
                                                                          if r is None or abs(r - 1) <= 1e-12)))
    inv = [1.0 / r for r in RAT['h12'].values() if r]
    plant('PLANT-CAL', any(not (r >= 1 - 1e-12) for r in inv), '(the dmaxH-12 ratios inverted, as if the exact norms were the larger)')
    bad = list(AK['h12'])
    im = max(range(len(bad)), key=lambda i: abs(bad[i]))
    bad[im] = bad[im] * (1 + 1e-6)
    plant('PLANT-CAL-AK', not (cmp_ak(bad, AK['h18']) <= 1e-12), '(the largest dmaxH-12 coefficient times 1 + 1e-6)')
    out('CALJSON ' + json.dumps({'N': NN, 'J': J_REF, 'key': name, 'trial': TRIAL, 'rule': [S_RAD, RCAP, RHO_P], 'values': V, 'ratios': RAT,
                                 'rem_split_printed': SPLIT, 'ak': AK}))


try:
    T0 = cpu()
    if FAM in OFSPEC:
        run_of(FAM)
        finish()
        sys.exit(0)
    if FAM == 'OFC':
        run_ofc()
        finish()
        sys.exit(0)
    if FAM == 'vDcal':
        run_dcal()
        finish()
        sys.exit(0)
    if FAM in U16FAM:
        run_u16()
        finish()
        sys.exit(0)
    if FAM in P16FAM:
        p16_setup()
    STAGE[0] = 'graph'
    if FAM in CFAM and not center_setup():
        finish()
        sys.exit(1)
    g, NPB, keys = family(FAM)
    riglap5b.NPOLY_B = NPB
    rr = [math.sqrt(min(S_RAD * g.G[v, v] / J_REF, RCAP)) for v in range(g.V)]
    ap = RHO_P * RHO_P
    out('family %s N=%d: V %d, F %d, pairs %s, NPOLY_B %d, qcap %d, %d keys: %s' % (FAM, NN, g.V, g.F, g.pairs, NPB, QCAP[FAM], len(keys),
                                                                             ', '.join(k[0] for k in keys)))
    if FAM in NPB4:
        gate('C-NPB', NPB == NPB4[FAM] and NPB ** g.F < 2 ** 63, '(npoly base %d for F = %d forms: %d**%d = %d, below 2**63 = %d)' % (
            NPB, g.F, NPB, g.F, NPB ** g.F, 2 ** 63))
    out('STAGE-CPU graph %.2f s' % (cpu() - T0))
    if FAM in S8FAM:
        s8_graph_check()
    if FAM in ('mix', 'free'):
        STAGE[0] = 'r_main'
        VD, ED = strip_graph(2, (A_EX, B_EX))
        gD = Graph(VD, ED, [(0, 1), (1, 2), (0, 2), (3, 4), (4, 5), (3, 5)], N=NN)
        gmix, gfree = Graph(6, Emix, [(0, 1), (1, 2), (0, 2)], N=NN), Graph(6, Efree, [], N=NN)
        r_main = math.exp(2 * gmix.logmain(J_REF) - gfree.logmain(J_REF) - gD.logmain(J_REF))
        rel = abs(r_main / ENDW_RMAIN - 1)
        gate('C-RMAIN', rel <= 1e-11, 'r_main %r at J = 300 vs endw_N%d_J170 %r: relative %.1e' % (r_main, NN, ENDW_RMAIN, rel))
        plant('PLANT-RMAIN', not (abs(r_main / (ENDW_RMAIN * (1 + 1e-9)) - 1) <= 1e-11), '(the stored value times 1 + 1e-9)')
        out('RMAINJSON ' + json.dumps({'N': NN, 'r_main': r_main, 'endw170': ENDW_RMAIN}))
    if RNG == 'mono':
        names = ('g,0,0', 'Na', 'Nw')
        sel = [k for k in keys if k[0] in names]
        bars = {}
        for J in (J_REF, 600.0, 1200.0):
            pr, _ = prep(g, J, rr, 'D')
            for name, facs, refs in sel:
                STAGE[0] = 'mono %s J=%g' % (name, J)
                t1 = cpu()
                ak, B = riglap5s.bound5s(pr, facs)
                bars[(name, J)] = B
                out('MONOJSON ' + json.dumps({'N': NN, 'J': J, 'key': name, 'ak': ak, 'B': B, 'cpu': round(cpu() - t1, 2)}))
        for name, facs, refs in sel:
            for J in (600.0, 1200.0):
                rat = {p: (bars[(name, J)][p] / bars[(name, J_REF)][p] if bars[(name, J_REF)][p] > 0 else None) for p in ('rem', 'tail', 'ann', 'far')}
                mono = all(r is None or r <= 1.0 for r in rat.values())
                out('C-MONO-INFO %s J=%g / J=300 per part %s -> %s' % (name, J, json.dumps(rat), 'nonincreasing' if mono else 'NOT nonincreasing'))
        finish()
        sys.exit(0)
    lo, hi = (0, len(keys) - 1) if RNG == 'all' else tuple(int(x) for x in RNG.split('-'))
    if not (0 <= lo <= hi < len(keys)):
        out('bad range %s for %d keys' % (RNG, len(keys)))
        out('VERDICT INVALID (range)')
        sys.exit(2)
    try:
        pr, dtp = prep(g, J_REF, rr, FAM)
    except StopPiece as sp_:
        p16_partial('prep: %s' % sp_)
        finish()
        sys.exit(0)
    STAGE[0] = 'theta0'
    th0, fb, tree = theta0(g, J_REF, ap)
    rel = abs(fb / pr.farbase - 1) if pr.ok else 0.0
    gate('C-THETA', (not pr.ok) or rel <= 1e-12, 'theta0 %r reproduces farbase %r: relative %.1e' % (th0, getattr(pr, 'farbase', None), rel))
    plant('PLANT-THETA', (not pr.ok) or not (abs(fb / (pr.farbase * (1 + 1e-9)) - 1) <= 1e-12), '(the base times 1 + 1e-9)')
    pj = {'family': FAM, 'N': NN, 'J': J_REF, 'rho': rr, 'a_v': [r * r for r in rr], 'ap': ap, 'ok': pr.ok, 'tree': tree, 'theta0': th0,
          'logmain': g.logmain(J_REF), 'cpu_prep': round(dtp, 2)}
    if pr.ok:
        pj.update({'rE': pr.rE, 'rE_parts': pr.rE_parts, 'nE': pr.nE, 'nE4': pr.nE4, 'nC8': pr.nC8, 'nC6': pr.nC6, 'Nc': pr.Nc, 'Np': pr.Np,
                   'Pout': pr.Pout, 'Pout_p': pr.Pout_p, 'farbase': pr.farbase})
    out('PREPJSON ' + json.dumps(pj))
    try:
        n = run_keys(g, pr, keys, J_REF, rr, lo, hi, [True])
    except StopPiece as sp_:
        p16_partial('keys: %s' % sp_)
        finish()
        sys.exit(0)
    out('keys done %d of range %d-%d' % (n, lo, hi))
    if FAM in S8FAM:
        s8_checks()
        if FAM in ANALOG_SRC:
            s8_analog()
        if FAM in REF16BASE:
            s8_dmax16_info()
        if FAM in CFAM:
            s8_center()
        if FAM in V3FAM:
            v3_checks()
        if FAM in V4FAM:
            v4_checks()
        if FAM in V9FAM:
            v9_checks(pj)
    if FAM in P16FAM:
        p16_done(pr)
    finish()
except SystemExit:
    raise
except BaseException:
    out('EXCEPTION in stage %s:' % STAGE[0])
    for ln in traceback.format_exc().rstrip().split('\n'):
        out('  ' + ln)
    out('VERDICT INVALID (EXCEPTION)')
    sys.exit(1)
