import datetime
import pytest
from almost_equal import datetime_almost_equal
from astral import moon
from astral.location import Location


@pytest.mark.parametrize('date_,risetime', [(datetime.date(2022, 11, 30), datetime.datetime(2022, 11, 30, 13, 17, 0)), (datetime.date(2022, 1, 1), datetime.datetime(2022, 1, 1, 6, 55, 0)), (datetime.date(2022, 2, 1), datetime.datetime(2022, 2, 1, 8, 24, 0))])
def test_moonrise_utc(date_: datetime.date, risetime: datetime.datetime, london: Location):
    risetime = risetime.replace(tzinfo=london.tzinfo)
    calc_time = moon.moonrise(london.observer, date_)
    assert (calc_time is not None)
    assert datetime_almost_equal(calc_time, risetime, seconds=300)
