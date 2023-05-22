import torch
import numpy as np


def _diags(self):
    indices = np.arange(self.dim)[(:, np.newaxis)]
    bin_reps = ((indices >> np.arange(self.N)[::(- 1)]) & 1)
    spins = (1 - (2 * bin_reps))
    spins_prime = np.hstack((spins[(:, 1:)], spins[(:, 0:1)]))
    self.diag_elements = (- (spins * spins_prime).sum(axis=1))
    self.diag_elements = torch.from_numpy(self.diag_elements).to(torch.float64)
