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


def get_texts_widths_heights_descents(self, renderer):
    '\n        return a list of width, height, descent for ticklabels.\n        '
    whd_list = []
    for ((x, y), a, l) in self._locs_angles_labels:
        if (not l.strip()):
            continue
        (clean_line, ismath) = self.is_math_text(l)
        whd = renderer.get_text_width_height_descent(clean_line, self._fontproperties, ismath=ismath)
        whd_list.append(whd)
    return whd_list
