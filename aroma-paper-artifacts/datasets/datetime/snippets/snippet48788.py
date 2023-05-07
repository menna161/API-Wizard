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


def _setup_updates(self, cur_dttm: datetime, cur_elev: Num) -> None:
    'Set up updates for next portion of elevation curve.'
    assert self._cp
    if self._cp.rising:
        nadir_dttm = (self._cp.tR_dttm - HALF_DAY)
        if (cur_dttm < nadir_dttm):
            self._attr_native_value = self._d.falling_states[(- 1)][1]
            nadir_elev = cast(float, self._astral_event(nadir_dttm))
            self._setup_update_at_time(nadir_dttm, self._d.rising_states[0][1], self._attrs_at_elev(nadir_elev))
    else:
        nadir_dttm = (self._cp.nxt_noon - HALF_DAY)
        if (cur_dttm >= nadir_dttm):
            self._attr_native_value = self._d.rising_states[0][1]
    super()._setup_updates(cur_dttm, cur_elev)
