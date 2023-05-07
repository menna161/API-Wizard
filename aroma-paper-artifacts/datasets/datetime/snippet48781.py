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


def _setup_update_at_elev(self, elev: Num) -> None:
    'Set up update when sun reaches given elevation.'
    assert self._cp
    try:

        def get_est_dttm(offset: (timedelta | None)=None) -> datetime:
            "Get estimated time when sun gets to given elevation.\n\n                Note that astral's time_at_elevation method is not very accurate\n                and can sometimes return None, especially near solar noon or solar\n                midnight.\n                "
            assert self._cp
            return nearest_second(cast(datetime, self._astral_event(((self._cp.mid_date + offset) if offset else self._cp.mid_date), 'time_at_elevation', elevation=elev, direction=(SunDirection.RISING if self._cp.rising else SunDirection.SETTING))))
        est_dttm = get_est_dttm()
        if (not (self._cp.tL_dttm <= est_dttm < self._cp.tR_dttm)):
            est_dttm = get_est_dttm((ONE_DAY if (est_dttm < self._cp.tL_dttm) else (- ONE_DAY)))
            if (not (self._cp.tL_dttm <= est_dttm < self._cp.tR_dttm)):
                raise ValueError
    except (TypeError, ValueError) as exc:
        if isinstance(exc, TypeError):
            LOGGER.debug('%s: time_at_elevation(%0.3f) returned None', self.name, elev)
        else:
            LOGGER.debug('%s: time_at_elevation(%0.3f) outside [tL, tR): %s', self.name, elev, est_dttm)
        t0_dttm = self._cp.tL_dttm
        t1_dttm = self._cp.tR_dttm
    else:
        t0_dttm = max((est_dttm - _DELTA), self._cp.tL_dttm)
        t1_dttm = min((est_dttm + _DELTA), self._cp.tR_dttm)
    update_dttm = self._get_dttm_at_elev(t0_dttm, t1_dttm, elev, MAX_ERR_PHASE)
    if update_dttm:
        self._setup_update_at_time(update_dttm, self._state_at_elev(elev), self._attrs_at_elev(elev))
    elif (self.hass.state == CoreState.running):
        LOGGER.error('%s: Failed to find the time at elev: %0.3f', self.name, elev)
