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


def _add_label(self, t, x, y, lev, cvalue):
    color = self.labelMappable.to_rgba(cvalue, alpha=self.alpha)
    _text = self.get_text(lev, self.labelFmt)
    self.set_label_props(t, _text, color)
    self.labelTexts.append(t)
    self.labelCValues.append(cvalue)
    self.labelXYs.append((x, y))
    self.ax.add_artist(t)
