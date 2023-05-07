import cv2
import numpy as np


def __call__(self, img, mask=None, label=None):
    if (np.random.uniform(0, 1) < self.p):
        attempts = np.random.randint(1, 3)
        for attempt in range(attempts):
            area = (img.shape[0] * img.shape[1])
            target_area = (np.random.uniform(self.area[0], self.area[1]) * area)
            aspect_ratio = np.random.uniform(0.5, 2)
            h = int(round(np.sqrt((target_area * aspect_ratio))))
            w = int(round(np.sqrt((target_area / aspect_ratio))))
            if ((w < img.shape[1]) and (h < img.shape[0])):
                x1 = np.random.randint(0, (img.shape[0] - h))
                y1 = np.random.randint(0, (img.shape[1] - w))
                img[(x1:(x1 + h), y1:(y1 + w), :)] = self.mean
    if (mask is not None):
        return (img, mask, label)
    else:
        return (img, label)
