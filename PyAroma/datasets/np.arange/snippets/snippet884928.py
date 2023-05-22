import numpy as np
from numpy.testing import assert_allclose
from sedpy import observate
from sedpy.observate import FilterSet
from sedpy.observate import FilterSet
from sedpy.observate import FilterSet


def test_gridded_filters():
    allfilters = np.array(_get_all_filters())
    w = np.array([f.wave_effective for f in allfilters])
    fnames = np.array([f.name for f in allfilters])
    good = (w < 100000.0)
    obs = {}
    obs['filters'] = allfilters[good][0:40]
    spec = np.random.uniform(0, 1.0, 5996)
    wave = np.exp(np.linspace(np.log(90), np.log(1000000.0), len(spec)))
    m_default = observate.getSED(wave, spec, obs['filters'])
    (wlo, whi, dlo) = ([], [], [])
    for f in obs['filters']:
        dlnlam = (np.gradient(f.wavelength) / f.wavelength)
        wlo.append(f.wavelength.min())
        dlo.append(dlnlam.min())
        whi.append(f.wavelength.max())
    wmin = np.min(wlo)
    wmax = np.max(whi)
    dlnlam = np.min(dlo)
    obs['filters'] = observate.load_filters(fnames[good][0:40], dlnlam=dlnlam, wmin=wmin)
    lnlam = np.exp(np.arange(np.log(wmin), np.log(wmax), dlnlam))
    lnspec = np.interp(lnlam, wave, spec)
    m_grid = observate.getSED(lnlam, lnspec, obs['filters'], gridded=True)
    assert np.allclose(m_grid, m_default, atol=0.05)
