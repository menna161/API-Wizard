from contextlib import contextmanager
import importlib
import io
import os
import sys
import time
import warnings
from weakref import WeakKeyDictionary
import numpy as np
from matplotlib import backend_tools as tools, cbook, colors, textpath, tight_bbox, transforms, widgets, get_backend, is_interactive, rcParams
from matplotlib._pylab_helpers import Gcf
from matplotlib.transforms import Bbox, TransformedBbox, Affine2D
from matplotlib.path import Path
from PIL import Image
from PIL import PILLOW_VERSION
from distutils.version import LooseVersion
from matplotlib.collections import QuadMesh
import sys
from matplotlib.figure import Figure
from matplotlib.texmanager import TexManager
from matplotlib import pyplot


def get_text_width_height_descent(self, s, prop, ismath):
    '\n        Get the width, height, and descent (offset from the bottom\n        to the baseline), in display coords, of the string *s* with\n        :class:`~matplotlib.font_manager.FontProperties` *prop*\n        '
    if (ismath == 'TeX'):
        size = prop.get_size_in_points()
        texmanager = self._text2path.get_texmanager()
        fontsize = prop.get_size_in_points()
        (w, h, d) = texmanager.get_text_width_height_descent(s, fontsize, renderer=self)
        return (w, h, d)
    dpi = self.points_to_pixels(72)
    if ismath:
        dims = self._text2path.mathtext_parser.parse(s, dpi, prop)
        return dims[0:3]
    flags = self._text2path._get_hinting_flag()
    font = self._text2path._get_font(prop)
    size = prop.get_size_in_points()
    font.set_size(size, dpi)
    font.set_text(s, 0.0, flags=flags)
    (w, h) = font.get_width_height()
    d = font.get_descent()
    w /= 64.0
    h /= 64.0
    d /= 64.0
    return (w, h, d)
