import datetime
import logging
import feedparser
import voluptuous as vol
from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.const import ATTR_ATTRIBUTION, ATTR_LATITUDE, ATTR_LONGITUDE, CONF_ICON, CONF_LATITUDE, CONF_LONGITUDE, CONF_NAME, CONF_RADIUS, CONF_SCAN_INTERVAL
from homeassistant.core import callback
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.dispatcher import async_dispatcher_connect, dispatcher_send
from homeassistant.helpers.event import async_track_time_interval
from homeassistant.helpers.restore_state import RestoreEntity
import homeassistant.util as util
from homeassistant.util.location import distance


@staticmethod
def _convert_time(time):
    try:
        return datetime.datetime.strptime(time.split(',')[1][:(- 6)], ' %d %b %Y %H:%M:%S')
    except IndexError:
        return None
