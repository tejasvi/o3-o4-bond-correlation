/-
G2S3.Cor38 (stage S3, Part C5): Corollary 3.8 at a vertex v of degree two with edges e = vx, f = vy and a positive path
from x to y in G - v of any length (STATEMENTS_S3_v5.md, C5). The law of the common label q_c = u_c k_c(J_e) k_c(J_f) / Z is a
probability law on ℕ, nonnegative, charging 0 and 1 (Part C4), and Cov(s_e, s_f) = Cov_q(r_c(J_e), r_c(J_f)) by the package's
`covDeriv_thm` and S1's `labelCov_gen`. Every N ≥ 2; `cor38_paper` states the paper's N = 3, 4.
-/
import G2S3.CornerFact
import G2S1.Prop21

noncomputable section
open MeasureTheory Real

namespace G2S3

open G2Kernel

section Cor

variable {N : ℕ} {V : Type*} [Fintype V] [DecidableEq V]

/-- the law of the common label of e = vx and f = vy -/
def qLabel (N : ℕ) (G : SimpleGraph V) [DecidableRel G.Adj] (J : Sym2 V → ℝ) (v x y : V) (c : ℕ) : ℝ :=
  uCorner N G J s(v, x) s(v, y) x y c * kConc N c (J s(v, x)) * kConc N c (J s(v, y)) / partition N G J

theorem update_self_self (J : Sym2 V → ℝ) (e f : Sym2 V) :
    Function.update (Function.update J e (J e)) f (J f) = J := by
  rw [Function.update_eq_self, Function.update_eq_self]

theorem corner_hasSum_Z (hN : 2 ≤ N) (G : SimpleGraph V) [DecidableRel G.Adj] (J : Sym2 V → ℝ) {v x y : V}
    (hnb : G.neighborFinset v = {x, y}) (hxy : x ≠ y) :
    HasSum (fun c => uCorner N G J s(v, x) s(v, y) x y c * kConc N c (J s(v, x)) * kConc N c (J s(v, y)))
      (partition N G J) := by
  have h := corner_factor hN G J hnb hxy (J s(v, x)) (J s(v, y))
  have hJJ : Function.update (Function.update J s(v, x) (J s(v, x))) s(v, y) (J s(v, y)) = J := by
    rw [Function.update_eq_self, Function.update_eq_self]
  rw [hJJ] at h
  exact h

theorem kConc_pos' (hN : 2 ≤ N) (c : ℕ) {a : ℝ} (ha : 0 < a) : 0 < kConc N c a := (hKReg_kConc N hN).1 c a ha

