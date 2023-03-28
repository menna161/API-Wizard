import datetime
import pytest
from almost_equal import datetime_almost_equal
from astral import moon
from astral.location import Location


@pytest.mark.parametrize('date_,settime', [(datetime.date(2021, 10, 28), datetime.datetime(2021, 10, 28, 14, 11, 0)), (datetime.date(2021, 11, 6), datetime.datetime(2021, 11, 6, 17, 21, 0)), (datetime.date(2022, 2, 1), datetime.datetime(2022, 2, 1, 16, 57, 0))])
def test_moonset_utc(date_: datetime.date, settime: datetime.datetime, london: Location):
    settime = settime.replace(tzinfo=datetime.timezone.utc)
    calc_time = moon.moonset(london.observer, date_)
    assert (calc_time is not None)
    assert datetime_almost_equal(calc_time, settime, seconds=180)
