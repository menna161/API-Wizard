import datetime
from typing import Tuple
import freezegun
import pytest
from almost_equal import datetime_almost_equal
from astral import LocationInfo, TimePeriod, sun
from astral.sun import Depression, SunDirection


@pytest.mark.parametrize('day,dawn', [(datetime.date(2015, 12, 1), datetime.datetime(2015, 12, 1, 6, 22)), (datetime.date(2015, 12, 2), datetime.datetime(2015, 12, 2, 6, 23)), (datetime.date(2015, 12, 3), datetime.datetime(2015, 12, 3, 6, 24)), (datetime.date(2015, 12, 12), datetime.datetime(2015, 12, 12, 6, 33)), (datetime.date(2015, 12, 25), datetime.datetime(2015, 12, 25, 6, 41))])
def test_Dawn_Nautical(day: datetime.date, dawn: datetime.datetime, london: LocationInfo):
    dawn = dawn.replace(tzinfo=datetime.timezone.utc)
    dawn_utc = sun.dawn(london.observer, day, 12)
    assert datetime_almost_equal(dawn, dawn_utc)
