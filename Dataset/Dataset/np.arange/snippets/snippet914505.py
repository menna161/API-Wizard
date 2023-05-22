import numpy as np
import scipy.sparse.linalg as sparselinalg
import torch
from DominantSparseEigenAD.eig import DominantEig
import DominantSparseEigenAD.eig as eig
import time

if (__name__ == '__main__'):
    import time
    data_E0 = np.load('datas/E0_sum.npz')
    gs = data_E0['gs']
    E0s = data_E0['E0s']
    for g_idx in [3, 4, 5]:
        (g, E0) = (gs[g_idx], E0s[g_idx])
        print(('g = %f, E0 = %.15f' % (g, E0)))
        Ds = np.arange(5, (100 + 1), step=5)
        ks = np.array(([10, 50, 80, 80, 100, 100] + ([200] * 14)))
        Npoints = Ds.size
        E0s_general = np.empty(Npoints)

        def closure():
            E0 = model.sparse_forward()
            optimizer.zero_grad()
            E0.backward()
            return E0
        initA = None
        for i in range(Npoints):
            (D, k) = (Ds[i], ks[i])
            model = TFIM(D, k)
            model.seth(g)
            model.setparameters(initA=initA)
            optimizer = torch.optim.LBFGS(model.parameters(), max_iter=20, tolerance_grad=0.0, tolerance_change=0.0, line_search_fn='strong_wolfe')
            iter_num = 60
            for epoch in range(iter_num):
                start = time.time()
                E0 = optimizer.step(closure)
                end = time.time()
                print('iter: ', epoch, E0.item(), (end - start))
                if (epoch == (iter_num - 1)):
                    E0s_general[i] = E0.detach().numpy()
                    if (i != (Npoints - 1)):
                        Dnew = Ds[(i + 1)]
                        initA = (1.0 * torch.randn(model.d, Dnew, Dnew, dtype=torch.float64))
                        initA[(:, :D, :D)] = model.A.detach()
        for i in range(Npoints):
            print(('D = %d: \t%.15f' % (Ds[i], E0s_general[i])))
        filename = ('datas/E0s_general/g_%.2f.npz' % g)
        np.savez(filename, Ds=Ds, E0s=E0s_general)
