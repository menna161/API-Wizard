import numpy as np
import random
import json
import sys
import config
from env import make_env
import time
import os
import ann
import argparse
from gym.wrappers import Monitor
import imageio


def make_model(game):
    model = Model(game)
    return model
