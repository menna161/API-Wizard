import dataclasses
import datetime
from typing import Any, Dict, Optional, Tuple, Union
import astral.moon
import astral.sun
from astral import Depression, Elevation, LocationInfo, Observer, SunDirection, dms_to_float, today
import zoneinfo
from backports import zoneinfo


def time_at_elevation(self, elevation: float, date: Optional[datetime.date]=None, direction: SunDirection=SunDirection.RISING, local: bool=True) -> datetime.datetime:
    "Calculate the time when the sun is at the specified elevation.\n\n        Note:\n            This method uses positive elevations for those above the horizon.\n\n            Elevations greater than 90 degrees are converted to a setting sun\n            i.e. an elevation of 110 will calculate a setting sun at 70 degrees.\n\n        :param elevation:  Elevation in degrees above the horizon to calculate for.\n\n        :param date: The date for which to calculate the elevation time.\n                     If no date is specified then the current date will be used.\n\n        :param direction:  Determines whether the time is for the sun rising or setting.\n                           Use ``SunDirection.RISING`` or ``SunDirection.SETTING``.\n                           Default is rising.\n\n        :param local: True  = Time to be returned in location's time zone;\n                      False = Time to be returned in UTC.\n                      If not specified then the time will be returned in local time\n\n        :returns: The date and time at which dusk occurs.\n        "
    if (local and (self.timezone is None)):
        raise ValueError('Local time requested but Location has no timezone set.')
    if (date is None):
        date = self.today(local)
    if (elevation > 90.0):
        elevation = (180.0 - elevation)
        direction = SunDirection.SETTING
    observer = Observer(self.latitude, self.longitude, 0.0)
    if local:
        return astral.sun.time_at_elevation(observer, elevation, date, direction, self.tzinfo)
    else:
        return astral.sun.time_at_elevation(observer, elevation, date, direction)
