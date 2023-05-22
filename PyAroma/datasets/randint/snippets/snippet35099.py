import cv2
import numpy as np


def __call__(self, img, mask=None, label=None):
    (h, w) = (img.shape[0], img.shape[1])
    (xmin, ymin) = (int((w * self.range_w[0])), int((h * self.range_h[0])))
    (xmax, ymax) = (int((w * self.range_w[1])), int((h * self.range_h[1])))
    x_start = np.random.randint(xmin, xmax)
    y_start = np.random.randint(ymin, ymax)
    x1 = max((x_start - self.size), 0)
    y1 = max((y_start - self.size), 0)
    x2 = min((x_start + self.size), w)
    y2 = min((y_start + self.size), h)
    img = img[(y1:y2, x1:x2, :)]
    if (mask is not None):
        mask = mask[(y1:y2, x1:x2, :)]
        return (img, mask, label)
    else:
        return (img, label)
