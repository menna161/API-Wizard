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


def get_text(self):
    'Get the text as string'
    return self._text
