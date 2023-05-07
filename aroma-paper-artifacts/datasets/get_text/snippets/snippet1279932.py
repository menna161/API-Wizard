import contextlib
import logging
import math
import warnings
import weakref
import numpy as np
from . import artist, cbook, docstring, rcParams
from .artist import Artist
from .font_manager import FontProperties
from .lines import Line2D
from .patches import FancyArrowPatch, FancyBboxPatch, Rectangle
from .textpath import TextPath
from .transforms import Affine2D, Bbox, BboxBase, BboxTransformTo, IdentityTransform, Transform
from matplotlib.offsetbox import DraggableAnnotation
from matplotlib.transforms import blended_transform_factory
from matplotlib.transforms import Affine2D
from matplotlib.projections import PolarAxes
from matplotlib.patheffects import PathEffectRenderer


def get_prop_tup(self, renderer=None):
    '\n        Return a hashable tuple of properties.\n\n        Not intended to be human readable, but useful for backends who\n        want to cache derived information about text (e.g., layouts) and\n        need to know if the text has changed.\n        '
    (x, y) = self.get_unitless_position()
    renderer = (renderer or self._renderer)
    return (x, y, self.get_text(), self._color, self._verticalalignment, self._horizontalalignment, hash(self._fontproperties), self._rotation, self._rotation_mode, self.figure.dpi, weakref.ref(renderer), self._linespacing)
