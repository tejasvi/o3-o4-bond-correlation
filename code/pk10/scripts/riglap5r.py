#!/usr/bin/env python3
# pk10 (code): Lemma 19.1c with a REFINED quartic remainder: the O(t^4) part of R_E is bounded by exact signed polynomials
# (H4, H2^2, H1H3, H1^2H2), majorants enter only at O(t^5) and beyond:
#   R4H = t^4 H4 + R5H, |R5H| <= t^5 hbar5/120;  D3 = t^3 H3 + R4H, |D3| <= t^3 hbar3/6;  E2 = t^2 H2 + D3, |E2| <= t^2 hbar2/2;
#   |R_E| <= t^4|H4| + t^5 hbar5/120 + (1/2)t^4 H2^2 + t^6 hbar3^2/72 + t^4|H1H3| + t^5|H1H4| + t^6|H1| hbar5/120 + (t^5/6)|H2| hbar3
#            + (1/2)t^4 H1^2|H2| + (t^5/12) H1^2 hbar3 + (t^5/8)|H1| hbar2^2 + (t^6/48) hbar2^3 + |rho4(H)|.
# (Derivation: R_E = R4H + (1/2)(t^4H2^2 + D3^2 + 2tH1D3 + 2t^2H2D3) + (1/6)(3t^2H1^2E2 + 3tH1E2^2 + E2^3) + rho4(H), with
#  2tH1D3 = 2t^4H1H3 + 2tH1 R4H, |2tH1R4H| <= 2t^5|H1H4| + t^6|H1|hbar5/60, and 3t^2H1^2E2 = 3t^4H1^2H2 + 3t^2H1^2 D3.)
import math
import numpy as np
import riglap2 as _r
import riglap3 as _r3
import riglap5b
from riglap4 import norm_any, _deg
from riglap5 import hhat2
from pseries import padd, pscale, pmul


class Prep5r(riglap5b.Prep5):
    def __init__(self, g, J, rho, rho_p, key="g", dmaxH=16, qcap=4, dexact=None):
        super().__init__(g, J, rho, rho_p, key=key, dmaxH=dmaxH, qcap=qcap, dexact=dexact)
        if not self.ok:
            return
        t, n, W, a_v = self.t, g.n, g.W, self.a_v
        Hs = _r3.Model3(g, 4, []).H(4)
        H1, H2, H3, H4 = Hs.c[1], Hs.c[2], Hs.c[3], Hs.c[4]
        mjH = _r.Majorants(_r.Model(g, 5, []), a_v, t, B=riglap5b.NPOLY_B)
        h2 = mjH.hbar(2).to_dict(); h3 = mjH.hbar(3).to_dict(); h5 = mjH.hbar(5).to_dict()
        kH = key + "|H"
        N2 = lambda P: norm_any(P, g.G, n, W, 2, kH, dmaxH)
        H1sq = pmul(H1, H1)
        self.rE_old = self.rE
        self.rE_parts = {
            "t4|H4|": t ** 4 * N2(H4), "t5 h5/120": t ** 5 / 120 * N2(h5), "t4 H2^2/2": 0.5 * t ** 4 * N2(pmul(H2, H2)),
            "t6 h3^2/72": t ** 6 / 72 * N2(pmul(h3, h3)), "t4|H1H3|": t ** 4 * N2(pmul(H1, H3)), "t5|H1H4|": t ** 5 * N2(pmul(H1, H4)),
            "t6|H1|h5/120": t ** 6 / 120 * N2(pmul(H1, h5)), "t5|H2|h3/6": t ** 5 / 6 * N2(pmul(H2, h3)),
            "t4 H1^2|H2|/2": 0.5 * t ** 4 * N2(pmul(H1sq, H2)), "t5 H1^2 h3/12": t ** 5 / 12 * N2(pmul(H1sq, h3)),
            "t5|H1|h2^2/8": t ** 5 / 8 * N2(pmul(H1, pmul(h2, h2))),
            "t5 h2^2 hhat/24": t ** 5 / 24 * N2(pmul(pmul(h2, h2), hhat2(g, a_v, t, h2)))}
        # (1/6)|E2|^3 <= (1/6)(t^2 hbar2/2)^2 (t hhat) = (t^5/24) hbar2^2 hhat  (one factor traded on Omega: (t^2/2) hbar2 <= t hhat)
        self.rE = sum(self.rE_parts.values())
