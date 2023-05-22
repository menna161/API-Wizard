import numpy as np
import cv2
from ...utils.argtools import shape2d
from ...utils.develop import log_deprecated
from .base import ImageAugmentor, ImagePlaceholder
from .transform import CropTransform, TransformList, ResizeTransform, PhotometricTransform
from .misc import ResizeShortestEdge


def get_transform(self, img):
    orig_shape = img.shape
    assert ((orig_shape[0] >= self.crop_shape[0]) and (orig_shape[1] >= self.crop_shape[1])), orig_shape
    diffh = (orig_shape[0] - self.crop_shape[0])
    h0 = self.rng.randint((diffh + 1))
    diffw = (orig_shape[1] - self.crop_shape[1])
    w0 = self.rng.randint((diffw + 1))
    return CropTransform(h0, w0, self.crop_shape[0], self.crop_shape[1])
