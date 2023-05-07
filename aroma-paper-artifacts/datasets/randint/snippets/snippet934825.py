from __future__ import print_function
import argparse
import collections
import datetime
import glob
import time
import copy
from collections import deque
import logging
import math
import os
import random
import re
import sys
import weakref
import matplotlib.pyplot as plt
import scipy
import carla
from carla import ColorConverter as cc
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
    blueprint = self.world.get_blueprint_library().find('vehicle.ford.mustang')
    blueprint.set_attribute('role_name', 'hero')
    if blueprint.has_attribute('color'):
        color = random.choice(blueprint.get_attribute('color').recommended_values)
        blueprint.set_attribute('color', color)
    if (self.vehicle is not None):
        spawn_point = self.vehicle.get_transform()
        spawn_point.location.z += 2.0
        spawn_point.rotation.roll = 0.0
        spawn_point.rotation.pitch = 0.0
        self.destroy()
        spawn_points = self.world.get_map().get_spawn_points()
        spawn_point = spawn_points[random.randint(0, 40)]
        self.vehicle = self.world.spawn_actor(blueprint, spawn_point)
    while (self.vehicle is None):
        spawn_points = self.world.get_map().get_spawn_points()
        spawn_point = spawn_points[random.randint(0, 40)]
        self.vehicle = self.world.spawn_actor(blueprint, spawn_point)
    camera = {'id': 'rgb', 'type': 'sensor.camera.rgb', 'image_size_x': 800, 'image_size_y': 600, 'fov': 100, 'position_x': 2.0, 'position_y': 0.0, 'position_z': 1.4, 'rotation_pitch': 0.0}
    self.cam = Camera(self.world, camera, self.vehicle)
    weak_self = weakref.ref(self)
    self.cam.actor.listen((lambda image: World._parse_camera(weak_self, image)))
    self.collision_sensor = CollisionSensor(self.vehicle, self.hud)
    self.lane_invasion_sensor = LaneInvasionSensor(self.vehicle, self.hud)
    self.camera_manager = CameraManager(self.vehicle, self.hud)
    self.camera_manager._transform_index = cam_pos_index
    self.camera_manager.set_sensor(cam_index, notify=False)
    actor_type = get_actor_display_name(self.vehicle)
    self.hud.notification(actor_type)
