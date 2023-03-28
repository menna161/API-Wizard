import datetime
from typing import Tuple
import freezegun
import pytest
from almost_equal import datetime_almost_equal
from astral import LocationInfo, TimePeriod, sun
from astral.sun import Depression, SunDirection


def test_Daylight(london: LocationInfo):
    d = datetime.date(2016, 1, 6)
    (start, end) = sun.daylight(london.observer, d)
    cstart = datetime.datetime(2016, 1, 6, 8, 5, 0, tzinfo=datetime.timezone.utc)
    cend = datetime.datetime(2016, 1, 6, 16, 7, 0, tzinfo=datetime.timezone.utc)
    assert datetime_almost_equal(start, cstart, 120)
    assert datetime_almost_equal(end, cend, 120)
