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


def _draw_bbox(self, renderer, posx, posy):
    '\n        Update the location and size of the bbox (`.patches.FancyBboxPatch`),\n        and draw.\n        '
    (x_box, y_box, w_box, h_box) = _get_textbox(self, renderer)
    self._bbox_patch.set_bounds(0.0, 0.0, w_box, h_box)
    theta = np.deg2rad(self.get_rotation())
    tr = Affine2D().rotate(theta)
    tr = tr.translate((posx + x_box), (posy + y_box))
    self._bbox_patch.set_transform(tr)
    fontsize_in_pixel = renderer.points_to_pixels(self.get_size())
    self._bbox_patch.set_mutation_scale(fontsize_in_pixel)
    self._bbox_patch.draw(renderer)
