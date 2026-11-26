# SPEC_M2B_CERT_v1_ADD3: LAW v1 and the record state the |g| form (pk02, after the C1 question)

Addendum to SPEC_M2B_CERT_v1.md (ffd842a2), ADD1 (2c97391f) and ADD2 (48d5fa54). It changes the wording of what LAW v1 and the M2B_KV_v1
record claim, not any computation. Written 2026-11-07 at the hand, after the review of Lemma E:
step (E4) needs bound (b) in the |g| form.

## 1. Statement
- Notation (PK10_NOTES sect. 19.2, 19.3.3 (v)): psihat = K^{1/2} phi is the trial vacuum, mhat its eigenvalue estimate, and
  g = VK phi - mhat phi the residual function, so (T - mhat) psihat = K^{1/2} g.
- LAW v1's eps_r bounds the |g| form: ||K^{1/2} |g| || <= eps_r mhat ||psihat|| for every J >= 300, t -> 0 included. Since K is a positive
  kernel, |<g, K g>| <= <|g|, K |g|>, so this implies S3 (b)'s ||(T - mhat) psihat|| <= eps_r mhat ||psihat||.
- eps_a, eps_ds5 (multipliers xi-type, |w| <= c_xi J and c_xi J/2 on the near region, 2J and J everywhere) and eps_w, eps_d (Lemma 19.5w's
  multipliers, |w| <= |lin_w| + B_w on the near region) bound ||K^{1/2} |w g| ||/(mhat ||psihat||).

## 2. Why the certified computation gives the |g| form
Every term of eps_r is either a bound for a positive kernel or a sign-blind second moment after Cauchy-Schwarz with a positive weight; the
certified pieces port these forms into balls (line numbers of m2b_cert_v1_2.py, whose shared pieces are m2b_cert_v1_1's verbatim):
- Good part on Omega_out (PK10_NOTES l.1117-1119): the form <., K .> is bounded by Cauchy-Schwarz for the positive weight M, which
  bounds <|g_G|, M |g_G|> by E_M[R^2]; that moment is the same for R and |R|. The cert's terms are the outer weighted second moments by
  Wishart moments: nP and R1 (l.974-975), nD of the conditional expectation of the positive majorant D-bar_5 (l.1055; D-bar l.532-543 from
  hk l.486-492 and pi_vac l.516-528, which takes abs of the q coefficients), nR0 with abs(m_j) (l.1099, l.1111).
- Tails and annulus (l.1114-1116 of the notes): Cauchy-Schwarz, then Chernoff on second moments (cert l.1152-1153, l.1198).
- Outer far (notes l.1120): |g_G| <= VK|phi| + mhat|phi|, so E4 + 2 mhat E3 + mhat^2 ED with |p| majorants: integrals of nonnegative
  functions (pk03's outer_far items, m3_reader_v5 57d17d7b).
- Bad bonds (notes l.1105): sup|p| <= 1 + sum_i t^i sum |q_{i,beta}| (2J)^deg times a positive kernel (m2b_asm_v1's supp uses abs).
- Assembly: Minkowski for the K-seminorm over g = g_G + g_B; the good part splits into pairs inside Omega_out and the outer region U, both
  nonnegative for |g|; hence sqrt(near^2 + far) + gB over sqrt(Z2).
- The weighted forms (wnorm l.943-946, dwt/dwl l.1066-1076) are Lemma 19.5w's ||lin_w P|| + ||B_w P|| (notes l.1503-1507).
- LAW v1 carries the J1 values to every J >= 300 by monotone factors on these positive and second-moment forms (SPEC sect. 3).
PK10_NOTES l.1254 and l.1293 (reviewer flag 2) state the same: the sect. 19.2 bounds control ||K^{1/2} |g| ||.

## 3. Where the wording goes
- m2b_reader_v1's CLAIM (the record's CLAIM line, compared by exact equality) states the |g| form and the multiplier forms (draft e2).
- THMS's S3 (b) can cite this addendum for the |g| form (pk14 strengthens it in the next THMS revision).
- Consumers: anything using eps_a, eps_ds5, eps_w or eps_d already rests on the |g| form through the multiplier step; a consumer using
  only eps_r and s needs the weaker form alone.
