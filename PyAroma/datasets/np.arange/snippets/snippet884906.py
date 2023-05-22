import numpy as np
import os
from .reference_spectra import vega, solar, sedpydir
from pkg_resources import resource_filename, resource_listdir
import numba
import matplotlib.pyplot as pl


def _set_filters(self, native, wmin=None, wmax=None, dlnlam=None, **loading_kwargs):
    'Set the filters and the wavelength grid\n\n        native : list of Filter() instances\n            The Filter objects that will be part of this FilterSet, including\n            their native transmission\n        '
    self.dlnlam_native = np.array([np.diff(np.log(f.wavelength)).min() for f in native])
    if (dlnlam is None):
        dlnlam = min(self.dlnlam_native.min(), 0.001)
    if (wmin is None):
        wmin = np.min([f.wavelength.min() for f in native])
    if (wmax is None):
        wmax = np.max([f.wavelength.max() for f in native])
    self.wmin = wmin
    self.wmax = np.exp((np.log(wmax) + dlnlam))
    self.dlnlam = dlnlam
    self.lnlam = np.arange(np.log(self.wmin), np.log(self.wmax), self.dlnlam)
    self.lam = np.exp(self.lnlam)
    self.filters = load_filters(self.filternames, wmin=self.wmin, dlnlam=self.dlnlam, **loading_kwargs)
