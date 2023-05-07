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


@cbook.deprecated('2.2')
def get_real_label_width(self, lev, fmt, fsize):
    '\n        This computes actual onscreen label width.\n        This uses some black magic to determine onscreen extent of non-drawn\n        label.  This magic may not be very robust.\n\n        This method is not being used, and may be modified or removed.\n        '
    xx = np.mean(np.asarray(self.ax.axis()).reshape(2, 2), axis=1)
    t = text.Text(xx[0], xx[1])
    self.set_label_props(t, self.get_text(lev, fmt), 'k')
    bbox = t.get_window_extent(renderer=self.ax.figure.canvas.renderer)
    lw = np.diff(bbox.corners()[(0::2, 0)])[0]
    return lw