/-- **Corollary 3.8, the law of the common label** (every N ≥ 2) -/
theorem cor38_law (hN : 2 ≤ N) (G : SimpleGraph V) [DecidableRel G.Adj] (J : Sym2 V → ℝ) (hJ : Ferro G J)
    {v x y : V} (hnb : G.neighborFinset v = {x, y}) (hxy : x ≠ y) (hJe : 0 < J s(v, x)) (hJf : 0 < J s(v, y))
    (p : G.Walk x y) (hp : p.IsPath) (hv : v ∉ p.support) (hpos : ∀ g ∈ p.edges, 0 < J g) :
    (∀ c, 0 ≤ qLabel N G J v x y c) ∧ HasSum (qLabel N G J v x y) 1 ∧
      0 < qLabel N G J v x y 0 ∧ 0 < qLabel N G J v x y 1 := by
  have hZ : 0 < partition N G J := partition_pos (by omega) G J
  refine ⟨fun c => ?_, ?_, ?_, ?_⟩
  · unfold qLabel
    exact div_nonneg (mul_nonneg (mul_nonneg (uCorner_nonneg hN G J hJ hxy c) (kConc_pos' hN c hJe).le)
      (kConc_pos' hN c hJf).le) hZ.le
  · have h := (corner_hasSum_Z hN G J hnb hxy).div_const (partition N G J)
    rw [div_self hZ.ne'] at h
    exact h
  · unfold qLabel
    exact div_pos (mul_pos (mul_pos (uCorner_zero_pos hN G J) (kConc_pos' hN 0 hJe)) (kConc_pos' hN 0 hJf)) hZ
  · unfold qLabel
    exact div_pos (mul_pos (mul_pos (uCorner_one_pos hN G J hJ hxy p hp hv hpos) (kConc_pos' hN 1 hJe))
      (kConc_pos' hN 1 hJf)) hZ

end Cor

/-- **Corollary 3.8, the covariance identity** -/
theorem cor38_cov {N : ℕ} {V : Type} [Fintype V] [DecidableEq V] (hN : 2 ≤ N) (G : SimpleGraph V)
    [DecidableRel G.Adj] (J : Sym2 V → ℝ) (hJ : Ferro G J) {v x y : V} (hnb : G.neighborFinset v = {x, y})
    (hxy : x ≠ y) (hJe : 0 < J s(v, x)) (hJf : 0 < J s(v, y)) :
    gibbsCov N G J (bond s(v, x)) (bond s(v, y))
      = covW (qLabel N G J v x y) (fun c => rRate N c (J s(v, x))) (fun c => rRate N c (J s(v, y))) := by
  have hN0 : 0 < N := by omega
  have hvx : G.Adj v x := (G.mem_neighborFinset v x).mp (by rw [hnb]; simp)
  have hvy : G.Adj v y := (G.mem_neighborFinset v y).mp (by rw [hnb]; simp)
  have hef : s(v, x) ≠ s(v, y) := fun h => hxy (Sym2.congr_right.mp h)
  have hcov := (covDeriv_thm N V G J s(v, x) s(v, y) hvx hvy hef).symm
  have hZab : ∀ a b, partition N G (Function.update (Function.update J s(v, x) a) s(v, y) b)
      = ∑' c, uCorner N G J s(v, x) s(v, y) x y c * kConc N c a * kConc N c b :=
    fun a b => (corner_factor hN G J hnb hxy a b).tsum_eq.symm
  -- the box around (J_e, J_f)
  have hδ : 0 < min (J s(v, x)) (J s(v, y)) / 2 := by positivity
  have hmin1 : min (J s(v, x)) (J s(v, y)) ≤ J s(v, x) := min_le_left _ _
  have hmin2 : min (J s(v, x)) (J s(v, y)) ≤ J s(v, y) := min_le_right _ _
  have hmax1 : J s(v, x) ≤ max (J s(v, x)) (J s(v, y)) := le_max_left _ _
  have hmax2 : J s(v, y) ≤ max (J s(v, x)) (J s(v, y)) := le_max_right _ _
  have hle : min (J s(v, x)) (J s(v, y)) / 2 ≤ max (J s(v, x)) (J s(v, y)) + min (J s(v, x)) (J s(v, y)) / 2 := by
    linarith
  have hhi : 0 ≤ max (J s(v, x)) (J s(v, y)) + min (J s(v, x)) (J s(v, y)) / 2 := by linarith
  obtain ⟨c0, hc0, hbox⟩ := kConc_box_bound hN hδ hle
  set δ := min (J s(v, x)) (J s(v, y)) / 2 with hδdef
  set hi := max (J s(v, x)) (J s(v, y)) + δ with hhidef
  set β : ℕ → ℝ := fun n => c0 * ((n : ℝ) + 2) * (hi / 2) ^ n / (n.factorial : ℝ) with hβ
  have hβ0 : ∀ n, 0 ≤ β n := fun n => by
    simp only [hβ]
    have : (0 : ℝ) ≤ hi / 2 := by linarith
    positivity
  have hβs : Summable (fun n : ℕ => ((n : ℝ) + 1) ^ N * β n) := by
    refine Summable.of_nonneg_of_le (fun n => mul_nonneg (by positivity) (hβ0 n)) (fun n => ?_)
      ((summable_poly_pow_div_factorial (N + 1) (show (0 : ℝ) ≤ hi / 2 by linarith)).mul_left (2 * c0))
    have hpow : ((n : ℝ) + 1) ^ N * ((n : ℝ) + 2) ≤ 2 * ((n : ℝ) + 1) ^ (N + 1) := by
      rw [pow_succ]
      have h0 : (0 : ℝ) ≤ ((n : ℝ) + 1) ^ N := by positivity
      have hn : (0 : ℝ) ≤ (n : ℝ) := Nat.cast_nonneg n
      nlinarith
    have hA : (0 : ℝ) ≤ c0 * (hi / 2) ^ n / (n.factorial : ℝ) := by
      have : (0 : ℝ) ≤ hi / 2 := by linarith
      positivity
    calc ((n : ℝ) + 1) ^ N * β n = (c0 * (hi / 2) ^ n / (n.factorial : ℝ)) * (((n : ℝ) + 1) ^ N * ((n : ℝ) + 2)) := by
          simp only [hβ]; ring
      _ ≤ (c0 * (hi / 2) ^ n / (n.factorial : ℝ)) * (2 * ((n : ℝ) + 1) ^ (N + 1)) :=
          mul_le_mul_of_nonneg_left hpow hA
      _ = 2 * c0 * (((n : ℝ) + 1) ^ (N + 1) * (hi / 2) ^ n / (n.factorial : ℝ)) := by ring
  have hβs1 : Summable β :=
    Summable.of_nonneg_of_le hβ0 (fun n => le_mul_of_one_le_left (hβ0 n) (one_le_pow₀ (by linarith))) hβs
  set B0 := ∑' n, β n with hB0
  have hβB : ∀ n, β n ≤ B0 := fun n => hβs1.le_tsum n (fun j _ => hβ0 j)
  set u0 := uCorner N G J s(v, x) s(v, y) x y 0 with hu0
  have hu0pos : 0 ≤ u0 := (uCorner_zero_pos hN G J).le
  have hu_abs : ∀ c, |uCorner N G J s(v, x) s(v, y) x y c| ≤ ((c : ℝ) + 1) ^ N * u0 := fun c => by
    rw [abs_of_nonneg (uCorner_nonneg hN G J hJ hxy c)]
    exact uCorner_le hN G J c
  have hAin : ∀ x' ∈ Set.Icc (J s(v, x) - δ) (J s(v, x) + δ), x' ∈ Set.Icc δ hi :=
    fun x' hx' => ⟨by linarith [hx'.1], by linarith [hx'.2]⟩
  have hBin : ∀ y' ∈ Set.Icc (J s(v, y) - δ) (J s(v, y) + δ), y' ∈ Set.Icc δ hi :=
    fun y' hy' => ⟨by linarith [hy'.1], by linarith [hy'.2]⟩
  have hMs : Summable (fun c : ℕ => ((c : ℝ) + 1) ^ N * u0 * β c * B0) :=
    (hβs.mul_left (u0 * B0)).congr (fun c => by ring)
  have hL := labelCov_gen (uCorner N G J s(v, x) s(v, y) x y) (fun c => kConc N c) (fun c => kConc N c)
    (J s(v, x)) (J s(v, y)) δ (fun c => ((c : ℝ) + 1) ^ N * u0 * β c * B0) hδ
    (fun c => differentiable_kConc hN c) (fun c => differentiable_kConc hN c) hMs
    (fun c x' hx' y' hy' => by
      have h1 := hu_abs c
      have h2 := hbox c x' (hAin x' hx')
      have h3 := (hbox c y' (hBin y' hy')).trans (hβB c)
      have hβc := hβ0 c
      calc |uCorner N G J s(v, x) s(v, y) x y c| * (|kConc N c x'| + |deriv (kConc N c) x'|)
            * (|kConc N c y'| + |deriv (kConc N c) y'|)
          ≤ (((c : ℝ) + 1) ^ N * u0) * β c * B0 := by
            refine mul_le_mul (mul_le_mul h1 h2 (by positivity) (by positivity)) h3 (by positivity) (by positivity)
        _ = ((c : ℝ) + 1) ^ N * u0 * β c * B0 := by ring)
    (fun a _ => by
      show 0 < ∑' c, uCorner N G J s(v, x) s(v, y) x y c * kConc N c a * kConc N c (J s(v, y))
      rw [← hZab a (J s(v, y))]
      exact partition_pos hN0 G _)
  rw [hcov]
  simp only [hZab]
  rw [hL]
  -- the algebra of Cov_q
  have hZ : (∑' c, uCorner N G J s(v, x) s(v, y) x y c * kConc N c (J s(v, x)) * kConc N c (J s(v, y)))
      = partition N G J := by
    rw [← hZab, update_self_self]
  have hZpos : 0 < partition N G J := partition_pos hN0 G J
  have h1 : ∀ c, qLabel N G J v x y c * (rRate N c (J s(v, x)) * rRate N c (J s(v, y)))
      = uCorner N G J s(v, x) s(v, y) x y c * deriv (kConc N c) (J s(v, x)) * deriv (kConc N c) (J s(v, y))
          / partition N G J := by
    intro c
    unfold qLabel rRate
    have ha := (kConc_pos' hN c hJe).ne'
    have hb := (kConc_pos' hN c hJf).ne'
    field_simp
  have h2 : ∀ c, qLabel N G J v x y c * rRate N c (J s(v, x))
      = uCorner N G J s(v, x) s(v, y) x y c * deriv (kConc N c) (J s(v, x)) * kConc N c (J s(v, y))
          / partition N G J := by
    intro c
    unfold qLabel rRate
    have ha := (kConc_pos' hN c hJe).ne'
    field_simp
  have h3 : ∀ c, qLabel N G J v x y c * rRate N c (J s(v, y))
      = uCorner N G J s(v, x) s(v, y) x y c * kConc N c (J s(v, x)) * deriv (kConc N c) (J s(v, y))
          / partition N G J := by
    intro c
    unfold qLabel rRate
    have hb := (kConc_pos' hN c hJf).ne'
    field_simp
  unfold covW
  simp only [h1, h2, h3, tsum_div_const]
  rw [hZ]
  field_simp

/-- **Corollary 3.8 in the paper's form**: N = 3 or N = 4 -/
theorem cor38_paper {N : ℕ} {V : Type} [Fintype V] [DecidableEq V] (hN : N = 3 ∨ N = 4) (G : SimpleGraph V)
    [DecidableRel G.Adj] (J : Sym2 V → ℝ) (hJ : Ferro G J) {v x y : V} (hnb : G.neighborFinset v = {x, y})
    (hxy : x ≠ y) (hJe : 0 < J s(v, x)) (hJf : 0 < J s(v, y)) (p : G.Walk x y) (hp : p.IsPath)
    (hv : v ∉ p.support) (hpos : ∀ g ∈ p.edges, 0 < J g) :
    (∀ c, 0 ≤ qLabel N G J v x y c) ∧ HasSum (qLabel N G J v x y) 1 ∧
      0 < qLabel N G J v x y 0 ∧ 0 < qLabel N G J v x y 1 ∧
      gibbsCov N G J (bond s(v, x)) (bond s(v, y))
        = covW (qLabel N G J v x y) (fun c => rRate N c (J s(v, x))) (fun c => rRate N c (J s(v, y))) := by
  have h2 : 2 ≤ N := by rcases hN with rfl | rfl <;> norm_num
  obtain ⟨a1, a2, a3, a4⟩ := cor38_law h2 G J hJ hnb hxy hJe hJf p hp hv hpos
  exact ⟨a1, a2, a3, a4, cor38_cov h2 G J hJ hnb hxy hJe hJf⟩

end G2S3

#print axioms G2S3.cor38_law
#print axioms G2S3.cor38_cov
#print axioms G2S3.cor38_paper
