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


def _get_text2(self):
    t = super()._get_text2()
    t.set_rotation_mode('anchor')
    t.set_transform((t.get_transform() + self._text2_translate))
    return t
