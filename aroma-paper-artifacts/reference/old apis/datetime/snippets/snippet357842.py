import datetime
from typing import Union
import pytest
from almost_equal import datetime_almost_equal
from astral.julian import Calendar, juliancentury_to_julianday, julianday, julianday_to_datetime, julianday_to_juliancentury


@pytest.mark.parametrize('day,jd', [(datetime.datetime(837, 4, 10, 7, 12, 0), 2026871.8), (datetime.datetime(333, 1, 27, 12, 0, 0), 1842713.0)])
def test_JulianDay_JulianCalendar(day: Union[(datetime.date, datetime.datetime)], jd: float):
    assert (julianday(day, Calendar.JULIAN) == jd)
