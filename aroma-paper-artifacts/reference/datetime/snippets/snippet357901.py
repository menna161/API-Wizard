import datetime
import pytest
from astral import Observer
from astral.location import Location
from astral.moon import azimuth


def print_moon_azimuth():
    o = Observer(51.5, (- 0.13))
    for hour in range(24):
        d = datetime.datetime(2022, 10, 10, hour, 0, 0)
        print(hour, ' 0', azimuth(o, d))
        d = datetime.datetime(2022, 10, 10, hour, 30, 0)
        print(hour, '30', azimuth(o, d))
