import os
import functools
import collections
import six
import packaging
import packaging.version
import numpy as np
import scipy
from scipy.optimize import minimize
import matplotlib.pyplot as plt
import sklearn
import FlowCal.plot
import FlowCal.transform
import FlowCal.stats
from sklearn.mixture import GaussianMixture
from sklearn.mixture import GMM


def plot_standard_curve(fl_rfi, fl_mef, beads_model, std_crv, xscale='linear', yscale='linear', xlim=None, ylim=(1.0, 100000000.0)):
    "\n    Plot a standard curve with fluorescence of calibration beads.\n\n    Parameters\n    ----------\n    fl_rfi : array_like\n        Fluorescence of the calibration beads' subpopulations, in RFI\n        units.\n    fl_mef : array_like\n        Fluorescence of the calibration beads' subpopulations, in MEF\n        units.\n    beads_model : function\n        Fluorescence model of the calibration beads.\n    std_crv : function\n        The standard curve, mapping relative fluorescence (RFI) units to\n        MEF units.\n\n    Other Parameters\n    ----------------\n    xscale : str, optional\n        Scale of the x axis, either ``linear`` or ``log``.\n    yscale : str, optional\n        Scale of the y axis, either ``linear`` or ``log``.\n    xlim : tuple, optional\n        Limits for the x axis.\n    ylim : tuple, optional\n        Limits for the y axis.\n\n    "
    plt.plot(fl_rfi, fl_mef, 'o', label='Beads', color=standard_curve_colors[0])
    if (xlim is None):
        xlim = plt.xlim()
    if (xscale == 'linear'):
        xdata = np.linspace(xlim[0], xlim[1], 200)
    elif (xscale == 'log'):
        xdata = np.logspace(np.log10(xlim[0]), np.log10(xlim[1]), 200)
    plt.plot(xdata, beads_model(xdata), label='Beads model', color=standard_curve_colors[1])
    plt.plot(xdata, std_crv(xdata), label='Standard curve', color=standard_curve_colors[2])
    plt.xscale(xscale)
    plt.yscale(yscale)
    plt.xlim(xlim)
    plt.ylim(ylim)
    plt.grid(True)
    plt.legend(loc='best')
