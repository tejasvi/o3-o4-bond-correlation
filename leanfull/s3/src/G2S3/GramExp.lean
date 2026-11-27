/-
G2S3.GramExp (stage S3, Part C3): the Gibbs weight against a kernel of positive type, and the strict term of a positive
path (STATEMENTS_S3_v5.md, C3). E^n = Σ over sequences of edges of (Π J) × (a Gram word), so ∫ F(σ_x, σ_y) e^E ≥ 0 by vertex
elimination, and keeping the term of one sequence gives a lower bound. For a path x = v_0, ..., v_r = y,
∫ (σ_x.σ_y) Π_i (σ_{v_i}.σ_{v_{i+1}}) = N^{-r}: integrate out v_1 with ∫ ⟪a,z⟫⟪b,z⟫ ω(dz) = ⟪a,b⟫/N and repeat.
-/
import G2S3.GramElim
import G2S3.Moments

noncomputable section
open MeasureTheory Real

namespace G2S3

open G2Kernel

/-- the second moment of ω: ∫ ⟪a, z⟫ ⟪b, z⟫ = ⟪a, b⟫ / N -/
theorem sphere_inner_inner {N : ℕ} (hN : 0 < N) (a b : Amb N) :
    ∫ z : Sph N, @inner ℝ (Amb N) _ a (z : Amb N) * @inner ℝ (Amb N) _ b (z : Amb N) ∂(omega N)
      = @inner ℝ (Amb N) _ a b / N := by
  have hprob := omega_isProbabilityMeasure N hN
  have hin : ∀ (u w : Amb N), @inner ℝ (Amb N) _ u w = ∑ i, u i * w i := by
    intro u w
    rw [PiLp.inner_apply]
    refine Finset.sum_congr rfl (fun i _ => ?_)
    rw [RCLike.inner_apply, conj_trivial, mul_comm]
  have hexp : ∀ z : Sph N, @inner ℝ (Amb N) _ a (z : Amb N) * @inner ℝ (Amb N) _ b (z : Amb N)
      = ∑ i, ∑ j, a i * b j * ((z : Amb N) i * (z : Amb N) j) := by
    intro z
    rw [hin, hin, Finset.sum_mul_sum]
    refine Finset.sum_congr rfl (fun i _ => Finset.sum_congr rfl (fun j _ => ?_))
    ring
  have hint : ∀ i j : Fin N, Integrable (fun z : Sph N => a i * b j * ((z : Amb N) i * (z : Amb N) j)) (omega N) := by
    intro i j
    refine Integrable.const_mul ?_ _
    refine integrable_of_abs_le ((measurable_coord measurable_id i).mul (measurable_coord measurable_id j)) 1
      (fun z => ?_)
    rw [abs_mul]
    exact mul_le_one₀ (abs_coord_le z i) (abs_nonneg _) (abs_coord_le z j)
  simp only [hexp]
  rw [integral_finsetSum _ (fun i _ => integrable_finset_sum _ (fun j _ => hint i j))]
  simp_rw [integral_finsetSum _ (fun j _ => hint _ j)]
  simp only [integral_const_mul, int_coord_mul hN]
  rw [hin a b, Finset.sum_div]
  refine Finset.sum_congr rfl (fun i _ => ?_)
  rw [Finset.sum_eq_single i (fun j _ hj => by simp [Ne.symm hj]) (fun h => absurd (Finset.mem_univ i) h)]
  simp only [if_true]
  ring

section Exp

variable {N : ℕ} {V : Type*} [Fintype V] [DecidableEq V]

/-- the endpoints of an edge, in the order of a representative -/
def ePair (g : Sym2 V) : V × V := Quot.out g

theorem bond_ePair (g : Sym2 V) (σ : Config N V) : bond g σ = dot (σ (ePair g).1) (σ (ePair g).2) := by
  unfold ePair
  conv_lhs => rw [← Quot.out_eq g]
  rfl

theorem bddF_gw {x y : V} {F : Sph N → Sph N → ℝ} (hF : BddMeas (fun p : Sph N × Sph N => F p.1 p.2))
    (L : List (V × V)) : BddMeas (fun σ : Config N V => F (σ x) (σ y) * gw L σ) := by
  obtain ⟨hFm, C, hC⟩ := hF
  have hFxy0 := hFm.comp ((measurable_pi_apply (X := fun _ : V => Sph N) x).prodMk (measurable_pi_apply y))
  have hFxy : Measurable (fun σ : Config N V => F (σ x) (σ y)) := hFxy0
  exact BddMeas.mul ⟨hFxy, C, fun σ => hC (σ x, σ y)⟩ (gw_bdd L)

