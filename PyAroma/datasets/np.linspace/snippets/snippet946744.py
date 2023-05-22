import copy
import numpy as np
from scipy import interpolate
from PySide6 import QtGui, QtCore
from Utils import Utils
import GraphicsItemsCollection as gic
import GraphicsItem
import logging


def spline(self, x, y, points=200, degree=2, evaluate=False):
    'Interpolate spline through given points\n\n        Args:\n            spline (int, optional): Number of points on the spline\n            degree (int, optional): Degree of the spline\n            evaluate (bool, optional): If True, evaluate spline just at\n                                       the coordinates of the knots\n        '
    (tck, u) = interpolate.splprep([x, y], s=0.0, k=degree)
    t = np.linspace(0.0, 1.0, points)
    if evaluate:
        t = u
    coo = interpolate.splev(t, tck, der=0)
    der1 = interpolate.splev(t, tck, der=1)
    der2 = interpolate.splev(t, tck, der=2)
    spline_data = [coo, u, t, der1, der2, tck]
    return spline_data
