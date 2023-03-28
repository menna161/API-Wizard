from datetime import datetime, timedelta, timezone
import pytest
import astral
from astral import sun
from astral.location import Location


def test_NorwaySunUp(tromso: Location):
    "Test location in Norway where the sun doesn't set in summer."
    june = datetime(2019, 6, 5, tzinfo=timezone.utc)
    with pytest.raises(ValueError):
        sun.sunrise(tromso.observer, june)
    with pytest.raises(ValueError):
        sun.sunset(tromso.observer, june)
    next_sunrise = _next_event(tromso.observer, june, 'sunrise')
    next_sunset = _next_event(tromso.observer, june, 'sunset')
    assert (next_sunset < next_sunrise)
