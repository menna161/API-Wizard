import datetime
import pytest
from almost_equal import datetime_almost_equal
from astral import moon
from astral.location import Location


@pytest.mark.parametrize('date_,risetime', [(datetime.date(2022, 5, 1), datetime.datetime(2022, 5, 1, 2, 34, 0)), (datetime.date(2022, 5, 24), datetime.datetime(2022, 5, 24, 22, 59, 0))])
def test_moonrise_riyadh_utc(date_: datetime.date, risetime: datetime.datetime, riyadh: Location):
    risetime = risetime.replace(tzinfo=datetime.timezone.utc)
    calc_time = moon.moonrise(riyadh.observer, date_)
    assert (calc_time is not None)
    assert datetime_almost_equal(calc_time, risetime, seconds=180)
