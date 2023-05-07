from __future__ import annotations
from abc import abstractmethod
from collections.abc import Mapping
from dataclasses import dataclass
from datetime import date, datetime, time, timedelta, tzinfo
from typing import Any, TypeVar, Union, cast
from astral import LocationInfo
from astral.location import Location
import voluptuous as vol
from homeassistant.const import CONF_ELEVATION, CONF_LATITUDE, CONF_LONGITUDE, CONF_TIME_ZONE, EVENT_CORE_CONFIG_UPDATE
from homeassistant.core import CALLBACK_TYPE, Event
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.dispatcher import async_dispatcher_connect, dispatcher_send
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.typing import ConfigType
from homeassistant.util import dt as dt_util, slugify
from .const import DOMAIN, LOGGER, ONE_DAY, SIG_HA_LOC_UPDATED


def _astral_event(self, date_or_dttm: (date | datetime), event: (str | None)=None, /, **kwargs: Mapping[(str, Any)]) -> Any:
    'Return astral event result.'
    if (not event):
        event = self._event
    loc = self._loc_data.loc
    if hasattr(self, '_solar_depression'):
        loc.solar_depression = self._solar_depression
    try:
        if (event in ('solar_midnight', 'solar_noon')):
            return getattr(loc, event.split('_')[1])(date_or_dttm)
        elif (event == 'time_at_elevation'):
            return loc.time_at_elevation(kwargs['elevation'], date_or_dttm, kwargs['direction'])
        else:
            return getattr(loc, event)(date_or_dttm, observer_elevation=self._loc_data.elv)
    except (TypeError, ValueError):
        return None
