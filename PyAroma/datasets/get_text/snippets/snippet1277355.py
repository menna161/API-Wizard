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


def get_text_widths(self, renderer):
    (bbox, bbox2) = self.get_ticklabel_extents(renderer)
    padPixels = self.majorTicks[0].get_pad_pixels()
    left = 0.0
    if bbox.width:
        left += (bbox.width + padPixels)
    right = 0.0
    if bbox2.width:
        right += (bbox2.width + padPixels)
    if (self.get_label_position() == 'left'):
        left += (self.label.get_window_extent(renderer).width + padPixels)
    else:
        right += (self.label.get_window_extent(renderer).width + padPixels)
    return (left, right)
