import datetime
from typing import Tuple
import freezegun
import pytest
from almost_equal import datetime_almost_equal
from astral import LocationInfo, TimePeriod, sun
from astral.sun import Depression, SunDirection


@freezegun.freeze_time('2016-1-4')
def test_TimeAtElevation_NoDate(london: LocationInfo):
    dt = sun.time_at_elevation(london.observer, 6, direction=SunDirection.RISING)
    cdt = datetime.datetime(2016, 1, 4, 9, 5, 0, tzinfo=datetime.timezone.utc)
    assert datetime_almost_equal(dt, cdt, seconds=300)
