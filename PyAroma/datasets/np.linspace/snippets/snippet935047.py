import numpy as np
from scipy.misc import comb


def bezier_curve(points, nTimes=1000):
    '\n       Given a set of control points, return the\n       bezier curve defined by the control points.\n\n       points should be a list of lists, or list of tuples\n       such as [ [1,1],\n                 [2,3],\n                 [4,5], ..[Xn, Yn] ]\n        nTimes is the number of time steps, defaults to 1000\n\n        See http://processingjs.nihongoresources.com/bezierinfo/\n    '
    nPoints = len(points)
    xPoints = np.array([p[0] for p in points])
    yPoints = np.array([p[1] for p in points])
    t = np.linspace(0.0, 1.0, nTimes)
    polynomial_array = np.array([bernstein_poly(i, (nPoints - 1), t) for i in range(0, nPoints)])
    xvals = np.dot(xPoints, polynomial_array)
    yvals = np.dot(yPoints, polynomial_array)
    return (xvals, yvals)
