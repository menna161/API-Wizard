import datetime
import logging
import warnings
import numpy as np
from matplotlib import rcParams
import matplotlib.artist as artist
from matplotlib.artist import allow_rasterization
import matplotlib.cbook as cbook
from matplotlib.cbook import _string_to_bool
import matplotlib.font_manager as font_manager
import matplotlib.lines as mlines
import matplotlib.patches as mpatches
import matplotlib.scale as mscale
import matplotlib.text as mtext
import matplotlib.ticker as mticker
import matplotlib.transforms as mtransforms
import matplotlib.units as munits
import dateutil.tz


def _apply_params(self, **kw):
    for name in ['gridOn', 'tick1On', 'tick2On', 'label1On', 'label2On']:
        if (name in kw):
            setattr(self, name, kw.pop(name))
    if any(((k in kw) for k in ['size', 'width', 'pad', 'tickdir'])):
        self._size = kw.pop('size', self._size)
        self._width = kw.pop('width', self._width)
        self._base_pad = kw.pop('pad', self._base_pad)
        self.apply_tickdir(kw.pop('tickdir', self._tickdir))
        self.tick1line.set_marker(self._tickmarkers[0])
        self.tick2line.set_marker(self._tickmarkers[1])
        for line in (self.tick1line, self.tick2line):
            line.set_markersize(self._size)
            line.set_markeredgewidth(self._width)
        trans = self._get_text1_transform()[0]
        self.label1.set_transform(trans)
        trans = self._get_text2_transform()[0]
        self.label2.set_transform(trans)
    tick_kw = {k: v for (k, v) in kw.items() if (k in ['color', 'zorder'])}
    self.tick1line.set(**tick_kw)
    self.tick2line.set(**tick_kw)
    for (k, v) in tick_kw.items():
        setattr(self, ('_' + k), v)
    if ('labelrotation' in kw):
        self._set_labelrotation(kw.pop('labelrotation'))
        self.label1.set(rotation=self._labelrotation[1])
        self.label2.set(rotation=self._labelrotation[1])
    label_kw = {k[5:]: v for (k, v) in kw.items() if (k in ['labelsize', 'labelcolor'])}
    self.label1.set(**label_kw)
    self.label2.set(**label_kw)
    for (k, v) in label_kw.items():
        v = getattr(self.label1, ('get_' + k))()
        setattr(self, ('_label' + k), v)
    grid_kw = {k[5:]: v for (k, v) in kw.items() if (k in _gridline_param_names)}
    self.gridline.set(**grid_kw)
    for (k, v) in grid_kw.items():
        setattr(self, ('_grid_' + k), v)
