import datetime
from typing import Tuple
import freezegun
import pytest
from almost_equal import datetime_almost_equal
from astral import LocationInfo, TimePeriod, sun
from astral.sun import Depression, SunDirection


def test_TimeAtElevation_BadElevation(london: LocationInfo):
    d = datetime.date(2016, 1, 4)
    with pytest.raises(ValueError):
        sun.time_at_elevation(london.observer, 20, d, SunDirection.RISING)
