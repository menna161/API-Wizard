import datetime
from typing import Tuple
import freezegun
import pytest
from almost_equal import datetime_almost_equal
from astral import LocationInfo, TimePeriod, sun
from astral.sun import Depression, SunDirection


@pytest.mark.parametrize('dt,angle', [(datetime.datetime(2022, 5, 1, 14, 0, 0), 32), (datetime.datetime(2022, 5, 1, 21, 20, 0), 126)])
def test_SolarZenith_Riyadh(dt: datetime.datetime, angle: float, riyadh: LocationInfo):
    dt = dt.replace(tzinfo=riyadh.tzinfo)
    zenith = sun.zenith(riyadh.observer, dt)
    assert (zenith == pytest.approx(angle, abs=0.5))
