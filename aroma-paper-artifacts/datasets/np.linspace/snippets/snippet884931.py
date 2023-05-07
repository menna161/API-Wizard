import numpy as np
from numpy.testing import assert_allclose
from sedpy import observate
from sedpy.observate import FilterSet
from sedpy.observate import FilterSet
from sedpy.observate import FilterSet


def test_gridded_shapes():
    from sedpy.observate import FilterSet
    (Nobj, Nwave) = (100, 3000)
    spec = np.ones([Nobj, Nwave], dtype=float)
    wave = np.exp(np.linspace(np.log(5000.0), np.log(51000.0), Nwave))
    fnames = [f'jwst_f{b}' for b in ['070w', '090w', '115w', '150w', '200w', '335m']]
    fnames.sort()
    wmin = wave.min()
    dlnlam = np.gradient(np.log(wave))
    dlnlam_filters = dlnlam.min()
    assert np.allclose(dlnlam, dlnlam[0])
    filterset = FilterSet(fnames, dlnlam=dlnlam_filters, wmin=wmin)
    inds = (np.log(wave) <= (np.log(filterset.lam.max()) + (dlnlam_filters * 0.1)))
    maggies = filterset.get_sed_maggies(spec[(:, inds)])
    assert (maggies.shape == (100, len(fnames)))
