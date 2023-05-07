import os
import time
import numpy as np
import torch
from PIL import Image
from datasets.cityscapes_Dataset import name_classes


def __init__(self, num_class):
    self.num_class = num_class
    self.confusion_matrix = np.zeros(((self.num_class,) * 2))
    self.ignore_index = None
    self.synthia = (True if (num_class == 16) else False)
