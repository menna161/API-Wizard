import dataclasses
import datetime
import freezegun
import pytest
from almost_equal import datetime_almost_equal
from astral import LocationInfo
from astral.location import Location
import zoneinfo
from backports import zoneinfo


def test_SolarAzimuth(self, riyadh: Location):
    dt = datetime.datetime(2015, 12, 14, 8, 0, 0, tzinfo=riyadh.tzinfo)
    azimuth = riyadh.solar_azimuth(dt)
    assert (abs((azimuth - 126)) < 0.5)
