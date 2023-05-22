import warnings
from . import artist, cbook, docstring
from .artist import Artist, allow_rasterization
from .patches import Rectangle
from .text import Text
from .transforms import Bbox
from .path import Path


def get_text_bounds(self, renderer):
    ' Get text bounds in axes co-ordinates. '
    bbox = self._text.get_window_extent(renderer)
    bboxa = bbox.inverse_transformed(self.get_data_transform())
    return bboxa.bounds
