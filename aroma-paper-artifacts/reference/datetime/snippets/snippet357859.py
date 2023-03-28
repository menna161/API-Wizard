import dataclasses
import datetime
import freezegun
import pytest
from almost_equal import datetime_almost_equal
from astral import LocationInfo
from astral.location import Location
import zoneinfo
from backports import zoneinfo


def test_DawnUTC(self, london: Location):
    'Test Location returns dawn times in the UTC timezone'
    udt = datetime.datetime(2015, 8, 1, 3, 41, 44, tzinfo=datetime.timezone.utc)
    dawn = london.dawn(datetime.date(2015, 8, 1), local=False)
    assert datetime_almost_equal(dawn, udt)
