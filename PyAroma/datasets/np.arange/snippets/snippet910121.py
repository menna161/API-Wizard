import packaging
import packaging.version
import collections
import numpy as np
import scipy.ndimage.filters
import matplotlib
import matplotlib.scale
import matplotlib.transforms
import matplotlib.ticker
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.font_manager import FontProperties
import warnings


def set_default_locators_and_formatters(self, axis):
    '\n        Set up the locators and formatters for the scale.\n\n        Parameters\n        ----------\n        axis: matplotlib.axis\n            Axis for which to set locators and formatters.\n\n        '
    axis.set_major_locator(_LogicleLocator(self._transform))
    axis.set_minor_locator(_LogicleLocator(self._transform, subs=np.arange(2.0, 10.0)))
    axis.set_major_formatter(matplotlib.ticker.LogFormatterSciNotation(labelOnlyBase=True))
