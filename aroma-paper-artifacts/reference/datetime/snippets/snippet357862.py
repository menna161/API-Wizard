import dataclasses
import datetime
import freezegun
import pytest
from almost_equal import datetime_almost_equal
from astral import LocationInfo
from astral.location import Location
import zoneinfo
from backports import zoneinfo


def test_SolarNoon(self, london: Location):
    ldt = datetime.datetime(2015, 8, 1, 13, 6, 53, tzinfo=london.tzinfo)
    noon = london.noon(datetime.date(2015, 8, 1))
    assert datetime_almost_equal(noon, ldt)
