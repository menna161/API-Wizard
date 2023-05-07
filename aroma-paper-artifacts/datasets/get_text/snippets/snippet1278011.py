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


def get_label_width(self, lev, fmt, fsize):
    '\n        Return the width of the label in points.\n        '
    if (not isinstance(lev, str)):
        lev = self.get_text(lev, fmt)
    (lev, ismath) = text.Text.is_math_text(lev)
    if (ismath == 'TeX'):
        if (not hasattr(self, '_TeX_manager')):
            self._TeX_manager = texmanager.TexManager()
        (lw, _, _) = self._TeX_manager.get_text_width_height_descent(lev, fsize)
    elif ismath:
        if (not hasattr(self, '_mathtext_parser')):
            self._mathtext_parser = mathtext.MathTextParser('bitmap')
        (img, _) = self._mathtext_parser.parse(lev, dpi=72, prop=self.labelFontProps)
        lw = img.get_width()
    else:
        lw = ((len(lev) * fsize) * 0.6)
    return lw
