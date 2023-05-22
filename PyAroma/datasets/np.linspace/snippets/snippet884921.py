import numpy as np
from numpy.fft import fft, ifft, fftfreq, rfftfreq


def smooth_lsf_fft(wave, spec, outwave, sigma=None, lsf=None, pix_per_sigma=2, eps=0.25, preserve_all_input_frequencies=False, **kwargs):
    'Smooth a spectrum by a wavelength dependent line-spread function, using\n    FFTs.\n\n    Parameters\n    ----------\n    wavelength : ndarray of shape ``(N_pix,)``\n        Wavelength vector of the input spectrum.\n\n    spectrum : ndarray of shape ``(N_pix,)``\n        Flux vector of the input spectrum.\n\n    outwave : ndarray of shape ``(N_pix_out,)``\n        Desired output wavelength vector.\n\n    sigma : ndarray of shape ``(N_pix,)`` (optional)\n        Dispersion (in same units as ``wave``) as a function `wave`.  If not\n        given, sigma will be computed from the function provided by the ``lsf``\n        keyword.\n\n    lsf : callable (optional)\n        Function used to calculate the dispersion as a function of wavelength.\n        Must be able to take as an argument the ``wave`` vector and any extra\n        keyword arguments and return the dispersion (in the same units as the\n        input wavelength vector) at every value of ``wave``.  If not provided\n        then ``sigma`` must be specified.\n\n    pix_per_sigma : float (optional, default: 2)\n        Number of pixels per sigma of the smoothed spectrum to use in\n        intermediate interpolation and FFT steps. Increasing this number will\n        increase the accuracy of the output (to a point), and the run-time, by\n        preserving all high-frequency information in the input spectrum.\n\n    preserve_all_input_frequencies : bool (default: False)\n        This is a switch to use a very dense sampling of the input spectrum that\n        preserves all input frequencies.  It can significantly increase the call\n        time for often modest gains...\n\n    eps : float (optional)\n        Deprecated.\n\n    Extra Parameters\n    ----------------\n    kwargs:\n        All additional keywords are passed to the function supplied to the\n        ``lsf`` keyword, if present.\n\n    Returns\n    -------\n    smoothed_spec : ndarray of shape ``(N_pix_out,)``\n        The smoothed spectrum.\n    '
    if (sigma is None):
        sigma = lsf(wave, **kwargs)
    dw = np.gradient(wave)
    cdf = np.cumsum((dw / sigma))
    cdf /= cdf.max()
    sigma_per_pixel = (dw / sigma)
    x_per_pixel = np.gradient(cdf)
    x_per_sigma = np.nanmedian((x_per_pixel / sigma_per_pixel))
    N = (pix_per_sigma / x_per_sigma)
    if preserve_all_input_frequencies:
        N = max(N, (1.0 / np.nanmin(x_per_pixel)))
    nx = int((2 ** np.ceil(np.log2(N))))
    x = np.linspace(0, 1, nx)
    dx = (1.0 / nx)
    lam = np.interp(x, cdf, wave)
    newspec = np.interp(lam, wave, spec)
    spec_conv = smooth_fft(dx, newspec, x_per_sigma)
    return np.interp(outwave, lam, spec_conv)
