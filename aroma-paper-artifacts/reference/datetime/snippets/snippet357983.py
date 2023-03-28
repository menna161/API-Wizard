import datetime
from typing import Tuple
import freezegun
import pytest
from almost_equal import datetime_almost_equal
from astral import LocationInfo, TimePeriod, sun
from astral.sun import Depression, SunDirection


@pytest.mark.parametrize('day,twilight', [(datetime.date(2019, 8, 29), (datetime.datetime(2019, 8, 29, 18, 54), datetime.datetime(2019, 8, 29, 19, 30)))])
def test_Twilight_SunSetting(day: datetime.date, twilight: TimePeriod, london: LocationInfo):
    (start, end) = twilight
    start = start.replace(tzinfo=datetime.timezone.utc)
    end = end.replace(tzinfo=datetime.timezone.utc)
    info = sun.twilight(london.observer, day, direction=SunDirection.SETTING)
    start_utc = info[0]
    end_utc = info[1]
    assert datetime_almost_equal(start, start_utc)
    assert datetime_almost_equal(end, end_utc)
