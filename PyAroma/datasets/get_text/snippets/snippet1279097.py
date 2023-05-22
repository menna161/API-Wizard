import warnings
import numpy as np
import matplotlib.transforms as mtransforms
import matplotlib.artist as martist
import matplotlib.text as mtext
import matplotlib.path as mpath
from matplotlib.transforms import Bbox, BboxBase, TransformedBbox
from matplotlib.font_manager import FontProperties
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
from matplotlib import rcParams
from matplotlib import docstring
from matplotlib.image import BboxImage
from matplotlib.patches import bbox_artist as mbbox_artist
from matplotlib.text import _AnnotationBase
import matplotlib.pyplot as plt


def get_extent(self, renderer):
    (clean_line, ismath) = self._text.is_math_text(self._text._text)
    (_, h_, d_) = renderer.get_text_width_height_descent('lp', self._text._fontproperties, ismath=False)
    (bbox, info, d) = self._text._get_layout(renderer)
    (w, h) = (bbox.width, bbox.height)
    line = info[(- 1)][0]
    self._baseline_transform.clear()
    if ((len(info) > 1) and self._multilinebaseline):
        d_new = ((0.5 * h) - (0.5 * (h_ - d_)))
        self._baseline_transform.translate(0, (d - d_new))
        d = d_new
    else:
        h_d = max((h_ - d_), (h - d))
        if self.get_minimumdescent():
            d = max(d, d_)
        h = (h_d + d)
    return (w, h, 0.0, d)
