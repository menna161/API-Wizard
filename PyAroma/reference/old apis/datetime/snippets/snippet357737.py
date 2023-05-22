import dataclasses
import datetime
from typing import Any, Dict, Optional, Tuple, Union
import astral.moon
import astral.sun
from astral import Depression, Elevation, LocationInfo, Observer, SunDirection, dms_to_float, today
import zoneinfo
from backports import zoneinfo


def today(self, local: bool=True) -> datetime.date:
    if local:
        return today(self.tzinfo)
    else:
        return today()
