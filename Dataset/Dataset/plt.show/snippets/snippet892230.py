from matplotlib import pyplot as plt
import math
from keras.callbacks import LambdaCallback
import keras.backend as K
import numpy as np


def plot_loss(self, n_skip_beginning=10, n_skip_end=5, x_scale='log'):
    '\n        Plots the loss.\n        Parameters:\n            n_skip_beginning - number of batches to skip on the left.\n            n_skip_end - number of batches to skip on the right.\n        '
    plt.ylabel('loss')
    plt.xlabel('learning rate (log scale)')
    plt.plot(self.lrs[n_skip_beginning:(- n_skip_end)], self.losses[n_skip_beginning:(- n_skip_end)])
    plt.xscale(x_scale)
    plt.show()
