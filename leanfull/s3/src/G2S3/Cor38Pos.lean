/-
G2S3.Cor38Pos (stage S3, after the freeze): Corollary 3.8's strict covariance on positive paths of any length
(STATEMENTS_S3_v6.md, planned section). The paper's route: Cov(s_e, s_f) = Cov_q(r_c(J_e), r_c(J_f)) (`cor38_cov`), q is a
probability law charging 0 and 1 (`cor38_law`), r_c(J) is strictly increasing in c (Lemma 2.2, `hRatio_kConc`, from an
unchanged copy of G2S2.Ratio), and a strict Chebyshev step: 2 Cov_q(f, g) = Σ_m Σ_n q_m q_n (f_m - f_n)(g_m - g_n), whose
terms are ≥ 0 and whose term (0, 1) is > 0.
-/
import G2S3.Cor38
import G2S2.Ratio

noncomputable section
open MeasureTheory Real

namespace G2S3

open G2Kernel

/-- **Strict Chebyshev** -/
theorem covW_pos (q f g : ℕ → ℝ) (hq : ∀ c, 0 ≤ q c) (hq1 : HasSum q 1) (hf : StrictMono f) (hg : StrictMono g)
    (hsf : Summable (fun c => q c * f c)) (hsg : Summable (fun c => q c * g c))
    (hsfg : Summable (fun c => q c * (f c * g c))) (h0 : 0 < q 0) (h1 : 0 < q 1) : 0 < covW q f g := by
  set F := ∑' c, q c * f c with hF
  set Gs := ∑' c, q c * g c with hG
  set P := ∑' c, q c * (f c * g c) with hP
  have hT : ∀ m n, 0 ≤ (f m - f n) * (g m - g n) := by
    intro m n
    rcases lt_trichotomy m n with h | h | h
    · exact mul_nonneg_of_nonpos_of_nonpos (sub_nonpos.mpr (hf h).le) (sub_nonpos.mpr (hg h).le)
    · rw [h, sub_self, zero_mul]
    · exact mul_nonneg (sub_nonneg.mpr (hf h).le) (sub_nonneg.mpr (hg h).le)
  have hS : ∀ m, HasSum (fun n => q m * q n * ((f m - f n) * (g m - g n)))
      (q m * (f m * g m) - q m * f m * Gs - q m * g m * F + q m * P) := by
    intro m
    have e : ∀ n, q m * q n * ((f m - f n) * (g m - g n))
        = q m * (f m * g m) * q n - q m * f m * (q n * g n) - q m * g m * (q n * f n)
          + q m * (q n * (f n * g n)) := by
      intro n; ring
    simp only [e]
    have h1' : HasSum (fun n => q m * (f m * g m) * q n) (q m * (f m * g m) * 1) := hq1.mul_left _
    have h2' : HasSum (fun n => q m * f m * (q n * g n)) (q m * f m * Gs) := hsg.hasSum.mul_left _
    have h3' : HasSum (fun n => q m * g m * (q n * f n)) (q m * g m * F) := hsf.hasSum.mul_left _
    have h4' : HasSum (fun n => q m * (q n * (f n * g n))) (q m * P) := hsfg.hasSum.mul_left _
    have h := ((h1'.sub h2').sub h3').add h4'
    rw [mul_one] at h
    exact h
  have hSum : HasSum (fun m => q m * (f m * g m) - q m * f m * Gs - q m * g m * F + q m * P)
      (2 * (P - F * Gs)) := by
    have h1' : HasSum (fun m => q m * (f m * g m)) P := hsfg.hasSum
    have h2' : HasSum (fun m => q m * f m * Gs) (F * Gs) := hsf.hasSum.mul_right _
    have h3' : HasSum (fun m => q m * g m * F) (Gs * F) := hsg.hasSum.mul_right _
    have h4' : HasSum (fun m => q m * P) (1 * P) := hq1.mul_right _
    have h := ((h1'.sub h2').sub h3').add h4'
    convert h using 1
    ring
  have hSnn : ∀ m, 0 ≤ q m * (f m * g m) - q m * f m * Gs - q m * g m * F + q m * P :=
    fun m => (hS m).nonneg (fun n => mul_nonneg (mul_nonneg (hq m) (hq n)) (hT m n))
  have hS0 : q 0 * q 1 * ((f 0 - f 1) * (g 0 - g 1))
      ≤ q 0 * (f 0 * g 0) - q 0 * f 0 * Gs - q 0 * g 0 * F + q 0 * P :=
    le_hasSum (hS 0) 1 (fun n _ => mul_nonneg (mul_nonneg (hq 0) (hq n)) (hT 0 n))
  have hpos01 : 0 < q 0 * q 1 * ((f 0 - f 1) * (g 0 - g 1)) := by
    have hf01 : f 0 < f 1 := hf (by norm_num)
    have hg01 : g 0 < g 1 := hg (by norm_num)
    exact mul_pos (mul_pos h0 h1) (mul_pos_of_neg_of_neg (by linarith) (by linarith))
  have hle := le_hasSum hSum 0 (fun m _ => hSnn m)
  have hcov : covW q f g = P - F * Gs := rfl
  rw [hcov]
  linarith

/-- the weights and the coefficients with their first derivatives at two positive couplings -/
theorem summable_corner_box {N : ℕ} {V : Type*} [Fintype V] [DecidableEq V] (hN : 2 ≤ N) (G : SimpleGraph V)
    [DecidableRel G.Adj] (J : Sym2 V → ℝ) (hJ : Ferro G J) {v x y : V} (hxy : x ≠ y) {a b : ℝ} (ha : 0 < a)
    (hb : 0 < b) :
    Summable (fun c => |uCorner N G J s(v, x) s(v, y) x y c| * (|kConc N c a| + |deriv (kConc N c) a|)
      * (|kConc N c b| + |deriv (kConc N c) b|)) := by
  have hlo : 0 < min a b := lt_min ha hb
  have hle : min a b ≤ max a b := min_le_max
  obtain ⟨c0, hc0, hbox⟩ := kConc_box_bound hN hlo hle
  have hhi0 : (0 : ℝ) ≤ max a b / 2 := by have := le_max_left a b; linarith
  set β : ℕ → ℝ := fun n => c0 * ((n : ℝ) + 2) * (max a b / 2) ^ n / (n.factorial : ℝ) with hβ
  have hβ0 : ∀ n, 0 ≤ β n := fun n => by simp only [hβ]; positivity
  have hβs : Summable (fun n : ℕ => ((n : ℝ) + 1) ^ N * β n) := by
    refine Summable.of_nonneg_of_le (fun n => mul_nonneg (by positivity) (hβ0 n)) (fun n => ?_)
      ((summable_poly_pow_div_factorial (N + 1) hhi0).mul_left (2 * c0))
    have hpow : ((n : ℝ) + 1) ^ N * ((n : ℝ) + 2) ≤ 2 * ((n : ℝ) + 1) ^ (N + 1) := by
      rw [pow_succ]
      have h0 : (0 : ℝ) ≤ ((n : ℝ) + 1) ^ N := by positivity
      have hn : (0 : ℝ) ≤ (n : ℝ) := Nat.cast_nonneg n
      nlinarith
    have hA : (0 : ℝ) ≤ c0 * (max a b / 2) ^ n / (n.factorial : ℝ) := by positivity
    calc ((n : ℝ) + 1) ^ N * β n
        = (c0 * (max a b / 2) ^ n / (n.factorial : ℝ)) * (((n : ℝ) + 1) ^ N * ((n : ℝ) + 2)) := by
          simp only [hβ]; ring
      _ ≤ (c0 * (max a b / 2) ^ n / (n.factorial : ℝ)) * (2 * ((n : ℝ) + 1) ^ (N + 1)) :=
          mul_le_mul_of_nonneg_left hpow hA
      _ = 2 * c0 * (((n : ℝ) + 1) ^ (N + 1) * (max a b / 2) ^ n / (n.factorial : ℝ)) := by ring
  have hβs1 : Summable β :=
    Summable.of_nonneg_of_le hβ0 (fun n => le_mul_of_one_le_left (hβ0 n) (one_le_pow₀ (by linarith))) hβs
  set B0 := ∑' n, β n with hB0
  have hβB : ∀ n, β n ≤ B0 := fun n => hβs1.le_tsum n (fun j _ => hβ0 j)
  set u0 := uCorner N G J s(v, x) s(v, y) x y 0 with hu0
  have hu0pos : 0 ≤ u0 := (uCorner_zero_pos hN G J).le
  have hu_abs : ∀ c, |uCorner N G J s(v, x) s(v, y) x y c| ≤ ((c : ℝ) + 1) ^ N * u0 := fun c => by
    rw [abs_of_nonneg (uCorner_nonneg hN G J hJ hxy c)]
    exact uCorner_le hN G J c
  have haI : a ∈ Set.Icc (min a b) (max a b) := ⟨min_le_left a b, le_max_left a b⟩
  have hbI : b ∈ Set.Icc (min a b) (max a b) := ⟨min_le_right a b, le_max_right a b⟩
  refine Summable.of_nonneg_of_le (fun c => by positivity) (fun c => ?_) (hβs.mul_left (u0 * B0))
  have h1 := hu_abs c
  have h2 := hbox c a haI
  have h3 := (hbox c b hbI).trans (hβB c)
  have hu0c : 0 ≤ ((c : ℝ) + 1) ^ N * u0 := mul_nonneg (by positivity) hu0pos
  calc |uCorner N G J s(v, x) s(v, y) x y c| * (|kConc N c a| + |deriv (kConc N c) a|)
        * (|kConc N c b| + |deriv (kConc N c) b|)
      ≤ (((c : ℝ) + 1) ^ N * u0) * β c * B0 :=
        mul_le_mul (mul_le_mul h1 h2 (by positivity) hu0c) h3 (by positivity) (mul_nonneg hu0c (hβ0 c))
    _ = u0 * B0 * (((c : ℝ) + 1) ^ N * β c) := by ring

/-- **Corollary 3.8, the strict covariance** (every N ≥ 2) -/
theorem cor38_cov_pos {N : ℕ} {V : Type} [Fintype V] [DecidableEq V] (hN : 2 ≤ N) (G : SimpleGraph V)
    [DecidableRel G.Adj] (J : Sym2 V → ℝ) (hJ : Ferro G J) {v x y : V} (hnb : G.neighborFinset v = {x, y})
    (hxy : x ≠ y) (hJe : 0 < J s(v, x)) (hJf : 0 < J s(v, y)) (p : G.Walk x y) (hp : p.IsPath)
    (hv : v ∉ p.support) (hpos : ∀ g ∈ p.edges, 0 < J g) :
    0 < gibbsCov N G J (bond s(v, x)) (bond s(v, y)) := by
  obtain ⟨hq0, hq1, hq0pos, hq1pos⟩ := cor38_law hN G J hJ hnb hxy hJe hJf p hp hv hpos
  rw [cor38_cov hN G J hJ hnb hxy hJe hJf]
  have hZpos : 0 < partition N G J := partition_pos (by omega) G J
  have hbox := summable_corner_box (v := v) hN G J hJ hxy hJe hJf
  have hX : ∀ (A B : ℕ → ℝ), (∀ c, |A c| ≤ |kConc N c (J s(v, x))| + |deriv (kConc N c) (J s(v, x))|) →
      (∀ c, |B c| ≤ |kConc N c (J s(v, y))| + |deriv (kConc N c) (J s(v, y))|) →
      Summable (fun c => uCorner N G J s(v, x) s(v, y) x y c * A c * B c / partition N G J) := by
    intro A B hA hB
    have hs : Summable (fun c => uCorner N G J s(v, x) s(v, y) x y c * A c * B c) := by
      refine Summable.of_norm_bounded hbox (fun c => ?_)
      show ‖uCorner N G J s(v, x) s(v, y) x y c * A c * B c‖
        ≤ |uCorner N G J s(v, x) s(v, y) x y c| * (|kConc N c (J s(v, x))| + |deriv (kConc N c) (J s(v, x))|)
          * (|kConc N c (J s(v, y))| + |deriv (kConc N c) (J s(v, y))|)
      rw [Real.norm_eq_abs, abs_mul, abs_mul]
      have h1 : |uCorner N G J s(v, x) s(v, y) x y c| * |A c|
          ≤ |uCorner N G J s(v, x) s(v, y) x y c| * (|kConc N c (J s(v, x))| + |deriv (kConc N c) (J s(v, x))|) :=
        mul_le_mul_of_nonneg_left (hA c) (abs_nonneg _)
      have h2 : 0 ≤ |uCorner N G J s(v, x) s(v, y) x y c|
          * (|kConc N c (J s(v, x))| + |deriv (kConc N c) (J s(v, x))|) :=
        mul_nonneg (abs_nonneg _) (add_nonneg (abs_nonneg _) (abs_nonneg _))
      exact mul_le_mul h1 (hB c) (abs_nonneg _) h2
    exact hs.div_const _
  have hk : ∀ (c : ℕ) (t : ℝ), |kConc N c t| ≤ |kConc N c t| + |deriv (kConc N c) t| :=
    fun c t => le_add_of_nonneg_right (abs_nonneg _)
  have hk' : ∀ (c : ℕ) (t : ℝ), |deriv (kConc N c) t| ≤ |kConc N c t| + |deriv (kConc N c) t| :=
    fun c t => le_add_of_nonneg_left (abs_nonneg _)
  refine covW_pos _ _ _ hq0 hq1 (hRatio_kConc N hN _ hJe) (hRatio_kConc N hN _ hJf) ?_ ?_ ?_ hq0pos hq1pos
  · refine (hX (fun c => deriv (kConc N c) (J s(v, x))) (fun c => kConc N c (J s(v, y)))
      (fun c => hk' c _) (fun c => hk c _)).congr (fun c => ?_)
    unfold qLabel rRate
    have ha := (kConc_pos' hN c hJe).ne'
    field_simp
  · refine (hX (fun c => kConc N c (J s(v, x))) (fun c => deriv (kConc N c) (J s(v, y)))
      (fun c => hk c _) (fun c => hk' c _)).congr (fun c => ?_)
    unfold qLabel rRate
    have hb := (kConc_pos' hN c hJf).ne'
    field_simp
  · refine (hX (fun c => deriv (kConc N c) (J s(v, x))) (fun c => deriv (kConc N c) (J s(v, y)))
      (fun c => hk' c _) (fun c => hk' c _)).congr (fun c => ?_)
    unfold qLabel rRate
    have ha := (kConc_pos' hN c hJe).ne'
    have hb := (kConc_pos' hN c hJf).ne'
    field_simp

/-- **Corollary 3.8 in the paper's form, complete** (N = 3 or N = 4) -/
theorem cor38_full {N : ℕ} {V : Type} [Fintype V] [DecidableEq V] (hN : N = 3 ∨ N = 4) (G : SimpleGraph V)
    [DecidableRel G.Adj] (J : Sym2 V → ℝ) (hJ : Ferro G J) {v x y : V} (hnb : G.neighborFinset v = {x, y})
    (hxy : x ≠ y) (hJe : 0 < J s(v, x)) (hJf : 0 < J s(v, y)) (p : G.Walk x y) (hp : p.IsPath)
    (hv : v ∉ p.support) (hpos : ∀ g ∈ p.edges, 0 < J g) :
    (∀ c, 0 ≤ qLabel N G J v x y c) ∧ HasSum (qLabel N G J v x y) 1 ∧
      0 < qLabel N G J v x y 0 ∧ 0 < qLabel N G J v x y 1 ∧
      gibbsCov N G J (bond s(v, x)) (bond s(v, y))
        = covW (qLabel N G J v x y) (fun c => rRate N c (J s(v, x))) (fun c => rRate N c (J s(v, y))) ∧
      0 < gibbsCov N G J (bond s(v, x)) (bond s(v, y)) := by
  have h2 : 2 ≤ N := by rcases hN with rfl | rfl <;> norm_num
  obtain ⟨a1, a2, a3, a4⟩ := cor38_law h2 G J hJ hnb hxy hJe hJf p hp hv hpos
  exact ⟨a1, a2, a3, a4, cor38_cov h2 G J hJ hnb hxy hJe hJf,
    cor38_cov_pos h2 G J hJ hnb hxy hJe hJf p hp hv hpos⟩

end G2S3

#print axioms G2S3.covW_pos
#print axioms G2S3.summable_corner_box
#print axioms G2S3.cor38_cov_pos
#print axioms G2S3.cor38_full
