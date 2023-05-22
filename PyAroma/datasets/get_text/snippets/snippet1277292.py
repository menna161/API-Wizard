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


def get_label_text(self):
    'Get the text of the label'
    return self.label.get_text()