theorem energy_pow (G : SimpleGraph V) [DecidableRel G.Adj] (J : Sym2 V → ℝ) (σ : Config N V) (n : ℕ) :
    energy G J σ ^ n = ∑ s : Fin n → G.edgeFinset,
      (∏ k, J (s k)) * gw (List.ofFn fun k => ePair ((s k : G.edgeFinset) : Sym2 V)) σ := by
  have he : energy G J σ = ∑ g : G.edgeFinset, J g * dot (σ (ePair (g : Sym2 V)).1) (σ (ePair (g : Sym2 V)).2) := by
    unfold energy
    rw [← Finset.sum_coe_sort G.edgeFinset]
    refine Finset.sum_congr rfl (fun g _ => ?_)
    rw [bond_ePair]
  rw [he, Fintype.sum_pow]
  refine Finset.sum_congr rfl (fun s _ => ?_)
  rw [gw_ofFn, ← Finset.prod_mul_distrib]

theorem integral_F_energy_pow (hN : 1 ≤ N) (G : SimpleGraph V) [DecidableRel G.Adj] (J : Sym2 V → ℝ) {x y : V}
    {F : Sph N → Sph N → ℝ} (hF : BddMeas (fun p : Sph N × Sph N => F p.1 p.2)) (n : ℕ) :
    ∫ σ, F (σ x) (σ y) * energy G J σ ^ n ∂(freeMeasure N V)
      = ∑ s : Fin n → G.edgeFinset, (∏ k, J (s k)) *
          ∫ σ, F (σ x) (σ y) * gw (List.ofFn fun k => ePair ((s k : G.edgeFinset) : Sym2 V)) σ ∂(freeMeasure N V) := by
  have hprob := omega_isProbabilityMeasure N (by omega)
  haveI : IsProbabilityMeasure (freeMeasure N V) := by unfold freeMeasure; infer_instance
  simp only [energy_pow, Finset.mul_sum]
  rw [integral_finsetSum _ (fun s _ => ((bddF_gw (x := x) (y := y) hF _).integrable).const_mul (∏ k, J (s k)) |>.congr
    (Filter.Eventually.of_forall (fun σ => by ring)))]
  refine Finset.sum_congr rfl (fun s _ => ?_)
  rw [← integral_const_mul]
  congr 1
  funext σ
  ring

theorem hasSum_integral_exp (hN : 1 ≤ N) (G : SimpleGraph V) [DecidableRel G.Adj] (J : Sym2 V → ℝ) {x y : V}
    {F : Sph N → Sph N → ℝ} (hF : BddMeas (fun p : Sph N × Sph N => F p.1 p.2)) :
    HasSum (fun n => ∫ σ, F (σ x) (σ y) * (energy G J σ ^ n / (n.factorial : ℝ)) ∂(freeMeasure N V))
      (∫ σ, F (σ x) (σ y) * Real.exp (energy G J σ) ∂(freeMeasure N V)) := by
  have hprob := omega_isProbabilityMeasure N (by omega)
  haveI : IsProbabilityMeasure (freeMeasure N V) := by unfold freeMeasure; infer_instance
  obtain ⟨hFm, C, hC⟩ := hF
  have hFxy0 := hFm.comp ((measurable_pi_apply (X := fun _ : V => Sph N) x).prodMk (measurable_pi_apply y))
  have hFxy : Measurable (fun σ : Config N V => F (σ x) (σ y)) := hFxy0
  obtain ⟨M, hMb⟩ : ∃ M : ℝ, ∀ σ : Config N V, |energy G J σ| ≤ M := ⟨_, fun σ => abs_energy_le G J σ⟩
  have hB : ∀ (n : ℕ) (σ : Config N V),
      |F (σ x) (σ y) * (energy G J σ ^ n / (n.factorial : ℝ))| ≤ |C| * (M ^ n / (n.factorial : ℝ)) := by
    intro n σ
    have h1 : |F (σ x) (σ y)| ≤ |C| := (hC (σ x, σ y)).trans (le_abs_self C)
    have h2 : |energy G J σ ^ n / (n.factorial : ℝ)| ≤ M ^ n / (n.factorial : ℝ) := by
      rw [abs_div, abs_pow, Nat.abs_cast]
      exact div_le_div_of_nonneg_right (pow_le_pow_left₀ (abs_nonneg _) (hMb σ) n) (Nat.cast_nonneg _)
    rw [abs_mul]
    exact mul_le_mul h1 h2 (abs_nonneg _) (abs_nonneg _)
  have hsum : Summable (fun n : ℕ => |C| * (M ^ n / (n.factorial : ℝ))) :=
    (Real.summable_pow_div_factorial M).mul_left _
  have hmeas : ∀ n : ℕ, AEStronglyMeasurable
      (fun σ : Config N V => F (σ x) (σ y) * (energy G J σ ^ n / (n.factorial : ℝ))) (freeMeasure N V) :=
    fun n => (hFxy.mul (((measurable_energy (N := N) G J).pow_const n).div_const _)).aestronglyMeasurable
  have hlim : ∀ σ : Config N V, HasSum (fun n => F (σ x) (σ y) * (energy G J σ ^ n / (n.factorial : ℝ)))
      (F (σ x) (σ y) * Real.exp (energy G J σ)) := by
    intro σ
    have h := NormedSpace.expSeries_div_hasSum_exp (𝔸 := ℝ) (energy G J σ)
    rw [← Real.exp_eq_exp_ℝ] at h
    exact h.mul_left (F (σ x) (σ y))
  exact hasSum_integral_of_bound _ _ _ hmeas hB hsum hlim

