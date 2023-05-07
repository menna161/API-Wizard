import matplotlib.artist as martist
import matplotlib.text as mtext
import matplotlib.font_manager as font_manager
from matplotlib.path import Path
from matplotlib.transforms import Affine2D, Bbox, IdentityTransform, ScaledTranslation, TransformedPath
from matplotlib.collections import LineCollection
from matplotlib import rcParams
from matplotlib.artist import allow_rasterization
import numpy as np
import matplotlib.lines as mlines
from .axisline_style import AxislineStyle
from matplotlib.artist import Artist
from matplotlib.lines import Line2D


def _get_ticklabels_offsets(self, renderer, label_direction):
    "\n        Calculates the offsets of the ticklabels from the tick and\n        their total heights. The offset only takes account the offset\n        due to the vertical alignment of the ticklabels, i.e.,if axis\n        direction is bottom and va is ;top', it will return 0. if va\n        is 'baseline', it will return (height-descent).\n        "
    whd_list = self.get_texts_widths_heights_descents(renderer)
    if (not whd_list):
        return (0, 0)
    r = 0
    (va, ha) = (self.get_va(), self.get_ha())
    if (label_direction == 'left'):
        pad = max((w for (w, h, d) in whd_list))
        if (ha == 'left'):
            r = pad
        elif (ha == 'center'):
            r = (0.5 * pad)
    elif (label_direction == 'right'):
        pad = max((w for (w, h, d) in whd_list))
        if (ha == 'right'):
            r = pad
        elif (ha == 'center'):
            r = (0.5 * pad)
    elif (label_direction == 'bottom'):
        pad = max((h for (w, h, d) in whd_list))
        if (va == 'bottom'):
            r = pad
        elif (va == 'center'):
            r = (0.5 * pad)
        elif (va == 'baseline'):
            max_ascent = max(((h - d) for (w, h, d) in whd_list))
            max_descent = max((d for (w, h, d) in whd_list))
            r = max_ascent
            pad = (max_ascent + max_descent)
    elif (label_direction == 'top'):
        pad = max((h for (w, h, d) in whd_list))
        if (va == 'top'):
            r = pad
        elif (va == 'center'):
            r = (0.5 * pad)
        elif (va == 'baseline'):
            max_ascent = max(((h - d) for (w, h, d) in whd_list))
            max_descent = max((d for (w, h, d) in whd_list))
            r = max_descent
            pad = (max_ascent + max_descent)
    return (r, pad)
