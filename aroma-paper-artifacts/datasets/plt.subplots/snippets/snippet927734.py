from matplotlib import pyplot as plt
import numpy as np
import seaborn as sns


def getAxis(axis):
    if (axis is not False):
        ax = axis
        fig = ax.figure.canvas
    else:
        (fig, ax) = plt.subplots()
    return (fig, ax)
