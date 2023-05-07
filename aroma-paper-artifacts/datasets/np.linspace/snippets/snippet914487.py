import numpy as np
import torch


def analytic_results(self):
    '\n            Some analytic results of the model, based on Jordan-Wigner transformation.\n        The formulas may be a little problematic for finite lattice size N.\n\n        E0_per_N:      E0 / N\n        pE0_per_N_pg:  \\partial (E0 / N) / \\partial g\n        p2E0_per_N_pg2: \\partial2 (E0 / N) / \\partial g2\n        '
    g = self.g.detach().item()
    ks = (((np.linspace(((- (self.N - 1)) / 2), ((self.N - 1) / 2), num=N) / self.N) * 2) * np.pi)
    epsilon_ks = (2 * np.sqrt((((g ** 2) - ((2 * g) * np.cos(ks))) + 1)))
    pepsilon_ks_pg = ((4 * (g - np.cos(ks))) / epsilon_ks)
    p2epsilon_ks_pg2 = ((16 * (np.sin(ks) ** 2)) / (epsilon_ks ** 3))
    E0_per_N = (((- 0.5) * epsilon_ks.sum()) / self.N)
    pE0_per_N_pg = (((- 0.5) * pepsilon_ks_pg.sum()) / self.N)
    p2E0_per_N_pg2 = (((- 0.5) * p2epsilon_ks_pg2.sum()) / self.N)
    return (E0_per_N, pE0_per_N_pg, p2E0_per_N_pg2)
