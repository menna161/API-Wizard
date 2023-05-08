import datetime
from typing import Tuple
import freezegun
import pytest
from almost_equal import datetime_almost_equal
from astral import LocationInfo, TimePeriod, sun
from astral.sun import Depression, SunDirection


@freezegun.freeze_time('2016-1-06')
def test_Daylight_NoDate(london: LocationInfo):
    ans = sun.daylight(london.observer)
    start = datetime.datetime(2016, 1, 6, 8, 5, 0, tzinfo=datetime.timezone.utc)
    end = datetime.datetime(2016, 1, 6, 16, 7, 0, tzinfo=datetime.timezone.utc)
    assert datetime_almost_equal(ans[0], start, 120)
    assert datetime_almost_equal(ans[1], end, 120)
