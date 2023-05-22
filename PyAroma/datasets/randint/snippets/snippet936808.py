import torch
from torchvision import transforms
import cv2
import numpy as np
from numpy import random


def __call__(self, image, img_meta, tubes, labels, start_frame):
    if random.randint(2):
        delta = random.uniform((- self.delta), self.delta)
        image[(:, :, :, 0)] = (image[(:, :, :, 0)] + delta)
        image[(:, :, :, 0)][(image[(:, :, :, 0)] > 360.0)] -= 360.0
        image[(:, :, :, 0)][(image[(:, :, :, 0)] < 0.0)] += 360.0
    return (image, img_meta, tubes, labels, start_frame)
