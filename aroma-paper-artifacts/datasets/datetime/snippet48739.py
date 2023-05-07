from __future__ import annotations
from datetime import datetime
from numbers import Real
from typing import Any, Mapping, cast
import voluptuous as vol
from homeassistant.components.binary_sensor import BinarySensorEntity, BinarySensorEntityDescription, DOMAIN as BINARY_SENSOR_DOMAIN, PLATFORM_SCHEMA
from homeassistant.const import CONF_ABOVE, CONF_ELEVATION, CONF_ENTITY_NAMESPACE, CONF_MONITORED_CONDITIONS, CONF_NAME
from homeassistant.core import CoreState, HomeAssistant, callback
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.event import async_track_point_in_utc_time
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType
from homeassistant.util import dt as dt_util
from .const import ATTR_NEXT_CHANGE, LOGGER, MAX_ERR_BIN, ONE_DAY, ONE_SEC, SUNSET_ELEV
from .helpers import LOC_PARAMS, LocParams, Num, Sun2Entity, get_loc_params, nearest_second


def _find_nxt_dttm(self, t0_dttm: datetime, t0_elev: Num, t1_dttm: datetime, t1_elev: Num) -> datetime:
    'Find time elevation crosses threshold between two points on elevation curve.'
    slope = (1 if (t1_elev > t0_elev) else (- 1))
    tn_dttm = nearest_second((t0_dttm + ((t1_dttm - t0_dttm) / 2)))
    tn_elev = cast(float, self._astral_event(tn_dttm))
    while (not (((self._attr_is_on and (tn_elev <= self._threshold)) or ((not self._attr_is_on) and (tn_elev > self._threshold))) and (abs((tn_elev - self._threshold)) <= MAX_ERR_BIN))):
        if (((tn_elev - self._threshold) * slope) > 0):
            if (t1_dttm == tn_dttm):
                break
            t1_dttm = tn_dttm
        else:
            if (t0_dttm == tn_dttm):
                break
            t0_dttm = tn_dttm
        tn_dttm = nearest_second((t0_dttm + ((t1_dttm - t0_dttm) / 2)))
        tn_elev = cast(float, self._astral_event(tn_dttm))
    if (self._attr_is_on and (tn_elev > self._threshold)):
        tn_dttm -= (slope * ONE_SEC)
        if (cast(float, self._astral_event(tn_dttm)) > self._threshold):
            raise RuntimeError("Couldn't find next update time")
    elif ((not self._attr_is_on) and (tn_elev <= self._threshold)):
        tn_dttm += (slope * ONE_SEC)
        if (cast(float, self._astral_event(tn_dttm)) <= self._threshold):
            raise RuntimeError("Couldn't find next update time")
    return tn_dttm
