import dataclasses
import datetime
from typing import Any, Dict, Optional, Tuple, Union
import astral.moon
import astral.sun
from astral import Depression, Elevation, LocationInfo, Observer, SunDirection, dms_to_float, today
import zoneinfo
from backports import zoneinfo


def rahukaalam(self, date: Optional[datetime.date]=None, local: bool=True, observer_elevation: Elevation=0.0) -> Tuple[(datetime.datetime, datetime.datetime)]:
    "Calculates the period of rahukaalam.\n\n        :param date: The date for which to calculate the rahukaalam period.\n                     A value of ``None`` uses the current date.\n\n        :param local: True  = Time to be returned in location's time zone;\n                      False = Time to be returned in UTC.\n\n        :param observer_elevation: Elevation of the observer in metres above\n                                   the location.\n\n        :return: Tuple containing the start and end times for Rahukaalam.\n        "
    if (local and (self.timezone is None)):
        raise ValueError('Local time requested but Location has no timezone set.')
    if (date is None):
        date = self.today(local)
    observer = Observer(self.latitude, self.longitude, observer_elevation)
    if local:
        return astral.sun.rahukaalam(observer, date, tzinfo=self.tzinfo)
    else:
        return astral.sun.rahukaalam(observer, date)
