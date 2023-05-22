import copy
import gzip
import sys
import warnings
import numpy as np
from .. import cbook
from matplotlib.backend_bases import _Backend, FigureCanvasBase, FigureManagerBase, GraphicsContextBase, RendererBase
from matplotlib.font_manager import ttfFontProperty
from matplotlib.mathtext import MathTextParser
from matplotlib.path import Path
from matplotlib.transforms import Affine2D
import cairocffi as cairo
import cairo


def get_text_width_height_descent(self, s, prop, ismath):
    if ismath:
        (width, height, descent, fonts, used_characters) = self.mathtext_parser.parse(s, self.dpi, prop)
        return (width, height, descent)
    ctx = self.text_ctx
    ctx.save()
    ctx.select_font_face(prop.get_name(), self.fontangles[prop.get_style()], self.fontweights[prop.get_weight()])
    size = ((prop.get_size_in_points() * self.dpi) / 72)
    ctx.set_font_size(size)
    (y_bearing, w, h) = ctx.text_extents(s)[1:4]
    ctx.restore()
    return (w, h, (h + y_bearing))
