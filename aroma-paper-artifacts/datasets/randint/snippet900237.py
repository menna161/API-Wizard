import math
import numbers
import random
import numpy as np
from PIL import Image, ImageOps, ImageChops


def __call__(self, img, mask):
    if (self.padding > 0):
        img = ImageOps.expand(img, border=self.padding, fill=0)
        mask = ImageOps.expand(mask, border=self.padding, fill=0)
    assert (img.size == mask.size)
    (w, h) = img.size
    (th, tw) = self.size
    if ((w == tw) and (h == th)):
        return (img, mask)
    if ((w < tw) or (h < th)):
        return (img.resize((tw, th), Image.BILINEAR), mask.resize((tw, th), Image.NEAREST))
    x1 = random.randint(0, (w - tw))
    y1 = random.randint(0, (h - th))
    return (img.crop((x1, y1, (x1 + tw), (y1 + th))), mask.crop((x1, y1, (x1 + tw), (y1 + th))))
