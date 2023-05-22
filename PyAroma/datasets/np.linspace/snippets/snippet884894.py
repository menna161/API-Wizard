import numpy as np
import os
from .reference_spectra import vega, solar, sedpydir
from pkg_resources import resource_filename, resource_listdir
import numba
import matplotlib.pyplot as pl


def gridify_transmission(self, dlnlam, wmin=100.0):
    'Place the transmission function on a regular grid in lnlam\n        (angstroms) defined by a lam_min and dlnlam.  Note that only the\n        non-zero values of the transmission on this grid stored.  The indices\n        corresponding to these values are stored as the `inds` attribute (a\n        slice object). (with possibly a zero at either end.)\n\n        Parameters\n        ----------\n        dlnlam : float\n            The spacing in ln-lambda of the regular wavelength grid onto which\n            the filter is to be placed.\n\n        wmin : float (optional, default: 100)\n            The starting wavelength (Angstroms) for the regular grid.\n        '
    ind_min = int(np.floor(((np.log(self.wavelength.min()) - np.log(wmin)) / dlnlam)))
    ind_max = int(np.ceil(((np.log(self.wavelength.max()) - np.log(wmin)) / dlnlam)))
    lnlam = np.linspace(((ind_min * dlnlam) + np.log(wmin)), ((ind_max * dlnlam) + np.log(wmin)), (ind_max - ind_min))
    lam = np.exp(lnlam)
    trans = np.interp(lam, self.wavelength, self.transmission, left=0.0, right=0.0)
    self.wmin = wmin
    self.dlnlam = dlnlam
    self.inds = slice(ind_min, ind_max)
    self._wavelength = lam
    self._transmission = trans
    self.dwave = np.gradient(lam)
