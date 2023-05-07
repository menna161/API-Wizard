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
        delta = random.uniform((- self.delta), self.delta)
        image += delta
    return (image, boxes, labels)
