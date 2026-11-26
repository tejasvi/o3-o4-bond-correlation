/-
StripIII.Small5Core: the
combinatorial part of the Lean statement that every pair of distinct edges of P_3 x P_n, n <= 5, middle-row edges included, has
Cov >= 0 at N = 3, 4 for every J >= 0. No Mathlib; it uses StripIII.Core's edge codes (every row, the middle row included), allCodes,
commonVertexAct and lrMirror, and none of Core's shape classes.
At n = 5 and J >= jLow N: a pair with no horizontal edge is a pair of vertical edges (Theorem 6.21); a pair with a common vertex is
S0 (Theorem 3.2); a mirror pair (t_i, bb_i) or a left-right mirror pair is S0 (Lemma 6.1); every other pair, one with a
horizontal edge and none of these, lies in the class `g5`, the 138 pairs of the 36 orbits of the whole-graph box runs at n = 5.
`box5AllList` holds the members of the 27 orbits that the box record of run 013023Z certifies at both N; the 9 orbits G04, G05, G08,
G11, G16, G20, G32, G33, G36 are added in StripIII.Small5Kit7 and StripIII.Small5Final, so `box5AllCheck box5AllList` alone is false (`box5AllList_open_until_kit7`).
-/
import StripIII.Core

namespace G2Kernel.StripIII

/-- a horizontal edge code (any row, the middle row included) -/
def ECode.isHor : ECode → Bool
  | .hor _ _ => true
  | .ver _ _ => false

theorem isHor_false {c : ECode} (h : c.isHor = false) : ∃ t j, c = .ver t j := by
  cases c with
  | hor r i => simp [ECode.isHor] at h
  | ver t j => exact ⟨t, j, rfl⟩

/-- the mirror pair (t_i, bb_i) of the reflection in the middle row, either order -/
def tbMirror (e f : ECode) : Bool :=
  (e == .hor 0 e.pos && f == .hor 2 e.pos) || (e == .hor 2 e.pos && f == .hor 0 e.pos)

theorem tbMirror_cases {e f : ECode} (h : tbMirror e f = true) :
    ∃ i, (e = .hor 0 i ∧ f = .hor 2 i) ∨ (e = .hor 2 i ∧ f = .hor 0 i) := by
  simp only [tbMirror, Bool.or_eq_true, Bool.and_eq_true, beq_iff_eq] at h
  exact ⟨e.pos, h⟩

/-- the class of the n = 5 box runs: two distinct valid edges of P_3 x P_5, at least one horizontal, no common vertex, not a mirror pair
(t_i, bb_i), not a left-right mirror pair -/
def g5 (e f : ECode) : Bool :=
  e.valid 5 && f.valid 5 && e != f && (e.isHor || f.isHor) && !commonVertexAct e f && !tbMirror e f && !lrMirror 5 e f

/-- every ordered pair of distinct valid edge codes of P_3 x P_n, middle-row edges included -/
def allPairsAll (n : Nat) : List (ECode × ECode) :=
  (allCodes n).flatMap fun e => ((allCodes n).filter fun f => e.valid n && f.valid n && e != f).map fun f => (e, f)

theorem mem_allPairsAll {n : Nat} {e f : ECode} (he : e.valid n = true) (hf : f.valid n = true) (hef : e ≠ f) :
    (e, f) ∈ allPairsAll n := by
  simp only [allPairsAll, List.mem_flatMap, List.mem_map, List.mem_filter]
  refine ⟨e, mem_allCodes he, f, ⟨mem_allCodes hf, ?_⟩, rfl⟩
  simp only [he, hf, Bool.true_and, bne_iff_ne, ne_eq]
  exact hef

/-- the case split at n = 5: every ordered pair of distinct valid codes is a common-vertex pair, a mirror pair (t_i, bb_i), a left-right
mirror pair, a pair of vertical codes or a pair of the class `g5` -/
theorem cases5 (e f : ECode) (he : e.valid 5 = true) (hf : f.valid 5 = true) (hef : e ≠ f) :
    (commonVertexAct e f || tbMirror e f || lrMirror 5 e f || (!e.isHor && !f.isHor) || g5 e f) = true := by
  have hne : (e != f) = true := by simp only [bne_iff_ne, ne_eq]; exact hef
  unfold g5
  rw [he, hf, hne]
  cases commonVertexAct e f <;> cases tbMirror e f <;> cases lrMirror 5 e f <;> cases e.isHor <;> cases f.isHor <;> rfl

