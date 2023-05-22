import pytest
import numpy as np
from astropy.tests.helper import catch_warnings
from astropy.table import Table, Column, QTable, table_helpers, NdarrayMixin, unique
from astropy.utils.exceptions import AstropyUserWarning
from astropy import time
from astropy import units as u
from astropy import coordinates


def test_mutable_operations(T1):
    '\n    Operations like adding or deleting a row should removing grouping,\n    but adding or removing or renaming a column should retain grouping.\n    '
    for masked in (False, True):
        t1 = Table(T1, masked=masked)
        tg = t1.group_by('a')
        tg.add_row((0, 'a', 3.0, 4))
        assert np.all((tg.groups.indices == np.array([0, len(tg)])))
        assert (tg.groups.keys is None)
        tg = t1.group_by('a')
        tg.remove_row(4)
        assert np.all((tg.groups.indices == np.array([0, len(tg)])))
        assert (tg.groups.keys is None)
        tg = t1.group_by('a')
        indices = tg.groups.indices.copy()
        tg.add_column(Column(name='e', data=np.arange(len(tg))))
        assert np.all((tg.groups.indices == indices))
        assert np.all((tg['e'].groups.indices == indices))
        assert np.all((tg['e'].groups.keys == tg.groups.keys))
        tg = t1.group_by('a')
        tg.remove_column('b')
        assert np.all((tg.groups.indices == indices))
        assert (tg.groups.keys.dtype.names == ('a',))
        assert np.all((tg['a'].groups.indices == indices))
        tg = t1.group_by('a')
        tg.remove_column('a')
        assert np.all((tg.groups.indices == indices))
        assert (tg.groups.keys.dtype.names == ('a',))
        assert np.all((tg['b'].groups.indices == indices))
        tg = t1.group_by('a')
        tg.rename_column('a', 'aa')
        assert np.all((tg.groups.indices == indices))
        assert (tg.groups.keys.dtype.names == ('a',))
        assert np.all((tg['aa'].groups.indices == indices))
