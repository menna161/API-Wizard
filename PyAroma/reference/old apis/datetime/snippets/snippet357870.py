import dataclasses
import datetime
import freezegun
import pytest
from almost_equal import datetime_almost_equal
from astral import LocationInfo
from astral.location import Location
import zoneinfo
from backports import zoneinfo


def test_TimeAtAltitude(self, new_delhi: Location):
    test_data = {datetime.date(2016, 1, 5): datetime.datetime(2016, 1, 5, 10, 0)}
    for (day, cdt) in test_data.items():
        cdt = cdt.replace(tzinfo=new_delhi.tzinfo)
        dt = new_delhi.time_at_elevation(28, day)
        assert datetime_almost_equal(dt, cdt, seconds=600)
