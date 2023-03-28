import datetime
from typing import Union
from astral.julian import julianday_2000


def gmst(at: Union[(datetime.datetime, datetime.date)]) -> Degrees:
    'Calculate Greenwich Mean Sidereal Time in degrees'
    jd2000 = julianday_2000(at)
    t0 = (jd2000 / 36525)
    value = (((280.46061837 + (360.98564736629 * jd2000)) + (0.000387933 * pow(t0, 2))) + (pow(t0, 3) / 38710000))
    return (value % 360)
