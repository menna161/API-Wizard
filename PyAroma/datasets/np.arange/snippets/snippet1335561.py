from collections import OrderedDict, UserDict
from collections.abc import Mapping
import pytest
import numpy as np
from astropy.table import Column, TableColumns, Table, MaskedColumn


def test_init_with_rows(self, table_type):
    for rows in ([[1, 'a'], [2, 'b']], [(1, 'a'), (2, 'b')], ((1, 'a'), (2, 'b'))):
        t = table_type(rows=rows, names=('a', 'b'))
        assert np.all((t['a'] == [1, 2]))
        assert np.all((t['b'] == ['a', 'b']))
        assert (t.colnames == ['a', 'b'])
        assert (t['a'].dtype.kind == 'i')
        assert (t['b'].dtype.kind in ('S', 'U'))
        assert t['b'].dtype.str.endswith('1')
    rows = np.arange(6).reshape(2, 3)
    t = table_type(rows=rows, names=('a', 'b', 'c'), dtype=['f8', 'f4', 'i8'])
    assert np.all((t['a'] == [0, 3]))
    assert np.all((t['b'] == [1, 4]))
    assert np.all((t['c'] == [2, 5]))
    assert (t.colnames == ['a', 'b', 'c'])
    assert t['a'].dtype.str.endswith('f8')
    assert t['b'].dtype.str.endswith('f4')
    assert t['c'].dtype.str.endswith('i8')
