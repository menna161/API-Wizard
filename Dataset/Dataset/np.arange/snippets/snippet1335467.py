import pytest
import numpy as np
from astropy.tests.helper import catch_warnings
from astropy.table import Table, Column, QTable, table_helpers, NdarrayMixin, unique
from astropy.utils.exceptions import AstropyUserWarning
from astropy import time
from astropy import units as u
from astropy import coordinates


def test_group_mixins():
    '\n    Test grouping a table with mixin columns\n    '
    idx = np.arange(4)
    x = np.array([3.0, 1.0, 2.0, 1.0])
    q = (x * u.m)
    lon = coordinates.Longitude((x * u.deg))
    lat = coordinates.Latitude((x * u.deg))
    tm = (time.Time(2000, format='jyear') + time.TimeDelta((x * 1e-10), format='sec'))
    sc = coordinates.SkyCoord(ra=lon, dec=lat)
    aw = table_helpers.ArrayWrapper(x)
    nd = np.array([(3, 'c'), (1, 'a'), (2, 'b'), (1, 'a')], dtype='<i4,|S1').view(NdarrayMixin)
    qt = QTable([idx, x, q, lon, lat, tm, sc, aw, nd], names=['idx', 'x', 'q', 'lon', 'lat', 'tm', 'sc', 'aw', 'nd'])
    mixin_keys = ['x', 'q', 'lon', 'lat', 'tm', 'sc', 'aw', 'nd']
    for key in mixin_keys:
        qtg = qt.group_by(key)
        assert np.all((qtg['idx'] == [1, 3, 2, 0]))
        for name in ['x', 'q', 'lon', 'lat', 'tm', 'aw', 'nd']:
            assert np.all((qt[name][[1, 3]] == qtg.groups[0][name]))
            assert np.all((qt[name][[2]] == qtg.groups[1][name]))
            assert np.all((qt[name][[0]] == qtg.groups[2][name]))
    uqt = unique(qt, keys=mixin_keys)
    assert (len(uqt) == 3)
    assert np.all((uqt['idx'] == [1, 2, 0]))
    assert np.all((uqt['x'] == [1.0, 2.0, 3.0]))
    idxg = qt['idx'].group_by(qt[mixin_keys])
    assert np.all((idxg == [1, 3, 2, 0]))
