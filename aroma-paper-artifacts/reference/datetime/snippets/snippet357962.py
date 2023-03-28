import datetime
import freezegun
import pytest
from almost_equal import datetime_almost_equal
from astral import TimePeriod, sun
from astral.location import Location
from astral.sun import SunDirection


@freezegun.freeze_time('2016-5-19')
def test_no_date(self, london: Location):
    start = datetime.datetime(2016, 5, 19, 20, 18, tzinfo=datetime.timezone.utc)
    end = datetime.datetime(2016, 5, 19, 20, 35, tzinfo=datetime.timezone.utc)
    ans = sun.blue_hour(london.observer, direction=SunDirection.SETTING)
    assert datetime_almost_equal(ans[0], start, 90)
    assert datetime_almost_equal(ans[1], end, 90)
