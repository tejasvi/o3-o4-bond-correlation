/-
G2S0.Orbit (stage S0 (c), part 1): the orbit step for the strips P_3 x P_n.
- A graph automorphism preserves the Gibbs law at uniform coupling, for every N (`gibbsExp_auto_invariant`, from the package's
  `gibbsExp_comp_bij`, G2Kernel.Proofs.AssemblyProof, which uses `measurePreserving_arrowCongr'`), so bond-energy covariances and the
  predicate `G2pair` are invariant (`G2pair_auto_iff`).
- The reflections of P_3 x P_n in the middle row (`rowFlip`, new) and in the vertical midline (`stripReflV`, StripIII.Statement) are
  graph automorphisms; on edge codes they act as `ECode.flip` and `ECode.lr n` (`edgeCode_rowFlip`; `edgeCode_stripReflV` is
  StripIII.Proof's).
- `G2pair_of_orbitForms`: a bound at every pair with the code pair (a, b) gives it at every pair whose code pair is one of the eight
  images of (a, b) (`StripIII.orbitForms`: the swap and the two reflections).
- H26 and H27 per representative (`hBoxAll5rep`, `hM1rep`), and the derivations of the package's per-class forms (`hBoxAll5_of_rep`,
  `hM1_of_rep`). H28 is in G2S0.OrbitM2.
Paper: "Positive correlation of bond energies in the O(3) and O(4) models", Appendix B, the proofs of Propositions B.14, B.22, B.24.
-/
import StripIIIM2.FullStripM2
import G2S0.Box5Reps

noncomputable section
open MeasureTheory

namespace G2Kernel

open StripIII (ECode)

/-! ### Automorphisms preserve the Gibbs law at uniform coupling -/

/-- a graph automorphism preserves the Gibbs law at uniform coupling: `⟨F(σ ∘ g)⟩ = ⟨F⟩` for every observable, every N -/
theorem gibbsExp_auto_invariant {N : ℕ} {V : Type*} [Fintype V] (G : SimpleGraph V) [DecidableRel G.Adj] (J0 : ℝ)
    (g : V → V) (hbij : Function.Bijective g) (hadj : ∀ p q, G.Adj p q ↔ G.Adj (g p) (g q)) (F : Config N V → ℝ) :
    gibbsExp N G (uniform J0) (fun σ => F (σ ∘ g)) = gibbsExp N G (uniform J0) F := by
  rcases Nat.eq_zero_or_pos N with rfl | hN
  · rcases isEmpty_or_nonempty V with hV | hV
    · have hF : (fun σ : Config 0 V => F (σ ∘ g)) = F := by
        funext σ
        congr 1
        funext v
        exact isEmptyElim v
      rw [hF]
    · have h0 : freeMeasure 0 V = 0 := freeMeasure_zero V
      simp [gibbsExp, partition, h0]
  · exact gibbsExp_comp_bij hN G J0 g hbij hadj F

theorem gibbsCov_auto_invariant {N : ℕ} {V : Type*} [Fintype V] (G : SimpleGraph V) [DecidableRel G.Adj] (J0 : ℝ)
    (g : V → V) (hbij : Function.Bijective g) (hadj : ∀ p q, G.Adj p q ↔ G.Adj (g p) (g q)) (a b : Sym2 V) :
    gibbsCov N G (uniform J0) (bond (Sym2.map g a)) (bond (Sym2.map g b))
      = gibbsCov N G (uniform J0) (bond a) (bond b) := by
  have ha : bond (N := N) (Sym2.map g a) = fun σ => bond a (σ ∘ g) :=
    funext fun σ => (bond_comp g a σ).symm
  have hb : bond (N := N) (Sym2.map g b) = fun σ => bond b (σ ∘ g) :=
    funext fun σ => (bond_comp g b σ).symm
  have e1 : (fun σ => bond (N := N) (Sym2.map g a) σ * bond (Sym2.map g b) σ)
      = fun σ => bond a (σ ∘ g) * bond b (σ ∘ g) := funext fun σ => by simp only [bond_comp]
  unfold gibbsCov
  rw [e1, gibbsExp_auto_invariant G J0 g hbij hadj (fun σ => bond a σ * bond b σ), ha, hb,
    gibbsExp_auto_invariant G J0 g hbij hadj (bond a), gibbsExp_auto_invariant G J0 g hbij hadj (bond b)]

