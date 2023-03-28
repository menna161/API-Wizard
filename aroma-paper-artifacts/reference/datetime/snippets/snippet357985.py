import datetime
from typing import Tuple
import freezegun
import pytest
from almost_equal import datetime_almost_equal
from astral import LocationInfo, TimePeriod, sun
from astral.sun import Depression, SunDirection


@pytest.mark.parametrize('day,rahu', [(datetime.date(2015, 12, 1), (datetime.datetime(2015, 12, 1, 9, 17), datetime.datetime(2015, 12, 1, 10, 35))), (datetime.date(2015, 12, 2), (datetime.datetime(2015, 12, 2, 6, 40), datetime.datetime(2015, 12, 2, 7, 58)))])
def test_Rahukaalam(day: datetime.date, rahu: TimePeriod, new_delhi: LocationInfo):
    (start, end) = rahu
    start = start.replace(tzinfo=datetime.timezone.utc)
    end = end.replace(tzinfo=datetime.timezone.utc)
    info = sun.rahukaalam(new_delhi.observer, day)
    start_utc = info[0]
    end_utc = info[1]
    assert datetime_almost_equal(start, start_utc)
    assert datetime_almost_equal(end, end_utc)
