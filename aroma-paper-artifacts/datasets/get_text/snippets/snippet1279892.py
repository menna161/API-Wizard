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


def _get_textbox(text, renderer):
    '\n    Calculate the bounding box of the text. Unlike\n    :meth:`matplotlib.text.Text.get_extents` method, The bbox size of\n    the text before the rotation is calculated.\n    '
    projected_xs = []
    projected_ys = []
    theta = np.deg2rad(text.get_rotation())
    tr = Affine2D().rotate((- theta))
    (_, parts, d) = text._get_layout(renderer)
    for (t, wh, x, y) in parts:
        (w, h) = wh
        (xt1, yt1) = tr.transform_point((x, y))
        yt1 -= d
        (xt2, yt2) = ((xt1 + w), (yt1 + h))
        projected_xs.extend([xt1, xt2])
        projected_ys.extend([yt1, yt2])
    (xt_box, yt_box) = (min(projected_xs), min(projected_ys))
    (w_box, h_box) = ((max(projected_xs) - xt_box), (max(projected_ys) - yt_box))
    (x_box, y_box) = Affine2D().rotate(theta).transform_point((xt_box, yt_box))
    return (x_box, y_box, w_box, h_box)
