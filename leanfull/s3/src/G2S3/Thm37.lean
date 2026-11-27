/-
G2S3.Thm37 (stage S3, Part E5b): Theorem 3.7 (tex l.419) for every N ≥ 2 and its N = 3 form, the cut part of
Theorem 1.2(b) for every N ≥ 2, and Theorem 1.2(b) (tex l.122) at N = 4 (STATEMENTS_S3_v8.md, E5). At a 2-edge cut the
factorization Z(a, b) = Σ_c u_c k_c(a) k_c(b) with u_c ≥ 0 (`cut_factor`) gives the law of the common label
q_c = u_c k_c(J_e) k_c(J_f) / Z (`commonLaw_cut`), and Cov(s_e, s_f) = Cov_q(r_c(J_e), r_c(J_f)) for J_e, J_f > 0
(Proposition 2.1: the package's `covDeriv_thm` with S1's `labelCov_gen`). Chebyshev with Lemma 2.2 (`hRatio_kConc`)
gives Cov ≥ 0, u_1 > 0 on a positive cycle gives Cov > 0, and zero couplings follow by continuity (Lemma 2.4).
-/
import G2S3.LawP
import G2S3.Cor38Pos
import G2S3.Dunlop
import G2Kernel.Proofs.ChebyshevProof

noncomputable section
open MeasureTheory Real

namespace G2S3

open G2Kernel

/-- nonstrict Chebyshev -/
theorem covW_nonneg (q f g : ℕ → ℝ) (hq : ∀ c, 0 ≤ q c) (hq1 : HasSum q 1) (hf : Monotone f) (hg : Monotone g)
    (hsf : Summable (fun c => q c * f c)) (hsg : Summable (fun c => q c * g c))
    (hsfg : Summable (fun c => q c * (f c * g c))) : 0 ≤ covW q f g :=
  chebyshev_thm q f g hq hq1 hf hg hsf hsg hsfg

theorem sym2_exists_mk {W : Type*} (e : Sym2 W) : ∃ x y : W, e = s(x, y) := by
  refine Sym2.ind (fun x y => ?_) e
  exact ⟨x, y, rfl⟩

theorem kConc_nonneg {N : ℕ} (hN : 2 ≤ N) (c : ℕ) {a : ℝ} (ha : 0 ≤ a) : 0 ≤ kConc N c a := by
  unfold kConc
  have hN2 : (2 : ℝ) ≤ (N : ℝ) := by exact_mod_cast hN
  refine mul_nonneg (Real.Gamma_pos_of_pos (by linarith)).le (tsum_nonneg (fun m => ?_))
  have hc0 : (0 : ℝ) ≤ (c : ℝ) := Nat.cast_nonneg c
  have hm0 : (0 : ℝ) ≤ (m : ℝ) := Nat.cast_nonneg m
  have hG : 0 < Real.Gamma ((c : ℝ) + (m : ℝ) + (N : ℝ) / 2) := Real.Gamma_pos_of_pos (by linarith)
  exact div_nonneg (pow_nonneg (by linarith) _) (mul_nonneg (Nat.cast_nonneg _) hG.le)

/-- weights with polynomial growth, against the coefficients and their first derivatives at two positive couplings -/
theorem summable_box {N : ℕ} (hN : 2 ≤ N) (u : ℕ → ℝ) (K : ℕ) (U : ℝ) (hu : ∀ c, |u c| ≤ ((c : ℝ) + 1) ^ K * U)
    {a b : ℝ} (ha : 0 < a) (hb : 0 < b) :
    Summable (fun c => |u c| * (|kConc N c a| + |deriv (kConc N c) a|) * (|kConc N c b| + |deriv (kConc N c) b|)) := by
  have hU : 0 ≤ U := by
    have h0 := hu 0
    rw [Nat.cast_zero, zero_add, one_pow, one_mul] at h0
    exact (abs_nonneg _).trans h0
  have hlo : 0 < min a b := lt_min ha hb
  have hle : min a b ≤ max a b := min_le_max
  obtain ⟨c0, hc0, hbox⟩ := kConc_box_bound hN hlo hle
  have hhi0 : (0 : ℝ) ≤ max a b / 2 := by have := le_max_left a b; linarith
  set β : ℕ → ℝ := fun n => c0 * ((n : ℝ) + 2) * (max a b / 2) ^ n / (n.factorial : ℝ) with hβ
  have hβ0 : ∀ n, 0 ≤ β n := fun n => by simp only [hβ]; positivity
  have hβs : Summable (fun n : ℕ => ((n : ℝ) + 1) ^ K * β n) := by
    refine Summable.of_nonneg_of_le (fun n => mul_nonneg (by positivity) (hβ0 n)) (fun n => ?_)
      ((summable_poly_pow_div_factorial (K + 1) hhi0).mul_left (2 * c0))
    have hpow : ((n : ℝ) + 1) ^ K * ((n : ℝ) + 2) ≤ 2 * ((n : ℝ) + 1) ^ (K + 1) := by
      rw [pow_succ]
      have h0 : (0 : ℝ) ≤ ((n : ℝ) + 1) ^ K := by positivity
      have hn : (0 : ℝ) ≤ (n : ℝ) := Nat.cast_nonneg n
      nlinarith
    have hA : (0 : ℝ) ≤ c0 * (max a b / 2) ^ n / (n.factorial : ℝ) := by positivity
    calc ((n : ℝ) + 1) ^ K * β n
        = (c0 * (max a b / 2) ^ n / (n.factorial : ℝ)) * (((n : ℝ) + 1) ^ K * ((n : ℝ) + 2)) := by
          simp only [hβ]; ring
      _ ≤ (c0 * (max a b / 2) ^ n / (n.factorial : ℝ)) * (2 * ((n : ℝ) + 1) ^ (K + 1)) :=
          mul_le_mul_of_nonneg_left hpow hA
      _ = 2 * c0 * (((n : ℝ) + 1) ^ (K + 1) * (max a b / 2) ^ n / (n.factorial : ℝ)) := by ring
  have hβs1 : Summable β :=
    Summable.of_nonneg_of_le hβ0 (fun n => le_mul_of_one_le_left (hβ0 n) (one_le_pow₀ (by linarith))) hβs
  set B0 := ∑' n, β n with hB0
  have hβB : ∀ n, β n ≤ B0 := fun n => hβs1.le_tsum n (fun j _ => hβ0 j)
  have haI : a ∈ Set.Icc (min a b) (max a b) := ⟨min_le_left a b, le_max_left a b⟩
  have hbI : b ∈ Set.Icc (min a b) (max a b) := ⟨min_le_right a b, le_max_right a b⟩
  refine Summable.of_nonneg_of_le (fun c => by positivity) (fun c => ?_) (hβs.mul_left (U * B0))
  have h1 := hu c
  have h2 := hbox c a haI
  have h3 := (hbox c b hbI).trans (hβB c)
  have hu0c : 0 ≤ ((c : ℝ) + 1) ^ K * U := mul_nonneg (by positivity) hU
  calc |u c| * (|kConc N c a| + |deriv (kConc N c) a|) * (|kConc N c b| + |deriv (kConc N c) b|)
      ≤ (((c : ℝ) + 1) ^ K * U) * β c * B0 :=
        mul_le_mul (mul_le_mul h1 h2 (by positivity) hu0c) h3 (by positivity) (mul_nonneg hu0c (hβ0 c))
    _ = U * B0 * (((c : ℝ) + 1) ^ K * β c) := by ring

