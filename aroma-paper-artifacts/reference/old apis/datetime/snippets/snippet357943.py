import datetime
import freezegun
import pytest
from astral import Observer, sun, today
from astral.location import Location


@pytest.mark.parametrize('d,ha', [(datetime.date(2012, 1, 1), 1.03555238), (datetime.date(3200, 11, 14), 1.172253118), (datetime.date(2018, 6, 1), 2.133712555)])
def test_HourAngle(d: datetime.date, ha: float, london: Location):
    midday = datetime.time(12, 0, 0)
    jd = sun.julianday(datetime.datetime.combine(d, midday))
    jc = sun.julianday_to_juliancentury(jd)
    decl = sun.sun_declination(jc)
    assert (sun.hour_angle(london.latitude, decl, 90.8333, sun.SunDirection.RISING) == pytest.approx(ha, abs=0.1))
