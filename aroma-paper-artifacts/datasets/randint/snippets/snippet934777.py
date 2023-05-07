from __future__ import print_function
import scipy
import os
import random
import re
import sys
import weakref
import queue
from PIL import Image
from carla08.client import make_carla_client
from carla08.settings import CarlaSettings
from carla08.client import VehicleControl
from carla08 import sensor
import carla08 as carla
from coilutils import AttributeDict
import pygame
from pygame.locals import KMOD_CTRL
from pygame.locals import KMOD_SHIFT
from pygame.locals import K_0
from pygame.locals import K_9
from pygame.locals import K_BACKQUOTE
from pygame.locals import K_BACKSPACE
from pygame.locals import K_COMMA
from pygame.locals import K_DOWN
from pygame.locals import K_ESCAPE
from pygame.locals import K_F1
from pygame.locals import K_LEFT
from pygame.locals import K_PERIOD
from pygame.locals import K_RIGHT
from pygame.locals import K_SLASH
from pygame.locals import K_SPACE
from pygame.locals import K_TAB
from pygame.locals import K_UP
from pygame.locals import K_a
from pygame.locals import K_c
from pygame.locals import K_d
from pygame.locals import K_h
from pygame.locals import K_m
from pygame.locals import K_p
from pygame.locals import K_q
from pygame.locals import K_r
from pygame.locals import K_s
from pygame.locals import K_w
import numpy as np


def restart(self):
    cam_index = (self.camera_manager._index if (self.camera_manager is not None) else 0)
    cam_pos_index = (self.camera_manager._transform_index if (self.camera_manager is not None) else 0)
    number_of_vehicles = random.randint(NumberOfVehicles[0], NumberOfVehicles[1])
    number_of_pedestrians = random.randint(NumberOfPedestrians[0], NumberOfPedestrians[1])
    weather = random.choice(set_of_weathers)
    carla_settings = make_carla_settings()
    carla_settings.set(NumberOfVehicles=number_of_vehicles, NumberOfPedestrians=number_of_pedestrians, WeatherId=weather)
    self.scene = self.client.load_settings(carla_settings)
    if (self.scene.map_name == 'Town01'):
        POSITIONS = POSITIONS_TOWN01
    else:
        POSITIONS = POSITIONS_TOWN02
    print('Starting new episode...')
    self._random_pose = random.choice(POSITIONS)
    self.client.start_episode(self._random_pose[0])
    self.camera_manager = CameraManager(self.vehicle, self.hud)
    self.camera_manager._transform_index = cam_pos_index
