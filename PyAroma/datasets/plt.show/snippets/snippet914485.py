import numpy as np
import torch
from TFIM import TFIM
from DominantSparseEigenAD.symeig import DominantSymeig
import DominantSparseEigenAD.symeig as symeig
import matplotlib.pyplot as plt

if (__name__ == '__main__'):
    N = 10
    device = torch.device('cpu')
    model = TFIM(N, device)
    k = 300
    Npoints = 100
    gs = np.linspace(0.5, 1.5, num=Npoints)
    E0s_analytic = np.empty(Npoints)
    E0s_torchAD = np.empty(Npoints)
    E0s_matrixAD = np.empty(Npoints)
    E0s_sparseAD = np.empty(Npoints)
    dE0s_analytic = np.empty(Npoints)
    dE0s_torchAD = np.empty(Npoints)
    dE0s_matrixAD = np.empty(Npoints)
    dE0s_sparseAD = np.empty(Npoints)
    d2E0s_analytic = np.empty(Npoints)
    d2E0s_torchAD = np.empty(Npoints)
    d2E0s_matrixAD = np.empty(Npoints)
    d2E0s_sparseAD = np.empty(Npoints)
    print('g    E0_analytic    E0_torchAD    E0_matrixAD    E0_sparseAD    dE0_analytic    dE0_torchAD    dE0_matrixAD    dE0_sparseAD    d2E0_analytic    d2E0_torchAD    d2E0_matrixAD    d2E0_sparseAD')
    for i in range(Npoints):
        model.g = torch.Tensor([gs[i]]).to(model.device, dtype=torch.float64)
        model.g.requires_grad_(True)
        (E0s_analytic[i], dE0s_analytic[i], d2E0s_analytic[i]) = E0_analytic(model)
        model.setHmatrix()
        (E0s_torchAD[i], dE0s_torchAD[i], d2E0s_torchAD[i]) = E0_torchAD(model)
        (E0s_matrixAD[i], dE0s_matrixAD[i], d2E0s_matrixAD[i]) = E0_matrixAD(model, k)
        (E0s_sparseAD[i], dE0s_sparseAD[i], d2E0s_sparseAD[i]) = E0_sparseAD(model, k)
        print(gs[i], E0s_analytic[i], E0s_torchAD[i], E0s_matrixAD[i], E0s_sparseAD[i], dE0s_analytic[i], dE0s_torchAD[i], dE0s_matrixAD[i], dE0s_sparseAD[i], d2E0s_analytic[i], d2E0s_torchAD[i], d2E0s_matrixAD[i], d2E0s_sparseAD[i])
    import matplotlib.pyplot as plt
    plt.plot(gs, E0s_analytic, label='Analytic result')
    plt.plot(gs, E0s_torchAD, label='AD: torch')
    plt.plot(gs, E0s_matrixAD, label='AD: normal representation')
    plt.plot(gs, E0s_sparseAD, label='AD: sparse representation')
    plt.legend()
    plt.xlabel('$g$')
    plt.ylabel('$\\frac{E_0}{N}$')
    plt.title(('Ground state energy per site of 1D TFIM\n$H = - \\sum_{i=0}^{N-1} (g\\sigma_i^x + \\sigma_i^z \\sigma_{i+1}^z)$\n$N=%d$' % model.N))
    plt.show()
    plt.plot(gs, dE0s_analytic, label='Analytic result')
    plt.plot(gs, dE0s_torchAD, label='AD: torch')
    plt.plot(gs, dE0s_matrixAD, label='AD: normal representation')
    plt.plot(gs, dE0s_sparseAD, label='AD: sparse representation')
    plt.legend()
    plt.xlabel('$g$')
    plt.ylabel('$\\frac{1}{N} \\frac{\\partial E_0}{\\partial g}$')
    plt.title(('1st derivative w.r.t. $g$ of ground state energy per site of 1D TFIM\n$H = - \\sum_{i=0}^{N-1} (g\\sigma_i^x + \\sigma_i^z \\sigma_{i+1}^z)$\n$N=%d$' % model.N))
    plt.show()
    plt.plot(gs, d2E0s_analytic, label='Analytic result')
    plt.plot(gs, d2E0s_torchAD, label='AD: torch')
    plt.plot(gs, d2E0s_matrixAD, label='AD: normal representation')
    plt.plot(gs, d2E0s_sparseAD, label='AD: sparse representation')
    plt.legend()
    plt.xlabel('$g$')
    plt.ylabel('$\\frac{1}{N} \\frac{\\partial^2 E_0}{\\partial g^2}$')
    plt.title(('2nd derivative w.r.t. $g$ of ground state energy per site of 1D TFIM\n$H = - \\sum_{i=0}^{N-1} (g\\sigma_i^x + \\sigma_i^z \\sigma_{i+1}^z)$\n$N=%d$' % model.N))
    plt.show()
