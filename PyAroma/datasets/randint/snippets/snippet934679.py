import os
import glob
import traceback
import collections
import sys
import math
import copy
import json
import random
import numpy as np
import torch
import cv2
from torch.utils.data import Dataset
from . import splitter
from . import data_parser
from configs import g_conf
from coilutils.general import sort_nicely


def augment_directions(self, directions):
    if (directions == 2.0):
        if (random.randint(0, 100) < 20):
            directions = random.choice([3.0, 4.0, 5.0])
    return directions
