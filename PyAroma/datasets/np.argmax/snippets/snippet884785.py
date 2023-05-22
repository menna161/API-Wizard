import argparse
import gc
import os
import random
import traceback
from multiprocessing import Pool, Process
import numpy as np
import tensorflow.compat.v1 as tf
import api
import board
import config
import gui
import net
import tree
from util import log, plane_2_line


def pick_move_probabilistically(pi):
    r = random.random()
    s = 0
    for move in range(len(pi)):
        s += pi[move]
        if (s >= r):
            return move
    return np.argmax(pi)
