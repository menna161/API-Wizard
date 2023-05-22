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


def get_text_width_height_descent(self, s, prop, ismath):
    '\n        get the width and height in display coords of the string s\n        with FontPropertry prop\n        '
    if ismath:
        s = self.strip_math(s)
    if (self.gc is None):
        gc = self.new_gc()
    else:
        gc = self.gc
    gfx_ctx = gc.gfx_ctx
    font = self.get_wx_font(s, prop)
    gfx_ctx.SetFont(font, wx.BLACK)
    (w, h, descent, leading) = gfx_ctx.GetFullTextExtent(s)
    return (w, h, descent)
