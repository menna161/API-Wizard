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


def get_text(self):
    "Returns the string representation of this area's text"
    return self._text.get_text()
