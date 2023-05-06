import math
import numpy as np
import matplotlib.pyplot as plt
from torch.optim.lr_scheduler import LambdaLR
from utils.torch import set_optimizer_mom


def plot_schedules(self):
    x = np.linspace(0, self.n_epochs, self.n_iter)
    (_, ax) = plt.subplots(1, 2, figsize=(15, 4))
    ax[0].set_title('LR Schedule')
    ax[0].set_ylabel('lr')
    ax[0].set_xlabel('epoch')
    ax[0].plot(x, self.lrs)
    ax[1].set_title('Momentum Schedule')
    ax[1].set_ylabel('momentum')
    ax[1].set_xlabel('epoch')
    ax[1].plot(x, self.moms)
