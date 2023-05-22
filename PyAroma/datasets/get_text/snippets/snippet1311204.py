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


def get_window_extent(self, renderer):
    self._update(renderer)
    tr = self.get_transform()
    angle_orig = self.get_rotation()
    offset_tr = Affine2D()
    self.set_transform((tr + offset_tr))
    text_ref_angle = self._get_text_ref_angle()
    offset_ref_angle = self._get_offset_ref_angle()
    theta = ((offset_ref_angle / 180.0) * np.pi)
    dd = self._get_offset_radius()
    (dx, dy) = ((dd * np.cos(theta)), (dd * np.sin(theta)))
    offset_tr.translate(dx, dy)
    self.set_rotation((text_ref_angle + angle_orig))
    bbox = super().get_window_extent(renderer).frozen()
    offset_tr.clear()
    self.set_transform(tr)
    self.set_rotation(angle_orig)
    return bbox
