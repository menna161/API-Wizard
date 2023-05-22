import logging
import warnings
import numpy as np
from matplotlib import rcParams
from matplotlib import docstring
from matplotlib.artist import Artist, allow_rasterization
from matplotlib.cbook import silent_list, is_hashable, warn_deprecated
import matplotlib.colors as colors
from matplotlib.font_manager import FontProperties
from matplotlib.lines import Line2D
from matplotlib.patches import Patch, Rectangle, Shadow, FancyBboxPatch
from matplotlib.collections import LineCollection, RegularPolyCollection, CircleCollection, PathCollection, PolyCollection
from matplotlib.transforms import Bbox, BboxBase, TransformedBbox
from matplotlib.transforms import BboxTransformTo, BboxTransformFrom
from matplotlib.offsetbox import HPacker, VPacker, TextArea, DrawingArea
from matplotlib.offsetbox import DraggableOffsetBox
from matplotlib.container import ErrorbarContainer, BarContainer, StemContainer
from . import legend_handler
from matplotlib.axes import Axes
from matplotlib.figure import Figure


def get_texts(self):
    'Return a list of `~.text.Text` instances in the legend.'
    return silent_list('Text', self.texts)
