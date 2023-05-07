from collections import OrderedDict
import functools
import urllib.parse
import warnings
import numpy as np
from matplotlib import cbook, dviread, font_manager, rcParams
from matplotlib.font_manager import FontProperties, get_font
from matplotlib.ft2font import KERNING_DEFAULT, LOAD_NO_HINTING, LOAD_TARGET_LIGHT
from matplotlib.mathtext import MathTextParser
from matplotlib.path import Path
from matplotlib.transforms import Affine2D
from matplotlib.texmanager import TexManager


def get_text_width_height_descent(self, s, prop, ismath):
    if rcParams['text.usetex']:
        texmanager = self.get_texmanager()
        fontsize = prop.get_size_in_points()
        (w, h, d) = texmanager.get_text_width_height_descent(s, fontsize, renderer=None)
        return (w, h, d)
    fontsize = prop.get_size_in_points()
    scale = (fontsize / self.FONT_SCALE)
    if ismath:
        prop = prop.copy()
        prop.set_size(self.FONT_SCALE)
        (width, height, descent, trash, used_characters) = self.mathtext_parser.parse(s, 72, prop)
        return ((width * scale), (height * scale), (descent * scale))
    font = self._get_font(prop)
    font.set_text(s, 0.0, flags=LOAD_NO_HINTING)
    (w, h) = font.get_width_height()
    w /= 64.0
    h /= 64.0
    d = font.get_descent()
    d /= 64.0
    return ((w * scale), (h * scale), (d * scale))
