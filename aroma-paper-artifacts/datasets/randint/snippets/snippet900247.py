import math
import numbers
import random
import numpy as np
from PIL import Image, ImageOps, ImageChops


def __call__(self, img, mask):
    assert (img.size == mask.size)
    for attempt in range(10):
        area = (img.size[0] * img.size[1])
        target_area = (random.uniform(0.45, 1.0) * area)
        aspect_ratio = random.uniform(0.5, 2)
        w = int(round(math.sqrt((target_area * aspect_ratio))))
        h = int(round(math.sqrt((target_area / aspect_ratio))))
        if (random.random() < 0.5):
            (w, h) = (h, w)
        if ((w <= img.size[0]) and (h <= img.size[1])):
            x1 = random.randint(0, (img.size[0] - w))
            y1 = random.randint(0, (img.size[1] - h))
            img = img.crop((x1, y1, (x1 + w), (y1 + h)))
            mask = mask.crop((x1, y1, (x1 + w), (y1 + h)))
            assert (img.size == (w, h))
            return (img.resize((self.size, self.size), Image.BILINEAR), mask.resize((self.size, self.size), Image.NEAREST))
    scale = Scale(self.size)
    crop = CenterCrop(self.size)
    return crop(*scale(img, mask))
