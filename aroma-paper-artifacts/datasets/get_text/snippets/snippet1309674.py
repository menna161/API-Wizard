import numpy as np
from collections import OrderedDict
from math import radians, cos, sin
from matplotlib import cbook, rcParams, __version__
from matplotlib.backend_bases import _Backend, FigureCanvasBase, FigureManagerBase, RendererBase
from matplotlib.font_manager import findfont, get_font
from matplotlib.ft2font import LOAD_FORCE_AUTOHINT, LOAD_NO_HINTING, LOAD_DEFAULT, LOAD_NO_AUTOHINT
from matplotlib.mathtext import MathTextParser
from matplotlib.path import Path
from matplotlib.transforms import Bbox, BboxBase
from matplotlib import colors as mcolors
from matplotlib.backends._backend_agg import RendererAgg as _RendererAgg
from matplotlib import _png
from matplotlib.backend_bases import _has_pil
import threading
from PIL import Image
import dummy_threading as threading


def get_text_width_height_descent(self, s, prop, ismath):
    '\n        Get the width, height, and descent (offset from the bottom\n        to the baseline), in display coords, of the string *s* with\n        :class:`~matplotlib.font_manager.FontProperties` *prop*\n        '
    if (ismath in ['TeX', 'TeX!']):
        size = prop.get_size_in_points()
        texmanager = self.get_texmanager()
        fontsize = prop.get_size_in_points()
        (w, h, d) = texmanager.get_text_width_height_descent(s, fontsize, renderer=self)
        return (w, h, d)
    if ismath:
        (ox, oy, width, height, descent, fonts, used_characters) = self.mathtext_parser.parse(s, self.dpi, prop)
        return (width, height, descent)
    flags = get_hinting_flag()
    font = self._get_agg_font(prop)
    font.set_text(s, 0.0, flags=flags)
    (w, h) = font.get_width_height()
    d = font.get_descent()
    w /= 64.0
    h /= 64.0
    d /= 64.0
    return (w, h, d)
