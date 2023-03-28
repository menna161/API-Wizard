import datetime
from typing import Tuple
import freezegun
import pytest
from almost_equal import datetime_almost_equal
from astral import LocationInfo, TimePeriod, sun
from astral.sun import Depression, SunDirection


def test_TimeAtElevation_SunSetting(london: LocationInfo):
    d = datetime.date(2016, 1, 4)
    dt = sun.time_at_elevation(london.observer, 14, d, SunDirection.SETTING)
    cdt = datetime.datetime(2016, 1, 4, 13, 20, 0, tzinfo=datetime.timezone.utc)
    assert datetime_almost_equal(dt, cdt, seconds=300)
