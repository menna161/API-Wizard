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


def _get_layout(self, renderer):
    '\n        return the extent (bbox) of the text together with\n        multiple-alignment information. Note that it returns an extent\n        of a rotated text when necessary.\n        '
    key = self.get_prop_tup(renderer=renderer)
    if (key in self._cached):
        return self._cached[key]
    horizLayout = []
    (thisx, thisy) = (0.0, 0.0)
    (xmin, ymin) = (0.0, 0.0)
    (width, height) = (0.0, 0.0)
    lines = self.get_text().split('\n')
    whs = np.zeros((len(lines), 2))
    horizLayout = np.zeros((len(lines), 4))
    (tmp, lp_h, lp_bl) = renderer.get_text_width_height_descent('lp', self._fontproperties, ismath=False)
    offsety = ((lp_h - lp_bl) * self._linespacing)
    baseline = 0
    for (i, line) in enumerate(lines):
        (clean_line, ismath) = self.is_math_text(line, self.get_usetex())
        if clean_line:
            (w, h, d) = renderer.get_text_width_height_descent(clean_line, self._fontproperties, ismath=ismath)
        else:
            (w, h, d) = (0, 0, 0)
        h = max(h, lp_h)
        d = max(d, lp_bl)
        whs[i] = (w, h)
        baseline = ((h - d) - thisy)
        thisy -= max(offsety, ((h - d) * self._linespacing))
        horizLayout[i] = (thisx, thisy, w, h)
        thisy -= d
        width = max(width, w)
        descent = d
    ymin = horizLayout[(- 1)][1]
    ymax = (horizLayout[0][1] + horizLayout[0][3])
    height = (ymax - ymin)
    xmax = (xmin + width)
    M = Affine2D().rotate_deg(self.get_rotation())
    offsetLayout = np.zeros((len(lines), 2))
    offsetLayout[:] = horizLayout[(:, 0:2)]
    if (len(lines) > 1):
        malign = self._get_multialignment()
        if (malign == 'center'):
            offsetLayout[(:, 0)] += ((width / 2.0) - (horizLayout[(:, 2)] / 2.0))
        elif (malign == 'right'):
            offsetLayout[(:, 0)] += (width - horizLayout[(:, 2)])
    cornersHoriz = np.array([(xmin, ymin), (xmin, ymax), (xmax, ymax), (xmax, ymin)], float)
    cornersHoriz[(:, 1)] -= descent
    cornersRotated = M.transform(cornersHoriz)
    txs = cornersRotated[(:, 0)]
    tys = cornersRotated[(:, 1)]
    (xmin, xmax) = (txs.min(), txs.max())
    (ymin, ymax) = (tys.min(), tys.max())
    width = (xmax - xmin)
    height = (ymax - ymin)
    halign = self._horizontalalignment
    valign = self._verticalalignment
    rotation_mode = self.get_rotation_mode()
    if (rotation_mode != 'anchor'):
        if (halign == 'center'):
            offsetx = (xmin + (width / 2.0))
        elif (halign == 'right'):
            offsetx = (xmin + width)
        else:
            offsetx = xmin
        if (valign == 'center'):
            offsety = (ymin + (height / 2.0))
        elif (valign == 'top'):
            offsety = (ymin + height)
        elif (valign == 'baseline'):
            offsety = ((ymin + height) - baseline)
        elif (valign == 'center_baseline'):
            offsety = ((ymin + height) - (baseline / 2.0))
        else:
            offsety = ymin
    else:
        (xmin1, ymin1) = cornersHoriz[0]
        (xmax1, ymax1) = cornersHoriz[2]
        if (halign == 'center'):
            offsetx = ((xmin1 + xmax1) / 2.0)
        elif (halign == 'right'):
            offsetx = xmax1
        else:
            offsetx = xmin1
        if (valign == 'center'):
            offsety = ((ymin1 + ymax1) / 2.0)
        elif (valign == 'top'):
            offsety = ymax1
        elif (valign == 'baseline'):
            offsety = (ymax1 - baseline)
        elif (valign == 'center_baseline'):
            offsety = (((ymin1 + ymax1) - baseline) / 2.0)
        else:
            offsety = ymin1
        (offsetx, offsety) = M.transform_point((offsetx, offsety))
    xmin -= offsetx
    ymin -= offsety
    bbox = Bbox.from_bounds(xmin, ymin, width, height)
    xys = M.transform(offsetLayout)
    xys -= (offsetx, offsety)
    (xs, ys) = (xys[(:, 0)], xys[(:, 1)])
    ret = (bbox, list(zip(lines, whs, xs, ys)), descent)
    self._cached[key] = ret
    return ret
