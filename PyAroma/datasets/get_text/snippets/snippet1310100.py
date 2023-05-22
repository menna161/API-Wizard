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


def draw_tex(self, gc, x, y, s, prop, angle, ismath='TeX!', mtext=None):
    '\n        draw a Text instance\n        '
    (w, h, bl) = self.get_text_width_height_descent(s, prop, ismath)
    fontsize = prop.get_size_in_points()
    thetext = ('psmarker%d' % self.textcnt)
    color = ('%1.3f,%1.3f,%1.3f' % gc.get_rgb()[:3])
    fontcmd = {'sans-serif': '{\\sffamily %s}', 'monospace': '{\\ttfamily %s}'}.get(rcParams['font.family'][0], '{\\rmfamily %s}')
    s = (fontcmd % s)
    tex = ('\\color[rgb]{%s} %s' % (color, s))
    corr = 0
    if rcParams['text.latex.preview']:
        pos = _nums_to_str((x - corr), y)
        self.psfrag.append(('\\psfrag{%s}[Bl][Bl][1][%f]{\\fontsize{%f}{%f}%s}' % (thetext, angle, fontsize, (fontsize * 1.25), tex)))
    else:
        pos = _nums_to_str((x - corr), (y - bl))
        self.psfrag.append(('\\psfrag{%s}[bl][bl][1][%f]{\\fontsize{%f}{%f}%s}' % (thetext, angle, fontsize, (fontsize * 1.25), tex)))
    ps = ('gsave\n%(pos)s moveto\n(%(thetext)s)\nshow\ngrestore\n    ' % locals())
    self._pswriter.write(ps)
    self.textcnt += 1
