import datetime
from typing import Union
import pytest
from almost_equal import datetime_almost_equal
from astral.julian import Calendar, juliancentury_to_julianday, julianday, julianday_to_datetime, julianday_to_juliancentury


@pytest.mark.parametrize('day,jd', [(datetime.datetime(1957, 10, 4, 19, 26, 24), 2436116.31), (datetime.date(2000, 1, 1), 2451544.5), (datetime.date(2012, 1, 1), 2455927.5), (datetime.date(2013, 1, 1), 2456293.5), (datetime.date(2013, 6, 1), 2456444.5), (datetime.date(1867, 2, 1), 2402998.5), (datetime.date(3200, 11, 14), 2890153.5), (datetime.datetime(2000, 1, 1, 12, 0, 0), 2451545.0), (datetime.datetime(1999, 1, 1, 0, 0, 0), 2451179.5), (datetime.datetime(1987, 1, 27, 0, 0, 0), 2446822.5), (datetime.date(1987, 6, 19), 2446965.5), (datetime.datetime(1987, 6, 19, 12, 0, 0), 2446966.0), (datetime.datetime(1988, 1, 27, 0, 0, 0), 2447187.5), (datetime.date(1988, 6, 19), 2447331.5), (datetime.datetime(1988, 6, 19, 12, 0, 0), 2447332.0), (datetime.datetime(1900, 1, 1, 0, 0, 0), 2415020.5), (datetime.datetime(1600, 1, 1, 0, 0, 0), 2305447.5), (datetime.datetime(1600, 12, 31, 0, 0, 0), 2305812.5), (datetime.datetime(2012, 1, 1, 12), 2455928.0), (datetime.date(2013, 1, 1), 2456293.5), (datetime.date(2013, 6, 1), 2456444.5), (datetime.date(1867, 2, 1), 2402998.5), (datetime.date(3200, 11, 14), 2890153.5)])
def test_JulianDay(day: Union[(datetime.date, datetime.datetime)], jd: float):
    assert (julianday(day) == jd)
