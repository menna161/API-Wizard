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


@contextlib.contextmanager
def _wrap_text(textobj):
    'Temporarily inserts newlines to the text if the wrap option is enabled.\n    '
    if textobj.get_wrap():
        old_text = textobj.get_text()
        try:
            textobj.set_text(textobj._get_wrapped_text())
            (yield textobj)
        finally:
            textobj.set_text(old_text)
    else:
        (yield textobj)
