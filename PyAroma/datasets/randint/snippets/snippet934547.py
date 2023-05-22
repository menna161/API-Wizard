import io
import random
import sys
from . import sensor as carla_sensor
from configparser import ConfigParser
from ConfigParser import RawConfigParser as ConfigParser


def randomize_weather(self):
    'Randomized the WeatherId.'
    self.WeatherId = random.randint(0, MAX_NUMBER_OF_WEATHER_IDS)
