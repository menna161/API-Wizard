import numpy as np
from matplotlib.animation import FuncAnimation
from matplotlib.font_manager import FontProperties
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from tadataka.plot.common import axis3d


def plot3d(P, *args, **kwargs):
    ax = axis3d()
    plot3d_(ax, P)
    plt.show()
