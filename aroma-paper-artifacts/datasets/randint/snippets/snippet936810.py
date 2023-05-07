import torch
from torchvision import transforms
import cv2
import numpy as np
from numpy import random


def __call__(self, image, img_meta, tubes, labels, start_frame):
    if random.randint(2):
        swap = self.perms[random.randint(len(self.perms))]
        shuffle = SwapChannels(swap)
        for i in range(len(image)):
            image[i] = shuffle(image[i])
    return (image, img_meta, tubes, labels, start_frame)
