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
def native_value(self) -> (datetime | StateType):
    'Return the state of the sensor.'
    attr = getattr(self.device, (self.entity_description.key if (self.entity_description.attr is None) else self.entity_description.attr))
    if (attr is None):
        return attr
    if (((not (self.hass.config.units is METRIC_SYSTEM)) and ((fn := self.entity_description.conversion_fn) is not None)) or ((fn := self.entity_description.value_fn) is not None)):
        attr = fn(attr)
    if isinstance(attr, Quantity):
        attr = attr.m
    elif isinstance(attr, Enum):
        attr = attr.name
    if ((decimals := self.entity_description.decimals) is not None):
        attr = round(attr, decimals)
    return attr
