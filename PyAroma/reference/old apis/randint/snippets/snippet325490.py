import numpy as np
import matplotlib.pyplot as plt
import os
import random
from PIL import Image
from PIL import ImageFilter


def crop(self, lr, hr):
    hr_crop_size = self.crop_size
    lr_crop_size = (hr_crop_size // self.scale)
    lr_w = np.random.randint(((lr.size[0] - lr_crop_size) + 1))
    lr_h = np.random.randint(((lr.size[1] - lr_crop_size) + 1))
    hr_w = (lr_w * self.scale)
    hr_h = (lr_h * self.scale)
    lr = lr.crop([lr_w, lr_h, (lr_w + lr_crop_size), (lr_h + lr_crop_size)])
    hr = hr.crop([hr_w, hr_h, (hr_w + hr_crop_size), (hr_h + hr_crop_size)])
    return (lr, hr)
