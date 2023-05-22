import torch
from torchvision import transforms
import cv2
import numpy as np
import types
from numpy import random
from matplotlib import pyplot as plt
from PIL import Image, ImageOps


def __call__(self, image, boxes, classes):
    (_, width, _) = image.shape
    if random.randint(2):
        image = image[(:, ::(- 1))]
        boxes = boxes.copy()
        boxes[(:, 0::2)] = (width - boxes[(:, 2::(- 2))])
    return (image, boxes, classes)
