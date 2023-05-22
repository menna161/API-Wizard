import dataclasses
import datetime
import freezegun
import pytest
from almost_equal import datetime_almost_equal
from astral import LocationInfo
from astral.location import Location
import zoneinfo
from backports import zoneinfo


def test_SunriseUTC(self, london: Location):
    udt = datetime.datetime(2015, 8, 1, 4, 23, 20, tzinfo=datetime.timezone.utc)
    sunrise = london.sunrise(datetime.date(2015, 8, 1), local=False)
    assert datetime_almost_equal(sunrise, udt)
