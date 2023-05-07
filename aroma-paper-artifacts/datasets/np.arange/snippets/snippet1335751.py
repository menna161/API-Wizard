import pytest
import numpy as np
from astropy import table
from astropy.table import Table, QTable
from astropy.table.table_helpers import simple_table
from astropy import units as u
from astropy.utils import console
from astropy import conf
from astropy import conf


def test_format0(self, table_type):
    "Try getting screen size but fail to defaults because testing doesn't\n        have access to screen (fcntl.ioctl fails).\n        "
    self._setup(table_type)
    arr = np.arange(4000, dtype=np.float64).reshape(100, 40)
    lines = table_type(arr).pformat()
    (nlines, width) = console.terminal_size()
    assert (len(lines) == nlines)
    for line in lines[:(- 1)]:
        assert ((width - 10) < len(line) <= width)
