import os
import time
import numpy as np
import torch
from PIL import Image
from datasets.cityscapes_Dataset import name_classes


def __generate_matrix(self, gt_image, pre_image):
    mask = ((gt_image >= 0) & (gt_image < self.num_class))
    label = ((self.num_class * gt_image[mask].astype('int')) + pre_image[mask])
    count = np.bincount(label, minlength=(self.num_class ** 2))
    confusion_matrix = count.reshape(self.num_class, self.num_class)
    return confusion_matrix
