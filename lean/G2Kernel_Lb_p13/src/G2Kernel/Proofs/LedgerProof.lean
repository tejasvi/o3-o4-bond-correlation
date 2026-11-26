/-
G2Kernel.Proofs.LedgerProof: proof of `ledger_statement` (module M8). Kernel proof, step L-b.
Every conjunct is a finite check on the vertices and edges of P_3 × P_3 and the eight elements of `d4`, decided by
kernel reduction of a `Decidable` instance (`decide +kernel`; this adds no axiom, as Axioms.lean shows). The checks
with nested quantifiers are split first so that each kernel evaluation stays small: conjunct (2) by the element of
`d4`, conjunct (3) by the two edges, and conjunct (9) by the reflection. The kernel recursion limit is raised for
this theorem.
-/
import G2Kernel.Ledger

namespace G2Kernel

set_option maxRecDepth 8192 in
set_option maxHeartbeats 0 in
theorem ledger_thm : ledger_statement := by
  unfold ledger_statement
  refine ⟨?c1, ?c2, ?c3, ?c4, ?c5, ?c6, ?c7, ?c8a, ?c8b, ?c9⟩
  case c1 => decide +kernel
  case c2 =>
    intro g hg
    simp only [d4, List.mem_cons, List.not_mem_nil, or_false] at hg
    rcases hg with rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl
    all_goals decide +kernel
  case c3 =>
    intro e he f hf hef
    simp only [edges33, Finset.mem_insert, Finset.mem_singleton] at he hf
    rcases he with rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl <;>
      rcases hf with rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl <;>
      first
        | exact absurd rfl hef
        | decide +kernel
  case c4 => decide +kernel
  case c5 => decide +kernel
  case c6 => decide +kernel
  case c7 => decide +kernel
  case c8a => decide +kernel
  case c8b => decide +kernel
  case c9 =>
    have h1 : ∀ p q : Fin 3 × Fin 3, grid33.Adj p q ↔ grid33.Adj (reflH p) (reflH q) := by
      decide +kernel
    have h2 : ∀ p q : Fin 3 × Fin 3, grid33.Adj p q ↔ grid33.Adj (reflAnti p) (reflAnti q) := by
      decide +kernel
    have h3 : ∀ p q : Fin 3 × Fin 3, grid33.Adj p q ↔ grid33.Adj (reflDiag p) (reflDiag q) := by
      decide +kernel
    exact fun p q => ⟨h1 p q, h2 p q, h3 p q⟩

end G2Kernel
