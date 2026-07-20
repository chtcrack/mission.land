import Mathlib

/-!
Genuine partial progress toward `erdos_242` (mission 5), NOT a proof of the
locked universal theorem — these two lemmas each cover one residue class only.
Written and kernel-checked locally while attempting the full conjecture; kept
here for the attempt write-up since they are correct, verified constructions.
-/

/-- n even: 4/n = 1/m + 1/(m+1) + 1/(m(m+1)) where n = 2m. -/
theorem erdos_straus_even (m : ℕ) (hm : 2 ≤ m) :
    ∃ x y z : ℕ, 1 ≤ x ∧ x < y ∧ y < z ∧
      (4 / (2 * m : ℕ) : ℚ) = 1 / x + 1 / y + 1 / z := by
  refine ⟨m, m + 1, m * (m + 1), ?_, ?_, ?_, ?_⟩
  · omega
  · omega
  · have : 1 ≤ m := by omega
    nlinarith
  · have hm0 : (m : ℚ) ≠ 0 := by exact_mod_cast (by omega : m ≠ 0)
    have hm1 : (m + 1 : ℚ) ≠ 0 := by positivity
    push_cast
    field_simp
    ring

/-- n ≡ 2 (mod 3), n = 3k+2, k ≥ 1: 4/n = 1/(k+1) + 1/n + 1/(n(k+1)). -/
theorem erdos_straus_mod3 (k : ℕ) (hk : 1 ≤ k) :
    ∃ x y z : ℕ, 1 ≤ x ∧ x < y ∧ y < z ∧
      (4 / (3 * k + 2 : ℕ) : ℚ) = 1 / x + 1 / y + 1 / z := by
  refine ⟨k + 1, 3 * k + 2, (3 * k + 2) * (k + 1), ?_, ?_, ?_, ?_⟩
  · omega
  · omega
  · nlinarith
  · have hk1 : (k + 1 : ℚ) ≠ 0 := by positivity
    have hn0 : (3 * (k : ℚ) + 2) ≠ 0 := by positivity
    push_cast
    field_simp
    ring
