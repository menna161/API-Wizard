import copy
from numbers import Integral
import numpy as np
from . import rcParams
from .lines import Line2D
from .patches import Circle, Rectangle, Ellipse
from .transforms import blended_transform_factory


def set_active(self, index):
    '\n        Trigger which radio button to make active.\n\n        *index* is an index into the original label list\n            that this object was constructed with.\n            Raise ValueError if the index is invalid.\n\n        Callbacks will be triggered if :attr:`eventson` is True.\n\n        '
    if (0 > index >= len(self.labels)):
        raise ValueError(('Invalid RadioButton index: %d' % index))
    self.value_selected = self.labels[index].get_text()
    for (i, p) in enumerate(self.circles):
        if (i == index):
            color = self.activecolor
        else:
            color = self.ax.get_facecolor()
        p.set_facecolor(color)
    if self.drawon:
        self.ax.figure.canvas.draw()
    if (not self.eventson):
        return
    for (cid, func) in self.observers.items():
        func(self.labels[index].get_text())
