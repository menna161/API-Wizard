import datetime
import freezegun
import pytest
from almost_equal import datetime_almost_equal
from astral import TimePeriod, sun
from astral.location import Location
from astral.sun import SunDirection


def test_morning(self, london: Location):
    test_data = {datetime.date(2016, 5, 19): (datetime.datetime(2016, 5, 19, 3, 19), datetime.datetime(2016, 5, 19, 3, 36))}
    for (day, blue_hour) in test_data.items():
        start1 = blue_hour[0].replace(tzinfo=datetime.timezone.utc)
        end1 = blue_hour[1].replace(tzinfo=datetime.timezone.utc)
        (start2, end2) = sun.blue_hour(london.observer, day, SunDirection.RISING)
        assert datetime_almost_equal(end1, end2, seconds=90)
        assert datetime_almost_equal(start1, start2, seconds=90)
