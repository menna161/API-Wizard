import datetime
from typing import Tuple
import freezegun
import pytest
from almost_equal import datetime_almost_equal
from astral import LocationInfo, TimePeriod, sun
from astral.sun import Depression, SunDirection


def test_TimeAtElevation_GreaterThan180(london: LocationInfo):
    d = datetime.date(2015, 12, 1)
    dt = sun.time_at_elevation(london.observer, 186, d, SunDirection.RISING)
    cdt = datetime.datetime(2015, 12, 1, 16, 34, tzinfo=datetime.timezone.utc)
    assert datetime_almost_equal(dt, cdt, seconds=300)
