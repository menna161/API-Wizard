import datetime
from typing import Tuple
import freezegun
import pytest
from almost_equal import datetime_almost_equal
from astral import LocationInfo, TimePeriod, sun
from astral.sun import Depression, SunDirection


@pytest.mark.parametrize('day,sunrise', [(datetime.date(2015, 1, 1), datetime.datetime(2015, 1, 1, 8, 6)), (datetime.date(2015, 12, 1), datetime.datetime(2015, 12, 1, 7, 43)), (datetime.date(2015, 12, 2), datetime.datetime(2015, 12, 2, 7, 45)), (datetime.date(2015, 12, 3), datetime.datetime(2015, 12, 3, 7, 46)), (datetime.date(2015, 12, 12), datetime.datetime(2015, 12, 12, 7, 56)), (datetime.date(2015, 12, 25), datetime.datetime(2015, 12, 25, 8, 5))])
def test_Sunrise(day: datetime.date, sunrise: datetime.datetime, london: LocationInfo):
    sunrise = sunrise.replace(tzinfo=datetime.timezone.utc)
    sunrise_utc = sun.sunrise(london.observer, day)
    assert datetime_almost_equal(sunrise, sunrise_utc)
