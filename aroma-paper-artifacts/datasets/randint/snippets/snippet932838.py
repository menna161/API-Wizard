from __future__ import absolute_import
from torchvision.transforms import *
from PIL import Image
import random, math


def __call__(self, img):
    for attempt in range(10):
        area = (img.size[0] * img.size[1])
        target_area = (random.uniform(0.64, 1.0) * area)
        aspect_ratio = random.uniform(2, 3)
        h = int(round(math.sqrt((target_area * aspect_ratio))))
        w = int(round(math.sqrt((target_area / aspect_ratio))))
        if ((w <= img.size[0]) and (h <= img.size[1])):
            x1 = random.randint(0, (img.size[0] - w))
            y1 = random.randint(0, (img.size[1] - h))
            img = img.crop((x1, y1, (x1 + w), (y1 + h)))
            assert (img.size == (w, h))
            return img.resize((self.width, self.height), self.interpolation)
    scale = RectScale(self.height, self.width, interpolation=self.interpolation)
    return scale(img)
