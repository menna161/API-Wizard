import torch
from torchvision import transforms
import cv2
import numpy as np
from numpy import random


def __call__(self, images, img_meta, tubes, labels, start_frame):
    if random.randint(2):
        res = self.mirror(images, tubes)
        images = res[0]
        tubes = res[1]
    return (images, img_meta, tubes, labels, start_frame)
