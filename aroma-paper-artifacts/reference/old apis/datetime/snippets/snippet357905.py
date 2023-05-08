import datetime
import pytest
from almost_equal import datetime_almost_equal
from astral import moon
from astral.location import Location


@pytest.mark.parametrize('date_,phase', [(datetime.date(2015, 12, 1), 19.477889), (datetime.date(2015, 12, 2), 20.333444), (datetime.date(2015, 12, 3), 21.189), (datetime.date(2014, 12, 1), 9.0556666), (datetime.date(2014, 12, 2), 10.066777), (datetime.date(2014, 1, 1), 27.955666)])
def test_moon_phase(date_: datetime.date, phase: float):
    'Test moon phase calculation'
    assert (moon.phase(date_) == pytest.approx(phase, abs=0.001))
