import os
import time
import numpy as np
import torch
from PIL import Image
from datasets.cityscapes_Dataset import name_classes


def Pixel_Accuracy(self):
    if (np.sum(self.confusion_matrix) == 0):
        print('Attention: pixel_total is zero!!!')
        PA = 0
    else:
        PA = (np.diag(self.confusion_matrix).sum() / self.confusion_matrix.sum())
    return PA
