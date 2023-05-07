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


def draw_tex(self, gc, x, y, s, prop, angle, ismath='TeX!', mtext=None):
    size = prop.get_size_in_points()
    texmanager = self.get_texmanager()
    Z = texmanager.get_grey(s, size, self.dpi)
    Z = np.array((Z * 255.0), np.uint8)
    (w, h, d) = self.get_text_width_height_descent(s, prop, ismath)
    xd = (d * sin(radians(angle)))
    yd = (d * cos(radians(angle)))
    x = np.round((x + xd))
    y = np.round((y + yd))
    self._renderer.draw_text_image(Z, x, y, angle, gc)
