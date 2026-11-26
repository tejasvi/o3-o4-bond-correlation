# su29: certified enclosures (mpmath interval arithmetic) of the 4-state inputs of STRIPW sections 5 and 9, for ALL J in (0, 1/100].
# Method: every base remainder below is a power series in J^2 with nonnegative coefficients, hence increasing in J, so over (0, J0]
# it lies in [value at 0, value at J0]; the J0 value is summed in interval arithmetic with an explicit tail bound (2 x last term).
# All derived quantities are written so that leading constants cancel by hand (u-expansions), then evaluated with J in [0, J0],
# w = J^2 in [0, J0^2] treated as independent intervals (valid, slightly loose). No division by an interval containing 0 occurs.
import sys
from mpmath import iv, factorial
iv.dps = 40
N = int(sys.argv[1])
J0 = iv.mpf(1) / 100
I = lambda a, b: iv.mpf([a, b])
def E2p(p):
    if N == 3: return iv.mpf(1) / (2 * p + 1)
    return iv.mpf(int(factorial(2 * p))) / (int(factorial(p)) * int(factorial(p + 1)) * 4 ** p)
def enc(coef, pmin, nterms=30):
    s = iv.mpf(0)
    for p in range(pmin, pmin + nterms):
        s += coef(p) * J0 ** (2 * (p - pmin))
    last = coef(pmin + nterms - 1) * J0 ** (2 * (nterms - 1))
    hi = s + 2 * last
    return I(coef(pmin).a, hi.b)
fac = lambda n: iv.mpf(int(factorial(n)))
K0r = enc(lambda p: E2p(p) / fac(2 * p), 1)            # (k0 - 1)/J^2
K1r = enc(lambda p: E2p(p + 1) / fac(2 * p + 1), 0)    # k1/J
K1rr = enc(lambda p: E2p(p + 1) / fac(2 * p + 1), 1)   # (k1/J - 1/N)/J^2
M2r = enc(lambda p: E2p(p + 1) / fac(2 * p), 1)        # (m2 - 1/N)/J^2
M3r = enc(lambda p: E2p(p + 2) / fac(2 * p + 1), 0)    # m3/J
K2r = enc(lambda p: (N * E2p(p + 2) - E2p(p + 1)) / ((N - 1) * fac(2 * p + 2)), 0)   # k2/J^2
J = I(0, J0.b); w = I(0, (J0 * J0).b)
sN = iv.sqrt(iv.mpf(N)); s2 = iv.sqrt(iv.mpf(2))
k0 = 1 + w * K0r; k1 = J * K1r; m2 = iv.mpf(1) / N + w * M2r; m3 = J * M3r
k1w = K1r ** 2 * k0                                      # kappa1 / w
Ar = (K0r - M2r) / (N - 1); Br = (N * M2r - K0r) / (N - 1)
e_k05 = K0r * (5 + 10 * w * K0r + 10 * w ** 2 * K0r ** 2 + 5 * w ** 3 * K0r ** 3 + w ** 4 * K0r ** 4)
e_hm = K0r + N * M2r + N * w * K0r * M2r - N * K1r ** 2
e_hp = K0r + N * M2r + N * w * K0r * M2r + N * K1r ** 2
e_h1 = 2 * N * Ar + 2 * Br + w * (N ** 2 * Ar ** 2 + 2 * N * Ar * Br + N * Br ** 2)
omJ = s2 * N * K1r * m2
aw = iv.sqrt(iv.mpf(2 * N)) * k0 ** 3 * K1r ** 2
bJ3 = sN * k0 ** 2 * K1r ** 3
a2kw = 2 * N * k0 ** 5 * K1r ** 2; abkJ3 = s2 * N * k0 ** 4 * K1r ** 3; b2kw2 = N * k0 ** 3 * K1r ** 4
def show(name, x, unit=''):
    print('  %-34s [%.6f, %.6f] %s' % (name, float(x.a), float(x.b), unit))
