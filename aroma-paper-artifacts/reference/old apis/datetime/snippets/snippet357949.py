import datetime
import freezegun
import pytest
from astral import Observer, sun, today
from astral.location import Location


def test_Elevation_Above85Degrees():
    d = datetime.datetime(2001, 6, 21, 13, 11, 0)
    assert (sun.elevation(Observer(86, 77.2), d) == pytest.approx(23.102501151619506, abs=0.001))
