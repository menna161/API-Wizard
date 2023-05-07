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


def tick(self, world, clock):
    if (not self._show_info):
        return
    self.command_status = world._command_cache
    t = world.vehicle.get_transform()
    v = world.vehicle.get_velocity()
    c = world.vehicle.get_control()
    heading = ('N' if (abs(t.rotation.yaw) < 89.5) else '')
    heading += ('S' if (abs(t.rotation.yaw) > 90.5) else '')
    heading += ('E' if (179.5 > t.rotation.yaw > 0.5) else '')
    heading += ('W' if ((- 0.5) > t.rotation.yaw > (- 179.5)) else '')
    colhist = world.collision_sensor.get_collision_history()
    collision = [colhist[((x + self.frame_number) - 200)] for x in range(0, 200)]
    max_col = max(1.0, max(collision))
    collision = [(x / max_col) for x in collision]
    vehicles = world.world.get_actors().filter('vehicle.*')
    self._info_text = [('Server:  % 16d FPS' % self.server_fps), '', ('Vehicle: % 20s' % get_actor_display_name(world.vehicle, truncate=20)), ('Map:     % 20s' % world.world.get_map().name), ('Simulation time: % 12s' % datetime.timedelta(seconds=int(self.simulation_time))), '', ('Speed:   % 15.0f km/h' % (3.6 * math.sqrt((((v.x ** 2) + (v.y ** 2)) + (v.z ** 2))))), (u'Heading:% 16.0f° % 2s' % (t.rotation.yaw, heading)), ('Location:% 20s' % ('(% 5.1f, % 5.1f)' % (t.location.x, t.location.y))), ('Height:  % 18.0f m' % t.location.z), '', ('Throttle:', c.throttle, 0.0, 1.0), ('Steer:', c.steer, (- 1.0), 1.0), ('Brake:', c.brake, 0.0, 1.0), ('Reverse:', c.reverse), ('Hand brake:', c.hand_brake), ('Manual:', c.manual_gear_shift), ('Gear:        %s' % {(- 1): 'R', 0: 'N'}.get(c.gear, c.gear)), '', 'Collision:', collision, '', ('Number of vehicles: % 8d' % len(vehicles))]
    if (len(vehicles) > 1):
        self._info_text += ['Nearby vehicles:']
        distance = (lambda l: math.sqrt(((((l.x - t.location.x) ** 2) + ((l.y - t.location.y) ** 2)) + ((l.z - t.location.z) ** 2))))
        vehicles = [(distance(x.get_location()), x) for x in vehicles if (x.id != world.vehicle.id)]
        for (d, vehicle) in sorted(vehicles):
            if (d > 200.0):
                break
            vehicle_type = get_actor_display_name(vehicle, truncate=22)
            self._info_text.append(('% 4dm %s' % (d, vehicle_type)))
    self._notifications.tick(world, clock)
