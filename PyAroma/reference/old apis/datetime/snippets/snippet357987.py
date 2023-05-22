import datetime
from typing import Tuple
import freezegun
import pytest
from almost_equal import datetime_almost_equal
from astral import LocationInfo, TimePeriod, sun
from astral.sun import Depression, SunDirection


@pytest.mark.parametrize('dt,angle', [(datetime.datetime(2015, 12, 14, 11, 0, 0), 14.381311), (datetime.datetime(2015, 12, 14, 20, 1, 0), (- 37.3710156))])
def test_SolarAltitude(dt: datetime.datetime, angle: float, london: LocationInfo):
    elevation = sun.elevation(london.observer, dt)
    assert (elevation == pytest.approx(angle, abs=0.5))
