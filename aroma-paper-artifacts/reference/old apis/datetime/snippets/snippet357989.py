import datetime
from typing import Tuple
import freezegun
import pytest
from almost_equal import datetime_almost_equal
from astral import LocationInfo, TimePeriod, sun
from astral.sun import Depression, SunDirection


@pytest.mark.parametrize('dt,angle', [(datetime.datetime(2015, 12, 14, 11, 0, 0), 166.9676), (datetime.datetime(2015, 12, 14, 20, 1, 0), 279.39927311745)])
def test_SolarAzimuth(dt: datetime.datetime, angle: float, london: LocationInfo):
    azimuth = sun.azimuth(london.observer, dt)
    assert (azimuth == pytest.approx(angle, abs=0.5))
