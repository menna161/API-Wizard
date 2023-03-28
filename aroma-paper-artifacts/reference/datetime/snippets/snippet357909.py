import datetime
import pytest
from almost_equal import datetime_almost_equal
from astral import moon
from astral.location import Location


@pytest.mark.parametrize('date_,settime', [(datetime.date(2021, 10, 28), datetime.datetime(2021, 10, 28, 9, 26, 0)), (datetime.date(2021, 11, 6), datetime.datetime(2021, 11, 6, 15, 33, 0)), (datetime.date(2022, 2, 1), datetime.datetime(2022, 2, 1, 14, 54, 0))])
def test_moonset_riyadh_utc(date_: datetime.date, settime: datetime.datetime, riyadh: Location):
    settime = settime.replace(tzinfo=datetime.timezone.utc)
    calc_time = moon.moonset(riyadh.observer, date_)
    assert (calc_time is not None)
    assert datetime_almost_equal(calc_time, settime, seconds=180)
