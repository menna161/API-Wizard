import numpy as np
from numpy.fft import fft, ifft, fftfreq, rfftfreq


def resample_wave(wavelength, spectrum, linear=False):
    'Resample spectrum, so that the number of elements is the next highest\n    power of two.  This uses np.interp.  Note that if the input wavelength grid\n    did not critically sample the spectrum then there is no gaurantee the\n    output wavelength grid will.\n    '
    (wmin, wmax) = (wavelength.min(), wavelength.max())
    nw = len(wavelength)
    nnew = int((2.0 ** np.ceil(np.log2(nw))))
    if linear:
        Rgrid = np.diff(wavelength)
        w = np.linspace(wmin, wmax, nnew)
    else:
        Rgrid = np.diff(np.log(wavelength))
        lnlam = np.linspace(np.log(wmin), np.log(wmax), nnew)
        w = np.exp(lnlam)
    s = np.interp(w, wavelength, spectrum)
    return (w, s)
