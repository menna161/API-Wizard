import datetime
import freezegun
import pytest
from astral import Observer, sun, today
from astral.location import Location


def test_Elevation_WithoutRefraction(new_delhi: Location):
    d = datetime.datetime(2001, 6, 21, 13, 11, 0)
    assert (sun.elevation(new_delhi.observer, d, with_refraction=False) == pytest.approx(7.29, abs=0.1))
