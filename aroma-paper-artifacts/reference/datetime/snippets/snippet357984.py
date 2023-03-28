import datetime
from typing import Tuple
import freezegun
import pytest
from almost_equal import datetime_almost_equal
from astral import LocationInfo, TimePeriod, sun
from astral.sun import Depression, SunDirection


@freezegun.freeze_time('2019-8-29')
def test_Twilight_NoDate(london: LocationInfo):
    start = datetime.datetime(2019, 8, 29, 18, 54, tzinfo=datetime.timezone.utc)
    end = datetime.datetime(2019, 8, 29, 19, 30, tzinfo=datetime.timezone.utc)
    ans = sun.twilight(london.observer, direction=SunDirection.SETTING)
    assert datetime_almost_equal(ans[0], start)
    assert datetime_almost_equal(ans[1], end)
