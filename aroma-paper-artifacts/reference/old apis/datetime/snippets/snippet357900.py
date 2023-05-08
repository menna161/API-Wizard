import datetime
import pytest
from astral import Observer
from astral.location import Location
from astral.moon import azimuth


@pytest.mark.parametrize('dt,value', [(datetime.datetime(2022, 10, 6, 1, 10, 0), 240.0), (datetime.datetime(2022, 10, 6, 16, 45, 0), 115.0), (datetime.datetime(2022, 10, 10, 6, 43, 0), 281.0), (datetime.datetime(2022, 10, 10, 3, 0, 0), 235.0)])
def test_moon_azimuth(dt: datetime.datetime, value: float, london: Location):
    az = azimuth(london.observer, dt)
    assert (pytest.approx(az, abs=1) == value)
