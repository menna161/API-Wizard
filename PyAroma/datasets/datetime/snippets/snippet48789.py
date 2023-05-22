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


@callback
def async_schedule_update_at_midnight(now: datetime) -> None:
    'Schedule an update at midnight.'
    next_midn = next_midnight(now.astimezone(self._loc_data.tzi))
    self._unsub_update = async_track_point_in_utc_time(self.hass, async_schedule_update_at_midnight, next_midn)
    self.async_schedule_update_ha_state(True)
