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
        swap = self.perms[random.randint(len(self.perms))]
        shuffle = SwapChannels(swap)
        image = shuffle(image)
    return (image, boxes, labels)
