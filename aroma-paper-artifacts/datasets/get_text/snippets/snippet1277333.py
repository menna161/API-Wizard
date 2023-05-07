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


def get_text_heights(self, renderer):
    '\n        Returns the amount of space one should reserve for text\n        above and below the axes.  Returns a tuple (above, below)\n        '
    (bbox, bbox2) = self.get_ticklabel_extents(renderer)
    padPixels = self.majorTicks[0].get_pad_pixels()
    above = 0.0
    if bbox2.height:
        above += (bbox2.height + padPixels)
    below = 0.0
    if bbox.height:
        below += (bbox.height + padPixels)
    if (self.get_label_position() == 'top'):
        above += (self.label.get_window_extent(renderer).height + padPixels)
    else:
        below += (self.label.get_window_extent(renderer).height + padPixels)
    return (above, below)