theorem exp_term_nonneg (hN : 1 ≤ N) (G : SimpleGraph V) [DecidableRel G.Adj] (J : Sym2 V → ℝ) (hJ : Ferro G J)
    {x y : V} (hxy : x ≠ y) {F : Sph N → Sph N → ℝ} (hF : BddMeas (fun p : Sph N × Sph N => F p.1 p.2))
    (hpos : PosType F) (n : ℕ) :
    0 ≤ ∫ σ, F (σ x) (σ y) * (energy G J σ ^ n / (n.factorial : ℝ)) ∂(freeMeasure N V) := by
  have e : (fun σ : Config N V => F (σ x) (σ y) * (energy G J σ ^ n / (n.factorial : ℝ)))
      = fun σ => (1 / (n.factorial : ℝ)) * (F (σ x) (σ y) * energy G J σ ^ n) := by
    funext σ; ring
  rw [e, integral_const_mul, integral_F_energy_pow hN G J hF n]
  refine mul_nonneg (by positivity) (Finset.sum_nonneg (fun s _ => mul_nonneg ?_ (gram_pos hN hxy hF hpos _)))
  exact Finset.prod_nonneg (fun k _ => hJ _ (G.mem_edgeFinset.mp (s k).2))

/-- the Gibbs weight against a kernel of positive type -/
theorem gram_exp_pos (hN : 1 ≤ N) (G : SimpleGraph V) [DecidableRel G.Adj] (J : Sym2 V → ℝ) (hJ : Ferro G J)
    {x y : V} (hxy : x ≠ y) {F : Sph N → Sph N → ℝ} (hF : BddMeas (fun p : Sph N × Sph N => F p.1 p.2))
    (hpos : PosType F) : 0 ≤ ∫ σ, F (σ x) (σ y) * Real.exp (energy G J σ) ∂(freeMeasure N V) :=
  (hasSum_integral_exp hN G J hF).nonneg (fun n => exp_term_nonneg hN G J hJ hxy hF hpos n)

