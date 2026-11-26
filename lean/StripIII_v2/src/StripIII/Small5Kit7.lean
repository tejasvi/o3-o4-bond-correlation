/-
StripIII.Small5Kit7: the small-n list after the kit v7
stage 1 runs. `box5AllList34` holds the members of 34 of the 36 orbits of P_3 x P_5: the 27 orbits of `StripIII.box5AllList`, from the
box record of run 013023Z (version v1_2, the same table), and the 7 orbits G04, G08, G11, G16, G20, G32, G36 that the kit
v7 stage 1 runs certify at both N (`box5Kit7S1`). The orbits G05 and G33 are added in StripIII.Small5Final: `box5AllList34_open_until_G05_G33` shows
that their members, as the probe enumerates them, are all the list lacks. `smallN_final` gives the small-n theorem once the stage 2
pairs pass the checks.
-/
import StripIII.Small5Proof

noncomputable section

namespace G2Kernel

open StripIII

/-- The members of the 7 orbits G04, G08, G11, G16, G20, G32, G36 of P_3 x P_5 that the kit v7 stage 1 runs certify at N = 3 (J1 300) and
N = 4 (J1 350): record code/pk23/o5/records/O5_BOX_RECORD_run_20261118T114847Z_v1_1.md (sha8 451b2115; manifest
MANIFEST_O5_BOX_RECORD_run_20261118T114847Z_v1_1.sha256 sha8 62e585ec; table O5_RECORD_TABLE_box_run_20261118T114847Z_v1.tsv sha8 c317dac0).
Made from the table by the converter record2lean_v1_1.py,
which takes an orbit only if it is certified at both N with the same members. -/
def box5Kit7S1 : List (ECode × ECode) := [
-- source code/pk23/o5/records/O5_RECORD_TABLE_box_run_20261118T114847Z_v1.tsv sha256 c317dac0cc1f3681f91e689e13119a608e0ff04fa03aaf99711f6c1e972d05c2; labels n5_G04,n5_G08,n5_G11,n5_G16,n5_G20,n5_G32,n5_G36; N 3,4
  -- n5_G04 (4 members): N=3 J1 300 L 4.951049e-05 c2 8.234492e-05 out fefa8063; N=4 J1 350 L 1.140998e-04 c2 1.235174e-04 out 34be0d83
  (.hor 0 0, .hor 1 2),
  (.hor 0 3, .hor 1 1),
  (.hor 1 1, .hor 2 3),
  (.hor 1 2, .hor 2 0),
  -- n5_G08 (2 members): N=3 J1 300 L 6.179895e-05 c2 6.696915e-05 out b4a8bc02; N=4 J1 350 L 8.720119e-05 c2 1.004537e-04 out 43a3e916
  (.hor 0 0, .hor 2 3),
  (.hor 0 3, .hor 2 0),
  -- n5_G11 (4 members): N=3 J1 300 L 5.582061e-05 c2 9.996700e-05 out 7f31752a; N=4 J1 350 L 1.371444e-04 c2 1.499505e-04 out d5591848
  (.hor 0 0, .ver 0 4),
  (.hor 0 3, .ver 0 0),
  (.hor 2 0, .ver 1 4),
  (.hor 2 3, .ver 1 0),
  -- n5_G16 (4 members): N=3 J1 300 L 6.198819e-05 c2 6.696915e-05 out ddfb76b8; N=4 J1 350 L 8.765588e-05 c2 1.004537e-04 out 6ec4e018
  (.hor 0 0, .ver 1 4),
  (.hor 0 3, .ver 1 0),
  (.hor 2 0, .ver 0 4),
  (.hor 2 3, .ver 0 0),
  -- n5_G20 (4 members): N=3 J1 300 L 5.288388e-05 c2 8.234492e-05 out 113c1f2e; N=4 J1 350 L 1.151697e-04 c2 1.235174e-04 out 2498ec13
  (.hor 0 1, .hor 1 3),
  (.hor 0 2, .hor 1 0),
  (.hor 1 0, .hor 2 2),
  (.hor 1 3, .hor 2 1),
  -- n5_G32 (4 members): N=3 J1 300 L 3.072130e-05 c2 5.270075e-05 out c5e3adf9; N=4 J1 350 L 7.272306e-05 c2 7.905112e-05 out 8c469dc3
  (.hor 1 0, .ver 0 3),
  (.hor 1 0, .ver 1 3),
  (.hor 1 3, .ver 0 1),
  (.hor 1 3, .ver 1 1),
  -- n5_G36 (4 members): N=3 J1 300 L 5.066329e-05 c2 8.234492e-05 out 2bafd1d3; N=4 J1 350 L 1.144505e-04 c2 1.235174e-04 out f021bd5e
  (.hor 1 1, .ver 0 4),
  (.hor 1 1, .ver 1 4),
  (.hor 1 2, .ver 0 0),
  (.hor 1 2, .ver 1 0)
-- total 26 pairs
]

