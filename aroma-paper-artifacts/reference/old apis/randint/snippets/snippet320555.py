import numpy as np
import sys
import random
import pygame
from .amazing_brick_utils import CONST, load, Box, Player, Block, pipes
import pygame.surfarray as surfarray
from pygame.locals import *


def _getRandomPipe(self, init=False):
    if ((self.score % 5) == 4):
        self.color_ind = ((self.color_ind + 1) % 5)
    gap_left_topXs = list(range(100, 190, 20))
    if init:
        index = random.randint(0, (len(gap_left_topXs) - 1))
        x = gap_left_topXs[index]
        y = ((CONST['SCREEN_HEIGHT'] / 2) - (CONST['PIPE_WIDTH'] / 2))
        first_pipes = pipes(x, y, self.color_ind)
        self.pipes.append(first_pipes[0])
        self.pipes.append(first_pipes[1])
        self._addBlocks()
    index = random.randint(0, (len(gap_left_topXs) - 1))
    x = (self.s_c.x + gap_left_topXs[index])
    y = (self.pipes[(- 1)].y - (CONST['SCREEN_HEIGHT'] / 2))
    pipe = pipes(x, y, self.color_ind)
    self.pipes.append(pipe[0])
    self.pipes.append(pipe[1])
    self._addBlocks()
