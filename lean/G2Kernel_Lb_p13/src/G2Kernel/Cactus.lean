/-
G2Kernel.Cactus (modules M3c and M4b): Theorem 1.1 of the paper "Positive correlation of bond energies in the O(3) and O(4) models" (DOI 10.5281/zenodo.24410344) on cacti, and the second part
of Lemma 2.3: across a cut vertex, the covariance of two edges on one side is the covariance
computed from the edges on that side alone.
A cactus is described by a list of blocks, each a single edge or a cycle, in which every block meets the union of the
earlier blocks in at most one vertex. For a finite graph this is equivalent to the statement that every block of the
graph (every maximal 2-connected subgraph and every bridge) is a cycle or a single edge: list the blocks of each
component in an order in which every block follows the block that contains its attaching cut vertex (for example
breadth-first from any block).
Skeleton (step L-a, v1_4). Not compiled yet.
-/
import G2Kernel.Cycle
import G2Kernel.Blocks

noncomputable section

namespace G2Kernel

/-- A block of a cactus: a single edge, or the cycle through `φ 0, φ 1, …, φ (n - 1)`. -/
inductive CactusBlock (α : Type*) where
  | edge (e : Sym2 α)
  | cycle (n : ℕ) (φ : Fin n → α)

variable {V : Type*}

/-- The graph of the edges of `G` that lie inside `A`. -/
def restrictTo (G : SimpleGraph V) (A : Set V) : SimpleGraph V where
  Adj x y := G.Adj x y ∧ x ∈ A ∧ y ∈ A
  symm := ⟨fun _ _ h => ⟨h.1.symm, h.2.2, h.2.1⟩⟩
  loopless := ⟨fun _ h => G.irrefl h.1⟩

instance (G : SimpleGraph V) [DecidableRel G.Adj] (A : Set V) [DecidablePred (· ∈ A)] :
    DecidableRel (restrictTo G A).Adj :=
  fun x y => inferInstanceAs (Decidable (G.Adj x y ∧ x ∈ A ∧ y ∈ A))

/-- Statement M4b (Lemma 2.3, second part): if `V = A ∪ B` with `A ∩ B = {v}` and every edge lies inside `A` or
inside `B`, then for two edges inside `A` the covariance on `G` equals the covariance on the graph of the edges inside
`A`. Uses hSphereIso. -/
def blockRestrict_statement (N : ℕ) : Prop :=
  hSphereIso N →
  ∀ (V : Type) [Fintype V] [DecidableEq V] (G : SimpleGraph V) [DecidableRel G.Adj] (J : Sym2 V → ℝ)
    (A B : Set V) [DecidablePred (· ∈ A)] (v : V), A ∪ B = Set.univ → A ∩ B = {v} →
    (∀ x y, G.Adj x y → (x ∈ A ∧ y ∈ A) ∨ (x ∈ B ∧ y ∈ B)) →
    ∀ e f : Sym2 V, (∀ x ∈ e, x ∈ A) → (∀ y ∈ f, y ∈ A) →
      gibbsCov N G J (bond e) (bond f) = gibbsCov N (restrictTo G A) J (bond e) (bond f)

namespace CactusBlock

/-- The edges of a block: `{e}`, or the images under `φ` of the edges of the cycle graph `C_n`. -/
def edges : CactusBlock V → Set (Sym2 V)
  | edge e => {e}
  | cycle n φ => Sym2.map φ '' (SimpleGraph.cycleGraph n).edgeSet

/-- The vertices of a block. -/
def verts : CactusBlock V → Set V
  | edge e => {x | x ∈ e}
  | cycle _ φ => Set.range φ

/-- A block of `G`: an edge of `G`, or a cycle of length at least three through distinct vertices whose edges are
edges of `G`. -/
def IsBlockOf (G : SimpleGraph V) : CactusBlock V → Prop
  | edge e => e ∈ G.edgeSet
  | cycle n φ => 3 ≤ n ∧ Function.Injective φ ∧ ∀ a b, (SimpleGraph.cycleGraph n).Adj a b → G.Adj (φ a) (φ b)

end CactusBlock

/-- `L` is a cactus decomposition of `G`: every listed block is a block of `G`, every edge of `G` lies in a listed
block, and every block meets the union of the earlier blocks in at most one vertex. -/
def IsCactusWith (G : SimpleGraph V) (L : List (CactusBlock V)) : Prop :=
  (∀ B ∈ L, B.IsBlockOf G) ∧
  (∀ e ∈ G.edgeSet, ∃ B ∈ L, e ∈ B.edges) ∧
  (∀ (L₁ L₂ : List (CactusBlock V)) (B : CactusBlock V), L = L₁ ++ B :: L₂ →
    ∀ x y, x ∈ B.verts → y ∈ B.verts → (∃ B' ∈ L₁, x ∈ B'.verts) → (∃ B' ∈ L₁, y ∈ B'.verts) → x = y)

/-- Every block of `G` is a cycle or a single edge. -/
def IsCactus (G : SimpleGraph V) : Prop := ∃ L : List (CactusBlock V), IsCactusWith G L

/-- Statement M3c (Theorem 1.1): on a cactus, two distinct edges have nonnegative covariance at all couplings
`J ≥ 0`. Uses hSphereIso, hFH, hKReg, hRatio and hCycleZ. -/
def cactus_statement (N : ℕ) : Prop :=
  hSphereIso N →
  ∀ (k : ℕ → ℝ → ℝ) (d : ℕ → ℝ) (C : ℕ → ℝ → ℝ), hFH N k d C → hKReg k → hRatio k → hCycleZ N k d →
    ∀ (V : Type) [Fintype V] [DecidableEq V] (G : SimpleGraph V) [DecidableRel G.Adj], IsCactus G →
      ∀ J : Sym2 V → ℝ, Ferro G J →
        ∀ e ∈ G.edgeSet, ∀ f ∈ G.edgeSet, e ≠ f → G2pair N G J e f

/-- Statement M3c' (Theorem 1.1, strict part): two distinct edges of one cycle block whose couplings are all positive
have positive covariance; the other couplings need only be nonnegative. -/
def cactus_strict_statement (N : ℕ) : Prop :=
  hSphereIso N →
  ∀ (k : ℕ → ℝ → ℝ) (d : ℕ → ℝ) (C : ℕ → ℝ → ℝ), hFH N k d C → hKReg k → hRatio k → hCycleZ N k d →
    (∀ c, 0 < d c) →
    ∀ (V : Type) [Fintype V] [DecidableEq V] (G : SimpleGraph V) [DecidableRel G.Adj] (L : List (CactusBlock V)),
      IsCactusWith G L → ∀ J : Sym2 V → ℝ, Ferro G J →
      ∀ (n : ℕ) (φ : Fin n → V), CactusBlock.cycle n φ ∈ L →
        (∀ g ∈ (CactusBlock.cycle n φ).edges, 0 < J g) →
        ∀ e ∈ (CactusBlock.cycle n φ).edges, ∀ f ∈ (CactusBlock.cycle n φ).edges, e ≠ f →
          0 < gibbsCov N G J (bond e) (bond f)

end G2Kernel
