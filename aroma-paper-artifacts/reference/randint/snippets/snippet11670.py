import numpy as np
import cv2
from .base import PhotometricAugmentor


def _get_augment_params(self, _):
    (sx, sy) = self.rng.randint(self.max_size, size=(2,))
    sx = ((sx * 2) + 1)
    sy = ((sy * 2) + 1)
    return (sx, sy)
