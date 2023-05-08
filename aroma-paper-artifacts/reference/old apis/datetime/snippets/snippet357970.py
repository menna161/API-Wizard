import datetime
from typing import Tuple
import freezegun
import pytest
from almost_equal import datetime_almost_equal
from astral import LocationInfo, TimePeriod, sun
from astral.sun import Depression, SunDirection


@pytest.mark.parametrize('day,dawn', [(datetime.date(2015, 12, 1), datetime.datetime(2015, 12, 1, 5, 41)), (datetime.date(2015, 12, 2), datetime.datetime(2015, 12, 2, 5, 42)), (datetime.date(2015, 12, 3), datetime.datetime(2015, 12, 3, 5, 44)), (datetime.date(2015, 12, 12), datetime.datetime(2015, 12, 12, 5, 52)), (datetime.date(2015, 12, 25), datetime.datetime(2015, 12, 25, 6, 1))])
def test_Dawn_Astronomical(day: datetime.date, dawn: datetime.datetime, london: LocationInfo):
    dawn = dawn.replace(tzinfo=datetime.timezone.utc)
    dawn_utc = sun.dawn(london.observer, day, 18)
    assert datetime_almost_equal(dawn, dawn_utc)
