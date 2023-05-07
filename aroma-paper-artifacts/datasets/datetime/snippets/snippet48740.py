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


def _get_nxt_dttm(self, cur_dttm: datetime) -> (datetime | None):
    'Get next time sensor should change state.'
    date = cur_dttm.date()
    evt_dttm1 = cast(datetime, self._astral_event(date, 'solar_midnight'))
    evt_dttm2 = cast(datetime, self._astral_event(date, 'solar_noon'))
    evt_dttm3 = cast(datetime, self._astral_event((date + ONE_DAY), 'solar_midnight'))
    evt_dttm4 = cast(datetime, self._astral_event((date + ONE_DAY), 'solar_noon'))
    evt_dttm5 = cast(datetime, self._astral_event((date + (2 * ONE_DAY)), 'solar_midnight'))
    end_date = (date + (366 * ONE_DAY))
    while (date < end_date):
        if (cur_dttm < evt_dttm1):
            if self._attr_is_on:
                t0_dttm = cur_dttm
                t1_dttm = evt_dttm1
            else:
                t0_dttm = evt_dttm1
                t1_dttm = evt_dttm2
        elif (cur_dttm < evt_dttm2):
            if (not self._attr_is_on):
                t0_dttm = cur_dttm
                t1_dttm = evt_dttm2
            else:
                t0_dttm = evt_dttm2
                t1_dttm = evt_dttm3
        elif (cur_dttm < evt_dttm3):
            if self._attr_is_on:
                t0_dttm = cur_dttm
                t1_dttm = evt_dttm3
            else:
                t0_dttm = evt_dttm3
                t1_dttm = evt_dttm4
        elif (not self._attr_is_on):
            t0_dttm = cur_dttm
            t1_dttm = evt_dttm4
        else:
            t0_dttm = evt_dttm4
            t1_dttm = evt_dttm5
        t0_elev = cast(float, self._astral_event(t0_dttm))
        t1_elev = cast(float, self._astral_event(t1_dttm))
        if ((t0_elev <= self._threshold < t1_elev) or (t1_elev <= self._threshold <= t0_elev)):
            nxt_dttm = self._find_nxt_dttm(t0_dttm, t0_elev, t1_dttm, t1_elev)
            if ((nxt_dttm - cur_dttm) > ONE_DAY):
                if (self.hass.state == CoreState.running):
                    LOGGER.warning('%s: Sun elevation will not reach %f again until %s', self.name, self._threshold, nxt_dttm.date())
            return nxt_dttm
        date += ONE_DAY
        evt_dttm1 = evt_dttm3
        evt_dttm2 = evt_dttm4
        evt_dttm3 = evt_dttm5
        evt_dttm4 = cast(datetime, self._astral_event((date + ONE_DAY), 'solar_noon'))
        evt_dttm5 = cast(datetime, self._astral_event((date + (2 * ONE_DAY)), 'solar_midnight'))
    return None
