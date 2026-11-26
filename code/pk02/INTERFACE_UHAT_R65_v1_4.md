# INTERFACE_UHAT_R65_v1_4: the contract between the u-hat record and R6.5's reader (FROZEN)

pk02, 2026-11-08, the frozen version. After v1 (6bda63f3),
v1_1 (9e72ae0c), v1_2 (cc40e32a, never sent) and v1_3 (d79f4e6a). Agreed by the review (CHECK_INTERFACE_UHAT_R65_v1_1 cbc3020c: accept with
P-1 and P-2) and by pk12's reader-side check of v1_1 (accept with P-1, ROWS named), with the 20:25Z rule on
the RECORD line's form and the review. V1_4 takes the rule on the N4
piece range, given after main checked kt_uhat_asm_v1_2 and this table's v1_3: centres.pieces and J_RANGE are stated per N, and at N4 the record covers
P0061..P0903 only, the range of S8, R6.5 and pk12's GJJ export (40957f70). RH_MODULE_v1_4 cor:rhstrips (l.442-445) proves
Cov >= 0 for every pair at N4 for J in [20, 350], and N4's P0061 starts at J = 349.3562470527477, inside that band. v1_4 also drops the
comparisons against ADD9 and ADD10 tolerances from the INFO keys (obsolete under lo > 0). The writer (pk02's kt_uhat_asm, from
v1_3 on) and the reader (R6.5's kt_p212_cert, pk12) both conform to this table; neither reads the other's code as the contract. It
supersedes the reader's key set of kt_p212_cert_v1_2_2 (24a59e32) and the writer's of kt_uhat_asm_v1_1 (3ce28648).

## 1. Value forms
Every key has exactly one form, named in sect. 2-4; a value outside its form is refused.
- dec: a finite decimal matching [-+]?[0-9]+(\.[0-9]*)?([eE][-+]?[0-9]+)?, exact as written.
- up: one dec, an upper end rounded up from the exact bound.
- ball: "lo hi", two decs with lo <= hi, lo rounded down and hi rounded up from the exact ends, so the exact set lies in [lo, hi]. This is
  the only form for two-sided quantities; "mid rad" is not used anywhere.
- tag: one word from the list the table gives.
- src: path:sha256, the path relative to code/ and the full 64-hex sha256 of that file.
- list: words separated by single spaces.
- range: P[0-9]{4}\.\.P[0-9]{4}, a first and a last piece index.
- text: free text whose first word the table fixes.

## 2. Header (keys spelled exactly)
| key | form | value |
|---|---|---|
| RECORD | tag | UHAT_ASM_v1 |
| FORMAT | tag | S4U_KV_v1 |
| EXPORT_STATUS | tag | MOCK or CERTIFIED (a failed run writes no record) |
| MOCK | tag | TRUE when EXPORT_STATUS is MOCK, FALSE when CERTIFIED |
| VERDICT_OF_WRITER | tag | VALID |
| N | tag | 4 or 3 |
| INTERFACE | src | pk02/INTERFACE_UHAT_R65_v1_4.md:<sha256> (this frozen table) |
| ROWS | src | pk12/R65_D3_ROUTE0_ROWS_v1.kv:c6822a6d3355b819813f78f561d16a745e016de757da968e78391c81fc7e48f1 (its ROWS_N<N> list: 34 rows at N4, 30 at N3) |
| J_RANGE | list | per N: the J_lo of the first piece of centres.pieces as written in centres.source, then inf: N4 "349.3562470527477 inf", N3 "300.0 inf" |
| J_UNIFORMITY | text | first word UNIFORM-J; each value below holds for every J in J_RANGE: the max over centres.pieces for up, the hull for ball |
| centres.source | src | pk15/out/export_p2_14_means_cert_kt_p2_assembly_v1_37.kv:<sha256> |
| centres.pieces | range | per N, P<first>..P<last>: N4 P0061..P0903, N3 P0000..P0903 |
| M2B | src | pk02/M2B_KV_v1.txt:<sha256>; the reader takes eps_r = N<N>_EPS_R_300 and s = N<N>_S_300 from it |
| CODE, LIB | src | the writer's code and library |
| WORLD_U_HAT | list | every u-hat-world key of sect. 3 |
| WORLD_TRUE_U | list | every true-vacuum key of sect. 3 |
| END | tag | UHAT_ASM_v1 (last line) |
- No eps_r and no s key appears in the record; the reader reads both from the pinned M2B record.

## 3. Values (one spelling per quantity; world: hat = u-hat, true = true vacuum, transfer = a bound between the two)
Route 0, per row. <row> = the reader's row name rname = "<fam> (<dL>,<dR>)" written as <fam>_<dL>_<dR> with '-' as 'm': D3 (1,2) ->
D3_1_2, D3 (-1,2) -> D3_m1_2, D3 (0,inf) -> D3_0_inf. The writer writes one block for every row of ROWS. A route P row carries T_s and no
T_U4; a route H row carries T_U4 and no T_s.
| key | form | world | meaning |
|---|---|---|---|
| route0b_hat.<row>.route | tag | - | P or H |
| route0b_hat.<row>.formula | tag | - | ROUTE_P_UHAT_v1 (q_b = q_hat + T_s) or ROUTE_H_NB1 (N-B1) |
| route0b_hat.<row>.q_hat_hi | up | hat | route 0's q-hat_b, max over pieces |
| route0b_hat.<row>.beta_hat_s | up | transfer | beta-hat_s, max over pieces |
| route0b_hat.<row>.m_hat_s_hi | up | hat | |m-hat_s|, max over pieces |
| route0b_hat.<row>.m_hat_s_source | tag | - | beta-hat_fallback or certified_mean |
| route0b_hat.<row>.xu_hi | up | hat | (q_hat_hi^2 + m_hat_s_hi^2)^(1/2) from those maxima (no (1 - s^2)^(-1/2) factor at the site) |
| route0b_hat.<row>.T_s | up | transfer | route P only: U4's T at the site on those maxima |
| route0b_hat.<row>.T_U4 | up | transfer | route H only: U4's T on those maxima |
| route0b_hat.<row>.q_b_hi | up | true | the row's final value by its formula on the recorded parts (route H with eps_r and s from M2B) |
L0 windows, <w> = D4L0 or D4ML0:
| key | form | world | meaning |
|---|---|---|---|
| l0_hat.<w>.route | tag | - | H |
| l0_hat.<w>.L0_hi | up | hat | the Cov form (a variance), max over pieces |
| l0_hat.<w>.q_hat_hi | up | hat | L0_hi^(1/2) rounded up |
| l0_hat.<w>.m_hat_s_hi | up | hat | |m-hat_s|, max over pieces |
| l0_hat.<w>.beta_hat | up | transfer | beta-hat (D4, D4M), max over pieces |
| l0_hat.<w>.xu_hi | up | hat | (1 - s^2)^(-1/2) (q_hat_hi^2 + m_hat_s_hi^2)^(1/2) from those maxima |
| l0_hat.<w>.xsu_hi | up | hat | the adjoint window's xu_hi (same centres), else beta_hat |
| l0_hat.<w>.xsu_source | tag | - | adjoint_same_c or beta-hat_fallback |
| l0_hat.<w>.T_U4 | up | transfer | U4's T on those maxima |
| l0_hat.<w>.q_hi | up | true | N-B1's route H: (1 - s^2)^(-1/2) q_hat_hi + eps_r m_hat_s_hi/(1 - eps_r) + T_U4 |
B' (FA):
| key | form | world | meaning |
|---|---|---|---|
| bprime_hat.FA.basis | tag | - | raw |
| bprime_hat.FA.v_hat_raw.<j>, j = 0..3 | ball | hat | E_j[X_c] in u-hat units, the hull over pieces; the same keys in both modes |
| bprime_hat.FA.T_v | up | transfer | beta-hat s', max over pieces (ADD6) |
| bprime_hat.FA.T_v_source | src | - | pk02/DESIGN_UHAT_ASM_v1_3_ADD6.md:a0fbebdd6da733c7538c609a9af737438c1b199c69b6da505763beee16fe60ad |
"Over pieces" means over centres.pieces of the record's N.
W-matrix: this table defines no wmat_hat key. Until a later table version defines the wmat_hat keys and their forms, the
writer writes none, any wmat_hat key is outside the table and refused, and a missing wmat_hat means WAIT-W.
WORLD lists (sect. 2): WORLD_U_HAT holds every key of world hat; WORLD_TRUE_U every key of world true; transfer keys are in neither.

## 4. INFO keys
Keys under the prefix info. are not read by R6.5 (per-piece values info.route0b_hat.P<pppp>.* and info.bprime_hat.FA.P<pppp>.*, for the
pieces of centres.pieces). They follow sect. 1's forms. The record carries no comparison against ADD9 or ADD10 tolerances.

## 5. Obligations
- Writer:
  - each J-uniform part is its own max (ball: hull) over centres.pieces (at N4 over P0061..P0903 only), and every final value is its
    form on the recorded parts (ADD4 sect. 3);
  - gates C-WORLD-U (each key in exactly its world list; plant: a true key filed under WORLD_U_HAT, run through the gate code), C-DEC
    (each decimal re-read brackets its exact end outward) and C-FORM (the forms of sect. 1, the key set of sect. 2-4 and the reader's
    refusals below, on the lines as written; plant: perturbed copies of the record, each refused); no record when a gate fails or a
    plant does not fire;
  - Rule V2 (strict): the run output (out_kt_uhat_asm_<version>_<item>_<tag>.out) carries exactly
    one line "RECORD <record file name> sha256 <full sha256>" per record file it writes, and exactly one VERDICT line, "VERDICT VALID",
    which is its last line;
  - one route0b_hat block for every row of ROWS_N<N>, with route P and formula ROUTE_P_UHAT_v1, or route H and ROUTE_H_NB1.
- Reader:
  - pins the writer's run output with the record and checks Rule V2 before it reads the record: the one RECORD line that names its record
    (name and sha256), and the single VERDICT line "VERDICT VALID" as the last line;
  - refuses a missing key, a key outside the table (info.* excepted; any wmat_hat key), a value outside its form, a src whose file
    does not hash to it, a route P row with T_U4 or a route H row with T_s, and a route tag that disagrees with its formula tag;
  - refuses centres.source, centres.pieces or J_RANGE that is not exactly its own pinned means export, its own piece set for the record's
    N and that set's J range;
  - refuses M2B, ROWS and INTERFACE values that differ from its own pins, even when their hashes are right;
  - refuses a negative value in every up of sect. 3 (q_hat_hi, m_hat_s_hi, xu_hi, xsu_hi, beta_hat_s, beta_hat, L0_hi, T_v, q_b_hi,
    q_hi), refuses T_s or T_U4 <= 0, and refuses eps_r or s from M2B outside [0, 1);
  - recomputes every q_b_hi and q_hi from the recorded parts with eps_r and s from M2B, checks them two-sided at 1e-9 and takes the max
    (ADD7 sect. 1);
  - treats a missing wmat_hat as WAIT-W on a clean refusal path, never an error.
