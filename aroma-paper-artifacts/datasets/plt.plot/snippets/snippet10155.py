import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation


def update(t):
    plt.plot(self.trajectory[t][0], self.trajectory[t][1], marker=marker, color='black')
    if ((t == (len(self.trajectory) - 1)) and repeat):
        ax.clear()
        ax.xaxis.set_ticklabels([])
        ax.yaxis.set_ticklabels([])
        ax.set_xticks([])
        ax.set_yticks([])
        plt.xlim(min_x, max_x)
        plt.ylim(min_y, max_y)