/-- the list check (the class within the list, either order) and its converse (the list within the class) -/
def box5AllCheck (L : List (ECode × ECode)) : Bool :=
  (allPairsAll 5).all fun p => !g5 p.1 p.2 || L.contains p || L.contains (p.2, p.1)

def box5AllInClass (L : List (ECode × ECode)) : Bool := L.all fun p => g5 p.1 p.2

/-- The members of the 27 orbits of P_3 x P_5 that the box record certifies at N = 3 (J1 300) and N = 4 (J1 350), as code pairs:
record code/pk23/o5/records/O5_BOX_RECORD_run_20261118T013023Z_v1_2.md (sha8 3abdb733; table O5_RECORD_TABLE_box_run_20261118T013023Z_v1.tsv
sha8 19945efd; manifest sha8 ff08d9ce);
"certified" there means J^2 Cov >= L > 0, i.e. Cov >= L/J^2 > 0, for every
J >= J1, the members as images of the representative under the grid automorphisms. Made from the table by the converter record2lean_v1.py.
The orbits G04, G05, G08, G11, G16, G20, G32, G33, G36 (34 pairs) are added in StripIII.Small5Kit7 and StripIII.Small5Final. -/
def box5AllList : List (ECode × ECode) := [
-- source code/pk23/o5/records/O5_RECORD_TABLE_box_run_20261118T013023Z_v1.tsv sha256 19945efdec713105192a164fff21914a1da8341c1e8a2513178ea784fccf1b21; labels n5_G01,n5_G02,n5_G03,n5_G06,n5_G07,n5_G09,n5_G10,n5_G12,n5_G13,n5_G14,n5_G15,n5_G17,n5_G18,n5_G19,n5_G21,n5_G22,n5_G23,n5_G24,n5_G25,n5_G26,n5_G27,n5_G28,n5_G29,n5_G30,n5_G31,n5_G34,n5_G35; N 3,4
  -- n5_G01 (4 members): N=3 J1 300 L 8.908049e-04 c2 1.011872e-03 out 13ed6cee; N=4 J1 350 L 1.259698e-03 c2 1.517808e-03 out 8c89d6ae
  (.hor 0 0, .hor 0 2),
  (.hor 0 1, .hor 0 3),
  (.hor 2 0, .hor 2 2),
  (.hor 2 1, .hor 2 3),
  -- n5_G02 (4 members): N=3 J1 300 L 4.345187e-02 c2 4.356046e-02 out 56fd39b2; N=4 J1 350 L 6.510848e-02 c2 6.534069e-02 out 23a361e3
  (.hor 0 0, .hor 1 0),
  (.hor 0 3, .hor 1 3),
  (.hor 1 0, .hor 2 0),
  (.hor 1 3, .hor 2 3),
  -- n5_G03 (4 members): N=3 J1 300 L 1.794533e-03 c2 1.897227e-03 out e1784d38; N=4 J1 350 L 2.625935e-03 c2 2.845840e-03 out 9ca97e16
  (.hor 0 0, .hor 1 1),
  (.hor 0 3, .hor 1 2),
  (.hor 1 1, .hor 2 0),
  (.hor 1 2, .hor 2 3),
  -- n5_G06 (4 members): N=3 J1 300 L 2.474672e-03 c2 2.595769e-03 out 8d17c86e; N=4 J1 350 L 3.635425e-03 c2 3.893653e-03 out bf072a5e
  (.hor 0 0, .hor 2 1),
  (.hor 0 1, .hor 2 0),
  (.hor 0 2, .hor 2 3),
  (.hor 0 3, .hor 2 2),
  -- n5_G07 (4 members): N=3 J1 300 L 3.960645e-04 c2 5.169040e-04 out bbcba437; N=4 J1 350 L 5.175540e-04 c2 7.753560e-04 out bb967e61
  (.hor 0 0, .hor 2 2),
  (.hor 0 1, .hor 2 3),
  (.hor 0 2, .hor 2 0),
  (.hor 0 3, .hor 2 1),
  -- n5_G09 (4 members): N=3 J1 300 L 3.834466e-03 c2 3.930779e-03 out 4b7ead69; N=4 J1 350 L 5.689678e-03 c2 5.896168e-03 out fed0c5d1
  (.hor 0 0, .ver 0 2),
  (.hor 0 3, .ver 0 2),
  (.hor 2 0, .ver 1 2),
  (.hor 2 3, .ver 1 2),
  -- n5_G10 (4 members): N=3 J1 300 L 3.762492e-04 c2 4.757451e-04 out 877042bd; N=4 J1 350 L 5.002345e-04 c2 7.136177e-04 out 092b3976
  (.hor 0 0, .ver 0 3),
  (.hor 0 3, .ver 0 1),
  (.hor 2 0, .ver 1 3),
  (.hor 2 3, .ver 1 1),
  -- n5_G12 (4 members): N=3 J1 300 L 7.361430e-03 c2 7.491487e-03 out 7a00b77f; N=4 J1 350 L 1.095971e-02 c2 1.123723e-02 out e2d9ea61
  (.hor 0 0, .ver 1 0),
  (.hor 0 3, .ver 1 4),
  (.hor 2 0, .ver 0 0),
  (.hor 2 3, .ver 0 4),
  -- n5_G13 (4 members): N=3 J1 300 L 1.168191e-03 c2 1.267694e-03 out 9bd41151; N=4 J1 350 L 1.688173e-03 c2 1.901540e-03 out 904da0ad
  (.hor 0 0, .ver 1 1),
  (.hor 0 3, .ver 1 3),
  (.hor 2 0, .ver 0 1),
  (.hor 2 3, .ver 0 3),
  -- n5_G14 (4 members): N=3 J1 300 L 6.997010e-04 c2 7.959827e-04 out 576ac62e; N=4 J1 350 L 9.875235e-04 c2 1.193974e-03 out 52793847
  (.hor 0 0, .ver 1 2),
  (.hor 0 3, .ver 1 2),
  (.hor 2 0, .ver 0 2),
  (.hor 2 3, .ver 0 2),
  -- n5_G15 (4 members): N=3 J1 300 L 1.122832e-04 c2 2.117623e-04 out 4991a995; N=4 J1 350 L 1.042919e-04 c2 3.176434e-04 out db40aa25
  (.hor 0 0, .ver 1 3),
  (.hor 0 3, .ver 1 1),
  (.hor 2 0, .ver 0 3),
  (.hor 2 3, .ver 0 1),
  -- n5_G17 (4 members): N=3 J1 300 L 1.798724e-03 c2 1.897227e-03 out 2e7c44db; N=4 J1 350 L 2.635227e-03 c2 2.845840e-03 out 10ca897a
  (.hor 0 1, .hor 1 0),
  (.hor 0 2, .hor 1 3),
  (.hor 1 0, .hor 2 1),
  (.hor 1 3, .hor 2 2),
  -- n5_G18 (4 members): N=3 J1 300 L 4.733526e-02 c2 4.743067e-02 out 18cf5f95; N=4 J1 350 L 7.094274e-02 c2 7.114601e-02 out 0c96976a
  (.hor 0 1, .hor 1 1),
  (.hor 0 2, .hor 1 2),
  (.hor 1 1, .hor 2 1),
  (.hor 1 2, .hor 2 2),
  -- n5_G19 (4 members): N=3 J1 300 L 1.964341e-03 c2 2.058623e-03 out 98cca3c6; N=4 J1 350 L 2.886582e-03 c2 3.087934e-03 out 69b9670c
  (.hor 0 1, .hor 1 2),
  (.hor 0 2, .hor 1 1),
  (.hor 1 1, .hor 2 2),
  (.hor 1 2, .hor 2 1),
  -- n5_G21 (2 members): N=3 J1 300 L 3.384966e-03 c2 3.496612e-03 out 98c93d0a; N=4 J1 350 L 5.007833e-03 c2 5.244918e-03 out 70841f60
  (.hor 0 1, .hor 2 2),
  (.hor 0 2, .hor 2 1),
  -- n5_G22 (4 members): N=3 J1 300 L 8.810074e-03 c2 8.931357e-03 out fbeee0c3; N=4 J1 350 L 1.313992e-02 c2 1.339704e-02 out 9b543d1a
  (.hor 0 1, .ver 0 0),
  (.hor 0 2, .ver 0 4),
  (.hor 2 1, .ver 1 0),
  (.hor 2 2, .ver 1 4),
  -- n5_G23 (4 members): N=3 J1 300 L 5.192318e-03 c2 5.284458e-03 out 6c84bf3a; N=4 J1 350 L 7.730061e-03 c2 7.926686e-03 out 886c618e
  (.hor 0 1, .ver 0 3),
  (.hor 0 2, .ver 0 1),
  (.hor 2 1, .ver 1 3),
  (.hor 2 2, .ver 1 1),
  -- n5_G24 (4 members): N=3 J1 300 L 8.920391e-04 c2 1.011872e-03 out f1542821; N=4 J1 350 L 1.263051e-03 c2 1.517808e-03 out 61dce499
  (.hor 0 1, .ver 0 4),
  (.hor 0 2, .ver 0 0),
  (.hor 2 1, .ver 1 4),
  (.hor 2 2, .ver 1 0),
  -- n5_G25 (4 members): N=3 J1 300 L 2.476063e-03 c2 2.595769e-03 out f7de626c; N=4 J1 350 L 3.639142e-03 c2 3.893653e-03 out 7034ad2d
  (.hor 0 1, .ver 1 0),
  (.hor 0 2, .ver 1 4),
  (.hor 2 1, .ver 0 0),
  (.hor 2 2, .ver 0 4),
  -- n5_G26 (4 members): N=3 J1 300 L 3.311583e-03 c2 3.403580e-03 out 8190a414; N=4 J1 350 L 4.909004e-03 c2 5.105370e-03 out f98330c9
  (.hor 0 1, .ver 1 1),
  (.hor 0 2, .ver 1 3),
  (.hor 2 1, .ver 0 1),
  (.hor 2 2, .ver 0 3),
  -- n5_G27 (4 members): N=3 J1 300 L 2.426746e-03 c2 2.515699e-03 out 815f6a81; N=4 J1 350 L 3.583683e-03 c2 3.773548e-03 out 63f1c615
  (.hor 0 1, .ver 1 2),
  (.hor 0 2, .ver 1 2),
  (.hor 2 1, .ver 0 2),
  (.hor 2 2, .ver 0 2),
  -- n5_G28 (4 members): N=3 J1 300 L 1.232784e-03 c2 1.324715e-03 out d9a37304; N=4 J1 350 L 1.790808e-03 c2 1.987072e-03 out c36f751a
  (.hor 0 1, .ver 1 3),
  (.hor 0 2, .ver 1 1),
  (.hor 2 1, .ver 0 3),
  (.hor 2 2, .ver 0 1),
  -- n5_G29 (4 members): N=3 J1 300 L 3.974315e-04 c2 5.169040e-04 out f014c835; N=4 J1 350 L 5.211888e-04 c2 7.753560e-04 out 00ad7f87
  (.hor 0 1, .ver 1 4),
  (.hor 0 2, .ver 1 0),
  (.hor 2 1, .ver 0 4),
  (.hor 2 2, .ver 0 0),
  -- n5_G30 (2 members): N=3 J1 300 L 2.466533e-04 c2 3.293797e-04 out d64b1847; N=4 J1 350 L 3.159551e-04 c2 4.940695e-04 out c9bd588c
  (.hor 1 0, .hor 1 2),
  (.hor 1 1, .hor 1 3),
  -- n5_G31 (4 members): N=3 J1 300 L 1.110808e-03 c2 1.189061e-03 out b988786a; N=4 J1 350 L 1.615210e-03 c2 1.783591e-03 out dacb2c14
  (.hor 1 0, .ver 0 2),
  (.hor 1 0, .ver 1 2),
  (.hor 1 3, .ver 0 2),
  (.hor 1 3, .ver 1 2),
  -- n5_G34 (4 members): N=3 J1 300 L 1.795858e-03 c2 1.897227e-03 out 3caeb7b1; N=4 J1 350 L 2.629326e-03 c2 2.845840e-03 out 769b7834
  (.hor 1 1, .ver 0 0),
  (.hor 1 1, .ver 1 0),
  (.hor 1 2, .ver 0 4),
  (.hor 1 2, .ver 1 4),
  -- n5_G35 (4 members): N=3 J1 300 L 1.239922e-03 c2 1.317519e-03 out 8680938a; N=4 J1 350 L 1.809608e-03 c2 1.976278e-03 out 19273f41
  (.hor 1 1, .ver 0 3),
  (.hor 1 1, .ver 1 3),
  (.hor 1 2, .ver 0 1),
  (.hor 1 2, .ver 1 1)
-- total 104 pairs

]

