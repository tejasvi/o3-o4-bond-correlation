/-
G2Kernel.Proofs.CornerFactorProof: proofs of `variance_pos_statement` (M1v), `cornerPair_statement` (M10c) and
`stripD_factor_statement` (M10d). Kernel proof, step L-b.
- M1v: the variance is the series of `p (f - μ)²`, whose terms are nonnegative and positive at a charged point where
  `f` differs from its mean.
- M10c: hCornerFactor writes `Z(a, b)` as a single-label series. With hKReg it is label-regular at `(J, J)`, so
  Proposition 2.1 (`gibbsCov_eq_covW`) makes the corner covariance the variance of `r_c(J)` under the law of the
  common label. The labels 0 and 1 carry positive weight and `r_0(J) < r_1(J)` by hRatio, so M1v gives `Cov > 0`. At
  `N = 0` the partition function vanishes while the series is positive, so the premises cannot hold.
- M10d: Theorem 1.4(ii) (`stripD_thm`) with hCornerPair from M10c.
-/
import G2Kernel.CornerFactor
import G2Kernel.Proofs.AssemblyProof

noncomputable section
open MeasureTheory Real

namespace G2Kernel

theorem variance_pos_thm : variance_pos_statement := by
  unfold variance_pos_statement
  intro p f hp hp1 hpf hpff hex
  obtain ⟨m, n, hm, hn, hmn⟩ := hex
  rw [covW_eq_centered p f f hp1 hpf hpf hpff (∑' k, p k * f k) (∑' k, p k * f k) rfl]
  have hterm : ∀ i, 0 ≤ p i * ((f i - ∑' k, p k * f k) * (f i - ∑' k, p k * f k)) :=
    fun i => mul_nonneg (hp i) (mul_self_nonneg _)
  have hpos : ∃ i, 0 < p i * ((f i - ∑' k, p k * f k) * (f i - ∑' k, p k * f k)) := by
    by_cases hfm : f m = ∑' k, p k * f k
    · have hfn : f n - ∑' k, p k * f k ≠ 0 := sub_ne_zero.mpr (fun h => hmn (hfm.trans h.symm))
      exact ⟨n, mul_pos hn (mul_self_pos.mpr hfn)⟩
    · exact ⟨m, mul_pos hm (mul_self_pos.mpr (sub_ne_zero.mpr hfm))⟩
  obtain ⟨i, hi⟩ := hpos
  exact (summable_centered p f f hp1.summable hpf hpf hpff _ _).tsum_pos hterm i hi

theorem cornerPair_thm (N : ℕ) : cornerPair_statement N := by
  unfold cornerPair_statement hCornerPair
  intro k hK hR hCF n hn J hJ0 _hJ20 e he f hf hef hsc
  obtain ⟨u, K, U, hu0, hu0pos, hu1pos, hub, hZ⟩ := hCF n hn J hJ0 e he f hf hef hsc
  have hreg : LabelRegular u k k J J := labelRegular_of_bounds hK hJ0 hJ0 hu0 hub
  have hkpos : ∀ c, 0 < k c J := fun c => hK.1 c J hJ0
  obtain ⟨s00, s10, -, s11⟩ := labelRegular_summable hreg
  have hS : 0 < ∑' c, u c * k c J * k c J :=
    s00.tsum_pos (fun c => mul_nonneg (mul_nonneg (hu0 c) (hkpos c).le) (hkpos c).le) 0
      (mul_pos (mul_pos hu0pos (hkpos 0)) (hkpos 0))
  have hSne := hS.ne'
  rcases Nat.eq_zero_or_pos N with rfl | hN
  · exfalso
    have hV : Nonempty (Fin 3 × Fin n) := ⟨((0 : Fin 3), ⟨0, by omega⟩)⟩
    have h0 : freeMeasure 0 (Fin 3 × Fin n) = 0 := freeMeasure_zero _
    have hz := hZ J J
    simp only [partition, h0, integral_zero_measure] at hz
    linarith
  have hcov : gibbsCov N (strip n) (uniform J) (bond e) (bond f)
      = covW (fun c => u c * k c J * k c J / ∑' c', u c' * k c' J * k c' J)
          (fun c => deriv (k c) J / k c J) (fun c => deriv (k c) J / k c J) :=
    gibbsCov_eq_covW hN (strip n) (uniform J) he hf hef u k k hZ hreg
  rw [hcov]
  apply variance_pos_thm
  · intro c
    exact div_nonneg (mul_nonneg (mul_nonneg (hu0 c) (hkpos c).le) (hkpos c).le) hS.le
  · have h1 := s00.hasSum.div_const (∑' c', u c' * k c' J * k c' J)
    rwa [div_self hSne] at h1
  · refine (s10.div_const (∑' c', u c' * k c' J * k c' J)).congr fun c => ?_
    have h1 := (hkpos c).ne'
    field
  · refine (s11.div_const (∑' c', u c' * k c' J * k c' J)).congr fun c => ?_
    have h1 := (hkpos c).ne'
    field
  · exact ⟨0, 1, div_pos (mul_pos (mul_pos hu0pos (hkpos 0)) (hkpos 0)) hS,
      div_pos (mul_pos (mul_pos hu1pos (hkpos 1)) (hkpos 1)) hS, ne_of_lt (hR J hJ0 Nat.zero_lt_one)⟩

theorem stripD_factor_thm (N : ℕ) : stripD_factor_statement N := by
  unfold stripD_factor_statement
  intro hN34 hS hW md hId hCert hSp k hK hR hCF n hn J hJ0 hJ20 e he f hf hef
  exact stripD_thm N hN34 hS hW md hId hCert hSp (cornerPair_thm N k hK hR hCF) n hn J hJ0 hJ20 e he f hf hef

end G2Kernel
