import dataclasses
import datetime
from typing import Any, Dict, Optional, Tuple, Union
import astral.moon
import astral.sun
from astral import Depression, Elevation, LocationInfo, Observer, SunDirection, dms_to_float, today
import zoneinfo
from backports import zoneinfo


def solar_zenith(self, dateandtime: Optional[datetime.datetime]=None, observer_elevation: Elevation=0.0) -> float:
    'Calculates the solar zenith angle for a specific time.\n\n        :param dateandtime: The date and time for which to calculate the angle.\n        :returns: The zenith angle in degrees from vertical.\n        '
    return (90.0 - self.solar_elevation(dateandtime, observer_elevation))
