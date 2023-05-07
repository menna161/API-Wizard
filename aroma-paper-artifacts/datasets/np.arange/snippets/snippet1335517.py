from collections import OrderedDict, UserDict
from collections.abc import Mapping
import pytest
import numpy as np
from astropy.table import Column, TableColumns, Table, MaskedColumn


def test_init(self):
    'Test initialisation with lists, tuples, dicts of arrays\n        rather than Columns [regression test for #2647]'
    x1 = np.arange(10.0)
    x2 = np.arange(5.0)
    x3 = np.arange(7.0)
    col_list = [('x1', x1), ('x2', x2), ('x3', x3)]
    tc_list = TableColumns(col_list)
    for col in col_list:
        assert (col[0] in tc_list)
        assert (tc_list[col[0]] is col[1])
    col_tuple = (('x1', x1), ('x2', x2), ('x3', x3))
    tc_tuple = TableColumns(col_tuple)
    for col in col_tuple:
        assert (col[0] in tc_tuple)
        assert (tc_tuple[col[0]] is col[1])
    col_dict = dict([('x1', x1), ('x2', x2), ('x3', x3)])
    tc_dict = TableColumns(col_dict)
    for col in tc_dict.keys():
        assert (col in tc_dict)
        assert (tc_dict[col] is col_dict[col])
    columns = [Column(col[1], name=col[0]) for col in col_list]
    tc = TableColumns(columns)
    for col in columns:
        assert (col.name in tc)
        assert (tc[col.name] is col)
