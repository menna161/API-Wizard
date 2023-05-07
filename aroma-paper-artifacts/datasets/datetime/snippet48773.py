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


def _get_dttm_at_elev(self, t0_dttm: datetime, t1_dttm: datetime, elev: Num, max_err: Num) -> (datetime | None):
    'Get datetime at elevation.'
    assert self._cp
    msg_base = f'{self.name}: trg = {elev:+7.3f}: '
    t0_elev = cast(float, self._astral_event(t0_dttm))
    t1_elev = cast(float, self._astral_event(t1_dttm))
    est_elev = (elev + (1.5 * max_err))
    est = 0
    while (abs((est_elev - elev)) >= max_err):
        est += 1
        msg = (msg_base + f't0 = {t0_dttm}/{t0_elev:+7.3f}, t1 = {t1_dttm}/{t1_elev:+7.3f} ->')
        try:
            est_dttm = nearest_second((t0_dttm + ((t1_dttm - t0_dttm) * ((elev - t0_elev) / (t1_elev - t0_elev)))))
        except ZeroDivisionError:
            LOGGER.debug('%s ZeroDivisionError', msg)
            return None
        if ((est_dttm < self._cp.tL_dttm) or (est_dttm > self._cp.tR_dttm)):
            LOGGER.debug('%s outside range', msg)
            return None
        est_elev = cast(float, self._astral_event(est_dttm))
        LOGGER.debug('%s est = %s/%+7.3f[%+7.3f/%2i]', msg, est_dttm, est_elev, (est_elev - elev), est)
        if (est_dttm in (t0_dttm, t1_dttm)):
            break
        if (est_dttm > t1_dttm):
            t0_dttm = t1_dttm
            t0_elev = t1_elev
            t1_dttm = est_dttm
            t1_elev = est_elev
        elif ((t0_elev < elev < est_elev) or (t0_elev > elev > est_elev)):
            t1_dttm = est_dttm
            t1_elev = est_elev
        else:
            t0_dttm = est_dttm
            t0_elev = est_elev
    return est_dttm
