from functools import reduce
from collections import defaultdict
import math
import warnings
import numpy as np
from matplotlib import artist
import matplotlib.axes as maxes
import matplotlib.cbook as cbook
import matplotlib.collections as mcoll
import matplotlib.colors as mcolors
import matplotlib.docstring as docstring
import matplotlib.scale as mscale
import matplotlib.transforms as mtransforms
from matplotlib.axes import Axes, rcParams
from matplotlib.colors import Normalize, LightSource
from matplotlib.transforms import Bbox
from matplotlib.tri.triangulation import Triangulation
from . import art3d
from . import proj3d
from . import axis3d
import matplotlib.projections as proj


def get_zlabel(self):
    '\n        Get the z-label text string.\n\n        .. versionadded :: 1.1.0\n            This function was added, but not tested. Please report any bugs.\n        '
    label = self.zaxis.get_label()
    return label.get_text()
