import random
import math
import numbers
import collections
import numpy as np
import torch
from PIL import Image, ImageOps
import accimage


def randomize_parameters(self):
    if self.randomize:
        self.crop_position = self.crop_positions[random.randint(0, (len(self.crop_positions) - 1))]
