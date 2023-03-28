import datetime
import freezegun
import pytest
from astral import Observer, sun, today
from astral.location import Location


def test_Azimuth(new_delhi: Location):
    d = datetime.datetime(2001, 6, 21, 13, 11, 0)
    assert (sun.azimuth(new_delhi.observer, d) == pytest.approx(292.76, abs=0.1))
