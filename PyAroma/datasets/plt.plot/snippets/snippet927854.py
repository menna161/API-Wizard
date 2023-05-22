from matplotlib import pyplot as plt
import numpy as np
import seaborn as sns


def lquart(x, y, label=[], axis=False):
    'Plots quartiles, x is a vector, y is a matrix with same length as x\n  '
    if (axis is not False):
        ax = axis
        fig = ax.figure.canvas
    else:
        (fig, ax) = plt.subplots()
    q = np.percentile(y, [25, 50, 75], axis=1)
    plt.plot(x, q[(1, :)], label=label)
    plt.plot(x, q[(0, :)], 'k:', alpha=0.5)
    plt.plot(x, q[(2, :)], 'k:', alpha=0.5)
    plt.fill_between(x, q[(0, :)], q[(2, :)], alpha=0.25)
    return ax