/-- the term of one sequence of edges is a lower bound -/
theorem gram_exp_term_le (hN : 1 ≤ N) (G : SimpleGraph V) [DecidableRel G.Adj] (J : Sym2 V → ℝ) (hJ : Ferro G J)
    {x y : V} (hxy : x ≠ y) {F : Sph N → Sph N → ℝ} (hF : BddMeas (fun p : Sph N × Sph N => F p.1 p.2))
    (hpos : PosType F) {r : ℕ} (s0 : Fin r → G.edgeFinset) :
    (∏ k, J (s0 k)) * (∫ σ, F (σ x) (σ y) * gw (List.ofFn fun k => ePair ((s0 k : G.edgeFinset) : Sym2 V)) σ
        ∂(freeMeasure N V)) / (r.factorial : ℝ)
      ≤ ∫ σ, F (σ x) (σ y) * Real.exp (energy G J σ) ∂(freeMeasure N V) := by
  refine le_trans ?_ (le_hasSum (hasSum_integral_exp hN G J hF) r
    (fun n _ => exp_term_nonneg hN G J hJ hxy hF hpos n))
  have e : (fun σ : Config N V => F (σ x) (σ y) * (energy G J σ ^ r / (r.factorial : ℝ)))
      = fun σ => (F (σ x) (σ y) * energy G J σ ^ r) / (r.factorial : ℝ) := by
    funext σ; ring
  rw [e, integral_div, integral_F_energy_pow hN G J hF r]
  refine div_le_div_of_nonneg_right ?_ (by positivity)
  exact Finset.single_le_sum (f := fun s => (∏ k, J (s k)) *
      ∫ σ, F (σ x) (σ y) * gw (List.ofFn fun k => ePair ((s k : G.edgeFinset) : Sym2 V)) σ ∂(freeMeasure N V))
    (fun s _ => mul_nonneg (Finset.prod_nonneg (fun k _ => hJ _ (G.mem_edgeFinset.mp (s k).2)))
      (gram_pos hN hxy hF hpos _)) (Finset.mem_univ s0)

/-- the consecutive pairs of a list of vertices -/
def pathW : List V → List (V × V)
  | a :: b :: l => (a, b) :: pathW (b :: l)
  | _ => []

theorem mem_pathW : ∀ (l : List V) (q : V × V), q ∈ pathW l → q.1 ∈ l ∧ q.2 ∈ l
  | [], q, h => by simp [pathW] at h
  | [a], q, h => by simp [pathW] at h
  | a :: b :: l, q, h => by
      simp only [pathW, List.mem_cons] at h
      rcases h with h | h
      · subst h; simp
      · obtain ⟨h1, h2⟩ := mem_pathW (b :: l) q h
        exact ⟨List.mem_cons_of_mem _ h1, List.mem_cons_of_mem _ h2⟩

theorem gw_update_of_notMem {u : V} (L : List (V × V)) (hL : ∀ q ∈ L, q.1 ≠ u ∧ q.2 ≠ u) (σ : Config N V)
    (z : Sph N) : gw L (Function.update σ u z) = gw L σ := by
  induction L with
  | nil => rfl
  | cons q L ih =>
    rw [gw_cons, gw_cons, ih (fun q' hq' => hL q' (List.mem_cons_of_mem _ hq'))]
    obtain ⟨h1, h2⟩ := hL q List.mem_cons_self
    rw [Function.update_of_ne h1, Function.update_of_ne h2]

