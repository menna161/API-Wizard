import copy
import json
import logging
import threading
import time
from datetime import timedelta
import homeassistant.helpers.config_validation as cv
import requests
import voluptuous as vol
from homeassistant.components.binary_sensor import DOMAIN as BINARY_SENSOR
from homeassistant.components.climate import DOMAIN as CLIMATE
from homeassistant.components.sensor import DOMAIN as SENSOR
from homeassistant.components.switch import DOMAIN as SWITCH
from homeassistant.components.water_heater import DOMAIN as WATER_HEATER
from homeassistant.const import ATTR_ENTITY_ID, CONF_BINARY_SENSORS, CONF_NAME, CONF_PASSWORD, CONF_SENSORS, CONF_SWITCHES, CONF_USERNAME
from homeassistant.helpers import discovery
from homeassistant.helpers.dispatcher import dispatcher_send
from homeassistant.helpers.event import track_point_in_time
from homeassistant.util import dt as dt_util
from .binary_sensor import BINARY_SENSORS
from .const import ARISTON_PARAM_LIST, ARISTON_DHW_TIME_PROG_COMFORT, ARISTON_DHW_TIME_PROG_ECONOMY, ARISTON_DHW_COMFORT_FUNCTION, ARISTON_INTERNET_TIME, ARISTON_INTERNET_WEATHER, ARISTON_CH_AUTO_FUNCTION, ARISTON_CH_COMFORT_TEMP, ARISTON_CH_ECONOMY_TEMP, ARISTON_THERMAL_CLEANSE_FUNCTION, ARISTON_THERMAL_CLEANSE_CYCLE, CH_MODE_TO_VALUE, CLIMATES, CONF_HVAC_OFF, CONF_HVAC_OFF_PRESENT, CONF_POWER_ON, CONF_MAX_RETRIES, CONF_STORE_CONFIG_FILES, CONF_CONTROL_FROM_WATER_HEATER, CONF_LOCALIZATION, CONF_UNITS, CONF_POLLING_RATE, CONF_INIT_AT_START, CONF_DHW_FLAME_UNKNOWN_ON, CONF_DHW_AND_CH, DATA_ARISTON, DAYS_OF_WEEK, DEVICES, DHW_MODE_TO_VALUE, DOMAIN, MODE_TO_VALUE, DHW_COMFORT_FUNCT_TO_VALUE, UNIT_TO_VALUE, SERVICE_SET_DATA, SERVICE_UPDATE, PARAM_MODE, PARAM_CH_AUTO_FUNCTION, PARAM_CH_MODE, PARAM_CH_SET_TEMPERATURE, PARAM_CH_COMFORT_TEMPERATURE, PARAM_CH_ECONOMY_TEMPERATURE, PARAM_CH_DETECTED_TEMPERATURE, PARAM_DHW_COMFORT_FUNCTION, PARAM_DHW_MODE, PARAM_DHW_SET_TEMPERATURE, PARAM_DHW_COMFORT_TEMPERATURE, PARAM_DHW_ECONOMY_TEMPERATURE, PARAM_DHW_STORAGE_TEMPERATURE, PARAM_INTERNET_TIME, PARAM_INTERNET_WEATHER, PARAM_STRING_TO_VALUE, PARAM_UNITS, PARAM_THERMAL_CLEANSE_CYCLE, PARAM_THERMAL_CLEANSE_FUNCTION, VAL_WINTER, VAL_SUMMER, VAL_HEATING_ONLY, VAL_OFF, VAL_MANUAL, VAL_PROGRAM, VAL_UNSUPPORTED, VAL_METRIC, VAL_IMPERIAL, VAL_AUTO, VAL_NORMAL, VAL_LONG, VALUE_TO_DHW_MODE, WATER_HEATERS, LANG_EN, LANG_LIST, GET_REQUEST_CH_PROGRAM, GET_REQUEST_CURRENCY, GET_REQUEST_DHW_PROGRAM, GET_REQUEST_ERRORS, GET_REQUEST_GAS, GET_REQUEST_MAIN, GET_REQUEST_PARAM, GET_REQUEST_UNITS, GET_REQUEST_VERSION, SET_REQUEST_MAIN, SET_REQUEST_PARAM, SET_REQUEST_UNITS
from .exceptions import CommError, LoginError, AristonError
from .helpers import service_signal
from .sensor import SENSORS
from .switch import SWITCHES


