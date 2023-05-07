from math import pi, sqrt
import numpy as np
from scipy.constants import physical_constants, speed_of_light


def plot_dielectric_functions(dielectric, ax=None):
    real_dielectric = parse_dielectric_data(dielectric[1])
    imag_dielectric = parse_dielectric_data(dielectric[2])
    if (ax is None):
        (fig, ax) = plt.subplots(1, 1, figsize=(6.0, 3.0))
    else:
        fig = None
    ax.plot(dielectric[0], np.mean(real_dielectric, axis=1), '-', zorder=2)
    ax.plot(dielectric[0], np.mean(imag_dielectric, axis=1), '-', zorder=2)
    ax.set_xlim([0, 8])
    ax.set_ylim([0, 5])
    return fig
