import numpy as np
import cv2
from ...utils.argtools import shape2d
from ...utils.develop import log_deprecated
from .base import ImageAugmentor, ImagePlaceholder
from .transform import CropTransform, TransformList, ResizeTransform, PhotometricTransform
from .misc import ResizeShortestEdge


def _get_cutout_shape(self):
    if isinstance(self.h_range, int):
        h = self.h_range
    else:
        h = self.rng.randint(self.h_range)
    if isinstance(self.w_range, int):
        w = self.w_range
    else:
        w = self.rng.randint(self.w_range)
    return (h, w)
