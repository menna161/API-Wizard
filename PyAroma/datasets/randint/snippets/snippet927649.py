import sys, math
import numpy as np
import Box2D
from Box2D.b2 import edgeShape, circleShape, fixtureDef, polygonShape, revoluteJointDef, contactListener
import gym
from gym import spaces
from gym.utils import colorize, seeding
from gym.envs.classic_control import rendering


def _generate_terrain(self, hardcore):
    (GRASS, STUMP, STAIRS, PIT, _STATES_) = range(5)
    state = GRASS
    velocity = 0.0
    y = TERRAIN_HEIGHT
    counter = TERRAIN_STARTPAD
    oneshot = False
    self.terrain = []
    self.terrain_x = []
    self.terrain_y = []
    for i in range(TERRAIN_LENGTH):
        x = (i * TERRAIN_STEP)
        self.terrain_x.append(x)
        if ((state == GRASS) and (not oneshot)):
            velocity = ((0.8 * velocity) + (0.01 * np.sign((TERRAIN_HEIGHT - y))))
            if (i > TERRAIN_STARTPAD):
                velocity += (self.np_random.uniform((- 1), 1) / SCALE)
            y += velocity
        elif ((state == PIT) and oneshot):
            counter = self.np_random.randint(3, 5)
            poly = [(x, y), ((x + TERRAIN_STEP), y), ((x + TERRAIN_STEP), (y - (4 * TERRAIN_STEP))), (x, (y - (4 * TERRAIN_STEP)))]
            self.fd_polygon.shape.vertices = poly
            t = self.world.CreateStaticBody(fixtures=self.fd_polygon)
            (t.color1, t.color2) = ((1, 1, 1), (0.6, 0.6, 0.6))
            self.terrain.append(t)
            self.fd_polygon.shape.vertices = [((p[0] + (TERRAIN_STEP * counter)), p[1]) for p in poly]
            t = self.world.CreateStaticBody(fixtures=self.fd_polygon)
            (t.color1, t.color2) = ((1, 1, 1), (0.6, 0.6, 0.6))
            self.terrain.append(t)
            counter += 2
            original_y = y
        elif ((state == PIT) and (not oneshot)):
            y = original_y
            if (counter > 1):
                y -= (4 * TERRAIN_STEP)
        elif ((state == STUMP) and oneshot):
            counter = self.np_random.randint(1, 3)
            poly = [(x, y), ((x + (counter * TERRAIN_STEP)), y), ((x + (counter * TERRAIN_STEP)), (y + (counter * TERRAIN_STEP))), (x, (y + (counter * TERRAIN_STEP)))]
            self.fd_polygon.shape.vertices = poly
            t = self.world.CreateStaticBody(fixtures=self.fd_polygon)
            (t.color1, t.color2) = ((1, 1, 1), (0.6, 0.6, 0.6))
            self.terrain.append(t)
        elif ((state == STAIRS) and oneshot):
            stair_height = ((+ 1) if (self.np_random.rand() > 0.5) else (- 1))
            stair_width = self.np_random.randint(4, 5)
            stair_steps = self.np_random.randint(3, 5)
            original_y = y
            for s in range(stair_steps):
                poly = [((x + ((s * stair_width) * TERRAIN_STEP)), (y + ((s * stair_height) * TERRAIN_STEP))), ((x + (((1 + s) * stair_width) * TERRAIN_STEP)), (y + ((s * stair_height) * TERRAIN_STEP))), ((x + (((1 + s) * stair_width) * TERRAIN_STEP)), (y + (((- 1) + (s * stair_height)) * TERRAIN_STEP))), ((x + ((s * stair_width) * TERRAIN_STEP)), (y + (((- 1) + (s * stair_height)) * TERRAIN_STEP)))]
                self.fd_polygon.shape.vertices = poly
                t = self.world.CreateStaticBody(fixtures=self.fd_polygon)
                (t.color1, t.color2) = ((1, 1, 1), (0.6, 0.6, 0.6))
                self.terrain.append(t)
            counter = (stair_steps * stair_width)
        elif ((state == STAIRS) and (not oneshot)):
            s = (((stair_steps * stair_width) - counter) - stair_height)
            n = (s / stair_width)
            y = (original_y + ((n * stair_height) * TERRAIN_STEP))
        oneshot = False
        self.terrain_y.append(y)
        counter -= 1
        if (counter == 0):
            counter = self.np_random.randint((TERRAIN_GRASS / 2), TERRAIN_GRASS)
            if ((state == GRASS) and hardcore):
                state = self.np_random.randint(1, _STATES_)
                oneshot = True
            else:
                state = GRASS
                oneshot = True
    self.terrain_poly = []
    for i in range((TERRAIN_LENGTH - 1)):
        poly = [(self.terrain_x[i], self.terrain_y[i]), (self.terrain_x[(i + 1)], self.terrain_y[(i + 1)])]
        self.fd_edge.shape.vertices = poly
        t = self.world.CreateStaticBody(fixtures=self.fd_edge)
        color = (0.3, (1.0 if ((i % 2) == 0) else 0.8), 0.3)
        t.color1 = color
        t.color2 = color
        self.terrain.append(t)
        color = (0.4, 0.6, 0.3)
        poly += [(poly[1][0], 0), (poly[0][0], 0)]
        self.terrain_poly.append((poly, color))
    self.terrain.reverse()
