import os
import random
import chainer
import numpy as np
import pandas as pd
from PIL import Image


def __init__(self, n_frames, root_path, config_path):
    self.conf = pd.read_pickle(config_path)
    self.n_frames = n_frames
    self.root_path = root_path
