import datetime
from typing import Tuple
import freezegun
import pytest
from almost_equal import datetime_almost_equal
from astral import LocationInfo, TimePeriod, sun
from astral.sun import Depression, SunDirection


@freezegun.freeze_time('2015-12-01')
def test_SolarNoon_NoDate(london: LocationInfo):
    ans = datetime.datetime(2015, 12, 1, 11, 49, tzinfo=datetime.timezone.utc)
    noon = sun.noon(london.observer)
    assert datetime_almost_equal(noon, ans)