/-- the small-n list after the kit v7 stage 1 runs: 34 of the 36 orbits -/
def box5AllList34 : List (ECode × ECode) := box5AllList ++ box5Kit7S1

/-- CANDIDATE (INFO, not certified data): the members of G05 and G33 as the n = 5 probe enumerates them, by
the converter orbits2lean_v1.py -/
def candG05G33 : List (ECode × ECode) := [
-- source code/pk23/out/o5_probe_n5.out sha256 06e3266f33623533fc2a472a661e27aa67923efccce59da01cb7d6f3bca1f9cf; orbits G05,G33; members 4,4; total 8
  (.hor 0 0, .hor 1 3),
  (.hor 0 3, .hor 1 0),
  (.hor 1 0, .hor 2 3),
  (.hor 1 3, .hor 2 0),
  (.hor 1 0, .ver 0 4),
  (.hor 1 0, .ver 1 4),
  (.hor 1 3, .ver 0 0),
  (.hor 1 3, .ver 1 0)

]

/-- the list lies within the class `g5`; it holds 104 + 26 = 130 ordered pairs, one per unordered pair -/
theorem box5AllList34_inClass : box5AllInClass box5AllList34 = true := by decide +kernel
theorem box5AllList34_len : box5Kit7S1.length = 26 ∧ box5AllList34.length = 130 := by decide +kernel

/-- open until G05 and G33: the list does not cover the class yet, and the members of G05 and G33 (8 pairs, within the class) are
exactly what it lacks -/
theorem box5AllList34_open_until_G05_G33 : box5AllCheck box5AllList34 = false ∧ box5AllCheck (box5AllList34 ++ candG05G33) = true ∧
    box5AllInClass candG05G33 = true ∧ candG05G33.length = 8 := by decide +kernel

/-- **hBoxAll5** with its records, for the list `box5AllList34 ++ L2` (kind: restatement; the 27 orbits of `box5AllList` backed by
the box record v1_2 of run 013023Z, code/pk23/o5/records/O5_BOX_RECORD_run_20261118T013023Z_v1_2.md (sha8 3abdb733; manifest sha8 ff08d9ce; table
O5_RECORD_TABLE_box_run_20261118T013023Z_v1.tsv sha8 19945efd, from which `box5AllList` was made);
the 7 orbits of `box5Kit7S1` by the kit v7 stage 1
record, cited at `box5Kit7S1`; G05 and G33 in `L2` by the stage 2
records of runs 154150Z and 041647Z (StripIII.Small5Final)) -/
theorem hBoxAll5_record (N : ℕ) (L : List (ECode × ECode)) : hBoxAll5 N L =
    (∀ J : ℝ, jLow N ≤ J → ∀ e ∈ (strip 5).edgeSet, ∀ f ∈ (strip 5).edgeSet, e ≠ f →
      L.contains (edgeCode e, edgeCode f) = true → G2pair N (strip 5) (uniform J) e f) := rfl

/-- **The complete small-n theorem, final form**: `smallN_statementL` with the list `box5AllList34 ++ L2`, where `L2` holds the members of
G05 and G33 from the stage 2 records (StripIII.Small5Final), once the list passes `box5AllCheck`; the in-class premise keeps the final list free of extra
pairs, and the proof does not use it. The records of the hypotheses: `hBoxAll5_record`, and StripIII.Statement and
StripIII.Small5Statement for the others. -/
theorem smallN_final (N : ℕ) (L2 : List (ECode × ECode)) (h : box5AllCheck (box5AllList34 ++ L2) = true)
    (_hc : box5AllInClass (box5AllList34 ++ L2) = true) : smallN_statementL N (box5AllList34 ++ L2) :=
  smallN_of_list N (box5AllList34 ++ L2) h

/-- TRIAL (INFO): with the candidate members of G05 and G33 (not certified data; never to be cited as the result) -/
theorem smallN_final_trial (N : ℕ) : smallN_statementL N (box5AllList34 ++ candG05G33) :=
  smallN_final N candG05G33 box5AllList34_open_until_G05_G33.2.1 (by decide +kernel)

end G2Kernel
