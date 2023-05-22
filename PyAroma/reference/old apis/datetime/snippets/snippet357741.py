import dataclasses
import datetime
from typing import Any, Dict, Optional, Tuple, Union
import astral.moon
import astral.sun
from astral import Depression, Elevation, LocationInfo, Observer, SunDirection, dms_to_float, today
import zoneinfo
from backports import zoneinfo


def noon(self, date: Optional[datetime.date]=None, local: bool=True) -> datetime.datetime:
    "Calculates the solar noon (the time when the sun is at its highest\n        point.)\n\n        :param date: The date for which to calculate the noon time.\n                     If no date is specified then the current date will be used.\n\n        :param local: True  = Time to be returned in location's time zone;\n                      False = Time to be returned in UTC.\n                      If not specified then the time will be returned in local time\n\n        :returns: The date and time at which the solar noon occurs.\n        "
    if (local and (self.timezone is None)):
        raise ValueError('Local time requested but Location has no timezone set.')
    if (date is None):
        date = self.today(local)
    observer = Observer(self.latitude, self.longitude)
    if local:
        return astral.sun.noon(observer, date, self.tzinfo)
    else:
        return astral.sun.noon(observer, date)
