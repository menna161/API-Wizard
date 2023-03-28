import numpy as np
import cv2
from .base import PhotometricAugmentor


def _get_augment_params(self, img):
    return self.rng.randint(*self.quality_range)
