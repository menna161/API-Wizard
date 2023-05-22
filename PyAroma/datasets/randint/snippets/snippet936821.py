import torch
from torchvision import transforms
import cv2
import numpy as np
from numpy import random


def __call__(self, images, img_meta, tubes, labels, start_frame):
    if random.randint(2):
        return (images, img_meta, tubes, labels, start_frame)
    (frames, height, width, depth) = images.shape
    ratio = random.uniform(1, 1.2)
    left = random.uniform(0, ((width * ratio) - width))
    top = random.uniform(0, ((height * ratio) - height))
    images = self.expand(images, frames, height, width, depth, ratio, left, top)
    img_meta['img_shape'] = [img_meta['img_shape'][0], images.shape[1], images.shape[2]]
    tubes = tubes.copy()
    tubes[(:, [0, 1, 2, 3])] += (int(left), int(top), int(left), int(top))
    return (images, img_meta, tubes, labels, start_frame)
