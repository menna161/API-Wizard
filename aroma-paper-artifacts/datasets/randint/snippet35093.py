import cv2
import numpy as np


def __call__(self, img, mask=None, label=None):
    if (np.random.uniform(0, 1) < self.p):
        (h, w) = (img.shape[0], img.shape[1])
        (x, y) = (np.random.randint(w), np.random.randint(h))
        edge = (np.random.randint(1, self.max_edge) // 2)
        (x1, x2) = (np.clip((x - edge), 0, w), np.clip((x + edge), 0, w))
        (y1, y2) = (np.clip((y - edge), 0, h), np.clip((y + edge), 0, h))
        img[(y1:y2, x1:x2, :)] = 0
    if (mask is not None):
        return (img, mask, label)
    else:
        return (img, label)