/-- the records' list against the class: within it; not yet covering it (the last 9 orbits follow in StripIII.Small5Kit7 and StripIII.Small5Final) -/
theorem box5AllList_inClass : box5AllInClass box5AllList = true := by decide +kernel
theorem box5AllList_open_until_kit7 : box5AllCheck box5AllList = false := by decide +kernel

/-- COUNTS (INFO, each unordered pair in both orders where marked): 22 edges at n = 5, 231 unordered pairs; the class g5 holds 138; the
list holds 104 (27 orbits) -/
theorem count_allPairsAll5 : (allPairsAll 5).length = 2 * 231 := by decide +kernel
theorem count_g5 : ((allPairsAll 5).filter fun p => g5 p.1 p.2).length = 2 * 138 := by decide +kernel
theorem count_box5AllList : box5AllList.length = 104 := by decide +kernel

/-- CANDIDATE (INFO, not certified data): the members of all 36 orbits as the n = 5 probe output enumerates them
(code/pk23/out/o5_probe_n5.out, by the converter orbits2lean_v1.py); its checks show that the class g5 is exactly the union of the 36
orbits, so the 9 orbits added later complete the list. -/
def cand5All : List (ECode × ECode) := [
-- source code/pk23/out/o5_probe_n5.out sha256 06e3266f33623533fc2a472a661e27aa67923efccce59da01cb7d6f3bca1f9cf; orbits G01,G02,G03,G04,G05,G06,G07,G08,G09,G10,G11,G12,G13,G14,G15,G16,G17,G18,G19,G20,G21,G22,G23,G24,G25,G26,G27,G28,G29,G30,G31,G32,G33,G34,G35,G36; members 4,4,4,4,4,4,4,2,4,4,4,4,4,4,4,4,4,4,4,4,2,4,4,4,4,4,4,4,4,2,4,4,4,4,4,4; total 138
  (.hor 0 0, .hor 0 2),
  (.hor 0 1, .hor 0 3),
  (.hor 2 0, .hor 2 2),
  (.hor 2 1, .hor 2 3),
  (.hor 0 0, .hor 1 0),
  (.hor 0 3, .hor 1 3),
  (.hor 1 0, .hor 2 0),
  (.hor 1 3, .hor 2 3),
  (.hor 0 0, .hor 1 1),
  (.hor 0 3, .hor 1 2),
  (.hor 1 1, .hor 2 0),
  (.hor 1 2, .hor 2 3),
  (.hor 0 0, .hor 1 2),
  (.hor 0 3, .hor 1 1),
  (.hor 1 1, .hor 2 3),
  (.hor 1 2, .hor 2 0),
  (.hor 0 0, .hor 1 3),
  (.hor 0 3, .hor 1 0),
  (.hor 1 0, .hor 2 3),
  (.hor 1 3, .hor 2 0),
  (.hor 0 0, .hor 2 1),
  (.hor 0 1, .hor 2 0),
  (.hor 0 2, .hor 2 3),
  (.hor 0 3, .hor 2 2),
  (.hor 0 0, .hor 2 2),
  (.hor 0 1, .hor 2 3),
  (.hor 0 2, .hor 2 0),
  (.hor 0 3, .hor 2 1),
  (.hor 0 0, .hor 2 3),
  (.hor 0 3, .hor 2 0),
  (.hor 0 0, .ver 0 2),
  (.hor 0 3, .ver 0 2),
  (.hor 2 0, .ver 1 2),
  (.hor 2 3, .ver 1 2),
  (.hor 0 0, .ver 0 3),
  (.hor 0 3, .ver 0 1),
  (.hor 2 0, .ver 1 3),
  (.hor 2 3, .ver 1 1),
  (.hor 0 0, .ver 0 4),
  (.hor 0 3, .ver 0 0),
  (.hor 2 0, .ver 1 4),
  (.hor 2 3, .ver 1 0),
  (.hor 0 0, .ver 1 0),
  (.hor 0 3, .ver 1 4),
  (.hor 2 0, .ver 0 0),
  (.hor 2 3, .ver 0 4),
  (.hor 0 0, .ver 1 1),
  (.hor 0 3, .ver 1 3),
  (.hor 2 0, .ver 0 1),
  (.hor 2 3, .ver 0 3),
  (.hor 0 0, .ver 1 2),
  (.hor 0 3, .ver 1 2),
  (.hor 2 0, .ver 0 2),
  (.hor 2 3, .ver 0 2),
  (.hor 0 0, .ver 1 3),
  (.hor 0 3, .ver 1 1),
  (.hor 2 0, .ver 0 3),
  (.hor 2 3, .ver 0 1),
  (.hor 0 0, .ver 1 4),
  (.hor 0 3, .ver 1 0),
  (.hor 2 0, .ver 0 4),
  (.hor 2 3, .ver 0 0),
  (.hor 0 1, .hor 1 0),
  (.hor 0 2, .hor 1 3),
  (.hor 1 0, .hor 2 1),
  (.hor 1 3, .hor 2 2),
  (.hor 0 1, .hor 1 1),
  (.hor 0 2, .hor 1 2),
  (.hor 1 1, .hor 2 1),
  (.hor 1 2, .hor 2 2),
  (.hor 0 1, .hor 1 2),
  (.hor 0 2, .hor 1 1),
  (.hor 1 1, .hor 2 2),
  (.hor 1 2, .hor 2 1),
  (.hor 0 1, .hor 1 3),
  (.hor 0 2, .hor 1 0),
  (.hor 1 0, .hor 2 2),
  (.hor 1 3, .hor 2 1),
  (.hor 0 1, .hor 2 2),
  (.hor 0 2, .hor 2 1),
  (.hor 0 1, .ver 0 0),
  (.hor 0 2, .ver 0 4),
  (.hor 2 1, .ver 1 0),
  (.hor 2 2, .ver 1 4),
  (.hor 0 1, .ver 0 3),
  (.hor 0 2, .ver 0 1),
  (.hor 2 1, .ver 1 3),
  (.hor 2 2, .ver 1 1),
  (.hor 0 1, .ver 0 4),
  (.hor 0 2, .ver 0 0),
  (.hor 2 1, .ver 1 4),
  (.hor 2 2, .ver 1 0),
  (.hor 0 1, .ver 1 0),
  (.hor 0 2, .ver 1 4),
  (.hor 2 1, .ver 0 0),
  (.hor 2 2, .ver 0 4),
  (.hor 0 1, .ver 1 1),
  (.hor 0 2, .ver 1 3),
  (.hor 2 1, .ver 0 1),
  (.hor 2 2, .ver 0 3),
  (.hor 0 1, .ver 1 2),
  (.hor 0 2, .ver 1 2),
  (.hor 2 1, .ver 0 2),
  (.hor 2 2, .ver 0 2),
  (.hor 0 1, .ver 1 3),
  (.hor 0 2, .ver 1 1),
  (.hor 2 1, .ver 0 3),
  (.hor 2 2, .ver 0 1),
  (.hor 0 1, .ver 1 4),
  (.hor 0 2, .ver 1 0),
  (.hor 2 1, .ver 0 4),
  (.hor 2 2, .ver 0 0),
  (.hor 1 0, .hor 1 2),
  (.hor 1 1, .hor 1 3),
  (.hor 1 0, .ver 0 2),
  (.hor 1 0, .ver 1 2),
  (.hor 1 3, .ver 0 2),
  (.hor 1 3, .ver 1 2),
  (.hor 1 0, .ver 0 3),
  (.hor 1 0, .ver 1 3),
  (.hor 1 3, .ver 0 1),
  (.hor 1 3, .ver 1 1),
  (.hor 1 0, .ver 0 4),
  (.hor 1 0, .ver 1 4),
  (.hor 1 3, .ver 0 0),
  (.hor 1 3, .ver 1 0),
  (.hor 1 1, .ver 0 0),
  (.hor 1 1, .ver 1 0),
  (.hor 1 2, .ver 0 4),
  (.hor 1 2, .ver 1 4),
  (.hor 1 1, .ver 0 3),
  (.hor 1 1, .ver 1 3),
  (.hor 1 2, .ver 0 1),
  (.hor 1 2, .ver 1 1),
  (.hor 1 1, .ver 0 4),
  (.hor 1 1, .ver 1 4),
  (.hor 1 2, .ver 0 0),
  (.hor 1 2, .ver 1 0)

]

theorem cand5All_check : box5AllCheck cand5All = true := by decide +kernel
theorem cand5All_inClass : box5AllInClass cand5All = true := by decide +kernel
theorem cand5All_len : cand5All.length = 138 := by decide +kernel

end G2Kernel.StripIII
