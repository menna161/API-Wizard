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


def get_window_extent(self, renderer=None, dpi=None):
    '\n        Return the `Bbox` bounding the text, in display units.\n\n        In addition to being used internally, this is useful for specifying\n        clickable regions in a png file on a web page.\n\n        Parameters\n        ----------\n        renderer : Renderer, optional\n            A renderer is needed to compute the bounding box.  If the artist\n            has already been drawn, the renderer is cached; thus, it is only\n            necessary to pass this argument when calling `get_window_extent`\n            before the first `draw`.  In practice, it is usually easier to\n            trigger a draw first (e.g. by saving the figure).\n\n        dpi : float, optional\n            The dpi value for computing the bbox, defaults to\n            ``self.figure.dpi`` (*not* the renderer dpi); should be set e.g. if\n            to match regions with a figure saved with a custom dpi value.\n        '
    if (not self.get_visible()):
        return Bbox.unit()
    if (dpi is not None):
        dpi_orig = self.figure.dpi
        self.figure.dpi = dpi
    if (self.get_text() == ''):
        (tx, ty) = self._get_xy_display()
        return Bbox.from_bounds(tx, ty, 0, 0)
    if (renderer is not None):
        self._renderer = renderer
    if (self._renderer is None):
        self._renderer = self.figure._cachedRenderer
    if (self._renderer is None):
        raise RuntimeError('Cannot get window extent w/o renderer')
    (bbox, info, descent) = self._get_layout(self._renderer)
    (x, y) = self.get_unitless_position()
    (x, y) = self.get_transform().transform_point((x, y))
    bbox = bbox.translated(x, y)
    if (dpi is not None):
        self.figure.dpi = dpi_orig
    return bbox
