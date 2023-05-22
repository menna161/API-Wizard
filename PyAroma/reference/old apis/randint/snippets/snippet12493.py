import numpy as np
import cv2
from ...utils.argtools import log_once
from .base import ImageAugmentor, _default_repr

if (__name__ == '__main__'):
    shape = (100, 100)
    center = (10, 70)
    mat = cv2.getRotationMatrix2D(center, 20, 1)
    trans = WarpAffineTransform(mat, (130, 130))

    def draw_points(img, pts):
        for p in pts:
            try:
                img[(int(p[1]), int(p[0]))] = 0
            except IndexError:
                pass
    image = cv2.imread('cat.jpg')
    image = cv2.resize(image, shape)
    orig_image = image.copy()
    coords = np.random.randint(100, size=(20, 2))
    draw_points(orig_image, coords)
    print(coords)
    for _ in range(1):
        coords = trans.apply_coords(coords)
        image = trans.apply_image(image)
    print(coords)
    draw_points(image, coords)
    orig_image = cv2.resize(orig_image, (600, 600))
    image = cv2.resize(image, (600, 600))
    viz = np.concatenate((orig_image, image), axis=1)
    cv2.imshow('mat', viz)
    cv2.waitKey()
