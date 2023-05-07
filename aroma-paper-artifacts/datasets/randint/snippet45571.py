import torch
from torchvision import transforms
import cv2
import numpy as np
import types
from numpy import random
from matplotlib import pyplot as plt
from PIL import Image, ImageOps


def __call__(self, image, boxes=None, labels=None):
    if random.randint(2):
        image[(:, :, 1)] *= random.uniform(self.lower, self.upper)
    return (image, boxes, labels)
