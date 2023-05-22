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


def text_get_vertices_codes(self, prop, s, usetex):
    '\n        convert the string *s* to vertices and codes using the\n        provided font property *prop*. Mostly copied from\n        backend_svg.py.\n        '
    if usetex:
        (verts, codes) = text_to_path.get_text_path(prop, s, usetex=True)
    else:
        (clean_line, ismath) = self.is_math_text(s)
        (verts, codes) = text_to_path.get_text_path(prop, clean_line, ismath=ismath)
    return (verts, codes)
