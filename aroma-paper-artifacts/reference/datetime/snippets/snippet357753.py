import dataclasses
import datetime
from typing import Any, Dict, Optional, Tuple, Union
import astral.moon
import astral.sun
from astral import Depression, Elevation, LocationInfo, Observer, SunDirection, dms_to_float, today
import zoneinfo
from backports import zoneinfo


def blue_hour(self, direction: SunDirection=SunDirection.RISING, date: Optional[datetime.date]=None, local: bool=True, observer_elevation: Elevation=0.0) -> Tuple[(datetime.datetime, datetime.datetime)]:
    "Returns the start and end times of the Blue Hour when the sun is traversing\n        in the specified direction.\n\n        This method uses the definition from PhotoPills i.e. the\n        blue hour is when the sun is between 6 and 4 degrees below the horizon.\n\n        :param direction:  Determines whether the time is for the sun rising or setting.\n                           Use ``SunDirection.RISING`` or ``SunDirection.SETTING``.\n                           Default is rising.\n\n        :param date: The date for which to calculate the times.\n                     If no date is specified then the current date will be used.\n\n        :param local: True  = Times to be returned in location's time zone;\n                      False = Times to be returned in UTC.\n                      If not specified then the time will be returned in local time\n\n        :param observer_elevation: Elevation of the observer in metres above\n                                   the location.\n\n        :return: A tuple of the date and time at which the Blue Hour starts and ends.\n        "
    if (local and (self.timezone is None)):
        raise ValueError('Local time requested but Location has no timezone set.')
    if (date is None):
        date = self.today(local)
    observer = Observer(self.latitude, self.longitude, observer_elevation)
    if local:
        return astral.sun.blue_hour(observer, date, direction, self.tzinfo)
    else:
        return astral.sun.blue_hour(observer, date, direction)
