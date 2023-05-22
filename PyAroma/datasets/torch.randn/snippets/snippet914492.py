import numpy as np
import torch


def setHmatrix(self):
    '\n            Set the Hamiltonian of the model, which is a (Hermitian) square matrix\n        represented as a normal torch Tensor.\n            The resulting Hamiltonian matrix is stored in `self.Hmatrix`.\n\n        Note: The applicability of this method is limited by Lattice size N. \n            To construct the Hamiltonian for larger N(~> 10, say), use\n            the method `H` below.\n        '
    diagmatrix = torch.diag(self.diag_elements)
    offdiagmatrix = torch.zeros(self.dim, self.dim).to(self.device, dtype=torch.float64)
    offdiagmatrix[(self.flips_basis.T, torch.arange(self.dim).to(self.device))] = (- self.g)
    randommatrix = (1e-12 * torch.randn(self.dim, self.dim).to(self.device, dtype=torch.float64))
    randommatrix = (0.5 * (randommatrix + randommatrix.T))
    self.Hmatrix = ((diagmatrix + offdiagmatrix) + randommatrix)
