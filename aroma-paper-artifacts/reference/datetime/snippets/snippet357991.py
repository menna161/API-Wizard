import datetime
from typing import Tuple
import freezegun
import pytest
from almost_equal import datetime_almost_equal
from astral import LocationInfo, TimePeriod, sun
from astral.sun import Depression, SunDirection


@pytest.mark.parametrize('dt,angle', [(datetime.datetime(2021, 10, 10, 6, 0, 0), 102.6), (datetime.datetime(2021, 10, 10, 7, 0, 0), 93.3), (datetime.datetime(2021, 10, 10, 18, 0, 0), 87.8), (datetime.datetime(2019, 8, 29, 14, 34, 0), 46), (datetime.datetime(2020, 2, 3, 10, 37, 0), 71)])
def test_SolarZenith_London(dt: datetime.datetime, angle: float, london: LocationInfo):
    dt = dt.replace(tzinfo=london.tzinfo)
    zenith = sun.zenith(london.observer, dt)
    assert (zenith == pytest.approx(angle, abs=0.5))
