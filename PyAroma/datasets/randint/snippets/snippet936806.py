import torch
from torchvision import transforms
import cv2
import numpy as np
from numpy import random


def __call__(self, image, img_meta, tubes, labels, start_frame):
    if random.randint(2):
        alpha = random.uniform(self.lower, self.upper)
        image[(:, :, :, 1)] = (image[(:, :, :, 1)] * alpha)
    return (image, img_meta, tubes, labels, start_frame)
