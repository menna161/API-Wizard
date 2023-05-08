from matplotlib import pyplot as plt
import numpy as np
import seaborn as sns
import torch


def lineplot(x, y, filename, xaxis='Steps', yaxis='Returns'):
    y = np.array(y)
    (y_mean, y_std) = (y.mean(axis=1), y.std(axis=1))
    sns.lineplot(x=x, y=y_mean, color='coral')
    plt.fill_between(x, (y_mean - y_std), (y_mean + y_std), color='coral', alpha=0.3)
    plt.xlim(left=0, right=x[(- 1)])
    plt.xlabel(xaxis)
    plt.ylabel(yaxis)
    plt.savefig(f'{filename}.png')
    plt.close()
