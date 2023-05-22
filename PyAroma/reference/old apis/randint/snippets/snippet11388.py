import numpy as np
import cv2
from ...utils.argtools import shape2d
from ...utils.develop import log_deprecated
from .base import ImageAugmentor, ImagePlaceholder
from .transform import CropTransform, TransformList, ResizeTransform, PhotometricTransform
from .misc import ResizeShortestEdge


def get_transform(self, img):
    (h, w) = img.shape[:2]
    area = (h * w)
    for _ in range(10):
        targetArea = (self.rng.uniform(*self.crop_area_fraction) * area)
        aspectR = self.rng.uniform(*self.aspect_ratio_range)
        ww = int((np.sqrt((targetArea * aspectR)) + 0.5))
        hh = int((np.sqrt((targetArea / aspectR)) + 0.5))
        if (self.rng.uniform() < 0.5):
            (ww, hh) = (hh, ww)
        if ((hh <= h) and (ww <= w)):
            x1 = self.rng.randint(0, ((w - ww) + 1))
            y1 = self.rng.randint(0, ((h - hh) + 1))
            return TransformList([CropTransform(y1, x1, hh, ww), ResizeTransform(hh, ww, self.target_shape, self.target_shape, interp=self.interp)])
    resize = ResizeShortestEdge(self.target_shape, interp=self.interp).get_transform(img)
    out_shape = (resize.new_h, resize.new_w)
    crop = CenterCrop(self.target_shape).get_transform(ImagePlaceholder(shape=out_shape))
    return TransformList([resize, crop])
