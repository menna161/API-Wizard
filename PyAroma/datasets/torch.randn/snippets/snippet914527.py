import torch
import numpy as np


def setHmatrix(self):
    diagmatrix = torch.diag(self.diag_elements)
    offdiagmatrix = torch.zeros(self.dim, self.dim).to(torch.float64)
    offdiagmatrix[(self.flips_basis.T, torch.arange(self.dim))] = 1.0
    randommatrix = (1e-12 * torch.randn(model.dim, model.dim).to(torch.float64))
    randommatrix = (0.5 * (randommatrix + randommatrix.T))
    self.Hmatrix = ((diagmatrix - (self.g * offdiagmatrix)) + randommatrix)
