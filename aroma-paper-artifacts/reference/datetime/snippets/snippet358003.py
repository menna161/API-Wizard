import datetime
from typing import Tuple
import freezegun
import pytest
from almost_equal import datetime_almost_equal
from astral import LocationInfo, TimePeriod, sun
from astral.sun import Depression, SunDirection


def test_Nighttime(london: LocationInfo):
    d = datetime.date(2016, 1, 6)
    (start, end) = sun.night(london.observer, d)
    cstart = datetime.datetime(2016, 1, 6, 16, 46, tzinfo=datetime.timezone.utc)
    cend = datetime.datetime(2016, 1, 7, 7, 25, tzinfo=datetime.timezone.utc)
    assert datetime_almost_equal(start, cstart, 120)
    assert datetime_almost_equal(end, cend, 120)
