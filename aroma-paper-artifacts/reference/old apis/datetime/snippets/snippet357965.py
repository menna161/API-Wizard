import datetime
from typing import Tuple
import freezegun
import pytest
from almost_equal import datetime_almost_equal
from astral import LocationInfo, TimePeriod, sun
from astral.sun import Depression, SunDirection


@pytest.mark.parametrize('day,dawn', [(datetime.date(2015, 12, 1), datetime.datetime(2015, 12, 1, 7, 4)), (datetime.date(2015, 12, 2), datetime.datetime(2015, 12, 2, 7, 5)), (datetime.date(2015, 12, 3), datetime.datetime(2015, 12, 3, 7, 6)), (datetime.date(2015, 12, 12), datetime.datetime(2015, 12, 12, 7, 16)), (datetime.date(2015, 12, 25), datetime.datetime(2015, 12, 25, 7, 25))])
def test_Sun(day: datetime.date, dawn: datetime.datetime, london: LocationInfo):
    dawn = dawn.replace(tzinfo=datetime.timezone.utc)
    dawn_utc = sun.sun(london.observer, day)['dawn']
    assert datetime_almost_equal(dawn, dawn_utc)
