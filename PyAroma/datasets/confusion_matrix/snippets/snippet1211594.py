import os
import time
import numpy as np
import torch
from PIL import Image
from datasets.cityscapes_Dataset import name_classes


def reset(self):
    self.confusion_matrix = np.zeros(((self.num_class,) * 2))
