import datetime
import freezegun
import pytest
from almost_equal import datetime_almost_equal
from astral import TimePeriod, sun
from astral.location import Location
from astral.sun import SunDirection


@pytest.mark.parametrize('day,golden_hour', [(datetime.date(2015, 12, 1), (datetime.datetime(2015, 12, 1, 1, 10, 10), datetime.datetime(2015, 12, 1, 2, 0, 43))), (datetime.date(2016, 1, 1), (datetime.datetime(2016, 1, 1, 1, 27, 46), datetime.datetime(2016, 1, 1, 2, 19, 1)))])
def test_morning(self, day: datetime.date, golden_hour: TimePeriod, new_delhi: Location):
    start1 = golden_hour[0].replace(tzinfo=datetime.timezone.utc)
    end1 = golden_hour[1].replace(tzinfo=datetime.timezone.utc)
    (start2, end2) = sun.golden_hour(new_delhi.observer, day, SunDirection.RISING)
    assert datetime_almost_equal(end1, end2, seconds=90)
    assert datetime_almost_equal(start1, start2, seconds=90)