theorem summable_q_box {N : ℕ} (hN : 2 ≤ N) (u : ℕ → ℝ) (K : ℕ) (U : ℝ)
    (hu : ∀ c, |u c| ≤ ((c : ℝ) + 1) ^ K * U) {a b : ℝ} (ha : 0 < a) (hb : 0 < b) (Z : ℝ) (A B : ℕ → ℝ)
    (hA : ∀ c, |A c| ≤ |kConc N c a| + |deriv (kConc N c) a|)
    (hB : ∀ c, |B c| ≤ |kConc N c b| + |deriv (kConc N c) b|) :
    Summable (fun c => u c * A c * B c / Z) := by
  have hbox := summable_box hN u K U hu ha hb
  have hs : Summable (fun c => u c * A c * B c) := by
    refine Summable.of_norm_bounded hbox (fun c => ?_)
    show ‖u c * A c * B c‖
      ≤ |u c| * (|kConc N c a| + |deriv (kConc N c) a|) * (|kConc N c b| + |deriv (kConc N c) b|)
    rw [Real.norm_eq_abs, abs_mul, abs_mul]
    have h1 : |u c| * |A c| ≤ |u c| * (|kConc N c a| + |deriv (kConc N c) a|) :=
      mul_le_mul_of_nonneg_left (hA c) (abs_nonneg _)
    have h2 : 0 ≤ |u c| * (|kConc N c a| + |deriv (kConc N c) a|) :=
      mul_nonneg (abs_nonneg _) (add_nonneg (abs_nonneg _) (abs_nonneg _))
    exact mul_le_mul h1 (hB c) (abs_nonneg _) h2
  exact hs.div_const _

section Thm37

variable {N : ℕ} {V : Type} [Fintype V] [DecidableEq V]