def __init__(self, hass, device, name, username, password, retries, store_file, units, polling, sensors, binary_sensors, switches):
    'Initialize.'
    self._ariston_data = {}
    self._ariston_gas_data = {}
    self._ariston_error_data = {}
    self._ariston_ch_data = {}
    self._ariston_dhw_data = {}
    self._ariston_currency = {}
    self._ariston_other_data = {}
    self._ariston_units = {}
    self._ariston_data_actual = {}
    self._ariston_gas_data_actual = {}
    self._ariston_error_data_actual = {}
    self._ariston_ch_data_actual = {}
    self._ariston_dhw_data_actual = {}
    self._ariston_currency_actual = {}
    self._ariston_other_data_actual = {}
    self._ariston_units_actual = {}
    self._data_lock = threading.Lock()
    self._device = device
    self._dhw_history = [UNKNOWN_TEMP, UNKNOWN_TEMP, UNKNOWN_TEMP, UNKNOWN_TEMP]
    self._dhw_trend_up = False
    self._errors = 0
    self._get_request_number_low_prio = 0
    self._get_request_number_high_prio = 0
    self._get_time_start = {REQUEST_GET_MAIN: 0, REQUEST_GET_CH: 0, REQUEST_GET_DHW: 0, REQUEST_GET_ERROR: 0, REQUEST_GET_GAS: 0, REQUEST_GET_OTHER: 0, REQUEST_GET_UNITS: 0, REQUEST_GET_CURRENCY: 0, REQUEST_GET_VERSION: 0}
    self._get_time_end = {REQUEST_GET_MAIN: 0, REQUEST_GET_CH: 0, REQUEST_GET_DHW: 0, REQUEST_GET_ERROR: 0, REQUEST_GET_GAS: 0, REQUEST_GET_OTHER: 0, REQUEST_GET_UNITS: 0, REQUEST_GET_CURRENCY: 0, REQUEST_GET_VERSION: 0}
    self._get_zero_temperature = {PARAM_CH_SET_TEMPERATURE: UNKNOWN_TEMP, PARAM_CH_COMFORT_TEMPERATURE: UNKNOWN_TEMP, PARAM_CH_ECONOMY_TEMPERATURE: UNKNOWN_TEMP, PARAM_CH_DETECTED_TEMPERATURE: UNKNOWN_TEMP, PARAM_DHW_SET_TEMPERATURE: UNKNOWN_TEMP, PARAM_DHW_COMFORT_TEMPERATURE: UNKNOWN_TEMP, PARAM_DHW_ECONOMY_TEMPERATURE: UNKNOWN_TEMP, PARAM_DHW_STORAGE_TEMPERATURE: UNKNOWN_TEMP}
    self._hass = hass
    self._lock = threading.Lock()
    self._login = False
    self._name = name
    self._password = password
    self._plant_id = ''
    self._plant_id_lock = threading.Lock()
    self._session = requests.Session()
    self._set_param = {}
    self._set_param_group = {REQUEST_GET_MAIN: False, REQUEST_GET_OTHER: False, REQUEST_GET_UNITS: False}
    self._set_retry = {REQUEST_SET_MAIN: 0, REQUEST_SET_OTHER: 0, REQUEST_SET_UNITS: 0}
    self._set_max_retries = retries
    self._set_new_data_pending = False
    self._set_scheduled = False
    self._set_time_start = {REQUEST_SET_MAIN: 0, REQUEST_SET_OTHER: 0, REQUEST_SET_UNITS: 0}
    self._set_time_end = {REQUEST_SET_MAIN: 0, REQUEST_SET_OTHER: 0, REQUEST_SET_UNITS: 0}
    self._store_file = store_file
    self._token_lock = threading.Lock()
    self._token = None
    self._units = units
    self._url = ARISTON_URL
    self._user = username
    self._verify = True
    self._version = ''
    self._valid_requests = {REQUEST_GET_MAIN: True, REQUEST_GET_CH: False, REQUEST_GET_DHW: False, REQUEST_GET_ERROR: False, REQUEST_GET_GAS: False, REQUEST_GET_OTHER: True, REQUEST_GET_UNITS: False, REQUEST_GET_CURRENCY: False, REQUEST_GET_VERSION: False}
    if ((binary_sensors != []) and (binary_sensors != None)):
        for item in binary_sensors:
            self._valid_requests[_get_request_for_parameter(item)] = True
    if ((sensors != []) and (sensors != None)):
        for item in sensors:
            self._valid_requests[_get_request_for_parameter(item)] = True
    if ((switches != []) and (switches != None)):
        for item in switches:
            self._valid_requests[_get_request_for_parameter(item)] = True
    if (self._units == VAL_AUTO):
        self._valid_requests[REQUEST_GET_UNITS] = True
    self._request_list_high_prio = []
    if self._valid_requests[REQUEST_GET_MAIN]:
        self._request_list_high_prio.append(self._get_main_data)
    if self._valid_requests[REQUEST_GET_OTHER]:
        self._request_list_high_prio.append(self._get_other_data)
    if self._valid_requests[REQUEST_GET_ERROR]:
        self._request_list_high_prio.append(self._get_error_data)
    self._request_list_low_prio = []
    if self._valid_requests[REQUEST_GET_UNITS]:
        self._request_list_low_prio.append(self._get_unit_data)
    if self._valid_requests[REQUEST_GET_CH]:
        self._request_list_low_prio.append(self._get_ch_data)
    if self._valid_requests[REQUEST_GET_DHW]:
        self._request_list_low_prio.append(self._get_dhw_data)
    if self._valid_requests[REQUEST_GET_GAS]:
        self._request_list_low_prio.append(self._get_gas_water_data)
    if self._valid_requests[REQUEST_GET_CURRENCY]:
        self._request_list_low_prio.append(self._get_currency_data)
    if self._valid_requests[REQUEST_GET_VERSION]:
        self._request_list_low_prio.append(self._get_version_data)
    self._timer_between_param_delay = (HTTP_PARAM_DELAY * POLLING_RATE_TO_VALUE[polling])
    self._timeout_long = (HTTP_TIMEOUT_GET_LONG * POLLING_RATE_TO_VALUE[polling])
    self._timeout_medium = (HTTP_TIMEOUT_GET_MEDIUM * POLLING_RATE_TO_VALUE[polling])
    self._timeout_short = (HTTP_TIMEOUT_GET_SHORT * POLLING_RATE_TO_VALUE[polling])
    self._timer_between_set = VAL_NORMAL
    if self._store_file:
        with open((('/config/data_' + self._name) + '_valid_requests.json'), 'w') as ariston_fetched:
            json.dump(self._valid_requests, ariston_fetched)
