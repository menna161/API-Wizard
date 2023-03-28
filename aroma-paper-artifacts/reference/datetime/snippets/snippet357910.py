import datetime
import pytest
from almost_equal import datetime_almost_equal
from astral import moon
from astral.location import Location


@pytest.mark.parametrize('date_,risetime', [(datetime.date(2021, 10, 28), datetime.datetime(2021, 10, 28, 2, 6, 0)), (datetime.date(2021, 11, 6), datetime.datetime(2021, 11, 6, 6, 45, 0))])
def test_moonrise_wellington(date_: datetime.date, risetime: datetime.datetime, wellington: Location):
    risetime = risetime.replace(tzinfo=wellington.tzinfo)
    calc_time = moon.moonrise(wellington.observer, date_, tzinfo=wellington.tzinfo)
    assert (calc_time is not None)
    calc_time = calc_time.astimezone(wellington.tzinfo)
    assert datetime_almost_equal(calc_time, risetime, seconds=120)
