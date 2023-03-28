import dataclasses
import datetime
import freezegun
import pytest
from almost_equal import datetime_almost_equal
from astral import LocationInfo
from astral.location import Location
import zoneinfo
from backports import zoneinfo


def test_Moon(self):
    d = datetime.date(2017, 12, 1)
    c = Location()
    assert (c.moon_phase(date=d) == pytest.approx(11.62, abs=0.01))
