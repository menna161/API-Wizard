from nnunet.training.learning_rate.poly_lr import poly_lr
from nnunet.training.network_training.nnUNetTrainerV2 import nnUNetTrainerV2
import matplotlib.pyplot as plt


def plot_cycle_lr():
    xvals = list(range(1000))
    yvals = [cycle_lr(i, 100, 1e-06, 0.001) for i in xvals]
    plt.plot(xvals, yvals)
    plt.show()
    plt.savefig('/home/fabian/temp.png')
    plt.close()
