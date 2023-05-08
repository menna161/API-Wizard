import datetime
from typing import Tuple
import freezegun
import pytest
from almost_equal import datetime_almost_equal
from astral import LocationInfo, TimePeriod, sun
from astral.sun import Depression, SunDirection


@pytest.mark.parametrize('day,dusk', [(datetime.date(2015, 12, 1), datetime.datetime(2015, 12, 1, 17, 16)), (datetime.date(2015, 12, 2), datetime.datetime(2015, 12, 2, 17, 16)), (datetime.date(2015, 12, 3), datetime.datetime(2015, 12, 3, 17, 16)), (datetime.date(2015, 12, 12), datetime.datetime(2015, 12, 12, 17, 14)), (datetime.date(2015, 12, 25), datetime.datetime(2015, 12, 25, 17, 19))])
def test_Dusk_Nautical(day: datetime.date, dusk: datetime.datetime, london: LocationInfo):
    dusk = dusk.replace(tzinfo=datetime.timezone.utc)
    dusk_utc = sun.dusk(london.observer, day, 12)
    assert datetime_almost_equal(dusk, dusk_utc)
