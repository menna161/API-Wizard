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


def next_midnight(dttm: datetime) -> datetime:
    'Return next midnight in same time zone.'
    return datetime.combine((dttm.date() + ONE_DAY), time(), dttm.tzinfo)
