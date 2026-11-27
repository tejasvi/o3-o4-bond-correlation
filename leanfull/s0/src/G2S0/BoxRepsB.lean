/-
G2S0.BoxRepsB (S0 follow-up, data): the representative pairs of the orbits behind the package's lists of H22 `hBox5`
(`StripIII.box5List`, the n = 5 orbits G12, G13, G26, G27, G06, G21) and of H25 `hO5` (`StripIII.o5List ++ L55`, the orbits
n6 G27, n6 G46 and n7 G55), one per orbit, as code pairs: the "orbit" column of the record tables named in the docstrings of
`hBox5` and `hO5` (StripIII.Statement) and in StripIII.FinalIIIG55. Each record certifies J^2 Cov >= L > 0 at its representative
pair for every J >= J1 (J1 = 300 at N = 3, 350 at N = 4; the hO5 orbits at N = 4 only). Made by
s0/scripts/gen_boxrepsB_v1.py; tables (release_N/code/pk23/o5/records/), sha256:
- O5_RECORD_TABLE_box_run_20261118T013023Z_v1.tsv 19945efdec713105192a164fff21914a1da8341c1e8a2513178ea784fccf1b21
- O5_RECORD_TABLE_box_run_20261118T045359Z_v1.tsv a1233479612e660f697e3d0e88be0a0bb878a7421ac71a4190db1e8df5b0472b
No Mathlib.
-/
import StripIII.Core

namespace G2Kernel.StripIII

/-- the representative pair of each of the 6 orbits of `box5List` (H22), in the docstring order G12, G13, G26, G27, G06, G21 -/
def box5RepsH22 : List (ECode × ECode) := [
  -- n5_G12 (run 013023Z, 4 members: (h00, v10) (h03, v14) (h20, v00) (h23, v04)): L N3 7.361430e-03, L N4 1.095971e-02
  (.hor 0 0, .ver 1 0),
  -- n5_G13 (run 013023Z, 4 members: (h00, v11) (h03, v13) (h20, v01) (h23, v03)): L N3 1.168191e-03, L N4 1.688173e-03
  (.hor 0 0, .ver 1 1),
  -- n5_G26 (run 013023Z, 4 members: (h01, v11) (h02, v13) (h21, v01) (h22, v03)): L N3 3.311583e-03, L N4 4.909004e-03
  (.hor 0 1, .ver 1 1),
  -- n5_G27 (run 013023Z, 4 members: (h01, v12) (h02, v12) (h21, v02) (h22, v02)): L N3 2.426746e-03, L N4 3.583683e-03
  (.hor 0 1, .ver 1 2),
  -- n5_G06 (run 013023Z, 4 members: (h00, h21) (h01, h20) (h02, h23) (h03, h22)): L N3 2.474672e-03, L N4 3.635425e-03
  (.hor 0 0, .hor 2 1),
  -- n5_G21 (run 013023Z, 2 members: (h01, h22) (h02, h21)): L N3 3.384966e-03, L N4 5.007833e-03
  (.hor 0 1, .hor 2 2)
]

/-- the representative of each of the 3 orbits of `o5List ++ L55` (H25), as (n, code pair): n6 G27, n6 G46, n7 G55 -/
def o5Reps : List (Nat × ECode × ECode) := [
  -- n6_G27 (run 013023Z, 4 members: (h01, h22) (h02, h21) (h02, h23) (h03, h22)): L N4 5.005397e-03
  (6, .hor 0 1, .hor 2 2),
  -- n6_G46 (run 013023Z, 4 members: (h02, v12) (h02, v13) (h22, v02) (h22, v03)): L N4 3.749486e-03
  (6, .hor 0 2, .ver 1 2),
  -- n7_G55 (run 045359Z, 2 members: (h02, h23) (h03, h22)): L N4 4.643864e-03
  (7, .hor 0 2, .hor 2 3)
]

theorem boxRepsB_len : box5RepsH22.length = 6 ∧ o5Reps.length = 3 := by decide

end G2Kernel.StripIII
