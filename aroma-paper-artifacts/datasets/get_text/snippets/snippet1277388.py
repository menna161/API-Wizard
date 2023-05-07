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


def _get_text_path_transform(self, x, y, s, prop, angle, ismath):
    '\n        return the text path and transform\n\n        Parameters\n        ----------\n        prop : `matplotlib.font_manager.FontProperties`\n          font property\n\n        s : str\n          text to be converted\n\n        usetex : bool\n          If True, use matplotlib usetex mode.\n\n        ismath : bool\n          If True, use mathtext parser. If "TeX", use *usetex* mode.\n        '
    text2path = self._text2path
    fontsize = self.points_to_pixels(prop.get_size_in_points())
    if (ismath == 'TeX'):
        (verts, codes) = text2path.get_text_path(prop, s, ismath=False, usetex=True)
    else:
        (verts, codes) = text2path.get_text_path(prop, s, ismath=ismath, usetex=False)
    path = Path(verts, codes)
    angle = np.deg2rad(angle)
    if self.flipy():
        transform = Affine2D().scale((fontsize / text2path.FONT_SCALE), (fontsize / text2path.FONT_SCALE))
        transform = transform.rotate(angle).translate(x, (self.height - y))
    else:
        transform = Affine2D().scale((fontsize / text2path.FONT_SCALE), (fontsize / text2path.FONT_SCALE))
        transform = transform.rotate(angle).translate(x, y)
    return (path, transform)
