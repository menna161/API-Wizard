import numpy as np
import torch
import DominantSparseEigenAD.symeig as symeig
import matplotlib.pyplot as plt
import time

if (__name__ == '__main__'):
    (xmin, xmax, N) = ((- 1.0), 1.0, 300)
    xmesh = np.linspace(xmin, xmax, num=N, endpoint=False)
    k = 300
    target = np.zeros(N)
    idx = (np.abs(xmesh) < 0.5)
    target[idx] = (1.0 - np.abs(xmesh[idx]))
    target /= np.linalg.norm(target)
    xmesh = torch.from_numpy(xmesh).to(torch.float64)
    target = torch.from_numpy(target).to(torch.float64)
    model = Schrodinger1D(xmin, xmax, N, xmesh)
    optimizer = torch.optim.LBFGS(model.parameters(), max_iter=10, tolerance_change=1e-07, tolerance_grad=1e-07, line_search_fn='strong_wolfe')

    def closure():
        import time
        optimizer.zero_grad()
        start1 = time.time()
        loss = model.forward_sparseAD(target, k)
        end1 = time.time()
        start2 = time.time()
        loss.backward()
        end2 = time.time()
        print('forward time: ', (end1 - start1), 'backward time: ', (end2 - start2))
        return loss
    plt.ion()
    for i in range(50):
        loss = optimizer.step(closure)
        print(i, loss.item())
        model.plot(target)
        plt.pause(0.01)
    plt.ioff()
    model.plot(target)
    plt.show()
