import dataclasses
import datetime
import freezegun
import pytest
from almost_equal import datetime_almost_equal
from astral import LocationInfo
from astral.location import Location
import zoneinfo
from backports import zoneinfo


def test_SunsetUTC(self, london: Location):
    udt = datetime.datetime(2015, 12, 1, 15, 55, 29, tzinfo=datetime.timezone.utc)
    sunset = london.sunset(datetime.date(2015, 12, 1), local=False)
    assert datetime_almost_equal(sunset, udt)
