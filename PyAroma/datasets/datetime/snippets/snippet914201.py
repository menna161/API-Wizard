from __future__ import division
import argparse
import bz2
from datetime import datetime
import os
import pickle
import atari_py
import numpy as np
import torch
from tqdm import trange
from agent import Agent
from env import Env
from memory import ReplayMemory
from test import test


def log(s):
    print(((('[' + str(datetime.now().strftime('%Y-%m-%dT%H:%M:%S'))) + '] ') + s))