print('N = %d, all J in (0, 1/100]' % N)
print('entries (section 5 "Entry bounds"):')
show('(h- - 1)/J^2', e_hm); show('(h+ - 1)/J^2', e_hp); show('(h1 - 1)/J^2', e_h1); show('(k0^5 - 1)/J^2', e_k05)
show('omega/J', omJ); show('a/J^2', aw); show('b/J^3', bJ3); show('a^2/(kappa1 J^2)', a2kw); show('kappa1/J^2', k1w)
# mu1
den2 = k0 ** 5 - 2 * w * k1w
chk = 1 + w * e_hp + J * omJ
m1r = I(e_k05.a, (e_k05 + (w * aw ** 2 + w * w * bJ3 ** 2) / den2).b)
mu1 = 1 + w * m1r
print('Lemma 5.1:'); show('(a) (mu1 - 1)/J^2', m1r); print('      (uses ||M\'|| <= kappa1 (h+ + omega) <= 2 kappa1: h+ + omega <= %.6f)' % float((1 + w * I(max(e_hp.b, e_h1.b), max(e_hp.b, e_h1.b)) + J * omJ).b))
c = iv.mpf('0.6')
Z = w * k1w * (1 + c * J * I(-1, 1))
den = k0 ** 5 - Z
pw = e_hp - a2kw / den; sw = e_h1 - w * b2kw2 / den; qJ = omJ - w * abkJ3 / den
RJ = iv.sqrt((J * (sw - pw) / 2) ** 2 + qJ ** 2)
mu2J = J * (pw + sw) / 2 + RJ; mu4J = J * (pw + sw) / 2 - RJ
show('p/J^2 (z in kappa1[1 +- 0.6J])', pw); show('s/J^2', sw); show('q/J', qJ)
show('(c) (mu2^ - 1)/J', mu2J); show('    (mu4^ - 1)/J', mu4J); show('(b) (mu3^ - 1)/J^2', e_hm)
print('      self-consistency: cluster eigenvalues inside kappa1[1 +- 0.6J]:', bool(mu2J.b < c.a and mu4J.a > -c.a))
show('(d) gap (mu2^ - mu3^)/J', mu2J - J * e_hm); show('    gap (mu3^ - mu4^)/J', J * e_hm - mu4J)
dRw = c * J * w * (aw + J * bJ3) ** 2 / den.a ** 2
conv = (pw + sw) - 2 * e_hm + I(-1, 1) * dRw
show('(d) convexity (mu2^+mu4^-2mu3^)/J^2', conv)
dz = (aw * aw * w * w + w ** 3 * bJ3 ** 2) * (Z.b - Z.a) / (den.a ** 2)   # ||M(z)-M(z')|| over the used z-range (absolute, not /kappa1)
show('    ||M(z)-M(z\')|| / J^6 (|z/k1-1|<=0.6J)', dz / w ** 3 if False else iv.mpf([0, (dz / iv.mpf(1)).b]) / (J0 ** 6) * 0 + I(0, ((aw.b ** 2 + J0.b ** 2 * bJ3.b ** 2) * (2 * c.b * J0.b * k1w.b) / den.a.a ** 2)), 'x J^7 (bound)')
# Lemma 5.2
h1 = 1 + w * e_h1; hp = 1 + w * e_hp; k1_ = w * k1w; om = J * omJ
det = (mu1 - k1_ * hp) * (mu1 - k1_ * h1) - k1_ ** 2 * om ** 2
betaw = ((mu1 - k1_ * h1) * aw + w * w * k1w * omJ * bJ3) / (s2 * det)
gamJ3 = (w * k1w * omJ * aw + (mu1 - k1_ * hp) * bJ3) / det
beta0 = sN / N ** 2; gam0 = sN / N ** 3
N1 = 1 / iv.sqrt(1 + 2 * (w * betaw) ** 2 + (w * J * gamJ3) ** 2)
print('Lemma 5.2:'); show('beta / (leading beta0 J^2)', betaw / beta0, '(beta0 = sqrt(N)/N^2)'); show('gamma / (leading gamma0 J^3)', gamJ3 / gam0, '(gamma0 = sqrt(N)/N^3)')
t2e = (sw - pw) / (2 * qJ)
epsJ = I((t2e.a / 2 * (1 - (J0.b * t2e.b) ** 2 / 3)).a, (t2e.b / 2).b)
show('tan(2 eps)/J', t2e); show('eps/J', epsJ)
psi0w = iv.sqrt(aw ** 2 + J ** 2 * bJ3 ** 2) / den.a
show('|psi_k(0)|/J^2 (k = 2, 4) <=', I(0, psi0w.b))
nu = I(iv.sqrt(1 - (J0 ** 2 * psi0w.b) ** 2).a, 1)
# Lemma 5.3 / (E5): horizontal overlaps
Jrho = m2 / K1r - w * K1r / k0
u_rho = (M2r - K1rr) / K1r - K1r / k0
sig_w2 = N1 ** 2 * (betaw ** 2 + w * gamJ3 ** 2)
u_N = -N1 * w * (2 * betaw ** 2 + w * gamJ3 ** 2) / (1 / N1 + 1)
B_t = betaw / (sN * K1r ** 2)            # B~ = beta/(sqrt(N) k1^2)
X1 = -k0 ** 3 * k1w * (hp * (mu1 - k1_ * h1) + k1_ * om ** 2 + mu1 * w * omJ * bJ3 / aw) / (mu1 * det)    # (k0^3/mu1 - B~)/J^2
# u_beta = (beta/w - beta0)/(w beta0):  beta/w - beta0 = sqrt(N)[K1r^2 B~ - 1/N^2];  K1r^2 B~ - 1/N^2 = K1r^2(B~ - 1) + (K1r^2 - 1/N^2)
# B~ - 1 = (k0^3/mu1 - 1) - (k0^3/mu1 - B~) ;  k0^3/mu1 - 1 = (k0^3 - mu1)/mu1 = w[K0r(3+3wK0r+w^2K0r^2) - m1r]/mu1
Bm1_w = (K0r * (3 + 3 * w * K0r + w ** 2 * K0r ** 2) - m1r) / mu1 - X1
u_beta = sN * (K1r ** 2 * Bm1_w + K1rr * (K1r + iv.mpf(1) / N)) / beta0
show('u_beta = (beta/beta0 - 1)/J^2', u_beta); show('u_rho = (J rho - 1)/J^2', u_rho)
sl = epsJ.a * (1 - (J0.b * epsJ.b) ** 2 / 6); sh = epsJ.b   # sin(eps)/J in [sl, sh]
sinJ = I(sl.a if hasattr(sl, 'a') else sl, sh.b if hasattr(sh, 'b') else sh)
u_c = I((-(epsJ.b ** 2) / 2).a, 0)                         # (cos eps - 1)/J^2
u_nu = I((-(w.b * psi0w.b ** 2)).a, 0)                     # (nu - 1)/J^2 >= -J^2 psi_w^2
def prod_minus_one_over_w(us):
    tot = iv.mpf(0); pref = iv.mpf(1)
    for u in us:
        tot += u * pref; pref = pref * (1 + w * u)
    return tot, pref
