import datetime
import freezegun
import pytest
from astral import Observer, sun, today
from astral.location import Location


def test_Azimuth_Above85Degrees():
    d = datetime.datetime(2001, 6, 21, 13, 11, 0)
    assert (sun.azimuth(Observer(86, 77.2), d) == pytest.approx(276.21, abs=0.1))