/-- **The integral of a path word** -/
theorem path_integral (hN : 0 < N) : ∀ (l : List V) (x y : V), (x :: l).Nodup → (x :: l).getLast? = some y →
    x ≠ y → ∫ σ, dot (σ x) (σ y) * gw (pathW (x :: l)) σ ∂(freeMeasure N V) = (1 / (N : ℝ)) ^ l.length
  | [], x, y, _, hy, hxy => by
      simp only [List.getLast?_singleton, Option.some.injEq] at hy
      exact absurd hy hxy
  | [u], x, y, hnd, hy, hxy => by
      have hprob := omega_isProbabilityMeasure N hN
      simp only [List.getLast?_cons_cons, List.getLast?_singleton, Option.some.injEq] at hy
      subst hy
      have hxu : x ≠ u := by
        intro h; rw [List.nodup_cons] at hnd; exact hnd.1 (by simp [h])
      have e : ∀ σ : Config N V, dot (σ x) (σ u) * gw (pathW [x, u]) σ = dot (σ x) (σ u) * dot (σ x) (σ u) := by
        intro σ; simp [pathW, gw]
      simp only [e]
      have hdm : Measurable (fun p : Sph N × Sph N => dot p.1 p.2) :=
        ((continuous_subtype_val.comp continuous_fst).inner (continuous_subtype_val.comp continuous_snd)).measurable
      rw [integral_two hN hxu (fun s t => dot s t * dot s t) ⟨hdm.mul hdm, 1, fun p => by
        rw [abs_mul]; exact mul_le_one₀ (abs_dot_le _ _) (abs_nonneg _) (abs_dot_le _ _)⟩]
      have hin : ∀ s : Sph N, ∫ t, dot s t * dot s t ∂(omega N) = 1 / (N : ℝ) := by
        intro s
        have h := sphere_inner_inner hN (s : Amb N) (s : Amb N)
        have hs : @inner ℝ (Amb N) _ (s : Amb N) (s : Amb N) = 1 := dot_self s
        rw [hs] at h
        simp only [dot]
        rw [h]
      simp only [hin]
      rw [integral_const]
      simp only [probReal_univ, one_smul, List.length_singleton, pow_one]
  | u :: w :: l, x, y, hnd, hy, hxy => by
      have hprob := omega_isProbabilityMeasure N hN
      haveI : IsProbabilityMeasure (freeMeasure N V) := by unfold freeMeasure; infer_instance
      have hnd1 := List.nodup_cons.mp hnd
      have hnd2 := List.nodup_cons.mp hnd1.2
      have hxu : x ≠ u := fun h => hnd1.1 (by simp [h])
      have hy' : (w :: l).getLast? = some y := by simpa only [List.getLast?_cons_cons] using hy
      have hyrest : y ∈ w :: l := List.mem_of_getLast? hy'
      have huy : u ≠ y := fun h => hnd2.1 (h ▸ hyrest)
      have huw : u ≠ w := fun h => hnd2.1 (by simp [h])
      have hxw_nd : (x :: w :: l).Nodup := by
        rw [List.nodup_cons]
        exact ⟨fun h => hnd1.1 (List.mem_cons_of_mem _ h), hnd2.2⟩
      have hy2 : (x :: w :: l).getLast? = some y := by simpa only [List.getLast?_cons_cons] using hy'
      have IH := path_integral hN (w :: l) x y hxw_nd hy2 hxy
      -- the words
      have hrest : ∀ q ∈ pathW (w :: l), q.1 ≠ u ∧ q.2 ≠ u := by
        intro q hq
        obtain ⟨h1, h2⟩ := mem_pathW (w :: l) q hq
        exact ⟨fun h => hnd2.1 (h ▸ h1), fun h => hnd2.1 (h ▸ h2)⟩
      have hW : ∀ σ : Config N V, gw (pathW (x :: u :: w :: l)) σ
          = dot (σ x) (σ u) * (dot (σ u) (σ w) * gw (pathW (w :: l)) σ) := by
        intro σ; simp only [pathW, gw_cons]
      have hW2 : ∀ σ : Config N V, gw (pathW (x :: w :: l)) σ = dot (σ x) (σ w) * gw (pathW (w :: l)) σ := by
        intro σ; simp only [pathW, gw_cons]
      have hbdd : BddMeas (fun σ : Config N V => dot (σ x) (σ y) * gw (pathW (x :: u :: w :: l)) σ) :=
        BddMeas.mul ⟨measurable_bond (N := N) s(x, y), 1, fun σ => abs_bond_le s(x, y) σ⟩ (gw_bdd _)
      rw [integral_update hN u _ hbdd]
      have hstep : ∀ σ : Config N V, ∫ z, dot ((Function.update σ u z) x) ((Function.update σ u z) y) *
          gw (pathW (x :: u :: w :: l)) (Function.update σ u z) ∂(omega N)
            = (1 / (N : ℝ)) * (dot (σ x) (σ y) * gw (pathW (x :: w :: l)) σ) := by
        intro σ
        simp only [hW, Function.update_of_ne hxu, Function.update_of_ne huy.symm, Function.update_self,
          Function.update_of_ne huw.symm, gw_update_of_notMem _ hrest]
        have e1 : (fun z : Sph N => dot (σ x) (σ y) * (dot (σ x) z * (dot z (σ w) * gw (pathW (w :: l)) σ)))
            = fun z : Sph N => (dot (σ x) (σ y) * gw (pathW (w :: l)) σ) *
                (@inner ℝ (Amb N) _ (σ x : Amb N) (z : Amb N) * @inner ℝ (Amb N) _ (σ w : Amb N) (z : Amb N)) := by
          funext z
          rw [dot_comm z (σ w)]
          simp only [dot]
          ring
        rw [e1, integral_const_mul, sphere_inner_inner hN, hW2]
        simp only [dot]
        ring
      simp only [hstep]
      rw [integral_const_mul, IH]
      simp only [List.length_cons]
      ring

