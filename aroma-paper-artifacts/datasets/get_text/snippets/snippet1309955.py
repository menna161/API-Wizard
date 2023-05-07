import codecs
import collections
from datetime import datetime
from functools import total_ordering
from io import BytesIO
import logging
from math import ceil, cos, floor, pi, sin
import os
import re
import struct
import sys
import time
import types
import warnings
import zlib
import numpy as np
from matplotlib import cbook, __version__, rcParams
from matplotlib._pylab_helpers import Gcf
from matplotlib.backend_bases import _Backend, FigureCanvasBase, FigureManagerBase, GraphicsContextBase, RendererBase
from matplotlib.backends.backend_mixed import MixedModeRenderer
from matplotlib.cbook import get_realpath_and_stat, is_writable_file_like, maxdict
from matplotlib.figure import Figure
from matplotlib.font_manager import findfont, is_opentype_cff_font, get_font
from matplotlib.afm import AFM
import matplotlib.type1font as type1font
import matplotlib.dviread as dviread
from matplotlib.ft2font import FIXED_WIDTH, ITALIC, LOAD_NO_SCALE, LOAD_NO_HINTING, KERNING_UNFITTED
from matplotlib.mathtext import MathTextParser
from matplotlib.transforms import Affine2D, BboxBase
from matplotlib.path import Path
from matplotlib.dates import UTC
from matplotlib import _path
from matplotlib import _png
from matplotlib import ttconv
from encodings import cp1252


def get_text_width_height_descent(self, s, prop, ismath):
    if rcParams['text.usetex']:
        texmanager = self.get_texmanager()
        fontsize = prop.get_size_in_points()
        (w, h, d) = texmanager.get_text_width_height_descent(s, fontsize, renderer=self)
        return (w, h, d)
    if ismath:
        (w, h, d, glyphs, rects, used_characters) = self.mathtext_parser.parse(s, 72, prop)
    elif rcParams['pdf.use14corefonts']:
        font = self._get_font_afm(prop)
        (l, b, w, h, d) = font.get_str_bbox_and_descent(s)
        scale = prop.get_size_in_points()
        w *= (scale / 1000)
        h *= (scale / 1000)
        d *= (scale / 1000)
    else:
        font = self._get_font_ttf(prop)
        font.set_text(s, 0.0, flags=LOAD_NO_HINTING)
        (w, h) = font.get_width_height()
        scale = (1.0 / 64.0)
        w *= scale
        h *= scale
        d = font.get_descent()
        d *= scale
    return (w, h, d)
