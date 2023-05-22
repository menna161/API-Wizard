import torch
import scipy.special as sp
import matplotlib.pyplot as plt
import time

if (__name__ == '__main__'):
    import matplotlib.pyplot as plt
    import time
    n = 4
    x = torch.linspace((- 7), 7, 100, requires_grad=True)
    bessel = Bessel.apply
    for i in range(18):
        start = time.time()
        if (i == 0):
            y = bessel(n, x)
        else:
            (y,) = torch.autograd.grad(y, x, grad_outputs=torch.ones(y.shape[0]), create_graph=True)
        end = time.time()
        print(('The %dth derivative: %f' % (i, (end - start))))
        plt.plot(x.detach().numpy(), y.detach().numpy(), '-', label=('$%g$' % i))
    plt.legend()
    plt.show()
