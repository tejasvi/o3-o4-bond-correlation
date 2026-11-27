/-
G2S0.Box5Reps (stage S0 (c), data): the representative pairs of the 36 orbits of P_3 x P_5 that the n = 5 box records
certify (Proposition B.14), one per orbit, as code pairs: the "orbit" column of the record tables (each record certifies
J^2 Cov >= L > 0 at its representative pair for every J >= J1, J1 = 300 at N = 3 and J1 = 350 at N = 4). Made by
s0/scripts/gen_box5reps_v1.py from the tables named in StripIII.Small5Statement (hBoxAll5): the 27 orbits of run
013023Z certified at both N, the 7 orbits G04, G08, G11, G16, G20, G32, G36 of run 114847Z, G05 of run 154150Z and
G33 of run 041647Z. Tables (release_N/code/pk23/o5/records/), sha256:
- O5_RECORD_TABLE_box_run_20261118T013023Z_v1.tsv 19945efdec713105192a164fff21914a1da8341c1e8a2513178ea784fccf1b21
- O5_RECORD_TABLE_box_run_20261118T114847Z_v1.tsv c317dac0cc1f3681f91e689e13119a608e0ff04fa03aaf99711f6c1e972d05c2
- O5_RECORD_TABLE_box_run_20261118T154150Z_v1.tsv 94284d6e2c75a8a1c8a47c4a22073184b284107f24eac6956fbe4fbee4b887c6
- O5_RECORD_TABLE_box_run_20261119T041647Z_v1.tsv d068beacbaf923c45f338718a9f2ca001bf2b63bc5fac302aef94b50c5e41d7c
No Mathlib.
-/
import StripIII.Core

namespace G2Kernel.StripIII

