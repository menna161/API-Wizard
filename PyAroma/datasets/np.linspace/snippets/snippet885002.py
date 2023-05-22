import numpy as np
from sedpy import observate
import fsps
import matplotlib.pyplot as pl


def test():
    from sedpy import observate
    import fsps
    import matplotlib.pyplot as pl
    filters = ['galex_NUV', 'sdss_u0', 'sdss_r0', 'sdss_r0', 'sdss_i0', 'sdss_z0', 'bessell_U', 'bessell_B', 'bessell_V', 'bessell_R', 'bessell_I', 'twomass_J', 'twomass_H']
    flist = observate.load_filters(filters)
    sps = fsps.StellarPopulation(compute_vega_mags=False)
    (wave, spec) = sps.get_spectrum(tage=1.0, zmet=2, peraa=True)
    sed = observate.getSED(wave, spec, flist)
    sed_unc = np.abs(np.random.normal(1, 0.3, len(sed)))
    wgrid = np.linspace(2000.0, 13000.0, 1000)
    fgrid = np.linspace((- 13), (- 9), 100)
    (psed, sedpoints) = sed_to_psed(flist, sed, sed_unc, wgrid, fgrid)
    pl.imshow(np.exp(psed).T, cmap='Greys_r', interpolation='nearest', origin='upper', aspect='auto')
