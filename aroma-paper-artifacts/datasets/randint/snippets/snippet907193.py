import cv2
import numpy as np
import random


def __call__(self, data):
    (height, width) = data[0].shape[:2]
    (c_h, c_w) = self.crop_size
    assert ((height >= c_h) and (width >= c_w)), f'({height}, {width}) v.s. ({c_h}, {c_w})'
    left = random.randint(0, (width - c_w))
    top = random.randint(0, (height - c_h))
    data = [d[(top:(top + c_h), left:(left + c_w))] for d in data]
    return data
