import copy
import pickle
from io import StringIO
import pytest
import numpy as np
from astropy.coordinates import EarthLocation
from astropy.table import Table, QTable, join, hstack, vstack, Column, NdarrayMixin
from astropy.table import serialize
from astropy import time
from astropy import coordinates
from astropy import units as u
from astropy.table.column import BaseColumn
from astropy.table import table_helpers
from astropy.utils.exceptions import AstropyUserWarning
from astropy.utils.metadata import MergeConflictWarning
from .conftest import MIXIN_COLS
import h5py
import yaml
from astropy.io.ascii.connect import _get_connectors_table


def test_ndarray_mixin():
    '\n    Test directly adding a plain structured array into a table instead of the\n    view as an NdarrayMixin.  Once added as an NdarrayMixin then all the previous\n    tests apply.\n    '
    a = np.array([(1, 'a'), (2, 'b'), (3, 'c'), (4, 'd')], dtype=('<i4,' + '|U1'))
    b = np.array([(10, 'aa'), (20, 'bb'), (30, 'cc'), (40, 'dd')], dtype=[('x', 'i4'), ('y', 'U2')])
    c = np.rec.fromrecords([(100, 'raa'), (200, 'rbb'), (300, 'rcc'), (400, 'rdd')], names=['rx', 'ry'])
    d = np.arange(8).reshape(4, 2).view(NdarrayMixin)
    t = Table([a], names=['a'])
    t['b'] = b
    t['c'] = c
    t['d'] = d
    assert isinstance(t['a'], NdarrayMixin)
    assert (t['a'][1][1] == a[1][1])
    assert (t['a'][2][0] == a[2][0])
    assert (t[1]['a'][1] == a[1][1])
    assert (t[2]['a'][0] == a[2][0])
    assert isinstance(t['b'], NdarrayMixin)
    assert (t['b'][1]['x'] == b[1]['x'])
    assert (t['b'][1]['y'] == b[1]['y'])
    assert (t[1]['b']['x'] == b[1]['x'])
    assert (t[1]['b']['y'] == b[1]['y'])
    assert isinstance(t['c'], NdarrayMixin)
    assert (t['c'][1]['rx'] == c[1]['rx'])
    assert (t['c'][1]['ry'] == c[1]['ry'])
    assert (t[1]['c']['rx'] == c[1]['rx'])
    assert (t[1]['c']['ry'] == c[1]['ry'])
    assert isinstance(t['d'], NdarrayMixin)
    assert (t['d'][1][0] == d[1][0])
    assert (t['d'][1][1] == d[1][1])
    assert (t[1]['d'][0] == d[1][0])
    assert (t[1]['d'][1] == d[1][1])
    assert (t.pformat() == ['   a         b           c       d [2] ', '-------- ---------- ------------ ------', "(1, 'a') (10, 'aa') (100, 'raa') 0 .. 1", "(2, 'b') (20, 'bb') (200, 'rbb') 2 .. 3", "(3, 'c') (30, 'cc') (300, 'rcc') 4 .. 5", "(4, 'd') (40, 'dd') (400, 'rdd') 6 .. 7"])
