from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import logging
from typing import Any
from pyweatherflowudp.calc import Quantity
from pyweatherflowudp.const import EVENT_RAPID_WIND
from pyweatherflowudp.device import EVENT_OBSERVATION, EVENT_STATUS_UPDATE, WeatherFlowDevice, WeatherFlowSensorDevice
import voluptuous as vol
from homeassistant.components.sensor import DOMAIN as SENSOR_DOMAIN, PLATFORM_SCHEMA, SensorDeviceClass, SensorEntity, SensorEntityDescription, SensorStateClass
from homeassistant.config_entries import SOURCE_IMPORT, ConfigEntry
from homeassistant.const import CONF_HOST, CONF_MONITORED_CONDITIONS, CONF_NAME, DEGREE, LIGHT_LUX, PERCENTAGE, SIGNAL_STRENGTH_DECIBELS_MILLIWATT, UV_INDEX, UnitOfElectricPotential, UnitOfIrradiance, UnitOfLength, UnitOfPrecipitationDepth, UnitOfPressure, UnitOfSpeed, UnitOfTemperature, UnitOfVolumetricFlux
from homeassistant.core import Callable, HomeAssistant, callback
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.dispatcher import async_dispatcher_connect
from homeassistant.helpers.entity import DeviceInfo, EntityCategory
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, StateType
from homeassistant.util.unit_system import METRIC_SYSTEM
from .const import DOMAIN


@property
def last_reset(self) -> (datetime | None):
    'Return the time when the sensor was last reset, if any.'
    if (self.entity_description.state_class == SensorStateClass.TOTAL):
        return self.device.last_report
    return None
