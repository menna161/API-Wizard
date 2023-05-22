import numpy as np
import torch
from DominantSparseEigenAD.Lanczos import symeigLanczos
import matplotlib.pyplot as plt

if (__name__ == '__main__'):
    N = 300
    ks = np.arange(10, (N + 1), step=2)
    Hmatrix = H1(N)
    (E0s, _) = torch.symeig(Hmatrix, eigenvectors=True)
    E0_groundtruth = E0s[0].item()
    E0s_lanczos = np.empty(ks.size)
    relative_error = np.empty(ks.size)
    for i in range(ks.size):
        (E0s_lanczos[i], _) = symeigLanczos(Hmatrix, ks[i], extreme='min')
        relative_error[i] = np.log10((np.abs((E0s_lanczos[i] - E0_groundtruth)) / np.abs(E0_groundtruth)))
        print('k = ', ks[i], relative_error[i])
    import matplotlib.pyplot as plt
    plt.plot(ks, relative_error)
    plt.title(('Log relative error of the minimum eigenvalue using various numbers of Lanczos vectors $k$\nDimension of the matrix being diagonalized: %d' % N))
    plt.xlabel('$k$')
    plt.ylabel('Log relative error')
    plt.show()
