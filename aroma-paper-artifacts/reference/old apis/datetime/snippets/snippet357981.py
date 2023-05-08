import datetime
from typing import Tuple
import freezegun
import pytest
from almost_equal import datetime_almost_equal
from astral import LocationInfo, TimePeriod, sun
from astral.sun import Depression, SunDirection


@freezegun.freeze_time('2016-2-18')
def test_SolarMidnight_NoDate(london: LocationInfo):
    ans = datetime.datetime(2016, 2, 18, 0, 14, tzinfo=datetime.timezone.utc)
    midnight = sun.midnight(london.observer)
    assert datetime_almost_equal(midnight, ans)
