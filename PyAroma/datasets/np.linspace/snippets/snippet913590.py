import matplotlib.pyplot as plt
import numpy as np
import math
import mplcyberpunk


def plot_colored_sinusoidal_lines(ax):
    'Plot sinusoidal lines with colors following the style color cycle.\n    '
    L = (2 * np.pi)
    x = np.linspace(0, L)
    nb_colors = len(plt.rcParams['axes.prop_cycle'])
    shift = np.linspace(0, L, nb_colors, endpoint=False)
    for s in shift:
        ax.plot(x, np.sin((x + s)), '-')
    ax.set_xlim([x[0], x[(- 1)]])
    return ax
