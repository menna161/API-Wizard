import atexit
import codecs
import errno
import logging
import math
import os
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile
import warnings
import weakref
import matplotlib as mpl
from matplotlib import _png, cbook, font_manager as fm, __version__, rcParams
from matplotlib.backend_bases import _Backend, FigureCanvasBase, FigureManagerBase, GraphicsContextBase, RendererBase
from matplotlib.backends.backend_mixed import MixedModeRenderer
from matplotlib.cbook import is_writable_file_like
from matplotlib.path import Path
from matplotlib.figure import Figure
from matplotlib._pylab_helpers import Gcf


def get_text_width_height_descent(self, s, prop, ismath):
    s = common_texification(s)
    (w, h, d) = self.latexManager.get_width_height_descent(s, prop)
    f = (mpl_pt_to_in * self.dpi)
    return ((w * f), (h * f), (d * f))
