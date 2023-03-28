import dataclasses
import datetime
import freezegun
import pytest
from almost_equal import datetime_almost_equal
from astral import LocationInfo
from astral.location import Location
import zoneinfo
from backports import zoneinfo


def test_Dawn(self, london: Location):
    'Test Location returns dawn times in the local timezone'
    ldt = datetime.datetime(2015, 8, 1, 4, 41, 44, tzinfo=london.tzinfo)
    dawn = london.dawn(datetime.date(2015, 8, 1))
    assert datetime_almost_equal(dawn, ldt)
