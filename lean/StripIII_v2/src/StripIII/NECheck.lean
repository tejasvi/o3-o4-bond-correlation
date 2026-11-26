/-
StripIII.NECheck: NE's certified record read against
Core's class cNE, by decide. No Mathlib. The record, code/pk22/w1/rc_cert/out/ne_rc_record_cert_kt_s8h_rcc_v1_5.kv (sha8 8ff64462), states
its coverage as class keys: FLIP/SAME ('H2', dL, dR, kind), ('Hinf', dL, 'inf', kind) and ('H1', dL, 'far', kind) with dL, dR in DN;
MIXED ('M2', 'HV', iH, dV, kind), ('Minf' or 'M1', 'HV', iH, 'inf' or 'far', kind) and ('Minf' or 'M1', 'VH', dV, 'inf' or 'far', kind) with
iH in NEAR_H and dV in NEAR_V. Each class covers every offset m (the rows m < m0 with n >= 5 and the top-mode form from m0 on), with the
bottom row as the parity mirror and the left-right mirror images. Its pair map gives the class keys of the 58 separated pairs of P_3 x P_5.
`keysOf N s` gives the record's keys of a shape, in the convention of the pair map. For two horizontal edges, dL = gl and dR = gr (the end
gaps, 0 at an end column), and the kind is same or flip as in Core. For a horizontal and a vertical edge, iH is the horizontal edge's end
gap and dV the vertical edge's end gap minus 1; the kind is same when the vertical edge meets the horizontal edge's row (a with t, b with
bb), else flip. A gap is near up to max DN (FLIP/SAME), T_M (iH) or T_M - 1 (dV), and far from there on. Checks, at N = 3 and N = 4:
(1) on the record's 58 separated pairs of n = 5, `keysOf` gives exactly the keys that the record lists; (2) these 58 pairs are the pairs of
cNE N 5, each unordered pair once; (3) `neRec_all`: every shape of class NE has a key, and every key it has is one of the record's class
keys (over the capped shapes by decide, then for every shape through the cap, as Core's coverage does). The record's lists below are made
by the converter nerec2lean_v1_1.py.
-/
import StripIII.Core

namespace G2Kernel.StripIII

/-- the record's kinds: FLIP/SAME classes by the rows of their two horizontal edges; MIXED classes by whether the vertical edge meets the
horizontal edge's row (same) or not (flip) -/
inductive RK where
  | flip | same
  deriving DecidableEq, Repr

/-- the record's class keys -/
inductive NEKey where
  | H2 (dL dR : Nat) (k : RK)
  | Hinf (d : Nat) (k : RK)
  | H1 (d : Nat) (k : RK)
  | M2 (iH : Nat) (dV : Int) (k : RK)
  | MinfHV (iH : Nat) (k : RK)
  | M1HV (iH : Nat) (k : RK)
  | MinfVH (dV : Int) (k : RK)
  | M1VH (dV : Int) (k : RK)
  deriving DecidableEq, Repr

-- source code/pk22/w1/rc_cert/out/ne_rc_record_cert_kt_s8h_rcc_v1_5.kv sha256 8ff64462ecac399475aec6c3c3c1ace63d88f800b11156ef163b91871bd17680; kt_s8h_rcc_v1_5:e42435489ed535ba049c0d9ceb325cc8d98b01ad7e9c97ef17cbb66be48636ce
-- C-COVER-LIST N=4: 87 class keys (DN {'flip': (0, 1, 2), 'same': (0, 1)}, NEAR_H (0, 1, 2, 3), NEAR_V (-1, 0, 1, 2), T_M 3, DF {'flip': 3, 'same': 2}, DF_V 3, DF_H 4, MM 16), each with an m0 on every piece of [61, 904): short none -> PASS
def recKeys4 : List NEKey := [
  .H2 0 0 .flip,
  .H2 0 1 .flip,
  .H2 0 2 .flip,
  .Hinf 0 .flip,
  .H1 0 .flip,
  .H2 1 0 .flip,
  .H2 1 1 .flip,
  .H2 1 2 .flip,
  .Hinf 1 .flip,
  .H1 1 .flip,
  .H2 2 0 .flip,
  .H2 2 1 .flip,
  .H2 2 2 .flip,
  .Hinf 2 .flip,
  .H1 2 .flip,
  .H2 0 0 .same,
  .H2 0 1 .same,
  .Hinf 0 .same,
  .H1 0 .same,
  .H2 1 0 .same,
  .H2 1 1 .same,
  .Hinf 1 .same,
  .H1 1 .same,
  .M2 0 (-1) .same,
  .M2 0 0 .same,
  .M2 0 1 .same,
  .M2 0 2 .same,
  .MinfHV 0 .same,
  .M1HV 0 .same,
  .M2 1 (-1) .same,
  .M2 1 0 .same,
  .M2 1 1 .same,
  .M2 1 2 .same,
  .MinfHV 1 .same,
  .M1HV 1 .same,
  .M2 2 (-1) .same,
  .M2 2 0 .same,
  .M2 2 1 .same,
  .M2 2 2 .same,
  .MinfHV 2 .same,
  .M1HV 2 .same,
  .M2 3 (-1) .same,
  .M2 3 0 .same,
  .M2 3 1 .same,
  .M2 3 2 .same,
  .MinfHV 3 .same,
  .M1HV 3 .same,
  .MinfVH (-1) .same,
  .M1VH (-1) .same,
  .MinfVH 0 .same,
  .M1VH 0 .same,
  .MinfVH 1 .same,
  .M1VH 1 .same,
  .MinfVH 2 .same,
  .M1VH 2 .same,
  .M2 0 (-1) .flip,
  .M2 0 0 .flip,
  .M2 0 1 .flip,
  .M2 0 2 .flip,
  .MinfHV 0 .flip,
  .M1HV 0 .flip,
  .M2 1 (-1) .flip,
  .M2 1 0 .flip,
  .M2 1 1 .flip,
  .M2 1 2 .flip,
  .MinfHV 1 .flip,
  .M1HV 1 .flip,
  .M2 2 (-1) .flip,
  .M2 2 0 .flip,
  .M2 2 1 .flip,
  .M2 2 2 .flip,
  .MinfHV 2 .flip,
  .M1HV 2 .flip,
  .M2 3 (-1) .flip,
  .M2 3 0 .flip,
  .M2 3 1 .flip,
  .M2 3 2 .flip,
  .MinfHV 3 .flip,
  .M1HV 3 .flip,
  .MinfVH (-1) .flip,
  .M1VH (-1) .flip,
  .MinfVH 0 .flip,
  .M1VH 0 .flip,
  .MinfVH 1 .flip,
  .M1VH 1 .flip,
  .MinfVH 2 .flip,
  .M1VH 2 .flip
]
-- C-PAIRMAP N=4: 80 pairs, 58 separated with an n = 5 class (each class with a row), 22 joint; pairs without an image or a row none -> PASS
def pairMap4 : List (ECode × ECode × List NEKey) := [
  (.ver 0 0, .hor 2 1, [.M2 2 (-1) .flip]),
  (.ver 0 4, .hor 2 2, [.M2 2 (-1) .flip]),
  (.ver 1 0, .hor 0 1, [.M2 2 (-1) .flip]),
  (.ver 1 4, .hor 0 2, [.M2 2 (-1) .flip]),
  (.ver 0 0, .hor 2 2, [.M2 1 (-1) .flip]),
  (.ver 0 4, .hor 2 1, [.M2 1 (-1) .flip]),
  (.ver 1 0, .hor 0 2, [.M2 1 (-1) .flip]),
  (.ver 1 4, .hor 0 1, [.M2 1 (-1) .flip]),
  (.ver 0 0, .hor 2 3, [.M2 0 (-1) .flip]),
  (.ver 0 4, .hor 2 0, [.M2 0 (-1) .flip]),
  (.ver 1 0, .hor 0 3, [.M2 0 (-1) .flip]),
  (.ver 1 4, .hor 0 0, [.M2 0 (-1) .flip]),
  (.ver 0 0, .hor 0 1, [.M2 2 (-1) .same]),
  (.ver 0 4, .hor 0 2, [.M2 2 (-1) .same]),
  (.ver 1 0, .hor 2 1, [.M2 2 (-1) .same]),
  (.ver 1 4, .hor 2 2, [.M2 2 (-1) .same]),
  (.ver 0 0, .hor 0 2, [.M2 1 (-1) .same]),
  (.ver 0 4, .hor 0 1, [.M2 1 (-1) .same]),
  (.ver 1 0, .hor 2 2, [.M2 1 (-1) .same]),
  (.ver 1 4, .hor 2 1, [.M2 1 (-1) .same]),
  (.ver 0 0, .hor 0 3, [.M2 0 (-1) .same]),
  (.ver 0 4, .hor 0 0, [.M2 0 (-1) .same]),
  (.ver 1 0, .hor 2 3, [.M2 0 (-1) .same]),
  (.ver 1 4, .hor 2 0, [.M2 0 (-1) .same]),
  (.ver 0 1, .hor 2 2, [.M2 1 0 .flip]),
  (.ver 0 3, .hor 2 1, [.M2 1 0 .flip]),
  (.ver 1 1, .hor 0 2, [.M2 1 0 .flip]),
  (.ver 1 3, .hor 0 1, [.M2 1 0 .flip]),
  (.ver 0 1, .hor 2 3, [.M2 0 0 .flip]),
  (.ver 0 3, .hor 2 0, [.M2 0 0 .flip]),
  (.ver 1 1, .hor 0 3, [.M2 0 0 .flip]),
  (.ver 1 3, .hor 0 0, [.M2 0 0 .flip]),
  (.ver 0 1, .hor 0 2, [.M2 1 0 .same]),
  (.ver 0 3, .hor 0 1, [.M2 1 0 .same]),
  (.ver 1 1, .hor 2 2, [.M2 1 0 .same]),
  (.ver 1 3, .hor 2 1, [.M2 1 0 .same]),
  (.ver 0 1, .hor 0 3, [.M2 0 0 .same]),
  (.ver 0 3, .hor 0 0, [.M2 0 0 .same]),
  (.ver 1 1, .hor 2 3, [.M2 0 0 .same]),
  (.ver 1 3, .hor 2 0, [.M2 0 0 .same]),
  (.ver 0 2, .hor 2 0, [.M2 0 1 .flip]),
  (.ver 0 2, .hor 2 3, [.M2 0 1 .flip]),
  (.ver 1 2, .hor 0 0, [.M2 0 1 .flip]),
  (.ver 1 2, .hor 0 3, [.M2 0 1 .flip]),
  (.ver 0 2, .hor 0 0, [.M2 0 1 .same]),
  (.ver 0 2, .hor 0 3, [.M2 0 1 .same]),
  (.ver 1 2, .hor 2 0, [.M2 0 1 .same]),
  (.ver 1 2, .hor 2 3, [.M2 0 1 .same]),
  (.hor 2 0, .hor 2 2, [.H2 0 1 .same, .H2 1 0 .same]),
  (.hor 2 1, .hor 2 3, [.H2 0 1 .same, .H2 1 0 .same]),
  (.hor 0 0, .hor 0 2, [.H2 0 1 .same, .H2 1 0 .same]),
  (.hor 0 1, .hor 0 3, [.H2 0 1 .same, .H2 1 0 .same]),
  (.hor 2 0, .hor 0 2, [.H2 0 1 .flip, .H2 1 0 .flip]),
  (.hor 2 1, .hor 0 3, [.H2 0 1 .flip, .H2 1 0 .flip]),
  (.hor 2 2, .hor 0 0, [.H2 0 1 .flip, .H2 1 0 .flip]),
  (.hor 2 3, .hor 0 1, [.H2 0 1 .flip, .H2 1 0 .flip]),
  (.hor 2 0, .hor 0 3, [.H2 0 0 .flip]),
  (.hor 2 3, .hor 0 0, [.H2 0 0 .flip])
]
-- C-COVER-LIST N=3: 65 class keys (DN {'flip': (0, 1, 2), 'same': (0, 1)}, NEAR_H (0, 1, 2), NEAR_V (-1, 0, 1), T_M 2, DF {'flip': 3, 'same': 2}, DF_V 2, DF_H 3, MM 16), each with an m0 on every piece of [0, 904): short none -> PASS
def recKeys3 : List NEKey := [
  .H2 0 0 .flip,
  .H2 0 1 .flip,
  .H2 0 2 .flip,
  .Hinf 0 .flip,
  .H1 0 .flip,
  .H2 1 0 .flip,
  .H2 1 1 .flip,
  .H2 1 2 .flip,
  .Hinf 1 .flip,
  .H1 1 .flip,
  .H2 2 0 .flip,
  .H2 2 1 .flip,
  .H2 2 2 .flip,
  .Hinf 2 .flip,
  .H1 2 .flip,
  .H2 0 0 .same,
  .H2 0 1 .same,
  .Hinf 0 .same,
  .H1 0 .same,
  .H2 1 0 .same,
  .H2 1 1 .same,
  .Hinf 1 .same,
  .H1 1 .same,
  .M2 0 (-1) .same,
  .M2 0 0 .same,
  .M2 0 1 .same,
  .MinfHV 0 .same,
  .M1HV 0 .same,
  .M2 1 (-1) .same,
  .M2 1 0 .same,
  .M2 1 1 .same,
  .MinfHV 1 .same,
  .M1HV 1 .same,
  .M2 2 (-1) .same,
  .M2 2 0 .same,
  .M2 2 1 .same,
  .MinfHV 2 .same,
  .M1HV 2 .same,
  .MinfVH (-1) .same,
  .M1VH (-1) .same,
  .MinfVH 0 .same,
  .M1VH 0 .same,
  .MinfVH 1 .same,
  .M1VH 1 .same,
  .M2 0 (-1) .flip,
  .M2 0 0 .flip,
  .M2 0 1 .flip,
  .MinfHV 0 .flip,
  .M1HV 0 .flip,
  .M2 1 (-1) .flip,
  .M2 1 0 .flip,
  .M2 1 1 .flip,
  .MinfHV 1 .flip,
  .M1HV 1 .flip,
  .M2 2 (-1) .flip,
  .M2 2 0 .flip,
  .M2 2 1 .flip,
  .MinfHV 2 .flip,
  .M1HV 2 .flip,
  .MinfVH (-1) .flip,
  .M1VH (-1) .flip,
  .MinfVH 0 .flip,
  .M1VH 0 .flip,
  .MinfVH 1 .flip,
  .M1VH 1 .flip
]
-- C-PAIRMAP N=3: 80 pairs, 58 separated with an n = 5 class (each class with a row), 22 joint; pairs without an image or a row none -> PASS
def pairMap3 : List (ECode × ECode × List NEKey) := [
  (.ver 0 0, .hor 2 1, [.M2 2 (-1) .flip]),
  (.ver 0 4, .hor 2 2, [.M2 2 (-1) .flip]),
  (.ver 1 0, .hor 0 1, [.M2 2 (-1) .flip]),
  (.ver 1 4, .hor 0 2, [.M2 2 (-1) .flip]),
  (.ver 0 0, .hor 2 2, [.M2 1 (-1) .flip]),
  (.ver 0 4, .hor 2 1, [.M2 1 (-1) .flip]),
  (.ver 1 0, .hor 0 2, [.M2 1 (-1) .flip]),
  (.ver 1 4, .hor 0 1, [.M2 1 (-1) .flip]),
  (.ver 0 0, .hor 2 3, [.M2 0 (-1) .flip]),
  (.ver 0 4, .hor 2 0, [.M2 0 (-1) .flip]),
  (.ver 1 0, .hor 0 3, [.M2 0 (-1) .flip]),
  (.ver 1 4, .hor 0 0, [.M2 0 (-1) .flip]),
  (.ver 0 0, .hor 0 1, [.M2 2 (-1) .same]),
  (.ver 0 4, .hor 0 2, [.M2 2 (-1) .same]),
  (.ver 1 0, .hor 2 1, [.M2 2 (-1) .same]),
  (.ver 1 4, .hor 2 2, [.M2 2 (-1) .same]),
  (.ver 0 0, .hor 0 2, [.M2 1 (-1) .same]),
  (.ver 0 4, .hor 0 1, [.M2 1 (-1) .same]),
  (.ver 1 0, .hor 2 2, [.M2 1 (-1) .same]),
  (.ver 1 4, .hor 2 1, [.M2 1 (-1) .same]),
  (.ver 0 0, .hor 0 3, [.M2 0 (-1) .same]),
  (.ver 0 4, .hor 0 0, [.M2 0 (-1) .same]),
  (.ver 1 0, .hor 2 3, [.M2 0 (-1) .same]),
  (.ver 1 4, .hor 2 0, [.M2 0 (-1) .same]),
  (.ver 0 1, .hor 2 2, [.M2 1 0 .flip]),
  (.ver 0 3, .hor 2 1, [.M2 1 0 .flip]),
  (.ver 1 1, .hor 0 2, [.M2 1 0 .flip]),
  (.ver 1 3, .hor 0 1, [.M2 1 0 .flip]),
  (.ver 0 1, .hor 2 3, [.M2 0 0 .flip]),
  (.ver 0 3, .hor 2 0, [.M2 0 0 .flip]),
  (.ver 1 1, .hor 0 3, [.M2 0 0 .flip]),
  (.ver 1 3, .hor 0 0, [.M2 0 0 .flip]),
  (.ver 0 1, .hor 0 2, [.M2 1 0 .same]),
  (.ver 0 3, .hor 0 1, [.M2 1 0 .same]),
  (.ver 1 1, .hor 2 2, [.M2 1 0 .same]),
  (.ver 1 3, .hor 2 1, [.M2 1 0 .same]),
  (.ver 0 1, .hor 0 3, [.M2 0 0 .same]),
  (.ver 0 3, .hor 0 0, [.M2 0 0 .same]),
  (.ver 1 1, .hor 2 3, [.M2 0 0 .same]),
  (.ver 1 3, .hor 2 0, [.M2 0 0 .same]),
  (.ver 0 2, .hor 2 0, [.M2 0 1 .flip]),
  (.ver 0 2, .hor 2 3, [.M2 0 1 .flip]),
  (.ver 1 2, .hor 0 0, [.M2 0 1 .flip]),
  (.ver 1 2, .hor 0 3, [.M2 0 1 .flip]),
  (.ver 0 2, .hor 0 0, [.M2 0 1 .same]),
  (.ver 0 2, .hor 0 3, [.M2 0 1 .same]),
  (.ver 1 2, .hor 2 0, [.M2 0 1 .same]),
  (.ver 1 2, .hor 2 3, [.M2 0 1 .same]),
  (.hor 2 0, .hor 2 2, [.H2 0 1 .same, .H2 1 0 .same]),
  (.hor 2 1, .hor 2 3, [.H2 0 1 .same, .H2 1 0 .same]),
  (.hor 0 0, .hor 0 2, [.H2 0 1 .same, .H2 1 0 .same]),
  (.hor 0 1, .hor 0 3, [.H2 0 1 .same, .H2 1 0 .same]),
  (.hor 2 0, .hor 0 2, [.H2 0 1 .flip, .H2 1 0 .flip]),
  (.hor 2 1, .hor 0 3, [.H2 0 1 .flip, .H2 1 0 .flip]),
  (.hor 2 2, .hor 0 0, [.H2 0 1 .flip, .H2 1 0 .flip]),
  (.hor 2 3, .hor 0 1, [.H2 0 1 .flip, .H2 1 0 .flip]),
  (.hor 2 0, .hor 0 3, [.H2 0 0 .flip]),
  (.hor 2 3, .hor 0 0, [.H2 0 0 .flip])
]
/-- the record's C-COVER-LIST parameters: max DN per kind (DN = 0..max), T_M (NEAR_H = 0..T_M, NEAR_V = -1..T_M - 1), DF = max DN + 1, DF_H = T_M + 1, DF_V = T_M -/
def recDNmax : RK → Nat
  | .flip => 2
  | .same => 1
def recTM (N : Nat) : Nat := if N == 4 then 3 else 2

def recKeys (N : Nat) : List NEKey := if N == 4 then recKeys4 else recKeys3
def pairMap (N : Nat) : List (ECode × ECode × List NEKey) := if N == 4 then pairMap4 else pairMap3

/-- the record's keys of a pair with left edge type `ta`, right edge type `tb` and end gaps `gl`, `gr` -/
def keysOfG (N : Nat) (ta tb : EType) (gl gr : Nat) : List NEKey :=
  if ta.isVer = false ∧ tb.isVer = false then
    let k : RK := if ta = tb then .same else .flip
    let m := recDNmax k
    (if gl ≤ m ∧ gr ≤ m then [NEKey.H2 gl gr k, NEKey.H2 gr gl k] else []) ++
    (if gl ≤ m ∧ m + 1 ≤ gr then [NEKey.H1 gl k] else []) ++
    (if gr ≤ m ∧ m + 1 ≤ gl then [NEKey.H1 gr k] else [])
  else if ta.isVer = true ∧ tb.isVer = true then []
  else
    let hl : Bool := !ta.isVer
    let th := if hl then ta else tb
    let tv := if hl then tb else ta
    let iH := if hl then gl else gr
    let gV := if hl then gr else gl
    let k : RK := if (th = .T ∧ tv = .A) ∨ (th = .BB ∧ tv = .B) then .same else .flip
    let t := recTM N
    (if iH ≤ t ∧ gV ≤ t then [NEKey.M2 iH ((gV : Int) - 1) k] else []) ++
    (if iH ≤ t ∧ t + 1 ≤ gV then [NEKey.M1HV iH k] else []) ++
    (if gV ≤ t ∧ t + 1 ≤ iH then [NEKey.M1VH ((gV : Int) - 1) k] else [])

/-- the record's keys of a shape; the end gaps enter capped at 5, which changes no key, since every near or far threshold is at most 4 -/
def keysOf (N : Nat) (s : Shape) : List NEKey := keysOfG N s.ta s.tb (min s.gl 5) (min s.gr 5)

theorem keysOf_cap (N : Nat) (s : Shape) : keysOf N s.cap = keysOf N s := by
  simp only [keysOf, Shape.cap, Nat.min_assoc, Nat.min_self]

/-- two key lists hold the same keys -/
def sameKeys (a b : List NEKey) : Bool := a.all (fun k => b.contains k) && b.all (fun k => a.contains k)

/-- (1) the convention: on the record's 58 separated n = 5 pairs, `keysOf` gives the keys the record lists -/
theorem pairMap4_keys : (pairMap 4).all (fun q => sameKeys (keysOf 4 (shapeOf 5 q.1 q.2.1)) q.2.2) = true := by decide +kernel
theorem pairMap3_keys : (pairMap 3).all (fun q => sameKeys (keysOf 3 (shapeOf 5 q.1 q.2.1)) q.2.2) = true := by decide +kernel

/-- (2) the record's 58 separated n = 5 pairs are the pairs of cNE N 5: each is admissible and in the class, every pair of the class is one
of them in one order or the other, and there are 58 of them (as many as the class has unordered pairs, `count_ne5_3`, `count_ne5_4`) -/
theorem pairMap4_cNE : (pairMap 4).all (fun q => admissible 5 q.1 q.2.1 && cNE 4 5 q.1 q.2.1) = true := by decide +kernel
theorem pairMap3_cNE : (pairMap 3).all (fun q => admissible 5 q.1 q.2.1 && cNE 3 5 q.1 q.2.1) = true := by decide +kernel
theorem cNE5_pairMap4 : (allPairs 5).all (fun p => !cNE 4 5 p.1 p.2 ||
    (pairMap 4).any (fun q => (q.1 == p.1 && q.2.1 == p.2) || (q.1 == p.2 && q.2.1 == p.1))) = true := by decide +kernel
theorem cNE5_pairMap3 : (allPairs 5).all (fun p => !cNE 3 5 p.1 p.2 ||
    (pairMap 3).any (fun q => (q.1 == p.1 && q.2.1 == p.2) || (q.1 == p.2 && q.2.1 == p.1))) = true := by decide +kernel
theorem pairMap_len : (pairMap 4).length = 58 ∧ (pairMap 3).length = 58 := by decide +kernel

/-- the record's class key counts (87 at N = 4, 65 at N = 3) -/
theorem recKeys_len : (recKeys 4).length = 87 ∧ (recKeys 3).length = 65 := by decide +kernel

/-- (3) NE's record covers the class NE of a shape: it has a key, and its keys are the record's -/
def neRec (N : Nat) (s : Shape) : Bool :=
  !s.isNE N || (!(keysOf N s).isEmpty && (keysOf N s).all fun k => (recKeys N).contains k)

theorem neRec_cap (N : Nat) (s : Shape) : neRec N s.cap = neRec N s := by
  simp only [neRec, Shape.isNE_cap, keysOf_cap]

theorem neRec_bounded3 : ∀ ta ∈ allTypes, ∀ tb ∈ allTypes, ∀ off, off < 5 → ∀ gl, gl < 6 → ∀ gr, gr < 6 →
    neRec 3 ⟨ta, tb, off, gl, gr⟩ = true := by decide +kernel

theorem neRec_bounded4 : ∀ ta ∈ allTypes, ∀ tb ∈ allTypes, ∀ off, off < 5 → ∀ gl, gl < 6 → ∀ gr, gr < 6 →
    neRec 4 ⟨ta, tb, off, gl, gr⟩ = true := by decide +kernel

/-- every shape, at N = 3 and N = 4: if it is of class NE, it has a record key, and all its keys are the record's class keys -/
theorem neRec_all (N : Nat) (hN : N = 3 ∨ N = 4) (s : Shape) : neRec N s = true := by
  rw [← neRec_cap]
  obtain ⟨h1, h2, h3⟩ := Shape.cap_bounds s
  rcases hN with rfl | rfl
  · exact neRec_bounded3 _ (mem_allTypes _) _ (mem_allTypes _) _ h1 _ h2 _ h3
  · exact neRec_bounded4 _ (mem_allTypes _) _ (mem_allTypes _) _ h1 _ h2 _ h3

end G2Kernel.StripIII
