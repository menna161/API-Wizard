import datetime
from typing import Tuple
import freezegun
import pytest
from almost_equal import datetime_almost_equal
from astral import LocationInfo, TimePeriod, sun
from astral.sun import Depression, SunDirection


@freezegun.freeze_time('2016-1-06')
def test_Nighttime_NoDate(london: LocationInfo):
    start = datetime.datetime(2016, 1, 6, 16, 46, tzinfo=datetime.timezone.utc)
    end = datetime.datetime(2016, 1, 7, 7, 25, tzinfo=datetime.timezone.utc)
    ans = sun.night(london.observer)
    assert datetime_almost_equal(ans[0], start, seconds=300)
    assert datetime_almost_equal(ans[1], end, seconds=300)
