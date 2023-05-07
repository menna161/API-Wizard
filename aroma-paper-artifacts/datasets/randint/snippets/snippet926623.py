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
import os
import cv2


def render(self, mode='human'):
    assert (mode in ['human', 'state_pixels', 'rgb_array'])
    if (self.viewer is None):
        from gym.envs.classic_control import rendering
        self.viewer = rendering.Viewer(WINDOW_W, WINDOW_H)
        self.score_label = pyglet.text.Label('0000', font_size=36, x=20, y=((WINDOW_H * 2.5) / 40.0), anchor_x='left', anchor_y='center', color=(255, 255, 255, 255))
        self.transform = rendering.Transform()
    if ('t' not in self.__dict__):
        return
    zoom = (((0.1 * SCALE) * max((1 - self.t), 0)) + ((ZOOM * SCALE) * min(self.t, 1)))
    zoom_state = (((ZOOM * SCALE) * STATE_W) / WINDOW_W)
    zoom_video = (((ZOOM * SCALE) * VIDEO_W) / WINDOW_W)
    scroll_x = self.car.hull.position[0]
    scroll_y = self.car.hull.position[1]
    angle = (- self.car.hull.angle)
    vel = self.car.hull.linearVelocity
    if (np.linalg.norm(vel) > 0.5):
        angle = math.atan2(vel[0], vel[1])
    self.transform.set_scale(zoom, zoom)
    self.transform.set_translation(((WINDOW_W / 2) - (((scroll_x * zoom) * math.cos(angle)) - ((scroll_y * zoom) * math.sin(angle)))), ((WINDOW_H / 4) - (((scroll_x * zoom) * math.sin(angle)) + ((scroll_y * zoom) * math.cos(angle)))))
    self.transform.set_rotation(angle)
    self.car.draw(self.viewer, (mode != 'state_pixels'))
    arr = None
    win = self.viewer.window
    win.switch_to()
    win.dispatch_events()
    win.clear()
    t = self.transform
    if (mode == 'rgb_array'):
        VP_W = VIDEO_W
        VP_H = VIDEO_H
    elif (mode == 'state_pixels'):
        VP_W = STATE_W
        VP_H = STATE_H
    else:
        pixel_scale = 1
        if hasattr(win.context, '_nscontext'):
            pixel_scale = win.context._nscontext.view().backingScaleFactor()
        VP_W = int((pixel_scale * WINDOW_W))
        VP_H = int((pixel_scale * WINDOW_H))
    gl.glViewport(0, 0, VP_W, VP_H)
    t.enable()
    self.render_road()
    for geom in self.viewer.onetime_geoms:
        geom.render()
    self.viewer.onetime_geoms = []
    t.disable()
    self.render_indicators(WINDOW_W, WINDOW_H)
    if (mode == 'human'):
        win.flip()
        return self.viewer.isopen
    image_data = pyglet.image.get_buffer_manager().get_color_buffer().get_image_data()
    arr = np.fromstring(image_data.data, dtype=np.uint8, sep='')
    arr = arr.reshape(VP_H, VP_W, 4)
    arr = arr[(::(- 1), :, 0:3)]
    return arr
    if (VP_W == 96):
        self.step_cnt += 1
    if (self.step_cnt > 1):
        import os
        import cv2
        mask = np.zeros([VP_H, VP_W], dtype=bool)
        mask[((arr[(:, :, 1)] == 204) | (arr[(:, :, 1)] == 230))] = True
        rand_noise = np.random.randint(0, 256, ((VP_W * VP_H) * 3))
        rand_noise = rand_noise.reshape([VP_H, VP_W, 3])
        for i in range(3):
            arr[(:, :, i)][mask] = rand_noise[(:, :, i)][mask]
        self.step_cnt += 1
    return arr
