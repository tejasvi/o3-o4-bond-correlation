
# ---------------------------------------------------------------- the 3 x 3 grid
NAMES = ['S', 'SE', 'E', 'NE', 'N', 'NW', 'W', 'SW', 'C']
EDGES = {'b0': (0, 1), 'b1': (1, 2), 'b2': (2, 3), 'b3': (3, 4), 'b4': (4, 5), 'b5': (5, 6), 'b6': (6, 7), 'b7': (7, 0),
         'sS': (8, 0), 'sE': (8, 2), 'sN': (8, 4), 'sW': (8, 6)}
ELIST = ['b0', 'b1', 'b2', 'b3', 'b4', 'b5', 'b6', 'b7', 'sS', 'sE', 'sN', 'sW']
# (name, e, f, Delta^2 from out_kt_c2unif_v1_full.out 438317a3 l.4-12, second member (sigma e, sigma f) for C-SYM)
ORBITS = [('O1', 'b0', 'b2', fmpq(1, 36), ('b2', 'b4')), ('O2', 'b0', 'b4', fmpq(1, 144), ('b1', 'b5')),
          ('O3', 'b0', 'sE', fmpq(25, 144), ('b6', 'sS')), ('O4', 'b0', 'sN', fmpq(1, 144), ('b2', 'sW')),
          ('O5', 'b0', 'sW', fmpq(1, 144), ('b2', 'sS'))]
G9 = Graph(9, [EDGES[x] for x in ELIST])
JGRID = [50, 55, 60, 65, 70, 75, 80, 90, 100, 110, 120, 135, 150, 175, 200]
SIGMAS = [fmpq(1, 4), fmpq(1, 3), fmpq(2, 5), fmpq(1, 2), fmpq(3, 5)]
KAPPA = fmpq(4, 5)
RHO2 = fmpq(9801, 10000)
# out_kt_c2unif_v1_full.out (438317a3) l.61-66: D(J_f = beta) for c2's pair (b6, sS) in O3, float quadrature
CDATA = {(3, 100): 4.361620e-06, (3, 150): 1.935314e-06, (3, 200): 1.087723e-06,
         (4, 100): 6.541862e-06, (4, 150): 2.902814e-06, (4, 200): 1.631521e-06}
# the NOTE_SPINWAVE_P3P3_v1 (a4e09eb6) through the REMAINDER_SHEET_LBU_v1 (c6f9cf3e) l.63-69: (A_ef(0), c2, c3) at N = 3, 4
ROW0 = {'O1': ((fmpq(293, 576), fmpq(1, 144), fmpq(1, 216)), (fmpq(875, 768), fmpq(1, 96), fmpq(245, 36864))),
        'O3': ((fmpq(263, 576), fmpq(25, 576), fmpq(73, 3456)), (fmpq(191, 192), fmpq(25, 384), fmpq(1151, 36864))),
        'O2': ((fmpq(145, 288), fmpq(1, 576), fmpq(1, 864)), (fmpq(869, 768), fmpq(1, 384), fmpq(17, 9216))),
        'O4': ((fmpq(239, 576), fmpq(1, 576), fmpq(13, 3456)), (fmpq(179, 192), fmpq(1, 384), fmpq(311, 36864))),
        'O5': ((fmpq(239, 576), fmpq(1, 576), fmpq(13, 3456)), (fmpq(179, 192), fmpq(1, 384), fmpq(311, 36864)))}
# the same sheet l.55: a_1 of F = 1 (A'(0) = E_gamma[H_1]), keyed by n = N - 1
A1ROW0 = {2: fmpq(5, 6), 3: fmpq(31, 64)}
# v1's partner list: the partners of O1..O5 in order, then b3 (M1) and b5 (M2)
PARTNERS_V1 = ['b2', 'b4', 'sE', 'sN', 'sW', 'b3', 'b5']

