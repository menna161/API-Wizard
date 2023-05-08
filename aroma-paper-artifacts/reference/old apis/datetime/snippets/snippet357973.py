import datetime
from typing import Tuple
import freezegun
import pytest
from almost_equal import datetime_almost_equal
from astral import LocationInfo, TimePeriod, sun
from astral.sun import Depression, SunDirection


@pytest.mark.parametrize('day,sunset', [(datetime.date(2015, 1, 1), datetime.datetime(2015, 1, 1, 16, 1)), (datetime.date(2015, 12, 1), datetime.datetime(2015, 12, 1, 15, 55)), (datetime.date(2015, 12, 2), datetime.datetime(2015, 12, 2, 15, 54)), (datetime.date(2015, 12, 3), datetime.datetime(2015, 12, 3, 15, 54)), (datetime.date(2015, 12, 12), datetime.datetime(2015, 12, 12, 15, 51)), (datetime.date(2015, 12, 25), datetime.datetime(2015, 12, 25, 15, 55))])
def test_Sunset(day: datetime.date, sunset: datetime.datetime, london: LocationInfo):
    sunset = sunset.replace(tzinfo=datetime.timezone.utc)
    sunset_utc = sun.sunset(london.observer, day)
    assert datetime_almost_equal(sunset, sunset_utc)
