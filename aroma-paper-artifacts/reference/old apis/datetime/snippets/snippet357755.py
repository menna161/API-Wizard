import dataclasses
import datetime
from typing import Any, Dict, Optional, Tuple, Union
import astral.moon
import astral.sun
from astral import Depression, Elevation, LocationInfo, Observer, SunDirection, dms_to_float, today
import zoneinfo
from backports import zoneinfo


def solar_elevation(self, dateandtime: Optional[datetime.datetime]=None, observer_elevation: Elevation=0.0) -> float:
    'Calculates the solar elevation angle for a specific time.\n\n        :param dateandtime: The date and time for which to calculate the angle.\n\n        :returns: The elevation angle in degrees above the horizon.\n        '
    if (dateandtime is None):
        dateandtime = astral.sun.now(self.tzinfo)
    elif (not dateandtime.tzinfo):
        dateandtime = dateandtime.replace(tzinfo=self.tzinfo)
    observer = Observer(self.latitude, self.longitude, observer_elevation)
    dateandtime = dateandtime.astimezone(datetime.timezone.utc)
    return astral.sun.elevation(observer, dateandtime)