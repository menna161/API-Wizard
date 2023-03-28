import datetime
from dataclasses import dataclass, field, replace
from math import asin, atan2, cos, degrees, fabs, pi, radians, sin, sqrt
from typing import Callable, List, Optional, Union
from astral import AstralBodyPosition, Observer, now, today
from astral.julian import julianday, julianday_2000
from astral.sidereal import lmst
from astral.table4 import Table4Row, table4_u, table4_v, table4_w
import zoneinfo
from backports import zoneinfo


def riseset(on: datetime.date, observer: Observer):
    'Calculate rise and set times'
    jd2000 = julianday_2000(on)
    t0 = lmst(on, observer.longitude)
    m: List[AstralBodyPosition] = []
    for interval in range(3):
        pos = moon_position((jd2000 + (interval * 0.5)))
        m.append(pos)
    for interval in range(1, 3):
        if (m[interval].right_ascension <= m[(interval - 1)].right_ascension):
            m[interval].right_ascension = (m[interval].right_ascension + (2 * pi))
    moon_position_window: List[AstralBodyPosition] = [replace(m[0]), AstralBodyPosition(), AstralBodyPosition()]
    rise_time = None
    set_time = None
    for hour in range(24):
        ph = ((hour + 1) / 24)
        moon_position_window[2].right_ascension = interpolate(m[0].right_ascension, m[1].right_ascension, m[2].right_ascension, ph)
        moon_position_window[2].declination = interpolate(m[0].declination, m[1].declination, m[2].declination, ph)
        transit_info = moon_transit_event(hour, t0, observer.latitude, m[1].distance, moon_position_window)
        if isinstance(transit_info, NoTransit):
            moon_position_window[2].distance = transit_info.parallax
        else:
            query_time = datetime.datetime(on.year, on.month, on.day, hour, 0, 0, tzinfo=datetime.timezone.utc)
            if (transit_info.event == 'rise'):
                event_time = transit_info.when
                event = datetime.datetime(on.year, on.month, on.day, event_time.hour, event_time.minute, 0, tzinfo=datetime.timezone.utc)
                if (rise_time is None):
                    rise_time = event
                else:
                    rq_diff = (rise_time - query_time).total_seconds()
                    eq_diff = (event - query_time).total_seconds()
                    if (set_time is not None):
                        sq_diff = (set_time - query_time).total_seconds()
                    else:
                        sq_diff = 0
                    update_rise_time = ((sgn(rq_diff) == sgn(eq_diff)) and (fabs(rq_diff) > fabs(eq_diff)))
                    update_rise_time |= ((sgn(rq_diff) != sgn(eq_diff)) and ((set_time is not None) and (sgn(rq_diff) == sgn(sq_diff))))
                    if update_rise_time:
                        rise_time = event
            elif (transit_info.event == 'set'):
                event_time = transit_info.when
                event = datetime.datetime(on.year, on.month, on.day, event_time.hour, event_time.minute, 0, tzinfo=datetime.timezone.utc)
                if (set_time is None):
                    set_time = event
                else:
                    sq_diff = (set_time - query_time).total_seconds()
                    eq_diff = (event - query_time).total_seconds()
                    if (rise_time is not None):
                        rq_diff = (rise_time - query_time).total_seconds()
                    else:
                        rq_diff = 0
                    update_set_time = ((sgn(sq_diff) == sgn(eq_diff)) and (fabs(sq_diff) > fabs(eq_diff)))
                    update_set_time |= ((sgn(sq_diff) != sgn(eq_diff)) and ((rise_time is not None) and (sgn(rq_diff) == sgn(sq_diff))))
                    if update_set_time:
                        set_time = event
        moon_position_window[0].right_ascension = moon_position_window[2].right_ascension
        moon_position_window[0].declination = moon_position_window[2].declination
        moon_position_window[0].distance = moon_position_window[2].distance
    return (rise_time, set_time)
