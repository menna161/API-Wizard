import dataclasses
import datetime
from typing import Any, Dict, Optional, Tuple, Union
import astral.moon
import astral.sun
from astral import Depression, Elevation, LocationInfo, Observer, SunDirection, dms_to_float, today
import zoneinfo
from backports import zoneinfo


def twilight(self, date: Optional[datetime.date]=None, direction: SunDirection=SunDirection.RISING, local: bool=True, observer_elevation: Elevation=0.0):
    "Returns the start and end times of Twilight in the UTC timezone when\n        the sun is traversing in the specified direction.\n\n        This method defines twilight as being between the time\n        when the sun is at -6 degrees and sunrise/sunset.\n\n        :param direction:  Determines whether the time is for the sun rising or setting.\n                           Use ``astral.SUN_RISING`` or ``astral.SunDirection.SETTING``.\n\n        :param date: The date for which to calculate the times.\n\n        :param local: True  = Time to be returned in location's time zone;\n                      False = Time to be returned in UTC.\n                      If not specified then the time will be returned in local time\n\n        :param observer_elevation: Elevation of the observer in metres above\n                                   the location.\n\n        :return: A tuple of the UTC date and time at which twilight starts and ends.\n        "
    if (local and (self.timezone is None)):
        raise ValueError('Local time requested but Location has no timezone set.')
    if (date is None):
        date = self.today(local)
    observer = Observer(self.latitude, self.longitude, observer_elevation)
    if local:
        return astral.sun.twilight(observer, date, direction, self.tzinfo)
    else:
        return astral.sun.twilight(observer, date, direction)
