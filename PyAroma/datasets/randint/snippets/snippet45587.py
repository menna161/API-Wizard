import torch
from torchvision import transforms
import cv2
import numpy as np
import types
from numpy import random
from matplotlib import pyplot as plt
from PIL import Image, ImageOps


def __call__(self, image, boxes, labels):
    if random.randint(2):
        return (image, boxes, labels)
    (height, width, depth) = image.shape
    ratio = random.uniform(1, 4)
    left = random.uniform(0, ((width * ratio) - width))
    top = random.uniform(0, ((height * ratio) - height))
    expand_image = np.zeros((int((height * ratio)), int((width * ratio)), depth), dtype=image.dtype)
    expand_image[(:, :, :)] = self.mean
    expand_image[(int(top):int((top + height)), int(left):int((left + width)))] = image
    image = expand_image
    boxes = boxes.copy()
    boxes[(:, :2)] += (int(left), int(top))
    boxes[(:, 2:)] += (int(left), int(top))
    return (image, boxes, labels)
