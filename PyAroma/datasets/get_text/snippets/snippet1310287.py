import os.path
import math
import sys
import warnings
import weakref
import matplotlib
from matplotlib.backend_bases import _Backend, FigureCanvasBase, FigureManagerBase, GraphicsContextBase, NavigationToolbar2, RendererBase, TimerBase, cursors, ToolContainerBase, StatusbarBase
from matplotlib.backend_bases import _has_pil
from matplotlib._pylab_helpers import Gcf
from matplotlib.cbook import is_writable_file_like, warn_deprecated
from matplotlib.figure import Figure
from matplotlib.path import Path
from matplotlib.transforms import Affine2D
from matplotlib.widgets import SubplotTool
from matplotlib.backend_managers import ToolManager
from matplotlib import cbook, rcParams, backend_tools
import wx
import traceback
import pdb


def draw_text(self, gc, x, y, s, prop, angle, ismath=False, mtext=None):
    if ismath:
        s = self.strip_math(s)
    DEBUG_MSG('draw_text()', 1, self)
    gc.select()
    self.handle_clip_rectangle(gc)
    gfx_ctx = gc.gfx_ctx
    font = self.get_wx_font(s, prop)
    color = gc.get_wxcolour(gc.get_rgb())
    gfx_ctx.SetFont(font, color)
    (w, h, d) = self.get_text_width_height_descent(s, prop, ismath)
    x = int(x)
    y = int((y - h))
    if (angle == 0.0):
        gfx_ctx.DrawText(s, x, y)
    else:
        rads = math.radians(angle)
        xo = (h * math.sin(rads))
        yo = (h * math.cos(rads))
        gfx_ctx.DrawRotatedText(s, (x - xo), (y - yo), rads)
    gc.unselect()
