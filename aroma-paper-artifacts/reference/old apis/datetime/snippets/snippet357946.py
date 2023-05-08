import datetime
import freezegun
import pytest
from astral import Observer, sun, today
from astral.location import Location


def test_Elevation_NonNaive(new_delhi: Location):
    d = datetime.datetime(2001, 6, 21, 18, 41, 0, tzinfo=new_delhi.tzinfo)
    assert (sun.elevation(new_delhi.observer, d) == pytest.approx(7.41, abs=0.1))
