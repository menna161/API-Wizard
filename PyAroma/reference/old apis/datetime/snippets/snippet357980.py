import datetime
from typing import Tuple
import freezegun
import pytest
from almost_equal import datetime_almost_equal
from astral import LocationInfo, TimePeriod, sun
from astral.sun import Depression, SunDirection


@pytest.mark.parametrize('day,midnight', [(datetime.date(2016, 2, 18), datetime.datetime(2016, 2, 18, 0, 14)), (datetime.date(2016, 10, 26), datetime.datetime(2016, 10, 25, 23, 44))])
def test_SolarMidnight(day: datetime.date, midnight: datetime.datetime, london: LocationInfo):
    solar_midnight = midnight.replace(tzinfo=datetime.timezone.utc)
    solar_midnight_utc = sun.midnight(london.observer, day)
    assert datetime_almost_equal(solar_midnight, solar_midnight_utc)
