import binascii
import datetime
import glob
from io import StringIO, TextIOWrapper
import logging
import os
import pathlib
import re
import shutil
import subprocess
import sys
from tempfile import TemporaryDirectory
import time
import numpy as np
from matplotlib import cbook, __version__, rcParams, checkdep_ghostscript
from matplotlib.afm import AFM
from matplotlib.backend_bases import _Backend, FigureCanvasBase, FigureManagerBase, GraphicsContextBase, RendererBase
from matplotlib.cbook import get_realpath_and_stat, is_writable_file_like, maxdict, file_requires_unicode
from matplotlib.font_manager import findfont, is_opentype_cff_font, get_font
from matplotlib.ft2font import KERNING_DEFAULT, LOAD_NO_HINTING
from matplotlib.ttconv import convert_ttf_to_ps
from matplotlib.mathtext import MathTextParser
from matplotlib._mathtext_data import uni2type1
from matplotlib.path import Path
from matplotlib import _path
from matplotlib.transforms import Affine2D
from matplotlib.backends.backend_mixed import MixedModeRenderer


def get_text_width_height_descent(self, s, prop, ismath):
    '\n        get the width and height in display coords of the string s\n        with FontPropertry prop\n\n        '
    if rcParams['text.usetex']:
        texmanager = self.get_texmanager()
        fontsize = prop.get_size_in_points()
        (w, h, d) = texmanager.get_text_width_height_descent(s, fontsize, renderer=self)
        return (w, h, d)
    if ismath:
        (width, height, descent, pswriter, used_characters) = self.mathtext_parser.parse(s, 72, prop)
        return (width, height, descent)
    if rcParams['ps.useafm']:
        if ismath:
            s = s[1:(- 1)]
        font = self._get_font_afm(prop)
        (l, b, w, h, d) = font.get_str_bbox_and_descent(s)
        fontsize = prop.get_size_in_points()
        scale = (0.001 * fontsize)
        w *= scale
        h *= scale
        d *= scale
        return (w, h, d)
    font = self._get_font_ttf(prop)
    font.set_text(s, 0.0, flags=LOAD_NO_HINTING)
    (w, h) = font.get_width_height()
    w /= 64.0
    h /= 64.0
    d = font.get_descent()
    d /= 64.0
    return (w, h, d)
