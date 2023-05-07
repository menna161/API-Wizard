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


def get_text(self):
    t = super().get_text()
    if (t == '__from_axes__'):
        return self._axis.get_label().get_text()
    return self._text
