import datetime
import nose
import traces
import pandas as pd
import numpy as np


def test_bin():
    start = datetime.datetime(2018, 12, 13, 7, 43, 15)
    end = datetime.datetime(2019, 2, 3, 8, 45, 10)
    span = (end - start)
    ts = traces.TimeSeries()
    ts[(start - (span / 2))] = 2
    ts[start] = 12
    ts[(start + (span / 3))] = 5
    ts[(end - (span / 4))] = 14
    ts[(end + span)] = None
    mask = traces.TimeSeries(default=False)
    mask[start] = True
    mask[end] = False
    mask[(start + ((3 * span) / 10))] = False
    mask[(start + ((5 * span) / 10))] = True
    binned = ts.bin('weeks', mask=mask)
    first = binned.peekitem(0)
    last = binned.peekitem()
    assert (len(binned) == 7)
    assert (first[0] == datetime.datetime(2018, 12, 10, 0, 0))
    assert (last[0] == datetime.datetime(2019, 1, 21, 0, 0))
    assert (int(last[1][5]) == 30581)
