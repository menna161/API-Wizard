from matplotlib import pyplot as plt
import numpy as np
import seaborn as sns


def lplot(*args, label=[], axis=False):
    'Plots an vector, a set of vectors, with or without an x scale\n  '
    (fig, ax) = getAxis(axis)
    if (len(args) == 1):
        x = np.arange(np.shape(args)[1])
        y = args[0]
    if (len(args) == 2):
        x = args[0]
        y = args[1]
    if (np.ndim(y) == 2):
        for i in range(np.shape(y)[1]):
            ax.plot(x, y[(:, i)], '-')
            if (len(label) > 0):
                ax.legend(label)
    else:
        ax.plot(x, y, 'o-')
    if (axis is False):
        return (fig, ax)
    else:
        return ax