theorem G2pair_auto_iff {N : ℕ} {V : Type*} [Fintype V] (G : SimpleGraph V) [DecidableRel G.Adj] (J0 : ℝ)
    (g : V → V) (hbij : Function.Bijective g) (hadj : ∀ p q, G.Adj p q ↔ G.Adj (g p) (g q)) (a b : Sym2 V) :
    G2pair N G (uniform J0) (Sym2.map g a) (Sym2.map g b) ↔ G2pair N G (uniform J0) a b := by
  unfold G2pair
  rw [gibbsCov_auto_invariant G J0 g hbij hadj a b]

/-! ### The two reflections of P_3 × P_n -/

/-- the reflection of `P_3 × P_n` in the middle row: row r to row 2 - r -/
def rowFlip {n : ℕ} (p : Fin 3 × Fin n) : Fin 3 × Fin n := (p.1.rev, p.2)

theorem rowFlip_rowFlip {n : ℕ} (p : Fin 3 × Fin n) : rowFlip (rowFlip p) = p := by
  simp [rowFlip]

theorem stripReflV_stripReflV {n : ℕ} (p : Fin 3 × Fin n) : stripReflV (stripReflV p) = p := by
  simp [stripReflV]

theorem rowFlip_bijective {n : ℕ} : Function.Bijective (rowFlip (n := n)) :=
  Function.Involutive.bijective rowFlip_rowFlip

theorem stripReflV_bijective {n : ℕ} : Function.Bijective (stripReflV (n := n)) :=
  Function.Involutive.bijective stripReflV_stripReflV

theorem strip_adj_iff' {n : ℕ} (p q : Fin 3 × Fin n) :
    (strip n).Adj p q ↔ p ≠ q ∧ (((p.1 = q.1 ∧ p.2.val + 1 = q.2.val) ∨ (p.2 = q.2 ∧ p.1.val + 1 = q.1.val)) ∨
      ((q.1 = p.1 ∧ q.2.val + 1 = p.2.val) ∨ (q.2 = p.2 ∧ q.1.val + 1 = p.1.val))) := by
  rw [strip, SimpleGraph.fromRel_adj]

