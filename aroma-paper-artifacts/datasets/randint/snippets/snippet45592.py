import torch
from torchvision import transforms
import cv2
import numpy as np
import types
from numpy import random
from matplotlib import pyplot as plt
from PIL import Image, ImageOps


def __call__(self, image, boxes, labels):
    im = image.copy()
    (im, boxes, labels) = self.rand_brightness(im, boxes, labels)
    if random.randint(2):
        distort = Compose(self.pd[:(- 1)])
    else:
        distort = Compose(self.pd[1:])
    (im, boxes, labels) = distort(im, boxes, labels)
    return self.rand_light_noise(im, boxes, labels)
