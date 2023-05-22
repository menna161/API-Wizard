import torch
from torchvision import transforms
import cv2
import numpy as np
from numpy import random


def __call__(self, images, img_meta, tubes, labels, start_frame):
    images = images.copy()
    (images, img_meta, tubes, labels, start_frame) = self.rand_brightness(images, img_meta, tubes, labels, start_frame)
    if random.randint(2):
        distort = Compose(self.pd[:(- 1)])
    else:
        distort = Compose(self.pd[1:])
    (images, img_meta, tubes, labels, start_frame) = distort(images, img_meta, tubes, labels, start_frame)
    return self.rand_light_noise(images, img_meta, tubes, labels, start_frame)
