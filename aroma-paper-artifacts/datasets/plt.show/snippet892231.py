from matplotlib import pyplot as plt
import math
from keras.callbacks import LambdaCallback
import keras.backend as K
import numpy as np


def plot_loss_change(self, sma=1, n_skip_beginning=10, n_skip_end=5, y_lim=((- 0.01), 0.01)):
    '\n        Plots rate of change of the loss function.\n        Parameters:\n            sma - number of batches for simple moving average to smooth out the curve.\n            n_skip_beginning - number of batches to skip on the left.\n            n_skip_end - number of batches to skip on the right.\n            y_lim - limits for the y axis.\n        '
    derivatives = self.get_derivatives(sma)[n_skip_beginning:(- n_skip_end)]
    lrs = self.lrs[n_skip_beginning:(- n_skip_end)]
    plt.ylabel('rate of loss change')
    plt.xlabel('learning rate (log scale)')
    plt.plot(lrs, derivatives)
    plt.xscale('log')
    plt.ylim(y_lim)
    plt.show()