/-- **Proposition 2.1 for a single-label factorization**: Cov(s_e, s_f) = Cov_q(r_c(J_e), r_c(J_f)) -/
theorem cov_factor_eq (hN : 2 ≤ N) (G : SimpleGraph V) [DecidableRel G.Adj] (J : Sym2 V → ℝ) {e f : Sym2 V}
    (he : e ∈ G.edgeSet) (hf : f ∈ G.edgeSet) (hef : e ≠ f) (u : ℕ → ℝ) (K : ℕ) (U : ℝ)
    (hu : ∀ c, |u c| ≤ ((c : ℝ) + 1) ^ K * U)
    (hZ : ∀ a b, HasSum (fun c => u c * kConc N c a * kConc N c b)
      (partition N G (Function.update (Function.update J e a) f b)))
    (hJe : 0 < J e) (hJf : 0 < J f) :
    gibbsCov N G J (bond e) (bond f) = covW (fun c => u c * kConc N c (J e) * kConc N c (J f) / partition N G J)
      (fun c => rRate N c (J e)) (fun c => rRate N c (J f)) := by
  have hN0 : 0 < N := by omega
  have hU : 0 ≤ U := by
    have h0 := hu 0
    rw [Nat.cast_zero, zero_add, one_pow, one_mul] at h0
    exact (abs_nonneg _).trans h0
  have hcov := (covDeriv_thm N V G J e f he hf hef).symm
  have hZab : ∀ a b, partition N G (Function.update (Function.update J e a) f b)
      = ∑' c, u c * kConc N c a * kConc N c b := fun a b => (hZ a b).tsum_eq.symm
  have hδ : 0 < min (J e) (J f) / 2 := by positivity
  have hmin1 : min (J e) (J f) ≤ J e := min_le_left _ _
  have hmin2 : min (J e) (J f) ≤ J f := min_le_right _ _
  have hmax1 : J e ≤ max (J e) (J f) := le_max_left _ _
  have hmax2 : J f ≤ max (J e) (J f) := le_max_right _ _
  have hle : min (J e) (J f) / 2 ≤ max (J e) (J f) + min (J e) (J f) / 2 := by linarith
  obtain ⟨c0, hc0, hbox⟩ := kConc_box_bound hN hδ hle
  set δ := min (J e) (J f) / 2 with hδdef
  set hi := max (J e) (J f) + δ with hhidef
  set β : ℕ → ℝ := fun n => c0 * ((n : ℝ) + 2) * (hi / 2) ^ n / (n.factorial : ℝ) with hβ
  have hβ0 : ∀ n, 0 ≤ β n := fun n => by
    simp only [hβ]
    have : (0 : ℝ) ≤ hi / 2 := by linarith
    positivity
  have hβs : Summable (fun n : ℕ => ((n : ℝ) + 1) ^ K * β n) := by
    refine Summable.of_nonneg_of_le (fun n => mul_nonneg (by positivity) (hβ0 n)) (fun n => ?_)
      ((summable_poly_pow_div_factorial (K + 1) (show (0 : ℝ) ≤ hi / 2 by linarith)).mul_left (2 * c0))
    have hpow : ((n : ℝ) + 1) ^ K * ((n : ℝ) + 2) ≤ 2 * ((n : ℝ) + 1) ^ (K + 1) := by
      rw [pow_succ]
      have h0 : (0 : ℝ) ≤ ((n : ℝ) + 1) ^ K := by positivity
      have hn : (0 : ℝ) ≤ (n : ℝ) := Nat.cast_nonneg n
      nlinarith
    have hA : (0 : ℝ) ≤ c0 * (hi / 2) ^ n / (n.factorial : ℝ) := by
      have : (0 : ℝ) ≤ hi / 2 := by linarith
      positivity
    calc ((n : ℝ) + 1) ^ K * β n = (c0 * (hi / 2) ^ n / (n.factorial : ℝ)) * (((n : ℝ) + 1) ^ K * ((n : ℝ) + 2)) := by
          simp only [hβ]; ring
      _ ≤ (c0 * (hi / 2) ^ n / (n.factorial : ℝ)) * (2 * ((n : ℝ) + 1) ^ (K + 1)) :=
          mul_le_mul_of_nonneg_left hpow hA
      _ = 2 * c0 * (((n : ℝ) + 1) ^ (K + 1) * (hi / 2) ^ n / (n.factorial : ℝ)) := by ring
  have hβs1 : Summable β :=
    Summable.of_nonneg_of_le hβ0 (fun n => le_mul_of_one_le_left (hβ0 n) (one_le_pow₀ (by linarith))) hβs
  set B0 := ∑' n, β n with hB0
  have hβB : ∀ n, β n ≤ B0 := fun n => hβs1.le_tsum n (fun j _ => hβ0 j)
  have hAin : ∀ x' ∈ Set.Icc (J e - δ) (J e + δ), x' ∈ Set.Icc δ hi :=
    fun x' hx' => ⟨by linarith [hx'.1], by linarith [hx'.2]⟩
  have hBin : ∀ y' ∈ Set.Icc (J f - δ) (J f + δ), y' ∈ Set.Icc δ hi :=
    fun y' hy' => ⟨by linarith [hy'.1], by linarith [hy'.2]⟩
  have hMs : Summable (fun c : ℕ => ((c : ℝ) + 1) ^ K * U * β c * B0) :=
    (hβs.mul_left (U * B0)).congr (fun c => by ring)
  have hL := labelCov_gen u (fun c => kConc N c) (fun c => kConc N c)
    (J e) (J f) δ (fun c => ((c : ℝ) + 1) ^ K * U * β c * B0) hδ
    (fun c => differentiable_kConc hN c) (fun c => differentiable_kConc hN c) hMs
    (fun c x' hx' y' hy' => by
      have h1 := hu c
      have h2 := hbox c x' (hAin x' hx')
      have h3 := (hbox c y' (hBin y' hy')).trans (hβB c)
      have hβc := hβ0 c
      calc |u c| * (|kConc N c x'| + |deriv (kConc N c) x'|) * (|kConc N c y'| + |deriv (kConc N c) y'|)
          ≤ (((c : ℝ) + 1) ^ K * U) * β c * B0 := by
            refine mul_le_mul (mul_le_mul h1 h2 (by positivity) (by positivity)) h3 (by positivity) (by positivity)
        _ = ((c : ℝ) + 1) ^ K * U * β c * B0 := by ring)
    (fun a _ => by
      show 0 < ∑' c, u c * kConc N c a * kConc N c (J f)
      rw [← hZab a (J f)]
      exact partition_pos hN0 G _)
  rw [hcov]
  simp only [hZab]
  rw [hL]
  have hZ' : (∑' c, u c * kConc N c (J e) * kConc N c (J f)) = partition N G J := by
    rw [← hZab, update_self_self]
  have h1 : ∀ c, u c * kConc N c (J e) * kConc N c (J f) / partition N G J * (rRate N c (J e) * rRate N c (J f))
      = u c * deriv (kConc N c) (J e) * deriv (kConc N c) (J f) / partition N G J := by
    intro c
    unfold rRate
    have ha := (kConc_pos' hN c hJe).ne'
    have hb := (kConc_pos' hN c hJf).ne'
    field_simp
  have h2 : ∀ c, u c * kConc N c (J e) * kConc N c (J f) / partition N G J * rRate N c (J e)
      = u c * deriv (kConc N c) (J e) * kConc N c (J f) / partition N G J := by
    intro c
    unfold rRate
    have ha := (kConc_pos' hN c hJe).ne'
    field_simp
  have h3 : ∀ c, u c * kConc N c (J e) * kConc N c (J f) / partition N G J * rRate N c (J f)
      = u c * kConc N c (J e) * deriv (kConc N c) (J f) / partition N G J := by
    intro c
    unfold rRate
    have hb := (kConc_pos' hN c hJf).ne'
    field_simp
  unfold covW
  simp only [h1, h2, h3, tsum_div_const]
  rw [hZ']
  field_simp

/-- the law of the common label at a cut, in closed form -/
def qCut (N : ℕ) (G : SimpleGraph V) [DecidableRel G.Adj] (J : Sym2 V → ℝ) (x y z w : V) (c : ℕ) : ℝ :=
  uCut N G J x y z w c * kConc N c (J s(x, y)) * kConc N c (J s(z, w)) / partition N G J

theorem cut_law_data (hN : 2 ≤ N) (G : SimpleGraph V) [DecidableRel G.Adj] (J : Sym2 V → ℝ) (hJ : Ferro G J)
    {x y z w : V} {A : Set V} (hS : CutSides G x y z w A) (hJe : 0 < J s(x, y)) (hJf : 0 < J s(z, w)) :
    (∀ c, 0 ≤ qCut N G J x y z w c) ∧ HasSum (qCut N G J x y z w) 1 ∧
      Summable (fun c => qCut N G J x y z w c * rRate N c (J s(x, y))) ∧
      Summable (fun c => qCut N G J x y z w c * rRate N c (J s(z, w))) ∧
      Summable (fun c => qCut N G J x y z w c * (rRate N c (J s(x, y)) * rRate N c (J s(z, w)))) ∧
      gibbsCov N G J (bond s(x, y)) (bond s(z, w))
        = covW (qCut N G J x y z w) (fun c => rRate N c (J s(x, y))) (fun c => rRate N c (J s(z, w))) := by
  have hZ : 0 < partition N G J := partition_pos (by omega) G J
  have hu : ∀ c, |uCut N G J x y z w c| ≤ ((c : ℝ) + 1) ^ (2 * N) * uCut N G J x y z w 0 :=
    fun c => uCut_le hN G J x y z w c
  have hk : ∀ (c : ℕ) (t : ℝ), |kConc N c t| ≤ |kConc N c t| + |deriv (kConc N c) t| :=
    fun c t => le_add_of_nonneg_right (abs_nonneg _)
  have hk' : ∀ (c : ℕ) (t : ℝ), |deriv (kConc N c) t| ≤ |kConc N c t| + |deriv (kConc N c) t| :=
    fun c t => le_add_of_nonneg_left (abs_nonneg _)
  refine ⟨fun c => ?_, ?_, ?_, ?_, ?_, ?_⟩
  · unfold qCut
    exact div_nonneg (mul_nonneg (mul_nonneg (uCut_nonneg hN G J hJ hS c) (kConc_pos' hN c hJe).le)
      (kConc_pos' hN c hJf).le) hZ.le
  · have h := cut_factor hN G J hJ hS (J s(x, y)) (J s(z, w))
    rw [update_self_self] at h
    have h2 := h.div_const (partition N G J)
    rw [div_self hZ.ne'] at h2
    exact h2
  · refine (summable_q_box hN (uCut N G J x y z w) (2 * N) (uCut N G J x y z w 0) hu hJe hJf (partition N G J)
      (fun c => deriv (kConc N c) (J s(x, y))) (fun c => kConc N c (J s(z, w)))
      (fun c => hk' c _) (fun c => hk c _)).congr (fun c => ?_)
    unfold qCut rRate
    have ha := (kConc_pos' hN c hJe).ne'
    field_simp
  · refine (summable_q_box hN (uCut N G J x y z w) (2 * N) (uCut N G J x y z w 0) hu hJe hJf (partition N G J)
      (fun c => kConc N c (J s(x, y))) (fun c => deriv (kConc N c) (J s(z, w)))
      (fun c => hk c _) (fun c => hk' c _)).congr (fun c => ?_)
    unfold qCut rRate
    have hb := (kConc_pos' hN c hJf).ne'
    field_simp
  · refine (summable_q_box hN (uCut N G J x y z w) (2 * N) (uCut N G J x y z w 0) hu hJe hJf (partition N G J)
      (fun c => deriv (kConc N c) (J s(x, y))) (fun c => deriv (kConc N c) (J s(z, w)))
      (fun c => hk' c _) (fun c => hk' c _)).congr (fun c => ?_)
    unfold qCut rRate
    have ha := (kConc_pos' hN c hJe).ne'
    have hb := (kConc_pos' hN c hJf).ne'
    field_simp
  · exact cov_factor_eq hN G J hS.adj_e hS.adj_f hS.ne (uCut N G J x y z w) (2 * N) (uCut N G J x y z w 0) hu
      (fun a b => cut_factor hN G J hJ hS a b) hJe hJf

theorem cut_cov_nonneg_pos (hN : 2 ≤ N) (G : SimpleGraph V) [DecidableRel G.Adj] (J : Sym2 V → ℝ) (hJ : Ferro G J)
    {x y z w : V} {A : Set V} (hS : CutSides G x y z w A) (hJe : 0 < J s(x, y)) (hJf : 0 < J s(z, w)) :
    0 ≤ gibbsCov N G J (bond s(x, y)) (bond s(z, w)) := by
  obtain ⟨hq0, hq1, hsf, hsg, hsfg, hcov⟩ := cut_law_data hN G J hJ hS hJe hJf
  rw [hcov]
  exact covW_nonneg _ _ _ hq0 hq1 (hRatio_kConc N hN _ hJe).monotone (hRatio_kConc N hN _ hJf).monotone hsf hsg hsfg

theorem cut_cov_strict (hN : 2 ≤ N) (G : SimpleGraph V) [DecidableRel G.Adj] (J : Sym2 V → ℝ) (hJ : Ferro G J)
    {x y z w : V} {A : Set V} (hS : CutSides G x y z w A) (hJe : 0 < J s(x, y)) (hJf : 0 < J s(z, w))
    (p : G.Walk x y) (hp : p.IsPath) (hpe : ∀ g ∈ p.edges, g ≠ s(x, y)) (hpos : ∀ g ∈ p.edges, 0 < J g) :
    0 < gibbsCov N G J (bond s(x, y)) (bond s(z, w)) := by
  obtain ⟨hq0, hq1, hsf, hsg, hsfg, hcov⟩ := cut_law_data hN G J hJ hS hJe hJf
  rw [hcov]
  have hZ : 0 < partition N G J := partition_pos (by omega) G J
  refine covW_pos _ _ _ hq0 hq1 (hRatio_kConc N hN _ hJe) (hRatio_kConc N hN _ hJf) hsf hsg hsfg ?_ ?_
  · unfold qCut
    exact div_pos (mul_pos (mul_pos (uCut_zero_pos hN G J x y z w) (kConc_pos' hN 0 hJe)) (kConc_pos' hN 0 hJf)) hZ
  · unfold qCut
    exact div_pos (mul_pos (mul_pos (uCut_one_pos hN G J hJ hS hJf p hp hpe hpos) (kConc_pos' hN 1 hJe))
      (kConc_pos' hN 1 hJf)) hZ

/-- the couplings J + t on e and on f -/
def shiftJ (J : Sym2 V → ℝ) (e f : Sym2 V) (t : ℝ) : Sym2 V → ℝ :=
  Function.update (Function.update J e (J e + t)) f (J f + t)

theorem contAt_int_shift (hN : 1 ≤ N) (G : SimpleGraph V) [DecidableRel G.Adj] (J : Sym2 V → ℝ) {e f : Sym2 V}
    (he : e ∈ G.edgeSet) (hf : f ∈ G.edgeSet) (hef : e ≠ f) {F : Config N V → ℝ} (hF : BddMeas F) :
    ContinuousAt (fun t : ℝ => ∫ σ, F σ * Real.exp (energy G (shiftJ J e f t) σ) ∂(freeMeasure N V)) 0 := by
  have hfm := freeMeasure_isProb (N := N) hN V
  obtain ⟨hFm, C, hC⟩ := hF
  have hJt : ∀ (t : ℝ) (g : Sym2 V), |shiftJ J e f t g| ≤ |J g| + |t| := by
    intro t g
    unfold shiftJ
    by_cases hgf : g = f
    · rw [hgf, Function.update_self]
      exact abs_add_le _ _
    · rw [Function.update_of_ne hgf]
      by_cases hge : g = e
      · rw [hge, Function.update_self]
        exact abs_add_le _ _
      · rw [Function.update_of_ne hge]
        linarith [abs_nonneg t]
  have h1 : ∀ᶠ t in nhds (0 : ℝ), AEStronglyMeasurable
      (fun σ : Config N V => F σ * Real.exp (energy G (shiftJ J e f t) σ)) (freeMeasure N V) :=
    Filter.Eventually.of_forall (fun t => (hFm.mul (measurable_energy (N := N) G (shiftJ J e f t)).exp).aestronglyMeasurable)
  have hball : ∀ᶠ t in nhds (0 : ℝ), |t| ≤ 1 := by
    have hI : Set.Icc (-1 : ℝ) 1 ∈ nhds (0 : ℝ) := Icc_mem_nhds (by norm_num) (by norm_num)
    filter_upwards [hI] with t ht
    exact abs_le.mpr ⟨ht.1, ht.2⟩
  have h2 : ∀ᶠ t in nhds (0 : ℝ), ∀ᵐ σ ∂(freeMeasure N V),
      ‖F σ * Real.exp (energy G (shiftJ J e f t) σ)‖ ≤ C * Real.exp (∑ g ∈ G.edgeFinset, (|J g| + 1)) := by
    refine hball.mono (fun t ht => Filter.Eventually.of_forall (fun σ => ?_))
    rw [Real.norm_eq_abs, abs_mul, abs_of_pos (Real.exp_pos _)]
    have hE : energy G (shiftJ J e f t) σ ≤ ∑ g ∈ G.edgeFinset, (|J g| + 1) := by
      refine (le_abs_self _).trans ((abs_energy_le G _ σ).trans (Finset.sum_le_sum (fun g _ => ?_)))
      linarith [hJt t g]
    have hC0 : 0 ≤ C := (abs_nonneg _).trans (hC σ)
    exact mul_le_mul (hC σ) (Real.exp_le_exp.mpr hE) (Real.exp_pos _).le hC0
  have h3 : Integrable (fun _ : Config N V => C * Real.exp (∑ g ∈ G.edgeFinset, (|J g| + 1))) (freeMeasure N V) :=
    integrable_const _
  have h4 : ∀ᵐ σ ∂(freeMeasure N V),
      ContinuousAt (fun t : ℝ => F σ * Real.exp (energy G (shiftJ J e f t) σ)) 0 := by
    refine Filter.Eventually.of_forall (fun σ => ?_)
    have hfun : (fun t : ℝ => F σ * Real.exp (energy G (shiftJ J e f t) σ))
        = fun t : ℝ => F σ * Real.exp (restEnergy G J e f σ + (J e + t) * bond e σ + (J f + t) * bond f σ) := by
      funext t
      have hE : energy G (shiftJ J e f t) σ = restEnergy G J e f σ + (J e + t) * bond e σ + (J f + t) * bond f σ :=
        energy_update G J he hf hef (J e + t) (J f + t) σ
      rw [hE]
    rw [hfun]
    exact Continuous.continuousAt (by fun_prop)
  exact continuousAt_of_dominated h1 h2 h3 h4

theorem contAt_cov_shift (hN : 1 ≤ N) (G : SimpleGraph V) [DecidableRel G.Adj] (J : Sym2 V → ℝ) {e f : Sym2 V}
    (he : e ∈ G.edgeSet) (hf : f ∈ G.edgeSet) (hef : e ≠ f) :
    ContinuousAt (fun t : ℝ => gibbsCov N G (shiftJ J e f t) (bond e) (bond f)) 0 := by
  have hb1 : BddMeas (fun _ : Config N V => (1 : ℝ)) := ⟨measurable_const, 1, fun _ => by rw [abs_one]⟩
  have hbe : BddMeas (bond (N := N) e) := ⟨measurable_bond e, 1, fun σ => abs_bond_le e σ⟩
  have hbf : BddMeas (bond (N := N) f) := ⟨measurable_bond f, 1, fun σ => abs_bond_le f σ⟩
  have hZc : ContinuousAt (fun t : ℝ => partition N G (shiftJ J e f t)) 0 := by
    have h := contAt_int_shift hN G J he hf hef hb1
    simp only [one_mul] at h
    exact h
  have hZ0 : partition N G (shiftJ J e f 0) ≠ 0 := (partition_pos (by omega) G _).ne'
  have hX : ∀ {F : Config N V → ℝ}, BddMeas F →
      ContinuousAt (fun t : ℝ => gibbsExp N G (shiftJ J e f t) F) 0 := by
    intro F hF
    have h := (contAt_int_shift hN G J he hf hef hF).div hZc hZ0
    exact h
  exact (hX (BddMeas.mul hbe hbf)).sub ((hX hbe).mul (hX hbf))

/-- **zero couplings, by continuity** (Lemma 2.4, last sentence) -/
theorem cut_cov_nonneg_ferro (hN : 2 ≤ N) (G : SimpleGraph V) [DecidableRel G.Adj] (J : Sym2 V → ℝ)
    (hJ : Ferro G J) {x y z w : V} {A : Set V} (hS : CutSides G x y z w A) :
    0 ≤ gibbsCov N G J (bond s(x, y)) (bond s(z, w)) := by
  have he : s(x, y) ∈ G.edgeSet := hS.adj_e
  have hf : s(z, w) ∈ G.edgeSet := hS.adj_f
  have hpos : ∀ t : ℝ, 0 < t → 0 ≤ gibbsCov N G (shiftJ J s(x, y) s(z, w) t) (bond s(x, y)) (bond s(z, w)) := by
    intro t ht
    have hJt : Ferro G (shiftJ J s(x, y) s(z, w) t) := by
      intro g hg
      unfold shiftJ
      by_cases hgf : g = s(z, w)
      · rw [hgf, Function.update_self]
        linarith [hJ _ hf]
      · rw [Function.update_of_ne hgf]
        by_cases hge : g = s(x, y)
        · rw [hge, Function.update_self]
          linarith [hJ _ he]
        · rw [Function.update_of_ne hge]
          exact hJ g hg
    have hJte : 0 < shiftJ J s(x, y) s(z, w) t s(x, y) := by
      unfold shiftJ
      rw [Function.update_of_ne hS.ne, Function.update_self]
      linarith [hJ _ he]
    have hJtf : 0 < shiftJ J s(x, y) s(z, w) t s(z, w) := by
      unfold shiftJ
      rw [Function.update_self]
      linarith [hJ _ hf]
    exact cut_cov_nonneg_pos hN G _ hJt hS hJte hJtf
  have hc := contAt_cov_shift (N := N) (by omega) G J he hf hS.ne
  have hJ0 : shiftJ J s(x, y) s(z, w) 0 = J := by
    unfold shiftJ
    rw [add_zero, add_zero, Function.update_eq_self, Function.update_eq_self]
  have hlim : Filter.Tendsto (fun t : ℝ => gibbsCov N G (shiftJ J s(x, y) s(z, w) t) (bond s(x, y)) (bond s(z, w)))
      (nhdsWithin 0 (Set.Ioi 0)) (nhds (gibbsCov N G (shiftJ J s(x, y) s(z, w) 0) (bond s(x, y)) (bond s(z, w)))) :=
    hc.tendsto.mono_left nhdsWithin_le_nhds
  have hev : ∀ᶠ t in nhdsWithin (0 : ℝ) (Set.Ioi 0),
      0 ≤ gibbsCov N G (shiftJ J s(x, y) s(z, w) t) (bond s(x, y)) (bond s(z, w)) :=
    eventually_nhdsWithin_of_forall (fun t ht => hpos t ht)
  have key := ge_of_tendsto hlim hev
  rw [hJ0] at key
  exact key

/-- the law of the common label at a cut is u_c k_c(J_e) k_c(J_f) / Z -/
theorem commonLaw_cut (hN : 2 ≤ N) (G : SimpleGraph V) [DecidableRel G.Adj] (J : Sym2 V → ℝ) (e f : G.edgeFinset)
    {x y z w : V} (he : (e : Sym2 V) = s(x, y)) (hf : (f : Sym2 V) = s(z, w)) (hef : e ≠ f) (c : ℕ) :
    commonLaw N G J e f c
      = uCut N G J x y z w c * kConc N c (J s(x, y)) * kConc N c (J s(z, w)) / partition N G J := by
  rw [commonLaw_eq hN G J e f hef c, he, hf]
  have hI : (∫ σ, zon N c (bond s(x, y) σ) * zon N c (bond s(z, w) σ) *
      Real.exp (energy G (Function.update (Function.update J s(x, y) 0) s(z, w) 0) σ) ∂(freeMeasure N V))
      = uCut N G J x y z w c := rfl
  rw [hI]
  ring

theorem commonLaw_hasSum_core (hN : 2 ≤ N) (G : SimpleGraph V) [DecidableRel G.Adj] (J : Sym2 V → ℝ)
    (hJ : Ferro G J) (e f : G.edgeFinset) {x y z w : V} {A : Set V} (he : (e : Sym2 V) = s(x, y))
    (hf : (f : Sym2 V) = s(z, w)) (hS : CutSides G x y z w A) : HasSum (commonLaw N G J e f) 1 := by
  have hef : e ≠ f := fun h => hS.ne (by rw [← he, ← hf, h])
  have hZ : 0 < partition N G J := partition_pos (by omega) G J
  have h := cut_factor hN G J hJ hS (J s(x, y)) (J s(z, w))
  rw [update_self_self] at h
  have h2 := h.div_const (partition N G J)
  rw [div_self hZ.ne'] at h2
  refine h2.congr_fun (fun c => ?_)
  exact commonLaw_cut hN G J e f he hf hef c

theorem thm37_core (hN : 2 ≤ N) (G : SimpleGraph V) [DecidableRel G.Adj] (J : Sym2 V → ℝ) (hJ : Ferro G J)
    (e f : G.edgeFinset) {x y z w : V} {A : Set V} (he : (e : Sym2 V) = s(x, y)) (hf : (f : Sym2 V) = s(z, w))
    (hS : CutSides G x y z w A) :
    (∀ c, 0 ≤ commonLaw N G J e f c) ∧ 0 ≤ gibbsCov N G J (bond (e : Sym2 V)) (bond (f : Sym2 V)) ∧
      (0 < J e → 0 < J f → (∃ (u : V) (c : G.Walk u u), c.IsCycle ∧ (e : Sym2 V) ∈ c.edges ∧ (f : Sym2 V) ∈ c.edges ∧
          ∀ g ∈ c.edges, 0 < J g) → 0 < gibbsCov N G J (bond (e : Sym2 V)) (bond (f : Sym2 V))) := by
  have hef : e ≠ f := fun h => hS.ne (by rw [← he, ← hf, h])
  have hZ : 0 < partition N G J := partition_pos (by omega) G J
  have hJe0 : 0 ≤ J s(x, y) := hJ _ hS.adj_e
  have hJf0 : 0 ≤ J s(z, w) := hJ _ hS.adj_f
  refine ⟨fun c => ?_, ?_, fun hJe hJf hcyc => ?_⟩
  · rw [commonLaw_cut hN G J e f he hf hef c]
    exact div_nonneg (mul_nonneg (mul_nonneg (uCut_nonneg hN G J hJ hS c) (kConc_nonneg hN c hJe0))
      (kConc_nonneg hN c hJf0)) hZ.le
  · rw [he, hf]
    exact cut_cov_nonneg_ferro hN G J hJ hS
  · rw [he] at hJe hcyc ⊢
    rw [hf] at hJf hcyc ⊢
    obtain ⟨u, c, hc, hce, -, hcpos⟩ := hcyc
    obtain ⟨p, hp, hpc⟩ := cycle_path c hc hce
    exact cut_cov_strict hN G J hJ hS hJe hJf p hp (fun g hg => (hpc g hg).2) (fun g hg => hcpos g (hpc g hg).1)

end Thm37

/-- the law of the common label at a 2-edge cut is a probability law -/
theorem commonLaw_hasSum {N : ℕ} {V : Type} [Fintype V] [DecidableEq V] (hN : 2 ≤ N) (G : SimpleGraph V)
    [DecidableRel G.Adj] (J : Sym2 V → ℝ) (hJ : Ferro G J) (e f : G.edgeFinset)
    (hcut : IsTwoEdgeCut G (e : Sym2 V) (f : Sym2 V)) : HasSum (commonLaw N G J e f) 1 := by
  obtain ⟨x, y, hexy⟩ := sym2_exists_mk (e : Sym2 V)
  obtain ⟨z, w, hfzw⟩ := sym2_exists_mk (f : Sym2 V)
  have hcut' : IsTwoEdgeCut G s(x, y) s(z, w) := by rw [← hexy, ← hfzw]; exact hcut
  obtain ⟨A, hA | hA⟩ := cut_sides hcut'
  · exact commonLaw_hasSum_core hN G J hJ e f hexy hfzw hA
  · exact commonLaw_hasSum_core hN G J hJ e f hexy (hfzw.trans Sym2.eq_swap) hA

/-- **Theorem 3.7, every N ≥ 2** -/
theorem thm37_all {N : ℕ} {V : Type} [Fintype V] [DecidableEq V] (hN : 2 ≤ N) (G : SimpleGraph V)
    [DecidableRel G.Adj] (J : Sym2 V → ℝ) (hJ : Ferro G J) (e f : G.edgeFinset)
    (hcut : IsTwoEdgeCut G (e : Sym2 V) (f : Sym2 V)) :
    (∀ c, 0 ≤ commonLaw N G J e f c) ∧ 0 ≤ gibbsCov N G J (bond (e : Sym2 V)) (bond (f : Sym2 V)) ∧
      (0 < J e → 0 < J f → (∃ (u : V) (c : G.Walk u u), c.IsCycle ∧ (e : Sym2 V) ∈ c.edges ∧ (f : Sym2 V) ∈ c.edges ∧
          ∀ g ∈ c.edges, 0 < J g) → 0 < gibbsCov N G J (bond (e : Sym2 V)) (bond (f : Sym2 V))) := by
  obtain ⟨x, y, hexy⟩ := sym2_exists_mk (e : Sym2 V)
  obtain ⟨z, w, hfzw⟩ := sym2_exists_mk (f : Sym2 V)
  have hcut' : IsTwoEdgeCut G s(x, y) s(z, w) := by rw [← hexy, ← hfzw]; exact hcut
  obtain ⟨A, hA | hA⟩ := cut_sides hcut'
  · exact thm37_core hN G J hJ e f hexy hfzw hA
  · exact thm37_core hN G J hJ e f hexy (hfzw.trans Sym2.eq_swap) hA

/-- **Theorem 3.7** (tex l.419): N = 3 -/
theorem thm37 {V : Type} [Fintype V] [DecidableEq V] (G : SimpleGraph V) [DecidableRel G.Adj] (J : Sym2 V → ℝ)
    (hJ : Ferro G J) (e f : G.edgeFinset) (hcut : IsTwoEdgeCut G (e : Sym2 V) (f : Sym2 V)) :
    (∀ c, 0 ≤ commonLaw 3 G J e f c) ∧ 0 ≤ gibbsCov 3 G J (bond (e : Sym2 V)) (bond (f : Sym2 V)) ∧
      (0 < J e → 0 < J f → (∃ (u : V) (c : G.Walk u u), c.IsCycle ∧ (e : Sym2 V) ∈ c.edges ∧ (f : Sym2 V) ∈ c.edges ∧
          ∀ g ∈ c.edges, 0 < J g) → 0 < gibbsCov 3 G J (bond (e : Sym2 V)) (bond (f : Sym2 V))) :=
  thm37_all (by norm_num) G J hJ e f hcut

/-- the cut part of Theorem 1.2(b), every N ≥ 2 -/
theorem cut_cov_nonneg {N : ℕ} {V : Type} [Fintype V] [DecidableEq V] (hN : 2 ≤ N) (G : SimpleGraph V)
    [DecidableRel G.Adj] (J : Sym2 V → ℝ) (hJ : Ferro G J) (e f : Sym2 V) (hcut : IsTwoEdgeCut G e f) :
    0 ≤ gibbsCov N G J (bond e) (bond f) := by
  obtain ⟨x, y, rfl⟩ := sym2_exists_mk e
  obtain ⟨z, w, rfl⟩ := sym2_exists_mk f
  obtain ⟨A, hA | hA⟩ := cut_sides hcut
  · exact cut_cov_nonneg_ferro hN G J hJ hA
  · have h := cut_cov_nonneg_ferro hN G J hJ hA
    have hswap : s(w, z) = s(z, w) := Sym2.eq_swap
    rw [hswap] at h
    exact h

/-- **Theorem 1.2(b)** (tex l.122): N = 4, every finite graph -/
theorem thm12b {V : Type} [Fintype V] [DecidableEq V] (G : SimpleGraph V) [DecidableRel G.Adj] (J : Sym2 V → ℝ)
    (hJ : Ferro G J) (e f : Sym2 V) (he : e ∈ G.edgeSet) (hf : f ∈ G.edgeSet) (hef : e ≠ f) :
    ((∃ v, v ∈ e ∧ v ∈ f) ∨ IsTwoEdgeCut G e f) → 0 ≤ gibbsCov 4 G J (bond e) (bond f) := by
  rintro (hv | hcut)
  · exact hShared_holds4 V G J hJ e he f hf hef hv
  · exact cut_cov_nonneg (by norm_num) G J hJ e f hcut

end G2S3

#print axioms G2S3.covW_nonneg
#print axioms G2S3.commonLaw_hasSum
#print axioms G2S3.thm37_all
#print axioms G2S3.thm37
#print axioms G2S3.cut_cov_nonneg
#print axioms G2S3.thm12b