pref0 = 2 * Jrho * N1 / beta0
# --- t (and bb): kappa = (1, +-sqrt2, 1)
bp = betaw * (1 - 2 * w * w * sig_w2)
cos2 = 1 + w * u_c; cos4 = cos2
nu2 = 1 + w * u_nu; nu4 = nu2
# (delta2 - delta4)/J
dcos_J = I(-1, 1) * J * epsJ.b ** 2 / 2
term_b = bp * ((I(-1, 1) * J ** 3 * psi0w.b ** 2) * 1 / s2 + nu4 * (dcos_J - 2 * sinJ) / 2)
sinth2 = (cos2 + J * sinJ) / s2; costh4 = (cos4 - J * sinJ) / s2
term_g = gamJ3 * (1 - w * w * sig_w2) * (nu2 * sinth2 + nu4 * costh4)
term_p = -J ** 3 * sig_w2 * (2 * I(-1, 1) * psi0w.b)
dmd = pref0 * (term_b + term_g + term_p)
# (delta2 + delta4)/J
u_sig = -2 * w * sig_w2
P1, Pp = prod_minus_one_over_w([u_rho, u_N, u_beta, u_sig])
u_cc = u_c + u_nu + w * u_c * u_nu
S_J = (nu4 * sinJ - nu2 * sinJ) / 2          # (nu4 sin eps4 - nu2 sin eps2)/(2J): independent eps
inner_tot, _ = prod_minus_one_over_w([u_rho, u_N, u_beta, u_sig, u_cc])
gam_term = pref0 * gamJ3 * (1 - w * w * sig_w2) * ((nu2 * cos2 - nu4 * cos4) / s2 + J * (nu2 * sinJ + nu4 * sinJ) / s2)
pp_term = -pref0 * J ** 3 * sig_w2 * (2 * I(-1, 1) * psi0w.b) / 1
dpd = 2 * J * inner_tot + 2 * Pp * S_J + gam_term + pp_term
d2 = (dpd + dmd) / 2; d4 = (dpd - dmd) / 2
print('Lemma 5.3 / (E5), t and bb (unit sqrt(N) J/(2N^2)), deep 4-state model:')
show('(delta2 - delta4)/J', dmd); show('(delta2 + delta4)/J', dpd); show('delta2/J', d2); show('delta4/J', d4)
d3 = s2 * J * P1
show('delta3/J (t; bb: same with sign)', d3)
# --- h: kappa = (2, 0, 2); u^h = rho N1 (-sig_h, beta(1-sig_h), -sig_h gamma, beta(1-sig_h)), sig_h = 2 N1^2 beta^2
sigh_w2 = 2 * N1 ** 2 * betaw ** 2
u_sigh = -w * sigh_w2
Ph_tot, Php = prod_minus_one_over_w([u_rho, u_N, u_beta, u_sigh])
# a2^h/u0 = pref0*[ -sig_h psi2(0)/w + nu2 sqrt2 beta_w (1-sig_h) cos th2 - sig_h (gamma/w) nu2 sin th2 ];  sqrt2 cos th = cos eps - sin eps
# a2^h/u0 - 2 = 2[Ph*nu2*cos eps2 - 1] - 2 Ph nu2 sin eps2 + small ; a4^h/u0 - 2 = 2[Ph nu4 cos eps4 - 1] + 2 Ph nu4 sin eps4 + small
inner_h, _ = prod_minus_one_over_w([u_rho, u_N, u_beta, u_sigh, u_nu, u_c])
small_h = pref0 * (I(-1, 1) * w * sigh_w2 * psi0w.b * w / J0.b * 0 + I(-1, 1) * (w * sigh_w2 * psi0w.b * J + w * w * sigh_w2 * J * gamJ3))
d2h = 2 * J * inner_h - 2 * Php * nu2 * sinJ + small_h
d4h = 2 * J * inner_h + 2 * Php * nu4 * sinJ + small_h
print('h (unit as above):'); show('delta2^h/J', d2h); show('delta4^h/J', d4h)
# --- top-bottom pairing f(0) deep (t vs bb): rho^2 N1^2 [gamma^2(1-s)^2 - 2 beta^2 s(1-s) + s^2], ratio to leading (gamma0 J^2... )^2 = (sqrt(N)/N^3)^2 J^4
f0 = Jrho ** 2 * N1 ** 2 * (gamJ3 ** 2 * (1 - w * w * sig_w2) ** 2 - 2 * w * betaw ** 2 * sig_w2 * (1 - w * w * sig_w2) + w * sig_w2 ** 2) / gam0 ** 2
show('f(0) deep t-bb / (N J^4/N^6)', f0, '(leading J^4/1024 at N=4, J^4/243 at N=3)')
# --- boundary-dressed (end horizontal t0): b4 = (1, beta_b, gamma_b, beta_b), beta_b = sqrt(N) k1^2/k0^2, gamma_b = sqrt(N) k1^3/k0^3
betab_w = sN * K1r ** 2 / k0 ** 2; gamb_J3 = sN * K1r ** 3 / k0 ** 3
show('beta_b/beta0', betab_w / beta0); show('gamma_b/gamma0', gamb_J3 / gam0)
# ---------------- verticals (a; b is the flip 110 <-> 011) ----------------
Apr = (K1r - M3r) / (N - 1); Bpr = (N * M3r - K1r) / (N - 1)        # A' = J Apr, B' = J Bpr
A_ = iv.mpf(1) / N + w * Ar; B_ = w * Br
C101 = N * A_ * Apr + Apr * B_ + A_ * Bpr + B_ * Bpr                    # (N A A' + A'B + AB' + BB')/J
Rest_w = (2 * K1r * k0 ** 3 * betaw * sN * m2 + 2 * w * K1r ** 2 * k0 ** 2 * gamJ3 * sN * m2 + 2 * w * K1r ** 3 * k0 ** 2 * betaw * sN
          + w ** 2 * K1r ** 2 * k0 ** 2 * betaw ** 2 * N * M3r + 2 * w ** 3 * K1r ** 3 * k0 * betaw * gamJ3 * N * M3r
          + 2 * w ** 2 * K1r ** 3 * k0 * betaw ** 2 * N * m2 + w ** 3 * K1r ** 2 * k0 * gamJ3 ** 2 * N * C101
          + 2 * w ** 2 * K1r ** 2 * k0 * gamJ3 * betaw * N * m2 ** 2 + w ** 2 * K1r ** 3 * k0 * betaw ** 2 * N * m2)
