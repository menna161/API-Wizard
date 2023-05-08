import datetime
import pytest
from almost_equal import datetime_almost_equal
from astral import moon
from astral.location import Location


@pytest.mark.parametrize('date_,settime', [(datetime.date(2021, 8, 18), datetime.datetime(2021, 8, 18, 3, 31, 0)), (datetime.date(2021, 7, 8), datetime.datetime(2021, 7, 8, 15, 16, 0))])
def test_moonset_wellington(date_: datetime.date, settime: datetime.datetime, wellington: Location):
    settime = settime.replace(tzinfo=wellington.tzinfo)
    calc_time = moon.moonset(wellington.observer, date_, wellington.tzinfo)
    assert (calc_time is not None)
    calc_time = calc_time.astimezone(wellington.tzinfo)
    assert datetime_almost_equal(calc_time, settime, seconds=120)
