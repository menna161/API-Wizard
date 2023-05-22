import cv2
import glob
import os
import sys, math
import numpy as np
import Box2D
from Box2D.b2 import edgeShape, circleShape, fixtureDef, polygonShape, revoluteJointDef, contactListener
import gym
from gym import spaces
from .car_dynamics import Car
from gym.utils import colorize, seeding, EzPickle
import pyglet
from pyglet import gl
from pyglet.window import key
from gym.wrappers.monitor import Monitor
from gym.envs.classic_control import rendering


def render_road(self):
    if (self._modification_type in ['noise', 'video']):
        H = W = int((PLAYFIELD * 2))
        if (self._modification_type == 'noise'):
            background = np.random.randint(0, 256, ((H * W) * 3)).reshape([H, W, 3])
            img_path = '/tmp/screen.png'
            cv2.imwrite(img_path, background)
        else:
            video_img_dir = os.environ.get('CARRACING_VIDEO_DIR', '/tmp/car_racing_video')
            max_steps = len(glob.glob(os.path.join(video_img_dir, '*.png')))
            img_path = os.path.join(video_img_dir, '{}.png'.format(((self.step_cnt + 1) % max_steps)))
        image = pyglet.image.load(img_path)
        image.anchor_x = (image.width // 2)
        image.anchor_y = (image.height // 2)
        s = pyglet.sprite.Sprite(image)
        s.draw()
    else:
        gl.glBegin(gl.GL_QUADS)
        gl.glColor4f(*self.grass_color)
        gl.glVertex3f((- PLAYFIELD), (+ PLAYFIELD), 0)
        gl.glVertex3f((+ PLAYFIELD), (+ PLAYFIELD), 0)
        gl.glVertex3f((+ PLAYFIELD), (- PLAYFIELD), 0)
        gl.glVertex3f((- PLAYFIELD), (- PLAYFIELD), 0)
        gl.glColor4f(0.4, 0.9, 0.4, 1.0)
        k = (PLAYFIELD / 20.0)
        for x in range((- 20), 20, 2):
            for y in range((- 20), 20, 2):
                gl.glVertex3f(((k * x) + k), ((k * y) + 0), 0)
                gl.glVertex3f(((k * x) + 0), ((k * y) + 0), 0)
                gl.glVertex3f(((k * x) + 0), ((k * y) + k), 0)
                gl.glVertex3f(((k * x) + k), ((k * y) + k), 0)
        gl.glEnd()
    gl.glBegin(gl.GL_QUADS)
    for (poly, color) in self.road_poly:
        gl.glColor4f(color[0], color[1], color[2], 1)
        for p in poly:
            gl.glVertex3f(p[0], p[1], 0)
    gl.glEnd()
