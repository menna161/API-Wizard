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


@artist.allow_rasterization
def draw(self, renderer):
    '\n        Draws the `.Text` object to the given *renderer*.\n        '
    if (renderer is not None):
        self._renderer = renderer
    if (not self.get_visible()):
        return
    if (self.get_text() == ''):
        return
    renderer.open_group('text', self.get_gid())
    with _wrap_text(self) as textobj:
        (bbox, info, descent) = textobj._get_layout(renderer)
        trans = textobj.get_transform()
        posx = float(textobj.convert_xunits(textobj._x))
        posy = float(textobj.convert_yunits(textobj._y))
        (posx, posy) = trans.transform_point((posx, posy))
        if ((not np.isfinite(posx)) or (not np.isfinite(posy))):
            _log.warning('posx and posy should be finite values')
            return
        (canvasw, canvash) = renderer.get_canvas_width_height()
        if textobj._bbox_patch:
            textobj._draw_bbox(renderer, posx, posy)
        gc = renderer.new_gc()
        gc.set_foreground(textobj.get_color())
        gc.set_alpha(textobj.get_alpha())
        gc.set_url(textobj._url)
        textobj._set_gc_clip(gc)
        angle = textobj.get_rotation()
        for (line, wh, x, y) in info:
            mtext = (textobj if (len(info) == 1) else None)
            x = (x + posx)
            y = (y + posy)
            if renderer.flipy():
                y = (canvash - y)
            (clean_line, ismath) = textobj.is_math_text(line, self.get_usetex())
            if textobj.get_path_effects():
                from matplotlib.patheffects import PathEffectRenderer
                textrenderer = PathEffectRenderer(textobj.get_path_effects(), renderer)
            else:
                textrenderer = renderer
            if textobj.get_usetex():
                textrenderer.draw_tex(gc, x, y, clean_line, textobj._fontproperties, angle, mtext=mtext)
            else:
                textrenderer.draw_text(gc, x, y, clean_line, textobj._fontproperties, angle, ismath=ismath, mtext=mtext)
    gc.restore()
    renderer.close_group('text')
    self.stale = False
