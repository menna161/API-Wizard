from collections import OrderedDict
import types
import numpy as np
from matplotlib.axes import Axes
import matplotlib.axis as maxis
from matplotlib import cbook
from matplotlib import docstring
import matplotlib.markers as mmarkers
import matplotlib.patches as mpatches
import matplotlib.path as mpath
from matplotlib import rcParams
import matplotlib.ticker as mticker
import matplotlib.transforms as mtransforms
import matplotlib.spines as mspines


def _copy_tick_props(self, src, dest):
    'Copy the props from src tick to dest tick'
    if ((src is None) or (dest is None)):
        return
    super()._copy_tick_props(src, dest)
    trans = dest._get_text1_transform()[0]
    dest.label1.set_transform((trans + dest._text1_translate))
    trans = dest._get_text2_transform()[0]
    dest.label2.set_transform((trans + dest._text2_translate))
