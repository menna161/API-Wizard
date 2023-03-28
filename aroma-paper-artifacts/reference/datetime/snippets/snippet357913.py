from datetime import datetime, timedelta, timezone
import pytest
import astral
from astral import sun
from astral.location import Location


def _next_event(obs: astral.Observer, dt: datetime, event: str):
    for offset in range(0, 365):
        newdate = (dt + timedelta(days=offset))
        try:
            t = getattr(sun, event)(date=newdate, observer=obs)
            return t
        except ValueError:
            pass
    assert False, 'Should be unreachable'
