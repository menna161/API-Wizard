import datetime
import re


def parse_rfc3339_re(m):
    r = map(int, m.groups()[:6])
    if m.group(7):
        micro = float(m.group(7))
    else:
        micro = 0
    if m.group(8):
        g = ((int(m.group(8), 10) * 60) + int(m.group(9), 10))
        tz = _TimeZone(datetime.timedelta(0, (g * 60)))
    else:
        tz = _TimeZone(datetime.timedelta(0, 0))
    (y, m, d, H, M, S) = r
    return datetime.datetime(y, m, d, H, M, S, int((micro * 1000000)), tz)