theorem strip_adj_rowFlip {n : ℕ} (p q : Fin 3 × Fin n) :
    (strip n).Adj p q ↔ (strip n).Adj (rowFlip p) (rowFlip q) := by
  obtain ⟨p1, p2⟩ := p
  obtain ⟨q1, q2⟩ := q
  have h1 := p1.isLt
  have h2 := q1.isLt
  simp only [strip_adj_iff', rowFlip, ne_eq, Prod.mk.injEq, Fin.ext_iff, Fin.val_rev]
  omega

theorem strip_adj_stripReflV {n : ℕ} (p q : Fin 3 × Fin n) :
    (strip n).Adj p q ↔ (strip n).Adj (stripReflV p) (stripReflV q) := by
  obtain ⟨p1, p2⟩ := p
  obtain ⟨q1, q2⟩ := q
  have h1 := p2.isLt
  have h2 := q2.isLt
  simp only [strip_adj_iff', stripReflV, ne_eq, Prod.mk.injEq, Fin.ext_iff, Fin.val_rev]
  omega

theorem nonempty_of_sym2 {α : Type*} (e : Sym2 α) : Nonempty α := by
  induction e using Sym2.ind with
  | h p q => exact ⟨p⟩

/-- the reflection in the middle row maps an edge to an edge, and its code to the flipped code -/
theorem edgeCode_rowFlip {n : ℕ} {e : Sym2 (Fin 3 × Fin n)} (he : e ∈ (strip n).edgeSet) :
    Sym2.map rowFlip e ∈ (strip n).edgeSet ∧ edgeCode (Sym2.map rowFlip e) = (edgeCode e).flip := by
  rcases strip_edge_forms he with ⟨r, i, j, hij, rfl⟩ | ⟨t, u, j, htu, rfl⟩
  · rw [Sym2.map_mk]
    show s((r.rev, i), (r.rev, j)) ∈ (strip n).edgeSet ∧
      edgeCode s((r.rev, i), (r.rev, j)) = (edgeCode s((r, i), (r, j))).flip
    refine ⟨strip_row_mem r.rev i j (Or.inl hij), ?_⟩
    rw [edgeCode_hor r.rev i j hij, edgeCode_hor r i j hij]
    show ECode.hor r.rev.val i.val = ECode.hor (2 - r.val) i.val
    rw [Fin.val_rev]
    congr 1
    omega
  · have hu := u.isLt
    have h' : u.rev.val + 1 = t.rev.val := by rw [Fin.val_rev, Fin.val_rev]; omega
    rw [Sym2.map_mk]
    show s((t.rev, j), (u.rev, j)) ∈ (strip n).edgeSet ∧
      edgeCode s((t.rev, j), (u.rev, j)) = (edgeCode s((t, j), (u, j))).flip
    have hs : s((t.rev, j), (u.rev, j)) = s((u.rev, j), (t.rev, j)) := Sym2.eq_swap
    rw [hs]
    refine ⟨strip_col_mem u.rev t.rev j h', ?_⟩
    rw [edgeCode_ver u.rev t.rev j h', edgeCode_ver t u j htu]
    show ECode.ver u.rev.val j.val = ECode.ver (1 - t.val) j.val
    rw [Fin.val_rev]
    congr 1
    omega

/-! ### Edge codes under the two reflections -/

namespace StripIII.ECode

theorem flip_flip {n : ℕ} {c : ECode} (h : c.valid n = true) : c.flip.flip = c := by
  cases c with
  | hor r i =>
    simp only [ECode.valid, Bool.and_eq_true, decide_eq_true_eq] at h
    simp only [ECode.flip, ECode.hor.injEq, and_true]
    omega
  | ver t j =>
    simp only [ECode.valid, Bool.and_eq_true, decide_eq_true_eq] at h
    simp only [ECode.flip, ECode.ver.injEq, and_true]
    omega

theorem lr_lr {n : ℕ} {c : ECode} (h : c.valid n = true) : (c.lr n).lr n = c := by
  cases c with
  | hor r i =>
    simp only [ECode.valid, Bool.and_eq_true, decide_eq_true_eq] at h
    simp only [ECode.lr, ECode.hor.injEq, true_and]
    omega
  | ver t j =>
    simp only [ECode.valid, Bool.and_eq_true, decide_eq_true_eq] at h
    simp only [ECode.lr, ECode.ver.injEq, true_and]
    omega

theorem valid_flip {n : ℕ} {c : ECode} (h : c.valid n = true) : c.flip.valid n = true := by
  cases c with
  | hor r i =>
    simp only [ECode.valid, Bool.and_eq_true, decide_eq_true_eq] at h
    simp only [ECode.flip, ECode.valid, Bool.and_eq_true, decide_eq_true_eq]
    omega
  | ver t j =>
    simp only [ECode.valid, Bool.and_eq_true, decide_eq_true_eq] at h
    simp only [ECode.flip, ECode.valid, Bool.and_eq_true, decide_eq_true_eq]
    omega

end StripIII.ECode

/-! ### The orbit step for one representative -/

/-- **the orbit step**: if every pair of edges with the code pair (a, b) satisfies `G2pair`, so does every pair of edges whose code
pair is one of the eight images of (a, b) under the swap and the reflections in the middle row and in the vertical midline -/
theorem G2pair_of_orbitForms {N n : ℕ} {J : ℝ} {a b : ECode} (ha : a.valid n = true) (hb : b.valid n = true)
    (hrep : ∀ e' ∈ (strip n).edgeSet, ∀ f' ∈ (strip n).edgeSet, edgeCode e' = a → edgeCode f' = b →
      G2pair N (strip n) (uniform J) e' f')
    {e f : Sym2 (Fin 3 × Fin n)} (he : e ∈ (strip n).edgeSet) (hf : f ∈ (strip n).edgeSet)
    (hmem : (edgeCode e, edgeCode f) ∈ StripIII.orbitForms n a b) : G2pair N (strip n) (uniform J) e f := by
  have hF : ∀ x y : Sym2 (Fin 3 × Fin n), G2pair N (strip n) (uniform J) (Sym2.map rowFlip x) (Sym2.map rowFlip y) ↔
      G2pair N (strip n) (uniform J) x y :=
    G2pair_auto_iff (strip n) J rowFlip rowFlip_bijective strip_adj_rowFlip
  have hR : ∀ x y : Sym2 (Fin 3 × Fin n),
      G2pair N (strip n) (uniform J) (Sym2.map stripReflV x) (Sym2.map stripReflV y) ↔ G2pair N (strip n) (uniform J) x y :=
    G2pair_auto_iff (strip n) J stripReflV stripReflV_bijective strip_adj_stripReflV
  have hfa := StripIII.ECode.valid_flip ha
  have hfb := StripIII.ECode.valid_flip hb
  simp only [StripIII.orbitForms, List.mem_cons, List.mem_nil_iff, or_false, Prod.mk.injEq] at hmem
  obtain ⟨heF, hceF⟩ := edgeCode_rowFlip he
  obtain ⟨hfF, hcfF⟩ := edgeCode_rowFlip hf
  obtain ⟨heR, hceR⟩ := edgeCode_stripReflV he
  obtain ⟨hfR, hcfR⟩ := edgeCode_stripReflV hf
  obtain ⟨heRF, hceRF⟩ := edgeCode_rowFlip heR
  obtain ⟨hfRF, hcfRF⟩ := edgeCode_rowFlip hfR
  rcases hmem with ⟨h1, h2⟩ | ⟨h1, h2⟩ | ⟨h1, h2⟩ | ⟨h1, h2⟩ | ⟨h1, h2⟩ | ⟨h1, h2⟩ | ⟨h1, h2⟩ | ⟨h1, h2⟩
  · exact hrep e he f hf h1 h2
  · exact G2pair_symm_strip (hrep f hf e he h2 h1)
  · have h := hrep _ heF _ hfF (by rw [hceF, h1, StripIII.ECode.flip_flip ha])
      (by rw [hcfF, h2, StripIII.ECode.flip_flip hb])
    exact (hF e f).mp h
  · have h := hrep _ hfF _ heF (by rw [hcfF, h2, StripIII.ECode.flip_flip ha])
      (by rw [hceF, h1, StripIII.ECode.flip_flip hb])
    exact G2pair_symm_strip ((hF f e).mp h)
  · have h := hrep _ heR _ hfR (by rw [hceR, h1, StripIII.ECode.lr_lr ha])
      (by rw [hcfR, h2, StripIII.ECode.lr_lr hb])
    exact (hR e f).mp h
  · have h := hrep _ hfR _ heR (by rw [hcfR, h2, StripIII.ECode.lr_lr ha])
      (by rw [hceR, h1, StripIII.ECode.lr_lr hb])
    exact G2pair_symm_strip ((hR f e).mp h)
  · have h := hrep _ heRF _ hfRF (by rw [hceRF, hceR, h1, StripIII.ECode.lr_lr hfa, StripIII.ECode.flip_flip ha])
      (by rw [hcfRF, hcfR, h2, StripIII.ECode.lr_lr hfb, StripIII.ECode.flip_flip hb])
    exact (hR e f).mp ((hF _ _).mp h)
  · have h := hrep _ hfRF _ heRF (by rw [hcfRF, hcfR, h2, StripIII.ECode.lr_lr hfa, StripIII.ECode.flip_flip ha])
      (by rw [hceRF, hceR, h1, StripIII.ECode.lr_lr hfb, StripIII.ECode.flip_flip hb])
    exact G2pair_symm_strip ((hR f e).mp ((hF _ _).mp h))

/-! ### H26 per representative (the n = 5 box records) -/

/-- **hBoxAll5rep** (H26 per representative; kind: restatement, exactly what the n = 5 box records certify, Proposition B.14):
for J >= jLow N, every pair of edges of P_3 x P_5 whose code pair is a representative pair in `R` has nonnegative covariance.
The records' representatives are `StripIII.box5Reps` (G2S0.Box5Reps, the tables' orbit column). -/
def hBoxAll5rep (N : ℕ) (R : List (ECode × ECode)) : Prop :=
  ∀ J : ℝ, jLow N ≤ J → ∀ q ∈ R, ∀ e ∈ (strip 5).edgeSet, ∀ f ∈ (strip 5).edgeSet,
    edgeCode e = q.1 → edgeCode f = q.2 → G2pair N (strip 5) (uniform J) e f

/-- the check of a representative list `R` against a class list `L` at n = 5: every representative is a pair of valid codes, and
every member of `L` is one of the eight images of a representative -/
def StripIII.box5RepCheck (R L : List (ECode × ECode)) : Bool :=
  R.all (fun q => q.1.valid 5 && q.2.valid 5) &&
    L.all (fun p => R.any (fun q => (StripIII.orbitForms 5 q.1 q.2).contains p))

theorem box5RepCheck_final :
    StripIII.box5RepCheck StripIII.box5Reps (box5AllList34 ++ box5Stage2) = true := by
  decide +kernel

/-- control: every representative is itself a member of the final list (in one order), and no two representatives lie in one
orbit, so the 36 representatives stand for 36 distinct orbits -/
theorem box5Reps_controls :
    StripIII.box5Reps.all (fun q => (box5AllList34 ++ box5Stage2).contains q ||
      (box5AllList34 ++ box5Stage2).contains (q.2, q.1)) = true ∧
    StripIII.box5Reps.all (fun q => (StripIII.box5Reps.filter fun q' =>
      (StripIII.orbitForms 5 q.1 q.2).contains q').length == 1) = true := by
  decide +kernel

theorem hBoxAll5_of_rep_gen (N : ℕ) (R L : List (ECode × ECode)) (hc : StripIII.box5RepCheck R L = true)
    (h : hBoxAll5rep N R) : hBoxAll5 N L := by
  intro J hJ e he f hf _hef hL
  simp only [StripIII.box5RepCheck, Bool.and_eq_true, List.all_eq_true, List.any_eq_true] at hc
  obtain ⟨hv, hcov⟩ := hc
  obtain ⟨q, hq, hqp⟩ := hcov _ (List.contains_iff_mem.mp hL)
  have hqv := hv q hq
  exact G2pair_of_orbitForms hqv.1 hqv.2 (fun e' he' f' hf' h1 h2 => h J hJ q hq e' he' f' hf' h1 h2) he hf
    (List.contains_iff_mem.mp hqp)

/-- **H26 from its representatives**: the n = 5 box records' representatives give the package's per-class hypothesis
`hBoxAll5 N (box5AllList34 ++ box5Stage2)` -/
theorem hBoxAll5_of_rep (N : ℕ) :
    hBoxAll5rep N StripIII.box5Reps → hBoxAll5 N (box5AllList34 ++ box5Stage2) :=
  hBoxAll5_of_rep_gen N _ _ box5RepCheck_final

/-! ### H27 per representative (M1's record rows) -/

/-- **hM1rep** (H27 per representative; kind: restatement, exactly what M1's assembly record certifies, Proposition B.22): for
J >= jLow N, each row (n, a, b) of `L` with 6 <= n <= nmax, the row's representative pair (a, b) of edges of P_3 x P_n has
nonnegative covariance. -/
def hM1rep (N : ℕ) (L : List (ℕ × ECode × ECode)) (nmax : ℕ) : Prop :=
  ∀ J : ℝ, jLow N ≤ J → ∀ q ∈ L, 6 ≤ q.1 → q.1 ≤ nmax →
    ∀ e ∈ (strip q.1).edgeSet, ∀ f ∈ (strip q.1).edgeSet, edgeCode e = q.2.1 → edgeCode f = q.2.2 →
      G2pair N (strip q.1) (uniform J) e f

theorem hM1_of_rep_gen (N : ℕ) (L : List (ℕ × ECode × ECode)) (nmax : ℕ)
    (hOrb : ∀ n, 6 ≤ n → n ≤ nmax → StripIII.m1Orbit L n = true)
    (hIn : ∀ n, 6 ≤ n → n ≤ nmax → StripIII.m1InClass L n = true)
    (h : hM1rep N L nmax) : hM1 N L nmax := by
  intro J hJ n h6 hn e he f hf hef hkey
  simp only [StripIII.m1Keys, List.contains_iff_mem, List.mem_map, List.mem_filter, beq_iff_eq] at hkey
  obtain ⟨q, ⟨hqL, hqn⟩, hqk⟩ := hkey
  have hp : (edgeCode e, edgeCode f) ∈ StripIII.allPairsAll n :=
    StripIII.mem_allPairsAll (edgeCode_valid he) (edgeCode_valid hf) (fun h' => hef (edgeCode_inj he hf h'))
  have hO := hOrb n h6 hn
  simp only [StripIII.m1Orbit, List.all_eq_true, List.mem_filter, beq_iff_eq, Bool.or_eq_true, bne_iff_ne,
    ne_eq] at hO
  have hmem0 := hO _ hp q ⟨hqL, hqn⟩
  have hmem : (edgeCode e, edgeCode f) ∈ StripIII.orbitForms n q.2.1 q.2.2 := by
    rcases hmem0 with hk | hk
    · exact absurd hqk hk
    · exact List.contains_iff_mem.mp hk
  have hI := hIn n h6 hn
  simp only [StripIII.m1InClass, List.all_eq_true, List.mem_filter, beq_iff_eq] at hI
  have hqt := hI q ⟨hqL, hqn⟩
  simp only [StripIII.todoH, Bool.and_eq_true] at hqt
  obtain ⟨⟨⟨⟨⟨⟨hva, hvb⟩, -⟩, -⟩, -⟩, -⟩, -⟩ := hqt
  subst hqn
  exact G2pair_of_orbitForms hva hvb (fun e' he' f' hf' h1 h2 => h J hJ q hqL h6 hn e' he' f' hf' h1 h2) he hf hmem

theorem m1Orbit_all : ∀ n, 6 ≤ n → n ≤ StripIII.NMAX_M1 → StripIII.m1Orbit StripIII.m1List n = true := by
  intro n h6 hn
  have h11 : n ≤ 11 := Nat.le_trans hn StripIII.NMAX_M1_range.2
  rcases (by omega : n = 6 ∨ n = 7 ∨ n = 8 ∨ n = 9 ∨ n = 10 ∨ n = 11) with rfl | rfl | rfl | rfl | rfl | rfl
  · exact StripIII.m1Orbit_n6
  · exact StripIII.m1Orbit_n7
  · exact StripIII.m1Orbit_n8
  · exact StripIII.m1Orbit_n9
  · exact StripIII.m1Orbit_n10
  · exact StripIII.m1Orbit_n11

theorem m1InClass_all : ∀ n, 6 ≤ n → n ≤ StripIII.NMAX_M1 → StripIII.m1InClass StripIII.m1List n = true := by
  intro n h6 hn
  have h11 : n ≤ 11 := Nat.le_trans hn StripIII.NMAX_M1_range.2
  rcases (by omega : n = 6 ∨ n = 7 ∨ n = 8 ∨ n = 9 ∨ n = 10 ∨ n = 11) with rfl | rfl | rfl | rfl | rfl | rfl
  · exact StripIII.m1InClass_n6
  · exact StripIII.m1InClass_n7
  · exact StripIII.m1InClass_n8
  · exact StripIII.m1InClass_n9
  · exact StripIII.m1InClass_n10
  · exact StripIII.m1InClass_n11

/-- **H27 from its representatives**: M1's record rows give the package's per-class hypothesis `hM1 N m1List NMAX_M1` -/
theorem hM1_of_rep (N : ℕ) : hM1rep N StripIII.m1List StripIII.NMAX_M1 → hM1 N StripIII.m1List StripIII.NMAX_M1 :=
  hM1_of_rep_gen N _ _ m1Orbit_all m1InClass_all

end G2Kernel

#print axioms G2Kernel.gibbsExp_auto_invariant
#print axioms G2Kernel.G2pair_auto_iff
#print axioms G2Kernel.strip_adj_rowFlip
#print axioms G2Kernel.strip_adj_stripReflV
#print axioms G2Kernel.edgeCode_rowFlip
#print axioms G2Kernel.G2pair_of_orbitForms
#print axioms G2Kernel.box5RepCheck_final
#print axioms G2Kernel.box5Reps_controls
#print axioms G2Kernel.hBoxAll5_of_rep
#print axioms G2Kernel.hM1_of_rep
