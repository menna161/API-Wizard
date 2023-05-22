import dataclasses
import datetime
import freezegun
import pytest
from almost_equal import datetime_almost_equal
from astral import LocationInfo
from astral.location import Location
import zoneinfo
from backports import zoneinfo


def test_Dusk(self, london: Location):
    ldt = datetime.datetime(2015, 12, 1, 16, 35, 11, tzinfo=london.tzinfo)
    dusk = london.dusk(datetime.date(2015, 12, 1))
    assert datetime_almost_equal(dusk, ldt)