/-- the word of a walk is the product of its bonds -/
theorem walk_gw (G : SimpleGraph V) {u w : V} (p : G.Walk u w) (σ : Config N V) :
    (p.edges.map fun g => bond g σ).prod = gw (pathW p.support) σ := by
  induction p with
  | nil => simp [pathW, gw]
  | cons h p ih =>
    rw [SimpleGraph.Walk.edges_cons, SimpleGraph.Walk.support_cons, List.map_cons, List.prod_cons, ih,
      ← p.cons_tail_support]
    simp only [pathW, gw_cons]
    rfl

/-- **The strict form**: a path from x to y with positive couplings -/
theorem gram_exp_path_pos (hN : 2 ≤ N) (G : SimpleGraph V) [DecidableRel G.Adj] (J : Sym2 V → ℝ) (hJ : Ferro G J)
    {x y : V} (hxy : x ≠ y) (p : G.Walk x y) (hp : p.IsPath) (hpos : ∀ g ∈ p.edges, 0 < J g) :
    0 < ∫ σ, zonal N 1 (σ x) (σ y) * Real.exp (energy G J σ) ∂(freeMeasure N V) := by
  have hN0 : 0 < N := by omega
  have hprob := omega_isProbabilityMeasure N hN0
  haveI : IsProbabilityMeasure (freeMeasure N V) := by unfold freeMeasure; infer_instance
  set r := p.edges.length with hr
  set s0 : Fin r → G.edgeFinset := fun k =>
    ⟨p.edges[(k : ℕ)], G.mem_edgeFinset.mpr (p.edges_subset_edgeSet (List.getElem_mem _))⟩ with hs0
  have hF : BddMeas (fun q : Sph N × Sph N => zonal N 1 q.1 q.2) :=
    ⟨(continuous_zonal N 1).measurable, dConc N 1, fun q => abs_zonal_le hN 1 q.1 q.2⟩
  have hterm := gram_exp_term_le (by omega) G J hJ hxy hF (zonal_posType hN 1) s0
  refine lt_of_lt_of_le ?_ hterm
  have hgw : ∀ σ : Config N V, gw (List.ofFn fun k => ePair ((s0 k : G.edgeFinset) : Sym2 V)) σ
      = gw (pathW p.support) σ := by
    intro σ
    rw [gw_ofFn, ← walk_gw G p σ, ← Fin.prod_univ_fun_getElem p.edges (fun g => bond g σ)]
    refine Finset.prod_congr rfl (fun k _ => ?_)
    rw [bond_ePair]
  have hz1 : ∀ s t : Sph N, zonal N 1 s t = (N : ℝ) * dot s t := by
    intro s t
    simp only [zonal, dConc_one hN, CConc]
  have hint : ∫ σ, zonal N 1 (σ x) (σ y) * gw (List.ofFn fun k => ePair ((s0 k : G.edgeFinset) : Sym2 V)) σ
      ∂(freeMeasure N V) = (N : ℝ) * (1 / (N : ℝ)) ^ p.support.tail.length := by
    simp only [hgw, hz1]
    have e : (fun σ : Config N V => (N : ℝ) * dot (σ x) (σ y) * gw (pathW p.support) σ)
        = fun σ => (N : ℝ) * (dot (σ x) (σ y) * gw (pathW (x :: p.support.tail)) σ) := by
      funext σ
      rw [p.cons_tail_support]
      ring
    rw [e, integral_const_mul]
    congr 1
    refine path_integral hN0 p.support.tail x y (by rw [p.cons_tail_support]; exact hp.support_nodup) ?_ hxy
    rw [p.cons_tail_support, List.getLast?_eq_some_getLast (SimpleGraph.Walk.support_ne_nil p),
      SimpleGraph.Walk.getLast_support]
  rw [hint]
  have hJpos : 0 < ∏ k, J (s0 k) := Finset.prod_pos (fun k _ => hpos _ (List.getElem_mem _))
  have hNpos : (0 : ℝ) < N := by exact_mod_cast hN0
  positivity

end Exp

end G2S3

#print axioms G2S3.sphere_inner_inner
#print axioms G2S3.gram_exp_pos
#print axioms G2S3.gram_exp_term_le
#print axioms G2S3.path_integral
#print axioms G2S3.walk_gw
#print axioms G2S3.gram_exp_path_pos
