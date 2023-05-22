import dataclasses
import datetime
from typing import Any, Dict, Optional, Tuple, Union
import astral.moon
import astral.sun
from astral import Depression, Elevation, LocationInfo, Observer, SunDirection, dms_to_float, today
import zoneinfo
from backports import zoneinfo


def dawn(self, date: Optional[datetime.date]=None, local: bool=True, observer_elevation: Elevation=0.0) -> datetime.datetime:
    "Calculates the time in the morning when the sun is a certain number\n        of degrees below the horizon. By default this is 6 degrees but can be\n        changed by setting the :attr:`Astral.solar_depression` property.\n\n        :param date: The date for which to calculate the dawn time.\n                     If no date is specified then the current date will be used.\n\n        :param local: True  = Time to be returned in location's time zone;\n                      False = Time to be returned in UTC.\n                      If not specified then the time will be returned in local time\n\n        :param observer_elevation: Elevation of the observer in metres above\n                                   the location.\n\n        :returns: The date and time at which dawn occurs.\n        "
    if (local and (self.timezone is None)):
        raise ValueError('Local time requested but Location has no timezone set.')
    if (date is None):
        date = self.today(local)
    observer = Observer(self.latitude, self.longitude, observer_elevation)
    if local:
        return astral.sun.dawn(observer, date, self.solar_depression, self.tzinfo)
    else:
        return astral.sun.dawn(observer, date, self.solar_depression)
