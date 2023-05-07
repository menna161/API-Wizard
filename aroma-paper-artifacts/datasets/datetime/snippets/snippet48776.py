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


def _update(self, cur_dttm: datetime) -> None:
    'Update state.'
    cur_dttm = nearest_second(cur_dttm)
    cur_elev = cast(float, self._astral_event(cur_dttm))
    self._attr_native_value = rnd_elev = round(cur_elev, 1)
    LOGGER.debug('%s: Raw elevation = %f -> %s', self.name, cur_elev, self.native_value)
    if ((not self._cp) or (cur_dttm >= self._cp.tR_dttm)):
        self._prv_dttm = None
        self._cp = self._get_curve_params(cur_dttm, cur_elev)
    if self._prv_dttm:
        if self._cp.rising:
            elev = (floor(((rnd_elev + ELEV_STEP) / ELEV_STEP)) * ELEV_STEP)
            if ((rnd_elev < SUNSET_ELEV) and (elev > (SUNSET_ELEV + MAX_ERR_ELEV))):
                elev = (SUNSET_ELEV + MAX_ERR_ELEV)
        else:
            elev = (ceil(((rnd_elev - ELEV_STEP) / ELEV_STEP)) * ELEV_STEP)
            if ((rnd_elev > SUNSET_ELEV) and (elev < (SUNSET_ELEV - MAX_ERR_ELEV))):
                elev = (SUNSET_ELEV - MAX_ERR_ELEV)
        nxt_dttm = self._get_dttm_at_elev(self._prv_dttm, cur_dttm, elev, MAX_ERR_ELEV)
    else:
        nxt_dttm = None
    if (not nxt_dttm):
        if ((self._cp.tR_dttm - _DELTA) <= cur_dttm < self._cp.tR_dttm):
            nxt_dttm = self._cp.tR_dttm
        else:
            nxt_dttm = (cur_dttm + _DELTA)
    self._set_attrs(self._attrs_at_elev(cur_elev), nxt_dttm)
    self._prv_dttm = cur_dttm

    @callback
    def async_schedule_update(now: datetime) -> None:
        'Schedule entity update.'
        self._unsub_update = None
        self.async_schedule_update_ha_state(True)
    self._unsub_update = async_track_point_in_utc_time(self.hass, async_schedule_update, nxt_dttm)
