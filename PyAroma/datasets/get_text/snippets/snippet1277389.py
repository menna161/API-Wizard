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


def _draw_text_as_path(self, gc, x, y, s, prop, angle, ismath):
    '\n        draw the text by converting them to paths using textpath module.\n\n        Parameters\n        ----------\n        prop : `matplotlib.font_manager.FontProperties`\n          font property\n\n        s : str\n          text to be converted\n\n        usetex : bool\n          If True, use matplotlib usetex mode.\n\n        ismath : bool\n          If True, use mathtext parser. If "TeX", use *usetex* mode.\n        '
    (path, transform) = self._get_text_path_transform(x, y, s, prop, angle, ismath)
    color = gc.get_rgb()
    gc.set_linewidth(0.0)
    self.draw_path(gc, path, transform, rgbFace=color)
