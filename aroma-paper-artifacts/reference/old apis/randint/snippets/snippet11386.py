import numpy as np
import cv2
from ...utils.argtools import shape2d
from ...utils.develop import log_deprecated
from .base import ImageAugmentor, ImagePlaceholder
from .transform import CropTransform, TransformList, ResizeTransform, PhotometricTransform
from .misc import ResizeShortestEdge


def get_transform(self, img):
    hmax = (self.hmax or img.shape[0])
    wmax = (self.wmax or img.shape[1])
    h = self.rng.randint(self.hmin, (hmax + 1))
    w = self.rng.randint(self.wmin, (wmax + 1))
    diffh = (img.shape[0] - h)
    diffw = (img.shape[1] - w)
    assert ((diffh >= 0) and (diffw >= 0)), ((str(diffh) + ', ') + str(diffw))
    y0 = (0 if (diffh == 0) else self.rng.randint(diffh))
    x0 = (0 if (diffw == 0) else self.rng.randint(diffw))
    return CropTransform(y0, x0, h, w)
