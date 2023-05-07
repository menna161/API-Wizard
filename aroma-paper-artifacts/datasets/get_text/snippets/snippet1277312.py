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


def set_ticklabels(self, ticklabels, *args, minor=False, **kwargs):
    '\n        Set the text values of the tick labels. Return a list of Text\n        instances.  Use *kwarg* *minor=True* to select minor ticks.\n        All other kwargs are used to update the text object properties.\n        As for get_ticklabels, label1 (left or bottom) is\n        affected for a given tick only if its label1On attribute\n        is True, and similarly for label2.  The list of returned\n        label text objects consists of all such label1 objects followed\n        by all such label2 objects.\n\n        The input *ticklabels* is assumed to match the set of\n        tick locations, regardless of the state of label1On and\n        label2On.\n\n        ACCEPTS: sequence of strings or Text objects\n        '
    get_labels = []
    for t in ticklabels:
        try:
            get_labels.append(t.get_text())
        except AttributeError:
            get_labels.append(t)
    ticklabels = get_labels
    if minor:
        self.set_minor_formatter(mticker.FixedFormatter(ticklabels))
        ticks = self.get_minor_ticks()
    else:
        self.set_major_formatter(mticker.FixedFormatter(ticklabels))
        ticks = self.get_major_ticks()
    ret = []
    for (tick_label, tick) in zip(ticklabels, ticks):
        tick.label1.set_text(tick_label)
        tick.label1.update(kwargs)
        tick.label2.set_text(tick_label)
        tick.label2.update(kwargs)
        if tick.label1On:
            ret.append(tick.label1)
        if tick.label2On:
            ret.append(tick.label2)
    self.stale = True
    return ret
