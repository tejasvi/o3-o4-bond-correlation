#!/usr/bin/env python3
# pk10 (code): boundary vector w = K^{1/2} V 1 of the free end (3 x n strip, free boundary): overlap with the trial vacuum.
#   I_mix = <phi, K V 1>/main_mix (left column: vacuum couplings (a, a, b) and the p-factor; right column: the free end, verticals (1, 1));
#   I_free = <V 1, K V 1>/main_free (both columns free ends).  q^2 = <u^, w>^2/||w||^2 = I_mix^2 r_main/(g00 I_free), r_main = main_mix^2/(main_D main_free).
# Usage: endw.py OUTJSON N J VACRES_JSON S_RAD RHO_P M2JSON
import sys, math, json, time
sys.path.insert(0, "/mnt/g2/release/root/code/pk10/scripts")
import riglap5b, riglap5s
riglap5b.NPOLY_B = 16
from riglap2 import Graph
from vacmod2 import A_EX, B_EX
from lapl2 import strip_graph
outf, NN, J, vf, s_rad, rho_p, m2f = sys.argv[1], int(sys.argv[2]), float(sys.argv[3]), sys.argv[4], float(sys.argv[5]), float(sys.argv[6]), sys.argv[7]
t = 1.0 / J
R3 = json.load(open(vf)); M2 = json.load(open(m2f))
a, b = A_EX, B_EX
H = {(0, 3): 1.0, (1, 4): 1.0, (2, 5): 1.0}
Emix = dict(H); Emix.update({(0, 1): a, (1, 2): a, (0, 2): b, (3, 4): 1.0, (4, 5): 1.0})
Efree = dict(H); Efree.update({(0, 1): 1.0, (1, 2): 1.0, (3, 4): 1.0, (4, 5): 1.0})
VD, ED = strip_graph(2, (A_EX, B_EX))
gmix = Graph(6, Emix, [(0, 1), (1, 2), (0, 2)], N=NN)
gfree = Graph(6, Efree, [], N=NN)
gD = Graph(VD, ED, [(0, 1), (1, 2), (0, 2), (3, 4), (4, 5), (3, 5)], N=NN)
r_main = math.exp(2 * gmix.logmain(J) - gfree.logmain(J) - gD.logmain(J))
pv = lambda col: ('p', col, R3["q1"], R3["q2"], R3["q3"])
res = {"N": NN, "J": J, "r_main": r_main, "items": {}}
T0 = time.time()
for name, g, facs in (("I_mix", gmix, [pv((0, 1, 2))]), ("I_free", gfree, [])):
    rr = [math.sqrt(min(s_rad * g.G[v, v] / J, 0.6)) for v in range(g.V)]
    pr = riglap5s.Prep5s(g, J, rr, rho_p, key=name, qcap=6)
    ak, B = riglap5s.bound5s(pr, facs)
    res["items"][name] = {"ak": ak, "B": B, "value": sum(c * t ** k for k, c in enumerate(ak)), "err": sum(B.values())}
    print("%s %.9f +- %.2e  ak %s (%.0f s)" % (name, res["items"][name]["value"], res["items"][name]["err"], ["%.6f" % c for c in ak], time.time() - T0)); sys.stdout.flush()
g00 = M2["items"]["g00"]["value"]
q2 = res["items"]["I_mix"]["value"] ** 2 * r_main / (g00 * res["items"]["I_free"]["value"])
print("r_main %.10f; q^2 = <u^,w>^2/|w|^2 = %.8f; R_w(trial) = sqrt(1/q^2 - 1) = %.5f" % (r_main, q2, math.sqrt(max(1 / q2 - 1, 0))))
json.dump(res, open(outf, "w"))
