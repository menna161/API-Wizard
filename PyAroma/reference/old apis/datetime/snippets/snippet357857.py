import dataclasses
import datetime
import freezegun
import pytest
from almost_equal import datetime_almost_equal
from astral import LocationInfo
from astral.location import Location
import zoneinfo
from backports import zoneinfo


def test_Sun(self, london: Location):
    "Test Location's version of the sun calculation"
    ldt = datetime.datetime(2015, 8, 1, 5, 23, 20, tzinfo=london.tzinfo)
    sunrise = london.sun(datetime.date(2015, 8, 1))['sunrise']
    assert datetime_almost_equal(sunrise, ldt)
