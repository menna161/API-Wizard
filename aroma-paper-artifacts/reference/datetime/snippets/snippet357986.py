import datetime
from typing import Tuple
import freezegun
import pytest
from almost_equal import datetime_almost_equal
from astral import LocationInfo, TimePeriod, sun
from astral.sun import Depression, SunDirection


@freezegun.freeze_time('2015-12-01')
def test_Rahukaalam_NoDate(new_delhi: LocationInfo):
    start = datetime.datetime(2015, 12, 1, 9, 17, tzinfo=datetime.timezone.utc)
    end = datetime.datetime(2015, 12, 1, 10, 35, tzinfo=datetime.timezone.utc)
    ans = sun.rahukaalam(new_delhi.observer)
    assert datetime_almost_equal(ans[0], start)
    assert datetime_almost_equal(ans[1], end)
