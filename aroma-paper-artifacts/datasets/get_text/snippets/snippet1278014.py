from numbers import Integral
import warnings
import numpy as np
from numpy import ma
import matplotlib as mpl
import matplotlib._contour as _contour
import matplotlib.path as mpath
import matplotlib.ticker as ticker
import matplotlib.cm as cm
import matplotlib.colors as mcolors
import matplotlib.collections as mcoll
import matplotlib.font_manager as font_manager
import matplotlib.text as text
import matplotlib.cbook as cbook
import matplotlib.mathtext as mathtext
import matplotlib.patches as mpatches
import matplotlib.texmanager as texmanager
import matplotlib.transforms as mtransforms
from matplotlib.blocking_input import BlockingContourLabeler


def get_text(self, lev, fmt):
    'Get the text of the label.'
    if isinstance(lev, str):
        return lev
    elif isinstance(fmt, dict):
        return fmt.get(lev, '%1.3f')
    elif callable(fmt):
        return fmt(lev)
    else:
        return (fmt % lev)
