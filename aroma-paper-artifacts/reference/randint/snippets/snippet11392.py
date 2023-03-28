import numpy as np
import cv2
from ...utils.argtools import shape2d
from ...utils.develop import log_deprecated
from .base import ImageAugmentor, ImagePlaceholder
from .transform import CropTransform, TransformList, ResizeTransform, PhotometricTransform
from .misc import ResizeShortestEdge


def get_transform(self, img):
    (h, w) = self._get_cutout_shape()
    x0 = self.rng.randint(0, ((img.shape[1] + 1) - w))
    y0 = self.rng.randint(0, ((img.shape[0] + 1) - h))
    return PhotometricTransform((lambda img: RandomCutout._cutout(img, y0, x0, h, w, self.fill)), 'cutout')
