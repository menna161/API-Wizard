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


def game_loop(args, agent):
    pygame.init()
    pygame.font.init()
    world = None
    try:
        client = carla.Client(args.host, args.port)
        client.set_timeout(4.0)
        display = pygame.display.set_mode((args.width, args.height), (pygame.HWSURFACE | pygame.DOUBLEBUF))
        if (args.output_folder is not None):
            if (not os.path.exists(args.output_folder)):
                os.mkdir(args.output_folder)
        hud = HUD(args.width, args.height)
        world = World(client.get_world(), hud)
        controller = KeyboardControl(world, False)
        print('###########################################################\n   CONDITIONAL IMITATION LEARNING VISUALIZATION SYSTEM \n    ON THE BOTTOM CORNER WE SHOW THE FIRST PERSON VIEW \n        AND THE ACTIVATIONS OF THE FIRST 3 LAYERS \n \n Use ARROWS  keys to give high level commands to the Agent\n###########################################################\n')
        spawn_point = world.world.get_map().get_spawn_points()[random.randint(0, 40)]
        clock = pygame.time.Clock()
        while True:
            if controller.parse_events(world, clock):
                return
            if (not world.world.wait_for_tick(20.0)):
                continue
            world.tick(clock)
            sensor_data = world.get_agent_sensor()
            world.render(display)
            pygame.display.flip()
            control = agent.run_step(world.get_forward_speed(), sensor_data, controller.get_command(), (spawn_point.location.x, spawn_point.location.y, spawn_point.location.z))
            attentions = agent.get_attentions()
            world.camera_manager.show_image_mini(agent.latest_image, attentions[0], attentions[1], attentions[2], out_folder=args.output_folder)
            world.vehicle.apply_control(control)
    finally:
        if (world is not None):
            world.destroy()
        pygame.quit()
