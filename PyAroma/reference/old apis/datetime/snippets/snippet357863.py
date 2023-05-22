import dataclasses
import datetime
import freezegun
import pytest
from almost_equal import datetime_almost_equal
from astral import LocationInfo
from astral.location import Location
import zoneinfo
from backports import zoneinfo


def test_SolarNoonUTC(self, london: Location):
    udt = datetime.datetime(2015, 8, 1, 12, 6, 53, tzinfo=datetime.timezone.utc)
    noon = london.noon(datetime.date(2015, 8, 1), local=False)
    assert datetime_almost_equal(noon, udt)