caJ = N1 ** 2 * (k0 ** 4 * K1r + w * Rest_w) / mu1                       # c_a / J
Rca_w = N1 ** 2 * Rest_w / mu1
Bt = betaw / (sN * K1r ** 2)
Y = ((m1r - e_k05) + N1 ** 2 * w * (2 * betaw ** 2 + w * gamJ3 ** 2) * k0 ** 5) / mu1 + N1 ** 2 * k0 ** 2 * X1
ua011_J5 = N1 * sN * K1r ** 2 * ((K1r * k0 ** 2 / mu1) * Y - Rca_w * Bt) + N1 * (2 * K1r ** 3 * k0 * N * m2 * betaw + K1r ** 2 * k0 * N * m2 ** 2 * gamJ3) / mu1
ua110_J = N1 * (K1r * k0 ** 3 * sN * m2 + w ** 2 * K1r ** 2 * k0 * N * (k0 * M3r * betaw + w * K1r * M3r * gamJ3 + K1r * m2 * betaw)) / mu1 - caJ * N1 * w * betaw
ua101_w = N1 * (K1r ** 2 * k0 ** 2 * sN * m2 + w ** 2 * K1r ** 3 * k0 * N * M3r * betaw + w ** 2 * K1r ** 2 * k0 * N * C101 * gamJ3 + w * K1r ** 2 * k0 * N * m2 ** 2 * betaw) / mu1 - w * caJ * N1 * gamJ3
T0r = K1r * k0 ** 2 * sN * (k0 * m2 * betaw + w * K1r * m2 * gamJ3 + w * K1r ** 2 * betaw)
ua0_J3 = N1 * (k0 ** 4 * K1r * N1 ** 2 * w * (2 * betaw ** 2 + w * gamJ3 ** 2) + T0r - N1 ** 2 * Rest_w) / mu1
print('verticals, deep 4-state model (A4 / Lemma 5.3):')
show('u^a(110) / (leading sqrt(N) J/N^2)', ua110_J / (sN / N ** 2)); show('u^a(101) / (leading sqrt(N) J^2/N^3)', ua101_w / (sN / N ** 3))
show('u^a(0) / (leading -J^3/N^3)', ua0_J3 / (-iv.mpf(1) / N ** 3)); show('u^a(011) / J^5', ua011_J5)
# differences from t, J-scaled
X2 = -k1w * (h1 * (mu1 - k1_ * hp) + k1_ * om ** 2 + mu1 * omJ * aw / (sN * k0 ** 2 * K1r ** 3)) / (mu1 * det)
Gt = gamJ3 / (sN * k0 ** 2 * K1r ** 3)
D110_Jw = N1 * sN * K1r * (m2 * X1 + Bt * K1r ** 2 / k0) + Jrho * N1 * betaw * w * sig_w2 + N1 * w * K1r ** 2 * k0 * N * (k0 * M3r * betaw + w * K1r * M3r * gamJ3 + K1r * m2 * betaw) / mu1 - caJ * N1 * betaw
D101_w2 = N1 * sN * k0 ** 2 * K1r ** 2 * (m2 * X2 + Gt * K1r ** 2 / k0) + N1 * (w * K1r ** 3 * k0 * N * M3r * betaw + w * K1r ** 2 * k0 * N * C101 * gamJ3 + K1r ** 2 * k0 * N * m2 ** 2 * betaw) / mu1 - caJ * N1 * gamJ3 + Jrho * N1 * gamJ3 * w * sig_w2
D0_J3 = ua0_J3 + Jrho * N1 * sig_w2
D011_J5 = ua011_J5 + Jrho * N1 * sig_w2 * betaw
show('(u^a - u^t)(110) / J^3', D110_Jw); show('(u^a - u^t)(101) / J^4', D101_w2); show('(u^a - u^t)(0) / J^3', D0_J3)
cth = (cos2 - J * sinJ) / s2; sth = (cos2 + J * sinJ) / s2      # cos(theta), sin(theta) with theta = pi/4 + eps
dd2 = (2 * w * J * psi0w.b * I(-1, 1) * D0_J3 + s2 * nu2 * cth * J * D110_Jw + s2 * nu2 * cth * J * w * D011_J5 + 2 * nu2 * sth * w * D101_w2) / beta0
dd4 = (2 * w * J * psi0w.b * I(-1, 1) * D0_J3 + s2 * nu4 * sth * J * D110_Jw + s2 * nu4 * sth * J * w * D011_J5 - 2 * nu4 * cth * w * D101_w2) / beta0
show('(delta2^a - delta2^t)/J', dd2); show('(delta4^a - delta4^t)/J', dd4)
print('   (these are (a^a_k - a^t_k)/(u0 J) with u0 = J beta0/2; each term carries an explicit power of J)')
show('delta2^a/J', d2 + dd2); show('delta4^a/J', d4 + dd4); show('(delta2^a - delta4^a)/J', dmd + dd2 - dd4)
# ---------------- top-bottom pairings f(0) / (gamma0^2 J^4), all variants ----------------
def vec_t():   # deep t: components scaled: (0: J^3, 110: J, 101: J^2, 011: J^5)
    return (-Jrho * N1 * sig_w2, Jrho * N1 * betaw * (1 - w * w * sig_w2), Jrho * N1 * gamJ3 * (1 - w * w * sig_w2), -Jrho * N1 * sig_w2 * betaw)
