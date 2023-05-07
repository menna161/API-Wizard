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
    if self._updates:
        return
    start_update = dt_util.now()
    cur_dttm = nearest_second(cur_dttm)
    cur_elev = cast(float, self._astral_event(cur_dttm))
    self._cp = self._get_curve_params(cur_dttm, cur_elev)
    self._attr_native_value = None
    self._setup_updates(cur_dttm, cur_elev)
    self._setup_update_at_time(self._cp.tR_dttm)
    if (not self._attr_native_value):
        self._attr_native_value = self._state_at_elev(cur_elev)
    self._set_attrs(self._attrs_at_elev(cur_elev), self._updates[0].when)

    def cancel_updates() -> None:
        'Cancel pending updates.'
        for update in self._updates:
            update.remove()
        self._updates = []
    self._unsub_update = cancel_updates
    LOGGER.debug('%s: _update time: %s', self.name, (dt_util.now() - start_update))
