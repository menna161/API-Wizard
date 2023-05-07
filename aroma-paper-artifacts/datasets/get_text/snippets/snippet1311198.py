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


def _get_text_ref_angle(self):
    if self._text_follow_ref_angle:
        return (self._get_ref_angle() + 90)
    else:
        return 0
