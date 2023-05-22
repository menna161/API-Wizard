import torch
import numpy as np

if (__name__ == '__main__'):
    N = 6
    model = TFIM(N)
    for g in np.linspace(0.0, 2.0, num=21):
        model.g = torch.Tensor([g]).to(torch.float64)
        model.g.requires_grad_(True)
        model.setHmatrix()
        (Es, psis) = torch.symeig(model.Hmatrix, eigenvectors=True)
        E0 = Es[0]
        (dE0,) = torch.autograd.grad(E0, model.g, create_graph=True)
        (d2E0,) = torch.autograd.grad(dE0, model.g)
        print(g, (E0.item() / model.N), (dE0.item() / model.N), (d2E0.item() / model.N))
