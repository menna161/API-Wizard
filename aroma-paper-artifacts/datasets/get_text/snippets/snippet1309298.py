import collections.abc
import functools
import itertools
import logging
import math
from numbers import Number
import warnings
import numpy as np
from numpy import ma
import matplotlib
from matplotlib import _preprocess_data
import matplotlib.cbook as cbook
import matplotlib.collections as mcoll
import matplotlib.colors as mcolors
import matplotlib.contour as mcontour
import matplotlib.category as _
import matplotlib.dates as _
import matplotlib.docstring as docstring
import matplotlib.image as mimage
import matplotlib.legend as mlegend
import matplotlib.lines as mlines
import matplotlib.markers as mmarkers
import matplotlib.mlab as mlab
import matplotlib.path as mpath
import matplotlib.patches as mpatches
import matplotlib.quiver as mquiver
import matplotlib.stackplot as mstack
import matplotlib.streamplot as mstream
import matplotlib.table as mtable
import matplotlib.text as mtext
import matplotlib.ticker as mticker
import matplotlib.transforms as mtransforms
import matplotlib.tri as mtri
from matplotlib.cbook import MatplotlibDeprecationWarning, warn_deprecated, STEP_LOOKUP_MAP, iterable, safe_first_element
from matplotlib.container import BarContainer, ErrorbarContainer, StemContainer
from matplotlib.axes._base import _AxesBase, _process_plot_format
from builtins import range


def get_ylabel(self):
    '\n        Get the ylabel text string.\n        '
    label = self.yaxis.get_label()
    return label.get_text()
