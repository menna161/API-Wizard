import warnings
from . import artist, cbook, docstring
from .artist import Artist, allow_rasterization
from .patches import Rectangle
from .text import Text
from .transforms import Bbox
from .path import Path


def get_text(self):
    'Return the cell `.Text` instance.'
    return self._text
