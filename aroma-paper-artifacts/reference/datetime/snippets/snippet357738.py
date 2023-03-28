import dataclasses
import datetime
from typing import Any, Dict, Optional, Tuple, Union
import astral.moon
import astral.sun
from astral import Depression, Elevation, LocationInfo, Observer, SunDirection, dms_to_float, today
import zoneinfo
from backports import zoneinfo


def sun(self, date: Optional[datetime.date]=None, local: bool=True, observer_elevation: Elevation=0.0) -> Dict[(str, Any)]:
    "Returns dawn, sunrise, noon, sunset and dusk as a dictionary.\n\n        :param date: The date for which to calculate the times.\n                     If no date is specified then the current date will be used.\n\n        :param local: True  = Time to be returned in location's time zone;\n                      False = Time to be returned in UTC.\n                      If not specified then the time will be returned in local time\n\n        :param observer_elevation: Elevation of the observer in metres above\n                                   the location.\n\n        :returns: Dictionary with keys ``dawn``, ``sunrise``, ``noon``,\n            ``sunset`` and ``dusk`` whose values are the results of the\n            corresponding methods.\n        "
    if (local and (self.timezone is None)):
        raise ValueError('Local time requested but Location has no timezone set.')
    if (date is None):
        date = self.today(local)
    observer = Observer(self.latitude, self.longitude, observer_elevation)
    if local:
        return astral.sun.sun(observer, date, self.solar_depression, self.tzinfo)
    else:
        return astral.sun.sun(observer, date, self.solar_depression)
