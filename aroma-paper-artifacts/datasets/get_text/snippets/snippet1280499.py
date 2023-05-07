import copy
from numbers import Integral
import numpy as np
from . import rcParams
from .lines import Line2D
from .patches import Circle, Rectangle, Ellipse
from .transforms import blended_transform_factory


def set_active(self, index):
    '\n        Directly (de)activate a check button by index.\n\n        *index* is an index into the original label list\n            that this object was constructed with.\n            Raises ValueError if *index* is invalid.\n\n        Callbacks will be triggered if :attr:`eventson` is True.\n\n        '
    if (0 > index >= len(self.labels)):
        raise ValueError(('Invalid CheckButton index: %d' % index))
    (l1, l2) = self.lines[index]
    l1.set_visible((not l1.get_visible()))
    l2.set_visible((not l2.get_visible()))
    if self.drawon:
        self.ax.figure.canvas.draw()
    if (not self.eventson):
        return
    for (cid, func) in self.observers.items():
        func(self.labels[index].get_text())
