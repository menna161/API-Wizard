import datetime
import logging
import warnings
import numpy as np
from matplotlib import rcParams
import matplotlib.artist as artist
from matplotlib.artist import allow_rasterization
import matplotlib.cbook as cbook
from matplotlib.cbook import _string_to_bool
import matplotlib.font_manager as font_manager
import matplotlib.lines as mlines
import matplotlib.patches as mpatches
import matplotlib.scale as mscale
import matplotlib.text as mtext
import matplotlib.ticker as mticker
import matplotlib.transforms as mtransforms
import matplotlib.units as munits
import dateutil.tz


def __init__(self, axes, loc, label, size=None, width=None, color=None, tickdir=None, pad=None, labelsize=None, labelcolor=None, zorder=None, gridOn=None, tick1On=True, tick2On=True, label1On=True, label2On=False, major=True, labelrotation=0, grid_color=None, grid_linestyle=None, grid_linewidth=None, grid_alpha=None, **kw):
    '\n        bbox is the Bound2D bounding box in display coords of the Axes\n        loc is the tick location in data coords\n        size is the tick size in points\n        '
    artist.Artist.__init__(self)
    if (gridOn is None):
        if (major and (rcParams['axes.grid.which'] in ('both', 'major'))):
            gridOn = rcParams['axes.grid']
        elif ((not major) and (rcParams['axes.grid.which'] in ('both', 'minor'))):
            gridOn = rcParams['axes.grid']
        else:
            gridOn = False
    self.set_figure(axes.figure)
    self.axes = axes
    name = self.__name__.lower()
    self._name = name
    self._loc = loc
    if (size is None):
        if major:
            size = rcParams[('%s.major.size' % name)]
        else:
            size = rcParams[('%s.minor.size' % name)]
    self._size = size
    if (width is None):
        if major:
            width = rcParams[('%s.major.width' % name)]
        else:
            width = rcParams[('%s.minor.width' % name)]
    self._width = width
    if (color is None):
        color = rcParams[('%s.color' % name)]
    self._color = color
    if (pad is None):
        if major:
            pad = rcParams[('%s.major.pad' % name)]
        else:
            pad = rcParams[('%s.minor.pad' % name)]
    self._base_pad = pad
    if (labelcolor is None):
        labelcolor = rcParams[('%s.color' % name)]
    self._labelcolor = labelcolor
    if (labelsize is None):
        labelsize = rcParams[('%s.labelsize' % name)]
    self._labelsize = labelsize
    self._set_labelrotation(labelrotation)
    if (zorder is None):
        if major:
            zorder = (mlines.Line2D.zorder + 0.01)
        else:
            zorder = mlines.Line2D.zorder
    self._zorder = zorder
    self._grid_color = (rcParams['grid.color'] if (grid_color is None) else grid_color)
    self._grid_linestyle = (rcParams['grid.linestyle'] if (grid_linestyle is None) else grid_linestyle)
    self._grid_linewidth = (rcParams['grid.linewidth'] if (grid_linewidth is None) else grid_linewidth)
    self._grid_alpha = (rcParams['grid.alpha'] if (grid_alpha is None) else grid_alpha)
    self._grid_kw = {k[5:]: v for (k, v) in kw.items()}
    self.apply_tickdir(tickdir)
    self.tick1line = self._get_tick1line()
    self.tick2line = self._get_tick2line()
    self.gridline = self._get_gridline()
    self.label1 = self._get_text1()
    self.label = self.label1
    self.label2 = self._get_text2()
    self.gridOn = gridOn
    self.tick1On = tick1On
    self.tick2On = tick2On
    self.label1On = label1On
    self.label2On = label2On
    self.update_position(loc)
