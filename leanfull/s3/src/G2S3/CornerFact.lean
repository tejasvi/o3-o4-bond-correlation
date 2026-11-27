/-
G2S3.CornerFact (stage S3, Part C4): Lemma 2.4 at a vertex v of degree two with edges e = vx, f = vy
(STATEMENTS_S3_v5.md, C4). Integrating out σ_v (S1's `exp_exp_integral_hasSum`) gives Z(a, b) = Σ_c u_c k_c(a) k_c(b) with
u_c = ∫ Π_c(σ_x, σ_y) e^{H}, H the energy with J_e = J_f = 0. Then u_c ≥ 0 (vertex elimination, Part C3), u_0 = Z_H > 0,
u_c ≤ d_c u_0 ≤ (c+1)^N u_0, and u_1 > 0 for a positive path from x to y avoiding v. At the corners of P_3 × P_n this is
H8 `hCornerFactor N (kConc N)`, for every N ≥ 2.
-/
import G2S3.GramExp
import G2S3.Corner

noncomputable section
open MeasureTheory Real

namespace G2S3

open G2Kernel

section Corner

variable {N : ℕ} {V : Type*} [Fintype V] [DecidableEq V]

/-- the weight of the common label: u_c = ∫ Π_c(σ_x, σ_y) e^{H}, H the energy with J_e = J_f = 0 -/
def uCorner (N : ℕ) (G : SimpleGraph V) [DecidableRel G.Adj] (J : Sym2 V → ℝ) (e f : Sym2 V) (x y : V) (c : ℕ) : ℝ :=
  ∫ σ, zonal N c (σ x) (σ y) * Real.exp (energy G (Function.update (Function.update J e 0) f 0) σ) ∂(freeMeasure N V)

theorem ferro_update2 {G : SimpleGraph V} [DecidableRel G.Adj] {J : Sym2 V → ℝ} (hJ : Ferro G J) (e f : Sym2 V) :
    Ferro G (Function.update (Function.update J e 0) f 0) := by
  intro g hg
  by_cases hgf : g = f
  · rw [hgf, Function.update_self]
  · rw [Function.update_of_ne hgf]
    by_cases hge : g = e
    · rw [hge, Function.update_self]
    · rw [Function.update_of_ne hge]
      exact hJ g hg

theorem bond_update_of_notMem {g : Sym2 V} {v : V} (hv : v ∉ g) (σ : Config N V) (z : Sph N) :
    bond g (Function.update σ v z) = bond g σ := by
  induction g using Sym2.ind with
  | h a b =>
    have ha : a ≠ v := fun h => hv (h ▸ Sym2.mem_mk_left a b)
    have hb : b ≠ v := fun h => hv (h ▸ Sym2.mem_mk_right a b)
    show dot (Function.update σ v z a) (Function.update σ v z b) = dot (σ a) (σ b)
    rw [Function.update_of_ne ha, Function.update_of_ne hb]

theorem energy_update_two (G : SimpleGraph V) [DecidableRel G.Adj] (J : Sym2 V → ℝ) {e f : Sym2 V}
    (he : e ∈ G.edgeFinset) (hf : f ∈ G.edgeFinset) (hef : e ≠ f) (a b : ℝ) (σ : Config N V) :
    energy G (Function.update (Function.update J e a) f b) σ
      = energy G (Function.update (Function.update J e 0) f 0) σ + a * bond e σ + b * bond f σ := by
  unfold energy
  have hf' : f ∈ G.edgeFinset.erase e := Finset.mem_erase.mpr ⟨hef.symm, hf⟩
  rw [← Finset.add_sum_erase _ _ he, ← Finset.add_sum_erase _ _ he, ← Finset.add_sum_erase _ _ hf',
    ← Finset.add_sum_erase _ _ hf']
  have hrest : ∀ g ∈ (G.edgeFinset.erase e).erase f, Function.update (Function.update J e a) f b g * bond g σ
      = Function.update (Function.update J e 0) f 0 g * bond g σ := by
    intro g hg
    have hgf : g ≠ f := (Finset.mem_erase.mp hg).1
    have hge : g ≠ e := (Finset.mem_erase.mp (Finset.mem_erase.mp hg).2).1
    rw [Function.update_of_ne hgf, Function.update_of_ne hge, Function.update_of_ne hgf, Function.update_of_ne hge]
  rw [Finset.sum_congr rfl hrest]
  have h1 : Function.update (Function.update J e a) f b e = a := by
    rw [Function.update_of_ne hef, Function.update_self]
  have h2 : Function.update (Function.update J e a) f b f = b := Function.update_self _ _ _
  have h3 : Function.update (Function.update J e 0) f 0 e = 0 := by
    rw [Function.update_of_ne hef, Function.update_self]
  have h4 : Function.update (Function.update J e 0) f 0 f = 0 := Function.update_self _ _ _
  rw [h1, h2, h3, h4]
  ring

theorem nbr_edge {G : SimpleGraph V} [DecidableRel G.Adj] {v x y : V} (hnb : G.neighborFinset v = {x, y})
    {g : Sym2 V} (hg : g ∈ G.edgeFinset) (hv : v ∈ g) : g = s(v, x) ∨ g = s(v, y) := by
  obtain ⟨w, rfl⟩ := Sym2.mem_iff_exists.mp hv
  have hadj : G.Adj v w := G.mem_edgeFinset.mp hg
  have hw : w ∈ G.neighborFinset v := (G.mem_neighborFinset v w).mpr hadj
  rw [hnb, Finset.mem_insert, Finset.mem_singleton] at hw
  rcases hw with rfl | rfl
  · exact Or.inl rfl
  · exact Or.inr rfl

theorem energy0_update_v (G : SimpleGraph V) [DecidableRel G.Adj] (J : Sym2 V → ℝ) {v x y : V}
    (hnb : G.neighborFinset v = {x, y}) (σ : Config N V) (z : Sph N) :
    energy G (Function.update (Function.update J s(v, x) 0) s(v, y) 0) (Function.update σ v z)
      = energy G (Function.update (Function.update J s(v, x) 0) s(v, y) 0) σ := by
  unfold energy
  refine Finset.sum_congr rfl (fun g hg => ?_)
  by_cases hv : v ∈ g
  · have h0 : Function.update (Function.update J s(v, x) 0) s(v, y) 0 g = 0 := by
      rcases nbr_edge hnb hg hv with rfl | rfl
      · by_cases hxy : s(v, x) = s(v, y)
        · rw [hxy, Function.update_self]
        · rw [Function.update_of_ne hxy, Function.update_self]
      · exact Function.update_self _ _ _
    rw [h0, zero_mul, zero_mul]
  · rw [bond_update_of_notMem hv]

theorem abs_kConc_le_series (hN : 2 ≤ N) (c : ℕ) (a : ℝ) :
    |kConc N c a| ≤ (∑' m : ℕ, ((|a| / 2) ^ 2) ^ m / (m.factorial : ℝ)) * ((|a| / 2) ^ c / (c.factorial : ℝ)) :=
  (abs_kConc_le hN c a).trans (kConc_abs_le hN c a)

/-- **Lemma 2.4 at a vertex of degree two**: Z = Σ_c u_c k_c(a) k_c(b) for all real a, b -/
theorem corner_factor (hN : 2 ≤ N) (G : SimpleGraph V) [DecidableRel G.Adj] (J : Sym2 V → ℝ) {v x y : V}
    (hnb : G.neighborFinset v = {x, y}) (hxy : x ≠ y) (a b : ℝ) :
    HasSum (fun c => uCorner N G J s(v, x) s(v, y) x y c * kConc N c a * kConc N c b)
      (partition N G (Function.update (Function.update J s(v, x) a) s(v, y) b)) := by
  have hN0 : 0 < N := by omega
  have hprob := omega_isProbabilityMeasure N hN0
  haveI : IsProbabilityMeasure (freeMeasure N V) := by unfold freeMeasure; infer_instance
  have hvx : G.Adj v x := (G.mem_neighborFinset v x).mp (by rw [hnb]; simp)
  have hvy : G.Adj v y := (G.mem_neighborFinset v y).mp (by rw [hnb]; simp)
  have hxv : x ≠ v := (G.ne_of_adj hvx).symm
  have hyv : y ≠ v := (G.ne_of_adj hvy).symm
  have he : s(v, x) ∈ G.edgeFinset := G.mem_edgeFinset.mpr hvx
  have hf : s(v, y) ∈ G.edgeFinset := G.mem_edgeFinset.mpr hvy
  have hef : s(v, x) ≠ s(v, y) := fun h => hxy (Sym2.congr_right.mp h)
  set J0 := Function.update (Function.update J s(v, x) 0) s(v, y) 0 with hJ0
  unfold partition
  simp only [energy_update_two G J he hf hef a b]
  have hmE : Measurable (energy (N := N) G J0) := measurable_energy G J0
  have hbdd : BddMeas (fun σ : Config N V => Real.exp (energy G J0 σ + a * bond s(v, x) σ + b * bond s(v, y) σ)) := by
    refine ⟨(((hmE.add ((measurable_bond s(v, x)).const_mul a)).add
      ((measurable_bond s(v, y)).const_mul b))).exp, Real.exp (∑ g ∈ G.edgeFinset, |J0 g| + |a| + |b|), fun σ => ?_⟩
    rw [abs_of_pos (Real.exp_pos _)]
    refine Real.exp_le_exp.mpr ?_
    have h1 := (le_abs_self _).trans (abs_energy_le G J0 σ)
    have h2 : a * bond s(v, x) σ ≤ |a| := by
      have := abs_bond_le s(v, x) σ
      calc a * bond s(v, x) σ ≤ |a * bond s(v, x) σ| := le_abs_self _
        _ = |a| * |bond s(v, x) σ| := abs_mul _ _
        _ ≤ |a| * 1 := mul_le_mul_of_nonneg_left this (abs_nonneg _)
        _ = |a| := mul_one _
    have h3 : b * bond s(v, y) σ ≤ |b| := by
      have := abs_bond_le s(v, y) σ
      calc b * bond s(v, y) σ ≤ |b * bond s(v, y) σ| := le_abs_self _
        _ = |b| * |bond s(v, y) σ| := abs_mul _ _
        _ ≤ |b| * 1 := mul_le_mul_of_nonneg_left this (abs_nonneg _)
        _ = |b| := mul_one _
    linarith
  rw [integral_update hN0 v _ hbdd]
  have hin : ∀ σ : Config N V, ∫ z, Real.exp (energy G J0 (Function.update σ v z) +
      a * bond s(v, x) (Function.update σ v z) + b * bond s(v, y) (Function.update σ v z)) ∂(omega N)
        = Real.exp (energy G J0 σ) * ∫ z, Real.exp (a * dot (σ x) z) * Real.exp (b * dot z (σ y)) ∂(omega N) := by
    intro σ
    rw [← integral_const_mul]
    congr 1
    funext z
    have hb1 : bond s(v, x) (Function.update σ v z) = dot (σ x) z := by
      show dot (Function.update σ v z v) (Function.update σ v z x) = dot (σ x) z
      rw [Function.update_self, Function.update_of_ne hxv, dot_comm]
    have hb2 : bond s(v, y) (Function.update σ v z) = dot z (σ y) := by
      show dot (Function.update σ v z v) (Function.update σ v z y) = dot z (σ y)
      rw [Function.update_self, Function.update_of_ne hyv]
    rw [energy0_update_v G J hnb σ z, hb1, hb2, Real.exp_add, Real.exp_add]
    ring
  simp only [hin]
  -- the series under the integral
  obtain ⟨M, hM⟩ : ∃ M : ℝ, ∀ σ : Config N V, |energy G J0 σ| ≤ M := ⟨_, fun σ => abs_energy_le G J0 σ⟩
  set Ka := ∑' m : ℕ, ((|a| / 2) ^ 2) ^ m / (m.factorial : ℝ) with hKa
  set Tb := ∑' l : ℕ, |kConc N l b| * dConc N l with hTb
  have hKa0 : 0 ≤ Ka := tsum_nonneg (fun m => by positivity)
  have hTb_le : ∀ c, |kConc N c b| * dConc N c ≤ Tb := fun c =>
    (summable_kConc_dConc hN b).le_tsum c (fun j _ => mul_nonneg (abs_nonneg _) (dConc_pos_S1 hN j).le)
  have hB : ∀ (c : ℕ) (σ : Config N V),
      |Real.exp (energy G J0 σ) * (kConc N c a * kConc N c b * zonal N c (σ x) (σ y))|
        ≤ Real.exp M * (Ka * ((|a| / 2) ^ c / (c.factorial : ℝ)) * Tb) := by
    intro c σ
    rw [abs_mul, abs_of_pos (Real.exp_pos _), abs_mul, abs_mul]
    have h1 : Real.exp (energy G J0 σ) ≤ Real.exp M := Real.exp_le_exp.mpr ((le_abs_self _).trans (hM σ))
    have h2 := abs_kConc_le_series hN c a
    have h3 : |kConc N c b| * |zonal N c (σ x) (σ y)| ≤ Tb :=
      (mul_le_mul_of_nonneg_left (abs_zonal_le hN c (σ x) (σ y)) (abs_nonneg _)).trans (hTb_le c)
    calc Real.exp (energy G J0 σ) * (|kConc N c a| * |kConc N c b| * |zonal N c (σ x) (σ y)|)
        = Real.exp (energy G J0 σ) * (|kConc N c a| * (|kConc N c b| * |zonal N c (σ x) (σ y)|)) := by ring
      _ ≤ Real.exp M * (Ka * ((|a| / 2) ^ c / (c.factorial : ℝ)) * Tb) := by
        refine mul_le_mul h1 (mul_le_mul h2 h3 (by positivity) (by positivity)) (by positivity) (Real.exp_pos _).le
  have hmeas : ∀ c : ℕ, AEStronglyMeasurable
      (fun σ : Config N V => Real.exp (energy G J0 σ) * (kConc N c a * kConc N c b * zonal N c (σ x) (σ y)))
      (freeMeasure N V) := by
    intro c
    have hz0 := ((continuous_zonal N c).measurable).comp
      ((measurable_pi_apply (X := fun _ : V => Sph N) x).prodMk (measurable_pi_apply y))
    have hz : Measurable (fun σ : Config N V => zonal N c (σ x) (σ y)) := hz0
    exact (hmE.exp.mul (hz.const_mul (kConc N c a * kConc N c b))).aestronglyMeasurable
  have hsum : Summable (fun c : ℕ => Real.exp M * (Ka * ((|a| / 2) ^ c / (c.factorial : ℝ)) * Tb)) :=
    (((Real.summable_pow_div_factorial (|a| / 2)).mul_left Ka).mul_right Tb).mul_left (Real.exp M)
  have hS := hasSum_integral_of_bound (μ := freeMeasure N V) _ _ _ hmeas hB hsum
    (fun σ => (exp_exp_integral_hasSum hN a b (σ x) (σ y)).mul_left (Real.exp (energy G J0 σ)))
  convert hS using 1
  funext c
  unfold uCorner
  rw [← hJ0]
  rw [show (fun σ : Config N V => Real.exp (energy G J0 σ) * (kConc N c a * kConc N c b * zonal N c (σ x) (σ y)))
      = fun σ => (kConc N c a * kConc N c b) * (zonal N c (σ x) (σ y) * Real.exp (energy G J0 σ)) from
      funext (fun σ => by ring), integral_const_mul]
  ring

theorem zonal_bdd (hN : 2 ≤ N) (c : ℕ) : BddMeas (fun q : Sph N × Sph N => zonal N c q.1 q.2) :=
  ⟨(continuous_zonal N c).measurable, dConc N c, fun q => abs_zonal_le hN c q.1 q.2⟩

theorem expE_bdd (G : SimpleGraph V) [DecidableRel G.Adj] (J : Sym2 V → ℝ) :
    BddMeas (fun σ : Config N V => Real.exp (energy G J σ)) :=
  ⟨(measurable_energy G J).exp, Real.exp (∑ g ∈ G.edgeFinset, |J g|), fun σ => by
    rw [abs_of_pos (Real.exp_pos _)]
    exact Real.exp_le_exp.mpr ((le_abs_self _).trans (abs_energy_le G J σ))⟩

theorem uCorner_nonneg (hN : 2 ≤ N) (G : SimpleGraph V) [DecidableRel G.Adj] (J : Sym2 V → ℝ) (hJ : Ferro G J)
    {v x y : V} (hxy : x ≠ y) (c : ℕ) : 0 ≤ uCorner N G J s(v, x) s(v, y) x y c :=
  gram_exp_pos (by omega) G _ (ferro_update2 hJ _ _) hxy (zonal_bdd hN c) (zonal_posType hN c)

theorem zonal_zero (N : ℕ) (s t : Sph N) : zonal N 0 s t = 1 := by
  simp [zonal, dConc_zero, CConc]

theorem uCorner_zero_eq (G : SimpleGraph V) [DecidableRel G.Adj] (J : Sym2 V → ℝ) (v x y : V) :
    uCorner N G J s(v, x) s(v, y) x y 0
      = partition N G (Function.update (Function.update J s(v, x) 0) s(v, y) 0) := by
  unfold uCorner partition
  simp only [zonal_zero, one_mul]

theorem uCorner_zero_pos (hN : 2 ≤ N) (G : SimpleGraph V) [DecidableRel G.Adj] (J : Sym2 V → ℝ) {v x y : V} :
    0 < uCorner N G J s(v, x) s(v, y) x y 0 := by
  rw [uCorner_zero_eq]
  exact partition_pos (by omega) G _

theorem uCorner_le (hN : 2 ≤ N) (G : SimpleGraph V) [DecidableRel G.Adj] (J : Sym2 V → ℝ) {v x y : V} (c : ℕ) :
    uCorner N G J s(v, x) s(v, y) x y c ≤ ((c : ℝ) + 1) ^ N * uCorner N G J s(v, x) s(v, y) x y 0 := by
  have hN0 : 0 < N := by omega
  have hprob := omega_isProbabilityMeasure N hN0
  haveI : IsProbabilityMeasure (freeMeasure N V) := by unfold freeMeasure; infer_instance
  set J0 := Function.update (Function.update J s(v, x) 0) s(v, y) 0 with hJ0
  have hz0 := ((continuous_zonal N c).measurable).comp
    ((measurable_pi_apply (X := fun _ : V => Sph N) x).prodMk (measurable_pi_apply y))
  have hz : Measurable (fun σ : Config N V => zonal N c (σ x) (σ y)) := hz0
  have hint1 : Integrable (fun σ : Config N V => zonal N c (σ x) (σ y) * Real.exp (energy G J0 σ))
      (freeMeasure N V) :=
    (BddMeas.mul ⟨hz, dConc N c, fun σ => abs_zonal_le hN c _ _⟩ (expE_bdd G J0)).integrable
  have hint2 : Integrable (fun σ : Config N V => dConc N c * Real.exp (energy G J0 σ)) (freeMeasure N V) :=
    ((expE_bdd G J0).integrable).const_mul _
  have h1 : uCorner N G J s(v, x) s(v, y) x y c ≤ ∫ σ, dConc N c * Real.exp (energy G J0 σ) ∂(freeMeasure N V) :=
    integral_mono hint1 hint2 (fun σ => mul_le_mul_of_nonneg_right
      ((le_abs_self _).trans (abs_zonal_le hN c _ _)) (Real.exp_pos _).le)
  have h2 : ∫ σ, dConc N c * Real.exp (energy G J0 σ) ∂(freeMeasure N V)
      = dConc N c * uCorner N G J s(v, x) s(v, y) x y 0 := by
    rw [integral_const_mul, uCorner_zero_eq]
    rfl
  rw [h2] at h1
  exact h1.trans (mul_le_mul_of_nonneg_right (dConc_le_pow hN c) (uCorner_zero_pos hN G J).le)

theorem uCorner_one_pos (hN : 2 ≤ N) (G : SimpleGraph V) [DecidableRel G.Adj] (J : Sym2 V → ℝ) (hJ : Ferro G J)
    {v x y : V} (hxy : x ≠ y) (p : G.Walk x y) (hp : p.IsPath) (hv : v ∉ p.support)
    (hpos : ∀ g ∈ p.edges, 0 < J g) : 0 < uCorner N G J s(v, x) s(v, y) x y 1 := by
  refine gram_exp_path_pos hN G _ (ferro_update2 hJ _ _) hxy p hp (fun g hg => ?_)
  have hvg : v ∉ g := by
    intro hvg
    obtain ⟨w, rfl⟩ := Sym2.mem_iff_exists.mp hvg
    exact hv (p.fst_mem_support_of_mem_edges hg)
  have hgx : g ≠ s(v, x) := fun h => hvg (h ▸ Sym2.mem_mk_left v x)
  have hgy : g ≠ s(v, y) := fun h => hvg (h ▸ Sym2.mem_mk_left v y)
  rw [Function.update_of_ne hgy, Function.update_of_ne hgx]
  exact hpos g hg

end Corner

/-- the neighbours of a corner of P_3 × P_n are its two neighbours along the edges -/
theorem strip_corner_nbr' {n : ℕ} (hn : 3 ≤ n) {c x y : Fin 3 × Fin n} (hc : isCorner n c)
    (hx : (strip n).Adj c x) (hy : (strip n).Adj c y) (hxy : x ≠ y) : (strip n).neighborFinset c = {x, y} := by
  obtain ⟨r, j⟩ := c
  obtain ⟨hr, hj⟩ := hc
  simp only at hr hj
  have hnb : ∃ j' : Fin n, (strip n).neighborFinset (r, j) = {((1 : Fin 3), j), (r, j')} := by
    rcases hj with hj | hj
    · exact ⟨⟨1, by omega⟩, strip_corner_nbr r j ⟨1, by omega⟩ hr (Or.inl ⟨hj, rfl⟩)⟩
    · refine ⟨⟨n - 2, by omega⟩, strip_corner_nbr r j ⟨n - 2, by omega⟩ hr (Or.inr ⟨hj, ?_⟩)⟩
      show n - 2 + 2 = n
      omega
  obtain ⟨j', hj'⟩ := hnb
  have hsub : ({x, y} : Finset (Fin 3 × Fin n)) ⊆ (strip n).neighborFinset (r, j) := by
    intro z hz
    rw [Finset.mem_insert, Finset.mem_singleton] at hz
    rcases hz with rfl | rfl
    · exact (SimpleGraph.mem_neighborFinset _ _ _).mpr hx
    · exact (SimpleGraph.mem_neighborFinset _ _ _).mpr hy
  refine (Finset.eq_of_subset_of_card_le hsub ?_).symm
  rw [hj', Finset.card_pair hxy]
  exact Finset.card_le_two

/-- **H8 for the paper's coefficients**, every N ≥ 2 (the top theorems use N = 3, 4) -/
theorem hCornerFactor_kConc (N : ℕ) (hN : 2 ≤ N) : hCornerFactor N (kConc N) := by
  intro n hn J hJ0 e he f hf hef hsc
  obtain ⟨c, hc, hce, hcf⟩ := hsc
  obtain ⟨x, rfl⟩ := Sym2.mem_iff_exists.mp hce
  obtain ⟨y, rfl⟩ := Sym2.mem_iff_exists.mp hcf
  have hadjx : (strip n).Adj c x := he
  have hadjy : (strip n).Adj c y := hf
  have hxy : x ≠ y := fun h => hef (by rw [h])
  have hnb := strip_corner_nbr' hn hc hadjx hadjy hxy
  obtain ⟨w, hwc, hxw, hwy⟩ := corner_witness hn hc hadjx hadjy hxy
  have hJF : Ferro (strip n) (uniform J) := fun _ _ => hJ0.le
  have hxw' : x ≠ w := hxw.ne
  have hwy' : w ≠ y := hwy.ne
  set p : (strip n).Walk x y := SimpleGraph.Walk.cons hxw (SimpleGraph.Walk.cons hwy SimpleGraph.Walk.nil) with hpdef
  have hp : p.IsPath := by
    apply SimpleGraph.Walk.IsPath.mk'
    simp [hpdef, hxw', hxy, hwy']
  have hcp : c ∉ p.support := by
    simp [hpdef, hadjx.ne, hadjy.ne, Ne.symm hwc]
  refine ⟨uCorner N (strip n) (uniform J) s(c, x) s(c, y) x y, N,
    uCorner N (strip n) (uniform J) s(c, x) s(c, y) x y 0,
    fun k => uCorner_nonneg hN _ _ hJF hxy k, uCorner_zero_pos hN _ _, ?_, fun k => uCorner_le hN _ _ k,
    fun a b => (corner_factor hN (strip n) (uniform J) hnb hxy a b).tsum_eq.symm⟩
  exact uCorner_one_pos hN _ _ hJF hxy p hp hcp (fun g _ => hJ0)

end G2S3

#print axioms G2S3.corner_factor
#print axioms G2S3.uCorner_nonneg
#print axioms G2S3.uCorner_zero_pos
#print axioms G2S3.uCorner_le
#print axioms G2S3.uCorner_one_pos
#print axioms G2S3.hCornerFactor_kConc
