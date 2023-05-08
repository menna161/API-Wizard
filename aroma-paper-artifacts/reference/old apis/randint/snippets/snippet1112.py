import pygame
import random
import os
import numpy as np
import gym
from gym import error, spaces, utils
from gym.utils import seeding
from gym.envs.registration import register


def _generate_maze(self):
    self.maze_cells = np.zeros(self.maze_size, dtype=int)
    current_cell = (random.randint(0, (self.MAZE_W - 1)), random.randint(0, (self.MAZE_H - 1)))
    num_cells_visited = 1
    cell_stack = [current_cell]
    while cell_stack:
        current_cell = cell_stack.pop()
        (x0, y0) = current_cell
        neighbours = dict()
        for (dir_key, dir_val) in self.COMPASS.items():
            x1 = (x0 + dir_val[0])
            y1 = (y0 + dir_val[1])
            if ((0 <= x1 < self.MAZE_W) and (0 <= y1 < self.MAZE_H)):
                if self.all_walls_intact(self.maze_cells[(x1, y1)]):
                    neighbours[dir_key] = (x1, y1)
        if neighbours:
            dir = random.choice(tuple(neighbours.keys()))
            (x1, y1) = neighbours[dir]
            self.maze_cells[(x1, y1)] = self.__break_walls(self.maze_cells[(x1, y1)], self.__get_opposite_wall(dir))
            cell_stack.append(current_cell)
            cell_stack.append((x1, y1))
            num_cells_visited += 1
    if self.has_loops:
        self.__break_random_walls(0.2)
