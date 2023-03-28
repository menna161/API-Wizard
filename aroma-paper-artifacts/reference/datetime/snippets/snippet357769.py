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


def moon_transit_event(hour: float, lmst: Degrees, latitude: Degrees, distance: float, window: List[AstralBodyPosition]) -> Union[(TransitEvent, NoTransit)]:
    'Check if the moon transits the horizon within the window.\n\n    Args:\n        hour: Hour of the day\n        lmst: Local mean sidereal time in degrees\n        latitude: Observer latitude\n        distance: Distance to the moon\n        window: Sliding window of moon positions that covers a part of the day\n    '
    mst = radians(lmst)
    hour_angle = [0.0, 0.0, 0.0]
    k1 = radians((15 * 1.0027379097096139))
    if (window[2].right_ascension < window[0].right_ascension):
        window[2].right_ascension = (window[2].right_ascension + (2 * pi))
    hour_angle[0] = ((mst - window[0].right_ascension) + (hour * k1))
    hour_angle[2] = (((mst - window[2].right_ascension) + (hour * k1)) + k1)
    hour_angle[1] = ((hour_angle[2] + hour_angle[0]) / 2)
    window[1].declination = ((window[2].declination + window[0].declination) / 2)
    sl = sin(radians(latitude))
    cl = cos(radians(latitude))
    z = cos(radians(((90 + MOON_APPARENT_RADIUS) - (41.685 / distance))))
    if (hour == 0):
        window[0].distance = (((sl * sin(window[0].declination)) + ((cl * cos(window[0].declination)) * cos(hour_angle[0]))) - z)
    window[2].distance = (((sl * sin(window[2].declination)) + ((cl * cos(window[2].declination)) * cos(hour_angle[2]))) - z)
    if (sgn(window[0].distance) == sgn(window[2].distance)):
        return NoTransit(window[2].distance)
    window[1].distance = (((sl * sin(window[1].declination)) + ((cl * cos(window[1].declination)) * cos(hour_angle[1]))) - z)
    a = (((2 * window[2].distance) - (4 * window[1].distance)) + (2 * window[0].distance))
    b = (((4 * window[1].distance) - (3 * window[0].distance)) - window[2].distance)
    discriminant = ((b * b) - ((4 * a) * window[0].distance))
    if (discriminant < 0):
        return NoTransit(window[2].distance)
    discriminant = sqrt(discriminant)
    e = (((- b) + discriminant) / (2 * a))
    if ((e > 1) or (e < 0)):
        e = (((- b) - discriminant) / (2 * a))
    time = ((hour + e) + (1 / 120))
    h = int(time)
    m = int(((time - h) * 60))
    sd = sin(window[1].declination)
    cd = cos(window[1].declination)
    hour_angle_crossing = (hour_angle[0] + (e * (hour_angle[2] - hour_angle[0])))
    sh = sin(hour_angle_crossing)
    ch = cos(hour_angle_crossing)
    x = ((cl * sd) - ((sl * cd) * ch))
    y = ((- cd) * sh)
    az = degrees(atan2(y, x))
    if (az < 0):
        az += 360
    if (az > 360):
        az -= 360
    event_time = datetime.time(h, m, 0)
    if ((window[0].distance < 0) and (window[2].distance > 0)):
        return TransitEvent('rise', event_time, az, window[2].distance)
    if ((window[0].distance > 0) and (window[2].distance < 0)):
        return TransitEvent('set', event_time, az, window[2].distance)
    return NoTransit(window[2].distance)
