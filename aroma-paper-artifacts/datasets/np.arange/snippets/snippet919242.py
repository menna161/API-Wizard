import numpy as np
from sphericalpolygon import create_polygon
from pyshtools.spectralanalysis import Curve2Mask
from ..ggclasses.class_Nodes import Nodes


def med(x):
    '\n    Calculate the middle divisor. This program is used to determine the optimal grid line spacing for regional maps.\n\n    Usage: \n    y = med(x)\n    \n    Inputs:\n    x -> [int] The longitude or latitude span of a map. It cannot be a prime number.\n\n    Outputs:\n    y -> [int] the optimal grid line spacing\n\n    Examples:\n    >>> print(med(20))\n    4\n    >>> print(med(25))\n    5\n    '
    y = np.unique(np.gcd(np.arange(x), x))
    n = len(y)
    if ((n % 2) == 1):
        return y[(n // 2)]
    else:
        return y[((n // 2) - 1)]