/-- the representative pair of each of the 36 orbits of the n = 5 box records, in orbit order G01..G36 -/
def box5Reps : List (ECode × ECode) := [
  -- n5_G01 (run 013023Z, 4 members): L N3 8.908049e-04, L N4 1.259698e-03
  (.hor 0 0, .hor 0 2),
  -- n5_G02 (run 013023Z, 4 members): L N3 4.345187e-02, L N4 6.510848e-02
  (.hor 0 0, .hor 1 0),
  -- n5_G03 (run 013023Z, 4 members): L N3 1.794533e-03, L N4 2.625935e-03
  (.hor 0 0, .hor 1 1),
  -- n5_G04 (run 114847Z, 4 members): L N3 4.951049e-05, L N4 1.140998e-04
  (.hor 0 0, .hor 1 2),
  -- n5_G05 (run 154150Z, 4 members): L N3 2.560374e-06, L N4 3.775544e-06
  (.hor 0 0, .hor 1 3),
  -- n5_G06 (run 013023Z, 4 members): L N3 2.474672e-03, L N4 3.635425e-03
  (.hor 0 0, .hor 2 1),
  -- n5_G07 (run 013023Z, 4 members): L N3 3.960645e-04, L N4 5.175540e-04
  (.hor 0 0, .hor 2 2),
  -- n5_G08 (run 114847Z, 2 members): L N3 6.179895e-05, L N4 8.720119e-05
  (.hor 0 0, .hor 2 3),
  -- n5_G09 (run 013023Z, 4 members): L N3 3.834466e-03, L N4 5.689678e-03
  (.hor 0 0, .ver 0 2),
  -- n5_G10 (run 013023Z, 4 members): L N3 3.762492e-04, L N4 5.002345e-04
  (.hor 0 0, .ver 0 3),
  -- n5_G11 (run 114847Z, 4 members): L N3 5.582061e-05, L N4 1.371444e-04
  (.hor 0 0, .ver 0 4),
  -- n5_G12 (run 013023Z, 4 members): L N3 7.361430e-03, L N4 1.095971e-02
  (.hor 0 0, .ver 1 0),
  -- n5_G13 (run 013023Z, 4 members): L N3 1.168191e-03, L N4 1.688173e-03
  (.hor 0 0, .ver 1 1),
  -- n5_G14 (run 013023Z, 4 members): L N3 6.997010e-04, L N4 9.875235e-04
  (.hor 0 0, .ver 1 2),
  -- n5_G15 (run 013023Z, 4 members): L N3 1.122832e-04, L N4 1.042919e-04
  (.hor 0 0, .ver 1 3),
  -- n5_G16 (run 114847Z, 4 members): L N3 6.198819e-05, L N4 8.765588e-05
  (.hor 0 0, .ver 1 4),
  -- n5_G17 (run 013023Z, 4 members): L N3 1.798724e-03, L N4 2.635227e-03
  (.hor 0 1, .hor 1 0),
  -- n5_G18 (run 013023Z, 4 members): L N3 4.733526e-02, L N4 7.094274e-02
  (.hor 0 1, .hor 1 1),
  -- n5_G19 (run 013023Z, 4 members): L N3 1.964341e-03, L N4 2.886582e-03
  (.hor 0 1, .hor 1 2),
  -- n5_G20 (run 114847Z, 4 members): L N3 5.288388e-05, L N4 1.151697e-04
  (.hor 0 1, .hor 1 3),
  -- n5_G21 (run 013023Z, 2 members): L N3 3.384966e-03, L N4 5.007833e-03
  (.hor 0 1, .hor 2 2),
  -- n5_G22 (run 013023Z, 4 members): L N3 8.810074e-03, L N4 1.313992e-02
  (.hor 0 1, .ver 0 0),
  -- n5_G23 (run 013023Z, 4 members): L N3 5.192318e-03, L N4 7.730061e-03
  (.hor 0 1, .ver 0 3),
  -- n5_G24 (run 013023Z, 4 members): L N3 8.920391e-04, L N4 1.263051e-03
  (.hor 0 1, .ver 0 4),
  -- n5_G25 (run 013023Z, 4 members): L N3 2.476063e-03, L N4 3.639142e-03
  (.hor 0 1, .ver 1 0),
  -- n5_G26 (run 013023Z, 4 members): L N3 3.311583e-03, L N4 4.909004e-03
  (.hor 0 1, .ver 1 1),
  -- n5_G27 (run 013023Z, 4 members): L N3 2.426746e-03, L N4 3.583683e-03
  (.hor 0 1, .ver 1 2),
  -- n5_G28 (run 013023Z, 4 members): L N3 1.232784e-03, L N4 1.790808e-03
  (.hor 0 1, .ver 1 3),
  -- n5_G29 (run 013023Z, 4 members): L N3 3.974315e-04, L N4 5.211888e-04
  (.hor 0 1, .ver 1 4),
  -- n5_G30 (run 013023Z, 2 members): L N3 2.466533e-04, L N4 3.159551e-04
  (.hor 1 0, .hor 1 2),
  -- n5_G31 (run 013023Z, 4 members): L N3 1.110808e-03, L N4 1.615210e-03
  (.hor 1 0, .ver 0 2),
  -- n5_G32 (run 114847Z, 4 members): L N3 3.072130e-05, L N4 7.272306e-05
  (.hor 1 0, .ver 0 3),
  -- n5_G33 (run 041647Z, 4 members): L N3 2.598678e-06, L N4 3.820294e-06
  (.hor 1 0, .ver 0 4),
  -- n5_G34 (run 013023Z, 4 members): L N3 1.795858e-03, L N4 2.629326e-03
  (.hor 1 1, .ver 0 0),
  -- n5_G35 (run 013023Z, 4 members): L N3 1.239922e-03, L N4 1.809608e-03
  (.hor 1 1, .ver 0 3),
  -- n5_G36 (run 114847Z, 4 members): L N3 5.066329e-05, L N4 1.144505e-04
  (.hor 1 1, .ver 0 4)
]

theorem box5Reps_len : box5Reps.length = 36 := by decide

end G2Kernel.StripIII
