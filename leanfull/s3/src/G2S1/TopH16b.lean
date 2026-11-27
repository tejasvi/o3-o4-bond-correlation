/-
G2S1.TopH16b (stage H16; successor of TopH16.lean, which also printed the two auxiliary exports that were
withdrawn): H16 at N = 3 and N = 4, with the axioms. `hLadder` is the package's definition (G2Kernel/Strip300.lean),
unchanged (STATEMENTS_H16_v2.md).
-/
import G2S1.Ladder

namespace G2Kernel

example : hLadder 3 := hLadder_holds3
example : hLadder 4 := hLadder_holds4

end G2Kernel

#print axioms G2Kernel.hLadder_holds3
#print axioms G2Kernel.hLadder_holds4
#print axioms G2S3.hShared_holds3
#print axioms G2S3.hShared_holds4
