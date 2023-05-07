from __future__ import annotations
from abc import abstractmethod
from collections.abc import Mapping, MutableMapping, Sequence
from contextlib import suppress
from dataclasses import dataclass
from datetime import date, datetime, timedelta
from math import ceil, floor
from typing import Any, Generic, Optional, TypeVar, Union, cast
from astral import SunDirection
import voluptuous as vol
from homeassistant.components.sensor import DOMAIN as SENSOR_DOMAIN, PLATFORM_SCHEMA, SensorDeviceClass, SensorEntity, SensorEntityDescription, SensorStateClass
from homeassistant.const import ATTR_ICON, CONF_ENTITY_NAMESPACE, CONF_MONITORED_CONDITIONS, DEGREE
from homeassistant.core import CALLBACK_TYPE, CoreState, HomeAssistant, callback
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.event import async_track_point_in_utc_time
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType
from homeassistant.util import dt as dt_util
from .const import ATTR_BLUE_HOUR, ATTR_DAYLIGHT, ATTR_GOLDEN_HOUR, ATTR_NEXT_CHANGE, ATTR_RISING, ATTR_TODAY, ATTR_TODAY_HMS, ATTR_TOMORROW, ATTR_TOMORROW_HMS, ATTR_YESTERDAY, ATTR_YESTERDAY_HMS, HALF_DAY, MAX_ERR_ELEV, ELEV_STEP, LOGGER, MAX_ERR_PHASE, ONE_DAY, SUNSET_ELEV
from .helpers import LOC_PARAMS, LocData, LocParams, Num, Sun2Entity, get_loc_params, hours_to_hms, nearest_second, next_midnight
from homeassistant.const import UnitOfTime
from homeassistant.const import TIME_HOURS


def _get_curve_params(self, cur_dttm: datetime, cur_elev: Num) -> CurveParameters:
    'Calculate elevation curve parameters.'
    cur_date = cur_dttm.date()
    hi_dttm = cast(datetime, self._astral_event(cur_date, 'solar_noon'))
    lo_dttm = cast(datetime, self._astral_event(cur_date, 'solar_midnight'))
    nxt_noon = cast(datetime, self._astral_event((cur_date + ONE_DAY), 'solar_noon'))
    if (cur_dttm < lo_dttm):
        tL_dttm = cast(datetime, self._astral_event((cur_date - ONE_DAY), 'solar_noon'))
        tR_dttm = lo_dttm
    elif (cur_dttm < hi_dttm):
        tL_dttm = lo_dttm
        tR_dttm = hi_dttm
    else:
        lo_dttm = cast(datetime, self._astral_event((cur_date + ONE_DAY), 'solar_midnight'))
        if (cur_dttm < lo_dttm):
            tL_dttm = hi_dttm
            tR_dttm = lo_dttm
        else:
            tL_dttm = lo_dttm
            tR_dttm = nxt_noon
    tL_elev = cast(float, self._astral_event(tL_dttm))
    tR_elev = cast(float, self._astral_event(tR_dttm))
    rising = (tR_elev > tL_elev)
    LOGGER.debug('%s: tL = %s/%0.3f, cur = %s/%0.3f, tR = %s/%0.3f, rising = %s', self.name, tL_dttm, tL_elev, cur_dttm, cur_elev, tR_dttm, tR_elev, rising)
    mid_date = (tL_dttm + ((tR_dttm - tL_dttm) / 2)).date()
    return CurveParameters(tL_dttm, tL_elev, tR_dttm, tR_elev, mid_date, nxt_noon, rising)
