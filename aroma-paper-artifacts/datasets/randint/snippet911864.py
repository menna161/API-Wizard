import cv2
import random
import numpy as np
import torch
from torch.utils.data import Dataset


def load_mosaic_image_and_boxes(self, index, imsize=1024):
    '\n        This implementation of mosaic author:  https://www.kaggle.com/nvnnghia\n        Refactoring and adaptation: https://www.kaggle.com/shonenkov\n        '
    (w, h) = (imsize, imsize)
    s = (imsize // 2)
    (xc, yc) = [int(random.uniform((imsize * 0.25), (imsize * 0.75))) for _ in range(2)]
    indexes = ([index] + [random.randint(0, (self.image_ids.shape[0] - 1)) for _ in range(3)])
    result_image = np.full((imsize, imsize, 3), 1, dtype=np.float32)
    result_boxes = []
    for (i, index) in enumerate(indexes):
        (image, boxes) = self.load_image_and_boxes(index)
        if (i == 0):
            (x1a, y1a, x2a, y2a) = (max((xc - w), 0), max((yc - h), 0), xc, yc)
            (x1b, y1b, x2b, y2b) = ((w - (x2a - x1a)), (h - (y2a - y1a)), w, h)
        elif (i == 1):
            (x1a, y1a, x2a, y2a) = (xc, max((yc - h), 0), min((xc + w), (s * 2)), yc)
            (x1b, y1b, x2b, y2b) = (0, (h - (y2a - y1a)), min(w, (x2a - x1a)), h)
        elif (i == 2):
            (x1a, y1a, x2a, y2a) = (max((xc - w), 0), yc, xc, min((s * 2), (yc + h)))
            (x1b, y1b, x2b, y2b) = ((w - (x2a - x1a)), 0, max(xc, w), min((y2a - y1a), h))
        elif (i == 3):
            (x1a, y1a, x2a, y2a) = (xc, yc, min((xc + w), (s * 2)), min((s * 2), (yc + h)))
            (x1b, y1b, x2b, y2b) = (0, 0, min(w, (x2a - x1a)), min((y2a - y1a), h))
        result_image[(y1a:y2a, x1a:x2a)] = image[(y1b:y2b, x1b:x2b)]
        padw = (x1a - x1b)
        padh = (y1a - y1b)
        boxes[(:, 0)] += padw
        boxes[(:, 1)] += padh
        boxes[(:, 2)] += padw
        boxes[(:, 3)] += padh
        result_boxes.append(boxes)
    result_boxes = np.concatenate(result_boxes, 0)
    np.clip(result_boxes[(:, 0:)], 0, (2 * s), out=result_boxes[(:, 0:)])
    result_boxes = result_boxes.astype(np.int32)
    result_boxes = result_boxes[np.where((((result_boxes[(:, 2)] - result_boxes[(:, 0)]) * (result_boxes[(:, 3)] - result_boxes[(:, 1)])) > 0))]
    return (result_image, result_boxes)
