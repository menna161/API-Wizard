import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D


def _construct_meshgrid(left=(- 15), right=15, npoints=100):
    x = np.linspace(left, right, npoints)
    y = x.copy()
    (X, Y) = np.meshgrid(x, y)
    return (X, Y)
