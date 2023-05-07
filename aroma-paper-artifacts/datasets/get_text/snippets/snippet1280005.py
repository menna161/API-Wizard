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


def _update_position_xytext(self, renderer, xy_pixel):
    '\n        Update the pixel positions of the annotation text and the arrow patch.\n        '
    self.set_transform(self._get_xy_transform(renderer, self.anncoords))
    (ox0, oy0) = self._get_xy_display()
    (ox1, oy1) = xy_pixel
    if (self.arrowprops is not None):
        (x0, y0) = xy_pixel
        (l, b, w, h) = Text.get_window_extent(self, renderer).bounds
        r = (l + w)
        t = (b + h)
        xc = (0.5 * (l + r))
        yc = (0.5 * (b + t))
        d = self.arrowprops.copy()
        ms = d.pop('mutation_scale', self.get_size())
        self.arrow_patch.set_mutation_scale(ms)
        if ('arrowstyle' not in d):
            shrink = d.pop('shrink', 0.0)
            width = d.pop('width', 4)
            headwidth = d.pop('headwidth', 12)
            frac = d.pop('frac', None)
            if (frac is not None):
                warnings.warn("'frac' option in 'arrowprops' is no longer supported; use 'headlength' to set the head length in points.")
            headlength = d.pop('headlength', 12)
            stylekw = dict(head_length=(headlength / ms), head_width=(headwidth / ms), tail_width=(width / ms))
            self.arrow_patch.set_arrowstyle('simple', **stylekw)
            xpos = ((l, 0), (xc, 0.5), (r, 1))
            ypos = ((b, 0), (yc, 0.5), (t, 1))
            (_, (x, relposx)) = min(((abs((val[0] - x0)), val) for val in xpos))
            (_, (y, relposy)) = min(((abs((val[0] - y0)), val) for val in ypos))
            self._arrow_relpos = (relposx, relposy)
            r = np.hypot((y - y0), (x - x0))
            shrink_pts = ((shrink * r) / renderer.points_to_pixels(1))
            self.arrow_patch.shrinkA = shrink_pts
            self.arrow_patch.shrinkB = shrink_pts
        relpos = self._arrow_relpos
        bbox = Text.get_window_extent(self, renderer)
        ox0 = (bbox.x0 + (bbox.width * relpos[0]))
        oy0 = (bbox.y0 + (bbox.height * relpos[1]))
        self.arrow_patch.set_positions((ox0, oy0), (ox1, oy1))
        if ('patchA' in d):
            self.arrow_patch.set_patchA(d.pop('patchA'))
        elif self._bbox_patch:
            self.arrow_patch.set_patchA(self._bbox_patch)
        else:
            pad = renderer.points_to_pixels(4)
            if (self.get_text() == ''):
                self.arrow_patch.set_patchA(None)
                return
            bbox = Text.get_window_extent(self, renderer)
            (l, b, w, h) = bbox.bounds
            l -= (pad / 2.0)
            b -= (pad / 2.0)
            w += pad
            h += pad
            r = Rectangle(xy=(l, b), width=w, height=h)
            r.set_transform(IdentityTransform())
            r.set_clip_on(False)
            self.arrow_patch.set_patchA(r)
