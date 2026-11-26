import StripIII.Core

/-! CANDIDATE list check (INFO, not certified data): the box-orbit member lists that the probe outputs enumerate
(code/pk23/out/o5_probe_n5.out, o5_probe_n6.out, o5_probe_n7.out, turned into edge codes by the converter orbits2lean_v1.py), checked against the
classes of StripIII.Core; the certified lists of the records stand in StripIII.Core, StripIII.FinalIIIG55 and StripIII.Small5Final. -/

namespace G2Kernel.StripIII

def candBox5 : List (ECode × ECode) := [
-- source code/pk23/out/o5_probe_n5.out sha256 06e3266f33623533fc2a472a661e27aa67923efccce59da01cb7d6f3bca1f9cf; orbits G12,G13,G26,G27,G06,G21; members 4,4,4,4,4,2; total 22
  (.hor 0 0, .ver 1 0),
  (.hor 0 3, .ver 1 4),
  (.hor 2 0, .ver 0 0),
  (.hor 2 3, .ver 0 4),
  (.hor 0 0, .ver 1 1),
  (.hor 0 3, .ver 1 3),
  (.hor 2 0, .ver 0 1),
  (.hor 2 3, .ver 0 3),
  (.hor 0 1, .ver 1 1),
  (.hor 0 2, .ver 1 3),
  (.hor 2 1, .ver 0 1),
  (.hor 2 2, .ver 0 3),
  (.hor 0 1, .ver 1 2),
  (.hor 0 2, .ver 1 2),
  (.hor 2 1, .ver 0 2),
  (.hor 2 2, .ver 0 2),
  (.hor 0 0, .hor 2 1),
  (.hor 0 1, .hor 2 0),
  (.hor 0 2, .hor 2 3),
  (.hor 0 3, .hor 2 2),
  (.hor 0 1, .hor 2 2),
  (.hor 0 2, .hor 2 1)

]

def candO5 : List (Nat × ECode × ECode) := [
-- source code/pk23/out/o5_probe_n6.out sha256 1c8eaa58cf4edae10ed3da2bab9123731bb89247150d165a10d67ef76df3c912; orbits G27,G46; members 4,4; total 8
  (6, .hor 0 1, .hor 2 2),
  (6, .hor 0 2, .hor 2 1),
  (6, .hor 0 2, .hor 2 3),
  (6, .hor 0 3, .hor 2 2),
  (6, .hor 0 2, .ver 1 2),
  (6, .hor 0 2, .ver 1 3),
  (6, .hor 2 2, .ver 0 2),
  (6, .hor 2 2, .ver 0 3)
,
-- source code/pk23/out/o5_probe_n7.out sha256 98e2acf7b50a0285683c19c06b71cb153873cc7ea6e10dc09114c0a8863c8057; orbits G55; members 2; total 2
  (7, .hor 0 2, .hor 2 3),
  (7, .hor 0 3, .hor 2 2)

]

theorem cand_box5_check : box5Check candBox5 = true := by decide +kernel
theorem cand_box5_in_class : candBox5.all (fun p => cBox5 5 p.1 p.2) = true := by decide +kernel
theorem cand_box5_len : candBox5.length = 22 := by decide
theorem cand_o5_check : o5Check candO5 = true := by decide +kernel
theorem cand_o5_in_class : candO5.all (fun q => cO5 4 q.1 q.2.1 q.2.2) = true := by decide +kernel
theorem cand_o5_len : candO5.length = 10 := by decide

end G2Kernel.StripIII
