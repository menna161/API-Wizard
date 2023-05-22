from collections import OrderedDict
import base64
import gzip
import hashlib
import io
import logging
import re
import uuid
import numpy as np
from matplotlib import cbook, __version__, rcParams
from matplotlib.backend_bases import _Backend, FigureCanvasBase, FigureManagerBase, RendererBase
from matplotlib.backends.backend_mixed import MixedModeRenderer
from matplotlib.colors import rgb2hex
from matplotlib.font_manager import findfont, get_font
from matplotlib.ft2font import LOAD_NO_HINTING
from matplotlib.mathtext import MathTextParser
from matplotlib.path import Path
from matplotlib import _path
from matplotlib.transforms import Affine2D, Affine2DBase
from matplotlib import _png


def get_text_width_height_descent(self, s, prop, ismath):
    return self._text2path.get_text_width_height_descent(s, prop, ismath)
