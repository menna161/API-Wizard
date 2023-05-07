import os
import time
import numpy as np
import torch
from PIL import Image
from datasets.cityscapes_Dataset import name_classes


def add_batch(self, gt_image, pre_image):
    assert (gt_image.shape == pre_image.shape)
    self.confusion_matrix += self.__generate_matrix(gt_image, pre_image)
