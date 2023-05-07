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


def _update(self, cur_dttm: datetime) -> None:
    'Update state.'
    cur_elev = cast(float, self._astral_event(cur_dttm))
    self._attr_is_on = (cur_elev > self._threshold)
    self._attr_icon = (ABOVE_ICON if self._attr_is_on else BELOW_ICON)
    LOGGER.debug('%s: above = %f, elevation = %f', self.name, self._threshold, cur_elev)
    nxt_dttm = self._get_nxt_dttm(cur_dttm)

    @callback
    def schedule_update(now: datetime) -> None:
        'Schedule state update.'
        self._unsub_update = None
        self.async_schedule_update_ha_state(True)
    if nxt_dttm:
        self._unsub_update = async_track_point_in_utc_time(self.hass, schedule_update, nxt_dttm)
        nxt_dttm = dt_util.as_local(nxt_dttm)
    elif (self.hass.state == CoreState.running):
        LOGGER.error('%s: Sun elevation never reaches %f at this location', self.name, self._threshold)
    self._attr_extra_state_attributes = {ATTR_NEXT_CHANGE: nxt_dttm}
