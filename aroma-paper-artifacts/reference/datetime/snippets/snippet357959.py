import datetime
import freezegun
import pytest
from almost_equal import datetime_almost_equal
from astral import TimePeriod, sun
from astral.location import Location
from astral.sun import SunDirection


@freezegun.freeze_time('2015-12-1')
def test_no_date(self, new_delhi: Location):
    start = datetime.datetime(2015, 12, 1, 1, 10, 10, tzinfo=datetime.timezone.utc)
    end = datetime.datetime(2015, 12, 1, 2, 0, 43, tzinfo=datetime.timezone.utc)
    ans = sun.golden_hour(new_delhi.observer)
    assert datetime_almost_equal(ans[0], start, 90)
    assert datetime_almost_equal(ans[1], end, 90)
