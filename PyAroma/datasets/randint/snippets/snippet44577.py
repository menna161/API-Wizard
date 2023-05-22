import random
import math
import numbers
import collections
import numpy as np
import torch
from PIL import Image, ImageOps
import accimage


def randomize_parameters(self):
    self.scale = self.scales[random.randint(0, (len(self.scales) - 1))]
    self.tl_x = random.random()
    self.tl_y = random.random()
