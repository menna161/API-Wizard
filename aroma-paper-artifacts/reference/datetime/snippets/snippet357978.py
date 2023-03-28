import datetime
from typing import Tuple
import freezegun
import pytest
from almost_equal import datetime_almost_equal
from astral import LocationInfo, TimePeriod, sun
from astral.sun import Depression, SunDirection


@pytest.mark.parametrize('day,noon', [(datetime.date(2015, 12, 1), datetime.datetime(2015, 12, 1, 11, 49)), (datetime.date(2015, 12, 2), datetime.datetime(2015, 12, 2, 11, 49)), (datetime.date(2015, 12, 3), datetime.datetime(2015, 12, 3, 11, 50)), (datetime.date(2015, 12, 12), datetime.datetime(2015, 12, 12, 11, 54)), (datetime.date(2015, 12, 25), datetime.datetime(2015, 12, 25, 12, 0))])
def test_SolarNoon(day: datetime.date, noon: datetime.datetime, london: LocationInfo):
    noon = noon.replace(tzinfo=datetime.timezone.utc)
    noon_utc = sun.noon(london.observer, day)
    assert datetime_almost_equal(noon, noon_utc)