def vec_bb():
    t = vec_t(); return (t[0], t[3], t[2], t[1])    # flip 110 <-> 011 (with scales swapped accordingly: handled in pair())
sb_w2 = (betaw * betab_w + w * gamJ3 * gamb_J3) / (1 + 2 * w * w * betaw * betab_w + w ** 3 * gamJ3 * gamb_J3)   # sigma_b / J^4
Nb = 1 / (N1 * (1 + 2 * w * w * betaw * betab_w + w ** 3 * gamJ3 * gamb_J3))
def vec_t0():
    return (-Jrho * Nb * sb_w2, Jrho * Nb * betab_w * (1 - w * w * sb_w2), Jrho * Nb * gamb_J3 * (1 - w * w * sb_w2), -Jrho * Nb * sb_w2 * betab_w)
def vec_a():
    return (ua0_J3, ua110_J, ua101_w, ua011_J5)
# scales: entry 0 ~ J^3, 110 ~ J, 101 ~ J^2, 011 ~ J^5 for "top" vectors; for "bottom" (flipped) vectors 110 ~ J^5 and 011 ~ J.
def pair(top, bot):
    # <top, flip(bot)>/J^4 where flip(bot) has (0, 110, 101, 011) = (bot0 J^3, bot011 J^5, bot101 J^2, bot110 J)
    s = top[0] * bot[0] * w + top[1] * bot[3] * w + top[2] * bot[2] + top[3] * bot[1] * w
    return s / gam0 ** 2
print('top-bottom pairings f(0)/(gamma0^2 J^4), deep 4-state vectors and the exact boundary-dressed b4 (gamma0^2 = 1/1024 at N=4, 1/243 at N=3):')
for nm, tv, bv in [('t - bb (deep)', vec_t(), vec_t()), ('t0 - bb (end, deep)', vec_t0(), vec_t()), ('t0 - bb0 (both ends)', vec_t0(), vec_t0()),
                   ('a - bb (deep)', vec_a(), vec_t()), ('a - b (deep)', vec_a(), vec_a()), ('t0 - b (end, deep vertical)', vec_t0(), vec_a())]:
    show(nm, pair(tv, bv))
