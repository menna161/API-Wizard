import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation


def plot(self, marker=''):
    (fig, ax) = plt.subplots()
    ax.set_aspect('equal')
    for state in self.trajectory:
        plt.plot(state[0], state[1], marker=marker, color='black')
    plt.gca().axes.xaxis.set_ticklabels([])
    plt.gca().axes.yaxis.set_ticklabels([])
    plt.xticks([])
    plt.yticks([])
    plt.show()
