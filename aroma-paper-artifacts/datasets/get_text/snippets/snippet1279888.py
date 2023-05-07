import copy
import glob
import hashlib
import logging
import os
from pathlib import Path
import re
import subprocess
import numpy as np
import matplotlib as mpl
from matplotlib import _png, cbook, dviread, rcParams


def get_text_width_height_descent(self, tex, fontsize, renderer=None):
    'Return width, height and descent of the text.'
    if (tex.strip() == ''):
        return (0, 0, 0)
    dpi_fraction = (renderer.points_to_pixels(1.0) if renderer else 1)
    if rcParams['text.latex.preview']:
        basefile = self.get_basefile(tex, fontsize)
        baselinefile = ('%s.baseline' % basefile)
        if (not os.path.exists(baselinefile)):
            dvifile = self.make_dvi_preview(tex, fontsize)
        with open(baselinefile) as fh:
            l = fh.read().split()
        (height, depth, width) = [(float(l1) * dpi_fraction) for l1 in l]
        return (width, (height + depth), depth)
    else:
        dvifile = self.make_dvi(tex, fontsize)
        with dviread.Dvi(dvifile, (72 * dpi_fraction)) as dvi:
            page = next(iter(dvi))
        return (page.width, (page.height + page.descent), page.descent)
