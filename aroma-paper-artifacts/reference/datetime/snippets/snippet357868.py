import dataclasses
import datetime
import freezegun
import pytest
from almost_equal import datetime_almost_equal
from astral import LocationInfo
from astral.location import Location
import zoneinfo
from backports import zoneinfo


def test_SolarElevation(self, riyadh: Location):
    dt = datetime.datetime(2015, 12, 14, 8, 0, 0, tzinfo=riyadh.tzinfo)
    elevation = riyadh.solar_elevation(dt)
    assert (abs((elevation - 17)) < 0.5)
