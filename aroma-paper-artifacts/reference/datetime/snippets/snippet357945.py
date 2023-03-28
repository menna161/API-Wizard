import datetime
import freezegun
import pytest
from astral import Observer, sun, today
from astral.location import Location


def test_Elevation(new_delhi: Location):
    d = datetime.datetime(2001, 6, 21, 13, 11, 0)
    assert (sun.elevation(new_delhi.observer, d) == pytest.approx(7.41, abs=0.1))
