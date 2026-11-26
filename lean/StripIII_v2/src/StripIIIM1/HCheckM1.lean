/-
StripIIIM1.HCheckM1: the checks of M1's list by
decide, one theorem per n (one kernel run each), n = 6..11: `m1Check m1List n` (every ordered to-do pair of P_3 x P_n outside the end
orbit has its key among the keys of the list at n), `m1InClass m1List n` (every entry at n is a to-do pair outside the end orbit) and
`m1Orbit m1List n` (every ordered pair of distinct valid codes with the key of an entry at n is one of the entry's images).
`m1Check_n11` holds trivially when NMAX_M1 = 10 (its left disjunct), so the module serves NMAX_M1 = 10 and 11 alike.
`m1List_bij`: at every n <= NMAX_M1 the list has one entry fewer than there are to-do orbits, so with the two checks it holds exactly one
entry per to-do orbit outside the end orbit; `m1Check_plant`: without its first entry the list fails the check. Controls: the
counts of ordered to-do pairs, to-do orbits and end-orbit pairs per n against an independent enumeration of the to-do pairs, whose
counts at n = 6..11 are the numbers below.
No Mathlib.
-/
import StripIIIM1.M1List

namespace G2Kernel.StripIII

theorem NMAX_M1_range : 10 ≤ NMAX_M1 ∧ NMAX_M1 ≤ 11 := by decide

/-- every entry of the list has 6 <= n <= NMAX_M1, and some entry has n = NMAX_M1 -/
theorem m1List_nmax : m1List.all (fun q => decide (6 ≤ q.1) && decide (q.1 ≤ NMAX_M1)) = true ∧
    m1List.any (fun q => q.1 == NMAX_M1) = true := by
  decide +kernel

theorem m1Check_n6 : m1Check m1List 6 = true := by decide +kernel
theorem m1Check_n7 : m1Check m1List 7 = true := by decide +kernel
theorem m1Check_n8 : m1Check m1List 8 = true := by decide +kernel
theorem m1Check_n9 : m1Check m1List 9 = true := by decide +kernel
theorem m1Check_n10 : m1Check m1List 10 = true := by decide +kernel
theorem m1Check_n11 : NMAX_M1 < 11 ∨ m1Check m1List 11 = true := by decide +kernel

theorem m1InClass_n6 : m1InClass m1List 6 = true := by decide +kernel
theorem m1InClass_n7 : m1InClass m1List 7 = true := by decide +kernel
theorem m1InClass_n8 : m1InClass m1List 8 = true := by decide +kernel
theorem m1InClass_n9 : m1InClass m1List 9 = true := by decide +kernel
theorem m1InClass_n10 : m1InClass m1List 10 = true := by decide +kernel
theorem m1InClass_n11 : m1InClass m1List 11 = true := by decide +kernel

theorem m1Orbit_n6 : m1Orbit m1List 6 = true := by decide +kernel
theorem m1Orbit_n7 : m1Orbit m1List 7 = true := by decide +kernel
theorem m1Orbit_n8 : m1Orbit m1List 8 = true := by decide +kernel
theorem m1Orbit_n9 : m1Orbit m1List 9 = true := by decide +kernel
theorem m1Orbit_n10 : m1Orbit m1List 10 = true := by decide +kernel
theorem m1Orbit_n11 : m1Orbit m1List 11 = true := by decide +kernel

/-- one entry per to-do orbit outside the end orbit, at every n <= NMAX_M1 -/
theorem m1List_bij : [6, 7, 8, 9, 10, 11].all (fun n =>
    decide (NMAX_M1 < n) || (m1List.filter fun q => q.1 == n).length + 1 == orbitCount n) = true := by
  decide +kernel

/-- plant: without its first entry the list fails the check at that entry's n (every entry is needed) -/
theorem m1Check_plant : (m1List.head?.map fun q => m1Check m1List.tail q.1) = some false := by decide +kernel

/-- the check for every n with 6 <= n <= NMAX_M1 -/
theorem m1Check_all : ∀ n, 6 ≤ n → n ≤ NMAX_M1 → m1Check m1List n = true := by
  intro n h6 hn
  have h11 : n ≤ 11 := Nat.le_trans hn NMAX_M1_range.2
  rcases (by omega : n = 6 ∨ n = 7 ∨ n = 8 ∨ n = 9 ∨ n = 10 ∨ n = 11) with rfl | rfl | rfl | rfl | rfl | rfl
  · exact m1Check_n6
  · exact m1Check_n7
  · exact m1Check_n8
  · exact m1Check_n9
  · exact m1Check_n10
  · exact m1Check_n11.resolve_left (Nat.not_lt.mpr hn)

/-- control: the ordered to-do pairs per n = 6..11 (the independent enumeration) -/
theorem count_todo : [6, 7, 8, 9, 10, 11].map (fun n => ((allPairsAll n).filter fun p => todoH n p.1 p.2).length) =
    [188, 280, 388, 516, 660, 824] := by
  decide +kernel

/-- control: the to-do orbits per n = 6..11 (the independent enumeration) -/
theorem count_orbits : [6, 7, 8, 9, 10, 11].map orbitCount = [25, 37, 52, 69, 89, 111] := by decide +kernel

/-- control: the ordered pairs of the end orbit per n = 6..11 (the independent enumeration), all of them to-do pairs -/
theorem count_end : [6, 7, 8, 9, 10, 11].map (fun n => ((allPairsAll n).filter fun p => sameBondEnd n p.1 p.2).length) =
    [8, 8, 8, 8, 8, 8] ∧
    [6, 7, 8, 9, 10, 11].all (fun n => (allPairsAll n).all fun p => !sameBondEnd n p.1 p.2 || todoH n p.1 p.2) = true := by
  decide +kernel

end G2Kernel.StripIII
